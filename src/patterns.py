import re


def extract_markdown_images(text:str) -> list[str]:
    pattern = r"\!\[.*?\]\(.*?\)"
    return re.findall(pattern, text)

def extract_markdown_links(text:str) -> list[str]:
    pattern = r"(?<!!)\[.*?\]\(.*?\)"
    return re.findall(pattern, text)
