from textnode import TextNode
from textnode import TextType

def main():
    test = TextNode("Some text", TextType.BOLD, "www.boot.dev")
    print(test)

if __name__ == "__main__":
    main()
