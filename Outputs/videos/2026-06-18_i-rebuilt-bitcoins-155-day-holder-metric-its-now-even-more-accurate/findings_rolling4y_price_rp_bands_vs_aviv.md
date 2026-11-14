# Findings — Quantile band rolling-4y (Price/RP) vs AVIV Mean/Upper

**Tanggal validasi:** 2026-07-30
**Sumber klaim:** Video "I Rebuilt Bitcoin's 155-Day Holder Metric" — Bitcoin Magazine Pro (Matt Crosby), 2026-06-18, [10:53]–[12:01] + Figure 11
**Script:** [`analyze_rolling4y_price_rp_bands_vs_aviv.py`](analyze_rolling4y_price_rp_bands_vs_aviv.py)
**Preseden:** [`../2025-01-22_bitcoin-ath-what-next/findings_mvrv_rolling1y_vs_aviv.md`](../2025-01-22_bitcoin-ath-what-next/findings_mvrv_rolling1y_vs_aviv.md) — versi window 1 tahun, sudah CLOSED

---

## Klaim yang diuji

Quantile band (q05/q10/q20 – q80/q90/q95) dari rasio harga terhadap filtered realized price, rolling 4 tahun, sebagai koridor upper/lower — analog fungsional AVIV Mean/Upper di framework kita. Klaim spesifik di video: harga ~$65k = **persentil ~20** dari regime 4-tahun.

**Verdict: confirming lemah, tidak ada K-node baru — CLOSED cepat**, sejalan preseden window-1-tahun.

---

## Batasan yang berlaku

Data kita **base "std" + boundary statis 155 hari**. Yang diuji metodologinya, bukan angkanya.

Konstruksi: `ratio(t) = btc_price / realized_price` → persentil rolling 1.460 hari, window berakhir **t−1**.

Band valid baru sejak **2014-07-16** → cycle 2011 & 2013 tidak tercakup.

---

## Hasil

### (a) Di puncak siklus — band atas praktis kelipatan tetap AVIV

| Event | Price | q90 | q95 | AVIV Upper | AVIV+1SD | q90/AVIVup | q95/AVIV1sd |
|---|---|---|---|---|---|---|---|
| ATH 2017-12-17 | 19.336 | 12.831 | 14.012 | 10.299 | 12.045 | 1,25 | 1,16 |
| ATH 2021-04-14 | 63.007 | 58.447 | 62.641 | 46.598 | 54.102 | 1,25 | 1,16 |
| ATH 2021-11-08 | 67.525 | 70.051 | 78.611 | 57.193 | 66.196 | 1,22 | 1,19 |
| Peak 2025-08-13 | 123.314 | 125.096 | 133.544 | 113.591 | 128.285 | 1,10 | 1,04 |
| Peak 2025-10-06 | 124.715 | 130.858 | 140.509 | 118.988 | 134.330 | 1,10 | 1,05 |

Sepanjang sejarah: median q90/AVIV Upper = **1,16** (p10 1,02 – p90 1,26). **Korelasi log-level q90 vs AVIV Upper = 0,9992.**

Band atas pada dasarnya = AVIV Upper yang digeser ~10–25% ke atas, dengan rasio yang **turun** dari 1,25 (2017 & Apr-2021) ke 1,10 (2025). Jadi bukan konstanta persis — tapi juga bukan informasi baru di luar AVIV.

### (b) Di bear bottom — band bawah bukan lantai

| Event | Price | q05 | q10 | RP | CVDD | P/RP | P/CVDD | percentile |
|---|---|---|---|---|---|---|---|---|
| 2018-12-14 | 3.281 | 3.690 | 3.840 | 4.671 | 3.270 | 0,70 | **1,00** | 0,005 |
| 2020-03-12 | 4.837 | 4.911 | 6.606 | 5.697 | 4.516 | 0,85 | 1,07 | 0,047 |
| 2022-11-21 | 15.774 | 16.999 | 18.300 | 20.313 | 16.062 | 0,78 | **0,98** | 0,011 |
| 2026-06-30 | 58.460 | 47.507 | 51.651 | 53.115 | 48.958 | 1,10 | 1,19 | 0,142 |

Harga **menembus ke bawah q05 di ketiga bottom yang sudah final**. CVDD jauh lebih ketat sebagai lantai (P/CVDD 0,98–1,07). Band bawah tidak menambah apa-apa di sisi lantai.

### (c) Klaim video — reproduce

Pada **2026-06-16**: harga $65.715, persentil rolling-4y aktual = **0,201 (20,1th percentile)** — **konsisten dengan klaim "bottom 20th percentile at ~$65,000"**.

Label zona kita hari itu: struktur **N → ZD (Dip dalam)**. RP $53.452 · STH RP $72.449 · AVIV Mean $97.829 · AVIV Upper $112.203 · CVDD $48.841. Konsisten arah dengan Matt: sama-sama "murah tapi belum ekstrem".

### Temuan bonus — yang paling berguna dari validasi ini

Band kita hampir identik dengan angka Matt **meski base RP berbeda 9,4%**:

| Band | Kita | Matt (frame, low confidence) |
|---|---|---|
| q10 | $50.764 | $50.764 |
| q20 | $65.681 | $65.631 |
| q90 | $124.694 | $124.582 |
| q95 | $131.778 | $131.523 |
| RP | $53.452 (std) | $58.468 (flt) |

Ini bisa dibuktikan secara analitis: band = `quantile(P/RP) × RP`, jadi **kalau base RP hanya berbeda faktor skala, band-nya IDENTIK**. Diuji numerik: skalakan RP ×1,094 → deviasi q90 = **0,0000%**.

**Konsekuensi: seluruh kerja "filtered realized price" Matt praktis tidak mengubah output band ini.** Klaim akurasi yang bersandar pada filtered RP tidak didukung mekanika band-nya sendiri.

### (d) vs K4 kondisi 4 (Price/CVDD < 1,10), n = 4.383 (sejak 2014-07-16)

| Sinyal | hari | irisan dgn P/CVDD | \|phi\| | Jaccard |
|---|---|---|---|---|
| P < q05 | 68 | 57 | 0,686 | 51,4% |
| P < q10 | 308 | 97 | 0,538 | 31,2% |
| P < q20 | 825 | 100 | 0,317 | 12,1% |

`P/CVDD < 1,10` nyala 100 hari, **97 di antaranya sudah tercakup P<q10** → band bawah adalah superset yang lebih longgar, bukan informasi baru. 211 hari tambahan P<q10 didominasi **2015 (113) dan 2022 (59)** = satu-dua cycle.

Kalibrasi band relatif rapi: P>q95 nyala 3,5% hari (nominal 5%), P<q10 nyala 7,0% (nominal 10%) — lebih rapi daripada expanding percentile di V1 (18,3%).

---

## Verdict

**CLOSED — confirming lemah, tidak ada K-node baru.** Sejalan dengan preseden window-1-tahun yang sudah ditutup lebih dulu.

**n = 5 puncak + 4 bottom (3 final + 1 bottom-so-far), 3–4 cycle;** band baru valid sejak 2014-07-16 sehingga 2011 & 2013 tidak tercakup.

Yang layak diingat dari sini: band = transformasi monoton dari Price/RP dan **invarian terhadap penskalaan base RP** — temuan mekanis yang berlaku juga untuk versi Matt.
