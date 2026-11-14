# Findings: Akurasi quantile bands (P5/P95 MVRV Ratio) out-of-sample

**Sumber klaim:** video Bitcoin Magazine Pro, 2026-07-13. Quantile bands (persentil ke-5/ke-95 dari decaying MVRV trend lines) diklaim akurat "practically to perfection" sepanjang sejarah BTC, termasuk out-of-sample (training dibatasi ke 2015/2019/2023) — walau pembicara sendiri mengakui versi cutoff-2019 gagal menangkap tepat bear low 2022. Klaim lanjutan: "kita baru masuk persentil ke-5 terbawah historis... unbelievable discount territory."

## Proxy yang dipakai (bukan replikasi persis)
Bukan fungsi decay eksponensial pembicara — proxy: band persentil 5/95 dari `mvrv_ratio` mentah, di-fit HANYA dari data ≤ training cutoff (2015-01-01 / 2019-01-01 / 2023-01-01), lalu band itu **dipakai tetap** (tidak diupdate) untuk cek forward. Ini genuine out-of-sample test, sama semangat dengan yang diklaim pembicara — tapi mengukur MVRV ratio langsung, bukan garis trend harga yang decaying.

## Definisi event
Breach = 1 hari kalender di mana `mvrv_ratio` di luar band [P5,P95] hasil fit ≤cutoff. Episode breach dipisahkan pakai gap ≥14 hari non-breach (supaya 1 episode capitulation panjang tidak dihitung sebagai puluhan "kejadian" independen).

## Hasil

| Cutoff training | Band (P5,P95) | Forward n hari | Breach total | % breach | n episode |
|---|---|---|---|---|---|
| 2015-01-01 | (0.805, 4.467) | 4213 | 133 | 3.16% | 7 |
| 2019-01-01 | (0.790, 3.554) | 2752 | 35 | 1.27% | 5 |
| 2023-01-01 | (0.809, 3.346) | 1291 | 0 | 0.00% | 0 |

Breakdown per cycle (cutoff 2015): Cycle 2012-2016 breach 17.0% (n=554), 2016-2020 breach 2.3% (n=1402), 2020-2024 breach 0.5% (n=1440), 2024-now breach 0.0% (n=817).

Fokus bear low Okt-Des 2022: cutoff-2015 breach 7.6% (min mvrv_ratio=0.760 vs band_low 0.805 — SEDIKIT tembus di bawah band); cutoff-2019 breach 3.3% (min sama 0.760 vs band_low 0.790). Jadi memang ada tembus tipis di 2022, tapi kecil dan singkat (episode ~13-20 hari), bukan miss besar.

Fokus 2025-2026 (s/d data terakhir 2026-07-15): breach 0.0% di SEMUA cutoff. mvrv_ratio range 1.101–2.523, band_low di kisaran 0.79–0.82 — **jauh di atas** band bawah.

Baseline in-sample (full-history, tidak valid sbg test tapi buat konteks): P5=0.822, mvrv_ratio terakhir=1.234 — **TIDAK di bawah P5** in-sample sekalipun.

## Cek Standar Validasi
1. **Definisi event eksplisit**: ✓
2. **n dilaporkan**: n forward-days per cutoff 1291-4213 hari; n episode breach 0-7. Dilaporkan penuh di tabel.
3. **Anti-lookahead**: ✓ band dihitung SEKALI dari data ≤cutoff, tidak expanding lagi sesudahnya — genuine out-of-sample.
4. **Independensi**: breach hari berdekatan sangat berkorelasi — makanya dihitung juga n episode (bukan raw day-count) sebagai unit kejadian lebih independen.
5. **Data mulai belakangan**: tidak berlaku (mvrv_ratio full history sejak 2010).
6. **Overfit**: hanya 3 cutoff diuji (persis yang disebut pembicara sendiri di video) + 1 baseline in-sample sbg pembanding — tidak overfit.

## Verdict
Klaim umum "band jarang ditembus" punya dukungan: breach rate rendah (0-3.2%) di ketiga cutoff out-of-sample, dan breach yang ada mostly tipis & singkat (episode beberapa hari-minggu, bukan miss besar) — termasuk di bear low 2022 yang diakui sendiri oleh pembicara "gagal nail tepat". Ini KONSISTEN dengan klaim kualitatif ("cukup akurat"), tapi TIDAK sekuat "practically to perfection" — breach tetap terjadi tiap cycle, khususnya di cycle 2012-2016 (breach rate 17%, jauh lebih tinggi, karena training set masih tipis).

Namun klaim SPESIFIK terkini ("baru masuk persentil ke-5 terbawah historis, unbelievable discount") **TIDAK terverifikasi** oleh proxy raw-MVRV kita: di semua cutoff (2015/2019/2023) DAN baseline in-sample, mvrv_ratio saat ini (1.234, data 2026-07-15) berada NYAMAN DI DALAM band, jauh dari batas bawah (0.79-0.82). Catatan penting: ini proxy raw MVRV-ratio, BUKAN replikasi model decaying-trend-line pembicara — jadi tidak bisa membantah model dia secara langsung, hanya menunjukkan bahwa lensa persentil MVRV-mentah yang sederhana tidak menghasilkan sinyal "bottom 5%" yang sama.

**[VALIDASI — 2026-07-29, CLOSED]** Proxy percentile-band out-of-sample dari MVRV Ratio (bukan replikasi model decay pembicara) menunjukkan breach rate rendah (0-3.2%, n forward 1291-4213 hari per cutoff, 0-7 episode breach) — mendukung klaim kualitatif "band cukup akurat" secara umum, tapi TIDAK sekuat "practically to perfection" (cycle 2012-2016 breach 17%). Klaim spesifik "saat ini masuk persentil ke-5 terbawah / unbelievable discount" TIDAK terverifikasi: mvrv_ratio terakhir (1.234) jauh di atas band bawah (0.79-0.82) di semua cutoff & baseline in-sample. Perlu dicatat ini proxy raw-MVRV, bukan replikasi persis model decaying-trend pembicara.
