"""
Szybki test - minimalna wersja
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cad_ai.task_manager import TaskManager, TaskType
from cad_ai.agents import MasterOrchestrator

init(autoreset=True)
# Załaduj zmienne środowiskowe z głównego katalogu projektu
load_dotenv(dotenv_path=ROOT / ".env")

print(f"{Fore.CYAN}Test Szybki - System Wieloagentowy{Style.RESET_ALL}\n")

provider = os.getenv("AI_PROVIDER", "openai")
api_key = os.getenv("API_KEY")
model = os.getenv("MODEL", "gpt-4o-mini")

print(f"Provider: {provider} | Model: {model}\n")

# Bardzo proste zadanie
task = "Zaplanuj krótki wypad na weekend do gór dla 2 osób."

print(f"Zadanie: {task}\n")

task_manager = TaskManager()
orchestrator = MasterOrchestrator(
    task_manager=task_manager,
    api_key=api_key,
    provider=provider,
    model=model,
    max_recursion_depth=10,
    persistence_dir=str(ROOT / "results")
)

main_task = task_manager.create_task(
    description=task,
    task_type=TaskType.MAIN,
    level=0
)

print(f"{Fore.GREEN}Start...{Style.RESET_ALL}\n")

success = orchestrator.process_task_recursive(main_task)

print(f"\n{Fore.YELLOW}{'='*80}{Style.RESET_ALL}")
print(f"{Fore.YELLOW}WYNIK{Style.RESET_ALL}")
print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}\n")

# Statystyki
all_tasks = list(task_manager.tasks.values())
print(f"Liczba zadań: {len(all_tasks)}")
print(f"Zweryfikowane: {len([t for t in all_tasks if t.is_verified()])}\n")

# Hierarchia
task_manager.print_hierarchy()

# Wynik
if main_task.result:
    print(f"\n{Fore.GREEN}Wynik końcowy:{Style.RESET_ALL}")
    print(main_task.result)
    
print(f"\n{Fore.GREEN if success else Fore.RED}Status: {'SUKCES ✓' if success else 'BŁĄD ✗'}{Style.RESET_ALL}\n")
