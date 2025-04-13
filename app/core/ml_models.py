import joblib
import pickle
import torch
import itertools
import numpy as np
from sanfis import SANFIS

# === ML model ===
ml_model = joblib.load("app/models/defect_predictor_final.pkl")

# === SANFIS ===
with open("app/models/sanfis_membfuncs.pkl", "rb") as f:
    membfuncs = pickle.load(f)

sanfis_model = SANFIS(membfuncs=membfuncs, n_input=5)
sanfis_model.load_state_dict(torch.load("app/models/sanfis_model.pt"))
sanfis_model.eval()

# === Правила для SANFIS ===
feature_names = ["temperature", "pressure", "humidity", "NaCl", "KCl"]

def generate_rules_dict(model):
    trained_mfs = {}
    for key, value in model.state_dict().items():
        if "fuzzylayer.fuzzyfication" in key:
            param_type = "mu" if "_mu" in key else "sigma"
            layer_index = int(key.split('.')[3])
            if layer_index not in trained_mfs:
                trained_mfs[layer_index] = {"mu": None, "sigma": None}
            trained_mfs[layer_index][param_type] = value.numpy()

    n_memb = trained_mfs[0]["mu"].shape[1]
    input_dim = len(trained_mfs)
    combinations = list(itertools.product(range(n_memb), repeat=input_dim))
    rules_dict = {}

    for combo in combinations:
        condition_parts = []
        inputs = []
        for i, mf_index in enumerate(combo):
            mu = trained_mfs[i]["mu"][0, mf_index]
            sigma = trained_mfs[i]["sigma"][0, mf_index]
            feature_name = feature_names[i]
            condition_parts.append(
                f"{feature_name} IS MF{mf_index+1} (mu={mu:.4f}, sigma={sigma:.4f})"
            )
            inputs.append(mu)
        rule_str = "IF " + " AND ".join(condition_parts)
        rules_dict[tuple(inputs)] = rule_str

    return rules_dict

rules_dict = generate_rules_dict(sanfis_model)
