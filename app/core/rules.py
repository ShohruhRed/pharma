import pickle, torch, itertools, numpy as np
from sanfis import SANFIS

with open("app/models/sanfis_membfuncs.pkl", "rb") as f:
    membfuncs = pickle.load(f)

sanfis_model = SANFIS(membfuncs=membfuncs, n_input=5)
sanfis_model.load_state_dict(torch.load("app/models/sanfis_model.pt", map_location="cpu"))
sanfis_model.eval()

def generate_rules_dict(model, feature_names):
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
    rules = {}

    for combo in combinations:
        cond = []
        inputs = []
        for i, mf_index in enumerate(combo):
            mu = trained_mfs[i]["mu"][0, mf_index]
            sigma = trained_mfs[i]["sigma"][0, mf_index]
            cond.append(f"{['temperature', 'pressure', 'humidity', 'NaCl', 'KCl'][i]} IS MF{mf_index+1} (mu={mu:.4f}, sigma={sigma:.4f})")
            inputs.append(mu)
        rules[tuple(inputs)] = "IF " + " AND ".join(cond)

    return rules

rules_dict = generate_rules_dict(sanfis_model, ["temperature", "pressure", "humidity", "NaCl", "KCl"])
