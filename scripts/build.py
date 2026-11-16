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
star_banner=(ROOT/'data/approved_ads/star-rental-server-banner.html').read_text(encoding='utf-8')
star_body += '<h2>広告</h2><p>PR：以下はアフィリエイト広告です。</p><div>' + star_ad + '</div><div>' + star_banner + '</div>'
(OUT/'star-rental-server.html').write_text(page('スターレンタルサーバーの特徴と契約前の確認点',star_body,'スターレンタルサーバーの特徴と契約前の確認点。PR・広告を含みます。'),encoding='utf-8')
index += '<h2>サービスの基礎情報</h2><ul><li><a href="./star-rental-server.html">スターレンタルサーバーの特徴と契約前の確認点</a> — PR・広告あり</li></ul>'
# Evergreen help articles: no fabricated benchmarks, prices, or rankings.
help_articles = [
 ('rental-server-selection.html', 'レンタルサーバーの選び方：契約前の7つの確認点', '''<h1>レンタルサーバーの選び方</h1><p>ブログやホームページを公開するときは、月額料金だけでなく、用途に合った機能と更新時の費用を確認することが重要です。</p><h2>契約前に確認したい7項目</h2><ol><li>WordPressの利用可否と導入方法</li><li>初回料金・更新料金・最低契約期間</li><li>容量とファイル数などの制限</li><li>無料SSLと独自ドメインの設定方法</li><li>バックアップの有無と復元費用</li><li>問い合わせ方法とサポート対応時間</li><li>解約・移転時のデータ取得方法</li></ol><h2>最初に必要なこと</h2><p>小規模なブログなら、使うCMS、必要なメールアドレス数、予算を整理してからプランを比較しましょう。速度は利用条件や計測環境で変わるため、宣伝文句だけで判断しないことをおすすめします。</p><p>関連：<a href="./star-rental-server.html">スターレンタルサーバーの紹介（PR・広告あり）</a></p>'''),
 ('wordpress-start-guide.html', 'WordPressブログを始める前の準備チェックリスト', '''<h1>WordPressブログを始める前の準備</h1><p>WordPressでブログを作るには、公開場所となるサーバー、必要に応じて独自ドメイン、記事を管理する仕組みを用意します。</p><h2>準備チェックリスト</h2><ol><li>ブログのテーマと想定読者を決める</li><li>独自ドメインを使うか決める</li><li>WordPressに対応するサーバーを選ぶ</li><li>SSL（HTTPS）を有効にする</li><li>管理者のパスワードと二要素認証を設定する</li><li>バックアップと更新の運用を決める</li><li>プライバシーポリシーや広告表示の要否を確認する</li></ol><h2>公開後の運用</h2><p>テーマやプラグインを定期更新し、バックアップを確認しましょう。広告を掲載する場合は利用するASPと広告主の条件も確認してください。</p><p>関連：<a href="./rental-server-selection.html">レンタルサーバーの選び方</a></p>'''),
 ('server-cost-checklist.html', 'レンタルサーバーの料金比較で見落としやすい費用', '''<h1>レンタルサーバーの料金比較で見落としやすい費用</h1><p>広告に表示される月額料金は、契約期間やキャンペーンの適用条件によって実際の支払額と異なることがあります。</p><h2>比較するときの項目</h2><ul><li>初回契約の合計金額</li><li>更新時の月額換算額</li><li>独自ドメインの取得・更新費</li><li>バックアップや復元の追加費用</li><li>契約期間と途中解約時の条件</li><li>支払方法と税の扱い</li></ul><h2>計算例</h2><p>初回12か月分が合計6,000円なら月額換算は500円です。ただし更新料金が異なる場合、2年目以降は別に計算する必要があります。これは説明用の仮定であり、特定サービスの料金ではありません。</p><p>関連：<a href="./rental-server-selection.html">サーバーの選び方</a>／<a href="./star-rental-server.html">スターレンタルサーバー（PR・広告あり）</a></p>''')
]
for filename, title, body in help_articles:
 (OUT/filename).write_text(page(title, body, title), encoding='utf-8')
index += '<h2>レンタルサーバー・ブログの基礎知識</h2><ul>' + ''.join('<li><a href="./'+filename+'">'+esc(title)+'</a></li>' for filename,title,_ in help_articles) + '</ul>'
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
