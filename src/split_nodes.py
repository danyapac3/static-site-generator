import re

from textnode import TextNode, TextType

image_pattern = r"(?P<before>.*?)!\[(?P<alt>.*?)\]\((?P<src>.*?)\)(?P<after>.*)"
link_pattern = r"(?P<before>.*?)(?<!\!)\[(?P<alt>.*?)\]\((?P<src>.*?)\)(?P<after>.*)"
delimiter_pattern_start = r"(?P<before>.*?)"
delimiter_pattern_middle = r"(?P<between>.*?)"
delimiter_pattern_end = r"(?P<after>.*)"

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text == "":
            return []

        parts = []
        current_node: TextNode | None = node

        while current_node is not None:
            m = re.search(image_pattern, current_node.text)
            if not m:
                break

            text_before, text_after = m.group("before"), m.group("after")
            alt, src = m.group("alt"), m.group("src")

            if text_before:
                parts.append(TextNode(text_before, TextType.TEXT))
            parts.append(TextNode(alt,TextType.IMAGE, src))
            if text_after:
                current_node = TextNode(text_after, TextType.TEXT)
            else:
                current_node = None

        if current_node:
            parts.append(current_node)

        new_nodes.extend(parts)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text == "":
            return []

        parts = []
        current_node: TextNode | None = node

        while current_node is not None:
            m = re.search(link_pattern, current_node.text)
            if not m:
                break

            text_before, text_after = m.group("before"), m.group("after")
            alt, src = m.group("alt"), m.group("src")

            if text_before:
                parts.append(TextNode(text_before, TextType.TEXT))
            parts.append(TextNode(alt,TextType.LINK, src))
            if text_after:
                current_node = TextNode(text_after, TextType.TEXT)
            else:
                current_node = None

        if current_node:
            parts.append(current_node)

        new_nodes.extend(parts)
    return new_nodes

def split_nodes_delimiters(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text == "":
            return []

        parts = []
        current_node: TextNode | None = node

        escaped_delimiter = re.escape(delimiter)
        delimiter_pattern = (
            delimiter_pattern_start +
            escaped_delimiter +
            delimiter_pattern_middle +
            escaped_delimiter +
            delimiter_pattern_end
        )


        while current_node is not None:
            m = re.search(delimiter_pattern, current_node.text)
            if not m:
                break

            text_before = m.group("before")
            text_between = m.group("between")
            text_after = m.group("after")

            if text_before:
                parts.append(TextNode(text_before, TextType.TEXT))
            parts.append(TextNode(text_between, text_type))
            if text_after:
                current_node = TextNode(text_after, TextType.TEXT)
            else:
                current_node = None

        if current_node:
            parts.append(current_node)

        new_nodes.extend(parts)
    return new_nodes

