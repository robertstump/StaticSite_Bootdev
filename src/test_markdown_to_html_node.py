import unittest
import textwrap
from markdown_html import markdown_to_html_node
from textnode import TextNode, TextType
from blocktype import BlockType

class TestMarkdownToHTML(unittest.TestCase):
    
    def test_paragraphs(self):
        md = textwrap.dedent("""
        This is a **bolded** paragraph 
        text in a p 
        tag here

        This is another paragraph with _italic_ text and `code` here
        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><p>This is a <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
            )

    def test_header_paragraph(self):
        md = """
        # Welcome to Markdown

        This is a paragraph with **bold** and _italic_ text.
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><h1>Welcome to Markdown</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p></div>")
    
    def test_header2_paragraph(self):
        md = """
        ## Welcome to Markdown

        This is a paragraph with **bold** and _italic_ text.
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><h2>Welcome to Markdown</h2><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p></div>")
    
    def test_header3_paragraph(self):
        md = """
        ### Welcome to Markdown

        This is a paragraph with **bold** and _italic_ text.
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><h3>Welcome to Markdown</h3><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p></div>")
    
    def test_header4_paragraph(self):
        md = """
        #### Welcome to Markdown

        This is a paragraph with **bold** and _italic_ text.
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><h4>Welcome to Markdown</h4><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p></div>")
    
    def test_header5_paragraph(self):
        md = """
        ##### Welcome to Markdown

        This is a paragraph with **bold** and _italic_ text.
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><h5>Welcome to Markdown</h5><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p></div>")
    
    def test_header6_paragraph(self):
        md = """
        ###### Welcome to Markdown

        This is a paragraph with **bold** and _italic_ text.
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><h6>Welcome to Markdown</h6><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p></div>")
   
    def test_block_quote(self):
        md = """
        > This is a blockquote

        Here is some `inline code` in a paragraph.
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><blockquote>This is a blockquote</blockquote><p>Here is some <code>inline code</code> in a paragraph.</p></div>")

    def test_paragraph_link_image(self):
        md = """
        This has a [link](https://boot.dev) and an ![image](img/cat.png)
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><p>This has a <a href=\"https://boot.dev\">link</a> and an <img src=\"img/cat.png\" alt=\"image\"></p></div>")

    def test_unordered(self):
        md = textwrap.dedent("""
        Start with a paragraph.

        - One
        - Two
        - Three
        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><p>Start with a paragraph.</p><ul><li>One</li><li>Two</li><li>Three</li></ul></div>")

 
    def test_unordered_single(self):
        md = """
        Start with a paragraph.

        - One
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><p>Start with a paragraph.</p><ul><li>One</li></ul></div>")

    def test_ordered_simple(self):
        md = textwrap.dedent("""
        1. First
        2. Second
        3. Third
        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>")
 
    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        ) 

    def test_simple(self):
        md = "Text **bold**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            "<div><p>Text <b>bold</b></p></div>")
   
    def test_step_one(self):
        md = "Text **bold**\n\nText **bold**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(html, "<div><p>Text <b>bold</b></p><p>Text <b>bold</b></p></div>") 

    def test_all_inline(self):
        md = """
        This is _italic_, **bold**, `code`, a [link](https://a.com), and an ![img](img.png)
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, 
            "<div><p>This is <i>italic</i>, <b>bold</b>, <code>code</code>, a <a href=\"https://a.com\">link</a>, and an <img src=\"img.png\" alt=\"img\"></p></div>")

    def test_odd_spacing(self):
        md = "This    is     spaced weirdly,   but still one paragraph."

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This    is     spaced weirdly,   but still one paragraph.</p></div>")

    def test_header_no_space(self):
        md = '''
        #Header without space

        Should this be a paragraph or header?
        '''

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>#Header without space</p><p>Should this be a paragraph or header?</p></div>")

    def test_not_a_list(self):
        md = textwrap.dedent('''
        -Not a list 
        -Because no space
        ''')

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>-Not a list -Because no space</p></div>")

    def test_bad_list(self):
        md = '''
        1. First
        2. Second
        4. Wait, what?
        '''

        self.assertRaises(ValueError, markdown_to_html_node, md)

    def test_untermed_code_block(self):
        md = "```This looks like code but doesn't close"

        self.assertRaises(ValueError, markdown_to_html_node, md)

    def test_long_sample(self):
        md = textwrap.dedent('''
        # Welcome to the Doc

        This is the opening paragraph with some _italic_, **bold**, and `code`.

        - Bullet one
        - Bullet two
        - Bullet three

        1. First step
        2. Second step
        3. Third step

        > A wise quote from someone very important.

        And one final ![image](img/final.png) to close.
        ''')

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,  '<div><h1>Welcome to the Doc</h1><p>This is the opening paragraph with some <i>italic</i>, <b>bold</b>, and <code>code</code>.</p><ul><li>Bullet one</li><li>Bullet two</li><li>Bullet three</li></ul><ol><li>First step</li><li>Second step</li><li>Third step</li></ol><blockquote>A wise quote from someone very important.</blockquote><p>And one final <img src="img/final.png" alt="image"> to close.</p></div>')

    def test_long_sample2(self):
        md = '''
        ## Developer Notes

        Please refer to the [documentation](https://example.com/docs) for usage.

        Do not forget to run `npm install` before starting development.

        Here's a quick snippet:

        ```
        function hello() {
        console.log("Hello, world!"); 
        }
        ```


        That should be everything for now.
        '''

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, '<div><h2>Developer Notes</h2><p>Please refer to the <a href="https://example.com/docs">documentation</a> for usage.</p><p>Do not forget to run <code>npm install</code> before starting development.</p><p>Here\'s a quick snippet:</p><pre><code>function hello() {\nconsole.log("Hello, world!");\n}\n</code></pre><p>That should be everything for now.</p></div>')

    def test_long_sample3(self):
        md = textwrap.dedent('''
        ### Goals for the Quarter

        > "Planning is bringing the future into the present." — Alan Lakein

        We will focus on these key areas:

        - Product Development
        - Customer Outreach
        - Infrastructure Improvements

        Each team should provide a weekly report.

        1. Monday: Planning
        2. Wednesday: Check-in
        3. Friday: Review

        Let’s make this a great quarter!
        ''')
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, '<div><h3>Goals for the Quarter</h3><blockquote>"Planning is bringing the future into the present." — Alan Lakein</blockquote><p>We will focus on these key areas:</p><ul><li>Product Development</li><li>Customer Outreach</li><li>Infrastructure Improvements</li></ul><p>Each team should provide a weekly report.</p><ol><li>Monday: Planning</li><li>Wednesday: Check-in</li><li>Friday: Review</li></ol><p>Let’s make this a great quarter!</p></div>')

    def test_unit_of_everywhere_test(self):
        md = textwrap.dedent('''
        ## Features

        - Simple CLI interface
        - Supports Markdown `*.md` files
        - Converts to clean, responsive HTML
        - Embeds images like ![diagram](assets/diagram.png)
        ''')

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>Features</h2><ul><li>Simple CLI interface</li><li>Supports Markdown <code>*.md</code> files</li><li>Converts to clean, responsive HTML</li><li>Embeds images like <img src=\"assets/diagram.png\" alt=\"diagram\"></li></ul></div>")
                                
    def test_everything_everywhere_all_at_once(self):
        md = textwrap.dedent('''
        # Project README

        Welcome to the **SiteGen** project — your one-stop _static site generator_ built with `Python`.

        ## Features

        - Simple CLI interface
        - Supports Markdown `*.md` files
        - Converts to clean, responsive HTML
        - Embeds images like ![diagram](assets/diagram.png)

        To learn more, check out [Boot.dev](https://boot.dev).

        ## Installation

        Run this command to install dependencies:

        ```bash
        pip install -r requirements.txt
        ```


        ## Usage

        1. Place your Markdown files in the `content/` folder
        2. Run `python3 main.py`
        3. Output will be saved in `dist/`

        > Note: You can configure the theme and settings in `config.yaml`.

        ## Example

        Here’s a sample `Markdown` input:

        ```markdown
        # Hello World

        This is a sample page with **bold**, _italic_, and `inline code`.
        ```


        And the rendered result will look like this:

        ```html
        <h1>Hello World</h1>
        <p>This is a sample page with <b>bold</b>, <i>italic</i>, and <code>inline code</code>.</p>
        ``` 


        ## Next Steps

        - [x] Write docs
        - [ ] Add tests
        - [ ] Improve parser

        ### Final Thoughts

        > “Programs must be written for people to read, and only incidentally for machines to execute.” — Harold Abelson

        That’s it!
        ''')
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(html)
        self.assertEqual(html,
            '<div><h1>Project README</h1><p>Welcome to the <b>SiteGen</b> project — your one-stop <i>static site generator</i> built with <code>Python</code>.</p><h2>Features</h2><ul><li>Simple CLI interface</li><li>Supports Markdown <code>*.md</code> files</li><li>Converts to clean, responsive HTML</li><li>Embeds images like <img src="assets/diagram.png" alt="diagram"></li></ul><p>To learn more, check out <a href="https://boot.dev">Boot.dev</a>.</p><h2>Installation</h2><p>Run this command to install dependencies:</p><pre><code>bash\npip install -r requirements.txt\n</code></pre><h2>Usage</h2><ol><li>Place your Markdown files in the <code>content/</code> folder</li><li>Run <code>python3 main.py</code></li><li>Output will be saved in <code>dist/</code></li></ol><blockquote>Note: You can configure the theme and settings in <code>config.yaml</code>.</blockquote><h2>Example</h2><p>Here’s a sample <code>Markdown</code> input:</p><pre><code>markdown\n# Hello World\n\nThis is a sample page with **bold**, _italic_, and `inline code`.\n</code></pre><p>And the rendered result will look like this:</p><pre><code>html\n<h1>Hello World</h1>\n<p>This is a sample page with <b>bold</b>, <i>italic</i>, and <code>inline code</code>.</p>\n</code></pre><h2>Next Steps</h2><ul><li>[x] Write docs</li><li>[ ] Add tests</li><li>[ ] Improve parser</li></ul><h3>Final Thoughts</h3><blockquote>“Programs must be written for people to read, and only incidentally for machines to execute.” — Harold Abelson</blockquote><p>That’s it!</p></div>')
             

if __name__ == "main__":
    unittest.main()
