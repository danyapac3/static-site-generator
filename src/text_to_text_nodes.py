from split_nodes import split_nodes_image, split_nodes_link, split_nodes_delimiters
from textnode import TextNode, TextType

split_funcs = [
    lambda nodes : split_nodes_with_delimiter(nodes, "**", TextType.BOLD),
    lambda nodes : split_nodes_with_delimiter(nodes, "_", TextType.ITALIC),
    lambda nodes : split_nodes_with_delimiter(nodes, "`", TextType.CODE),
    split_nodes_image,
    split_nodes_link,
]

def text_to_text_nodes(text: str) -> list[TextNode]:
    result = [TextNode(text, TextType.TEXT)]
    for split_func in split_funcs:
        result = split_func(processed_nodes)
    return result

    
