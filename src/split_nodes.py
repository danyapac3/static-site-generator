import re

from textnode import TextNode, TextType

image_pattern = r"(\!\[.*?\]\(.*?\))"
link_pattern = r"((?<!!)\[.*?\]\(.*?\))"

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        parts = re.split(image_pattern, text, maxsplit=1)

        if len(parts) == 1:
            new_nodes.append(node)
            continue

        m = re.search(r"\[(?P<alt>.*?)\]\((?P<src>.*?)\)", parts[1])
        image = TextNode("", TextType.IMAGE, "")
        if m:
            alt = m.group("alt")
            src = m.group("src")
            image.text = alt
            image.url = src

        new_nodes.extend([
            TextNode(parts[0], TextType.TEXT),
            image,
            TextNode(parts[2], TextType.TEXT),
        ])

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text

        parts = re.split(link_pattern, text, maxsplit=1)

        if len(parts) == 1:
            new_nodes.append(node)
            continue

        m = re.search(r"\[(?P<alt>.*?)\]\((?P<href>.*?)\)", parts[1])
        link = TextNode("", TextType.LINK, "")
        if m:
            alt = m.group("alt")
            href = m.group("href")
            link.text = alt
            link.url = href

        new_nodes.extend([
            TextNode(parts[0], TextType.TEXT),
            link,
            TextNode(parts[2], TextType.TEXT),
        ])

    return new_nodes

class NoClosingDelimiterError(Exception):
    "There must be a closing delimiter"

class EmptyDelimiterError(Exception):
    "Delimiter can't be an empty string"

def split_node_with_delimiter(old_node: TextNode, delimiter: str, text_type: TextType) -> list[TextNode]:
    if delimiter == "":
        raise EmptyDelimiterError

    if old_node.text_type is not TextType.TEXT:
        return [old_node]

    text = old_node.text

    parts = text.split(delimiter, 2)

    if len(parts) <= 1:
        return [old_node]

    if len(parts) == 2:
        raise NoClosingDelimiterError

    return [
        TextNode(parts[0], TextType.TEXT),
        TextNode(parts[1], text_type),
        TextNode(parts[2], TextType.TEXT),
    ]


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        new_nodes.extend(split_node_with_delimiter(node, delimiter, text_type))
    return new_nodes
