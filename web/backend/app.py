from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def get_base_root(project_root: Path) -> Path:
    return project_root.parent


def get_results_dir(base_root: Path) -> Path:
    return base_root / "results"


def get_public_dir(project_root: Path) -> Path:
    return project_root / "public"


PROJECT_ROOT = get_project_root()
BASE_ROOT = get_base_root(PROJECT_ROOT)
RESULTS_DIR = get_results_dir(BASE_ROOT)
PUBLIC_DIR = get_public_dir(PROJECT_ROOT)

app = FastAPI()
app.state.current_root = PROJECT_ROOT

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


from typing import Optional
from backend.routes.fs_routes import (
    RootRequest, SaveFileRequest, get_root, list_roots, set_root, fs_tree, fs_browse, fs_file, fs_save_file
)
from backend.routes.task_routes import (
    RunRequest, api_results, api_task, api_run, api_status
)


@app.get("/api/fs/root")
def route_get_root():
    return get_root(app.state)


@app.get("/api/fs/roots")
def route_list_roots():
    return list_roots(app.state, BASE_ROOT)


@app.post("/api/fs/root")
def route_set_root(payload: RootRequest):
    return set_root(payload, app.state, BASE_ROOT)


@app.get("/api/fs/tree")
def route_fs_tree(path: str = ".", depth: int = 4):
    return fs_tree(app.state, path, depth)


@app.get("/api/fs/browse")
def route_fs_browse(path: str = "/"):
    return fs_browse(path)


@app.get("/api/fs/file")
def route_fs_file(path: Optional[str] = None):
    return fs_file(app.state, path)


@app.post("/api/fs/file")
def route_fs_save_file(payload: SaveFileRequest):
    return fs_save_file(payload, app.state)


@app.get("/api/results")
def route_results():
    return api_results(RESULTS_DIR)


@app.get("/api/task/{task_id}")
def route_task(task_id: str):
    return api_task(task_id, RESULTS_DIR)


@app.post("/api/run")
def route_run(payload: RunRequest):
    return api_run(payload, PROJECT_ROOT, BASE_ROOT)


@app.get("/api/status")
def route_status():
    return api_status(app.state, RESULTS_DIR)


app.mount("/", StaticFiles(directory=PUBLIC_DIR, html=True), name="static")
