# Helveti House Rent — Web App

hosted at [helvetisciprog.ikoronka.com](https://helvetisciprog.ikoronka.com)

This repository is the **interactive companion** to the [`helveti-sci-prog`](https://github.com/ikoronka/helveti-sci-prog) data science project. That project contains the original exploratory analysis, statistical tests, and regression modelling of the Indian house rent dataset (Kaggle). This web app packages the same analysis pipeline into a live dashboard so the findings can be explored interactively — filtering by city and BHK, inspecting key metrics, and generating AI-written research conclusions via Google Gemini.

The two repos are kept separate by design: `helveti-sci-prog` is the submission/notebook repo; this repo is the production application that surfaces those results. The backend (`backend/analysis/`) re-implements the core analysis functions from the notebook as pure Python, and the SQLite data layer mirrors the ingestion logic from the data science project.

Vue 3 + FastAPI dashboard for the [House Rent Prediction Dataset](https://www.kaggle.com/datasets/iamsouravbanerjee/house-rent-prediction-dataset/).

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 · Vite · Pinia · vue-chartjs · Tailwind CSS |
| Backend | FastAPI · Pandas · SciPy · SQLite |
| AI insight | Google Gemini API |
| Deploy | Docker Compose · Nginx |

## Local development

### Backend

```bash
cd backend
cp .env.example .env   # add your GOOGLE_API_KEY
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be at `http://localhost:8000`. On first run it downloads the Kaggle dataset — make sure `~/.kaggle/kaggle.json` is present.

### Frontend

```bash
cd frontend
pnpm install
pnpm run dev
```

The dev server at `http://localhost:5173` proxies `/api/` to the backend automatically.

## Production (Docker Compose)

```bash
cp .env.example .env   # fill in values
docker compose up --build -d
```

Nginx listens on port 80 and routes `/api/` → FastAPI, `/` → Vue.

For HTTPS, add Certbot and update `nginx/default.conf` to listen on 443.

## API reference

| Endpoint | Description |
|----------|-------------|
| `GET /api/filters` | City list and BHK range |
| `GET /api/data?city=Mumbai&bhk=2` | KPIs, histogram, scatter, regression |
| `POST /api/insight` | AI-generated research conclusion |
