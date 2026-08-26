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
            figures = re.findall(
                r'<figure class="repo-shot desktop chocomics-shot">.*?</figure>',
                self.card,
                re.DOTALL,
            )
            matching_figures = [
                figure
                for figure in figures
                if f'src="assets/work-repos/{filename}"' in figure
            ]
            self.assertEqual(
                len(matching_figures),
                1,
                f"expected exactly one figure for screenshot: {filename}",
            )
            figure = matching_figures[0] if matching_figures else ""
            self.assertIn(f'alt="{alt}"', figure)
            self.assertIn(f"<figcaption>{caption}</figcaption>", figure)
            self.assertEqual(figure.count("data-live-preview"), 1)

            path = ROOT / "assets" / "work-repos" / filename
            if not path.is_file():
                self.fail(f"missing screenshot: {filename}")
            header = path.read_bytes()
            self.assertGreaterEqual(len(header), 24)
            self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack(">I", header[8:12])[0], 13)
            self.assertEqual(header[12:16], b"IHDR")
            width, height = struct.unpack(">II", header[16:24])
            self.assertGreaterEqual(width, 1200)
            self.assertGreaterEqual(height, 650)


if __name__ == "__main__":
    unittest.main()
