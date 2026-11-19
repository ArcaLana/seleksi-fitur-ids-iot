"""Kode 2.1  Mengelompokkan 80 fitur RT-IoT2022 menurut jenis penghitungannya
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import pandas as pd
 
D = "output/"                                            # keluaran Bab 8 pada Jilid 1
fitur = [c for c in pd.read_csv(D + "X_train.csv", nrows=2).columns if c not in ("proto", "service")]
 
def kelompok(f):
    n = f.lower()
    if n.startswith("id."): return "port"
    if n.startswith(("active.", "idle.")): return "aktif dan diam"
    if "bulk" in n: return "rentetan paket (bulk)"
    if "_iat." in n: return "selang waktu antarpaket (IAT)"
    if "payload." in n: return "ukuran payload"
    if "flag_count" in n: return "flag TCP"
    if "header_size" in n: return "ukuran header"
    if "window" in n: return "jendela TCP"
    if "subflow" in n: return "subflow"
    if "per_sec" in n or "per_second" in n or n == "down_up_ratio": return "laju dan rasio"
    return "hitungan paket dan durasi"
 
peta = pd.Series([kelompok(f) for f in fitur]).value_counts()
print(f"{len(fitur)} fitur dalam {len(peta)} kelompok")
print(peta.to_string())
