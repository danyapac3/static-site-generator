class NoTitleError(Exception):
    "There is no title to extract"

def extract_title(markdown: str) -> str:
    if markdown.startswith("# "):
        return markdown.split("\n")[0].removeprefix("# ").strip()
    raise NoTitleError
