# CloudLatch website design

Product-led static site in the style of a native macOS utility. Three pages (`index.html`, `support.html`, `privacy.html`), one stylesheet (`css/main.css`), no JavaScript, remote fonts, analytics or third-party embeds.

## System

- Cascade layers in order: `tokens`, `base`, `layout`, `components`, `pages`.
- System font stack with fluid type via `clamp()`.
- OKLCH tokens: cool neutrals and a forest-green accent. Light and dark follow `prefers-color-scheme`; text contrast is at least 4.5:1.
- Spacing token scale, 16px minimum side gutter on phones, CSS grid and container queries.
- Cards: `.cards-wrap` is the query container and `.cards` the grid inside it.
- Support and privacy: sticky table of contents beside the prose on wide screens; a collapsed `<details class="toc">` on narrow screens.
- Transitions only, disabled under `prefers-reduced-motion`. Visible `:focus-visible` outlines and a skip link.

## Asset provenance

- The hero image is conceptual brand artwork generated with an image generation tool and optimized locally. It is not an app screenshot. Source: the previous `cloudlatch-concept.jpg`, kept in `_old/assets/`.
- The menu-bar illustration on the home page is hand-written inline SVG. It is an abstract drawing, not a screenshot, and contains no identifiers.
- The hero ships as WebP and JPEG at 512 and 1024 px. AVIF was not produced because no encoder was available.
- `assets/favicon.svg` and `assets/og-image.png` are brand assets. No app screenshots, App Store links, prices or reviews are used.

## Metadata

Each page has a title, description, canonical URL, Open Graph and Twitter card tags and `theme-color` for both schemes. The index canonical is the bare directory URL. There is no `SoftwareApplication` JSON-LD because it would imply availability and pricing. `sitemap.xml` lists the three canonical URLs.

## Backup

The previous site is kept under `_old/` (pages, `styles.css`, assets and the previous design notes). Its pages carry a `noindex` meta tag, which is what keeps them out of search results. `robots.txt` disallows `/cloudlatch-site/_old/`, but it takes effect only if served at the host root, not under the project path. It is excluded from `scripts/check_site.py`.

## Content rules

Product, support and privacy copy follows `AGENTS.md`: IAM-user access key and MFA only, no SSO claim, no invented App Store link. Privacy content remains development-stage until the distribution artifact and contact are final.
