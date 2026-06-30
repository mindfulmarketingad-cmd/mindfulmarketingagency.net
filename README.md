# Mindful Marketing Agency

A one-page website for Mindful Marketing Agency — a digital marketing studio run by David.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The one-page site: hero, about, services, work, guides, contact. |
| `styles.css` | All styling. Theme colors live at the top in `:root`. |
| `script.js` | Mobile nav toggle + footer year. |
| `assets/logo.svg` | Logo (recreated from your brand mark as a crisp SVG). |
| `assets/favicon.svg` | Favicon (the logo blob with an "M"). |
| `assets/brands/*.svg` | **Placeholder** wordmarks for managed brands (Sigvaris, Pillow Perfect, Scuf Gaming). |
| `guides/domain-investing/index.html` | Full "Domain Investing 101" guide page. |
| `guides/affiliate-marketing/index.html` | Full "Affiliate Marketing 101" guide page. |

## SEO

- Primary keyword **"Atlanta Digital Marketing Agency"** is in the `<title>`
  and the homepage `<h1>`, with location context ("Atlanta, GA · Serving
  clients nationwide") in the hero and About sections.

## Guides

The homepage has a **Guides section** (`#guides`) that links out to two full
guide pages under `/guides/...`. Add more guides by creating another
`guides/<slug>/index.html` and adding a card to the `#guides` section and the
footer.

## Brand logos (managed brands)

The "A few results I'm proud of" section includes a *Brands I've managed*
strip. The files in `assets/brands/` are **plain text placeholders** — I
couldn't download the official Sigvaris / Pillow Perfect / Scuf Gaming logos
because this environment's network policy blocks outbound image hosts. Drop the
real logo files into `assets/brands/` (keep the same filenames, or update the
`<img src>` in `index.html`) to replace them.

## Social links

Footer social icons (Instagram, Facebook, X) currently point to `#` — replace
those `href="#"` values with your real profile URLs.

## Theme colors (from the logo)

```
--charcoal: #3D3B39   /* logo background */
--cream:    #F6EFDF   /* logo text */
--accent:   #9aa886   /* soft sage, complements the above */
```

## How to edit the content

All copy is plain text in `index.html` — search for the section you want:

- **Hero headline / intro** → `<section class="hero">`
- **About / bio** → `id="about"` (currently written for "David")
- **Services** → `id="services"` (six `<article class="card">` blocks)
- **Portfolio** → `id="work"` — three placeholder projects. Replace the
  names, descriptions, and metrics. To use real images instead of the
  charcoal placeholder tiles, swap each `<div class="project-thumb">` for
  an `<img>`.
- **Contact** → `id="contact"` — emails `David@mindfulmarketingagency.net`.

> The portfolio case studies (Bloom & Co., Northwind, Terra Goods) and the
> hero stats are **placeholders** — update them with your real work.

## Using the original logo PNG

The logo here is an SVG recreation. To use your original raster image, drop
it into `assets/` and point the `<img src>` / favicon `<link href>` tags at it.

## Running locally

It's a static site — open `index.html` in a browser, or serve it:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```
