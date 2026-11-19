"""Kode 12.3  Menerapkan kriteria K1 sampai K5 pada hasil
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
t = pd.read_csv("tabel_b12.csv", index_col=0)                    # gabungan 20 seed dan 5 seed serangan baru
baru_penuh = t.loc["C0_semua", "rec_baru"]
lulus = pd.DataFrame({
    "K1 biaya": t.biaya_maks <= 40,                              # anggaran adalah batas keras, dinilai pada seed terburuk
    "K2 F1": t.f1 >= 0.955,
    "K3 FIN": t.fin >= 0.80,
    "K4 stabil": t.kuncheva >= 0.80,
    "K5 baru": t.rec_baru >= baru_penuh - 0.05}).astype(object)
lulus.loc[t.rec_baru.isna(), "K5 baru"] = "tidak diuji"; lulus.loc["C0_semua", "K4 stabil"] = "-"
print(lulus.to_string())
