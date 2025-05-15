from datetime import datetime

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.core.config import get_db
from app.db import schemas, models
from app.crud import crud
from app.simulate_realtime import simulate_for_batch

router = APIRouter(
    prefix="/batches",
    tags=["Batches"]
)

@router.post("/")
def create_batch_endpoint(batch: schemas.BatchCreate = Depends(), db: Session = Depends(get_db)):
    return crud.create_batch(db, batch)

# ✅ Получить все партии
@router.get("/")
def get_all_batches(db: Session = Depends(get_db)):
    return db.query(models.Batch).order_by(models.Batch.start_time.desc()).all()

# ✅ Получить одну партию по ID
@router.get("/{batch_id}")
def get_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(models.Batch).filter(models.Batch.id == batch_id).first()
    if not batch:
        return {"error": "Batch not found"}
    return batch

@router.post("/start", response_model=schemas.Batch)
def start_batch(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # 1) Создаём новую партию в БД
    new_batch = models.Batch(status="active", start_time=datetime.utcnow())
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)

    # 2) Запускаем симуляцию в фоне
    background_tasks.add_task(simulate_for_batch, new_batch.id, 5)

    return new_batch

@router.post("/{batch_id}/stop", response_model=schemas.Batch)
def stop_batch(
    batch_id: int,
    db: Session = Depends(get_db)
):
    batch = db.query(models.Batch).filter(models.Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    batch.status = "stopped"
    db.commit()
    db.refresh(batch)
    return batch
