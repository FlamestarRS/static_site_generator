import unittest

from main import *

class TestTextToHTML(unittest.TestCase):
    def test_TEXT(self):
        node = TextNode("normal text", TextType.TEXT, "www.normaltext.com")
        self.assertEqual(text_node_to_html_node(node).to_html(),"normal text")
    
    def test_BOLD(self):
        node = TextNode("bold text", TextType.BOLD, "www.boldtext.com")
        self.assertEqual(text_node_to_html_node(node).to_html(),"<b>bold text</b>")

    def test_ITALIC(self):
        node = TextNode("italic text", TextType.ITALIC, "www.italictext.com")
        self.assertEqual(text_node_to_html_node(node).to_html(),"<i>italic text</i>")

    def test_CODE(self):
        node = TextNode("code text", TextType.CODE, "www.codetext.com")
        self.assertEqual(text_node_to_html_node(node).to_html(),"<code>code text</code>")

    def test_LINK(self):
        node = TextNode("link text", TextType.LINK, "www.linktext.com")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<a href="www.linktext.com">link text</a>')

    def test_IMAGE(self):
        node = TextNode("image text", TextType.IMAGE, "www.imagetext.com")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<img src="www.imagetext.com" alt="image text"></img>')
    
    def test_ERROR(self):
        node = TextNode("crazy style", "crazy", "www.crazystyle.com")
        self.assertRaises(ValueError, lambda: text_node_to_html_node(node))
        # lambda is used to call the function at the right time
        # assertRaises requires a callable as the 2nd argument
        # without lambda, function is called too early, and error is not properly caught



if __name__ == "__main__":
    unittest.main()