# Findings: CAGR Realized Price — klaim 38% historis vs 0-8% saat ini

**Sumber klaim:** video Bitcoin Magazine Pro, 2026-07-13. Pembicara: CAGR realized price historis rata-rata ~38% (nilai proyeksi model best-fit-nya), sedangkan saat ini (real, bukan proyeksi) hanya sekitar 0-8%, karena harga setahun lalu mirip harga sekarang.

## Definisi
Rolling 1-year growth rate: `CAGR_365(t) = RP(t) / RP(t-365d) − 1` (window persis 1 tahun, tidak perlu pemangkatan tambahan). Dihitung dari `realized_price` (data_price_level.csv), full history 2011-07-17 s/d 2026-07-15.

## Hasil

Seluruh histori (n=5478 hari): mean **556.7%** (sangat terdistorsi outlier awal), median **48.2%**.

Breakdown per cycle (halving-to-halving):
| Cycle | n | mean | median | min | max |
|---|---|---|---|---|---|
| 2010-2012 | 500 | 3743.6% | 1433.0% | -31.6% | 14542.0% |
| 2012-2016 | 1319 | 566.6% | 73.5% | -22.1% | 3792.8% |
| 2016-2020 | 1402 | 212.6% | 45.9% | -20.1% | 1123.2% |
| 2020-2024 | 1440 | 62.3% | 15.2% | -19.8% | 253.7% |
| 2024-now | 817 | 52.0% | 55.1% | 5.9% | 87.5% |

Pooled post-2012-halving (mengikuti pendekatan pembicara sendiri yang fit dari 2012 halving): n=4978, mean=236.5% (masih terdistorsi outlier 2013), **median=44.1%** — cukup dekat dengan klaim "~38%" (order-of-magnitude match, meski bukan angka persis).

**Nilai saat ini (data terakhir 2026-07-15): CAGR = 5.92%** — cocok dengan klaim "0-8%".
Verifikasi klaim "harga setahun lalu mirip sekarang": RP(2026-07-15)=$52,740 vs RP(2025-07-15)=$49,792 (growth 5.92%) — RP memang tumbuh tipis. Sebagai konteks tambahan, btc_price sendiri malah TURUN -44.7% YoY (65,098 vs 117,747) — RP jauh lebih stabil daripada price karena efek smoothing/lag realized cap.

## Cek Standar Validasi
1. **Definisi event**: bukan event diskrit, deret waktu kontinu — dilaporkan sbg rata-rata & sebaran per cycle. ✓
2. **n dilaporkan**: n=5478 hari full-history, breakdown n per cycle 500-1440 hari. ✓
3. **Anti-lookahead**: CAGR_365(t) hanya pakai RP(t) & RP(t-365d), keduanya ≤t — valid at-gate. ✓
4. **Independensi**: rolling 365d window sangat overlap/otokorelasi — makanya dilaporkan per-cycle rata-rata, bukan n hari mentah sbg n independen. Rata-rata per cycle didominasi oleh level harga masing-masing cycle (bukan random sample).
5. **Data mulai belakangan**: tidak berlaku (realized_price full history sejak 2010).
6. **Overfit**: murni deskriptif, tidak ada threshold yang di-fit.

## Verdict
Klaim "historis rata-rata ~38%" **partial-match**: MEAN gabungan (556.7%) jauh di atas 38% karena didominasi outlier awal 2010-2012 (yang diakui sendiri pembicara "very influential, skewed"); tapi MEDIAN per-cycle (44-74% untuk cycle 2012-2020, turun ke 15% di 2020-2024, naik lagi ke 55% di cycle saat ini) dan median pooled post-2012 (44.1%) berada di **order-of-magnitude yang sama** dengan 38% — cukup masuk akal sebagai estimasi kasar, meski tidak presisi. Klaim "saat ini 0-8%" **terverifikasi kuat**: nilai aktual 5.92% tepat di tengah rentang itu, dan penyebabnya (RP setahun lalu ≈ RP sekarang) juga terverifikasi.

**[VALIDASI — 2026-07-29, CLOSED]** CAGR Realized Price saat ini (5.92%, data 2026-07-15) match dengan klaim "0-8%" — terverifikasi kuat, n=1 titik data terakhir tapi didukung tren 90 hari (5.9-23.8%, mean 15.6%) yang konsisten arah turun. Klaim "rata-rata historis ~38%" cuma partial-match: median per-cycle (n=500-1440 hari/cycle) berkisar 15-74%, dan median pooled post-2012-halving 44.1% — dalam order-of-magnitude yang sama dengan 38% tapi tidak presisi; MEAN gabungan (556.7%) sangat menyesatkan karena didominasi outlier 2010-2012 (harus dibuang/di-median-kan, bukan dirata-ratakan mentah).
