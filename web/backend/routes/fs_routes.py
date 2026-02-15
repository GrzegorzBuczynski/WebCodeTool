from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import Optional
from backend.utils.path_utils import (
    normalize_root, validate_root, safe_resolve, list_entries
)
from backend.services.fs_service import build_tree, browse_folders

router = APIRouter(prefix="/api/fs", tags=["filesystem"])

MAX_FILE_SIZE = 200 * 1024


class RootRequest(BaseModel):
    root: str
    
class SaveFileRequest(BaseModel):
    path: str
    content: str
MAX_WRITE_SIZE = 1024 * 1024


@router.get("/root")
def get_root(app_state) -> dict:
    return {"root": str(app_state.current_root)}


@router.get("/roots")
def list_roots(app_state, base_root: Path) -> dict:
    roots = [
        {"name": entry.name, "path": str(entry.resolve())}
        for entry in list_entries(base_root)
        if entry.is_dir()
    ]
    return {"roots": roots}


@router.post("/root")
def set_root(payload: RootRequest, app_state, base_root: Path) -> dict:
    target = normalize_root(payload.root)
    validate_root(target, base_root)
    app_state.current_root = target
    return {"root": str(target)}


@router.get("/tree")
def fs_tree(app_state, path: str = ".", depth: int = 4) -> dict:
    rel_path = Path("") if path in (".", "", None) else Path(path)
    target = safe_resolve(rel_path, app_state.current_root)
    if not target.exists() or not target.is_dir():
        raise HTTPException(status_code=404, detail="Katalog nie istnieje")
    tree = build_tree(target, rel_path, depth)
    return {"root": str(app_state.current_root), "tree": tree}


@router.get("/browse")
def fs_browse(path: str = "/") -> dict:
    target = Path(path).expanduser().resolve()
    if not target.exists() or not target.is_dir():
        raise HTTPException(status_code=404, detail="Katalog nie istnieje")
    folders = browse_folders(target)
    return {"path": str(target), "folders": folders}


@router.get("/file")
def fs_file(app_state, path: Optional[str] = None) -> dict:
    if not path:
        raise HTTPException(status_code=400, detail="Brak parametru path")
    target = safe_resolve(Path(path), app_state.current_root)
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="Plik nie istnieje")
    size = target.stat().st_size
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Plik zbyt duży do podglądu")
    content = target.read_text(encoding="utf-8")
    return {"path": path, "size": size, "content": content}

@router.post("/file")
def fs_save_file(payload: SaveFileRequest, app_state) -> dict:
    if not payload.path:
        raise HTTPException(status_code=400, detail="Brak parametru path")
    if len(payload.content.encode("utf-8")) > MAX_WRITE_SIZE:
        raise HTTPException(status_code=413, detail="Plik zbyt duży do zapisu")
    target = safe_resolve(Path(payload.path), app_state.current_root)
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="Plik nie istnieje")
    target.write_text(payload.content, encoding="utf-8")
    size = target.stat().st_size
    return {"path": payload.path, "size": size}
