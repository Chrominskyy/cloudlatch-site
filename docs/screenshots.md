# Capturing CloudLatch screenshots for the website

The site currently shows HTML illustrations of the menu panel (labels from the app, sample data). Replace them with real captures once they can be made on a Mac. Never fabricate a successful AWS session for a screenshot: use the isolated test environment, and synthetic names only.

## Setup

- A signed or development build of the current version (record version and build).
- A dedicated macOS user or a clean desktop: plain wallpaper, no other status items if possible, Dock hidden.
- An isolated AWS test account with least-privilege roles. Never the owner's production credentials.
- Synthetic names matching the site: account `Work`, source profile `work-source`, roles `dev`, `stable`, `prod-readonly`. Add a second account `Personal` for the account menu.
- System appearance: one set in Light and one in Dark.

## Shots

| File | What to capture | Notes |
| --- | --- | --- |
| `assets/shots/panel-active.png` | Menu panel open with an active role (`AWS: dev`), source and role expiry visible | Replaces the hero illustration |
| `assets/shots/panel-mfa.png` | Panel after `Refresh dev...` with the `MFA code for dev` prompt, field empty | Do not type a real code |
| `assets/shots/panel-switch.png` | `Switch Profile` menu open with the three aliases | |
| `assets/shots/panel-account.png` | `Account: Work` menu open showing `Work` and `Personal` | |
| `assets/shots/settings.png` | Settings window: account picker, AWS directory, AWS Source, Authentication and Profiles sections | Directory path and role ARNs must be synthetic |

Capture with `⇧⌘4`, then `Space`, and click the panel or window (this keeps the macOS shadow). Capture the menu bar strip separately with `⇧⌘4` and a drag if needed. Retina captures are 2×; keep the PNG at 2× and set `width`/`height` in HTML to the 1× size.

## Before publishing

1. Inspect every image at full size for real account IDs, ARNs, paths, user names, other apps' status items and notifications. Replace or retake if anything real is visible.
2. Convert to WebP with a PNG or JPEG fallback (for example `cwebp -q 85 panel-active.png -o panel-active.webp`).
3. In `index.html`, replace the `.stage` figure's panel with a `<picture>` of `panel-active`, keep the menu bar strip, and change the caption to "Screenshot · version X.Y (build N), sample data".
4. Update `docs/design.md` (asset provenance) and run `python3 scripts/check_site.py`.
