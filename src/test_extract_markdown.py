import unittest
from mdsplitter import extract_markdown_images, extract_markdown_links

class TestMDImageExtract(unittest.TestCase):
    def test_image_only(self):
        test_text = "![solo](local/solo.png)"
        extraction = extract_markdown_images(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("solo", "local/solo.png")])

    def test_single_image(self):
        test_text = "This is a simple ![image](local/image_name.png)"
        extraction = extract_markdown_images(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("image", "local/image_name.png")])

    def test_image_first(self):
        test_text = "![first](local/first_image)Does it matter where it goes?"
        extraction = extract_markdown_images(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("first", "local/first_image")])

    def test_double_image(self):
        test_text = "This is a dog ![dog](local/dog.png) and a cat ![cat](local/cat.jpg)"
        extraction = extract_markdown_images(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("dog", "local/dog.png"), ("cat", "local/cat.jpg")])

    def test_text_with_exclaim(self):
        test_text = "What if there is this!? ![exclaim](local/exclaim.bmp)"
        extraction = extract_markdown_images(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("exclaim", "local/exclaim.bmp")])

    def test_with_other_parentheses(self):
        test_text = "Pictured Bob Hope(left) ![Bob Hope](local/bob_hope.jpg)"
        extraction = extract_markdown_images(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("Bob Hope", "local/bob_hope.jpg")])

    def test_with_image_in_paren(self):
        test_text = "Text (with an ![side_note](local/side_note.png) image in parentheses)"
        extraction = extract_markdown_images(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("side_note", "local/side_note.png")])

    def test_image_special_name(self):
        test_text = "An image with ![special chars](imag@34.spec.gif)"
        extraction = extract_markdown_images(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("special chars", "imag@34.spec.gif")])

    def test_broken_tag(self):
        test_text = "a broken image ![oops(local/mistakes.gif)"
        self.assertRaises(ValueError, extract_markdown_images, test_text)

    def test_broken_tag2(self):
        test_text = "broken2 !oops](local/mistakes.gif)"
        self.assertRaises(ValueError, extract_markdown_images, test_text)

    def test_no_images(self):
        test_text = "this is a plain string"
        extraction = extract_markdown_images(test_text)
        self.assertEqual(extraction, [])

    def test_empty_string(self):
        test_text = ""
        extraction = extract_markdown_images(test_text)
        self.assertEqual(extraction, []) 

    def test_bad_format(self):
        test_text = "this is wrong ! [bad](local/no_good.bmp)"
        extraction = extract_markdown_images(test_text)
        self.assertEqual(extraction, [])

    def test_escaped_format(self):
        test_text = r"this is also wrong \!\[bad\]\(local/no_good.bmp\)"
        extraction = extract_markdown_images(test_text)
        self.assertEqual(extraction, [])

    def test_empty_alt(self):
        test_text = "empty alt test image: ![](local/ablist.jpg)"
        extraction = extract_markdown_images(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("", "local/ablist.jpg")])

    def test_empty_src(self):
        test_text = "empty url, fails: ![missing]()"
        self.assertRaises(ValueError, extract_markdown_images, test_text)

    #trade-off works with everything but nested parentheses..... 
    #rewrite as manual parser with open close checker (char by char)
    # no regex, will work with all sorts of nested structures.... 
    #def test_image_name_parens(self):
     #   test_text = "This is valid (and common): ![dl_twice](mom(1).jpg)"
      #  extraction = extract_markdown_images(test_text)
       # #print(extraction)
        #self.assertEqual(extraction, [("dl_twice", "mom(1).jpg")])

class TestMDLinkExtract(unittest.TestCase):
    def test_only_link(self):
        test_text = "[click me](web.site)"
        extraction = extract_markdown_links(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("click me", "web.site")])

    def test_simple_link(self):
        test_text = "This is a [link](boot.dev)"
        extraction = extract_markdown_links(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("link", "boot.dev")])
        
    def test_double_link(self):
        test_text = "These are two [link](boot.dev) and [link2](web.site)"
        extraction = extract_markdown_links(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("link", "boot.dev"), ("link2", "web.site")])

    def test_link_first(self):
        test_text = "[link](boot.dev) and then some text."
        extraction = extract_markdown_links(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("link", "boot.dev")]) 

    def test_link_exclaim(self):
        test_text = "Whoa, check out the link! [link](boot.dev)"
        extraction = extract_markdown_links(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("link", "boot.dev")])

    def test_with_extra_paren(self):
        test_text = "Pictured: Kermit the Frog(left), Miss Piggy(right)[link](muppets.com)"
        extraction = extract_markdown_links(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("link", "muppets.com")])

    def test_with_image_and_link(self):
        test_text = "![dog](local/dog.jpg) This is a link[link](link.link)"
        extraction = extract_markdown_links(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("link", "link.link")])

    def test_link_in_paren(self):
        test_text = "TFA (Totally [Freaking](awesome.sauce) Awesome)"
        extraction = extract_markdown_links(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("Freaking", "awesome.sauce")])

    def test_link_with_special_chars(self):
        test_text = "Be [3!337](leetcode.com), nah just kidding"
        extraction = extract_markdown_links(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("3!337", "leetcode.com")])

    def test_broken_link_tag(self):
        test_text = "a broken link [oops(local/mistakes.com)"
        self.assertRaises(ValueError, extract_markdown_links, test_text)

    def test_broken_link_tag2(self):
        test_text = "broken2 oops](local/mistakes.com)"
        self.assertRaises(ValueError, extract_markdown_links, test_text)

    def test_no_links(self):
        test_text = "this is a plain string"
        extraction = extract_markdown_links(test_text)
        self.assertEqual(extraction, [])

    def test_empty_link_string(self):
        test_text = ""
        extraction = extract_markdown_links(test_text)
        self.assertEqual(extraction, [])

    def test_bad_link_format(self):
        test_text = "this is wrong [bad(local/no_good.com)"
        self.assertRaises(ValueError, extract_markdown_links, test_text)

    def test_empty_alt_link(self):
        test_text = "empty alt link text test : [](local/ablist.com)"
        extraction = extract_markdown_links(test_text)
        #print(extraction)
        self.assertEqual(extraction, [("", "local/ablist.com")])

    def test_empty_url(self):
        test_text = "empty url, fails: [missing]()"
        self.assertRaises(ValueError, extract_markdown_links, test_text)

if __name__ == "main()__":
    unittest.main()
