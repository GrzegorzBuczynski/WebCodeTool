import subprocess
import sys
import threading
from pathlib import Path
from typing import Iterable


def run_test_process(script_path: Path, cwd: Path, args: Iterable[str] | None = None) -> None:
    if not script_path.exists():
        return
    extra_args = list(args or [])
    process = subprocess.Popen(
        [sys.executable, str(script_path), *extra_args],
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    if stdout:
        print("[Python stdout]", stdout)
    if stderr:
        print("[Python stderr]", stderr)


def start_test_thread(script_path: Path, cwd: Path, args: Iterable[str] | None = None) -> None:
    thread = threading.Thread(
        target=run_test_process,
        args=(script_path, cwd, args),
        daemon=True
    )
    thread.start()
