from textnode import *
from htmlnode import *


      


def main():
    test = TextNode("idk", TextType.TEXT, "https://www.boot.dev")
    print(test)

    print(text_node_to_html_node(test))

if __name__ == "__main__":
    main()