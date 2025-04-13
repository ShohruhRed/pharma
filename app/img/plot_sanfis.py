import torch
import matplotlib.pyplot as plt
import pickle

# Загрузка сохранённых membfuncs
with open("../sanfis_membfuncs.pkl", "rb") as f:
    membfuncs = pickle.load(f)

# Названия признаков
feature_names = ["temperature", "pressure", "humidity", "NaCl", "KCl"]

# Визуализация
x = torch.linspace(0, 1, 300)

for i, funcs in enumerate(membfuncs):
    plt.figure(figsize=(6, 4))
    for mf in funcs:
        y = mf(x)
        plt.plot(x.numpy(), y.numpy(), label=str(mf))
    plt.title(f"Функции принадлежности — {feature_names[i]}")
    plt.xlabel("Нормализованное значение")
    plt.ylabel("Принадлежность")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"mf_{feature_names[i]}.png")
    plt.show()
