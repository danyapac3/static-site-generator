from textnode import TextNode, TextType


def main() -> None:
    my_link = TextNode("Just follow this link!", TextType.LINK, "www.example.com")
    print(my_link)

if __name__ == "__main__":
    main()
