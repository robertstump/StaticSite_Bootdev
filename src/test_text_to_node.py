import unittest

from textnode import TextNode, TextType
from mdsplitter import text_to_text_nodes, markdown_to_blocks

class TestTextToTextNode(unittest.TestCase):
    def test_given_test(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node_list = text_to_text_nodes(text)
        self.assertEqual(node_list,
            [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ])

    def test_bold(self):
        text1 = "Simple sentence with **bold** text."
        node_list = text_to_text_nodes(text1)
        self.assertEqual(node_list, 
            [ 
            TextNode("Simple sentence with ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.NORMAL)
            ])
    def test_italic_and_code(self):
        text2 = "Here is _italic_ text followed by `inline code`."
        node_list = text_to_text_nodes(text2)
        self.assertEqual(node_list, 
            [
            TextNode("Here is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text followed by ", TextType.NORMAL),
            TextNode("inline code", TextType.CODE),
            TextNode(".", TextType.NORMAL)
            ])
    def test_bold_italic_and_code(self):
        text3 = "Mixing **bold**, _italic_, and `code` in one line."
        node_list = text_to_text_nodes(text3)
        self.assertEqual(node_list,
            [
            TextNode("Mixing ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(", and ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" in one line.", TextType.NORMAL)
            ])

    def test_link_and_bold(self):
        text4 = "This includes a [link](https://example.com) and **bold**."
        node_list = text_to_text_nodes(text4)
        self.assertEqual(node_list,
            [
            TextNode("This includes a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(".", TextType.NORMAL)
            ])

    def test_multiple_bold(self):
        text5 = "Multiple **bold** and **strong** words together."
        node_list = text_to_text_nodes(text5)
        self.assertEqual(node_list,
            [
            TextNode("Multiple ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("strong", TextType.BOLD),
            TextNode(" words together.", TextType.NORMAL)
            ])
    def test_image_italic(self):
        text6 = "Image here ![cat](https://imgur.com/cat.png) and _italic_ too."
        node_list = text_to_text_nodes(text6)
        self.assertEqual(node_list,
            [
            TextNode("Image here ", TextType.NORMAL),
            TextNode("cat", TextType.IMAGE, "https://imgur.com/cat.png"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" too.", TextType.NORMAL)
            ])

    def test_code_link_code(self):
        text7 = "`code` block, then a [link](https://boot.dev), then another `code`."
        node_list = text_to_text_nodes(text7)
        self.assertEqual(node_list,
            [
            TextNode("code", TextType.CODE),
            TextNode(" block, then a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(", then another ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.NORMAL)
            ])

    def test_image_link_italic(self):
        text8 = "An image ![meme](https://i.imgur.com/funny.png), a [link](https://google.com), and _emphasis_."
        node_list = text_to_text_nodes(text8)
        self.assertEqual(node_list,
            [
            TextNode("An image ", TextType.NORMAL),
            TextNode("meme", TextType.IMAGE, "https://i.imgur.com/funny.png"),
            TextNode(", a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://google.com"),
            TextNode(", and ", TextType.NORMAL),
            TextNode("emphasis", TextType.ITALIC),
            TextNode(".", TextType.NORMAL)
            ])

    def test_bold_image_code_italics(self):
        text9 = "**Bold** start, then ![img](https://img.com/a.png), then `code`, then _italics_."
        node_list = text_to_text_nodes(text9)
        self.assertEqual(node_list,
            [
            TextNode("Bold", TextType.BOLD),
            TextNode(" start, then ", TextType.NORMAL),
            TextNode("img", TextType.IMAGE, "https://img.com/a.png"),
            TextNode(", then ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(", then ", TextType.NORMAL),
            TextNode("italics", TextType.ITALIC),
            TextNode(".", TextType.NORMAL)
            ])
    def test_all_together(self):
        text10 = "Crazy combo: _one_ [two](https://two.com) `three` ![four](https://four.io/img.jpg) **five**."
        node_list = text_to_text_nodes(text10)
        self.assertEqual(node_list,
            [
            TextNode("Crazy combo: ", TextType.NORMAL),
            TextNode("one", TextType.ITALIC),
            TextNode(" ", TextType.NORMAL),
            TextNode("two", TextType.LINK, "https://two.com"),
            TextNode(" ", TextType.NORMAL),
            TextNode("three", TextType.CODE),
            TextNode(" ", TextType.NORMAL),
            TextNode("four", TextType.IMAGE, "https://four.io/img.jpg"),
            TextNode(" ", TextType.NORMAL),
            TextNode("five", TextType.BOLD),
            TextNode(".", TextType.NORMAL)
            ])

class TestMDToBlock(unittest.TestCase):
    def test_given_test(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
        [
        "This is **bolded** paragraph",
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        "- This is a list\n- with items",
        ],
        )

    def test_header_paragraph(self):
        md1 = "# Header One\n\nThis is a paragraph under a header."
        blocks = markdown_to_blocks(md1)
        self.assertEqual(blocks,
            [
            "# Header One",
            "This is a paragraph under a header."
            ])

    def test_header_two_lines(self):
        md2 = "## Subheader\n\nAnother paragraph here with two lines.\nStill part of the same block."
        blocks = markdown_to_blocks(md2)
        self.assertEqual(blocks,
            [
            "## Subheader",
            "Another paragraph here with two lines.\nStill part of the same block."
            ])

    def test_list(self):
        md3 = "- Item 1\n- Item 2\n- Item 3"
        blocks = markdown_to_blocks(md3)
        self.assertEqual(blocks,
            [
            "- Item 1\n- Item 2\n- Item 3"
            ])

    def test_ordered_list(self):
        md4 = "1. First item\n2. Second item\n3. Third item"
        blocks = markdown_to_blocks(md4)
        self.assertEqual(blocks,
            [
            "1. First item\n2. Second item\n3. Third item"
            ])

    def test_empty(self):
        md5 = ""
        blocks = markdown_to_blocks(md5)
        self.assertEqual(blocks, [])

    def test_breaks(self):
        md6 = "\n\n\n"
        blocks = markdown_to_blocks(md6)
        self.assertEqual(blocks, [])

    #this really should break differently but we aren't handling bad formatting yet...
    def test_weird_list(self):
        md7 = "Paragraph\n- List without break\n- Still list\n\nNew paragraph"
        blocks = markdown_to_blocks(md7)
        self.assertEqual(blocks, 
            [
            "Paragraph\n- List without break\n- Still list",
            "New paragraph"
            ])
    def test_extra_breaks(self):
        md8 = "This is spaced oddly\n\n\n\n\nBut still should become separate blocks"
        blocks = markdown_to_blocks(md8)
        self.assertEqual(blocks, 
            [
            "This is spaced oddly",
            "But still should become separate blocks"
            ])

    def test_leading_space(self):
        md9 = "   This line has leading spaces\n\n   So does this one"
        blocks = markdown_to_blocks(md9)
        self.assertEqual(blocks,
            [
            "This line has leading spaces",
            "So does this one"
            ])
        
if __name__ == "main__()":
    unittest.main()
