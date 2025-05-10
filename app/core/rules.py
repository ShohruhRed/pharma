import pickle, torch, itertools, numpy as np
from sanfis import SANFIS

# 1) загрузка membfuncs и модели
with open("app/models/sanfis_membfuncs.pkl", "rb") as f:
    membfuncs = pickle.load(f)

sanfis_model = SANFIS(membfuncs=membfuncs, n_input=len(membfuncs))
sanfis_model.load_state_dict(
    torch.load("app/models/sanfis_model.pt", map_location="cpu")
)
sanfis_model.eval()

# 2) имена фичей в том же порядке, что и в membfuncs
feature_names = ["temperature", "pressure", "humidity", "NaCl", "KCl", "stage_idx"]

def generate_rules_dict(model, membfuncs, feature_names):
    state = model.state_dict()
    input_dim = len(feature_names)

    trained_mfs = []
    for i, mf in enumerate(membfuncs):
        key_mu    = f"layers.fuzzylayer.fuzzyfication.{i}._mu"
        key_sigma = f"layers.fuzzylayer.fuzzyfication.{i}._sigma"

        if key_mu in state and key_sigma in state:
            mu_vals    = state[key_mu].numpy()[0]
            sigma_vals = state[key_sigma].numpy()[0]
        else:
            # если нет обучаемых параметров (как для stage_idx), берём из membfuncs
            mu_vals    = np.array(mf["params"]["mu"]["value"], dtype=float)
            sigma_vals = np.array(mf["params"]["sigma"]["value"], dtype=float)

        trained_mfs.append({"mu": mu_vals, "sigma": sigma_vals})

    # генерируем все возможные правила
    n_memb = trained_mfs[0]["mu"].shape[0]
    combos = itertools.product(range(n_memb), repeat=input_dim)

    rules = {}
    for combo in combos:
        vec = []; cond = []
        for idx, mf_idx in enumerate(combo):
            name  = feature_names[idx]
            mu    = trained_mfs[idx]["mu"][mf_idx]
            sigma = trained_mfs[idx]["sigma"][mf_idx]
            cond.append(f"{name} IS MF{mf_idx+1} (μ={mu:.3f}, σ={sigma:.3f})")
            vec.append(mu)
        rules[tuple(vec)] = "IF " + " AND ".join(cond)

    return rules

# создаём словарь правил
rules_dict = generate_rules_dict(sanfis_model, membfuncs, feature_names)
