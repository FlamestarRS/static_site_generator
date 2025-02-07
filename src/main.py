from textnode import *
from htmlnode import *


def text_node_to_html_node(text_node):  # converts TextNodes to HTMLNodes for tagging
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise ValueError("invalid text type: {text_node.text_type}")
        


def main():
    test = TextNode("idk", TextType.TEXT, "https://www.boot.dev")
    print(test)

    print(text_node_to_html_node(test))

if __name__ == "__main__":
    main()