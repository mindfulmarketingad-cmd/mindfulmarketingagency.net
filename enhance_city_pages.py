#!/usr/bin/env python3
"""Adds two crawlable, server-rendered blocks to every /<city>/ hub page:

1. A static list of every agency in that city (so search engines see real
   links/content even before directory.js renders the interactive grid).
2. A call-to-action for Mindful Marketing Agency's own services.

Idempotent: re-run after generate_directory.py; blocks live between
<!-- city-static:start --> / <!-- city-static:end --> markers.
"""
import json, os, re, html
BASE = os.path.dirname(os.path.abspath(__file__))
agencies = json.load(open(os.path.join(BASE, "data", "agencies.json"), encoding="utf-8"))
by_city = {}
for a in agencies:
    by_city.setdefault(a["city_slug"], []).append(a)

pat = re.compile(r"\n?\s*<!-- city-static:start -->.*?<!-- city-static:end -->", re.S)
count = 0
for slug, items in by_city.items():
    path = os.path.join(BASE, slug, "index.html")
    if not os.path.isfile(path):
        continue
    s = open(path, encoding="utf-8").read()
    if "data-listings" not in s:
        continue
    city = items[0]["city"]
    items = sorted(items, key=lambda a: (not a.get("featured"), a["name"].lower()))
    lis = "".join(
        f'<li><a href="/{slug}/{a["slug"]}/">{html.escape(a["name"])}</a> — {html.escape(a.get("category") or "")}</li>'
        for a in items
    )
    n = len(items)
    cta = f'''
    <!-- city-cta:start -->
    <section class="section" style="max-width:var(--maxw);padding-bottom:0;">
      <div class="own-cta">
        <h2>Need digital marketing in {html.escape(city)}?</h2>
        <p>Besides running this directory, Mindful Marketing Agency (based in Atlanta) offers flat-priced
        <a href="/seo/">SEO packages</a> from $49.99, <a href="/seo/local-citations/">local citation building</a> from $35,
        and <a href="/social-media-marketing/">social media management</a> for {html.escape(city)} businesses — no long-term contracts.</p>
        <p style="margin-bottom:0;"><a class="btn btn-primary" href="/#packages">See packages &amp; pricing</a></p>
      </div>
    </section>
    <!-- city-cta:end -->'''
    block = f'''
    <!-- city-static:start -->
    <section class="section" style="max-width:860px;">
      <h2>All {n} marketing {"agency" if n == 1 else "agencies"} listed in {html.escape(city)}, GA</h2>
      <ul class="static-agency-list">{lis}</ul>
    </section>
    <!-- city-static:end -->'''
    s = pat.sub("", s)
    s = re.sub(r"\n?\s*<!-- city-cta:start -->.*?<!-- city-cta:end -->", "", s, flags=re.S)
    m = re.search(r"<div data-listings></div>\s*</section>", s)
    if not m:
        print("no marker:", path); continue
    s = s[:m.end()] + block + s[m.end():]
    m2 = re.search(r'\n    <section class="section">\s*<div class="filter-bar">', s)
    if m2:
        s = s[:m2.start()] + cta + s[m2.start():]
    open(path, "w", encoding="utf-8").write(s)
    count += 1
print("enhanced", count, "city pages")
