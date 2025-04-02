from mdsplitter import text_to_text_nodes, markdown_to_blocks
from blocktype import block_to_block_type, BlockType
from textnode import text_node_to_html_node, TextNode, TextType
from parentnode import ParentNode
from leafnode import LeafNode
import re

def process_paragraph(node_list):
    leaf_list = []
    for node in node_list:
        node.text = node.text.replace("\n", "")
        html_node = text_node_to_html_node(node)
        leaf_list.append(html_node)
    return ParentNode("p", leaf_list)

def process_header_size(node_list, size):
    leaf_list = []
    for node in node_list:
        html_node = text_node_to_html_node(node)
        leaf_list.append(html_node)

    match(size):
        case 1:
            return ParentNode("h1", leaf_list)
        case 2:
            return ParentNode("h2", leaf_list)
        case 3:
            return ParentNode("h3", leaf_list)
        case 4:
            return ParentNode("h4", leaf_list)
        case 5:
            return ParentNode("h5", leaf_list)
        case 6:
            return ParentNode("h6", leaf_list)

def process_quote(node_list):
    leaf_list = []
    for node in node_list:
        if node.text.startswith("> "):
            node.text = node.text[2:]
        html_node = text_node_to_html_node(node)
        leaf_list.append(html_node)
    return ParentNode("blockquote", leaf_list)

def process_unordered(node_list):
    leaf_list = []
    for node in node_list:
        if node.text.startswith("- "):
            split_text = node.text.split("- ")
            for text in split_text:
                if text == '':
                    continue
                text = text.replace('\n', '')
                split_node_list = text_to_text_nodes(text)
                split_list = []
                for new_node in split_node_list:
                    html_node = text_node_to_html_node(new_node)
                    split_list.append(html_node)
                leaf_list.append(ParentNode("li", split_list))
    return ParentNode("ul", leaf_list)

def process_ordered(node_list):
    leaf_list = []
    for node in node_list:
        if re.match(r"(\d\.)", node.text):
            split_text = node.text.splitlines() 
            for text in split_text:
                if text == '':
                    continue
                text = text.replace('\n', '')
                split_node_list = text_to_text_nodes(text[3:])
                split_list = []
                for new_node in split_node_list:
                    html_node = text_node_to_html_node(new_node)
                    split_list.append(html_node)
                leaf_list.append(ParentNode("li", split_list))
    return ParentNode("ol", leaf_list)

def process_code_block(node_list):
    new_text = ""
    for node in node_list:
        node.text = node.text.replace('```','')
        new_text += node.text.strip()
        new_text = new_text + '\n'
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, new_text)])])


def block_node_list_to_html(node_list, block_list):
    nested_list = []
    
    for index in range(len(block_list)):
        
        match(block_list[index]):
            case BlockType.PARA:
                nested_list.append(process_paragraph(node_list[index]))

            case BlockType.HEAD:
                if node_list[index][0].text.startswith("# "):
                    node_list[index][0].text = node_list[index][0].text[2:]
                    nested_list.append(process_header_size(node_list[index], 1))
                
                elif node_list[index][0].text.startswith("## "):
                    node_list[index][0].text = node_list[index][0].text[3:]
                    nested_list.append(process_header_size(node_list[index], 2))
                
                elif node_list[index][0].text.startswith("### "):
                    node_list[index][0].text = node_list[index][0].text[4:]
                    nested_list.append(process_header_size(node_list[index], 3))

                elif node_list[index][0].text.startswith("#### "):
                    node_list[index][0].text = node_list[index][0].text[5:]
                    nested_list.append(process_header_size(node_list[index], 4))

                elif node_list[index][0].text.startswith("##### "):
                    node_list[index][0].text = node_list[index][0].text[6:]
                    nested_list.append(process_header_size(node_list[index], 5))

                elif node_list[index][0].text.startswith("###### "):
                    node_list[index][0].text = node_list[index][0].text[7:]
                    nested_list.append(process_header_size(node_list[index], 6))

            case BlockType.QUOTE:
                nested_list.append(process_quote(node_list[index]))
                
            case BlockType.UL:
                nested_list.append(process_unordered(node_list[index]))

            case BlockType.OL:
                nested_list.append(process_ordered(node_list[index]))

            case BlockType.CODE:
                nested_list.append(process_code_block(node_list[index]))
                
    return ParentNode("div", nested_list)

def markdown_to_html_node(markdown):
    block_list = []
    node_list = []
    markdown_list = markdown_to_blocks(markdown)

    for block in markdown_list:
        block_type = block_to_block_type(block)
        block_list.append(block_type)
        if block_type == BlockType.CODE:
            node_list.append([(TextNode(block, TextType.NORMAL))])
        elif block_type == BlockType.UL or block_type == BlockType.OL:
            node_list.append([(TextNode(block, TextType.NORMAL))])
        else:
            text_node_list = text_to_text_nodes(block)
            node_list.append(text_node_list)
       
    return block_node_list_to_html(node_list, block_list)
