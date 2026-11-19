"""Jilid 2: satu seed untuk pengulangan seleksi fitur pada RT-IoT2022.
Pemakaian: python3 -I run_seed.py <seed> <folder_keluaran>
Data bersih (117.922 baris, 80 fitur numerik) diambil dari keluaran jilid 1 (gabungan latih dan uji), lalu
dibagi ulang 70:30 secara stratifikasi dengan seed yang diberikan. Seleksi fitur hanya melihat data latih."""
import sys, os, time, json, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from sklearn.feature_selection import f_classif, mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
from sklearn.metrics import f1_score, accuracy_score, recall_score
from xgboost import XGBClassifier
 
SEED = int(sys.argv[1]); OUT = sys.argv[2]
D = "output/"
X = pd.concat([pd.read_csv(D + "X_train.csv"), pd.read_csv(D + "X_test.csv")], ignore_index=True).drop(columns=["proto", "service"])
y = np.concatenate([pd.read_csv(D + "y_train.csv")["y"].values, pd.read_csv(D + "y_test.csv")["y"].values])
peta = pd.read_csv(D + "pemetaan_label.csv"); nama = dict(zip(peta["kode"], peta["label"]))
fitur = list(X.columns)
idx_tr, idx_te = train_test_split(np.arange(len(X)), test_size=0.30, stratify=y, random_state=SEED)
Xtr, Xte, ytr, yte = X.values[idx_tr], X.values[idx_te], y[idx_tr], y[idx_te]
rare = {nama[k]: k for k in nama if nama[k] in ("NMAP_FIN_SCAN", "Metasploit_Brute_Force_SSH")}
 
def xgb(): return XGBClassifier(learning_rate=0.1, max_depth=6, n_estimators=100, tree_method="hist", n_jobs=2, random_state=SEED, verbosity=0)
def rfm(): return RandomForestClassifier(n_estimators=100, n_jobs=2, random_state=SEED)
 
def nilai(make, cols, ukur=False):
    ci = [fitur.index(c) for c in cols]
    t = time.time(); m = make(); m.fit(Xtr[:, ci], ytr); tf = time.time() - t
    t = time.time(); p = m.predict(Xte[:, ci]); tp = time.time() - t
    r = dict(f1_macro=f1_score(yte, p, average="macro"), f1_weighted=f1_score(yte, p, average="weighted"),
             akurasi=accuracy_score(yte, p), t_latih=tf, t_pred_batch=tp)
    for nm, k in rare.items():
        r["recall_" + nm] = recall_score(yte, p, labels=[k], average=None)[0]
    if ukur:
        satu = Xte[:1, ci]; m.predict(satu)
        t = time.time()
        for _ in range(100): m.predict(satu)
        r["t_pred_1baris_ms"] = (time.time() - t) / 100 * 1000
        r["ukuran_pickle_MB"] = len(pickle.dumps(m)) / 1e6
    return r
 
t0 = time.time(); rank = {}
F, _ = f_classif(Xtr, ytr); rank["anova"] = np.argsort(-np.nan_to_num(F))
sub, _ = train_test_split(np.arange(len(Xtr)), train_size=40000, stratify=ytr, random_state=SEED)
rank["mi"] = np.argsort(-mutual_info_classif(Xtr[sub], ytr[sub], random_state=SEED))
rank["rf_imp"] = np.argsort(-rfm().fit(Xtr, ytr).feature_importances_)
rank["xgb_imp"] = np.argsort(-xgb().fit(Xtr, ytr).feature_importances_)
i1, i2 = train_test_split(np.arange(len(Xtr)), test_size=0.2, stratify=ytr, random_state=SEED)
mv = xgb().fit(Xtr[i1], ytr[i1])
pi = permutation_importance(mv, Xtr[i2[:8000]], ytr[i2[:8000]], n_repeats=3, random_state=SEED, scoring="f1_macro", n_jobs=1)
rank["perm"] = np.argsort(-pi.importances_mean)
sc = StandardScaler().fit(Xtr[sub]); lr = LogisticRegression(penalty="l1", solver="saga", C=0.05, max_iter=150, tol=1e-3)
lr.fit(sc.transform(Xtr[sub]), ytr[sub]); rank["l1"] = np.argsort(-np.abs(lr.coef_).max(axis=0))
s30, _ = train_test_split(np.arange(len(Xtr)), train_size=30000, stratify=ytr, random_state=SEED)
rfe = RFE(XGBClassifier(learning_rate=0.1, max_depth=4, n_estimators=40, tree_method="hist", n_jobs=2, random_state=SEED, verbosity=0), n_features_to_select=5, step=5)
rfe.fit(Xtr[s30], ytr[s30]); rank["rfe_xgb"] = np.argsort(rfe.ranking_)
t_sel = time.time() - t0
json.dump({m: [fitur[i] for i in r[:40]] for m, r in rank.items()}, open(f"{OUT}/fitur_seed{SEED}.json", "w"))
 
K = [5, 10, 20, 40]; rows = []
rows.append(dict(seed=SEED, model="XGB", metode="semua", k=len(fitur), ulang=0, **nilai(xgb, fitur, True)))
rows.append(dict(seed=SEED, model="RF", metode="semua", k=len(fitur), ulang=0, **nilai(rfm, fitur, True)))
for metode, r in rank.items():
    for k in K:
        cols = [fitur[i] for i in r[:k]]
        rows.append(dict(seed=SEED, model="XGB", metode=metode, k=k, ulang=0, **nilai(xgb, cols, True)))
        if k in (10, 20): rows.append(dict(seed=SEED, model="RF", metode=metode, k=k, ulang=0, **nilai(rfm, cols)))
rng = np.random.default_rng(1000 + SEED)
for k in K:
    for u in range(3):
        cols = [fitur[i] for i in rng.choice(len(fitur), k, replace=False)]
        rows.append(dict(seed=SEED, model="XGB", metode="acak", k=k, ulang=u, **nilai(xgb, cols)))
d = pd.DataFrame(rows); d["t_seleksi_total"] = t_sel
d.to_csv(f"{OUT}/hasil_seed{SEED}.csv", index=False)
print("seed", SEED, "selesai", round(time.time() - t0), "s; seleksi", round(t_sel), "s", flush=True)
