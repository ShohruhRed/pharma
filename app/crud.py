from sqlalchemy.orm import Session
from . import models, schemas
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

def log_prediction(db: Session, temperature, pressure, humidity, NaCl, KCl,
                   defect_probability, risk_level, recommendation,
                   source_model: str, rule_used: str = None):
    from . import models
    prediction = models.Prediction(
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
