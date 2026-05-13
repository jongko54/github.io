# Portfolio Analytics

This portfolio is hosted on GitHub Pages, so page-level visitor logs need an external analytics endpoint.

## Active tracking hook

The site sends lightweight visit beacons to a Vercel endpoint:

```text
https://portfolio-visitor-tracker.vercel.app/api/visit
```

The tracker logs runtime events with the `PORTFOLIO_VISIT` marker. It captures:

- path, including hash fragments such as `#work-repos`
- page title
- referrer, when the browser sends it
- browser language, screen size, viewport, and timezone
- Vercel geo headers such as country/region/city when available
- user agent for rough browser/bot/AI-client inference

It intentionally does not log raw IP addresses.

Check recent events with:

```text
vercel logs portfolio-visitor-tracker.vercel.app
```

Browsers and services often hide the exact previous URL, so referrers may show
only the domain such as `github.com`, `google.com`, or `jobkorea.co.kr`.

## GitHub repository traffic

GitHub also exposes repository traffic, but it is not the same as exact GitHub Pages visitor analytics.

```bash
gh api repos/jongko54/github.io/traffic/views
gh api repos/jongko54/github.io/traffic/popular/referrers
gh api repos/jongko54/github.io/traffic/popular/paths
```
