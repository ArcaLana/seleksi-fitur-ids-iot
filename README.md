
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

| Berkas / folder | Isi | Bab pada buku |
|---|---|---|
| `01_dasar_dan_biaya_fitur.ipynb` | Kutukan dimensi, pengelompokan 80 fitur menurut biaya, kebocoran data dan seleksi pada data acak, pemeriksaan versi pustaka | Bab 1 sampai 3, Lampiran A |
| `02_filter_wrapper_embedded.ipynb` | Fitur konstan dan berkorelasi, waktu metode filter, forward selection, waktu lima metode berbasis model | Bab 4 dan 5 |
| `03_data_timpang_dan_biaya.ipynb` | Seleksi pada kelas langka, F1 makro, G-mean, recall per kelas, model biaya dan anggaran, titik Pareto | Bab 6 dan 7 |
| `04_stabilitas_dan_praktikum.ipynb` | Indeks Jaccard dan Kuncheva, agregasi peringkat, praktikum 20 seed, uji Friedman dan Wilcoxon | Bab 8 dan 9 |
| `05_ketahanan_sumber_daya_studi_kasus.ipynb` | Ablasi fitur port, serangan baru, latensi dan memori, studi kasus gateway | Bab 10 sampai 12 |
| `kode_buku/` | Potongan kode per nomor pada buku (Kode 1.1 sampai 12.3; Kode A.1 di `lampiran_A/`), berkas `kode_N_M.py` beserta `kode_N_M_keluaran.txt` | Bab 1 sampai 12 |
| `eksperimen/` | Skrip lengkap eksperimen (Lampiran F): `siapkan_output.py`, `run_seed.py`, `analisis.py`, `run_b4x.py`, `run_b5x.py`, `buat_gambar.py` | Bab 4, 5, 9 |
| `hasil_nyata/` | Keluaran asli dari menjalankan kode (CSV, JSON, teks, gambar), per bab; lihat bagian paling bawah | Bab 1 sampai 12 |
| `data/` | Petunjuk menyiapkan data (data tidak diunggah) | |
| `requirements.txt` | Versi pustaka yang dipakai penulis | |

Nomor kode pada notebook sama dengan nomor pada buku, sehingga mudah dicocokkan. Keluaran yang tersimpan di bawah sel adalah keluaran asli dari hasil menjalankan kode oleh penulis.

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

Dataset **RT-IoT2022** tidak disertakan. Unduh `RT_IOT2022.csv` dari UCI (<https://doi.org/10.24432/C5P338>), letakkan di `data/`,
lalu folder `output/` (setara keluaran Bab 8 Jilid 1) dapat disusun dengan:

```bash
python3 -I eksperimen/siapkan_output.py data/RT_IOT2022.csv output
```

Bila Anda sudah menjalankan notebook Jilid 1, folder `output/` dari sana dapat dipakai langsung. Rincian ada di `data/README.md`.

## Cara menjalankan di Google Colab

1. Buka notebook dari repositori ini di Colab (**File → Open notebook → GitHub**, tempel alamat repositori), atau unduh notebook dan unggah ke <https://colab.research.google.com>.
2. Jalankan sel **Persiapan** di notebook pertama yang Anda buka. Sel itu mengambil repositori, memasang pustaka, meminta Anda mengunggah `RT_IOT2022.csv`, lalu menyusun `output/`.
3. Jalankan sel berurutan dari atas ke bawah. Urutan yang disarankan: `01` → `02` → `03` → `04` → `05`.

Catatan waktu: Kode 5.2, 9.3, dan 9.4 memakan satu sampai tiga menit pada mesin dua inti. Berkas yang diunggah ke panel Files hilang ketika sesi Colab berakhir.

Kode 7.3, 8.2, 10.1, 11.1, 11.2, 12.2, dan 12.3 memerlukan berkas hasil percobaan penulis yang belum tersedia di repositori ini; pada notebook, sel-sel itu diberi catatan dan keluaran aslinya tetap tampil.

### Tanpa Colab

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -I eksperimen/siapkan_output.py data/RT_IOT2022.csv output
python3 kode_buku/bab9/kode_9_1.py
cd eksperimen && mkdir hasil && python3 -I run_seed.py 42 hasil
```

Sebagian potongan kode bergantung pada variabel dari potongan sebelumnya dalam bab yang sama (misalnya Kode 6.2 memakai
data yang disiapkan Kode 6.1), jadi jalankan berurutan dalam satu sesi, atau pakai notebook.

## Lingkungan penulis

Python 3.13.16, pandas 3.0.5, NumPy 2.5.3, scikit-learn 1.9.1, XGBoost 3.4.1, SciPy 1.18.1, Matplotlib 3.11.2.
Percobaan dijalankan pada mesin Linux dua inti. Skor dapat sedikit berbeda bila versi pustaka atau mesin berbeda.

## Status pengujian

- Kelima notebook dan 39 berkas `.py` lolos pemeriksaan sintaks.
- Notebook 01 sampai 04 dijalankan sampai selesai pada data RT-IoT2022 asli, kecuali Kode 7.3 dan 8.2 yang memerlukan berkas hasil yang belum ada. Notebook 05: Kode 10.2, 10.3, dan 12.1 dijalankan; Kode 10.1, 11.1, 11.2, 12.2, dan 12.3 menunggu berkas hasil.
- Skor pada Bab 4, 5, dan 9 dihitung ulang dari awal (20, 10, dan 20 seed) dan cocok dengan angka pada buku; keluarannya ada di `hasil_nyata/`.

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
