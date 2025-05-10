from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class BatchCreate(BaseModel):
    start_time: Optional[datetime] = None
    status: Optional[str] = "active"

class Batch(BaseModel):
    id: int
    start_time: datetime
    end_time: Optional[datetime]
    status: str

    class Config:
        orm_mode = True


# === Этап производства ===
class StageCreate(BaseModel):
    batch_id: int
    name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class Stage(BaseModel):
    id: int
    batch_id: int
    name: str
    start_time: datetime
    end_time: Optional[datetime]

    class Config:
        orm_mode = True


# === Данные с сенсоров на этапе ===
class StageSensorDataCreate(BaseModel):
    stage_id: int
    timestamp: Optional[datetime] = None
    temperature: Optional[float]
    pressure: Optional[float]
    humidity: Optional[float]
    composition: Optional[Dict[str, float]]
    stage_idx: int


# === Прогноз по этапу ===
class StagePredictionCreate(BaseModel):
    stage_id: int
    timestamp: Optional[datetime] = None
    defect_prob: float
    recommendation: Optional[str]

class PredictionInput(BaseModel):
    stage_id: int
    temperature: float
    pressure: float
    humidity: float
    NaCl: float
    KCl: float
    stage_idx: int



# app/db/schemas.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PredictionBase(BaseModel):
    temperature: float
    pressure: float
    humidity: float
    NaCl: float
    KCl: float
    defect_probability: float
    risk_level: str
    recommendation: str
    source_model: str      # 'ml' или 'sanfis'
    rule_used: Optional[str] = None

class PredictionCreate(PredictionBase):
    stage_id: Optional[int] = None

class Prediction(PredictionBase):
    id: int
    timestamp: datetime
    stage_id: Optional[int]

    class Config:
        orm_mode = True