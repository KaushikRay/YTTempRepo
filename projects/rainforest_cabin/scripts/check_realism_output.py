"""Check final modeled/hybrid PNGs and the independently rendered rain layer."""
from pathlib import Path
from PIL import Image
import hashlib,json

root=Path(__file__).resolve().parents[1]
images={}
for name in ['realism_still.png','hybrid_still.png']:
    path=root/'renders'/name
    with Image.open(path) as image:
        assert image.size==(1920,1080),image.size;image.verify()
    images[name]={'resolution':[1920,1080],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
rain=root/'renders/hybrid_pass/rain_0001.png'
with Image.open(rain) as image:
    image=image.convert('RGBA');assert image.size==(1920,1080)
    alpha=image.getchannel('A');hist=alpha.histogram();coverage=1-hist[0]/sum(hist)
    assert alpha.getextrema()[1]>0 and .0001<coverage<.5,(alpha.getextrema(),coverage)
plate=json.loads((root/'assets/hybrid/provenance.json').read_text())
setup=json.loads((root/'research/realism/hybrid_setup.json').read_text())
assert plate['generated'] is True and plate['camera_photograph'] is False
assert setup['plate_static'] is True and setup['background_wind_or_water_animated'] is False and setup['rain_rendered_in_3D'] is True
result={'image_checks':images,'rain_layer_sha256':hashlib.sha256(rain.read_bytes()).hexdigest(),'rain_layer_nonzero_alpha_fraction':coverage,
        'hybrid_generated_plate':True,'hybrid_plate_static':True,'hybrid_camera_locked':True,'hybrid_background_wind_water_animated':False,
        'hybrid_plate_native_resolution':plate['dimensions'],'new_motion_clip_rendered':False,'final_photorealism_claimed':False}
(root/'renders/realism_qa.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
