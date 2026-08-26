# ChoComics Portfolio Card Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a live-linked ChoComics project card with two current product screenshots to the portfolio's `WEB/APP` category and publish it through GitHub Pages.

**Architecture:** Keep the portfolio as one static `index.html` and reuse its existing wide project-card and two-column screenshot-grid patterns. Add one Python standard-library contract test for the HTML and PNG assets, then capture the deployed ChoComics homepage into two repository assets and verify both the local and deployed portfolio in a browser.

**Tech Stack:** Static HTML/CSS/JavaScript, Python 3 `unittest`, PNG assets, GitHub Pages

---

### Task 1: Define the portfolio contract with a failing test

**Files:**
- Create: `tests/test_chocomics_portfolio.py`
- Inspect: `index.html:1640-1646`
- Inspect: `index.html:2421-2454`

- [ ] **Step 1: Write the failing structural and asset test**

Create `tests/test_chocomics_portfolio.py` with this complete content:

```python
import re
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
SCREENSHOTS = (
    "chocomics-01-featured-ranking.png",
    "chocomics-02-new-weekday.png",
)


class ChoComicsPortfolioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.normalized_html = " ".join(cls.html.split())
        cls.web_app = cls.html.split(
            'id="work-category-web-app"', 1
        )[1].split('id="work-category-ai-workflow"', 1)[0]
        match = re.search(
            r'<article class="work-project is-wide" data-project="chocomics">(.*?)</article>',
            cls.web_app,
            re.DOTALL,
        )
        cls.card = match.group(1) if match else ""

    def test_web_app_count_and_card_placement(self):
        self.assertIn(
            'WEB/APP <span class="tab-count">6</span>',
            self.normalized_html,
        )
        self.assertTrue(self.card, "ChoComics card is missing")
        self.assertLess(
            self.web_app.index('data-project="chocomics"'),
            self.web_app.index(
                '<div class="work-project-name">Marketing App Platform</div>'
            ),
        )

    def test_card_content_and_live_links(self):
        self.assertIn("ChoComics · AI 웹툰 플랫폼", self.card)
        self.assertIn("React · TypeScript · Webtoon platform", self.card)
        self.assertIn("오늘의 웹툰", self.card)
        self.assertIn("실시간 랭킹", self.card)
        self.assertIn("이달의 신작", self.card)
        self.assertIn("요일 연재", self.card)
        self.assertGreaterEqual(
            self.card.count('href="https://chocomics.keiailab.com/"'),
            3,
        )
        self.assertEqual(self.card.count("data-live-preview"), 2)

    def test_screenshot_markup_and_png_files(self):
        expected = {
            "chocomics-01-featured-ranking.png": (
                "ChoComics featured webtoon and real-time ranking",
                "Featured &amp; Ranking",
            ),
            "chocomics-02-new-weekday.png": (
                "ChoComics monthly releases and weekday serialization",
                "New &amp; Weekday",
            ),
        }

        for filename in SCREENSHOTS:
            alt, caption = expected[filename]
            self.assertIn(f'src="assets/work-repos/{filename}"', self.card)
            self.assertIn(f'alt="{alt}"', self.card)
            self.assertIn(f"<figcaption>{caption}</figcaption>", self.card)

            path = ROOT / "assets" / "work-repos" / filename
            self.assertTrue(path.is_file(), f"missing screenshot: {filename}")
            header = path.read_bytes()[:24]
            self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n")
            width, height = struct.unpack(">II", header[16:24])
            self.assertGreaterEqual(width, 1200)
            self.assertGreaterEqual(height, 650)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and confirm the expected red state**

Run:

```bash
python3 -m unittest tests/test_chocomics_portfolio.py -v
```

Expected: 3 failing tests because the tab still says 5, the ChoComics card is absent, and both screenshots are absent.

### Task 2: Capture the two live ChoComics views

**Files:**
- Create: `assets/work-repos/chocomics-01-featured-ranking.png`
- Create: `assets/work-repos/chocomics-02-new-weekday.png`

- [ ] **Step 1: Capture the home hero and ranking view**

Open `https://chocomics.keiailab.com/` with the in-app browser, wait for the homepage to finish rendering, select the dark theme, return to the top of the page, and save a normal desktop viewport screenshot as:

```text
assets/work-repos/chocomics-01-featured-ranking.png
```

The screenshot must visibly include the ChoComics header, featured hero, and the first row of real-time ranking cards. Do not include browser chrome, login-only content, or personal data.

- [ ] **Step 2: Capture the new-release and weekday view**

In the same browser tab and theme, scroll until `이달의 신작.` is at the top portion of the viewport and `요일 연재.` is also visible, then save a normal desktop viewport screenshot as:

```text
assets/work-repos/chocomics-02-new-weekday.png
```

The two PNGs must use the same browser viewport dimensions.

- [ ] **Step 3: Verify both image files before editing HTML**

Run:

```bash
file assets/work-repos/chocomics-01-featured-ranking.png assets/work-repos/chocomics-02-new-weekday.png
sips -g pixelWidth -g pixelHeight assets/work-repos/chocomics-01-featured-ranking.png assets/work-repos/chocomics-02-new-weekday.png
```

Expected: both files report PNG format, both widths are at least 1200 pixels, both heights are at least 650 pixels, and their dimensions match.

- [ ] **Step 4: Re-run the contract test**

Run:

```bash
python3 -m unittest tests/test_chocomics_portfolio.py -v
```

Expected: the PNG existence and dimension checks are now satisfiable, while the card/count tests remain red because `index.html` is unchanged.

### Task 3: Add the ChoComics card and link behavior

**Files:**
- Modify: `index.html:909-936`
- Modify: `index.html:1644-1646`
- Modify: `index.html:2421-2454`
- Modify: `index.html:3145`
- Test: `tests/test_chocomics_portfolio.py`

- [ ] **Step 1: Add narrow ChoComics screenshot-link styles**

Immediately after the existing `.repo-shot.desktop` rule, add:

```css
        .repo-shot.chocomics-shot {
            aspect-ratio: auto;
        }

        .repo-shot.chocomics-shot a {
            color: inherit;
            display: block;
            text-decoration: none;
        }

        .repo-shot.chocomics-shot img {
            aspect-ratio: 16 / 9;
            height: auto;
        }
```

This keeps both captions visible while retaining the existing hover and responsive grid behavior.

- [ ] **Step 2: Update the Web/App count**

Change the Web/App tab markup to:

```html
            <button class="portfolio-tab" id="portfolio-tab-web-app" type="button" role="tab" aria-selected="false" data-tab-target="work-repos-panel" data-work-category-target="work-category-web-app">
                WEB/APP <span class="tab-count">6</span>
            </button>
```

- [ ] **Step 3: Insert the approved wide card before Marketing App Platform**

Insert this card as the first child of `.work-board-grid` inside `work-category-web-app`:

```html
                    <article class="work-project is-wide" data-project="chocomics">
                        <div class="work-project-header">
                            <div class="work-project-name">
                                <a href="https://chocomics.keiailab.com/" target="_blank" rel="noreferrer" style="color: inherit; text-decoration: none;">ChoComics · AI 웹툰 플랫폼</a>
                            </div>
                            <div class="work-project-meta">React · TypeScript · Webtoon platform</div>
                        </div>
                        <div class="work-project-description">
                            <p><a href="https://chocomics.keiailab.com/" target="_blank" rel="noreferrer">ChoComics</a>는 오래된 꿈을 펼쳐보는 웹툰 독자를 위한 웹 플랫폼입니다.</p>
                            <p>오늘의 웹툰과 실시간 랭킹, 이달의 신작, 요일 연재 탐색을 하나의 홈 흐름으로 구성하고 작품 상세와 서재 진입을 연결했습니다.</p>
                        </div>
                        <div class="shot-grid desktop-shots">
                            <figure class="repo-shot desktop chocomics-shot">
                                <a href="https://chocomics.keiailab.com/" target="_blank" rel="noreferrer" aria-label="Open ChoComics featured and ranking view">
                                    <img data-live-preview src="assets/work-repos/chocomics-01-featured-ranking.png" alt="ChoComics featured webtoon and real-time ranking" loading="lazy">
                                    <figcaption>Featured &amp; Ranking</figcaption>
                                </a>
                            </figure>
                            <figure class="repo-shot desktop chocomics-shot">
                                <a href="https://chocomics.keiailab.com/" target="_blank" rel="noreferrer" aria-label="Open ChoComics new and weekday view">
                                    <img data-live-preview src="assets/work-repos/chocomics-02-new-weekday.png" alt="ChoComics monthly releases and weekday serialization" loading="lazy">
                                    <figcaption>New &amp; Weekday</figcaption>
                                </a>
                            </figure>
                        </div>
                    </article>
```

- [ ] **Step 4: Keep live-linked screenshots out of the lightbox button set**

Change the gallery image selector to:

```javascript
        const galleryImages = Array.from(document.querySelectorAll('.repo-shot img:not([data-live-preview])'));
```

This prevents the screenshot links from opening the portfolio lightbox and a new browser tab at the same time.

- [ ] **Step 5: Run the contract test and confirm green**

Run:

```bash
python3 -m unittest tests/test_chocomics_portfolio.py -v
```

Expected: 3 tests pass, 0 failures.

- [ ] **Step 6: Commit the tested implementation**

Run:

```bash
git add index.html tests/test_chocomics_portfolio.py assets/work-repos/chocomics-01-featured-ranking.png assets/work-repos/chocomics-02-new-weekday.png
git commit -m "feat: add ChoComics portfolio showcase"
```

Expected: one feature commit containing the card, two screenshots, and its contract test.

### Task 4: Perform local desktop and mobile design QA

**Files:**
- Verify: `index.html`
- Verify: `assets/work-repos/chocomics-01-featured-ranking.png`
- Verify: `assets/work-repos/chocomics-02-new-weekday.png`

- [ ] **Step 1: Start the static portfolio locally**

Run from the worktree root:

```bash
python3 -m http.server 4173
```

Expected: the server listens on `http://127.0.0.1:4173/`.

- [ ] **Step 2: Verify the desktop card**

Open `http://127.0.0.1:4173/#work-repos` in the in-app browser and activate `WEB/APP`. Confirm all of the following in the rendered page:

```text
WEB/APP count: 6
First project: ChoComics · AI 웹툰 플랫폼
Desktop layout: two equal screenshot columns
Captions: Featured & Ranking; New & Weekday
Link target: https://chocomics.keiailab.com/
```

Capture a local QA screenshot showing the complete ChoComics card.

- [ ] **Step 3: Verify the mobile card**

Temporarily set the browser viewport to 390 × 844, reload the same local URL, and activate `WEB/APP`. Confirm that both screenshot figures stack in one column, text does not overflow, the tab strip remains usable, and both live links retain their targets. Capture a mobile QA screenshot, then reset the temporary viewport override.

- [ ] **Step 4: Check browser errors and rerun automated verification**

Run:

```bash
python3 -m unittest tests/test_chocomics_portfolio.py -v
git diff --check
git status --short --branch
```

Expected: 3 tests pass, `git diff --check` emits no output, and the worktree is clean after the feature commit. Browser console inspection reports no new errors from the ChoComics card.

### Task 5: Integrate, publish, and verify GitHub Pages

**Files:**
- Integrate: branch `feat/chocomics-portfolio-card`
- Publish: branch `main`
- Verify: `https://jongko54.github.io/github.io/`

- [ ] **Step 1: Confirm the feature branch is ready to integrate**

Run:

```bash
git status --short --branch
git log --oneline --decorate -5
python3 -m unittest tests/test_chocomics_portfolio.py -v
```

Expected: clean feature branch and 3 passing tests.

- [ ] **Step 2: Fast-forward the primary checkout to the feature branch**

Run:

```bash
git -C /Users/jongho/Temp/T1/github.io fetch origin main
git -C /Users/jongho/Temp/T1/github.io merge --ff-only feat/chocomics-portfolio-card
```

Expected: local `main` advances without a merge commit and preserves the approved design and implementation-plan commits.

- [ ] **Step 3: Push main and verify the exact remote ref**

Run:

```bash
git -C /Users/jongho/Temp/T1/github.io push origin main
git -C /Users/jongho/Temp/T1/github.io rev-parse HEAD
git ls-remote https://github.com/jongko54/github.io.git refs/heads/main
```

Expected: the local `HEAD` and remote `refs/heads/main` hashes are identical.

- [ ] **Step 4: Smoke-test the published HTML and image assets**

Run:

```bash
curl -fsSL https://jongko54.github.io/github.io/ | rg 'ChoComics · AI 웹툰 플랫폼|chocomics-01-featured-ranking.png|chocomics-02-new-weekday.png'
curl -fsSI https://jongko54.github.io/github.io/assets/work-repos/chocomics-01-featured-ranking.png
curl -fsSI https://jongko54.github.io/github.io/assets/work-repos/chocomics-02-new-weekday.png
```

Expected: the live HTML contains the title and both asset paths, and both image requests return HTTP 200.

- [ ] **Step 5: Verify the deployed visual result**

Open `https://jongko54.github.io/github.io/#work-repos` in the browser, activate `WEB/APP`, and capture the deployed desktop card. Confirm the count, ordering, two images, captions, mobile stacking, and links against the local QA result.
