# ❓ FAQ - Najczęściej Zadawane Pytania

## 🔧 Instalacja & Konfiguracja

### P: Co potrzebuję do uruchomienia tego systemu?
**O:** Tylko:
- Python 3.8+
- API key (OpenAI, OpenRouter) LUB lokalnie: Ollama
- ~100MB place na dysku

### P: Czy mogę uruchomić bez internetu?
**O:** Tak! Użyj Ollama:
```bash
# Zainstaluj: https://ollama.ai
ollama pull llama2
ollama serve

# W .env:
AI_PROVIDER=ollama
MODEL=llama2
```

### P: Jaki dostawca wybrać?
**O:** To zależy:
- **OpenRouter** - Najlepszy wybór dla początkujących (tańszy)
- **OpenAI** - Najlepsza jakość, droższy
- **Ollama** - Darmowy, ale wymaga zainstalowania

### P: Ile będzie mnie to kosztować?
**O:** Zależy od dostawcy:
- **OpenRouter**: ~$0.0015 za request
- **OpenAI (gpt-4o-mini)**: ~$0.003 za request
- **Ollama**: $0 (lokalnie)

10 requestów = $0.015 - $0.03

### P: Czy API key jest bezpieczny?
**O:** Zalecenia:
1. ✅ Przechowuj w `.env` (w `.gitignore`)
2. ❌ NIGDY nie commituj `.env`
3. ✅ Jeśli wycieknął - zresetuj w panelu API
4. ✅ Monitoruj użycie w panelu dostawcy

---

## 🤖 Jak działa system?

### P: Co robi ComplexityAnalyzer?
**O:** Analizuje czy zadanie powinno być podzielone:

```
Złożoność: NISKA/ŚREDNIA/WYSOKA/BARDZO_WYSOKA
Output: <500/<1500/<5000/>5000 słów

NISKA + KRÓTKI → Wykonaj bezpośrednio
WYSOKA + BARDZO_DŁUGI → Podziel na 4-5 podtasków
```

### P: Ile maksymalnie poziomów rekursji?
**O:** System poddział maksymalnie na 10 poziomów (safety limit), ale zazwyczaj 1-3 wystarczają.

### P: Czy 5 ExecutorAgentów to minimum?
**O:** Nie, to domyślnie. Możesz zmienić:
```python
MasterOrchestrator(num_executors=10)
```

### P: Co robi VerificationAgent?
**O:** Sprawdza każde zadanie i daje mu ocenę 0-10 + feedback.

### P: Czy mogę zobaczyć hierarchię zadań?
**O:** Tak:
```python
orchestrator.print_statistics()  # Podsumowanie
```

i w `results/task_results/task_XXXX_hierarchy.json`

---

## 💾 Persistencja & Wyniki

### P: Gdzie są zapisane wyniki?
**O:** W katalogu `results/`:
- `task_results/` - Wyniki zadań
- `statistics/` - Statystyki
- `execution_logs/` - Logi

### P: Mogę zmienić folder na wyniki?
**O:** Tak:
```python
orchestrator = MasterOrchestrator(
    persistence_dir="/moja/sciezka"
)
```

### P: Co jeśli brakuje `results/`?
**O:** System tworzy automatycznie. Jeśli nie - problem z uprawnieniami:
```bash
mkdir -p results/{task_results,statistics,execution_logs}
chmod 755 results
```

### P: Czy mogę wyeksportować wyniki do CSV?
**O:** Na razie JSON i TXT. CSV planuje się w v3.0.

### P: Jak duże mogą być wyniki?
**O:** Zależy od liczby zadań:
- Proste: ~10 KB
- Średnie: ~100 KB
- Duże: ~1-10 MB

### P: Czy starego wyniki się usuwają?
**O:** Nie, pozostają. Jeśli chcesz wyczyścić:
```bash
rm -rf results/
```

---

## 🌐 API & Modele

### P: Jakie modele obsługujesz?
**O:** Teoretycznie każdy przez OpenAI SDK:
- OpenAI: gpt-4, gpt-4o-mini, gpt-3.5-turbo
- OpenRouter: 100+ modeli
- Ollama: llama2, mistral, neural-chat, itp.

### P: Czy mogę przełączać modele mid-execution?
**O:** Nie, musiałbyś zrestartować. Zmień w `.env`.

### P: OpenRouter - czy są jakieś limity?
**O:** Tak:
- Free tier: ograniczone RPM
- Płatny: $5/miesiąc lub "pay as you go"

### P: Czy wspierasz Claude/GPT-4?
**O:** Tak, przez OpenRouter:
- Claude: `anthropic/claude-3-sonnet`
- GPT-4: `openai/gpt-4`

---

## 🐛 Problemy & Rozwiązania

### P: "ModuleNotFoundError: No module named 'openai'"
**O:**
```bash
pip install openai>=1.12.0
# LUB
pip install -r requirements.txt
```

### P: "Błąd połączenia z API"
**O:** Sprawdź:
1. Klucz API w `.env` jest prawidłowy
2. Internet działa
3. Limit requestów nie wyczerpany

### P: "Ollama connection refused"
**O:**
```bash
# Terminal 1:
ollama serve

# Terminal 2:
python main.py
```

### P: "Task output is BARDZO_DŁUGI but not decomposing"
**O:** Bug? Sprawdź czy:
1. ComplexityAnalyzer ma dostęp do LLM
2. Model "rozumie" instrukcje (nie wszystkie)

### P: Zadanie trwa zbyt długo
**O:** Zmniejsz głębokość lub liczba podtasków:
```python
# W main.py:
max_recursion_depth=5  # Zamiast 10
```

### P: Błędy w JSON w results/
**O:** Sprawdź uprawnienia zapisu:
```bash
chmod -R 755 results/
```

---

## 📊 Optymalizacja

### P: Jak mogę przyśpieszyć wykonanie?
**O:**
1. Użyj szybszego modelu (llama zamiast gpt-4)
2. OpenRouter zamiast OpenAI
3. Zmniejsz num_executors lub max_recursion_depth

### P: Ile czasu zajmuje jedno zadanie?
**O:** Zależy:
- Proste (NISKA): 10-20 sekund
- Średnie (ŚREDNIA): 30-60 sekund
- Duże (WYSOKA): 1-3 minuty

### P: Czy mogę paralelizować Executor Agents?
**O:** Nie, to "pseudo-parallel" (round-robin). Rzeczywista paralelizacja w v3.0.

### P: Czy mogę cachować wyniki?
**O:** Na razie nie, ale planuje się w v3.0.

---

## 💡 Zaawansowane

### P: Czy mogę edytować agentów?
**O:** Oczywiście! W `agents.py` zmień prompty czy logikę.

### P: Jak dodać nowego agenta?
**O:** 
```python
class MojAgent(BaseAgent):
    def analyze(self, task: str) -> str:
        prompt = f"Zrób coś z: {task}"
        return self.call_llm(prompt)
```

### P: Czy mogę użyć tego w produkcji?
**O:** Ostrożnie:
- Wersja 2.0.0 - Production Ready
- Ale pamiętaj o kosztach API!
- Dodaj monitoring i logowanie

### P: Czy wspierasz múltijęzyczność?
**O:** Tak, system zawsze używa języka wejścia (PL w tym przypadku).

### P: Czy mogę integrować z Django/Flask?
**O:** Tak:
```python
from agents import MasterOrchestrator

def my_view(request):
    task = request.GET.get('task')
    orchestrator = MasterOrchestrator()
    result = orchestrator.process_task_recursive(task)
    return JsonResponse(result)
```

### P: Czy jest REST API?
**O:** Na razie nie, ale planuje się w v3.0.

---

## 📚 Zasoby & Nauka

### P: Gdzie mogę dowiedzieć się więcej o multi-agent systems?
**O:** 
- Paper: "Multi-Agent Systems: A Modern Approach" (Wooldridge)
- Video: LangChain docs na YouTube
- GitHub: microsoft/autogen

### P: Czy system wspiera LangChain?
**O:** Nie, ale je można integrować.

### P: Czy mogę dodać własne narzędzia (tools)?
**O:** Tak, w `BaseAgent.call_llm()` można dodać function calling.

### P: Jak wdrożyć do produkcji?
**O:** Best practices:
1. Containerize (Docker)
2. Dodaj monitoring (Sentry/Datadog)
3. Setup rate limiting
4. Backup results
5. Monitoring cost

---

## 🎯 Najczęstsze Use Cases

### 1. Analiza dużych dokumentów
```
"Przeanalizuj raport i wyciągnij kluczowe punkty"
```
→ System podzieli na sekcje

### 2. Tworzenie zawartości
```
"Napisz 5000-słowy artykuł o AI"
```
→ Podzielone na rozdziały, każdy napisany osobno

### 3. Rozwiązywanie problemów
```
"Jak zbudownić startup? Od pomysłu do IPO"
```
→ Podzielone na fazy (ideacja, MVP, funding, itp.)

### 4. Testowanie
```
"Testuj mój kod na edge cases"
```
→ Różne agenty testują różne scenariusze

---

## 🚀 Tips & Tricks

### 1. Szybkie testowanie
```bash
python quick_test.py
# Zamiast czekać na full workflow
```

### 2. Debug mode
Edytuj `agents.py` i zmień print() na:
```python
print(f"[DEBUG] {message}")
# Plus log to file
```

### 3. Monitoring kosztów OpenRouter
```bash
# Sprawdzaj w panelu: https://openrouter.ai/account/usage
```

### 4. Custom models
```python
# W .env
MODEL=meta-llama/llama-2-70b-chat:free
# :free = darmowy tier (jeśli dostępny)
```

---

## 📞 Jak uzyskać pomoc?

1. **Sprawdzę dokumentację**: 
   - [README_COMPLETE.md](README_COMPLETE.md)
   - [PERSISTENCE.md](PERSISTENCE.md)

2. **Szukaj w FAQ** (ten plik)

3. **Testuj funkcje**: `python test_*.py`

4. **Sprawdź logi**: `results/execution_logs/`

5. **Modyfikuj kod**: Wszystko jest open source

---

**Ostatnia aktualizacja**: 2024-12-07  
**Wersja**: 2.0.0

Masz pytanie które nie jest tu? Dodaj je! 📝
