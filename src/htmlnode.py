
from types import NotImplementedType


class WrongParametersError(Exception):
    "Both \"value\" and \"children\" parameters aren't passed"

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

        if (value is None) and (children is None):
            raise WrongParametersError()

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
