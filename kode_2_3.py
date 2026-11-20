"""Kode 2.3  Biaya total per kelompok fitur dan batas biaya himpunan fitur
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import pandas as pd
 
D = "output/"
fitur = [c for c in pd.read_csv(D + "X_train.csv", nrows=2).columns if c not in ("proto", "service")]
 
def kelompok(f):                                          # sama dengan Kode 2.1
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
 
def biaya(f):                                             # asumsi penulis (Tabel 2.4)
    n = f.lower(); std = n.endswith(".std")
    if n.startswith(("active.", "idle.")): return 5 if std else 4
    if "bulk" in n: return 4
    if "_iat." in n: return 4 if std else 3
    if "payload." in n: return 3 if std else 2
    if "per_sec" in n or n == "down_up_ratio" or "subflow" in n or "per_second" in n: return 2
    return 1
 
d = pd.DataFrame({"fitur": fitur})
d["kelompok"] = d.fitur.map(kelompok); d["biaya"] = d.fitur.map(biaya)
r = d.groupby("kelompok").biaya.agg(["count", "sum"]).sort_values("sum", ascending=False)
r["persen"] = (100 * r["sum"] / d.biaya.sum()).round(1)
print(r.to_string()); print("total:", d.biaya.sum(), "| rata-rata per fitur: %.3f" % d.biaya.mean())
b = d.biaya.sort_values()
print("20 fitur termurah:", b.head(20).sum(), "| 20 fitur termahal:", b.tail(20).sum())
print("fitur berbiaya >= 3:", (d.biaya >= 3).sum(), "fitur,", d.biaya[d.biaya >= 3].sum(), "satuan")
