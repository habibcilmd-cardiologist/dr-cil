# SEO Audit Findings

## Root Redirect Issues ✅ TAMAMLANDI

Root redirects are conflicting and likely suppressing rankings:

-   `netlify.toml` forces 302 from `/` to `/en/` for many countries and `/ar/`/`/tr/` for others
-   `config.toml` also has a dev redirect `/` → `/tr/`
-   Googlebot will get a 302 away from the Turkish homepage, blocking "İstanbul Kardiyolog" visibility
-   **Fix**: Unify to a single canonical homepage (ideally `/tr/` or `/`) and serve other languages via hreflang, not geo-302

## Duplicate Homepage Variants

-   With `defaultContentLanguageInSubdir=true`, the real Turkish home is `/tr/`
-   Canonical in `head.html` points to the current URL, so `/` vs `/tr/` may both exist
-   **Fix**: Pick one canonical (recommend `/tr/`) and ensure the other redirects 301 to it

## Hreflang Coverage ✅ TAMAMLANDI

-   Head partial doesn't emit hreflang tags
-   Without hreflang, TR/EN/AR pages can compete with each other
-   **Fix**: Check/enable theme hreflang or add a partial

## Structured Data ✅ TAMAMLANDI

Structured data is strong but fragmented:

-   Homepage/about injects `Person` + `MedicalBusiness` + keyword-rich `knowsAbout` (`extend-head-uncached.html`)
-   Services get `MedicalProcedure` (`schema-procedure.html`)
-   FAQ front matter supported (`schema-faq.html`)
-   Generic `Article` fallback (`schema.html`)
-   **Risk**: Blog/services/clinic pages skip the fallback schema to avoid conflicts
-   **Fix**: Ensure every target page loads exactly one JSON-LD block and that procedures include `body_location`, `medical_specialty`, `how_performed`, `faq` in front matter for richer snippets

## Homepage Keyword Focus ✅ TAMAMLANDI

-   Good in TR (`_index.md` title "İstanbul Kardiyolog…" plus keyword list)
-   EN/AR don't target Turkish queries (OK, but internal links from EN/AR to TR pillar will help authority)
-   Hero H1 is just the name
-   **Fix**: Consider an H1/H2 that explicitly says "İstanbul Kardiyolog" while keeping E-E-A-T context

## Search UX

-   Works client-side (`search.html` + Fuse) but there's no precomputed snippet
-   **Fix**: Ensure `index.json` includes services/clinic pages so long-tail queries like "diyabetik ayak" surface

## Verification & Analytics

-   GSC/Bing codes empty in `params.toml`; GA disabled
-   **Fix**: Add and verify to monitor

## Other Technical Elements

-   ✅ Robots/sitemap fine (`robots.txt`, sitemap shipped)
-   ✅ Headers: strict and cached

---

# Keyword-Specific Plan

_TR primary; mirror to EN/AR with equivalent intents_

## Service Landing Pages

Create/optimize service landing pages (one per intent) under `tr/hizmetler/` (and `/services/`, `/ar/services/` equivalents) using existing `MedicalProcedure` schema:

1. **"İstanbul Kardiyolog / Kardiyoloji Uzmanı İstanbul"** (pillar: Turkish homepage or `/tr/hizmetler/kardiyoloji-uzmani-istanbul/`)
2. **"Bacak Damarlarını Açma"** & **"Ayak Damarlarını Açma"** (peripheral arterial interventions, CTA to WhatsApp/clinic)
3. **"Periferik Arter Hastalığı Tedavisi"**
4. **"Girişimsel Kardiyoloji İstanbul"**
5. **"Damar Açma / Ameliyatsız Damar Açma"**
6. **"Ayak Yarası / Diyabetik Ayak"** (include wound care, vascular angle)

### For Each Page

-   Set `title`, `description`, `keywords`, `procedure_type`, `body_location`, `medical_specialty`, `how_performed`
-   Add 3–6 FAQs in front matter (`faq:` array) to trigger FAQ rich results
-   Interlink between related pages + blog posts

## Internal Linking ✅ TAMAMLANDI

-   From homepage services grid, add anchor links to these exact slugs
-   From every blog article insert contextual links to the relevant service landing

## On-Page Elements

-   Unique H1 that matches the main keyword
-   H2s covering variants
-   Include city ("İstanbul") in intro and CTA blocks
-   Add local schema markers (`areaServed` already present—keep consistent)

## Multilingual Hreflang

-   Add hreflang cluster for each page trio (TR/EN/AR)
-   Ensure canonicals point to themselves and no mixed 302

## Local Signals

-   Embed map link already in schema
-   Add a visible NAP block and a Google Maps link on homepage/clinic
-   Add testimonials (with `Review` schema) if policy allows

---

# Technical Fixes (Priority)

1. **Remove/replace geo 302s**: Make `/` serve Turkish (or 301 to `/tr/`), serve EN/AR via language switcher + hreflang. Avoid country-conditional redirects for bots.
2. **Add hreflang tags** for all three languages (site-wide partial) and set canonical to the chosen primary URL.
3. **Ensure only one JSON-LD per page**: Keep `Person`/`Business` on home/about; `MedicalProcedure` on service pages; `Article`/`FAQ` as needed.
4. **Fill verification IDs**; submit sitemaps per locale in GSC; monitor coverage and queries ("İstanbul Kardiyolog" etc.).
5. **Performance/UX**: Keep lazyloading (already on), ensure hero images are compressed WebP with `width`/`height` attributes.

---

# Next Actions

1. Implement hreflang + canonical cleanup and adjust netlify redirects to a single canonical root
2. Build/optimize TR/EN/AR service landing pages for the listed keywords with enriched front matter + FAQ
3. Add homepage H1/H2 and internal links tuned for "İstanbul Kardiyolog"
4. Wire verification codes and sanity-check JSON-LD outputs

**Pick a step (1–4) to proceed.**
