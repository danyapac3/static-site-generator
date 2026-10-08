import unittest

from blocktype import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertIs(block_to_block_type("# some hello world"), BlockType.HEADING)
        self.assertIs(block_to_block_type("## some hello world"), BlockType.HEADING)
        self.assertIs(block_to_block_type("### some hello world"), BlockType.HEADING)
        self.assertIs(block_to_block_type("#### some hello world"), BlockType.HEADING)
        self.assertIs(block_to_block_type("##### some hello world"), BlockType.HEADING)
        self.assertIs(block_to_block_type("###### some hello world"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#some hello world"), BlockType.PARAGRAPH)

    def test_code(self):
        text = "```\n```"
        self.assertIs(block_to_block_type(text), BlockType.CODE)
        text = "```\nsome\n```"
        self.assertIs(block_to_block_type(text), BlockType.CODE)
        text = "```\nsome```"
        self.assertIs(block_to_block_type(text), BlockType.PARAGRAPH)
        text = "``````"
        self.assertIs(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_quote(self):
        text = "```\n```"
        self.assertIs(block_to_block_type(text), BlockType.CODE)
        text = "```\nsome\n```"
        self.assertIs(block_to_block_type(text), BlockType.CODE)
        text = "```\nsome```"
        self.assertIs(block_to_block_type(text), BlockType.PARAGRAPH)
        text = "``````"
        self.assertIs(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        text = "- item\n- item\n- item"
        self.assertIs(block_to_block_type(text), BlockType.UNORDERED_LIST)

        text = "- item\n-item\n- item"
        self.assertIs(block_to_block_type(text), BlockType.PARAGRAPH)

        text = "- item\n- item\nx item"
        self.assertIs(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        text = "1. item\n2. item\n3. item"
        self.assertIs(block_to_block_type(text), BlockType.ORDERED_LIST)
        
        text = "2. item\n3. item\n4. item"
        self.assertIs(block_to_block_type(text), BlockType.PARAGRAPH)
        
        text = "1. item\n2.item\n3. item"
        self.assertIs(block_to_block_type(text), BlockType.PARAGRAPH)
        
        text = "1. item\n2 item\n3. item"
        self.assertIs(block_to_block_type(text), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
