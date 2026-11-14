# Validasi: Support band touch = bottom signal ("excellent accumulation")

**Insight diuji:** [STRATEGI] Harga di dalam/di bawah band Support = periode akumulasi bagus (bottom signal) — klaim eksplisit teks post, didukung visual 4 titik historis di Gambar 1.

**Tanggal validasi:** 2026-07-29
**Script:** `analyze_volatility_channel_support_bottom.py`
**Data event:** `events_volatility_channel_support_bottom.csv`

---

## Definisi kerja (eksplisit, wajib karena vendor tidak publikasikan formula)

Vendor ("INVESTE MAIS") tidak menjelaskan formula matematis pasti dari "Bitcoin Volatility Channel" — hanya deskripsi kualitatif ("central price average... calculated based on annualized realized volatility, 365-day window"). Untuk menguji klaim, band direkonstruksi sebagai berikut (best-effort reconstruction, BUKAN replikasi formula asli vendor):

- **Centerline** (proxy "Fair Value"): `center = exp(rolling_mean(log(btc_price), W))` — window W dicoba di 365, 730, dan 1095 hari
- **Band width**: `support/resistance = center × exp(∓k · σ365)`, dengan σ365 = annualized realized volatility dari log-return harian rolling 365 hari
- **Kalibrasi**: k dan W dipilih dengan mencocokkan ke SATU snapshot chart (~2026-07-15: Fair Value≈$66.690, Support≈$53.678, Resistance≈$82.860) — ini kalibrasi post-hoc terhadap satu titik data, bukan formula tervalidasi independen. k=0.5 mereproduksi rasio Support/Resistance-ke-Center paling dekat; window 365/730 hari (sesuai deskripsi vendor "365-day") ternyata **overshoot level centerline 28-30%** dari snapshot chart — hanya window ~3 tahun (1095 hari) yang cocok levelnya (+2,9%). Ini indikasi kuat bahwa "365-day" di teks vendor kemungkinan merujuk ke window volatility, bukan window centerline — atau formula sesungguhnya berbeda dari rekonstruksi ini.
- **Event**: harga close di bawah garis Support, dengan cooldown 30 hari antar-event (event baru hanya dihitung kalau ≥30 hari dari event tercatat sebelumnya, supaya tidak menghitung ulang noise harian di sekitar band yang sama)
- **Reversal window**: 180 hari — event dianggap "clean reversal" kalau harga naik balik melewati centerline dalam ≤180 hari sejak event tanpa turun lebih dalam dulu; "false-start-then-reversal" kalau turun lebih dalam dulu baru reversal; "no reversal" kalau belum reversal sampai akhir data. Event dari 2025-2026 yang belum genap 180 hari sejak tanggal event **di-censor** (tidak dihitung sebagai "gagal", karena outcome-nya belum bisa diketahui)

## Hasil

| Config | n total | Sebaran per cycle (2013-15 / 2018-19 / 2020 / 2022 / 2025-26) | n resolved (non-censored) | Clean reversal | False-start-then-reversal | No reversal |
|---|---|---|---|---|---|---|
| W365, k0.5 | 26 | 6 / 5 / 1 / 9 / 5 | 21 (5 censored) | 9,5% (2/21) | 47,6% (10/21) | 42,9% (9/21) |
| W730, k0.5 | 18 | 5 / 0 / 0 / 9 / 4 | 14 (4 censored) | 7,1% (1/14) | 35,7% (5/14) | 57,1% (8/14) |
| W1095, k0.5 (best-fit level) | 2 | 0 / 0 / 0 / 2 / 0 | 2 (0 censored) | 0,0% | 100,0% (2/2) | 0,0% |

**Independensi sample:** siklus 2022 mendominasi (9 dari 26 event di config W365, dan 9 dari 18 di W730 — sekitar 35-50% dari total) — hasil TIDAK independen lintas cycle, banyak event 2022 kemungkinan adalah noise/re-touch dalam satu leg turun yang sama meski sudah difilter cooldown 30 hari.

## Verdict

Klaim "harga menyentuh/di bawah Support = excellent accumulation period" **tidak didukung** sebagai sinyal bottom yang reliable pada horizon 180 hari: pada config manapun, hanya 0-9,5% kejadian yang berujung "clean reversal" — mayoritas (36-58%) turun lebih dalam dulu sebelum akhirnya reversal (false start), atau bahkan belum reversal sama sekali. Config yang levelnya paling cocok dengan snapshot chart vendor (W1095) hanya punya n=2, keduanya false-start-then-reversal — bukan clean bottom signal.

4 titik yang di-highlight vendor di Gambar 1 (2014, 2018-19, 2019-20, 2021-22 & 2025-26) tampak **hindsight-picked** dari total 18-26 kejadian mekanis yang jauh lebih banyak sepanjang histori — vendor hanya menampilkan touch yang kebetulan diikuti pemulihan panjang, bukan representasi lengkap dari behavior band ini.

**Catatan metodologi:** hasil ini bergantung penuh pada rekonstruksi band yang tidak match persis dengan formula vendor asli (lihat overshoot 28-30% di atas) — hasil negatif ini kuat terlepas dari ketidakpastian formula, karena base rate reversal rendah konsisten di ketiga config W365/W730/W1095.

---

**[VALIDASI — 2026-07-29, CLOSED]** Rekonstruksi band (kalibrasi post-hoc ke satu snapshot chart) gagal mereproduksi level Fair Value vendor dengan window 365/730 hari (overshoot 28-30%), dan pada config manapun **hanya 0-9,5% kejadian "harga di bawah Support" (n=0-2 dari 2-21 event resolved, didominasi siklus 2022 ~35-50% dari total) diikuti reversal bersih dalam 180 hari** — mayoritas false-start atau belum reversal. Klaim "excellent accumulation" tidak didukung sebagai sinyal bottom reliable pada horizon 180 hari; hasil negatif, konsisten di semua config yang dicoba.
