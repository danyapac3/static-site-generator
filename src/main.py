from split_nodes import split_nodes_delimiters 
from textnode import TextNode, TextType


def main() -> None:
    my_link = TextNode("Just follow this link!", TextType.LINK, "www.example.com")
    print(my_link)
    nodes = split_nodes_delimiters([TextNode("**bold****bold1", text_type=TextType.TEXT)], "**", TextType.BOLD)
   
    print(end)

if __name__ == "__main__":
    main()
