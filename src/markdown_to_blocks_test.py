import unittest

from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks:
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_removes_empty_blocks(self):
        md = """
        This is paragraph



        This is paragraph
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is paragraph",
                "This is paragraph",
            ],
        )
    

    def test_removes_trailing_spaces(self):
        md = "This is paragraph        "
        blocks = markdown_to_blocks(md)
        self.assertEqual( blocks, ["This is paragraph"],
        )


if __name__ == "__main__":
    unittest.main()

