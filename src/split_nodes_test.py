import unittest

from split_nodes import (
    NoSecondDelimiterError,
    split_node_image,
    split_node_link,
    split_node_with_delimiters,
)
from textnode import TextNode, TextType


class TestSplitNodesImage(unittest.TestCase):
    CORRECT_IMAGE = "![alt text](www.imageurl.com)"
    def test_split_not_text_type(self):
        node = TextNode(self.CORRECT_IMAGE, TextType.BOLD)
        result_nodes = split_node_image(node)
        self.assertEqual(len(result_nodes), 1)
        self.assertEqual(node, result_nodes[0])

    def test_nothing_to_split(self):
        node = TextNode("some", TextType.TEXT)
        result_nodes = split_node_image(node)
        self.assertEqual(len(result_nodes), 1)
        self.assertEqual(node, result_nodes[0])

    def test_split_correct_image(self):
        node = TextNode("some![some alt](www.imageurl.com)some1", TextType.TEXT)
        result_nodes = split_node_image(node)
        self.assertEqual(len(result_nodes), 3)
        self.assertIs(result_nodes[0].text_type, TextType.TEXT)
        self.assertIs(result_nodes[1].text_type, TextType.IMAGE)
        self.assertIs(result_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(result_nodes[0].text, "some")
        self.assertEqual(result_nodes[2].text, "some1")
        self.assertEqual(result_nodes[1].text, "some alt")
        self.assertEqual(result_nodes[1].url, "www.imageurl.com")

    def test_split_correct_image_but_nothing_before_and_after(self):
        node = TextNode(self.CORRECT_IMAGE, TextType.TEXT)
        result_nodes = split_node_image(node)
        self.assertEqual(len(result_nodes), 3)
        self.assertIs(result_nodes[0].text_type, TextType.TEXT)
        self.assertIs(result_nodes[1].text_type, TextType.IMAGE)
        self.assertIs(result_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(result_nodes[0].text, "")
        self.assertEqual(result_nodes[2].text, "")


class TestSplitNodesLink(unittest.TestCase):
    CORRECT_LINK = "[alt text](www.imageurl.com)"
    def test_split_another_from_text_type(self):
        node = TextNode(self.CORRECT_LINK, TextType.BOLD)
        result_nodes = split_node_link(node)
        self.assertEqual(len(result_nodes), 1)
        self.assertEqual(node, result_nodes[0])

    def test_nothing_to_split(self):
        node = TextNode("some", TextType.TEXT)
        result_nodes = split_node_link(node)
        self.assertEqual(len(result_nodes), 1)
        self.assertEqual(node, result_nodes[0])

    def test_split_correct_link(self):
        node = TextNode(f"some{self.CORRECT_LINK}some1", TextType.TEXT)
        result_nodes = split_node_link(node)
        self.assertEqual(len(result_nodes), 3)
        self.assertIs(result_nodes[0].text_type, TextType.TEXT)
        self.assertIs(result_nodes[1].text_type, TextType.LINK)
        self.assertIs(result_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(result_nodes[0].text, "some")
        self.assertEqual(result_nodes[2].text, "some1")

    def test_split_correct_link_but_nothing_before_and_after(self):
        node = TextNode("some[some alt](www.imageurl.com)some1", TextType.TEXT)
        result_nodes = split_node_link(node)
        self.assertEqual(len(result_nodes), 3)
        self.assertIs(result_nodes[0].text_type, TextType.TEXT)
        self.assertIs(result_nodes[1].text_type, TextType.LINK)
        self.assertIs(result_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(result_nodes[0].text, "some")
        self.assertEqual(result_nodes[2].text, "some1")
        self.assertEqual(result_nodes[1].text, "some alt")
        self.assertEqual(result_nodes[1].url, "www.imageurl.com")


class TestSplitNodeWithDelimiter(unittest.TestCase):
    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        parts = split_node_with_delimiters(node, "**", TextType.TEXT)
        self.assertEqual(len(parts), 1)
        self.assertIs(parts[0].text, "")

    def test_extract_from_another_text_type(self):
        node = TextNode("some **hello** text", TextType.BOLD)
        parts = split_node_with_delimiters(node, "**", TextType.BOLD)
        self.assertEqual(len(parts), 1)
        self.assertIs(parts[0], node)

    def test_no_closing_delimiter_found(self):
        node = TextNode("some **hello text", TextType.TEXT)
        self.assertRaises(NoSecondDelimiterError ,split_node_with_delimiters, node, "**", TextType.TEXT)
        node = TextNode("some __hello text", TextType.TEXT)
        self.assertRaises(NoSecondDelimiterError ,split_node_with_delimiters, node, "__", TextType.TEXT)

    def test_correct_text(self):
        node = TextNode("some **hello** text", TextType.TEXT)
        parts = split_node_with_delimiters(node, "**", TextType.BOLD)
        self.assertEqual(len(parts), 3)
        text, bold, text2 = parts

        self.assertIs(text.text_type, TextType.TEXT)
        self.assertIs(text2.text_type, TextType.TEXT)
        self.assertIs(bold.text_type, TextType.BOLD)
        self.assertEqual(text.text, "some ")
        self.assertEqual(text2.text, " text")
        self.assertEqual(bold.text, "hello")

if __name__ == "__main__":
    unittest.main()
