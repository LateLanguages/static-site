from __future__ import annotations 

class HTMLNode:
    def __init__(
        self,
        tag: str|None =None,
        value: str|None =None,
        children: list[HTMLNode]|None =None,
        props: dict[str, str]|None =None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None or len(self.props) == 0:
            return ""
        c = ""
        for (key, value) in self.props.items():
            c += f" {key}=\"{value}\""
        return c

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str|None,
        value: str|None,
        props: dict[str, str]|None =None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("No value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str|None,
        children: list[HTMLNode]|None,
        props: dict[str, str]|None =None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("No tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("No children")
        c = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            c += child.to_html()
        return c + f"</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
