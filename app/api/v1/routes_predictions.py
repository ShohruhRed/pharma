from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import schemas, models
from app.crud import crud
from app.core.config import get_db

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)

# 1) POST /predictions/ — создать новый лог
@router.post("/", response_model=schemas.Prediction)
def create_prediction(
    pred_in: schemas.PredictionCreate,
    db: Session = Depends(get_db)
):
    return crud.create_prediction(db, pred_in)

# 2) GET /predictions/ — получить все (с фильтрами)
@router.get("/", response_model=List[schemas.Prediction])
def get_all_predictions(
    source_model: Optional[str] = None,
    risk_level:   Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Prediction)
    if source_model:
        query = query.filter(models.Prediction.source_model == source_model)
    if risk_level:
        query = query.filter(models.Prediction.risk_level == risk_level)
    return query.order_by(models.Prediction.timestamp.desc()).all()

# 3) GET /predictions/{id} — получить одну запись
@router.get("/{prediction_id}", response_model=schemas.Prediction)
def get_prediction_by_id(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    pred = db.query(models.Prediction).get(prediction_id)
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return pred

@router.get("/by-stage/{stage_id}", response_model=List[schemas.Prediction])
def get_predictions_by_stage(stage_id: int, db: Session = Depends(get_db)):
    return (
      db.query(models.Prediction)
        .filter(models.Prediction.stage_id == stage_id)
        .order_by(models.Prediction.timestamp)
        .all()
    )

@router.get("/latest/{stage_id}", response_model=schemas.Prediction)
def get_latest_prediction(stage_id: int, db: Session = Depends(get_db)):
    pred = (
        db.query(models.Prediction)
          .filter(models.Prediction.stage_id == stage_id)
          .order_by(models.Prediction.timestamp.desc())
          .first()
    )
    if not pred:
        raise HTTPException(status_code=404, detail="No predictions found")
    return pred
