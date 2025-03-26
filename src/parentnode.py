from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        if tag == None:
            raise ValueError("ParentNode must have tag")
        if children == None:
            raise ValueError("ParentNode must have children")

        if type(children) != list:
            raise ValueError("Children must be a list")

    def to_html(self):
        result = ""

        for child in self.children:
            if type(child) == ParentNode:
                result += f"{child.to_html()}" 
            if type(child) == LeafNode:
                result += f"{child.to_html()}"
        if self.props != None:
            return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"
        return f"<{self.tag}>{result}</{self.tag}>"

#need dict to check for validity of html tags
