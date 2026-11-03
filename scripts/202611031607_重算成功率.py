"""Recompute SR for locally retained complete native GPT Direct trajectories."""
from pathlib import Path
import argparse,csv,json,collections
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args()
rows=list(csv.DictReader(next((a.root/'statistics').glob('*_逐回合结果索引.csv')).open()));groups=collections.defaultdict(list)
for r in rows:
 assert r['category']=='accepted_native_terminal' and r['counted_in_primary_SR']=='True'
 groups[r['cohort']].append(r)
result=[]
for cohort,rr in sorted(groups.items()):
 s=sum(r['native_success']=='True' for r in rr);tasks=sorted({r['task'] for r in rr})
 rates=[sum(r['native_success']=='True' for r in rr if r['task']==t)/sum(r['task']==t for r in rr) for t in tasks]
 result.append(dict(cohort=cohort,subset=rr[0]['subset'],scene_split=rr[0]['scene_split'],complete_native_episodes=len(rr),successes=s,SR=s/len(rr),tasks_with_complete_trajectories=len(tasks),macro_task_SR=sum(rates)/len(rates)))
reference=json.loads(next((a.root/'statistics').glob('*_分子集场景成功率.json')).read_text());by={r['cohort']:r for r in reference}
for r in result:
 for k in ['complete_native_episodes','successes','SR','tasks_with_complete_trajectories','macro_task_SR']:assert abs(r[k]-by[r['cohort']][k])<1e-12,(r['cohort'],k)
print(json.dumps(dict(status='PASS',episodes=len(rows),cohorts=result),ensure_ascii=False,indent=2))
