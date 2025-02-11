import unittest

from main import *
from delimiter import *

class split_delimiter(unittest.TestCase):
    def test_single_node(self):
        node = TextNode("what about **bold** words?", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter(node), [TextNode("what about ", TextType.TEXT, None), TextNode("bold", TextType.BOLD, None), TextNode(" words?", TextType.TEXT, None)])
    
    def test_list_of_nodes(self):
        node_list = [
            TextNode("what about **bold** words?", TextType.TEXT),
            TextNode("what about *italic* words?", TextType.TEXT),
            TextNode("what about `code` words?", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(node_list), [
            TextNode("what about ", TextType.TEXT, None), TextNode("bold", TextType.BOLD, None), TextNode(" words?", TextType.TEXT, None),
            TextNode("what about ", TextType.TEXT, None), TextNode("italic", TextType.ITALIC, None), TextNode(" words?", TextType.TEXT, None),
            TextNode("what about ", TextType.TEXT, None), TextNode("code", TextType.CODE, None), TextNode(" words?", TextType.TEXT, None)
        ])
    
    def test_delimiter_list(self):
        node_list = [
            TextNode("what about **bold** words?", TextType.TEXT),
            TextNode("what about *italic* words?", TextType.TEXT),
            TextNode("what about `code` words?", TextType.TEXT),
            TextNode("imjust a regular old text node", TextType.TEXT)
        ]
        self.assertEqual(identify_delimiter(node_list), ["**", "*", "`", ""])

    def test_non_text_nodes(self):
        node = TextNode("im so bold right now", TextType.BOLD)
        self.assertEqual(split_nodes_delimiter(node), TextNode("im so bold right now", TextType.BOLD, None))

    def test_starts_with_inline_element(self):
        node = TextNode("**oh my god im bolding** so hard rn", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter(node), [TextNode("", TextType.TEXT, None), TextNode("oh my god im bolding", TextType.BOLD, None), TextNode(" so hard rn", TextType.TEXT, None)])

    def test_multiple_inline_elements(self):
        node = TextNode("im bold **here** and **there**", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter(node), [
            TextNode("im bold ", TextType.TEXT, None), 
            TextNode("here", TextType.BOLD, None), 
            TextNode(" and ", TextType.TEXT, None), 
            TextNode("there", TextType.BOLD, None), 
            TextNode("", TextType.TEXT, None)
            ])
        
    def test_two_different_elements(self):
        node = TextNode("im **bold** here and im *italic* there", TextType.TEXT)
        test = split_nodes_delimiter(node)
        self.assertEqual(split_nodes_delimiter(test), [
            TextNode("im ", TextType.TEXT, None), 
            TextNode("bold", TextType.BOLD, None), 
            TextNode(" here and im ", TextType.TEXT, None), 
            TextNode("italic", TextType.ITALIC, None), 
            TextNode(" there", TextType.TEXT, None)

        ])

class regex_extract_images_links(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT, None)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            #TextNode("", TextType.TEXT, None)
        ])

    def test_split_nodes_image(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT, None)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            #TextNode("", TextType.TEXT, None)
        ])

class TextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            #TextNode("", TextType.TEXT)
        ])
        
if __name__ == "__main__":
    unittest.main()