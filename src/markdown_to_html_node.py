from blocktype import BlockType, block_to_block_type
from htmlnode import HtmlNode
from markdown_to_blocks import markdown_to_blocks
from parentnode import ParentNode
from src.leafnode import LeafNode
from text_to_text_nodes import text_to_text_nodes
from textnode import TextNode, TextType, text_node_to_html_node


def create_heading(block: str) -> HtmlNode:
    hashes_count = block[0:6].count("#")
    text_nodes = text_to_text_nodes(block[hashes_count + 1:])
    children = [text_node_to_html_node(text_node) for text_node in text_nodes]
    result = ParentNode(f"h{hashes_count}", children)
    return result

def create_code_block(block: str) -> HtmlNode:
    result = ParentNode("pre", [LeafNode("code", value=block)])
    return result

def create_paragraph(block: str) -> HtmlNode:
    text_nodes = text_to_text_nodes(block)
    children = [text_node_to_html_node(text_node) for text_node in text_nodes]
    result = ParentNode("p", children)
    return result

def create_quote(block: str) -> HtmlNode:
    lines = [line.removeprefix('>') for line in block.split("\n")]
    children = []
    for line_index in range(len(lines)):
        line = lines[line_index]
        text_nodes = text_to_text_nodes(line)
        if line_index != len(lines) - 1:
            text_nodes.append(TextNode("\n", TextType.TEXT))
        children.extend([text_node_to_html_node(text_node) for text_node in text_nodes])
    result = ParentNode("pre", [ParentNode("blockquote", children)])
    return result

def create_ordered_list(block: str) -> HtmlNode:
    lines = [line.lstrip('0123456789').removeprefix(". ") for line in block.split("\n")]
    children = []
    for line in lines:
        text_nodes = text_to_text_nodes(line);
        children.append(ParentNode("li", [text_node_to_html_node(node) for node in text_nodes]))
    result = ParentNode("ol", children)
    return result

def create_unordered_list(block: str) -> HtmlNode:
    lines = [line.removeprefix("- ") for line in block.split("\n")]
    children = []
    for line in lines:
        text_nodes = text_to_text_nodes(line);
        children.append(ParentNode("li", [text_node_to_html_node(node) for node in text_nodes]))
    result = ParentNode("ul", children)
    return result

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)

    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                children.append(create_heading(block))
            case BlockType.CODE:
                children.append(create_code_block(block))
            case BlockType.QUOTE:
                children.append(create_quote(block))
            case BlockType.ORDERED_LIST:
                children.append(create_ordered_list(block))
            case BlockType.UNORDERED_LIST:
                children.append(create_unordered_list(block))
            case _:
                children.append(create_paragraph(block))
    return ParentNode("div", children)
