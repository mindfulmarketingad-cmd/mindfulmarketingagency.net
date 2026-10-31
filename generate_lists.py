#!/usr/bin/env python3
"""
Georgia Marketing Agencies — programmatic "best of" list pages.

Generates, for each niche x city combination, a real static page at:
  /lists/<niche-slug>/<city-slug>/index.html

titled "Best <Niche> Marketing Agencies in <City>, Georgia — Contact Info
& Services", plus a niche hub at /lists/<niche-slug>/ listing every city.

IMPORTANT — honesty constraint: our data has no verified field for "this
agency specializes in restaurants/gyms/ecommerce/retail". We only know an
agency's general category (SEO, social, web design, etc.) and its Google
subtypes. So each page is built from two honestly-labeled sections:

  1. Agencies whose name/description/subtypes genuinely mention the niche
     (keyword match) — shown first, framed as "with experience in".
  2. Other marketing agencies based in the city — shown as a general
     fallback, explicitly NOT claimed to specialize in the niche.

Never claim a specific business specializes in something we have no
evidence for.

Run this after generate_directory.py (it reads data/agencies.json).

Usage:
  python3 generate_lists.py
"""
import json
import os
import re
from urllib.parse import quote

from generate_directory import HEADER_NAV, FOOTER, esc, slugify, summarize_hours

BASE = os.path.dirname(os.path.abspath(__file__))

# kind = "vertical" (the niche is a type of client business, e.g. gyms,
# restaurants — lead copy reads "help grow a {X} business") or "channel"
# (the niche is a marketing specialty/channel, e.g. SEO, LinkedIn — lead
# copy reads "that specialize in {niche}" instead, since "help grow a
# linkedin business" doesn't make sense).
NICHES = [
    (
        "ecommerce-marketing-agencies",
        "Ecommerce Marketing Agencies",
        "ecommerce marketing agency",
        ["ecommerce", "e-commerce", "shopify", "amazon", "online store", "dtc", "d2c"],
        "vertical",
    ),
    (
        "restaurant-marketing-agencies",
        "Restaurant Marketing Agencies",
        "restaurant marketing agency",
        ["restaurant", "food", "hospitality", "cafe", "café", "catering", "brewery"],
        "vertical",
    ),
    (
        "retail-marketing-agencies",
        "Retail Marketing Agencies",
        "retail marketing agency",
        ["retail", " store", "boutique", "shop"],
        "vertical",
    ),
    (
        "gym-marketing-agencies",
        "Gym Marketing Agencies",
        "gym marketing agency",
        ["gym", "fitness", "health club", "wellness", "yoga", "crossfit"],
        "vertical",
    ),
    (
        "digital-marketing-agencies",
        "Digital Marketing Agencies",
        "digital marketing agency",
        ["digital marketing"],
        "channel",
    ),
    (
        "youtube-marketing-agencies",
        "YouTube Marketing Agencies",
        "youtube marketing agency",
        ["youtube", "video marketing", "video content marketing"],
        "channel",
    ),
    (
        "social-media-marketing-agencies",
        "Social Media Marketing Agencies",
        "social media marketing agency",
        ["social media"],
        "channel",
    ),
    (
        "linkedin-marketing-agencies",
        "LinkedIn Marketing Agencies",
        "linkedin marketing agency",
        ["linkedin", "b2b social media"],
        "channel",
    ),
]


# Exact-match niches: unlike NICHES above (which always publishes a page
# per city, falling back to "other agencies" when there's no genuine
# match), these only publish a page for a city when at least one real
# agency genuinely matches — no page, no fallback section, nothing
# fabricated. Per explicit instruction: only make pages for cities with
# actual agencies offering this service.
EXACT_MATCH_NICHES = [
    (
        "seo-content-marketing-agencies",
        "SEO Content Marketing Agencies",
        "SEO content marketing agency",
        ["seo", "search engine optimization", "content marketing", "content writing", "copywriting"],
    ),
]


def pluralize_agency(phrase):
    """'gym marketing agency' -> 'gym marketing agencies' (not 'agencys')."""
    if phrase.endswith("agency"):
        return phrase[:-len("agency")] + "agencies"
    return phrase + "s"


def article_for(phrase):
    """'a gym marketing agency' vs 'an SEO content marketing agency' —
    based on the first word's leading sound, not just its spelling."""
    first = phrase.split()[0]
    vowel_sound_acronym = first.isupper() and first[:1] in "AEFHILMNORSX"
    if vowel_sound_acronym or first[:1].lower() in "aeiou":
        return "an"
    return "a"


def niche_match(agency, keywords):
    text = " ".join([
        agency.get("name", ""),
        agency.get("description", "") or "",
        agency.get("category", "") or "",
        " ".join(agency.get("subtypes") or []),
    ]).lower()
    return any(k in text for k in keywords)


def stars_html(a):
    if not a.get("rating"):
        return ""
    full = round(a["rating"])
    reviews = a.get("reviews_count") or 0
    return (
        f'<div class="listing-rating"><span class="stars">{"★"*full}{"☆"*(5-full)}</span>'
        f'<span class="rating-num">{a["rating"]:.1f}</span>'
        f'<span class="review-count">({reviews} review{"" if reviews == 1 else "s"})</span></div>'
    )


def list_card_html(a):
    href = f"/{a['city_slug']}/{a['slug']}/"
    hours_summary = summarize_hours(a.get("hours"))
    directions_url = f"https://www.google.com/maps/dir/?api=1&destination={quote(a['address'])}" if a.get("address") else None

    bits = []
    if a.get("address"):
        bits.append(f'<li><strong>Address</strong>{esc(a["address"])}</li>')
    if hours_summary:
        bits.append(f'<li><strong>Hours</strong>{esc(hours_summary)}</li>')
    if a.get("phone"):
        bits.append(f'<li><strong>Phone</strong><a href="tel:{esc(a["phone"])}">{esc(a["phone"])}</a></li>')
    contact_html = f'<ul class="detail-list" style="margin-top:.8rem;">{"".join(bits)}</ul>' if bits else ""

    actions = []
    if directions_url:
        actions.append(f'<a class="btn btn-ghost btn-sm" href="{directions_url}" target="_blank" rel="noopener">Directions</a>')
    if a.get("website"):
        actions.append(f'<a class="btn btn-ghost btn-sm" href="{esc(a["website"])}" target="_blank" rel="noopener">Visit site</a>')
    actions.append(f'<a class="btn btn-ghost btn-sm" href="{href}">Full profile →</a>')
    actions_html = f'<div class="listing-actions">{"".join(actions)}</div>'

    return f'''
      <div class="listing-card" style="cursor:default;">
        <div class="listing-top">
          <h3><a href="{href}">{esc(a['name'])}</a></h3>
        </div>
        {stars_html(a)}
        <div class="listing-meta">
          <span class="tag">{esc(a['category'])}</span>
          <span>{esc(a['city'])}, {esc(a.get('state_code') or 'GA')}</span>
        </div>
        {f'<p class="desc">{esc(a["description"])}</p>' if a.get("description") else ''}
        {contact_html}
        {actions_html}
      </div>'''


def niche_page_html(niche_slug, niche_name, niche_singular, kind, genuine, others, city_slug, city_name, total_in_city):
    url = f"https://www.mindfulmarketingagency.net/lists/{niche_slug}/{city_slug}/"
    title = f"Best {niche_name} in {city_name}, Georgia | Contact Info & Services"
    has_genuine = len(genuine) > 0
    desc = (
        f"Compare {niche_name.lower()} with verified experience in {city_name}, GA — contact info, ratings, and services."
        if has_genuine else
        f"Find marketing agencies in {city_name}, GA that can help with {niche_name.lower().replace(' agencies', '')} — contact info, ratings, and services."
    )

    genuine_html = ""
    if has_genuine:
        genuine_html = f'''
      <section class="section">
        <h2>{esc(niche_name)} with experience in {esc(city_name)}</h2>
        <p style="color:var(--muted);">These agencies list {esc(niche_name.lower().replace(" agencies", ""))}-related work or specialties.</p>
        <div class="listing-grid">{"".join(list_card_html(a) for a in genuine)}</div>
      </section>'''

    others_shown = others[:12]
    more_count = len(others) - len(others_shown)
    others_html = ""
    if others_shown:
        heading = "Other marketing agencies in " + esc(city_name) if has_genuine else "Marketing agencies in " + esc(city_name)
        note = (
            f"We don't have agencies specifically verified for {esc(niche_name.lower().replace(' agencies',''))} in {esc(city_name)} yet — "
            f"here are general marketing agencies based there that may be able to help."
            if not has_genuine else
            f"These agencies aren't specifically tagged for {esc(niche_name.lower().replace(' agencies',''))}, but offer general marketing services and may still be a fit."
        )
        more_link = f'<p style="margin-top:1rem;"><a class="btn btn-ghost" href="/{city_slug}/">See all {total_in_city} agencies in {esc(city_name)} →</a></p>' if more_count > 0 else ""
        others_html = f'''
      <section class="section" style="background:var(--paper);max-width:none;">
        <div style="max-width:var(--maxw);margin:0 auto;">
          <h2>{heading}</h2>
          <p style="color:var(--muted);">{note}</p>
          <div class="listing-grid">{"".join(list_card_html(a) for a in others_shown)}</div>
          {more_link}
        </div>
      </section>'''

    faqs = [
        (
            f"Are there {pluralize_agency(niche_singular)} based in {city_name}, GA?",
            (f"Yes — {city_name} has {len(genuine)} agenc{'y' if len(genuine)==1 else 'ies'} in this directory with listed {niche_name.lower().replace(' agencies','')}-related experience."
             if has_genuine else
             f"We don't yet have an agency in {city_name} specifically verified for {niche_name.lower().replace(' agencies','')} — check the general marketing agencies below, or check back as the directory grows.")
        ),
        (
            f"How much does {article_for(niche_singular)} {niche_singular} cost?",
            f"Pricing varies widely by agency, scope, and ongoing vs. one-time work — contact agencies directly for quotes based on your specific needs."
        ),
        (
            f"What should I look for in {article_for(niche_singular)} {niche_singular}?",
            f"Look for relevant experience, clear communication, transparent reporting, and client reviews. Ask for examples of past work in your industry before committing."
        ),
        (
            "How do I get my agency listed here?",
            'Add your agency to the directory for free at <a href="/submit/">mindfulmarketingagency.net/submit/</a> — submissions are reviewed before going live.'
        ),
    ]
    faq_html = "".join(
        f'<details class="faq-item"><summary>{esc(q)}</summary><p class="faq-answer">{a}</p></details>'
        for q, a in faqs
    )
    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}}
            for q, a in faqs
        ],
    }

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#1E3A8A" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:site_name" content="Mindful Marketing Agency" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  <script type="application/ld+json">{json.dumps(faq_schema)}</script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.mindfulmarketingagency.net/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Lists", "item": "https://www.mindfulmarketingagency.net/lists/" }},
      {{ "@type": "ListItem", "position": 3, "name": "{esc(niche_name)}", "item": "https://www.mindfulmarketingagency.net/lists/{niche_slug}/" }},
      {{ "@type": "ListItem", "position": 4, "name": "{esc(city_name)}", "item": "{url}" }}
    ]
  }}
  </script>
</head>
<body>
{HEADER_NAV}
  <main>
    <section class="page-hero">
      <div class="page-hero-inner">
        <p class="crumbs"><a href="/">Home</a> / <a href="/lists/">Lists</a> / <a href="/lists/{niche_slug}/">{esc(niche_name)}</a> / {esc(city_name)}</p>
        <p class="eyebrow">Best Of · {esc(city_name)}, GA</p>
        <h1>Best {esc(niche_name)} in {esc(city_name)}, Georgia</h1>
        <p class="lead">
          {
            f"Contact info, services, and ratings for marketing agencies in {esc(city_name)}, GA that can help grow {article_for(niche_singular.replace(' marketing agency',''))} {esc(niche_singular.replace(' marketing agency',''))} business."
            if kind == "vertical" else
            f"Contact info, services, and ratings for marketing agencies in {esc(city_name)}, GA that specialize in {esc(niche_name.lower().replace(' agencies', ''))}."
          }
        </p>
      </div>
    </section>
    {genuine_html}
    {others_html}
    <section class="section" style="max-width:820px;">
      <h2>Frequently asked questions</h2>
      <div class="faq-list">{faq_html}</div>
    </section>
    <section class="section">
      <div class="claim-banner">
        <h2>Run {article_for(niche_singular)} {esc(niche_singular)} in {esc(city_name)}?</h2>
        <p>Add your agency to the directory for free — it takes less than five minutes.</p>
        <a class="btn btn-primary btn-lg" href="/submit/">Add your agency</a>
      </div>
    </section>
  </main>
{FOOTER}
  <script src="/script.js"></script>
  <script src="/directory.js"></script>
</body>
</html>
'''


def niche_hub_html(niche_slug, niche_name, cities):
    url = f"https://www.mindfulmarketingagency.net/lists/{niche_slug}/"
    title = f"Best {niche_name} in Georgia by City"
    desc = f"Find {niche_name.lower()} across Georgia — browse by city for contact info, services, and ratings."
    city_links = "".join(
        f'<a href="/lists/{niche_slug}/{slug}/">{esc(name)}, GA</a>'
        for slug, name in cities
    )
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#1E3A8A" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:site_name" content="Mindful Marketing Agency" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.mindfulmarketingagency.net/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Lists", "item": "https://www.mindfulmarketingagency.net/lists/" }},
      {{ "@type": "ListItem", "position": 3, "name": "{esc(niche_name)}", "item": "{url}" }}
    ]
  }}
  </script>
</head>
<body>
{HEADER_NAV}
  <main>
    <section class="page-hero">
      <div class="page-hero-inner">
        <p class="crumbs"><a href="/">Home</a> / <a href="/lists/">Lists</a> / {esc(niche_name)}</p>
        <p class="eyebrow">Best Of</p>
        <h1>Best {esc(niche_name)} in Georgia by City</h1>
        <p class="lead">Select a city to see agencies with contact info, services, and ratings.</p>
      </div>
    </section>
    <section class="section">
      <div class="text-link-list">{city_links}</div>
    </section>
  </main>
{FOOTER}
  <script src="/script.js"></script>
</body>
</html>
'''


def exact_niche_page_html(niche_slug, niche_name, niche_singular, agencies, city_slug, city_name):
    """Page for an exact-match niche — only ever written when `agencies`
    is non-empty, and shows only those genuine matches (no fallback
    section of unrelated agencies)."""
    url = f"https://www.mindfulmarketingagency.net/lists/{niche_slug}/{city_slug}/"
    title = f"Best {niche_name} in {city_name}, Georgia | Contact Info & Services"
    desc = f"Compare {niche_name.lower()} in {city_name}, GA with real SEO and content marketing experience — contact info, ratings, and services."
    agencies_sorted = sorted(agencies, key=lambda a: -(a.get("rating") or 0))

    faqs = [
        (
            f"Are there {pluralize_agency(niche_singular)} based in {city_name}, GA?",
            f"Yes — {city_name} has {len(agencies_sorted)} agenc{'y' if len(agencies_sorted)==1 else 'ies'} in this directory with listed SEO and/or content marketing experience."
        ),
        (
            f"How much does {article_for(niche_singular)} {niche_singular} cost?",
            "Pricing varies by agency, scope, and ongoing vs. one-time work — contact agencies directly for quotes based on your specific needs."
        ),
        (
            f"What should I look for in {article_for(niche_singular)} {niche_singular}?",
            "Look for relevant experience, clear communication, transparent reporting, and client reviews. Ask for examples of past SEO or content work before committing."
        ),
        (
            "How do I get my agency listed here?",
            'Add your agency to the directory for free at <a href="/submit/">mindfulmarketingagency.net/submit/</a> — submissions are reviewed before going live.'
        ),
    ]
    faq_html = "".join(
        f'<details class="faq-item"><summary>{esc(q)}</summary><p class="faq-answer">{a}</p></details>'
        for q, a in faqs
    )
    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}}
            for q, a in faqs
        ],
    }

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#1E3A8A" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:site_name" content="Mindful Marketing Agency" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  <script type="application/ld+json">{json.dumps(faq_schema)}</script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.mindfulmarketingagency.net/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Lists", "item": "https://www.mindfulmarketingagency.net/lists/" }},
      {{ "@type": "ListItem", "position": 3, "name": "{esc(niche_name)}", "item": "https://www.mindfulmarketingagency.net/lists/{niche_slug}/" }},
      {{ "@type": "ListItem", "position": 4, "name": "{esc(city_name)}", "item": "{url}" }}
    ]
  }}
  </script>
</head>
<body>
{HEADER_NAV}
  <main>
    <section class="page-hero">
      <div class="page-hero-inner">
        <p class="crumbs"><a href="/">Home</a> / <a href="/lists/">Lists</a> / <a href="/lists/{niche_slug}/">{esc(niche_name)}</a> / {esc(city_name)}</p>
        <p class="eyebrow">Best Of · {esc(city_name)}, GA</p>
        <h1>Best {esc(niche_name)} in {esc(city_name)}, Georgia</h1>
        <p class="lead">
          Contact info, services, and ratings for marketing agencies in {esc(city_name)}, GA with
          real, listed SEO and content marketing experience.
        </p>
      </div>
    </section>
    <section class="section">
      <div class="listing-grid">{"".join(list_card_html(a) for a in agencies_sorted)}</div>
    </section>
    <section class="section" style="max-width:820px;">
      <h2>Frequently asked questions</h2>
      <div class="faq-list">{faq_html}</div>
    </section>
    <section class="section">
      <div class="claim-banner">
        <h2>Run {article_for(niche_singular)} {esc(niche_singular)} in {esc(city_name)}?</h2>
        <p>Add your agency to the directory for free — it takes less than five minutes.</p>
        <a class="btn btn-primary btn-lg" href="/submit/">Add your agency</a>
      </div>
    </section>
  </main>
{FOOTER}
  <script src="/script.js"></script>
  <script src="/directory.js"></script>
</body>
</html>
'''


RELATED_LISTS_START = "<!-- related-lists:start -->"
RELATED_LISTS_END = "<!-- related-lists:end -->"


def related_lists_block(city_slug, city_name, extra_niches=()):
    links = "".join(
        f'<a href="/lists/{niche_slug}/{city_slug}/">Best {niche_name} in {esc(city_name)}</a>'
        for niche_slug, niche_name, _, _, _ in NICHES
    )
    links += "".join(
        f'<a href="/lists/{niche_slug}/{city_slug}/">Best {niche_name} in {esc(city_name)}</a>'
        for niche_slug, niche_name in extra_niches
    )
    return f'''{RELATED_LISTS_START}
    <section class="section">
      <div class="section-head">
        <p class="eyebrow">Guides &amp; Lists</p>
        <h2>More about marketing agencies in {esc(city_name)}</h2>
      </div>
      <div class="text-link-list">{links}</div>
    </section>
    {RELATED_LISTS_END}'''


def inject_related_lists(by_city, exact_city_niches=None):
    """Link every city page to its niche 'best of' list pages — run after
    the list pages exist so /atlanta/ links to /lists/*/atlanta/ etc.
    exact_city_niches maps city_slug -> [(niche_slug, niche_name), ...]
    for exact-match niches, only added for cities that actually have a
    page (no dead links to cities with no genuine match)."""
    exact_city_niches = exact_city_niches or {}
    updated = 0
    for city_slug, rows in by_city.items():
        path = os.path.join(BASE, city_slug, "index.html")
        if not os.path.exists(path):
            continue
        city_name = rows[0]["city"]
        with open(path, encoding="utf-8") as f:
            content = f.read()
        block = related_lists_block(city_slug, city_name, exact_city_niches.get(city_slug, []))
        if RELATED_LISTS_START in content:
            content = re.sub(
                re.escape(RELATED_LISTS_START) + r".*?" + re.escape(RELATED_LISTS_END),
                block, content, flags=re.S
            )
        elif "</main>" in content:
            content = content.replace("</main>", f"  {block}\n  </main>")
        else:
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        updated += 1
    print(f"linked {updated} city pages to their niche list pages")


def main():
    data_path = os.path.join(BASE, "data", "agencies.json")
    with open(data_path, encoding="utf-8") as f:
        agencies = json.load(f)

    by_city = {}
    for a in agencies:
        by_city.setdefault(a["city_slug"], []).append(a)

    cities = sorted(
        [(slug, rows[0]["city"]) for slug, rows in by_city.items()],
        key=lambda c: c[1]
    )

    list_entries = []
    new_urls = []

    for niche_slug, niche_name, niche_singular, keywords, kind in NICHES:
        for city_slug, city_rows in by_city.items():
            city_name = city_rows[0]["city"]
            genuine = [a for a in city_rows if niche_match(a, keywords)]
            genuine_keys = {a["slug"] for a in genuine}
            others = [a for a in city_rows if a["slug"] not in genuine_keys]
            genuine.sort(key=lambda a: -(a.get("rating") or 0))
            others.sort(key=lambda a: -(a.get("rating") or 0))

            page_dir = os.path.join(BASE, "lists", niche_slug, city_slug)
            os.makedirs(page_dir, exist_ok=True)
            html = niche_page_html(niche_slug, niche_name, niche_singular, kind, genuine, others, city_slug, city_name, len(city_rows))
            with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            new_urls.append(f"/lists/{niche_slug}/{city_slug}/")

        hub_dir = os.path.join(BASE, "lists", niche_slug)
        os.makedirs(hub_dir, exist_ok=True)
        with open(os.path.join(hub_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(niche_hub_html(niche_slug, niche_name, cities))
        new_urls.append(f"/lists/{niche_slug}/")

        list_entries.append({
            "slug": niche_slug,
            "title": f"Best {niche_name} in Georgia",
            "description": f"Browse {niche_name.lower()} by city — contact info, services, and ratings.",
        })

    # Exact-match niches: only write a page for a city when at least one
    # agency genuinely matches — no fallback section, no page at all
    # otherwise.
    exact_city_niches = {}
    for niche_slug, niche_name, niche_singular, keywords in EXACT_MATCH_NICHES:
        qualifying_cities = []
        for city_slug, city_rows in by_city.items():
            city_name = city_rows[0]["city"]
            matches = [a for a in city_rows if niche_match(a, keywords)]
            if not matches:
                continue
            qualifying_cities.append((city_slug, city_name))
            exact_city_niches.setdefault(city_slug, []).append((niche_slug, niche_name))

            page_dir = os.path.join(BASE, "lists", niche_slug, city_slug)
            os.makedirs(page_dir, exist_ok=True)
            html = exact_niche_page_html(niche_slug, niche_name, niche_singular, matches, city_slug, city_name)
            with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            new_urls.append(f"/lists/{niche_slug}/{city_slug}/")

        qualifying_cities.sort(key=lambda c: c[1])
        hub_dir = os.path.join(BASE, "lists", niche_slug)
        os.makedirs(hub_dir, exist_ok=True)
        with open(os.path.join(hub_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(niche_hub_html(niche_slug, niche_name, qualifying_cities))
        new_urls.append(f"/lists/{niche_slug}/")

        list_entries.append({
            "slug": niche_slug,
            "title": f"Best {niche_name} in Georgia",
            "description": f"Browse {niche_name.lower()} by city — contact info, services, and ratings. {len(qualifying_cities)} Georgia cities covered.",
        })
        print(f"{niche_slug}: {len(qualifying_cities)} qualifying cities")

    with open(os.path.join(BASE, "data", "lists.json"), "w", encoding="utf-8") as f:
        json.dump(list_entries, f, indent=2)

    print(f"wrote {len(NICHES)} niche hubs and {len(NICHES) * len(by_city)} city x niche pages")

    # Append new URLs to sitemap.xml (idempotent — skip ones already present).
    sitemap_path = os.path.join(BASE, "sitemap.xml")
    with open(sitemap_path, encoding="utf-8") as f:
        sitemap = f.read()

    import datetime
    today = datetime.date.today().isoformat()
    added = 0
    for path in new_urls:
        loc = f"https://www.mindfulmarketingagency.net{path}"
        if f"<loc>{loc}</loc>" in sitemap:
            continue
        entry = f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n"
        sitemap = sitemap.replace("</urlset>", entry + "</urlset>")
        added += 1
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"added {added} new URLs to sitemap.xml")

    inject_related_lists(by_city, exact_city_niches)


if __name__ == "__main__":
    main()
