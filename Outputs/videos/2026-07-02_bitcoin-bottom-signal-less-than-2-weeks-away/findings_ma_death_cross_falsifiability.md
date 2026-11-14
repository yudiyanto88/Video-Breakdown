# Findings: 50w/100w MA Death Cross — Falsifiability Check (proxy 50wma/200wma)

**Video sumber:** Bitcoin Magazine Pro, "Bitcoin Bottom Signal (Less Than 2 Weeks Away)", 2026-07-02
**Tanggal analisis:** 2026-07-28
**Script:** `analyze_ma_death_cross_falsifiability.py`
**Data:** `data_master_all_metrics.csv`, kolom `50_wma`, `200_wma`, `btc_price`, sampai 2026-07-15

## Klaim yang diuji
Pembicara memproyeksikan death cross 50-week/100-week MA pada **10 Juli 2026** sebagai penanda area bear low.

## Keterbatasan data — WAJIB dibaca sebelum verdict
Kolom `100_wma` **tidak ada** di data kita (cek `data_dictionary.md`). Proxy terdekat yang tersedia adalah `200_wma` (jauh lebih lambat dari 100wma). Semua hasil di bawah adalah uji terhadap **proxy 50wma/200wma**, BUKAN uji langsung klaim asli video (50w/100w) — tidak bisa dipakai sebagai konfirmasi atau penolakan definitif klaim tersebut.

## Definisi event
- Death cross = hari pertama `50_wma < 200_wma` setelah sebelumnya `>=`.
- Proyeksi crossing masa depan = ekstrapolasi linear gap (50wma−200wma) dari slope 90 hari terakhir — ini estimasi kasar, bukan fakta.

## Hasil
Sepanjang histori data (mulai 200wma tersedia, ~2011), hanya ada **3 event cross** total, dan **hanya 1 death cross**: 2023-02-16.

| Event | Tanggal |
|---|---|
| Golden cross | 2011-07-02 |
| Death cross | **2023-02-16** |
| Golden cross | 2024-01-11 |

**n = 1 death cross historis** untuk proxy 50wma/200wma — sample sangat kecil, WAJIB dianggap low-confidence, bukan pola berulang.

Untuk death cross 2023-02-16 satu-satunya itu: harga terendah lokal (±200 hari) ada di **2022-11-21 ($15,774)** — yaitu **87 hari SEBELUM** death cross terjadi. Artinya proxy 50wma/200wma ini bersifat **lagging confirmation**, bukan leading indicator — cross baru muncul ~3 bulan SETELAH harga sudah mencapai titik terendah siklus.

**Siklus sekarang (2026-07-15):** 50wma=$87,461, 200wma=$62,945, gap=$24,516 (50wma masih 38.9% di atas 200wma). Slope gap 90 hari terakhir: -141.76 USD/hari (mengecil, tapi masih jauh). Proyeksi linear kasar: gap baru mencapai 0 sekitar **awal Januari 2027** — bukan 10 Juli 2026 seperti klaim video.

## Verdict
Berdasarkan proxy 50wma/200wma (bukan klaim asli 50w/100w — catatan keterbatasan berlaku), klaim "death cross 10 Juli 2026" **tidak didukung data**: per 2026-07-15 gap kedua MA masih ~38.9% dan proyeksi linear mengarah ke akhir 2026/awal 2027, meleset ~6 bulan dari tanggal yang disebut video. Ditambah, satu-satunya preseden historis proxy ini (n=1, 2023) menunjukkan cross terjadi 87 hari **setelah** bottom harga sebenarnya, bukan menandainya di muka — jadi bahkan kalau proyeksi 2027 itu benar terjadi, historisnya proxy ini cenderung terlambat mengonfirmasi, bukan memprediksi bottom. Catatan: n=1 terlalu kecil untuk kesimpulan kuat soal lag-nya, tapi arah proyeksi tanggal cross itu sendiri cukup jelas melenceng dari klaim video.

Bahasa probabilistik: cenderung klaim tanggal spesifik ini keliru berdasarkan proxy yang tersedia; verdict soal klaim asli 50w/100w tetap NEEDS-DATA-WE-DONT-HAVE.
