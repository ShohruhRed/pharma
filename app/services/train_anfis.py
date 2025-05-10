import pandas as pd
import torch
import numpy as np
from sanfis import SANFIS
from sklearn.metrics import classification_report
import pickle
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt

# === 1. Загрузка ML-датасета ===
data = pd.read_csv("../data/ml_dataset_balanced.csv")
X_train = data.drop(columns=["batch_id", "stage", "defect_prob", "is_defect"]).values
y_train = data["is_defect"].values.astype(int)  # Метки дефектов

# === 2. Выделяем тестовую выборку ===
X_test = X_train[:300]  # Первые 300 примеров для тестирования
y_test = y_train[:300]

# === 3. Проверяем баланс классов и применяем SMOTE ===
class_counts = np.bincount(y_train)
print(f"Баланс классов перед SMOTE: {class_counts}")

if class_counts[1] < class_counts[0]:  # Балансируем классы, если дефекты в меньшинстве
    smote = SMOTE(sampling_strategy="minority", random_state=42)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    print(f"Баланс классов после SMOTE: {np.bincount(y_train_balanced)}")
else:
    X_train_balanced, y_train_balanced = X_train, y_train

# === 4. Нормализация данных ===
def normalize_data(X, train_min, train_max):
    return (X - train_min) / (train_max - train_min)

train_min = X_train_balanced.min(axis=0)
train_max = X_train_balanced.max(axis=0)
X_train_balanced = normalize_data(X_train_balanced, train_min, train_max)
X_test = normalize_data(X_test, train_min, train_max)

# === 5. Сохранение нормализационных параметров ===
np.save("../models/train_min.npy", train_min)
np.save("../models/train_max.npy", train_max)

# === 6. Преобразование в тензоры ===
X_train_balanced = torch.tensor(X_train_balanced, dtype=torch.float32)
y_train_balanced = torch.tensor(y_train_balanced.reshape(-1, 1), dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test.reshape(-1, 1), dtype=torch.float32)

# === 7. Используем мини-батчи ===
batch_size = 32
train_loader = torch.utils.data.DataLoader(list(zip(X_train_balanced, y_train_balanced)), batch_size=batch_size, shuffle=True)

# === 8. Инициализация модели SANFIS ===
input_dim = X_train_balanced.shape[1]
membfuncs = [
    {
        'function': 'gaussian',
        'n_memb': 5,  # Увеличиваем чувствительность модели
        'params': {
            'mu': {'value': np.linspace(0, 1, 5).tolist(), 'trainable': True},
            'sigma': {'value': [0.15] * 5, 'trainable': True}
        }
    }
] * input_dim

model = SANFIS(membfuncs=membfuncs, n_input=input_dim)

# === 9. Используем `Adam` для обучения ===
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
loss_fn = torch.nn.BCEWithLogitsLoss()

# === 10. Обучение модели (EPOCHS = 300) ===
EPOCHS = 300
for epoch in range(EPOCHS):
    model.train()

    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        output = model(X_batch=X_batch, S_batch=X_batch)
        loss = loss_fn(output, y_batch.float())

        if torch.isnan(loss):
            print("⚠️ Обнаружены NaN! Пропускаем батч...")
            optimizer.zero_grad()
            continue

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # Ограничение градиентов
        optimizer.step()

    if (epoch + 1) % 50 == 0:
        print(f"Epoch {epoch + 1}/{EPOCHS} - Loss: {loss.item():.4f}")

# === 11. Оценка модели ===
threshold = 0.35
model.eval()
with torch.no_grad():
    y_pred_sanfis = torch.sigmoid(model(X_batch=X_test, S_batch=X_test)).numpy()
y_pred_ml = data["defect_prob"][:300].values  # Прогнозы ML

# === 12. Сравнение предсказаний SANFIS vs ML ===
comparison_df = pd.DataFrame({
    "ML_pred": y_pred_ml,
    "SANFIS_pred": y_pred_sanfis.flatten(),
    "Real_defect": y_test.numpy().flatten()
})

print("\n📊 Сравнение предсказаний SANFIS vs ML:")
print(comparison_df.head(15))  # Вывод первых 15 строк

# === 13. Визуализация расхождений ===
plt.figure(figsize=(8, 4))
plt.scatter(y_pred_ml, y_pred_sanfis, c=y_test.numpy().flatten(), cmap="coolwarm", alpha=0.7)
plt.xlabel("ML (defect_prob)")
plt.ylabel("SANFIS (defect probability)")
plt.title("Сравнение предсказаний SANFIS vs ML")
plt.colorbar(label="Истинный дефект (0 = нет, 1 = да)")
plt.savefig("../models/sanfis_vs_ml.png")
print("📊 График расхождений SANFIS vs ML сохранен!")

# === 14. Сохранение модели ===
torch.save(model.state_dict(), "../models/sanfis_model.pt")
with open("../models/sanfis_membfuncs.pkl", "wb") as f:
    pickle.dump(membfuncs, f)

print("✅ SANFIS обучен на ML-данных, сравнение с ML завершено!")
