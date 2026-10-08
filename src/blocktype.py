import re

from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered"
    ORDERED_LIST = "ordered"


def check_if_heading(block: str) -> bool:
    pattern = r"^[#]{1,6} "
    return bool(re.match(pattern, block))

def check_if_code(block: str) -> bool:
    return block.startswith("```\n") and block.endswith("\n```")

def check_if_quote(block: str) -> bool:
    lines = block.split("\n")
    return all(line.startswith((">", "> ")) for line in lines) 

def check_if_unordered_list(block: str) -> bool:
    lines = block.split("\n")
    return all(line.startswith("- ") for line in lines) 

def check_if_ordered_list(block: str) -> bool:
    line_pattern = "^(?P<number>[\d]+)\."
    for i, line in enumerate(block.split("\n"), start=1):
        if not line.startswith(f"{i}. "):
            return False
    return True 

def block_to_block_type(block: str):
    if check_if_heading(block): 
        return BlockType.HEADING
    if check_if_code(block): 
        return BlockType.CODE
    if check_if_quote(block): 
        return BlockType.QUOTE
    if check_if_unordered_list(block): 
        return BlockType.UNORDERED_LIST
    if check_if_ordered_list(block): 
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

