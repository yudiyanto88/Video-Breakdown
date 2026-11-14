# Findings: Dynamic LTH classification (multi age-band) vs fixed 155-day cutoff

**Sumber klaim:** video "Mathematically Modelling The Future Of Bitcoin" (Bitcoin Magazine Pro, 2026-07-13), merujuk paper pembicara sendiri "Dynamic Long-Term Holder Classification for Bitcoin" — memakai age band 0-30d, 30-90d, ..., 730d+ untuk realized price, bukan satu cutoff tetap 155 hari yang dipakai framework kita untuk STH/LTH split.

## Pertanyaan
Apakah pindah cutoff STH/LTH split dari 155 hari (fixed) ke boundary alternatif (<90d, <180d, <270d) menggeser secara material tanggal *crossing* STH RP ↔ RP — titik transisi struktur N↔T yang jadi gerbang K5/Z2 di Decision Framework v2?

## Definisi event
- **Crossing** = hari di mana tanda `(candidate_RP − RP_full)` berubah dan bertahan ≥5 hari berturut (anti one-day noise).
- Dicocokkan ke event crossing "official" (155d, dari `sth_cost_basis`) dengan window toleransi ±180 hari, arah (UP/DOWN) harus sama.
- **Catatan unit data penting** (bug ditemukan & diperbaiki saat menulis script): `supply_<band>` dan `realized_cap_<band>` di `data_hodl_waves.csv` adalah **persentase** (dari total supply/realized cap), bukan nilai absolut BTC/USD. Harga rata-rata proxy dihitung: `price_subset = RP_full × (Σcap_pct_subset / Σsupply_pct_subset)`.
- **Proxy <270 hari**: age-band data kita berhenti tepat di 90d/180d/365d (bin `3m-6m`, `6m-12m`). Tidak ada boundary asli di 270 hari — dipakai interpolasi linear (asumsi supply/realized-cap terdistribusi merata per-hari di dalam bin 180-365d, ambil 48.6% proporsinya). Ini **asumsi kasar**, bukan data asli — hasil untuk <270d dibaca lower-confidence dibanding <90d/<180d.

## Hasil
n = 9 tanggal crossing "official" (155d) sepanjang histori 2010-2026:
- 1 crossing di 2010-07-18 (artefak awal dataset, bukan regime transition nyata)
- 4 pasang DOWN→UP mewakili **4 siklus bear-bottom berbeda**: 2011-12/2012-04, 2015-02/2015-11, 2019-01/2019-05, 2022-11/2023-03

| Cutoff | n matched | mean offset | median offset | max abs offset |
|---|---|---|---|---|
| <90 hari | 9/9 | -27.7 hari (lebih awal) | -22.0 hari | 57 hari |
| <180 hari | 9/9 | +13.0 hari (lebih lambat) | +10.0 hari | 50 hari |
| <270 hari (interpolasi) | 3/9 | +42.3 hari | +1.0 hari | 126 hari |

Arah pergeseran konsisten dengan intuisi: cutoff lebih pendek (<90d) → cost basis kohort lebih reaktif ke harga terkini → cross lebih dulu. Cutoff lebih panjang (<180d) → sedikit lebih lambat. Cutoff <270d (via interpolasi) paling tidak stabil: cuma 3 dari 9 event official yang punya padanan crossing — 6 event lain TIDAK terdeteksi sama sekali di seri <270d dalam window ±180 hari, mengindikasikan cutoff selebar ini menghaluskan sinyal sampai beberapa regime transition menghilang, bukan cuma bergeser.

## Cek Standar Validasi
1. **Definisi event eksplisit**: ✓
2. **n dilaporkan**: n=9 crossing dates, tapi hanya **~4 transisi regime independen** + 1 artefak dataset-start. **n kecil — flag rigor wajib.**
3. **Anti-lookahead**: ✓ semua proxy dari snapshot hari itu (hodl_waves end-of-day), tanpa revisi masa depan.
4. **Independensi sample**: pasangan DOWN/UP dari siklus sama BERKORELASI (1 regime transition = 2 crossing tercatat, bukan 2 kejadian independen). Hasil didominasi 4 episode bear-bottom 2011-2023.
5. **Data mulai belakangan**: tidak berlaku (hodl_waves full history sejak 2009).
6. **Overfit**: hanya 3 varian cutoff diuji (90d/180d/270d), sesuai yang eksplisit disebut klaim — tidak overfit.

## Verdict
Pergeseran cutoff STH/LTH dari 155 hari ke 90-180 hari cenderung menggeser tanggal transisi struktur N↔T sekitar 10-22 hari (median, max 57 hari) — kecil relatif terhadap skala waktu zone/K-node kita (bulan-tahun), jadi kemungkinan **low-impact** untuk keputusan zone-level. Cutoff 270 hari (proxy interpolasi kasar) berperilaku secara kualitatif berbeda — bukan cuma lebih lambat, tapi 6 dari 9 event bahkan tidak terdeteksi. Dengan n efektif hanya 4 episode regime terpisah, kesimpulan ini low-confidence — indikasi arah saja, bukan bukti kuat untuk mengubah cutoff 155-hari framework, tapi juga tidak memberi alasan kuat menggantinya.

**[VALIDASI — 2026-07-29, CLOSED]** Menggeser cutoff STH/LTH dari 155 hari ke 90-180 hari cenderung menggeser tanggal crossing STH RP↔RP sekitar 10-22 hari (median), dari n=9 tanggal crossing yang mewakili hanya **4 episode regime independen** (2011-12, 2015, 2019, 2022-23) — sample kecil, jadi ini indikasi arah, bukan bukti kuat. Cutoff 270 hari (proxy interpolasi, bukan boundary data asli) berperilaku secara kualitatif berbeda (6 dari 9 event tidak match sama sekali dalam window ±180 hari), tapi ini bukan perbandingan apple-to-apple karena asumsi interpolasi kasar. Kesimpulan: granularitas cutoff dalam rentang 90-180 hari kemungkinan low-impact untuk zone structure kita yang beroperasi di skala bulan-tahun — tidak ada alasan kuat untuk mengubah 155-hari fixed cutoff.
