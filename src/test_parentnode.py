import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        print(parent_node.to_html())
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        print(parent_node.to_html())
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_two_leaves(self):
         child1 = LeafNode("b", "grandchild")
         child2 = LeafNode(None, "second child")
         parent_node = ParentNode("div", [child1, child2])
         print(parent_node.to_html())
         self.assertEqual(parent_node.to_html(), "<div><b>grandchild</b>second child</div>")
    
    def test_to_html_parent_props(self):
        node = ParentNode("span", 
            [
            LeafNode(None, "Blue "),
            LeafNode("sup", "Super")
            ], 
            {"style" : "color:blue;"})
        print(node.to_html())
        self.assertEqual(node.to_html(), "<span style=\"color:blue;\">Blue <sup>Super</sup></span>")


    def test_to_html_sample(self):
        node = ParentNode(
            "p",
            [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ])
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_sam2(self):
        node = ParentNode("p",
            [
            ParentNode("b", 
                [
                LeafNode(None, "Bold "),
                LeafNode("i", "and italic"),
                LeafNode(None, " text")
                ]),
            LeafNode(None, " Normal text")
            ])
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p><b>Bold <i>and italic</i> text</b> Normal text</p>")

    def test_to_html_sam3(self):
        node = ParentNode("p",
            [
            ParentNode("b", 
                [
                LeafNode(None, "Bold "),
                ParentNode("i", 
                    [
                    LeafNode(None, "Italic "),
                    LeafNode("u", "Underlined")
                    ]),
                LeafNode(None, " Text")
                ]),
            LeafNode(None, " Normal")
            ])
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p><b>Bold <i>Italic <u>Underlined</u></i> Text</b> Normal</p>")

    def test_to_html_sam4(self):
        node = ParentNode("p",
            [
            ParentNode("b",
                [
                LeafNode(None, "Bold "),
                ParentNode("i",
                    [
                    LeafNode(None, "Italic "),
                    ParentNode("u",
                        [
                        LeafNode(None, "Underlined "),
                        LeafNode("span", "Red", {"style" : "color:red;"})
                        ])
                    ])
                ]),
            LeafNode(None, " Text")
        ])
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p><b>Bold <i>Italic <u>Underlined <span style=\"color:red;\">Red</span></u></i></b> Text</p>")
    
    def test_to_html_sam5(self):
        node = ParentNode("p",
            [
            ParentNode("b",
                [
                LeafNode(None, "Bold "),
                ParentNode("i",
                    [
                    LeafNode(None, "Italic "),
                    ParentNode("u",
                        [
                        LeafNode(None, "Underlined "),
                        ParentNode("span", 
                            [
                            LeafNode(None, "Blue "),
                            LeafNode("sup", "Super")
                            ], {"style" : "color:blue;"})
                        ]),
                    ]),
                ]),
            LeafNode(None, " Text")
            ])
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p><b>Bold <i>Italic <u>Underlined <span style=\"color:blue;\">Blue <sup>Super</sup></span></u></i></b> Text</p>")

    def test_to_html_sam6(self):
        node = ParentNode("p",
            [
            ParentNode("b",
                [
                LeafNode(None, "Bold "),
                ParentNode("i",
                    [
                    LeafNode(None, "Italic "),
                    ParentNode("u", 
                        [
                        LeafNode(None, "Underlined "),
                        ParentNode("span", 
                            [
                            LeafNode(None, "Green "),
                            ParentNode("sup",
                                [
                                LeafNode(None, "Super "),
                                LeafNode("sub", "Sub")
                                ]),
                            ], {"style" : "color:green;"})
                        ]),
                    ]),
                ]),
            LeafNode(None, " Text")
            ])
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p><b>Bold <i>Italic <u>Underlined <span style=\"color:green;\">Green <sup>Super <sub>Sub</sub></sup></span></u></i></b> Text</p>")

    def test_to_html_sam7(self):
        node = ParentNode("p", 
            [
            ParentNode("b", 
                [
                LeafNode(None, "Bold "),
                ParentNode("i",
                    [
                    LeafNode(None, "Italic "),
                    ParentNode("u",
                        [
                        LeafNode(None, "Underlined "),
                        ParentNode("span", 
                            [
                            LeafNode(None, "Purple "),
                            ParentNode("sup",
                                [
                                LeafNode(None, "Super "),
                                ParentNode("sub", 
                                    [
                                    LeafNode(None, "Sub "),
                                    LeafNode("a", "Link", {"href" : "#"})
                                    ]),
                                ]),
                            ], {"style" : "color:purple;"}),
                        ]),
                    ]),
                ]),
            LeafNode(None, " End")
            ])
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p><b>Bold <i>Italic <u>Underlined <span style=\"color:purple;\">Purple <sup>Super <sub>Sub <a href=\"#\">Link</a></sub></sup></span></u></i></b> End</p>")

    def test_to_html_sam8(self):
        node = ParentNode("p",
            [
            ParentNode("b",
                [
                LeafNode(None, "Bold "),
                ParentNode("i", 
                    [
                    LeafNode(None, "Italic "),
                    ParentNode("u", 
                        [
                        LeafNode(None, "Underlined "),
                        ParentNode("span",
                            [
                            LeafNode(None, "Brown Text "),
                            LeafNode("abbr", "API", {"title": "Application Programming Interface"}),
                            ParentNode("sup", 
                                [
                                LeafNode(None, "Super "),
                                ParentNode("sub",
                                    [
                                    LeafNode(None, "Sub "),
                                    ParentNode("a",
                                        [
                                        LeafNode("code", "code()"),
                                        LeafNode("span", "Important", {"style" : "color:darkred; font-weight:bold;"})
                                        ], {"href" : "#"}),
                                    ]),
                                ]),
                            ], {"style" : "color:brown; font-size:14px;"}),
                        ]),
                    ]),
                ]),
            LeafNode(None, " Done.")
            ])
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p><b>Bold <i>Italic <u>Underlined <span style=\"color:brown; font-size:14px;\">Brown Text <abbr title=\"Application Programming Interface\">API</abbr><sup>Super <sub>Sub <a href=\"#\"><code>code()</code><span style=\"color:darkred; font-weight:bold;\">Important</span></a></sub></sup></span></u></i></b> Done.</p>")

    def test_to_html_sam9(self):
        node = ParentNode("p",
            [
            ParentNode("b",
                [
                LeafNode(None, "Deep "),
                ParentNode("i",
                    [
                    LeafNode(None, "Styled "),
                    ParentNode("u", 
                        [
                        LeafNode(None, "Underlined "),
                        ParentNode("span", 
                            [
                            LeafNode(None, "Text with "),
                            LeafNode("a", "external link", {"href":"https://example.com", "title":"Visit Example", "target":"_blank", "style":"text-decoration:none; color:crimson; font-weight:bold;"}),
                            LeafNode(None, ", plus "),
                            LeafNode("abbr", "XML", {"title":"Extensible Markup Language", "style":"border-bottom:1px dotted gray; cursor:help;"}),
                            LeafNode(None, " and "),
                            LeafNode("code", "console.log()", {"style":"background-color:#f4f4f4; padding:2px 4px; border:1px solid #ccc;"}),
                            LeafNode(None, "inside a "),
                            LeafNode("span", "styled span", {"style":"color:darkgreen; font-style:italic; font-weight:600;"}),
                            LeafNode(None, ".")
                            ], {"style":"color:navy; font-size:15px;"})
                        ]),
                    ]),
                ]),
            LeafNode(None, " That's a wrap!")
        ])
        print(node.to_html())
        self.assertEqual(node.to_html(), "<p><b>Deep <i>Styled <u>Underlined <span style=\"color:navy; font-size:15px;\">Text with <a href=\"https://example.com\" title=\"Visit Example\" target=\"_blank\" style=\"text-decoration:none; color:crimson; font-weight:bold;\">external link</a>, plus <abbr title=\"Extensible Markup Language\" style=\"border-bottom:1px dotted gray; cursor:help;\">XML</abbr> and <code style=\"background-color:#f4f4f4; padding:2px 4px; border:1px solid #ccc;\">console.log()</code>inside a <span style=\"color:darkgreen; font-style:italic; font-weight:600;\">styled span</span>.</span></u></i></b> That's a wrap!</p>")

 
