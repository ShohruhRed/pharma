from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import get_db
from app.db import schemas
from app.crud import crud

router = APIRouter()

@router.post("/batches")
def create_batch_endpoint(batch: schemas.BatchCreate = Depends(), db: Session = Depends(get_db)):
    return crud.create_batch(db, batch)
