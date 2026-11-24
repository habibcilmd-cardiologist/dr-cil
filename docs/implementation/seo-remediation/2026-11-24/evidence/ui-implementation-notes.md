# UI implementation notes — 24 November 2026

Source implementation is complete for this UI slice. Runtime acceptance is
owned by the parent integration task; this file does not claim a browser,
native zoom, full contrast audit or WCAG pass.

## Changes and audit linkage

| IDs / status | Change | Source |
| --- | --- | --- |
| UI-01 / Uygulandı–Doğrulama Bekliyor | Correct the existing header.showTitle/disableTextInHeader boolean lookup; respect the configured hidden text. Give navigation its own 1024px breakpoint, nonshrinking words and 44px controls. Remove the global horizontal overflow mask. The actual header height updates spacer and anchor offsets. | layouts/partials/header/basic.html:24,208; header/fixed.html; assets/css/custom.css:11; assets/js/mobilemenu.js |
| UI-02 / Uygulandı–Doğrulama Bekliyor | Direct and legacy fallback expertise strings are Interventional Cardiology in TR/EN/AR; no global removal of vascular terminology. Floating card values can wrap. Hero fallback wiring is the performance slice. | i18n/tr.yaml:12,26; en.yaml:14,28; ar.yaml:138,151; custom.css |
| UI-03 / Uygulandı–Doğrulama Bekliyor | Native mobile menu buttons with names, controls/expanded, hidden labelled dialog, Escape and focus restoration. Common controller preserves prior inert/overflow state, traps focus and tabs. A native details navigation fallback remains available when the bundle cannot execute. | header/basic.html:91; assets/js/mobilemenu.js:14,74 |
| UI-04 / Uygulandı–Doğrulama Bekliyor | Named search dialog, real input label, localized live status, Escape/Tab handling and exact opener restoration. Search form cannot accidentally submit/reload. Appointment triggers use real href and progressive dialog behavior; Space/Enter work on the enhanced trigger. Dialog content scrolls in short/zoomed viewports. | search.html; assets/js/search.js:26,38; extend-footer.html:552 |
| UI-05 / Uygulandı–Doğrulama Bekliyor | Shared controls/status/disclaimer/WhatsApp messages are translated, including Arabic. Language picker is native details with real language links. Foreign search entries show languageName and have lang/dir metadata. New optional 3D strings and keyboard hint match the performance implementation. | header/language-switcher.html; i18n/*.yaml; search.js; extend-footer.html |
| UI-06 / Uygulandı–Doğrulama Bekliyor | Mobile fallback navigation and native language selector work without the deferred bundle; appointment floating link points to the correct contact page. Script-only search/appearance controls are exposed after enhancement. Hero fallback is coordinated through data-appointment-trigger in the performance slice. | header/basic.html; mobilemenu.js; extend-footer.html; performance-owned hero.html |
| UI-07 / Uygulandı–Doğrulama Bekliyor | Real Arabic message and /ar/ recovery/contact links; TR recovery uses the root canonical path. Contact block is a neutral contact label, not a claim that the private number is emergency care. Actual HTTP404 remains a server acceptance test. | layouts/404.html; i18n/*.yaml |
| PERF-02 related / Uygulandı–Doğrulama Bekliyor | Reduced-motion covers hero and the actual .ic-diagram-section/.all-services-section selectors. 3D request/render preferences are performance-owned. | assets/css/custom.css |

Search index content and query text are rendered with DOM text nodes;
non-HTTP(S) result targets are rejected. The original 15-second timeout and
retry-on-reopen behavior are retained. Index failure does not break the
other UI controllers. This is not a full security assessment.

The red/green CTA palette is retained with darker opaque text backgrounds.
The calculated white-on-background contrast improved from 1.983 to 5.428
for the WhatsApp hero CTA and 3.547 to 5.622 for the appointment hero CTA.
Floating WhatsApp's icon pair improved from 1.983 to 4.135. These exact
CSS-color calculations are in `ui-color-pairs.json`; actual computed styles,
transparent surfaces, all text and all states still require browser review.

## Checks actually run

- `node --check assets/js/search.js`: exit0.
- `node --check assets/js/mobilemenu.js`: exit0.
- Extracted appointment footer script + `node --check`: exit0.
- Shared UI/3D localization key-set and duplicate-key checks: see
  `ui-static-validation.json`; in-memory Python AST parses the contract helper.
- Own isolated minify Hugo build: **TIMEOUT after 180 seconds**, during
  concurrent source implementation. No completed build or render acceptance
  is claimed from this attempt. Exact command and limitation: `ui-build.json`.

The first Python bytecode compilation attempt was blocked because its
configured global cache was outside writable roots. The helper was checked
with an in-memory AST parse; no cache permission was bypassed.

## Integration checks still required

Use the parent's final consolidated build, not the incomplete UI temp output:

```sh
python3 scripts/check_ui_contract.py BUILD --output ui-contract-final.json
```

This checks every non-alias HTML's native controls, dialog title references,
input labels, localized feedback, fallback contact targets and 404 recovery
language. It is a rendered HTML contract test, not computed layout or focus.

Root browser acceptance: TR/EN/AR, requested width matrix including both the
old 852/853/854 boundary and new 1023/1024/1025 boundary; native %200; actual
focus cycle/Escape/return and inert background; language/details dismissal;
search loading/error/empty/result keyboard behavior; JS/CDN disabled fallback;
short-height modal scrolling; touch targets, computed contrast and RTL.
No DNS/account, real message, commit/push/deploy or theme-submodule edit was
performed by the UI slice.

## Primary sources opened on 2026-11-24

- https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- https://www.w3.org/WAI/ARIA/apg/patterns/button/
- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html

These guide implementation and the color-pair checks; they do not certify
this site's complete accessibility compliance.
