"""Kode 12.1  Mengisi anggaran biaya dengan skor per biaya, dengan dan tanpa fitur port
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
# Anggaran biaya 40 satuan (model biaya Kode 7.1; model penuh = 190). Dua langkah: peringkat skor, lalu isi anggaran.
B = 40
def isi(skor, bayar=True, larang=()):
    pilih, total = [], 0
    for i in np.argsort(-(skor / cost if bayar else skor)):      # skor per biaya, atau skor saja
        if i in larang: continue
        if total + cost[i] <= B: pilih.append(int(i)); total += cost[i]
    return pilih
 
PORT = [fitur.index("id.orig_p"), fitur.index("id.resp_p")]
ix = xgb().fit(Xtr, ytr).feature_importances_                    # importance XGBoost
C4 = isi(ix / ix.sum())                                          # C4: skor per biaya
ip = xgb().fit(np.delete(Xtr, PORT, axis=1), ytr).feature_importances_
sp = np.zeros(len(fitur)); sp[[i for i in range(len(fitur)) if i not in PORT]] = ip / ip.sum()
C5 = isi(sp, larang=set(PORT))                                   # C5: sama, tanpa fitur port
ir = RandomForestClassifier(n_estimators=100, n_jobs=2, random_state=42).fit(Xtr, ytr).feature_importances_
C6 = isi(ir / ir.sum())                                          # C6: importance Random Forest per biaya
