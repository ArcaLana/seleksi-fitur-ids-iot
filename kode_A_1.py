"""Kode A.1  Memeriksa versi pustaka
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import sys, sklearn, xgboost, pandas, numpy, scipy
print("python", sys.version.split()[0])
for m in (sklearn, xgboost, pandas, numpy, scipy):
    print(m.__name__, m.__version__)
