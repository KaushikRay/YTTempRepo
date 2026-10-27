"""Labelled collection of real photographs, with individual source credits."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import json, re, textwrap

root=Path(__file__).resolve().parents[1];folder=root/'research'/'forest_photographs'
records=json.loads((folder/'sources.json').read_text())
selected=[r for r in records if r['id'] not in [9,11]]
W=1800;CW=450;CH=335;canvas=Image.new('RGB',(W,4*CH+150),(17,23,24));draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',25)
draw.text((24,14),'REAL PHOTOGRAPH REFERENCES — tropical forest, leaf structure and wetness',font=title,fill='white')
for i,r in enumerate(selected):
    x=(i%4)*CW;y=65+(i//4)*CH
    with Image.open(folder/r['path']) as src:tile=ImageOps.contain(ImageOps.exif_transpose(src).convert('RGB'),(CW-16,CH-67))
    canvas.paste(tile,(x+(CW-tile.width)//2,y))
    label=f"{r['id']}. {r['title'].removeprefix('File:')}"
    for k,line in enumerate(textwrap.wrap(label,width=47)[:2]):draw.text((x+10,y+CH-62+k*19),line,font=font,fill=(225,230,230))
    draw.text((x+10,y+CH-23),r['licence']+' | credits: CREDITS.md',font=font,fill=(158,183,168))
draw.text((940,65+3*CH+35),'OBSERVATIONS',font=title,fill='white')
for i,line in enumerate(['Thin curved edges; staggered pinnae; irregular droop.',
                         'Wetness produces patchy highlights and droplets.',
                         'Understory leaves overlap in layers with fine gaps.',
                         'Daylight guides anatomy; original image guides night mood.']):
    draw.text((940,65+3*CH+90+i*30),line,font=font,fill=(190,210,198))
draw.text((22,65+4*CH+8),'Real photographs for reference only; source licences retained per panel. No reference photograph is used as a scene texture.',font=font,fill='white')
canvas.save(folder/'reference_board.jpg',quality=94)
(folder/'CREDITS.md').write_text('# Real photograph references\n\nPhotographs, not generated images. The reference board is a labelled collection of resized images; each retains its source licence and credit below. Used for visual research, not as scene textures.\n\n'+'\n\n'.join('## '+str(v['id'])+'. '+v['title']+'\n\n'+re.sub('<[^>]+>','',v['author_html'])+' — '+v['licence']+'\n\nSource: '+v['source_page']+'\n\nLicence: '+str(v['licence_url']) for v in selected))
print('Reference board:',len(selected),'real photographs')
