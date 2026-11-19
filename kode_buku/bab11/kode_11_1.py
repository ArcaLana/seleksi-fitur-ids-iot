"""Kode 11.1  Mengukur waktu latih, latensi satu baris, dan waktu batch (contoh dengan 20 fitur)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import time, pickle, resource
import numpy as np
from xgboost import XGBClassifier
 
k = 20                                                   # jumlah fitur yang diukur
Xtr = np.load(f"tr{k}.npy"); Xte = np.load(f"te{k}.npy"); ytr = np.load("ytr.npy")
m = XGBClassifier(learning_rate=0.1, max_depth=6, n_estimators=100,
                  tree_method="hist", n_jobs=1, random_state=42, verbosity=0)
t = time.perf_counter(); m.fit(Xtr, ytr); t_latih = time.perf_counter() - t
 
m.predict(Xte[:1])                                       # pemanasan, tidak dihitung
lat = []
for i in range(1000):                                    # satu baris per panggilan
    baris = Xte[i:i+1]
    t = time.perf_counter(); m.predict(baris); lat.append((time.perf_counter() - t) * 1000)
bt = []
for _ in range(5):                                       # seluruh data uji sekaligus
    t = time.perf_counter(); m.predict(Xte); bt.append(time.perf_counter() - t)
print(f"latih {t_latih:.2f} dtk | satu baris: median {np.median(lat):.3f} ms, "
      f"p95 {np.percentile(lat, 95):.3f} ms")
print(f"batch {len(Xte)} baris: {np.median(bt):.3f} dtk "
      f"({np.median(bt) / len(Xte) * 1e6:.2f} mikrodetik per baris)")
