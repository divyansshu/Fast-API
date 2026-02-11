from fastapi import FastAPI
from pydantic import BaseModel
from model import model
import numpy as np

app = FastAPI()

class Iris(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float

@app.post('/predict')
def predict(data: Iris):
    features = np.array([
        [
    data.SepalLengthCm,
    data.SepalWidthCm,
    data.PetalLengthCm,
    data.PetalWidthCm
        ]
    ])
    prediction = model.predict(features)
    return {'prediction': int(prediction[0])}