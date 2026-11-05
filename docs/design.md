# CloudLatch website design

Static product site with the precision of a macOS utility. Three pages (`index.html`, `support.html`, `privacy.html`), one stylesheet (`assets/site.css`), no JavaScript, no remote fonts, analytics or third-party embeds.

## System

- Light "aluminium" scheme by default, dark navy scheme through `prefers-color-scheme`. Tokens are CSS custom properties at the top of `site.css`; text meets 4.5:1 contrast in both schemes.
- Colors follow the current app icon: navy ink and an azure accent, with the icon's sky blue for decoration only.
- Type: Instrument Sans (variable width and weight) for display and body; Martian Mono for labels, credentials-file excerpts and metadata.
- Background: a faint brushed-metal line texture with a sky glow at the top.
- Signature elements:
  - Hero: a macOS menu bar with the `AWS: dev` status item and the panel beneath it. Every label comes from the app's SwiftUI source (`MenuBarRootView`), with sample data.
  - "Two sessions, two clocks": the source session and repeated role sessions with the five-minute renewal window.
  - A credentials-file excerpt showing which profiles a refresh writes and which it leaves alone.
- Motion: one staggered load sequence, the panel opening and the session bars growing; all off under `prefers-reduced-motion`.
- Support and privacy: sticky table of contents beside the prose on wide screens, a `<details>` table of contents on narrow screens, `<details>` troubleshooting items.

## Asset provenance

- `assets/app-icon-256.png`, `assets/apple-touch-icon.png`, `assets/favicon-32.png`: the app icon (cloud and lock), exported from the app's asset catalog.
- `assets/og-image.png`: rendered from the hero illustration and headline; marked "Illustration with sample data".
- There are no app screenshots yet. The interface drawings are HTML illustrations, labelled as such. See `docs/screenshots.md`.
- The previous brushed-metal hero artwork and the green favicon are kept in `_old/assets/`.

## Content rules

Product, support and privacy copy follows `AGENTS.md`. Saved accounts (1.1) and access keys without MFA (1.2) are described from the app source; the privacy policy says so until a signed build of those versions has been inspected.

## Backup

`_old/` holds the previous site (pages, `css/main.css`, assets); `_old/v1/` holds the first site. All backup pages carry `noindex` and are checked by `scripts/check_site.py`.
