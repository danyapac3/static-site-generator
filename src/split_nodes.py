import re

from textnode import TextNode, TextType

image_pattern = r"(\!\[.*?\]\(.*?\))"
link_pattern = r"((?<!!)\[.*?\]\(.*?\))"

def extract_image_node(node: TextNode) -> list[TextNode]:
    if node.text_type is not TextType.TEXT:
        return [node]

    parts = re.split(image_pattern, node.text, maxsplit=1)
    if len(parts) == 1:
        return [node]

    m = re.search(r"\[(?P<alt>.*?)\]\((?P<src>.*?)\)", parts[1])
    image = TextNode("", TextType.IMAGE, "")
    if m:
        alt = m.group("alt")
        src = m.group("src")
        image.text = alt
        image.url = src

    return [
        TextNode(parts[0], TextType.TEXT),
        image,
        TextNode(parts[2], TextType.TEXT),
    ]


def extract_link_node(node: TextNode) -> list[TextNode]:
    if node.text_type is not TextType.TEXT:
        return [node]

    parts = re.split(link_pattern, node.text, maxsplit=1)
    if len(parts) == 1:
        return [node]

    m = re.search(r"\[(?P<alt>.*?)\]\((?P<href>.*?)\)", parts[1])
    link = TextNode("", TextType.LINK, "")
    if m:
        alt = m.group("alt")
        href = m.group("href")
        link.text = alt
        link.url = href

    return [
        TextNode(parts[0], TextType.TEXT),
        link,
        TextNode(parts[2], TextType.TEXT),
    ]

class NoSecondDelimiterError(Exception):
    "There must be 2 delimiters"

def extract_text_node_with_delimiter(node: TextNode, delimiter: str, text_type: TextType) -> list[TextNode]:
    if node.text_type is not TextType.TEXT:
        return [node]

    parts = node.text.split(delimiter, maxsplit=2)

    if len(parts) == 1:
        return [node]

    if len(parts) == 2:
        raise NoSecondDelimiterError

    return [
        TextNode(parts[0], TextType.TEXT),
        TextNode(parts[1], text_type),
        TextNode(parts[2], TextType.TEXT)
    ]
