#!/usr/bin/env python3
"""Regenerate derived files from metadata.json (stdlib only, no dependencies).

- index.html : the <noscript> article list between the noscript markers
- feed.xml   : RSS 2.0 feed of published articles
- sitemap.xml: sitemap for the index and every published article
- articles/* : managed <!-- seo --> head metadata (for pages without their own
               canonical link) and a <!-- related --> "Keep reading" block

It also checks that every metadata entry points at an existing file and that
every file in articles/ is listed. Run it after adding an article:

    python3 scripts/build.py
"""
import datetime
import html
import json
import pathlib
import sys
from email.utils import format_datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
PILLARS = {
    "deployment-practice": "Deployment Practice", "customer-judgment": "Customer Judgment",
    "discovery-scoping": "Discovery & Scoping", "internal-advocacy": "Internal Advocacy",
    "market-comp": "Market & Comp", "role-craft": "Role Craft",
}


def set_block(page, name, content, anchor):
    """Replace the <!-- name:start/end --> block, or insert it before `anchor`.
    An empty `content` removes the block."""
    start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    if start in page:
        head, rest = page.split(start, 1)
        _, tail = rest.split(end, 1)
        page = head.rstrip(" ") + tail.lstrip("\n")
    if not content:
        return page
    block = f"{start}\n{content}\n{end}\n"
    i = page.rfind(anchor)
    return page[:i] + block + page[i:]


def seo_block(page, a, base):
    """Head metadata for articles that don't carry their own canonical link."""
    stripped = set_block(page, "seo", "", "</head>")
    if 'rel="canonical"' in stripped:
        return stripped
    esc = html.escape
    url = f"{base}{a['path']}"
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Article", "headline": a["title"],
        "description": a["hook"], "datePublished": a["date"], "url": url,
        "publisher": {"@type": "Organization", "name": "FDE Field Notes"},
    }, ensure_ascii=False).replace("</", "<\\/")
    lines = []
    if 'name="description"' not in stripped:
        lines.append(f'<meta name="description" content="{esc(a["hook"])}">')
    lines += [
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:type" content="article">',
        '<meta property="og:site_name" content="FDE Field Notes">',
        f'<meta property="og:title" content="{esc(a["title"])}">',
        f'<meta property="og:description" content="{esc(a["hook"])}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="article:published_time" content="{a["date"]}">',
        '<meta name="twitter:card" content="summary">',
        f'<meta name="twitter:title" content="{esc(a["title"])}">',
        f'<meta name="twitter:description" content="{esc(a["hook"])}">',
        f'<script type="application/ld+json">{ld}</script>',
    ]
    return set_block(stripped, "seo", "\n".join(lines), "</head>")


def related_block(page, a, published):
    """'Keep reading' links: the newer and older neighbours in the same pillar."""
    esc = html.escape
    same = [x for x in published if x.get("pillar") == a.get("pillar")]
    links = []
    if a in same:
        i = same.index(a)
        if i > 0:
            links.append(("Newer", same[i - 1]))
        if i < len(same) - 1:
            links.append(("Older", same[i + 1]))
    items = "".join(
        f'<li style="margin:0 0 10px"><span style="opacity:.65">{label} ·</span> '
        f'<a href="{esc(x["slug"])}.html" style="color:inherit">{esc(x["title"])}</a></li>'
        for label, x in links)
    items += '<li><a href="../index.html" style="color:inherit">All field notes →</a></li>'
    label = PILLARS.get(a.get("pillar"), "Field Notes")
    content = (
        '<nav class="fdefn-related" aria-label="Keep reading" style="max-width:700px;margin:48px auto 24px;'
        'padding:20px 16px 0;border-top:1px solid currentColor;line-height:1.5">'
        f'<p style="font-size:12px;letter-spacing:.08em;text-transform:uppercase;opacity:.7;margin:0 0 12px">'
        f'Keep reading · {esc(label)}</p>'
        f'<ul style="list-style:none;padding:0;margin:0">{items}</ul></nav>')
    anchor = "<footer" if "<footer" in page else "</body>"
    return set_block(page, "related", content, anchor)


def main():
    data = json.loads((ROOT / "metadata.json").read_text())
    site = data["site"]
    base = site["base_url"]
    published = sorted(
        (a for a in data["articles"] if a.get("status") == "published"),
        key=lambda a: a["date"], reverse=True)

    errors = []
    ids = [a["id"] for a in data["articles"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate ids in metadata.json")
    listed = {a["path"] for a in data["articles"]}
    for path in listed:
        if not (ROOT / path).is_file():
            errors.append(f"missing file for metadata entry: {path}")
    for f in sorted((ROOT / "articles").glob("*.html")):
        if f"articles/{f.name}" not in listed:
            errors.append(f"article not in metadata.json: articles/{f.name}")
    if errors:
        sys.exit("\n".join(errors))

    esc = html.escape
    for a in data["articles"]:
        path = ROOT / a["path"]
        page = path.read_text()
        page = seo_block(page, a, base)
        page = related_block(page, a, published)
        path.write_text(page)

    items = "\n".join(
        f'    <li><a href="{esc(a["path"])}">{esc(a["title"])}</a> — {esc(a["hook"])}</li>'
        for a in published)
    index = (ROOT / "index.html").read_text()
    start, end = "<!-- noscript:start -->", "<!-- noscript:end -->"
    head, rest = index.split(start)
    _, tail = rest.split(end)
    (ROOT / "index.html").write_text(f"{head}{start}\n{items}\n{end}{tail}")

    def rfc822(d):
        return format_datetime(datetime.datetime.fromisoformat(d).replace(tzinfo=datetime.timezone.utc))

    rss_items = "\n".join(f"""  <item>
    <title>{esc(a["title"])}</title>
    <link>{base}{a["path"]}</link>
    <guid isPermaLink="true">{base}{a["path"]}</guid>
    <pubDate>{rfc822(a["date"])}</pubDate>
    <description>{esc(a["hook"])}</description>
  </item>""" for a in published)
    (ROOT / "feed.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{esc(site["title"])}</title>
  <link>{base}</link>
  <atom:link href="{base}feed.xml" rel="self" type="application/rss+xml"/>
  <description>{esc(site["description"])}</description>
  <language>en</language>
{rss_items}
</channel>
</rss>
""")

    urls = [f"  <url><loc>{base}</loc><lastmod>{published[0]['date']}</lastmod></url>"] if published else []
    urls += [f"  <url><loc>{base}{a['path']}</loc><lastmod>{a['date']}</lastmod></url>" for a in published]
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n")
    print(f"ok: {len(published)} published articles")


if __name__ == "__main__":
    main()
