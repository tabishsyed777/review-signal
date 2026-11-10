import argparse, json
from pathlib import Path
import pandas as pd
import statsmodels.formula.api as smf
ASPECTS=['battery','delivery','price','quality','service']
def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 df=pd.read_csv(a.input).dropna(subset=['rating']); df['rating']=pd.to_numeric(df.rating)
 if len(df)<30: raise SystemExit('Need at least 30 reviews; recommended: hundreds per aspect.')
 model=smf.ols('rating ~ '+ ' + '.join(ASPECTS)+' + C(product_id)',data=df).fit(cov_type='HC3')
 effects=[]
 for x in ASPECTS:
  ci=model.conf_int().loc[x]; effects.append({'aspect':x,'coefficient':round(float(model.params[x]),3),'ci_low':round(float(ci[0]),3),'ci_high':round(float(ci[1]),3),'n_mentioned':int(df[x].sum())})
 Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps({'n_reviews':len(df),'model':'OLS: rating ~ aspects + product fixed effects; HC3 robust 95% CI','effects':effects},indent=2))
if __name__=='__main__':main()
