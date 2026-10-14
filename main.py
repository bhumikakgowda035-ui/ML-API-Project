from pathlib import Path
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.joblib"

app = FastAPI(
    title="Iris Prediction API",
    description="A beginner-friendly machine learning API for Iris flower prediction.",
    version="1.0.0",
)

# The model is loaded once when the application starts.
if not MODEL_PATH.exists():
    raise RuntimeError(
        f"Model file not found: {MODEL_PATH}. "
        "Run `python generate_model.py` from the project root first."
    )
model = joblib.load(MODEL_PATH)

class PredictionInput(BaseModel):
    # Iris measurements are in centimeters.
    sepal_length: float = Field(gt=0, description="Sepal length in cm")
    sepal_width: float = Field(gt=0, description="Sepal width in cm")
    petal_length: float = Field(gt=0, description="Petal length in cm")
    petal_width: float = Field(gt=0, description="Petal width in cm")

@app.get("/")
def home():
    return {
        "message": "Iris Prediction API is running",
        "docs": "/docs",
        "prediction_endpoint": "POST /predict",
    }

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
def predict(payload: PredictionInput):
    features = [[
        payload.sepal_length,
        payload.sepal_width,
        payload.petal_length,
        payload.petal_width,
    ]]
    try:
        prediction = int(model.predict(np.asarray(features, dtype=float))[0])
        names = {0: "setosa", 1: "versicolor", 2: "virginica"}
        probabilities = model.predict_proba(np.asarray(features, dtype=float))[0]
        return {
            "prediction_id": prediction,
            "prediction": names.get(prediction, "unknown"),
            "confidence": round(float(max(probabilities)), 4),
            "input": payload.model_dump(),
        }
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid input: {exc}") from exc
