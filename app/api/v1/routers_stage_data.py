from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.config import get_db
from app.db import models, schemas

router = APIRouter(
    prefix="/stage-data",
    tags=["Stage Sensor Data"]
)

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

# ✅ Получить все сенсорные данные
@router.get("/")
def get_all_stage_data(db: Session = Depends(get_db)):
    return db.query(models.StageSensorData).order_by(models.StageSensorData.timestamp.desc()).all()

# ✅ Получить сенсорные данные по ID этапа
@router.get("/by-stage/{stage_id}")
def get_stage_data_by_stage(stage_id: int, db: Session = Depends(get_db)):
    return db.query(models.StageSensorData).filter(models.StageSensorData.stage_id == stage_id).order_by(models.StageSensorData.timestamp).all()