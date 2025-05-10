import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# === 1. Загрузка нового реалистичного датасета ===
df = pd.read_csv("../data/ml_dataset_balanced.csv")

# === 2. Маппинг этапов в индекс ===
stage_map = {
    "Mixing":      0,
    "Granulation": 1,
    "Drying":      2,
    "Pressing":    3,
    "Coating":     4,
    "Packaging":   5
}
df["stage_idx"] = df["stage"].map(stage_map)

# === 3. Подготовка признаков и целевой переменной ===
FEATURES = ["temperature", "pressure", "humidity", "NaCl", "KCl", "stage_idx"]
X = df[FEATURES]
y = df["is_defect"]

# === 4. Разделение на тренировочную и тестовую выборки ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# === 5. Обучение модели RandomForest с учётом дисбаланса классов ===
clf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)
clf.fit(X_train, y_train)

# === 6. Оценка качества на тесте ===
y_pred = clf.predict(X_test)
print("\n📊 Classification Report (Random Forest):")
print(classification_report(y_test, y_pred, digits=4))
print(f"✅ Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# === 7. Сохранение обученной модели и списка фичей ===
joblib.dump(clf, "../models/defect_predictor_final.pkl")
# На всякий случай — сохраните порядок колонок, чтобы при инференсе делать pd.DataFrame(data, columns=FEATURES)
joblib.dump(FEATURES, "../models/defect_predictor_features.pkl")

print("✅ Модель сохранена как defect_predictor_final.pkl")
print("✅ Список признаков сохранён как defect_predictor_features.pkl")
