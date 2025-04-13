import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# === 1. Загрузка нового реалистичного датасета ===
df = pd.read_csv("../ml_dataset_balanced.csv")

# === 2. Подготовка признаков и целевой переменной ===
X = df[["temperature", "pressure", "humidity", "NaCl", "KCl"]]
y = df["is_defect"]

# === 3. Разделение на тренировочную и тестовую выборки ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# === 4. Обучение модели RandomForest с балансировкой классов ===
clf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)
clf.fit(X_train, y_train)

# === 5. Оценка модели ===
y_pred = clf.predict(X_test)
print("\n📊 Classification Report (Random Forest):")
print(classification_report(y_test, y_pred))
print("✅ Accuracy:", accuracy_score(y_test, y_pred))

# === 6. Сохранение обученной модели ===
joblib.dump(clf, "../defect_predictor_final.pkl")
print("✅ Модель сохранена как defect_predictor_final.pkl")
