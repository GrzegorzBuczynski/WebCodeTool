from pathlib import Path
from backend.utils.path_utils import FS_EXCLUDE, list_entries


def make_file_node(entry: Path, rel_path: Path) -> dict:
    return {
        "type": "file",
        "name": entry.name,
        "path": rel_path.as_posix(),
        "size": entry.stat().st_size
    }


def make_dir_node(entry: Path, rel_path: Path, depth: int) -> dict:
    return {
        "type": "dir",
        "name": entry.name,
        "path": rel_path.as_posix(),
        "children": build_tree(entry, rel_path, depth - 1)
    }


def build_tree(dir_path: Path, rel_base: Path, depth: int) -> list[dict]:
    if depth < 0:
        return []
    items: list[dict] = []
    for entry in list_entries(dir_path):
        rel_path = rel_base / entry.name if rel_base else Path(entry.name)
        if entry.is_dir():
            items.append(make_dir_node(entry, rel_path, depth))
        elif entry.is_file():
            items.append(make_file_node(entry, rel_path))
    return items


def browse_folders(dir_path: Path) -> list[dict]:
    folders = []
    try:
        for entry in sorted(dir_path.iterdir(), key=lambda e: e.name.lower()):
            if entry.is_dir() and entry.name not in FS_EXCLUDE:
                folders.append({
                    "name": entry.name,
                    "path": str(entry.resolve())
                })
    except PermissionError:
        pass
    return folders
