"""
Test inteligentnej oceny złożoności - pokazuje jak system SAM decyduje o podziale
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
print(f"{Fore.CYAN}  Test Inteligentnej Oceny Złożoności")
print(f"{Fore.CYAN}  System SAM decyduje o głębokości rekursji!")
print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

provider = os.getenv("AI_PROVIDER", "openai")
api_key = os.getenv("API_KEY")
model = os.getenv("MODEL", "gpt-4o-mini")

print(f"{Fore.WHITE}Konfiguracja: {provider} | {model}{Style.RESET_ALL}")
print(f"{Fore.GREEN}System: Inteligentna ocena - BRAK sztywnych limitów!{Style.RESET_ALL}\n")

# Zadanie o średniej złożoności
task = "Przygotuj prosty przewodnik jak założyć blog."

print(f"{Fore.YELLOW}Zadanie:{Style.RESET_ALL}")
print(f"{task}\n")
print(f"{Fore.CYAN}System będzie:")
print(f"  ✓ Oceniać każde zadanie pod kątem złożoności")
print(f"  ✓ Decydować czy dzielić czy wykonać bezpośrednio")
print(f"  ✓ Automatycznie dostosowywać głębokość rekursji")
print(f"  ✓ Wyświetlać szczegółowe statystyki{Style.RESET_ALL}\n")

task_manager = TaskManager()
orchestrator = MasterOrchestrator(
    task_manager=task_manager,
    api_key=api_key,
    provider=provider,
    model=model,
    max_recursion_depth=10  # Safety limit, ale system zazwyczaj przestanie wcześniej
)

main_task = task_manager.create_task(
    description=task,
    task_type=TaskType.MAIN,
    level=0
)

print(f"{Fore.GREEN}Rozpoczynam inteligentne przetwarzanie...{Style.RESET_ALL}\n")

try:
    success = orchestrator.process_task_recursive(main_task)
    
    # Statystyki dekompozycji
    orchestrator.print_statistics()
    
    print(f"\n{Fore.YELLOW}{'='*80}")
    print(f"{Fore.YELLOW}WYNIK")
    print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}\n")
    
    # Podsumowanie
    all_tasks = list(task_manager.tasks.values())
    total = len(all_tasks)
    verified = len([t for t in all_tasks if t.is_verified()])
    
    print(f"{Fore.WHITE}Podsumowanie:")
    print(f"  • Wszystkich zadań: {total}")
    print(f"  • Zweryfikowanych: {verified}")
    print(f"  • Status: {'SUKCES ✓' if success else 'BŁĄD ✗'}{Style.RESET_ALL}\n")
    
    # Hierarchia
    print(f"{Fore.CYAN}Hierarchia zadań:{Style.RESET_ALL}")
    task_manager.print_hierarchy()
    
    # Wynik końcowy
    if main_task.result:
        print(f"\n{Fore.GREEN}{'='*80}")
        print(f"{Fore.GREEN}WYNIK KOŃCOWY:")
        print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}\n")
        result_preview = main_task.result[:600] + "..." if len(main_task.result) > 600 else main_task.result
        print(result_preview)
    
    print()
    
except Exception as e:
    print(f"\n{Fore.RED}Błąd: {e}{Style.RESET_ALL}")
    import traceback
    traceback.print_exc()
