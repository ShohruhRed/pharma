from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import models
from app.core.config import get_db

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)

# ✅ Получить все предсказания
@router.get("/")
def get_all_predictions(
    db: Session = Depends(get_db),
    source_model: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None)
):
    query = db.query(models.Prediction)

    if source_model:
        query = query.filter(models.Prediction.source_model == source_model)

    if risk_level:
        query = query.filter(models.Prediction.risk_level == risk_level)

    return query.order_by(models.Prediction.timestamp.desc()).all()


# ✅ Получить одно предсказание по ID
@router.get("/{prediction_id}")
def get_prediction_by_id(prediction_id: int, db: Session = Depends(get_db)):
    prediction = db.query(models.Prediction).filter(models.Prediction.id == prediction_id).first()
    if not prediction:
        return {"error": "Prediction not found"}
    return prediction
