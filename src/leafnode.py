from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props) 
        self.no_close_tags = ("br", "hr", "img", "meta", "link")
        if value == None and tag not in self.no_close_tags:
            raise ValueError("LeafNode must have value")
        
    def to_html(self):
        if self.value == None and self.tag not in self.no_close_tags:
            raise ValueError("LeafNode must have value")

        if self.tag == "":
            self.tag = None

        if self.tag == None:
            return f"{self.value}"
        elif self.tag in self.no_close_tags and self.props == None:
            return f"<{self.tag}>"
        elif self.tag in self.no_close_tags:
            return f"<{self.tag}{self.props_to_html()}>"
        elif self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
