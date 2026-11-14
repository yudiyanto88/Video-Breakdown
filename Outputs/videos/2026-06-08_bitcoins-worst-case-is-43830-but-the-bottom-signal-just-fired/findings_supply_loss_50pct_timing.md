# Findings — Timing Klaim >50% Supply in Loss (HIGH PRIORITY — cek konflik faktual)

**Tanggal validasi:** 2026-07-30
**Script:** `analyze_supply_loss_50pct_timing.py`
**Event CSV:** `events_supply_loss_50pct_timing.csv`

## Klaim yang diuji

Presenter (video direkam 2026-06-08) mengklaim ">50% Bitcoin supply in loss" sebagai
capitulation signal historis (dikutip dari chart eksternal Benjamin Cowen), dan bilang
kondisi ini "just happened again" pada saat perekaman.

## Data aktual di sekitar tanggal video

| Tanggal | Price | % Supply Profit | % Supply Loss | % STH Loss |
|---|---|---|---|---|
| 2026-06-01 | $71,189 | 57.47 | 42.53 | 72.93 |
| 2026-06-03 | $64,257 | 49.87 | **50.13** (pertama tembus 50%) | 97.94 |
| 2026-06-06 | $60,811 | 47.71 | 52.29 (puncak periode ini) | 95.63 |
| **2026-06-08 (tanggal video)** | **$63,029** | **49.74** | **50.26** | 93.16 |
| 2026-06-12 | $61,369 | 47.86 | 52.15 | 97.23 |
| 2026-07-15 (data terbaru) | $65,098 | 56.88 | 43.12 | — |

## Verdict

**[VALIDASI — 2026-07-30, CLOSED]** Klaim presenter **terbukti akurat** — bukan konflik faktual seperti dugaan awal claim-tester. `%Supply in Loss` menembus 50% pertama kali pada 2026-06-03 (50.13%), lima hari sebelum video direkam, dan berada di 50.26% tepat pada tanggal video (2026-06-08). STH supply in loss jauh lebih ekstrem di periode yang sama (93-98%), konsisten dengan pola capitulation short-term-holder yang biasa menyertai kondisi ini. Per data terbaru (2026-07-15), angka sudah pulih ke 43.12% — kondisi >50% ini bersifat sementara/marginal (puncak 52.29%, tidak jauh di atas ambang), bukan capitulation dalam yang berkepanjangan. Catatan: ini konfirmasi klaim faktual presenter tentang timing, terpisah dari pertanyaan apakah threshold 50% itu sendiri adalah sinyal yang reliable (sudah established di framework lewat K4 kondisi #3, lihat `analysis.md`).
