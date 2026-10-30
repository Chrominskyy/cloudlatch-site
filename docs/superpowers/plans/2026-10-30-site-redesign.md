# CloudLatch Website Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the public CloudLatch site with a product-led redesign, keeping the old site as a tracked backup in `_old/`.

**Architecture:** Three static HTML pages share one layered stylesheet (`css/main.css`). The checker script gates every task. Old files move with `git mv` first so history is preserved.

**Tech Stack:** HTML, CSS (cascade layers, OKLCH, container queries), inline SVG, Python 3 stdlib checker, Playwright for visual checks.

**Spec:** `docs/superpowers/specs/2026-10-30-site-redesign-design.md`

## Global Constraints

- IAM-user access key + MFA only. No SSO, Identity Center or external provider support claims.
- No App Store link, download link, screenshot, price, review or contact detail that is not already in the old site.
- Relative URLs only, no leading `/`, valid under a GitHub Pages project path.
- No JavaScript, remote fonts, analytics or third-party embeds.
- Privacy and support body text is copied verbatim from `_old/`. Only markup and layout change.
- Preserve ids: `index.html#workflow`, `support.html#setup`, `support.html#reports`, `privacy.html#remove-data`.
- No em dash (`—`) in any HTML page.
- `CHANGELOG.md` stays at root; README keeps its visible changelog link.
- Text contrast at least 4.5:1; 16px minimum side gutter at phone width; honor `prefers-color-scheme` and `prefers-reduced-motion`.
- Every GitHub-facing artifact written to the repo contains no AWS identifiers or credentials.

## Review Focus

- 320px viewport: no horizontal scroll, nav still reachable.
- Forced high zoom (200%): layout does not overlap.
- Dark mode: all text and focus rings keep contrast.
- Old deep links (`privacy.html#remove-data`) land on a heading after the move.
- Images blocked/failed: hero alt text and layout space remain.

## File Structure

- `_old/` : backup of previous site (moved, not edited except `noindex`).
- `css/main.css` : all styles, layered `tokens, base, layout, components, pages`.
- `index.html`, `support.html`, `privacy.html` : pages.
- `assets/` : `cloudlatch-hero.{avif,webp,jpg}`, `favicon.svg`, `og-image.png`.
- `robots.txt`, `sitemap.xml` : crawl control.
- `scripts/check_site.py` : site checker.
- `docs/design.md` : rewritten design notes.

---

### Task 1: Backup the old site and extend the checker

**Files:**
- Move: `index.html`, `support.html`, `privacy.html`, `styles.css`, `assets/`, `docs/design.md` to `_old/` (same relative names)
- Create: `robots.txt`
- Modify: `scripts/check_site.py`

**Interfaces:**
- Produces: `check_site.py` rules used by every later task: pages = root `*.html` only; each page needs `<title>`, `meta description`, `link rel=canonical` (relative-safe https URL under `https://chrominskyy.github.io/cloudlatch-site/`), `og:title`, `og:description`, `og:image`; heading levels never skip; `_old/` pages must contain `noindex`; forbidden-claims scan on root pages.

- [ ] **Step 1: Extend `check_site.py` with the rules above and a `FORBIDDEN` list** (`"Identity Center"` and `"SSO"` allowed only in a sentence containing "not"; regex for `apps.apple.com`, `$\d`, `€\d`, `—`). Keep the `ROOT.glob("*.html")` page set.
- [ ] **Step 2: Run `python3 scripts/check_site.py`**. Expected: FAIL (missing canonical/og tags on old pages).
- [ ] **Step 3: `git mv` the listed files into `_old/`, then add `<meta name="robots" content="noindex">` to each `_old/*.html` head and fix its `styles.css`/`assets/` relative paths remain valid (they move together).**
- [ ] **Step 4: Create `robots.txt`** with `User-agent: *`, `Disallow: /cloudlatch-site/_old/`, `Sitemap: https://chrominskyy.github.io/cloudlatch-site/sitemap.xml`.
- [ ] **Step 5: Commit** `git commit -m "Move previous site to _old and tighten site checker"`.

### Task 2: Design system stylesheet and assets

**Files:**
- Create: `css/main.css`, `assets/favicon.svg`, `assets/og-image.png`, `assets/cloudlatch-hero.avif`, `.webp`, `.jpg` (from `_old/assets/cloudlatch-concept.jpg` via local conversion, 1024 and 512 widths)

**Interfaces:**
- Produces CSS classes later tasks use: `.container`, `.site-header`, `.site-nav`, `.skip-link`, `.hero`, `.notice`, `.steps`, `.cards`, `.card`, `.scope`, `.band`, `.prose`, `.toc`, `.callout`, `.site-footer`. Tokens: `--bg`, `--surface`, `--text`, `--muted`, `--line`, `--accent`, `--on-accent` (OKLCH, with dark overrides in `@media (prefers-color-scheme: dark)`).

- [ ] **Step 1: Write `css/main.css`** with `@layer tokens, base, layout, components, pages;`, fluid type via `clamp()`, `.container { padding-inline: max(16px, 4vw) }`, `:focus-visible` outline, `@media (prefers-reduced-motion: reduce)` disabling transitions, container query on `.cards`.
- [ ] **Step 2: Produce image variants** with `cwebp`/`avifenc`/ImageMagick if available (check with `which`); if a tool is missing, ship JPEG + WebP only and record that in `docs/design.md`.
- [ ] **Step 3: Create `favicon.svg`** (forest-green latch glyph, no text) and `og-image.png` 1200x630 from the hero.
- [ ] **Step 4: Verify contrast** with a short script computing WCAG ratios for text/background token pairs in both schemes. Expected: all text pairs >= 4.5.
- [ ] **Step 5: Commit** `git commit -m "Add layered stylesheet and optimized assets"`.

### Task 3: Home page

**Files:**
- Create: `index.html`

**Interfaces:**
- Consumes: Task 2 classes and assets.
- Produces: header/footer markup that Tasks 4 and 5 copy exactly (nav: How it works `index.html#workflow`, Support, Privacy; footer links Support, Privacy, GitHub).

- [ ] **Step 1: Run checker** `python3 scripts/check_site.py`. Expected: FAIL (`index.html` missing).
- [ ] **Step 2: Write `index.html`** with one `<h1>` ("Your AWS roles. Within reach."), availability `.notice` ("In preparation for the App Store", no link), `<picture>` hero with `fetchpriority="high"` and width/height, inline SVG menu-bar illustration with `role="img"` and an `aria-label` stating it is an illustration, `#workflow` three-step list, three `.card`s, `.scope` block (macOS 14 or later, IAM user access keys and MFA, SSO and external providers not supported), support band, independence disclaimer. Copy text from `_old/index.html`; add no new claims.
- [ ] **Step 3: Add head metadata**: title, description, canonical, Open Graph, Twitter card, `theme-color` for light and dark, favicon link, stylesheet `css/main.css`.
- [ ] **Step 4: Run checker.** Expected: pass for `index.html` (support/privacy still missing is acceptable only until Task 5).
- [ ] **Step 5: Commit** `git commit -m "Add redesigned home page"`.

### Task 4: Support page

**Files:**
- Create: `support.html`

**Interfaces:**
- Consumes: Task 3 header/footer; `.prose`, `.toc`, `.callout`.

- [ ] **Step 1: Write `support.html`** by carrying every section of `_old/support.html` verbatim into `<main class="prose">`, keeping ids `setup` and `reports` and adding ids to other h2s. Table of contents inside a `<details open>` that CSS pins open on wide screens.
- [ ] **Step 2: Add head metadata** as in Task 3; `aria-current="page"` on Support nav link.
- [ ] **Step 3: Verify text parity:** extract visible text of old and new `<main>` and diff. Expected: only the TOC differs.
- [ ] **Step 4: Run checker.** Expected: pass.
- [ ] **Step 5: Commit** `git commit -m "Add redesigned support page"`.

### Task 5: Privacy page

**Files:**
- Create: `privacy.html`

- [ ] **Step 1: Write `privacy.html`** exactly as Task 4 but from `_old/privacy.html`, preserving id `remove-data` and every external link.
- [ ] **Step 2: Verify text parity** with the same diff method. Expected: only the TOC differs.
- [ ] **Step 3: Run checker.** Expected: all three pages pass.
- [ ] **Step 4: Commit** `git commit -m "Add redesigned privacy page"`.

### Task 6: Metadata, docs and visual verification

**Files:**
- Create: `sitemap.xml`
- Modify: `README.md`, `docs/design.md` (new file, rewritten), `CONTRIBUTING.md` only if it references moved paths

- [ ] **Step 1: Write `sitemap.xml`** with the three canonical URLs.
- [ ] **Step 2: Rewrite `docs/design.md`** describing the new system, asset provenance (hero is conceptual artwork, illustration is not a screenshot) and the `_old/` backup. Update README layout and preview sections; keep the changelog link.
- [ ] **Step 3: Serve locally** `python3 -m http.server 8765 --bind 127.0.0.1` and capture Playwright screenshots of all three pages at 375, 768 and 1280 px, light and dark. Check for horizontal overflow with `document.documentElement.scrollWidth <= innerWidth`. Expected: no overflow, no console errors, no failed requests.
- [ ] **Step 4: Run checker and `grep -rn "styles.css" --include=*.html --include=*.md . | grep -v _old`**. Expected: pass, no stale references.
- [ ] **Step 5: Commit and push** `git push -u origin claude/gracious-ptolemy-hl4879`. Report repository changes, local preview and live deployment separately; do not claim the site is live.
