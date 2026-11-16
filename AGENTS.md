# AGENTS.md — affiliate-auto project operating rules

Read this file before modifying, reviewing, or publishing anything in this repository. Also read `COMPLIANCE.md` and the current A8.net official rules linked there. This is a repository instruction file, not a replacement for current ASP rules or advertiser-specific conditions.

## Objective
Operate a useful Japanese-language calculator/comparison website with no unnecessary paid services, accurate information, and compliance-first publishing. Never promise revenue or search ranking.

## Mandatory safety gates
1. NEVER publish an A8.net ad by extracting only a destination URL from A8-issued ad code, changing its wording, or reconstructing an ad. Use approved ad code unchanged and only within the specific program's permitted media and formats.
2. The legacy `data/offers.csv` URL-only publication path is deliberately disabled for all `enabled=true` records. Do not remove this gate until a compliant ad-code storage/rendering method, tests, and a review process are implemented.
3. Do not publish pending, rejected, ended, or unapproved affiliate programs. Verify individual program approval and applicable terms before enabling.
4. Do not auto-click ads, make test orders, generate fake conversions, or crawl ad links for click-testing.
5. No spam, incentivized clicks, deceptive rankings, copied content, unauthorized trademarks/images, or invented prices, claims, results, approvals, operator identity, or contact details.
6. Use conspicuous PR/advertising disclosures and distinguish editorial links from paid advertisements.
7. Never commit private ASP dashboards, program-only details, commissions, screenshots, credentials, tokens, or personal data to this public repository.
8. Do not post affiliate ads to X, Instagram, TikTok, YouTube or other media without confirming A8 media-registration requirements and each platform's current rules. No unattended bulk posting.
9. Before changes touching ads, review official A8 rules and check the latest program-specific conditions with the account owner. If rules cannot be verified, stop advertising changes and report the limitation.
10. Run `python scripts/test_site.py`; check the latest GitHub Actions run. A successful workflow does not establish Search Console indexing or advertiser approval.

## Workflow
- Read `COMPLIANCE.md` and current official source URLs.
- Plan and implement the smallest safe change, keep GitHub Pages build functional, and test.
- For every handoff, report completed work, what is blocked, and **次の作業 / 具体的な作業内容**.
- Any claim of ongoing monitoring requires an actual scheduled task. This file alone does not trigger a recurring run.
