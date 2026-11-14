# Findings — Bullish MVRV Momentum cross di bear market di luar Z1: penanda akhir bear?

**Insight yang diuji:** K8 (crossover momentum "lead" big trend changes) · X1/S3 (momentum "right on the edge" → "might confirm bull is back")
**Sumber:** On-Chain Mind, 15 Sep 2026, `[08:10]-[08:50]`, `[13:18]`
**Tanggal validasi:** 16 September 2026
**Script:** [`analyze_bullcross_bear_nonz1.py`](analyze_bullcross_bear_nonz1.py) · **Event table:** [`events_bullcross_bear_nonz1.csv`](events_bullcross_bear_nonz1.csv)
**Data:** `data_master_all_metrics.csv` s/d 2026-09-15

## Ringkasan sederhana
Bullish cross MVRV Momentum yang muncul selama bear market tapi di luar Z1 cenderung **bukan** penanda akhir bear. Dari 12 event yang bisa dinilai, cuma **2 HIT (17%)** — dua-duanya dari bear 2011. Di bear 2013, 2017 dan 2021: **0 dari 9**. Hasil ini di bawah kandidat (i) (29%) dan setara Signal D like-for-like (14%) maupun base rate harian (14%). Satu-satunya pembeda: apakah harga sudah di atas STH RP ≥3 hari saat cross dikonfirmasi. Tanpa itu **0/9**, dengan itu 2/3 (n=3, didominasi 2011). Cross bear sekarang (sah 2026-07-29) masuk kelompok **tanpa Signal D**.

## Definisi (dikunci di muka, tanpa varian tambahan)
- MVRV Momentum (KB 6C.1, verbatim `research/analyze_mvrv_momentum_bullcross.py`): gap = SMA30(mvrv_ratio) − SMA30(SMA30). Cross valid = regime negatif sebelumnya ≥7 hari, lalu gap ≥0 bertahan ≥7 hari.
- **Anti-lookahead:** tanggal keputusan = hari cross + 6 (hari ke-7). Zona, Signal D, bear window dan outcome semuanya dihitung dari tanggal ini.
- Bear window, reclaim permanen, HIT/MISS: persis findings 08-25. Window = peak → reclaim permanen + 60 hari. HIT = keputusan ≥ reclaim − 30 hari DAN maxDD 90 hari > −20%.
- Event = cross valid di bear window, zona DF v2 at-gate ≠ Z1, cooldown 30 hari. Sub-kelompok: Signal D at-gate (close > sth_cost_basis ≥3 hari).
- Catatan data: reclaim permanen bergeser 1 hari dari run 08-25 (2012-11-04 vs 11-03; 2019-03-27 vs 03-28) karena revisi kecil data ChartInspect.

## Bear window
| Cycle | Peak | Low | Reclaim permanen | Window s/d |
|---|---|---|---|---|
| 2011 | 2011-06-08 | 2011-11-18 | 2012-11-04 | 2013-01-03 |
| 2013 | 2013-11-29 | 2015-01-14 | 2015-10-13 | 2015-12-12 |
| 2017 | 2017-12-16 | 2018-12-14 | 2019-03-27 | 2019-05-26 |
| 2021 | 2021-11-08 | 2022-11-21 | 2023-01-11 | 2023-03-12 |
| 2025 | 2025-10-06 | 2026-06-30 (sementara) | BELUM | censored |

## Hasil utama — n=16 event (12 dinilai, 4 censored) | HIT 2 | MISS 10 | hit rate 17%
| Cycle | Keputusan | Harga | Zona | Streak>STH RP | Lag vs reclaim | maxDD90 | Ret90 | Verdict |
|---|---|---|---|---|---|---|---|---|
| 2011 | 2012-03-27 | $4,82 | Z1b | 2 | −222 | −2,6% | +31,0% | MISS |
| 2011 | 2012-10-06 | $12,51 | Z3 | 48 | −29 | −18,7% | +8,1% | HIT |
| 2011 | 2012-12-05 | $13,37 | Z3 | 32 | +31 | −0,8% | +204,6% | HIT |
| 2013 | 2014-05-31 | $626 | Z3 | 2 | −500 | −25,3% | −18,8% | MISS |
| 2017 | 2018-03-14 | $8.398 | ZD | 0 | −378 | −21,1% | −21,1% | MISS |
| 2017 | 2018-05-05 | $9.762 | ZD | 0 | −326 | −39,4% | −23,8% | MISS |
| 2017 | 2018-07-28 | $8.218 | Z3 | 5 | −242 | −24,8% | −21,4% | MISS |
| 2017 | 2018-10-25 | $6.461 | ZD | 0 | −153 | −49,2% | −43,7% | MISS |
| 2017 | 2019-01-15 | $3.588 | Z2 | 0 | −71 | −4,4% | +40,5% | MISS |
| 2021 | 2022-03-03 | $42.476 | ZD | 0 | −314 | −32,7% | −29,9% | MISS |
| 2021 | 2022-08-03 | $22.845 | ZD | 0 | −161 | −19,1% | −10,3% | MISS |
| 2021 | 2022-11-01 | $20.482 | Z2 | 0 | −71 | −23,0% | +11,5% | MISS |
| 2025 | 2025-10-11 | $110.810 | ZD | 0 | n/a | −23,5% | −18,3% | CENSORED |
| 2025 | 2026-01-19 | $92.584 | ZD | 0 | n/a | −32,1% | −20,3% | CENSORED |
| 2025 | 2026-03-28 | $66.346 | ZD | 0 | n/a | −9,9% | −9,4% | CENSORED |
| 2025 | 2026-07-29 | $63.984 | ZD | 0 | n/a | −1,8% (48 hari) | n/a | CENSORED |

(Cross 2022-03-31 dibuang karena cooldown; outcome-nya MISS, maxDD −58%.)

- **Per cycle:** 2011 = 3 (2 HIT) · 2013 = 1 · 2017 = 5 · 2021 = 3 · 2025 = 4 censored. Zona: ZD 9, Z3 4, Z2 2, Z1b 1.
- Dari 12 yang dinilai: median ret90 **−14,6%**, median maxDD90 **−22,1%**.
- Satu HIT 2011 (2012-12-05) datang 31 hari **setelah** reclaim, artinya telat, bukan memimpin.
- Tiga event 2025 pertama **pasti MISS**: reclaim permanen tidak mungkin terjadi sebelum low 06-30, jadi ketiganya terlalu dini. Kalau dihitung: **2/15 = 13%**. Yang benar-benar terbuka cuma 2026-07-29.

### Sub-kelompok Signal D at-gate
| Kelompok | n (dinilai) | HIT | Hit rate | Per cycle | Med ret90 / maxDD90 |
|---|---|---|---|---|---|
| Aktif | 3 (3) | 2 | 67% | 2011 = 2, 2017 = 1 | +8,1% / −18,7% |
| Tidak aktif | 13 (9) | 0 | **0%** | 2011 = 1, 2013 = 1, 2017 = 4, 2021 = 3, 2025 = 4 | −18,8% / −23,0% |

Referensi: ada 6 cross berzona Z1 yang dikecualikan (KB mencatat n=4). Bedanya kemungkinan karena di sini zona dibaca di tanggal keputusan, bukan tanggal cross, dan data 2011 ikut masuk. Tidak mempengaruhi uji ini.

## Baseline
| Pembanding | n | Hit rate |
|---|---|---|
| **Uji ini** | 12 dinilai | **17%** (13% termasuk 3 event 2025 yang pasti MISS) |
| Kandidat (i) ≥21 hari (08-25) | 7 | 29% |
| Signal D BREAK → unlock ≤90 hari (08-04, kriteria beda) | 8 | 12% |
| 8 tanggal BREAK Signal D dinilai pakai aturan HIT/MISS 08-25 | 7 dinilai | 14% |
| Base rate harian: bear window selesai, non-Z1 | 2.021 hari | 14% |
| — hari Signal D aktif / tidak | 774 / 1.247 hari | 33% / 2% |

Deskriptif (bukan uji): hari dengan gap > 0 DAN Signal D aktif = 520 hari, hit 43%. Tapi 210 hari di antaranya jatuh setelah reclaim, jadi otomatis HIT. Kalau cuma hari sebelum reclaim: **310 hari, hit 5%**. Pemisahan ini memakai label ex-post, jadi hanya untuk menunjukkan kenapa 43% menyesatkan.

## Mid-cycle 2019-06-26 s/d 2020-05-01 (terpisah)
Low 2020-03-12 $4.837; reclaim analog 2020-04-23. **n=3, HIT 1:** 2019-11-12 ZD MISS (maxDD −23,7%) · 2020-01-15 Z3, Signal D aktif, MISS (−46,1%, COVID) · 2020-04-24 Z3 HIT (+27,8%).

## Status 2025-26 per 09-15
- Cross naik 2026-07-23, sah 07-29 (ZD, tanpa Signal D). Gap +0,125, tertinggi sejak cross.
- Close > STH RP sejak 08-19 (28 hari).
- Event 07-29 baru HIT kalau episode 08-19 bertahan 90 hari (s/d ±**2026-11-16**) DAN harga tidak ≤ $51.187 s/d 10-27. Low sejauh ini $62.824 (08-01).

## Standar Validasi
1 definisi dikunci, OK · 2 n=16/12 dinilai, sample kecil · 3 keputusan di hari ke-7; reclaim hanya label · 4 **kedua HIT dari bear 2011**; di luar 2011 0/9 · 5 tidak berlaku (full-history) · 6 tanpa varian; baseline cuma pembanding.

Keterbatasan: bear window ex-post, bukan alarm bear cepat real-time. Konstruksi momentum video tidak diungkap. Versi kita **tidak** "right on the edge": gap positif 55 hari, dan sempat positif juga Okt 2025, Jan 2026, Mar-Mei 2026. Klaim "hijau pertama >1 tahun" tidak terreplikasi.

## Verdict
**NEGATIF** untuk "momentum crossover lead big trend changes" di bear non-Z1: **2/12 HIT (17%), kedua HIT dari 2011; 0/9 di 2013/2017/2021**. Median ret90 −14,6%. Tidak lebih baik dari base rate harian atau Signal D (14%). Pembeda satu-satunya, Signal D at-gate (2/3 vs 0/9), berdiri di n=3 → low confidence. Hasil KB 6C.1 untuk Z1 (4/4) tidak bisa digeneralisasi ke bear berstruktur N.
