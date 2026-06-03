# 🛸 UFO Sighting Predictor

A small machine-learning web app that predicts **which country** a UFO sighting
was reported from, based on the sighting's duration and geographic coordinates.

Originally a Flask app, **migrated to FastAPI + Uvicorn** with a Streamlit
frontend, and containerized with Docker.

## 🚀 Quick Start

The trained model (`ufo-model.pkl`) is included, so no training is needed.

**Option A — Docker (one command):**

```bash
git clone https://github.com/yuan6862/ufo-webapp
cd ufo-webapp
docker compose up --build
```

**Option B — without Docker (two terminals):**

```bash
git clone https://github.com/yuan6862/ufo-webapp
cd ufo-webapp
pip install -r requirements.txt
uvicorn backend:app --port 8000      # Terminal 1
streamlit run frontend.py            # Terminal 2
```

Then open **http://localhost:8501**. Backend docs at http://localhost:8000/docs.
Full details below.

- **Backend:** FastAPI + Uvicorn (REST `/predict` endpoint)
- **Frontend:** Streamlit
- **Model:** Logistic Regression (scikit-learn), ~96% accuracy
- **Data:** NUFORC sightings (~80k records)

## Project structure

```
ufo-webapp/
├── backend.py            # FastAPI service (POST /predict)
├── frontend.py           # Streamlit UI
├── train_model.py        # trains the model -> ufo-model.pkl
├── train_model.ipynb     # notebook version of training
├── ufo-model.pkl         # trained model
├── data/ufos.csv         # dataset
├── requirements.txt
├── Dockerfile            # backend image
├── Dockerfile.frontend   # frontend image
├── docker-compose.yml    # runs both together
└── .github/workflows/ci.yml
```

## Run locally (without Docker)

```bash
pip install -r requirements.txt
python train_model.py          # creates ufo-model.pkl (optional, already shipped)
```

Open two terminals:

```bash
# Terminal 1 — backend
uvicorn backend:app --reload --port 8000

# Terminal 2 — frontend
streamlit run frontend.py
```

Then open http://localhost:8501. Backend docs at http://localhost:8000/docs.

## Run with Docker

One command builds and starts both services:

```bash
docker compose up --build
```

- Frontend: http://localhost:8501
- Backend:  http://localhost:8000

The frontend reaches the backend via the `BACKEND_URL` env var (set to
`http://backend:8000` inside the compose network).

## Configuration

`frontend.py` reads the backend address from an environment variable, so the
same code works locally, in Docker, and on a cloud VM:

```bash
# default: http://localhost:8000
BACKEND_URL=http://<your-server-ip>:8000 streamlit run frontend.py
```

## API

`POST /predict`

```json
{ "seconds": 10, "latitude": 44.0, "longitude": -100.0 }
```

Response:

```json
{ "country": "US", "code": 4 }
```

## CI

GitHub Actions (`.github/workflows/ci.yml`) runs on every push / PR:

- **test** job: installs deps, trains the model, syntax-checks `backend.py` /
  `frontend.py`, and health-checks the backend.
- **docker** job: builds both images, starts the stack with Docker Compose, and
  health-checks the backend and frontend.
