import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        htmlnode = HTMLNode("tag", "value", "children", "props")
        self.assertEqual(repr(htmlnode), "HTMLNode(tag, value, children, props)")
        
    def test_props_to_html(self):
        dict = {
            "Link":"Ocarina",
            "Zelda":"Letter",
            "Gerudo":"Fortress",
            "Ganon":"Castle"
        }
        htmlnode = HTMLNode(None, None, None, dict)
        self.assertEqual(htmlnode.props_to_html(), ' Link="Ocarina" Zelda="Letter" Gerudo="Fortress" Ganon="Castle"')

    def test_to_html(self):
        htmlnode = HTMLNode()
        self.assertRaises(NotImplementedError, htmlnode.to_html)

class TestLeafNode(unittest.TestCase):
    def test_to_html_without_props(self):
        leafnode = LeafNode("p", "normal text")
        self.assertEqual(leafnode.to_html(), "<p>normal text</p>")

    def test_to_html_with_props(self):
        dict = {"href":"weesnaw"}
        leafnode = LeafNode("p", "normal text", dict)
        self.assertEqual(leafnode.to_html(), '<p href="weesnaw">normal text</p>')

    def test_repr(self):
        leafnode = LeafNode("tag", "value", "props")
        self.assertEqual(repr(leafnode), "LeafNode(tag, value, props)")


if __name__ == "__main__":
    unittest.main()