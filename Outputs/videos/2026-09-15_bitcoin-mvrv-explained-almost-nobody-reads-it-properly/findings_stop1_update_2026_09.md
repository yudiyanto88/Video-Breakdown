# Findings — Update fakta STOP-1 (data s/d 2026-09-15)

**Insight terkait:** X1/S3 (STH-MVRV reclaim 1,0 + momentum hijau = bull kembali) · STOP-1
**Tanggal validasi:** 16 September 2026
**Script:** [`analyze_stop1_update_2026_09.py`](analyze_stop1_update_2026_09.py)
**Sifat:** deskriptif, bukan uji sinyal baru. Semua definisi dari findings 08-25, 08-04, KB 6C.1, DF v2 §1, btlib gate G1.

## Ringkasan sederhana
Struktur masih N penuh (0 hari T dalam 345 hari), jadi unlock formal DF v2 **masih mustahil secara mekanis**. Yang berubah sejak 07-15:
- harga close di atas STH RP sejak 2026-08-19 (28 hari) dan di atas 200 DMA sejak tanggal yang sama
- kandidat (ii) nyala 08-21 dan kandidat (i) nyala 09-08, **pertama kali di bear ini**
- MVRV Momentum sudah bullish-valid sejak 07-29

Semua sinyal ini baru bisa dinilai HIT/MISS setelah ±2026-11-16.

## (a) Struktur
- Peak 2025-10-06 → 09-15 = 345 hari; **hari struktur T = 0**
- Min STH RP/RP = **1,272** (2026-08-16); per 09-15 = 1,337

## (b) Episode close > STH RP
| Episode sejak peak | Hari |
|---|---|
| 2025-10-12..10-13 | 2 |
| 2025-10-26..10-27 | 2 |
| 2026-05-04..05-15 | 12 (event BREAK 08-04) |
| **2026-08-19..09-15 (berjalan)** | **28** |

- Kandidat (i) (streak = 21, cooldown 180): **nyala 2026-09-08**
- Kandidat (ii) (streak = 3 & slope30 STH RP > 0): **nyala 2026-08-21**, dengan slope cuma **+$23** (marginal). Slope30 per 09-15 = +$4.164
- Close vs 200_dma: $76.784 vs $70.258 → **di atas**, sejak 2026-08-19 (28 hari)
- STH RP $71.177 · RP $53.237
- Baseline historis: (i) 29% (n=7), (ii) 25% (n=4). HIT kalau reclaim permanen ≤ keputusan + 30 hari, jadi episode 08-19 harus bertahan 90 hari (±2026-11-16) dan tanpa DD ≥20%

## (c) MVRV Momentum (versi KB 6C.1)
- Gap per 09-15 = **+0,12523 (positif)**; cross bullish **2026-07-23**, bertahan **55 hari**, regime negatif sebelumnya 52 hari → **valid**, tanggal keputusan 2026-07-29
- Gap sekarang = maksimum sejak cross
- Pergantian tanda sejak Sep 2025: bull 10-05 · bear 10-16 · bull 01-13 · bear 02-02 · bull 03-22 · bear 06-01 · bull 07-23 → hari positif terakhir sebelum episode ini = 2026-05-31
- Klaim video "hijau pertama >1 tahun / right on the edge" **tidak cocok** dengan versi kita

## (d) STH-MVRV
- 2026-04-20..05-31: **max 1,0480 (05-10), 12 hari > 1,0** dari 42 hari
- Episode > 1,0 sejak peak:

| Episode | Hari | Max |
|---|---|---|
| 2025-10-06..10-09 | 4 | 1,098 |
| 2025-10-12..10-13 | 2 | 1,010 |
| 2025-10-26..10-27 | 2 | 1,012 |
| 2026-05-04..05-15 | 12 | 1,048 |
| **2026-08-19..09-15** | **28** | **1,151** |

- Per 09-15 = 1,0776
- sth_mvrv ≈ harga/STH RP (1,0776 vs 1,0788) → "STH-MVRV reclaim 1,0" pada dasarnya = Signal D / harga > STH RP
- Klaim video "pertama sejak Oktober" melewatkan episode Mei (12 hari, max 1,048) yang gagal. Episode sekarang memang yang terpanjang & tertinggi sejak peak
- Data 08-04: Signal D di bear balik ke bawah STH RP dalam 90 hari 7/8 kali → "in every other historical case" **tidak didukung data**

## (e) Sejak peak
- Min P/RP = **1,103** (2026-06-30); per 09-15 = 1,442. (08-05 mencatat 1,101 → revisi data kecil)
- Min lth_mvrv = **1,173** (2026-06-30); per 09-15 = 1,551

## (f) Zona & gate K2 per 2026-09-15
- Harga $76.784 · STH RP $71.177 · RP $53.237 · LTH RP $49.457 · AVIV Mean $98.748 · AVIV Upper $112.429
- Struktur **N**, zona **Z3**
- Gate K2: sth_mvrv 1,0776 → **di luar band 0,80-0,97 (di atas)**
- Unlock DF v2 (STH RP cross naik RP) tetap mustahil selama struktur tidak pernah T

## Standar Validasi
Deskriptif; definisi dipakai ulang persis; semua nilai at-date; tidak ada n baru. Sinyal (i), (ii) dan cross momentum semuanya **censored** (90 hari belum lewat).
