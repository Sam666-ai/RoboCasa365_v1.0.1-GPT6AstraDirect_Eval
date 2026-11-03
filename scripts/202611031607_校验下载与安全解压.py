"""Verify release assets and every trajectory member; optionally extract safely."""
from pathlib import Path,PurePosixPath
import argparse,json,csv,hashlib,tarfile,collections
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--extract',action='store_true');p.add_argument('--core-only',action='store_true');a=p.parse_args();root=a.root.resolve()
def filehash(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
core=next((root/'metadata').glob('*_项目文件SHA256.json'))
for e in json.loads(core.read_text()):assert filehash(root/e['path'])==e['sha256'],e['path']
if a.core_only:print('PASS: project files');raise SystemExit
assets=json.loads(next((root/'metadata').glob('*_轨迹分包索引.json')).read_text())
manifest=list(csv.DictReader(next((root/'metadata').glob('*_轨迹文件SHA256索引.csv')).open()))
expected={e['path']:e for e in manifest};seen=set();results={};simulators={};n=0
for asset in assets:
 path=root/asset['file'];assert path.is_file(),f"Missing release asset: {path.name}"
 assert path.stat().st_size==asset['bytes'];assert filehash(path)==asset['sha256'],path.name
 with tarfile.open(path,'r:gz') as t:
  for member in t:
   name=member.name;parts=PurePosixPath(name)
   assert member.isfile() and not parts.is_absolute() and '..' not in parts.parts,name
   assert name in expected and name not in seen,name
   data=t.extractfile(member).read();e=expected[name]
   assert len(data)==int(e['bytes']) and hashlib.sha256(data).hexdigest()==e['sha256'],name
   if name.endswith('/episode_result.json'):results[e['episode_id']]=json.loads(data)
   if name.endswith('/evaluator/simulator_result.json'):simulators[e['episode_id']]=json.loads(data)
   if a.extract:
    dest=root.joinpath(*parts.parts);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
   seen.add(name);n+=1
 assert sum(e['archive']==path.name for e in manifest)==asset['members']
 print(f'PASS: {path.name}',flush=True)
assert seen==set(expected)
catalog=list(csv.DictReader(next((root/'statistics').glob('*_逐回合结果索引.csv')).open()))
for e in catalog:
 if e['counted_in_primary_SR']!='True':continue
 r=results[e['episode_id']];s=simulators[e['episode_id']]
 assert r['task']==e['task'] and (r['native_success']==(e['native_success']=='True'))
 assert int(e['control_steps'])==s['control_steps'] and r['native_success']==s['task_success']
 assert s['native_checker_calls']==s['control_steps']+1 and r['reset_count']==1 and not s['unknown_execution']
print(f'PASS: {n} trajectory files; 174 complete native outcomes match their native result evidence')
