import re
import struct
import unittest
import zlib
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
        style_match = re.search(r"<style\b[^>]*>(.*?)</style>", cls.html, re.DOTALL)
        cls.css = style_match.group(1) if style_match else ""
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

        anchors = re.findall(r"<a\b[^>]*>", self.card)
        self.assertEqual(len(anchors), 4, "ChoComics card must contain exactly 4 anchors")
        for index, anchor in enumerate(anchors, start=1):
            self.assertEqual(
                re.findall(r'\bhref="([^"]*)"', anchor),
                ["https://chocomics.keiailab.com/"],
                f"anchor {index} must have the exact ChoComics href",
            )
            self.assertEqual(
                re.findall(r'\btarget="([^"]*)"', anchor),
                ["_blank"],
                f"anchor {index} must target _blank",
            )
            self.assertEqual(
                re.findall(r'\brel="([^"]*)"', anchor),
                ["noreferrer"],
                f"anchor {index} must use rel=noreferrer",
            )

    def _read_png_dimensions(self, path):
        data = path.read_bytes()
        label = path.name
        self.assertGreaterEqual(
            len(data),
            24,
            f"{label} must contain a complete PNG signature and IHDR header",
        )
        self.assertEqual(
            data[:8],
            b"\x89PNG\r\n\x1a\n",
            f"{label} has an invalid PNG signature",
        )
        self.assertEqual(
            struct.unpack(">I", data[8:12])[0],
            13,
            f"{label} first chunk must be a 13-byte IHDR",
        )
        self.assertEqual(
            data[12:16],
            b"IHDR",
            f"{label} first chunk must be IHDR",
        )

        offset = 8
        dimensions = None
        iend_seen = False
        while offset < len(data):
            self.assertLessEqual(
                offset + 12,
                len(data),
                f"{label} has a truncated chunk header at byte {offset}",
            )
            length = struct.unpack(">I", data[offset : offset + 4])[0]
            chunk_type = data[offset + 4 : offset + 8]
            chunk_data_start = offset + 8
            chunk_data_end = chunk_data_start + length
            chunk_crc_end = chunk_data_end + 4
            self.assertLessEqual(
                chunk_data_start,
                len(data),
                f"{label} chunk {chunk_type!r} starts past EOF",
            )
            self.assertLessEqual(
                chunk_data_end,
                len(data),
                f"{label} chunk {chunk_type!r} exceeds EOF",
            )
            self.assertLessEqual(
                chunk_crc_end,
                len(data),
                f"{label} chunk {chunk_type!r} has a truncated CRC",
            )

            chunk_data = data[chunk_data_start:chunk_data_end]
            expected_crc = struct.unpack(">I", data[chunk_data_end:chunk_crc_end])[0]
            actual_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
            self.assertEqual(
                actual_crc,
                expected_crc,
                f"{label} chunk {chunk_type!r} has an invalid CRC",
            )

            if chunk_type == b"IHDR":
                self.assertIsNone(dimensions, f"{label} contains duplicate IHDR chunks")
                self.assertEqual(
                    length,
                    13,
                    f"{label} IHDR must contain exactly 13 bytes",
                )
                dimensions = struct.unpack(">II", chunk_data[:8])
            elif chunk_type == b"IEND":
                self.assertEqual(length, 0, f"{label} IEND must have zero length")
                self.assertEqual(
                    chunk_crc_end,
                    len(data),
                    f"{label} IEND must terminate exactly at EOF",
                )
                iend_seen = True
                break

            offset = chunk_crc_end

        self.assertTrue(iend_seen, f"{label} is missing a terminating IEND chunk")
        self.assertIsNotNone(dimensions, f"{label} is missing an IHDR chunk")
        return dimensions

    def _css_rule_body(self, selector):
        match = re.search(
            rf"{re.escape(selector)}\s*\{{([^}}]*)\}}",
            self.css,
            re.DOTALL,
        )
        self.assertIsNotNone(match, f"missing CSS rule for {selector}")
        return match.group(1) if match else ""

    def test_chocomics_styling_contract(self):
        description_match = re.search(
            r'<div class="work-project-description">(.*?)</div>',
            self.card,
            re.DOTALL,
        )
        self.assertIsNotNone(description_match, "ChoComics description is missing")
        description = description_match.group(1) if description_match else ""
        self.assertRegex(
            description,
            r'<a\b[^>]*class="chocomics-inline-link"[^>]*>ChoComics</a>',
            "ChoComics description link must use chocomics-inline-link",
        )

        inline_link = self._css_rule_body(".chocomics-inline-link")
        self.assertRegex(
            inline_link,
            r"\bcolor\s*:\s*var\(--accent-blue\)\s*;",
            "chocomics-inline-link must use the accent blue color",
        )
        self.assertRegex(
            inline_link,
            r"\btext-decoration\s*:\s*underline\s*;",
            "chocomics-inline-link must be underlined",
        )

        visited_link = self._css_rule_body(".chocomics-inline-link:visited")
        self.assertRegex(
            visited_link,
            r"\bcolor\s*:\s*var\(--accent-blue\)\s*;",
            "visited ChoComics links must retain the accent blue color",
        )
        self.assertRegex(
            visited_link,
            r"\btext-decoration\s*:\s*underline\s*;",
            "visited ChoComics links must remain underlined",
        )

        focus_visible = self._css_rule_body(".chocomics-inline-link:focus-visible")
        self.assertRegex(
            focus_visible,
            r"\boutline\s*:\s*(?!none\b)(?!0(?:\.0+)?(?:px)?\b)[^;]+;",
            "focused ChoComics links must have a visible outline",
        )

        screenshot_image = self._css_rule_body(".repo-shot.chocomics-shot img")
        self.assertRegex(
            screenshot_image,
            r"\bcursor\s*:\s*pointer\s*;",
            "ChoComics screenshot images must use a pointer cursor",
        )

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
            self.assertEqual(
                self._read_png_dimensions(path),
                (1280, 720),
                f"{filename} must be exactly 1280x720",
            )


if __name__ == "__main__":
    unittest.main()
