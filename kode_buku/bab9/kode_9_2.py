"""Kode 9.2  Peringkat fitur dengan metode filter (ANOVA F dan mutual information)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
from sklearn.feature_selection import f_classif, mutual_info_classif
 
rank = {}
F, _ = f_classif(Xtr, ytr)                                   # ANOVA F
rank["anova"] = np.argsort(-np.nan_to_num(F))
sub, _ = train_test_split(np.arange(len(Xtr)), train_size=40000,
                          stratify=ytr, random_state=SEED)    # subsampel agar cepat
rank["mi"] = np.argsort(-mutual_info_classif(Xtr[sub], ytr[sub], random_state=SEED))
for m in ("anova", "mi"):
    print(m, [fitur[i] for i in rank[m][:5]])
