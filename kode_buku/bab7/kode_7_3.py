"""Kode 7.3  Menemukan titik Pareto dari hasil seluruh seed
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
hasil = pd.read_csv("hasil_b7.csv")                       # satu baris per seed, strategi, dan anggaran
rata = hasil[hasil.strategi != "semua"].groupby(["skor", "strategi", "B"], as_index=False)[["biaya", "f1_macro"]].mean()
rata = rata.sort_values("biaya").reset_index(drop=True)
 
depan, terbaik = [], -1                                   # titik Pareto: tak ada titik lain lebih murah dan lebih baik
for _, r in rata.iterrows():
    if r.f1_macro > terbaik + 1e-9: depan.append(r); terbaik = r.f1_macro
for r in depan:
    print(f"biaya {r.biaya:5.0f}  F1 makro {r.f1_macro:.3f}  ({r.skor}, {r.strategi}, B={r.B})")
