"""Kode 8.4  Menghitung jumlah fitur berbeda yang pernah terpilih dan irisan antar-pasangan seed
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
import json, itertools, collections
E = "hasil/"                                             # fitur_seed42.json ... fitur_seed61.json
fs = {s: json.load(open(f"{E}fitur_seed{s}.json")) for s in range(42, 62)}
k = 20
for m in ("anova", "perm"):
    himp = [set(fs[s][m][:k]) for s in fs]
    cnt = collections.Counter(f for h in himp for f in h)            # berapa seed memilih tiap fitur
    irisan = [len(a & b) for a, b in itertools.combinations(himp, 2)]
    print(f"{m:6s} k={k}: fitur berbeda yang pernah terpilih = {len(cnt)} dari 80 | "
          f"terpilih di 20 seed = {sum(v == 20 for v in cnt.values())} | di >=10 seed = {sum(v >= 10 for v in cnt.values())}")
    print(f"       irisan antar-pasangan: min {min(irisan)}, maks {max(irisan)}, rata-rata {sum(irisan)/len(irisan):.2f}")
print("perm, frekuensi pemilihan 6 fitur teratas:", collections.Counter(f for s in fs for f in fs[s]['perm'][:k]).most_common(6))
