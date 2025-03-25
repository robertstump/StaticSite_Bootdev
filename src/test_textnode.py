import unittest

from textnode import TextNode, TextType

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

if __name__== "main__":
    unittest.main()
