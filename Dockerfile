# Backend image: FastAPI + Uvicorn serving the UFO prediction model.
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Regenerate the model against the installed scikit-learn version so the
# pickle always loads cleanly (avoids version-mismatch errors at runtime).
RUN python train_model.py

EXPOSE 8000
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]
