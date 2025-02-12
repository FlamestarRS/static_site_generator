import re
from htmlnode import *
from textnode import *
from delimiter import *

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    rm_whitespace = []

    for block in blocks:
        stripped = block.strip(" ")

        if block.find("\n") != -1:
            block_sections = block.split("\n")
            new_block_sections = []
            for block in block_sections:
                stripped2 = block.strip(" ")
                new_block_sections.append(stripped2)
            joined = "\n".join(new_block_sections)
            rm_whitespace.append(joined)
            continue

        rm_whitespace.append(stripped)

    result = []
    for block in rm_whitespace:
        final = block.strip()
        if final == "":
            continue
        result.append(final)

    return result


def block_to_block_type(markdown):
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"

    if markdown.startswith("```") and markdown.endswith("```"):
        return "code"
    if markdown.startswith(">"):
        verification = verify_multiline_block(markdown, "quote")
        if all(verification) == True:
            return "quote"
    if markdown.startswith(("* ", "- ")):
        verification = verify_multiline_block(markdown, "unordered list")
        if all(verification) == True:
            return "unordered list"
    if markdown.startswith("1. "):
        verification = verify_multiline_block(markdown, "ordered list")
        if all(verification) == True:
            return "ordered list"
  
    return "paragraph"

def verify_multiline_block(markdown, type):
    verification = []
    count = 0
    numbered_list = re.split("\n", markdown)
    for item in numbered_list:
        match type:
            case "quote":
                if f"{item[0]}" == f">":
                    verification.append(True)
                else:
                    verification.append(False)

            case "unordered list":
                if f"{item[0]} " == f"* " or f"{item[0]} " == f"- ":
                    verification.append(True)
                else:
                    verification.append(False)

            case "ordered list":
                count += 1
                if f"{item[0]}. " == f"{count}. ":
                    verification.append(True)
                else:
                    verification.append(False)

    return verification



def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    children = []
    for block in markdown_blocks:

        block_type = block_to_block_type(block)

        '''
        if block_type != "unordered list":
            text_nodes += text_to_textnodes(block)
        elif block_type == "unordered list":
            text_nodes += [TextNode(block, TextType.TEXT)]
        
        for text_node in text_nodes:
            html_node = text_node_to_html_node(text_node)
        '''

        match block_type:
            case "heading":
                children.append(heading_to_html_node(block))
            case "code":
                children.append(code_to_html(block))
            case "quote":
                children.append(quote_to_html(block))
            case "unordered list":
                children.append(unordered_list_to_html(block))
            case "ordered list":
                children.append(ordered_list_to_html(block))
            case "paragraph":
                children.append(paragraph_to_html(block))

    parent = ParentNode("div", children)

    return parent

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def heading_to_html_node(block):
    if block.startswith("# "):
        text = block[2:]
        children = text_to_children(text)
        return ParentNode("h1", children)
    if block.startswith("## "):
        text = block[3:]
        children = text_to_children(text)
        return ParentNode("h2", children)
    if block.startswith("### "):
        text = block[4:]
        children = text_to_children(text)
        return ParentNode("h3", children)
    if block.startswith("#### "):
        text = block[5:]
        children = text_to_children(text)
        return ParentNode("h4", children)
    if block.startswith("##### "):
        text = block[6:]
        children = text_to_children(text)
        return ParentNode("h5", children)
    if block.startswith("###### "):
        text = block[7:]
        children = text_to_children(text)
        return ParentNode("h6", children)
    
def code_to_html(block):
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def quote_to_html(block):
    text = []
    lines = block.split("\n")
    for line in lines:
        stripped = line.lstrip(">").strip()
        text.append(stripped)
    full_quote = " ".join(text)
    children = text_to_children(full_quote)
    return ParentNode("blockquote", children)

def unordered_list_to_html(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ul", html_items)


def ordered_list_to_html(block):
    lines = block.split("\n")
    html_items = []
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ol", html_items)

def paragraph_to_html(block):
    text = block.split("\n")
    paragraph = " ".join(text)
    children = (text_to_children(paragraph))
    return ParentNode("p", children)