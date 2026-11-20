"""Kode 10.2  Menyembunyikan satu jenis serangan dan menyiapkan data latih tanpa serangan itu (seed 42)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
 
D = "output/"                                            # keluaran Bab 8 Jilid 1
X = pd.concat([pd.read_csv(D + "X_train.csv"), pd.read_csv(D + "X_test.csv")], ignore_index=True)
X = X.drop(columns=["proto", "service"]); fitur = list(X.columns)
y = np.concatenate([pd.read_csv(D + "y_train.csv")["y"].values, pd.read_csv(D + "y_test.csv")["y"].values])
peta = pd.read_csv(D + "pemetaan_label.csv"); kode = dict(zip(peta["label"], peta["kode"]))
 
normal = [kode[n] for n in ("MQTT_Publish", "Thing_Speak", "Wipro_bulb")]
ybin = (~np.isin(y, normal)).astype(int)                 # 1 = serangan, 0 = lalu lintas normal
 
baru = "NMAP_UDP_SCAN"                                   # jenis serangan yang disembunyikan
m_baru = y == kode[baru]
idx = np.where(~m_baru)[0]                               # semua baris selain serangan baru
itr, ite = train_test_split(idx, test_size=0.30, stratify=y[idx], random_state=42)
print(f"latih {len(itr)} baris | uji dikenal {len(ite)} baris | serangan baru {int(m_baru.sum())} baris (tidak dipakai di mana pun)")
