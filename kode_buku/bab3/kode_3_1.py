"""Kode 3.1  Kebocoran akibat seleksi sebelum pembagian data (data sintetis, label acak)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
 
salah, benar = [], []
for ulang in range(20):                                  # 20 dataset sintetis dengan label acak murni
    rng = np.random.default_rng(ulang)
    X = rng.normal(size=(100, 2000)); y = rng.integers(0, 2, 100)      # tidak ada hubungan fitur dan label
    cv = StratifiedKFold(5, shuffle=True, random_state=ulang)
    Xs = SelectKBest(f_classif, k=20).fit_transform(X, y)              # SALAH: seleksi melihat seluruh data
    salah.append(cross_val_score(LogisticRegression(max_iter=1000), Xs, y, cv=cv).mean())
    pipa = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=1000))   # BENAR: seleksi di dalam lipatan
    benar.append(cross_val_score(pipa, X, y, cv=cv).mean())
print(f"seleksi sebelum pembagian : akurasi {np.mean(salah):.3f}")
print(f"seleksi di dalam lipatan  : akurasi {np.mean(benar):.3f}   (nilai sebenarnya 0,5)")
