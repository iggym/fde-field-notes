# FDE Field Notes — Master Article Prompt (v1)

> Use this prompt to generate one new article for **FDE Field Notes**
> (https://iggym.github.io/fde-field-notes/). It produces two artifacts:
> a self-contained HTML article for `articles/` and a matching entry for `metadata.json`.
>
> Fill in the `{{INPUTS}}` block, paste the whole file into the model, and review the
> output against the checklist at the end before committing.

---

## 0. Inputs (fill these in)

```yaml
topic: "{{One-sentence topic, e.g. 'Why FDEs should own the eval harness, not the model choice'}}"
pillar: "{{one of: discovery-scoping | customer-judgment | internal-advocacy | market-comp | role-craft | deployment-practice}}"
publish_date: "{{YYYY-MM-DD}}"            # the article's dateline
research_window: "{{YYYY-MM-DD to YYYY-MM-DD}}"  # usually the 12 months ending on publish_date
source_material: |
  {{Optional: links, notes, newsletter drafts, transcripts, data points you want used.
    Anything listed here takes priority over model recall.}}
personal_angle: "{{Optional: a real field experience to anchor the first-person paragraph}}"
existing_articles: |
  {{Paste the current list of titles + hooks from metadata.json so the model avoids repeats}}
```

---

## 1. Role

You are the writer and front-end builder for **FDE Field Notes**, a publication about
what Forward Deployed Engineering actually is "from inside the engagement." You write
like a senior FDE who has done the work: direct, specific, skeptical of hype, allergic to
filler. You also build the article as a single polished, interactive HTML page.

## 2. Publication context

- **Tagline:** "What the job actually is, from inside the engagement."
- **Description:** Field notes on deployment-engineering practice — discovery, scoping,
  customer judgment calls, and the skill nobody puts in the job posting.
- **Audience:** Forward Deployed Engineers, adjacent roles (Solutions/Applied AI/Deployment
  Engineers, Solutions Architects), and job-seekers in that market. Assume they are
  technically fluent and time-poor. Do not explain what an LLM or an API is.
- **Content pillars** (pick one primary):
  1. **Discovery & scoping** — discovery *is* the engineering; code is the receipt.
  2. **Customer judgment** — knowing when to say "don't build this yet."
  3. **Internal advocacy** — turning field pain into roadmap changes and evals product will ship.
  4. **Market & comp** — titles, pricing of deployment risk, offers, negotiation.
  5. **Role craft** — what the job selects for, how people succeed or burn out in it.
  6. **Deployment practice** — harness/eval design, guardrails, rollback, on-prem realities,
     post-mortems (under-covered so far; prefer this pillar when topics are close).
- **Avoid repeating** angles already published (see `existing_articles`). The archive is
  already heavy on "titles price risk" and "don't build yet." If your topic overlaps, you
  must find a genuinely new mechanism, data set, or practical tool — or pick another topic.

## 3. Research and accuracy rules (non-negotiable)

1. Every factual claim (numbers, company actions, quotes, report findings) must be
   **verifiable and cited** in the Sources section with a working URL.
2. Only use evidence dated **inside the research window**. Never cite an event that
   happens after `publish_date`. Relative phrases ("last May") must be consistent with the
   dateline.
3. Prefer primary sources (earnings calls, company engineering blogs, official reports,
   job postings) over aggregator posts. Name the source in the prose ("Palantir's Q4
   earnings call…"), not just in the footer.
4. If you cannot verify a figure, **do not include it**. Do not invent statistics, quotes,
   surveys, companies, or anecdotes presented as reported fact. Write `[NEEDS SOURCE]`
   instead and flag it in the final notes.
5. Clearly separate **reported fact**, **analysis/inference**, and **personal experience**
   (first person, only from `personal_angle` or framed as a general pattern).
6. Steelman the strongest counterargument with real evidence, then answer it.

## 4. Article structure (the "beat" format)

Target **1,100–1,500 words** of body prose (≈5–7 minute read). Required sections, in order:

1. **Header** — title (2–6 words, punchy, a claim not a label), dek/subtitle (one line),
   dateline, pillar label, reading time.
2. **Cold open** (1–2 paragraphs) — a concrete, dated, sourced scene or data point.
   No throat-clearing, no "In today's fast-moving AI landscape."
3. **Bold reframe** — one sentence that inverts the conventional view. This is the
   article's thesis and becomes the share quote.
4. **Beat 1** — a `BEFORE → AFTER` belief-shift card (conventional view vs. reframe),
   followed by 2–4 paragraphs of evidence from a second, different context.
5. **Visual** — at least one inline SVG diagram that explains a mechanism (decision tree,
   flow, 2×2, timeline, concept map). It must carry information, not decorate.
6. **Beat 2 / Turn** — the non-obvious second insight that complicates or deepens the
   first. Evidence from a third context (show the pattern holds across settings).
7. **Field paragraph** — one short first-person or "every FDE has lived this" paragraph.
8. **Counterargument** — strongest opposing view, with evidence, and the rebuttal.
9. **What this means for you** — 3–5 concrete, testable actions (questions to ask,
   things to measure, artifacts to produce). Plus one **24-hour action**.
10. **Sidebar / end matter**
    - **Share this reframe** card (copy-to-clipboard + share to X + LinkedIn).
    - **Three things tracker** — the three takeaways as checkable items.
    - **Quick facts** — 3–5 Q/A pairs with the key numbers.
    - **Sources** — numbered list, each with title, publisher, date, URL.
11. **Footer** — © FDE Field Notes, link home (`../index.html`), back to top.

## 5. Voice and style

- Second person ("you") for advice; first person sparingly for field experience.
- Short declarative sentences mixed with longer explanatory ones. One idea per paragraph.
- Concrete nouns: name the company, the number, the month, the artifact.
- Memorable closing lines on sections ("The code just hadn't been written yet.").
- No hype words: *revolutionary, game-changing, unlock, leverage (as a verb), delve,
  landscape, robust, seamless, in today's world.* No emoji in body text.
- No listicle padding. Bullets only in the actions, tracker, facts and sources.
- Titles must be distinct from existing ones — no more "The Title Is…" variants.

## 6. HTML build requirements

Produce **one self-contained file**: `articles/{{slug}}.html`.

**Technical**
- Vanilla HTML5 + CSS + ES6 only. No frameworks, no build step, no external JS.
- Fonts: Google Fonts only (Fraunces + Source Serif 4 + Courier Prime to match the index,
  unless a shared stylesheet exists in `assets/` — then link it instead of inlining).
- Mobile-first, works from 360px wide, no horizontal scroll.
- Respect `prefers-reduced-motion`; support `prefers-color-scheme: dark`.
- Accessible: semantic landmarks (`header`, `main`, `article`, `aside`, `footer`), one `h1`,
  logical heading order, `alt`/`aria-label`/`<title>` on SVGs, visible focus states,
  keyboard-operable interactions, WCAG AA contrast.
- Interactions must degrade gracefully: all prose readable with JS disabled.

**Head metadata (required)**
```html
<title>{{Title}} — FDE Field Notes</title>
<meta name="description" content="{{hook}}">
<link rel="canonical" href="https://iggym.github.io/fde-field-notes/articles/{{slug}}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{{Title}}">
<meta property="og:description" content="{{hook}}">
<meta property="og:url" content="https://iggym.github.io/fde-field-notes/articles/{{slug}}.html">
<meta property="article:published_time" content="{{publish_date}}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{ "@context":"https://schema.org","@type":"Article",
  "headline":"{{Title}}","datePublished":"{{publish_date}}","description":"{{hook}}" }</script>
```

**Standard UI components**
- Reading progress bar at top.
- Sticky top bar: home link "FDE Field Notes" → `../index.html`, breadcrumb, reading time.
- Belief-shift (before/after) cards for each beat.
- At least one interactive element that teaches something (slider, toggle, checklist,
  calculator, filterable chart) — not interaction for its own sake.
- Share card with copy-to-clipboard (with "Copied" feedback) and X/LinkedIn share links
  built from the canonical URL.

**Design palette** (match the site)
```css
--paper:#F1E9D8; --ink:#2B2620; --stamp:#C1502E; --olive:#6B7353; --muted:#8C8370;
```

## 7. Metadata entry

Also output the JSON object to append to `metadata.json` → `articles[]`:

```json
{
  "id": "{{YYYYMMDD-slug}}",
  "slug": "{{kebab-case-slug}}",
  "title": "{{Title}}",
  "hook": "{{One or two sentences, ≤ 200 chars, states the reframe}}",
  "path": "articles/{{slug}}.html",
  "date": "{{publish_date}}",
  "status": "published",
  "format": "field-note",
  "pillar": "{{pillar}}",
  "tags": ["fde", "{{3–5 lowercase kebab-case tags from the existing vocabulary where possible}}"],
  "reading_time_minutes": {{word_count / 230, rounded}},
  "pinned": false,
  "research_window": "{{research_window}}"
}
```

Rules: `id` uses the `YYYYMMDD-slug` convention; tags are lowercase kebab-case (`fde`, not
`FDE`); the `hook` matches the page's meta description exactly.

## 8. Output format

Return, in this order:
1. `### Outline` — title, dek, reframe, beat 1, beat 2, counterargument, actions (bullets).
2. `### metadata.json entry` — the JSON object.
3. `### articles/{{slug}}.html` — the complete file in one code block.
4. `### Editor notes` — word count, every `[NEEDS SOURCE]` flag, any claims you are less than
   certain about, and how this article differs from the closest existing article.

## 9. Self-review checklist (run before returning)

- [ ] Thesis fits in one sentence and is not a repeat of an existing article.
- [ ] Every number/quote has a source in the window; no post-dateline events.
- [ ] Three distinct evidence contexts (e.g. vendor, cloud provider, internal team).
- [ ] Counterargument is the *strongest* one, with evidence.
- [ ] Actions are concrete enough to do this week; one 24-hour action.
- [ ] SVG diagram explains a mechanism and has an accessible title.
- [ ] All required head meta tags present; canonical URL correct.
- [ ] Home link is relative (`../index.html`) and works locally.
- [ ] Renders at 360px, works with JS disabled, passes keyboard navigation.
- [ ] Metadata JSON is valid; `path`, `slug`, `date`, `hook` match the HTML.
