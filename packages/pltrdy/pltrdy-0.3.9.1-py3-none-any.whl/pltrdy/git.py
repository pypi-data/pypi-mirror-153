import subprocess
from types import ModuleType

from pathlib import Path


def get_git_revision_hash(root, short=False):
    short_str = "--short" if short else ""
    cmd = f"git rev-parse {short_str} HEAD"
    args = cmd.split()

    if isinstance(root, str):
        root = Path(root)

    elif isinstance(root, Path):
        pass

    elif isinstance(root, ModuleType):
        root = Path(root.__file__).resolve().parent

    else:
        raise TypeError(
            f"Invalid root type ({type(root)}), should be either str, Path or module"
        )

    if root.is_file():
        root = root.parent

    return subprocess.check_output(args, cwd=root).decode("ascii").strip()
