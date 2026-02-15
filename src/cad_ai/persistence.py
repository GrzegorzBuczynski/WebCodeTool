"""
Moduł persistencji - przechowywanie wyników w plikach
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from .task_manager import Task, TaskStatus, TaskType


class PersistenceManager:
    """Manager do zarządzania persistencją wyników"""
    
    def __init__(self, base_dir: str = "results"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def get_next_task_counter(self) -> int:
        """Pobiera następny licznik zadań na podstawie istniejących folderów"""
        max_counter = 0
        for task_dir in self.base_dir.iterdir():
            if task_dir.is_dir() and task_dir.name.startswith("task_"):
                try:
                    counter = int(task_dir.name.split("_")[1])
                    max_counter = max(max_counter, counter)
                except (ValueError, IndexError):
                    pass
        return max_counter
    
    def _get_task_dir(self, task_id: str) -> Path:
        """Zwraca katalog dla konkretnego zadania"""
        task_dir = self.base_dir / task_id
        task_dir.mkdir(exist_ok=True)
        return task_dir
    
    def save_task_output(self, task_id: str, output: str) -> str:
        """Zapisuje sam output zadania (czysty wynik)"""
        task_dir = self._get_task_dir(task_id)
        filepath = task_dir / "output.txt"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output)
        
        return str(filepath)
    
    def save_task_result(self, task: Task, execution_time: float = 0.0) -> str:
        """Zapisuje wynik pojedynczego zadania"""
        task_dir = self._get_task_dir(task.id)
        
        task_data = {
            "id": task.id,
            "description": task.description,
            "type": task.task_type.value,
            "status": task.status.value,
            "level": task.level,
            "result": task.result,
            "verification": task.verification_result,
            "subtasks_count": len(task.subtasks),
            "execution_time_seconds": execution_time,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "metadata": task.metadata
        }
        
        filename = "result.json"
        filepath = task_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def save_execution_summary(self, task_id: str, task_description: str, 
                              stats: Dict[str, Any], execution_time: float) -> str:
        """Zapisuje podsumowanie wykonania zadania głównego"""
        task_dir = self._get_task_dir(task_id)
        logs_dir = task_dir / "execution_logs"
        logs_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary = {
            "execution_id": f"{task_id}_{timestamp}",
            "task_id": task_id,
            "task_description": task_description,
            "timestamp": timestamp,
            "execution_time_seconds": execution_time,
            "statistics": stats
        }
        
        filename = f"summary_{timestamp}.json"
        filepath = logs_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def save_decomposition_stats(self, stats: Dict[str, Any], 
                                task_id: str) -> str:
        """Zapisuje statystyki dekompozycji"""
        task_dir = self._get_task_dir(task_id)
        
        stat_data = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "statistics": stats
        }
        
        filename = "stats.json"
        filepath = task_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stat_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def save_task_hierarchy(self, task: Task, task_manager) -> str:
        """Zapisuje hierarchię wszystkich zadań"""
        task_dir = self._get_task_dir(task.id)
        
        def task_to_dict(t: Task) -> Dict[str, Any]:
            return {
                "id": t.id,
                "description": t.description[:100],
                "type": t.task_type.value,
                "status": t.status.value,
                "level": t.level,
                "verified": t.is_verified(),
                "subtasks": [task_to_dict(st) for st in t.subtasks],
                "result_preview": t.result[:200] if t.result else None
            }
        
        hierarchy = {
            "main_task_id": task.id,
            "main_task_description": task.description,
            "total_tasks": len(task_manager.tasks),
            "hierarchy": task_to_dict(task),
            "timestamp": datetime.now().isoformat()
        }
        
        filename = "hierarchy.json"
        filepath = task_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(hierarchy, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def save_detailed_report(self, task: Task, task_manager, 
                            stats: Dict[str, Any], execution_time: float) -> str:
        """Zapisuje szczegółowy raport z wszystkimi informacjami"""
        task_dir = self._get_task_dir(task.id)
        
        def collect_all_tasks(t: Task, level: int = 0) -> List[Dict[str, Any]]:
            """Zbiera wszystkie zadania hierarchicznie"""
            tasks_list = [{
                "id": t.id,
                "level": t.level,
                "description": t.description,
                "type": t.task_type.value,
                "status": t.status.value,
                "verified": t.is_verified(),
                "result_length": len(t.result) if t.result else 0,
                "result_preview": (t.result[:300] + "...") if t.result and len(t.result) > 300 else t.result,
                "verification": t.verification_result,
                "subtasks_count": len(t.subtasks)
            }]
            
            for subtask in t.subtasks:
                tasks_list.extend(collect_all_tasks(subtask, level + 1))
            
            return tasks_list
        
        report = {
            "execution_info": {
                "timestamp": datetime.now().isoformat(),
                "execution_time_seconds": execution_time,
                "main_task_id": task.id,
                "main_task_description": task.description
            },
            "statistics": stats,
            "all_tasks": collect_all_tasks(task),
            "task_summary": {
                "total_created": len(task_manager.tasks),
                "verified": len([t for t in task_manager.tasks.values() if t.is_verified()]),
                "failed": len([t for t in task_manager.tasks.values() if t.status == TaskStatus.FAILED])
            },
            "final_result": task.result if task.result else None
        }
        
        filename = "detailed_report.json"
        filepath = task_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def load_task_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Ładuje zapisany wynik zadania"""
        filepath = self._get_task_dir(task_id) / "result.json"
        
        if not filepath.exists():
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_saved_results(self) -> List[Dict[str, Any]]:
        """Lista wszystkich zapisanych rezultatów"""
        results = []
        
        # Iteruj po folderach zadań
        for task_dir in self.base_dir.iterdir():
            if task_dir.is_dir() and task_dir.name not in ['statistics', 'execution_logs']:
                result_file = task_dir / "result.json"
                if result_file.exists():
                    with open(result_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        results.append({
                            "filename": result_file.name,
                            "task_id": data.get("id"),
                            "description": data.get("description"),
                            "status": data.get("status"),
                            "verified": data.get("verification", {}).get("passed") if data.get("verification") else False
                        })
        
        return results
    
    def list_execution_logs(self, limit: int = 10) -> List[str]:
        """Lista ostatnich logów wykonania"""
        logs = sorted(self.logs_dir.glob("summary_*.json"), reverse=True)[:limit]
        return [str(log) for log in logs]
    
    def get_statistics_summary(self) -> Dict[str, Any]:
        """Pobiera podsumowanie wszystkich statystyk"""
        results = self.list_saved_results()
        
        # Zlicz logi wykonania i statystyki z folderów task
        execution_logs = 0
        stats_files = 0
        
        for task_dir in self.base_dir.glob("task_*"):
            execution_logs += len(list((task_dir / "execution_logs").glob("summary_*.json"))) if (task_dir / "execution_logs").exists() else 0
            stats_files += 1 if (task_dir / "stats.json").exists() else 0
        
        summary = {
            "total_tasks_saved": len(results),
            "verified_tasks": len([r for r in results if r["verified"]]),
            "failed_tasks": len([r for r in results if r["status"] == "failed"]),
            "execution_logs": execution_logs,
            "stats_files": stats_files
        }
        
        return summary
    
    def export_as_text_report(self, task: Task, stats: Dict[str, Any], 
                             execution_time: float) -> str:
        """Eksportuje wynik jako tekst (dla łatwego czytania)"""
        task_dir = self._get_task_dir(task.id)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
================================================================================
RAPORT WYKONANIA ZADANIA
================================================================================

Data: {timestamp}
Czas wykonania: {execution_time:.2f} sekund

================================================================================
ZADANIE GŁÓWNE
================================================================================
ID: {task.id}
Opis: {task.description}
Status: {task.status.value}
Zweryfikowane: {"TAK" if task.is_verified() else "NIE"}

================================================================================
STATYSTYKI
================================================================================
Wszystkich zadań: {stats.get('total_tasks', 0)}
Podzielonych: {stats.get('decomposed', 0)}
Wykonanych bezpośrednio: {stats.get('executed_directly', 0)}
Maksymalny poziom: {stats.get('max_level_reached', 0)}

================================================================================
WYNIK
================================================================================
{task.result if task.result else "Brak wyniku"}

================================================================================
WERYFIKACJA
================================================================================
"""
        
        if task.verification_result:
            v = task.verification_result
            report += f"""
Status: {"PASS" if v.get('passed') else 'FAIL'}
Ocena: {v.get('score', 0)}/10.0
Feedback: {v.get('feedback', '')}
Problemy: {', '.join(v.get('issues', [])) if v.get('issues') else 'Brak'}
"""
        
        filename = "report.txt"
        filepath = task_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(filepath)
    
    def print_summary(self):
        """Wyświetla podsumowanie zapisanych plików"""
        from colorama import Fore, Style
        
        stats = self.get_statistics_summary()
        
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}PODSUMOWANIE PERSISTENCJI")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Ścieżka: {self.base_dir}")
        print(f"Zapisane wyniki: {stats['total_tasks_saved']}")
        print(f"Zweryfikowane: {stats['verified_tasks']}")
        print(f"Nieudane: {stats['failed_tasks']}")
        print(f"Logi wykonania: {stats['execution_logs']}")
        print(f"Pliki statystyk: {stats['stats_files']}{Style.RESET_ALL}\n")
