from sqlalchemy.orm import Session
from app.db import models, schemas
from datetime import datetime


# === Партии ===
def create_batch(db: Session, batch: schemas.BatchCreate):
    db_batch = models.Batch(
        start_time=batch.start_time or datetime.utcnow(),
        status=batch.status
    )
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch

def get_batch(db: Session, batch_id: int):
    return db.query(models.Batch).filter(models.Batch.id == batch_id).first()

# === Этапы ===
def create_stage(db: Session, stage: schemas.StageCreate):
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

# === Сенсорные данные ===
def add_stage_sensor_data(db: Session, data: schemas.StageSensorDataCreate):
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

# === Прогнозы ===
def add_stage_prediction(db: Session, prediction: schemas.StagePredictionCreate):
    db_pred = models.StagePrediction(
        stage_id=prediction.stage_id,
        timestamp=prediction.timestamp or datetime.utcnow(),
        defect_prob=prediction.defect_prob,
        recommendation=prediction.recommendation
    )
    db.add(db_pred)
    db.commit()
    db.refresh(db_pred)
    return db_pred

def log_prediction(db: Session,stage_id, temperature, pressure, humidity, NaCl, KCl,
                   defect_probability, risk_level, recommendation,
                   source_model: str, rule_used: str = None):

    prediction = models.Prediction(
        stage_id = stage_id,
        temperature=temperature,
        pressure=pressure,
        humidity=humidity,
        NaCl=NaCl,
        KCl=KCl,
        defect_probability=defect_probability,
        risk_level=risk_level,
        recommendation=recommendation,
        source_model=source_model,
        rule_used=rule_used
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction

# app/crud/crud.py

from sqlalchemy.orm import Session
from app.db import models, schemas

# crud.py
def create_prediction(db: Session, pred_in: schemas.PredictionCreate):
    db_pred = models.Prediction(
        temperature=pred_in.temperature,
        pressure=pred_in.pressure,
        humidity=pred_in.humidity,
        NaCl=pred_in.NaCl,
        KCl=pred_in.KCl,
        defect_probability=pred_in.defect_probability,
        risk_level=pred_in.risk_level,
        recommendation=pred_in.recommendation,
        source_model=pred_in.source_model,
        rule_used=pred_in.rule_used,
        stage_id=pred_in.stage_id,      # вот он!
    )
    db.add(db_pred)
    db.commit()
    db.refresh(db_pred)
    return db_pred



# def log_prediction(db: Session, **kwargs):
#     entry = models.MLPrediction(**kwargs)
#     db.add(entry)
#     db.commit()
#     db.refresh(entry)
#     return entry
#
# def log_sanfis_prediction(db: Session, input_data: dict, prediction: dict, rule: str):
#     db_log = models.SANFISPrediction(
#         temperature=input_data["temperature"],
#         pressure=input_data["pressure"],
#         humidity=input_data["humidity"],
#         NaCl=input_data["NaCl"],
#         KCl=input_data["KCl"],
#         defect_probability=prediction["defect_probability"],
#         risk_level=prediction["risk_level"],
#         recommendation=prediction["recommendation"],
#         rule_used=rule
#     )
#     db.add(db_log)
#     db.commit()
#     db.refresh(db_log)
#     return db_log
