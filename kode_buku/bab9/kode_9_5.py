"""Kode 9.5  Menghitung indeks Kuncheva antarseed
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import itertools, json
 
N = 80
def kuncheva(a, b, k):
    r = len(a & b)
    return (r * N - k * k) / (k * (N - k))
 
fs = {s: json.load(open(f"fitur_seed{s}.json")) for s in range(42, 62)}   # 20 seed
for m in ("anova", "mi", "xgb_imp", "perm"):
    for k in (10, 20):
        sets = [set(fs[s][m][:k]) for s in fs]
        v = [kuncheva(a, b, k) for a, b in itertools.combinations(sets, 2)]
        print(f"{m:8s} k={k:2d}  Kuncheva = {np.mean(v):.3f}")
