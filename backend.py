import pickle
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="UFO Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = pickle.load(open("ufo-model.pkl", "rb"))

COUNTRIES = ["Australia", "Canada", "Germany", "UK", "US"]


class UFOInput(BaseModel):
    seconds: float
    latitude: float
    longitude: float


@app.get("/")
def root():
    return {"message": "UFO Prediction API is running"}


@app.post("/predict")
def predict(data: UFOInput):
    features = np.array([[data.seconds, data.latitude, data.longitude]])
    prediction = int(model.predict(features)[0])
    country = COUNTRIES[prediction]
    return {"country": country, "code": prediction}
