from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import numpy as np
import torch

from app.crud import crud
from app.db import schemas
from app.core.rules import rules_dict, sanfis_model, feature_names
from app.core.config import get_db
from app.core.risk import classify_risk

router = APIRouter()

# загружаем параметры нормализации
train_min = np.load("app/models/train_min.npy")
train_max = np.load("app/models/train_max.npy")

def normalize_data(X, train_min, train_max):
    return (X - train_min) / (train_max - train_min)

@router.post("/sanfis-predict")
def sanfis_predict(data: schemas.PredictionInput, db: Session = Depends(get_db)):
    # 1) Формируем массив со всеми 6 признаками
    x = np.array([[
        data.temperature,
        data.pressure,
        data.humidity,
        data.NaCl,
        data.KCl,
        data.stage_idx
    ]], dtype=float)

    # 2) Нормализация по тем же min/max, что и при обучении
    x_norm = normalize_data(x, train_min, train_max)
    x_tensor = torch.tensor(x_norm, dtype=torch.float32)

    # 3) Прогноз SANFIS
    with torch.no_grad():
        raw = sanfis_model(X_batch=x_tensor, S_batch=x_tensor)
        prob = torch.sigmoid(raw).item()

    # 4) Находим ближайшее правило по μ-вектору
    mu_vec = list(x_norm.flatten()[:5]) + [ data.stage_idx ]  # берем нормированные μ для сенсоров + stage_idx
    closest_rule = min(
        rules_dict.items(),
        key=lambda item: np.linalg.norm(np.array(item[0]) - np.array(mu_vec))
    )[1]

    # 5) Определяем уровень риска и рекомендацию
    risk_level, recommendation = classify_risk(prob)

    # 6) Логируем в БД
    crud.log_prediction(
        db=db,
        temperature=data.temperature,
        pressure=data.pressure,
        humidity=data.humidity,
        NaCl=data.NaCl,
        KCl=data.KCl,
        defect_probability=round(prob, 2),
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
