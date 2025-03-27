import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_uneq(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is not a pipe", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_empty(self):
        node = TextNode("", None, None)
        node2 = TextNode("", None, None)
        self.assertEqual(node, node2) 

    def test_eq_self(self):
        node = TextNode("This is a text node", TextType.ITALIC, "boot.dev")
        self.assertEqual(node, node)
    
    def test_eq_unequal_all(self):
        node = TextNode("this is a text node", TextType.BOLD, "boot.dev")
        node2 = TextNode("This is a text node", TextType.NORMAL, "root.dev")
        self.assertNotEqual(node, node2)

    def test_eq_one_url(self):
        node = TextNode("This", TextType.LINK, "boot.dev")
        node2 = TextNode("This", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_eq_nonestring(self):
        node = TextNode("This", TextType.CODE, "None")
        node2 = TextNode("This", TextType.CODE, None)
        self.assertNotEqual(node, node2)

    def test_eq_uninit(self):
        node = TextNode
        node.text = None
        node.text_type = None
        node.url = None
        node2 = TextNode("", None, None)
        self.assertNotEqual(node, node2) 
    
    def test_eq_uninit_2(self):
        node = TextNode
        node.text = None
        node.text_type = None
        node.url = None
        node2 = TextNode(None, None, None)
        self.assertEqual(node, node2)

    def test_eq_text_type(self):
        node = TextNode("This", "bold", "boot.dev")
        node2 = TextNode("This", TextType.BOLD, "boot.dev")
        self.assertNotEqual(node, node2)

    def test_eq_bad_string(self):
        an_int = 0
        node = TextNode(an_int, TextType.IMAGE)
        node2 = TextNode("This is not a string", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_eq_bad_order(self):
        node = TextNode(TextType.BOLD, "This is a string", None)
        node2 = TextNode(TextType.BOLD, "This is a string", None)
        self.assertEqual(node, node2)

    def test_eq_bad_order_one(self):
        node = TextNode(TextType.BOLD, "This is a string", None)
        node2 = TextNode("This is a string", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, node.text)

    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, node.text)

    def test_code(self):
        node = TextNode("This is code()", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, node.text)
        
    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, node.text)
        self.assertEqual(html_node.props, {"href":node.url})

    def test_image(self):
        node = TextNode("Image of a dog", TextType.IMAGE, "/folder/dog.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":node.url, "alt":node.text})

    def test_image_no_alt(self):
        node = TextNode(None, TextType.IMAGE, "/folder/butt.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":node.url})

    def test_break(self):
        node = TextNode(None, TextType.BREAK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "br")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.value, None)

    def test_break_text(self):
        node = TextNode("Text after line break", TextType.BREAK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "br")
        self.assertEqual(html_node.value, node.text)
        self.assertEqual(html_node.props, None)

    def test_horizontal(self):
        node = TextNode(None, TextType.HORZ)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "hr")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, None)

    def test_horz_text(self):
        node = TextNode("Text after horizontal", TextType.HORZ)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "hr")
        self.assertEqual(html_node.value, node.text)
        self.assertEqual(html_node.props, None)
    
if __name__== "main__":
    unittest.main()
