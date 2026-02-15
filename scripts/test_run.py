"""
Skrypt testowy - uruchamia system z uproszczonym zadaniem
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
from cad_ai.persistence import PersistenceManager

init(autoreset=True)

# Załaduj zmienne środowiskowe z głównego katalogu projektu
load_dotenv(dotenv_path=ROOT / ".env")

print(f"{Fore.CYAN}{'='*80}")
print(f"{Fore.CYAN}  Test Systemu Wieloagentowego")
print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

# Konfiguracja
provider = os.getenv("AI_PROVIDER", "openai")
api_key = os.getenv("API_KEY")
model = os.getenv("MODEL", "gpt-4o-mini")

print(f"{Fore.WHITE}Konfiguracja:")
print(f"  • Dostawca AI: {Fore.CYAN}{provider}{Fore.WHITE}")
print(f"  • Model: {Fore.CYAN}{model}{Fore.WHITE}")
print(f"  • System: {Fore.GREEN}Inteligentna ocena złożoności{Fore.WHITE}")
print(f"  • Limit rekursji (safety): 10{Style.RESET_ALL}\n")

# Proste zadanie testowe (można nadpisać argumentem CLI)
default_task = "Zaplanuj prosty obiad dla 4 osób: zupa, drugie danie i deser."
cli_task = " ".join(sys.argv[1:]).strip()
test_task = cli_task or default_task

print(f"{Fore.YELLOW}Zadanie testowe:{Style.RESET_ALL}")
print(f"{test_task}\n")

# Inicjalizacja
persistence_manager = PersistenceManager(base_dir=str(ROOT / "results"))
task_manager = TaskManager(persistence_manager=persistence_manager)
orchestrator = MasterOrchestrator(
    task_manager=task_manager,
    api_key=api_key,
    provider=provider,
    model=model,
    max_recursion_depth=10,
    persistence_dir=str(ROOT / "results")
)

# Utwórz zadanie główne
main_task = task_manager.create_task(
    description=test_task,
    task_type=TaskType.MAIN,
    level=0
)

print(f"{Fore.GREEN}Rozpoczynam przetwarzanie...{Style.RESET_ALL}\n")

try:
    success = orchestrator.process_task_recursive(main_task)
    
    # Pokaż statystyki dekompozycji
    orchestrator.print_statistics()
    
    # Zapisz rezultaty
    orchestrator.save_results(main_task)
    
    print(f"\n{Fore.YELLOW}{'='*80}")
    print(f"{Fore.YELLOW}WYNIK KOŃCOWY")
    print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}\n")
    
    # Hierarchia
    print(f"{Fore.WHITE}Hierarchia zadań:{Style.RESET_ALL}")
    task_manager.print_hierarchy()
    
    # Wynik
    if main_task.result:
        print(f"\n{Fore.GREEN}Wynik:{Style.RESET_ALL}")
        print(main_task.result[:500] + "..." if len(main_task.result) > 500 else main_task.result)
    
    # Status
    status_color = Fore.GREEN if success else Fore.RED
    status_text = "SUKCES" if success else "BŁĄD"
    print(f"\n{status_color}Status: {status_text}{Style.RESET_ALL}\n")
    
except Exception as e:
    print(f"\n{Fore.RED}Błąd: {e}{Style.RESET_ALL}")
    import traceback
    traceback.print_exc()
