"""Two-role, no-API editorial workflow. Roles are deterministic, not LLM instances."""
import json, pathlib, datetime, html
ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; DOCS=ROOT/'docs'; DOCS.mkdir(exist_ok=True)
CATALOG=[
 {'id':'percentage-calculator','title':'割合・増減率計算ツール','summary':'元の値と新しい値から増減率を計算します。','kind':'percentage'},
 {'id':'hourly-rate-calculator','title':'時給・月収換算ツール','summary':'時給と労働時間から月収と年収の概算を計算します。','kind':'hourly'},
 {'id':'break-even-calculator','title':'損益分岐点計算ツール','summary':'固定費・単価・変動費から必要販売数を計算します。','kind':'break_even'},
]
JS={
'percentage':('元の値','新しい値','const a=+x.value,b=+y.value;if(!Number.isFinite(a)||!Number.isFinite(b)||a===0)throw Error("元の値は0以外で入力してください");return ((b-a)/Math.abs(a)*100).toFixed(2)+"%";'),
'hourly':('時給（円）','月間労働時間','const a=+x.value,b=+y.value;if(a<0||b<0||!Number.isFinite(a)||!Number.isFinite(b))throw Error("0以上の数値を入力してください");return "月収 "+Math.round(a*b).toLocaleString()+"円 / 年収 "+Math.round(a*b*12).toLocaleString()+"円";'),
'break_even':('月間固定費（円）','1件あたり限界利益（円）','const a=+x.value,b=+y.value;if(a<0||b<=0||!Number.isFinite(a)||!Number.isFinite(b))throw Error("固定費は0以上、限界利益は0より大きく入力してください");return "必要販売数 "+Math.ceil(a/b).toLocaleString()+"件";')}
def planner(state):
 pending=[x for x in CATALOG if x['id'] not in state['published']]
 return pending[0] if pending else None
def reviewer(item):
 errors=[]
 if not item or item['kind'] not in JS: errors.append('unknown calculator')
 if item and (not item['title'] or not item['summary']): errors.append('missing editorial fields')
 return errors
def render(item):
 a,b,formula=JS[item['kind']]
 return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(item['title'])}</title><style>body{{font-family:system-ui;max-width:680px;margin:3em auto;padding:0 1em;line-height:1.7}}input,button{{font:inherit;padding:.5em;margin:.3em 0}}label{{display:block}}.disclaimer{{color:#555}}</style></head><body><nav><a href="./index.html">トップへ</a></nav><h1>{html.escape(item['title'])}</h1><p>{html.escape(item['summary'])}</p><label>{a}<input id="x" type="number" step="any" required></label><label>{b}<input id="y" type="number" step="any" required></label><button id="calculate">計算する</button><output id="result" aria-live="polite"></output><p class="disclaimer">計算結果は概算です。入力条件をご確認ください。</p><script>document.getElementById('calculate').addEventListener('click',()=>{{try{{document.getElementById('result').textContent=(()=>{{{formula}}})()}}catch(e){{document.getElementById('result').textContent=e.message}}}})</script></body></html>'''
def run():
 path=DATA/'agent_state.json'
 state=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'published':[]}
 proposal=planner(state)
 report={'date':datetime.date.today().isoformat(),'planner':proposal['id'] if proposal else 'no pending items','reviewer':'not needed','published':None}
 if proposal:
  errors=reviewer(proposal)
  report['reviewer']='approved' if not errors else '; '.join(errors)
  if not errors:
   (DOCS/(proposal['id']+'.html')).write_text(render(proposal),encoding='utf-8')
   state['published'].append(proposal['id'])
   path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
   report['published']=proposal['id']
 # Always regenerate previously approved pages so deployments remain reproducible.
 for item in CATALOG:
  if item['id'] in state['published'] and not reviewer(item):
   (DOCS/(item['id']+'.html')).write_text(render(item),encoding='utf-8')
 (DATA/'last_agent_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':run()
