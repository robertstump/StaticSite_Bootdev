import unittest

from blocktype import BlockType, block_to_block_type

class TestBlockType(unittest.TestCase):
    def simple_block_test(self):
        md = "This is **bolded** paragraph"
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.PARA)

    def test_bigger_simple_block(self):
        md = "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.PARA)

    def test_unorder_list_simple(self):
        md = "- This is a list\n- with items"
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.UL)

    def test_order_list_simple(self):
        md = "1. This is one\n2. This is two\n3. This is three"
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.OL)

    def test_order_list_bad_num(self):
        md = "1. This is one\n2. This is two\n5. This is three"
        self.assertRaises(ValueError, block_to_block_type, md)

    def test_unorder_bad_line(self):
        md = "- This is a list\n# with items"
        self.assertRaises(ValueError, block_to_block_type, md)

    def test_header_simple(self):
        md = "# Header One"
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.HEAD)

    def test_code_block(self):
        md = "```\nThis is a code block\n```"
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.CODE)

    def test_bad_code_block(self):
        md = "```\nThis is a bad code block"
        self.assertRaises(ValueError, block_to_block_type, md) 

    def test_simple_quote(self):
        md = ">Wither 'tis better to be a blockquote\n>Ay, there's the rub! \n>For in that sleep of death what dreams may come,\n> When we have shuffled off this mortal coil,\n> Must give us pause—there's the respect"
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.QUOTE)

    def test_bad_quote(self):
        md = "Wither tis better\n>to be a blockquote"
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.PARA)

    def test_three_header(self):
        md = "### A level three header"
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.HEAD)

    def test_unorder_leading_space(self):
        md = "- Bullet one\n - Bullet two\n - Bullet three"
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.UL)

    def test_multi_line_paragraph(self):
        md = "Paragraph with no special formatting but multiple lines\nStill the same paragraph"
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.PARA)

    def test_header_no_space(self):
        md = "#HeaderNoSpace"
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.PARA)

    def test_unorder_no_space(self):
        md = "- Missing space after dash\n-not a list item"
        self.assertRaises(ValueError, block_to_block_type, md)

    def test_bad_block_quote(self):
        md = ">Quote line\nNon-quote continuation"
        self.assertRaises(ValueError, block_to_block_type, md) 

    def test_empty_md(self):
        md = ""
        bl_type = block_to_block_type(md)
        self.assertEqual(bl_type, BlockType.PARA)

    def test_extra_bad_list(self):
        md = "1. This\n2. That\nThree. Not a number"
        self.assertRaises(ValueError, block_to_block_type, md)
