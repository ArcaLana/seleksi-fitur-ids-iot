"""Kode 9.4  Mengevaluasi tiap subset fitur dan mengukur waktu latih
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import time
from sklearn.metrics import f1_score
 
def nilai(cols):
    ci = [fitur.index(c) for c in cols]
    t = time.time(); m = xgb().fit(Xtr[:, ci], ytr); t_latih = time.time() - t
    return dict(f1_macro=f1_score(yte, m.predict(Xte[:, ci]), average="macro"), t_latih=t_latih)
 
hasil = []
hasil.append(dict(metode="semua", k=80, **nilai(fitur)))
for metode, r in rank.items():
    for k in (5, 10, 20, 40):
        hasil.append(dict(metode=metode, k=k, **nilai([fitur[i] for i in r[:k]])))
rng = np.random.default_rng(1000 + SEED)                       # kontrol: fitur acak
for k in (5, 10, 20, 40):
    for u in range(3):
        cols = [fitur[i] for i in rng.choice(len(fitur), k, replace=False)]
        hasil.append(dict(metode="acak", k=k, **nilai(cols)))
