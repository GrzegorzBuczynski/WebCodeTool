"""
Utility do zarządzania i przeglądania zapisanych wyników
"""
import json
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)


def list_saved_tasks():
    """Wyświetla listę wszystkich zapisanych zadań"""
    results_dir = Path("results")
    
    if not results_dir.exists():
        print(f"{Fore.YELLOW}Brak zapisanych wyników.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}ZAPISANE WYNIKI")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    result_files = list(results_dir.glob("task_*/result.json"))
    
    if not result_files:
        print(f"{Fore.YELLOW}Brak zapisanych wyników.{Style.RESET_ALL}")
        return
    
    for filepath in sorted(result_files):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            task_id = data.get("id")
            status = data.get("status")
            description = data.get("description", "")[:60]
            verified = "✓" if data.get("verification", {}).get("passed") else "✗"
            
            status_color = Fore.GREEN if status == "verified" else Fore.YELLOW
            
            print(f"{status_color}[{task_id}] {verified} {description}...{Style.RESET_ALL}")
    
    print()


def view_task_result(task_id: str):
    """Wyświetla szczegółowe wyniki zadania"""
    result_path = Path(f"results/{task_id}/result.json")
    
    if not result_path.exists():
        print(f"{Fore.RED}Nie znaleziono wyniku dla {task_id}{Style.RESET_ALL}")
        return
    
    with open(result_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}WYNIK ZADANIA {task_id}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    print(f"{Fore.WHITE}Opis:{Style.RESET_ALL}")
    print(f"  {data.get('description')}\n")
    
    print(f"{Fore.WHITE}Status: {Fore.YELLOW}{data.get('status')}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Typ: {Fore.YELLOW}{data.get('type')}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Poziom: {Fore.YELLOW}{data.get('level')}{Style.RESET_ALL}")
    
    if data.get('verification'):
        v = data['verification']
        print(f"\n{Fore.WHITE}Weryfikacja:{Style.RESET_ALL}")
        print(f"  Status: {Fore.GREEN if v.get('passed') else Fore.RED}{'PASS' if v.get('passed') else 'FAIL'}{Style.RESET_ALL}")
        print(f"  Ocena: {v.get('score', 0)}/10.0")
        print(f"  Feedback: {v.get('feedback', '')}")
    
    if data.get('result'):
        print(f"\n{Fore.GREEN}WYNIK:{Style.RESET_ALL}")
        print(f"{data['result']}\n")


def view_detailed_report(task_id: str):
    """Wyświetla szczegółowy raport"""
    report_path = Path(f"results/{task_id}/detailed_report.json")
    
    if not report_path.exists():
        print(f"{Fore.RED}Nie znaleziono raportu dla {task_id}{Style.RESET_ALL}")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}RAPORT SZCZEGÓŁOWY {task_id}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    exec_info = data.get('execution_info', {})
    print(f"{Fore.WHITE}Informacje o wykonaniu:{Style.RESET_ALL}")
    print(f"  Timestamp: {exec_info.get('timestamp')}")
    print(f"  Czas: {exec_info.get('execution_time_seconds', 0):.2f}s")
    
    stats = data.get('task_summary', {})
    print(f"\n{Fore.WHITE}Podsumowanie:{Style.RESET_ALL}")
    print(f"  Wszystkich zadań: {stats.get('total_created', 0)}")
    print(f"  Zweryfikowanych: {stats.get('verified', 0)}")
    print(f"  Nieudanych: {stats.get('failed', 0)}")
    
    dec_stats = data.get('statistics', {})
    print(f"\n{Fore.WHITE}Statystyki dekompozycji:{Style.RESET_ALL}")
    print(f"  Podzielonych: {dec_stats.get('decomposed', 0)}")
    print(f"  Wykonanych bezpośrednio: {dec_stats.get('executed_directly', 0)}")
    print(f"  Maksymalny poziom: {dec_stats.get('max_level_reached', 0)}")
    
    if data.get('final_result'):
        print(f"\n{Fore.GREEN}WYNIK KOŃCOWY:{Style.RESET_ALL}")
        result_preview = data['final_result'][:500] + "..." if len(data['final_result']) > 500 else data['final_result']
        print(f"{result_preview}\n")


def view_text_report(task_id: str):
    """Wyświetla tekstowy raport"""
    report_path = Path(f"results/{task_id}/report.txt")
    
    if not report_path.exists():
        print(f"{Fore.RED}Nie znaleziono raportu tekstowego dla {task_id}{Style.RESET_ALL}")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"{Fore.CYAN}{content}{Style.RESET_ALL}")


def list_execution_logs():
    """Wyświetla listę logów wykonania"""
    results_dir = Path("results")
    if not results_dir.exists():
        print(f"{Fore.YELLOW}Brak logów wykonania.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}LOGI WYKONANIA")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    logs = []
    for task_dir in results_dir.glob("task_*"):
        logs_dir = task_dir / "execution_logs"
        if logs_dir.exists():
            logs.extend(list(logs_dir.glob("summary_*.json")))
    logs = sorted(logs, reverse=True)[:10]
    
    for log_path in logs:
        with open(log_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            timestamp = data.get('timestamp')
            task_desc = data.get('task_description', '')[:50]
            exec_time = data.get('execution_time_seconds', 0)
            
            print(f"{Fore.YELLOW}[{timestamp}]{Style.RESET_ALL} {task_desc}... ({exec_time:.1f}s)")
    
    print()


if __name__ == "__main__":
    print(f"{Fore.CYAN}Narzędzia do przeglądania rezultatów{Style.RESET_ALL}\n")
    print("Dostępne funkcje:")
    print("  list_saved_tasks()     - lista wszystkich zadań")
    print("  view_task_result(id)   - wynik zadania")
    print("  view_detailed_report(id) - szczegółowy raport")
    print("  view_text_report(id)   - raport tekstowy")
    print("  list_execution_logs()  - ostatnie logi wykonania")
