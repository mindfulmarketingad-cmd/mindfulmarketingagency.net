#!/usr/bin/env python3
"""Adds a trust/promise strip under the last pricing grid on every service page.
Idempotent (<!-- trust:start --> / <!-- trust:end -->). Only promise what fulfillment
actually offers — edit EXTRA below per page. Run after pay_buttons.py."""
import glob, os, re
BASE = os.path.dirname(os.path.abspath(__file__))
SVG = lambda p: f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" width="20" height="20">{p}</svg>'
LOCK = SVG('<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>')
TAG = SVG('<path d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.3"/>')
CHAT = SVG('<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>')
DOC = SVG('<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>')
REDO = SVG('<path d="M3 12a9 9 0 0 1 15.5-6.2L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15.5 6.2L3 16"/><path d="M3 21v-5h5"/>')
EXTRA = {
    "youtube-thumbnails": (REDO, "Unlimited revisions", "We keep refining your thumbnail until you're happy with it."),
    "backlinks": (DOC, "Full link report", "Every backlink we build is listed in your delivery report."),
    "seo/local-citations": (DOC, "Full citation report", "A report of every listing we create or update for you."),
}
DEFAULT = (DOC, "Proof of delivery", "Files, live links, or a report of exactly what was done.")
pat = re.compile(r"\n?[ \t]*<!-- trust:start -->.*?<!-- trust:end -->", re.S)

def end_of_div(s, start):
    depth, i = 0, start
    for m in re.finditer(r"<div\b|</div>", s[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0: return start + m.end()
    return -1

n = 0
for path in glob.glob(os.path.join(BASE, "**", "index.html"), recursive=True):
    s = open(path, encoding="utf-8").read()
    if 'class="pricing-grid"' not in s or "pay-btn" not in s: continue
    s = pat.sub("", s)
    rel = os.path.relpath(os.path.dirname(path), BASE)
    icon, title, text = EXTRA.get(rel, DEFAULT)
    items = [(LOCK, "Secure checkout by Stripe", "Your card details never touch our website."),
             (TAG, "Clear scope, flat price", "What's included is listed above — no surprise invoices."),
             (CHAT, "A real person to talk to", "We follow up within two business days of your order."),
             (icon, title, text)]
    block = '\n        <!-- trust:start -->\n        <div class="trust-strip" aria-label="Our promise">' + "".join(
        f'\n          <div class="ts-item">{i}<div><strong>{t}</strong><span>{x}</span></div></div>' for i, t, x in items
    ) + "\n        </div>\n        <!-- trust:end -->"
    last = s.rfind('<div class="pricing-grid"')
    end = end_of_div(s, last)
    if end < 0: print("unbalanced", path); continue
    s = s[:end] + block + s[end:]
    open(path, "w", encoding="utf-8").write(s); n += 1
print("trust strip on", n, "pages")
