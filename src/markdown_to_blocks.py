def markdown_to_blocks(md: str) -> list[str]:
    return list(filter(lambda s: s, md.strip().split("\n\n")))
