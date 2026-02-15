"""
Główny program - System wieloagentowy z rekursywną dekompozycją zadań
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cad_ai.task_manager import TaskManager, TaskType, TaskStatus
from cad_ai.agents import MasterOrchestrator

init(autoreset=True)


def print_banner():
    """Wyświetla banner programu"""
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}  System Wieloagentowy z Rekursywną Dekompozycją Zadań")
    print(f"{Fore.CYAN}  Hierarchiczny system AI do analizy i wykonywania złożonych zadań")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")


def print_summary(task_manager: TaskManager, main_task_id: str):
    """Wyświetla podsumowanie wykonania"""
    print(f"\n{Fore.YELLOW}{'='*80}")
    print(f"{Fore.YELLOW}PODSUMOWANIE WYKONANIA")
    print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}\n")
    
    # Statystyki
    all_tasks = list(task_manager.tasks.values())
    total_tasks = len(all_tasks)
    verified_tasks = len([t for t in all_tasks if t.status == TaskStatus.VERIFIED])
    completed_tasks = len([t for t in all_tasks if t.status == TaskStatus.COMPLETED])
    failed_tasks = len([t for t in all_tasks if t.status == TaskStatus.FAILED])
    
    print(f"{Fore.WHITE}Statystyki:")
    print(f"  • Łączna liczba zadań: {total_tasks}")
    print(f"  • Zadania zweryfikowane: {Fore.GREEN}{verified_tasks}{Fore.WHITE}")
    print(f"  • Zadania ukończone: {Fore.BLUE}{completed_tasks}{Fore.WHITE}")
    print(f"  • Zadania nieudane: {Fore.RED}{failed_tasks}{Fore.WHITE}")
    
    # Hierarchia zadań
    print(f"\n{Fore.WHITE}Hierarchia zadań:")
    task_manager.print_hierarchy()
    
    # Wynik głównego zadania
    main_task = task_manager.get_task(main_task_id)
    if main_task and main_task.result:
        print(f"\n{Fore.GREEN}{'='*80}")
        print(f"{Fore.GREEN}WYNIK KOŃCOWY:")
        print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
        print(f"\n{main_task.result}\n")
        
        if main_task.verification_result:
            verification = main_task.verification_result
            print(f"{Fore.MAGENTA}{'='*80}")
            print(f"{Fore.MAGENTA}WERYFIKACJA:")
            print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
            print(f"Status: {Fore.GREEN if verification['passed'] else Fore.RED}{'PASS' if verification['passed'] else 'FAIL'}{Style.RESET_ALL}")
            print(f"Ocena: {verification['score']}/10.0")
            print(f"Feedback: {verification['feedback']}")
            if verification['issues']:
                print(f"Problemy: {', '.join(verification['issues'])}")
            print()


def main():
    """Główna funkcja programu"""
    # Załaduj zmienne środowiskowe z głównego katalogu projektu
    load_dotenv(dotenv_path=ROOT / ".env")
    
    # Sprawdź konfigurację
    provider = os.getenv("AI_PROVIDER", "openai")
    api_key = os.getenv("API_KEY")
    model = os.getenv("MODEL", "gpt-4o-mini")
    
    if provider in ["openai", "openrouter"] and not api_key:
        print(f"{Fore.RED}BŁĄD: Brak klucza API dla providera {provider}!")
        print(f"{Fore.YELLOW}Ustaw zmienną API_KEY w pliku .env")
        print(f"{Fore.YELLOW}Przykład: API_KEY=sk-xxx...{Style.RESET_ALL}")
        sys.exit(1)
    
    if provider == "ollama":
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        print(f"{Fore.CYAN}Używam Ollama pod adresem: {ollama_url}{Style.RESET_ALL}")
    
    print_banner()
    
    # Przykładowe zadanie główne
    main_goal = """Stwórz kompletny plan i wykonaj analizę dla uruchomienia małego sklepu internetowego.
Obejmuje to: analizę rynku, wybór platformy e-commerce, strategię marketingową, logistykę 
i obsługę klienta. Każdy aspekt powinien być szczegółowo omówiony."""
    
    print(f"{Fore.WHITE}Zadanie główne:")
    print(f"{Fore.CYAN}{main_goal}{Style.RESET_ALL}\n")
    
    response = input(f"{Fore.YELLOW}Czy kontynuować z tym zadaniem? (t/n, lub wpisz własne): {Style.RESET_ALL}")
    
    if response.lower() == 'n':
        print("Program zakończony.")
        return
    elif response.lower() != 't':
        main_goal = response
    
    # Konfiguracja
    MAX_RECURSION = 10  # Safety limit przeciw nieskończonej rekursji
    
    print(f"\n{Fore.WHITE}Konfiguracja:")
    print(f"  • Dostawca AI: {Fore.CYAN}{provider}{Fore.WHITE}")
    print(f"  • Model: {Fore.CYAN}{model}{Fore.WHITE}")
    print(f"  • System: {Fore.GREEN}Inteligentna ocena złożoności AI{Fore.WHITE}")
    print(f"  • Limit rekursji (safety): {MAX_RECURSION}")
    print(f"  • Liczba agentów wykonawczych: 5{Style.RESET_ALL}\n")
    
    input(f"{Fore.YELLOW}Naciśnij Enter aby rozpocząć...{Style.RESET_ALL}")
    
    # Inicjalizacja systemu
    task_manager = TaskManager()
    orchestrator = MasterOrchestrator(
        task_manager=task_manager,
        api_key=api_key,
        provider=provider,
        model=model,
        max_recursion_depth=MAX_RECURSION,
        persistence_dir=str(ROOT / "results")
    )
    
    # Utwórz zadanie główne
    main_task = task_manager.create_task(
        description=main_goal,
        task_type=TaskType.MAIN,
        level=0
    )
    
    print(f"\n{Fore.GREEN}System uruchomiony. Rozpoczynam przetwarzanie...{Style.RESET_ALL}\n")
    
    # Przetwórz zadanie
    try:
        success = orchestrator.process_task_recursive(main_task)
        
        # Wyświetl statystyki dekompozycji
        orchestrator.print_statistics()
        
        # Zapisz rezultaty
        orchestrator.save_results(main_task)
        
        # Wyświetl podsumowanie
        print_summary(task_manager, main_task.id)
        
        if success:
            print(f"{Fore.GREEN}✓ Zadanie główne wykonane i zweryfikowane pomyślnie!{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}✗ Zadanie główne nie zostało ukończone pomyślnie.{Style.RESET_ALL}\n")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Program przerwany przez użytkownika.{Style.RESET_ALL}")
        print_summary(task_manager, main_task.id)
    except Exception as e:
        print(f"\n{Fore.RED}Błąd: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
