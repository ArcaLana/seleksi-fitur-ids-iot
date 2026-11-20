"""Kode 7.1  Model biaya ilustratif per fitur (asumsi penulis)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import sys; sys.path.insert(0, ".")
import numpy as np, pandas as pd
 
def biaya(f):
    """Biaya relatif ILUSTRATIF: asumsi penulis, bukan hasil pengukuran. Ganti dengan biaya terukur Anda."""
    n = f.lower(); std = n.endswith(".std")
    if n.startswith(("active.", "idle.")): return 5 if std else 4     # perlu ambang waktu diam
    if "bulk" in n: return 4                                         # perlu deteksi rentetan paket
    if "_iat." in n: return 4 if std else 3                          # selisih waktu antarpaket
    if "payload." in n and "bytes_per" not in n: return 3 if std else 2   # agregat ukuran payload
    if "per_sec" in n or n == "down_up_ratio" or "subflow" in n or "bytes_per_second" in n: return 2
    return 1                                                         # hitungan, flag, header, jendela TCP, durasi
 
D = "output/"                                            # keluaran Bab 8 Jilid 1
fitur = [c for c in pd.read_csv(D + "X_train.csv", nrows=2).columns if c not in ("proto", "service")]
cost = np.array([biaya(f) for f in fitur])
print("jumlah fitur:", len(fitur), "| biaya total:", cost.sum())
for b in sorted(set(cost)):
    print(f"biaya {b}: {int((cost == b).sum()):2d} fitur, contoh {[f for f in fitur if biaya(f) == b][:2]}")
