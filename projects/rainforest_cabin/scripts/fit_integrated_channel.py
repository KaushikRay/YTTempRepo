import numpy as np,json
from scipy.optimize import least_squares
from pathlib import Path
W,H=1672,941
def bed(y):
 def drop(a,b):
  t=np.clip((y-a)/(b-a),0,1);return 1-t*t*(3-2*t)
 return .18+.37*drop(1.35,1.7)+.28*drop(2.55,2.8)+.24*drop(3.7,4)
ys=np.array([0.,1.45,2.7,3.9,5.55]);points=np.array([[1.2,y,bed(y)+.13] for y in ys]);targets=np.array([[905,747],[969,783],[1057,828],[1151,879],[1276,951]])
def project(q,p):
 x,y,z,yaw,pitch,f=p;pos=np.array([x,y,z]);forward=np.array([np.sin(yaw)*np.cos(pitch),-np.cos(yaw)*np.cos(pitch),-np.sin(pitch)]);right=np.cross(forward,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,forward);d=q-pos;depth=d@forward
 return np.array([W/2+f*(d@right)/depth,H/2-f*(d@up)/depth]).T,depth
def residual(p):
 uv,depth=project(points,p)
 # At the far and near ends, additionally constrain approximate stream widths.
 q=np.array([[.5,0,bed(0)+.13],[1.9,0,bed(0)+.13],[.5,5.55,bed(5.55)+.13],[1.9,5.55,bed(5.55)+.13]])
 end,_=project(q,p);widths=[np.linalg.norm(end[0]-end[1]),np.linalg.norm(end[2]-end[3])]
 return np.r_[((uv-targets)*np.array([1,1])).ravel(),(np.array(widths)-[82,240])*.3,np.maximum(0,.3-depth)*100]
best=None
for seed in range(10):
 init=[3.7+seed*.08,8+seed*.1,2.8,-.38,.1,1000]
 fit=least_squares(residual,init,bounds=([1.4,5.9,1.5,-1.2,-.3,300],[10,16,6,.4,.8,2300]),max_nfev=3000)
 if best is None or np.linalg.norm(fit.fun)<np.linalg.norm(best.fun):best=fit
p=best.x;uv,depth=project(points,p);forward=np.array([np.sin(p[3])*np.cos(p[4]),-np.cos(p[3])*np.cos(p[4]),-np.sin(p[4])])
report={'camera_location':p[:3].tolist(),'camera_forward':forward.tolist(),'focal_pixels':p[5],'lens_mm':p[5]*36/W,'sensor_width_mm':36,'image_size':[W,H],'rms_center_error_pixels':float(np.sqrt(np.mean((uv-targets)**2))),
 'targets':targets.tolist(),'world_points':points.tolist(),'projected':uv.tolist(),'fit_norm':float(np.linalg.norm(best.fun))}
root=Path(__file__).resolve().parents[1];(root/'research/integrated_fluid').mkdir(exist_ok=True);(root/'research/integrated_fluid/camera_fit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
from scipy.interpolate import PchipInterpolator
pos=p[:3];fwd=forward;right=np.cross(fwd,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,fwd)
def inverse(u,v,y):
 ray=fwd+right*((u-W/2)/p[5])-up*((v-H/2)/p[5]);return pos+ray*((y-pos[1])/ray[1])
anchors=[(0,908,744),(1.15,942,751),(1.45,958,770),(1.85,982,794),(2.35,1005,799),(2.65,1048,805),(2.95,1068,830),(3.5,1110,856),(4.0,1150,889),(4.8,1215,916),(5.6,1290,955)]
centres=np.array([inverse(u,v,y) for y,u,v in anchors]);grid_y=np.linspace(0,5.8,581)
cx=PchipInterpolator(centres[:,1],centres[:,0],extrapolate=True)(grid_y);bed_z=PchipInterpolator(centres[:,1],centres[:,2]-.13,extrapolate=True)(grid_y)
desired_pixels=np.array([60,80,86,100,94,110,120,135,155,195,250]);depth=(centres-pos)@fwd
half=np.maximum(.20,desired_pixels*depth/p[5]/abs(right[0])/2-.105)
width=PchipInterpolator(centres[:,1],half,extrapolate=True)(grid_y)
rock_specs=[(877,755,1.0,[.43,.36,.32]),(1013,745,.9,[.46,.35,.32]),(1125,790,2.9,[.35,.35,.28]),(1275,855,4.6,[.50,.45,.36]),(964,895,4.5,[.68,.55,.40])]
rocks=[[*inverse(u,v,y),*radius] for u,v,y,radius in rock_specs]
cfg={'camera':report,'photo_centerline_anchors':anchors,'profile_step_m':.01,'bed_profile_z':bed_z.tolist(),'center_profile_x':cx.tolist(),'half_width_profile':width.tolist(),
 'bank_stiffness':8.,'solid_ellipsoids':rocks,'water_surface_reference_offset_m':.13,'bounds_m':[2.4,5.8,2.4],'estimated_scale':True,'camera_is_approximate_single_image_fit':True}
(root/'assets/integrated_fluid').mkdir(exist_ok=True);(root/'assets/integrated_fluid/channel.json').write_text(json.dumps(cfg,indent=2));print('Channel:',len(grid_y),'profile samples,',len(rocks),'collision rocks, width range',float(width.min()),float(width.max()))
# Keep the inlet two metres upstream, behind the photographed bank. Translate
# the camera and all fitted obstacles together to retain the same projection.
extension=2.;old_y=np.arange(len(cfg['bed_profile_z']))*.01;new_y=np.arange(781)*.01-extension
for name in ['bed_profile_z','center_profile_x','half_width_profile']:cfg[name]=np.interp(new_y,old_y,cfg[name]).tolist()
cfg['bounds_m'][1]+=extension;cfg['camera']['camera_location'][1]+=extension
for point in cfg['camera']['world_points']:point[1]+=extension
for rock in cfg['solid_ellipsoids']:rock[1]+=extension
cfg['upstream_extension_m']=extension
(root/'assets/integrated_fluid/channel.json').write_text(json.dumps(cfg,indent=2));(root/'research/integrated_fluid/camera_fit.json').write_text(json.dumps(cfg['camera'],indent=2))
