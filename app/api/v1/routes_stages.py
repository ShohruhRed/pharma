from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.config import get_db
from app.db import models, schemas

router = APIRouter(
    prefix="/stages",
    tags=["Stages"]
)

@router.post("/", response_model=schemas.Stage)
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

# ✅ Получить все этапы
@router.get("/")
def get_all_stages(db: Session = Depends(get_db)):
    return db.query(models.Stage).order_by(models.Stage.start_time.desc()).all()

# ✅ Получить этапы по ID партии
@router.get("/by-batch/{batch_id}")
def get_stages_by_batch(batch_id: int, db: Session = Depends(get_db)):
    return db.query(models.Stage).filter(models.Stage.batch_id == batch_id).order_by(models.Stage.start_time).all()

# ✅ Получить один этап по ID
@router.get("/{stage_id}")
def get_stage(stage_id: int, db: Session = Depends(get_db)):
    stage = db.query(models.Stage).filter(models.Stage.id == stage_id).first()
    if not stage:
        return {"error": "Stage not found"}
    return stage

