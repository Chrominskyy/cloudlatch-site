# CloudLatch changelog

This log describes app changes. An unreleased entry is in development, not an available download or App Store release.

## [1.4.0] - 2026-11-26

Build: 11

### Added
- "Refresh all roles..." in the menu refreshes every role of the selected account in one action, asking for an MFA code once when a new source session is needed. The role selected in the menu is refreshed last, so it stays the active role behind the default profile and keeps auto-renewal; the other roles are refreshed but not auto-renewed. A role that fails does not stop the others, and the failures are listed.
- Optional `cloudlatch://refresh-role?alias=<role alias>` link refreshes one role of the selected account. It cannot carry an MFA code, so it needs an active source session (or access-key authentication). Like account switching, it is disabled by default and its outcome, including the active profile, is written to `external-command-result.json`.

### Changed
- External commands now run one at a time in arrival order, so a refresh finishes before a following account switch is applied.

## [1.3.0] - Unreleased

Build: 10

### Added
- Optional `cloudlatch://switch-account?name=<account>` (or `?id=<account id>`) link for switching the selected account from scripts and tools. Disabled by default; enable it in Settings. Switching does not refresh credentials, and the outcome is written to `external-command-result.json`.

## [1.2.2] - Unreleased

Build: 9

### Fixed
- Menu bar popover closes after a successful refresh and when the app loses focus; refresh errors remain visible.
- Settings opens in front of other applications, including when reopening an existing Settings window.

## [1.2.1] - Unreleased

Build: 8

### Fixed
- Restored standard macOS editing shortcuts, including paste, in profile editors and other text fields.

## [1.2.0] - Unreleased

Build: 7

### Added
- Optional access-key authentication without MFA, selectable separately for each saved account.
- Automatic renewal of temporary source sessions for accounts configured without MFA.

### Changed
- Existing configurations continue to require MFA. Cached source sessions are isolated by authentication method.

## [1.1.3] - Unreleased

Build: 6

### Fixed
- Account name entry now receives keyboard focus when adding or renaming an account.
- SwiftPM launches explicitly use the menu bar app activation policy so Settings can accept keyboard input.

## [1.1.2] - Unreleased

Build: 5

### Changed
- Updated AWS SDK 1.8.14 → 1.8.17, Smithy 0.259.0 → 0.260.0 and AWS CRT 0.64.2 → 0.64.3.
- Updated compatible Swift Certificates, Collections, Configuration, Distributed Tracing and NIO Extras releases.
- Retained checksum-verified SDK archive preparation and local package references for repeatable builds.

## [1.1.1] - Unreleased

Build: 4

### Fixed
- Local builds prepare the pinned AWS SDK from its verified release source archive, avoiding the SDK Git-history fetch in Xcode and SwiftPM.
- Added a repeatable dependency preparation command shared by native and package builds.

## [1.1.0] - Unreleased

Build: 3

### Added
- Saved AWS accounts with names and switching from Settings or the menu bar.
- Separate account configurations, authorized AWS directories and Keychain MFA sessions.
- Existing settings remain available as Default account without moving credentials or configuration files.

### Changed
- Only the selected account renews. Switching preserves cached MFA sessions and requires an explicit role refresh before replacing AWS credentials.
- Account switching is blocked during a credential refresh; pending prompts are cleared when the account changes.

## [1.0.1] - Unreleased

Build: 2

### Fixed
- Replaced the Project.Hermes icon with CloudLatch cloud-and-lock artwork matching DevPulse and Mighty Markdown.
- Preserved the original artwork in the repository as `artwork/Media_old.xcassets`.

## [1.0.0] - Unreleased

Build: 1

### Added
- Native macOS menu bar workflow for AWS IAM user credentials, MFA and role switching.
- Separate source-session and role-session expiry information.
- Automatic role-renewal attempts while the source MFA session remains valid.
- User-selected AWS configuration directory with persistent authorized access.
- macOS Keychain storage for temporary source sessions.
- Product website, setup guidance and channels for support, incidents and private security reports.

### Changed
- Public product name is CloudLatch, with the descriptor AWS Session Manager.
- Authentication uses the AWS SDK for Swift without requiring an AWS CLI installation.

### Fixed
- Credential updates preserve unrelated profiles and reject source/output collisions and detected file conflicts.
- Changing authentication configuration invalidates the cached source session.
- Persisted diagnostics omit profile names and raw AWS error payloads.

### Current scope
- IAM user access keys with MFA; IAM Identity Center / SSO and external credential providers are not currently supported.
- Refreshing replaces credentials in the selected role profile and `default`.
- Distribution signing, live AWS validation and final privacy disclosures remain release work.
