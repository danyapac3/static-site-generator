from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

class WrongTextTypePropertyError:
    '"text_type" property must be instance of TextType class'

def text_node_to_html_node(textnode: TextNode) -> LeafNode:
    match textnode.text_type:
        case TextType.TEXT:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.ITALIC:
            return LeafNode("i", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            return LeafNode("a", textnode.text, {"href": textnode.url or ""})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": textnode.url or "", "alt": textnode.text})
        case _:
            raise WrongTextTypePropertyError


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
