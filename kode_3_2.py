"""Kode 3.2  Besarnya kebetulan pada 2.000 fitur acak dengan 100 baris (20 dataset sintetis)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import numpy as np
from sklearn.feature_selection import f_classif
 
maks, k20 = [], []
for ulang in range(20):                                  # label acak murni, 2.000 fitur acak, 100 baris
    rng = np.random.default_rng(ulang)
    X = rng.normal(size=(100, 2000)); y = rng.integers(0, 2, 100)
    r = np.abs([np.corrcoef(X[:, j], y)[0, 1] for j in range(2000)])
    maks.append(r.max())
    F, _ = f_classif(X, y)
    k20.append(np.sort(F)[-20:].mean())
print(f"|r| terbesar antara fitur acak dan label : rata-rata {np.mean(maks):.3f}")
print(f"rata-rata F dari 20 fitur teratas        : {np.mean(k20):.2f}   (F tipikal satu fitur acak: sekitar 1)")
