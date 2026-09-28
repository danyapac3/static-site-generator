import unittest

from patterns import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImage(unittest.TestCase):
    def test_exact_match(self):
        text = "![example](https://example.com)"
        self.assertListEqual(extract_markdown_images(text), [text])

    def test_two_exact_matches(self):
        text = "some garbage![example](https://example.com)![example](https://example.com)sdfdf"
        self.assertListEqual(
            extract_markdown_images(text),
            ["![example](https://example.com)", "![example](https://example.com)"]
        )

    def test_doesnt_match_link(self):
        text = "[example](https://example.com/image.com)"
        self.assertEqual(len(extract_markdown_images(text)), 0)

    def test_empty_alt_and_src(self):
        text = "![]()"
        self.assertListEqual(extract_markdown_images(text), [text])

class TestExtractMarkdownLink(unittest.TestCase):
    def test_exact_match(self):
        text = "[example](https://example.com)"
        self.assertListEqual(extract_markdown_links(text), [text])

    def test_two_exact_matches(self):
        text = "some garbage[example](https://example.com)[example](https://example.com)sdfdf"
        self.assertListEqual(
            extract_markdown_links(text),
            ["[example](https://example.com)", "[example](https://example.com)"]
        )

    def test_doesnt_match_image(self):
        text = "![example](https://example.com/image.com)"
        self.assertEqual(len(extract_markdown_links(text)), 0)

    def test_empty_alt_and_src(self):
        text = "[]()"
        self.assertListEqual(extract_markdown_links(text), [text])

if __name__ == "__main__":
    unittest.main()
