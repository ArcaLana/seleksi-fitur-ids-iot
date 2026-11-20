"""Kode 9.6  Uji Friedman dan uji Wilcoxon
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
from scipy.stats import wilcoxon, friedmanchisquare
 
hasil = pd.read_csv("hasil_semua_seed.csv")        # satu baris per seed, metode, dan k
f1 = hasil.pivot_table(index="seed", columns=["metode", "k"], values="f1_macro")
metode = ["anova", "mi", "rf_imp", "xgb_imp", "perm", "l1", "rfe_xgb"]
st, p = friedmanchisquare(*[f1[(m, 20)] for m in metode])
print(f"Friedman k=20: statistik = {st:.1f}, p = {p:.1e}")
for m in ("anova", "perm"):
    sel = f1[(m, 20)] - f1[("semua", 80)]
    print(f"{m} vs model penuh: selisih = {sel.mean():+.4f}, menang {int((sel>0).sum())}/20, p = {wilcoxon(sel).pvalue:.4f}")
