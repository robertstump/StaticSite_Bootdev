from textnode import TextNode, TextType, text_node_to_html_node
import re

def split_nodes_delimitter(old_nodes, delimitter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        if delimitter == "" or delimitter == None:
            raise ValueError("invalid delimitter")

        divisions = node.text.split(delimitter)
        if len(divisions) % 2 == 0:
            return old_nodes
            #raise ValueError("invalid input, no closing delimitter")
        
        split_nodes = []
        for i in range(0, len(divisions)):
            if divisions[i] == "":
                continue
            elif i % 2 == 0:
                split_nodes.append(TextNode(divisions[i], TextType.NORMAL))
            elif i % 2 != 0:
                split_nodes.append(TextNode(divisions[i], text_type))
        new_nodes.extend(split_nodes)  
    
    if len(new_nodes) == 0:
        return old_nodes

    return new_nodes

def extract_markdown_images(text):
    image_list = []
    image_strings_join = ""
    image_strings = re.findall(r"(\!\[)(.*?)(\))", text)
    #image_strings = re.findall(r"(!\[(.*?)\]\(([^\s()]+(?:\([^\s()]*\)[^\s()]*)*)\))", text)
   
    for part in image_strings:
        for piece in part:
            image_strings_join += piece
    
    text_ext = re.findall(r"\!\[(.*?)\]", image_strings_join)
    #url_ext = re.findall(r"\(([^\s()]+(?:\([^\s()]*\)[^\s()]*)*)\)", image_strings_join)
    src_ext = re.findall(r"\((.*?)\)", image_strings_join)
    
    if len(text_ext) == len(src_ext) and len(text_ext) > 0:
        for i in range(len(text_ext)):
            image_list.append((text_ext[i], src_ext[i]))
            if src_ext[i] == "":
                raise ValueError("must have valid src")
    else:
        raise ValueError("text contains partial image tags")

    return image_list

def extract_markdown_links(text):
    link_list = []
    link_strings_join = ""
    link_strings = re.findall(r"((?<!!)\[)(.*?)(\))", text)

    for part in link_strings:
        for piece in part:
            link_strings_join += piece

    text_ext = re.findall(r"\[(.*?)\]", link_strings_join)
    url_ext = re.findall(r"\((.*?)\)", link_strings_join)

    if len(text_ext) == len(url_ext) and len(text_ext) > 0:
        for i in range(len(text_ext)):
            link_list.append((text_ext[i], url_ext[i]))
            if url_ext[i] == "":
                raise ValueError("must have valid url")
    else: 
        raise ValueError("text contains partial link tags")

    return link_list
