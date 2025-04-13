from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.config import get_db
from app.db import models, schemas

router = APIRouter()
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