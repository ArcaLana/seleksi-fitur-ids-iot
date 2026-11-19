import sys, glob, json, itertools
import numpy as np, pandas as pd
from scipy.stats import wilcoxon, friedmanchisquare
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
S = sys.argv[1]
d = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(S + "/hasil_seed*.csv"))], ignore_index=True)
seeds = sorted(d.seed.unique()); print("seed:", seeds)
NM = {"anova": "ANOVA F", "mi": "Mutual information", "rf_imp": "Importance RF", "xgb_imp":
      "Importance XGBoost",
      "perm": "Permutation importance", "l1": "Regresi logistik L1", "rfe_xgb": "RFE (XGBoost)", "acak": "Acak (kontrol)"}
K = [5, 10, 20, 40]
x = d[d.model == "XGB"].copy()
# rata-rata pengulangan acak per seed
x = x.groupby(["seed", "metode", "k"], as_index=False).mean(numeric_only=True)
base = x[x.metode == "semua"].set_index("seed")["f1_macro"]
print("baseline F1 macro: %.4f ± %.4f" % (base.mean(), base.std()))
 
# Tabel 1: F1 macro rata-rata ± simpangan baku
rows = []
for m in NM:
    r = {"Metode": NM[m]}
    for k in K:
        v = x[(x.metode == m) & (x.k == k)].set_index("seed")["f1_macro"]
        r["%d fitur" % k] = "%.4f ± %.4f" % (v.mean(), v.std())
    rows.append(r)
pd.DataFrame(rows).to_csv(S + "/tabel_f1_macro.csv", index=False)
 
# Tabel 2: uji Wilcoxon terhadap model penuh dan terhadap acak
ws = []
for m in NM:
    if m == "acak": continue
    for k in K:
        v = x[(x.metode == m) & (x.k == k)].set_index("seed")["f1_macro"]
        a = x[(x.metode == "acak") & (x.k == k)].set_index("seed")["f1_macro"]
        for lawan, ref in (("penuh", base), ("acak", a)):
            sel = (v - ref.loc[v.index])
            try: p = wilcoxon(sel).pvalue
            except ValueError: p = 1.0
            ws.append(dict(metode=NM[m], k=k, lawan=lawan, selisih_rata=sel.mean(), menang=int((sel > 0).sum()), seri=int((sel == 0).sum()), p=p))
w = pd.DataFrame(ws); n_uji = len(w); w["p_bonferroni"] = np.minimum(1, w.p * n_uji)
o = np.argsort(w.p.values); h = np.empty(n_uji); run = 0
for r, i in enumerate(o):
    run = max(run, (n_uji - r) * w.p.values[i]); h[i] = min(1, run)
w["p_holm"] = h
w.to_csv(S + "/uji_wilcoxon.csv", index=False)
print("jumlah uji:", n_uji, "; p minimum yang mungkin (dua sisi, n=%d): %.7f" % (len(seeds), 2 / 2 ** len(seeds)))
 
# Friedman antar tujuh metode per k
fr = []
for k in K:
    mat = np.array([x[(x.metode == m) & (x.k == k)].set_index("seed")["f1_macro"].loc[seeds].values for m in NM if m != "acak"])
    st, p = friedmanchisquare(*mat); fr.append(dict(k=k, statistik=st, p=p))
pd.DataFrame(fr).to_csv(S + "/uji_friedman.csv", index=False); print(pd.DataFrame(fr).round(4))
 
# Kestabilan: Jaccard rata-rata dan indeks Kuncheva antar-seed
N = 80
fs = {s: json.load(open(f"{S}/fitur_seed{s}.json")) for s in seeds}
st = []
for m in NM:
    if m == "acak": continue
    for k in K:
        sets = [set(fs[s][m][:k]) for s in seeds]
        jac, kun = [], []
        for a, b in itertools.combinations(sets, 2):
            r = len(a & b); jac.append(r / len(a | b)); kun.append((r * N - k * k) / (k * (N - k)))
        st.append(dict(metode=NM[m], k=k, jaccard=np.mean(jac), kuncheva=np.mean(kun)))
sd = pd.DataFrame(st); sd.to_csv(S + "/kestabilan.csv", index=False)
print(sd.pivot(index="metode", columns="k", values="kuncheva").round(3))
# fitur yang paling sering terpilih pada k=20
cnt = pd.Series([f for s in seeds for m in NM if m != "acak" for f in fs[s][m][:20]]).value_counts()
cnt.head(15).to_csv(S + "/fitur_paling_sering_k20.csv", header=["jumlah"])
 
# Kelas langka
rl = []
for m in NM:
    r = {"Metode": NM[m]}
    for k in K:
        sub = x[(x.metode == m) & (x.k == k)]
        r["FIN %d" % k] = "%.2f" % sub["recall_NMAP_FIN_SCAN"].mean(); r["Meta %d" % k] = "%.2f" % sub["recall_Metasploit_Brute_Force_SSH"].mean()
    rl.append(r)
pd.DataFrame(rl).to_csv(S + "/recall_kelas_langka.csv", index=False)
pen = x[x.metode == "semua"]
print("recall penuh FIN %.3f Meta %.3f" % (pen.recall_NMAP_FIN_SCAN.mean(), pen.recall_Metasploit_Brute_Force_SSH.mean()))
 
# Sumber daya (XGBoost; rata-rata atas metode dan seed)
xs = d[(d.model == "XGB") & (d.metode != "acak")]
rs = xs.groupby("k")[["t_latih", "t_pred_1baris_ms", "ukuran_pickle_MB", "t_pred_batch"]].mean().round(3)
rs.to_csv(S + "/sumber_daya.csv"); print(rs)
print(d.groupby("seed").t_seleksi_total.first().describe().round(1))
rfd = d[d.model == "RF"].groupby(["metode", "k"]).f1_macro.agg(["mean", "std"]).round(4); rfd.to_csv(S + "/hasil_rf.csv"); print(rfd)
 
# Gambar 1: F1 macro terhadap jumlah fitur
fig, ax = plt.subplots(figsize=(8, 5))
cols = plt.cm.tab10(np.arange(7)); i = 0
ak = x[x.metode == "acak"].groupby("k").f1_macro.agg(["mean", "min", "max"]).reindex(K)
ax.fill_between(K, ak["min"], ak["max"], color="#cccccc", alpha=0.6, label="Acak (rentang antar-seed)")
ax.plot(K, ak["mean"], color="#888888", ls="--", label="Acak (rata-rata)")
for m in NM:
    if m == "acak": continue
    mm = [x[(x.metode == m) & (x.k == k)].f1_macro.mean() for k in K]
    ax.plot(K, mm, marker="o", color=cols[i], label=NM[m]); i += 1
ax.axhline(base.mean(), color="k", lw=1, label="Seluruh 80 fitur")
ax.set_xscale("log"); ax.set_xticks(K); ax.set_xticklabels(K); ax.set_xlabel("Jumlah fitur terpilih"); ax.set_ylabel("F1 macro (data uji, rata-rata 20 seed)")
ax.set_ylim(0.5, 1.0); ax.legend(fontsize=7, ncol=2, loc="lower right"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(S + "/g_f1_vs_k.png", dpi=200); plt.close(fig)
# Gambar 2: kestabilan Kuncheva
fig, ax = plt.subplots(figsize=(8, 4.5)); wd = 0.18
for j, k in enumerate(K):
    v = [sd[(sd.metode == NM[m]) & (sd.k == k)].kuncheva.iloc[0] for m in NM if m != "acak"]
    ax.bar(np.arange(7) + (j - 1.5) * wd, v, wd, label="%d fitur" % k)
ax.set_xticks(range(7)); ax.set_xticklabels([NM[m] for m in NM if m != "acak"], rotation=25, ha="right", fontsize=8)
ax.set_ylabel("Indeks Kuncheva antar-seed"); ax.set_ylim(0, 1.05); ax.legend(fontsize=8, ncol=4); ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig(S + "/g_kestabilan.png", dpi=200); plt.close(fig)
# Gambar 3: waktu latih dan ukuran model
fig, ax = plt.subplots(1, 2, figsize=(9, 3.6)); ks = [5, 10, 20, 40, 80]
r2 = d[(d.model == "XGB") & (d.metode != "acak")].groupby("k")[["t_latih", "ukuran_pickle_MB"]].mean().reindex(ks)
ax[0].plot(ks, r2.t_latih, marker="o"); ax[0].set_xlabel("Jumlah fitur"); ax[0].set_ylabel("Waktu latih XGBoost (dtk)"); ax[0].grid(alpha=0.3)
ax[1].plot(ks, r2.ukuran_pickle_MB, marker="o", color="C1"); ax[1].set_xlabel("Jumlah fitur"); ax[1].set_ylabel("Ukuran model (MB)"); ax[1].grid(alpha=0.3)
fig.tight_layout(); fig.savefig(S + "/g_sumber_daya.png", dpi=200); plt.close(fig)
print("analisis selesai")
