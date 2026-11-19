"""Kode 4.1  Memeriksa fitur konstan dan pasangan fitur berkorelasi tinggi pada data latih (seed 42)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
 
D = "output/"
X = pd.concat([pd.read_csv(D + "X_train.csv"), pd.read_csv(D + "X_test.csv")], ignore_index=True).drop(columns=["proto", "service"])
y = np.concatenate([pd.read_csv(D + "y_train.csv")["y"].values, pd.read_csv(D + "y_test.csv")["y"].values])
fitur = list(X.columns)
itr, ite = train_test_split(np.arange(len(X)), test_size=0.30, stratify=y, random_state=42)
Xtr, Xte, ytr, yte = X.values[itr], X.values[ite], y[itr], y[ite]
 
nunik = pd.Series([len(np.unique(Xtr[:, j])) for j in range(Xtr.shape[1])], index=fitur)
print("fitur konstan di data latih :", int((nunik == 1).sum()), "| fitur dengan <= 3 nilai berbeda:", int((nunik <= 3).sum()))
 
korr = pd.DataFrame(Xtr, columns=fitur).corr().abs()
atas = korr.where(np.triu(np.ones(korr.shape), k=1).astype(bool))
for batas in (0.90, 0.95, 0.99):
    buang = [c for c in atas.columns if (atas[c] > batas).any()]        # buang satu dari tiap pasangan yang berkorelasi
    print(f"|r| > {batas:.2f}: {int((atas > batas).sum().sum()):4d} pasangan, {len(buang):2d} fitur dapat dibuang")
