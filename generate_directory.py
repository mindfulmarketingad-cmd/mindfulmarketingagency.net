#!/usr/bin/env python3
"""
Georgia Marketing Agencies — directory build script.

Run this whenever you import new Outscraper Google Maps data. It:
  1. Reads listings (CSV or JSON) and normalizes them into data/agencies.json
  2. Writes a real static page for every listing at /cities/<city>/<listing>/
  3. Auto-creates a /cities/<city>/ hub page for any new city it discovers
  4. Regenerates /cities/index.html and /services/index.html hub grids
  5. Regenerates sitemap.xml with every URL

Usage:
  python3 generate_directory.py path/to/outscraper_export.csv
  python3 generate_directory.py path/to/agencies.json --format json

Outscraper CSV columns it understands (common Google Maps export names):
  name, full_address / address, city, phone / phone_1, site / website,
  rating, reviews / reviews_count, category / type, working_hours / hours,
  about / description, place_id

Columns it can't map are ignored — nothing fails if a field is missing.
"""
import csv
import json
import os
import re
import sys
import argparse

BASE = os.path.dirname(os.path.abspath(__file__))

CATEGORY_KEYWORDS = [
    ("seo-agencies", "SEO Agencies", ["seo", "search engine optimization"]),
    ("ppc-paid-media-agencies", "PPC & Paid Media Agencies", ["ppc", "paid media", "paid search", "google ads", "ad agency", "advertising agency"]),
    ("social-media-marketing-agencies", "Social Media Marketing Agencies", ["social media"]),
    ("web-design-agencies", "Web Design Agencies", ["web design", "website design", "web developer", "web development"]),
    ("branding-graphic-design-agencies", "Branding & Graphic Design Agencies", ["branding", "graphic design", "brand"]),
    ("content-marketing-agencies", "Content Marketing Agencies", ["content marketing", "content agency", "copywriting"]),
    ("email-marketing-agencies", "Email Marketing Agencies", ["email marketing"]),
]
DEFAULT_CATEGORY = ("full-service-digital-marketing-agencies", "Full-Service Digital Marketing Agencies")

KNOWN_CITIES = {
    "atlanta": "Atlanta", "savannah": "Savannah", "augusta": "Augusta",
    "columbus": "Columbus", "macon": "Macon", "athens": "Athens",
    "sandy springs": "Sandy Springs", "roswell": "Roswell", "albany": "Albany",
    "warner robins": "Warner Robins",
}


def slugify(text):
    text = (text or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "listing"


def map_category(raw):
    raw_l = (raw or "").lower()
    for slug, name, keywords in CATEGORY_KEYWORDS:
        if any(k in raw_l for k in keywords):
            return slug, name
    return DEFAULT_CATEGORY


def map_city(raw):
    raw_clean = (raw or "").strip()
    raw_l = raw_clean.lower().replace(", ga", "").replace(" georgia", "").strip()
    if raw_l in KNOWN_CITIES:
        return slugify(raw_l), KNOWN_CITIES[raw_l]
    if not raw_clean:
        return "other", "Other"
    return slugify(raw_clean), raw_clean.title()


def normalize_row(row):
    def get(*keys):
        for k in keys:
            if k in row and row[k]:
                return row[k]
        return ""

    name = get("name", "Name")
    city_slug, city_name = map_city(get("city", "City"))
    category_slug, category_name = map_category(get("category", "type", "Category", "Type"))

    rating = get("rating", "Rating")
    try:
        rating = float(rating) if rating not in ("", None) else None
    except ValueError:
        rating = None

    reviews = get("reviews", "reviews_count", "Reviews")
    try:
        reviews = int(float(reviews)) if reviews not in ("", None) else None
    except ValueError:
        reviews = None

    hours_raw = get("working_hours", "hours", "Hours")
    hours = None
    if hours_raw:
        if isinstance(hours_raw, dict):
            hours = hours_raw
        else:
            try:
                hours = json.loads(hours_raw)
            except Exception:
                hours = {"Hours": hours_raw}

    return {
        "name": name,
        "slug": slugify(name),
        "category": category_name,
        "category_slug": category_slug,
        "city": city_name,
        "city_slug": city_slug,
        "address": get("full_address", "address", "Address"),
        "phone": get("phone", "phone_1", "Phone"),
        "website": get("site", "website", "Website"),
        "rating": rating,
        "reviews_count": reviews,
        "hours": hours,
        "description": get("about", "description", "Description"),
        "place_id": get("place_id", "placeId"),
        "featured": False,
    }


def load_rows(path, fmt):
    if fmt == "json":
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def dedupe_slugs(agencies):
    seen = {}
    for a in agencies:
        key = (a["city_slug"], a["slug"])
        if key in seen:
            seen[key] += 1
            a["slug"] = f'{a["slug"]}-{seen[key]}'
        else:
            seen[key] = 1
    return agencies


HEADER_NAV = '''  <header class="site-header" id="top">
    <a class="brand" href="/" aria-label="Georgia Marketing Agencies home">
      <img src="/assets/favicon.svg" alt="Georgia Marketing Agencies" width="40" height="40" />
      <span class="brand-name">Georgia Marketing <span class="accent">Agencies</span></span>
    </a>
    <nav class="nav" aria-label="Primary">
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu" aria-label="Toggle menu">
        <span></span><span></span><span></span>
      </button>
      <ul id="nav-menu" class="nav-menu">
        <li><a href="/cities/">Cities</a></li>
        <li><a href="/services/">Services</a></li>
        <li><a href="/about/">About</a></li>
        <li><a href="/submit/" class="nav-cta">Add your agency</a></li>
      </ul>
    </nav>
  </header>'''

FOOTER = '''  <footer class="site-footer">
    <div class="footer-inner">
      <a class="brand small" href="/">
        <img src="/assets/favicon.svg" alt="" width="36" height="36" />
        <span>Georgia Marketing Agencies</span>
      </a>
      <p class="footer-note">A directory of marketing agencies across the state of Georgia.</p>
      <nav class="footer-nav" aria-label="Footer">
        <a href="/">Home</a>
        <a href="/cities/">Cities</a>
        <a href="/services/">Services</a>
        <a href="/about/">About</a>
        <a href="/submit/">Add your agency</a>
      </nav>
      <ul class="socials" aria-label="Social media">
        <li><a href="#" aria-label="Instagram" rel="noopener"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg></a></li>
        <li><a href="#" aria-label="Facebook" rel="noopener"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M14 9h3V6h-3c-2.2 0-4 1.8-4 4v2H7v3h3v6h3v-6h3l1-3h-4v-2c0-.6.4-1 1-1z"/></svg></a></li>
        <li><a href="#" aria-label="X (Twitter)" rel="noopener"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M17.5 3h3l-6.6 7.5L21.7 21h-5.9l-4.2-5.5L6.6 21H3.5l7-8L2.9 3h6l3.8 5L17.5 3zm-1 16h1.6L8.1 4.7H6.4L16.5 19z"/></svg></a></li>
      </ul>
      <p class="copyright">© <span id="year"></span> Georgia Marketing Agencies. All rights reserved.</p>
    </div>
  </footer>'''


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def listing_page_html(a):
    url = f"https://mindfulmarketingagency.net/cities/{a['city_slug']}/{a['slug']}/"
    title = f"{a['name']} | {a['city']} Marketing Agency"
    desc = a.get("description") or f"{a['name']} is a {a['category']} based in {a['city']}, GA."

    stars = ""
    if a.get("rating"):
        full = round(a["rating"])
        stars = f'<div class="listing-rating"><span class="stars">{"★"*full}{"☆"*(5-full)}</span><span class="rating-num">{a["rating"]:.1f}</span>'
        if a.get("reviews_count"):
            stars += f'<span class="review-count">({a["reviews_count"]} reviews)</span>'
        stars += "</div>"

    hours_html = ""
    if a.get("hours"):
        rows = "".join(f"<tr><td>{esc(d)}</td><td>{esc(h)}</td></tr>" for d, h in a["hours"].items())
        hours_html = f'<li><strong>Hours</strong><table class="hours-table">{rows}</table></li>'

    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": a["name"],
        "address": a.get("address") or f"{a['city']}, GA",
        "telephone": a.get("phone") or None,
        "url": a.get("website") or None,
        "aggregateRating": ({"@type": "AggregateRating", "ratingValue": a["rating"], "reviewCount": a.get("reviews_count") or 0} if a.get("rating") else None),
    }
    schema = {k: v for k, v in schema.items() if v is not None}

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="/assets/favicon.svg" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:site_name" content="Georgia Marketing Agencies" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  <script type="application/ld+json">{json.dumps(schema)}</script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://mindfulmarketingagency.net/" }},
      {{ "@type": "ListItem", "position": 2, "name": "{esc(a['city'])}", "item": "https://mindfulmarketingagency.net/cities/{a['city_slug']}/" }},
      {{ "@type": "ListItem", "position": 3, "name": "{esc(a['name'])}", "item": "{url}" }}
    ]
  }}
  </script>
</head>
<body>
{HEADER_NAV}
  <main>
    <section class="section">
      <div class="listing-detail">
        <p class="crumbs"><a href="/">Home</a> / <a href="/cities/">Cities</a> / <a href="/cities/{a['city_slug']}/">{esc(a['city'])}</a> / {esc(a['name'])}</p>
        <div class="listing-detail-head">
          <div>
            <h1>{esc(a['name'])}</h1>
            {stars}
            <div class="listing-meta">
              <span class="tag">{esc(a['category'])}</span>
              <span>{esc(a['city'])}, GA</span>
            </div>
          </div>
          {f'<a class="btn btn-primary" href="{esc(a["website"])}" target="_blank" rel="noopener">Visit website</a>' if a.get("website") else ''}
        </div>
        <div class="detail-grid">
          <div>
            <p>{esc(a.get("description") or "No description available yet for this listing.")}</p>
          </div>
          <div class="detail-card">
            <h4>Contact &amp; details</h4>
            <ul class="detail-list">
              {f'<li><strong>Address</strong>{esc(a["address"])}</li>' if a.get("address") else ''}
              {f'<li><strong>Phone</strong><a href="tel:{esc(a["phone"])}">{esc(a["phone"])}</a></li>' if a.get("phone") else ''}
              {f'<li><strong>Website</strong><a href="{esc(a["website"])}" target="_blank" rel="noopener">{esc(a["website"])}</a></li>' if a.get("website") else ''}
              {hours_html}
            </ul>
          </div>
        </div>
      </div>
    </section>
  </main>
{FOOTER}
  <script src="/script.js"></script>
  <script src="/directory.js"></script>
</body>
</html>
'''


def city_hub_card_grid(cities):
    cards = "\n".join(
        f'<a class="hub-card" href="/cities/{slug}/"><h3>{name}</h3><span class="count">Marketing agencies in {name}</span></a>'
        for slug, name in cities
    )
    return cards


def write_city_shell(city_slug, city_name):
    """Write the city hub (browse) page if it doesn't already exist."""
    path = os.path.join(BASE, "cities", city_slug, "index.html")
    if os.path.exists(path):
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    url = f"https://mindfulmarketingagency.net/cities/{city_slug}/"
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Marketing Agencies in {city_name}, GA</title>
  <meta name="description" content="Browse top-rated marketing agencies in {city_name}, Georgia." />
  <link rel="canonical" href="{url}" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="/assets/favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
</head>
<body>
{HEADER_NAV}
  <main>
    <section class="page-hero">
      <div class="page-hero-inner">
        <p class="crumbs"><a href="/">Home</a> / <a href="/cities/">Cities</a> / {city_name}</p>
        <p class="eyebrow">Browse by Location</p>
        <h1>Marketing Agencies in {city_name}, Georgia</h1>
        <p class="lead">Compare marketing agencies based in or serving {city_name}, GA.</p>
      </div>
    </section>
    <section class="section">
      <div class="filter-bar">
        <select id="category-filter" aria-label="Filter by service"><option value="">All services</option></select>
        <span class="result-count" data-result-count></span>
      </div>
      <div data-listings></div>
    </section>
  </main>
{FOOTER}
  <script src="/script.js"></script>
  <script src="/directory.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      const categorySelect = document.getElementById('category-filter');
      (GAMDirectory.CATEGORIES || []).forEach(c => {{
        const opt = document.createElement('option');
        opt.value = c.slug; opt.textContent = c.name;
        categorySelect.appendChild(opt);
      }});
      function load() {{
        const catObj = (GAMDirectory.CATEGORIES || []).find(c => c.slug === categorySelect.value);
        GAMDirectory.renderListings('[data-listings]', {{ city: '{city_name}', category: catObj ? catObj.name : undefined }});
      }}
      categorySelect.addEventListener('change', load);
      load();
    }});
  </script>
</body>
</html>
'''
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("created new city page:", path)


def build_sitemap(agencies, extra_cities):
    static_urls = [
        ("/", "1.0", "weekly"),
        ("/cities/", "0.9", "weekly"),
        ("/services/", "0.9", "weekly"),
        ("/about/", "0.6", "monthly"),
        ("/submit/", "0.6", "monthly"),
    ]
    for slug, _ in KNOWN_CITIES_LIST:
        static_urls.append((f"/cities/{slug}/", "0.8", "weekly"))
    for slug in extra_cities:
        static_urls.append((f"/cities/{slug}/", "0.8", "weekly"))
    for slug, _, _ in CATEGORY_KEYWORDS:
        static_urls.append((f"/services/{slug}/", "0.8", "weekly"))
    static_urls.append((f"/services/{DEFAULT_CATEGORY[0]}/", "0.8", "weekly"))

    import datetime
    today = datetime.date.today().isoformat()

    entries = []
    for path, priority, freq in static_urls:
        entries.append(f"  <url>\n    <loc>https://mindfulmarketingagency.net{path}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{priority}</priority>\n  </url>")
    for a in agencies:
        loc = f"https://mindfulmarketingagency.net/cities/{a['city_slug']}/{a['slug']}/"
        entries.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n"
    with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


KNOWN_CITIES_LIST = [
    ("atlanta", "Atlanta"), ("savannah", "Savannah"), ("augusta", "Augusta"),
    ("columbus", "Columbus"), ("macon", "Macon"), ("athens", "Athens"),
    ("sandy-springs", "Sandy Springs"), ("roswell", "Roswell"), ("albany", "Albany"),
    ("warner-robins", "Warner Robins"),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to Outscraper CSV or normalized JSON")
    parser.add_argument("--format", choices=["csv", "json"], default="csv")
    parser.add_argument("--merge", action="store_true", help="Merge with existing data/agencies.json instead of replacing it")
    args = parser.parse_args()

    rows = load_rows(args.input, args.format)
    if args.format == "csv":
        agencies = [normalize_row(r) for r in rows]
    else:
        agencies = rows  # assume already normalized

    agencies = dedupe_slugs(agencies)

    data_path = os.path.join(BASE, "data", "agencies.json")
    if args.merge and os.path.exists(data_path):
        with open(data_path, encoding="utf-8") as f:
            existing = json.load(f)
        existing_keys = {(a["city_slug"], a["slug"]) for a in existing}
        agencies = existing + [a for a in agencies if (a["city_slug"], a["slug"]) not in existing_keys]

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(agencies, f, indent=2)
    print(f"wrote {len(agencies)} listings to data/agencies.json")

    known_slugs = {s for s, _ in KNOWN_CITIES_LIST}
    extra_cities = {}
    for a in agencies:
        if a["city_slug"] not in known_slugs:
            extra_cities[a["city_slug"]] = a["city"]

    for slug, name in extra_cities.items():
        write_city_shell(slug, name)

    for a in agencies:
        page_dir = os.path.join(BASE, "cities", a["city_slug"], a["slug"])
        os.makedirs(page_dir, exist_ok=True)
        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(listing_page_html(a))
    print(f"wrote {len(agencies)} listing pages")

    build_sitemap(agencies, extra_cities.keys())
    print("sitemap.xml updated")
    print("Done. New cities discovered:", list(extra_cities.values()) or "none")


if __name__ == "__main__":
    main()
