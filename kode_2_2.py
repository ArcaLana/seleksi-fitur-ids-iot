"""Kode 2.2  Ilustrasi memori status aliran menurut banyak variabel dan banyak aliran
Buku: Fundamental Seleksi Fitur untuk IDS IoT (Jilid 2).
Data: lihat data/README.md (folder output/ hasil Jilid 1)."""
# Ilustrasi memori status aliran (angka hipotetis, bukan pengukuran)
KUNCI, UKURAN_VAR = 40, 8                      # byte
print("variabel  status/aliran(B)   10.000 aliran   50.000 aliran  100.000 aliran")
for v in (12, 20, 30, 80):
    s = KUNCI + v * UKURAN_VAR
    kol = [f"{s * n / 1e6:10.2f} MB" for n in (10_000, 50_000, 100_000)]
    print(f"{v:8d}  {s:16d}  " + "  ".join(kol))
