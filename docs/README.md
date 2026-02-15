# System Wieloagentowy z Rekursywną Dekompozycją Zadań

Zaawansowany system AI, który automatycznie analizuje złożone cele, dzieli je na mniejsze zadania i deleguje do specjalizowanych agentów. System wykorzystuje rekursywną dekompozycję (minimum 3 poziomy) oraz weryfikację wykonanych zadań.

## 🌟 Funkcjonalności

- **Inteligentna ocena złożoności** - AI samo decyduje czy zadanie wymaga podziału
- **Dynamiczna głębokość rekursji** - brak sztywnych limitów, adaptacyjny podział
- **Analiza potencjalnego outputu** - system ocenia ile danych wygeneruje zadanie
- **Wieloagentowa architektura**:
  - `ComplexityAnalyzerAgent` - ocenia czy zadanie wymaga podziału i ile outputu wygeneruje
  - `CoordinatorAgent` - analizuje i dzieli zadania na podzadania
  - `DuplicationDetectorAgent` - wykrywa i eliminuje pokrywające się zadania
  - `ExecutorAgent` (x5) - wykonuje atomowe zadania
  - `VerificationAgent` - weryfikuje jakość wykonania
  - `MasterOrchestrator` - koordynuje wszystkich agentów
- **Elastyczne API** - obsługa OpenAI, OpenRouter i Ollama
- **Inteligentny przekaz danych** - kontekst przekazywany między agentami
- **Kolorowe logi** - śledzenie postępu w czasie rzeczywistym
- **Hierarchia zadań** - wizualizacja struktury zadań
- **Automatyczna weryfikacja** - każde zadanie jest sprawdzane pod kątem jakości
- **Statystyki dekompozycji** - szczegółowe informacje o procesie podziału zadań

## 📋 Wymagania

- Python 3.8+
- Klucz API OpenAI
- Pakiety: `openai`, `python-dotenv`, `colorama`

## 🚀 Instalacja

1. Sklonuj lub pobierz projekt

2. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

3. Utwórz plik `.env` z konfiguracją:
```bash
cp .env.example .env
# Edytuj .env i skonfiguruj wybranego dostawcę API
```

### Konfiguracja dostawców API

**OpenAI:**
```env
AI_PROVIDER=openai
API_KEY=sk-your-openai-key
MODEL=gpt-4o-mini
```

**OpenRouter:**
```env
AI_PROVIDER=openrouter
API_KEY=sk-or-v1-your-openrouter-key
MODEL=openai/gpt-4o-mini
```

**Ollama (lokalnie):**
```env
AI_PROVIDER=ollama
MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
```
(Ollama nie wymaga klucza API)

## 💻 Użycie

Uruchom program:
```bash
python main.py
```

Program:
1. Wyświetli przykładowe zadanie główne
2. Pozwoli wprowadzić własne zadanie
3. Automatycznie:
   - Podzieli zadanie na podzadania (poziom 1)
   - Każde podzadanie podzieli dalej (poziom 2)
   - Wykona atomowe zadania (poziom 3)
   - Zweryfikuje każde zadanie
   - Zagreguje wyniki

## 🏗️ Architektura

```
Zadanie (dowolny poziom)
    │
    ├─► ComplexityAnalyzer ocenia:
    │   • Czy zadanie jest wystarczająco proste? (TAK/NIE)
    │   • Ile outputu wygeneruje? (KRÓTKI/ŚREDNI/DŁUGI)
    │   • Złożoność (NISKA/ŚREDNIA/WYSOKA/BARDZO_WYSOKA)
    │   
    ├─► Jeśli PROSTE → Executor wykonuje → Verifier weryfikuje
    │
    └─► Jeśli ZŁOŻONE:
        ├─► Coordinator dzieli na N podzadań (2-5)
        ├─► DuplicationDetector eliminuje duplikaty
        └─► Każde podzadanie → proces rekurencyjny
                               (ponownie ComplexityAnalyzer)

Brak sztywnych limitów głębokości!
System sam decyduje kiedy przestać dzielić.
```

## 📁 Struktura projektu

```
.
├── main.py              # Główny program
├── agents.py            # Definicje agentów AI
├── task_manager.py      # Zarządzanie hierarchią zadań
├── requirements.txt     # Zależności
├── .env.example         # Przykład konfiguracji
└── README.md            # Ta dokumentacja
```

## 🔧 Konfiguracja

W pliku `main.py` można dostosować:

- `MAX_DEPTH` - maksymalny poziom rekursji (domyślnie 3)
- Model AI - w `agents.py` w klasie `BaseAgent` (domyślnie `gpt-4o-mini`)
- Liczbę executorów - w `MasterOrchestrator.__init__()` (domyślnie 5)

## 📊 Przykładowy wynik

Program wyświetla:
- Postęp w czasie rzeczywistym z kolorowymi logami
- Hierarchię wszystkich utworzonych zadań
- Wynik końcowy z agregacją
- Statystyki (liczba zadań, weryfikacje, itp.)
- Ocenę jakości wykonania

## 🎯 Przykładowe zadania

Dobre przykłady zadań do testowania:

1. "Stwórz plan uruchomienia aplikacji mobilnej"
2. "Przeprowadź kompleksową analizę konkurencji dla nowego produktu"
3. "Zaprojektuj strategię marketingową dla startupu"
4. "Przygotuj dokumentację techniczną dla systemu e-commerce"

## 🎯 Jak to działa

1. **Ocena złożoności**: ComplexityAnalyzerAgent analizuje czy zadanie wymaga podziału na podstawie:
   - Złożoności (niska/średnia/wysoka/bardzo wysoka)
   - Przewidywanej ilości outputu (krótki/średni/długi/bardzo długi)
   - Liczby kroków wymaganych do wykonania
2. **Decyzja**: System AI decyduje: podzielić (TAK) czy wykonać bezpośrednio (NIE)
3. **Dekompozycja**: Jeśli TAK → CoordinatorAgent dzieli na 2-5 podzadań (liczba też ustalana przez AI)
4. **Eliminacja duplikatów**: DuplicationDetectorAgent analizuje podzadania i usuwa pokrywające się
5. **Delegacja**: MasterOrchestrator przydziela zadania do odpowiednich executorów
6. **Wykonanie**: ExecutorAgents realizują atomowe zadania z kontekstem
7. **Weryfikacja**: VerificationAgent sprawdza jakość i kompletność
8. **Agregacja**: Wyniki są łączone hierarchicznie od dołu do góry
9. **Rekursja**: Każde podzadanie przechodzi przez ten sam proces (kroki 1-8)

**Kluczowa różnica**: System SAM decyduje o głębokości rekursji, nie ma sztywnych limitów!

## 🔒 Bezpieczeństwo

- Klucz API przechowywany w `.env` (dodany do `.gitignore`)
- Brak hardcodowanych sekretów w kodzie
- Walidacja wszystkich wejść

## 📝 Licencja

Projekt edukacyjny - użyj dowolnie.

## 🤝 Wkład

Mile widziane pull requesty i propozycje ulepszeń!
