from textnode import TextNode, TextType, text_node_to_html_node

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
