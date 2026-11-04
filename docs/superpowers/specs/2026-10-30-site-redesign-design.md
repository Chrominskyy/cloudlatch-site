# CloudLatch website redesign

Date: 2026-10-30. Status: awaiting review.

## Goal

Rebuild the public CloudLatch website from scratch with current web best practices. Keep the previous site as a tracked backup. Direction: product-led, native macOS utility look.

## Constraints

- Follow `AGENTS.md`: IAM-user access key + MFA only, no SSO or external provider claims, no invented App Store link, screenshots, prices, reviews or contact details.
- Static site, relative URLs, GitHub Pages project path, no JavaScript, remote fonts, analytics or third-party embeds.
- Privacy and support text move over verbatim. Only markup and layout change.
- `CHANGELOG.md` stays at the root and its README link stays visible.
- Existing deep links keep working (`privacy.html#remove-data`, `support.html#setup`, `support.html#reports`, `index.html#workflow`).

## Structure

Backup via `git mv` into `_old/`: `index.html`, `support.html`, `privacy.html`, `styles.css`, `assets/`, `docs/design.md`. `_old/` pages carry `noindex`; `robots.txt` disallows `/cloudlatch-site/_old/`.

New root files: `index.html`, `support.html`, `privacy.html`, `css/main.css` (cascade layers: tokens, base, layout, components, pages), `assets/` (hero in AVIF/WebP/JPEG, `favicon.svg`, `og-image.png`), `robots.txt`, `sitemap.xml`, rewritten `docs/design.md`. README updated for the layout and backup. Hero source: existing `cloudlatch-concept.jpg`.

## Visual system

- System font stack, fluid type via `clamp()`.
- OKLCH tokens, cool neutrals and forest-green accent; light/dark via `prefers-color-scheme`; text contrast at least 4.5:1.
- CSS grid and container queries; spacing token scale; 16px minimum side gutter on phones.
- Transitions only, disabled under `prefers-reduced-motion`. Visible `:focus-visible` outlines. Skip link.

## Pages

Home: hero with availability notice ("In preparation for the App Store", no download link) and a labelled abstract menu-bar illustration in inline SVG (not a screenshot, no identifiers); three-step flow; three feature cards; scope block (macOS 14+, IAM user access keys and MFA, no SSO); support band; independence disclaimer in footer.

Support and privacy: shared header/footer; sticky table of contents on wide screens, collapsed `<details>` on narrow; original heading ids preserved.

## Metadata and performance

Per page: title, description, canonical, Open Graph, Twitter card, `theme-color` for both schemes. No JSON-LD `SoftwareApplication` (implies availability/pricing). Hero via `<picture>`, `fetchpriority="high"`, explicit dimensions. One stylesheet, no fonts, no third-party requests.

## Verification

`scripts/check_site.py` extended: `_old/` excluded from the page set; required meta and canonical; image dimensions and alt; heading order; anchors including legacy ones; forbidden-claims scan (SSO support, App Store links, prices, em dash). Local preview with Playwright screenshots at 375, 768 and 1280 px, light and dark. Report repository changes, local preview and live deployment separately; deployment is not claimed.

## Out of scope

New copy claims, app screenshots, download links, JavaScript, build tooling.
