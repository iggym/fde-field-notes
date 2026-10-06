# FDE Field Notes — Improvement Tasks

Findings from a review of the repo (16 articles, `metadata.json`, `index.html`, `README.md`)
as of 2026-10-06. Priority: **P0** = correctness/trust, **P1** = high value, **P2** = nice to have.

---

## 1. Content quality & editorial

- [ ] **P0 — Fact-check and source every article.** 5 articles have no Sources section
  (`code-is-just-a-receipt`, `not-yet-is-the-deliverable`, `roadmap-is-not-wish-list`,
  `same-work-different-price`, `youre-not-deploying-youre-correcting`). Add sources or
  remove unverifiable figures.
- [ ] **P0 — Fix date/timeline inconsistencies.** Some articles cite events outside or after
  their dateline (e.g. `title-is-tell` is dated 2026-03-14 but cites "Paraform May 2026"
  data and "last May" events). Reconcile `date`, `research_window`, and in-text references.
- [ ] **P1 — Consolidate overlapping articles.** The archive repeats a few theses:
  - Titles/comp: `same-work-different-price`, `what-the-title-actually-prices`,
    `the-title-is-the-price`, `the-title-isnt-the-job`, `title-is-tell` (5 pieces).
  - Don't-build: `not-yet-is-the-deliverable`, `the-courage-to-not-build`,
    `customer-context-judgment-dont-build-this-yet`, `when-the-building-stops`,
    `the-code-you-dont-write` (5 pieces).
  - Roadmap/advocacy: `roadmap-is-not-wish-list`, `your-real-job-is-roadmap`,
    `youre-not-deploying-youre-correcting` (3 pieces).
  Merge the strongest into one flagship per theme, or turn each cluster into an explicit
  series with "Part N" links and cross-references.
- [ ] **P1 — Cover the under-served pillar.** The README promises harness/eval design,
  guardrails, on-prem benchmarks, MCP glue, and post-mortems; none of the 16 articles cover
  them. Plan 4–6 deployment-practice articles (use `docs/master-prompt-v1.md`).
- [ ] **P1 — Set a pinned flagship article** (`"pinned": true`) so the index has an entry point.
- [ ] **P2 — Editorial calendar.** Add `tasks/content-calendar.md` with planned topics,
  pillar, status, and target dates to avoid future duplication.
- [ ] **P2 — Version the master prompt.** Record changes in `docs/` (v1 → v2) as the
  generated output is reviewed.

## 2. Metadata (`metadata.json`)

- [ ] **P0 — Normalize IDs.** IDs are inconsistent (`0001`, `00021`, `000101`, `00101`,
  `20260314-title-is-tell`). Adopt `YYYYMMDD-slug` for all.
- [ ] **P1 — Normalize tags.** Mixed case (`FDE` vs `fde`) and near-duplicates
  (`product-roadmap`/`roadmap`, `market-data`/`market-signals`/`market`,
  `customer-judgment`/`customer-context`, `fde-career`/`career`/`career-craft`).
  Define a controlled vocabulary in `docs/`.
- [ ] **P1 — Add a `pillar` field** to each entry (matches the master prompt) and fill
  missing `research_window` (`what-the-title-actually-prices`).
- [ ] **P1 — Reformat consistently** (2-space indentation; entries currently mix styles).
- [ ] **P1 — Add a JSON Schema** (`docs/metadata.schema.json`) and validate it in CI.
- [ ] **P2 — Sort entries** by date descending in the file for easier diffs.

## 3. Site — index page

- [ ] **P1 — Tag / pillar filtering and search** on the feed (client-side, no deps).
- [ ] **P1 — No-JS fallback.** The feed is built entirely from `fetch('./metadata.json')`;
  with JS off or a fetch failure, visitors see "The notebook is still blank." Add a
  `<noscript>` list or pre-render the list into the HTML at build time.
- [ ] **P1 — Escape metadata before `innerHTML`.** Titles/hooks/tags are interpolated
  unescaped; add a small `escapeHTML()` helper.
- [ ] **P1 — Fix footer copy.** It mentions "an eight-repo portfolio" with no link; link it
  or remove it.
- [ ] **P2 — Show the pillar label / series** on cards and group by pillar.
- [ ] **P2 — Add an about section** and link to the Buttondown newsletter (subscribe CTA).

## 4. Site — articles

- [ ] **P0 — Use relative home links.** All articles link home via the absolute
  `https://iggym.github.io/fde-field-notes/`, which breaks local preview and forks.
  Use `../index.html`.
- [ ] **P1 — SEO/social meta.** 14/16 articles lack `<meta name="description">`; none have
  Open Graph, Twitter card, canonical, or JSON-LD `Article` markup.
- [ ] **P1 — Shared design system.** Each article ships 20–56 KB of inline CSS and a
  different font pairing (DM Serif/DM Sans, Lora/Space Mono, Instrument Serif/Inter,
  IBM Plex…); the index uses Fraunces/Source Serif/Courier Prime. Extract
  `assets/css/article.css` + `assets/js/article.js` (progress bar, share, tracker) and
  align typography with the index.
- [ ] **P1 — "Next / previous" and "related articles"** links at the end of each article,
  generated from `metadata.json` tags.
- [ ] **P2 — Dark mode** (`prefers-color-scheme`) — only 1/16 articles supports it.
- [ ] **P2 — Accessibility pass.** 2 articles have no ARIA attributes; check SVG titles,
  focus states, contrast, and keyboard access for sliders/checklists.
- [ ] **P2 — Social preview images** (`og:image`) per article.

## 5. Discoverability & infrastructure

- [ ] **P1 — RSS/Atom feed** (`feed.xml`) generated from `metadata.json`.
- [ ] **P1 — `sitemap.xml` and `robots.txt`.**
- [ ] **P1 — CI checks (GitHub Actions):** validate `metadata.json` against the schema,
  check every `path` exists and every article file is listed, run an HTML validator and a
  link checker, and lint for required meta tags.
- [ ] **P2 — Small generator script** (`scripts/build.py`, stdlib only) to produce
  `feed.xml`, `sitemap.xml`, and a no-JS index list from `metadata.json` — keeps the
  "zero dependencies" principle.
- [ ] **P2 — `404.html`, favicon, and `manifest.webmanifest`.**
- [ ] **P2 — Privacy-friendly analytics** (e.g. GoatCounter) to learn which topics land.

## 6. Repository hygiene

- [ ] **P0 — Fix README formatting.** The Quickstart code block is never closed, the clone
  URL is wrapped in Markdown link syntax inside the code block, and the deployment link
  points at a Google redirect URL.
- [ ] **P1 — Align README with the actual content** (career/discovery/judgment notes) or
  deliver the promised technical topics.
- [ ] **P1 — Add `CONTRIBUTING.md`** describing how to add an article (master prompt →
  HTML → metadata entry → checklist → PR).
- [ ] **P2 — Replace the Node boilerplate `.gitignore`** with one suited to a static site.
- [ ] **P2 — PR template** (`.github/pull_request_template.md`) with the article checklist.
- [ ] **P2 — Commit message hygiene.** Recent commit messages ("Change greeting from
  'Hello' to 'Goodbye'", "Update fmt.Println message…") don't match the diffs; use
  descriptive messages.
