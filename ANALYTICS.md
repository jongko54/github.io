# Portfolio Analytics

This portfolio is hosted on GitHub Pages, so page-level visitor logs need an external analytics endpoint.

## Active tracking hook

The site includes GoatCounter tracking code:

```html
https://jongko54.goatcounter.com/count
```

Create or claim the GoatCounter site code `jongko54`, then open:

```text
https://jongko54.goatcounter.com/
```

GoatCounter can show:

- visitor count
- page views
- popular paths, including `#work-repos`
- referrers, when the previous site/browser sends referrer data

Browsers and services often hide the exact previous URL, so referrers may show only the domain such as `github.com`, `google.com`, or `jobkorea.co.kr`.

## GitHub repository traffic

GitHub also exposes repository traffic, but it is not the same as exact GitHub Pages visitor analytics.

```bash
gh api repos/jongko54/github.io/traffic/views
gh api repos/jongko54/github.io/traffic/popular/referrers
gh api repos/jongko54/github.io/traffic/popular/paths
```
