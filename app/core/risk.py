def classify_risk(prob: float):
    if prob > 0.6:
        return "high", "🔴 Немедленно вмешаться"
    elif prob > 0.3:
        return "medium", "🟡 Проверьте условия"
    else:
        return "low", "🟢 Всё в норме"
