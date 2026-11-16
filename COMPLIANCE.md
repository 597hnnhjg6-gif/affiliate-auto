# A8.net compliance reference

Last manually reviewed: 2026-11-17. **This date is not a guarantee of current validity.** Check the live official pages and the account's program-specific terms before publishing any advertising.

## Official public references
- Overview: https://www.a8.net/compliance/
- Prohibited practices: https://www.a8.net/compliance/prohibited-matter.php
- Media member agreement: https://www.a8.net/compliance/media-userpolicy.php

The overview links to additional guidance on PR disclosure, SNS (including Instagram/YouTube/TikTok), legal issues, prohibited media practices, and paid search. Revisit relevant links before enabling each feature.

## Confirmed public-page requirements (summary; official text controls)
- A8 prohibits unauthorized modification of ad code, including taking only the link portion from generated code.
- A8 prohibits self-clicks, cooperative clicks, bot/crawler-driven fraudulent clicks, and test orders.
- Advertising on unregistered media is prohibited. SNS rules and advertiser conditions are media-specific.
- Do not continue displaying ended or unpartnered programs.
- Do not publish account-only program names, rewards, conditions, or screenshots in public repositories.
- Avoid mass indiscriminate partnership applications, spam, misleading ad placement, and unsubstantiated claims.
- Display PR/advertising status conspicuously and follow the relevant disclosure guidance.

## Current technical decision
- `scripts/check.py` rejects every enabled legacy CSV offer because `scripts/build.py` currently reconstructs affiliate links from `affiliate_url`. This must **not** be used for A8.net ad publication.
- Existing calculators and informational pages remain publishable.
- A future renderer must support exact, approved A8-issued ad materials, validate partnership status by a documented manual approval gate, avoid code mutation, and avoid exposing non-public program information in Git history.
- GitHub Actions may fail closed rather than publish an unsafe ad. Never bypass compliance checks just to make a deployment green.
- Public pages and rules cannot verify advertiser-specific terms visible only after login. Ask the account owner for a compliance confirmation without copying confidential content into public files.

## Recurring checks
A scheduled ChatGPT task, if configured, can check changes to official public rules and report potential impacts. It does **not** itself update this repository or approve programs unless it explicitly performs those actions with available tools. It cannot independently inspect private A8 dashboard conditions without appropriate access.
