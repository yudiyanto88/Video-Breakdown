# Validasi: Severity Dip di Bawah Realized Price Mengecil Tiap Cycle

**Sumber:** "EVERYONE Expects Bitcoin To Break This Line, It's Held 99% Of The Time" — Bitcoin Magazine Pro, 2026-07-09
**Script:** `analyze_rp_dip_severity.py`
**Events pendukung:** `events_rp_dip_severity.csv`
**Tanggal validasi:** 2026-07-28

---

## Klaim yang diuji

Magnitude/severity dip harga BTC di bawah realized price (dalam %, bukan USD nominal) mengecil tiap cycle secara monoton -- argumen: makin banyak lost/locked supply di harga tinggi -> severity dip berkurang.

## Definisi event

- Satu "dip event" = periode kontinu BTC price cross-under realized_price sampai cross-back-over berikutnya. Segmen kontinu yang jaraknya <30 hari di-merge (cooldown) supaya tidak overcount micro-whipsaw sebagai event terpisah.
- Severity = `(realized_price_at_min - btc_price_min) / realized_price_at_min`, dihitung memakai realized_price PADA TANGGAL btc_price minimum tsb (at-gate, bukan lookahead dari luar window).
- Raw (tanpa filter cycle) menghasilkan **10 event** (termasuk beberapa micro-dip 0-1 hari di awal data 2010-2012 yang bukan bear market sungguhan, dan COVID crash 2020 yang exogenous/bukan cycle top-bottom penuh).

## Hasil — View mentah (semua 10 event, termasuk noise)

| Tanggal min | Severity % | Durasi (hari) |
|---|---|---|
| 2010-07-17 | 0.00% | 0 (awal data, bukan event nyata) |
| 2011-08-06 | 4.96% | 0 (micro whipsaw) |
| 2011-11-18 | 58.84% | 116 |
| 2012-02-18 | 15.60% | 56 |
| 2012-05-10 | 0.83% | 0 (micro whipsaw) |
| 2014-10-05 | 8.57% | 32 |
| 2015-01-14 | 43.23% | 311 |
| 2018-12-14 | 29.75% | 133 |
| 2020-03-12 (COVID) | 15.10% | 6 |
| 2022-11-21 | 22.34% | 213 |

**View mentah TIDAK monoton** — banyak whipsaw kecil & satu event exogenous (COVID) mengacaukan urutan.

## Hasil — View utama (severity MAKSIMUM per cycle bull-bear PENUH, n=4)

Karena beberapa "event" di atas adalah secondary bounce dalam cycle bear yang sama (misal 2012-02-18 adalah gelombang kedua dari bear market 2011-2012), diambil severity TERDALAM per cycle penuh:

| Cycle | Tanggal trough | Severity % |
|---|---|---|
| 2011-12 | 2011-11-18 | 58.84% |
| 2014-16 | 2015-01-14 | 43.23% |
| 2018-19 | 2018-12-14 | 29.75% |
| 2022-23 | 2022-11-21 | 22.34% |

Selisih berurutan: -15.62, -13.47, -7.41 -- **semua negatif, monoton mengecil.**

COVID 2020-03 (severity 15.10%, hanya 6 hari) DIKELUARKAN dari view utama karena bukan cycle top-to-bottom penuh (exogenous shock, recovery <1 bulan, bukan bear market terminal yang menentukan siklus). Kalau dimasukkan sebagai titik tersendiri di antara 2018-19 dan 2022-23, urutan jadi 29.75 -> 15.10 -> 22.34 (naik lagi) -- BUKAN monoton.

## Catatan penting: bukan bukti independen dari Topik 2

Severity = `1 - MVRV_ratio` pada titik trough. Ini **secara matematis identik** dengan temuan Topik 2 (trough MVRV naik monoton: 0.401 -> 0.568 -> 0.702 -> 0.760, yang setara dengan severity 59.9% -> 43.2% -> 29.8% -> 24.0%, sangat dekat dengan hasil independen kami 58.84/43.23/29.75/22.34 -- selisih kecil karena window boundary sedikit berbeda). Jadi Topik 2 dan Topik 3 BUKAN dua bukti independen yang saling menguatkan — keduanya adalah reframing unit yang sama dari satu pola dasar.

## Verdict

**SUPPORTED secara deskriptif — TAPI HANYA kalau membatasi definisi ke "severity maksimum per cycle bull-bear penuh" (n=4) dan mengeluarkan micro-whipsaw serta shock exogenous (COVID) dari perhitungan.**

- Dengan definisi granular "setiap cross-under/cross-over adalah event terpisah" (n=10, termasuk noise), pola TIDAK monoton -- ada whipsaw kecil dan COVID yang mengacaukan urutan.
- Dengan definisi "trough terdalam per cycle penuh" (n=4), pola konsisten monoton mengecil.
- **n=4 adalah sample yang sangat kecil** (sama seperti Topik 1 & 2) — 4 cycle bear market lengkap yang tersedia sepanjang sejarah BTC. Tidak cukup untuk memastikan pola ini akan berlanjut, hanya cukup untuk bilang "cenderung" konsisten dengan argumen struktural (lost/locked supply makin banyak di harga tinggi).
- Perlu ditekankan lagi: temuan ini SECARA MATEMATIS sama dengan Topik 2 (trough MVRV naik = severity mengecil), bukan konfirmasi independen tambahan.

**n & sebaran:** 4 cycle bull-bear penuh (2011-12, 2014-16, 2018-19, 2022-23), 1 titik severity per cycle. COVID 2020 (n tambahan, dikeluarkan dari view utama karena bukan cycle penuh) dicatat terpisah sebagai footnote.
