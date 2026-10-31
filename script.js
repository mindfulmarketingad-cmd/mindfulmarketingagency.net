// Mobile nav toggle
const toggle = document.querySelector('.nav-toggle');
const menu = document.getElementById('nav-menu');

if (toggle && menu) {
  toggle.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  // Close the menu after tapping a link
  menu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      menu.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// Current year in the footer
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// TOC scroll spy — highlights the active section as you scroll
(function () {
  const article = document.querySelector('.guide-article');
  const tocEl   = document.querySelector('.toc-list');
  if (!article || !tocEl) return;

  const headings = Array.from(article.querySelectorAll('h2[id], h3[id]'));
  if (!headings.length) return;

  // Build id → <a> map from every TOC anchor
  const linkMap = {};
  tocEl.querySelectorAll('a[href^="#"]').forEach(a => {
    linkMap[a.getAttribute('href').slice(1)] = a;
  });

  function setActive(id) {
    Object.values(linkMap).forEach(a => a.classList.remove('toc-active'));
    if (linkMap[id]) linkMap[id].classList.add('toc-active');
  }

  // Pick the last heading whose top edge is above the trigger line
  function onScroll() {
    const triggerY = window.scrollY + 110; // 110px offset accounts for sticky header
    let active = headings[0];
    for (const h of headings) {
      const top = h.getBoundingClientRect().top + window.scrollY;
      if (top <= triggerY) active = h;
      else break;
    }
    setActive(active.id);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

// Header shadow once the page scrolls
(function () {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

// Gentle reveal-on-scroll. Skipped entirely for reduced-motion users and old browsers,
// and never hides anything that is already on screen at load.
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const sel = '.section-head, .svc-card, .step4, .diff, .commit-item, .promise, .cta-band, .tool-card, .pricing-card, .include-card, .process-step, .why-card, .faq-item, .hub-card, .rel-card, .trust-strip, .own-cta, .split .prose';
  const els = Array.from(document.querySelectorAll(sel));
  const vh = window.innerHeight;
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  const groups = new Map();
  els.forEach((el) => {
    if (el.getBoundingClientRect().top < vh) return; // already visible: leave as is
    const parent = el.parentElement;
    const i = groups.get(parent) || 0; groups.set(parent, i + 1);
    el.style.setProperty('--d', Math.min(i, 5) * 0.07 + 's');
    el.classList.add('rv');
    io.observe(el);
  });
})();

// Hide third-party listing photos/logos that fail to load (expired Google image URLs)
document.querySelectorAll('img.listing-cover, img.listing-logo').forEach((img) => {
  const drop = () => img.remove();
  if (img.complete && img.naturalWidth === 0) drop(); else img.addEventListener('error', drop);
});
