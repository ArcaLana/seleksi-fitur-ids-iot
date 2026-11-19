"""Kode 7.2  Memilih fitur dengan anggaran biaya, dengan dan tanpa memperhitungkan biaya (seed 42, anggaran 20)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
from sklearn.feature_selection import f_classif
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
 
X = pd.concat([pd.read_csv(D + "X_train.csv"), pd.read_csv(D + "X_test.csv")], ignore_index=True).drop(columns=["proto", "service"])
y = np.concatenate([pd.read_csv(D + "y_train.csv")["y"].values, pd.read_csv(D + "y_test.csv")["y"].values])
itr, ite = train_test_split(np.arange(len(X)), test_size=0.30, stratify=y, random_state=42)
Xtr, Xte, ytr, yte = X.values[itr], X.values[ite], y[itr], y[ite]
mdl = XGBClassifier(learning_rate=0.1, max_depth=6, n_estimators=100, tree_method="hist", n_jobs=2, random_state=42, verbosity=0)
skor = mdl.fit(Xtr, ytr).feature_importances_; skor = skor / skor.sum()
 
def isi(urutan, B):                                       # ambil fitur sesuai urutan selama biaya masih muat
    pilih, total = [], 0
    for i in urutan:
        if total + cost[i] <= B: pilih.append(i); total += cost[i]
    return pilih
 
B = 20
buta = isi(np.argsort(-skor), B)                          # peringkat skor saja
rasio = isi(np.argsort(-(skor / cost)), B)                # skor dibagi biaya
for nm, p in (("tanpa biaya", buta), ("skor per biaya", rasio)):
    print(f"{nm:15s} {len(p):2d} fitur, biaya {cost[p].sum()}:", [fitur[i] for i in p[:4]], "...")
