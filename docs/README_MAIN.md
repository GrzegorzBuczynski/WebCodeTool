# 🤖 Multi-Agent Task Decomposition System

**Zaawansowany system AI do hierarchicznej dekompozycji złożonych zadań na mniejsze podzadania, wykorzystujący sieć wyspecjalizowanych agentów.**

| | |
|---|---|
| **Status** | ✅ Production Ready |
| **Wersja** | 2.0.0 |
| **Python** | 3.8+ |
| **API** | OpenAI, OpenRouter, Ollama |
| **Dokumentacja** | 2500+ linii |

---

## 🚀 Szybki Start (5 minut)

### 1. Instalacja
```bash
cd /home/grzegorz/Documents/programowanie/cad
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Konfiguracja
```bash
# Skopiuj szablon
cp .env.example .env

# Edytuj .env - dodaj API key
nano .env
```

Opcje:
- **OpenRouter** (rekomendowany): `sk-or-v1-YOUR_KEY`
- **OpenAI**: `sk-YOUR_KEY`
- **Ollama** (darmowy, offline): `http://localhost:11434`

### 3. Uruchomienie
```bash
# Demo z pełnym workflow
python demo_persistence.py

# LUB interaktywnie
python main.py

# LUB szybki test
python quick_test.py
```

**To wszystko! Wyniki będą w `results/` folder.**

---

## 📚 Dokumentacja

| Plik | Dla kogo | Czas |
|------|----------|------|
| **[QUICKSTART.md](QUICKSTART.md)** | Wszyscy | 5 min |
| **[README_COMPLETE.md](README_COMPLETE.md)** | Zainteresowani | 30 min |
| **[PERSISTENCE.md](PERSISTENCE.md)** | Developers | 20 min |
| **[FAQ.md](FAQ.md)** | Wszyscy | Lookup |
| **[INDEX.md](INDEX.md)** | Nawigacja | 5 min |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Podsumowanie | 10 min |
| **[CHANGELOG.md](CHANGELOG.md)** | Historia | 10 min |

---

## 🎯 Co to robi?

```
Złożone zadanie
     ↓
[Analiza złożoności] ← AI określa czy podzielić
     ↓
[Dekompozycja] ← Podział na mniejsze podzadania
     ↓
[Wykonanie] ← 5 agentów pracuje równolegle
     ↓
[Weryfikacja] ← Każdy wynik sprawdzany
     ↓
[Zapis] ← Automatyczne zapisanie do pliku
     ↓
Kompleksowy rezultat
```

---

## 🤖 Agenty w Systemie

1. **ComplexityAnalyzer** - Ocena czy zadanie powinno być podzielone
2. **Coordinator** - Podział na podzadania
3. **DuplicationDetector** - Eliminacja duplikatów
4. **Executor (x5)** - Wykonanie rzeczywistych zadań
5. **Verification** - Sprawdzenie jakości (0-10)
6. **MasterOrchestrator** - Koordynacja wszystkiego

---

## 💾 Wyniki Automatycznie Zapisywane

```
results/
├── task_results/
│   ├── task_0001_result.json
│   ├── task_0001_detailed_report.json
│   ├── task_0001_report.txt (do czytania)
│   └── task_0001_hierarchy.json
├── statistics/
│   └── task_0001_decomposition_stats.json
└── execution_logs/
    └── summary_YYYYMMDD_HHMMSS.json
```

---

## 🌐 Obsługiwane API

| Dostawca | Koszt | Offline | Model |
|----------|-------|---------|-------|
| **OpenRouter** ⭐ | Tanio | ❌ | 100+ modeli |
| **OpenAI** | Drogo | ❌ | GPT-4o, itp |
| **Ollama** | Gratis | ✅ | llama2, mistral |

---

## 📊 Parametry

- **Maksymalne poziomy**: 10 (safety limit)
- **Agenty**: 7 typów
- **Formaty outputu**: 8+ (JSON, TXT, hierarchia, etc.)
- **Czas wykonania**: 1-3 minuty (średnio)

---

## 📝 Przykładowe Zastosowania

### 📖 Analiza dużych dokumentów
```
"Przeanalizuj 50-stronicowy raport"
→ Podzielone na sekcje
→ Każda analizada niezależnie
→ Wynik syntetyzowany
```

### ✍️ Tworzenie zawartości
```
"Napisz 5000-słowy artykuł o AI"
→ Podzielone na rozdziały
→ Każdy napisany osobno
→ Sklejone w całość
```

### 🏗️ Planowanie
```
"Plan budowy domu od A do Z"
→ Podzielone na fazy
→ Dla każdej fazy szczegóły
→ Pełny plan budowy
```

---

## ✨ Główne Cechy

✅ **Inteligentna dekompozycja** - Nie hardkodowane poziomy, ale analiza  
✅ **Multi-provider** - 3 główne dostawcy API  
✅ **Persistence** - Wszystko zapisywane do pliku  
✅ **Deduplikacja** - Eliminacja duplikatów  
✅ **Weryfikacja** - Każde zadanie oceniane  
✅ **Pełna dokumentacja** - 2500+ linii  
✅ **Production ready** - Obsługa błędów, logging  

---

## 🛠️ Setup (Jeśli chcesz interaktywnie)

```bash
python setup.py
# Wizard poprosi o:
# 1. Dostawcę API
# 2. Klucz API
# 3. Model do użycia
```

---

## 📈 Metryki Projektu

- **Linie kodu**: ~2000
- **Dokumentacji**: ~2500 linii
- **Plików**: 24
- **Agentów**: 7 typów
- **API Dostawcy**: 3
- **Testów**: 5

---

## 🆘 Potrzebujesz Pomocy?

1. **[QUICKSTART.md](QUICKSTART.md)** - Setup (5 minut)
2. **[README_COMPLETE.md](README_COMPLETE.md)** - Pełna info
3. **[FAQ.md](FAQ.md)** - 50+ pytań i odpowiedzi
4. **[INDEX.md](INDEX.md)** - Pełna nawigacja

---

## 🐛 Szybka Diagnoza

### "API key invalid"
```bash
cat .env | grep API_KEY
# Powinno coś być, jeśli puste - dodaj klucz
```

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Too slow"
```python
# W main.py zmniejsz:
max_recursion_depth=3  # Zamiast 10
```

Więcej: [QUICKSTART.md - Troubleshooting](QUICKSTART.md)

---

## 📦 Zawartość Projektu

```
📁 DOKUMENTACJA (8 plików)
├─ QUICKSTART.md ⭐ (START TUTAJ)
├─ README_COMPLETE.md
├─ PERSISTENCE.md
├─ FAQ.md
├─ INDEX.md
├─ PROJECT_SUMMARY.md
└─ CHANGELOG.md

💻 KOD (11 plików)
├─ agents.py (642 linii - główny system)
├─ task_manager.py (153 linii)
├─ persistence.py (283 linii)
├─ main.py (program interaktywny)
├─ results_viewer.py (narzędzie)
├─ setup.py (setup wizard)
└─ 5 testów

⚙️ KONFIGURACJA
├─ .env (zmienne, nie commituj!)
├─ .env.example (szablon)
└─ requirements.txt (zależności)
```

---

## 🚀 Następne Kroki

1. **Przeczytaj**: [QUICKSTART.md](QUICKSTART.md) (5 minut)
2. **Zainstaluj**: Kroki wyżej (1 minuta)
3. **Uruchom**: `python demo_persistence.py` (2 minuty)
4. **Eksperymentuj**: `python main.py` (30 minut)
5. **Rozwijaj**: Modyfikuj agentów w [agents.py](agents.py)

---

## 📞 Kontakt & Info

- **Wersja**: 2.0.0
- **Status**: ✅ Production Ready
- **Python**: 3.8+
- **Licencja**: MIT

---

# 👉 **[ZACZNIJ OD TUTAJ → QUICKSTART.md](QUICKSTART.md)**

Powodzenia! 🎉
