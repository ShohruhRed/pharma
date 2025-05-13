from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.config import get_db
from app.db import models, schemas

router = APIRouter(
    prefix="/stage-data",
    tags=["Stage Sensor Data"]
)

@router.post("/")
def add_stage_sensor_data(data: schemas.StageSensorDataCreate, db: Session = Depends(get_db)):
    db_data = models.StageSensorData(
        stage_id=data.stage_id,
        timestamp=data.timestamp or datetime.utcnow(),
        temperature=data.temperature,
        pressure=data.pressure,
        humidity=data.humidity,
        composition=data.composition,
        stage_idx=data.stage_idx
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

@router.get("/current")
def get_current_stage_info(db: Session = Depends(get_db)):
    # 1. Самая последняя строка (по ID)
    latest = (
        db.query(models.StageSensorData)
        .order_by(models.StageSensorData.id.desc())
        .first()
    )
    if not latest:
        raise HTTPException(status_code=404, detail="No sensor data available")

    # 2. Получить этап
    stage = db.query(models.Stage).filter(models.Stage.id == latest.stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    # 3. Получить партию
    batch = db.query(models.Batch).filter(models.Batch.id == stage.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    # 4. Название этапа по индексу
    stage_names = ["Mixing", "Granulation", "Drying", "Pressing", "Coating", "Packaging"]
    stage_label = stage_names[latest.stage_idx] if latest.stage_idx is not None and 0 <= latest.stage_idx < len(stage_names) else "Unknown"

    return {
        "batch": {
            "id": batch.id
        },
        "stage": {
            "id": stage.id,
            "name": stage.name,
            "stage_idx": latest.stage_idx,
            "stage_label": stage_label
        },
        "sensor_data": {
            "temperature": latest.temperature,
            "pressure": latest.pressure,
            "humidity": latest.humidity,
            "composition": latest.composition,
            "timestamp": latest.timestamp
        }
    }


