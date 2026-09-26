import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_none_value_to_html(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_none_tag_to_html(self):
        node = LeafNode(None, "text you'd like to read")
        self.assertEqual(node.to_html(), "text you'd like to read")

    def test_to_html(self):
        node = LeafNode("p", "some text")
        self.assertEqual(node.to_html(), "<p>some text</p>")

    def test_to_html_with_props(self):
        node = LeafNode("p", "some text", {"color": "red", "title": "just hover me and you will see..."})
        self.assertEqual(node.to_html(), '<p color="red" title="just hover me and you will see...">some text</p>')

    def test_repr(self):
       node = LeafNode("p", "some", {"color": "red"})
       self.assertEqual(node.__repr__(), "LeafNode(p, some, {'color': 'red'})")
