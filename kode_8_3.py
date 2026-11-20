"""Kode 8.3  Melaporkan F1 makro sebagai rata-rata, simpangan baku, dan rentang antarseed
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
hasil = pd.read_csv(E + "hasil_semua_seed.csv")           # satu baris per seed, metode, dan k
for m in ("anova", "perm"):
    v = hasil[(hasil.metode == m) & (hasil.k == 20)].f1_macro
    print(f"{m:6s} k=20 ({len(v)} seed): rata-rata {v.mean():.4f} | simpangan baku {v.std():.4f} | "
          f"rentang {v.min():.4f} sampai {v.max():.4f}")
