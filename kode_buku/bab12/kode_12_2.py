"""Kode 12.2  Merangkum hasil 20 seed untuk tiap kandidat
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
hasil = pd.concat([pd.read_csv(f) for f in glob.glob("b12_m_seed*.csv")])      # 20 seed, 12 kelas
ring = hasil.groupby("kandidat").agg(fitur=("n_fitur", "mean"), biaya=("biaya", "mean"), biaya_maks=("biaya", "max"),
                                     f1=("f1_macro", "mean"), recall_FIN=("recall_FIN", "mean"), latih_dtk=("t_latih", "mean"))
print(ring.round(3).to_string())
