"""3D position-based particle liquid: gravity, density constraints, solid rocks.

An original CPU Taichi implementation following Macklin & Mueller, Position Based
Fluids (2013). Surface reconstruction is from simulated particles. Foam is an
empirical surface field driven by their velocity/curl. No image/footage motion.
"""
import json,math,os,time,traceback
from pathlib import Path
import numpy as np
import taichi as ti
from scipy.ndimage import gaussian_filter,map_coordinates
from skimage.measure import marching_cubes

ROOT=Path(__file__).resolve().parents[1];VARIANT=os.environ.get('FLUID_VARIANT','fluid_river');CACHE=ROOT/f'assets/{VARIANT}/meshes'
CACHE.mkdir(parents=True,exist_ok=True)
for p in [f'research/{VARIANT}',f'renders/{VARIANT}','logs/taichi_cache']:(ROOT/p).mkdir(parents=True,exist_ok=True)
CONFIG=json.loads((ROOT/f'assets/{VARIANT}/channel.json').read_text()) if (ROOT/f'assets/{VARIANT}/channel.json').exists() else None
CUSTOM=CONFIG is not None
ti.init(arch=ti.cpu,cpu_max_num_threads=4,default_fp=ti.f32,random_seed=4821,offline_cache_file_path=str(ROOT/'logs/taichi_cache'))
S=float(os.environ.get('PARTICLE_SPACING','.03'));H=S*(.095/.045);REST=1000.;MASS=REST*S**3;SUBSTEPS=8
SIMULATION_FPS=float(os.environ.get('SIMULATION_FPS','24'));assert SIMULATION_FPS>0
DT=1/(SIMULATION_FPS*SUBSTEPS);ITER=4;BOUNDS=np.array([2.4,5.8,2.4],np.float32)
if CUSTOM:BOUNDS=np.array(CONFIG['bounds_m'],np.float32)
GRID=tuple((np.ceil(BOUNDS/H).astype(int)+2).tolist());CAP=64;NEIGH=100
ROCKS=np.array([[.67,1.55,.91,.26,.24,.24],[1.68,2.27,.91,.29,.29,.27],[.65,2.83,.56,.32,.31,.25],[1.79,3.61,.50,.27,.27,.23],[.55,4.40,.30,.25,.32,.23],[1.66,4.94,.31,.29,.35,.20]],np.float32)
if CUSTOM:ROCKS=np.array(CONFIG['solid_ellipsoids'],np.float32)
def bed_np(y):
 def drop(a,b):
  t=np.clip((y-a)/(b-a),0,1);return 1-t*t*(3-2*t)
 return np.interp(y,np.arange(len(CONFIG['bed_profile_z']))*.01,CONFIG['bed_profile_z']) if CUSTOM else .18+.37*drop(1.35,1.7)+.28*drop(2.55,2.8)+.24*drop(3.7,4.)
def center_np(y):return np.interp(y,np.arange(len(CONFIG['center_profile_x']))*.01,CONFIG['center_profile_x']) if CUSTOM else 1.2
def half_np(y):return np.interp(y,np.arange(len(CONFIG['half_width_profile']))*.01,CONFIG['half_width_profile']) if CUSTOM else .75
initial=[]
for y in np.arange(.16,float(BOUNDS[1])-.32,S):
 for x in (np.arange(center_np(y)-half_np(y),center_np(y)+half_np(y),S) if CUSTOM else np.arange(.46,1.96,S)):
  for z in np.arange(S,.42 if CUSTOM else .228,S):
   p=np.array([x,y,float(bed_np(y))+z],np.float32)
   if all(np.linalg.norm((p-r[:3])/(r[3:]+.025))>1 for r in ROCKS):initial.append(p)
INITIAL=np.array(initial,np.float32);N=len(INITIAL)
if CUSTOM:ITER=6
p=ti.Vector.field(3,ti.f32,N);old=ti.Vector.field(3,ti.f32,N);v=ti.Vector.field(3,ti.f32,N);dp=ti.Vector.field(3,ti.f32,N);w=ti.Vector.field(3,ti.f32,N)
lam=ti.field(ti.f32,N);rho=ti.field(ti.f32,N);foam=ti.field(ti.f32,N);nc=ti.field(ti.i32,N);neighbors=ti.field(ti.i32,(N,NEIGH))
alive=ti.field(ti.i32,N);inlet_lock=ti.field(ti.i32,2048);step_count=ti.field(ti.i32,())
count=ti.field(ti.i32,GRID);grid=ti.field(ti.i32,(*GRID,CAP));overflow=ti.field(ti.i32,());rocks=ti.Vector.field(6,ti.f32,len(ROCKS));rocks.from_numpy(ROCKS)
PROFILE_COUNT=len(CONFIG['bed_profile_z']) if CUSTOM else 581
profile_bed=ti.field(ti.f32,PROFILE_COUNT);profile_center=ti.field(ti.f32,PROFILE_COUNT);profile_width=ti.field(ti.f32,PROFILE_COUNT)
if CUSTOM:
 profile_bed.from_numpy(np.array(CONFIG['bed_profile_z'],np.float32));profile_center.from_numpy(np.array(CONFIG['center_profile_x'],np.float32));profile_width.from_numpy(np.array(CONFIG['half_width_profile'],np.float32))
POLY=315/(64*math.pi*H**9);SPIKY=-45/(math.pi*H**6)
@ti.func
def kernel(r2):
 value=0.
 if r2<H*H:value=POLY*(H*H-r2)**3
 return value
@ti.func
def gradient(r):
 length=r.norm();value=ti.Vector([0.,0.,0.])
 if 1e-6<length<H:value=SPIKY*(H-length)**2/length*r
 return value
@ti.func
def drop(y,a,b):
 t=ti.min(1.,ti.max(0.,(y-a)/(b-a)));return 1-t*t*(3-2*t)
@ti.func
def profile(arr:ti.template(),y):
 index=ti.min(PROFILE_COUNT-2,ti.max(0,ti.cast(y*100,ti.i32)));blend=ti.min(1.,ti.max(0.,y*100-index));return arr[index]*(1-blend)+arr[index+1]*blend
@ti.func
def floor_z(q):
 z=.18+.37*drop(q.y,1.35,1.7)+.28*drop(q.y,2.55,2.8)+.24*drop(q.y,3.7,4.)+3*ti.max(0.,ti.abs(q.x-1.2)-.76)**2
 if ti.static(CUSTOM):z=profile(profile_bed,q.y)+8*ti.max(0.,ti.abs(q.x-profile(profile_center,q.y))-profile(profile_width,q.y))**2
 return z
@ti.func
def collide(q):
 a=q;a.x=ti.min(2.25,ti.max(.15,a.x));a.y=ti.max(.06,a.y)
 if ti.static(CUSTOM):
  for iteration in ti.static(range(4)):
   depth=floor_z(a)+.021-a.z
   if depth>0:
    dx=ti.Vector([.002,0.,0.]);dy=ti.Vector([0.,.002,0.]);gx=(floor_z(a+dx)-floor_z(a-dx))/.004;gy=(floor_z(a+dy)-floor_z(a-dy))/.004
    normal=ti.Vector([-gx,-gy,1.]);a+=normal*depth/(1+gx*gx+gy*gy)
 else:a.z=ti.max(a.z,floor_z(a)+.021)
 for k in ti.static(range(len(ROCKS))):
  r=rocks[k];c=ti.Vector([r[0],r[1],r[2]]);radius=ti.Vector([r[3]+.021,r[4]+.021,r[5]+.021]);d=(a-c)/radius;length=d.norm()
  if length<1.:a=c+d/ti.max(length,1e-5)*radius
 return a
@ti.func
def cell(q):
 c=ti.cast(q/H,ti.i32)
 return ti.Vector([ti.min(GRID[0]-1,ti.max(0,c.x)),ti.min(GRID[1]-1,ti.max(0,c.y)),ti.min(GRID[2]-1,ti.max(0,c.z))])
@ti.kernel
def initialize():
 for i in range(N):v[i]=ti.Vector([0.,1.35,0.]);foam[i]=0;alive[i]=1
@ti.kernel
def prepare_inlet():
 if ti.static(CUSTOM):
  for k in range(2048):inlet_lock[k]=0
  step_count[None]+=1
@ti.kernel
def predict():
 for i in range(N):
  q=p[i]
  if ti.static(CUSTOM):
   if alive[i]==1 and (q.y>BOUNDS[1]-.21 or q.z>2.30):alive[i]=0;q=ti.Vector([-1.,-1.,-1.]);v[i]=ti.Vector([0.,0.,0.]);foam[i]=0
   if alive[i]==0:
    slot=(i+step_count[None])%1092;ix=slot%26;iz=(slot//26)%14;layer=slot//364;yy=.075+layer*S+(step_count[None]*DT*1.35)%S
    candidate=ti.Vector([profile(profile_center,yy)+(ix-12.5)*S,yy,profile(profile_bed,yy)+(iz+1)*S]);free=ti.atomic_add(inlet_lock[slot],1)==0
    if candidate.z<floor_z(candidate)+.021:free=False
    c0=cell(candidate)
    for dx,dy,dz in ti.ndrange((-1,2),(-1,2),(-1,2)):
     c=c0+ti.Vector([dx,dy,dz])
     if 0<=c.x<GRID[0] and 0<=c.y<GRID[1] and 0<=c.z<GRID[2]:
      for k in range(ti.min(count[c],CAP)):
       j=grid[c.x,c.y,c.z,k]
       if alive[j]==1 and (p[j]-candidate).norm_sqr()<(.82*S)**2:free=False
    if free:q=candidate;alive[i]=1;v[i]=ti.Vector([0.,1.35,0.])
  else:
   if q.y>5.59 or q.z>2.30:q=ti.Vector([.48+ti.random()*1.42,.12+ti.random()*.65,1.12+ti.random()*.18]);v[i]=ti.Vector([.03*(ti.random()-.5),1.4,0]);foam[i]=0
  old[i]=q
  if alive[i]==1:v[i].z-=9.81*DT;p[i]=collide(q+v[i]*DT)
  else:p[i]=q
@ti.kernel
def build():
 for I in ti.grouped(count):count[I]=0
 overflow[None]=0
 for i in range(N):
  if alive[i]==1:
   c=cell(p[i]);k=ti.atomic_add(count[c],1)
   if k<CAP:grid[c.x,c.y,c.z,k]=i
   else:ti.atomic_add(overflow[None],1)
@ti.kernel
def find_neighbors():
 for i in range(N):
  center=cell(p[i]);n=0
  for dx,dy,dz in ti.ndrange((-1,2),(-1,2),(-1,2)):
   c=center+ti.Vector([dx,dy,dz])
   if 0<=c.x<GRID[0] and 0<=c.y<GRID[1] and 0<=c.z<GRID[2]:
    for k in range(ti.min(count[c],CAP)):
     j=grid[c.x,c.y,c.z,k]
     if j!=i and (p[i]-p[j]).norm_sqr()<H*H:
      if n<NEIGH:neighbors[i,n]=j
      n+=1
  nc[i]=ti.min(n,NEIGH)
  if n>NEIGH:ti.atomic_add(overflow[None],n-NEIGH)
@ti.kernel
def pressure():
 for i in range(N):
  density=MASS*kernel(0.);squared=0.;total=ti.Vector([0.,0.,0.])
  for k in range(nc[i]):
   j=neighbors[i,k];r=p[i]-p[j];density+=MASS*kernel(r.norm_sqr());g=MASS/REST*gradient(r);squared+=g.norm_sqr();total+=g
  rho[i]=density;lam[i]=-ti.max(0.,density/REST-1.)/(squared+total.norm_sqr()+1e-3)
@ti.kernel
def displacement():
 for i in range(N):
  delta=ti.Vector([0.,0.,0.])
  for k in range(nc[i]):
   j=neighbors[i,k];r=p[i]-p[j];correction=-.000001*(kernel(r.norm_sqr())/kernel((.3*H)**2))**4
   delta+=(lam[i]+lam[j]+correction)*MASS/REST*gradient(r)
  limit=.012 if ti.static(CUSTOM) else .025
  dp[i]=delta*ti.min(1.,limit/ti.max(delta.norm(),1e-6))
@ti.kernel
def apply():
 for i in range(N):
  if alive[i]==1:p[i]=collide(p[i]+dp[i])
@ti.kernel
def velocity():
 for i in range(N):
  if alive[i]==1:v[i]=(p[i]-old[i])/DT
@ti.kernel
def curl():
 for i in range(N):
  omega=ti.Vector([0.,0.,0.])
  for k in range(nc[i]):
   j=neighbors[i,k];omega+=(v[j]-v[i]).cross(gradient(p[i]-p[j]))*MASS/ti.max(REST*.3,rho[j])
  w[i]=omega
@ti.kernel
def forces():
 for i in range(N):
  eta=ti.Vector([0.,0.,0.]);visc=ti.Vector([0.,0.,0.])
  for k in range(nc[i]):
   j=neighbors[i,k];r=p[i]-p[j];vol=MASS/ti.max(REST*.3,rho[j]);eta+=(w[j].norm()-w[i].norm())*gradient(r)*vol;visc+=(v[j]-v[i])*kernel(r.norm_sqr())*vol
  confinement=.0025 if ti.static(CUSTOM) else .015
  dp[i]=confinement*eta.normalized(1e-6).cross(w[i])*DT+.012*visc
  active=nc[i]<20 and v[i].norm()>1.9 and p[i].y>1.3 and p[i].z-floor_z(p[i])>.07 and (w[i].norm()>15 or v[i].z<-.9)
  foam[i]=ti.max(foam[i]*ti.exp(-DT/.7),.75 if active else 0.)
@ti.kernel
def apply_forces():
 for i in range(N):
  q=v[i]+dp[i];limit=5.5 if ti.static(CUSTOM) else 7.;v[i]=q*ti.min(1.,limit/ti.max(q.norm(),1e-6))
def status(phase,**extra):
 d={'phase':phase,'worker_running':phase not in ['complete','failed'],'updated_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'pid':os.getpid(),'variant':'true_3D_particle_liquid',**extra}
 for path in [ROOT/'status.json',ROOT/f'renders/{VARIANT}/status.json']:path.write_text(json.dumps(d,indent=2))
 print('FLUID STATUS',json.dumps(d),flush=True)
def reconstruct(q,f,out):
 spacing=.020;shape=np.ceil(BOUNDS/spacing).astype(int)+1;idx=np.floor(q/spacing).astype(int);valid=np.all((idx>=0)&(idx<shape),axis=1);idx=idx[valid];f=f[valid]
 density=np.zeros(shape,np.float32);froth=np.zeros(shape,np.float32);np.add.at(density,tuple(idx.T),1);np.add.at(froth,tuple(idx.T),f)
 density=gaussian_filter(density,1.05);froth=gaussian_filter(froth,1.1)
 vertices,faces,_,_=marching_cubes(density,.45*(spacing/S)**3,spacing=(spacing,)*3,allow_degenerate=False)
 concentration=map_coordinates(froth/np.maximum(density,1e-6),(vertices/spacing).T,order=1,mode='nearest')
 np.savez_compressed(out,vertices=vertices.astype(np.float32),faces=faces.astype(np.int32),foam=concentration.astype(np.float32));return len(vertices),len(faces)
def main():
 for cached_foam in CACHE.glob('foam_points_*.npz'):cached_foam.unlink()
 p.from_numpy(INITIAL);initialize();frames=int(os.environ.get('FLUID_FRAMES','192'));warmup=int(os.environ.get('WARMUP','96'));start=time.monotonic();stats=[]
 status('compiling_fluid_solver',particles=N)
 for frame in range(1,frames+1):
  for sub in range(SUBSTEPS):
   prepare_inlet();predict();build();find_neighbors()
   for iteration in range(ITER):pressure();displacement();apply()
   velocity();curl();forces();apply_forces()
  if overflow[None]>0:raise RuntimeError('Particle neighbor capacity exceeded: '+str(overflow[None]))
  q=p.to_numpy();vv=v.to_numpy();f=foam.to_numpy();assert np.isfinite(q).all() and np.isfinite(vv).all()
  speed=np.linalg.norm(vv,axis=1);live=alive.to_numpy().astype(bool);row={'simulation_frame':frame,'active_particles':int(live.sum()),'mean_speed_m_s':float(speed[live].mean()),'max_speed_m_s':float(speed.max()),'foam_particles':int(((f>.3)&live).sum())}
  if frame>warmup:
   output=frame-warmup;nv,nf=reconstruct(q,f,CACHE/f'liquid_{output:04d}.npz');row.update(output_frame=output,mesh_vertices=nv,mesh_triangles=nf)
   np.savez_compressed(CACHE/f'particles_{output:04d}.npz',positions=q,velocity=vv,foam=f)
  stats.append(row);status('simulating_3D_liquid',current_frame=frame,total_frames=frames,output_frames=max(0,frame-warmup),particles=N,estimated_seconds_remaining=round((time.monotonic()-start)/frame*(frames-frame)),**{k:row[k] for k in ['mean_speed_m_s','max_speed_m_s','foam_particles']})
 report={'solver':'Original 3D position-based fluid, Taichi CPU','reference':'Macklin and Mueller, Position Based Fluids (2013)','gravity_m_s2':9.81,'particles':N,'particle_spacing_m':S,'smoothing_radius_m':H,'pressure_iterations':ITER,'substeps_per_frame':SUBSTEPS,'dt_seconds':DT,'simulation_frames':frames,'warmup_frames':warmup,'output_frames':frames-warmup,'fps':24,'channel_bounds_m':BOUNDS.tolist(),'solid_ellipsoids':ROCKS.tolist(),'geometry_from_simulated_particles':True,'image_or_stock_footage_motion':False,'foam_is_heuristic_surface_field':True,'mesh_voxel_spacing_m':.020,'limitations':['coarse resolution','approximate incompressibility','empirical vorticity confinement and foam','no air-phase solver'],'elapsed_seconds':time.monotonic()-start,'timeline':stats}
 report['channel_configuration']=f'assets/{VARIANT}/channel.json' if CUSTOM else None
 report.update(simulation_sampling_fps=SIMULATION_FPS,delivery_fps=24,water_playback_rate=24/SIMULATION_FPS,warmup_physical_seconds=warmup/SIMULATION_FPS)
 (ROOT/f'research/{VARIANT}/simulation.json').write_text(json.dumps(report,indent=2));status('complete',output_frames=frames-warmup,particles=N)
if __name__=='__main__':
 try:main()
 except BaseException as exc:traceback.print_exc();status('failed',error=str(exc));raise
