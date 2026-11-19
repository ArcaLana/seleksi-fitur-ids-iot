"""Menyusun folder output/ (setara keluaran Bab 8 Jilid 1) dari RT_IOT2022.csv.
Pakai: python3 -I siapkan_output.py data/RT_IOT2022.csv output
Langkah: buang kolom indeks, buang duplikat (123.117 -> 117.922 baris), buang kolom konstan,
kode label menurut urutan abjad, pembagian 70:30 berstrata (seed 42). Skrip eksperimen
menggabung ulang data latih dan uji lalu membagi per seed."""
import sys, os, pandas as pd
from sklearn.model_selection import train_test_split
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
df = pd.read_csv(src); lab = "Attack_type"
d = df.drop(columns=[df.columns[0]]).drop_duplicates().reset_index(drop=True)
d = d.drop(columns=[c for c in d.columns if d[c].nunique(dropna=False) <= 1])
kls = sorted(d[lab].unique()); y = d[lab].map({k: i for i, k in enumerate(kls)}).values; X = d.drop(columns=[lab])
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.30, stratify=y, random_state=42)
Xtr.to_csv(f"{out}/X_train.csv", index=False); Xte.to_csv(f"{out}/X_test.csv", index=False)
pd.DataFrame({"y": ytr}).to_csv(f"{out}/y_train.csv", index=False); pd.DataFrame({"y": yte}).to_csv(f"{out}/y_test.csv", index=False)
pd.DataFrame({"kode": range(len(kls)), "label": kls}).to_csv(f"{out}/pemetaan_label.csv", index=False)
print(Xtr.shape, Xte.shape, len(kls), "kelas")
