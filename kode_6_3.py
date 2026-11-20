"""Kode 6.3  Menilai subset fitur dengan F1 makro, G-mean, dan recall NMAP_FIN_SCAN
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
from xgboost import XGBClassifier
from sklearn.metrics import f1_score, recall_score
 
def xgb(): return XGBClassifier(learning_rate=0.1, max_depth=6, n_estimators=100,
                                tree_method="hist", n_jobs=2, random_state=42, verbosity=0)
 
def nilai(idx_fitur):
    m = xgb().fit(Xtr[:, idx_fitur], ytr); p = m.predict(Xte[:, idx_fitur])
    rc = recall_score(yte, p, labels=list(kelas), average=None, zero_division=0)
    gmean = np.exp(np.mean(np.log(np.maximum(rc, 1e-3))))   # recall 0 diganti 0,001 agar log terdefinisi
    fin = rc[list(kelas).index([k for k, v in nama.items() if v == "NMAP_FIN_SCAN"][0])]
    return f"F1 makro {f1_score(yte, p, average='macro'):.3f} | G-mean {gmean:.3f} | recall FIN {fin:.2f}"
 
for nm, f in (("global", seleksi_global), ("satu-lawan-semua", seleksi_ovr)):
    for K in (5, 10):
        print(f"{nm:17s} k={K:2d}  {nilai(f(K))}")
