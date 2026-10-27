"""Frame contact sheets and brightness-jump checks for the short motion diagnostic."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageStat
import json

root=Path(__file__).resolve().parents[1];out=root/'renders/motion';frames=out/'frames'
levels=[];roof=[]
for frame in range(1,97):
    with Image.open(frames/f'{frame:04d}.png') as im:
        im=im.convert('RGB');mean=ImageStat.Stat(im).mean
        levels.append(sum(a*b for a,b in zip(mean,[.2126,.7152,.0722])))
        mean=ImageStat.Stat(im.crop((355,65,450,120))).mean
        roof.append(sum(a*b for a,b in zip(mean,[.2126,.7152,.0722])))
jump=max(abs(a-b) for a,b in zip(levels,levels[1:]))
assert jump<3,(jump,'Unexpected whole-frame brightness jump')
sheet=Image.new('RGB',(1920,780),(18,24,22));draw=ImageDraw.Draw(sheet)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
for i,frame in enumerate([1,20,39,58,77,96]):
    x=(i%3)*640;y=(i//3)*390
    with Image.open(frames/f'{frame:04d}.png') as src:sheet.paste(src.convert('RGB'),(x,y+30))
    draw.text((x+12,y+6),f'Frame {frame} — {(frame-1)/24:.2f} s',font=font,fill='white')
sheet.save(out/'contact.jpg',quality=95)
result={'frames_checked':96,'global_mean_luma_code_range':[min(levels),max(levels)],
        'maximum_adjacent_global_mean_luma_jump_codes':jump,'static_roof_mean_luma_code_range':[min(roof),max(roof)],
        'large_brightness_jumps_detected':False,'detail_flicker_ruled_out':False,
        'rain_detail_limited_at_preview_resolution':True,'full_size_material_reference':'renders/clear_view_still.png'}
(out/'visual_checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
