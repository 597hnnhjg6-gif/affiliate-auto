import csv, html, pathlib, datetime, re, urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'; OUT.mkdir(exist_ok=True)
BASE_URL='https://597hnnhjg6-gif.github.io/affiliate-auto/'
rows=list(csv.DictReader((ROOT/'data/offers.csv').open(encoding='utf-8-sig',newline='')))
def esc(s): return html.escape(str(s or ''))
def slug(s): return re.sub(r'[^a-z0-9-]','-',s.lower()).strip('-')[:60]
def page(title,body,description='無料の計算ツールとサービス比較情報を掲載しています。'):
 return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow"><meta name="description" content="{esc(description)}"><title>{esc(title)}</title><style>body{{font-family:system-ui,sans-serif;max-width:760px;margin:40px auto;padding:0 20px;line-height:1.8;color:#222}}a{{color:#1454a3}}.note{{background:#f4f4f4;padding:12px;border-radius:8px}}footer{{margin-top:60px;color:#555;font-size:.9em}}</style></head><body><header><a href="./index.html">サービス比較ノート</a></header><main>{body}</main><footer>広告を含む場合があります。情報は掲載時点のものです。最新の条件は公式サイトをご確認ください。<p><a href="./about.html">サイトについて・運営者情報</a> ｜ <a href="./privacy.html">プライバシーポリシー</a> ｜ <a href="./advertising.html">広告掲載方針</a></p></footer></body></html>'''
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
# Editorial-only page: no A8 tracking link or unapproved ad material.
star_body='''<h1>スターレンタルサーバーとは？</h1>
<p class="note">PR：本ページにはアフィリエイト広告が含まれます。</p>
<p>スターレンタルサーバーは、エックスサーバー株式会社が運営するレンタルサーバーサービスです。WordPressによるブログやホームページの公開に利用できます。</p>
<h2>公式情報で確認できる特徴</h2>
<ul><li>NVMe SSDを採用したサーバー環境</li><li>WordPressの利用に対応</li><li>無料独自SSLに対応</li><li>エックスサーバーのシステムを採用</li></ul>
<h2>契約前に確認したい点</h2>
<p>プランごとの料金、契約期間、更新時の料金、容量、バックアップ、サポート範囲は公式サイトの最新表示で確認してください。速度や「最安」「最強」といった比較表現は、測定条件によって結果が変わります。</p>
<h2>公式情報</h2><p><a href="https://www.star.ne.jp/" rel="noopener" target="_blank">スターレンタルサーバー公式サイト（広告リンクではありません）</a></p>
<p>情報確認日：2026-11-17。実利用による検証・速度測定は実施していません。</p>'''
# Preserve the user-supplied A8 code byte-for-byte; never reconstruct a URL-only link.
star_ad=(ROOT/'data/approved_ads/star-rental-server.html').read_text(encoding='utf-8')
star_body += '<h2>広告</h2><p>PR：以下はアフィリエイト広告です。</p><div>' + star_ad + '</div>'
(OUT/'star-rental-server.html').write_text(page('スターレンタルサーバーの特徴と契約前の確認点',star_body,'スターレンタルサーバーの公式情報に基づく特徴と契約前の確認点。広告リンクなし。'),encoding='utf-8')
index += '<h2>サービスの基礎情報</h2><ul><li><a href="./star-rental-server.html">スターレンタルサーバーの特徴と契約前の確認点</a> — PR・広告あり</li></ul>'
(OUT/'index.html').write_text(page('サービス比較ノート',index,'クラウド費用・割合・時給・損益分岐点を無料で計算できるツールとサービス比較情報。'),encoding='utf-8')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n',encoding='utf-8')
print(f'Built {len(valid)} offer pages')

import subprocess, sys
subprocess.run([sys.executable, str(ROOT/'scripts/add_tools.py')], check=True)

# Informational pages: do not invent operator identity or contact details.
about_body='''<h1>サイトについて・運営者情報</h1>
<p>当サイトは、日常や仕事で使える無料の計算ツールと、確認済みのサービス比較情報を掲載する個人運営のウェブサイトです。</p>
<h2>運営者</h2><p>運営者の氏名・屋号は現在未掲載です。</p>
<h2>お問い合わせ</h2><p>お問い合わせ窓口は現在準備中です。窓口の公開までは、当サイト経由で個別のお問い合わせを受け付けていません。</p>
<h2>免責事項</h2><p>計算結果や掲載情報の正確性・完全性を保証するものではありません。重要な判断の際は公式情報や専門家の助言をご確認ください。</p>'''
privacy_body='''<h1>プライバシーポリシー</h1>
<h2>計算ツールの入力内容</h2><p>当サイトの計算ツールはブラウザ上で計算を行う設計であり、入力値を当サイト運営者のサーバーへ送信する機能は設けていません。</p>
<h2>ホスティング事業者による情報の取扱い</h2><p>当サイトはGitHub Pagesを利用しています。アクセス時の技術的な情報は、ホスティング事業者がその方針に従って処理する場合があります。詳しくはGitHubのプライバシーステートメントをご確認ください。</p>
<h2>外部サイト・広告リンク</h2><p>外部サイトへ移動した後の個人情報やCookie等の取扱いは、移動先のプライバシーポリシーが適用されます。広告を掲載する場合は広告である旨を明示します。</p>
<h2>変更について</h2><p>本方針はサイトの機能や利用サービスに応じて更新する場合があります。</p>'''
advertising_body='''<h1>広告掲載方針</h1>
<p>当サイトはアフィリエイト広告を掲載する場合があります。紹介リンクを通じて契約・購入等が成立すると、運営者が報酬を受け取ることがあります。</p>
<p>広告を含む記事には「PR」等の表示を行い、広告リンクには広告であることを分かるように記載します。</p>
<p>紹介内容は確認できた情報に基づいて記載する方針ですが、料金・条件・提供状況は変更されることがあります。契約前に必ず公式サイトをご確認ください。</p>
<p>スターレンタルサーバーの紹介記事にアフィリエイト広告を掲載しています。</p>'''
for filename,title,body,description in [
 ('about.html','サイトについて・運営者情報',about_body,'サイトの運営方針、運営者情報、お問い合わせ状況について。'),
 ('privacy.html','プライバシーポリシー',privacy_body,'計算ツールの入力内容、ホスティング、外部リンクの情報の取扱いについて。'),
 ('advertising.html','広告掲載方針',advertising_body,'アフィリエイト広告の表示方法とサービス紹介の方針について。')
]:
 (OUT/filename).write_text(page(title,body,description),encoding='utf-8')

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
