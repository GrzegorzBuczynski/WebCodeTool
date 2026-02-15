import subprocess
import sys
import threading
from pathlib import Path


def run_test_process(script_path: Path, cwd: Path) -> None:
    if not script_path.exists():
        return
    process = subprocess.Popen(
        [sys.executable, str(script_path)],
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


def start_test_thread(script_path: Path, cwd: Path) -> None:
    thread = threading.Thread(
        target=run_test_process,
        args=(script_path, cwd),
        daemon=True
    )
    thread.start()
