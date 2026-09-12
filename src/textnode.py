from enum import Enum

class TextType(Enum):
    TEXT_PLAIN = "text_plain"
    TEXT_BOLD = "text_bold"
    TEXT_ITALIC = "text_italic"
    TEXT_CODE = "text_code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"