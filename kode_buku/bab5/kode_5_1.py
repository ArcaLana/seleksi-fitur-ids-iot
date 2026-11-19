"""Kode 5.1  Forward selection lima fitur dengan pohon keputusan pada subsampel 5.000 baris (seed 42)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.tree import DecisionTreeClassifier
 
s5, _ = train_test_split(np.arange(len(Xtr)), train_size=5000, stratify=ytr, random_state=42)
sfs = SequentialFeatureSelector(DecisionTreeClassifier(max_depth=6, random_state=42), n_features_to_select=5,
                                direction="forward", scoring="f1_macro", cv=3, n_jobs=1)
t = time.perf_counter(); sfs.fit(Xtr[s5], ytr[s5]); dtk = time.perf_counter() - t
banyak = sum(Xtr.shape[1] - i for i in range(5)) * 3             # kandidat tiap langkah dikali lipatan
print("fitur terpilih :", [fitur[i] for i in np.where(sfs.get_support())[0]])
print(f"{banyak} pelatihan model, {dtk:.0f} dtk (5.000 baris, pohon keputusan)")
