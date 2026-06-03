#!/usr/bin/env bash
# One-process launcher for Render (and any single-port host).
#
# Render exposes ONE public port via $PORT. We run the FastAPI backend
# internally on 127.0.0.1:8000 and publish the Streamlit frontend on $PORT.
# The frontend reaches the backend through the default BACKEND_URL
# (http://localhost:8000), so no extra config is needed.
set -e
cd "$(dirname "$0")"

# Start the FastAPI backend in the background.
uvicorn backend:app --host 127.0.0.1 --port 8000 &

# Wait until the backend is up before Streamlit's first request.
python - <<'PY'
import time, urllib.request
for _ in range(40):
    try:
        urllib.request.urlopen("http://127.0.0.1:8000/", timeout=2)
        break
    except Exception:
        time.sleep(1)
PY

# Publish the Streamlit UI on the port Render gives us.
exec streamlit run frontend.py \
  --server.port "${PORT:-8501}" \
  --server.address 0.0.0.0 \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false
