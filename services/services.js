// Shared service-page contact form handler — submits leads to Supabase.
(function () {
  const SUPABASE_URL = 'https://tbqigevoksabizjogvtm.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_aHlx0Tdu2rhOTBUp3lhkQw_Lv6Awz7a';

  const form = document.querySelector('.lead-form');
  if (!form) return;

  const submitBtn = form.querySelector('button[type="submit"]');
  const errorEl = form.querySelector('.form-error');
  const successEl = document.querySelector('.form-success');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (errorEl) errorEl.style.display = 'none';

    const formData = new FormData(form);
    const payload = {
      service: form.dataset.service || '',
      name: formData.get('name') || '',
      email: formData.get('email') || '',
      phone: formData.get('phone') || '',
      description: formData.get('description') || '',
      experience_level: formData.get('experience_level') || '',
      reason: formData.get('reason') || '',
      budget: formData.get('budget') || null,
      website: formData.get('website') || null,
      platforms: formData.get('platforms') || null,
      created_at: new Date().toISOString(),
    };

    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending...';

    try {
      const res = await fetch(`${SUPABASE_URL}/rest/v1/leads`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`,
          'Prefer': 'return=minimal',
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error(`Request failed: ${res.status}`);

      form.style.display = 'none';
      if (successEl) successEl.style.display = 'block';
    } catch (err) {
      if (errorEl) {
        errorEl.textContent = "Something went wrong sending your request — please email David@mindfulmarketingagency.net directly.";
        errorEl.style.display = 'block';
      }
      submitBtn.disabled = false;
      submitBtn.textContent = 'Send my request';
    }
  });
})();
