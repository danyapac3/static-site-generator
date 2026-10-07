import unittest

from split_nodes import (
    split_nodes_image,
    split_nodes_link,
    split_nodes_delimiters,
)
from textnode import TextNode, TextType


class TestSplitNodesImage(unittest.TestCase):
    def test_splits_image(self):
        node = TextNode("before ![text](www.i.com) after", text_type=TextType.TEXT)
        parts = split_nodes_image([node])
        self.assertEqual(
            parts,
            [
                TextNode("before ", text_type=TextType.TEXT),
                TextNode("text", text_type=TextType.IMAGE, url="www.i.com"),
                TextNode(" after", text_type=TextType.TEXT),
            ])

        node = TextNode("![alt text](www.imageurl.com)", text_type=TextType.TEXT)
        parts = split_nodes_image([node])
        self.assertEqual(
            parts,
            [
                TextNode("alt text", text_type=TextType.IMAGE, url="www.imageurl.com"),
            ])

    def test_splits_three_images(self):
        node = TextNode("before ![text](www.i.com)![text2](www.i.com) between ![text3](www.i.com)after", text_type=TextType.TEXT)
        parts = split_nodes_image([node])
        self.assertEqual(
            parts,
            [
                TextNode("before ", text_type=TextType.TEXT),
                TextNode("text", text_type=TextType.IMAGE, url="www.i.com"),
                TextNode("text2", text_type=TextType.IMAGE, url="www.i.com"),
                TextNode(" between ", text_type=TextType.TEXT),
                TextNode("text3", text_type=TextType.IMAGE, url="www.i.com"),
                TextNode("after", text_type=TextType.TEXT),
            ])
    
    def test_splits_three_nodes(self):
        node = TextNode("before![text](www.i.com)between![text1](www.i.com)", text_type=TextType.TEXT)
        node2 = TextNode("![text3](www.i.com)![text4](www.i.com) between ![text5](www.i.com)", text_type=TextType.TEXT)
        node3 = TextNode("![text6](www.i.com) after", text_type=TextType.TEXT)
        parts = split_nodes_image([node, node2, node3])
        self.assertEqual(
            parts,
            [
                TextNode("before", text_type=TextType.TEXT),
                TextNode("text", text_type=TextType.IMAGE, url="www.i.com"),
                TextNode("between", text_type=TextType.TEXT),
                TextNode("text1", text_type=TextType.IMAGE, url="www.i.com"),
                TextNode("text3", text_type=TextType.IMAGE, url="www.i.com"),
                TextNode("text4", text_type=TextType.IMAGE, url="www.i.com"),
                TextNode(" between ", text_type=TextType.TEXT),
                TextNode("text5", text_type=TextType.IMAGE, url="www.i.com"),
                TextNode("text6", text_type=TextType.IMAGE, url="www.i.com"),
                TextNode(" after", text_type=TextType.TEXT),
            ])
    
    def test_text_type_is_not_text(self):
        node = TextNode("![text](www.i.com)", text_type=TextType.BOLD)
        parts = split_nodes_image([node])
        self.assertEqual(parts, [node])




class TestSplitNodesLink(unittest.TestCase):
    def test_splits_link(self):
        node = TextNode("before [text](www.i.com) after", text_type=TextType.TEXT)
        parts = split_nodes_link([node])
        self.assertEqual(
            parts,
            [
                TextNode("before ", text_type=TextType.TEXT),
                TextNode("text", text_type=TextType.LINK, url="www.i.com"),
                TextNode(" after", text_type=TextType.TEXT),
            ])

        node = TextNode("[text](www.imageurl.com)", text_type=TextType.TEXT)
        parts = split_nodes_link([node])
        self.assertEqual(
            parts,
            [
                TextNode("text", text_type=TextType.LINK, url="www.imageurl.com")
            ])

    def test_splits_three_links(self):
        node = TextNode("before [text](www.i.com)[text2](www.i.com) between [text3](www.i.com)after", text_type=TextType.TEXT)
        parts = split_nodes_link([node])
        self.assertEqual(
            parts,
            [
                TextNode("before ", text_type=TextType.TEXT),
                TextNode("text", text_type=TextType.LINK, url="www.i.com"),
                TextNode("text2", text_type=TextType.LINK, url="www.i.com"),
                TextNode(" between ", text_type=TextType.TEXT),
                TextNode("text3", text_type=TextType.LINK, url="www.i.com"),
                TextNode("after", text_type=TextType.TEXT),
            ])
    
    def test_splits_three_nodes(self):
        node = TextNode("before[text](www.i.com)between[text1](www.i.com)", text_type=TextType.TEXT)
        node2 = TextNode("[text3](www.i.com)[text4](www.i.com) between [text5](www.i.com)", text_type=TextType.TEXT)
        node3 = TextNode("[text6](www.i.com) after", text_type=TextType.TEXT)
        parts = split_nodes_link([node, node2, node3])
        self.assertEqual(
            parts,
            [
                TextNode("before", text_type=TextType.TEXT),
                TextNode("text", text_type=TextType.LINK, url="www.i.com"),
                TextNode("between", text_type=TextType.TEXT),
                TextNode("text1", text_type=TextType.LINK, url="www.i.com"),
                TextNode("text3", text_type=TextType.LINK, url="www.i.com"),
                TextNode("text4", text_type=TextType.LINK, url="www.i.com"),
                TextNode(" between ", text_type=TextType.TEXT),
                TextNode("text5", text_type=TextType.LINK, url="www.i.com"),
                TextNode("text6", text_type=TextType.LINK, url="www.i.com"),
                TextNode(" after", text_type=TextType.TEXT),
            ])
    
    def test_doesnt_extract_images(self):
        node = TextNode("some![text](www.i.com)some", text_type=TextType.TEXT)
        parts = split_nodes_link([node])
        self.assertEqual(
            parts,
            [
                TextNode("some![text](www.i.com)some", text_type=TextType.TEXT),
            ])
    
    def test_text_type_is_not_text(self):
        node = TextNode("![text](www.i.com)", text_type=TextType.BOLD)
        parts = split_nodes_image([node])
        self.assertEqual(parts, [node])


class TestSplitNodesDelimiters(unittest.TestCase):
    def test_splits_one_node_with_two_delimiters(self):
        node = TextNode("before**between**after", TextType.TEXT)
        parts = split_nodes_delimiters([node], "**", TextType.BOLD)
        self.assertEqual(parts, [
            TextNode("before", TextType.TEXT),
            TextNode("between", TextType.BOLD),
            TextNode("after", TextType.TEXT),
        ])
    
    def test_splits_node_with_nothing_before_and_after(self):
        node = TextNode("**between**", TextType.TEXT)
        parts = split_nodes_delimiters([node], "**", TextType.BOLD)
        self.assertEqual(parts, [
            TextNode("between", TextType.BOLD),
        ])
    
    def test_splits_node_with_several_occurrences(self):
        node = TextNode("**bold1**between**bold2** **bold3**", TextType.TEXT)
        parts = split_nodes_delimiters([node], "**", TextType.BOLD)
        self.assertEqual(parts, [
            TextNode("bold1", TextType.BOLD),
            TextNode("between", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("bold3", TextType.BOLD),
        ])
    
    def test_splits_several_nodes(self):
        node = TextNode("**bold1**", TextType.TEXT)
        node1 = TextNode("**bold2**", TextType.TEXT)
        node2 = TextNode("**bold3**", TextType.TEXT)
        parts = split_nodes_delimiters([node, node1, node2], "**", TextType.BOLD)
        self.assertEqual(parts, [
            TextNode("bold1", TextType.BOLD),
            TextNode("bold2", TextType.BOLD),
            TextNode("bold3", TextType.BOLD),
        ])
    
    def test_nothing_happenes_when_no_closing_delimiter_occured(self):
        node = TextNode("**bold1", TextType.TEXT)
        parts = split_nodes_delimiters([node], "**", TextType.BOLD)
        self.assertEqual(parts, [
            TextNode("**bold1", TextType.TEXT),
        ])
        
        node = TextNode("**bold1****bold2", TextType.TEXT)
        parts = split_nodes_delimiters([node], "**", TextType.BOLD)
        self.assertEqual(parts, [
            TextNode("bold1", TextType.BOLD),
            TextNode("**bold2", TextType.TEXT),
        ])
    
    def test_nothing_happenes_when_text_type_is_not_text(self):
        node = TextNode("**bold1**", TextType.LINK)
        parts = split_nodes_delimiters([node], "**", TextType.BOLD)
        self.assertEqual(parts, [node])

    def test_works_with_different_delimiters(self):
        node = TextNode("**bold**", TextType.TEXT)
        parts = split_nodes_delimiters([node], "**", TextType.BOLD)
        self.assertEqual(parts, [
            TextNode("bold", TextType.BOLD),
        ])

        node = TextNode("_italic_", TextType.TEXT)
        parts = split_nodes_delimiters([node], "_", TextType.ITALIC)
        self.assertEqual(parts, [
            TextNode("italic", TextType.ITALIC),
        ])

        node = TextNode("`code`", TextType.TEXT)
        parts = split_nodes_delimiters([node], "`", TextType.CODE)
        self.assertEqual(parts, [
            TextNode("code", TextType.CODE),
        ])

        node = TextNode("** **red** **", TextType.TEXT)
        parts = split_nodes_delimiters([node], "** **", TextType.BOLD)
        self.assertEqual(parts, [
            TextNode("red", TextType.BOLD),
        ])


if __name__ == "__main__":
    unittest.main()
