"""Kode 5.2  Mengukur waktu lima metode berbasis model pada data latih (seed 42, mesin 2 inti)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance
from sklearn.feature_selection import RFE
from xgboost import XGBClassifier
 
def xgb(n=100, d=6): return XGBClassifier(learning_rate=0.1, max_depth=d, n_estimators=n, tree_method="hist", n_jobs=2, random_state=42, verbosity=0)
def ukur(nama, f):
    t = time.perf_counter(); f(); print(f"{nama:38s} {time.perf_counter() - t:6.1f} dtk")
 
s40, _ = train_test_split(np.arange(len(Xtr)), train_size=40000, stratify=ytr, random_state=42)
s30, _ = train_test_split(np.arange(len(Xtr)), train_size=30000, stratify=ytr, random_state=42)
i1, i2 = train_test_split(np.arange(len(Xtr)), test_size=0.2, stratify=ytr, random_state=42)
ukur("importance Random Forest", lambda: RandomForestClassifier(n_estimators=100, n_jobs=2, random_state=42).fit(Xtr, ytr))
ukur("importance XGBoost", lambda: xgb().fit(Xtr, ytr))
ukur("permutation importance (3 pengulangan)", lambda: permutation_importance(xgb().fit(Xtr[i1], ytr[i1]), Xtr[i2[:8000]], ytr[i2[:8000]], n_repeats=3, random_state=42, scoring="f1_macro"))
ukur("regresi logistik L1 (40.000 baris)", lambda: LogisticRegression(penalty="l1", solver="saga", C=0.05, max_iter=150, tol=1e-3).fit(StandardScaler().fit_transform(Xtr[s40]), ytr[s40]))
ukur("RFE dengan XGBoost (30.000 baris)", lambda: RFE(xgb(40, 4), n_features_to_select=5, step=5).fit(Xtr[s30], ytr[s30]))
