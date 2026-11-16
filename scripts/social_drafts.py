"""Generate free, reviewable social post drafts from existing site tools.
No credentials, paid APIs, scraping, or automatic posting.
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "social-output"
OUT.mkdir(exist_ok=True)
SITE = "https://597hnnhjg6-gif.github.io/affiliate-auto/"
TOPICS = [
    ("percentage-calculator.html", "割合と増減率", "値上がり・値下がりを何％か確認したいとき", "元の数値と変化後の数値を入力して増減率を確認できます。"),
    ("hourly-rate-calculator.html", "時給・月収換算", "時給から月収の目安を考えたいとき", "時給と労働時間から収入の目安を計算できます。"),
    ("break-even-calculator.html", "損益分岐点", "商品を何個売れば固定費を回収できるか考えたいとき", "固定費・販売価格・変動費を使って必要販売数を計算できます。"),
    ("cloud-cost-calculator.html", "クラウド費用比較", "クラウドの月額費用を比較したいとき", "2つのサービスの月額費用と期間合計を比較できます。"),
]
def generate(date=None):
    today = date or datetime.now(timezone(timedelta(hours=9))).date().isoformat()
    index = int(today.replace("-", "")) % len(TOPICS)
    slug, title, hook, detail = TOPICS[index]
    url = SITE + slug
    short = f"【{title}】{hook}。{detail} 無料ツールはこちら：{url}"
    reel = f"{title}を30秒でチェック。\n{hook}？\n{detail}\n詳しくはプロフィールのサイトから。\n#無料ツール #計算 #便利"
    story = [
        {"seconds": 0, "caption": f"{title}を簡単に確認"},
        {"seconds": 5, "caption": hook},
        {"seconds": 12, "caption": detail},
        {"seconds": 22, "caption": "無料ツールはプロフィールから"},
    ]
    payload = {
        "date": today, "source_url": url, "topic": title,
        "status": "draft_only", "requires_review": True,
        "x": {"text": short},
        "instagram": {"caption": reel, "format": "reel_draft"},
        "tiktok": {"caption": reel, "format": "vertical_video_draft"},
        "youtube": {"title": title + "を簡単に確認 #Shorts", "description": detail + "\n" + url, "format": "shorts_draft"},
        "vertical_video_script": story,
        "checks": {"no_claimed_earnings": True, "no_fake_reviews": True, "no_auto_post": True}
    }
    assert len(short) <= 280
    assert all(x["seconds"] >= 0 for x in story)
    (OUT / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "latest.md").write_text(
        f"# {today} 投稿下書き\n\n元ページ: {url}\n\n## X\n{short}\n\n## Instagram / TikTok\n{reel}\n\n## YouTube Shorts\n{payload['youtube']['title']}\n{payload['youtube']['description']}\n\n## 縦動画構成\n"
        + "\n".join(f"- {x['seconds']}秒: {x['caption']}" for x in story)
        + "\n\n※未投稿の下書きです。公開前に内容・広告表記・各媒体の規約を確認してください。\n",
        encoding="utf-8")
    print(f"Generated social drafts for {today}: {title} (not posted)")
if __name__ == "__main__":
    generate()
