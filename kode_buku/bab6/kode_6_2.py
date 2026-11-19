"""Kode 6.2  Seleksi global dibanding seleksi satu-lawan-semua dengan pemilihan bergiliran
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
def seleksi_global(K):
    F, _ = f_classif(Xtr, ytr)                           # satu skor per fitur untuk semua kelas
    return list(np.argsort(-np.nan_to_num(F))[:K])
 
def seleksi_ovr(K):
    """Setiap kelas menilai fitur sebagai kelas-lawan-sisanya, lalu bergiliran
    menyumbang fitur teratasnya (kelas terkecil lebih dulu) sampai terkumpul K fitur."""
    ranks = {c: np.argsort(-np.nan_to_num(f_classif(Xtr, (ytr == c).astype(int))[0])) for c in kelas}
    pilih, pos = [], {c: 0 for c in kelas}
    while len(pilih) < K:
        for c in urut:
            while pos[c] < len(fitur) and ranks[c][pos[c]] in pilih: pos[c] += 1
            if len(pilih) < K and pos[c] < len(fitur): pilih.append(ranks[c][pos[c]])
    return pilih
 
for nm, f in (("global", seleksi_global), ("satu-lawan-semua", seleksi_ovr)):
    print(f"{nm:17s}", [fitur[i] for i in f(5)])
