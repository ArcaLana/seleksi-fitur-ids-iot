"""Jilid 2, Bab 4 (tambahan): filter dengan pemangkasan korelasi. python3 -I run_b4x.py <seed> <keluaran>"""
import sys, json, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from sklearn.feature_selection import f_classif, chi2
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, recall_score
from xgboost import XGBClassifier
SEED = int(sys.argv[1]); OUT = sys.argv[2]
D = "output/"
X = pd.concat([pd.read_csv(D+"X_train.csv"), pd.read_csv(D+"X_test.csv")], ignore_index=True).drop(columns=["proto","service"])
y = np.concatenate([pd.read_csv(D+"y_train.csv")["y"].values, pd.read_csv(D+"y_test.csv")["y"].values])
peta = pd.read_csv(D+"pemetaan_label.csv"); nama = dict(zip(peta["kode"], peta["label"])); fitur = list(X.columns)
itr, ite = train_test_split(np.arange(len(X)), test_size=0.30, stratify=y, random_state=SEED)
Xtr, Xte, ytr, yte = X.values[itr], X.values[ite], y[itr], y[ite]; kl = list(np.unique(y))
fin = kl.index([k for k, v in nama.items() if v == "NMAP_FIN_SCAN"][0])
def xgb(): return XGBClassifier(learning_rate=0.1, max_depth=6, n_estimators=100, tree_method="hist", n_jobs=2, random_state=SEED, verbosity=0)
F = np.nan_to_num(f_classif(Xtr, ytr)[0]); C = np.nan_to_num(chi2(MinMaxScaler().fit_transform(Xtr), ytr)[0])
R = np.abs(np.nan_to_num(np.corrcoef(Xtr, rowvar=False)))
def prune(skor, batas):
    """urut menurut skor; simpan fitur hanya bila |r| dengan semua fitur yang sudah disimpan <= batas"""
    simpan = []
    for i in np.argsort(-skor):
        if all(R[i, j] <= batas for j in simpan): simpan.append(int(i))
    return simpan
rank = {"anova": list(np.argsort(-F)), "chi2": list(np.argsort(-C)), "anova_pangkas95":
      prune(F, 0.95), "anova_pangkas80": prune(F, 0.80)}
rows = []; fs = {}
for m, r in rank.items():
    fs[m] = [fitur[i] for i in r[:40]]
    for k in (5, 10, 20, 40):
        if len(r) < k: continue
        ci = list(r[:k]); p = xgb().fit(Xtr[:, ci], ytr).predict(Xte[:, ci]); rc = recall_score(yte, p, labels=kl, average=None, zero_division=0)
        rows.append(dict(seed=SEED, metode=m, k=k, tersedia=len(r), f1_macro=f1_score(yte, p, average="macro"), gmean=float(np.exp(np.mean(np.log(np.maximum(rc, 1e-3))))), recall_FIN=float(rc[fin])))
json.dump(fs, open(f"{OUT}/b4x_fitur_seed{SEED}.json", "w"))
pd.DataFrame(rows).to_csv(f"{OUT}/b4x_seed{SEED}.csv", index=False); print("b4x seed", SEED, "ok", flush=True)
