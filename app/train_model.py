import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# === 1. Загрузка датасета ===
df = pd.read_csv("ml_dataset_balanced.csv")  # Убедись, что файл рядом

# === 2. Подготовка признаков ===
X = df[["temperature", "pressure", "humidity", "NaCl", "KCl"]]
y = df["is_defect"]

# === 3. Разделение на train/test ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# === 4. Обучение модели с балансировкой классов ===
clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
clf.fit(X_train, y_train)

# === 5. Оценка модели ===
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
print(accuracy_score(y_test, y_pred))

# === 6. Сохранение модели ===
joblib.dump(clf, "defect_predictor_final.pkl")
print("✅ Модель сохранена как defect_predictor_final.pkl")
