#!/usr/bin/env python3
"""
Demonstracja pełnego systemu z persistencją wyników
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cad_ai.agents import MasterOrchestrator
from cad_ai.task_manager import TaskManager, TaskType
from cad_ai.results_viewer import list_saved_tasks, view_detailed_report, list_execution_logs

def main():
    print("\n" + "="*80)
    print("DEMONSTRACJA: Hierarchiczna dekompozycja zadań z persistencją")
    print("="*80 + "\n")
    
    # Konfiguracja
    main_task_desc = "Opisz proces budowy domu: planowanie, przygotowanie, fundament, ściany, dach, instalacje, wykończenie"
    
    # Inicjacja orchestratora z persistencją
    task_manager = TaskManager()
    orchestrator = MasterOrchestrator(
        task_manager=task_manager,
        max_recursion_depth=10,
        persistence_dir=str(ROOT / "results")
    )
    
    # Utworzenie głównego zadania
    main_task = task_manager.create_task(
        description=main_task_desc,
        task_type=TaskType.MAIN,
        level=0
    )
    
    print(f"📋 GŁÓWNE ZADANIE:\n{main_task_desc}\n")
    print(f"Rozpoczynanie przetwarzania...\n")
    
    # Przetwarzanie rekursywne
    orchestrator.process_task_recursive(main_task)
    
    # Zapisanie wszystkich wyników
    print("\n" + "="*80)
    print("ZAPISYWANIE WYNIKÓW...")
    print("="*80 + "\n")
    
    orchestrator.save_results(main_task)
    
    # Wyświetlenie statystyk
    print("\n" + "="*80)
    print("STATYSTYKI WYKONANIA")
    print("="*80 + "\n")
    
    orchestrator.print_statistics()
    
    # Przeglądanie zapisanych wyników
    print("\n" + "="*80)
    print("ZAPISANE WYNIKI")
    print("="*80)
    
    list_saved_tasks()
    
    # Szczegółowy raport
    print("\n" + "="*80)
    print("SZCZEGÓŁOWY RAPORT")
    print("="*80)
    
    view_detailed_report("0001")
    
    # Logi wykonania
    print("\n" + "="*80)
    print("LOGI WYKONANIA")
    print("="*80)
    
    list_execution_logs()
    
    print("\n" + "="*80)
    print("✅ DEMO UKOŃCZONE")
    print("="*80)
    print("\nWyniki zapisane w:")
    print("  📁 results/task_results/    - wyniki zadań")
    print("  📁 results/statistics/      - statystyki")
    print("  📁 results/execution_logs/  - logi wykonania")
    print()


if __name__ == "__main__":
    main()
