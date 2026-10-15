import os
import shutil
import sys

from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node


def generate_files(target_path: str):
    if not os.path.isdir(target_path):
        raise NotADirectoryError("current_path must be a directory")

    files: list[str] = []
    dirs: list[str] = []

    for item in os.listdir(target_path):
        item_path = os.path.join(target_path, item)
        if os.path.isdir(item_path):
            dirs.append(item_path)
        else:
            files.append(item_path)
    yield from files

    for dir in dirs:
        yield from generate_files(dir)

def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str | None = None):
    print(f"Generating page from {from_path} into {dest_path} using template {template_path}.")

    markdown = None
    template = None
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    if base_path:
         page = page.replace('href="/', f'href="{base_path}')
         page = page.replace('src="/', f'src="{base_path}')

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as f:
        f.write(page)


def generate_page_recursively(from_path: str, template_path: str, dest_path: str, base_path: str | None = None):
    for f in generate_files(from_path):
        original_filename = os.path.basename(f)

        if not original_filename.endswith(".md"):
            continue

        changed_filename = original_filename.removesuffix(".md") + ".html"

        dst_path = os.path.normpath(os.path.join(dest_path, os.path.relpath(os.path.dirname(f), from_path), changed_filename))
        generate_page(f, template_path, dst_path, base_path=base_path)

def recursive_copy(src: str, dist: str):
    if not os.path.exists(src):
        raise FileNotFoundError(f"There is no such file of directory as \"{src}\"")

    if os.path.exists(dist):
        shutil.rmtree(dist)

    if not os.path.isdir(src):
        shutil.copy(src, dist)
        return

    os.mkdir(dist)
    for entry in os.listdir(src):
        recursive_copy(os.path.join(src, entry), os.path.join(dist, entry))

def main() -> None:
    base_path = None
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    try:
        recursive_copy(os.path.join(project_root, "static"), os.path.join(project_root, "docs"))
    except OSError:
        print("Cannot copy static files into public directory")
        sys.exit(1)

    generate_page_recursively(
        os.path.join(project_root, "content"),
        os.path.join(project_root, "template.html"),
        os.path.join(project_root, "docs"),
        base_path=base_path
    )

if __name__ == "__main__":
    main()
