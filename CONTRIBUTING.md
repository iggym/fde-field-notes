# Contributing to FDE Field Notes

This guide explains how to contribute articles to FDE Field Notes.

## Article Creation Workflow

### 1. Use the Master Prompt

Start with [`docs/master-prompt-v1.md`](docs/master-prompt-v1.md), which provides:
- Research guidelines and fact-checking rules
- Article structure requirements (1,100–1,500 words)
- HTML/accessibility specifications
- Voice and style guidelines

Fill in the INPUTS block, paste the entire file into Claude, and follow the self-review checklist before submitting.

### 2. Generate HTML and Metadata

The master prompt produces three artifacts:

1. **Outline** — title, dek, reframe, beats, counterargument, actions
2. **metadata.json entry** — JSON object for `articles[]`
3. **articles/{slug}.html** — complete self-contained HTML file

### 3. Add Files to the Repository

```bash
# Copy the HTML file to articles/
cp ~/Downloads/your-slug.html articles/

# Add the metadata entry to metadata.json
# (Append it to the articles[] array)
```

### 4. Run the Build Script

```bash
python3 scripts/build.py
```

This script:
- Validates that all metadata entries point to existing files
- Checks that all files in `articles/` are listed in metadata
- Injects SEO metadata (canonical links, OG tags, JSON-LD, Twitter cards)
- Generates pillar-based "Keep reading" navigation
- Regenerates `index.html` (noscript list), `feed.xml`, and `sitemap.xml`

**Important:** Always run this after adding or modifying articles. The changes it makes are idempotent.

### 5. Review and Commit

```bash
# Check the changes
git status
git diff metadata.json
git diff articles/your-slug.html | head -50

# Commit
git add articles/ metadata.json
git commit -m "Add article: {title} ({pillar})"

# Push and open a PR
git push -u origin improve/your-article
```

### 6. CI Validation

Your PR will run automated checks:
- Build script validation (no unintended file changes)
- Metadata schema validation (required fields, format, pillar)
- SEO meta tags check (canonical, description, OG, Twitter, JSON-LD)
- HTML structure validation (semantic elements, headings)
- Link checking (internal links point to existing files)

All checks must pass before merging.

## Metadata Guidelines

Each article requires these fields in `metadata.json`:

| Field | Format | Notes |
|-------|--------|-------|
| `id` | `YYYYMMDD-slug` | Unique ID; slug must match filename |
| `slug` | kebab-case | Used in URL and filename |
| `title` | 2–6 words | Punchy claim, not a label |
| `hook` | ≤ 200 chars | One or two sentences stating the reframe |
| `path` | `articles/slug.html` | Relative path to HTML file |
| `date` | `YYYY-MM-DD` | Publish date (dateline) |
| `status` | `published` | Must be "published" to appear on site |
| `format` | `field-note` | Article format (not yet diversified) |
| `pillar` | One of 6 | See [master prompt](docs/master-prompt-v1.md) for list |
| `tags` | lowercase, kebab-case | Must include `"fde"` + 2–4 domain tags |
| `reading_time_minutes` | Integer 1–30 | Roughly word count ÷ 230, rounded |
| `pinned` | Boolean | Reserve for flagship articles per pillar |
| `research_window` | `YYYY-MM-DD to YYYY-MM-DD` | Date range sources were within |

## Quality Checklist

Before opening a PR, ensure:

- [ ] Thesis fits in one sentence and doesn't repeat existing articles
- [ ] Every claim has a source dated within the research window
- [ ] Three distinct evidence contexts (e.g., vendor, cloud provider, internal team)
- [ ] Counterargument is the strongest one, with evidence
- [ ] Actions are concrete enough to start this week; one 24-hour action
- [ ] SVG diagram explains a mechanism, not just decorates
- [ ] All required meta tags are present and correct
- [ ] Home link is relative (`../index.html`) and works locally
- [ ] Page renders at 360px, works with JS disabled, passes keyboard navigation
- [ ] Metadata JSON is valid and matches HTML
- [ ] `python3 scripts/build.py` passes with no unexpected changes

## Article Design System

All articles use shared CSS and JavaScript:

- **`assets/css/article.css`** — typography, layout, components (cards, widgets, navigation)
- **`assets/js/article.js`** — progress bar, share buttons, tracker persistence

These handle dark mode, accessibility (WCAG AA), and responsive design (360px+).

### Custom Styling

If your article needs custom styles:
1. Prefer CSS custom properties (`var(--stamp)`, `var(--ink)`, etc.)
2. Add a `<style>` block in the `<head>` (keep it under 5KB)
3. Avoid inline styles except for layout tweaks

### Interactive Elements

Use vanilla HTML5 + ES6:
- Input elements with `oninput` handlers
- `<details>` for accordions
- `<svg>` for diagrams
- Custom trackers and widgets with `localStorage`

All interactions must degrade gracefully with JavaScript disabled.

## Fact-Checking

Non-negotiable: every factual claim must be **verifiable and cited**.

1. Use primary sources (earnings calls, engineering blogs, official reports, job postings)
2. Name the source in prose ("Palantir's Q4 earnings call…"), not just the footer
3. Only cite events dated inside the research window
4. If you can't verify a figure, don't include it — write `[NEEDS SOURCE]` and flag it
5. Clearly separate reported fact, analysis, and personal experience

See [`docs/master-prompt-v1.md` §3](docs/master-prompt-v1.md) for detailed research rules.

## Questions?

Refer to:
- [`docs/master-prompt-v1.md`](docs/master-prompt-v1.md) — article generation prompt with full guidelines
- [`assets/css/article.css`](assets/css/article.css) — design system
- [`tasks/tasks.md`](tasks/tasks.md) — content and infrastructure backlog
