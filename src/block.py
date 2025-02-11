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
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "heading":
                text_node = 



