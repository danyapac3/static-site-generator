from htmlnode import HtmlNode


class LeafNode(HtmlNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if (self.value is None):
            raise ValueError("All leaf nodes must have value")
        if (self.tag is None):
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
       return f"LeafNode({self.tag}, {self.value}, {self.props})"
