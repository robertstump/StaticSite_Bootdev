from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    BREAK = "line-break"
    HORZ = "horizontal"
    

class TextNode():
    def __init__(self, text, text_type, url=None):
       self.text = text
       self.text_type = text_type
       self.url = url

    def __eq__(self, other):
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)
       
    def __repr__(self):
        return f"\nTextNode({self.text}, {self.text_type.value}, {self.url})\n"

   
def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            if text_node.text == None or text_node.text == "":
                return LeafNode("img", "", {"src":text_node.url})
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case TextType.BREAK:
            if text_node.text != None:
                return LeafNode("br", text_node.text)
            return LeafNode("br", None)
        case TextType.HORZ:
            if text_node.text != None:
                return LeafNode("hr", text_node.text)
            return LeafNode("hr", None)
        case _:
            raise ValueError(f"incompatible text type {text_node.text_type}")
