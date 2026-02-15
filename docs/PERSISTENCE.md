# 📦 System Persistencji Wyników

## Przegląd

System persistencji pozwala na zapisywanie i zarządzanie wynikami hierarchicznej dekompozycji zadań. Wszystkie rezultaty są przechowywane w strukturalnych plikach JSON oraz raportach tekstowych.

## 📁 Struktura katalogów

```
results/
├── task_results/           # Wyniki poszczególnych zadań
│   ├── task_0001_result.json
│   ├── task_0001_detailed_report.json
│   ├── task_0001_report.txt
│   ├── task_0001_hierarchy.json
│   └── ...
├── statistics/             # Statystyki dekompozycji
│   ├── task_0001_decomposition_stats.json
│   └── ...
└── execution_logs/         # Logi wykonania
    ├── summary_20241207_143022.json
    └── ...
```

## 🔧 Komponenty

### 1. **PersistenceManager** (`persistence.py`)

Klasa odpowiadająca za zarządzanie wszystkimi aspektami persistencji.

#### Metody zapisu:

```python
# Zapisz wynik pojedynczego zadania
save_task_result(task_id: str, status: str, description: str, result: str, verification=None)

# Zapisz szczegółowy raport
save_detailed_report(task_id: str, report_data: dict)

# Eksportuj jako raport tekstowy
export_as_text_report(task_id: str, report_data: dict)

# Zapisz hierarchię zadań
save_task_hierarchy(task_id: str, hierarchy_data: dict)

# Zapisz statystyki dekompozycji
save_decomposition_stats(task_id: str, stats: dict)

# Zapisz podsumowanie wykonania
save_execution_summary(task_id: str, summary: dict)
```

#### Metody odczytu:

```python
# Załaduj wynik zadania
load_task_result(task_id: str) -> dict

# Wyświetl listę wszystkich wyników
list_saved_results() -> list

# Wyświetl logi wykonania
list_execution_logs() -> list

# Pobierz podsumowanie statystyk
get_statistics_summary() -> dict

# Wyświetl streszczenie persistencji
print_summary()
```

### 2. **MasterOrchestrator** - integracja z persistencją

```python
from agents import MasterOrchestrator, Task

orchestrator = MasterOrchestrator(
    num_executors=5,
    max_recursion_depth=10,
    persistence_dir="results"  # Włącz persistencję
)

main_task = Task(id="0001", description="...", type="MAIN", level=0)
orchestrator.process_task_recursive(main_task)

# Zapisz wszystkie wyniki
orchestrator.save_results(main_task)
```

### 3. **Results Viewer** (`results_viewer.py`)

Narzędzie do przeglądania i analizy zapisanych wyników.

```python
from results_viewer import (
    list_saved_tasks,
    view_task_result,
    view_detailed_report,
    view_text_report,
    list_execution_logs
)

# Wyświetl listę wszystkich zadań
list_saved_tasks()

# Wyświetl wynik konkretnego zadania
view_task_result("0001")

# Wyświetl szczegółowy raport
view_detailed_report("0001")

# Wyświetl raport tekstowy
view_text_report("0001")

# Wyświetl ostatnie logi
list_execution_logs()
```

## 📊 Formaty danych

### task_result.json
```json
{
  "id": "0001",
  "description": "Główne zadanie",
  "type": "MAIN",
  "level": 0,
  "status": "VERIFIED",
  "result": "Wynik zadania...",
  "verification": {
    "passed": true,
    "score": 9.5,
    "feedback": "Doskonale opracowane"
  },
  "timestamp": "2024-12-07T14:30:22"
}
```

### detailed_report.json
```json
{
  "task_id": "0001",
  "timestamp": "2024-12-07T14:30:22",
  "execution_info": {
    "execution_time_seconds": 45.3,
    "status": "completed"
  },
  "task_summary": {
    "total_created": 15,
    "decomposed": 8,
    "executed_directly": 7,
    "verified": 12,
    "failed": 0
  },
  "statistics": {
    "decomposed": 8,
    "executed_directly": 7,
    "max_level_reached": 2
  },
  "final_result": "Pełny wynik zadania..."
}
```

### decomposition_stats.json
```json
{
  "task_id": "0001",
  "timestamp": "2024-12-07T14:30:22",
  "total_tasks": 15,
  "decomposed_tasks": 8,
  "directly_executed": 7,
  "max_depth": 2,
  "avg_execution_time": 3.02,
  "total_execution_time": 45.3,
  "by_level": {
    "0": 1,
    "1": 8,
    "2": 6
  }
}
```

## 🚀 Przykłady użycia

### 1. Uruchomienie demo z persistencją

```bash
python demo_persistence.py
```

Wynik:
- Przetwarza główne zadanie
- Zapisuje wszystkie wyniki do `results/`
- Wyświetla statystyki i raporty
- Pokazuje strukturę zapisanych plików

### 2. Przeglądanie zapisanych wyników

```python
from results_viewer import list_saved_tasks, view_detailed_report

# Lista wszystkich zadań
list_saved_tasks()

# Szczegółowy raport
view_detailed_report("0001")
```

### 3. Analiza statystyk

```python
import json
from pathlib import Path

stats_path = Path("results/statistics/task_0001_decomposition_stats.json")
with open(stats_path) as f:
    stats = json.load(f)

print(f"Całkowite zadania: {stats['total_tasks']}")
print(f"Maksymalna głębokość: {stats['max_depth']}")
print(f"Czas całkowity: {stats['total_execution_time']:.2f}s")
```

### 4. Załadowanie i wznowienie

```python
from persistence import PersistenceManager

pm = PersistenceManager("results")

# Załaduj poprzedni wynik
result = pm.load_task_result("0001")
print(result['result'])

# Załaduj statystyki
stats = pm.get_statistics_summary()
print(stats)
```

## 📈 Analiza wydajności

### Śledzenie czasu wykonania

```python
# MasterOrchestrator automatycznie śledzuje czas
stats = orchestrator.statistics
print(f"Maksymalny poziom: {stats['max_level_reached']}")
print(f"Zadań podzielonych: {stats['decomposed']}")
print(f"Zadań wykonanych bezpośrednio: {stats['executed_directly']}")
```

### Metryki w raportach

- **Execution Time**: Czas całkowity wykonania w sekundach
- **Task Distribution**: Rozkład zadań po poziomach
- **Success Rate**: Procent zadań zweryfikowanych pozytywnie
- **Complexity Distribution**: Rozkład zadań po poziomach złożoności

## 🔍 Wyszukiwanie i filtrowanie

### Znalezienie wszystkich zweryfikowanych zadań

```python
from pathlib import Path
import json

results_dir = Path("results/task_results")
for result_file in results_dir.glob("*_result.json"):
    with open(result_file) as f:
        data = json.load(f)
        if data['verification']['passed']:
            print(f"✓ {data['id']}: {data['description']}")
```

### Znalezienie najmniej wykonanego poziomu

```python
from persistence import PersistenceManager

pm = PersistenceManager("results")
all_stats = pm.get_statistics_summary()

for task_id, stats in all_stats.items():
    by_level = stats['by_level']
    min_level = min(by_level, key=by_level.get)
    print(f"Najmniej zadań na poziomie {min_level}")
```

## ⚠️ Ograniczenia i uwagi

1. **Rozmiar plików**: Bardzo duże raporty mogą zajmować dużo miejsca na dysku
2. **Liczba plików**: Wiele małych plików JSON może spowolnić system plików
3. **Brak bazy danych**: System używa JSON, co jest wolniejsze niż dedykowana baza danych
4. **Brak indeksowania**: Szukanie wymaga iteracji po wszystkich plikach

## 🔄 Przyszłe usprawnienia

- [ ] Wsparcie dla bazy danych SQLite
- [ ] Kompresja starych raportów
- [ ] API REST do dostępu do wyników
- [ ] Dashboard webowy do wizualizacji
- [ ] Eksport do CSV/Excel
- [ ] Synchronizacja z chmurą

## 📝 Notatki implementacyjne

### Threads i persistencja

Jeśli używasz wielowątkowości (co jest potrzebne dla `ExecutorAgent` x5), upewnij się, że:
- Każdy wątek ma swój unikatowy ID zadania
- PersistenceManager jest thread-safe
- Nie ma konfliktów przy pisaniu do tego samego pliku

### Bezpieczeństwo

- Nie przechowuj danych wrażliwych w wynikach (API keys, hasła)
- Ograniczy dostęp do katalogu `results/` na serwerach produkcyjnych
- Regularne kopie bezpieczeństwa katalogów

### Optymalizacja

Aby uniknąć problemów z wydajnością:
1. Archiwizuj stare wyniki (>30 dni)
2. Usuń tymczasowe pliki JSON
3. Rozważ migrację do bazy danych dla dużych projektów

---

**Wersja**: 1.0  
**Data**: 2024-12-07  
**Status**: Production Ready
