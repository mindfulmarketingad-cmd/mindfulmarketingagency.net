#!/usr/bin/env python3
"""Build /privacy-policy/, /contact/, /terms/ from about/ chrome; add footer legal links + AdSense head script sitewide."""
import os, re, glob
B = os.path.dirname(os.path.abspath(__file__))
ADS = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9332749804326149" crossorigin="anonymous"></script>'
EMAIL = 'David@mindfulmarketingagency.net'
tpl = open(os.path.join(B, 'about/index.html'), encoding='utf-8').read()
head, rest = tpl.split('<main>', 1)
_, tail = rest.split('</main>', 1)

def page(slug, title, desc, crumb, h1, lead, body, extra_js=''):
    h = head.replace('About Mindful Marketing Agency | Atlanta, GA', title)
    h = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc, h)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + desc, h)
    h = h.replace('/about/"', f'/{slug}/"')
    h = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '', h, flags=re.S)
    main = f'''<main>
    <section class="page-hero">
      <div class="page-hero-inner">
        <p class="crumbs"><a href="/">Home</a> / {crumb}</p>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
      </div>
    </section>
    <article class="article">
{body}
    </article>
  </main>'''
    t = tail
    if extra_js:
        t = t.replace('</body>', extra_js + '\n</body>')
    os.makedirs(os.path.join(B, slug), exist_ok=True)
    open(os.path.join(B, slug, 'index.html'), 'w', encoding='utf-8').write(h + main + t)

UPD = 'November 4, 2026'
page('privacy-policy', 'Privacy Policy | Mindful Marketing Agency',
 'How Mindful Marketing Agency collects, uses, and protects your information, including forms, payments, cookies, and Google advertising.',
 'Privacy Policy', 'Privacy Policy', f'Last updated: {UPD}', f'''
      <p>This Privacy Policy explains how Mindful Marketing Agency ("we", "us") collects, uses, and shares information when you visit mindfulmarketingagency.net (the "Site") or buy our services.</p>
      <h2>Information we collect</h2>
      <ul>
        <li><strong>Information you submit.</strong> When you fill out a request, proposal, contact, or agency-listing form, we collect what you enter, such as your name, email, phone number, website, business details, and message. Form submissions are stored securely with our database provider, Supabase.</li>
        <li><strong>Payment information.</strong> Payments are processed by Stripe. We do not see or store your full card number. Stripe handles your payment details under its own <a href="https://stripe.com/privacy" rel="noopener">privacy policy</a>. We receive limited details such as your name, email, amount, and purchase.</li>
        <li><strong>Usage data and cookies.</strong> Like most websites, our hosting provider and third-party services may automatically collect information such as IP address, browser type, pages visited, and referring site. Cookies and similar technologies may be used for this.</li>
        <li><strong>Free tools.</strong> Our free logo maker runs in your browser. Logos you design are not uploaded to our servers.</li>
      </ul>
      <h2>How we use information</h2>
      <ul>
        <li>To reply to your request and deliver the services you buy.</li>
        <li>To process payments, send receipts, and keep business records.</li>
        <li>To operate, secure, and improve the Site.</li>
        <li>To show advertising, as described below.</li>
      </ul>
      <p>We do not sell your personal information. We share it only with service providers that help us run the business (such as Supabase, Stripe, our hosting provider Vercel, and specialists who help fulfill your project under confidentiality), or when required by law.</p>
      <h2>Advertising and Google AdSense</h2>
      <p>We use Google AdSense to show ads on this Site. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this Site or other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to this Site and/or other sites on the internet.</p>
      <p>You may opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies for personalized advertising at <a href="https://www.aboutads.info/choices/" rel="noopener">www.aboutads.info</a>. Learn more about how Google uses information from sites that use its services at <a href="https://policies.google.com/technologies/ads" rel="noopener">https://policies.google.com/technologies/ads</a>.</p>
      <h2>Your choices</h2>
      <p>You can set your browser to refuse or delete cookies. You can ask us to access, correct, or delete the personal information you've given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>. We'll respond within two business days.</p>
      <h2>Data retention and security</h2>
      <p>We keep information as long as needed to provide services and meet legal and accounting obligations, and we use reasonable safeguards to protect it. No method of transmission or storage is completely secure.</p>
      <h2>Children</h2>
      <p>The Site is meant for businesses and is not directed to children under 13. We do not knowingly collect their information.</p>
      <h2>Changes</h2>
      <p>We may update this policy. The date at the top shows the latest version.</p>
      <h2>Contact</h2>
      <p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or use our <a href="/contact/">contact page</a>.</p>''')

page('terms', 'Terms of Service | Mindful Marketing Agency',
 'Terms of service for mindfulmarketingagency.net and services purchased from Mindful Marketing Agency.',
 'Terms of Service', 'Terms of Service', f'Last updated: {UPD}', f'''
      <p>By using mindfulmarketingagency.net (the "Site") or buying a service from Mindful Marketing Agency ("we", "us"), you agree to these terms.</p>
      <h2>Services</h2>
      <p>Each service page describes the scope, deliverables, and price of a package. We may use trusted specialists to help deliver your project; we remain responsible for the work. After purchase we may ask for information or access needed to start, and delivery timelines begin once we have it.</p>
      <h2>Payments</h2>
      <p>Prices are in US dollars and are paid upfront through Stripe unless agreed otherwise. Monthly plans renew each month until canceled; you can cancel anytime before the next billing date and there are no long-term contracts.</p>
      <h2>Refunds and revisions</h2>
      <p>If a deliverable doesn't match the described scope, tell us and we'll make it right through revisions. If we can't deliver what was described, we'll refund the undelivered portion. Work already delivered and completed months of a monthly plan are not refundable.</p>
      <h2>No guaranteed rankings</h2>
      <p>Search engines and ad platforms control their own results. We do not guarantee specific rankings, traffic, leads, or sales.</p>
      <h2>Your responsibilities</h2>
      <p>You confirm that you have the right to the content, accounts, and materials you provide, and that your business and ads comply with applicable laws and platform policies.</p>
      <h2>Directory listings</h2>
      <p>Agency listings in our Georgia directory are provided for information only and are not endorsements. Information may be incomplete or out of date; please verify details with each business.</p>
      <h2>Free tools</h2>
      <p>Free tools such as the logo maker are provided "as is" without warranty. You are responsible for checking that your designs don't infringe anyone else's trademarks.</p>
      <h2>Limitation of liability</h2>
      <p>To the extent allowed by law, our total liability for any claim is limited to the amount you paid us for the service in question, and we are not liable for indirect or consequential damages.</p>
      <h2>Governing law</h2>
      <p>These terms are governed by the laws of the State of Georgia, USA.</p>
      <h2>Contact</h2>
      <p>Questions about these terms? Email <a href="mailto:{EMAIL}">{EMAIL}</a>. See also our <a href="/privacy-policy/">Privacy Policy</a>.</p>''')

# contact page reuses the lead form + service-leads.js (saves to Supabase leads)
bl = open(os.path.join(B, 'backlinks/index.html'), encoding='utf-8').read()
leads_js = re.search(r'<script src="/service-leads\.js[^"]*"></script>', bl).group(0)
form = f'''      <h2>Send us a message</h2>
      <p>Tell us about your business and what you need. We reply within two business days. Prefer email? Write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      <form class="lead-form" data-service="Contact">
          <div class="form-grid">
            <div class="form-group full">
              <label for="tier">What can we help with? <span class="req">*</span></label>
              <select id="tier" name="tier" required>
                <option value="">Select a topic</option>
                <option value="General question">General question</option>
                <option value="SEO / Local SEO">SEO / Local SEO</option>
                <option value="Google Business Profile">Google Business Profile</option>
                <option value="Ads management">Google, Facebook or Instagram ads</option>
                <option value="Social media">Social media</option>
                <option value="Website design">Website design</option>
                <option value="Monthly plan">Monthly plan</option>
                <option value="Existing order">Question about an existing order</option>
                <option value="Directory listing">Directory listing</option>
              </select>
            </div>
            <div class="form-group">
              <label for="name">Full name <span class="req">*</span></label>
              <input type="text" id="name" name="name" required autocomplete="name" />
            </div>
            <div class="form-group">
              <label for="email">Email <span class="req">*</span></label>
              <input type="email" id="email" name="email" required autocomplete="email" />
            </div>
            <div class="form-group">
              <label for="phone">Phone number</label>
              <input type="tel" id="phone" name="phone" autocomplete="tel" />
            </div>
            <div class="form-group">
              <label for="website">Website URL</label>
              <input type="text" id="website" name="website" placeholder="yourbusiness.com" />
            </div>
            <div class="form-group full">
              <label for="description">Your message <span class="req">*</span></label>
              <textarea id="description" name="description" required></textarea>
            </div>
          </div>
          <div class="form-submit">
            <button type="submit" class="btn btn-primary btn-lg">Send message</button>
            <div class="form-error"></div>
          </div>
        </form>
      <p>Mindful Marketing Agency · Atlanta, Georgia · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>By submitting, you agree to our <a href="/privacy-policy/">Privacy Policy</a>.</p>'''
page('contact', 'Contact Mindful Marketing Agency | Atlanta Digital Marketing',
 'Contact Mindful Marketing Agency, an Atlanta digital marketing agency. Send a message and we reply within two business days.',
 'Contact', 'Contact us', 'Questions about a service, a monthly plan, or an existing order? Send a note and we\'ll reply within two business days.',
 form, '  ' + leads_js if leads_js not in tail else '')

# sitewide: footer links + adsense head script
LEGAL = '<p class="footer-legal"><a href="/contact/">Contact</a> · <a href="/privacy-policy/">Privacy Policy</a> · <a href="/terms/">Terms of Service</a></p>'
n = 0
for f in glob.glob(os.path.join(B, '**/*.html'), recursive=True):
    if '/.git/' in f: continue
    s = open(f, encoding='utf-8').read(); o = s
    if 'pagead2.googlesyndication.com' not in s and '</head>' in s:
        s = s.replace('</head>', '  ' + ADS + '\n</head>', 1)
    if 'footer-legal' not in s and '<div class="footer-bottom">' in s:
        s = s.replace('<div class="footer-bottom">', '<div class="footer-bottom">\n      ' + LEGAL, 1)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); n += 1
print('updated', n)
