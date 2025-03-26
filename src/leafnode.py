from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props) 
        if value == None:
            raise ValueError("LeafNode must have value")
        self.no_close_tags = ("br", "hr", "img", "input", "meta", "link")
        
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have value")

        if self.tag == "":
            self.tag = None

        if self.tag == None:
            return f"{self.value}"
        elif self.tag in self.no_close_tags and self.props == None:
            return f"<{self.tag}>"
        elif self.tag in self.no_close_tags:
            return f"<{self.tag}{self.props_to_html}>"
        elif self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
