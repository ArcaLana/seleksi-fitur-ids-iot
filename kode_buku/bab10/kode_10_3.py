"""Kode 10.3  Seleksi dan pelatihan tanpa serangan baru, lalu uji deteksinya
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
from sklearn.feature_selection import f_classif
 
def xgb(): return XGBClassifier(learning_rate=0.1, max_depth=6, n_estimators=100,
                                tree_method="hist", n_jobs=2, random_state=42, verbosity=0)
 
Xtr, ytr = X.values[itr], ybin[itr]
anova = [fitur[i] for i in np.argsort(-np.nan_to_num(f_classif(Xtr, ytr)[0]))]   # seleksi tanpa serangan baru
 
def uji(cols):
    ci = [fitur.index(c) for c in cols]; m = xgb().fit(Xtr[:, ci], ytr)
    pt = m.predict(X.values[ite][:, ci]); yt = ybin[ite]
    ph = m.predict(X.values[m_baru][:, ci])
    return (f"terdeteksi serangan baru {ph.mean():.2f} | serangan dikenal {pt[yt == 1].mean():.3f} "
            f"| alarm palsu {pt[yt == 0].mean():.3f}")
 
print("80 fitur      :", uji(fitur))
print("ANOVA 20 fitur:", uji(anova[:20]))
