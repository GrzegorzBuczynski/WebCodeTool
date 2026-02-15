# Workspace UI

## Uruchomienie serwisu (backend + UI)

1. Aktywuj środowisko Python (jeśli używasz lokalnego venv):

   - Linux/macOS:
     - `source venv/bin/activate`

2. Zainstaluj zależności Pythona, jeśli nie są dostępne:

   - `python -m pip install fastapi uvicorn`

3. Uruchom backend (FastAPI):

   - `uvicorn backend.app:app --reload`

4. Otwórz UI w przeglądarce:

   - http://localhost:8000

## Stylowanie (Tailwind CSS)

Jednorazowa kompilacja CSS:

- `npm install`
- `npm run build:css`

Tryb watch (automatyczna kompilacja):

- `npm run watch:css`

## Uwagi

- Backend serwuje pliki statyczne z katalogu `public/`.
- Endpointy API są dostępne pod `/api/*` (np. `/api/fs/tree`, `/api/results`).
