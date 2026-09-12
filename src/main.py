from textnode import TextNode, TextType

def main():
    t = TextNode("TeXt", TextType.TEXT_PLAIN, "https://http.cat/404")
    print(t)

main()