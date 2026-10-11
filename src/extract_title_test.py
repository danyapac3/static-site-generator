import unittest

from extract_title import NoTitleError, extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# title"
        self.assertEqual(extract_title(md), "title")

        md = "# title 1 2 3\n\nsome paragraph"
        self.assertEqual(extract_title(md), "title 1 2 3")

    def test_no_title_found(self):
        md = " # title"
        self.assertRaises(NoTitleError, extract_title, md)
        md = "## title"
        self.assertRaises(NoTitleError, extract_title, md)
        md = "title"
        self.assertRaises(NoTitleError, extract_title, md)

if __name__ == "__main__":
    unittest.main()
