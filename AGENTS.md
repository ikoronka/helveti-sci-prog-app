# AGENTS.md — Helveti House Rent Web App

AI coding instructions and project rules for all models. Follow every rule unconditionally unless the user explicitly overrides one in the same session.

---

## Project Overview

A full-stack web application that exposes the Helveti house rent analysis as an interactive dashboard. The backend is a FastAPI REST API wrapping the analysis pipeline; the frontend is a Vue 3 SPA consuming that API.

**This repo is intentionally separate** from `helveti-sci-prog` (the data science / submission repo). Do not copy changes back into that repo unless explicitly asked.

**Backend entry point:** `backend/main.py` (FastAPI app with lifespan)
**Data layer:** `backend/db_handler.py` (Kaggle download → SQLite cache)
**Analysis layer:** `backend/analysis/` (pure functions — no FastAPI imports)
**LLM layer:** `backend/llm_service.py` (Google Gemini API)
**Frontend entry point:** `frontend/src/main.ts` (Vue 3 + Pinia + Vue Router)
**Dataset:** `iamsouravbanerjee/house-rent-prediction-dataset` (Kaggle)

---

## Project Structure

```
helveti-sci-prog-app/
├── backend/
│   ├── main.py               ← FastAPI app, lifespan, router mounts
│   ├── db_handler.py         ← SQLite ingestion (copied from analysis repo)
│   ├── llm_service.py        ← Gemini AI integration
│   ├── analysis/             ← pure analysis functions (no FastAPI deps)
│   │   ├── filters.py        ← city list, BHK range
│   │   ├── kpis.py           ← avg rent, median size, count
│   │   ├── charts.py         ← histogram bins, scatter points
│   │   └── regression.py     ← scipy linregress wrapper
│   └── routers/              ← thin HTTP wrappers around analysis/
│       ├── filters.py        ← GET /api/filters
│       ├── data.py           ← GET /api/data
│       └── insight.py        ← POST /api/insight
├── frontend/
│   └── src/
│       ├── api/client.ts     ← axios wrappers for all endpoints
│       ├── types/api.ts      ← TypeScript interfaces for all API shapes
│       ├── stores/           ← Pinia stores
│       ├── views/            ← page-level components
│       └── components/       ← layout/, dashboard/, shared/
├── nginx/default.conf        ← reverse proxy (prod)
├── docker-compose.yml
└── .env.example
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Google Gemini API key |
| `DB_PATH` | No | SQLite path (default `house_rent.db`) |

Never hardcode values. Load from environment only. Only `.env.example` (with placeholders) may be committed — never a populated `.env`.

Kaggle credentials must be at `~/.kaggle/kaggle.json`. The backend does not manage these; ensure they are present before starting.

---

## 1. Backend Rules (FastAPI / Python)

### Architecture

- **Routers are thin.** All business logic — filtering, aggregation, statistical computation — lives in `analysis/`. Routers only parse query params, call analysis functions, and return the result.
- **Database opened once at startup.** `HouseRentDatabase.get_data()` is called in the FastAPI lifespan and the resulting DataFrame stored on `app.state.df`. Never open the database per-request.
- **LLMService instantiated once at startup.** Stored on `app.state.llm`. Never instantiate per-request.

### Dependencies

- Pin all versions with `==` in `backend/requirements.txt`. Never use bare package names or `>=` without a pinned upper bound.
- Update `requirements.txt` in the same commit as any new import.
- Do not add `marimo`, `scikit-learn`, or `statsmodels` unless a specific feature requires them — they are excluded from the MVP backend to keep the image small.

### Code Style

- **Type hints on every function.** All parameters and return types must be annotated.
- **One-line docstring on every public function.** Describe what it returns, not its internals.
- **Use `logging`, never `print`.** All modules use `logging.getLogger(__name__)`.
- **No bare `except:`.** Catch specific exception types. Never `pass` or silently swallow.
- **No silent empty returns.** Every error path must either raise, log with `logger.error/exception`, or return a typed fallback. Never return `None` without a documented reason.
- **Line length:** 88 characters (Black default).

### Data Handling

- **Validate schema after load.** After `get_data()` in lifespan, assert the expected columns are present. Expected minimum: `BHK, Rent, Size, Floor, Area Type, Area Locality, City, Furnishing Status, Tenant Preferred, Bathroom, Point of Contact`.
- **Assert non-empty.** After load, assert `len(df) > 0`.
- **Preserve decimals in regex cleaning.** The Size column cleaner uses `r"[^0-9.]"` — never `r"[^0-9]"`.
- **DB path via env var.** Use `os.environ.get("DB_PATH", "house_rent.db")` — never a bare string literal.

### LLM Integration (`llm_service.py`)

- **Structured prompt with mandatory context fields.** Every Gemini prompt must include: city, BHK, N (sample size), slope with units (₹/sqft), R², p-value, and a synthesis task description.
- **Validate response before returning.** If the response text is empty, return the human-readable fallback string — never an empty string.
- **Never surface raw exceptions to the API caller.** Catch all exceptions, log with `logger.error`, return a fallback string:
  ```
  "AI insight is temporarily unavailable. Please try again later."
  ```
- **Never log the API key.** Do not log `os.environ.get("GOOGLE_API_KEY")` or any fragment of it.

### API Design

- All routes are prefixed `/api/`.
- Return HTTP 404 (not 200 with empty data) when a filter combination yields zero rows.
- Never return raw Python tracebacks in API responses. Use FastAPI's `HTTPException` with a descriptive `detail` string.

---

## 2. Frontend Rules (Vue 3 / TypeScript)

### Vue Patterns

- **Always use `<script setup>` with the Composition API.** Never use the Options API or the older `defineComponent` form.
- **`ref()` for primitive state, `reactive()` for objects only when the whole object is always replaced together.** Default to `ref()`.
- **Derived values use `computed()`.** Never recompute in the template or in watchers. Transform API data into Chart.js format via `computed()` in the component.
- **Side effects on state changes use `watch()` or `watchEffect()`.** The `DashboardView` watches `filtersStore.city` and `filtersStore.bhk` with `{ immediate: true }` to trigger fetches on mount and on change.
- **Props are typed with `defineProps<{...}>()`** — no runtime validators unless the type alone is insufficient.
- **Events are typed with `defineEmits<{...}>()`** — never untyped `$emit`.

### Stores (Pinia)

- **One store per concern.** `filtersStore` owns city + BHK selection. `dashboardStore` owns fetched data, loading, and error state. Do not mix concerns.
- **Actions handle all async.** Components call store actions, never `axios` directly.
- **Loading and error state live in the store**, not in component-local `ref`. This allows any component to react to the same fetch state.

### API Client (`src/api/client.ts`)

- All HTTP calls go through the typed functions in `client.ts`. No component imports `axios` directly.
- Always type the response with the corresponding interface from `src/types/api.ts`.
- The base URL is always `/api` — never an absolute URL. Vite proxies it in dev; Nginx routes it in prod.

### TypeScript

- **`strict: true` is assumed.** Do not use `any` unless there is a documented reason (e.g. Chart.js mixed-type dataset workaround) with an inline comment explaining why.
- **All API response shapes are defined in `src/types/api.ts`.** Never use inline object types for API data.
- **No `// @ts-ignore`.** Fix the type issue properly or cast with `as T` and a comment.

### Styling

- **Tailwind CSS only.** No custom CSS files beyond `src/assets/main.css` (which contains only the Tailwind directives). No `<style scoped>` blocks unless a Tailwind utility genuinely cannot express the rule.
- **No inline `style` attributes** unless dynamically computed (e.g. a progress bar width from a variable).
- Use semantic HTML elements (`<header>`, `<main>`, `<aside>`, `<nav>`, `<dl>`, etc.) rather than generic `<div>` wrappers everywhere.

### Charts (vue-chartjs / Chart.js)

- **Register Chart.js components explicitly** in each chart component — never use the global registration approach.
- **Chart data is always a `computed()` ref** — never mutated directly.
- Mixed scatter + line datasets require a cast to satisfy TypeScript; document this with a brief inline comment.

---

## 3. Deployment Rules

### Docker

- **Backend Dockerfile:** `python:3.13-slim` base. Install deps from `requirements.txt`, copy source, start with `uvicorn main:app --host 0.0.0.0 --port 8000`.
- **Frontend Dockerfile:** Multi-stage. Stage 1: `node:22-alpine`, run `npm ci && npm run build`. Stage 2: `nginx:alpine`, copy `dist/` and `nginx.conf`.
- **Never use `:latest` tags** in Dockerfiles. Pin base image versions.
- **`house_rent.db` is a volume mount**, not baked into the image. This persists the SQLite database across container rebuilds without re-downloading from Kaggle.

### Nginx

- `nginx/default.conf` (the reverse proxy container) routes `/api/` → `http://backend:8000/api/` and `/` → `http://frontend:80`.
- `frontend/nginx.conf` (inside the frontend container) must include `try_files $uri $uri/ /index.html` so Vue Router history mode works on direct URL access.
- Never proxy WebSocket or SSE routes unless a feature explicitly requires them.

### Environment

- All secrets are injected via `env_file: .env` in `docker-compose.yml`. Never hardcode values in compose files or Dockerfiles.
- `DB_PATH` in the container should be `/app/house_rent.db`, matching the volume mount target.

---

## 4. Testing

- **Tests live in `backend/tests/`.** Run with `pytest backend/tests/`.
- **Minimum required tests:**
  - `tests/test_analysis.py`: unit tests for each function in `analysis/` using a small in-memory DataFrame fixture.
  - `tests/test_llm_service.py`: mock the Gemini client to raise an exception; assert `generate_conclusion()` returns a non-empty string (not raises).
- **Do not mock the database in integration tests.** Use a real SQLite fixture (`tmp_path`) so schema assertions are exercised.
- **Frontend:** no test framework is configured in the MVP. If Vitest is added later, tests live in `frontend/src/__tests__/`.

---

## 5. File & Commit Hygiene

- **Do not commit `house_rent.db` or `.ingestion_failed`.** Both are gitignored.
- **Do not commit `.env`.** Only `.env.example` with placeholder values.
- **Do not commit `frontend/dist/` or `frontend/node_modules/`.**
- **Commit messages follow Conventional Commits:** `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`.
- **Do not modify the original `helveti-sci-prog` repo** from within this repo's context. They are separate projects.

---

## Future Enhancements

- **Statistics view:** add `/api/stats` endpoint (outlier detection, normality tests, Kruskal-Wallis) and a `StatisticsView.vue` page.
- **Feature engineering endpoint:** expose derived columns (Rent_per_sqft, Bath_per_BHK, log transforms) for display.
- **HTTPS on Hetzner VPS:** add Certbot/Let's Encrypt to the Nginx container and update `nginx/default.conf` to listen on 443.
- **Export:** one-click CSV download of the filtered slice via a `GET /api/export` endpoint.
- **ML predictions:** train a Random Forest on startup and expose `POST /api/predict` for rent estimation.
