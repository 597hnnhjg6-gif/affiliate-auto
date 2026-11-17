# Private development / Public publishing migration

Status: **preparation only**. Do not disable or privatize the current repository until the replacement publishing pipeline has been verified.

## Target architecture

- Private repository `affiliate-auto-dev`: source scripts, article templates, tests, development workflows, and private configuration (GitHub Actions secrets only; never commit credentials).
- Public repository `affiliate-auto`: generated static site files for GitHub Pages. Keep A8-approved advertising HTML intact, including the required tracking markup; public site HTML is inherently viewable.
- Private build workflow: run checks, generate the static site, then publish only the generated static output to the public repository using narrowly scoped credentials. No unattended deployment until access and content controls are tested.

## Preconditions

1. Create a **private** repository named `affiliate-auto-dev` under the same account. This requires an account action; the current GitHub connector cannot create repositories.
2. Transfer the source into the private repository without committing any API tokens, A8 dashboard details, account-only program terms, or other secrets.
3. Configure a dedicated fine-grained token or GitHub App credential with minimum necessary write access to the public repository, stored in **private repository Actions secrets**. Never paste it into code or chat.
4. Add a publishing workflow that copies only the generated public-site output; explicitly exclude `scripts/`, `data/`, `AGENTS.md`, `COMPLIANCE.md`, and private workflow configuration from the public artifact.
5. Run offline tests and verify exact unchanged A8-issued ad HTML, visible PR labels, valid links, sitemap and privacy text. Do not click or crawl ad tracking URLs.
6. Validate a test publish and GitHub Pages deployment before disabling the current build workflow.
7. Preserve the current public Pages URL where possible; verify the final site and rollback procedure.

## Important limitations

- GitHub Pages on a Free account generally requires a public repository; making the existing repository private can interrupt the published site.
- Moving files to a private repository does **not** erase source code from the public repository's existing Git history. For genuine secrecy, avoid treating previously public code as confidential and assess whether a new clean public publishing repository and URL migration are necessary.
- The published website and its ad HTML are always publicly inspectable. Do not put secrets in generated HTML.
- Changing the publishing repository or Pages source requires configuration and credential access beyond the current connector.
- Existing `affiliate-auto` workflow stays active until migration has been tested and approved.

## Next actions

**Assistant:** once the private repository is created and accessible through the GitHub connection, add private-side build/test workflow, minimal-permission publishing workflow, and verify deployments. Do not copy sensitive material into public outputs.

**User:** create `affiliate-auto-dev` as Private and grant the GitHub connection access to it. No token or secret should be sent in chat.
