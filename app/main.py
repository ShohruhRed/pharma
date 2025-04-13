from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base
from datetime import datetime
import joblib
import numpy as np
import torch
import pickle
from sanfis import SANFIS

Base.metadata.create_all(bind=engine)
app = FastAPI()

# === Загрузка моделей ===
ml_model = joblib.load("app/defect_predictor_final.pkl")

with open("app/sanfis_membfuncs.pkl", "rb") as f:
    membfuncs = pickle.load(f)

sanfis_model = SANFIS(membfuncs=membfuncs, n_input=5)
sanfis_model.load_state_dict(torch.load("app/sanfis_model.pt"))
sanfis_model.eval()


# === DB Dependency ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# === Общая функция определения уровня риска ===
def classify_risk(prob: float):
    if prob > 0.6:
        return "high", "🔴 Немедленно вмешаться"
    elif prob > 0.3:
        return "medium", "🟡 Проверьте условия"
    else:
        return "low", "🟢 Всё в норме"


# === CRUD API ===

@app.post("/batches")
def create_batch(batch: schemas.BatchCreate = Depends(), db: Session = Depends(get_db)):
    return crud.create_batch(db, batch)


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
    probability = ml_model.predict_proba(features)[0][1]
    risk_level, recommendation = classify_risk(probability)

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
        source_model="ml"
    )

    return {
        "risk_level": risk_level,
        "defect_probability": round(float(probability), 2),
        "recommendation": recommendation,
    }


@app.post("/sanfis-predict")
def sanfis_predict(data: schemas.PredictionInput, db: Session = Depends(get_db)):
    x = np.array([[data.temperature, data.pressure, data.humidity, data.NaCl, data.KCl]])
    x_tensor = torch.tensor(x, dtype=torch.float32)

    with torch.no_grad():
        output = sanfis_model(X_batch=x_tensor, S_batch=x_tensor)
        prob = output.item()

    risk_level, recommendation = classify_risk(prob)

    crud.log_prediction(
        db,
        temperature=data.temperature,
        pressure=data.pressure,
        humidity=data.humidity,
        NaCl=data.NaCl,
        KCl=data.KCl,
        defect_probability=round(float(prob), 2),
        risk_level=risk_level,
        recommendation=recommendation,
        source_model="sanfis"
    )

    return {
        "defect_probability": round(prob, 2),
        "risk_level": risk_level,
        "recommendation": recommendation
    }
