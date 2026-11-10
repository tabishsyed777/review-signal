"""Extract review-level aspects. Rules are an auditable baseline; OpenAI mode is opt-in."""
import argparse, json, os, re
from pathlib import Path
import pandas as pd

ASPECTS = {
    "battery": r"\b(battery|charge|charging|power drain)\b",
    "delivery": r"\b(deliver(?:y|ed)|shipping|arriv(?:e|ed|al)|late)\b",
    "price": r"\b(price|priced|cost|value|expensive|cheap)\b",
    "quality": r"\b(quality|broken|defect|durable|build)\b",
    "service": r"\b(service|support|customer care|refund)\b",
}
def records(path):
    for line in Path(path).read_text().splitlines():
        if line.strip():
            yield json.loads(line)
def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--output',required=True); p.add_argument('--mode',choices=['rules','openai'],default='rules'); a=p.parse_args()
    if a.mode == 'openai':
        raise SystemExit('OpenAI extraction runner is intentionally not bundled without a pinned model and budget. Use rules for baseline, or implement your approved model call with schema/version/cost logging.')
    rows=[]
    for n,r in enumerate(records(a.input)):
        text=(r.get('text') or r.get('reviewText') or '').strip(); low=text.lower()
        rows.append({'review_id':r.get('review_id',r.get('asin',n)), 'product_id':r.get('parent_asin',r.get('asin','unknown')), 'rating':r.get('rating',r.get('overall')), 'text':text, **{k:int(bool(re.search(v,low))) for k,v in ASPECTS.items()}, 'extractor':'rules-v1'})
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame(rows).dropna(subset=['rating']).to_csv(out,index=False)
if __name__=='__main__': main()
