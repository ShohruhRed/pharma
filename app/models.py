from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey, TIMESTAMP, JSON
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    end_time = Column(TIMESTAMP)
    status = Column(Text, default="active")

    stages = relationship("Stage", back_populates="batch", cascade="all, delete")


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    start_time = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    end_time = Column(TIMESTAMP)

    batch = relationship("Batch", back_populates="stages")
    sensor_data = relationship("StageSensorData", back_populates="stage", cascade="all, delete")
    predictions = relationship("StagePrediction", back_populates="stage", cascade="all, delete")


class StageSensorData(Base):
    __tablename__ = "stage_sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("stages.id", ondelete="CASCADE"))
    timestamp = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    composition = Column(JSON)

    stage = relationship("Stage", back_populates="sensor_data")


class StagePrediction(Base):
    __tablename__ = "stage_predictions"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("stages.id", ondelete="CASCADE"))
    timestamp = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    defect_prob = Column(Float)
    recommendation = Column(Text)

    stage = relationship("Stage", back_populates="predictions")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    NaCl = Column(Float)
    KCl = Column(Float)

    defect_probability = Column(Float)
    risk_level = Column(String)
    recommendation = Column(String)

    source_model = Column(String)  # 'ml' или 'sanfis'
    rule_used = Column(String, nullable=True)  # только для sanfis, можно None


# class MLPrediction(Base):
#     __tablename__ = "ml_predictions"
#
#     id = Column(Integer, primary_key=True, index=True)
#     timestamp = Column(TIMESTAMP, default=datetime.utcnow)
#     temperature = Column(Float)
#     pressure = Column(Float)
#     humidity = Column(Float)
#     NaCl = Column(Float)
#     KCl = Column(Float)
#     defect_probability = Column(Float)
#     risk_level = Column(String)
#     recommendation = Column(Text)
#
# class SANFISPrediction(Base):
#     __tablename__ = "sanfis_predictions"
#
#     id = Column(Integer, primary_key=True, index=True)
#     timestamp = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
#
#     temperature = Column(Float)
#     pressure = Column(Float)
#     humidity = Column(Float)
#     NaCl = Column(Float)
#     KCl = Column(Float)
#
#     defect_probability = Column(Float)
#     risk_level = Column(String)
#     recommendation = Column(String)
#     rule_used = Column(String)
