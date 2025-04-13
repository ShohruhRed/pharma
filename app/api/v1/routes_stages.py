from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.config import get_db
from app.db import models, schemas

router = APIRouter()

@router.post("/stages", response_model=schemas.Stage)
def create_stage(stage: schemas.StageCreate, db: Session = Depends(get_db)):
    db_stage = models.Stage(
        batch_id=stage.batch_id,
        name=stage.name,
        start_time=stage.start_time or datetime.utcnow(),
        end_time=stage.end_time
    )
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage
