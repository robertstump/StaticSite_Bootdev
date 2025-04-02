import re
import textwrap
from enum import Enum

class BlockType(Enum):
    
    PARA = "paragraph"
    HEAD = "header"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"

def block_to_block_type(markdown):
    markdown = textwrap.dedent(markdown).strip()

    if markdown == '':
        return BlockType.PARA

    if markdown[0] == '#':
        if markdown.startswith("# ") or markdown.startswith("## ") or markdown.startswith("### ") or markdown.startswith("#### ") or markdown.startswith("##### ") or markdown.startswith("###### "):
            return BlockType.HEAD
    
    if markdown.startswith("```"):
        code_index = markdown.find('```')
        if '```' in markdown[code_index + 3:]: 
            return BlockType.CODE
        else:
            raise ValueError("code block must end with three backticks")
    
    if markdown[0] == '>':
        quote_lines = markdown.splitlines()
        for line in quote_lines:
            line = line.strip()
            if not line.startswith(">"):
                raise ValueError("Quote blocks must start each line with '>'")
        return BlockType.QUOTE
    
    if markdown.startswith("- "): 
        ul_lines = markdown.splitlines()
        for line in ul_lines:
            line = line.strip()
            if not line.startswith("- "):
                raise ValueError("each line much be part of unordered list")
        return BlockType.UL
    
    if markdown.startswith(r'1.'):
        if '\n' in markdown and not re.search(r"(\n\d\.)", markdown):
            raise ValueError("every line of list must be numbered")
        ol_lines = markdown.splitlines()
        count = 0
        correct_num = True
        for line in ol_lines:
            count += 1
            if not line.startswith(f"{count}. "):
                correct_num = False

        if correct_num:
            return BlockType.OL
        else: 
            raise ValueError("ordered list must be in proper order")
    
    return BlockType.PARA
