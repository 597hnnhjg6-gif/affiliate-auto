import csv, html, pathlib, datetime, re, urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'; OUT.mkdir(exist_ok=True)
BASE_URL='https://597hnnhjg6-gif.github.io/affiliate-auto/'
rows=list(csv.DictReader((ROOT/'data/offers.csv').open(encoding='utf-8-sig',newline='')))
def esc(s): return html.escape(str(s or ''))
def slug(s): return re.sub(r'[^a-z0-9-]','-',s.lower()).strip('-')[:60]
def page(title,body,description='無料の計算ツールとサービス比較情報を掲載しています。'):
 return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow"><meta name="description" content="{esc(description)}"><title>{esc(title)}</title><style>body{{font-family:system-ui,sans-serif;max-width:760px;margin:40px auto;padding:0 20px;line-height:1.8;color:#222}}a{{color:#1454a3}}.note{{background:#f4f4f4;padding:12px;border-radius:8px}}footer{{margin-top:60px;color:#555;font-size:.9em}}</style></head><body><header><a href="./index.html">サービス比較ノート</a></header><main>{body}</main><footer>広告を含む場合があります。情報は掲載時点のものです。最新の条件は公式サイトをご確認ください。<p>運営者情報・お問い合わせ先は公開前に追記してください。</p></footer></body></html>'''
valid=[]
for r in rows:
 if r['enabled'].strip().lower()!='true': continue
 u=r['affiliate_url'].strip()
 if not u.startswith('https://') or not urllib.parse.urlsplit(u).netloc: continue
 if not re.fullmatch(r'[a-z0-9-]+',r['id']): continue
 valid.append(r)
links=[]
for r in valid:
 name=esc(r['name']); filename=f"{r['id']}.html"
 body=f'''<h1>{name}</h1><p class="note">PR：本ページにはアフィリエイト広告が含まれます。</p><p>{esc(r['description'])}</p><h2>特徴</h2><p>{esc(r['benefits'])}</p><h2>注意点</h2><p>{esc(r['cautions'])}</p><h2>料金</h2><p>{esc(r['price_note'])}</p><p>情報確認日：{esc(r['verified_at'])}</p><p><a href="{esc(r['affiliate_url'])}" rel="sponsored nofollow noopener" target="_blank">サービスの詳細を見る（広告）</a></p><p><a href="{esc(r['official_url'])}" rel="noopener" target="_blank">公式情報を確認</a></p>'''
 (OUT/filename).write_text(page(r['name'],body,r['description']),encoding='utf-8')
 links.append(f'<li><a href="./{filename}">{name}</a> — {esc(r["category"])}</li>')
index='''<h1>無料の計算ツール・サービス比較ノート</h1>
<p>日常や仕事で使える計算ツールを無料で公開しています。入力した値はブラウザ上で計算します。</p>
<h2>無料の計算ツール</h2>
<ul>
<li><a href="./cloud-cost-calculator.html">クラウド月額コスト比較</a> — 2つのサービスの月額費用・期間合計を比較</li>
<li><a href="./percentage-calculator.html">割合・増減率計算</a> — 数値の増減率を計算</li>
<li><a href="./hourly-rate-calculator.html">時給・月収換算</a> — 時給と労働時間から収入を概算</li>
<li><a href="./break-even-calculator.html">損益分岐点計算</a> — 必要販売数を計算</li>
</ul>
<p>計算結果は参考値です。契約・取引・意思決定の前に条件をご確認ください。</p>
<h2>サービス紹介</h2>'''
index+= '<ul>'+''.join(links)+'</ul>' if links else '<p>現在、公開中の紹介記事はありません。広告案件は提携・内容確認後に掲載します。</p>'
(OUT/'index.html').write_text(page('サービス比較ノート',index,'クラウド費用・割合・時給・損益分岐点を無料で計算できるツールとサービス比較情報。'),encoding='utf-8')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n',encoding='utf-8')
print(f'Built {len(valid)} offer pages')

import subprocess, sys
subprocess.run([sys.executable, str(ROOT/'scripts/add_tools.py')], check=True)

# Generate a fresh sitemap after all calculator pages have been created.
from xml.etree.ElementTree import Element, SubElement, ElementTree
sitemap=Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for file in sorted(OUT.glob('*.html')):
    if file.name.startswith('google'):
        continue
    entry=SubElement(sitemap,'url')
    SubElement(entry,'loc').text=BASE_URL+file.name
ElementTree(sitemap).write(OUT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE_URL+'sitemap.xml\n',encoding='utf-8')
print('Generated sitemap.xml')
