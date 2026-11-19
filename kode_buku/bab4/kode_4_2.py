"""Kode 4.2  Mengukur waktu metode filter pada data latih (seed 42, mesin 2 inti)
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import time
from sklearn.feature_selection import f_classif, chi2, mutual_info_classif
from sklearn.preprocessing import MinMaxScaler
 
def ukur(nama, f):
    t = time.perf_counter(); f(); print(f"{nama:34s} {time.perf_counter() - t:6.2f} dtk")
 
ukur("ANOVA F (seluruh data latih)", lambda: f_classif(Xtr, ytr))
ukur("chi-kuadrat (seluruh data latih)", lambda: chi2(MinMaxScaler().fit_transform(Xtr), ytr))
sub, _ = train_test_split(np.arange(len(Xtr)), train_size=10000, stratify=ytr, random_state=42)
ukur("mutual information (10.000 baris)", lambda: mutual_info_classif(Xtr[sub], ytr[sub], random_state=42))
