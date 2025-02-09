from textnode import *
from htmlnode import *

import re

def split_nodes_delimiter(old_nodes):

    if not isinstance(old_nodes, list): # turns a single node in a list containing that node
        old_nodes = [old_nodes]
    
    if len(old_nodes) <= 0:             # error handling
        raise ValueError("Invalid nodes: no nodes")
    
    delimiter = identify_delimiter(old_nodes)   # create list of delimiters based on markdown for each node
    if all(item == "" for item in delimiter):
        return old_nodes
    new_nodes = []
    for i in range(0, len(old_nodes)):
        if old_nodes[i].text_type != TextType.TEXT:     # inline elements only supported for normal text
            new_nodes.append(old_nodes[i])
        else:
            delimiter_type = delimiter_to_TextType(delimiter[i])    # match case for delimiter
            node_text = old_nodes[i].text
            if delimiter[i] == "":              # this makes multiple different inline elements work
                new_nodes += [old_nodes[i]]
                continue
            split_node = node_text.split(delimiter[i])              # "" is added if inline element is at the start or end of text, Ex: text = "im **bold" becomes ["im ", "bold", ""]

            if len(split_node) % 2 == 0:
                raise ValueError("Invalid markdown: check delimiter placement")
            for i in range(0, len(split_node)):
                if i % 2 == 0:
                    new_nodes += [TextNode(split_node[i], TextType.TEXT)]   # even numbered list elements are text
                if i % 2 != 0:
                    new_nodes += [TextNode(split_node[i], delimiter_type)]  # odd numbered list elements require inline formatting
    return split_nodes_delimiter(new_nodes)

def delimiter_to_TextType(delimiter):   # input is single markdown element
    match delimiter:
        case "":
            return TextType.TEXT
        case "**":
            return TextType.BOLD
        case "*":
            return TextType.ITALIC
        case "`":
            return TextType.CODE
        case _:
            raise ValueError("Invalid delimiter")
        
def identify_delimiter(old_nodes):      # input is list of nodes
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    delimiter_list = []
    for i in range(0, len(old_nodes)):
        node_text = old_nodes[i].text
        bold = node_text.find("**")     # .find() returns index value or -1 if not found
        italic = node_text.find("*")
        code = node_text.find("`")
        if bold != -1:                  # appends markdown element to list
            delimiter_list.append("**")
        elif italic != -1:
            delimiter_list.append("*")
        elif code != -1:
            delimiter_list.append("`")
        else:
            delimiter_list.append("")
    return delimiter_list               # list of markdown elements to match input list


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
    

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

"""
def split_nodes_image(old_nodes):
    new_nodes = []
    for i in range(0, len(old_nodes)):
        matches = extract_markdown_images(old_nodes[i].text)
        node_text = old_nodes[i].text
        if old_nodes[i].text_type != TextType.TEXT:
            new_nodes.append(old_nodes[i])
            continue
        #replaced = old_nodes[i].text.replace(")","!")
        for image in matches:
            split_text = node_text.split("![{image[0]}]({image[1]})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node_text = split_text[0]

            # original code below   
        for i in range(0, len(split_text)):
            print(split_text[i])
            if i % 2 == 0:
                node = TextNode(split_text[i], TextType.TEXT, None)
                new_nodes.append(node)
            if i % 2 != 0:
                node = TextNode(matches[i//2][0], TextType.IMAGE, matches[i//2][1])
                new_nodes.append(node)
            # original code above
        

        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes
"""


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

    

"""
def split_nodes_link(old_nodes):
    new_nodes = []
    for i in range(0, len(old_nodes)):
        matches = extract_markdown_links(old_nodes[i].text)
        replaced = old_nodes[i].text.replace(")","[")
        split_text = replaced.split("[")
        for i in range(0, len(split_text)):
            if i % 2 == 0:
                node = TextNode(split_text[i], TextType.TEXT, None)
                new_nodes.append(node)
            if i % 2 != 0:
                node = TextNode(matches[i//2][0], TextType.LINK, matches[i//2][1])
                new_nodes.append(node)
    return new_nodes

"""

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    split1 = split_nodes_delimiter(node)
    split2 = split_nodes_image(split1)
    split3 = split_nodes_link(split2)
    return split3