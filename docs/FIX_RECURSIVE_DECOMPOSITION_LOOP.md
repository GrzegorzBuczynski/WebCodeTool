# Naprawa Recursive Decomposition Loop - Dokumentacja Zmian

## Problem
System uległ awarii typu "Recursive Decomposition Loop", generując 170+ zadań o głębokości 10 poziomów zamiast produkować wyniki. Agent zamiast pracować, odmawiał pracy powołując się na ograniczenia wiedzy.

## Rozwiązanie: Cztery Filarowe Heurystyki Cięcia

### 1. **Limit Dekompozycji (Decomposition Limit)** ✅
**Plik**: `src/cad_ai/agents.py` - `MasterOrchestrator.process_task_recursive()`

**Implementacja**:
- **Max Depth Guard**: Zadania na poziomie `L > 3` są automatycznie redirectowane do `_execute_atomic_task()`
- **Complexity Factor**: Hard cap na maksymalnie **5 podzadań** na zadanie (enforced w linii `num_subtasks = min(num_subtasks, 5)`)

**Efekt**:
```
❌ PRZED: Level 0 -> 7 tasks -> Level 1 -> 7 tasks -> ... -> Level 10 (170+ tasks total)
✅ PO: Level 0 -> 5 tasks max -> Level 1 -> 5 tasks max -> Level 3 STOP -> Direct Execution
```

---

### 2. **Assumption-Based Execution** ✅
**Plik**: `src/cad_ai/agents.py` - `ExecutorAgent.execute_task()`

**Zmiana logiki**:
```python
# PRZED:
Brak dostępu do danych → "Nie mogę, fail"

# PO:
Brak dostępu do danych → Użyj Industry Standards → Zwróć konkretny wynik
```

**Embedded Knowledge (w system prompt)**:
- Średnia marża e-commerce: 20-30%
- Średni CTR digital marketing: 1-3%
- Średni ROI kampanii: 300-400%
- Koszt pozyskania klienta: $10-$50
- Itp. standardy rynkowe

**Efekt**: Agent NIE MÓWI "nie mogę" - zawsze zwraca estimate bazujący na assumptions.

---

### 3. **Validation Gate - Value-Added Filter** ✅
**Plik**: `src/cad_ai/agents.py` - `VerificationAgent.verify_task()` + `_check_value_added()`

**Nowe reguły weryfikacji**:

#### Wyniki AKCEPTOWALNE zawierają minimum jedno z:
- ✅ **Analiza** (insights, wnioski, interpretacja)
- ✅ **Tekst** (opisowe wyjaśnienia, szczegóły)
- ✅ **Kod** (implementacja, skrypty)
- ✅ **Tabela/Dane** (strukturyzowane dane, metryki)

#### Wyniki ODRZUCANE zawierają TYLKO:
- ❌ "Szukaj tu..." (instrukcje bez treści)
- ❌ "Przeczytaj plik..." (linki bez analizy)
- ❌ "Użyj API..." (wskazówki bez implementacji)
- ❌ "Sprawdź dokumentację..." (referencje bez kontekstu)

**Automatyczne filtry**:
1. Wynik < 50 znaków → FAIL (zbyt krótki)
2. 3+ razy słowa "szukaj/sprawdź/przejdź" + brak value indicators → FAIL
3. Brak żadnych wskaźników wartości → FAIL

**Efekt**: System MUSI produkować rzeczywiste dane, nie instrukcje.

---

### 4. **Semantic Bureaucratic Loop Detector** ✅
**Plik**: `src/cad_ai/agents.py` - `SemanticLoopDetectorAgent` (NOWA KLASA)

**Mechanizm**:
```
Zadanie na Level 4: "Zbierz raporty o rynku"
    ↓ (sprawdzenie przodków)
Zadanie na Level 1: "Analizuj rynek"
    ↓
WYKRYTO: Są semantycznie identyczne (>85% similarity)
    ↓
AKCJA: Przerwij dekompozycję, scalaj w jedno atomic zadanie
```

**Implementacja**:
- Każde nowe zadanie sprawdzane względem ALL przodków
- LLM ocenia: identyczność, stopień podobieństwa, czy to pętla
- Jeśli `PĘTLA: TAK` lub similarity > 85% → STOP rekursji

**Efekt**: Eliminuje pętle "analizuj -> zbierz raporty -> analizuj -> zbierz raporty"

---

## Statystyka Zmian

| Metrika | Wartość |
|---------|---------|
| Nowych metod/agentów | 2 (SemanticLoopDetectorAgent + _check_value_added) |
| Zmodyfikowanych metod | 3 (process_task_recursive, execute_task, verify_task) |
| Nowych linii kodu | ~200 |
| Linii usuniętych | 0 (czysty add) |
| Błędy Python | 0 |

---

## Jak to działa razem - Flow

```
[Task] → MAX_LEVEL_GUARD (L>3?) ──YES→ ATOMIC EXECUTION
           ↓NO
         COMPLEXITY_ANALYZER
           ↓
         [Should Decompose?] ──NO→ ATOMIC EXECUTION
           ↓YES
         COORDINATOR (max 5 subtasks)
           ↓
         DUPLICATION_DETECTOR
           ↓
         SEMANTIC_LOOP_DETECTOR (check ancestors) ──LOOP→ ATOMIC EXECUTION
           ↓NO LOOP
         [Create subtasks]
           ↓
         RECURSIVE CALL on subtasks
           ↓
         VERIFIER (VALUE_ADDED_CHECK) ──FAIL→ RETRY or FAIL
           ↓PASS
         AGGREGATION
```

---

## Testowanie

### Test 1: Limit głębokości
```python
# Task "Analizuj globalny rynek technologiczny"
# Oczekiwane: Max 3 poziomy, max 5 podzadań per level
# Poprzednie: 10 poziomów, 170+ zadań
```

### Test 2: Assumption-Based
```python
# Task "Wylicz ROI kampanii bez danych dostępu"
# Oczekiwane: Wynik z industry standards
# Poprzednie: Fail
```

### Test 3: Value-Added Filter
```python
# Task z wynikiem "Szukaj danych tutaj: ..."
# Oczekiwane: FAIL weryfikacji
# Poprzednie: PASS
```

### Test 4: Loop Detection
```python
# Task L4: "Zbierz raporty o rynku"
# Task L1 (przodek): "Analizuj rynek"
# Oczekiwane: LOOP DETECTED → ATOMIC EXECUTION
# Poprzednie: Kontynuacja rekursji
```

---

## Konfiguracja

Brak dodatkowych zmiennych środowiskowych. System używa istniejących:
- `AI_PROVIDER` (openai/openrouter/ollama)
- `API_KEY`
- `MODEL`

Limity (hardcoded, możemy parametryzować):
```python
MAX_DECOMPOSITION_DEPTH = 3
MAX_SUBTASKS_PER_TASK = 5
MIN_RESULT_LENGTH = 50  # chars
```

---

## Backward Compatibility

✅ **Pełna kompatybilność** z istniejącym kodem:
- Nowy agent jest opcjonalny (ale defaultowo wkompilowany)
- Wszystkie publiczne interfejsy bez zmian
- Istniejące task_manager, persistence działają jak wcześniej

---

## Dalsze Usprawnienia (Optional)

1. **Parametryzacja limitów**: Przenieść stałe do `config/.env`
2. **Adaptive depth**: Głębokość zależna od złożoności (L1 złożoność = max 5 levels)
3. **Caching similarity checks**: LLM cache dla podobnych poleceń
4. **Metrics export**: JSON z danymi o wykrytych pętlach

---

## Podsumowanie

System ma teraz **4 warstwowe obrony** przeciw Recursive Decomposition Loop:

1. ✅ **Bariera na poziomie** (L > 3)
2. ✅ **Bariera na liczbie podzadań** (max 5)
3. ✅ **Bariera na jakości wyniku** (Value-Added)
4. ✅ **Bariera na semantyce** (Loop Detection)

**Wynik**: System zamiast tworzyć 170+ zadań, będzie produkować **rzeczywiste wyniki** w maksymalnie 3 poziomach.
