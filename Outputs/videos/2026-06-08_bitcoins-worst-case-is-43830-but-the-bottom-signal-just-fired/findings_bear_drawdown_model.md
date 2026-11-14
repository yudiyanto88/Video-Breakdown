# Findings — Bitcoin Bear Market Drawdown Model (indikator custom, Bitcoin Magazine Pro)

**Tanggal validasi:** 2026-07-30
**Script:** `analyze_bear_drawdown_model.py`
**Event CSV:** `events_bear_drawdown_model.csv`

## Klaim yang diuji

Presenter menghitung rasio (bear log-drawdown / bull log-return) untuk 3 cycle historis:
2013→2015 (ratio 0.312), 2017→2018 (ratio 0.384), 2021→2022 (ratio 0.483). Rata-rata
0.393 (range 1SD 0.363–0.504), diterapkan ke bull run cycle saat ini (log-return 2.099
dari return 715.47%, ATH $126,219.03) → proyeksi central $55,311, worst-case (ratio
tertinggi 1SD) $43,830, optimistic (ratio 2013 murni) $65,528.

**n = 3 cycle historis** — di bawah standar 3-4 cycle minimum framework. Semua kesimpulan di bawah low-confidence secara struktural.

## (a) Reproduksi rasio dari `btc_price` aktual

| Cycle | Bull low → Peak | Peak → Bear low | Ratio reproduksi | Ratio klaim presenter |
|---|---|---|---|---|
| 2013→2015 | 2011-11-18 ($2.05) → 2013-11-29 ($1,156) | → 2015-01-14 ($178.50) | 0.295 | 0.312 |
| 2017→2018 | 2015-01-14 ($178.50) → 2017-12-16 ($19,538) | → 2018-12-14 ($3,281) | 0.380 | 0.384 |
| 2021→2022 | 2018-12-14 ($3,281) → 2021-11-08 ($67,525) | → 2022-11-21 ($15,774) | 0.481 | 0.483 |

Selisih maksimum 0.017 — formula presenter reproducible dan bukan karangan, hanya beda definisi tanggal peak/low yang presisi.

## (b) Mean±1SD vs regresi tren linear

Presenter treat 3 ratio (0.312, 0.384, 0.483) sebagai sampel acak (mean ± SD). Tapi ketiganya sebenarnya **tren naik monoton** (0.312 → 0.384 → 0.483). Kalau diperlakukan sebagai tren linear dan diekstrapolasi ke cycle ke-4 (bukan mean±SD):

- Metode presenter (mean+1SD): ratio 0.504 → **$43,830** (worst-case)
- Regresi linear tren, ekstrapolasi: → **$38,063**

Selisih **47.7%** dari basis proyeksi central presenter sendiri ($56,228 vs $38,063) — bahkan skenario "worst-case" presenter berpotensi masih terlalu optimis kalau tren linear (bukan mean±SD) yang dipakai. Dengan n=3, pilihan metode statistik saja sudah mengubah hasil hampir separuh.

## (c) Perbandingan ke Realized Price & LTH RP terkini

Data terbaru (2026-07-15): Realized Price = $52,740, LTH RP = $49,890.

- Worst-case presenter $43,830 = **-16.9%** vs RP, **-12.1%** vs LTH RP
- Central case presenter $55,311 = **+4.9%** vs RP, **+10.9%** vs LTH RP

Historis, BTC pernah dip di bawah LTH RP sebanyak 9 episode dengan kedalaman -7.9% s/d -40.5%. Level -12.1% (worst-case presenter) **berada di tengah range historis** — bukan skenario ekstrem/tidak masuk akal.

## Verdict

**[VALIDASI — 2026-07-30, CLOSED]** Rasio bear-log-drawdown/bull-log-return presenter (0.312/0.384/0.483) berhasil direproduksi dari `btc_price` aktual (0.295/0.380/0.481) — formula valid, bukan karangan. Tapi **n=3 cycle**: metode presenter (mean±1SD) vs treat sebagai tren linear monoton menghasilkan proyeksi berbeda 47.7% ($56,228 vs $38,063) dari basis yang sama — sangat sensitif ke pilihan metode statistik. Level worst-case $43,830 (-12.1% vs LTH RP terkini) **tidak ekstrem** secara historis — masuk dalam range kedalaman below-LTH-RP yang sudah pernah terjadi 9 kali (-7.9% s/d -40.5%). Kesimpulan: model matematisnya konsisten dan bisa direproduksi, tapi proyeksi harga spesifiknya (baik central maupun worst-case) adalah **low-confidence directional guess** dari sample 3 cycle, bukan angka presisi — jangan dipakai sebagai anchor keputusan tunggal.
