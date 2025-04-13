import torch
import pickle

# === Чтение конфигурации из .pkl файла ===
def load_pkl(file_path):
    print(f"Загрузка .pkl файла: {file_path}")
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    print("Содержимое .pkl файла:")
    print(data)  # Вывод содержимого .pkl файла
    return data

# === Чтение параметров модели из .pt файла ===
def load_pt(file_path):
    print(f"Загрузка .pt файла: {file_path}")
    model_state = torch.load(file_path)
    print("Ключи state_dict модели:")
    for key in model_state.keys():
        print(f"- {key}")  # Список ключей из state_dict
    return model_state

# === Анализ структуры модели SANFIS ===
def analyze_model(model):
    print("Анализ структуры модели SANFIS:")
    print("Доступные атрибуты:")
    print(dir(model))
    print("Обучаемые параметры:")
    for name, param in model.named_parameters():
        print(f"- {name}: {param.shape}")


# Укажите пути к вашим файлам
pkl_file = "models/sanfis_membfuncs.pkl"
pt_file = "models/sanfis_model.pt"

# Загрузка и анализ .pkl файла
membfuncs = load_pkl(pkl_file)

# Загрузка и анализ .pt файла
model_state = load_pt(pt_file)

# Если нужно загрузить модель и проанализировать её структуру
from sanfis import SANFIS  # Убедитесь, что библиотека SANFIS доступна

input_dim = len(membfuncs)  # Определяем количество входов из .pkl файла
model = SANFIS(membfuncs=membfuncs, n_input=input_dim)
model.load_state_dict(model_state)
analyze_model(model)
