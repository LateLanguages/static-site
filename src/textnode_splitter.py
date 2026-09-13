from textnode import TextNode, TextType
import re

def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        s = node.text.split(delimiter)
        if len(s) % 2 == 0:
            raise Exception(f"Missing closing delimiter '{delimiter}'! ({node.text})")
        for j in range(len(s)):
            if s[j] == '':
                continue
            elif j % 2 == 0:
                new_nodes.append(TextNode(s[j], TextType.PLAIN))
            else:
                new_nodes.append(TextNode(s[j], text_type))

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: TextNode = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        r = extract_markdown_images(node.text)
        if len(r) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for (image_alt, image_link) in r:
            sections = remaining_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(text=sections[0], text_type=TextType.PLAIN))
            new_nodes.append(TextNode(text=image_alt, text_type=TextType.IMAGE, url=image_link))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(text=remaining_text, text_type=TextType.PLAIN))
        return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: TextNode = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        r = extract_markdown_links(node.text)
        if len(r) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for (link_text, link) in r:
            sections = remaining_text.split(f"[{link_text}]({link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(text=sections[0], text_type=TextType.PLAIN))
            new_nodes.append(TextNode(text=link_text, text_type=TextType.LINK, url=link))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(text=remaining_text, text_type=TextType.PLAIN))
        return new_nodes

def extract_markdown_images(text: str) -> list[str]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[str]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
