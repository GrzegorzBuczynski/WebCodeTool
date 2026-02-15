from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import Request
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


def inject_dependencies(request: Request):
    return {
        "app_state": app.state,
        "results_dir": RESULTS_DIR,
        "base_root": BASE_ROOT,
        "project_root": PROJECT_ROOT
    }


from backend.routes import fs_routes, task_routes


@fs_routes.router.api_route(methods=["GET", "POST"], path="/{path:path}", include_in_schema=False)
async def fs_route_handler(request: Request):
    deps = inject_dependencies(request)
    for route in fs_routes.router.routes:
        if route.path == request.url.path and request.method in route.methods:
            return await route.endpoint(**deps, **request.query_params, **await request.json() if request.method == "POST" else {})


app.include_router(
    fs_routes.router,
    dependencies=[]
)

app.include_router(
    task_routes.router,
    dependencies=[]
)

app.mount("/", StaticFiles(directory=PUBLIC_DIR, html=True), name="static")
