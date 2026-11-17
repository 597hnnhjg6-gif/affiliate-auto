"""Offline smoke tests; no paid services or credentials required."""
from pathlib import Path
import csv
import re
import subprocess
import sys
from html.parser import HTMLParser
ROOT = Path(__file__).resolve().parents[1]


class Inspector(HTMLParser):
    def __init__(self): super().__init__(); self.links = []; self.titles = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title':
            self.titles += 1
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])


def test():
    subprocess.run([sys.executable, str(
        ROOT/'scripts/check.py')], check=True, cwd=ROOT)
    subprocess.run([sys.executable, str(
        ROOT/'scripts/agents.py')], check=True, cwd=ROOT)
    subprocess.run([sys.executable, str(
        ROOT/'scripts/build.py')], check=True, cwd=ROOT)
    docs = ROOT/'docs'
    assert (docs/'index.html').exists()
    assert (docs/'robots.txt').exists()
    for article in ('rental-server-selection.html', 'wordpress-start-guide.html', 'server-cost-checklist.html'):
        assert (docs/article).exists(), f'{article}: missing evergreen article'
        assert './'+article in (docs/'index.html').read_text(encoding='utf-8'), f'{article}: missing homepage link'
    for info in ('about.html', 'privacy.html', 'advertising.html'):
        assert (docs/info).exists(), f'{info}: missing information page'
        assert '運営者情報' in (docs/'index.html').read_text(encoding='utf-8')
    from xml.etree import ElementTree as ET
    sitemap = docs/'sitemap.xml'
    assert sitemap.exists(), 'sitemap.xml missing'
    urls = [node.text for node in ET.parse(sitemap).iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    assert len(urls) >= 8, 'sitemap should contain calculators and policy pages'
    for info in ('about.html', 'privacy.html', 'advertising.html'):
        assert any(url.endswith('/'+info) for url in urls), f'{info}: not in sitemap'
    assert all('googlee2ddc50d2788833b' not in url for url in urls)
    assert 'Sitemap: https://597hnnhjg6-gif.github.io/affiliate-auto/sitemap.xml' in (docs/'robots.txt').read_text(encoding='utf-8')
    # The approved ad snippet must be embedded verbatim, including the tracking pixel.
    approved = (ROOT/'data/approved_ads/star-rental-server.html').read_text(encoding='utf-8')
    star = (docs/'star-rental-server.html').read_text(encoding='utf-8')
    assert approved in star, 'approved A8 ad code must not be altered'
    banner = (ROOT/'data/approved_ads/star-rental-server-banner.html').read_text(encoding='utf-8')
    assert banner in star, 'approved A8 banner code must not be altered'
    assert 'width="300" height="250"' in star
    # Both approved ad units must occur exactly once; duplicate tracking pixels are not acceptable.
    assert star.count(approved) == 1, 'text ad must be embedded exactly once'
    assert star.count(banner) == 1, 'banner ad must be embedded exactly once'
    assert star.count('https://px.a8.net/svt/ejp?') == 2, 'unexpected A8 click links'
    assert star.count('/0.gif?a8mat=') == 2, 'unexpected A8 tracking pixels'
    assert '<h2>広告</h2>' in star, 'advertising section missing'
    assert 'PR：本ページにはアフィリエイト広告が含まれます。' in star
    assert 'PR・広告あり' in (docs/'index.html').read_text(encoding='utf-8')
    assert '現在、公開中の紹介記事はありません' not in (docs/'index.html').read_text(encoding='utf-8')
    for filename in ('index.html', 'star-rental-server.html', 'rental-server-selection.html', 'wordpress-start-guide.html', 'server-cost-checklist.html'):
        assert '<link rel="canonical" href="https://597hnnhjg6-gif.github.io/affiliate-auto/'+filename+'">' in (docs/filename).read_text(encoding='utf-8'), f'{filename}: missing canonical'
    assert 'スターレンタルサーバーの紹介記事にアフィリエイト広告' in (docs/'advertising.html').read_text(encoding='utf-8')
    count = 0
    for f in docs.glob('*.html'):
        text = f.read_text(encoding='utf-8')
        p = Inspector()
        p.feed(text)
        if f.name.startswith("google") and f.name.endswith(".html"):
            continue
        assert p.titles == 1, f'{f.name}: title missing or duplicated'
        assert 'lang="ja"' in text, f'{f.name}: missing language'
        assert '<meta name="viewport"' in text, f'{f.name}: missing viewport'
        for url in p.links:
            if url.startswith('./'):
                assert (docs/url[2:]).exists(), f'{f.name}: broken link {url}'
        count += 1
    assert count >= 5, 'expected index and four calculators'
    with (ROOT/'data/offers.csv').open(encoding='utf-8-sig', newline='') as h:
        active = [r for r in csv.DictReader(
            h) if r['enabled'].lower() == 'true']
    for r in active:
        article = docs/(r['id']+'.html')
        assert article.exists(), f"{r['id']}: missing offer page"
        content = article.read_text(encoding='utf-8')
        assert 'PR：' in content, f"{r['id']}: missing PR disclosure"
        assert 'rel="sponsored nofollow noopener"' in content, f"{r['id']}: missing sponsored link attributes"
        assert 'サービスの詳細を見る（広告）' in content, f"{r['id']}: missing ad label"
        assert any(url.endswith('/'+r['id']+'.html') for url in urls), f"{r['id']}: missing from sitemap"
        assert './'+r['id']+'.html' in (docs/'index.html').read_text(encoding='utf-8'), f"{r['id']}: missing homepage link"
    print(f'PASS: {count} HTML pages, internal links, enabled offer disclosures')


if __name__ == '__main__':
    test()
