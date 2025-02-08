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
        
        
if __name__ == "__main__":
    unittest.main()