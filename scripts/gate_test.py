"""Generate a C++ simulator from actual Yosys gates, then exhaustively test it."""
import json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parents[1]
mod=json.loads((root/'build/generic.json').read_text())['modules']['tt_um_skypiggy8_tinycalc']
ports=mod['ports'];cells=list(mod['cells'].values())
def bit(b):return ('true' if b=='1' else 'false') if isinstance(b,str) else f'n[{b}]'
def pin(c,p):return bit(c['connections'][p][0])
known={'0','1','x','z'}
for p in ports.values():
 if p['direction']=='input':known.update(p['bits'])
dffs=[];comb=[]
for c in cells:
 if c['type']=='$_DFF_P_':dffs.append(c);known.update(c['connections']['Q'])
 else:comb.append(c)
ordered=[]
while comb:
 ready=[c for c in comb if all(b in known for p,bs in c['connections'].items() if c['port_directions'][p]=='input' for b in bs)]
 if not ready:raise RuntimeError('Unsupported cells or combinational cycle')
 for c in ready:
  comb.remove(c);ordered.append(c)
  for p,bs in c['connections'].items():
   if c['port_directions'][p]=='output':known.update(bs)
def expr(c):
 t=c['type'];p=lambda k:pin(c,k)
 if t=='$_NOT_':return '!'+p('A')
 if t=='$_BUF_':return p('A')
 if t=='$_MUX_':return f"({p('S')}?{p('B')}:{p('A')})"
 ops={'$_AND_':'&','$_OR_':'|','$_XOR_':'^','$_NAND_':'&','$_NOR_':'|','$_XNOR_':'^','$_ANDNOT_':'&','$_ORNOT_':'|'}
 if t not in ops:raise ValueError(t)
 b='!'+p('B') if 'NOT_' in t else p('B')
 e=f"({p('A')}{ops[t]}{b})"
 return '!'+e if t in ('$_NAND_','$_NOR_','$_XNOR_') else e
maxbit=max(b for p in mod['netnames'].values() for b in p['bits'] if isinstance(b,int))
lines=['struct Model {',f'bool n[{maxbit+1}]={{}};','unsigned ui_in=0,uio_in=0;bool ena=1,rst_n=1;','void eval(){']
for name,p in ports.items():
 if p['direction']!='input' or name=='clk':continue
 for i,b in enumerate(p['bits']):lines.append(f'{bit(b)}=({name}>>{i})&1;')
for c in ordered:lines.append(f"{pin(c,'Y')}={expr(c)};")
lines+=['}','void tick(){eval();']
for i,c in enumerate(dffs):lines.append(f"bool q{i}={pin(c,'D')};")
for i,c in enumerate(dffs):lines.append(f"{pin(c,'Q')}=q{i};")
lines+=['eval();}','unsigned output(){eval();return '+'|'.join(f'(unsigned({bit(b)})<<{i})' for i,b in enumerate(ports['uo_out']['bits']))+';}',
 'unsigned result(){unsigned save=uio_in;uio_in&=~32u;unsigned lo=output();uio_in|=32;unsigned hi=output();uio_in=save;eval();return lo|(hi<<8);}',
 'bool busy(){eval();return '+bit(ports['uio_out']['bits'][6])+';}',
 'bool divzero(){eval();return '+bit(ports['uio_out']['bits'][7])+';}','};']
cpp=(root/'tests/exhaustive.cpp.in').read_text().replace('@MODEL@','\n'.join(lines))
(root/'build/exhaustive.cpp').write_text(cpp)
exe=root/'build'/('exhaustive.exe' if sys.platform=='win32' else 'exhaustive')
subprocess.run(['g++','-O2','-std=c++11',str(root/'build/exhaustive.cpp'),'-o',str(exe)],check=True)
r=subprocess.run([str(exe)],check=True,capture_output=True,text=True)
print(r.stdout,end='');(root/'build/verification.txt').write_text(r.stdout)
