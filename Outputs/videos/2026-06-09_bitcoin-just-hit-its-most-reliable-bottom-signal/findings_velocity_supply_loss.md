# Findings — Velocity supply-in-loss (ROC 30-hari) sebagai sinyal dekat-capitulation?

**Video:** Bitcoin Just Hit Its Most Reliable Bottom Signal (On-Chain Mind, 2026-06-09)
**Tanggal validasi:** 2026-07-19
**Data:** `data_master_all_metrics.csv`, kolom `percent_btc_in_loss`
**Script:** `analyze_bottom_signals.py`
**Event CSV:** `events_v4_roc_loss_episodes.csv`

## Klaim video
Supply-in-loss melonjak ~16 poin dari ~34% (sebulan lalu) ke >50% sekarang; "ekspansi cepat unrealized pain" ini menandakan pasar sangat dekat capitulation floor.

## Definisi event
ROC 30-hari = `percent_btc_in_loss` hari ini − 30 hari lalu. Ambil semua hari dengan ROC ≥ +15 poin, merge episode berdekatan (30 hari). Untuk tiap episode: forward drawdown harga 30/60/90 hari sesudahnya, dan apakah dalam ±60 hari dari cycle low.

## Hasil (n=43 episode)
- 388 signal-days → **43 episode** (merge 30d).
- Sebaran per cycle: 2011=7, 2015=10, 2018=14, 2022+=12.
- **Hanya 2/43 episode dekat cycle low (±60d)** — keduanya di cycle 2018 (2018-12-06, 2019-02-06).
- Median forward drawdown: −13.4% (30d), −16.2% (60d), −17.0% (90d). Terburuk −75% (2011).

## Interpretasi
- Ekspansi cepat supply-in-loss jauh lebih sering menandai **AWAL crash** (harga masih turun rata-rata −13% s/d −17% ke depan) daripada dekat-dasar.
- Hanya 2/43 yang dekat low → velocity spike bukan penanda floor yang reliabel.
- Klaim video benar secara deskriptif untuk kejadian spesifik ini (lonjakan +16 poin memang terjadi), tapi sebagai aturan umum tidak terdukung lintas sejarah.
- n=43 episode lintas 4 cycle.

## Verdict
**[VALIDASI — 2026-07-19, CLOSED]** REJECTED kuat: klaim "lonjakan cepat supply-in-loss (~+16 poin/30 hari) = dekat capitulation floor" tidak terdukung. Dari 43 episode ROC30 ≥+15 poin (2011=7 / 2015=10 / 2018=14 / 2022+=12), cuma 2 yang dekat cycle low (±60d, keduanya 2018); mayoritas justru diikuti downside lanjutan (median forward drawdown −13% s/d −17%, terburuk −75%). Ekspansi cepat supply-in-loss cenderung menandai AWAL crash, bukan dekat-dasar. n=43 episode.
