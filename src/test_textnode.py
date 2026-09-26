import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()
