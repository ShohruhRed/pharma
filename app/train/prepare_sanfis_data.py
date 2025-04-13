import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# === 1. Загрузка CSV-файла ===
df = pd.read_csv("../data/ml_dataset_balanced.csv")  # Замените на путь к вашему датасету

# === 2. Выбор признаков и целевого признака ===
X = df[["temperature", "pressure", "humidity", "NaCl", "KCl"]].values
y = df["is_defect"].values

# === 3. Нормализация признаков в диапазоне [0, 1] ===
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# === 4. Разделение на обучающую и тестовую выборки ===
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# === 5. Сохранение подготовленных данных для SANFIS-модели ===
pd.DataFrame(X_train, columns=["temperature", "pressure", "humidity", "NaCl", "KCl"]).to_csv("anfis_X_train.csv", index=False)
pd.DataFrame(y_train, columns=["is_defect"]).to_csv("anfis_y_train.csv", index=False)
pd.DataFrame(X_test, columns=["temperature", "pressure", "humidity", "NaCl", "KCl"]).to_csv("anfis_X_test.csv", index=False)
pd.DataFrame(y_test, columns=["is_defect"]).to_csv("anfis_y_test.csv", index=False)

print("✅ Данные подготовлены для обучения SANFIS-модели.")
