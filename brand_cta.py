#!/usr/bin/env python3
"""Adds a server-rendered "Work with Mindful Marketing" call-to-action to every
directory page (agency listing pages, city hubs without one, category pages,
lists, and /cities/) so directory traffic funnels to our own services.

Idempotent: the block lives between <!-- brand-cta:start --> / <!-- brand-cta:end -->.
Re-run after generate_directory.py / generate_lists.py.  City hub pages get
their CTA from enhance_city_pages.py instead (they contain <!-- city-cta:start -->).
"""
import os, re
BASE = os.path.dirname(os.path.abspath(__file__))
PAT = re.compile(r"\n?\s*<!-- brand-cta:start -->.*?<!-- brand-cta:end -->", re.S)

def cta(heading):
    return f'''
    <!-- brand-cta:start -->
    <section class="section" style="max-width:var(--maxw);">
      <div class="own-cta">
        <p class="eyebrow" style="margin-bottom:.3rem;">Work with Mindful Marketing</p>
        <h2>{heading}</h2>
        <p>Mindful Marketing Agency is the Atlanta team behind this directory. We sell flat-priced, done-for-you marketing you can buy online — no contracts:
        <a href="/seo/">SEO packages</a> from $49.99, <a href="/seo/local-citations/">local citations</a> from $35,
        <a href="/google-business-profile/">Google Business Profile optimization</a> ($109), <a href="/social-media-marketing/">social media plans</a> from $99,
        <a href="/google-ads-management/">Google Ads</a> from $179, <a href="/facebook-ads/">Facebook &amp; Instagram ads</a> from $209,
        <a href="/backlinks/">backlinks</a> from $259, and <a href="/website-design/">website design</a> from $369.</p>
        <p style="margin-bottom:0;"><a class="btn btn-primary" href="/services/">See all services &amp; pricing</a> <a class="btn btn-ghost" href="/digital-marketing/#apply">Get a free proposal</a></p>
      </div>
    </section>
    <!-- brand-cta:end -->'''

count = 0
for d, _, fs in os.walk(BASE):
    if "/.git" in d or "index.html" not in fs:
        continue
    rel = os.path.relpath(d, BASE).replace(os.sep, "/")
    p = os.path.join(d, "index.html")
    s = open(p, encoding="utf-8").read()
    if "<!-- city-cta:start -->" in s:
        continue
    if 'class="listing-detail"' in s:
        heading = "Comparing agencies? Get a quote from us too."
    elif rel == "cities" or rel.startswith("lists") or (rel.startswith("services/") and rel.count("/") == 1):
        heading = "Want it done for you? Hire our Atlanta team."
    elif "data-listings" in s:
        heading = "Need digital marketing? Work with Mindful Marketing."
    else:
        continue
    o = s
    s = PAT.sub("", s)
    s = s.replace("\n  </main>", cta(heading) + "\n  </main>", 1)
    if s != o:
        open(p, "w", encoding="utf-8").write(s)
        count += 1
print("brand-cta:", count, "pages")
