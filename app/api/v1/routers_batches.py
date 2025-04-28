from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import get_db
from app.db import schemas, models
from app.crud import crud

router = APIRouter(
    prefix="/batches",
    tags=["Batches"]
)

@router.post("/batches")
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
