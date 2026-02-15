"""
Moduł zarządzania zadaniami - hierarchiczna struktura zadań
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Status zadania"""
    CREATED = "created"
    DECOMPOSED = "decomposed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VERIFIED = "verified"
    FAILED = "failed"


class TaskType(Enum):
    """Typ zadania"""
    MAIN = "main"
    SUBTASK = "subtask"
    ATOMIC = "atomic"


@dataclass
class Task:
    """Reprezentacja pojedynczego zadania"""
    id: str
    description: str
    task_type: TaskType
    status: TaskStatus = TaskStatus.CREATED
    level: int = 0
    parent_id: Optional[str] = None
    subtasks: List['Task'] = field(default_factory=list)
    result: Optional[str] = None
    verification_result: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_subtask(self, subtask: 'Task'):
        """Dodaje podzadanie"""
        self.subtasks.append(subtask)
        
    def is_completed(self) -> bool:
        """Sprawdza czy zadanie jest ukończone"""
        return self.status in [TaskStatus.COMPLETED, TaskStatus.VERIFIED]
    
    def is_verified(self) -> bool:
        """Sprawdza czy zadanie jest zweryfikowane"""
        return self.status == TaskStatus.VERIFIED
    
    def to_dict(self) -> Dict[str, Any]:
        """Konwertuje zadanie do słownika"""
        return {
            'id': self.id,
            'description': self.description,
            'type': self.task_type.value,
            'status': self.status.value,
            'level': self.level,
            'parent_id': self.parent_id,
            'result': self.result,
            'verification': self.verification_result,
            'subtasks_count': len(self.subtasks)
        }


class TaskManager:
    """Manager do zarządzania hierarchią zadań"""
    
    def __init__(self, persistence_manager=None):
        self.tasks: Dict[str, Task] = {}
        # Załaduj counter z istniejących zadań
        if persistence_manager:
            self.task_counter = persistence_manager.get_next_task_counter()
        else:
            self.task_counter = 0
        
    def create_task(self, description: str, task_type: TaskType, 
                   level: int = 0, parent_id: Optional[str] = None) -> Task:
        """Tworzy nowe zadanie"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter:04d}"
        
        task = Task(
            id=task_id,
            description=description,
            task_type=task_type,
            level=level,
            parent_id=parent_id
        )
        
        self.tasks[task_id] = task
        
        # Dodaj jako podzadanie do rodzica
        if parent_id and parent_id in self.tasks:
            self.tasks[parent_id].add_subtask(task)
            
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Pobiera zadanie po ID"""
        return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: TaskStatus):
        """Aktualizuje status zadania"""
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            
    def update_task_result(self, task_id: str, result: str):
        """Aktualizuje wynik zadania"""
        if task_id in self.tasks:
            self.tasks[task_id].result = result
            
    def update_verification(self, task_id: str, verification: Dict[str, Any]):
        """Aktualizuje wynik weryfikacji zadania"""
        if task_id in self.tasks:
            self.tasks[task_id].verification_result = verification
            
    def get_all_tasks_by_level(self, level: int) -> List[Task]:
        """Pobiera wszystkie zadania z danego poziomu"""
        return [task for task in self.tasks.values() if task.level == level]
    
    def get_subtasks(self, task_id: str) -> List[Task]:
        """Pobiera podzadania danego zadania"""
        task = self.get_task(task_id)
        return task.subtasks if task else []
    
    def print_hierarchy(self, task_id: Optional[str] = None, indent: int = 0):
        """Wyświetla hierarchię zadań"""
        if task_id is None:
            # Wyświetl zadania główne (bez rodzica)
            root_tasks = [t for t in self.tasks.values() if t.parent_id is None]
            for task in root_tasks:
                self.print_hierarchy(task.id, indent)
        else:
            task = self.get_task(task_id)
            if task:
                prefix = "  " * indent
                status_symbol = self._get_status_symbol(task.status)
                print(f"{prefix}{status_symbol} [{task.id}] {task.description[:60]}...")
                
                for subtask in task.subtasks:
                    self.print_hierarchy(subtask.id, indent + 1)
    
    def _get_status_symbol(self, status: TaskStatus) -> str:
        """Zwraca symbol dla statusu"""
        symbols = {
            TaskStatus.CREATED: "○",
            TaskStatus.DECOMPOSED: "◐",
            TaskStatus.IN_PROGRESS: "◑",
            TaskStatus.COMPLETED: "●",
            TaskStatus.VERIFIED: "✓",
            TaskStatus.FAILED: "✗"
        }
        return symbols.get(status, "?")
