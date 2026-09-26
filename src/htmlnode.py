class WrongParamsError(Exception):
    'Must be presented one of "children" or "value" params'

class HtmlNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HtmlNode"] | None = None,
        props: dict[str, str] | None = None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

        if (value is not None) and (children is not None):
            raise WrongParamsError()

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        result = ""
        for name, value in sorted(self.props.items()):
            result += f" {name}=\"{value}\""
        return result

    def __repr__(self):
        return f"""HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"""


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
