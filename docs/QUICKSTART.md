# 🚀 QUICKSTART - Szybki start w 5 minut

## Dla niecierpliwych - zainstaluj i uruchom natychmiast!

### 1️⃣ Instalacja (1 minuta)

```bash
# Przejdź do katalogu projektu
cd /home/grzegorz/Documents/programowanie/cad

# Stwórz wirtualne środowisko (jeśli jeszcze nie istnieje)
python3 -m venv venv

# Aktywuj
source venv/bin/activate  # Na Linux/Mac
# LUB
venv\Scripts\activate  # Na Windows

# Zainstaluj zależności
pip install -r requirements.txt
```

**Czas: ~1 minuta (lub ~3 minuty przy pierwszej instalacji)**

### 2️⃣ Konfiguracja API (2 minuty)

#### Opcja A: OpenRouter (REKOMENDOWANA - tańsza)

1. Idź na https://openrouter.ai/keys
2. Skopiuj klucz (zaczyna się od `sk-or-v1-`)
3. Utwórz `.env`:

```bash
cat > .env << 'EOF'
AI_PROVIDER=openrouter
API_KEY=sk-or-v1-TWOJ_KLUCZ_TUTAJ
MODEL=meta-llama/llama-2-70b-chat
EOF
```

#### Opcja B: OpenAI (oficjalny)

```bash
cat > .env << 'EOF'
AI_PROVIDER=openai
API_KEY=sk-TWOJ_KLUCZ_TUTAJ
MODEL=gpt-4o-mini
EOF
```

#### Opcja C: Ollama (offline, darmowy)

```bash
# Najpierw zainstaluj Ollama: https://ollama.ai

# Potem uruchom:
ollama serve

# W innym terminalu:
cat > .env << 'EOF'
AI_PROVIDER=ollama
MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
EOF
```

### 3️⃣ Uruchomienie (1 minuta)

```bash
# Demo z pełnym workflow
python demo_persistence.py

# LUB program interaktywny
python main.py

# LUB szybki test
python quick_test.py
```

**Oczekiwany output:**
```
================================================================================
DEMONSTRACJA: Hierarchiczna dekompozycja zadań z persistencją
================================================================================

📋 GŁÓWNE ZADANIE:
Opisz proces budowy domu...

Rozpoczynanie przetwarzania...

[ComplexityAnalyzerAgent] Analizuję złożoność: WYSOKA | Output: BARDZO_DŁUGI
[CoordinatorAgent] Podzielę to na 4 subtasków
[ExecutorAgent#1] Wykonuję: ...
...
```

### 4️⃣ Podgląd wyników (1 minuta)

```python
# W Pythonie:
from results_viewer import list_saved_tasks, view_detailed_report

# Lista wszystkich zadań
list_saved_tasks()

# Szczegółowy raport
view_detailed_report("0001")
```

Lub w terminalu:
```bash
ls -la results/
cat results/task_results/task_0001_report.txt
```

### 5️⃣ Gotowe! 🎉

Teraz możesz:
- ✅ Tworzyć własne zadania: `main.py` - program interaktywny
- ✅ Przeglądać wyniki: `results_viewer.py`
- ✅ Uruchamiać testy: `test_*.py`

---

## 🎯 Następne kroki

### Chcesz zrozumieć system?
Czytaj w tej kolejności:
1. [README_COMPLETE.md](README_COMPLETE.md) - Pełny przegląd
2. [PERSISTENCE.md](PERSISTENCE.md) - Jak działają wyniki
3. Kod w [agents.py](agents.py) - Implementacja

### Chcesz własne zadania?
```python
# Edytuj main.py i zmień:
main_task_desc = "TWOJE ZADANIE TUTAJ"

# Lub uruchom interaktywnie:
python main.py
```

### Chcesz zmienić model/dostawcę?
Edytuj `.env`:
```bash
nano .env
# Zmień: AI_PROVIDER, API_KEY, MODEL
```

### Chcesz mniej kosztów?
Użyj Ollama (darmowy, lokalny):
```
AI_PROVIDER=ollama
MODEL=llama2
```

---

## 🆘 Troubleshooting

### "API key invalid"
```bash
# Sprawdź czy klucz jest prawidłowy
cat .env | grep API_KEY

# Jeśli pusty, dodaj:
echo "API_KEY=sk-or-v1-TWOJ_KLUCZ" >> .env
```

### "Module not found"
```bash
# Zainstaluj zależności
pip install -r requirements.txt

# Lub manualnie:
pip install openai python-dotenv colorama
```

### "Connection refused" (dla Ollama)
```bash
# Upewnij się, że Ollama działa
ollama serve

# W innym terminalu:
python main.py
```

### "Too many tasks / Token limit"
```python
# Zmniejsz głębokość w main.py:
orchestrator = MasterOrchestrator(
    max_recursion_depth=3,  # Zamiast 10
    ...
)
```

---

## 📊 Porównanie dostawców

| | OpenRouter | OpenAI | Ollama |
|---|---|---|---|
| Koszt | Taniej (~50%) | Drogi | Darmowy |
| Szybkość | ~2-3s | ~2-3s | Zależy |
| Offline | ❌ | ❌ | ✅ |
| Jakość | Dobra | Najlepsza | Średnia |
| Instalacja | Łatwa | Łatwa | Hard |

**Rekomendacja dla początkujących:** OpenRouter

---

## 🎓 Przykładowe zadania

### 1. Prosty obiad 🍽️
```
"Zaplanuj obiad dla 4 osób"
```
→ Wykonane bezpośrednio (NISKA złożoność)

### 2. Projekt budowy domu 🏠
```
"Opisz proces budowy domu: planowanie, fundament, ściany, dach, instalacje"
```
→ Podzielone na 4-5 podtasków (WYSOKA złożoność)

### 3. Analiza systemu 🤖
```
"Przeanalizuj architekturę AI i zaproponuj usprawnienia"
```
→ Podzielone na 3-4 podtasków (BARDZO_WYSOKA złożoność)

---

## 📈 Co się stanie po uruchomieniu

1. **Analiza** - ComplexityAnalyzer oceni czy podzielić
2. **Dekompozycja** - CoordinatorAgent podzieli na podtaskami
3. **Wykonanie** - ExecutorAgent (x5) pracuje równolegle
4. **Weryfikacja** - VerificationAgent sprawdza wyniki
5. **Zapis** - Wszystko zapisane do `results/`
6. **Raport** - Wyświetlony raport tekstowy

**Całkowity czas:** 1-2 minuty dla prostych zadań

---

## 🔐 Bezpieczeństwo

⚠️ **Nigdy nie commituj `.env`!**

```bash
# Sprawdź czy jest w .gitignore:
cat .gitignore | grep ".env"

# Jeśli nie, dodaj:
echo ".env" >> .gitignore
```

---

## 📞 Potrzebujesz więcej?

- **Pełna dokumentacja**: [README_COMPLETE.md](README_COMPLETE.md)
- **Persistencja**: [PERSISTENCE.md](PERSISTENCE.md)
- **Historia zmian**: [CHANGELOG.md](CHANGELOG.md)
- **Setup wizard**: `python setup.py`

---

## ✅ Checklist - czy wszystko działa?

- [ ] Python 3.8+ zainstalowany
- [ ] venv aktywny
- [ ] Zależności zainstalowane (`pip install -r requirements.txt`)
- [ ] `.env` skonfigurowany z API key
- [ ] `python quick_test.py` działa
- [ ] Wyniki w `results/` folder

Jeśli ✅ wszystko - **gratulacje, jesteś gotowy!** 🚀

---

**Szacunkowy czas setup: 5 minut ⏱️**

Powodzenia! 🎉
