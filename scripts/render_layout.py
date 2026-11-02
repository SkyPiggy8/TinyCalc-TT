"""Raster preview of exact GDS polygons; no fabricated geometry."""
import pathlib
import gdstk
from PIL import Image,ImageDraw
root=pathlib.Path(__file__).resolve().parents[1]
for filename,title in [('calculator_placement_ONLY','CALCULATOR / PLACEMENT ONLY / NOT ROUTED'),('full_adder_EXPERIMENTAL','FULL ADDER / EXPERIMENTAL / NO DRC OR LVS')]:
    top=gdstk.read_gds(root/'layout'/(filename+'.gds')).top_level()[0]
    (xmin,ymin),(xmax,ymax)=top.bounding_box()
    width=1400;scale=(width-80)/(xmax-xmin);height=int((ymax-ymin)*scale)+120
    im=Image.new('RGB',(width,height),'#151a22');d=ImageDraw.Draw(im)
    d.text((30,18),title,fill='#ffffff')
    d.text((30,36),f'{xmax-xmin:.2f} x {ymax-ymin:.2f} um',fill='#c3c9d1')
    palette={64:'#756b89',65:'#97a987',66:'#cfb695',67:'#7fa59d',68:'#b4c9df',69:'#d1a6ab',70:'#a5be9f',71:'#d3b874',235:'#677482'}
    for p in sorted(top.get_polygons(),key=lambda p:p.layer):
        if p.layer not in palette:continue
        pts=[(40+(x-xmin)*scale,height-35-(y-ymin)*scale) for x,y in p.points]
        if p.layer==235:d.line(pts+[pts[0]],fill=palette[235],width=2)
        else:d.polygon(pts,fill=palette.get(p.layer,'#777d87'))
    im.save(root/'layout'/(filename+'.png'))
