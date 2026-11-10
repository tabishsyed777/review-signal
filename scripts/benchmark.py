import argparse,json
from pathlib import Path
import pandas as pd
ASPECTS=['battery','delivery','price','quality','service']
def main():
 p=argparse.ArgumentParser();p.add_argument('--gold',required=True);p.add_argument('--extractions',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 gold=pd.read_csv(a.gold,comment='#'); pred=pd.read_csv(a.extractions); d=gold.merge(pred,on='review_id',suffixes=('_gold','_pred'))
 if len(d)<30: raise SystemExit('Benchmark needs labelled overlap; use a held-out 200–800 review set.')
 rows=[]
 for x in ASPECTS:
  y=d[x+'_gold'].astype(int); z=d[x+'_pred'].astype(int); tp=int((y&z).sum()); f1=2*tp/(int(y.sum()+z.sum()) or 1);rows.append({'aspect':x,'f1':round(f1,3),'n':len(d)})
 Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps({'method':'rules-v1 baseline','labelled_n':len(d),'per_aspect':rows},indent=2))
if __name__=='__main__':main()
