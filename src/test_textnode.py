import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


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
        self.assertDictEqual(htmlnode.props, {"src": "https://example.com/img.png", "alt": "example image"})

    def test_converts_link(self):
        node = TextNode("this is a link node", TextType.LINK, "https://example.com")
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, "a")
        self.assertEqual(htmlnode.value, "this is a link node")
        self.assertDictEqual(htmlnode.props, {"href": "https://example.com"})

if __name__ == "__main__":
    unittest.main()
