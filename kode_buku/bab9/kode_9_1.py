"""Kode 9.1  Memuat data bersih dan membagi ulang data dengan satu seed
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
 
D = "output/"                      # keluaran Bab 8 pada Jilid 1
X = pd.concat([pd.read_csv(D + "X_train.csv"), pd.read_csv(D + "X_test.csv")], ignore_index=True)
X = X.drop(columns=["proto", "service"])          # tersisa 80 fitur numerik
y = np.concatenate([pd.read_csv(D + "y_train.csv")["y"].values,
                    pd.read_csv(D + "y_test.csv")["y"].values])
fitur = list(X.columns)
 
SEED = 42
idx_tr, idx_te = train_test_split(np.arange(len(X)), test_size=0.30,
                                  stratify=y, random_state=SEED)
Xtr, Xte, ytr, yte = X.values[idx_tr], X.values[idx_te], y[idx_tr], y[idx_te]
print("baris:", len(X), "| fitur:", len(fitur), "| kelas:", len(np.unique(y)))
print("latih:", Xtr.shape, "| uji:", Xte.shape)
