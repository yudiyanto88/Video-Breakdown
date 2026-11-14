# Findings — Apakah persentil MVRV kebal diminishing peaks?

**Insight yang diuji:** B2 ("p90 2013 = p90 hari ini") · C1/C3 (frame percentile & panel distribusi)
**Sumber:** On-Chain Mind, 15 Sep 2026, `[06:28]-[07:47]`, `[09:10]-[09:40]`
**Tanggal validasi:** 16 September 2026
**Script:** [`analyze_mvrv_percentile_diminishing_peaks.py`](analyze_mvrv_percentile_diminishing_peaks.py) · **Event table:** [`events_mvrv_percentile_diminishing_peaks.csv`](events_mvrv_percentile_diminishing_peaks.csv)
**Data:** s/d 2026-09-15 (n = 5.905 hari)

## Ringkasan sederhana
Tidak kebal. Persentil MVRV menyusut **lebih lambat** dari angka mentah, tapi tetap **turun searah** di tiap cycle. Bull 2024-25 **tidak pernah** menyentuh p90 (0 hari, max 88,1), sementara 2013/2017/2021 masing-masing 59/100/102 hari. Kriteria falsifikasi yang ditetapkan di muka **terpenuhi → klaim GAGAL**. Sebaliknya, angka layar video (C3) **terreplikasi hampir persis**. Artinya video memakai persentil mentah full-history dari data yang sama.

## Definisi (dipakai ulang dari findings 08-05)
- **P1 causal** = percentile rank expanding (≤), burn-in 365 hari (valid sejak 2011-07-17). Full-sample hanya cermin. Tanpa varian detrended.
- Peak: 2011-06-08 / 2013-11-29 / 2017-12-16 / 2021-11-08 / 2025-10-06. Low (08-25): 2011-11-18 / 2015-01-14 / 2018-12-14 / 2022-11-21 / 2026-06-30 (sementara).
- Bull window = low sebelumnya → peak. Bull 2011 seluruhnya di burn-in, jadi cuma cermin full-sample.
- **Falsifikasi (di muka):** gagal kalau bull 2021 ATAU 2024-25 tidak mencapai ≥p90 causal, ATAU persentil peak turun searah raw.

## (1) Di tanggal cycle peak
| Cycle | MVRV | P1 causal | P1 full |
|---|---|---|---|
| 2011 | 7,445 | burn-in | 100,0 |
| 2013 | 5,167 | 97,9 | 99,6 |
| 2017 | 4,387 | 96,9 | 98,6 |
| 2021 | 2,851 | 87,4 | 91,2 |
| 2025 | 2,285 | **77,6** | 78,9 |

## (2) Per bull window
| Bull | Hari | Max MVRV (tgl) | Max P1 causal (tgl) | Hari ≥p90 causal | % hari | Hari ≥p95 | Max P1 full |
|---|---|---|---|---|---|---|---|
| 2011 | 327 | 7,868 (06-04) | burn-in | – | – | – | 100,0 |
| 2013 | 743 | 5,988 (2013-11-18) | 99,2 | 59 | 7,9% | 21 | 99,8 |
| 2017 | 1.068 | 4,982 (2017-12-07) | 98,5 | 100 | 9,4% | 16 | 99,3 |
| 2021 | 1.061 | 3,954 (2021-02-21) | 96,8 | 102 | 9,6% | 35 | 97,9 |
| 2025 | 1.051 | 2,770 (2024-03-11) | **88,1** | **0** | **0,0%** | 0 | 89,9 |

MVRV setara p90 causal di tanggal peak: 3,602 (2013) → 3,066 → 2,998 → 2,813 (2025) → 2,776 (09-15). Batas p90 cuma turun ~22%, sementara peak raw turun ~56%. Karena itu cycle terbaru tidak sampai.

## (3) Bear low (P1 causal)
| Bear | @ low | Min dalam bear |
|---|---|---|
| 2011 | 0,4 | 0,2 |
| 2013 | 2,4 | 2,4 |
| 2017 | 2,5 | 2,5 |
| 2021 | 3,2 | 2,7 (2022-11-09) |
| **2025 berjalan** | – | **17,0 (2026-06-30)** |

(08-05 mencatat 2,3/2,6/3,2 vs 16,9; selisih ≤0,1 karena konvensi low 12-14 vs 12-15 dan revisi data.)

## (4) Falsifikasi
- Bull 2021 ≥p90: **YA** (96,8). Bull 2024-25 ≥p90: **TIDAK** (88,1; full-sample 89,9 juga di bawah 90)
- Di tanggal peak: raw 5,17 → 4,39 → 2,85 → 2,29 dan P1 97,9 → 96,9 → 87,4 → 77,6, **dua-duanya turun monoton**
- Max per bull: raw 5,99 → 4,98 → 3,95 → 2,77 dan P1 99,2 → 98,5 → 96,8 → 88,1, **dua-duanya turun monoton**
- **Kriteria falsifikasi terpenuhi → klaim GAGAL**

## (5) Sanity C1/C3 per 2026-09-15
| Item | Data kita | Video (frame, low confidence) |
|---|---|---|
| mvrv_ratio | 1,4432 | 1,43 |
| % hari di bawah nilai sekarang | 37,5% | 36,6% |
| % hari di bawah 1,43 | **36,7%** | 36,6% |
| Hari di bucket 1,40-1,60 | **605** | 605 |
| P1 per 09-15 | 37,5 | ~35-40 |
| Min P1 2026 | 17,0 (06-30) | ~15-20 |

→ Persentil video = rank mentah full-history (tanpa model decay). Di hari terakhir causal = full-sample, tapi chart historisnya tetap memuat lookahead (rata-rata 4,6 pp, findings 08-05).

## Standar Validasi
1 definisi & falsifikasi di muka · 2 **n = 4 bull yang bisa diuji causal** (2013/2017/2021/2025) + 4 bear low → sample kecil · 3 P1 causal; full-sample cuma cermin · 4 unit = cycle, bukan hari · 5 tidak berlaku · 6 tanpa varian (p95 cuma kolom informatif).

## Verdict
**KLAIM GAGAL (low-n, tapi arahnya konsisten).** Persentil MVRV causal di cycle peak turun searah raw (97,9 → 96,9 → 87,4 → 77,6), dan bull 2024-25 tidak pernah mencapai p90 (0 hari vs 59-102 hari di tiga bull sebelumnya). Persentil cuma **meredam** kompresi, tidak menghilangkannya. p90 2013 dan p90 hari ini **tidak setara**. Angka layar video (36,6%, 605 hari, ~35-40) terreplikasi hampir persis.
