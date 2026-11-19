# Skrip eksperimen

Skrip dijalankan dari folder yang berisi `output/` (lihat `../data/README.md`) dan dengan Python yang sudah
memasang `requirements.txt`. Gunakan satu proses pada satu waktu bila Anda ingin mengukur waktu.

| Skrip | Bab | Fungsi | Cara jalan |
|---|---|---|---|
| `run_seed.py` | 9 | Satu seed: ANOVA F, informasi bersama, importance RF dan XGBoost, permutation, L1, RFE, kontrol acak, dan model penuh | `python3 -I run_seed.py 42 hasil` |
| `analisis.py` | 9 | Ringkasan semua seed, kestabilan Kuncheva, uji Friedman, Wilcoxon dengan koreksi Holm, gambar | `python3 -I analisis.py hasil` |
| `run_b4x.py` | 4 | Filter ANOVA dan chi-kuadrat, dengan dan tanpa pemangkasan korelasi (0,95 dan 0,80) | `python3 -I run_b4x.py 42 hasil` |
| `run_b5x.py` | 5 | Sensitivitas penalti L1, langkah RFE, jenis importance XGBoost, dan ulangan permutation | `python3 -I run_b5x.py 42 hasil` |

Folder keluaran (`hasil` pada contoh di atas) harus sudah ada: `mkdir hasil`.

## Mengulang 20 seed (Bab 9)

```bash
mkdir hasil
for s in $(seq 42 61); do
  [ -f hasil/hasil_seed$s.csv ] || python3 -I run_seed.py $s hasil
done
python3 -I analisis.py hasil
```

Pengecekan `[ -f ... ]` membuat proses dapat dilanjutkan bila terputus. Bab 4 memakai seed 42–61 dan Bab 5 seed 42–51.

## Catatan kejujuran

- Skrip di folder ini adalah skrip yang dimuat pada Lampiran F buku. Pada penyusunan repositori ini, skrip diambil dari
  Lampiran F dan diperiksa sintaksnya; hasil lengkap 20 seed pada buku berasal dari proses asli di mesin dua inti.
- Waktu yang tertera pada buku (terutama Bab 5 dan Bab 11) diukur pada satu mesin dan hanya indikatif.
- Skrip untuk Bab 6, 7, 8, 10, 11, dan 12 pada bentuk aslinya tidak ikut disertakan. Inti logikanya ada pada potongan
  kode di `../kode_buku/` (misalnya Kode 6.2, 7.2, 8.2, 10.2, 11.1, 12.1), yang dapat dijalankan setelah `output/` tersedia.

## Catatan hasil run ulang
Bab 4 (20 seed), Bab 5 (10 seed) dan Bab 9 (20 seed) dijalankan ulang dari awal dengan skrip di folder ini;
keluarannya ada di `hasil_nyata/bab4/`, `bab5/` dan `bab9/`. Folder `output/` disusun dengan `siapkan_output.py`.
Waktu proses (detik) bergantung mesin dan beda 5–20% antarproses; angka skor tidak terpengaruh.
