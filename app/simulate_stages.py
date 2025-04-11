import requests
import random
import time
from datetime import datetime

API_URL = "http://localhost:8000"

# === Названия этапов ===
STAGE_NAMES = ["Mixing", "Granulation", "Drying", "Pressing", "Coating", "Packaging"]

# === Создание партии ===
def create_batch():
    res = requests.post(f"{API_URL}/batches", json={})
    res.raise_for_status()
    return res.json()["id"]

# === Создание этапа ===
def create_stage(batch_id, name):
    payload = {
        "batch_id": batch_id,
        "name": name
    }
    res = requests.post(f"{API_URL}/stages", json=payload)
    res.raise_for_status()
    return res.json()["id"]

# === Отправка сенсорных данных ===
def send_stage_data(stage_id):
    data = {
        "stage_id": stage_id,
        "temperature": round(random.uniform(20, 40), 2),
        "pressure": round(random.uniform(1.0, 2.5), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "composition": {
            "NaCl": round(random.uniform(0.4, 0.6), 2),
            "KCl": round(random.uniform(0.2, 0.3), 2)
        }
    }
    res = requests.post(f"{API_URL}/stage-data", json=data)
    res.raise_for_status()
    return data

# === Предсказание вероятности брака ===
def send_prediction(stage_id, sensor_data):
    prob = 0.1
    if sensor_data["pressure"] > 1.8 and sensor_data["humidity"] < 45:
        prob = 0.8

    recommendation = None
    if prob > 0.6:
        recommendation = "Понизить давление и увлажнить установку."

    payload = {
        "stage_id": stage_id,
        "defect_prob": prob,
        "recommendation": recommendation
    }
    res = requests.post(f"{API_URL}/stage-predictions", json=payload)
    res.raise_for_status()

# === Основной цикл ===
def run_simulation():
    batch_id = create_batch()
    print(f"[✓] Создана партия #{batch_id}")

    for stage_name in STAGE_NAMES:
        stage_id = create_stage(batch_id, stage_name)
        print(f"  └ Этап: {stage_name} (id={stage_id})")

        for _ in range(5):  # по 5 измерений на этап
            sensor_data = send_stage_data(stage_id)
            send_prediction(stage_id, sensor_data)
            print(f"    └ Sensor: {sensor_data}")
            time.sleep(0.5)

    print("\n[✓] Симуляция завершена успешно!")

if __name__ == "__main__":
    run_simulation()
