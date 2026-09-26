from htmlnode import HtmlNode


class ParentNode(HtmlNode):
    def __init__(
        self,
        tag: str | None,
        children: list | None,
        props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag, children=children, props=props)

    # TODO: Maybe add pretty print
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError('"tag" property must be presented for ParentNode')
        if self.children is None:
            raise ValueError('"children" property must be presented for ParentNode')

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"


    def __repr__(self):
       return f"LeafNode({self.tag}, {self.value}, {self.props})"
