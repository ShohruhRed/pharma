import pandas as pd
import torch
import numpy as np
from sanfis import SANFIS
from sklearn.metrics import classification_report
import pickle
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt

# 1) Загрузка сбалансированного ML-датаcета
df = pd.read_csv("../data/ml_dataset_balanced.csv")

# 1.1) Маппинг этапов в числовой индекс
stage_map = {
    "Mixing":      0,
    "Granulation": 1,
    "Drying":      2,
    "Pressing":    3,
    "Coating":     4,
    "Packaging":   5,
}
df["stage_idx"] = df["stage"].map(stage_map)

# 2) Формируем X и y (включаем stage_idx)
features = ["temperature", "pressure", "humidity", "NaCl", "KCl", "stage_idx"]
X = df[features].values.astype(float)
y = df["is_defect"].values.astype(int)

# 3) Тестовый срез для оценки
X_test = X[:300]
y_test = y[:300]

# 4) SMOTE (если «дефект» в меньшинстве)
counts = np.bincount(y)
print("Баланс до SMOTE:", counts)
if counts[1] < counts[0]:
    sm = SMOTE(sampling_strategy="minority", random_state=42)
    X_train, y_train = sm.fit_resample(X, y)
    print("Баланс после SMOTE:", np.bincount(y_train))
else:
    X_train, y_train = X, y

# 5) Нормализация [0–1]
min_, max_ = X_train.min(axis=0), X_train.max(axis=0)
def norm(a): return (a - min_) / (max_ - min_)
X_train = norm(X_train)
X_test  = norm(X_test)
# сохраняем параметры
np.save("../models/train_min.npy", min_)
np.save("../models/train_max.npy", max_)

# 6) Тензоры и DataLoader
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train.reshape(-1,1), dtype=torch.float32)
X_test  = torch.tensor(X_test,  dtype=torch.float32)
y_test  = torch.tensor(y_test.reshape(-1,1), dtype=torch.float32)

loader = torch.utils.data.DataLoader(
    list(zip(X_train, y_train)), batch_size=32, shuffle=True
)

# 7) Собираем membfuncs:
# — для 5 сенсоров: 5 гауссов с обучаемыми μ∈[0,1], σ∈[0.15]
sensor_mf = {
    "function":"gaussian", "n_memb":5,
    "params":{
        "mu":    {"value": np.linspace(0,1,5).tolist(), "trainable":True},
        "sigma": {"value": [0.15]*5,               "trainable":True}
    }
}
# — для stage_idx: 6 гауссов с фиксированными μ=0..5, σ=0.5
stage_mf = {
    "function":"gaussian", "n_memb":6,
    "params":{
        "mu":    {"value": list(range(6)), "trainable":False},
        "sigma": {"value": [0.5]*6,        "trainable":False}
    }
}
membfuncs = [sensor_mf]*5 + [stage_mf]       # всего 6 признаков
assert len(membfuncs) == X_train.shape[1]

# 8) Инициализация SANFIS
model = SANFIS(membfuncs=membfuncs, n_input=len(membfuncs))

# 9) Обучение
opt     = torch.optim.Adam(model.parameters(), lr=0.005)
loss_fn = torch.nn.BCEWithLogitsLoss()

EPOCHS = 300
for epoch in range(1, EPOCHS+1):
    model.train()
    for xb, yb in loader:
        opt.zero_grad()
        out = model(X_batch=xb, S_batch=xb)
        loss = loss_fn(out, yb)
        if torch.isnan(loss):
            opt.zero_grad()
            continue
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
    if epoch % 50 == 0:
        print(f"Epoch {epoch}/{EPOCHS} — loss: {loss.item():.4f}")

# 10) Оценка на тесте
model.eval()
with torch.no_grad():
    preds = torch.sigmoid(model(X_batch=X_test, S_batch=X_test)).numpy().flatten()
cls = (preds > 0.5).astype(int)
print("\nClassification Report (SANFIS):")
print(classification_report(y_test.numpy(), cls))

# 11) Сохраняем модель и membfuncs
torch.save(model.state_dict(),    "../models/sanfis_model.pt")
with open("../models/sanfis_membfuncs.pkl","wb") as f:
    pickle.dump(membfuncs, f)

print("✅ SANFIS обучен и сохранён")
