import unittest

from block import *


class TestSplitBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = ("""# This is a heading 

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item""")

        self.assertEqual([
            "# This is a heading", 
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ],
            markdown_to_blocks(markdown))
        

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        markdown = "# im a heading"
        self.assertEqual(block_to_block_type(markdown), "heading")

        markdumb = "#im not a heading"
        self.assertEqual(block_to_block_type(markdumb), "paragraph")

    def test_code(self):
        markdown = "```im code```"
        self.assertEqual(block_to_block_type(markdown), "code")
        markdumb = "`im not code ```"
        self.assertEqual(block_to_block_type(markdumb), "paragraph")

    def test_quote(self):
        markdown = ">im a quote \n>im still a quote"
        self.assertEqual(block_to_block_type(markdown), "quote")
        markdumb = ">im a quote \n but im not"
        self.assertEqual(block_to_block_type(markdumb), "paragraph")

    def test_unordered_list(self):
        markdown = "* im a list \n- and so am i"
        self.assertEqual(block_to_block_type(markdown), "unordered list")
        markdumb = "- im a list \n but im not"
        self.assertEqual(block_to_block_type(markdumb), "paragraph")

    def test_ordered_list(self):
        markdown = "1. im a list \n2. and so am i \n3. still a list!"
        self.assertEqual(block_to_block_type(markdown), "ordered list")
        markdumb = "1. im a list \n but im not \n3. oh no!"
        self.assertEqual(block_to_block_type(markdumb), "paragraph")
    
    def test_paragraph(self):
        markdown = "aifg# ``` ``` > > > \n1. \n* \n- "
        self.assertEqual(block_to_block_type(markdown), "paragraph")



class TestMarkdownToHTMLNode(unittest.TestCase):
    '''
    def test_markdown_to_html_node(self):
        md = """
# this is a heading

## this is another heading

This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

> i am a quote
> all in one block

1. ordered
2. list
3. sadly

* This is a list
* with items
"""
        blocks = markdown_to_html_node(md)
        self.assertEqual(blocks, "")
    '''
    
    def test_paragraph(self): # tests below are copied from boot dev
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )



if __name__ == "__main__":
    unittest.main()