import pandas as pd
import torch
from sanfis import SANFIS
from sklearn.metrics import classification_report
import pickle

# === 1. Загрузка подготовленных данных ===
X_train = pd.read_csv("anfis_X_train.csv").values
y_train = pd.read_csv("anfis_y_train.csv").values.ravel()
X_test = pd.read_csv("anfis_X_test.csv").values
y_test = pd.read_csv("anfis_y_test.csv").values.ravel()

# === 2. Преобразование в тензоры ===
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train.reshape(-1, 1), dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test.reshape(-1, 1), dtype=torch.float32)

# === 3. Настройка функций принадлежности ===
input_dim = X_train.shape[1]
membfuncs = [
    {
        'function': 'gaussian',
        'n_memb': 3,
        'params': {
            'mu': {'value': [-0.5, 0.0, 0.5], 'trainable': True},
            'sigma': {'value': [1.0, 1.0, 1.0], 'trainable': True}
        }
    }
] * input_dim

# === 4. Инициализация модели SANFIS ===
model = SANFIS(membfuncs=membfuncs, n_input=input_dim)

optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = torch.nn.MSELoss()

# === 5. Обучение ===
EPOCHS = 150
for epoch in range(EPOCHS):
    model.train()
    optimizer.zero_grad()
    output = model(X_batch=X_train, S_batch=X_train)
    loss = loss_fn(output, y_train)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch + 1}/{EPOCHS} - Loss: {loss.item():.4f}")

# === 6. Предсказание и метрики ===
model.eval()
with torch.no_grad():
    y_pred = model(X_batch=X_test, S_batch=X_test)
    y_pred_classes = (y_pred > 0.5).int().numpy()
    y_true = y_test.numpy().astype(int)

print("\n📊 Classification Report (SANFIS):")
print(classification_report(y_true, y_pred_classes))

# === 7. Сохранение модели и конфигурации ===
torch.save(model.state_dict(), "../sanfis_model.pt")
with open("../sanfis_membfuncs.pkl", "wb") as f:
    pickle.dump(membfuncs, f)

print("✅ SANFIS модель и параметры сохранены")
