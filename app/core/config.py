from app.db.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def classify_risk(prob: float):
    if prob > 0.6:
        return "high", "🔴 Немедленно вмешаться"
    elif prob > 0.3:
        return "medium", "🟡 Проверьте условия"
    else:
        return "low", "🟢 Всё в норме"
