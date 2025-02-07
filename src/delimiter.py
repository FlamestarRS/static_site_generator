from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes):

    if not isinstance(old_nodes, list): # turns a single node in a list containing that node
        old_nodes = [old_nodes]
    
    if len(old_nodes) <= 0: # error handling
        raise ValueError("Invalid nodes: no nodes")
    
    delimiter = identify_delimiter(old_nodes) # create list of delimiters based on markdown for each node
    new_nodes = []
    for i in range(0, len(old_nodes)):
        if old_nodes[i].text_type != TextType.TEXT: # inline elements only supported for normal text
            new_nodes.append(old_nodes[i])
        else:
            delimiter_type = delimiter_to_TextType(delimiter[i]) # match case for delimiter
            node_text = old_nodes[i].text
            split_node = node_text.split(delimiter[i])
            if len(split_node) != 3:
                raise ValueError("Invalid markdown: check delimiter placement")
            new_node1 = TextNode(split_node[0], TextType.TEXT)
            new_node2 = TextNode(split_node[1], delimiter_type) 
            new_node3 = TextNode(split_node[2], TextType.TEXT)
            new_nodes += [new_node1, new_node2, new_node3]
    return new_nodes

def delimiter_to_TextType(delimiter):
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
        
def identify_delimiter(old_nodes):
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    delimiter_list = []
    for i in range(0, len(old_nodes)):
        node_text = old_nodes[i].text
        bold = node_text.find("**")
        italic = node_text.find("*")
        code = node_text.find("`")
        if bold != -1:
            delimiter_list.append("**")
        elif italic != -1:
            delimiter_list.append("*")
        elif code != -1:
            delimiter_list.append("`")
        else:
            delimiter_list.append("")
    return delimiter_list
            