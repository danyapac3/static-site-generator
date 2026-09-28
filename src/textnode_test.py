import unittest

from textnode import (
    NoClosingDelimiterError,
    TextNode,
    TextType,
    split_node_with_delimiter,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("this is link node", TextType.LINK, "www.follow-me.com")
        node2 = TextNode("this is link node", TextType.LINK)
        self.assertNotEqual(node, node2)

        node = TextNode("this is another link node", TextType.LINK)
        node2 = TextNode("this is link node", TextType.LINK)
        self.assertNotEqual(node, node2)

        node = TextNode("this is link node", TextType.BOLD)
        node2 = TextNode("this is link node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_default_url_none(self):
        node = TextNode("this is link node", TextType.LINK)
        self.assertIsNone(node.url)

    def test_expected_repr(self):
        node = TextNode("some", TextType.ITALIC)
        self.assertEqual(node.__repr__(), "TextNode(some, italic, None)")

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_converts_text(self):
        node = TextNode("this is link node", TextType.TEXT)
        htmlnode = text_node_to_html_node(node)

        self.assertEqual(htmlnode.tag, None)
        self.assertEqual(htmlnode.value, node.text)
        self.assertIsNone(htmlnode.props)

    def test_converts_simple_tags(self):
        node = TextNode("this is link node", TextType.BOLD)
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, "b")
        self.assertEqual(htmlnode.value, "this is link node")
        self.assertIsNone(htmlnode.props)

        node = TextNode("this is link node", TextType.ITALIC)
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, "i")

        node = TextNode("this is link node", TextType.CODE)
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, "code")

    def test_converts_image(self):
        node = TextNode("example image", TextType.IMAGE, "https://example.com/img.png")
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, "img")
        self.assertEqual(htmlnode.value, "")
        if htmlnode.props is None:
            self.fail("Somewhat props is not passed correctly")
        self.assertDictEqual(htmlnode.props, {"src": "https://example.com/img.png", "alt": "example image"})

    def test_converts_link(self):
        node = TextNode("this is a link node", TextType.LINK, "https://example.com")
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, "a")
        self.assertEqual(htmlnode.value, "this is a link node")
        if htmlnode.props is None:
            self.fail("Somewhat props is not passed correctly")
        self.assertDictEqual(htmlnode.props, {"href": "https://example.com"})


class TestSplitNodeWithDelimiter(unittest.TestCase):
    def test_no_delimiter_found(self):
        node = TextNode("some text", TextType.TEXT)
        parts = split_node_with_delimiter(node, "**", TextType.TEXT)
        self.assertEqual(len(parts), 1)
        self.assertIs(parts[0], node)

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        parts = split_node_with_delimiter(node, "**", TextType.TEXT)
        self.assertEqual(len(parts), 1)
        self.assertIs(parts[0].text, "")

    def test_another_text_type(self):
        node = TextNode("some **hello** text", TextType.BOLD)
        parts = split_node_with_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(len(parts), 1)
        self.assertIs(parts[0], node)

    def test_no_closing_delimiter_found(self):
        node = TextNode("some **hello text", TextType.TEXT)
        self.assertRaises(NoClosingDelimiterError, split_node_with_delimiter, node, "**", TextType.BOLD)

    def test_two_delimiters(self):
        node = TextNode("some **hello** text", TextType.TEXT)
        parts = split_node_with_delimiter(node, "**", TextType.BOLD)
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
