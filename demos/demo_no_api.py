#!/usr/bin/env python3
"""
Szybki test bez API - Demo funkcjonalności
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cad_ai.task_manager import TaskManager, TaskType, Task

print("="*80)
print("DEMO: System Wieloagentowy (bez API)")
print("="*80 + "\n")

# Utwórz TaskManager i zadania
task_manager = TaskManager()

# Główne zadanie
main_task = task_manager.create_task(
    description="Opisz proces budowy domu",
    task_type=TaskType.MAIN,
    level=0
)

print(f"✓ Główne zadanie: {main_task.description}")
print(f"  ID: {main_task.id}")
print(f"  Status: {main_task.status}")
print(f"  Typ: {main_task.task_type}")
print(f"  Poziom: {main_task.level}\n")

# Podzadania (przykład)
sub_tasks = []
for i, subtask_desc in enumerate([
    "Planowanie i projekt",
    "Przygotowanie terenu",
    "Budowa fundamentu",
    "Podnoszenie ścian",
    "Dach",
    "Instalacje",
    "Wykończenie"
], 1):
    subtask = task_manager.create_task(
        description=subtask_desc,
        task_type=TaskType.SUBTASK,
        level=1,
        parent_id=main_task.id
    )
    sub_tasks.append(subtask)
    main_task.subtasks.append(subtask.id)
    print(f"✓ Podzadanie {i}: {subtask_desc}")

print("\n" + "="*80)
print("STATYSTYKI")
print("="*80 + "\n")

all_tasks = list(task_manager.tasks.values())
print(f"Całkowite zadania: {len(all_tasks)}")
print(f"Główne zadania: {len([t for t in all_tasks if t.task_type == TaskType.MAIN])}")
print(f"Podzadania: {len([t for t in all_tasks if t.task_type == TaskType.SUBTASK])}")

print("\n" + "="*80)
print("✅ DEMO UKOŃCZONE")
print("="*80 + "\n")

print("To był demo TaskManager (bez API).")
print("Aby uruchomić pełny system z AI:")
print("  1. Ustaw API_KEY w .env")
print("  2. Uruchom: python test_run.py")
