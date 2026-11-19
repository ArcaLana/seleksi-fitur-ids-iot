"""Jilid 2, Bab 5 (tambahan): sensitivitas parameter L1, langkah RFE, jenis importance, ulangan permutation. python3 -I run_b5x.py <seed> <keluaran>"""
import sys, json, time, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from xgboost import XGBClassifier
SEED = int(sys.argv[1]); OUT = sys.argv[2]
D = "output/"
X = pd.concat([pd.read_csv(D+"X_train.csv"), pd.read_csv(D+"X_test.csv")], ignore_index=True).drop(columns=["proto","service"])
y = np.concatenate([pd.read_csv(D+"y_train.csv")["y"].values, pd.read_csv(D+"y_test.csv")["y"].values]); fitur = list(X.columns)
itr, ite = train_test_split(np.arange(len(X)), test_size=0.30, stratify=y, random_state=SEED)
Xtr, Xte, ytr, yte = X.values[itr], X.values[ite], y[itr], y[ite]
def xgb(n=100, d=6): return XGBClassifier(learning_rate=0.1, max_depth=d, n_estimators=n, tree_method="hist", n_jobs=2, random_state=SEED, verbosity=0)
def f1(ci): ci = list(ci); return f1_score(yte, xgb().fit(Xtr[:, ci], ytr).predict(Xte[:, ci]), average="macro")
rows = []; fs = {}
s40, _ = train_test_split(np.arange(len(Xtr)), train_size=40000, stratify=ytr, random_state=SEED)
sc = StandardScaler().fit(Xtr[s40]); Z = sc.transform(Xtr[s40])
for Cc in (0.01, 0.05, 0.2):                                   # a) kekuatan penalti L1
    t = time.perf_counter(); lr = LogisticRegression(penalty="l1", solver="saga", C=Cc, max_iter=150, tol=1e-3).fit(Z, ytr[s40]); dt = time.perf_counter() - t
    w = np.abs(lr.coef_).max(axis=0); nz = int((w > 0).sum()); r = list(np.argsort(-w)); fs[f"l1_C{Cc}"] = [fitur[i] for i in r[:40]]
    rows.append(dict(seed=SEED, kelompok="L1", pengaturan=f"C={Cc}", waktu=dt, n_taknol=nz, f1_k20=f1(r[:20]), f1_himpunan_taknol=f1(r[:nz]) if 1 <= nz <= 80 else np.nan))
s30, _ = train_test_split(np.arange(len(Xtr)), train_size=30000, stratify=ytr, random_state=SEED)
ref = None
for st in (1, 5, 10):                                          # b) langkah pembuangan RFE
    t = time.perf_counter(); rf = RFE(xgb(40, 4), n_features_to_select=20, step=st).fit(Xtr[s30], ytr[s30]); dt = time.perf_counter() - t
    sel = set(np.where(rf.support_)[0]); ref = sel if ref is None else ref
    fs[f"rfe_step{st}"] = [fitur[i] for i in sorted(sel)]
    rows.append(dict(seed=SEED, kelompok="RFE", pengaturan=f"step={st}", waktu=dt, f1_k20=f1(sorted(sel)), jaccard_vs_step1=len(sel & ref) / len(sel | ref)))
mod = xgb().fit(Xtr, ytr); bst = mod.get_booster()
for tp in ("gain", "weight", "cover", "total_gain", "total_cover"):   # c) jenis importance XGBoost
    sk = bst.get_score(importance_type=tp); v = np.array([sk.get(f"f{i}", 0.0) for i in range(len(fitur))]); r = list(np.argsort(-v)); fs[f"imp_{tp}"] = [fitur[i] for i in r[:40]]
    rows.append(dict(seed=SEED, kelompok="importance_XGB", pengaturan=tp, waktu=0.0, f1_k10=f1(r[:10]), f1_k20=f1(r[:20])))
i1, i2 = train_test_split(np.arange(len(Xtr)), test_size=0.2, stratify=ytr, random_state=SEED); mv = xgb().fit(Xtr[i1], ytr[i1])
for nr in (1, 3, 10):                                          # d) jumlah ulangan permutation
    t = time.perf_counter(); pi = permutation_importance(mv, Xtr[i2[:8000]], ytr[i2[:8000]], n_repeats=nr, random_state=SEED, scoring="f1_macro", n_jobs=1); dt = time.perf_counter() - t
    r = list(np.argsort(-pi.importances_mean)); fs[f"perm_n{nr}"] = [fitur[i] for i in r[:40]]
    rows.append(dict(seed=SEED, kelompok="permutation", pengaturan=f"n_repeats={nr}", waktu=dt, f1_k10=f1(r[:10]), f1_k20=f1(r[:20])))
json.dump(fs, open(f"{OUT}/b5x_fitur_seed{SEED}.json", "w")); pd.DataFrame(rows).to_csv(f"{OUT}/b5x_seed{SEED}.csv", index=False); print("b5x seed", SEED, "ok", flush=True)
