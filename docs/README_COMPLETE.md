# 🤖 Multi-Agent Task Decomposition System

## 📌 Przegląd projektu

Zaawansowany system AI do **hierarchicznej dekompozycji złożonych zadań** na mniejsze podzadania przy użyciu **wielu agentów wyspecjalizowanych**. System automatycznie decyduje, czy zadanie powinno być podzielone (na podstawie analizy złożoności i potencjalnego rozmiaru outputu) czy wykonane bezpośrednio.

### Kluczowe cechy

✨ **Inteligentna dekompozycja** - System analizuje złożoność i rozmiar outputu, aby zdecydować, czy podzielić zadanie  
🤖 **7 typów agentów** - Każdy agent ma specjalizowaną rolę  
🔄 **Rekursywne podzielanie** - Zadania mogą być dzielone na wiele poziomów (minimum 3)  
✅ **Weryfikacja wyników** - Każde zadanie jest sprawdzane przez agenta weryfikacji  
💾 **Persistencja wyników** - Wszystkie rezultaty zapisywane w strukturalnych plikach JSON  
🌐 **Wielowspórnikowa obsługa API** - OpenAI, OpenRouter, Ollama  
📊 **Szczegółowe raportowanie** - Logi, statystyki, hierarchia zadań

## 🏗️ Architektura systemu

```
┌─────────────────────────────────────────────────────────────┐
│                    MasterOrchestrator                        │
│  (Główny koordynator, śledzenie statystyk, persistencja)    │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │Complexity│ │Coordinator│ │Duplication│
  │Analyzer  │ │Agent      │ │Detector   │
  └──────────┘ └──────────┘ └──────────┘
        │            │            │
        │            ▼            │
        │      ┌──────────────────┘
        │      │
        └──────┼──────────────────────┐
               │                      │
        ┌──────▼─────┐          ┌─────▼──────┐
        │Executor     │          │Verification│
        │Agent (x5)   │          │Agent       │
        └─────────────┘          └────────────┘
```

## 🔧 Agenty w systemie

### 1. **BaseAgent**
- Klasa bazowa dla wszystkich agentów
- Zarządza komunikacją z LLM (OpenAI/OpenRouter/Ollama)
- Dynamiczna konfiguracja dostawcy API

### 2. **ComplexityAnalyzerAgent** ⭐ (Nowość!)
- **Główna funkcja**: Analizuje, czy zadanie powinno być podzielone
- Ocenia: `NISKA / ŚREDNIA / WYSOKA / BARDZO_WYSOKA` złożoność
- **Kluczowy czynnik**: Potencjalny rozmiar outputu (< 500 słów? → execute; > 5000 słów? → decompose)
- Zwraca: Liczbę podtasków (2-5) lub 0 (wykonaj bezpośrednio)

### 3. **CoordinatorAgent**
- Dzieli zadanie na dokładnie tyle podtasków, ile zasugerował ComplexityAnalyzer
- Tworzy hierar

chię zadań
- Przekazuje kontekst między poziomami

### 4. **DuplicationDetectorAgent**
- Identyfikuje nakładające się/zduplikowane zadania
- Eliminuje redundancję
- Unika wielokrotnego wykonywania tej samej pracy

### 5. **ExecutorAgent** (x5)
- 5 agentów pracujących równolegle
- Przydzielane metodą round-robin
- Wykonują rzeczywistą pracę (pisanie, analiza, itp.)
- Mogą wznowić przerwane zadania

### 6. **VerificationAgent**
- Sprawdza jakość wykonania zadania
- Ocenia: 0-10 punków
- Feedback: opisowy komentarz
- Decyduje: PASS / FAIL

### 7. **MasterOrchestrator**
- Koordynuje wszystkie procesy
- Śledzenie statystyk (total tasks, decomposed, executed_directly, max_level)
- Zarządzanie persistencją wyników
- Czas wykonania
- Hierarchia zadań

## 📋 API: Obsługa 3 dostawców

### OpenAI
```python
AI_PROVIDER=openai
API_KEY=sk-...
MODEL=gpt-4o-mini
```

### OpenRouter (rekomendowany - tańszy)
```python
AI_PROVIDER=openrouter
API_KEY=sk-or-v1-...
MODEL=meta-llama/llama-2-70b-chat
```

### Ollama (lokalnie)
```python
AI_PROVIDER=ollama
MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434/v1
```

## 📦 Struktura projektu

```
cad/
├── agents.py                 # Wszystkie definicje agentów
├── task_manager.py          # Zarządzanie hierarchią zadań
├── persistence.py           # System persistencji wyników
├── results_viewer.py        # Narzędzie do przeglądania wyników
├── main.py                  # Główny program interaktywny
├── demo_persistence.py      # Demo z persistencją
├── test_run.py             # Test podstawowy
├── test_duplication.py      # Test deduplikacji
├── test_intelligent.py      # Test inteligentnej analizy
├── quick_test.py           # Szybki test
├── requirements.txt        # Zależności
├── .env                    # Konfiguracja (nie commituj!)
├── .env.example            # Szablon konfiguracji
├── README.md               # Ten plik
├── PERSISTENCE.md          # Dokumentacja persistencji
└── results/                # Wyniki (generowane)
    ├── task_results/
    ├── statistics/
    └── execution_logs/
```

## 🚀 Szybki start

### 1. Instalacja

```bash
cd /home/grzegorz/Documents/programowanie/cad
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Konfiguracja

```bash
cp .env.example .env
# Edytuj .env z twoim API key i dostawcą
nano .env
```

### 3. Uruchomienie

```bash
# Demo z persistencją
python demo_persistence.py

# Program interaktywny
python main.py

# Test szybki
python quick_test.py

# Test z deduplikacją
python test_duplication.py

# Test inteligentnej analizy
python test_intelligent.py
```

## 📊 Przykład wyjścia

```
================================================================================
DEMONSTRACJA: Hierarchiczna dekompozycja zadań z persistencją
================================================================================

📋 GŁÓWNE ZADANIE:
Opisz proces budowy domu: planowanie, przygotowanie, fundament, ściany, dach, instalacje, wykończenie

Rozpoczynanie przetwarzania...

[BaseAgent] Kompleksowa analiza systemu AI...
[ComplexityAnalyzerAgent] Analizuję złożoność: WYSOKA | Output: BARDZO_DŁUGI
[CoordinatorAgent] Podzielę to na 4 subtasków
[ExecutorAgent#1] Wykonuję: Planowanie budowy domu
[ExecutorAgent#2] Wykonuję: Przygotowanie terenu i fundament
...
[VerificationAgent] Weryfikuję wynik - Ocena: 9.5/10 ✓

================================================================================
STATYSTYKI WYKONANIA
================================================================================

Całkowite zadania: 15
Zadania podzielone: 8
Zadania wykonane bezpośrednio: 7
Maksymalny poziom rekursji: 2
Zweryfikowane: 12
Nieudane: 0
Czas wykonania: 45.3 sekundy
```

## 🧪 Testy

### Test 1: Podstawowy (test_run.py)
```bash
python test_run.py
```
- Testuje proste zadanie: "Zaplanuj obiad"
- Powinno być zidentyfikowane jako NISKA złożoność
- Powinno być wykonane bez dekompozycji

### Test 2: Deduplikacja (test_duplication.py)
```bash
python test_duplication.py
```
- Tworzy zadania z nakładającymi się podtaskami
- Weryfikuje, że DuplicationDetectorAgent eliminuje duplikaty

### Test 3: Inteligentna analiza (test_intelligent.py)
```bash
python test_intelligent.py
```
- Testuje ComplexityAnalyzer z różnymi typami zadań
- Sprawdza czy decyzje o dekompozycji są poprawne

## 💾 Persistencja wyników

Wszystkie wyniki automatycznie zapisywane do `results/`:

```
results/
├── task_results/
│   ├── task_0001_result.json          # Wynik głównego zadania
│   ├── task_0001_detailed_report.json # Szczegółowy raport
│   ├── task_0001_report.txt           # Raport tekstowy
│   ├── task_0001_hierarchy.json       # Hierarchia zadań
│   └── ...
├── statistics/
│   ├── task_0001_decomposition_stats.json
│   └── ...
└── execution_logs/
    ├── summary_20241207_143022.json
    └── ...
```

### Przeglądanie wyników

```python
from results_viewer import list_saved_tasks, view_detailed_report

list_saved_tasks()           # Wyświetl listę
view_detailed_report("0001") # Szczegółowy raport
```

Więcej szczegółów: [PERSISTENCE.md](PERSISTENCE.md)

## 📈 Statystyki i metryki

System automatycznie śledzi:

- **Total Tasks**: Całkowita liczba utworzonych zadań
- **Decomposed**: Zadania które zostały podzielone
- **Executed Directly**: Zadania wykonane bez dekompozycji
- **Max Level Reached**: Maksymalna głębokość rekursji
- **Execution Time**: Całkowity czas w sekundach
- **Verification Rate**: Procent zweryfikowanych zadań

## 🔍 Inteligentna analiza złożoności

### Proces decyzyjny ComplexityAnalyzer:

1. **Analiza złożoności**: NISKA → ŚREDNIA → WYSOKA → BARDZO_WYSOKA
2. **Estymacja outputu**: < 500 słów (KRÓTKI) → ... → > 5000 słów (BARDZO_DŁUGI)
3. **Decyzja**: 
   - NISKA + KRÓTKI → Wykonaj bezpośrednio (0 subtasków)
   - WYSOKA + BARDZO_DŁUGI → Podziel na 4-5 subtasków
   - ŚREDNIA + ŚREDNI → Podziel na 2-3 subtasków

```python
# Przykład:
complexity = "WYSOKA"
output_size = "BARDZO_DŁUGI"  # > 5000 słów
# Wynik: Podziel na 4-5 subtasków
```

## ⚙️ Konfiguracja zaawansowana

### Zmiana liczby Executor Agentów

```python
orchestrator = MasterOrchestrator(
    num_executors=10,  # Zamiast domyślnych 5
    max_recursion_depth=15,  # Maksymalna głębokość
    persistence_dir="results"  # Gdzie zapisywać
)
```

### Własny context store

```python
orchestrator.context_store = {
    "user_domain": "medicina",
    "language": "pl",
    "style": "formal"
}
```

## 🐛 Debugowanie

### Włącz verbose logging

Edytuj plik i zmień `print()` na bardziej szczegółowe wyjście:

```python
# W agents.py
def log(self, message: str):
    print(f"{Fore.CYAN}[{self.__class__.__name__}] {message}{Style.RESET_ALL}")
    # Zaloguj też do pliku:
    with open("debug.log", "a") as f:
        f.write(f"[{self.__class__.__name__}] {message}\n")
```

### Sprawdź saved results

```bash
# Lista wszystkich zapisanych wyników
python -c "from results_viewer import list_saved_tasks; list_saved_tasks()"

# Szczegółowy raport
python -c "from results_viewer import view_detailed_report; view_detailed_report('0001')"
```

## 🚨 Rozwiązywanie problemów

### Problem: "API key not found"
```bash
# Sprawdź .env
cat .env

# Upewnij się, że istnieje:
echo "API_KEY=twoj_klucz" >> .env
```

### Problem: "Module not found"
```bash
# Zainstaluj zależności
pip install -r requirements.txt

# Sprawdź wersję Pythona
python --version  # Powinno być 3.8+
```

### Problem: "Ollama connection failed"
```bash
# Upewnij się, że Ollama jest uruchomiona
ollama serve

# W innym terminalu:
python main.py
```

### Problem: "Too many tasks / token limit"
```python
# Zmniejsz max_recursion_depth
orchestrator = MasterOrchestrator(
    max_recursion_depth=5,  # Zamiast 10
    ...
)
```

## 📚 Dodatkowe zasoby

- [Dokumentacja Persistencji](PERSISTENCE.md) - Szczegóły systemu zapisu wyników
- [OpenAI Docs](https://platform.openai.com/docs) - Dokumentacja OpenAI API
- [OpenRouter](https://openrouter.ai) - Alternatywny dostawca
- [Ollama](https://ollama.ai) - Lokalne modele

## 🎯 Roadmap - Przyszłe funkcjonalności

- [ ] **Database Backend** - SQLite zamiast JSON
- [ ] **Web Dashboard** - Wizualizacja wyników
- [ ] **API REST** - Do dostępu do wyników
- [ ] **Cost Tracking** - Śledzenie kosztów per API provider
- [ ] **Parallel Execution** - Rzeczywiste paralelne przetwarzanie
- [ ] **Caching** - Cache wyników powtarzających się zadań
- [ ] **Streaming Output** - Wyświetlanie wyników na żywo
- [ ] **Export to CSV/Excel** - Alternatywne formaty
- [ ] **Task Templates** - Szablony dla typowych zadań
- [ ] **Monitoring Dashboard** - Śledzenie real-time

## 🤝 Wkład i fejchy

Aby zaproponować nową funkcjonalność:

1. Utwórz issue opisujące idealnie co chcesz
2. Jeśli chcesz kodować: fork, branch, pull request
3. Upewnij się, że kod jest testowany

## 📜 Licencja

MIT License - Możesz używać swobodnie w projektach

## ✉️ Kontakt i wsparcie

Problem? Pytanie?
- Sprawdź [PERSISTENCE.md](PERSISTENCE.md) dla persistencji
- Przeglądaj istniejące testy
- Sprawdź `results/` po uruchomieniu programu

---

**Wersja**: 2.0  
**Status**: ✅ Production Ready  
**Data ostatniej aktualizacji**: 2024-12-07  
**Python**: 3.8+  
**Agenci**: 7 typów  
**API Providers**: 3 (OpenAI, OpenRouter, Ollama)
