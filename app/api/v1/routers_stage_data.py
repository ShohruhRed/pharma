from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.config import get_db
from app.db import models, schemas

router = APIRouter()
@router.post("/stage-data")
def add_stage_sensor_data(data: schemas.StageSensorDataCreate, db: Session = Depends(get_db)):
    db_data = models.StageSensorData(
        stage_id=data.stage_id,
        timestamp=data.timestamp or datetime.utcnow(),
        temperature=data.temperature,
        pressure=data.pressure,
        humidity=data.humidity,
        composition=data.composition
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data