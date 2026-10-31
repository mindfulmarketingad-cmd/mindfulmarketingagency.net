#!/usr/bin/env python3
"""Make pages robust on mobile Safari / stale caches. Idempotent; run LAST after any build step
(generate_directory.py calls it automatically).

1. Cache-busting: every local CSS/JS reference (/styles.css, /script.js, /directory.js, ...) gets
   ?v=<content hash>, so a new deploy never pairs new HTML with an old cached stylesheet.
   vercel.json serves ?v= URLs as immutable and un-versioned ones with must-revalidate.
2. Inline SVG icons without width/height attributes get explicit ones, so if CSS is ever
   missing an icon renders at icon size instead of filling the screen.
"""
import glob, hashlib, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
_hash = {}
def ver(path):
    if path not in _hash:
        fp = os.path.join(BASE, path.lstrip("/"))
        _hash[path] = hashlib.md5(open(fp, "rb").read()).hexdigest()[:10] if os.path.isfile(fp) else None
    return _hash[path]

ASSET = re.compile(r'((?:href|src)=")(/[^"?#:]+\.(?:css|js))(?:\?v=[0-9a-f]+)?(")')
def bust(m):
    v = ver(m.group(2))
    return f"{m.group(1)}{m.group(2)}?v={v}{m.group(3)}" if v else m.group(0)

SVG = re.compile(r"<svg\b[^>]*>")
def size_svg(m):
    t = m.group(0)
    if re.search(r'\swidth=', t) or 'viewBox="0 0 24 24"' not in t:
        return t
    return t[:-1].rstrip("/").rstrip() + ' width="20" height="20"' + (" />" if t.endswith("/>") else ">")

def process(s):
    return SVG.sub(size_svg, ASSET.sub(bust, s))

def main():
    n = 0
    for f in glob.glob(os.path.join(BASE, "**", "*.html"), recursive=True):
        if "/node_modules/" in f or "/.git/" in f: continue
        s = open(f, encoding="utf-8").read(); s2 = process(s)
        if s2 != s:
            open(f, "w", encoding="utf-8").write(s2); n += 1
    print(f"harden_assets: updated {n} page(s); versions: " + ", ".join(f"{k}={v}" for k, v in sorted(_hash.items()) if v))

if __name__ == "__main__":
    main()
