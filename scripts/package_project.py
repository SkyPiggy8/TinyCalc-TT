"""Package sources and review artifacts, excluding git internals and executables."""
import pathlib,zipfile
root=pathlib.Path(__file__).resolve().parents[1]
out=root.parent/'outputs'/'TinyCalc_TT_checkpoint_20261102.zip';out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(root.rglob('*')):
  rel=p.relative_to(root)
  if not p.is_file() or any(s in {'.git','build','__pycache__','sim_build'} for s in rel.parts):continue
  if p.suffix in {'.exe','.pyc','.zip'}:continue
  z.write(p,pathlib.Path('TinyCalc-TT')/rel)
print(str(out))
