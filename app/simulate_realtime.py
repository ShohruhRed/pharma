import requests
import random
import time
from datetime import datetime

API_URL    = "http://localhost:8000/api/v1"
STAGE_NAMES = ["Mixing", "Granulation", "Drying", "Pressing", "Coating", "Packaging"]

RANGES = {
    "temperature": (20.0, 40.0),
    "pressure":    (1.0,  2.5),
    "humidity":    (30.0, 70.0),
    "NaCl":        (0.4,  0.6),
    "KCl":         (0.2,  0.3),
}


def create_batch():
    r = requests.post(f"{API_URL}/batches", json={})
    r.raise_for_status()
    return r.json()["id"]


def create_stage(batch_id: int, name: str):
    r = requests.post(f"{API_URL}/stages", json={"batch_id": batch_id, "name": name})
    r.raise_for_status()
    return r.json()["id"]


def send_stage_data(stage_id: int):
    """Отправляет одно измерение сенсоров, возвращает словарь sensor."""
    now = datetime.utcnow().isoformat()
    payload = {
        "stage_id":    stage_id,
        "timestamp":   now,
        "temperature": round(random.uniform(*RANGES["temperature"]), 2),
        "pressure":    round(random.uniform(*RANGES["pressure"]),    2),
        "humidity":    round(random.uniform(*RANGES["humidity"]),    2),
        "composition": {
            "NaCl": round(random.uniform(*RANGES["NaCl"]), 2),
            "KCl":  round(random.uniform(*RANGES["KCl"]),  2),
        }
    }
    r = requests.post(f"{API_URL}/stage-data", json=payload)
    r.raise_for_status()
    return payload


def get_sanfis_prediction(sensor: dict):
    """Запрос к /sanfis-predict, подставляем правильные имена полей."""
    inp = {
        "stage_id":    sensor["stage_id"],
        "temperature": sensor["temperature"],
        "pressure":    sensor["pressure"],
        "humidity":    sensor["humidity"],
        "NaCl":        sensor["composition"]["NaCl"],
        "KCl":         sensor["composition"]["KCl"],
    }
    r = requests.post(f"{API_URL}/sanfis-predict", json=inp)
    if r.status_code == 422:
        print("🛑 Sanfis 422 error:", r.json())
    r.raise_for_status()
    return r.json()


def log_sanfis(stage_id: int, sensor: dict, sf: dict):
    # """Записываем предсказание в общий /predictions."""
    # entry = {
    #     "stage_id":           stage_id,
    #     "timestamp":          datetime.utcnow().isoformat(),
    #     "temperature":        sensor["temperature"],
    #     "pressure":           sensor["pressure"],
    #     "humidity":           sensor["humidity"],
    #     "NaCl":               sensor["composition"]["NaCl"],
    #     "KCl":                sensor["composition"]["KCl"],
    #     "defect_probability": sf["defect_probability"],
    #     "risk_level":         sf["risk_level"],
    #     "recommendation":     sf["recommendation"],
    #     "source_model":       "sanfis",
    #     "rule_used":          sf.get("rule_used"),
    # }
    # r = requests.post(f"{API_URL}/predictions", json=entry)
    # r.raise_for_status()
    pass


def run_simulation_sanfis(measurements_per_stage: int = 5):
    print("=== Стартуем симуляцию только для SANFIS ===")
    batch_id = create_batch()
    print(f"[+] Создана партия #{batch_id}")

    # 1) Создаём все этапы один раз
    stage_ids = {}
    for name in STAGE_NAMES:
        sid = create_stage(batch_id, name)
        stage_ids[name] = sid
        print(f"  • Этап {name} (id={sid})")

    # 2) По очереди делаем measurements_per_stage замеров на каждом этапе
    for name, sid in stage_ids.items():
        print(f"--- {name}: {measurements_per_stage} замеров ---")
        for i in range(1, measurements_per_stage + 1):
            sensor = send_stage_data(sid)
            sf     = get_sanfis_prediction(sensor)
            log_sanfis(sid, sensor, sf)
            print(f"  [{name}·{i}] prob={sf['defect_probability']:.2f}, "
                  f"risk={sf['risk_level']}, rule={sf.get('rule_used','-')}")
            time.sleep(random.uniform(0.5, 1.5))


if __name__ == "__main__":
    run_simulation_sanfis(5)
