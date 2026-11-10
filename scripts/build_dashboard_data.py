"""Fail closed: dashboard receives only computed artifacts, otherwise shows no claims."""
import json
from pathlib import Path
root=Path(__file__).parents[1]; analysis=root/'results/analysis.json'; benchmark=root/'results/benchmark.json'
payload={'status':'awaiting_analysis','message':'Run the documented pipeline on an authorised dataset to populate this dashboard.'}
if analysis.exists():
 payload={'status':'computed','analysis':json.loads(analysis.read_text()),'benchmark':json.loads(benchmark.read_text()) if benchmark.exists() else None}
(root/'dist/data').mkdir(parents=True,exist_ok=True);(root/'dist/data/results.json').write_text(json.dumps(payload,indent=2))
