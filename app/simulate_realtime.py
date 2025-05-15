# simulate_realtime.py

import requests
import random
import time
from datetime import datetime

API_URL = "http://localhost:8000/api/v1"
STAGE_NAMES = ["Mixing", "Granulation", "Drying", "Pressing", "Coating", "Packaging"]
STAGE_MAP = {
    "Mixing": 0, "Granulation": 1, "Drying": 2, "Pressing": 3, "Coating": 4, "Packaging": 5
}
RANGES = {
    "temperature": (20.0, 43.0),
    "pressure":    (1.0,  2.7),
    "humidity":    (30.0, 70.0),
    "NaCl":        (0.4,  0.7),
    "KCl":         (0.2,  0.3),
}

def create_stage(batch_id: int, name: str):
    r = requests.post(f"{API_URL}/stages", json={"batch_id": batch_id, "name": name})
    r.raise_for_status()
    return r.json()["id"]

def send_stage_data(stage_id: int, stage_name: str):
    """Отправляет измерение сенсоров, включая `stage_idx` и `composition`."""
    now = datetime.utcnow().isoformat()
    stage_idx = int(STAGE_MAP.get(stage_name, -1))  # 📌 Если этап неизвестен, `stage_idx = -1`

    payload = {
        "stage_id": stage_id,
        "timestamp": now,
        "temperature": round(random.uniform(*RANGES["temperature"]), 2),
        "pressure": round(random.uniform(*RANGES["pressure"]), 2),
        "humidity": round(random.uniform(*RANGES["humidity"]), 2),
        "composition": {  # 📌 Теперь `NaCl` и `KCl` внутри `composition`
            "NaCl": round(random.uniform(*RANGES["NaCl"]), 2),
            "KCl": round(random.uniform(*RANGES["KCl"]), 2),
        },
        "stage_idx": stage_idx  # 📌 `stage_idx` остаётся отдельным
    }

    # 🔎 Проверяем, что `composition` присутствует
    import json
    print(f"🔎 Отправляем в API:\n{json.dumps(payload, indent=2)}")

    r = requests.post(f"{API_URL}/stage-data", json=payload)
    r.raise_for_status()
    return payload

def get_sanfis_prediction(sensor: dict):
    """Запрос к SANFIS API, включая `NaCl` и `KCl` как отдельные поля."""
    inp = {
        "stage_id":    sensor["stage_id"],
        "temperature": sensor["temperature"],
        "pressure":    sensor["pressure"],
        "humidity":    sensor["humidity"],
        "NaCl":        sensor["composition"]["NaCl"],  # 📌 Теперь передаём напрямую!
        "KCl":         sensor["composition"]["KCl"],  # 📌 Теперь передаём напрямую!
        "stage_idx":   sensor["stage_idx"]
    }

    # 🔎 Проверяем, что `NaCl` и `KCl` правильно переданы
    import json
    print(f"🔎 Запрос в SANFIS API:\n{json.dumps(inp, indent=2)}")

    r = requests.post(f"{API_URL}/sanfis-predict", json=inp)
    if r.status_code == 422:
        print(f"🛑 Sanfis 422 error: {r.json()}")
    r.raise_for_status()
    return r.json()

def log_sanfis(stage_id: int, sensor: dict, sf: dict):
    # entry = {
    #     "stage_id":          stage_id,
    #     "timestamp":         sensor["timestamp"],
    #     "temperature":       sensor["temperature"],
    #     "pressure":          sensor["pressure"],
    #     "humidity":          sensor["humidity"],
    #     "NaCl":              sensor["composition"]["NaCl"],
    #     "KCl":               sensor["composition"]["KCl"],
    #     "stage_idx":         sensor["stage_idx"],
    #     "defect_probability":sf["defect_probability"],
    #     "risk_level":        sf["risk_level"],
    #     "recommendation":    sf["recommendation"],
    #     "source_model":      "sanfis",
    #     "rule_used":         sf.get("rule_used")
    # }
    #      requests.post(f"{API_URL}/predictions", json=entry).raise_for_status()
    pass
def simulate_for_batch(batch_id: int, measurements_per_stage: int = 5):
    """
    Симулирует этапы, замеры и предсказания для уже созданной партии.
    """
    print(f"🚀 Start simulation for batch {batch_id}")
    stage_ids = {}
    for name in STAGE_NAMES:
        sid = create_stage(batch_id, name)
        stage_ids[name] = sid
        print(f"  • Этап {name} (id={sid})")

    for name, sid in stage_ids.items():
        print(f"--- {name}: {measurements_per_stage} замеров ---")
        for i in range(1, measurements_per_stage + 1):
            sensor = send_stage_data(sid, name)  # 📌 Теперь `stage_idx` передаётся корректно
            sf = get_sanfis_prediction(sensor)
            log_sanfis(sid, sensor, sf)
            print(f"  [{name}·{i}] prob={sf['defect_probability']:.2f}, "
                  f"risk={sf['risk_level']}, rule={sf.get('rule_used', '-')}")
            time.sleep(random.uniform(0.5, 1.5))

# старый entry-point, если нужно
# def run_simulation_sanfis(measurements_per_stage: int = 5):
#     batch_id = create_batch()
#     simulate_for_batch(batch_id, measurements_per_stage)
