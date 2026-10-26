"""Orient the CC0 growth photograph and retain measured leaf outlines.

This is texture preparation, not a generated scene image. Traces are expressed
in the 1200x1600 inspection view; the atlas keeps the original photo resolution.
"""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageOps

root=Path(__file__).resolve().parents[1]/'assets/creeper'
image=ImageOps.exif_transpose(Image.open(root/'ivy_growth.jpg'));image.save(root/'ivy_atlas.jpg',quality=95)
leaves=[
 {'name':'broad_three_lobe','root':[434,854],'centre':[379,859],'outline':[[434,854],[436,833],[423,815],[409,805],[392,798],[375,800],[359,804],[343,815],[328,805],[312,802],[298,806],[285,820],[277,838],[263,858],[254,877],[268,891],[265,904],[286,907],[310,897],[331,890],[343,899],[350,909],[367,904],[379,901],[387,920],[396,930],[410,918],[422,908],[435,914],[453,925],[469,922],[485,914],[494,900],[491,882],[470,872],[448,861]]},
 {'name':'five_lobe_young','root':[618,707],'centre':[701,741],'outline':[[618,707],[616,692],[618,671],[630,651],[652,647],[681,640],[707,623],[739,615],[774,618],[804,624],[827,629],[813,639],[798,650],[783,665],[769,682],[768,697],[779,714],[791,736],[796,758],[798,779],[806,804],[815,826],[817,843],[798,838],[777,830],[755,824],[739,821],[729,824],[713,838],[694,849],[679,852],[669,846],[660,826],[644,815],[628,806],[615,798],[602,784],[591,771],[590,758],[593,742],[603,727],[613,717]]},
 {'name':'large_rounded_leaf','root':[522,1244],'centre':[573,1358],'outline':[[522,1244],[539,1215],[560,1198],[581,1184],[604,1173],[622,1174],[643,1179],[663,1188],[681,1201],[699,1217],[718,1226],[738,1228],[753,1238],[756,1253],[745,1268],[729,1283],[713,1301],[704,1319],[706,1338],[712,1358],[713,1379],[709,1400],[702,1421],[700,1441],[705,1463],[710,1481],[697,1490],[680,1493],[661,1490],[641,1486],[619,1479],[597,1474],[576,1466],[555,1459],[537,1456],[518,1465],[496,1481],[475,1483],[458,1473],[449,1457],[449,1438],[439,1414],[423,1394],[415,1369],[420,1344],[432,1321],[446,1299],[456,1281],[468,1268],[486,1263],[506,1253]]}
]
data={'source':'ivy_growth.jpg','licence':'CC0','atlas':'ivy_atlas.jpg','atlas_resolution':list(image.size),'trace_reference_resolution':[1200,1600],'leaves':leaves,'atlas_sha256':hashlib.sha256((root/'ivy_atlas.jpg').read_bytes()).hexdigest()}
(root/'leaf-traces.json').write_text(json.dumps(data,indent=2));print('Leaf atlas prepared',image.size)
