class HTMLNode():
    def __init__(self=None, tag=None, value=None, children=None, props=None):
        if type(tag) == str:
            self.tag = tag
        else:
            self.tag = None

        if type(value) == str:
            self.value = value
        else:
            self.value = None

        if type(children) == list:
            self.children = children
        else:
            self.children = None

        if type(props) == dict:
            self.props = props
        else: 
            self.props = None

    def to_html(self):
        raise NotImplementedError("Function not implemented")

    def props_to_html(self):
        html_string = ""
        if self.props != None:
            for key in self.props:
                html_string +=  f" {key}=\"{self.props[key]}\""
        return html_string

    def __repr__(self):
        prop_string = self.props_to_html()
        return f"Tag: {self.tag} Value: {self.value} Children:{self.children} Props:{prop_string}"
