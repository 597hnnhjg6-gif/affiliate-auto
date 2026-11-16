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
        assert 'PR：' in (docs/(r['id']+'.html')).read_text(encoding='utf-8')
    print(f'PASS: {count} HTML pages, internal links, enabled offer disclosures')


if __name__ == '__main__':
    test()
