"""Kode 6.1  Menyiapkan data dan melihat kelas terkecil (seed 42)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import numpy as np, pandas as pd
from sklearn.feature_selection import f_classif
from sklearn.model_selection import train_test_split
 
D = "output/"                                            # keluaran Bab 8 Jilid 1
X = pd.concat([pd.read_csv(D + "X_train.csv"), pd.read_csv(D + "X_test.csv")], ignore_index=True)
X = X.drop(columns=["proto", "service"]); fitur = list(X.columns)
y = np.concatenate([pd.read_csv(D + "y_train.csv")["y"].values, pd.read_csv(D + "y_test.csv")["y"].values])
peta = pd.read_csv(D + "pemetaan_label.csv"); nama = dict(zip(peta["kode"], peta["label"]))
itr, ite = train_test_split(np.arange(len(X)), test_size=0.30, stratify=y, random_state=42)
Xtr, Xte, ytr, yte = X.values[itr], X.values[ite], y[itr], y[ite]
 
kelas = np.unique(ytr); jml = {c: int((ytr == c).sum()) for c in kelas}
urut = sorted(kelas, key=lambda c: jml[c])               # kelas terkecil lebih dulu
for c in urut[:3]:
    print(f"{nama[c]:28s} {jml[c]:6d} baris latih")
