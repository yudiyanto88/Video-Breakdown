# MVRV Z-Score Rolling-1Y vs AVIV — Cross-Check & Divergence Findings

**Sumber awal:** Video On-Chain Mind, 2025-01-22, item [INDIKATOR CUSTOM]
**Sesi validasi:** 2026-07-07 s/d 2026-07-11
**Status: CLOSED**

## Ringkasan
Video mengklaim MVRV Z-Score dengan rolling window 1 tahun lebih responsif menangkap turning point dibanding versi cumulative/4Y/2Y. Diuji dua hal: (1) apakah price band-nya align dengan AVIV Mean/Upper framework sebagai cross-check independen, (2) apakah divergensi antara dua metrik ini bisa jadi sinyal regime yang berguna.

## Bagian 1 — Cross-check price band (2026-07-07)
Data 2025-01-16: Video's Mean $91K vs AVIV Mean $83.25K (beda ~9%, ballpark sama, tidak presisi). Video's "+2σ" $113K vs AVIV Upper (0.5σ) $97.78K (beda ~15%). Tapi video's +2σ ($113K) hampir persis sama dengan AVIV +1σ Price ($112.3K, selisih <1%) — menunjukkan skala sigma kedua metode TIDAK setara (kira-kira 2:1, video's "2σ" ≈ AVIV's "1σ"). Tidak bisa dipakai sebagai cross-check sigma-ke-sigma langsung tanpa kalibrasi ulang.

**Kesimpulan: confirming lemah untuk ballpark umum, TIDAK confirming untuk klaim presisi.**

## Bagian 2 — Divergence check (2026-07-11)

### Formula
```
delta(t)      = MarketCap(t) - RealizedCap(t)
mean_1y(t)    = mean(delta) 365 hari trailing sebelum t
std_1y(t)     = stdev(delta) 365 hari trailing sebelum t
z_MVRV1Y(t)   = (delta(t) - mean_1y(t)) / std_1y(t)

sigma_unit(t) = price_at_aviv_plus_1_sigma(t) - price_at_aviv_mean(t)
z_AVIV(t)     = (Price(t) - price_at_aviv_mean(t)) / sigma_unit(t)
```

### Hasil (n=7 titik, 2 cycle, threshold divergen |selisih|>1.0)

| Tanggal | Regime | z_AVIV | z_MVRV1Y | \|Selisih\| | Divergen? |
|---|---|---:|---:|---:|:---:|
| 2021-10-20 | Local high pra-konsolidasi | 1.156 | 1.875 | 0.719 | Tidak |
| 2021-11-08 | Cycle top aktual | 1.074 | 1.807 | 0.734 | Tidak |
| 2024-01-15 | Awal bull, ETF launch | -0.151 | 1.892 | 2.042 | Ya |
| 2024-03-13 | Local top pre-correction | 0.997 | 3.878 | 2.881 | Ya |
| 2024-09-06 | Dasar mid-cycle correction | -0.442 | -0.319 | 0.123 | Tidak |
| 2025-01-16 | Recovery ke ATH baru | 0.576 | 1.865 | 1.289 | Ya |
| 2026-07-10 | Fase sekarang (bear) | -1.184 | -1.197 | 0.013 | Tidak |

3 dari 7 divergen, semua arah sama (z_MVRV1Y >> z_AVIV), semua cluster di cycle 2023-2025.

### Hipotesis awal (std_1y compression) — DIUJI DAN GAGAL
Hipotesis: divergensi terjadi karena std_1y(delta) rendah di baseline (window rolling-1Y masih "ingat" fase tenang sebelumnya). Dicek langsung di 3 titik divergen:

- 2024-01-15: std_1y 1.10e11 (rendah, tapi bukan trough absolut — trough sebenarnya Mei 2023 ~8.1e10)
- 2024-03-13: std_1y 1.68e11 (+52% dari Jan, SEDANG NAIK — bukan tertekan)
- 2025-01-16: std_1y 2.26e11 (di ujung ATAS range yang diamati)

**Hipotesis gagal untuk 2/3 titik.** Penggerak dominan ternyata numerator (delta - mean_1y), bukan denominator std yang tertekan. Konsisten dengan lompatan Market Cap yang genuinely besar/cepat relatif rata-rata trailing 1 tahunnya sendiri.

## Kesimpulan final
Divergensi z_MVRV1Y vs z_AVIV adalah **artefak struktural** dari perbedaan reaktivitas formula — MVRV1Y (window pendek, basis dolar mentah, all-supply) inherently lebih reaktif ke rally cepat dibanding AVIV (basis realized price active-investor, mean bergerak lambat). Rally cepat → divergen itu konsekuensi cara metrik dibangun, bukan sinyal regime independen.

**Tidak ada K-node atau threshold baru diusulkan. Status: CLOSED.**
Next step test cycle 2017/2019 di-skip — mekanisme sudah predictable dari formula, tambahan cycle tidak akan menjawab pertanyaan baru.

## Keterbatasan
n=7 titik bukan independent samples (turunan series yang sama, sebagian berdekatan dalam satu cycle). Cluster 3 titik divergen semuanya dari 1 cycle (2023-2025) — cuma 2 cycle dalam sample, di bawah minimum 3-4 cycle yang biasa dipakai framework untuk klaim confirming.
