"""Kode 10.1  Ablasi fitur port: membandingkan F1 makro dengan dan tanpa kedua fitur port (20 seed)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import glob
hasil = pd.concat([pd.read_csv(f) for f in glob.glob("b10_e2_seed*.csv")])   # 20 seed, 12 kelas
rata = hasil.groupby(["varian", "metode", "k"]).f1_macro.mean().unstack(0)
rata["selisih"] = rata["tanpa_port"] - rata["dengan_port"]
print(rata.round(4).to_string())
