from pathlib import Path
from fastapi import HTTPException

FS_EXCLUDE = {"node_modules", "venv", "__pycache__", ".git", "results"}


def is_within_base(target: Path, base: Path) -> bool:
    return str(target).startswith(str(base))


def normalize_root(path_str: str) -> Path:
    return Path(path_str).expanduser().resolve()


def validate_root(target: Path, base: Path) -> None:
    if not target.exists() or not target.is_dir():
        raise HTTPException(status_code=404, detail="Katalog nie istnieje")
    if not is_within_base(target, base):
        raise HTTPException(status_code=400, detail="Nieprawidłowa ścieżka")


def safe_resolve(rel_path: Path, base: Path) -> Path:
    target = (base / rel_path).resolve()
    if not is_within_base(target, base):
        raise HTTPException(status_code=400, detail="Nieprawidłowa ścieżka")
    return target


def list_entries(dir_path: Path) -> list[Path]:
    return sorted(
        [entry for entry in dir_path.iterdir() if entry.name not in FS_EXCLUDE],
        key=lambda entry: entry.name.lower()
    )
