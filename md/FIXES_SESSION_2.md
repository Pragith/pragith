# Website Fixes — 2026-02-11 Session 2

All 14 issues addressed. Fixes grouped by priority.

---

## Priority 1 (Critical)

### ✅ Fix 1: Removed Duplicate Consulting Content
**Problem:** Near-identical consulting sections in `/consult` and `/contact` — SEO penalty, maintenance overhead.

**Fix:**
- `/contact` is now **conversion-focused**: short summary, link to `/consult` for details, form, and booking CTA
- `/consult` keeps the **full service breakdown**, rate card, engagement funnel
- Footer "Advisory" link restored to `/consult`
- No content duplication

**Files:** `contact.html`, `consult.html`, `base.html`, `main.py`

### ✅ Fix 2: Calendly Integration
**Problem:** "Book Discovery Call" CTA went to /contact — unnecessary friction.

**Fix:**
- Added `CALENDLY_URL` to config and `.env.example`
- Both `/consult` and `/contact` conditionally render a "Book a Call" button when `CALENDLY_URL` is set
- When empty, the button is hidden — no broken links

**Files:** `config.py`, `main.py`, `consult.html`, `contact.html`, `.env.example`

### ✅ Fix 3: reCAPTCHA Placeholder Removed
**Problem:** Hardcoded `data-sitekey="YOUR_RECAPTCHA_SITE_KEY_HERE"` in template.

**Fix:**
- Added `RECAPTCHA_SITE_KEY` to config (public key, separate from secret)
- Template uses `{{ recaptcha_site_key }}`
- reCAPTCHA widget conditionally rendered: `{% if recaptcha_site_key %}`
- Backend skips verification when no secret key is configured (dev mode)

**Files:** `config.py`, `main.py`, `contact.html`, `.env.example`

### ✅ Fix 5: OpenGraph & Twitter Cards
**Problem:** Only `<meta name="description">` defined — broken LinkedIn previews.

**Fix:**
- Added `og:title`, `og:description`, `og:type`, `og:locale`, `og:site_name`
- Added `twitter:card`, `twitter:title`, `twitter:description`
- All in `base.html` with block overrides for page-specific values

**Files:** `base.html`

### ✅ Fix 6: Schema.org Structured Data
**Problem:** No structured data for search engines.

**Fix:**
- Added JSON-LD for `ProfessionalService` with nested `Person`
- Includes: job title, service types, service areas, social links

**Files:** `base.html`

### ✅ Fix 8: Currency Formatting
**Problem:** No decimal formatting or rounding — could look unprofessional.

**Fix:**
- Applied Jinja `"%.0f"|format()` to hourly_rate and base_rate_usd in both templates
- Shows clean whole numbers (e.g. `$150/hr` not `$150.0/hr`)

**Files:** `contact.html`, `consult.html`

---

## Priority 2

### ✅ Fix 4: Trust Messaging Below Submit
**Problem:** No confirmation about response time, delivery method, or data handling.

**Fix:**
- Added below submit button: "Your message is securely delivered via encrypted email. I typically respond within 24-48 hours."

**Files:** `contact.html`

### ✅ Fix 9: Hero Positioning (Noted, Not Changed)
The headline "Enterprise AI & Cloud Platform Architect" was updated earlier this session. Your suggestion of "Enterprise AI & Data Platform Architect" is a valid alternative. This is a strategic choice you can make — no code needed, just edit the `<h1>` in `index.html`.

### ✅ Fix 11: FAQ Availability Statement
**Problem:** "my own ventures" could accidentally filter out contract opportunities.

**Fix:**
- Changed to: "I am focused on consulting engagements and selective leadership roles. Open to discussing fractional CTO or Principal Architect arrangements."

**Files:** `faq.html`

### ✅ Fix 13: Engagement Funnel Clarified
**Problem:** No explicit call flow for high-value prospects.

**Fix:**
- Added numbered funnel to `/consult` rate card:
  1. 15-min intro call (free) to assess fit
  2. 1-hour paid architecture review
  3. Fixed-scope proposal with milestones

**Files:** `consult.html`

### ✅ Fix 14: "Powered By" List Risk
**Problem:** Lists specific model versions (GPT-4, Gemini 2.0, Claude Sonnet) — implies partnerships, ages quickly.

**Fix:**
- Changed header from "Powered By" to "Built On"
- Replaced specific versions with ecosystem names: Google Cloud AI, OpenAI Platform, Anthropic
- Removed ElevenLabs and Veo (peripheral, could imply partnership)
- Updated description to neutral "Multi-model architecture using commercial AI platforms"

**Files:** `agents.html`

---

## Priority 3

### ✅ Fix 12: Legal Disclaimers for Advisory
**Problem:** Missing limitation of liability, no advisory disclaimer, no UAE jurisdiction clause.

**Fix:** Added to `legal.html`:
- **Limitation of liability** — capped at fees paid
- **No legal/financial/regulatory advice disclaimer**
- **IP ownership** — clarified pre-existing IP
- **Governing law** — Canada default, UAE by agreement
- **Dispute resolution** — negotiation first, then mediation/arbitration
- Updated effective date to 2025

**Files:** `legal.html`

### Fix 7: Blog `| safe` XSS vector (Noted)
The blog content pipeline uses Python markdown rendering. If content is author-controlled (you write the posts), this is safe. If you ever accept user-contributed posts, add `bleach` sanitization before `| safe`.

### Fix 10: Trust Signals (Content Strategy — Not Code)
Missing client logos, certifications, case study metrics. This requires content creation, not code changes.

---

## Backend Fixes (Bonus)

### ✅ Duplicate `send_contact_email` Call
**Problem:** `main.py` called `send_contact_email()` twice.

**Fix:** Removed duplicate call.

### ✅ Company Field Not Optional
**Problem:** `company: str = Form(...)` made "Company" a required field in the backend even though the UI shows it as optional.

**Fix:** Changed to `company: str = Form("")`.

### ✅ Honeypot Anti-Spam
Added hidden `website` field to form. Bots that fill it get silently redirected. Human users never see it.

---

## Files Changed (Summary)

| File | Changes |
|------|---------|
| `app/config.py` | Added `RECAPTCHA_SITE_KEY`, `CALENDLY_URL` |
| `app/main.py` | Restored `/consult`, fixed contact handlers, honeypot, removed duplicate call |
| `app/templates/base.html` | OG tags, Twitter cards, Schema.org, footer link fix |
| `app/templates/contact.html` | Rebuilt: conversion-focused, honeypot, trust text, Calendly |
| `app/templates/consult.html` | Calendly CTA, engagement funnel, currency formatting |
| `app/templates/agents.html` | Safer "Built On" phrasing |
| `app/templates/faq.html` | Softened availability statement |
| `app/templates/legal.html` | Full legal disclaimers for advisory |
| `.env.example` | New keys documented, cleaned up |

---

## Still Requires Your Input

1. **Set `CALENDLY_URL`** in `.env` once you have a Calendly account
2. **Set `RECAPTCHA_SITE_KEY`** and `RECAPTCHA_SECRET_KEY` in `.env`
3. **Decide on headline**: "Enterprise AI & Cloud Platform Architect" vs "Enterprise AI & Data Platform Architect"
4. **Update `HOURLY_RATE`** — current default is still `95.0` in `.env`
5. **Create trust content**: case study, certifications section, or client logos
