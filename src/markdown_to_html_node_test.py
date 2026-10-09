import textwrap
import unittest

from markdown_to_html_node import create_code_block, markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        markdown = textwrap.dedent(
            """
            hello world _hello_ **hello** ![penguin](www.image.penguin.com)!
            """
        )

        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><p>hello world <i>hello</i> <b>hello</b> <img alt=\"penguin\" src=\"www.image.penguin.com\"></img>!</p></div>")

    def test_headings(self):
        markdown = textwrap.dedent(
            """
            # title1

            ## title2

            ### title3

            #### title4

            ##### title5

            ###### title6
            """
        )

        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><h1>title1</h1><h2>title2</h2><h3>title3</h3><h4>title4</h4><h5>title5</h5><h6>title6</h6></div>")

    def test_code(self):
        markdown = textwrap.dedent(
            """
            ```
            # expected output _**i love markdown**_
            s = "**i love markdown**")
            print(f"_{s}_")
            ```
            """
        ).strip()

        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), f"<div><pre><code>{markdown}</code></pre></div>")

    def test_quote(self):
        markdown = textwrap.dedent(
            """
            >hello1
            >hello2
            >hello3
            >hello4
            """
        )

        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><pre><blockquote>hello1\nhello2\nhello3\nhello4</blockquote></pre></div>")

        markdown = textwrap.dedent(
            """
            > **hello1**
            >  hello2
            >   hello3
            >hello4
            """
        )
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><pre><blockquote> <b>hello1</b>\n  hello2\n   hello3\nhello4</blockquote></pre></div>")

    def test_ordered_list(self):
        markdown = textwrap.dedent(
            """
            1. hello1
            2. hello2
            3. hello3
            4. hello4
            """
        )

        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><ol><li>hello1</li><li>hello2</li><li>hello3</li><li>hello4</li></ol></div>")

        markdown = textwrap.dedent(
            """
            1.  hello1
            """
        )

        node = markdown_to_html_node(markdown)
        self.assertIn(" hello1", node.to_html())

        markdown = textwrap.dedent(
            """
            1. hello1
            2. hello2
            2. hello3
            4. hello4
            """
        )

        node = markdown_to_html_node(markdown)
        self.assertIn("<p>", node.to_html())
        self.assertIn("hello1", node.to_html())
        self.assertIn("4. hello4", node.to_html())

    def test_unordered_list(self):
        markdown = textwrap.dedent(
            """
            - hello1
            - hello2
            - hello3
            """
        )

        node = markdown_to_html_node(markdown)
        self.assertEqual(node.to_html(), "<div><ul><li>hello1</li><li>hello2</li><li>hello3</li></ul></div>")

        markdown = textwrap.dedent(
            " -  hello1"
        )

        node = markdown_to_html_node(markdown)
        self.assertIn(" hello1", node.to_html())

        markdown = textwrap.dedent(
            """
            - hello1
            -hello2
            - hello3
            """
        )

        node = markdown_to_html_node(markdown)
        self.assertIn("<p>", node.to_html())
        self.assertIn("hello1", node.to_html())
        self.assertIn("- hello3", node.to_html())

if __name__ == "__main__":
    unittest.main()
