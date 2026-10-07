# FDE Field Notes — Improvement Tasks

Backlog from the repo review, ranked **P0** = correctness/trust, **P1** = high value,
**P2** = nice to have. `[x]` = done, `[~]` = partly done (what's left is noted).

_Last updated: 2026-10-07 — P0 pass, six new deployment-practice articles, index and feed work._

---

## Changelog

**2026-10-07**
- Fixed home links in all 16 legacy articles and the index (relative paths instead of the live URL).
- Normalized `metadata.json`: `YYYYMMDD-slug` IDs, lowercase/merged tags, new `pillar` field,
  2-space formatting, sorted newest first.
- Fact-check pass on the P0 articles (details in section 1). Corrected wrong Palantir figures in
  two articles, wrong Snowflake/Salesforce figures in one, the dateline and deal description in
  `title-is-tell`, and removed leaked generation notes from `roadmap-is-not-wish-list`.
- Fixed README (unclosed code block, broken clone command, Google-redirect link); linked the
  master prompt and this backlog.
- Added `assets/css/article.css` + `assets/js/article.js` (shared design system, dark mode,
  progress bar, share card, tracker).
- Published six deployment-practice articles from `docs/master-prompt-v1.md`.
- Index: escaped metadata before rendering, topic filter chips, pillar label on cards,
  `<noscript>` article list, description/canonical/RSS meta, fixed footer copy.
- Added `scripts/build.py` (stdlib only): validates metadata ↔ files and regenerates the
  `<noscript>` list, `feed.xml` and `sitemap.xml`.

---

## 1. Content quality & editorial

- [~] **P0 — Fact-check and source every article.**
  _Correction to the first audit:_ the five articles flagged as having "no Sources section" do
  have a **Citations** block. The real problems are citations without links and figures that don't
  match the primary sources. Done so far:
  - `lost-before-you-type`, `code-is-just-a-receipt`: Palantir FY2024 figures corrected to
    **US commercial revenue $702M, +54%** (were "$636M, +64%" and "$722M, +36%", which mixed
    up Q4 and full-year numbers).
  - `code-is-just-a-receipt`: removed the Snowflake "$146M professional services" and Salesforce
    "$1.47B professional services" figures, which don't match the filings. Added an editor's note.
  - `title-is-tell`: OpenAI Deployment Company ($4B+, Tomoro acquisition, May 12, 2026) and the
    Anthropic/Blackstone/H&F/Goldman Sachs firm (May 4, 2026) verified and linked; deal wording corrected.

  **Remaining:**
  - `code-is-just-a-receipt`: verify or remove the "~80% AIP bootcamp conversion" claim, which the
    whole article rests on, and the Ramaswamy/Benioff remarks. Rewrite if they can't be sourced.
  - `title-is-tell`: source the 800% posting growth, Levels.fyi bands, PwC 56% premium,
    the 42-fold demand figure, and Salesforce's ~1,000-FDE hiring claim with primary links.
  - `not-yet-is-the-deliverable`: find a primary link for the "650 enterprise tech leaders" survey
    (Digital Applied) or drop the 14%/86%/89% figures; link the MIT NANDA report.
  - `same-work-different-price`: the comp figures are attributed to Levels.fyi with no snapshot.
    Add dated links or mark them as illustrative.
  - `youre-not-deploying-youre-correcting`: the Palantir Q3 2024 "~30% commercial growth" and
    Snowflake Cortex claims need transcript links.
  - `roadmap-is-not-wish-list`: link the Pragmatic Engineer, NVIDIA/Palantir/Lowe's and Databricks sources.
  - Add URLs to every citation in the other legacy articles.
- [x] **P0 — Fix date/timeline inconsistencies.** `title-is-tell` re-dated 2026-03-14 → 2026-08-10
  (the events it cites happened in May 2026); research window and in-text "Last May" updated.
- [ ] **P1 — Consolidate overlapping articles.** Still open. The archive repeats three theses:
  - Titles/comp: `same-work-different-price`, `what-the-title-actually-prices`,
    `the-title-is-the-price`, `the-title-isnt-the-job`, `title-is-tell` (5 pieces).
  - Don't-build: `not-yet-is-the-deliverable`, `the-courage-to-not-build`,
    `customer-context-judgment-dont-build-this-yet`, `when-the-building-stops`,
    `the-code-you-dont-write` (5 pieces).
  - Roadmap/advocacy: `roadmap-is-not-wish-list`, `your-real-job-is-roadmap`,
    `youre-not-deploying-youre-correcting` (3 pieces).
  Merge into one flagship per theme, or make each an explicit series with cross-links.
- [x] **P1 — Cover the under-served pillar.** Six deployment-practice articles published:
  `rollback-is-the-feature`, `dry-run-before-autonomy`, `prompt-injection-is-a-permissions-bug`,
  `the-handoff-is-the-product`, `the-harness-moves-the-number`, `context-is-the-integration`.
  Still uncovered from the README's promises: on-prem/sovereign inference benchmarks and
  cost/batching. Candidates for the next batch.
- [ ] **P1 — Set a pinned flagship article** (`"pinned": true`). Suggest one per pillar once the
  consolidation above is done.
- [ ] **P1 — Expand the new articles to the master prompt's 1,100–1,500-word target.** They landed
  at roughly 980–1,180 words including widgets.
- [ ] **P1 — Re-verify the newsletter source** cited in `the-harness-moves-the-number`
  (buttondown.com was unreachable from the build environment; the 60→82% figure is taken from the README's quote).
- [ ] **P2 — Editorial calendar** (`tasks/content-calendar.md`) with planned topics, pillar,
  status and target dates.
- [ ] **P2 — Version the master prompt.** Record v1 → v2 changes in `docs/` (e.g. word-count floor,
  link to `scripts/build.py`, a list of banned title patterns).

## 2. Metadata (`metadata.json`)

- [x] **P0 — Normalize IDs** to `YYYYMMDD-slug`.
- [x] **P1 — Normalize tags.** Lowercased; merged `product-roadmap`→`roadmap`,
  `fde-career`/`career`→`career-craft`, `market`/`market-data`→`market-signals`.
- [~] **P1 — Add a `pillar` field** (done for all 22 entries). `research_window` is still missing for
  `what-the-title-actually-prices`; the original window isn't recorded anywhere.
- [x] **P1 — Reformat consistently** (2-space indentation).
- [ ] **P1 — JSON Schema** (`docs/metadata.schema.json`), validated in CI. `scripts/build.py`
  already checks IDs and metadata ↔ file consistency.
- [x] **P2 — Sort entries** by date, newest first.
- [ ] **P2 — Controlled tag vocabulary** documented in `docs/` (the near-duplicates
  `customer-judgment`/`customer-context` and `judgment` remain).

## 3. Site — index page

- [~] **P1 — Topic filtering and search.** Pillar filter chips done; free-text search still open.
- [x] **P1 — No-JS fallback.** `<noscript>` list generated by `scripts/build.py`.
- [x] **P1 — Escape metadata before `innerHTML`.**
- [x] **P1 — Fix footer copy** (removed the unlinked "eight-repo portfolio" line).
- [x] **P2 — Show the pillar label** on cards.
- [ ] **P2 — About section** and Buttondown subscribe CTA.

## 4. Site — articles

- [x] **P0 — Use relative home links** (`../index.html`) in all articles.
- [~] **P1 — SEO/social meta.** All six new articles have description, canonical, Open Graph,
  Twitter and JSON-LD `Article`. The 16 legacy articles still lack most of it.
- [~] **P1 — Shared design system.** `assets/css/article.css` + `assets/js/article.js` exist and
  the new articles use them. Migrating the 16 legacy articles (each with its own inline CSS and fonts) is still open.
- [ ] **P1 — "Next / previous" and "related articles"** links generated from `metadata.json`.
- [~] **P2 — Dark mode.** Supported by the shared stylesheet (new articles); legacy articles still 1/16.
- [ ] **P2 — Accessibility pass** on legacy articles (`customer-context-judgment-dont-build-this-yet`
  and `roadmap-is-not-wish-list` have no ARIA attributes; check SVG titles, focus, contrast).
- [ ] **P2 — Social preview images** (`og:image`).

## 5. Discoverability & infrastructure

- [x] **P1 — RSS feed** (`feed.xml`, linked from the index).
- [x] **P1 — `sitemap.xml`.** No `robots.txt`: on a GitHub Pages project site it would be served
  under `/fde-field-notes/`, where crawlers don't look. Submit the sitemap in Search Console instead.
- [ ] **P1 — CI checks (GitHub Actions):** run `scripts/build.py` and fail if it reports errors or
  changes generated files; add an HTML validator, a link checker and a required-meta-tag lint.
- [x] **P2 — Generator script** (`scripts/build.py`, stdlib only).
- [ ] **P2 — `404.html`, favicon** (browsers currently 404 on `/favicon.ico`), `manifest.webmanifest`.
- [ ] **P2 — Privacy-friendly analytics** (e.g. GoatCounter).

## 6. Repository hygiene

- [x] **P0 — Fix README formatting.**
- [~] **P1 — Align README with the actual content.** The deployment-practice articles now cover
  harness/eval design, guardrails, agent loops and MCP; on-prem benchmarks are still promised but not covered.
- [ ] **P1 — `CONTRIBUTING.md`:** master prompt → HTML → metadata entry → `python3 scripts/build.py` → PR.
- [ ] **P2 — Replace the Node boilerplate `.gitignore`** with one suited to a static site.
- [ ] **P2 — PR template** (`.github/pull_request_template.md`) with the article checklist.
- [ ] **P2 — Commit message hygiene.** Several past commits ("Change greeting from 'Hello' to
  'Goodbye'") added articles; use descriptive messages.
