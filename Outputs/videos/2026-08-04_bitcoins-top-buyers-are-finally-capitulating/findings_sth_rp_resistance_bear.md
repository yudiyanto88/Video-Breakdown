# Findings — STH RP sebagai Resistance di Bear Market (kalibrasi Signal D)

**Tanggal validasi:** 4 Agustus 2026
**Script:** `analyze_sth_rp_resistance_bear.py`
**Event table:** `events_sth_rp_resistance_bear.csv`
**Data:** `data_master_all_metrics.csv` (2010-07-17 s/d 2026-07-15, n = 5.843 hari)

---

## Ringkasan sederhana

Klaim video **terkonfirmasi kuat**, dan hasilnya langsung mengkalibrasi Signal D. Dari 13 kali harga rally balik menyentuh STH RP dari bawah selama bear market, 8 kali "berhasil break" menurut definisi Signal D (close di atas STH RP ≥3 hari) — **tapi 7 dari 8 break itu balik ke bawah lagi dalam 90 hari, dan cuma 1 dari 8 yang benar-benar diikuti unlock struktural.** Artinya Signal D dalam bentuknya sekarang punya **hit rate ~12%** sebagai penanda pembalikan asli.

---

## Definisi event (dikunci sebelum menghitung)

- **Bear window:** cycle peak → tanggal unlock struktural. Cycle 2025-26 **BERJALAN / CENSORED** (unlock belum terjadi):
  - 2011: 2011-06-08 → 2012-04-19 (316 hari)
  - 2013: 2013-11-29 → 2015-11-03 (704 hari)
  - 2017: 2017-12-16 → 2019-05-07 (507 hari)
  - 2021: 2021-11-08 → 2023-03-01 (478 hari)
  - 2025: 2025-10-06 → 2026-07-15 (282 hari, censored)
- **Event "sentuhan dari bawah":** hari pertama `btc_price >= 98% x sth_cost_basis` setelah ≥30 hari berturut di bawah 98%. Cooldown 30 hari
- **Outcome (window 30 hari sesudah, at-gate):** "BREAK" kalau ada ≥3 hari berturut close di atas `sth_cost_basis` (**persis Signal D**). Selain itu "DITOLAK"
- **Sub-uji:** dari event BREAK, berapa diikuti unlock struktural dalam 90 hari
- **Tambahan:** dari event BREAK, berapa yang harganya balik ke bawah STH RP dalam 90 hari

---

## Hasil utama — hit rate

**n total = 13 event | BREAK = 8 (62%) | DITOLAK = 5 (38%)**

Sebaran per cycle:

| Cycle | BREAK | DITOLAK |
|-------|-------|---------|
| 2011 | 1 | 0 |
| 2013 | 3 | 0 |
| 2017 | 1 | 3 |
| 2021 | 2 | 1 |
| 2025 (censored) | 1 | 1 |

⚠️ **Independensi:** event dalam satu cycle berkorelasi (bear yang sama). **Jumlah bear independen = 5, bukan 13.** Hasil 2013 (3 BREAK, 0 DITOLAK) dan 2017 (1 BREAK, 3 DITOLAK) saling berlawanan arah — tidak ada satu cycle yang mendominasi kesimpulan akhir, tapi sample-nya tetap kecil.

**Tabel event lengkap:**

| Cycle | Tanggal event | Harga | STH RP | % dari STH RP | Outcome | Max hari berturut di atas | DD 30d | Ret 30d |
|-------|---------------|-------|--------|---------------|---------|---------------------------|--------|---------|
| 2011 | 2011-12-31 | $4,71 | $4,43 | 106,2% | BREAK | 31 | 0,0% | +16,7% |
| 2013 | 2014-05-30 | $621 | $603 | 102,9% | BREAK | 13 | -8,7% | -3,2% |
| 2013 | 2015-03-09 | $290 | $291 | 100,0% | BREAK | 3 | -16,4% | -15,5% |
| 2013 | 2015-06-16 | $252 | $245 | 102,7% | BREAK | 20 | -4,7% | +10,7% |
| 2017 | 2018-07-24 | $8.385 | $8.004 | 104,8% | BREAK | 4 | -26,3% | -22,1% |
| 2017 | 2018-09-01 | $7.184 | $7.309 | 98,3% | DITOLAK | 1 | -12,5% | -8,0% |
| 2017 | 2018-11-07 | $6.550 | $6.633 | 98,7% | DITOLAK | 0 | **-47,4%** | -47,4% |
| 2017 | 2019-02-23 | $4.154 | $4.230 | 98,2% | DITOLAK | 1 | -8,7% | -4,3% |
| 2021 | 2022-03-27 | $46.829 | $46.323 | 101,1% | BREAK | 4 | -18,6% | -18,6% |
| 2021 | 2022-10-29 | $20.808 | $21.192 | 98,2% | DITOLAK | 2 | -24,2% | -22,1% |
| 2021 | 2023-01-11 | $17.938 | $17.829 | 100,6% | BREAK | 31 | 0,0% | +20,6% |
| 2025 | 2026-01-14 | $96.918 | $98.346 | 98,5% | DITOLAK | 0 | -35,2% | -29,0% |
| 2025 | 2026-04-26 | $78.674 | $79.288 | 99,2% | BREAK | 12 | -3,7% | -3,6% |

---

## Biaya salah baca rally ini

- **Event DITOLAK (n=5):** drawdown 30 hari **median -24,2%** (rentang -8,7% s/d **-47,4%**), return 30 hari median **-22,1%**
- **Event BREAK (n=8):** drawdown 30 hari median -6,7%, return 30 hari median -3,4%

Bahkan yang "berhasil break" pun median return 30 harinya masih **negatif**. Jadi rally balik ke STH RP di bear market cenderung mahal untuk dikejar, apapun outcome-nya.

---

## Sub-pertanyaan (yang membedakan reversal asli dari resistance-rally)

| Cycle | Event | Break date | Unlock ≤90d? | Hari break → unlock berikutnya | Balik ke bawah STH RP ≤90d? |
|-------|-------|-----------|----------------|-------------------------------|------------------------------|
| 2011 | 2011-12-31 | 2012-01-02 | TIDAK | 108 | Ya |
| 2013 | 2014-05-30 | 2014-06-01 | TIDAK | 520 | Ya |
| 2013 | 2015-03-09 | 2015-03-12 | TIDAK | 236 | Ya |
| 2013 | 2015-06-16 | 2015-06-18 | TIDAK | 138 | Ya |
| 2017 | 2018-07-24 | 2018-07-29 | TIDAK | 282 | Ya |
| 2021 | 2022-03-27 | 2022-03-29 | TIDAK | 337 | Ya |
| 2021 | **2023-01-11** | **2023-01-13** | **2023-03-01** | **47** | **Tidak** |
| 2025 | 2026-04-26 | 2026-05-06 | TIDAK | (belum ada) | Ya |

- **BREAK diikuti unlock ≤90 hari: 1 dari 8 (12%)**
- **BREAK yang harganya balik ke bawah STH RP dalam 90 hari: 7 dari 8 (88%)**
- Satu-satunya break "asli" = **2023-01-11** (bear 2022-23), yang tidak pernah kembali ke bawah STH RP dan diikuti unlock 47 hari kemudian
- Break 2011-12-31 dan 2015-06-16 sempat bertahan lama (31 dan 20 hari di atas) tapi tetap balik ke bawah — **durasi streak saja bukan pembeda yang andal**

---

## Verdict akhir

**KONFIRMASI KUAT untuk klaim video, dan PERINGATAN untuk Signal D.**

Di **n=13 event** yang tersebar di **5 bear (2011:1, 2013:3, 2017:4, 2021:3, 2025:2 — cycle 2025 masih berjalan/censored)**, rally yang menyentuh STH RP dari bawah selama bear market cenderung **berperilaku sebagai resistance**: median return 30 hari negatif di kedua kelompok, dan yang ditolak menderita **drawdown median -24,2%** dalam 30 hari.

Yang paling penting untuk framework: **Signal D dalam bentuk sekarang (harga > STH RP ≥3 hari) menyala 8 kali di bear market, tapi hanya 1 dari 8 (12%) yang benar-benar mendahului unlock struktural dalam 90 hari — 7 dari 8 (88%) harganya balik ke bawah STH RP dalam 90 hari.** Ini konsisten dengan `Price_Level_knowledge_base v1.4.md` § 6.3 yang sudah mencatat STH RP sebagai level paling rawan false signal.

**Rekomendasi (usulan, bukan penerapan):** Signal D sebaiknya **tidak dipakai sendirian** untuk wrap-up K4 → Z1b. Kandidat penguat yang datanya sudah ada dan sudah tervalidasi: pasangkan dengan **200D MA reclaim** (lead 23-51 hari ke unlock, 4/4, CLOSED 2026-07-28), atau naikkan syarat persistensi jauh di atas 3 hari. Catatan: menaikkan persistensi saja **tidak cukup** — break 31 hari (2011) dan 20 hari (2015) tetap gagal.

**Konteks sekarang:** event terakhir 2026-04-26 dinilai BREAK (12 hari berturut di atas STH RP) tapi harga sudah balik ke bawah dan per 2026-07-15 ada di $65.098 vs STH RP $67.143. Berdasarkan basis rate di atas, itu cenderung masuk kategori resistance-rally (kelompok 7-dari-8), bukan reversal.
