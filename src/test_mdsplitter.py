import unittest
from mdsplitter import split_nodes_delimitter, split_nodes_images, split_nodes_links
from textnode import TextNode, TextType

class TestMDSplitter(unittest.TestCase):
    def test_bold_text(self):
        node = TextNode("This has a **bold** word", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], '**', TextType.BOLD)
        ###print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This has a ", TextType.NORMAL), TextNode("bold", TextType.BOLD), TextNode(" word", TextType.NORMAL)])

    def test_simple_bad_delim_text(self):
        node = TextNode("This is plain text", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], '*', TextType.NORMAL)
        ###print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This is plain text", TextType.NORMAL)])

    def test_italic_text(self):
        node = TextNode("This is _italic_ text", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "_", TextType.ITALIC)
        ###print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This is ", TextType.NORMAL), TextNode("italic", TextType.ITALIC), TextNode(" text", TextType.NORMAL)])

    def test_code_text(self):
        node = TextNode("This is ...\ncode...\n in text", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "...\n", TextType.CODE)
        ###print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This is ", TextType.NORMAL), TextNode("code", TextType.CODE), TextNode(" in text", TextType.NORMAL)])
    
    def test_code_block_text(self):
        node = TextNode("This has a 'code block' word", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "'", TextType.CODE)
        ###print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This has a ", TextType.NORMAL), TextNode("code block", TextType.CODE), TextNode(" word", TextType.NORMAL)])

    def test_double_bold_text(self):
        node = TextNode("This text **has** two words **bolded**", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "**", TextType.BOLD)
        ###print(new_nodes)
        self.assertEqual(new_nodes, 
            [
            TextNode("This text ", TextType.NORMAL),
            TextNode("has", TextType.BOLD),
            TextNode(" two words ", TextType.NORMAL),
            TextNode("bolded", TextType.BOLD)
            ])

    def test_bold_italic_text(self):
        node = TextNode("This text _has_ bold and **italic** text", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimitter(new_nodes, "_", TextType.ITALIC)
        ###print(new_nodes)
        self.assertEqual(new_nodes,
            [
            TextNode("This text ", TextType.NORMAL),
            TextNode("has", TextType.ITALIC),
            TextNode(" bold and ", TextType.NORMAL),
            TextNode("italic", TextType.BOLD),
            TextNode(" text", TextType.NORMAL)
            ])

    def test_half_delimitter1(self):
        node = TextNode("This text **has half delimitter", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "**", TextType.BOLD)
        ###print(new_nodes)
        self.assertEqual(new_nodes[0], node)

    #has to be on inside of ** delim, would be nice to have more optoins......
    def test_include_delim_char(self):
        node = TextNode(r"This should have **\*asterix and bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "**", TextType.BOLD)
        ###print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This should have ", TextType.NORMAL), TextNode(r"\*asterix and bold", TextType.BOLD)])

    #should this remove the extra spaces? should it ignore double delimitters?
    def test_adjacent_delim(self):
        node = TextNode("These **** should **** disappear", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "**", TextType.BOLD)
        ###print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("These ", TextType.NORMAL), TextNode(" should ", TextType.NORMAL), TextNode(" disappear", TextType.NORMAL)]) 

    def test_multiple_node_input(self):
        node = []
        node.append(TextNode("This is plain", TextType.NORMAL))
        node.append(TextNode("This has **bold** text", TextType.NORMAL))
        node.append(TextNode("But this was already bold", TextType.BOLD))
        new_nodes = split_nodes_delimitter(node, "**", TextType.BOLD)
        ###print(new_nodes)
        self.assertEqual(new_nodes,
[
            TextNode("This is plain", TextType.NORMAL),
            TextNode("This has ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
            TextNode("But this was already bold", TextType.BOLD),
            ])

    def test_empty_node_text(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "_", TextType.ITALIC)
        ###print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("", TextType.NORMAL)])

class TestMDImageSplitter(unittest.TestCase):
    def test_simple_image_node(self):
        node = TextNode("This has a ![dog](local/dog.jpg) dog", TextType.NORMAL)
        new_nodes = split_nodes_images([node])
        ##print(f"OUTPUT: {new_nodes}")
        self.assertEqual(new_nodes, 
                        [
                        TextNode("This has a ", TextType.NORMAL), 
                        TextNode("dog", TextType.IMAGE, "local/dog.jpg"), 
                        TextNode(" dog", TextType.NORMAL)
                        ])

    def test_only_image_node(self):
        node = TextNode("![dog](local/dog.jpg)", TextType.NORMAL)
        new_nodes = split_nodes_images([node])
        ##print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("dog", TextType.IMAGE, "local/dog.jpg")])

    def test_double_image_node(self):
        node = TextNode("This has two images ![dog](local/dog.jpg) and ![cat](local/cat.jpg)", TextType.NORMAL)
        new_nodes = split_nodes_images([node])
        ##print(new_nodes)
        self.assertEqual(new_nodes, 
                        [
                        TextNode("This has two images ", TextType.NORMAL),
                        TextNode("dog", TextType.IMAGE, "local/dog.jpg"),
                        TextNode(" and ", TextType.NORMAL),
                        TextNode("cat", TextType.IMAGE, "local/cat.jpg")
                        ])

    def test_bad_image_node(self):
        node = TextNode("This has bad [image](bad.com)", TextType.NORMAL)
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [node])

    def test_image_with_link(self):
        node = TextNode("This has link [link](boot.dev) and ![image](local/dog.png)", TextType.NORMAL)
        new_nodes = split_nodes_images([node])
        ##print(new_nodes)
        self.assertEqual(new_nodes,
                        [
                        TextNode("This has link [link](boot.dev) and ", TextType.NORMAL),
                        TextNode("image", TextType.IMAGE, "local/dog.png")
                        ])

    def test_begin_end_image(self):
       node = TextNode("![cat](local/cat.jpg) and a ![dog](local/dog.jpg)", TextType.NORMAL)
       new_nodes = split_nodes_images([node])
       ##print(new_nodes)
       self.assertEqual(new_nodes,
                        [
                        TextNode("cat", TextType.IMAGE, "local/cat.jpg"),
                        TextNode(" and a ", TextType.NORMAL),
                        TextNode("dog", TextType.IMAGE, "local/dog.jpg")
                        ])

    def test_only_plain_text(self):
        node = TextNode("This is plain text", TextType.NORMAL)
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [TextNode("This is plain text", TextType.NORMAL)])

class TestMDLinkSplitter(unittest.TestCase):
    def test_simple_link(self):
        node = TextNode("[link](boot.dev)", TextType.NORMAL)
        new_nodes = split_nodes_links([node])
        ##print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("link", TextType.LINK, 'boot.dev')])
   
    def test_only_link_node(self):
        node = TextNode("[dog](boot.dev/dog.html)", TextType.NORMAL)
        new_nodes = split_nodes_links([node])
        ##print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("dog", TextType.LINK, "boot.dev/dog.html")])

    def test_double_link_node(self):
        node = TextNode("This has two links [dog](boot.dev) and [cat](web.site)", TextType.NORMAL)
        new_nodes = split_nodes_links([node])
        #print(f"FAILING: {new_nodes}")
        self.assertEqual(new_nodes, 
                        [
                        TextNode("This has two links ", TextType.NORMAL),
                        TextNode("dog", TextType.LINK, "boot.dev"),
                        TextNode(" and ", TextType.NORMAL),
                        TextNode("cat", TextType.LINK, "web.site")
                        ])

    def test_bad_link_node(self):
        node = TextNode("This has bad [imagebad.com)", TextType.NORMAL)
        self.assertRaises(ValueError, split_nodes_links, [node])

    def test_image_with_link(self):
        node = TextNode("This has link [link](boot.dev) and ![image](local/dog.png)", TextType.NORMAL)
        new_nodes = split_nodes_links([node])
        #print(f"FAILING: {new_nodes}")
        self.assertEqual(new_nodes,
                        [
                        TextNode("This has link ", TextType.NORMAL),
                        TextNode("link", TextType.LINK, "boot.dev"),
                        TextNode(" and ![image](local/dog.png)", TextType.NORMAL)
                        ])

    def test_begin_end_link(self):
       node = TextNode("[cat](boot.dev) and a [dog](web.site)", TextType.NORMAL)
       new_nodes = split_nodes_links([node])
       #print(new_nodes)
       self.assertEqual(new_nodes,
                        [
                        TextNode("cat", TextType.LINK, "boot.dev"),
                        TextNode(" and a ", TextType.NORMAL),
                        TextNode("dog", TextType.LINK, "web.site")
                        ])

    def test_only_plain_text_link(self):
        node = TextNode("This is plain text", TextType.NORMAL)
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [node])

if __name__ =="main__":
    unittest.main()
