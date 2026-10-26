# CloudLatch

**AWS Session Manager for macOS**

Public website repository for CloudLatch, a native Mac menu bar app for AWS MFA sessions and IAM role switching.

## Brand

- Product name: **CloudLatch**
- Descriptor: **AWS Session Manager**
- Repository: `cloudlatch-site`, following `devpulse-site` and `mighty-markdown-site`
- Language: English

CloudLatch pairs a cloud reference with the idea of controlled access. It belongs alongside DevPulse and Mighty Markdown as a focused native utility.

## Website scope

- Product overview and supported authentication flow
- Setup instructions and support
- Privacy policy based on the shipped application and its AWS SDK dependencies

## Status

The first static website is implemented: product overview, setup/support and development-stage privacy information. It has not been deployed. The application is being prepared for App Store distribution; no download or App Store availability is claimed.

Only public website content belongs here. Keep application source, AWS credentials, account identifiers, session files, signing material and private diagnostics out of this repository.

CloudLatch is an independent product and is not affiliated with or endorsed by Amazon Web Services.

## Support and reports

Use the [issue chooser](https://github.com/Chrominskyy/cloudlatch-site/issues/new/choose) for bugs, incidents, feature requests and support questions. Reports may be written in English or Polish.

Read [Contributing and support](CONTRIBUTING.md) before attaching evidence. Issues are public; never include AWS credentials, identifiers, profile files or private diagnostics.

Report vulnerabilities through the [private security channel](SECURITY.md). Community participation follows the [Code of conduct](CODE_OF_CONDUCT.md).

## Local preview

No package installation or build step is required.

```sh
python3 scripts/check_site.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765. Relative links support the GitHub Pages project path.

## Release work

- Verify the final app artifact and replace development-stage privacy information with the approved policy and dedicated privacy contact.
- Add approved app screenshots and a verified App Store URL when available.
- Enable GitHub Pages separately and verify the live site.

The site uses no JavaScript, remote fonts, analytics or third-party embeds. Appearance follows the system light/dark preference.
