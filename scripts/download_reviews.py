"""Download a bounded JSONL(.gz) review sample from an authorised public URL."""
import argparse, gzip, json, shutil, urllib.request
from pathlib import Path
def main():
 p=argparse.ArgumentParser(description='Use a provider download URL you are authorised to use.')
 p.add_argument('--url',required=True,help='Public JSONL or JSONL.GZ source URL')
 p.add_argument('--out',default='data/raw/reviews.jsonl');p.add_argument('--limit',type=int,default=1000);a=p.parse_args()
 out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
 with urllib.request.urlopen(a.url) as response:
  stream=gzip.GzipFile(fileobj=response) if a.url.endswith('.gz') else response
  with out.open('w') as target:
   for n,line in enumerate(stream):
    if n>=a.limit: break
    row=json.loads(line); target.write(json.dumps(row)+'\n')
 print(f'Wrote at most {a.limit} reviews to {out}')
if __name__=='__main__':main()
