# Findings — 50/50 Supply in Profit sebagai "most reliable" bottom signal?

**Video:** Bitcoin Just Hit Its Most Reliable Bottom Signal (On-Chain Mind, 2026-06-09)
**Tanggal validasi:** 2026-07-19
**Data:** `data_master_all_metrics.csv`, kolom `percent_btc_in_profit`
**Script:** `analyze_bottom_signals.py`
**Event CSV:** `events_v2_profit_min_by_cycle.csv`, `events_v2_crossings.csv`

## Klaim video
Saat supply in profit turun ke ~50% (50/50 split profit/loss), itu menandai dasar tiap major bear sejak 2010 — dibingkai sebagai "most reliable bottom signal" yang berdiri sendiri (standalone). Framework aktif memakai `supply in profit <50%` sebagai 1 dari 4 kondisi komposit K4, bukan sinyal tunggal.

## Definisi event
(a) **Depth per cycle:** MIN `percent_btc_in_profit` dalam ±30 hari (61 hari-observasi) sekitar tiap cycle low.
(b) **Standalone reliability:** setiap kali `percent_btc_in_profit` cross ke bawah 50%, dengan merge/cooldown 180 hari antar crossing berdekatan. TP = crossing dalam ±90 hari dari cycle low; FP = di luar itu.

## Hasil

### (a) MIN supply-in-profit di sekitar tiap cycle low (n=4)
| Cycle | MIN pct_in_profit | Tgl |
|-------|-------------------|-----|
| 2011 | 43.48% | 2011-11-18 |
| 2015 | 39.32% | 2015-01-14 |
| 2018 | 39.86% | 2018-12-13 |
| 2022 | 44.48% | 2022-11-21 |

Tiap bottom menembus **di bawah 50%**, turun ke ~39–45% — bukan berhenti/mantul di 50/50 seperti dibingkai video.

### (b) Standalone crossing <50% (merge cooldown 180d, n=8)
4 TP / 4 FP → **precision 50%**.

| Cross date | Price | Cycle | Dalam ±90d low? |
|-----------|-------|-------|-----------------|
| 2011-09-16 | 4.82 | 2011 | TP |
| 2014-09-17 | 458 | 2015 | FP (mid-bear) |
| 2015-03-18 | 257 | 2015 | TP |
| 2018-11-14 | 5809 | 2018 | TP |
| 2020-03-12 | 4837 | 2018 | FP (COVID crash) |
| 2022-06-16 | 20381 | 2022 | FP (~5 bln sebelum low) |
| 2022-12-16 | 16636 | 2022 | TP |
| 2026-06-03 | 64257 | 2022+ | FP (current) |

## Interpretasi
- Sebagai **kondisi necessary**, supply-in-profit memang selalu turun di bawah 50% di tiap cycle low → mendukung penggunaannya di K4.
- Sebagai **sinyal standalone**, crossing <50% cuma coin-flip (precision 50%): sering menyala di tengah bear (2014-09) atau crash likuiditas (2020-03 COVID) yang bukan the-low. Ini persis alasan framework memperlakukannya sebagai komponen komposit yang butuh konfirmasi, bukan trigger tunggal.
- n=8 crossing / 4 cycle = sample kecil.

## Verdict
**[VALIDASI — 2026-07-19, CLOSED]** Framing "most reliable standalone" REJECTED; penggunaan `<50%` sebagai 1-dari-4 kondisi komposit K4 JUSTIFIED. Di tiap cycle low supply-in-profit turun di bawah 50% (ke ~39-45%, bukan berhenti di 50/50), jadi valid sebagai kondisi necessary. Tapi sebagai sinyal standalone, crossing <50% cuma coin-flip (4 TP / 4 FP, precision 50%, n=8 crossing / 4 cycle) — sering menyala di tengah bear atau crash likuiditas yang bukan the-low. Butuh konfirmasi, bukan trigger tunggal.
