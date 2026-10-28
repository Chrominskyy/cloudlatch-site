# CloudLatch changelog

This log describes app changes. An unreleased entry is in development, not an available download or App Store release.

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
