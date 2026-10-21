#!/usr/bin/env python3
"""
Georgia Marketing Agencies — /blog/ hub and posts.

Generates a static blog hub at /blog/ and one page per post at
/blog/<slug>/index.html, each with:
  - a generated branded SVG featured image (no external image fetches —
    everything here is self-contained, consistent with the rest of the
    site's blue/white design system)
  - an auto-built table of contents linking to each H2 section
  - BlogPosting + BreadcrumbList (+ FAQPage where present) JSON-LD
  - internal links back into the directory and the owner's own services

Run with:
  python3 generate_blog.py
"""
import json
import os
import re
import textwrap

from generate_directory import HEADER_NAV, FOOTER, esc, slugify

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://mindfulmarketingagency.net"


# ---------------------------------------------------------------- content --

BLOG_POSTS = [
    {
        "slug": "what-is-domain-investing",
        "title": "What Is Domain Investing?",
        "category": "Domains",
        "read_minutes": 7,
        "description": "Domain investing explained: how buying and reselling domain names works, what makes a domain valuable, common strategies, and the real risks involved.",
        "excerpt": "Domain investing — or \"domaining\" — means buying domain names as assets, not just addresses. Here's how it actually works, and what makes one domain worth $50 and another worth $50,000.",
        "intro": """
          <p>If you've ever typed a short, memorable domain into your browser and wondered what it would sell
          for, you've already brushed up against domain investing. It's a real, if niche, market — people
          buy domain names the way others buy real estate or stocks, betting that a name will be worth more
          later than it costs today.</p>
          <p>This isn't the same thing as registering a domain for your own business website. Domain investing
          is specifically about acquiring names <em>as assets</em> — to resell, lease, or develop later — rather
          than to put a website on them immediately.</p>
        """,
        "sections": [
            ("How Domain Investing Works", """
              <p>At its core, domain investing follows a simple pattern: buy a domain for less than you believe
              it's worth, hold it, and sell it later for more. Investors source domains a few different ways:</p>
              <ul>
                <li><strong>Hand-registration</strong> — registering a brand-new domain directly through a
                registrar for the standard annual fee (often $10–$20), betting on future demand.</li>
                <li><strong>Expired or dropped domains</strong> — picking up domains that a previous owner let
                lapse, sometimes still carrying age, backlinks, or existing traffic.</li>
                <li><strong>Aftermarket purchases</strong> — buying already-registered premium domains from
                current owners or marketplaces, usually at a markup reflecting the name's perceived value.</li>
              </ul>
              <p>Once acquired, a domain is typically parked (sometimes with ads to generate small passive
              income), listed for sale on a marketplace, or developed with a basic site to demonstrate its
              potential use case to a buyer.</p>
            """),
            ("What Makes a Domain Valuable", """
              <p>Not all domains are created equal, and the gap between a $12 registration and a five- or
              six-figure sale usually comes down to a handful of factors:</p>
              <ul>
                <li><strong>Length and memorability</strong> — shorter, pronounceable names are easier to
                remember, type, and say out loud, which makes them inherently more useful.</li>
                <li><strong>Extension (TLD)</strong> — .com remains the most trusted and valuable extension in
                most markets, though country-code and newer extensions (.io, .ai, .co) have built real demand
                in specific industries.</li>
                <li><strong>Keyword relevance</strong> — exact-match keyword domains (think a generic industry
                term) can carry built-in search intent and perceived SEO value.</li>
                <li><strong>Brandability</strong> — invented or distinctive names that could plausibly become a
                company name on their own (think the kind of word a startup would pick).</li>
                <li><strong>History</strong> — age, existing backlinks, and prior traffic can add real value,
                but also real risk if that history includes spam or penalties.</li>
              </ul>
            """),
            ("Common Domain Investing Strategies", """
              <p>Most domain investors specialize in one or two approaches rather than trying everything at
              once:</p>
              <ul>
                <li><strong>Geo-targeted domains</strong> — city or region plus industry combinations (useful
                to local service businesses looking for an SEO-friendly name).</li>
                <li><strong>Niche/industry domains</strong> — generic terms within a specific vertical that a
                startup or established company might want to acquire as they scale.</li>
                <li><strong>Brandable one- or two-word names</strong> — invented or dictionary words that sound
                like a company name.</li>
                <li><strong>Expired domain flipping</strong> — acquiring domains right as they drop, based on
                existing metrics like backlink profiles or historical traffic.</li>
              </ul>
            """),
            ("The Risks of Domain Investing", """
              <p>Domain investing is accessible — anyone can register a domain for a few dollars — but it's
              far from risk-free:</p>
              <ul>
                <li><strong>Carrying costs.</strong> Every domain in a portfolio renews annually, and a large
                portfolio of unsold names adds up in renewal fees every year, whether or not anything sells.</li>
                <li><strong>No guaranteed buyer.</strong> A domain is only worth what someone will actually pay
                for it — liquidity is far lower than in stocks or real estate.</li>
                <li><strong>Trademark exposure.</strong> Registering a domain that's confusingly similar to an
                existing trademark can expose an investor to a UDRP dispute or legal action, and in bad-faith
                cases, the domain can simply be taken away.</li>
                <li><strong>Market shifts.</strong> Demand for certain extensions or keyword patterns can change
                as search and branding trends evolve.</li>
              </ul>
            """),
            ("Domain Investing vs. Buying a Domain for Your Business", """
              <p>It's worth drawing a clear line here: if you're a business owner who just needs a domain for
              your website, you're not domain investing — you're buying infrastructure. The calculus is
              completely different. You're not trying to resell it later; you're trying to find a name that
              represents your brand, is easy for customers to find, and that you can actually afford, even if
              your first-choice domain is already registered.</p>
              <p>That's a common enough problem that it deserves its own answer — see
              <a href="/blog/what-if-my-business-domain-is-already-taken/">What If My Business Domain Is Already
              Taken?</a> for a practical walkthrough.</p>
            """),
        ],
        "faqs": [
            ("Is domain investing legal?", "Yes — buying and reselling domain names is a legitimate, legal activity. The exception is registering domains in bad faith to profit from someone else's trademark (cybersquatting), which can result in losing the domain and potential legal liability."),
            ("How much money do you need to start domain investing?", "You can start with the cost of a single domain registration, typically $10–$20 a year. Most investors reinvest early sales into acquiring more names, building a portfolio over time."),
            ("What's the difference between a domain investor and a domain squatter?", "A domain investor typically registers available, generic, or brandable names. A squatter deliberately registers names identical or confusingly similar to existing trademarks or brands, which is both unethical and legally risky."),
        ],
        "cta": {
            "heading": "Need help turning a domain into a real marketing presence?",
            "text": "A good domain is a starting point, not a strategy. If you're ready to build out the SEO, content, and marketing behind it, see what we offer directly.",
            "href": "/digital-marketing/",
            "label": "See our digital marketing services",
        },
    },
    {
        "slug": "what-if-my-business-domain-is-already-taken",
        "title": "What If My Business Domain Is Already Taken?",
        "category": "Domains",
        "read_minutes": 6,
        "description": "Your ideal .com is already registered. Here are five practical options — from alternate extensions to buying it outright — and what to avoid.",
        "excerpt": "You've picked the perfect business name and the .com is gone. Before you panic-rebrand, here are five real options, in order of how much they'll cost you.",
        "intro": """
          <p>You've settled on a business name, you're ready to build a website, and then it happens — the
          domain is already registered. It's one of the most common snags in starting or rebranding a business,
          and it's rarely the dead end it feels like at first.</p>
          <p>Here's how to work through it methodically, starting with the cheapest options first.</p>
        """,
        "sections": [
            ("First, Check What's Actually There", """
              <p>Before changing plans, find out what you're dealing with. Visit the domain directly:</p>
              <ul>
                <li><strong>It's an active, unrelated business.</strong> You'll likely need a different name or
                extension — see the options below.</li>
                <li><strong>It's a parked page or "domain for sale" notice.</strong> The owner may be a domain
                investor willing to sell — see "Buy the domain" below.</li>
                <li><strong>It shows nothing at all.</strong> It may still be registered but unused. A WHOIS
                lookup (through your registrar or a site like whois.com) can confirm registration status and,
                sometimes, ownership contact details.</li>
              </ul>
            """),
            ("Option 1: Try a Different Extension", """
              <p>.com is still the most recognized and trusted extension for most businesses, but it's no
              longer the only credible option. Depending on your industry, consider:</p>
              <ul>
                <li><strong>.co</strong> — a popular, clean-looking .com alternative</li>
                <li><strong>.net or .biz</strong> — widely recognized, if slightly dated-feeling</li>
                <li><strong>Industry-specific extensions</strong> — .agency, .law, .shop, .tech, and similar
                options can actually reinforce what you do</li>
                <li><strong>.us</strong> — a reasonable option for a business specifically serving U.S.
                customers</li>
              </ul>
              <p>Search ranking is not meaningfully affected by which extension you choose — Google ranks
              content and authority, not TLD. The main trade-off is customer trust and the risk that people
              will type ".com" out of habit and land on a competitor's site instead.</p>
            """),
            ("Option 2: Add a Word or Modifier", """
              <p>Small additions can make an otherwise-taken name available again without changing your actual
              business name:</p>
              <ul>
                <li>A location: <code>yourbrandatlanta.com</code></li>
                <li>A descriptor: <code>yourbrandmarketing.com</code>, <code>yourbrandhq.com</code></li>
                <li>An action word: <code>getyourbrand.com</code>, <code>tryyourbrand.com</code>, <code>shopyourbrand.com</code></li>
              </ul>
              <p>This keeps your actual brand name unchanged on signage, social handles, and verbal
              introductions — only the domain gets a small addition.</p>
            """),
            ("Option 3: Buy the Domain From Its Current Owner", """
              <p>If the domain is dormant, parked, or clearly held by a domain investor rather than a competing
              business, you can often buy it outright. Steps:</p>
              <ul>
                <li>Look up the registrant through a WHOIS lookup, or check if the registrar offers a "make an
                offer" or "buy now" option directly on the parked page.</li>
                <li>Reach out professionally and make a reasonable offer — premium or aftermarket domains can
                range from a few hundred to tens of thousands of dollars depending on demand.</li>
                <li>Use an escrow service (such as Escrow.com) for the transaction rather than wiring money
                directly — this protects both buyer and seller until the domain transfer is confirmed.</li>
              </ul>
              <p>Be prepared to walk away if the asking price doesn't make sense for your budget — there's
              almost always a workable alternative.</p>
            """),
            ("Option 4: Adjust the Name Itself", """
              <p>Sometimes the cleanest fix is a small tweak to the business name itself — a synonym, a
              different spelling, or dropping a generic word — that happens to free up a clean, close-match
              domain. This is worth considering early, before the name is on signage, packaging, or legal
              paperwork, since changing it later gets expensive fast.</p>
            """),
            ("Option 5: Use a Domain Marketplace or Broker", """
              <p>If the name is listed for sale, marketplaces like Afternic, Sedo, and GoDaddy's aftermarket
              let you make an offer or buy at a listed price, often with built-in escrow and transfer handling.
              A domain broker can also negotiate on your behalf for premium or high-value names, usually for a
              commission on the sale.</p>
            """),
            ("What Not to Do", """
              <ul>
                <li><strong>Don't register a near-identical domain to an existing trademarked brand</strong> —
                this can trigger a legal dispute and you could lose the domain (and more) regardless of intent.</li>
                <li><strong>Don't ignore the problem and launch on a confusing workaround</strong> (like a free
                subdomain) if you're a serious business — it undercuts trust from day one.</li>
                <li><strong>Don't overpay out of urgency.</strong> A few days of research almost always turns up
                a workable, affordable option.</li>
              </ul>
            """),
        ],
        "faqs": [
            ("Does the domain extension affect SEO rankings?", "Not directly. Google ranks based on content quality, relevance, and authority — not the TLD. The bigger consideration is user trust and whether people will remember and correctly type your domain."),
            ("Is it safe to buy a domain directly from a stranger?", "Use an escrow service rather than sending payment directly. Reputable escrow providers hold the funds until the domain transfer is verified, protecting both sides of the transaction."),
            ("Should I just use a free subdomain instead?", "For a serious, ongoing business, a proper domain is worth the investment — it's more memorable, more trustworthy to customers, and won't need to change later as you grow."),
        ],
        "cta": {
            "heading": "Already have your domain sorted? Let's build what goes on it.",
            "text": "Once your domain is settled, the real work is getting found. Browse the directory to compare Georgia marketing agencies, or see our own done-for-you services.",
            "href": "/services/",
            "label": "Browse the directory",
        },
    },
    {
        "slug": "how-to-choose-a-marketing-agency-in-georgia",
        "title": "How to Choose a Marketing Agency in Georgia: A Complete Guide",
        "category": "Strategy",
        "read_minutes": 9,
        "description": "A step-by-step guide to picking the right marketing agency in Georgia — defining goals, comparing services, red flags to avoid, and questions to ask before signing.",
        "excerpt": "Georgia has hundreds of marketing agencies. Here's how to narrow that down to the handful that are actually right for your business, your budget, and your goals.",
        "intro": """
          <p>With hundreds of marketing agencies operating across Georgia — from one-person SEO consultants to
          full-service shops in Atlanta — picking the right one can feel overwhelming. The good news: the
          process gets much simpler once you know what to look for, in what order.</p>
        """,
        "sections": [
            ("Start With Your Goal, Not the Agency List", """
              <p>Before comparing a single agency, get specific about what success looks like. "More marketing"
              isn't a goal — "20 qualified leads a month" or "rank on page one for our top 5 local search terms"
              is. A clear goal does two things: it tells you which <em>type</em> of agency you actually need, and
              it gives you a benchmark to hold them to later.</p>
            """),
            ("Figure Out Which Service You Actually Need", """
              <p>Most agencies specialize, even if they offer a broader menu. Common categories:</p>
              <ul>
                <li><strong>SEO agencies</strong> — for long-term organic search visibility</li>
                <li><strong>PPC & paid media agencies</strong> — for fast, budget-controlled traffic via ads</li>
                <li><strong>Social media marketing agencies</strong> — for content, scheduling, and community</li>
                <li><strong>Web design agencies</strong> — for a new or rebuilt website</li>
                <li><strong>Branding & graphic design agencies</strong> — for identity, logo, and visual systems</li>
                <li><strong>Full-service digital marketing agencies</strong> — for a combination of the above
                under one roof</li>
              </ul>
              <p>You can browse all of these by <a href="/services/">service</a> or by
              <a href="/cities/">city</a> to see who's actually active near you.</p>
            """),
            ("Local vs. National Agency", """
              <p>A Georgia-based agency isn't automatically better than a national one, but there are real
              trade-offs. Local agencies tend to understand regional search behavior, local competitors, and
              can often meet in person. National agencies may bring more specialized tooling or industry-specific
              experience. For local-service businesses (think contractors, restaurants, clinics), local
              expertise usually wins; for ecommerce or SaaS, it matters less.</p>
            """),
            ("Green Flags to Look For", """
              <ul>
                <li>Specific, verifiable client results — not just vague "we grew their traffic" claims</li>
                <li>Transparent reporting and a clear explanation of what you'll actually receive each month</li>
                <li>A contract with a reasonable minimum term and clear exit terms, not an indefinite lock-in</li>
                <li>Real reviews with real review counts, not just a handful of 5-stars with no detail</li>
                <li>Willingness to explain their process in plain language, not just jargon</li>
              </ul>
            """),
            ("Red Flags to Avoid", """
              <ul>
                <li>Guarantees of a #1 Google ranking — no agency controls Google's algorithm</li>
                <li>Pressure to sign immediately or "lock in" a discount same-day</li>
                <li>No clear reporting cadence, or reports that only show vanity metrics</li>
                <li>Opaque pricing that's hard to pin down until after you've committed</li>
                <li>No case studies, portfolio, or client examples at all</li>
              </ul>
            """),
            ("Questions to Ask Before You Sign", """
              <ul>
                <li>What does a typical first 30/60/90 days look like with you?</li>
                <li>Who will actually be working on our account day-to-day?</li>
                <li>How do you measure and report success, and how often?</li>
                <li>What's included in the monthly cost, and what's billed separately?</li>
                <li>What happens if we want to cancel or change scope?</li>
              </ul>
            """),
            ("How to Use This Directory", """
              <p>Use the search bar on the <a href="/">homepage</a> or the <a href="/cities/">city</a> and
              <a href="/services/">service</a> pages to filter down to agencies matching your location and
              service need, then compare ratings, reviews, and contact details side by side before reaching
              out. Every listing links straight to the agency's profile — no lead forms or gatekeeping in the
              way.</p>
            """),
        ],
        "faqs": [
            ("How much should I expect to pay a marketing agency?", "It varies widely by service and scope — see our guide on how much digital marketing costs for typical ranges by service type."),
            ("Should I hire one full-service agency or several specialists?", "A full-service agency is simpler to manage if your needs span several channels. Specialists can be more cost-effective and deeply skilled in one area, but require more coordination on your end."),
            ("How long before I see results from an agency?", "PPC can show results within days to weeks. SEO typically takes 3–6 months to show meaningful movement, and longer in competitive markets."),
        ],
        "cta": {
            "heading": "Ready to compare agencies?",
            "text": "Browse the full Georgia Marketing Agencies directory by city or service, or work with us directly if you'd rather skip the search.",
            "href": "/cities/",
            "label": "Browse agencies by city",
        },
    },
    {
        "slug": "seo-vs-ppc-which-is-right-for-your-business",
        "title": "SEO vs. PPC: Which Is Right for Your Business?",
        "category": "SEO & PPC",
        "read_minutes": 7,
        "description": "SEO and PPC solve different problems. Here's how they compare on cost, timeline, and control — and how to decide which one your business needs first.",
        "excerpt": "SEO builds compounding, long-term visibility. PPC buys immediate traffic. Most businesses eventually need both — but which one should come first?",
        "intro": """
          <p>SEO and PPC both get you found on Google, but they work in almost opposite ways. Understanding the
          difference — not just in theory, but in cost, timeline, and effort — makes it much easier to decide
          where to put your first marketing dollar.</p>
        """,
        "sections": [
            ("What SEO Actually Is", """
              <p>Search engine optimization (SEO) is the practice of improving your website so it ranks higher
              in Google's organic (unpaid) search results. It covers technical site health, on-page content,
              local signals like your Google Business Profile, and earning links and citations from other
              sites. The traffic it earns is "free" in the sense that you don't pay per click — but it takes
              real time and consistent work to build.</p>
            """),
            ("What PPC Actually Is", """
              <p>Pay-per-click (PPC) advertising — Google Ads, Meta Ads, and similar platforms — puts your
              business directly in front of people searching or browsing, and you pay each time someone clicks.
              Results are close to immediate: launch a campaign today, get traffic today. The trade-off is that
              traffic stops the moment you stop paying.</p>
            """),
            ("Cost Comparison", """
              <p>SEO's cost is mostly labor and time — content, technical fixes, and ongoing optimization —
              typically billed as a monthly retainer. PPC's cost is a combination of agency management fees
              plus actual ad spend paid directly to the platform, which scales with how much traffic you want.
              SEO tends to get cheaper per lead over time as rankings build; PPC costs stay roughly proportional
              to the traffic you're buying.</p>
            """),
            ("Timeline Comparison", """
              <ul>
                <li><strong>PPC:</strong> traffic within hours of launching a campaign</li>
                <li><strong>SEO:</strong> meaningful ranking movement typically takes 3–6 months, longer in
                competitive industries or markets</li>
              </ul>
            """),
            ("When to Choose PPC First", """
              <ul>
                <li>You need leads or sales now — a new location opening, a seasonal push, a launch</li>
                <li>You want to test messaging or offers quickly before investing in long-term content</li>
                <li>Your industry is too competitive to realistically rank organically in the short term</li>
              </ul>
            """),
            ("When to Choose SEO First", """
              <ul>
                <li>You're building for the long term and want compounding, lower-cost-per-lead traffic</li>
                <li>Your budget can't sustain ongoing ad spend indefinitely</li>
                <li>Your industry has strong, consistent search demand that doesn't require urgency</li>
              </ul>
            """),
            ("Why Most Businesses End Up Doing Both", """
              <p>PPC can fund growth while SEO is still building momentum in the background, and SEO reduces
              long-term reliance on paid traffic once it kicks in. Many businesses run PPC early for immediate
              volume, then shift budget toward SEO as organic rankings mature and the cost-per-lead from search
              starts to drop.</p>
            """),
        ],
        "faqs": [
            ("Can I just do SEO and skip PPC entirely?", "Yes, plenty of businesses do — it just means accepting a slower ramp-up period before organic traffic becomes meaningful."),
            ("Does running PPC help my SEO rankings?", "Not directly — Google doesn't use ad spend as a ranking factor for organic results. Indirectly, PPC can surface which keywords and pages convert, which can inform your SEO content strategy."),
            ("Which is better for a brand-new business with no website history?", "PPC usually makes more sense early on, since a new site has no ranking history or authority yet — SEO can be built in parallel."),
        ],
        "cta": {
            "heading": "Not sure which one fits your business?",
            "text": "See our own done-for-you SEO service, or browse PPC & paid media agencies in the directory to compare options.",
            "href": "/seo/",
            "label": "See our SEO service",
        },
    },
    {
        "slug": "how-much-does-digital-marketing-cost",
        "title": "How Much Does Digital Marketing Cost in 2026?",
        "category": "Budgeting",
        "read_minutes": 8,
        "description": "Typical digital marketing costs by service type — SEO, PPC, social media, and full-service — plus the factors that actually move your price up or down.",
        "excerpt": "Digital marketing pricing varies a lot by service, scope, and provider. Here's what to actually expect to pay in 2026, broken down by channel.",
        "intro": """
          <p>"How much does digital marketing cost?" doesn't have one answer — it depends heavily on which
          service, how competitive your industry and market are, and who you hire. Here's a realistic
          breakdown by channel, plus the factors that move the price in either direction.</p>
        """,
        "sections": [
            ("Common Pricing Models", """
              <ul>
                <li><strong>Monthly retainer</strong> — a fixed monthly fee for ongoing work, most common for
                SEO and social media management</li>
                <li><strong>Hourly</strong> — billed per hour worked, more common for consulting or smaller
                projects</li>
                <li><strong>Project-based</strong> — a flat fee for a defined deliverable, like a website build</li>
                <li><strong>Performance/commission-based</strong> — tied to results such as ad spend managed or
                leads generated, most common for PPC management</li>
              </ul>
            """),
            ("Typical Cost Ranges by Service", """
              <ul>
                <li><strong>SEO:</strong> small businesses typically see retainers from a few hundred dollars a
                month for a narrow, local-focused scope, up to several thousand a month for competitive,
                multi-location, or ecommerce SEO.</li>
                <li><strong>PPC management:</strong> agency fees are often a flat rate or a percentage of ad
                spend (commonly in the 10–20% range), on top of the actual spend paid to Google or Meta.</li>
                <li><strong>Social media management:</strong> ranges from a few hundred dollars a month for
                basic posting and light engagement, up to several thousand for full content production, paid
                social, and community management.</li>
                <li><strong>Web design:</strong> typically a one-time project fee, from under a thousand for a
                simple site to five figures for a custom, complex build.</li>
                <li><strong>Full-service digital marketing:</strong> bundles multiple channels under one
                retainer, generally priced higher than any single service alone but often more cost-effective
                than hiring separately for each.</li>
              </ul>
              <p>As a concrete example, our own <a href="/seo/">SEO service</a> is tiered starting at $49.99/mo,
              scaling up with the number of pages and scope covered — a useful reference point for what a
              narrowly-scoped SEO engagement can actually cost.</p>
            """),
            ("What Actually Moves the Price", """
              <ul>
                <li><strong>Competition in your market</strong> — ranking for "coffee shop near me" in a small
                town costs far less effort than in downtown Atlanta.</li>
                <li><strong>Scope</strong> — number of locations, pages, platforms, or campaigns covered.</li>
                <li><strong>Current state of your assets</strong> — a site with major technical issues costs more
                to fix before growth work can even begin.</li>
                <li><strong>Speed you want results</strong> — accelerated timelines generally cost more.</li>
              </ul>
            """),
            ("In-House vs. Agency vs. Freelancer", """
              <p>An in-house marketer gives you full control and availability, but comes with a full salary,
              benefits, and the challenge of covering every specialty (SEO, PPC, design, content) with one
              person. A freelancer is often cheaper hourly, but availability and depth across multiple channels
              can vary. An agency sits in between — access to a full team and established processes, generally
              for less than a full in-house team, with less day-to-day control than hiring directly.</p>
            """),
            ("How to Build a Realistic Budget", """
              <p>A common starting benchmark is 5–10% of revenue for established businesses, with growth-stage
              or newer businesses sometimes allocating more to build initial visibility. From there, prioritize
              the one or two channels most likely to move your specific goal, rather than spreading a small
              budget thin across everything at once.</p>
            """),
        ],
        "faqs": [
            ("Is cheaper always worse in digital marketing?", "Not necessarily, but very low prices often mean a narrower scope, less experienced staff, or heavy reliance on automation. Compare what's actually included, not just the sticker price."),
            ("Do I need to sign a long-term contract?", "Many agencies offer month-to-month after an initial minimum term (commonly 3–6 months) since results like SEO take time to materialize. Be wary of indefinite lock-ins with no exit terms."),
            ("What's a reasonable minimum budget to start with?", "It depends on the channel and market, but a few hundred dollars a month is a realistic entry point for a narrowly-scoped local SEO or social media engagement."),
        ],
        "cta": {
            "heading": "Want a real number for your business?",
            "text": "See our transparent SEO pricing tiers, or browse the directory to compare quotes from multiple Georgia agencies.",
            "href": "/seo/",
            "label": "See SEO pricing",
        },
    },
    {
        "slug": "signs-its-time-to-hire-a-marketing-agency",
        "title": "10 Signs It's Time to Hire a Marketing Agency",
        "category": "Strategy",
        "read_minutes": 6,
        "description": "Ten clear signals that DIY marketing has hit its limit and it's time to bring in a marketing agency — from stagnant growth to no time to execute.",
        "excerpt": "DIY marketing works great — until it doesn't. Here are 10 signals that it's time to hand some of it off to a professional agency.",
        "intro": """
          <p>Plenty of businesses start out handling their own marketing, and that's often the right call early
          on. But there's usually a point where doing it all in-house starts costing more — in missed growth,
          wasted time, or both — than hiring help would. Here are ten signs you've reached that point.</p>
        """,
        "sections": [
            ("1. You Don't Have Time to Execute Consistently", """
              <p>Marketing only works with consistency — a blog post here and there, or sporadic social posts,
              rarely move the needle. If marketing keeps getting pushed to "whenever there's time," it's
              effectively not happening.</p>
            """),
            ("2. Growth Has Plateaued", """
              <p>If revenue or lead volume has been flat for several months despite effort, it's often a sign
              that your current approach has hit its ceiling and needs either new strategy or new execution
              capacity.</p>
            """),
            ("3. You're Not Tracking Results", """
              <p>If you can't say with confidence where your last 10 customers came from, you're flying blind —
              and can't tell what's actually working.</p>
            """),
            ("4. Competitors Are Outranking You", """
              <p>If competitors consistently show up above you in local search or ads, they're capturing
              demand that could be yours — often because they've invested in SEO or PPC and you haven't yet.</p>
            """),
            ("5. Your Website Hasn't Been Updated in Years", """
              <p>An outdated site — slow, not mobile-friendly, visually dated — actively undermines trust with
              potential customers before they even reach your pitch.</p>
            """),
            ("6. Your Social Presence Is Inconsistent", """
              <p>Sporadic posting, long gaps, or no clear content strategy makes a business look inactive, even
              if it's thriving operationally.</p>
            """),
            ("7. You Have No SEO Strategy at All", """
              <p>If you've never done keyword research, optimized a page, or claimed your Google Business
              Profile, there's likely significant free traffic sitting on the table.</p>
            """),
            ("8. You're Scaling and Marketing Can't Keep Up", """
              <p>Opening new locations, launching new products, or entering new markets all require marketing
              capacity that a single in-house generalist often can't stretch to cover alone.</p>
            """),
            ("9. You've Tried DIY Tools and Hit a Wall", """
              <p>Website builders and social schedulers get you started, but they don't replace strategy —
              knowing <em>what</em> to post, build, or target in the first place.</p>
            """),
            ("10. You Know What to Do, But Not How to Do It Well", """
              <p>Sometimes the gap isn't knowledge, it's execution — knowing you need better SEO content but not
              having the skill or time to produce it consistently and well.</p>
            """),
        ],
        "faqs": [
            ("Can I hire an agency for just one thing, like SEO, instead of everything?", "Yes — most agencies specialize or offer standalone services, so you can hire narrowly for the one area where you need the most help."),
            ("Will hiring an agency mean giving up control of my marketing?", "A good agency works as an extension of your team, not a replacement for your input — you should still have visibility and a say in strategy and messaging."),
        ],
        "cta": {
            "heading": "Recognize a few of these?",
            "text": "Browse the directory to compare Georgia agencies, or talk to us directly about our own SEO, digital marketing, and social media services.",
            "href": "/services/",
            "label": "Browse the directory",
        },
    },
    {
        "slug": "local-seo-checklist-for-georgia-small-businesses",
        "title": "Local SEO Checklist for Georgia Small Businesses",
        "category": "SEO & PPC",
        "read_minutes": 8,
        "description": "A practical local SEO checklist for Georgia small businesses — Google Business Profile, citations, reviews, local content, and more.",
        "excerpt": "Local SEO is one of the highest-ROI channels for a Georgia small business. Here's the full checklist, in priority order.",
        "intro": """
          <p>For most local businesses — contractors, clinics, restaurants, service providers — local SEO is
          where the bulk of discoverable demand actually lives. Here's a practical, prioritized checklist to
          work through.</p>
        """,
        "sections": [
            ("1. Claim and Fully Optimize Your Google Business Profile", """
              <ul>
                <li>Claim and verify your listing if you haven't already</li>
                <li>Fill out every field — category, service area, hours, phone, website, description</li>
                <li>Add real photos of your location, team, and work</li>
                <li>Keep hours accurate, especially around holidays</li>
              </ul>
            """),
            ("2. Keep NAP Consistent Everywhere", """
              <p>Your Name, Address, and Phone number (NAP) should match exactly across your website, Google
              Business Profile, and every directory or citation. Inconsistencies — even small formatting
              differences — can quietly undermine local ranking signals.</p>
            """),
            ("3. Target Local Keywords, Not Just Generic Ones", """
              <p>Rather than optimizing only for "marketing agency," target the combinations people actually
              search: "[service] in [city]," "[service] near me," and neighborhood- or region-specific phrases
              relevant to how your customers search.</p>
            """),
            ("4. Build Citations in Relevant Directories", """
              <p>Being listed consistently across relevant directories — industry-specific and general local
              directories alike — reinforces your business's legitimacy and location to search engines. (If
              you run a marketing agency in Georgia, for example, <a href="/submit/">getting listed here</a> is
              a free citation and referral source in one.)</p>
            """),
            ("5. Actively Manage Reviews", """
              <ul>
                <li>Ask satisfied customers directly for a Google review</li>
                <li>Respond to every review, positive or negative, professionally</li>
                <li>Never buy or fake reviews — it violates platform policy and erodes trust fast if discovered</li>
              </ul>
            """),
            ("6. Build Location-Specific Landing Pages", """
              <p>If you serve multiple cities or neighborhoods, dedicated pages for each (rather than one
              generic "service area" page) let you target local search intent directly and give Google clearer
              signals about where you operate.</p>
            """),
            ("7. Earn Local Links", """
              <p>Links from local news sites, community organizations, chambers of commerce, and relevant local
              partners carry real local-relevance weight that generic link-building doesn't.</p>
            """),
            ("8. Don't Neglect Mobile Speed and Usability", """
              <p>The majority of local searches happen on mobile, often with immediate intent (calling, getting
              directions). A slow or clunky mobile site actively loses customers at the exact moment they're
              ready to act.</p>
            """),
        ],
        "faqs": [
            ("How long does local SEO take to show results?", "Often faster than broader national SEO — meaningful movement in local pack rankings can appear within weeks to a few months, depending on competition."),
            ("Do online directories actually help local SEO?", "Yes, when they're relevant and reputable — consistent citations across trustworthy directories reinforce your business's legitimacy and location to search engines."),
            ("Is a Google Business Profile free?", "Yes, it's free to claim and maintain — it's one of the highest-ROI steps available to any local business."),
        ],
        "cta": {
            "heading": "Want this handled for you?",
            "text": "See our done-for-you SEO service, including Google Search Console and Google Analytics setup from the first tier.",
            "href": "/seo/",
            "label": "See our SEO service",
        },
    },
    {
        "slug": "social-media-marketing-trends-2026",
        "title": "Social Media Marketing Trends to Watch in 2026",
        "category": "Social Media",
        "read_minutes": 6,
        "description": "The social media marketing trends actually shaping 2026 — short-form video, social search, AI-assisted content, and the shift toward authenticity.",
        "excerpt": "Social media keeps moving fast. Here's what's actually shaping strategy in 2026 — and what's worth your attention versus what's just noise.",
        "intro": """
          <p>Social platforms change constantly, but a few real shifts are shaping how businesses need to show
          up in 2026. Here's what's worth paying attention to.</p>
        """,
        "sections": [
            ("Short-Form Video Is Still the Default, Not the Trend", """
              <p>Short-form video has moved from "emerging trend" to baseline expectation across nearly every
              platform. Businesses without a short-form video presence are increasingly invisible to algorithms
              that heavily favor the format.</p>
            """),
            ("Social Platforms as Search Engines", """
              <p>A growing share of users, especially younger audiences, start product and local business
              searches directly on social platforms instead of Google. This means social content increasingly
              needs to be written and tagged with the same search intent in mind as a webpage.</p>
            """),
            ("AI-Assisted Content Creation", """
              <p>AI tools are increasingly used to draft captions, generate ideas, and speed up editing — but
              the brands winning attention are still the ones pairing that speed with a genuine, specific voice,
              not generic AI-sounding copy.</p>
            """),
            ("Community Over Raw Follower Count", """
              <p>Engaged, responsive communities are increasingly valued over large but passive follower counts
              — both by audiences themselves and by platform algorithms, which reward meaningful engagement
              over reach alone.</p>
            """),
            ("Social Commerce Keeps Expanding", """
              <p>In-app shopping and checkout features continue to mature, shortening the path from discovery to
              purchase and making social content a more direct revenue channel, not just a top-of-funnel
              awareness play.</p>
            """),
            ("Authenticity and UGC Outperform Polish", """
              <p>Lower-production, authentic content — including real user-generated content — continues to
              outperform overly polished, ad-like content in both engagement and trust, particularly with
              younger audiences.</p>
            """),
            ("Platform Diversification Is a Hedge, Not a Nice-to-Have", """
              <p>Relying entirely on one platform carries real risk if its algorithm, policies, or popularity
              shift. Maintaining even a modest presence across two or three relevant platforms protects against
              that single point of failure.</p>
            """),
        ],
        "faqs": [
            ("Do small businesses actually need to be on every platform?", "No — it's usually better to do two or three platforms well, matched to where your actual customers spend time, than to spread thin across all of them."),
            ("Is organic social media still worth it without paid promotion?", "Yes, especially for community-building and trust, though pairing it with modest paid promotion typically extends reach faster."),
        ],
        "cta": {
            "heading": "Want a real content and posting strategy?",
            "text": "See our done-for-you social media marketing service — content, scheduling, and community management, handled for you.",
            "href": "/social-media-marketing/",
            "label": "See our social media service",
        },
    },
    {
        "slug": "how-to-build-a-marketing-budget-for-a-small-business",
        "title": "How to Build a Marketing Budget for a Small Business",
        "category": "Budgeting",
        "read_minutes": 7,
        "description": "A practical framework for building a small business marketing budget — benchmarks, channel allocation, tracking ROI, and common mistakes to avoid.",
        "excerpt": "Most small businesses either overspend on the wrong channels or underspend entirely. Here's a practical framework for getting your marketing budget right.",
        "intro": """
          <p>Building a marketing budget from scratch is harder than it sounds — too little and nothing moves,
          too much in the wrong place and you've wasted money you can't easily get back. Here's a practical
          framework to work from.</p>
        """,
        "sections": [
            ("Start With a Revenue Benchmark", """
              <p>A widely used starting point is allocating roughly 5–10% of revenue to marketing for an
              established business, with newer or growth-focused businesses sometimes allocating more to build
              initial visibility faster. Treat this as a starting range to adjust, not a fixed rule.</p>
            """),
            ("Separate Fixed Costs From Variable Spend", """
              <ul>
                <li><strong>Fixed costs</strong> — retainers, software/tool subscriptions, website hosting</li>
                <li><strong>Variable spend</strong> — ad spend, which can flex up or down month to month based
                on performance and cash flow</li>
              </ul>
              <p>Separating the two makes it much easier to see what you can scale back in a lean month without
              losing core capability.</p>
            """),
            ("Allocate Across Channels Based on Goals, Not Trends", """
              <p>Rather than copying what's trendy, allocate based on your specific goal: SEO and content for
              long-term, compounding visibility; PPC for immediate, controllable volume; social media for brand
              and community; email for retention and repeat business. Most small businesses do best
              concentrating budget in one or two channels well rather than spreading thin across all of them.</p>
            """),
            ("Track Cost Per Lead and Cost Per Customer", """
              <p>A budget without tracking is just a guess. At minimum, track how many leads and customers each
              channel actually generates relative to what you spent on it — this is what lets you shift budget
              toward what's working and away from what isn't.</p>
            """),
            ("Revisit the Budget Quarterly", """
              <p>Marketing performance shifts with seasonality, competition, and your own growth stage. A
              quarterly check-in — not just an annual one — keeps the budget responsive instead of locked to
              assumptions made a year ago.</p>
            """),
            ("Common Budgeting Mistakes", """
              <ul>
                <li>Spreading a small budget across too many channels, so none of them get enough to work</li>
                <li>Cutting marketing entirely during a slow month, which often deepens the slowdown</li>
                <li>No tracking, so spend can't be tied to actual results</li>
                <li>Chasing trends instead of the channel that fits the actual business and audience</li>
              </ul>
            """),
        ],
        "faqs": [
            ("What percentage of revenue should a new business spend on marketing?", "Newer businesses often need to spend above the typical 5–10% benchmark early on to build initial visibility, then can taper toward the standard range as the business matures."),
            ("Should I include staff time in my marketing budget?", "Yes — the time spent by you or your team on marketing has a real cost, even if it isn't a direct cash expense, and should factor into whether outsourcing makes financial sense."),
        ],
        "cta": {
            "heading": "Want help allocating your budget effectively?",
            "text": "Compare agencies and services across the directory, or see our own transparent SEO pricing as a starting benchmark.",
            "href": "/seo/",
            "label": "See our pricing",
        },
    },
    {
        "slug": "diy-marketing-vs-hiring-an-agency",
        "title": "DIY Marketing vs. Hiring an Agency: Pros and Cons",
        "category": "Strategy",
        "read_minutes": 7,
        "description": "A balanced look at DIY marketing versus hiring an agency — real pros and cons of each, plus how to know when a hybrid approach makes sense.",
        "excerpt": "Neither DIY marketing nor hiring an agency is universally right. Here's an honest look at the real trade-offs of each — and when a hybrid approach works best.",
        "intro": """
          <p>There's no universally correct answer to "DIY or agency" — it depends on your time, budget, skill,
          and growth stage. Here's an honest breakdown of both sides.</p>
        """,
        "sections": [
            ("The Case for DIY Marketing", """
              <ul>
                <li><strong>Full control</strong> — every decision, every piece of content, stays in your hands</li>
                <li><strong>Lower direct cost</strong> — no agency fees, just your own time and any tools you use</li>
                <li><strong>Deep product knowledge</strong> — nobody knows your business better than you do</li>
                <li><strong>Flexibility</strong> — you can shift direction instantly without a client conversation</li>
              </ul>
            """),
            ("The Downsides of DIY Marketing", """
              <ul>
                <li><strong>Time cost</strong> — marketing done well takes real, consistent hours that could
                otherwise go into running the business</li>
                <li><strong>Skill gaps</strong> — SEO, paid ads, and design all have real learning curves, and
                mistakes in paid ads specifically can waste money quickly</li>
                <li><strong>Inconsistency</strong> — DIY marketing often slips first when the business gets busy,
                which undercuts the consistency marketing actually needs to work</li>
                <li><strong>No outside perspective</strong> — it's easy to miss blind spots in your own messaging</li>
              </ul>
            """),
            ("The Case for Hiring an Agency", """
              <ul>
                <li><strong>Specialized expertise</strong> — across SEO, paid media, design, and content,
                typically with more depth than one in-house generalist can cover</li>
                <li><strong>Established processes and tools</strong> — agencies bring tested workflows and paid
                tools you'd otherwise have to build or buy yourself</li>
                <li><strong>Frees up your time</strong> — to focus on running and growing the business itself</li>
                <li><strong>Outside perspective</strong> — an agency sees patterns across many clients and
                industries that you can't see from inside your own business</li>
              </ul>
            """),
            ("The Downsides of Hiring an Agency", """
              <ul>
                <li><strong>Direct cost</strong> — a real monthly or project expense</li>
                <li><strong>Less day-to-day control</strong> — decisions move through a relationship, not
                instantly in your own hands</li>
                <li><strong>Onboarding time</strong> — any outside team needs time to learn your business before
                hitting full stride</li>
                <li><strong>Variable quality</strong> — agency quality varies significantly, making the
                selection process genuinely important (see our
                <a href="/blog/how-to-choose-a-marketing-agency-in-georgia/">guide to choosing an agency</a>)</li>
              </ul>
            """),
            ("The Hybrid Approach", """
              <p>Many businesses land somewhere in between — handling some channels in-house (like day-to-day
              social posting or email) while outsourcing the more specialized, time-intensive work like SEO or
              paid media management. This keeps cost down while still getting expert execution where it matters
              most.</p>
            """),
            ("How to Decide", """
              <ul>
                <li>If you have more time than budget, and the stakes of a mistake are low, DIY can make sense</li>
                <li>If you have more budget than time, or the channel has a steep learning curve (like paid
                ads), an agency usually pays for itself faster</li>
                <li>If you're unsure, start with one channel handled by an agency and keep the rest in-house,
                then adjust based on results</li>
              </ul>
            """),
        ],
        "faqs": [
            ("Can I start DIY and switch to an agency later?", "Yes — this is a common and reasonable path. Many businesses start DIY to learn the basics, then outsource once growth outpaces what they can handle internally."),
            ("Is it cheaper to do everything myself?", "Cheaper in direct cost, not necessarily in total cost once your time and any costly mistakes (especially in paid ads) are factored in."),
        ],
        "cta": {
            "heading": "Thinking about outsourcing part of your marketing?",
            "text": "Browse the directory to compare agencies, or see our own SEO, digital marketing, and social media services.",
            "href": "/services/",
            "label": "Browse the directory",
        },
    },
    {
        "slug": "what-are-local-seo-citations",
        "title": "What Are Local SEO Citations and Why Do They Matter?",
        "category": "SEO & PPC",
        "read_minutes": 8,
        "description": "Local SEO citations explained — what they are, structured vs. unstructured citations, data aggregators, NAP consistency, and why they influence local rankings.",
        "excerpt": "Citations are one of the quieter local SEO ranking signals — but also one of the easiest to get wrong. Here's what they actually are and why they matter.",
        "intro": """
          <p>If you've researched local SEO at all, you've likely run into the term "citation" without a clear
          explanation of what it actually means. Citations are one of the foundational — if less glamorous —
          building blocks of local search visibility, and getting them right (or wrong) has a real effect on
          whether your business shows up when nearby customers search.</p>
        """,
        "sections": [
            ("What a Citation Actually Is", """
              <p>A local SEO citation is any online mention of your business's Name, Address, and Phone number
              (commonly shortened to <strong>NAP</strong>) — typically on a directory, app, or platform other
              than your own website. Think Yelp, the Better Business Bureau, industry-specific directories,
              data platforms that feed GPS apps, and hundreds of smaller local and niche directories.</p>
              <p>Each citation is a small, independent confirmation that your business exists, is active, and
              is located where you say it is.</p>
            """),
            ("Structured vs. Unstructured Citations", """
              <ul>
                <li><strong>Structured citations</strong> — your business info listed in a defined format on a
                directory, like a Yelp or Yellow Pages profile with dedicated fields for name, address, phone,
                category, and hours.</li>
                <li><strong>Unstructured citations</strong> — mentions of your business in free-form text, like
                a local news article or blog post that references your name, address, or phone number without a
                dedicated listing format.</li>
              </ul>
              <p>Most citation-building work focuses on structured citations, since they're easier to build
              deliberately and verify — but unstructured mentions still carry real value when they happen
              naturally.</p>
            """),
            ("Why Citations Influence Local Rankings", """
              <p>Search engines can't physically verify that a business is real and located where it claims to
              be — so they rely on corroborating signals instead. When the same business name, address, and
              phone number appear consistently across many independent, reputable sources, it reinforces
              confidence that the listing is accurate and trustworthy. Scattered, inconsistent, or sparse
              citations do the opposite — they introduce doubt into exactly the signal local rankings depend
              on most.</p>
            """),
            ("NAP Consistency Is the Whole Game", """
              <p>The single biggest factor in whether citations help or hurt is consistency. "123 Main Street
              Suite 4" and "123 Main St. #4" might look identical to a person, but inconsistent formatting
              across listings can muddy the signal search engines are trying to read. Before building new
              citations, it's worth standardizing exactly how your business name, address, and phone number
              should appear — then using that exact format everywhere, including your own website.</p>
            """),
            ("What Data Aggregators Do", """
              <p>A small number of large data aggregators collect and redistribute business information to a
              much wider network of directories, apps, and GPS systems automatically. Submitting accurate
              information directly to these aggregators — rather than only to individual directories one at a
              time — is one of the most efficient ways to correct or establish your business data across a huge
              number of downstream sources at once.</p>
            """),
            ("How Many Citations Does a Business Actually Need?", """
              <p>There's no single magic number — it depends heavily on competition in your market and
              industry. A handful of accurate, high-authority citations outperforms a large volume of
              low-quality, inconsistent ones. That said, most local businesses benefit from building out beyond
              just the two or three best-known directories, since different platforms carry different weight in
              different niches and regions.</p>
            """),
            ("Common Citation Mistakes", """
              <ul>
                <li><strong>Duplicate listings</strong> — multiple, slightly different listings for the same
                business confuse rather than reinforce the signal, and can actively work against you.</li>
                <li><strong>Inconsistent NAP</strong> — different formatting, an old address, or an outdated
                phone number across listings undercuts the trust citations are supposed to build.</li>
                <li><strong>Low-quality or irrelevant directories</strong> — citations on spammy, low-authority,
                or completely unrelated sites add little value and occasionally raise red flags.</li>
                <li><strong>Keyword-stuffing the business name</strong> — listing your business as "Acme
                Plumbing Best Atlanta Plumber" instead of its real name violates most directories' guidelines
                and can get listings removed or penalized.</li>
              </ul>
            """),
            ("Where Citations Fit Into a Local SEO Strategy", """
              <p>Citations are one piece of a broader local SEO approach — alongside a fully optimized Google
              Business Profile, on-page local content, and reviews. See our
              <a href="/blog/local-seo-checklist-for-georgia-small-businesses/">local SEO checklist</a> for how
              citations fit alongside the rest. If you're ready to actually build yours out, see our
              <a href="/seo/local-citations/">local SEO citation packages</a> — flat pricing, 50 to 300 high-DA
              citations, delivered in 4-5 days.</p>
            """),
        ],
        "faqs": [
            ("Do citations still matter for local SEO in 2026?", "Yes — consistent, accurate business information across the web remains a foundational trust signal for local search, even as other ranking factors evolve."),
            ("Can bad citations hurt my rankings?", "Inconsistent or duplicate citations don't typically cause a penalty, but they dilute the trust signal citations are meant to build, which can indirectly hold back local rankings."),
            ("Should I build citations myself or hire it out?", "It's doable yourself with time and attention to detail — the main risk is inconsistency across dozens of listings. Many businesses outsource it specifically to guarantee accuracy at scale."),
        ],
        "cta": {
            "heading": "Ready to build yours out?",
            "text": "See our local SEO citation packages — 50 to 300 high-DA citations with accurate, consistent NAP, delivered in 4-5 days.",
            "href": "/seo/local-citations/",
            "label": "See citation packages",
        },
    },
    {
        "slug": "how-to-build-local-citations-the-right-way",
        "title": "How to Build Local Citations the Right Way (Without Hurting Your Rankings)",
        "category": "SEO & PPC",
        "read_minutes": 8,
        "description": "A step-by-step process for building local SEO citations correctly — auditing existing listings, standardizing NAP, prioritizing quality, and avoiding the mistakes that backfire.",
        "excerpt": "Building citations badly can do more harm than not building them at all. Here's the right order of operations — audit first, then build, then maintain.",
        "intro": """
          <p>Citation building sounds simple — get your business listed in more places — but done carelessly,
          it can actually work against you. Duplicate listings, inconsistent formatting, and low-quality
          directories can dilute the exact trust signal citations are supposed to build. Here's the right order
          of operations.</p>
        """,
        "sections": [
            ("Step 1: Audit What Already Exists", """
              <p>Before building anything new, find out what's already out there. Search your business name,
              address, and phone number directly, and check major directories individually. You're looking
              for:</p>
              <ul>
                <li>Duplicate listings for the same location</li>
                <li>Outdated information — an old address, a disconnected phone number, a former business name</li>
                <li>Inconsistent formatting of your name, address, or phone number across listings</li>
              </ul>
              <p>Skipping this step is the single most common reason citation building backfires — building 100
              new, accurate citations doesn't fix 20 old, conflicting ones sitting alongside them.</p>
            """),
            ("Step 2: Standardize Your NAP Before Building Anything New", """
              <p>Decide on one exact, canonical format for your business name, address, and phone number —
              down to abbreviations ("Street" vs. "St.", "Suite" vs. "#") — and use that exact format
              everywhere going forward, starting with your own website. Every new citation should match this
              format precisely.</p>
            """),
            ("Step 3: Fix Existing Inconsistencies Before Adding New Listings", """
              <p>Where possible, claim and correct existing listings you found in the audit before adding new
              ones. Piling new, accurate citations on top of old, conflicting ones only adds more noise to clean
              up later.</p>
            """),
            ("Step 4: Prioritize Quality and Relevance Over Raw Volume", """
              <p>A smaller number of citations on high-authority, relevant directories is worth more than a
              large volume of low-quality or unrelated ones. Prioritize well-known general directories, plus
              directories specific to your industry or region — a citation on a directory your actual
              customers might browse carries more value than an obscure, low-traffic listing site.</p>
            """),
            ("Step 5: Submit to Data Aggregators Early", """
              <p>Since aggregators redistribute your information to a much wider network automatically,
              getting accurate data into them early means many downstream listings inherit the correct
              information from the start, rather than needing individual correction later.</p>
            """),
            ("Step 6: Monitor and Maintain Over Time", """
              <p>Citations aren't a one-time task. Business moves, phone number changes, and even directories
              themselves restructuring can all introduce drift over time. A periodic check — every few months
              for an active business — catches small inconsistencies before they accumulate.</p>
            """),
            ("DIY vs. Hiring It Out", """
              <p>Doing it yourself is entirely possible — the work itself isn't technically difficult, just
              detail-heavy and repetitive across dozens of individual listings. The real risk is inconsistency
              creeping in across that volume of manual work, which is exactly what undermines the strategy. For
              that reason, many businesses — especially ones without the spare time to do it carefully — hire
              it out specifically to guarantee accuracy at scale. See our
              <a href="/seo/local-citations/">local SEO citation packages</a> if that's the route you'd rather
              take.</p>
            """),
            ("Common Mistakes That Backfire", """
              <ul>
                <li><strong>Buying cheap, bulk citation packages from unknown sources</strong> — often built on
                low-quality, spammy directories that add little value and occasionally carry real risk.</li>
                <li><strong>Skipping the audit step</strong> — building new citations without first cleaning up
                existing duplicates or inconsistencies.</li>
                <li><strong>Inconsistent formatting between the new citations and your own website</strong> —
                undercutting the very consistency citations are meant to establish.</li>
                <li><strong>Treating it as "set and forget"</strong> — citations drift out of accuracy over
                time without periodic review.</li>
              </ul>
            """),
            ("How This Fits Into Your Broader Local SEO", """
              <p>Citation building works best alongside the rest of your local SEO — see our
              <a href="/blog/what-are-local-seo-citations/">guide to what citations actually are</a> if you want
              the fundamentals first, or our
              <a href="/blog/local-seo-checklist-for-georgia-small-businesses/">full local SEO checklist</a> for
              everything else that should be in place alongside your citations.</p>
            """),
        ],
        "faqs": [
            ("How long does it take to see results from citation building?", "Citations tend to work as a cumulative trust signal rather than an immediate ranking trigger — many businesses see gradual improvement in local visibility over weeks to a couple of months as listings propagate and get indexed."),
            ("Can I remove duplicate citations myself?", "Often yes, through each directory's claim and edit process, though it can be time-consuming across many listings — this is one of the more tedious parts of a proper citation audit."),
            ("Is it better to build citations slowly or all at once?", "Either can work. A large, sudden batch is fine as long as every listing is accurate and consistent from the start — the risk isn't speed, it's inaccuracy."),
        ],
        "cta": {
            "heading": "Want this done right the first time?",
            "text": "Skip the manual audit and cleanup — see our local SEO citation packages, built with accurate, consistent NAP from the start.",
            "href": "/seo/local-citations/",
            "label": "See citation packages",
        },
    },
]


# ------------------------------------------------------------- image gen --

BLUE_DEEP = "#1E3A8A"
BLUE = "#2563EB"
BLUE_DARK = "#1D4ED8"
GOLD = "#F5B400"


def _wrap_title(title, width=17):
    return textwrap.wrap(title, width=width, break_long_words=False)


def featured_image_svg(title, category):
    lines = _wrap_title(title)
    line_height = 64
    start_y = 315 - (len(lines) - 1) * line_height / 2
    text_tspans = "".join(
        f'<tspan x="80" y="{start_y + i * line_height:.0f}">{esc(line)}</tspan>'
        for i, line in enumerate(lines)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BLUE_DEEP}"/>
      <stop offset="0.55" stop-color="{BLUE}"/>
      <stop offset="1" stop-color="{BLUE_DARK}"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <path d="M1000 630c0-140 80-260 200-320v320z" fill="#ffffff" opacity="0.06"/>
  <path d="M1090 50c-55 0-100 45-100 100 0 75 100 170 100 170s100-95 100-170c0-55-45-100-100-100z"
        fill="#ffffff" opacity="0.10"/>
  <circle cx="1090" cy="150" r="50" fill="none" stroke="#ffffff" stroke-opacity="0.10" stroke-width="12"/>
  <rect x="80" y="70" width="150" height="38" rx="19" fill="{GOLD}"/>
  <text x="155" y="95" text-anchor="middle" font-family="Poppins, Arial, sans-serif" font-size="16"
        font-weight="700" fill="#3a2c00" letter-spacing="0.5">{esc(category.upper())}</text>
  <text font-family="Fraunces, Georgia, serif" font-size="56" font-weight="600" fill="#ffffff">{text_tspans}</text>
  <text x="80" y="580" font-family="Poppins, Arial, sans-serif" font-size="20" fill="#ffffff" opacity="0.85">
    Georgia Marketing Agencies
  </text>
</svg>'''


# ----------------------------------------------------------------- build --

def toc_html(sections):
    items = "".join(
        f'<li><a href="#{slugify(heading)}">{esc(heading)}</a></li>'
        for heading, _ in sections
    )
    return f'<nav class="toc" aria-label="Table of contents"><p class="toc-title">On this page</p><ol>{items}</ol></nav>'


def sections_html(sections):
    out = []
    for heading, body in sections:
        out.append(f'<h2 id="{slugify(heading)}">{esc(heading)}</h2>{body}')
    return "".join(out)


def faq_block(faqs):
    if not faqs:
        return "", None
    html = "".join(
        f'<details class="faq-item"><summary>{esc(q)}</summary><p class="faq-answer">{a}</p></details>'
        for q, a in faqs
    )
    schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}}
            for q, a in faqs
        ],
    }
    return f'<section class="section" style="max-width:820px;"><h2>Frequently asked questions</h2><div class="faq-list">{html}</div></section>', schema


def blog_post_html(post):
    slug = post["slug"]
    url = f"{SITE}/blog/{slug}/"
    img_url = f"/assets/blog/{slug}.svg"
    faq_html, faq_schema = faq_block(post.get("faqs"))

    schemas = [
        {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post["title"],
            "description": post["description"],
            "image": f"{SITE}{img_url}",
            "author": {"@type": "Organization", "name": "Georgia Marketing Agencies"},
            "publisher": {"@type": "Organization", "name": "Georgia Marketing Agencies"},
            "mainEntityOfPage": url,
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
                {"@type": "ListItem", "position": 3, "name": post["title"], "item": url},
            ],
        },
    ]
    if faq_schema:
        schemas.append(faq_schema)
    schema_html = "".join(f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in schemas)

    cta = post.get("cta") or {}

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(post["title"])} | Georgia Marketing Agencies Blog</title>
  <meta name="description" content="{esc(post["description"])}" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="/assets/favicon.svg" />
  <meta property="og:title" content="{esc(post["title"])}" />
  <meta property="og:description" content="{esc(post["description"])}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{SITE}{img_url}" />
  <meta property="og:site_name" content="Georgia Marketing Agencies" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(post["title"])}" />
  <meta name="twitter:description" content="{esc(post["description"])}" />
  <meta name="twitter:image" content="{SITE}{img_url}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  {schema_html}
</head>
<body>
{HEADER_NAV}
  <main>
    <article class="blog-article">
      <section class="page-hero">
        <div class="page-hero-inner">
          <p class="crumbs"><a href="/">Home</a> / <a href="/blog/">Blog</a> / {esc(post["title"])}</p>
          <p class="eyebrow">{esc(post["category"])} · {post["read_minutes"]} min read</p>
          <h1>{esc(post["title"])}</h1>
        </div>
      </section>

      <img class="blog-featured-image" src="{img_url}" alt="{esc(post["title"])}" width="1200" height="630" />

      <div class="blog-body">
        {post["intro"]}
        {toc_html(post["sections"])}
        {sections_html(post["sections"])}
      </div>
    </article>

    {faq_html}

    <section class="section">
      <div class="claim-banner">
        <h2>{esc(cta.get("heading", "Ready to find the right marketing partner?"))}</h2>
        <p>{esc(cta.get("text", "Browse the directory or see our own services."))}</p>
        <a class="btn btn-primary btn-lg" href="{cta.get("href", "/services/")}">{esc(cta.get("label", "Get started"))}</a>
      </div>
    </section>
  </main>
{FOOTER}
  <script src="/script.js"></script>
</body>
</html>
'''


def blog_card_html(post):
    img_url = f"/assets/blog/{post['slug']}.svg"
    return f'''
      <a class="blog-card" href="/blog/{post['slug']}/">
        <img src="{img_url}" alt="" loading="lazy" />
        <div class="blog-card-body">
          <span class="tag">{esc(post['category'])}</span>
          <h3>{esc(post['title'])}</h3>
          <p>{esc(post['excerpt'])}</p>
          <span class="blog-card-meta">{post['read_minutes']} min read</span>
        </div>
      </a>'''


def blog_hub_html(posts):
    url = f"{SITE}/blog/"
    title = "Blog | Georgia Marketing Agencies"
    desc = "Marketing strategy, SEO, domains, and budgeting guides for Georgia businesses and the agencies that serve them."
    cards = "".join(blog_card_html(p) for p in posts)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <link rel="canonical" href="{url}" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="/assets/favicon.svg" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:site_name" content="Georgia Marketing Agencies" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "{url}" }}
    ]
  }}
  </script>
</head>
<body>
{HEADER_NAV}
  <main>
    <section class="page-hero">
      <div class="page-hero-inner">
        <p class="crumbs"><a href="/">Home</a> / Blog</p>
        <p class="eyebrow">Guides &amp; Resources</p>
        <h1>The Georgia Marketing Agencies Blog</h1>
        <p class="lead">Strategy, SEO, budgeting, and domain guides for Georgia businesses — and the agencies
        that serve them.</p>
      </div>
    </section>
    <section class="section">
      <div class="blog-grid">{cards}</div>
    </section>
  </main>
{FOOTER}
  <script src="/script.js"></script>
</body>
</html>
'''


def main():
    blog_dir = os.path.join(BASE, "blog")
    os.makedirs(blog_dir, exist_ok=True)
    img_dir = os.path.join(BASE, "assets", "blog")
    os.makedirs(img_dir, exist_ok=True)

    for post in BLOG_POSTS:
        post_dir = os.path.join(blog_dir, post["slug"])
        os.makedirs(post_dir, exist_ok=True)
        with open(os.path.join(post_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(blog_post_html(post))
        with open(os.path.join(img_dir, f"{post['slug']}.svg"), "w", encoding="utf-8") as f:
            f.write(featured_image_svg(post["title"], post["category"]))

    with open(os.path.join(blog_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(blog_hub_html(BLOG_POSTS))

    print(f"wrote 1 blog hub and {len(BLOG_POSTS)} posts")

    # Append new URLs to sitemap.xml (idempotent).
    sitemap_path = os.path.join(BASE, "sitemap.xml")
    with open(sitemap_path, encoding="utf-8") as f:
        sitemap = f.read()
    import datetime
    today = datetime.date.today().isoformat()
    new_urls = ["/blog/"] + [f"/blog/{p['slug']}/" for p in BLOG_POSTS]
    added = 0
    for path in new_urls:
        loc = f"{SITE}{path}"
        if loc in sitemap:
            continue
        entry = f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n"
        sitemap = sitemap.replace("</urlset>", entry + "</urlset>")
        added += 1
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"added {added} new URLs to sitemap.xml")


if __name__ == "__main__":
    main()
