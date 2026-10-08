def markdown_to_blocks(md: str) -> list[str]:
    return filter(lambda s: s, md.split("\n\n").strip())
