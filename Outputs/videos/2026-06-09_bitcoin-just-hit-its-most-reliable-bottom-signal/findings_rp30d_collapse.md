# Findings — Rolling-30d realized profit collapse sebagai bottom signal?

**Video:** Bitcoin Just Hit Its Most Reliable Bottom Signal (On-Chain Mind, 2026-06-09)
**Tanggal validasi:** 2026-07-19
**Data:** `data_master_all_metrics.csv`, kolom `daily_realized_profit_btc`, `btc_price`
**Script:** `analyze_bottom_signals.py`
**Event CSV:** `events_v3_rp30d_by_cycle.csv`, `events_v3_collapse_episodes.csv`

## Klaim video
"Cash extracted" (realized profit) pada basis rolling 30-hari kolaps ~10x dari peak cycle (~$55B → ~$3B) = "textbook bottom-forming behavior".

## Proksi & keterbatasan (EKSPLISIT)
Data kita tidak punya gross realized profit USD ala Glassnode. Proksi yang dipakai: **`daily_realized_profit_btc × btc_price`** (USD notional harian), lalu rolling 30-hari sum. Keterbatasan: ini notional harian × harga close, **bukan** cost-basis-adjusted realized value Glassnode — level absolut tidak identik dengan angka video, tapi bentuk slope (kolaps relatif dari peak) tetap informatif.

## Definisi event
- Per cycle: rasio `trough_rp30d / peak_rp30d` dalam window cycle, dan lead/lag trough terhadap price low.
- FP scan: setiap hari di mana rolling-30d ≤10% dari trailing-365d max (cooldown 90d) = "collapse episode". Near-low jika dalam ±90 hari cycle low.

## Hasil

### Trough vs peak per cycle (n=4)
| Cycle | peak_rp30d | trough_rp30d | trough/peak | low − trough (hari) |
|-------|-----------|--------------|-------------|---------------------|
| 2011 | 1,197,735 | 8,322 | 0.007 | +28 (trough sebelum low) |
| 2015 | 72,465,357 | 599,235 | 0.008 | −90 (trough setelah low) |
| 2018 | 1,275,898,818 | 8,365,708 | 0.007 | −64 (setelah low) |
| 2022 | 2,238,829,632 | 40,226,381 | 0.018 | −41 (setelah low) |

Kolaps di tiap bottom jauh melampaui 10x — praktis >50–100x (trough/peak 0.7–1.8%).

### FP scan (≤10% trailing-365d max, cooldown 90d)
**8 episode, 0 dekat cycle low** (semua False near_low_90d): 2011-07, 2013-06, 2014-04, 2018-03, 2019-12, 2021-07, 2022-01, 2022-06.

## Interpretasi
- Kolaps realized-profit adalah kondisi yang hampir selalu ADA di bottom (necessary-ish), TAPI **non-spesifik**: kolaps ≤10%-of-peak juga muncul di 8 episode lain yang semuanya bukan bottom (0/8 TP).
- Trough juga cenderung **telat 40–90 hari** setelah price low (kecuali 2011) → bukan sinyal timing yang presisi.
- n=4 cycle bottom + 8 FP episode.

## Verdict
**[VALIDASI — 2026-07-19, CLOSED]** REJECTED sebagai sinyal timing standalone (proksi `daily_realized_profit_btc × btc_price`, bukan gross realized profit Glassnode). Rolling-30d memang kolaps ke <2% dari peak di tiap cycle low (necessary-ish), tapi kolaps ≤10%-of-peak juga muncul di 8 episode lain yang semuanya BUKAN dekat bottom (0/8 TP) — jadi non-spesifik, high false-positive. Trough juga cenderung telat 40-90 hari setelah price low (kecuali 2011). Berguna sebagai confirming context, bukan trigger. n=4 cycle bottom + 8 FP episode.
