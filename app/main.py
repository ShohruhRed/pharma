from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from datetime import datetime
import joblib
import numpy as np

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Загружаем модель один раз при старте
model = joblib.load("app/defect_predictor_final.pkl")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/batches")
def create_batch(batch: schemas.BatchCreate = Depends(), db: Session = Depends(get_db)):
    return crud.create_batch(db, batch)


# --- Добавление этапа ---
@app.post("/stages", response_model=schemas.Stage)
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

# --- Добавление данных сенсора ---
@app.post("/stage-data")
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

# --- Добавление прогноза по этапу ---
@app.post("/stage-predictions")
def add_stage_prediction(pred: schemas.StagePredictionCreate, db: Session = Depends(get_db)):
    db_pred = models.StagePrediction(
        stage_id=pred.stage_id,
        timestamp=pred.timestamp or datetime.utcnow(),
        defect_prob=pred.defect_prob,
        recommendation=pred.recommendation
    )
    db.add(db_pred)
    db.commit()
    db.refresh(db_pred)
    return db_pred

@app.post("/ml-predict")
def predict_defect(data: schemas.PredictionInput, db: Session = Depends(get_db)):
    features = np.array([[data.temperature, data.pressure, data.humidity, data.NaCl, data.KCl]])
    probability = model.predict_proba(features)[0][1]

    if probability > 0.6:
        risk_level = "high"
        recommendation = "🔴 Требуется немедленное вмешательство"
    elif probability > 0.3:
        risk_level = "medium"
        recommendation = "🟡 Проверьте параметры"
    else:
        risk_level = "low"
        recommendation = "🟢 Процесс в норме"

    # логгируем
    crud.log_prediction(
        db,
        temperature=data.temperature,
        pressure=data.pressure,
        humidity=data.humidity,
        NaCl=data.NaCl,
        KCl=data.KCl,
        defect_probability=round(float(probability), 2),
        risk_level=risk_level,
        recommendation=recommendation,
    )

    return {
        "risk_level": risk_level,
        "defect_probability": round(float(probability), 2),
        "recommendation": recommendation,
    }
