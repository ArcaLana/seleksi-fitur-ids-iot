"""Gambar tambahan dari hasil run. python3 -I buat_gambar.py <folder_hasil> <folder_output_data> <hasil_nyata>"""
import sys, glob, os, pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H, D, R = sys.argv[1:4]
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})
def save(f, p): f.tight_layout(); f.savefig(p, dpi=160); plt.close(f); print(p)
# Bab 2: distribusi kelas
y = pd.concat([pd.read_csv(D+"/y_train.csv"), pd.read_csv(D+"/y_test.csv")])["y"]
nm = pd.read_csv(D+"/pemetaan_label.csv").set_index("kode")["label"]; c = y.map(nm).value_counts().sort_values()
f, a = plt.subplots(figsize=(7.5, 4.2)); a.barh(c.index, c.values, color="#3b6ea5"); a.set_xscale("log"); a.set_xlabel("Jumlah baris (skala log)")
for i, v in enumerate(c.values): a.text(v*1.08, i, f"{v:,}".replace(",", "."), va="center", fontsize=8)
a.set_title("Distribusi 12 kelas RT-IoT2022 setelah duplikat dibuang"); save(f, R+"/bab2/g_distribusi_kelas.png")
# Bab 4
d = pd.concat([pd.read_csv(x) for x in glob.glob(H+"/b4x_seed*.csv")]); nama = {"anova": "ANOVA F", "chi2": "Chi-kuadrat", "anova_pangkas95": "ANOVA + pangkas 0,95", "anova_pangkas80": "ANOVA + pangkas 0,80"}
f, ax = plt.subplots(1, 2, figsize=(9, 3.8))
for m, n in nama.items():
    g = d[d.metode == m].groupby("k"); ax[0].errorbar(g.f1_macro.mean().index, g.f1_macro.mean(), g.f1_macro.std(), marker="o", capsize=3, label=n)
    ax[1].plot(g.recall_FIN.mean().index, g.recall_FIN.mean(), marker="o", label=n)
ax[0].set_xlabel("Jumlah fitur k"); ax[0].set_ylabel("F1 makro (20 seed)"); ax[1].set_xlabel("Jumlah fitur k"); ax[1].set_ylabel("Recall NMAP_FIN_SCAN"); ax[0].legend(fontsize=8)
save(f, R+"/bab4/g_filter_f1_recall_vs_k.png")
# Bab 5
e = pd.concat([pd.read_csv(x) for x in glob.glob(H+"/b5x_seed*.csv")]); f, ax = plt.subplots(1, 3, figsize=(11, 3.6))
for kel, a, jd in (("L1", ax[0], "L1: waktu (detik) menurut C"), ("RFE", ax[1], "RFE: waktu (detik) menurut step"), ("permutation", ax[2], "Permutation: waktu (detik) menurut ulangan")):
    g = e[e.kelompok == kel].groupby("pengaturan", sort=False).waktu; a.bar(g.mean().index, g.mean(), yerr=g.std(), capsize=3, color="#5b8f6b"); a.set_title(jd, fontsize=9)
save(f, R+"/bab5/g_sensitivitas_waktu.png")
f, a = plt.subplots(figsize=(6.5, 3.8)); g = e[e.kelompok == "importance_XGB"].groupby("pengaturan", sort=False)
a.bar(np.arange(len(g))-.2, g.f1_k20.mean(), .4, yerr=g.f1_k20.std(), capsize=3, label="k = 20"); a.bar(np.arange(len(g))+.2, g.f1_k10.mean(), .4, yerr=g.f1_k10.std(), capsize=3, label="k = 10")
a.set_xticks(range(len(g))); a.set_xticklabels(g.f1_k20.mean().index); a.set_ylim(.7, 1); a.set_ylabel("F1 makro (10 seed)"); a.legend(); a.set_title("Lima jenis importance XGBoost")
save(f, R+"/bab5/g_jenis_importance_xgboost.png")
# Bab 9: recall langka
r = pd.read_csv(H+"/recall_kelas_langka.csv"); f, ax = plt.subplots(1, 2, figsize=(9, 3.8)); ks = [5, 10, 20, 40]
for i, kl in enumerate(("FIN", "Meta")):
    for _, row in r.iterrows(): ax[i].plot(ks, [row[f"{kl} {k}"] for k in ks], marker="o", label=row["Metode"])
    ax[i].set_title("NMAP_FIN_SCAN" if kl == "FIN" else "Metasploit_Brute_Force_SSH"); ax[i].set_xlabel("Jumlah fitur k"); ax[i].set_ylabel("Recall rata-rata 20 seed")
ax[1].legend(fontsize=7); save(f, R+"/bab9/g_recall_kelas_langka.png")
