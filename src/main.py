from textnode import TextNode, TextNode
from parentnode import ParentNode
from leafnode import LeafNode

def main():
    test = TextNode("Some text", TextType.BOLD, "www.boot.dev")
    print(test)

if __name__ == "__main__":
    main()
