import unittest
from htmlnode import HTMLNode

props_dict = {
        "html": "boot.dev",
        "p": "bunch of text",
        "br": "\\n"
        }
child_list = ["node2", "node3", "node4"]

class TestHTMLNode(unittest.TestCase):
    def test_props_base(self):
        node = HTMLNode("p", "the stuff in tag", child_list, props_dict)
        print(node)
        print()
    
    def test_props_one(self):
        node = HTMLNode(None, "A paragraph of text", child_list, props_dict)
        print(node)
        print()

    def test_props_two(self):
        node = HTMLNode("p", None, child_list, props_dict)
        print(node)
        print()

    def test_props_third(self):
        node = HTMLNode("p", "A paragraph of text", None, props_dict)
        print(node)
        print()

    def test_props_fourth(self):
        node = HTMLNode("p", "A paragraph of text", child_list, None)
        print(node)
        print()

    def test_not_string(self):
        node = HTMLNode(0, 0, 0, 0)
        self.assertEqual(node.tag, None)

    def test_not_string2(self):
        node = HTMLNode(0, 0, 0, 0)
        self.assertEqual(node.value, None)

    def test_not_list(self):
        node = HTMLNode(0, 0, 0, 0)
        self.assertEqual(node.children, None)

    def test_not_dictionary(self):
        node = HTMLNode(0, 0, 0, 0)
        self.assertEqual(node.props, None)

if __name__ == "main__":
    unittest.main()
