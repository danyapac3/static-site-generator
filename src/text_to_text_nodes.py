from split_nodes import split_nodes_delimiters, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

split_funcs = [
    lambda nodes : split_nodes_delimiters(nodes, "**", TextType.BOLD),
    lambda nodes : split_nodes_delimiters(nodes, "_", TextType.ITALIC),
    lambda nodes : split_nodes_delimiters(nodes, "`", TextType.CODE),
    split_nodes_image,
    split_nodes_link,
]

def text_to_text_nodes(text: str) -> list[TextNode]:
    result = [TextNode(text, TextType.TEXT)]
    for split_func in split_funcs:
        result = split_func(result)
    return result
