// Georgia Marketing Agencies directory — static-data listing engine.
// Listing data lives in /data/agencies.json (regenerated whenever new
// Outscraper data is imported — see generate_directory.py).
(function () {
  const DATA_URL = '/data/agencies.json';

  const CITIES = [
    { slug: 'atlanta', name: 'Atlanta' },
    { slug: 'savannah', name: 'Savannah' },
    { slug: 'augusta', name: 'Augusta' },
    { slug: 'columbus', name: 'Columbus' },
    { slug: 'macon', name: 'Macon' },
    { slug: 'athens', name: 'Athens' },
    { slug: 'sandy-springs', name: 'Sandy Springs' },
    { slug: 'roswell', name: 'Roswell' },
    { slug: 'albany', name: 'Albany' },
    { slug: 'warner-robins', name: 'Warner Robins' },
  ];

  // path is the canonical URL for each category. The three main branches
  // (SEO, Digital Marketing, Social Media Marketing) live at the site root;
  // the rest stay nested under /services/.
  // branchLabel/branchDesc are used only for the "Main Service Branches"
  // cards, since those 3 pages are our own services (drop-serviced), not
  // directory listings of other agencies — so their copy reads differently
  // from the directory-browse category cards.
  const CATEGORIES = [
    { slug: 'seo-agencies', name: 'SEO Agencies', path: '/seo/', branch: true, branchLabel: 'SEO', branchDesc: 'Done-for-you SEO, from technical setup to keyword-rich content.' },
    { slug: 'ppc-paid-media-agencies', name: 'PPC & Paid Media Agencies', path: '/services/ppc-paid-media-agencies/' },
    { slug: 'social-media-marketing-agencies', name: 'Social Media Marketing Agencies', path: '/social-media-marketing/', branch: true, branchLabel: 'Social Media Marketing', branchDesc: 'Content, scheduling, and community management, handled for you.' },
    { slug: 'web-design-agencies', name: 'Web Design Agencies', path: '/services/web-design-agencies/' },
    { slug: 'branding-graphic-design-agencies', name: 'Branding & Graphic Design Agencies', path: '/services/branding-graphic-design-agencies/' },
    { slug: 'content-marketing-agencies', name: 'Content Marketing Agencies', path: '/services/content-marketing-agencies/' },
    { slug: 'email-marketing-agencies', name: 'Email Marketing Agencies', path: '/services/email-marketing-agencies/' },
    { slug: 'full-service-digital-marketing-agencies', name: 'Full-Service Digital Marketing Agencies', path: '/digital-marketing/', branch: true, branchLabel: 'Digital Marketing', branchDesc: 'Strategy, SEO, social, and paid media working together under one roof.' },
  ];

  let agenciesCache = null;

  async function loadAgencies() {
    if (agenciesCache) return agenciesCache;
    try {
      const res = await fetch(DATA_URL);
      agenciesCache = res.ok ? await res.json() : [];
    } catch (e) {
      agenciesCache = [];
    }
    return agenciesCache;
  }

  // Cities are derived from the actual data (there can be 100+ once real
  // Outscraper data is imported) — the hardcoded CITIES list above is only
  // a fallback for when data/agencies.json is still empty.
  let citiesCache = null;

  async function getCities() {
    if (citiesCache) return citiesCache;
    const agencies = await loadAgencies();
    if (!agencies.length) {
      citiesCache = CITIES.map(c => ({ ...c, count: 0 }));
      return citiesCache;
    }
    const byCity = new Map();
    agencies.forEach(a => {
      if (!a.city_slug || !a.city) return;
      const existing = byCity.get(a.city_slug);
      if (existing) existing.count += 1;
      else byCity.set(a.city_slug, { slug: a.city_slug, name: a.city, count: 1 });
    });
    citiesCache = Array.from(byCity.values());
    return citiesCache;
  }

  function renderStars(rating) {
    if (!rating) return '';
    const full = Math.round(rating);
    return '★'.repeat(full) + '☆'.repeat(5 - full);
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
  }

  function listingCardHtml(a) {
    const href = `/${a.city_slug}/${a.slug}/`;
    const rating = a.rating ? `
      <div class="listing-rating">
        <span class="stars">${renderStars(a.rating)}</span>
        <span class="rating-num">${Number(a.rating).toFixed(1)}</span>
        ${a.reviews_count ? `<span class="review-count">(${a.reviews_count} review${a.reviews_count === 1 ? '' : 's'})</span>` : ''}
      </div>` : '';
    return `
      <a class="listing-card" href="${href}">
        <div class="listing-top">
          <h3>${escapeHtml(a.name)}</h3>
          ${a.featured ? '<span class="listing-featured-tag">Featured</span>' : ''}
        </div>
        ${rating}
        <div class="listing-meta">
          ${a.category ? `<span class="tag">${escapeHtml(a.category)}</span>` : ''}
          ${a.city ? `<span>${escapeHtml(a.city)}, GA</span>` : ''}
        </div>
        ${a.description ? `<p class="desc">${escapeHtml(a.description)}</p>` : ''}
      </a>`;
  }

  function emptyStateHtml({ city, category } = {}) {
    let where = 'this directory';
    if (city && category) where = `${category} in ${city}`;
    else if (city) where = city;
    else if (category) where = category;
    return `
      <div class="empty-state">
        <span class="icon">—</span>
        <h3>No listings yet for ${escapeHtml(where)}</h3>
        <p>We're actively adding agencies to the directory. Check back soon, or if you run an agency, be the first to list it.</p>
        <p style="margin-top:1.2rem;"><a class="btn btn-primary" href="/submit/">Add your agency</a></p>
      </div>`;
  }

  async function renderListings(targetSelector, { city, category, search, limit, featured } = {}) {
    const el = document.querySelector(targetSelector);
    if (!el) return;
    const all = await loadAgencies();
    let filtered = all.slice();
    if (city) filtered = filtered.filter(a => (a.city || '').toLowerCase() === city.toLowerCase());
    if (category) filtered = filtered.filter(a => (a.category || '').toLowerCase() === category.toLowerCase());
    if (featured) filtered = filtered.filter(a => a.featured);
    if (search) {
      const q = search.toLowerCase();
      filtered = filtered.filter(a => (a.name || '').toLowerCase().includes(q));
    }
    filtered.sort((a, b) => (b.featured - a.featured) || ((b.rating || 0) - (a.rating || 0)));
    if (limit) filtered = filtered.slice(0, limit);

    const countEl = document.querySelector('[data-result-count]');
    if (countEl) countEl.innerHTML = `<strong>${filtered.length}</strong> agenc${filtered.length === 1 ? 'y' : 'ies'} found`;

    if (!filtered.length) {
      el.innerHTML = emptyStateHtml({ city, category });
      return;
    }
    el.innerHTML = `<div class="listing-grid">${filtered.map(listingCardHtml).join('')}</div>`;
  }

  async function initHeroSearch() {
    const form = document.querySelector('[data-hero-search]');
    if (!form) return;
    const citySelect = form.querySelector('[name="city"]');
    const categorySelect = form.querySelector('[name="category"]');
    if (citySelect) {
      const cities = (await getCities()).slice().sort((a, b) => a.name.localeCompare(b.name));
      citySelect.innerHTML = '<option value="">Any city</option>' + cities.map(c => `<option value="${c.slug}">${c.name}</option>`).join('');
    }
    if (categorySelect) categorySelect.innerHTML = '<option value="">Any service</option>' + CATEGORIES.map(c => `<option value="${c.slug}">${c.name}</option>`).join('');

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const city = citySelect ? citySelect.value : '';
      const category = categorySelect ? categorySelect.value : '';
      if (city && category) window.location.href = `/${city}/?category=${category}`;
      else if (city) window.location.href = `/${city}/`;
      else if (category) {
        const catObj = CATEGORIES.find(c => c.slug === category);
        window.location.href = catObj ? catObj.path : `/services/${category}/`;
      } else window.location.href = '/cities/';
    });
  }

  async function populateHubGrids() {
    const cities = await getCities();

    const cityHub = document.querySelector('[data-city-hub]');
    if (cityHub) {
      // Homepage preview: top cities by listing count (most useful first).
      const top = cities.slice().sort((a, b) => b.count - a.count || a.name.localeCompare(b.name)).slice(0, 12);
      cityHub.innerHTML = top.map(c => `
        <a class="hub-card" href="/${c.slug}/">
          <h3>${c.name}</h3>
          <span class="count">${c.count ? `${c.count} agenc${c.count === 1 ? 'y' : 'ies'}` : `Marketing agencies in ${c.name}`}</span>
        </a>`).join('');
    }
    const serviceHub = document.querySelector('[data-service-hub]');
    if (serviceHub) {
      serviceHub.innerHTML = CATEGORIES.map(c => `
        <a class="hub-card" href="${c.path}">
          <h3>${c.name}</h3>
          <span class="count">Find ${c.name.toLowerCase()} in Georgia</span>
        </a>`).join('');
    }
    const cityList = document.querySelector('[data-city-list]');
    if (cityList) {
      // Full list, alphabetical.
      const all = cities.slice().sort((a, b) => a.name.localeCompare(b.name));
      cityList.innerHTML = all.map(c => `<a href="/${c.slug}/">${c.name}, GA${c.count ? ` (${c.count})` : ''}</a>`).join('');
    }
    const branchHub = document.querySelector('[data-branch-hub]');
    if (branchHub) {
      branchHub.innerHTML = CATEGORIES.filter(c => c.branch).map(c => `
        <a class="hub-card" href="${c.path}">
          <h3>${c.branchLabel || c.name}</h3>
          <span class="count">${c.branchDesc || ''}</span>
        </a>`).join('');
    }
  }

  async function loadLists() {
    try {
      const res = await fetch('/data/lists.json');
      return res.ok ? await res.json() : [];
    } catch (e) {
      return [];
    }
  }

  async function renderLists(targetSelector) {
    const el = document.querySelector(targetSelector);
    if (!el) return;
    const lists = await loadLists();
    if (!lists.length) {
      el.innerHTML = `
        <div class="empty-state">
          <span class="icon">—</span>
          <h3>No lists published yet</h3>
          <p>We're building out "best of" lists — top SEO agencies by city, top-rated social media agencies, and more. Check back soon.</p>
        </div>`;
      return;
    }
    el.innerHTML = `<div class="hub-grid">${lists.map(l => `
      <a class="hub-card" href="/lists/${l.slug}/">
        <h3>${l.title}</h3>
        <span class="count">${l.description || ''}</span>
      </a>`).join('')}</div>`;
  }

  window.GAMDirectory = { CITIES, CATEGORIES, loadAgencies, getCities, renderListings, loadLists, renderLists };

  document.addEventListener('DOMContentLoaded', () => {
    initHeroSearch();
    populateHubGrids();
  }); // both async; fire-and-forget is fine since nothing else depends on completion order
})();
