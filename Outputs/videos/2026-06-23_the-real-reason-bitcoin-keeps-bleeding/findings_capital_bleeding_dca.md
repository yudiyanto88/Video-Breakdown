# Uji Hipotesis: Capital Bleeding (30d % Change Realized Cap) sebagai Sinyal DCA

- **Asal klaim:** video "The Real Reason Bitcoin Keeps Bleeding" (On-Chain Mind, 2026-06-23)
- **Tanggal uji:** 2026-07-13
- **Data:** `realized_cap_usd` dari `data_master_all_metrics.csv` (Onchain-Dashboard), full history s/d 2026-07-12
- **Script:** `analyze_capital_bleeding_dca.py` (folder ini). Tabel episode: `_capital_bleeding_episodes.csv`

## Definisi event (ditetapkan sebelum lihat hasil)

- `rc30` = % change 30 hari `realized_cap_usd`. Hari negatif = rc30 < 0.
- **Sinyal aktif (at-gate, tanpa lookahead):** rc30 < 0 sudah >=14 hari berturut-turut sampai hari itu.
- **Episode** (untuk hitung n): rangkaian hari negatif, digabung kalau dipisah <=7 hari non-negatif; qualifying kalau total hari negatif >=14.
- Forward return 90/180/365 hari dari harga close; hari tanpa data forward dibuang per horizon.

## Ringkasan Sederhana

Video benar secara deskriptif: streak "capital bleeding" memang muncul di setiap bear besar (2011, 2014-15, 2018-19, 2022, sekarang), dan makin panjang streak-nya makin bagus forward return-nya (arah klaim benar). Tapi sebagai sinyal DCA, bleeding TIDAK menambah alpha di atas aturan sederhana "harga sudah drawdown >=20% dari ATH" — semua hari bleeding ternyata subset dari hari drawdown >=20%, dan di dalam subset itu hari bleeding justru sedikit lebih jelek median return-nya. Paling penting untuk konteks sekarang: reading -1.35%/bulan di tanggal video itu biasa-biasa saja (persentil 48 dari semua hari negatif historis — persis median), dan di ketiga bear sebelumnya, saat level ini pertama kali tercapai, cycle bottom masih 50-57% LEBIH RENDAH dan 3-10 bulan kemudian. Klaim "potent local DCA signal" tidak didukung — kalau pun dipakai, ini sinyal "kita ada di dalam fase akumulasi multi-bulan", bukan sinyal bottom dekat.

## Hipotesis & Hasil

| Hipotesis | Verdict | Ringkasan |
|-----------|---------|-----------|
| (a) Streak negatif muncul di bear besar (2014, 2015, 2018-19, 2022, sekarang) | **CONFIRM (deskriptif)** | **n=18 episode** qualifying, sebaran per cycle: C1=1, C2=3, C3=5, C4=6, C5=3. Semua bear yang disebut video ada, plus episode kecil mid-cycle (2019, 2021, 2023) |
| (b) DCA saat bleeding > DCA uniform / DCA saat drawdown >=20% | **NOT-SUPPORTED** | BLEED adalah subset DD20 (0 hari bleeding di luar drawdown >=20% dari ATH). Median fwd180: BLEED +28.5% vs DD20 +39.3% vs DD20-tanpa-BLEED +42.7%. Di semua horizon median BLEED < DD20. Satu-satunya keunggulan: win rate 365d lebih tinggi (81.7% vs 76.2%) |
| (c) Makin panjang streak = makin discounted (monotonic) | **PARTIAL (arah benar)** | Spearman rho(panjang run, fwd return) = +0.23 (90d), **+0.39 (180d)**, +0.16 (365d), semua signifikan. Bucket run >=100 hari: fwd180 median +50.2%, 82.8% positif; fwd365 100% positif (n=379 hari, tapi hari-hari ini berkorelasi — efektifnya cuma ~4 episode panjang, 1 per cycle) |
| (d) Redundan dengan K4? | **TIDAK redundan — jauh lebih awal & jauh lebih kasar** | Dari 1.255 hari sinyal aktif, cuma 11.8% punya K4 count >=2 dan 22.6% di Z1. Sebaliknya 98% hari K4>=2 juga bleeding. Lead time first-fire: 2014-04 vs K4>=2 2015-01 (~8 bln), 2018-02 vs 2018-11 (~9 bln), 2022-01 vs 2022-08 (~7 bln). Bleeding = superset awal yang tidak presisi; K4 = filter presisinya |
| (e) Reading -1.3%/bulan = "potent local DCA signal right now" | **NOT-SUPPORTED** | -1.35% ada di **persentil 48** hari negatif historis (median, bukan ekstrem). Di bear 2014/2018/2022, saat rc30 pertama kali <= -1.35%, bottom masih **-50.4% / -57.0% / -55.1%** lebih rendah, 103/311/303 hari kemudian, dan bleeding masih memburuk ke -4.3% / -6.3% / -5.7% |

## Detail penting

- **Dominasi cycle:** BLEED mengalahkan UNIFORM cuma di C4 (median fwd180 +37% vs +13%) dan C5 (+70% vs +26%). Di C1/C2/C3 kalah telak (C2: **-27.5%** vs +91%). "Beli saat bleeding" bekerja di 2 cycle terakhir saja — hati-hati recency bias.
- Klaim video "second largest bleeding event of this bear" benar tapi trivial: bear 2025-26 baru punya 2 episode (Des 2025–Mei 2026: 123 hari negatif, min -2.60% di 2026-02-18; episode berjalan sejak 23 Mei 2026: min -1.62% di 2026-06-30). Dengan n=2, otomatis "terbesar kedua".
- Independensi sample lemah: 1.255 hari sinyal berasal dari ~9 rezim bear/koreksi; bucket run 100+ (hasil terbaik) hanya dari 4 episode panjang (2011, 2014-15, 2018-19, 2022).
- Interpretasi yang bisa dipertahankan: bleeding streak panjang (>60-100 hari) = konfirmasi konteks rezim bear-bottom multi-bulan — cocok sebagai context, bukan timing. Fungsi timing/presisi tetap di K4 confidence count.

## Verdict akhir

**PARTIAL.** Deskripsi fenomena dan arah monotonicity benar; klaim actionable ("naikkan DCA sekarang karena reading potent") tidak didukung — reading saat video di median historis, tanpa alpha di atas drawdown-filter sederhana, dan preseden 3 bear menunjukkan downside lanjutan besar setelah level ini pertama tercapai. Tidak perlu masuk framework sebagai sinyal; paling banter catatan konteks di K4.
