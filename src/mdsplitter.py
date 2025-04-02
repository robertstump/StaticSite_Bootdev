from textnode import TextNode, TextType 
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
    if text == "":
        return image_list

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
        if '](' in text and '[' not in text:
            raise ValueError("text contains partial image tags")
        if '![' in text and '](' not in text:
            raise ValueError("missing close bracket, open parentheses")

    return image_list

def extract_markdown_links(text):
    link_list = []
    if text == "":
        return link_list

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
        if '[' not in text and '](' in text: 
            raise ValueError("missing close bracket")
        elif  '[' in text and not ']' in text: 
            raise ValueError("text contains partial link tags")
        elif '[' in text and '](' in text and ')' not in text:
            raise ValueError("missing close parentheses")
        elif ')' in text and '](' not in text:
            raise ValueERror("missing open parentheses")

    return link_list

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        divisions = re.split(r"(!\[.*?\))", node.text)
        extraction = extract_markdown_images(node.text)

        split_nodes = []
        extraction_count = 0
        for i in range(0, len(divisions)):
            if divisions[i] == "":
                continue
            elif divisions[i][0] == '!' and divisions[i][1] == "[": 
                split_nodes.append(TextNode(extraction[extraction_count][0], TextType.IMAGE, extraction[extraction_count][1]))
                extraction_count += 1
            else:
                split_nodes.append(TextNode(divisions[i], TextType.NORMAL))
        new_nodes.extend(split_nodes)

    if len(new_nodes) == 0:
        return old_nodes

    return new_nodes
        
def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        divisions = re.split(r"(?<!!)(\[.*?\))", node.text)
        extraction = extract_markdown_links(node.text)

        split_nodes = []
        extraction_count = 0
        for i in range(0, len(divisions)):
            if divisions[i] == "":
                continue
            elif divisions[i][0] == '[' and '](' in divisions[i]:
                split_nodes.append(TextNode(extraction[extraction_count][0], TextType.LINK, extraction[extraction_count][1]))
                extraction_count += 1 
            else:
                split_nodes.append(TextNode(divisions[i], TextType.NORMAL))
        new_nodes.extend(split_nodes)

    if len(new_nodes) == 0:
        return old_nodes
    
    return new_nodes

def text_to_text_nodes(text):
    node = TextNode(text, TextType.NORMAL)
    new_nodes = split_nodes_delimitter([node], '**', TextType.BOLD)
    new_nodes = split_nodes_delimitter(new_nodes, '_', TextType.ITALIC)
    new_nodes = split_nodes_delimitter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_images(new_nodes)
    new_nodes = split_nodes_links(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    block_list = []

    if markdown == "":
        return block_list
    
    if  '```' in markdown:
        start = markdown.find('```')
        if '```' in markdown[start + 3:]:
            block_list = markdown_to_blocks(markdown[:start])
            end = markdown[start + 3:].find('```') + (start + 3)
            
            code_block = markdown[start:end + 3]
            code_block = code_block.split('\n')
            tmp_code_list = []
            for code in code_block:
                code = code.strip()
                tmp_code_list.append(code)
            code_block = '\n'.join(tmp_code_list)

            block_list.append(code_block)
            block_list.extend(markdown_to_blocks(markdown[end + 3:]))
            return block_list     

    tmp_list = markdown.split("\n\n")
    for block in tmp_list:
        block = block.strip()
        if block == '':
            continue
        block_list.append(block)


    return block_list
