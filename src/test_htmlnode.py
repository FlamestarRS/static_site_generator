import unittest

from htmlnode import *

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


class TestParentNode(unittest.TestCase):
    def test_children_list_without_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.children_list(), "<b>Bold text</b>Normal text<i>italic text</i>Normal text")

    def test_children_list_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", "textprop"),
                LeafNode(None, "Normal text", {"href":"weesnaw"}),
                LeafNode("i", "italic text", {"dict":"prop"}),
                LeafNode(None, "Normal text", "props"),
            ],
        )
        self.assertEqual(node.children_list(), '<btextprop>Bold text</b>Normal text<i dict="prop">italic text</i>Normal text')

    def test_to_html_children_no_list_no_arguments(self):
        node = ParentNode("p", LeafNode(None, None, None))
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_children_not_class(self):
        node = ParentNode("p", "im not a node!")
        self.assertRaises(ValueError, node.to_html)

    def test_parent_tags(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", "textprop"),
                LeafNode(None, "Normal text", {"href":"weesnaw"}),
                LeafNode("i", "italic text", {"dict":"prop"}),
                LeafNode(None, "Normal text", "props"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><btextprop>Bold text</b>Normal text<i dict="prop">italic text</i>Normal text</p>')

    def test_parent_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", "textprop"),
                LeafNode(None, "Normal text", {"href":"weesnaw"}),
                LeafNode("i", "italic text", {"dict":"prop"}),
                LeafNode(None, "Normal text", "props"),
            ], "im a prop!!!"
        )
        self.assertEqual(node.to_html(), '<pim a prop!!!><btextprop>Bold text</b>Normal text<i dict="prop">italic text</i>Normal text</p>')

    def test_repr(self):
        node = ParentNode("tag", "value", "props")
        self.assertEqual(repr(node), "ParentNode(tag, value, props)")


if __name__ == "__main__":
    unittest.main()