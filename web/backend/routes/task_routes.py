from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import Optional
from backend.services.task_service import (
    list_task_dirs, build_task_item, load_task_data
)
from backend.services.test_runner import start_test_thread

router = APIRouter(prefix="/api", tags=["tasks"])


class RunRequest(BaseModel):
    taskDescription: Optional[str] = None


@router.get("/results")
def api_results(results_dir: Path) -> dict:
    tasks = [build_task_item(path) for path in list_task_dirs(results_dir)]
    return {"tasks": list(reversed(tasks)), "total": len(tasks)}


@router.get("/task/{task_id}")
def api_task(task_id: str, results_dir: Path) -> dict:
    task_path = results_dir / task_id
    if not task_path.exists():
        raise HTTPException(status_code=404, detail="Zadanie nie znalezione")
    return load_task_data(task_path)


@router.post("/run")
def api_run(payload: RunRequest, project_root: Path, base_root: Path) -> dict:
    description = payload.taskDescription or "Zaplanuj prosty obiad dla 4 osób: zupa, drugie danie i deser."
    script_path = base_root / "scripts" / "test_run.py"
    start_test_thread(script_path, project_root)
    return {
        "status": "running",
        "message": "Uruchamianie testu w tle...",
        "taskDescription": description
    }


@router.get("/status")
def api_status(app_state, results_dir: Path) -> dict:
    return {
        "status": "ok",
        "root": str(app_state.current_root),
        "resultsDir": str(results_dir),
        "resultsExist": results_dir.exists()
    }
