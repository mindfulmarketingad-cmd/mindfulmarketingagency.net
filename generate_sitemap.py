#!/usr/bin/env python3
"""Rebuild sitemap.xml from every index.html page in the repo.

Run after any generator script (generate_directory.py also writes a sitemap,
but it doesn't know about blog/lists/guides/owned-service pages).
Uses the canonical https://www. host, and git commit dates for <lastmod>.
"""
import os, subprocess, datetime
BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.mindfulmarketingagency.net"
SKIP = {".git", "__pycache__", "data", "assets"}
PRIORITY = {"/": "1.0", "/seo/": "0.9", "/digital-marketing/": "0.9", "/social-media-marketing/": "0.9",
            "/seo/seo-buildout/": "0.9", "/seo/local-citations/": "0.9", "/content-marketing/": "0.8",
            "/digital-marketing/buckhead/": "0.8", "/digital-marketing/stone-mountain/": "0.8",
            "/cities/": "0.7", "/services/": "0.7", "/blog/": "0.7", "/lists/": "0.6"}
today = datetime.date.today().isoformat()
def lastmod(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], cwd=BASE,
                             capture_output=True, text=True).stdout.strip()
        return out or today
    except Exception:
        return today
urls = []
for d, dirs, files in os.walk(BASE):
    dirs[:] = sorted(x for x in dirs if x not in SKIP)
    if "index.html" not in files:
        continue
    rel = os.path.relpath(d, BASE)
    url_path = "/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/"
    with open(os.path.join(d, "index.html"), encoding="utf-8") as fh:
        if 'name="robots" content="noindex' in fh.read(4000):
            continue
    urls.append((url_path, lastmod(os.path.join(d, "index.html"))))
urls.sort(key=lambda u: (u[0] != "/", u[0].count("/"), u[0]))
entries = []
for p, lm in urls:
    pr = PRIORITY.get(p, "0.6" if p.count("/") > 2 else "0.7")
    entries.append(f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{lm}</lastmod>\n    <priority>{pr}</priority>\n  </url>")
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n"
open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8").write(xml)
print(f"sitemap.xml: {len(urls)} URLs")
