# ReviewSignal

**Reproducible customer-review mining with evidence, benchmarks, and honest uncertainty.**

ReviewSignal turns product-review text into structured aspect mentions (battery, delivery, price, quality, and service), estimates their association with star ratings, and prepares a transparent benchmark against hand labels. The dashboard is deliberately **fail-closed**: it shows no “verified” findings, accuracy, cost, sales, or return claim until an analysis artifact has been generated.

> This repository is an analysis template—not a source of precomputed business findings. Its committed dashboard begins in “awaiting analysis” state by design.

## What it does

- Downloads a bounded sample from an authorised JSONL/JSONL.GZ review source.
- Extracts review-level aspects with an auditable rules baseline.
- Provides a gold-label template for independent annotation and held-out evaluation.
- Fits `rating ~ aspect mentions + product fixed effects` with HC3 robust 95% confidence intervals.
- Writes analysis artifacts to JSON, which the static dashboard reads at runtime.

## What it does *not* claim

- Aspect coefficients are associations, **not causal effects**.
- The supplied Amazon-style source has ratings and text, not return outcomes. A real returns analysis needs an authorised order/return join.
- Rules-baseline F1 is not LLM F1. LLM performance and cost may only be shown after a model version, labelled holdout, and usage record are saved.
- Evidence quotes must be randomly sampled from matching reviews; never hand-picked to persuade.

## Quick start

```bash
git clone https://github.com/tabishsyed777/review-signal.git
cd review-signal
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

# Bring your own authorised public JSONL/JSONL.GZ URL.
python scripts/download_reviews.py --url "https://example.org/reviews.jsonl.gz" --limit 1000
python scripts/extract_aspects.py --input data/raw/reviews.jsonl --output data/processed/extractions.csv --mode rules
python scripts/analyze.py --input data/processed/extractions.csv --out results/analysis.json
python scripts/build_dashboard_data.py
python -m http.server 8000 --directory dist
```

Open `http://localhost:8000`. Before real results exist, the page correctly displays an empty analysis state.

## Benchmarking extraction

1. Randomly sample 200–800 reviews before looking at their predicted aspects.
2. Have an annotator fill `labels/gold.csv` with one `0`/`1` column per aspect.
3. Keep a hold-out set unseen during prompt/rule design.
4. Run:

```bash
python scripts/benchmark.py --gold labels/gold.csv --extractions data/processed/extractions.csv --out results/benchmark.json
python scripts/build_dashboard_data.py
```

The benchmark reports per-aspect F1 and labelled sample size. To compare an LLM, BERTopic, and LDA fairly, save each method’s per-review predictions on the identical hold-out set and report their measured latency/cost separately.

## Statistical model

`scripts/analyze.py` estimates ordinary least squares with product fixed effects and HC3 robust standard errors:

```text
rating ~ battery + delivery + price + quality + service + C(product_id)
```

For every aspect it outputs the coefficient, 95% confidence interval, and number of mentioning reviews. Interpret this as adjusted correlation. Causal claims need a different design (for example, experiment or valid quasi-experiment).

## Data governance

The recommended starting point is [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/), collected by McAuley Lab. The provider requests research use and citation, but says it does not control or offer a license for the underlying data. Review the source terms and your organisation’s rights before downloading or publishing derived data; do not treat this repository’s MIT license as a license to the dataset.

## Project layout

```text
scripts/       Reproducible ingestion, extraction, analysis, and benchmark jobs
labels/        Gold-label schema (never ship annotations containing personal data)
data/          Local input/output folders; raw and processed data are gitignored
results/       Local analysis artifacts; gitignored
dist/          Static dashboard and generated display payload
```

## License

Code in this repository is available under the [MIT License](LICENSE). Third-party data, models, and platform terms remain subject to their own licenses and policies.
