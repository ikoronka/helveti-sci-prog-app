# Helveti House Rent — Web App

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
npm install
npm run dev
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
