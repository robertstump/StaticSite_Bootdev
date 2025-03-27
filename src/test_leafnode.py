import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_close(self):
        node = LeafNode("br", "")
        print(node.to_html())
        self.assertEqual(node.to_html(), "<br>")

    def test_leaf_no_close_prop(self):
        node = LeafNode("a", "boot.dev", {"href": "boot.dev"})
        print(node.to_html())
        self.assertEqual(node.to_html(), "<a href=\"boot.dev\">boot.dev</a>")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "some plain text")
        print(node.to_html())
        self.assertEqual(node.to_html(), "some plain text")

    def test_leaf_bad_data(self):
        node = LeafNode(0, 0, 0)
        self.assertRaises(ValueError, node.to_html) 

    def test_leaf_no_tag_prop(self):
        node = LeafNode(None, "some text", {"href": "boot.dev"})
        print(node.to_html())
        self.assertEqual(node.to_html(), "some text")

    def test_leaf_empties(self):
        node = LeafNode("", "", "")
        self.assertEqual(node.to_html(), "")

    def test_leaf_value_empties(self):
        node = LeafNode("", "text", "")
        print(node.to_html())
        self.assertEqual(node.to_html(), "text")

if __name__== "main__":
    unittest.main()
