# Mindful Marketing Agency

A one-page website for Mindful Marketing Agency — a digital marketing studio run by David.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole page: hero, about, services, work, contact. |
| `styles.css` | All styling. Theme colors live at the top in `:root`. |
| `script.js` | Mobile nav toggle + footer year. |
| `assets/logo.svg` | Logo (recreated from your brand mark as a crisp SVG). |
| `assets/favicon.svg` | Favicon (the logo blob with an "M"). |

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
