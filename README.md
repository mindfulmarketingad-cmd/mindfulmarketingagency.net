# Mindful Marketing Agency (mindfulmarketingagency.net)

Atlanta digital marketing agency site (owned, drop-serviced packages) plus a
free directory of Georgia marketing agencies.

## SEO maintenance checklist

- Canonical host is **https://www.mindfulmarketingagency.net** (the apex 308-redirects to www).
  All canonicals, OG URLs, JSON-LD and the sitemap use the www host.
- After running any generator, run `python3 enhance_city_pages.py` (adds the
  crawlable agency list + our services CTA to every city page) and then
  `python3 generate_sitemap.py` (rebuilds `sitemap.xml` from every page —
  `generate_directory.py`'s own sitemap misses blog/lists/guides/owned pages).
- `vercel.json` holds 301s for the pre-rebuild URLs Google still has indexed
  (`/services/seo/`, `/services/social-media/`, `/guides/...`) and enforces trailing slashes.
- Brand assets: `assets/logo.svg` (header), `assets/logo-white.svg` (footer),
  `assets/favicon.svg`, `/favicon.ico`, `/apple-touch-icon.png`,
  `assets/icon-192.png`, `assets/icon-512.png`, `assets/og-image.png` (1200×630 social share image).
- Don't add fake reviews, ratings, addresses, or stats.

## Selling a package (Stripe "Pay now" buttons)

All fixed-price packages live in **`data/packages.json`** (name, price, Stripe
product/price IDs, Payment Link URL). Buttons are
generated from it by **`python3 pay_buttons.py`**, which fills these markers
in any HTML page:

- `<!-- pay:seo_tier_1 --><!-- /pay -->`: full-width green "Pay now — $49.99" button
- `<!-- payrow:citations_basic,citations_standard --><!-- /payrow -->`: compact row of pay chips

It also writes `pay-links.js`, which `/thank-you/` uses to show what was bought.

**To add a new (e.g. white-labeled) service:**
1. Pick a key (`logo_design_basic`) and price. Rule of thumb: fulfillment cost × 1.2, then round to a
   clean price (e.g. $40 cost → $48 or $49).
2. In Stripe: create a Product + one-time Price, then a Payment Link with name +
   phone collection, `payment_intent_data.statement_descriptor_suffix = "MINDFUL MKTG"`,
   metadata `site=mindfulmarketingagency.net, package=<key>`, and after-completion redirect
   `https://www.mindfulmarketingagency.net/thank-you/?package=<key>&session_id={CHECKOUT_SESSION_ID}`.
3. Add the entry to `data/packages.json` (set `intake`). Keep fulfillment sources and costs in the private fulfillment map, never in this repo.
4. Give the service its own Atlanta landing page (see `/backlinks/`, `/google-ads-management/` for the
   pattern: pricing cards, FAQ + Service schema, request form) and link it from the nav, `/services/`,
   a homepage service card (no price), and the footer.
5. Put a `<!-- pay:<key> --><!-- /pay -->` marker on the service page (keep a "request via form"
   button next to it), then run the post-processing order below.

**Homepage has no prices.** It shows services only as linked cards (name, benefit, icon,
"Learn more"). Prices, Pay now buttons and Offer prices in schema live on each service page and
`/services/` only. Keep it that way (no `$` amounts, `pay-btn`, or `priceRange` on `/`).

## Post-processing order (run after any generator or page edit)

All of these are idempotent (they replace their own `<!-- name:start/end -->` blocks):

1. `python3 pay_buttons.py`: Stripe Pay now buttons from `data/packages.json`.
2. `python3 trust_strip.py`: "Secure checkout by Stripe / Clear scope / A real person / …" strip
   under the pricing grid of every page with Pay now buttons (`<!-- trust:start/end -->`).
3. `python3 internal_links.py`: directory internal linking (also run automatically at the end of
   `generate_directory.py`):
   - every listing: breadcrumb Home > Directory > City > Listing, "Similar agencies" (8 cards:
     same city + category, same city, same category in nearby cities, then nearby cities), links
     to its city page, its category page, nearby cities, and matching Mindful Marketing services;
   - every city page: nearby cities (by distance, from `data/city-coords.json`, built from the
     2023 Census Gazetteer; add a lat/lng entry when a new city is added) and top categories;
   - every category page (`/services/<category>/`): a static list of its agencies grouped by city,
     plus top cities and other categories (creates `/services/full-service-digital-marketing-agencies/`);
   - `/cities/`, `/services/` and `/blog/` hubs: static, crawlable link lists (cities, categories, guides).
4. `python3 enhance_city_pages.py`
5. `python3 brand_cta.py`
6. `python3 generate_sitemap.py`

Then check for broken internal links and orphans (every listing should be reachable from `/`).

## Design system

`styles.css` ends with the "Premium design system (v2)" layer: Plus Jakarta Sans (headings) +
Inter (body), navy/blue palette from the logo with an amber accent, gradient buttons, cards, the
dark homepage hero, and scroll-reveal animations (`.rv` → `.in`, added by `script.js`; disabled for
`prefers-reduced-motion`). Hero/CTA image: `assets/atl-skyline.webp` (+ `-640` for mobile), an
illustrative skyline, not a photo of our office or clients. Platforms on the homepage are listed as
tools we use, never as partner badges.

Directory pages (listings, city hubs, categories, lists) carry a "Work with Mindful Marketing" CTA
added by `brand_cta.py` / `enhance_city_pages.py` — re-run both after regenerating the directory.

After payment, buyers land on `/thank-you/` (noindex) and fill the intake form,
which is saved to the Supabase `leads` table with `service = "Paid Order Intake"`,
`tier = <package name>`, and `budget = "PAID via Stripe | <checkout session id>"`.
Match it to the Stripe payment by email or session ID.

---

# Directory notes

A directory of marketing agencies across the state of Georgia — browse by
city or by service, with real agency data imported from Outscraper Google
Maps exports.

## Files

| Path | Purpose |
| --- | --- |
| `index.html` | Homepage — hero search, featured listings, city/service hub previews. |
| `styles.css` | All styling. Theme colors (blue/white) live at the top in `:root`. |
| `directory.js` | Shared front-end engine: loads `data/agencies.json`, renders listing cards, powers the hero search bar and hub grids. |
| `script.js` | Mobile nav toggle + footer year. |
| `data/agencies.json` | **The single source of truth for all listings.** Regenerated by `generate_directory.py`. |
| `generate_directory.py` | Build script — turns an Outscraper export into real static pages. See below. |
| `cities/index.html` | Hub page listing all Georgia cities. Every city and listing page links back here. |
| `<city>/index.html` | Per-city browse page (filterable by service) — lives at the site root, e.g. `/atlanta/`. |
| `<city>/<listing>/index.html` | **Individual agency listing page** — a real static file, generated by the build script, e.g. `/atlanta/some-agency-name/`. |
| `services/index.html` | Hub page listing all service categories (SEO, PPC, etc.) **and** the 3 owned-service branches. |
| `services/<category>/index.html` | Directory browse page for one category, filterable by city (other agencies, not us). |
| `seo/`, `digital-marketing/`, `social-media-marketing/` | **Our own services** — real sales pages (pricing/includes/process/form), not directory listings. See below. |
| `service-leads.js` | Form handler for the 3 owned-service pages — posts to the Supabase `leads` table. |
| `lists/index.html` | Hub for programmatic "best of" lists, reads `data/lists.json`. |
| `data/lists.json` | Source of truth for list articles (`[{slug, title, description}]`). Add an entry + create `lists/<slug>/index.html` to publish one. |
| `submit/index.html` | "Add your agency" form — submits to Supabase for review. |
| `about/index.html` | About the directory. |
| `assets/logo.svg`, `assets/favicon.svg` | Mindful Marketing Agency logo + icon (see checklist above). |

## Directory listings vs. our own services

This site does two different jobs, and it's important to keep them visually
and structurally separate:

- **Directory** (`/cities/`, `/services/`, individual city and listing
  pages) — a genuine directory of *other* Georgia marketing agencies,
  pulled from Outscraper data.
- **Owned services** (`/seo/`, `/digital-marketing/`,
  `/social-media-marketing/`) — services *we* sell and fulfill ourselves
  (drop-serviced). These are sales pages with pricing/includes/process and
  a lead form, not browse/filter pages. Don't reuse the directory's
  `renderListings()` on these — use `service-leads.js` and the
  `.pricing-grid` / `.includes-grid` / `.process-steps` / `.why-grid` CSS
  components instead.

The `/services/` hub links to both: a "Services we provide ourselves"
section (the 3 owned pages) and a "Browse the Directory" section (the
other 5 categories, genuine listings of other agencies).

## How URLs work

- City hub (all cities): `/cities/`
- One city: `/atlanta/` — lives at the site root, **not** under `/cities/`
- One listing: `/atlanta/some-agency-name/` — a real pre-rendered HTML file
  (not a client-side route), so it's immediately crawlable and shareable
- Service hub: `/services/`
- One service: `/services/seo-agencies/`

Every city page and listing page links back to `/cities/` as the "Cities"
breadcrumb/nav entry, even though the city itself lives at the root.

City and service pages are static shells that render their listing grid
client-side from `data/agencies.json` (fast, no backend needed). Individual
listing pages are fully static — baked in by the build script — since a
static host can't route arbitrary `/<city>/<listing>/` paths on the fly.

## Importing Outscraper data

Whenever you export new Google Maps listings from Outscraper:

```bash
python3 generate_directory.py path/to/outscraper_export.csv
```

This will:

1. Normalize the rows into `data/agencies.json` (maps Outscraper's common
   column names — `name`, `full_address`, `city`, `phone`, `site`, `rating`,
   `reviews`, `category`/`type`, `working_hours`, `about`, `place_id` — see
   the top of the script for the full list it understands).
2. Auto-assign each listing to one of the 8 canonical service categories
   using keyword matching against its Outscraper category/type (falls back
   to "Full-Service Digital Marketing Agencies" if nothing matches).
3. Write a real static page for every listing at
   `/<city-slug>/<listing-slug>/index.html`.
4. Auto-create a new `/<city>/` hub page for any city not already in
   the canonical list of 10 (Atlanta, Savannah, Augusta, Columbus, Macon,
   Athens, Sandy Springs, Roswell, Albany, Warner Robins).
5. Regenerate `sitemap.xml` with every URL.

Add `--merge` to add to the existing dataset instead of replacing it
(dedupes on city + slug):

```bash
python3 generate_directory.py path/to/new_export.csv --merge
```

If your data is already in the site's JSON shape (see any entry in
`data/agencies.json` for the exact fields), pass `--format json` instead of
the default `--format csv`.

### Fields used by the site

```json
{
  "name": "Acme Marketing Co.",
  "slug": "acme-marketing-co",
  "category": "SEO Agencies",
  "city": "Atlanta",
  "city_slug": "atlanta",
  "address": "123 Main St, Atlanta, GA 30303",
  "phone": "(404) 555-0100",
  "website": "https://example.com",
  "rating": 4.8,
  "reviews_count": 132,
  "hours": { "Monday": "9am - 5pm" },
  "description": "...",
  "place_id": "...",
  "featured": false
}
```

Set `"featured": true` on any listing to have it show in the homepage
featured section and sort to the top of its city/service pages.

## "Add your agency" submissions (Supabase)

The `/submit/` form currently posts to the existing Supabase `leads` table
(service = "Directory Submission"), because `agency_submissions` was never
created. To use a dedicated table instead, create it with the SQL below and
point `submit/index.html` back at it:

```sql
create table if not exists agency_submissions (
  id uuid default gen_random_uuid() primary key,
  created_at timestamptz default now(),
  site text,
  agency_name text,
  city text,
  category text,
  website text,
  phone text,
  address text,
  contact_name text,
  contact_email text,
  description text,
  status text default 'pending'
);

alter table agency_submissions enable row level security;
create policy "Allow public inserts" on agency_submissions
  for insert to anon with check (true);
```

Review submissions in Supabase, then fold approved ones into
`data/agencies.json` (or a CSV) and re-run `generate_directory.py`.

## Theme colors

```
--blue:       #2563EB   /* primary */
--blue-dark:  #1D4ED8
--blue-deep:  #1E3A8A   /* logo navy */
--navy-950:   #060E2B   /* hero / footer / CTA band */
--accent:     #F59E0B   /* eyebrow dots, featured badge */
--blue-light: #EFF6FF   /* soft backgrounds */
```

## Running locally

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```
