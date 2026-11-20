"""Kode 8.1  Menghitung indeks Jaccard dan Kuncheva rata-rata atas semua pasangan seed
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import json, itertools
import numpy as np, pandas as pd
 
N = 80                                                   # jumlah seluruh fitur
def jaccard(a, b): return len(a & b) / len(a | b)
def kuncheva(a, b, k):                                   # dikoreksi terhadap kecocokan kebetulan
    r = len(a & b)
    return (r * N - k * k) / (k * (N - k))
 
E = "hasil/"                                             # fitur_seed42.json ... fitur_seed61.json
fs = {s: json.load(open(f"{E}fitur_seed{s}.json")) for s in range(42, 62)}
k = 20
for m in ("anova", "perm"):
    himp = [set(fs[s][m][:k]) for s in fs]
    pas = list(itertools.combinations(himp, 2))
    print(f"{m:6s} k={k}: Jaccard {np.mean([jaccard(a, b) for a, b in pas]):.3f} | "
          f"Kuncheva {np.mean([kuncheva(a, b, k) for a, b in pas]):.3f}  ({len(pas)} pasangan)")
print(f"dua himpunan acak: harapan irisan = k*k/N = {k*k/N:.1f} fitur, Jaccard sekitar {(k*k/N)/(2*k-k*k/N):.2f}")
