"""Kode 8.2  Agregasi peringkat permutation importance atas bootstrap
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
from sklearn.inspection import permutation_importance
 
def peringkat_agregat(Xtr, ytr, M=5, seed=42):
    """Rata-rata peringkat permutation importance atas M resampel bootstrap data latih;
    validasi memakai baris di luar bootstrap (OOB), jadi tetap hanya data latih."""
    rng = np.random.default_rng(seed); skor = np.zeros(Xtr.shape[1])
    for b in range(M):
        bi = rng.choice(len(Xtr), len(Xtr), replace=True)
        oob = np.setdiff1d(np.arange(len(Xtr)), bi); ov = rng.choice(oob, 8000, replace=False)
        mv = xgb().fit(Xtr[bi], ytr[bi])
        pi = permutation_importance(mv, Xtr[ov], ytr[ov], n_repeats=3, random_state=seed + b, scoring="f1_macro")
        skor += pd.Series(pi.importances_mean).rank(ascending=False).values
    return list(np.argsort(skor))
 
# peringkat tunggal dan agregat pada seed 42 (hasil dari eksperimen penuh)
tunggal = json.load(open(E + "fitur_seed42.json"))["perm"]
agregat = json.load(open(E + "agr_fitur_seed42.json"))
print("tunggal :", tunggal[:5]); print("agregat :", agregat[:5])
