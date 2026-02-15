# 🤝 CONTRIBUTING - Jak Wnieść Wkład

Dziękujemy za zainteresowanie wkładem w projektu! Tutaj znajduje się wszystko co musisz wiedzieć.

---

## 🎯 Sposoby Wkładu

### 1. Bug Reports 🐛
Jeśli znalazłeś bug:
1. Sprawdzę czy już nie jest zgłoszony
2. Otwórz issue z:
   - Opisem problemu
   - Kroki do reprodukcji
   - Oczekiwane vs rzeczywiste zachowanie
   - Wersja Pythona, OS, etc.

### 2. Feature Requests ✨
Masz pomysł na ulepszenie?
1. Otwórz issue z "enhancement" tagiem
2. Opisz use case
3. Zależy ci na tym? Napisz kod!

### 3. Code Contributions 💻
Chcesz kodować?
1. Fork projekt
2. Utwórz branch: `git checkout -b feature/my-feature`
3. Commit: `git commit -am "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Otwórz Pull Request

### 4. Documentation 📝
Chcesz poprawy dokumentację?
1. Edytuj `.md` pliki
2. Zaproponuj zmiany

### 5. Testing 🧪
Testuj i reportuj wyniki

---

## 🛠️ Zanim Zaczniesz

### Setup Development Environment

```bash
# Fork & clone
git clone https://github.com/YOUR_USERNAME/multi-agent.git
cd multi-agent

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8  # Dev tools

# Pre-commit hooks (opcjonalnie)
pip install pre-commit
pre-commit install
```

### Sprawdzenie że wszystko działa

```bash
# Uruchom testy
python test_run.py
python test_intelligent.py
python test_duplication.py

# Linting
flake8 agents.py
black --check agents.py
```

---

## 📋 Coding Standards

### 1. Style Guide

```python
# DOBRY - PEP 8 compliant
def analyze_task_complexity(task: str) -> dict:
    """
    Analyze task complexity.
    
    Args:
        task: Task description
        
    Returns:
        Dictionary with complexity assessment
    """
    complexity = "ŚREDNIA"
    return {"complexity": complexity}

# ZŁY - nie PEP 8
def analyzeTaskComplexity(task):
    # brak docstring
    c = "SREDNIA"
    return c
```

### 2. Type Hints

```python
# DOBRY
def process_task(task: Task, level: int) -> TaskResult:
    pass

# ZŁY
def process_task(task, level):
    pass
```

### 3. Docstrings

```python
# DOBRY
def execute_task(task: Task) -> str:
    """
    Execute an atomic task.
    
    This method executes the task using the LLM API
    and returns the result with context awareness.
    
    Args:
        task: Task object with description and metadata
        
    Returns:
        Task result as string
        
    Raises:
        APIError: If API call fails
        ValueError: If task is invalid
        
    Example:
        >>> task = Task(id="1", description="Write poem")
        >>> result = execute_task(task)
        >>> print(result)
    """
    pass

# ZŁY
def execute_task(task):
    # wykonaj zadanie
    pass
```

### 4. Formatting

```bash
# Auto-format code
black agents.py

# Check style
flake8 agents.py

# Max line length: 100 characters
```

---

## 🧪 Testing

### Pisanie testów

```python
# test_my_feature.py
import pytest
from agents import MasterOrchestrator

def test_complexity_analyzer():
    """Test ComplexityAnalyzer"""
    orchestrator = MasterOrchestrator()
    
    # Arrange
    task_description = "Zaplanuj obiad"
    
    # Act
    result = orchestrator.orchestrator.analyze_complexity(task_description)
    
    # Assert
    assert result['should_decompose'] == False  # NISKA złożoność
    
def test_executor_agent():
    """Test ExecutorAgent"""
    from agents import ExecutorAgent
    
    agent = ExecutorAgent(agent_id=1)
    result = agent.execute("Test task")
    
    assert isinstance(result, str)
    assert len(result) > 0

@pytest.mark.slow
def test_full_workflow():
    """Full integration test (może być długi)"""
    # Full workflow test
    pass
```

### Uruchamianie testów

```bash
# Wszystkie testy
pytest

# Z pokryciem
pytest --cov=. --cov-report=html

# Tylko szybkie
pytest -m "not slow"

# Verbose
pytest -vv
```

### Test Coverage

Cel: minimum 70% pokrycia
```bash
# Check coverage
pytest --cov=agents --cov=task_manager --cov-report=term-missing
```

---

## 📝 Commit Messages

### Format

```
[TYPE] Subject (max 50 chars)

Optional detailed description explaining:
- Why this change
- What it does
- How it solves the problem

Footer: Closes #issue_number
```

### Typy

- `feat:` - Nowa funkcja
- `fix:` - Bug fix
- `docs:` - Dokumentacja
- `style:` - Formatowanie (bez zmian kodu)
- `refactor:` - Zmiana kodu bez nowych features
- `test:` - Dodanie/zmiana testów
- `chore:` - Maintenance (dependencies, etc.)

### Przykłady

```
feat: Add SQLite persistence backend

This adds SQLite support as alternative to JSON files.
Benefits:
- Faster queries
- Better concurrent access
- Automatic indexing

Closes #123

---

fix: Prevent duplicate task execution

DuplicationDetectorAgent now properly identifies
overlapping tasks before execution.

Closes #456

---

docs: Update README with new API section

Added documentation for:
- OpenRouter integration
- Cost comparison table
- Setup wizard usage
```

---

## 🔀 Pull Request Process

### 1. Przed otwarciem PR

- [ ] Fork repo
- [ ] Utwórz feature branch
- [ ] Napisz kod z testami
- [ ] Testy przechodzą
- [ ] Kod sformatowany (`black`)
- [ ] Brak linting błędów (`flake8`)
- [ ] Dokumentacja zaktualizowana
- [ ] Changelog updatered

### 2. PR Template

```markdown
## Description
Krótko opisz zmiany

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Breaking change

## Testing
Opisz jak przetestowałeś zmiany

## Checklist
- [ ] Testy przechodzą
- [ ] Kod sformatowany
- [ ] Dokumentacja updatered
- [ ] Brak breaking changes
```

### 3. Code Review Process

Reviewer sprawdzą:
- Jakość kodu
- Dokumentacja
- Testy
- Performance impact
- Security issues

---

## 🏗️ Project Structure

```
/home/grzegorz/Documents/programowanie/cad/
│
├── 📚 DOCUMENTATION
│   ├── README.md                ← Main entry point
│   ├── QUICKSTART.md            ← Setup guide
│   ├── README_COMPLETE.md       ← Full docs
│   ├── PERSISTENCE.md           ← Persistence details
│   ├── FAQ.md                   ← Q&A
│   ├── CHANGELOG.md             ← Version history
│   ├── DEPLOYMENT.md            ← Production guide
│   ├── CONTRIBUTING.md          ← This file
│   └── PROJECT_SUMMARY.md       ← Overview
│
├── 💻 SOURCE CODE
│   ├── agents.py                ← Main system (DON'T TOUCH LIGHTLY)
│   ├── task_manager.py          ← Task management
│   ├── persistence.py           ← Results storage
│   ├── main.py                  ← CLI interface
│   ├── results_viewer.py        ← Results viewer
│   └── setup.py                 ← Setup wizard
│
├── 🧪 TESTS
│   ├── test_run.py              ← Basic test
│   ├── test_intelligent.py      ← Complexity test
│   ├── test_duplication.py      ← Dedup test
│   ├── quick_test.py            ← Quick test
│   └── demo_persistence.py      ← Demo
│
├── ⚙️ CONFIG
│   ├── .env.example             ← Config template
│   ├── .gitignore               ← Git ignore
│   └── requirements.txt         ← Dependencies
│
└── 📁 GENERATED
    └── results/                 ← Task results (generated)
```

---

## 🔑 Key Files to Understand

### agents.py (642 linii)
**Nie modyfikuj bez zrozumienia!**

Główne klasy:
- `BaseAgent` - Base class for all agents
- `ComplexityAnalyzerAgent` - Decides decomposition
- `CoordinatorAgent` - Splits tasks
- `ExecutorAgent` (x5) - Executes tasks
- `VerificationAgent` - Verifies results
- `MasterOrchestrator` - Coordinates all

**Przed zmianami:**
1. Czytaj cały plik
2. Uruchom testy
3. Zrozum wpływ zmian
4. Napisz nowe testy

### persistence.py (283 linii)
**Gdy zmienisz format danych:**
1. Update version w CHANGELOG
2. Add migration script
3. Test backward compatibility

### task_manager.py (153 linii)
**Bezpieczny do zmiany:**
1. Dodaj nowe pola jeśli potrzeba
2. Zachowaj backward compatibility
3. Update docstrings

---

## 🚀 Feature Development

### Dla nowej funkcjonalności

```python
# 1. Write test first (TDD)
def test_new_feature():
    assert feature_works()

# 2. Implement feature
def new_feature():
    pass

# 3. Run all tests
pytest

# 4. Add documentation
# 5. Update CHANGELOG
```

### Checklist dla features

- [ ] Feature works
- [ ] Tests pass
- [ ] Code reviewed
- [ ] Docs updated
- [ ] Examples provided
- [ ] No breaking changes
- [ ] Performance OK
- [ ] Security OK

---

## 🐛 Bug Fixing

### Jak naprawiać bugs

1. **Replikuj bug**
   ```python
   # Napisz test który pokazuje bug
   def test_bug_reproduction():
       # This should fail with current code
       assert bug_exists()
   ```

2. **Napraw kod**
   ```python
   # Fix the bug
   def buggy_function():
       return correct_result()
   ```

3. **Sprawdzenie**
   ```bash
   pytest  # Test should pass now
   ```

4. **Dokumentuj**
   ```
   commit: fix: Description of bug and fix
   ```

---

## 📊 Performance Guidelines

### Optimization priorities

1. **Correctness** > Performance (zawsze)
2. **Readability** > Clever code
3. **Maintainability** > Cleverness

### Performance considerations

```python
# ❌ Don't micro-optimize
x = [[0 for _ in range(1000)] for _ in range(1000)]

# ✅ Focus on algorithm complexity
if len(tasks) > 100:
    use_set()  # O(1) lookup instead O(n)
```

### Benchmarking

```python
import time

start = time.time()
result = heavy_operation()
duration = time.time() - start

print(f"Took {duration:.2f}s")
```

---

## 🔐 Security Guidelines

### Never do this

```python
# ❌ Hardcode API keys
API_KEY = "sk-..."

# ❌ Log sensitive data
print(f"API Key: {api_key}")

# ❌ Use eval()
code = "dangerous_code()"
eval(code)
```

### Always do this

```python
# ✅ Use environment variables
API_KEY = os.getenv("API_KEY")

# ✅ Sanitize inputs
task = task.strip().replace("\0", "")

# ✅ Handle errors gracefully
try:
    result = api_call()
except Exception as e:
    logger.error(f"API error: {type(e).__name__}")
```

---

## 📖 Documentation

### Adding docs

1. **Docstrings** - Wszystkie funkcje/klasy
2. **README** - High-level overview
3. **Comments** - Dziwne/skomplikowane części
4. **Examples** - Jak korzystać
5. **Changelog** - Co się zmieniło

### Updating existing docs

```bash
# Edytuj .md pliki
nano README_COMPLETE.md

# Sprawdzę markdown
# (nie ma built-in linter)
```

---

## 🎓 Learning Resources

### Aby zrozumieć system

1. **Czytaj [README_COMPLETE.md](README_COMPLETE.md)** - Architecture
2. **Czytaj [PERSISTENCE.md](PERSISTENCE.md)** - Data flow
3. **Czytaj code** - start z `task_manager.py`
4. **Uruchom testy** - See what works
5. **Modyfikuj, eksperymentuj** - Break things!

### External Resources

- [Python Best Practices](https://pep8.org/)
- [Git Best Practices](https://git-scm.com/book/)
- [Testing Guide](https://docs.pytest.org/)
- [Async Python](https://docs.python.org/3/library/asyncio.html)

---

## ❓ FAQ dla Contributors

**P: Gdzie zacząć?**
O: Czytaj [README_COMPLETE.md](README_COMPLETE.md), uruchom [QUICKSTART.md](QUICKSTART.md), ekserymentuj z testami.

**P: Jak znaleźć issue do pracy?**
O: Szukaj `good-first-issue` i `help-wanted` labels.

**P: Jak się komunikować?**
O: Issues, Discussions, Pull Requests.

**P: Jaki jest timeline dla PR review?**
O: Staram się odpowiedzieć w 48 godzin.

**P: Czy mój PR będzie zaakceptowany?**
O: Jeśli spełnia kryteria i jest dobrej jakości - tak!

---

## 🎉 Dziękujemy!

Każdy wkład (mały czy duży) jest ważny.

Możesz:
- ✅ Zgłaszać bugs
- ✅ Proponować features
- ✅ Pisać kod
- ✅ Poprawiać dokumentację
- ✅ Dzielić się pomysłami
- ✅ Testować
- ✅ Promować projekt

---

## 📞 Kontakt

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: See GitHub profile

---

**Dziękujemy za zainteresowanie! Czekam na Twój PR! 🚀**

