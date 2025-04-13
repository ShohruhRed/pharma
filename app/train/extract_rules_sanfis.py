import torch
import pickle
import itertools
import pandas as pd
from sanfis import SANFIS

model_path = "../sanfis_model.pt"
membfuncs_path = "../sanfis_membfuncs.pkl"
feature_names = ["temperature", "pressure", "humidity", "NaCl", "KCl"]

with open(membfuncs_path, "rb") as f:
    membfuncs = pickle.load(f)

input_dim = len(membfuncs)
model = SANFIS(membfuncs=membfuncs, n_input=input_dim)
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

def extract_trained_mf_params(model):
    trained_mfs = {}
    for key, value in model.state_dict().items():
        if "fuzzylayer.fuzzyfication" in key:
            param_type = "mu" if "_mu" in key else "sigma"
            layer_index = int(key.split('.')[3])
            if layer_index not in trained_mfs:
                trained_mfs[layer_index] = {"mu": None, "sigma": None}
            trained_mfs[layer_index][param_type] = value.numpy()
    return trained_mfs

trained_mfs = extract_trained_mf_params(model)

rules_data = []
combinations = list(itertools.product(range(trained_mfs[0]["mu"].shape[1]), repeat=input_dim))

for combo in combinations:
    conditions = []
    inputs = []
    for i, mf_index in enumerate(combo):
        mu = trained_mfs[i]["mu"][0, mf_index]
        sigma = trained_mfs[i]["sigma"][0, mf_index]
        feature_name = feature_names[i]
        conditions.append(f"{feature_name} IS MF{mf_index+1} (mu={mu:.4f}, sigma={sigma:.4f})")
        inputs.append(mu)

    with torch.no_grad():
        X_batch = torch.tensor([inputs], dtype=torch.float32)
        S_batch = X_batch
        prediction = model(X_batch=X_batch, S_batch=S_batch).item()

    risk_level = (
        "🟢 low" if prediction < 0.4 else
        "🟡 medium" if prediction < 0.7 else
        "🔴 high"
    )

    rules_data.append({
        "Rule": f"IF {' AND '.join(conditions)}",
        "Output": f"{prediction:.4f}",
        "Risk Level": risk_level
    })

df_rules = pd.DataFrame(rules_data)
df_rules.to_csv("sanfis_rules.csv", index=False)
df_rules.to_markdown("sanfis_rules.md", index=False)

print("✅ Правила сохранены в 'sanfis_rules.csv' и 'sanfis_rules.md'")
