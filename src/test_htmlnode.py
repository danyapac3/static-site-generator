import unittest

from htmlnode import HtmlNode, WrongParamsError


class TestHtmlNode(unittest.TestCase):
    def test_wrong_params(self):
        caught = False
        try:
            HtmlNode(value="garbage value", children=[HtmlNode(value="garbage value")])
        except WrongParamsError:
            caught = True
        self.assertTrue(caught)

    def test_correct_params(self):
        caught = False
        try:
            HtmlNode(value="garbage value")
        except WrongParamsError:
            caught = True
        self.assertFalse(caught)

        caught = False
        try:
            HtmlNode(children=[HtmlNode(value="garbage value")])
        except WrongParamsError:
            caught = True
        self.assertFalse(caught)


    def test_props_to_html(self):
        node = HtmlNode("p", "some text", props = {"link": "www.example.com", "color": "red", "title": "click me"})
        self.assertEqual(node.props_to_html(), ' color="red" link="www.example.com" title="click me"')

        node = HtmlNode("p", "some text", props = {"link": "www.example.com"})
        self.assertEqual(node.props_to_html(), ' link="www.example.com"')

        node = HtmlNode("p", "some text")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HtmlNode("p", "value")
        self.assertEqual(node.__repr__(), "HtmlNode(p, value, None, None)")
        node = HtmlNode("p", children=[HtmlNode("em", "emphasized")])
        self.assertEqual(node.__repr__(), "HtmlNode(p, None, [HtmlNode(em, emphasized, None, None)], None)")
        node = HtmlNode("p", "value", props={"color": "red"})
        self.assertEqual(node.__repr__(), "HtmlNode(p, value, None, {'color': 'red'})")
