"""Reproduce explicitly positioned SKY130 cells, plus a hand-wired full-adder.

The complete calculator GDS is a PLACEMENT ONLY checkpoint, not tapeout-ready.
The full-adder is an experimental routed block; DRC/LVS have NOT been run.
No automatic placer/router is invoked. Coordinates are editable in placement.csv.
"""
import argparse,csv,json,pathlib,re
import gdstk
ROOT=pathlib.Path(__file__).resolve().parents[1]
L={'li1':(67,20),'mcon':(67,44),'met1':(68,20),'via1':(68,44),
   'met2':(69,20),'via2':(69,44),'met3':(70,20),'met4':(71,20)}
MAP={'$_AND_':('and2','X'),'$_OR_':('or2','X'),'$_XOR_':('xor2','X'),
     '$_NOT_':('inv','Y'),'$_MUX_':('mux2','X'),'$_DFF_P_':('dfxtp','Q')}
ap=argparse.ArgumentParser();ap.add_argument('--cells',type=pathlib.Path,required=True)
ap.add_argument('--seed-placement',action='store_true');args=ap.parse_args()
cellroot=args.cells.resolve();out=ROOT/'layout';out.mkdir(exist_ok=True)
lib=gdstk.Library(unit=1e-6,precision=1e-9);cache={};lefs={}
def cell(kind):
 name=f'sky130_fd_sc_hd__{kind}_1'
 if name not in cache:
  path=cellroot/'cells'/kind
  g=gdstk.read_gds(path/(name+'.gds'));top=g.top_level()[0]
  for c in g.cells:
   if c.name not in cache:lib.add(c);cache[c.name]=c
  cache[name]=top
  txt=(path/(name+'.lef')).read_text()
  w,h=map(float,re.search(r'SIZE\s+([\d.]+)\s+BY\s+([\d.]+)',txt).groups())
  pins={}
  for p,body in re.findall(r'\bPIN (\S+)\s+(.*?)\n\s*END \1',txt,re.S):
   rects=[];layer=None
   for line in body.splitlines():
    lm=re.search(r'LAYER\s+(\S+)',line)
    if lm:layer=lm.group(1)
    rm=re.search(r'RECT\s+([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)',line)
    if rm:rects.append((layer,tuple(map(float,rm.groups()))))
   pins[p]=rects
  lefs[kind]=(w,h,pins)
 return cache[name]
def rect(c,a,b,layer):c.add(gdstk.rectangle(a,b,layer=L[layer][0],datatype=L[layer][1]))
def line(c,points,width,layer):c.add(gdstk.FlexPath(points,width,simple_path=True,layer=L[layer][0],datatype=L[layer][1]))
def contact(c,x,y):
 # Experimental pin access. Enclosures must be checked against the target PDK.
 for layer,width in [('mcon',.17),('met1',.32),('via1',.15),('met2',.34),('via2',.20),('met3',.40)]:
  rect(c,(x-width/2,y-width/2),(x+width/2,y+width/2),layer)
def access(kind,p,x,y):
 pins=lefs[kind][2][p]
 layer,r=max((z for z in pins if z[0]=='li1'),key=lambda z:(z[1][2]-z[1][0])*(z[1][3]-z[1][1]))
 return x+(r[0]+r[2])/2,y+(r[1]+r[3])/2
# Hand-defined 1-bit full-adder: p=A xor B; S=p xor CI;
# CO=~(~(A&B)&~(p&CI)). Five real standard cells, eight fixed routing tracks.
fa=lib.new_cell('tinycalc_manual_fa_EXPERIMENTAL')
instances=[('xp','xor2',0.),('xs','xor2',4.6),('nab','nand2',9.2),('npc','nand2',11.5),('nc','nand2',13.8)]
netpins={'A':[('xp','A'),('nab','A')], 'B':[('xp','B'),('nab','B')],
 'P':[('xp','X'),('xs','A'),('npc','A')], 'CI':[('xs','B'),('npc','B')],
 'NAB':[('nab','Y'),('nc','A')], 'NPC':[('npc','Y'),('nc','B')],
 'S':[('xs','X')], 'CO':[('nc','Y')]}
pos={}
for name,kind,x in instances:
 fa.add(gdstk.Reference(cell(kind),(x,1.36)));pos[name]=(kind,x,1.36)
routes=[]
for i,(net,connections) in enumerate(netpins.items()):
 track=5.44+i*.80;points=[]
 for inst,p in connections:
  kind,x,y=pos[inst];px,py=access(kind,p,x,y);contact(fa,px,py)
  line(fa,[(px,py),(px,track)],.30,'met3')
  rect(fa,(px-.10,track-.10),(px+.10,track+.10),'via2')
  rect(fa,(px-.20,track-.20),(px+.20,track+.20),'met3')
  rect(fa,(px-.20,track-.20),(px+.20,track+.20),'met2');points.append(px)
 line(fa,[(min(points)-.20,track),(max(points)+.20,track)],.30,'met2')
 fa.add(gdstk.Label(net,(min(points),track+.20),layer=230,texttype=0))
 routes.append({'net':net,'horizontal_met2_y_um':track,'pins':connections})
for net,y in [('VGND',1.36),('VPWR',4.08)]:
 rect(fa,(0,y-.24),(15.18,y+.24),'met1')
 fa.add(gdstk.Label(net,(0,y),layer=230,texttype=0))
(out/'full_adder_routes.json').write_text(json.dumps(routes,indent=2))
# Full calculator: fixed manual coordinate manifest, no fabricated interconnect.
mod=json.loads((ROOT/'build/generic.json').read_text())['modules']['tt_um_skypiggy8_tinycalc']
cells=mod['cells'];manifest=out/'placement.csv'
for c in cells.values():cell(MAP[c['type']][0])
if args.seed_placement or not manifest.exists():
 # Initial worksheet packing only. Subsequent rendering reads the fixed CSV.
 x=4.60;y=5.44;rows=[]
 for name,c in sorted(cells.items(),key=lambda z:(z[1]['type']!='$_DFF_P_',z[0])):
  kind=MAP[c['type']][0];w,h,_=lefs[kind]
  if x+w>156.40:x=4.60;y+=5.44
  rows.append([name,kind,round(x,3),round(y,3),'R0']);x+=w
 with manifest.open('w',newline='') as f:
  wr=csv.writer(f);wr.writerow(['instance','cell','x_um','y_um','orientation']);wr.writerows(rows)
top=lib.new_cell('tt_um_skypiggy8_tinycalc_PLACEMENT_ONLY')
rectangles=[];instmap={};area=0.;maxy=0.
with manifest.open() as f:
 for row in csv.DictReader(f):
  name=row['instance'];kind=row['cell'];x=float(row['x_um']);y=float(row['y_um'])
  assert MAP[cells[name]['type']][0]==kind
  assert row['orientation']=='R0'
  w,h,_=lefs[kind];assert 0<=x and 0<=y and x+w<=161.0 and y+h<=111.52
  for ox,oy,ow,oh in rectangles:
   assert min(x+w,ox+ow)-max(x,ox)<.0001 or min(y+h,oy+oh)-max(y,oy)<.0001,'Cell overlap'
  rectangles.append((x,y,w,h));area+=w*h;maxy=max(maxy,y+h)
  top.add(gdstk.Reference(cell(kind),(x,y)));instmap[name]={'cell':kind,'origin_um':[x,y]}
assert set(instmap)==set(cells)
top.add(gdstk.rectangle((0,0),(161.0,111.52),layer=235,datatype=4))
netlist={}
for name,c in cells.items():
 kind,outpin=MAP[c['type']];con={}
 for p,bs in c['connections'].items():
  if p=='C':p='CLK'
  elif p=='Y':p=outpin
  con[p]=bs
 con.update(VPWR=['VPWR'],VGND=['VGND'],VPB=['VPWR'],VNB=['VGND'])
 netlist[name]={'cell':f'sky130_fd_sc_hd__{kind}_1','connections':con}
(out/'mapped_connections.json').write_text(json.dumps(netlist,indent=2))
# Keep the two designs in separate files so the test block cannot be mistaken for the calculator.
def write_tree(top,path):
 l=gdstk.Library(unit=1e-6,precision=1e-9);l.add(top,*top.dependencies(True));l.write_gds(path)
write_tree(top,out/'calculator_placement_ONLY.gds')
write_tree(fa,out/'full_adder_EXPERIMENTAL.gds')
top.write_svg(out/'calculator_placement.svg',background='#151a22',pad='3%')
fa.write_svg(out/'full_adder.svg',background='#151a22',pad='3%')
report={'status':'NOT_TAPEOUT_READY','tile_um':[161.0,111.52],
 'standard_cells':len(cells),'standard_cell_area_um2':round(area,3),
 'cell_area_fraction_of_tile':round(area/(161.0*111.52),4),
 'placement_max_y_um':round(maxy,3),'placement_overlap_check':'PASS',
 'cell_library_commit':'ac7fb61f06e6470b94e8afdf7c25268f62fbd7b1',
 'tile_source_commit':'b7b993ac507a3d0dd9c2c82c213ff6fab7d6dacc',
 'full_calculator_signal_routing':'NOT_IMPLEMENTED','clock_tree':'NOT_IMPLEMENTED',
 'power_tap_filler_antenna':'NOT_IMPLEMENTED','DRC':'NOT_RUN','LVS':'NOT_RUN','STA':'NOT_RUN',
 'full_adder':'experimental explicit routes; not integrated into synthesized calculator netlist',
 'minimum_area_proven':False}
(out/'status.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
