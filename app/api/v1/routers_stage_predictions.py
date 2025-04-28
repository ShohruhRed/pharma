from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.config import get_db
from app.db import models, schemas

router = APIRouter(
    prefix="/stage-predictions",
    tags=["Stage Predictions"]
)

@router.post("/stage-predictions")
def add_stage_prediction(pred: schemas.StagePredictionCreate, db: Session = Depends(get_db)):
    db_pred = models.StagePrediction(
        stage_id=pred.stage_id,
        timestamp=pred.timestamp or datetime.utcnow(),
        defect_prob=pred.defect_prob,
        recommendation=pred.recommendation
    )
    db.add(db_pred)
    db.commit()
    db.refresh(db_pred)
    return db_pred

# ✅ Получить все предсказания по этапам
@router.get("/")
def get_all_stage_predictions(db: Session = Depends(get_db)):
    return db.query(models.StagePrediction).order_by(models.StagePrediction.timestamp.desc()).all()

# ✅ Получить предсказания по ID этапа
@router.get("/by-stage/{stage_id}")
def get_predictions_by_stage(stage_id: int, db: Session = Depends(get_db)):
    return db.query(models.StagePrediction).filter(models.StagePrediction.stage_id == stage_id).order_by(models.StagePrediction.timestamp).all()