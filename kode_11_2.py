"""Kode 11.2  Mengukur ukuran model terserialisasi dan memori puncak proses
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
ukuran = len(pickle.dumps(m)) / 1e6                      # ukuran model terserialisasi (MB)
puncak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024   # memori puncak proses (MB)
print(f"ukuran model: {ukuran:.3f} MB | memori puncak proses: {puncak:.0f} MB")
