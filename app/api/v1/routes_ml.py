from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import numpy as np
from app.crud import crud
from app.db import schemas
from app.core.risk import classify_risk
from app.core.ml_models import ml_model
from app.core.config import get_db

router = APIRouter()

@router.post("/ml-predict")
def predict_defect(data: schemas.PredictionInput, db: Session = Depends(get_db)):
    features = np.array([[data.temperature, data.pressure, data.humidity, data.NaCl, data.KCl]])
    probability = ml_model.predict_proba(features)[0][1]
    risk_level, recommendation = classify_risk(probability)

    crud.log_prediction(
        db=db,
        temperature=data.temperature,
        pressure=data.pressure,
        humidity=data.humidity,
        NaCl=data.NaCl,
        KCl=data.KCl,
        defect_probability=round(float(probability), 2),
        risk_level=risk_level,
        recommendation=recommendation,
        source_model="ml",
        stage_id=data.stage_id

    )

    return {
        "risk_level": risk_level,
        "defect_probability": round(float(probability), 2),
        "recommendation": recommendation,
    }
