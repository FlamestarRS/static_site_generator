import unittest

from htmlnode import HTMLNode

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


if __name__ == "__main__":
    unittest.main()