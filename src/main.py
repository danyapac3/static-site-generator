import os
import shutil
import sys


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
    project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    try:
        recursive_copy(os.path.join(project_root, "static"), os.path.join(project_root, "public"))
    except OSError:
        print("Cannot copy static files into public directory")
        sys.exit(1)

if __name__ == "__main__":
    main()
