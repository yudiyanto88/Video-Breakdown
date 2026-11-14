# Findings — Velocity RSI "generational bottom" cross-check terhadap state on-chain

**Video:** Bitcoin's Trend Is Bearish — Here's Where It Flips (On-Chain Mind, 2026-08-11)
**Tanggal validasi:** 2026-08-12
**Script:** `analyze_velocity_rsi_onchain_crosscheck.py`

---

## Klaim yang diuji

Video mengklaim weekly velocity RSI (indikator proprietary channel) saat ini ~14%, di bawah threshold 15% yang menurut mereka historically menandai "generational bottom" / setiap peluang akumulasi besar dalam sejarah Bitcoin.

## Kenapa tidak direplikasi langsung

Velocity RSI adalah indikator proprietary On-Chain Mind — formula "directional pressure" tidak dipublikasikan dan tidak bisa direkonstruksi dari kolom `data_master_all_metrics.csv` (yang isinya metrik on-chain, bukan price-momentum custom). Karena itu validasi ini BUKAN replikasi indikatornya, melainkan **cross-check independen**: apakah kondisi on-chain kita sendiri di tanggal yang sama mendukung atau membantah narasi "generational bottom / historically cheap".

## Catatan data

`data_master_all_metrics.csv` mentok update di **2026-07-15** — gap 27 hari ke tanggal video (2026-08-11). Semua angka di bawah pakai 2026-07-15 sebagai proxy tanpa ekstrapolasi (state on-chain seperti MVRV/SOPR tidak diekstrapolasi linear karena bukan trend yang smooth).

## Hasil — kondisi K4 @2026-07-15 (proxy)

| Kondisi K4 | Threshold | Nilai aktual | Status |
|---|---|---|---|
| LTH-MVRV | < 1.0 | 1.305 | OFF |
| aSOPR < 0.93 selama ≥7 hari & LTH-SOPR < 0.50 | — | aSOPR streak = 0 hari; LTH-SOPR = 0.725 | OFF |
| Supply in Profit < 50% & STH profit < 10% | — | Supply in profit = 56.9%; STH profit = 45.0% | OFF |
| Price/CVDD < 1.10 | — | 1.326 | OFF |

**K4 count = 0/4 kondisi menyala.**

## Zona harga

Zona harga @2026-07-15 = **ZD (dip dalam)**, bukan ZC/Z1 (bear bottom/capitulation).

## Konteks harga

Price turun ~48% dari ATH siklus ($124,714 @2025-10-06) ke $65,098 (2026-07-15) — downtrend riil dan cukup dalam, tapi metrik on-chain tidak menunjukkan capitulation state.

## Kapan terakhir K4 count ≥2

**2023-01-10** — 1,282 hari sebelum tanggal proxy (2026-07-15). Artinya sudah lebih dari 3.5 tahun sejak framework kita terakhir mendeteksi ≥2 kondisi K4 menyala bersamaan.

## Sample

**n = 1 snapshot** (cross-check kondisi hari ini, bukan event study lintas-cycle — by design, karena tujuannya menjawab "apakah kondisi SEKARANG capitulation", bukan pola historis berulang).

---

## Verdict

**[VALIDASI — 2026-08-12, CLOSED]** Cross-check independen K4 (4 kondisi bear-bottom framework) di 2026-07-15 (proxy, gap 27 hari ke tanggal video 2026-08-11) menunjukkan **0/4 kondisi menyala** dan zona = **ZD (dip dalam)**, bukan Z1/capitulation — terakhir kali K4 count≥2 adalah 2023-01-10 (1,282 hari sebelumnya). Ini **kontradiksi** dengan narasi "generational bottom" video: harga memang turun ~48% dari ATH cycle, tapi metrik on-chain kita (MVRV, LTH-SOPR, Supply in Profit, Price/CVDD) semuanya masih jauh dari level capitulation historis. **n=1 snapshot** (bukan event study) — tidak bisa memastikan kondisi persis di 2026-08-11 karena gap data 27 hari, tapi perlu penurunan on-chain yang sangat tajam dan cepat untuk berubah dari ZD ke Z1/capitulation dalam waktu sesingkat itu.
