"""
Test detekcji duplikatów - pokazuje jak system eliminuje pokrywające się zadania
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
load_dotenv(dotenv_path=ROOT / "config" / ".env")

print(f"{Fore.CYAN}{'='*80}")
print(f"{Fore.CYAN}  Test Detekcji Duplikatów")
print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

provider = os.getenv("AI_PROVIDER", "openai")
api_key = os.getenv("API_KEY")
model = os.getenv("MODEL", "gpt-4o-mini")

print(f"{Fore.WHITE}Konfiguracja: {provider} | {model}{Style.RESET_ALL}\n")

# Zadanie które może generować duplikaty
task = "Przygotuj prosty raport o wydatkach firmy za ostatni kwartał."

print(f"{Fore.YELLOW}Zadanie:{Style.RESET_ALL}")
print(f"{task}\n")
print(f"{Fore.CYAN}Ten test pokaże jak system:")
print(f"  1. Dzieli zadanie na podzadania")
print(f"  2. Wykrywa i eliminuje duplikaty")
print(f"  3. Wykonuje tylko unikalne zadania{Style.RESET_ALL}\n")

task_manager = TaskManager()
orchestrator = MasterOrchestrator(
    task_manager=task_manager,
    api_key=api_key,
    provider=provider,
    model=model,
    max_recursion_depth=10
)

main_task = task_manager.create_task(
    description=task,
    task_type=TaskType.MAIN,
    level=0
)

print(f"{Fore.GREEN}Rozpoczynam przetwarzanie...{Style.RESET_ALL}\n")

try:
    success = orchestrator.process_task_recursive(main_task)
    
    print(f"\n{Fore.YELLOW}{'='*80}")
    print(f"{Fore.YELLOW}PODSUMOWANIE")
    print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}\n")
    
    # Statystyki
    all_tasks = list(task_manager.tasks.values())
    total = len(all_tasks)
    verified = len([t for t in all_tasks if t.is_verified()])
    
    print(f"{Fore.WHITE}Statystyki:")
    print(f"  • Wszystkich zadań: {total}")
    print(f"  • Zweryfikowanych: {verified}")
    print(f"  • Sukces: {'TAK ✓' if success else 'NIE ✗'}{Style.RESET_ALL}\n")
    
    # Hierarchia
    print(f"{Fore.CYAN}Hierarchia zadań:{Style.RESET_ALL}")
    task_manager.print_hierarchy()
    
    # Wynik
    if main_task.result:
        print(f"\n{Fore.GREEN}Wynik końcowy:{Style.RESET_ALL}")
        result_preview = main_task.result[:400] + "..." if len(main_task.result) > 400 else main_task.result
        print(result_preview)
    
    print()
    
except Exception as e:
    print(f"\n{Fore.RED}Błąd: {e}{Style.RESET_ALL}")
    import traceback
    traceback.print_exc()
