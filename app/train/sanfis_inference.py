import pickle
import torch
import numpy as np
from sanfis import SANFIS

# === 1) Загружаем membfuncs и модель ===
with open("../models/sanfis_membfuncs.pkl", "rb") as f:
    membfuncs = pickle.load(f)

model = SANFIS(membfuncs=membfuncs, n_input=len(membfuncs))
model.load_state_dict(torch.load("../models/sanfis_model.pt", map_location="cpu"))
model.eval()


# === 2) Нормализация входных данных ===
def normalize_data(X, train_min, train_max):
    return (X - train_min) / (train_max - train_min)


def predict_sanfis(raw_values: np.ndarray, train_min: np.ndarray, train_max: np.ndarray) -> float:
    """
    raw_values: numpy array shape (1, n_features),
      в том же порядке, что и при тренировке.
    train_min, train_max: минимальные и максимальные значения обучающей выборки.
    """
    # Нормализация входных данных
    raw_norm = normalize_data(raw_values, train_min, train_max)

    X = torch.tensor(raw_norm, dtype=torch.float32)
    with torch.no_grad():
        out = model(X_batch=X, S_batch=X)

    # Проверка выхода перед `sigmoid`
    print(f"Выход SANFIS перед sigmoid: {out.numpy()}")

    return torch.sigmoid(out).item()


# === 3) Пример вызова ===
if __name__ == "__main__":
    # Передача диапазона нормализации
    train_min = np.load("../models/train_min.npy")
    train_max = np.load("../models/train_max.npy")

    raw = np.array([[44.64, 1.87, 44.97, 0.2, 0.2]])
    prob = predict_sanfis(raw, train_min, train_max)
    print(f"Вероятность дефекта (SANFIS): {prob:.3f}")
