#!/usr/bin/env python3
"""Regenerate derived files from metadata.json (stdlib only, no dependencies).

- index.html : the <noscript> article list between the noscript markers
- feed.xml   : RSS 2.0 feed of published articles
- sitemap.xml: sitemap for the index and every published article

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
