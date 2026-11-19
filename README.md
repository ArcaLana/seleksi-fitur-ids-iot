
# Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2)

**Teori, Algoritma, dan Praktikum**

Kode pendamping buku *Fundamental Seleksi Fitur untuk IDS IoT* (Jilid 2 dari seri Fundamental … untuk IDS IoT).
Seluruh percobaan memakai dataset publik **RT-IoT2022** dan Python (dapat dijalankan di Google Colab).

## Penulis

1. Assoc. Prof. Dr. Ir. Zulhipni Reno Saputra Elsi, S.T., M.Kom.
2. Arif Maulana
3. Muhammad Ihsan, S.T., M.Kom.
4. Dedi Haryanto, S.Kom., M.Kom.

## Isi repositori

| Folder | Isi |
|---|---|
| `kode_buku/` | Potongan kode per nomor pada buku (Kode 1.1 sampai 12.3; Kode A.1 ada di `lampiran_A/`), tiap berkas `kode_N_M.py`, beserta `kode_N_M_keluaran.txt` berisi keluaran nyata yang tercetak pada buku |
| `eksperimen/` | Skrip lengkap eksperimen (Lampiran F): `run_seed.py`, `analisis.py`, `run_b4x.py`, `run_b5x.py` |
| `data/` | Petunjuk menyiapkan data (data tidak diunggah) |
| `requirements.txt` | Versi pustaka yang dipakai penulis |

### Peta kode per bab

| Bab | Topik | Berkas di `kode_buku/` |
|---|---|---|
| 1 | Kutukan dimensi | `bab1/kode_1_1.py` |
| 2 | Data, kelompok fitur, biaya | `bab2/kode_2_1.py` … `kode_2_3.py` |
| 3 | Kebocoran dan kebetulan pada banyak fitur | `bab3/kode_3_1.py`, `kode_3_2.py` |
| 4 | Metode filter | `bab4/kode_4_1.py`, `kode_4_2.py` |
| 5 | Wrapper dan embedded | `bab5/kode_5_1.py`, `kode_5_2.py` |
| 6 | Kelas langka | `bab6/kode_6_1.py` … `kode_6_3.py` |
| 7 | Seleksi sadar biaya | `bab7/kode_7_1.py` … `kode_7_3.py` |
| 8 | Kestabilan | `bab8/kode_8_1.py` … `kode_8_4.py` |
| 9 | Pengulangan 20 seed | `bab9/kode_9_1.py` … `kode_9_6.py` |
| 10 | Ablasi port dan serangan tak terlihat | `bab10/kode_10_1.py` … `kode_10_3.py` |
| 11 | Sumber daya | `bab11/kode_11_1.py`, `kode_11_2.py` |
| 12 | Keputusan akhir | `bab12/kode_12_1.py` … `kode_12_3.py` |

## Data

Dataset **RT-IoT2022** tidak disertakan. Unduh dari UCI (<https://doi.org/10.24432/C5P338>) dan siapkan folder `output/`
dengan notebook Jilid 1; rinciannya ada di `data/README.md`.

## Cara menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# letakkan folder output/ (hasil Jilid 1) di direktori kerja
python3 kode_buku/bab9/kode_9_1.py
cd eksperimen && mkdir hasil && python3 -I run_seed.py 42 hasil
```

Di Google Colab: unggah `output/` ke panel Files, lalu jalankan skrip dengan `!python3 ...` atau tempel isinya pada sel.

Sebagian potongan kode bergantung pada variabel dari potongan sebelumnya dalam bab yang sama (misalnya Kode 6.2 memakai
data yang disiapkan Kode 6.1), jadi jalankan berurutan dalam satu sesi, atau gabungkan ke satu berkas.

## Lingkungan penulis

Python 3.13.16, pandas 3.0.5, NumPy 2.5.3, scikit-learn 1.9.1, XGBoost 3.4.1, SciPy 1.18.1, Matplotlib 3.11.2.
Percobaan dijalankan pada mesin Linux dua inti. Skor dapat sedikit berbeda bila versi pustaka atau mesin berbeda.

## Status pengujian

- Seluruh 39 berkas `.py` lolos pemeriksaan sintaks.
- Empat skrip di `eksperimen/` dijalankan penuh sampai selesai pada data **sintetis** berbentuk sama dengan keluaran Jilid 1 (80 fitur, 12 kelas), untuk memastikan tidak ada galat. Skor pada data sintetis itu tidak bermakna dan tidak dipakai di buku. Hasil pada buku berasal dari data RT-IoT2022 asli.
- Potongan di `kode_buku/` yang tidak membutuhkan data dapat dijalankan langsung; sisanya membutuhkan folder `output/`.

## Prinsip percobaan

- Seleksi fitur hanya melihat data latih; data uji tidak dipakai untuk memilih fitur.
- Setiap seed membagi ulang data 70:30 secara stratifikasi; hasil dilaporkan sebagai rata-rata dan simpangan baku atas seed.
- Biaya fitur pada Bab 2 dan 7 adalah asumsi ilustratif penulis, bukan pengukuran perangkat.
- Hasil yang kurang menguntungkan suatu metode tetap dilaporkan.

## Cara mengutip

> Elsi, Z. R. S., Maulana, A., Ihsan, M., & Haryanto, D. (2026). *Fundamental Seleksi Fitur untuk IDS IoT: Teori, Algoritma, dan Praktikum*. [Penerbit].

Sesuaikan penerbit, tahun, dan ISBN setelah buku terbit.

## Lisensi

Kode berlisensi MIT (lihat `LICENSE`). Dataset RT-IoT2022 tunduk pada lisensi pemilik aslinya di UCI.

## Isi folder `hasil_nyata/`

Keluaran asli dari menjalankan kode, dikelompokkan per bab seperti pada repositori Jilid 1.

| Folder | Isi |
|---|---|
| `bab1/` sampai `bab12/`, `lampiran_A/` | `kode_N_M_keluaran.txt`: keluaran teks tiap nomor kode pada buku |
| `bab2/` | `g_distribusi_kelas.png` (gambar tambahan: distribusi 12 kelas) |
| `bab4/` | hasil 20 seed (`b4x_seed*.csv`, `b4x_fitur_seed*.json`) dan `g_filter_f1_recall_vs_k.png` (gambar tambahan) |
| `bab5/` | hasil 10 seed (`b5x_seed*.csv`), `gambar_5_1.png` dan dua gambar tambahan |
| `bab6/`, `bab7/`, `bab8/`, `bab10/`, `bab11/`, `bab12/` | `gambar_N_M.png`: gambar yang sama dengan yang tercetak pada buku |
| `bab9/` | hasil 20 seed (`hasil_seed*.csv`), tabel ringkasan (F1, kestabilan Kuncheva, Friedman, Wilcoxon, recall kelas langka, sumber daya), `gambar_9_1` sampai `gambar_9_3`, serta gambar hasil `analisis.py` |

Nama `gambar_N_M.png` sama dengan nomor gambar pada buku. Berkas yang diawali `g_` adalah gambar tambahan yang
dibuat dari hasil run (skrip: `eksperimen/buat_gambar.py`) dan tidak tercetak di buku.
Berkas `output/` dibuat dengan `eksperimen/siapkan_output.py` (lihat `data/README.md`).
Waktu proses bergantung mesin, sehingga pada mesin Anda dapat berbeda 5 sampai 20 persen dari angka pada buku.
