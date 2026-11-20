"""Kode 1.1  Gejala kutukan dimensi dan banyaknya subset fitur yang mungkin dari 80 fitur
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import numpy as np
from math import comb
 
rng = np.random.default_rng(0)
n = 500                                                  # banyaknya titik acak per percobaan
print(" d   (jarak terjauh - terdekat) / terdekat")
for d in (2, 10, 80, 1000):
    X = rng.random((n, d))
    q = rng.random(d)
    j = np.sqrt(((X - q) ** 2).sum(axis=1))
    print(f"{d:>4}   {(j.max() - j.min()) / j.min():.2f}")
 
print()
print("kemungkinan subset dari 80 fitur")
print(f"semua subset      : 2^80 = {2.0**80:.2e}")
for k in (5, 10, 20, 40):
    print(f"tepat {k:>2} fitur    : {comb(80, k):.2e}")
