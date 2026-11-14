# Findings: 200-day/200-week MA Reclaim vs Z1→Z2 Unlock (STH RP cross RP)

**Video sumber:** Bitcoin Magazine Pro, "Bitcoin Bottom Signal (Less Than 2 Weeks Away)", 2026-07-02
**Tanggal analisis:** 2026-07-28
**Script:** `analyze_ma_reclaim_vs_z1z2_unlock.py`
**Data:** `data_master_all_metrics.csv`, kolom `sth_cost_basis`, `realized_price`, `200_dma`, `200_wma`, `btc_price`

## Klaim yang diuji
Pembicara pakai reclaim 200-day / 365-day / 200-week MA sebagai konfirmasi keluar bear market. Framework sendiri pakai definisi lain: STH RP cross naik melewati RP (Z1→Z2 unlock, Decision_Framework v2.md). Pertanyaan: berapa jarak (lead/lag) antara MA reclaim teknikal dengan unlock objektif framework?

## Definisi event
- **Z1→Z2 unlock** = hari pertama `sth_cost_basis > realized_price` setelah sebelumnya `<=`. Whipsaw (<14 hari) di-merge, dipakai tanggal cross-up terakhir sebelum status bertahan >14 hari.
- **200_dma / 200_wma reclaim** = hari pertama `btc_price` > MA tsb setelah sebelumnya `<=`, DAN bertahan di atas >=30 hari kalender berturut-turut (sustained, bukan whipsaw).
- Untuk tiap episode Z1→Z2, dicari event reclaim MA terdekat secara absolut waktu (bisa sebelum/sesudah). Kalau tidak ada dalam radius wajar (>200 hari), dilaporkan N/A, bukan dipaksa dipasangkan.

## Hasil — n = 4 episode Z1→Z2 unlock historis (satu per bear-market cycle, independen)

| Episode Z1→Z2 | 200dma reclaim | lag (hari) | 200wma reclaim | lag (hari) |
|---|---|---|---|---|
| 2012-04-19 | 2012-03-05 | -45 | 2011-12-22 | -119 |
| 2015-11-03 | 2015-10-11 | -23 | 2015-10-03 | -31 |
| 2019-05-07 | 2019-04-02 | -35 | N/A (tidak ada di sekitar) | - |
| 2023-03-05 | 2023-01-13 | -51 | 2023-03-17 | +12 |

(negatif = MA reclaim terjadi SEBELUM Z1→Z2 unlock; positif = SESUDAH)

**200dma lag — n=4, semua negatif: -45, -23, -35, -51 hari.** Sangat konsisten: 200dma reclaim selalu mendahului Z1→Z2 unlock sekitar 23-51 hari.

**200wma lag — n=3 valid (dari 4 episode; 1 N/A):** -119, -31, +12. Untuk episode 2019, tidak ada event reclaim 200wma yang bersih di sekitar tanggal itu — karena selama crash 2018, harga **tidak pernah turun di bawah 200wma sama sekali** (200wma terlalu lambat untuk crash sedalam itu), jadi tidak ada "reclaim" yang bisa dideteksi.

## Verdict
Dengan n=4 episode historis independen (2012, 2015, 2019, 2023), reclaim **200-day MA cenderung mendahului** unlock objektif framework (STH RP cross RP) sekitar 3-7 minggu — ini artinya MA teknikal 200d duluan sinyal, baru dikonfirmasi belakangan oleh cost-basis on-chain. Untuk **200-week MA**, polanya kurang konsisten (n=3 valid saja, rentang lag -119 s/d +12 hari, dan salah satu episode tidak punya event reclaim sama sekali karena harga tidak sempat turun di bawah 200wma). Kesimpulan: MA reclaim teknikal (terutama 200dma) berguna sebagai **leading proxy** terhadap unlock framework, tapi bukan pengganti — jarak leadnya sendiri tidak konstan (23-51 hari), jadi tidak bisa dipakai untuk timing presisi. Sample n=4 kecil, wajib dianggap indikatif bukan definitif.

Bahasa probabilistik: 200dma cenderung reclaim lebih dulu daripada unlock STH RP/RP; 200wma tidak cukup konsisten untuk disimpulkan arah lead/lag-nya.
