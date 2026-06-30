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
