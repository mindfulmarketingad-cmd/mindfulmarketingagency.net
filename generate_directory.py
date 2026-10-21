#!/usr/bin/env python3
"""
Georgia Marketing Agencies — directory build script.

Run this whenever you import new Outscraper Google Maps data. It:
  1. Reads listings (CSV or JSON) and normalizes them into data/agencies.json
  2. Writes a real static page for every listing at /<city>/<listing>/
  3. Auto-creates a /<city>/ hub page for any new city it discovers
  4. Regenerates /cities/index.html and /services/index.html hub grids
  5. Regenerates sitemap.xml with every URL

City pages live at the site root (/<city>/, not /cities/<city>/) — only the
cities directory listing itself stays at /cities/. Every city and listing
page links back to /cities/ as the "Cities" breadcrumb/nav entry.

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

# Singular, grammatically-safe form for use in prose ("is a ___", not "is a ___s").
CATEGORY_SINGULAR = {
    "seo-agencies": "SEO agency",
    "ppc-paid-media-agencies": "paid media agency",
    "social-media-marketing-agencies": "social media marketing agency",
    "web-design-agencies": "web design agency",
    "branding-graphic-design-agencies": "branding and graphic design agency",
    "content-marketing-agencies": "content marketing agency",
    "email-marketing-agencies": "email marketing agency",
    "full-service-digital-marketing-agencies": "full-service digital marketing agency",
}

# Generic terms that show up on almost every Google Maps listing and add no
# differentiating signal — excluded from specialty lists and "about" copy.
GENERIC_SUBTYPES = {"marketing agency", "marketing consultant"}

# The three main service branches live at the site root; the rest stay
# nested under /services/. Keep in sync with directory.js's CATEGORIES list.
CATEGORY_PATHS = {
    "seo-agencies": "/seo/",
    "social-media-marketing-agencies": "/social-media-marketing/",
    "full-service-digital-marketing-agencies": "/digital-marketing/",
}


def category_path(slug):
    return CATEGORY_PATHS.get(slug, f"/services/{slug}/")

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


def parse_subtypes(raw):
    """Outscraper's subtypes column: a comma-separated string of Google
    business types, usually far more specific than the generic category/type
    column. Returns a clean list, e.g. ['Advertising agency', 'Branding agency']."""
    if not raw:
        return []
    parts = [p.strip() for p in str(raw).split(",")]
    return [p for p in parts if p]


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
            if k in row and row[k] not in (None, ""):
                return row[k]
        return ""

    name = get("name", "Name")
    state_code = str(get("state_code", "State", "state")).strip().upper()
    city_slug, city_name = map_city(get("city", "City"))
    subtypes = parse_subtypes(get("subtypes"))
    # subtypes carry far more specific signal than the generic "type"/
    # "category" column (e.g. "Marketing agency" tells us nothing, but
    # "Branding agency, Website designer" does) — combine both for matching.
    category_text = " ".join([str(get("category", "type", "Category", "Type"))] + subtypes)
    category_slug, category_name = map_category(category_text)

    rating = get("rating", "Rating")
    try:
        rating = float(rating) if rating not in ("", None) else None
    except (ValueError, TypeError):
        rating = None

    reviews = get("reviews", "reviews_count", "Reviews")
    try:
        reviews = int(float(reviews)) if reviews not in ("", None) else None
    except (ValueError, TypeError):
        reviews = None

    hours_raw = get("working_hours", "hours", "Hours")
    hours = None
    if hours_raw:
        hours_obj = hours_raw if isinstance(hours_raw, dict) else None
        if hours_obj is None:
            try:
                hours_obj = json.loads(hours_raw)
            except Exception:
                hours_obj = None
        if hours_obj and isinstance(hours_obj, dict):
            # Values can be lists like ["8AM-5PM"] — flatten to plain strings.
            hours = {}
            for day, val in hours_obj.items():
                if isinstance(val, list):
                    hours[day] = ", ".join(str(v) for v in val)
                else:
                    hours[day] = str(val)
        elif hours_obj is None and isinstance(hours_raw, str):
            hours = {"Hours": hours_raw}

    photo = get("photo", "street_view")
    logo = get("logo")
    reviews_per_score = get("reviews_per_score")
    if isinstance(reviews_per_score, str):
        try:
            reviews_per_score = json.loads(reviews_per_score)
        except Exception:
            reviews_per_score = None

    return {
        "name": name,
        "slug": slugify(name),
        "state_code": state_code,
        "category": category_name,
        "category_slug": category_slug,
        "subtypes": subtypes,
        "city": city_name,
        "city_slug": city_slug,
        "address": get("full_address", "address", "Address"),
        "phone": get("phone", "phone_1", "Phone"),
        "website": get("site", "website", "Website"),
        "rating": rating,
        "reviews_count": reviews,
        "reviews_per_score": reviews_per_score if isinstance(reviews_per_score, dict) else None,
        "hours": hours,
        "photo": photo,
        "logo": logo,
        "photos_count": get("photos_count"),
        "business_status": get("business_status"),
        # NOTE: Outscraper's "about" column is a structured JSON blob of
        # accessibility features (e.g. {"Accessibility": {...}}), not prose —
        # never use it as a description. Only "description" ever holds real
        # text, and even that's rare; the real bio gets generated below.
        "description": get("description", "Description"),
        "place_id": get("place_id", "placeId"),
        "featured": False,
    }


def load_rows(path, fmt):
    if fmt == "json":
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    if fmt == "xlsx":
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb[wb.sheetnames[0]]
        rows_iter = ws.iter_rows(values_only=True)
        header = [str(h) if h is not None else "" for h in next(rows_iter)]
        rows = []
        for r in rows_iter:
            rows.append({header[i]: r[i] for i in range(len(header)) if i < len(r)})
        return rows
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
        <li><a href="/lists/">Lists</a></li>
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
        <a href="/lists/">Lists</a>
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


def join_oxford(items):
    items = list(items)
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"


def specialties_for(a, limit=4):
    """Specialty list for display/content, preferring subtypes (specific)
    over the generic category, and never repeating the category itself or
    generic terms like "Marketing agency" that appear on nearly every
    listing and add no differentiating signal."""
    cat = (a.get("category") or "").strip()
    seen = set()
    out = []
    for s in a.get("subtypes") or []:
        s = s.strip()
        if not s or s.lower() == cat.lower() or s.lower() in seen or s.lower() in GENERIC_SUBTYPES:
            continue
        seen.add(s.lower())
        out.append(s)
        if len(out) >= limit:
            break
    if not out and cat:
        out = [cat]
    return out


def stable_pick(options, *seed_parts):
    """Deterministic pseudo-random pick so re-running the generator on the
    same data always yields the same variant (idempotent builds)."""
    seed = "|".join(str(p) for p in seed_parts)
    h = 0
    for ch in seed:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return options[h % len(options)]


def summarize_hours(hours):
    if not hours:
        return None
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_ranges = [hours.get(d) for d in days_order[:5] if hours.get(d)]
    weekday_open = [r for r in weekday_ranges if r and "closed" not in r.lower()]
    if weekday_open and len(set(weekday_open)) == 1 and len(weekday_open) >= 4:
        return f"Monday–Friday, {weekday_open[0]}"
    return None


def about_us_html(a):
    specialties = specialties_for(a)
    specialties_str = join_oxford([s.lower() for s in specialties]) if specialties else (a.get("category") or "marketing").lower()
    cat_lower = CATEGORY_SINGULAR.get(a.get("category_slug"), "marketing agency")

    rating_sentence = ""
    if a.get("rating"):
        rating_sentence = f' The business holds a {a["rating"]:.1f}-star rating on Google from {a.get("reviews_count") or 0} review{"s" if (a.get("reviews_count") or 0) != 1 else ""}.'

    templates = [
        f"{a['name']} is a {cat_lower} based in {a['city']}, GA, specializing in {specialties_str}.{rating_sentence}",
        f"Based in {a['city']}, Georgia, {a['name']} offers {specialties_str}.{rating_sentence}",
        f"{a['name']} serves {a['city']} and the surrounding area, with a focus on {specialties_str}.{rating_sentence}",
        f"Clients in {a['city']}, GA turn to {a['name']} for {specialties_str}.{rating_sentence}",
        f"{a['name']} is a {cat_lower} listed in the Georgia Marketing Agencies directory, specializing in {specialties_str}.{rating_sentence}",
    ]
    return stable_pick(templates, a.get("place_id") or a["slug"], "about")


def faq_items(a):
    specialties = specialties_for(a)
    specialties_str = join_oxford([s.lower() for s in specialties]) if specialties else (a.get("category") or "marketing").lower()
    items = []

    items.append((
        f"What does {a['name']} specialize in?",
        f"{a['name']} specializes in {specialties_str}."
    ))

    if a.get("address"):
        items.append((
            f"Where is {a['name']} located?",
            f"{a['name']} is located at {a['address']}."
        ))
    else:
        items.append((
            f"Where is {a['name']} located?",
            f"{a['name']} serves the {a['city']}, GA area."
        ))

    hours_summary = summarize_hours(a.get("hours"))
    if hours_summary:
        items.append((
            f"What are {a['name']}'s hours?",
            f"{a['name']} is open {hours_summary}."
        ))
    elif a.get("hours"):
        items.append((
            f"What are {a['name']}'s hours?",
            f"Hours vary by day — see the full hours listed below, or contact {a['name']} directly to confirm."
        ))
    else:
        items.append((
            f"What are {a['name']}'s hours?",
            f"Hours aren't listed for {a['name']} yet — contact them directly to confirm availability."
        ))

    if a.get("rating"):
        items.append((
            f"Is {a['name']} highly rated?",
            f"{a['name']} holds a {a['rating']:.1f}-star rating from {a.get('reviews_count') or 0} Google review{'s' if (a.get('reviews_count') or 0) != 1 else ''}."
        ))
    else:
        items.append((
            f"Is {a['name']} highly rated?",
            f"{a['name']} doesn't yet have a public rating on Google — check back as more customer feedback comes in, or ask them directly for references."
        ))

    contact_bits = []
    if a.get("phone"):
        contact_bits.append(f"by phone at {a['phone']}")
    if a.get("website"):
        contact_bits.append(f"through their website")
    if contact_bits:
        items.append((
            f"How do I contact {a['name']}?",
            f"You can reach {a['name']} {join_oxford(contact_bits)}."
        ))

    return items


def listing_page_html(a):
    url = f"https://mindfulmarketingagency.net/{a['city_slug']}/{a['slug']}/"
    title = f"{a['name']} | {a['city']} Marketing Agency"
    about = a.get("description") or about_us_html(a)
    desc = about[:160]

    stars = ""
    if a.get("rating"):
        full = round(a["rating"])
        stars = f'<div class="listing-rating"><span class="stars">{"★"*full}{"☆"*(5-full)}</span><span class="rating-num">{a["rating"]:.1f}</span>'
        if a.get("reviews_count"):
            stars += f'<span class="review-count">({a["reviews_count"]} review{"" if a["reviews_count"] == 1 else "s"})</span>'
        stars += "</div>"

    hours_html = ""
    if a.get("hours"):
        rows = "".join(f"<tr><td>{esc(d)}</td><td>{esc(h)}</td></tr>" for d, h in a["hours"].items())
        hours_html = f'<li><strong>Hours</strong><table class="hours-table">{rows}</table></li>'

    specialties = specialties_for(a, limit=6)
    specialties_html = ""
    if specialties:
        tags = "".join(f'<span class="tag">{esc(s)}</span>' for s in specialties)
        specialties_html = f'<div class="section" style="padding-top:0;"><h2>What {esc(a["name"])} specializes in</h2><div class="listing-meta" style="gap:.5rem .6rem;">{tags}</div></div>'

    logo_html = f'<img class="listing-logo" src="{esc(a["logo"])}" alt="{esc(a["name"])} logo" width="56" height="56" loading="lazy" />' if a.get("logo") else ""
    photo_html = f'<img class="listing-cover" src="{esc(a["photo"])}" alt="{esc(a["name"])} — photo" loading="lazy" />' if a.get("photo") else ""

    status_badge = ""
    status = (a.get("business_status") or "").upper()
    if status and status != "OPERATIONAL":
        label = "Temporarily closed" if "TEMP" in status else ("Permanently closed" if "PERM" in status else status.title())
        status_badge = f'<span class="listing-featured-tag" style="background:#d9534f;color:#fff;">{esc(label)}</span>'

    faqs = faq_items(a)
    faq_html = "".join(
        f'<details class="faq-item"><summary>{esc(q)}</summary><p class="faq-answer">{esc(ans)}</p></details>'
        for q, ans in faqs
    )
    faq_schema_items = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}}
        for q, ans in faqs
    ]

    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": a["name"],
        "image": a.get("photo") or a.get("logo") or None,
        "description": about,
        "address": a.get("address") or f"{a['city']}, GA",
        "telephone": a.get("phone") or None,
        "url": a.get("website") or None,
        "aggregateRating": ({"@type": "AggregateRating", "ratingValue": a["rating"], "reviewCount": a.get("reviews_count") or 0} if a.get("rating") else None),
    }
    schema = {k: v for k, v in schema.items() if v is not None}

    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema_items}

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
  {f'<meta property="og:image" content="{esc(a["photo"])}" />' if a.get("photo") else ''}
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  <script type="application/ld+json">{json.dumps(schema)}</script>
  <script type="application/ld+json">{json.dumps(faq_schema)}</script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://mindfulmarketingagency.net/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Cities", "item": "https://mindfulmarketingagency.net/cities/" }},
      {{ "@type": "ListItem", "position": 3, "name": "{esc(a['city'])}", "item": "https://mindfulmarketingagency.net/{a['city_slug']}/" }},
      {{ "@type": "ListItem", "position": 4, "name": "{esc(a['name'])}", "item": "{url}" }}
    ]
  }}
  </script>
</head>
<body>
{HEADER_NAV}
  <main>
    {photo_html}
    <section class="section">
      <div class="listing-detail">
        <p class="crumbs"><a href="/">Home</a> / <a href="/cities/">Cities</a> / <a href="/{a['city_slug']}/">{esc(a['city'])}</a> / {esc(a['name'])}</p>
        <div class="listing-detail-head">
          <div style="display:flex;gap:1rem;align-items:flex-start;">
            {logo_html}
            <div>
              <h1 style="margin-bottom:.3rem;">{esc(a['name'])} {status_badge}</h1>
              {stars}
              <div class="listing-meta">
                <span class="tag">{esc(a['category'])}</span>
                <span>{esc(a['city'])}, GA</span>
              </div>
            </div>
          </div>
          {f'<a class="btn btn-primary" href="{esc(a["website"])}" target="_blank" rel="noopener">Visit website</a>' if a.get("website") else ''}
        </div>
        <div class="detail-grid">
          <div>
            <h2>About {esc(a['name'])}</h2>
            <p>{esc(about)}</p>
          </div>
          <div class="detail-card">
            <h4>Contact &amp; details</h4>
            <ul class="detail-list">
              {f'<li><strong>Address</strong>{esc(a["address"])}</li>' if a.get("address") else ''}
              {f'<li><strong>Phone</strong><a href="tel:{esc(a["phone"])}">{esc(a["phone"])}</a></li>' if a.get("phone") else ''}
              {f'<li><strong>Website</strong><a href="{esc(a["website"])}" target="_blank" rel="noopener">{esc(a["website"])}</a></li>' if a.get("website") else ''}
              {hours_html}
              {f'<li><strong>Photos</strong>{esc(str(a["photos_count"]))} on Google</li>' if a.get("photos_count") else ''}
            </ul>
          </div>
        </div>
      </div>
    </section>
    {specialties_html}
    <section class="section" style="max-width:900px;">
      <h2>Frequently asked questions</h2>
      <div class="faq-list">{faq_html}</div>
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
        f'<a class="hub-card" href="/{slug}/"><h3>{name}</h3><span class="count">Marketing agencies in {name}</span></a>'
        for slug, name in cities
    )
    return cards


def write_city_shell(city_slug, city_name):
    """Write the city hub (browse) page if it doesn't already exist."""
    path = os.path.join(BASE, city_slug, "index.html")
    if os.path.exists(path):
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    url = f"https://mindfulmarketingagency.net/{city_slug}/"
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
        ("/lists/", "0.8", "weekly"),
        ("/about/", "0.6", "monthly"),
        ("/submit/", "0.6", "monthly"),
    ]
    # /seo/, /digital-marketing/, /social-media-marketing/ are covered below
    # via category_path(), since those slugs now resolve to root URLs.
    for slug, _ in KNOWN_CITIES_LIST:
        static_urls.append((f"/{slug}/", "0.8", "weekly"))
    for slug in extra_cities:
        static_urls.append((f"/{slug}/", "0.8", "weekly"))
    for slug, _, _ in CATEGORY_KEYWORDS:
        static_urls.append((category_path(slug), "0.8", "weekly"))
    static_urls.append((category_path(DEFAULT_CATEGORY[0]), "0.8", "weekly"))

    import datetime
    today = datetime.date.today().isoformat()

    entries = []
    for path, priority, freq in static_urls:
        entries.append(f"  <url>\n    <loc>https://mindfulmarketingagency.net{path}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{priority}</priority>\n  </url>")
    for a in agencies:
        loc = f"https://mindfulmarketingagency.net/{a['city_slug']}/{a['slug']}/"
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
    parser.add_argument("input", help="Path to Outscraper CSV/XLSX export or normalized JSON")
    parser.add_argument("--format", choices=["csv", "json", "xlsx"], default=None, help="Defaults to the input file's extension")
    parser.add_argument("--merge", action="store_true", help="Merge with existing data/agencies.json instead of replacing it")
    args = parser.parse_args()

    fmt = args.format
    if fmt is None:
        ext = os.path.splitext(args.input)[1].lower().lstrip(".")
        fmt = ext if ext in ("csv", "json", "xlsx") else "csv"

    rows = load_rows(args.input, fmt)
    if fmt == "json":
        agencies = rows  # assume already normalized
    else:
        agencies = [normalize_row(r) for r in rows]

    # This is a Georgia-only directory — drop listings outside GA (Outscraper
    # search radii sometimes pick up a few out-of-state businesses).
    before = len(agencies)
    agencies = [a for a in agencies if not a.get("state_code") or a["state_code"] == "GA"]
    dropped = before - len(agencies)
    if dropped:
        print(f"dropped {dropped} non-Georgia listing(s)")

    agencies = dedupe_slugs(agencies)

    # Generate each agency's "description" (used for card previews and the
    # listing page's About section) from verified data fields — never
    # fabricated. Only for freshly-normalized rows; JSON input is assumed
    # to already carry a real description.
    if fmt != "json":
        for a in agencies:
            if not a.get("description"):
                a["description"] = about_us_html(a)

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
        page_dir = os.path.join(BASE, a["city_slug"], a["slug"])
        os.makedirs(page_dir, exist_ok=True)
        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(listing_page_html(a))
    print(f"wrote {len(agencies)} listing pages")

    build_sitemap(agencies, extra_cities.keys())
    print("sitemap.xml updated")
    print("Done. New cities discovered:", list(extra_cities.values()) or "none")


if __name__ == "__main__":
    main()
