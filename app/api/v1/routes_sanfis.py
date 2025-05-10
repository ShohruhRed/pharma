from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import numpy as np
import torch
from app.crud import crud
from app.db import schemas
from app.core.rules import rules_dict
from app.core.ml_models import sanfis_model
from app.core.config import get_db
from app.core.risk import classify_risk

router = APIRouter()
# Загружаем минимальные и максимальные значения тренировочных данных
train_min = np.load("app/models/train_min.npy")
train_max = np.load("app/models/train_max.npy")

# Нормализация входных данных
def normalize_data(X, train_min, train_max):
    return (X - train_min) / (train_max - train_min)

@router.post("/sanfis-predict")
def sanfis_predict(data: schemas.PredictionInput, db: Session = Depends(get_db)):
    x = np.array([[data.temperature, data.pressure, data.humidity, data.NaCl, data.KCl]])

    # Применяем ту же нормализацию, что и при обучении SANFIS
    x_normalized = normalize_data(x, train_min, train_max)
    x_tensor = torch.tensor(x_normalized, dtype=torch.float32)

    with torch.no_grad():
        output = sanfis_model(X_batch=x_tensor, S_batch=x_tensor)
        prob = torch.sigmoid(output).item()  # Теперь вероятности корректные!

    # Находим ближайшее правило
    x_arr = x.flatten()
    closest_rule = min(rules_dict.items(), key=lambda item: np.linalg.norm(np.array(item[0]) - x_arr))[1]

    risk_level, recommendation = classify_risk(prob)

    crud.log_prediction(
        db=db,
        temperature=data.temperature,
        pressure=data.pressure,
        humidity=data.humidity,
        NaCl=data.NaCl,
        KCl=data.KCl,
        defect_probability=round(float(prob), 2),
        risk_level=risk_level,
        recommendation=recommendation,
        source_model="sanfis",
        rule_used=closest_rule,
        stage_id=data.stage_id
    )

    return {
        "defect_probability": round(prob, 2),
        "risk_level": risk_level,
        "recommendation": recommendation,
        "rule_used": closest_rule
    }
