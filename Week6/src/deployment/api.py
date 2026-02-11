from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime
import uuid

# PATHS 
BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "features" / "preprocessing_pipeline.pkl"

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "predictions.log"

# ---------------- LOGGER SETUP ----------------
logger = logging.getLogger("prediction_logger")
logger.setLevel(logging.INFO)

LOG_FILE.touch(exist_ok=True)

file_handler = logging.FileHandler(LOG_FILE, mode="a")
formatter = logging.Formatter("%(asctime)s | %(message)s")
file_handler.setFormatter(formatter)

logger.handlers.clear()
logger.addHandler(file_handler)

logger.propagate = False

model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)

app = FastAPI(title="Titanic Survival Prediction API")

class PredictionInput(BaseModel):
    Age: float
    Fare: float
    Sex: str
    Pclass: int
    SibSp: int
    Parch: int
    Embarked: str


@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": True}

@app.post("/predict")
def predict(data: PredictionInput):
    request_id = str(uuid.uuid4())

    # Convert input to DataFrame
    df = pd.DataFrame([data.dict()])

    # -------- FEATURE ENGINEERING --------
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
    df["FarePerPerson"] = df["Fare"] / df["FamilySize"]
    df["FareLog"] = np.log1p(df["Fare"])
    df["AgeFilled"] = df["Age"]
    df["IsChild"] = (df["AgeFilled"] < 12).astype(int)

    df["AgeBucket"] = pd.cut(
        df["AgeFilled"],
        bins=[0, 12, 20, 40, 60, 80],
        labels=["Child", "Teen", "Adult", "MiddleAge", "Senior"]
    )

    df["HighFare"] = (df["Fare"] > df["Fare"].median()).astype(int)
    df["LargeFamily"] = (df["FamilySize"] >= 5).astype(int)
    df["PclassFare"] = df["Pclass"] * df["Fare"]


    features = preprocessor.transform(df)

    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])

    # -------- LOG --------
    logger.info(
        f"request_id={request_id} | "
        f"model_version=best_model.pkl | "
        f"input={data.dict()} | "
        f"probability={round(probability,4)} | "
        f"prediction={prediction}"
    )
    for handler in logger.handlers:
        handler.flush()

    return {
        "request_id": request_id,
        "prediction": prediction,
        "survival_probability": round(probability, 4)
    }
