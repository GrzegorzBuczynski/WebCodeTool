from pathlib import Path
import json


def read_json_file(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def read_text_preview(path: Path, limit: int = 200) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")[:limit]


def list_task_dirs(results_dir: Path) -> list[Path]:
    if not results_dir.exists():
        return []
    return sorted(
        [p for p in results_dir.iterdir() if p.is_dir() and p.name.startswith("task_")],
        key=lambda p: p.name
    )


def build_task_item(task_path: Path) -> dict:
    result = read_json_file(task_path / "result.json") or {}
    preview = read_text_preview(task_path / "output.txt") or "(brak wyniku)"
    stat = task_path.stat()
    return {
        "id": task_path.name,
        "description": result.get("description", "(brak)"),
        "status": result.get("status", "unknown"),
        "verified": (result.get("verification") or {}).get("passed", False),
        "score": (result.get("verification") or {}).get("score", 0),
        "preview": preview,
        "timestamp": stat.st_ctime
    }


def load_task_data(task_path: Path) -> dict:
    files = [
        "result.json",
        "output.txt",
        "report.txt",
        "detailed_report.json",
        "hierarchy.json",
        "stats.json"
    ]
    payload: dict = {}
    for name in files:
        file_path = task_path / name
        if not file_path.exists():
            continue
        if name.endswith(".json"):
            payload[name] = json.loads(file_path.read_text(encoding="utf-8"))
        else:
            payload[name] = file_path.read_text(encoding="utf-8")
    return payload
