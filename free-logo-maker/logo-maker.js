/* Mindful Marketing Agency — Free Logo Maker
   100% client-side: nothing is uploaded, no sign-up, no watermark.
   Icons: Lucide (ISC license) — see /free-logo-maker/LICENSE-lucide.txt */
(function () {
  'use strict';

  var root = document.getElementById('logo-maker');
  if (!root) return;

  // ---------- Data ----------
  var FONTS = [
    ['Montserrat', 'sans', [300, 400, 500, 600, 700, 800, 900]],
    ['Poppins', 'sans', [300, 400, 500, 600, 700, 800, 900]],
    ['Inter', 'sans', [300, 400, 500, 600, 700, 800, 900]],
    ['Raleway', 'sans', [300, 400, 500, 600, 700, 800, 900]],
    ['Outfit', 'sans', [300, 400, 500, 600, 700, 800, 900]],
    ['Sora', 'sans', [300, 400, 500, 600, 700, 800]],
    ['Space Grotesk', 'sans', [300, 400, 500, 600, 700]],
    ['Nunito', 'rounded', [300, 400, 500, 600, 700, 800, 900]],
    ['Fredoka', 'rounded', [300, 400, 500, 600, 700]],
    ['Comfortaa', 'rounded', [300, 400, 500, 600, 700]],
    ['Josefin Sans', 'sans', [300, 400, 500, 600, 700]],
    ['Rubik', 'sans', [300, 400, 500, 600, 700, 800, 900]],
    ['Syne', 'sans', [400, 500, 600, 700, 800]],
    ['Oswald', 'condensed', [300, 400, 500, 600, 700]],
    ['Bebas Neue', 'display', [400]],
    ['Anton', 'display', [400]],
    ['Archivo Black', 'display', [400]],
    ['Righteous', 'display', [400]],
    ['Bungee', 'display', [400]],
    ['Orbitron', 'display', [400, 500, 600, 700, 800, 900]],
    ['Playfair Display', 'serif', [400, 500, 600, 700, 800, 900]],
    ['Lora', 'serif', [400, 500, 600, 700]],
    ['Merriweather', 'serif', [300, 400, 700, 900]],
    ['DM Serif Display', 'serif', [400]],
    ['Cinzel', 'serif', [400, 500, 600, 700, 800, 900]],
    ['Abril Fatface', 'serif', [400]],
    ['Pacifico', 'script', [400]],
    ['Lobster', 'script', [400]],
    ['Dancing Script', 'script', [400, 500, 600, 700]],
    ['Great Vibes', 'script', [400]],
    ['Caveat', 'script', [400, 500, 600, 700]],
    ['Permanent Marker', 'script', [400]]
  ];
  var FONT_MAP = {};
  FONTS.forEach(function (f) { FONT_MAP[f[0]] = { cat: f[1], weights: f[2] }; });

  // [name, bg, shape, icon, text, tagline, shape2]
  var PALETTES = [
    ['Atlanta Blue', '#ffffff', '#1e3a8a', '#ffffff', '#1e3a8a', '#64748b', '#2563eb'],
    ['Peach', '#fff7ed', '#f97316', '#ffffff', '#7c2d12', '#c2410c', '#fb923c'],
    ['Forest', '#f0fdf4', '#166534', '#ecfccb', '#14532d', '#4d7c0f', '#22c55e'],
    ['Midnight', '#0f172a', '#6366f1', '#ffffff', '#f8fafc', '#a5b4fc', '#ec4899'],
    ['Gold & Black', '#0b0b0b', '#d4af37', '#0b0b0b', '#d4af37', '#e5e5e5', '#f5d77a'],
    ['Blush', '#fdf2f8', '#db2777', '#ffffff', '#831843', '#be185d', '#f472b6'],
    ['Ocean', '#ecfeff', '#0e7490', '#ffffff', '#164e63', '#0891b2', '#22d3ee'],
    ['Mono', '#ffffff', '#111827', '#ffffff', '#111827', '#6b7280', '#374151'],
    ['Sunset', '#1c1917', '#f43f5e', '#fff7ed', '#fff7ed', '#fdba74', '#f59e0b'],
    ['Lavender', '#f5f3ff', '#7c3aed', '#ffffff', '#4c1d95', '#7c3aed', '#c084fc'],
    ['Earth', '#faf5ef', '#92400e', '#fef3c7', '#451a03', '#a16207', '#d97706'],
    ['Mint', '#f0fdfa', '#14b8a6', '#ffffff', '#134e4a', '#0f766e', '#5eead4'],
    ['Crimson', '#ffffff', '#b91c1c', '#ffffff', '#111827', '#b91c1c', '#ef4444'],
    ['Neon', '#030712', '#22d3ee', '#030712', '#a3e635', '#22d3ee', '#a3e635']
  ];

  var SIZES = [
    ['sq1000', 'Square 1000 × 1000', 1000, 1000],
    ['sq500', 'Square 500 × 500', 500, 500],
    ['sq2000', 'Square 2000 × 2000 (print)', 2000, 2000],
    ['horiz', 'Horizontal logo 1600 × 600', 1600, 600],
    ['web', 'Website header 800 × 240', 800, 240],
    ['banner', 'Wide banner 1500 × 500 (X / Twitter header)', 1500, 500],
    ['fbcover', 'Facebook cover 1640 × 624', 1640, 624],
    ['social', 'Social profile picture 800 × 800', 800, 800],
    ['favicon', 'Favicon / app icon 512 × 512', 512, 512],
    ['custom', 'Custom size…', 0, 0]
  ];

  var SHAPES = ['none', 'circle', 'rounded', 'square', 'shield', 'hexagon', 'diamond', 'seal'];
  var SHAPE_LABEL = { none: 'No shape', circle: 'Circle', rounded: 'Rounded square', square: 'Square', shield: 'Shield', hexagon: 'Hexagon', diamond: 'Diamond', seal: 'Badge / seal' };
  var LAYOUTS = { left: 'Icon left', top: 'Icon on top', icon: 'Icon only', text: 'Text only', emblem: 'Badge / emblem' };

  var DEFAULT = {
    v: 1,
    name: 'Your Brand', tagline: 'Your tagline here',
    font: 'Montserrat', weight: 700, size: 64, ls: 0, tcase: 'none',
    tFont: '', tWeight: 500, tSize: 22, tLs: 18, tCase: 'upper',
    icon: 'sparkles', iconScale: 100, iconRot: 0, iconStroke: 2, iconInner: 56,
    shape: 'circle', shapeStyle: 'fill',
    layout: 'top', gap: 100, align: 'auto',
    cName: '#1e3a8a', cTag: '#64748b', cIcon: '#ffffff', cShape: '#1e3a8a', cBg: '#ffffff',
    gName: false, cName2: '#2563eb', gShape: true, cShape2: '#2563eb', gBg: false, cBg2: '#dbeafe', gAngle: 135,
    transparent: false,
    sizeKey: 'sq1000', w: 1000, h: 1000, pad: 12,
    scale: 1
  };

  var TEMPLATES = [
    { label: 'Coffee shop', s: { icon: 'coffee', font: 'Playfair Display', weight: 700, tcase: 'none', shape: 'circle', shapeStyle: 'fill', layout: 'top', tFont: 'Montserrat', tWeight: 500, tCase: 'upper', tLs: 24, cBg: '#faf5ef', cShape: '#92400e', cShape2: '#d97706', gShape: true, cIcon: '#fef3c7', cName: '#451a03', cTag: '#a16207', gName: false, gBg: false, transparent: false, ls: 0 } },
    { label: 'Real estate', s: { icon: 'house', font: 'Cinzel', weight: 700, tcase: 'upper', ls: 8, shape: 'shield', shapeStyle: 'fill', layout: 'left', tFont: 'Lora', tWeight: 400, tCase: 'none', tLs: 4, cBg: '#ffffff', cShape: '#1e3a8a', cShape2: '#1e3a8a', gShape: false, cIcon: '#f5d77a', cName: '#1e3a8a', cTag: '#64748b', gName: false, gBg: false, transparent: false } },
    { label: 'Tech startup', s: { icon: 'zap', font: 'Space Grotesk', weight: 700, tcase: 'lower', ls: -2, shape: 'rounded', shapeStyle: 'fill', layout: 'left', tFont: 'Inter', tWeight: 500, tCase: 'none', tLs: 0, cBg: '#0f172a', cShape: '#6366f1', cShape2: '#ec4899', gShape: true, cIcon: '#ffffff', cName: '#f8fafc', cTag: '#a5b4fc', gName: false, gBg: false, transparent: false } },
    { label: 'Fitness', s: { icon: 'dumbbell', font: 'Bebas Neue', weight: 400, tcase: 'upper', ls: 6, shape: 'hexagon', shapeStyle: 'fill', layout: 'top', tFont: 'Oswald', tWeight: 500, tCase: 'upper', tLs: 30, cBg: '#030712', cShape: '#22d3ee', cShape2: '#a3e635', gShape: true, cIcon: '#030712', cName: '#a3e635', cTag: '#22d3ee', gName: false, gBg: false, transparent: false } },
    { label: 'Beauty & salon', s: { icon: 'flower-2', font: 'Great Vibes', weight: 400, tcase: 'none', ls: 0, shape: 'none', shapeStyle: 'fill', layout: 'top', tFont: 'Raleway', tWeight: 500, tCase: 'upper', tLs: 40, cBg: '#fdf2f8', cShape: '#db2777', cShape2: '#f472b6', gShape: false, cIcon: '#db2777', cName: '#831843', cTag: '#be185d', gName: false, gBg: false, transparent: false } },
    { label: 'Law firm', s: { icon: 'scale', font: 'DM Serif Display', weight: 400, tcase: 'none', ls: 0, shape: 'circle', shapeStyle: 'outline', layout: 'left', tFont: 'Montserrat', tWeight: 600, tCase: 'upper', tLs: 30, cBg: '#ffffff', cShape: '#111827', cShape2: '#111827', gShape: false, cIcon: '#111827', cName: '#111827', cTag: '#b91c1c', gName: false, gBg: false, transparent: false } },
    { label: 'Restaurant badge', s: { icon: 'chef-hat', font: 'Righteous', weight: 400, tcase: 'upper', ls: 4, shape: 'seal', shapeStyle: 'fill', layout: 'emblem', tFont: 'Nunito', tWeight: 700, tCase: 'upper', tLs: 20, cBg: '#ffffff', cShape: '#b91c1c', cShape2: '#ef4444', gShape: true, cIcon: '#ffffff', cName: '#ffffff', cTag: '#fee2e2', gName: false, gBg: false, transparent: true } },
    { label: 'Landscaping', s: { icon: 'trees', font: 'Fredoka', weight: 600, tcase: 'none', ls: 0, shape: 'none', shapeStyle: 'fill', layout: 'left', tFont: 'Fredoka', tWeight: 400, tCase: 'none', tLs: 4, cBg: '#f0fdf4', cShape: '#166534', cShape2: '#22c55e', gShape: false, cIcon: '#16a34a', cName: '#14532d', cTag: '#4d7c0f', gName: false, gBg: false, transparent: false } }
  ];

  var STORE_KEY = 'mma-logo-maker-v1';
  var ICONS = [];          // [name, innerSvg, tags]
  var ICON_MAP = {};
  var state = loadState();
  var history = [JSON.stringify(state)];
  var hIndex = 0;

  // ---------- Helpers ----------
  function $(sel, el) { return (el || root).querySelector(sel); }
  function $all(sel, el) { return Array.prototype.slice.call((el || root).querySelectorAll(sel)); }
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function clamp(n, a, b) { return Math.max(a, Math.min(b, n)); }
  function rnd(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
  function slug(s) { return (String(s).toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'my').slice(0, 60); }
  function nearestWeight(font, w) {
    var ws = (FONT_MAP[font] || FONT_MAP.Montserrat).weights;
    return ws.reduce(function (best, x) { return Math.abs(x - w) < Math.abs(best - w) ? x : best; }, ws[0]);
  }
  function applyCase(t, c) {
    if (c === 'upper') return t.toUpperCase();
    if (c === 'lower') return t.toLowerCase();
    if (c === 'title') return t.toLowerCase().replace(/(^|[\s\-])(\S)/g, function (m, a, b) { return a + b.toUpperCase(); });
    return t;
  }
  function tagFont() { return state.tFont && FONT_MAP[state.tFont] ? state.tFont : state.font; }

  function loadState() {
    var s = Object.assign({}, DEFAULT);
    try {
      var saved = JSON.parse(localStorage.getItem(STORE_KEY) || 'null');
      if (saved && saved.v === 1) Object.keys(DEFAULT).forEach(function (k) { if (k in saved) s[k] = saved[k]; });
    } catch (e) { /* ignore */ }
    if (!FONT_MAP[s.font]) s.font = DEFAULT.font;
    return s;
  }
  function save() { try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) { /* private mode */ } }

  // ---------- Fonts ----------
  var loadedFonts = {};
  function ensureFont(family) {
    if (!FONT_MAP[family] || loadedFonts[family]) return loadedFonts[family] || Promise.resolve();
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://fonts.googleapis.com/css2?family=' + encodeURIComponent(family).replace(/%20/g, '+') + ':wght@' + FONT_MAP[family].weights.join(';') + '&display=swap';
    document.head.appendChild(link);
    loadedFonts[family] = new Promise(function (res) {
      link.onload = function () { res(); };
      link.onerror = function () { res(); };
    });
    return loadedFonts[family];
  }
  function fontsReady() {
    var fams = [state.font, tagFont()];
    return Promise.all(fams.map(function (f) { return ensureFont(f); })).then(function () {
      if (!document.fonts || !document.fonts.load) return;
      return Promise.all([
        document.fonts.load(nearestWeight(state.font, state.weight) + ' 64px "' + state.font + '"', state.name || 'A'),
        document.fonts.load(nearestWeight(tagFont(), state.tWeight) + ' 32px "' + tagFont() + '"', state.tagline || 'A')
      ]).catch(function () {});
    });
  }

  // Font picker previews use a tiny subset of each font, renamed so it never clashes with the real font.
  function loadFontPreviews() {
    var chars = FONTS.map(function (f) { return f[0]; }).join('') + 'Aa';
    var uniq = Array.from(new Set(chars.split(''))).join('');
    var url = 'https://fonts.googleapis.com/css2?' + FONTS.map(function (f) {
      var w = f[2].indexOf(400) >= 0 ? 400 : f[2][0];
      return 'family=' + encodeURIComponent(f[0]).replace(/%20/g, '+') + ':wght@' + w;
    }).join('&') + '&text=' + encodeURIComponent(uniq) + '&display=swap';
    fetch(url).then(function (r) { return r.ok ? r.text() : ''; }).then(function (css) {
      if (!css) return;
      css = css.replace(/font-family:\s*'([^']+)'/g, function (m, f) { return "font-family: 'lmprev-" + f + "'"; });
      var st = document.createElement('style');
      st.textContent = css;
      document.head.appendChild(st);
    }).catch(function () {});
  }

  // ---------- Measurement ----------
  var mctx = document.createElement('canvas').getContext('2d');
  function measure(text, family, weight, size, lsEm) {
    if (!text) return { w: 0, a: 0, d: 0 };
    mctx.font = weight + ' ' + size + 'px "' + family + '", sans-serif';
    var m = mctx.measureText(text);
    var n = Array.from(text).length;
    var ls = (lsEm / 100) * size;
    var a = m.actualBoundingBoxAscent, d = m.actualBoundingBoxDescent;
    if (!(a >= 0)) { a = size * 0.72; d = size * 0.2; }
    // Keep line boxes stable while typing: use at least cap-height-ish ascent.
    a = Math.max(a, size * 0.5);
    d = Math.max(d, 0);
    var left = m.actualBoundingBoxLeft || 0;
    var w = Math.max(m.width, (m.actualBoundingBoxRight || 0) + left) + ls * (n - 1);
    return { w: w, a: a, d: d, left: left, ls: ls };
  }

  // ---------- SVG building ----------
  function shapeSvg(kind, x, y, size, fill, style, sw) {
    if (kind === 'none') return '';
    var s = size / 100;
    var inset = style === 'outline' ? sw / 2 : 0;
    var k = (100 - inset * 2) / 100;
    var attrs = style === 'outline'
      ? 'fill="none" stroke="' + fill + '" stroke-width="' + (sw / k) + '" stroke-linejoin="round"'
      : 'fill="' + fill + '"';
    var inner;
    switch (kind) {
      case 'circle': inner = '<circle cx="50" cy="50" r="50" ' + attrs + '/>'; break;
      case 'rounded': inner = '<rect x="0" y="0" width="100" height="100" rx="22" ' + attrs + '/>'; break;
      case 'square': inner = '<rect x="0" y="0" width="100" height="100" ' + attrs + '/>'; break;
      case 'shield': inner = '<path d="M50 1 L93 15 V46 C93 73 74 91 50 99 C26 91 7 73 7 46 V15 Z" ' + attrs + '/>'; break;
      case 'hexagon': inner = '<polygon points="' + poly(6, 50, 50, -90) + '" ' + attrs + '/>'; break;
      case 'diamond': inner = '<path d="M50 0 L100 50 L50 100 L0 50 Z" ' + attrs + '/>'; break;
      case 'seal': inner = '<polygon points="' + seal() + '" ' + attrs + '/>'; break;
      default: return '';
    }
    return '<g transform="translate(' + r2(x + inset * s) + ' ' + r2(y + inset * s) + ') scale(' + r4(s * k) + ')">' + inner + '</g>';
  }
  function poly(n, r, c, rot) {
    var pts = [];
    for (var i = 0; i < n; i++) {
      var a = (rot + i * 360 / n) * Math.PI / 180;
      pts.push(r2(c + r * Math.cos(a)) + ',' + r2(c + r * Math.sin(a)));
    }
    return pts.join(' ');
  }
  function seal() {
    var pts = [], n = 40;
    for (var i = 0; i < n; i++) {
      var r = i % 2 ? 45 : 50, a = (-90 + i * 360 / n) * Math.PI / 180;
      pts.push(r2(50 + r * Math.cos(a)) + ',' + r2(50 + r * Math.sin(a)));
    }
    return pts.join(' ');
  }
  function r2(n) { return Math.round(n * 100) / 100; }
  function r4(n) { return Math.round(n * 10000) / 10000; }

  function iconSvg(name, cx, cy, size, color, rot, stroke) {
    var ic = ICON_MAP[name];
    if (!ic) return '';
    var s = size / 24;
    return '<g transform="translate(' + r2(cx) + ' ' + r2(cy) + ') rotate(' + (rot || 0) + ') scale(' + r4(s) + ') translate(-12 -12)" fill="none" stroke="' + color + '" color="' + color + '" stroke-width="' + stroke + '" stroke-linecap="round" stroke-linejoin="round">' + ic[1] + '</g>';
  }

  function gradDef(id, c1, c2, angle) {
    var a = (angle - 90) * Math.PI / 180;
    var x = Math.cos(a) / 2, y = Math.sin(a) / 2;
    return '<linearGradient id="' + id + '" x1="' + r4(0.5 - x) + '" y1="' + r4(0.5 - y) + '" x2="' + r4(0.5 + x) + '" y2="' + r4(0.5 + y) + '"><stop offset="0" stop-color="' + c1 + '"/><stop offset="1" stop-color="' + c2 + '"/></linearGradient>';
  }

  function textSvg(str, x, baseline, family, weight, size, lsPx, fill) {
    return '<text x="' + r2(x) + '" y="' + r2(baseline) + '" font-family="\'' + esc(family) + '\', sans-serif" font-weight="' + weight + '" font-size="' + r2(size) + '"' + (lsPx ? ' letter-spacing="' + r2(lsPx) + '"' : '') + ' fill="' + fill + '" xml:space="preserve">' + esc(str) + '</text>';
  }

  // opts: {w, h, transparent, markOnly, pad, fontCss}
  function buildSvg(st, opts) {
    opts = opts || {};
    var W = opts.w || st.w, H = opts.h || st.h;
    var transparent = 'transparent' in opts ? opts.transparent : st.transparent;
    var padPct = 'pad' in opts ? opts.pad : st.pad;
    var layout = opts.markOnly ? 'icon' : st.layout;
    var hasIcon = !!ICON_MAP[st.icon];
    var shape = st.shape;
    if (layout === 'emblem' && shape === 'none') shape = 'circle';
    if (opts.markOnly && !hasIcon && shape === 'none') shape = 'rounded';

    var defs = '';
    var nameFill = st.cName, shapeFill = st.cShape, bgFill = st.cBg;
    if (st.gName) { defs += gradDef('lmgName', st.cName, st.cName2, st.gAngle); nameFill = 'url(#lmgName)'; }
    if (st.gShape) { defs += gradDef('lmgShape', st.cShape, st.cShape2, st.gAngle); shapeFill = 'url(#lmgShape)'; }
    if (st.gBg) { defs += gradDef('lmgBg', st.cBg, st.cBg2, st.gAngle); bgFill = 'url(#lmgBg)'; }

    var nameW = nearestWeight(st.font, st.weight);
    var tFam = st.tFont && FONT_MAP[st.tFont] ? st.tFont : st.font;
    var tagW = nearestWeight(tFam, st.tWeight);
    var nameTxt = applyCase(st.name || '', st.tcase);
    var tagTxt = applyCase(st.tagline || '', st.tCase);
    var gapK = st.gap / 100;
    var M = 100 * st.iconScale / 100;          // mark size in design units
    var sw = 4 * (M / 100);                    // outline width

    var body = '';
    var bw, bh;

    function mark(x, y, size, letterFallback) {
      var out = shapeSvg(shape, x, y, size, shapeFill, st.shapeStyle, 4 * size / 100);
      var inner = shape === 'none' ? size : size * st.iconInner / 100;
      var cy = y + size / 2 + (shape === 'shield' ? -size * 0.03 : 0);
      if (hasIcon) out += iconSvg(st.icon, x + size / 2, cy, inner, st.cIcon, st.iconRot, st.iconStroke);
      else if (letterFallback) {
        var ch = applyCase(Array.from((st.name || 'A').trim())[0] || 'A', 'upper');
        var fs = inner * 1.05;
        var m = measure(ch, st.font, nameW, fs, 0);
        out += textSvg(ch, x + size / 2 - m.w / 2 + (m.left || 0), cy + (m.a - m.d) / 2, st.font, nameW, fs, 0, shape === 'none' ? nameFill : st.cIcon);
      }
      return out;
    }

    function textBlock(x, y, align, width, nameSize, tagSize) {
      var out = '';
      var nm = measure(nameTxt, st.font, nameW, nameSize, st.ls);
      var tg = measure(tagTxt, tFam, tagW, tagSize, st.tLs);
      var cy = y;
      if (nameTxt) {
        var nx = align === 'center' ? x + (width - nm.w) / 2 : align === 'right' ? x + width - nm.w : x;
        out += textSvg(nameTxt, nx + (nm.left || 0), cy + nm.a, st.font, nameW, nameSize, nm.ls, nameFill);
        cy += nm.a + nm.d;
      }
      if (tagTxt) {
        if (nameTxt) cy += tagSize * 0.55 * gapK;
        var tx = align === 'center' ? x + (width - tg.w) / 2 : align === 'right' ? x + width - tg.w : x;
        out += textSvg(tagTxt, tx + (tg.left || 0), cy + tg.a, tFam, tagW, tagSize, tg.ls, st.cTag);
      }
      return out;
    }
    function textSize(nameSize, tagSize) {
      var nm = measure(nameTxt, st.font, nameW, nameSize, st.ls);
      var tg = measure(tagTxt, tFam, tagW, tagSize, st.tLs);
      var h = (nameTxt ? nm.a + nm.d : 0) + (tagTxt ? tg.a + tg.d : 0) + (nameTxt && tagTxt ? tagSize * 0.55 * gapK : 0);
      return { w: Math.max(nm.w, tg.w), h: h };
    }

    var align = st.align;
    if (layout === 'left' && (!hasIcon && shape === 'none')) layout = 'text';
    if (layout === 'top' && (!hasIcon && shape === 'none')) layout = 'text';

    if (layout === 'icon') {
      bw = bh = M;
      body = mark(0, 0, M, true);
    } else if (layout === 'text') {
      var ts = textSize(st.size, st.tSize);
      bw = Math.max(ts.w, 1); bh = Math.max(ts.h, 1);
      body = textBlock(0, 0, align === 'auto' ? 'center' : align, bw, st.size, st.tSize);
    } else if (layout === 'left') {
      var ts2 = textSize(st.size, st.tSize);
      var ML = Math.max(ts2.h * 1.3, st.size * 0.95) * st.iconScale / 100; // icon scales with the text block
      var gap = ML * 0.22 * gapK;
      bw = ML + gap + ts2.w; bh = Math.max(ML, ts2.h);
      body = mark(0, (bh - ML) / 2, ML) + textBlock(ML + gap, (bh - ts2.h) / 2, align === 'auto' ? 'left' : align, ts2.w, st.size, st.tSize);
    } else if (layout === 'top') {
      var ts3 = textSize(st.size, st.tSize);
      var MT = Math.max(st.size * 1.55, ts3.w * 0.26) * st.iconScale / 100;
      var gap3 = MT * 0.2 * gapK;
      bw = Math.max(MT, ts3.w); bh = MT + gap3 + ts3.h;
      body = mark((bw - MT) / 2, 0, MT) + textBlock(0, MT + gap3, align === 'auto' ? 'center' : align, bw, st.size, st.tSize);
    } else { // emblem
      var S = 300;
      var inner = S * (shape === 'shield' || shape === 'diamond' ? 0.56 : shape === 'hexagon' ? 0.64 : 0.68);
      var iconS = hasIcon ? S * 0.26 * st.iconScale / 100 : 0;
      var nm1 = measure(nameTxt, st.font, nameW, 100, st.ls);
      var tg1 = measure(tagTxt, tFam, tagW, 100, st.tLs);
      var nSize = nameTxt ? Math.min(st.size, inner / Math.max(nm1.w / 100, 0.01)) : 0;
      var tSize = tagTxt ? Math.min(st.tSize, (inner * 0.92) / Math.max(tg1.w / 100, 0.01)) : 0;
      var tsE = textSize(nSize || 1, tSize || 1);
      var g = S * 0.05 * gapK;
      var stackH = iconS + (iconS && (nameTxt || tagTxt) ? g : 0) + tsE.h;
      var maxH = S * (shape === 'diamond' ? 0.5 : 0.66);
      var k = stackH > maxH ? maxH / stackH : 1;
      iconS *= k; nSize *= k; tSize *= k; tsE = textSize(nSize || 1, tSize || 1); g *= k;
      stackH = iconS + (iconS && (nameTxt || tagTxt) ? g : 0) + tsE.h;
      var cy0 = S / 2 - stackH / 2 + (shape === 'shield' ? -S * 0.04 : 0);
      body = shapeSvg(shape, 0, 0, S, shapeFill, st.shapeStyle, 4 * S / 100);
      if (st.shapeStyle === 'outline' && shape !== 'none') body += shapeSvg(shape, S * 0.06, S * 0.06, S * 0.88, shapeFill, 'outline', S * 0.012);
      if (iconS) body += iconSvg(st.icon, S / 2, cy0 + iconS / 2, iconS, st.cIcon, st.iconRot, st.iconStroke);
      var savedSize = [st.size, st.tSize];
      body += textBlock((S - tsE.w) / 2, cy0 + iconS + (iconS ? g : 0), 'center', tsE.w, nSize || 1, tSize || 1);
      bw = bh = S;
      void savedSize;
    }

    // Fit into the canvas with padding
    var p = Math.min(W, H) * padPct / 100;
    var availW = Math.max(W - 2 * p, 1), availH = Math.max(H - 2 * p, 1);
    var k2 = Math.min(availW / bw, availH / bh);
    var ox = (W - bw * k2) / 2, oy = (H - bh * k2) / 2;

    var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + ' ' + H + '">';
    if (opts.title) svg += '<title>' + esc(opts.title) + '</title>';
    if (opts.fontCss) svg += '<style>' + opts.fontCss + '</style>';
    if (defs) svg += '<defs>' + defs + '</defs>';
    if (!transparent) svg += '<rect width="' + W + '" height="' + H + '" fill="' + (opts.bgOverride || bgFill) + '"/>';
    svg += '<g transform="translate(' + r2(ox) + ' ' + r2(oy) + ') scale(' + r4(k2) + ')">' + body + '</g></svg>';
    return svg;
  }

  // ---------- Render ----------
  var stage = $('#lm-stage');
  var rafPending = false;
  function render() {
    if (rafPending) return;
    rafPending = true;
    requestAnimationFrame(function () {
      rafPending = false;
      var svg = buildSvg(state, { title: (state.name || 'Logo') + ' logo preview' });
      stage.innerHTML = svg;
      var el = stage.firstChild;
      el.setAttribute('role', 'img');
      el.setAttribute('aria-label', 'Logo preview: ' + (state.name || 'untitled'));
      el.removeAttribute('width'); el.removeAttribute('height');
      fitStage();
      stage.classList.toggle('is-transparent', !!state.transparent);
      $('#lm-dims').textContent = state.w + ' × ' + state.h + ' px';
    });
  }
  function fitStage() {
    var box = stage.parentNode;
    var cs = getComputedStyle(box);
    var availW = box.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    var mobile = window.matchMedia('(max-width: 960px)').matches;
    var availH = Math.max(160, window.innerHeight * (mobile ? 0.3 : 0.62));
    var k = Math.min(availW / state.w, availH / state.h);
    stage.style.aspectRatio = 'auto';
    stage.style.width = Math.floor(state.w * k) + 'px';
    stage.style.height = Math.floor(state.h * k) + 'px';
  }
  var resizeT;
  window.addEventListener('resize', function () { clearTimeout(resizeT); resizeT = setTimeout(fitStage, 120); });
  function update() {
    render();
    fontsReady().then(render);
    scheduleCommit();
  }

  // ---------- History ----------
  var commitTimer;
  function scheduleCommit() {
    clearTimeout(commitTimer);
    commitTimer = setTimeout(commit, 350);
  }
  function commit() {
    var snap = JSON.stringify(state);
    if (snap === history[hIndex]) return;
    history = history.slice(0, hIndex + 1);
    history.push(snap);
    if (history.length > 120) history.shift();
    hIndex = history.length - 1;
    save();
    updateHistoryButtons();
  }
  function restore(idx) {
    hIndex = idx;
    state = JSON.parse(history[hIndex]);
    save();
    syncControls();
    render();
    fontsReady().then(render);
    updateHistoryButtons();
  }
  function undo() { clearTimeout(commitTimer); commit(); if (hIndex > 0) { restore(hIndex - 1); announce('Undo'); } }
  function redo() { if (hIndex < history.length - 1) { restore(hIndex + 1); announce('Redo'); } }
  function updateHistoryButtons() {
    $('#lm-undo').disabled = hIndex <= 0;
    $('#lm-redo').disabled = hIndex >= history.length - 1;
  }
  var live = $('#lm-live');
  function announce(msg) { live.textContent = ''; setTimeout(function () { live.textContent = msg; }, 30); }


  function hexRgb(h) { h = String(h || '#000').replace('#', ''); if (h.length === 3) h = h.replace(/./g, '$&$&'); var n = parseInt(h, 16) || 0; return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; }
  function lum(h) { var c = hexRgb(h).map(function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; }
  function contrast(a, b) { var x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
  function onColor(bg) { return contrast(bg, '#ffffff') >= contrast(bg, '#111827') ? '#ffffff' : '#111827'; }
  // Keep things readable when a shape/layout change puts icon or text on top of the shape.
  function fixContrast() {
    if (state.shapeStyle !== 'fill') return;
    var shapeOn = state.shape !== 'none' || state.layout === 'emblem';
    if (shapeOn && contrast(state.cIcon, state.cShape) < 2.2) state.cIcon = onColor(state.cShape);
    if (state.layout === 'emblem') {
      if (contrast(state.cName, state.cShape) < 2.5) state.cName = onColor(state.cShape);
      if (contrast(state.cTag, state.cShape) < 2.5) state.cTag = onColor(state.cShape);
      state.gName = false;
    }
    if (!state.transparent && state.layout !== 'emblem' && contrast(state.cName, state.cBg) < 1.6) state.cName = onColor(state.cBg);
  }

  // ---------- Controls ----------
  function setState(patch) { Object.assign(state, patch); fixContrast(); syncControls(); update(); }

  function syncControls() {
    $all('[data-k]').forEach(function (el) {
      var k = el.getAttribute('data-k');
      var v = state[k];
      if (el.type === 'checkbox') el.checked = !!v;
      else if (el.type === 'radio') el.checked = String(v) === el.value;
      else if (document.activeElement !== el || el.type !== 'text') el.value = v;
      var out = root.querySelector('output[for="' + el.id + '"]');
      if (out) out.textContent = formatOut(k, v);
    });
    // weights available for the selected font(s)
    fillWeights($('#lm-weight'), state.font, state.weight);
    fillWeights($('#lm-tweight'), tagFont(), state.tWeight);
    $('#lm-custom-size').hidden = state.sizeKey !== 'custom';
    $all('[data-icon]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-icon') === state.icon)); });
    $all('[data-shape]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-shape') === state.shape)); });
    $all('[data-layout]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-layout') === state.layout)); });
    $all('.lm-grad2').forEach(function (el) { el.hidden = !state[el.getAttribute('data-for')]; });
    var cur = $('#lm-icon-current');
    if (cur) cur.textContent = ICON_MAP[state.icon] ? state.icon.replace(/-/g, ' ') : 'none';
  }
  function fillWeights(sel, font, val) {
    var ws = (FONT_MAP[font] || FONT_MAP.Montserrat).weights;
    var key = ws.join(',');
    if (sel.getAttribute('data-ws') !== key) {
      sel.innerHTML = ws.map(function (w) { return '<option value="' + w + '">' + w + ' — ' + weightName(w) + '</option>'; }).join('');
      sel.setAttribute('data-ws', key);
    }
    sel.value = nearestWeight(font, val);
    sel.disabled = ws.length < 2;
  }
  function weightName(w) { return { 300: 'Light', 400: 'Regular', 500: 'Medium', 600: 'Semibold', 700: 'Bold', 800: 'Extra bold', 900: 'Black' }[w] || ''; }
  function formatOut(k, v) {
    if (k === 'ls' || k === 'tLs') return (v / 100).toFixed(2) + ' em';
    if (k === 'iconScale' || k === 'iconInner' || k === 'gap') return v + '%';
    if (k === 'pad') return v + '%';
    if (k === 'iconRot' || k === 'gAngle') return v + '°';
    return String(v);
  }

  function bindInputs() {
    $all('[data-k]').forEach(function (el) {
      var evt = (el.tagName === 'SELECT' || el.type === 'checkbox' || el.type === 'radio') ? 'change' : 'input';
      el.addEventListener(evt, function () {
        var k = el.getAttribute('data-k');
        var v;
        if (el.type === 'checkbox') v = el.checked;
        else if (el.type === 'range' || el.type === 'number' || el.getAttribute('data-num') !== null) v = Number(el.value);
        else v = el.value;
        if (el.type === 'radio' && !el.checked) return;
        if (el.type === 'number') {
          if (!isFinite(v) || v <= 0) return;
          v = clamp(Math.round(v), 16, 4000);
        }
        state[k] = v;
        if (k === 'sizeKey') {
          var p = SIZES.filter(function (s) { return s[0] === v; })[0];
          if (p && p[2]) { state.w = p[2]; state.h = p[3]; }
        }
        if (k === 'font') state.weight = nearestWeight(v, state.weight);
        if (k === 'shape' && state.layout === 'emblem' && v === 'none') state.layout = 'top';
        if (k === 'shapeStyle') fixContrast();
        syncControls();
        update();
      });
    });
  }

  function buildFontPicker() {
    var wrap = $('#lm-fonts');
    wrap.innerHTML = FONTS.map(function (f, i) {
      return '<label class="lm-font"><input type="radio" name="lm-font" value="' + esc(f[0]) + '" data-k="font"' + (i === 0 ? '' : '') + ' />' +
        '<span style="font-family:\'lmprev-' + esc(f[0]) + '\', ' + (f[1] === 'serif' ? 'Georgia, serif' : f[1] === 'script' ? 'cursive' : 'system-ui, sans-serif') + '">' + esc(f[0]) + '</span></label>';
    }).join('');
    var sel = $('#lm-tfont');
    sel.innerHTML = '<option value="">Same as brand name</option>' + FONTS.map(function (f) { return '<option value="' + esc(f[0]) + '">' + esc(f[0]) + '</option>'; }).join('');
  }

  function buildShapes() {
    $('#lm-shapes').innerHTML = SHAPES.map(function (s) {
      var prev = s === 'none'
        ? '<svg viewBox="0 0 100 100" aria-hidden="true"><path d="M20 20 L80 80 M80 20 L20 80" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg>'
        : '<svg viewBox="-4 -4 108 108" aria-hidden="true">' + shapeSvg(s, 0, 0, 100, 'currentColor', 'fill', 0) + '</svg>';
      return '<button type="button" class="lm-chip" data-shape="' + s + '" aria-pressed="false" title="' + SHAPE_LABEL[s] + '">' + prev + '<span>' + SHAPE_LABEL[s] + '</span></button>';
    }).join('');
    $('#lm-shapes').addEventListener('click', function (e) {
      var b = e.target.closest('[data-shape]'); if (!b) return;
      var v = b.getAttribute('data-shape');
      var patch = { shape: v };
      if (v === 'none' && state.layout === 'emblem') patch.layout = 'top';
      setState(patch);
    });
  }

  function buildLayouts() {
    $('#lm-layouts').innerHTML = Object.keys(LAYOUTS).map(function (k) {
      var ill = {
        left: '<rect x="6" y="14" width="20" height="20" rx="10"/><rect x="32" y="18" width="40" height="7" rx="2"/><rect x="32" y="29" width="26" height="4" rx="2"/>',
        top: '<rect x="30" y="4" width="18" height="18" rx="9"/><rect x="16" y="27" width="46" height="7" rx="2"/><rect x="25" y="38" width="28" height="4" rx="2"/>',
        icon: '<rect x="25" y="8" width="30" height="30" rx="15"/>',
        text: '<rect x="12" y="17" width="56" height="9" rx="2"/><rect x="22" y="30" width="36" height="4" rx="2"/>',
        emblem: '<circle cx="40" cy="24" r="21"/><rect x="28" y="22" width="24" height="5" rx="2" fill="#fff"/><rect x="33" y="30" width="14" height="3" rx="1.5" fill="#fff"/><circle cx="40" cy="14" r="4" fill="#fff"/>'
      }[k];
      return '<button type="button" class="lm-chip lm-layout" data-layout="' + k + '" aria-pressed="false"><svg viewBox="0 0 80 46" aria-hidden="true" fill="currentColor">' + ill + '</svg><span>' + LAYOUTS[k] + '</span></button>';
    }).join('');
    $('#lm-layouts').addEventListener('click', function (e) {
      var b = e.target.closest('[data-layout]'); if (!b) return;
      var v = b.getAttribute('data-layout');
      var patch = { layout: v };
      if (v === 'emblem' && state.shape === 'none') patch.shape = 'circle';
      if ((v === 'left' || v === 'top' || v === 'icon') && !ICON_MAP[state.icon] && ICONS.length) patch.icon = 'sparkles';
      setState(patch);
    });
  }

  function buildPalettes() {
    $('#lm-palettes').innerHTML = PALETTES.map(function (p, i) {
      return '<button type="button" class="lm-palette" data-pal="' + i + '" aria-label="Apply ' + esc(p[0]) + ' color palette" title="' + esc(p[0]) + '">' +
        [p[1], p[2], p[6], p[4]].map(function (c) { return '<i style="background:' + c + '"></i>'; }).join('') + '</button>';
    }).join('');
    $('#lm-palettes').addEventListener('click', function (e) {
      var b = e.target.closest('[data-pal]'); if (!b) return;
      setState(paletteToPatch(PALETTES[+b.getAttribute('data-pal')]));
      announce(PALETTES[+b.getAttribute('data-pal')][0] + ' palette applied');
    });
  }
  function paletteToPatch(p) {
    var emblemFill = state.layout === 'emblem' && state.shapeStyle === 'fill';
    return { cBg: p[1], cShape: p[2], cIcon: state.shape === 'none' ? p[2] : p[3], cName: emblemFill ? p[3] : p[4], cTag: emblemFill ? p[3] : p[5], cShape2: p[6], cName2: p[6], cBg2: p[6] };
  }

  function buildTemplates() {
    $('#lm-templates').innerHTML = TEMPLATES.map(function (t, i) {
      return '<button type="button" class="lm-template" data-tpl="' + i + '"><i style="background:' + (t.s.gShape ? 'linear-gradient(135deg,' + t.s.cShape + ',' + t.s.cShape2 + ')' : t.s.cShape) + '"></i>' + esc(t.label) + '</button>';
    }).join('');
    $('#lm-templates').addEventListener('click', function (e) {
      var b = e.target.closest('[data-tpl]'); if (!b) return;
      var t = TEMPLATES[+b.getAttribute('data-tpl')];
      setState(Object.assign({}, t.s));
      announce(t.label + ' template applied');
    });
  }

  // ---------- Icons ----------
  function loadIcons() {
    return fetch('/free-logo-maker/icons.json').then(function (r) { return r.json(); }).then(function (list) {
      ICONS = list;
      list.forEach(function (ic) { ICON_MAP[ic[0]] = ic; });
      var grid = $('#lm-icons');
      grid.innerHTML = '<button type="button" class="lm-icon" data-icon="" aria-pressed="false" aria-label="No icon" title="No icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>' +
        list.map(function (ic) {
          return '<button type="button" class="lm-icon" data-icon="' + ic[0] + '" data-tags="' + esc(ic[0].replace(/-/g, ' ') + ' ' + ic[2]) + '" aria-pressed="false" aria-label="' + esc(ic[0].replace(/-/g, ' ')) + '" title="' + esc(ic[0].replace(/-/g, ' ')) + '"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + ic[1] + '</svg></button>';
        }).join('');
      $('#lm-icon-count').textContent = list.length + ' icons';
      syncControls();
      render();
    }).catch(function () {
      $('#lm-icons').innerHTML = '<p>Icons could not load. Check your connection and refresh.</p>';
    });
  }
  function bindIcons() {
    $('#lm-icons').addEventListener('click', function (e) {
      var b = e.target.closest('[data-icon]'); if (!b) return;
      var v = b.getAttribute('data-icon');
      var patch = { icon: v };
      if (!v && (state.layout === 'icon')) patch.layout = 'text';
      if (v && state.layout === 'text') patch.layout = 'top';
      setState(patch);
    });
    var search = $('#lm-icon-search');
    search.addEventListener('input', function () {
      var q = search.value.trim().toLowerCase();
      var words = q.split(/\s+/).filter(Boolean);
      var shown = 0;
      $all('#lm-icons [data-icon]').forEach(function (b) {
        var tags = b.getAttribute('data-tags') || 'none';
        var ok = !words.length || words.every(function (w) { return tags.indexOf(w) >= 0; });
        b.hidden = !ok;
        if (ok) shown++;
      });
      $('#lm-icon-count').textContent = words.length ? shown + ' match' + (shown === 1 ? '' : 'es') : ICONS.length + ' icons';
    });
  }

  // ---------- Tabs ----------
  function bindTabs() {
    var tabs = $all('[role="tab"]');
    function select(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      if (focus) tab.focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
        if (e.key === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === 'Home') n = tabs[0];
        if (e.key === 'End') n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
  }

  // ---------- Randomize ----------
  var NICE_ICONS = ['rocket', 'star', 'sparkles', 'zap', 'flame', 'leaf', 'sprout', 'mountain', 'sun', 'moon', 'globe', 'compass', 'anchor', 'heart', 'crown', 'gem', 'shield-check', 'target', 'house', 'building-2', 'briefcase', 'chart-line', 'trending-up', 'coffee', 'chef-hat', 'pizza', 'camera', 'music', 'palette', 'pen-tool', 'code', 'cpu', 'brain', 'lightbulb', 'atom', 'puzzle', 'wrench', 'hammer', 'book-open', 'graduation-cap', 'megaphone', 'dumbbell', 'paw-print', 'flower-2', 'trees', 'waves', 'droplet', 'feather', 'infinity', 'hexagon', 'scissors', 'car', 'truck', 'plane', 'key-round', 'layers', 'bird', 'fish', 'cake', 'wine'];
  function inspire() {
    var pal = rnd(PALETTES);
    var layout = rnd(['left', 'left', 'top', 'top', 'emblem', 'text', 'icon']);
    var shape = rnd(['none', 'circle', 'rounded', 'shield', 'hexagon', 'seal', 'square', 'diamond', 'none']);
    if (layout === 'emblem' && shape === 'none') shape = rnd(['circle', 'seal', 'shield', 'hexagon']);
    var font = rnd(FONTS);
    var tf = rnd(FONTS.filter(function (f) { return f[1] === 'sans' || f[1] === 'rounded' || f[1] === 'serif'; }));
    var style = rnd(['fill', 'fill', 'fill', 'outline']);
    var patch = {
      font: font[0], weight: rnd(font[2].filter(function (w) { return w >= 400; }).concat(font[2])),
      tcase: font[1] === 'script' ? 'none' : rnd(['none', 'none', 'upper', 'lower', 'title']),
      ls: font[1] === 'script' ? 0 : rnd([0, 0, 2, 5, 10, -2]),
      tFont: rnd(['', tf[0], tf[0]]), tWeight: rnd([400, 500, 600]), tCase: rnd(['upper', 'none', 'upper']), tLs: rnd([10, 20, 30, 5]),
      icon: ICONS.length ? (Math.random() < 0.85 ? rnd(NICE_ICONS.filter(function (n) { return ICON_MAP[n]; })) : rnd(ICONS)[0]) : state.icon,
      iconRot: 0, iconStroke: rnd([1.5, 2, 2, 2.5]), iconInner: rnd([50, 56, 60]), iconScale: 100,
      shape: shape, shapeStyle: style, layout: layout,
      gShape: Math.random() < 0.4, gName: Math.random() < 0.12, gBg: false,
      gAngle: rnd([90, 135, 180, 45]), transparent: false
    };
    Object.assign(state, patch);
    Object.assign(state, paletteToPatch(pal));
    if (shape === 'none' || style === 'outline') state.cIcon = pal[2];
    if (layout === 'emblem' && style === 'outline') { state.cName = pal[2]; state.cTag = pal[5]; }
    if (layout === 'emblem' && style === 'fill') { state.cName = pal[3]; state.cTag = pal[3]; }
    fixContrast();
    syncControls();
    update();
    announce('New random design');
  }

  // ---------- Export ----------
  function fontCssFor(st) {
    var tFam = st.tFont && FONT_MAP[st.tFont] ? st.tFont : st.font;
    var jobs = [];
    var nameTxt = applyCase(st.name || '', st.tcase);
    var tagTxt = applyCase(st.tagline || '', st.tCase);
    var need = {};
    function add(fam, w, txt) { if (!txt) return; var key = fam + '|' + w; need[key] = (need[key] || '') + txt; }
    add(st.font, nearestWeight(st.font, st.weight), nameTxt + (ICON_MAP[st.icon] ? '' : nameTxt.charAt(0).toUpperCase()));
    add(tFam, nearestWeight(tFam, st.tWeight), tagTxt);
    Object.keys(need).forEach(function (key) {
      var parts = key.split('|');
      var chars = Array.from(new Set(Array.from(need[key]))).join('');
      var url = 'https://fonts.googleapis.com/css2?family=' + encodeURIComponent(parts[0]).replace(/%20/g, '+') + ':wght@' + parts[1] + '&text=' + encodeURIComponent(chars);
      jobs.push(fetch(url).then(function (r) { return r.ok ? r.text() : ''; }).then(function (css) {
        var srcs = [];
        css.replace(/url\(([^)]+)\)\s*format\('([^']+)'\)/g, function (m, u, f) { srcs.push([u, f]); return m; });
        return Promise.all(srcs.map(function (s) {
          return fetch(s[0]).then(function (r) { return r.arrayBuffer(); }).then(function (buf) {
            return "@font-face{font-family:'" + parts[0] + "';font-style:normal;font-weight:" + parts[1] + ";src:url(data:font/" + s[1] + ';base64,' + b64(buf) + ") format('" + s[1] + "')}";
          });
        })).then(function (a) { return a.join(''); });
      }).catch(function () { return ''; }));
    });
    return Promise.all(jobs).then(function (a) { return a.join(''); });
  }
  function b64(buf) {
    var bytes = new Uint8Array(buf), bin = '';
    for (var i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    return btoa(bin);
  }

  function svgToCanvas(svg, w, h, bg) {
    return new Promise(function (resolve, reject) {
      var img = new Image();
      var url = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml;charset=utf-8' }));
      img.onload = function () {
        var draw = function () {
          var c = document.createElement('canvas');
          c.width = w; c.height = h;
          var ctx = c.getContext('2d');
          if (bg) { ctx.fillStyle = bg; ctx.fillRect(0, 0, w, h); }
          ctx.drawImage(img, 0, 0, w, h);
          URL.revokeObjectURL(url);
          resolve(c);
        };
        // give embedded fonts a moment to be applied inside the SVG image
        (img.decode ? img.decode().catch(function () {}) : Promise.resolve()).then(function () { setTimeout(draw, 60); });
      };
      img.onerror = function () { URL.revokeObjectURL(url); reject(new Error('Could not render image')); };
      img.src = url;
    });
  }
  function canvasBlob(c, type, q) {
    return new Promise(function (res) { c.toBlob(function (b) { res(b); }, type, q); });
  }
  function download(blob, name) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
  }

  var fontCssCache = { key: '', css: '' };
  function getFontCss(st) {
    var key = [st.font, st.weight, st.tFont, st.tWeight, st.name, st.tagline, st.tcase, st.tCase, st.icon].join('|');
    if (fontCssCache.key === key) return Promise.resolve(fontCssCache.css);
    return fontCssFor(st).then(function (css) { fontCssCache = { key: key, css: css }; return css; });
  }

  function exportScale() { return clamp(Number(state.scale) || 1, 1, 4); }
  function outDims() {
    var s = exportScale();
    var w = Math.round(state.w * s), h = Math.round(state.h * s);
    var max = 8000;
    if (w > max || h > max) { var k = max / Math.max(w, h); w = Math.round(w * k); h = Math.round(h * k); }
    return { w: w, h: h };
  }
  function baseName() { return slug(state.name) + '-logo'; }

  var busy = false;
  function withBusy(btn, fn) {
    if (busy) return;
    busy = true;
    var label = btn.innerHTML;
    btn.disabled = true; btn.setAttribute('aria-busy', 'true');
    btn.innerHTML = 'Preparing…';
    return fontsReady().then(fn).then(function (msg) {
      showCta(msg);
    }).catch(function (err) {
      announce('Export failed: ' + (err && err.message ? err.message : 'unknown error'));
      alert('Sorry — the export failed in this browser. Try another browser or a smaller size.');
    }).then(function () {
      busy = false; btn.disabled = false; btn.removeAttribute('aria-busy'); btn.innerHTML = label;
    });
  }

  function exportRaster(type) {
    var d = outDims();
    return getFontCss(state).then(function (css) {
      var jpg = type === 'jpg';
      var svg = buildSvg(state, { w: d.w, h: d.h, fontCss: css, transparent: jpg ? true : state.transparent });
      var bg = jpg ? (state.transparent ? '#ffffff' : null) : null;
      if (jpg && !state.transparent) { svg = buildSvg(state, { w: d.w, h: d.h, fontCss: css, transparent: false }); }
      return svgToCanvas(svg, d.w, d.h, bg).then(function (c) {
        return canvasBlob(c, jpg ? 'image/jpeg' : 'image/png', 0.92);
      }).then(function (blob) {
        var name = baseName() + '-' + d.w + 'x' + d.h + (type === 'png' && state.transparent ? '-transparent' : '') + '.' + type;
        download(blob, name);
        return name;
      });
    });
  }
  function exportSvg() {
    return getFontCss(state).then(function (css) {
      var svg = '<?xml version="1.0" encoding="UTF-8"?>\n<!-- Made with the free logo maker at https://www.mindfulmarketingagency.net/free-logo-maker/ — icon from Lucide (ISC license) -->\n' +
        buildSvg(state, { fontCss: css, title: state.name || 'Logo' });
      var name = baseName() + '.svg';
      download(new Blob([svg], { type: 'image/svg+xml' }), name);
      return name;
    });
  }

  // Minimal ZIP writer (store, no compression) — PNGs are already compressed.
  var CRC_TABLE = (function () {
    var t = new Uint32Array(256);
    for (var n = 0; n < 256; n++) { var c = n; for (var k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; }
    return t;
  })();
  function crc32(u8) { var c = 0xFFFFFFFF; for (var i = 0; i < u8.length; i++) c = CRC_TABLE[(c ^ u8[i]) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; }
  function makeZip(files) { // [{name, data:Uint8Array}]
    var enc = new TextEncoder(), parts = [], central = [], offset = 0;
    var now = new Date();
    var dosTime = (now.getHours() << 11) | (now.getMinutes() << 5) | (now.getSeconds() >> 1);
    var dosDate = ((now.getFullYear() - 1980) << 9) | ((now.getMonth() + 1) << 5) | now.getDate();
    files.forEach(function (f) {
      var nameB = enc.encode(f.name), crc = crc32(f.data), size = f.data.length;
      var lh = new DataView(new ArrayBuffer(30));
      lh.setUint32(0, 0x04034b50, true); lh.setUint16(4, 20, true); lh.setUint16(6, 0x0800, true); lh.setUint16(8, 0, true);
      lh.setUint16(10, dosTime, true); lh.setUint16(12, dosDate, true); lh.setUint32(14, crc, true);
      lh.setUint32(18, size, true); lh.setUint32(22, size, true); lh.setUint16(26, nameB.length, true); lh.setUint16(28, 0, true);
      parts.push(new Uint8Array(lh.buffer), nameB, f.data);
      var ch = new DataView(new ArrayBuffer(46));
      ch.setUint32(0, 0x02014b50, true); ch.setUint16(4, 20, true); ch.setUint16(6, 20, true); ch.setUint16(8, 0x0800, true); ch.setUint16(10, 0, true);
      ch.setUint16(12, dosTime, true); ch.setUint16(14, dosDate, true); ch.setUint32(16, crc, true); ch.setUint32(20, size, true); ch.setUint32(24, size, true);
      ch.setUint16(28, nameB.length, true); ch.setUint16(30, 0, true); ch.setUint16(32, 0, true); ch.setUint16(34, 0, true); ch.setUint16(36, 0, true);
      ch.setUint32(38, 0, true); ch.setUint32(42, offset, true);
      central.push(new Uint8Array(ch.buffer), nameB);
      offset += 30 + nameB.length + size;
    });
    var cdSize = central.reduce(function (a, b) { return a + b.length; }, 0);
    var end = new DataView(new ArrayBuffer(22));
    end.setUint32(0, 0x06054b50, true); end.setUint16(8, files.length, true); end.setUint16(10, files.length, true);
    end.setUint32(12, cdSize, true); end.setUint32(16, offset, true);
    return new Blob(parts.concat(central, [new Uint8Array(end.buffer)]), { type: 'application/zip' });
  }
  function makeIco(pngs) { // [{size, data}]
    var header = new DataView(new ArrayBuffer(6 + 16 * pngs.length));
    header.setUint16(0, 0, true); header.setUint16(2, 1, true); header.setUint16(4, pngs.length, true);
    var offset = 6 + 16 * pngs.length;
    pngs.forEach(function (p, i) {
      var o = 6 + i * 16;
      header.setUint8(o, p.size >= 256 ? 0 : p.size); header.setUint8(o + 1, p.size >= 256 ? 0 : p.size);
      header.setUint8(o + 2, 0); header.setUint8(o + 3, 0); header.setUint16(o + 4, 1, true); header.setUint16(o + 6, 32, true);
      header.setUint32(o + 8, p.data.length, true); header.setUint32(o + 12, offset, true);
      offset += p.data.length;
    });
    var out = new Uint8Array(offset);
    out.set(new Uint8Array(header.buffer), 0);
    var pos = 6 + 16 * pngs.length;
    pngs.forEach(function (p) { out.set(p.data, pos); pos += p.data.length; });
    return out;
  }

  function exportFavicons() {
    var markOnly = true;
    var sizes = [16, 32, 48, 180, 192, 512];
    return getFontCss(state).then(function (css) {
      var big = buildSvg(state, { w: 512, h: 512, fontCss: css, markOnly: markOnly, pad: markOnly ? 4 : 8 });
      return Promise.all(sizes.map(function (s) {
        var opaque = s === 180; // iOS ignores transparency
        var svg = opaque && state.transparent ? buildSvg(state, { w: 512, h: 512, fontCss: css, markOnly: markOnly, pad: 10, transparent: false, bgOverride: state.cBg }) : big;
        return svgToCanvas(svg, s, s).then(function (c) { return canvasBlob(c, 'image/png'); })
          .then(function (b) { return b.arrayBuffer(); }).then(function (ab) { return { size: s, data: new Uint8Array(ab) }; });
      }));
    }).then(function (pngs) {
      var by = {}; pngs.forEach(function (p) { by[p.size] = p.data; });
      var enc = new TextEncoder();
      var app = state.name || 'My Brand';
      var manifest = JSON.stringify({ name: app, short_name: app.slice(0, 12), icons: [{ src: '/android-chrome-192x192.png', sizes: '192x192', type: 'image/png' }, { src: '/android-chrome-512x512.png', sizes: '512x512', type: 'image/png' }], theme_color: state.cShape, background_color: state.cBg, display: 'standalone' }, null, 2);
      var readme = 'Favicon pack for ' + app + '\n\nUpload these files to the root folder of your website, then paste this inside <head>:\n\n' +
        '<link rel="icon" href="/favicon.ico" sizes="any">\n<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">\n<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">\n<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">\n<link rel="manifest" href="/site.webmanifest">\n\n' +
        'WordPress, Wix, Squarespace and Shopify: upload android-chrome-512x512.png as your "Site icon" / "Favicon" in the site settings.\n\nMade with the free logo maker by Mindful Marketing Agency — https://www.mindfulmarketingagency.net/free-logo-maker/\n';
      var files = [
        { name: 'favicon.ico', data: makeIco([16, 32, 48].map(function (s) { return { size: s, data: by[s] }; })) },
        { name: 'favicon-16x16.png', data: by[16] },
        { name: 'favicon-32x32.png', data: by[32] },
        { name: 'favicon-48x48.png', data: by[48] },
        { name: 'apple-touch-icon.png', data: by[180] },
        { name: 'android-chrome-192x192.png', data: by[192] },
        { name: 'android-chrome-512x512.png', data: by[512] },
        { name: 'site.webmanifest', data: enc.encode(manifest) },
        { name: 'README.txt', data: enc.encode(readme) }
      ];
      var name = baseName() + '-favicon-pack.zip';
      download(makeZip(files), name);
      return name;
    });
  }

  function showCta(fileName) {
    var cta = $('#lm-cta');
    $('#lm-cta-file').textContent = fileName;
    cta.hidden = false;
    announce('Downloaded ' + fileName);
    try {
      var d = document.getElementById('description');
      if (d && !d.value) d.value = 'I made a starter logo for "' + (state.name || 'my business') + '" with your free logo maker and would like a professional version / brand kit.';
    } catch (e) { /* ignore */ }
  }

  function bindExport() {
    $all('[data-export]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var t = btn.getAttribute('data-export');
        withBusy(btn, function () {
          if (t === 'png' || t === 'jpg') return exportRaster(t);
          if (t === 'svg') return exportSvg();
          if (t === 'favicon') return exportFavicons();
        });
      });
    });
    $('#lm-cta-close').addEventListener('click', function () { $('#lm-cta').hidden = true; });
  }

  // ---------- Init ----------
  function init() {
    buildFontPicker();
    buildShapes();
    buildLayouts();
    buildPalettes();
    buildTemplates();
    $('#lm-size').innerHTML = SIZES.map(function (s) { return '<option value="' + s[0] + '">' + s[1] + '</option>'; }).join('');
    bindTabs();
    bindInputs();
    bindIcons();
    bindExport();
    $('#lm-undo').addEventListener('click', undo);
    $('#lm-redo').addEventListener('click', redo);
    $('#lm-random').addEventListener('click', inspire);
    $('#lm-reset').addEventListener('click', function () {
      if (!confirm('Start over with a blank design? (You can still undo.)')) return;
      state = Object.assign({}, DEFAULT);
      syncControls(); update(); announce('Design reset');
    });
    document.addEventListener('keydown', function (e) {
      if (!(e.ctrlKey || e.metaKey)) return;
      var t = e.target;
      if (t && (t.tagName === 'TEXTAREA' || (t.tagName === 'INPUT' && (t.type === 'text' || t.type === 'search' || t.type === 'email' || t.type === 'tel')))) return;
      var k = e.key.toLowerCase();
      if (k === 'z' && !e.shiftKey) { e.preventDefault(); undo(); }
      else if ((k === 'z' && e.shiftKey) || k === 'y') { e.preventDefault(); redo(); }
    });
    root.classList.add('is-ready');
    syncControls();
    updateHistoryButtons();
    render();
    fontsReady().then(render);
    loadIcons();
    if ('requestIdleCallback' in window) requestIdleCallback(loadFontPreviews); else setTimeout(loadFontPreviews, 400);
    // Test hook for automated checks
    window.__logoMaker = { state: function () { return state; }, buildSvg: function (o) { return buildSvg(state, o); } };
  }
  init();
})();
