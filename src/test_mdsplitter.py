import unittest
from mdsplitter import split_nodes_delimitter
from textnode import TextNode, TextType

class TestMDSplitter(unittest.TestCase):
    def test_bold_text(self):
        node = TextNode("This has a **bold** word", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], '**', TextType.BOLD)
        #print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This has a ", TextType.NORMAL), TextNode("bold", TextType.BOLD), TextNode(" word", TextType.NORMAL)])

    def test_simple_bad_delim_text(self):
        node = TextNode("This is plain text", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], '*', TextType.NORMAL)
        #print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This is plain text", TextType.NORMAL)])

    def test_italic_text(self):
        node = TextNode("This is _italic_ text", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "_", TextType.ITALIC)
        #print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This is ", TextType.NORMAL), TextNode("italic", TextType.ITALIC), TextNode(" text", TextType.NORMAL)])

    def test_code_text(self):
        node = TextNode("This is ...\ncode...\n in text", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "...\n", TextType.CODE)
        #print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This is ", TextType.NORMAL), TextNode("code", TextType.CODE), TextNode(" in text", TextType.NORMAL)])
    
    def test_code_block_text(self):
        node = TextNode("This has a 'code block' word", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "'", TextType.CODE)
        #print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This has a ", TextType.NORMAL), TextNode("code block", TextType.CODE), TextNode(" word", TextType.NORMAL)])

    def test_double_bold_text(self):
        node = TextNode("This text **has** two words **bolded**", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "**", TextType.BOLD)
        #print(new_nodes)
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
        #print(new_nodes)
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
        #print(new_nodes)
        self.assertEqual(new_nodes[0], node)

    #has to be on inside of ** delim, would be nice to have more optoins......
    def test_include_delim_char(self):
        node = TextNode(r"This should have **\*asterix and bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "**", TextType.BOLD)
        #print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("This should have ", TextType.NORMAL), TextNode(r"\*asterix and bold", TextType.BOLD)])

    #should this remove the extra spaces? should it ignore double delimitters?
    def test_adjacent_delim(self):
        node = TextNode("These **** should **** disappear", TextType.NORMAL)
        new_nodes = split_nodes_delimitter([node], "**", TextType.BOLD)
        #print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("These ", TextType.NORMAL), TextNode(" should ", TextType.NORMAL), TextNode(" disappear", TextType.NORMAL)]) 

    def test_multiple_node_input(self):
        node = []
        node.append(TextNode("This is plain", TextType.NORMAL))
        node.append(TextNode("This has **bold** text", TextType.NORMAL))
        node.append(TextNode("But this was already bold", TextType.BOLD))
        new_nodes = split_nodes_delimitter(node, "**", TextType.BOLD)
        #print(new_nodes)
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
        #print(new_nodes)
        self.assertEqual(new_nodes, [TextNode("", TextType.NORMAL)])

if __name__ =="main__":
    unittest.main()
