#!/usr/bin/env python3
"""Server-rendered internal links for the Georgia agency directory.

Run after generate_directory.py (it is also called automatically at the end of it),
then enhance_city_pages.py / brand_cta.py / generate_sitemap.py. Idempotent — every
block lives between <!-- il:NAME:start --> / <!-- il:NAME:end --> markers.

What it adds:
* Listing pages  (/<city>/<listing>/): breadcrumbs Home > Directory > City > Listing,
  a "Similar agencies" grid (same city + category first, then same city, then the same
  category in the nearest cities), links to the city and category pages, nearby cities,
  and a block of relevant Mindful Marketing services.
* City pages (/<city>/): nearby cities (by distance, data/city-coords.json) + categories.
* Category pages (/services/<category>/): every listing grouped by city + top cities.
  Also (re)creates /services/full-service-digital-marketing-agencies/ from the web-design
  page template, because that category has no other crawlable directory page.
* /cities/ and /services/: static, crawlable lists of every city / category page.
"""
import json, os, re, html, math
BASE = os.path.dirname(os.path.abspath(__file__))
E = lambda s: html.escape(str(s or ""), quote=True)
agencies = [a for a in json.load(open(os.path.join(BASE, "data", "agencies.json"), encoding="utf-8"))]
coords = json.load(open(os.path.join(BASE, "data", "city-coords.json")))

CATS = {  # slug -> (name, directory path)
    "full-service-digital-marketing-agencies": "Full-Service Digital Marketing Agencies",
    "ppc-paid-media-agencies": "PPC & Paid Media Agencies",
    "web-design-agencies": "Web Design Agencies",
    "branding-graphic-design-agencies": "Branding & Graphic Design Agencies",
    "content-marketing-agencies": "Content Marketing Agencies",
    "email-marketing-agencies": "Email Marketing Agencies",
}
def cat_url(slug): return f"/services/{slug}/"
BRAND = {  # category -> relevant owned services
    "ppc-paid-media-agencies": [("/google-ads-management/", "Google Ads management"), ("/facebook-ads/", "Facebook & Instagram ads"), ("/website-design/", "Landing page design"), ("/seo/", "SEO packages")],
    "web-design-agencies": [("/website-design/", "Website design"), ("/seo/", "SEO packages"), ("/google-business-profile/", "Google Business Profile"), ("/free-logo-maker/", "Free logo maker")],
    "branding-graphic-design-agencies": [("/free-logo-maker/", "Free logo maker"), ("/website-design/", "Website design"), ("/youtube-thumbnails/", "YouTube thumbnails"), ("/social-media-marketing/", "Social media management")],
}
BRAND_DEFAULT = [("/seo/", "SEO packages"), ("/seo/local-citations/", "Local citations"), ("/google-business-profile/", "Google Business Profile"), ("/social-media-marketing/", "Social media management"), ("/google-ads-management/", "Google Ads management")]

by_city, by_cat, city_name = {}, {}, {}
for a in agencies:
    by_city.setdefault(a["city_slug"], []).append(a)
    by_cat.setdefault(a["category_slug"], []).append(a)
    city_name[a["city_slug"]] = a["city"]

def dist(c1, c2):
    if c1 not in coords or c2 not in coords: return 9e9
    (la1, lo1), (la2, lo2) = coords[c1], coords[c2]
    p = math.radians
    h = math.sin(p(la2 - la1) / 2) ** 2 + math.cos(p(la1)) * math.cos(p(la2)) * math.sin(p(lo2 - lo1) / 2) ** 2
    return 3958.8 * 2 * math.asin(math.sqrt(h))
def nearby(c, n=6):
    return sorted((s for s in by_city if s != c), key=lambda s: dist(c, s))[:n]
def rank(a): return (not a.get("featured"), -(a.get("rating") or 0) * math.log((a.get("reviews_count") or 0) + 2), a["name"].lower())

def put(s, name, block, anchor_re, before=True):
    """Replace an existing marker block, or insert it at anchor."""
    mk = re.compile(rf"\n?[ \t]*<!-- il:{name}:start -->.*?<!-- il:{name}:end -->", re.S)
    block = f"\n    <!-- il:{name}:start -->{block}\n    <!-- il:{name}:end -->"
    if mk.search(s): return mk.sub(lambda m: block, s, count=1)
    m = re.search(anchor_re, s, re.S)
    if not m: return None
    i = m.start() if before else m.end()
    return s[:i] + block + s[i:]

def mini_card(a):
    r = f'<span class="rel-rating">★ {a["rating"]:.1f}</span>' if a.get("rating") else ""
    return (f'\n          <a class="rel-card" href="/{a["city_slug"]}/{a["slug"]}/"><strong>{E(a["name"])}</strong>'
            f'<span>{E(a["category"])} · {E(a["city"])}</span>{r}</a>')

def chip_links(items):
    return '<ul class="link-chips">' + "".join(f'<li><a href="{u}">{E(t)}</a></li>' for u, t in items) + "</ul>"

def related_for(a):
    seen = {(a["city_slug"], a["slug"])}
    out = []
    def add(pool):
        for b in sorted(pool, key=rank):
            k = (b["city_slug"], b["slug"])
            if k in seen: continue
            seen.add(k); out.append(b)
            if len(out) >= 8: return True
    city = by_city[a["city_slug"]]
    if add([b for b in city if b["category_slug"] == a["category_slug"]]): return out
    if add(city): return out
    for c in nearby(a["city_slug"], 12):
        if add([b for b in by_city[c] if b["category_slug"] == a["category_slug"]]): return out
    for c in nearby(a["city_slug"], 12):
        if add(by_city[c]): return out
    return out

def write(p, s):
    open(p, "w", encoding="utf-8").write(s)

# ---------- listing pages ----------
n_list = 0
for a in agencies:
    p = os.path.join(BASE, a["city_slug"], a["slug"], "index.html")
    if not os.path.isfile(p): print("missing listing page", p); continue
    s = open(p, encoding="utf-8").read()
    cs, cn = a["city_slug"], E(a["city"])
    # breadcrumbs: Home > Directory > City > Listing (visible + schema)
    s = s.replace('<a href="/cities/">Cities</a>', '<a href="/cities/">Directory</a>')
    s = s.replace('"position": 2, "name": "Cities"', '"position": 2, "name": "Directory"')
    cat_name = CATS.get(a["category_slug"], a["category"])
    near = nearby(cs, 6)
    rel = "".join(mini_card(b) for b in related_for(a))
    brand = BRAND.get(a["category_slug"], BRAND_DEFAULT)
    block = f'''
    <section class="section related-section">
      <div class="section-head">
        <p class="eyebrow">Keep exploring</p>
        <h2>Similar agencies to {E(a["name"])}</h2>
      </div>
      <div class="rel-grid">{rel}
      </div>
      <div class="explore-grid">
        <div class="explore-col">
          <h3>More in {cn}</h3>
          {chip_links([(f"/{cs}/", f"All marketing agencies in {a['city']}"), (cat_url(a['category_slug']), f"{cat_name} in Georgia"), ("/cities/", "Browse the Georgia directory")])}
        </div>
        <div class="explore-col">
          <h3>Nearby cities</h3>
          {chip_links([(f"/{c}/", f"{city_name[c]} agencies") for c in near])}
        </div>
        <div class="explore-col">
          <h3>Prefer done-for-you?</h3>
          {chip_links(brand + [("/services/", "All Mindful Marketing services")])}
        </div>
      </div>
    </section>'''
    s2 = put(s, "related", block, r"\n\s*</main>")
    if s2 is None: print("no anchor", p); continue
    write(p, s2); n_list += 1

# ---------- full-service category page (cloned from web design template) ----------
fs_dir = os.path.join(BASE, "services", "full-service-digital-marketing-agencies")
tpl = open(os.path.join(BASE, "services", "web-design-agencies", "index.html"), encoding="utf-8").read()
tpl = re.sub(r"\n?[ \t]*<!-- il:\w+:start -->.*?<!-- il:\w+:end -->", "", tpl, flags=re.S)
fs = (tpl.replace("web-design-agencies", "full-service-digital-marketing-agencies")
         .replace("Web Design Agencies", "Full-Service Digital Marketing Agencies")
         .replace("web design agencies", "full-service digital marketing agencies"))
os.makedirs(fs_dir, exist_ok=True)
if not os.path.isfile(os.path.join(fs_dir, "index.html")):
    write(os.path.join(fs_dir, "index.html"), fs)

# ---------- category pages ----------
n_cat = 0
for slug, name in CATS.items():
    p = os.path.join(BASE, "services", slug, "index.html")
    if not os.path.isfile(p): continue
    s = open(p, encoding="utf-8").read()
    items = by_cat.get(slug, [])
    groups = {}
    for a in sorted(items, key=rank): groups.setdefault(a["city_slug"], []).append(a)
    order = sorted(groups, key=lambda c: (-len(groups[c]), city_name[c]))
    body = "".join(
        f'\n        <div class="cat-city"><h3><a href="/{c}/">{E(city_name[c])}</a> <small>{len(groups[c])}</small></h3><ul>'
        + "".join(f'<li><a href="/{c}/{a["slug"]}/">{E(a["name"])}</a></li>' for a in groups[c]) + "</ul></div>"
        for c in order)
    top_cities = sorted(by_city, key=lambda c: -len(by_city[c]))[:12]
    others = [(cat_url(k), v) for k, v in CATS.items() if k != slug and by_cat.get(k)]
    if items:
        lead = f'<h2>All {len(items)} {E(name.lower())} listed in Georgia, by city</h2>\n      <div class="cat-city-grid">{body}\n      </div>'
    else:
        lead = f'<h2>{E(name)} in Georgia</h2>\n      <p>No agencies are listed in this category yet. Browse a city below, or <a href="/submit/">add your agency</a>.</p>'
    block = f'''
    <section class="section">
      {lead}
      <div class="explore-grid">
        <div class="explore-col"><h3>Top cities</h3>{chip_links([(f"/{c}/", city_name[c]) for c in top_cities] + [("/cities/", "All cities →")])}</div>
        <div class="explore-col"><h3>Other categories</h3>{chip_links(others)}</div>
      </div>
    </section>'''
    s2 = put(s, "category", block, r"\n\s*<section class=\"section\">\s*<div class=\"claim-banner\">")
    if s2 is None: print("no anchor", p); continue
    write(p, s2); n_cat += 1

# ---------- city pages ----------
n_city = 0
for c in by_city:
    p = os.path.join(BASE, c, "index.html")
    if not os.path.isfile(p): continue
    s = open(p, encoding="utf-8").read()
    if "data-listings" not in s: continue
    cats_here = {}
    for a in by_city[c]: cats_here[a["category_slug"]] = cats_here.get(a["category_slug"], 0) + 1
    cat_links = [(f"/{c}/?category={k}", f"{CATS.get(k,k)} in {city_name[c]} ({n})") for k, n in sorted(cats_here.items(), key=lambda x: -x[1])]
    cat_links += [(cat_url(k), f"{v} statewide") for k, v in CATS.items() if by_cat.get(k)]
    block = f'''
    <section class="section">
      <div class="explore-grid">
        <div class="explore-col"><h3>Marketing agencies in nearby cities</h3>{chip_links([(f"/{n}/", f"{city_name[n]} ({len(by_city[n])})") for n in nearby(c, 8)])}</div>
        <div class="explore-col"><h3>Top categories</h3>{chip_links(cat_links)}</div>
      </div>
    </section>'''
    anchor = r"<!-- city-static:end -->" if "<!-- city-static:end -->" in s else r"\n\s*</main>"
    s2 = put(s, "nearby", block, anchor, before=(anchor != r"<!-- city-static:end -->"))
    if s2 is None: print("no anchor", p); continue
    write(p, s2); n_city += 1

# ---------- /cities/ and /services/ hubs: static crawlable lists ----------
p = os.path.join(BASE, "cities", "index.html"); s = open(p, encoding="utf-8").read()
lst = "".join(f'<li><a href="/{c}/">{E(city_name[c])}</a> <small>({len(by_city[c])})</small></li>' for c in sorted(by_city, key=lambda c: city_name[c]))
block = f'''
    <section class="section">
      <h2>Every Georgia city in the directory</h2>
      <ul class="area-list city-index">{lst}</ul>
      <h3 style="margin-top:2rem;">Browse by category</h3>
      {chip_links([(cat_url(k), v) for k, v in CATS.items() if by_cat.get(k)])}
    </section>'''
s2 = put(s, "cityindex", block, r"\n\s*</main>"); write(p, s2 or s)
p = os.path.join(BASE, "services", "index.html"); s = open(p, encoding="utf-8").read()
block = f'''
        <div class="explore-grid" style="margin-top:1.5rem;">
          <div class="explore-col"><h3>Directory categories</h3>{chip_links([(cat_url(k), f"{v} ({len(by_cat.get(k, []))})") for k, v in CATS.items()])}</div>
          <div class="explore-col"><h3>Top cities</h3>{chip_links([(f"/{c}/", city_name[c]) for c in sorted(by_city, key=lambda c: -len(by_city[c]))[:12]] + [("/cities/", "All cities →")])}</div>
        </div>'''
s2 = put(s, "catindex", block, r"<div class=\"hub-grid\" data-service-hub></div>", before=False); write(p, s2 or s)

# ---------- /blog/: link standalone guides so they aren't orphaned ----------
p = os.path.join(BASE, "blog", "index.html"); gdir = os.path.join(BASE, "guides")
if os.path.exists(p) and os.path.isdir(gdir):
    items = []
    for g in sorted(os.listdir(gdir)):
        gp = os.path.join(gdir, g, "index.html")
        if os.path.exists(gp):
            m = re.search(r"<h1[^>]*>(.*?)</h1>", open(gp, encoding="utf-8").read(), re.S)
            items.append((f"/guides/{g}/", re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else g.replace("-", " ").title()))
    if items:
        s = open(p, encoding="utf-8").read()
        block = f'''
    <section class="section">
      <h2>Guides</h2>
      {chip_links(items)}
    </section>'''
        s2 = put(s, "guides", block, r"\n\s*</main>"); write(p, s2 or s)
print(f"internal links: {n_list} listings, {n_cat} category pages, {n_city} city pages, hubs updated")
