# Findings — Cohort 6m-12m Realized Price ("top buyers capitulating")

**Tanggal validasi:** 4 Agustus 2026
**Script:** `analyze_cohort_6m12m_realized_price.py`
**Event table:** `events_cohort_6m12m_realized_price.csv`
**Data:** `data_master_all_metrics.csv` (2010-07-17 s/d 2026-07-15, n = 5.843 hari)

---

## Ringkasan sederhana

Klaim video soal **durasi** cukup akurat: kohort 6m-12m memang cenderung underwater 13-15 bulan di tiga bear terakhir. Tapi klaim yang paling berharga buat kita — bahwa momen flip "menandai resumsi bull market" — **tidak lolos** sebagai alat baru. Flip-nya cenderung datang **belakangan**, bukan mendahului unlock struktural framework. Metrik ini berguna sebagai *penanda durasi/konteks*, bukan sebagai *sinyal timing*.

⚠️ **Peringatan metodologis wajib:** ini **rekonstruksi dari HODL-wave band**, BUKAN seri realized-price kohort resmi Glassnode. Angka absolutnya bisa berbeda dari yang ditampilkan On-Chain Mind. Formula:

```
cohort_RP = (realized_cap_6m-12m% x realized_cap_usd) / (supply_6m-12m% x total_supply_btc)
```

---

## Sanity gate (sebelum analisis lanjut) — LULUS

| Cek | Hasil |
|-----|-------|
| Rasio coh_RP / RP per 2026-07-01 | **1,901x** (target claim-tester ~1,90x) — cocok |
| coh_RP > RP di peak+9 bulan, semua cycle | 2,54x / 1,77x / 2,13x / 2,37x / 1,90x — **5/5 OK** |
| Episode underwater terakhir mulai ~Nov 2025 @ ~$95.000 | **2025-11-14 @ $94.668** (coh_RP $94.693) — cocok |

Temuan saat gate: band 6m-12m itu **rolling**. Pembeli puncak baru masuk band ini 6-12 bulan **setelah** peak, jadi cek coh_RP>RP harus di peak+9 bulan, bukan di awal bear. Di awal bear (misal Feb 2018) band ini justru berisi pembeli *murah* dari fase awal bull sehingga coh_RP < RP — itu perilaku normal, bukan kegagalan rekonstruksi.

---

## Definisi event (dikunci sebelum menghitung)

- **Start episode:** hari pertama `btc_price < cohort_RP` setelah ≥90 hari berturut di atasnya
- **Flip (end):** hari pertama `btc_price > cohort_RP` yang bertahan ≥14 hari berturut. **Anti-lookahead:** tanggal flip baru *diketahui* 13 hari kemudian — lead/lag dilaporkan untuk versi mentah DAN versi terkonfirmasi
- **Unlock struktural:** hari pertama `sth_cost_basis > realized_price` setelah ≥30 hari berturut inversi. At-gate (tanpa data masa depan) dan mereproduksi **persis n=4 unlock** dari validasi 200D-MA CLOSED: 2012-04-19, 2015-11-03, 2019-05-07, 2023-03-01
- **Matching episode→unlock:** unlock pertama dalam window [start episode, flip + 365 hari]

---

## Hipotesis A — "underwater rata-rata 13 bulan" → SEBAGIAN BENAR

**n = 6 episode total** (5 selesai + 1 berjalan). Sebaran per cycle:

| Ep | Konteks | Start | Flip | Durasi | Terdalam di bawah coh_RP |
|----|---------|-------|------|--------|--------------------------|
| 1 | 2011 bear | 2011-12-02 @ $3,11 | 2012-06-29 | 210 hari (6,9 bln) | -65,0% |
| 2 | 2014-15 bear | 2014-07-29 @ $583 | 2015-10-25 | **453 hari (14,9 bln)** | -70,9% |
| 3 | 2018-19 bear | 2018-06-13 @ $6.350 | 2019-05-11 | **332 hari (10,9 bln)** | -69,4% |
| 4 | 2020 COVID | 2020-02-28 @ $8.704 | 2020-07-06 | 129 hari (4,2 bln) | -46,6% |
| 5 | 2022-23 bear | 2021-12-31 @ $46.234 | 2023-03-23 | **447 hari (14,7 bln)** | -64,7% |
| 6 | 2025-26 (berjalan) | 2025-11-14 @ $94.668 | ONGOING | 243 hari per 2026-07-15 | -42,1% |

**Subset "3 bear terakhir" seperti maksud video (ep 2, 3, 5; n=3):** mean = **411 hari = 13,5 bulan** → klaim "13 bulan" **cocok**. Tapi **spread 121 hari (4,0 bulan)**: 10,9 / 14,7 / 14,9 bulan. "13 bulan" itu rata-rata tiga titik yang tidak berdekatan, bukan pola ketat.

**Catatan rigor:** **n efektif = 3**. Episode 1 (2011) dari era supply-band tipis → flag low-reliability. Episode 4 (2020 COVID) **bukan** cycle bear — video tidak menghitungnya, tapi mesin event tetap menangkapnya (artinya flip mentah punya false positive). Episode 6 **censored**.

### Proyeksi "Desember 2026" — rentang sebenarnya jauh lebih lebar

Dari start 2025-11-14:

| Basis | Implied flip |
|-------|--------------|
| mean 3 bear (411 hari) | **2026-12-29** |
| rentang 3 bear (332-453 hari) | **2026-10-12 s/d 2027-02-10** |
| rentang semua episode (129-453 hari) | 2026-03-23 s/d 2027-02-10 |

Proyeksi video (~Des 2026) jatuh persis di titik mean — tapi rentang jujurnya **Okt 2026 – Feb 2027**. Perlakukan "Desember 2026" sebagai titik tengah, bukan target.

---

## Hipotesis B (paling penting) — "flip = leading marker resumsi bull" → TIDAK LOLOS

**n = 4 pasangan flip↔unlock.** Positif = flip mendahului unlock.

| Ep | Cycle | Flip | Flip terkonfirmasi | Unlock | Selisih (mentah) | Selisih (terkonfirmasi) |
|----|-------|------|--------------------|--------|------------------|--------------------------|
| 1 | 2011 | 2012-06-29 | 2012-07-12 | 2012-04-19 | **-71 hari** | -84 hari |
| 2 | 2014-15 | 2015-10-25 | 2015-11-07 | 2015-11-03 | **+9 hari** | -4 hari |
| 3 | 2018-19 | 2019-05-11 | 2019-05-24 | 2019-05-07 | **-4 hari** | -17 hari |
| 5 | 2022-23 | 2023-03-23 | 2023-04-05 | 2023-03-01 | **-22 hari** | -35 hari |
| 4 | 2020 COVID | 2020-07-06 | 2020-07-19 | **TIDAK ADA** | – | – |

- Versi mentah: median **-13 hari**, mean -22 hari, hanya **1 dari 4** positif
- Versi terkonfirmasi (yang realistis dipakai live): median **-26 hari**, **0 dari 4** positif
- **Pembanding:** 200D MA reclaim mendahului unlock **+23 s/d +51 hari, konsisten 4/4** (validasi CLOSED 2026-07-28)

**Verdict:** flip kohort 6m-12m cenderung **coincident-to-lagging** terhadap unlock struktural, tidak leading. Tidak menambah lead time di atas yang sudah kita punya, dan kalah dari 200D MA reclaim. Episode 4 (2020) malah menyalakan flip di periode yang framework tidak pernah sebut bear.

---

## Hipotesis C — "flip diikuti return kuat" → EDGE TIPIS, n terlalu kecil

| Horizon | Median return dari flip (n=5) | **Baseline tanpa syarat** | Tanpa ep1 2012 (n=4) |
|---------|-------------------------------|---------------------------|----------------------|
| 90 hari | +35,8% | **+13,3%** (n=5.753, 61% positif) | +25,0% |
| 180 hari | +57,6% | **+37,2%** (n=5.663, 66% positif) | +43,3% |
| 365 hari | +130,8% | **+99,7%** (n=5.478, 74% positif) | +127,9% |

Median di atas baseline di semua horizon, tapi **n = 5 (efektif 4)** terlalu kecil untuk memisahkan edge nyata dari noise. Selisih di 365 hari cuma ~30 poin persen di atas baseline BTC yang memang trennya naik. Return 1.326% di ep1 (2012) mendominasi mean — sudah dikeluarkan di kolom terakhir. Lima flip datang dari lima cycle berbeda, jadi independensi relatif OK, tapi jumlahnya tetap lima.

---

## Verdict akhir

**PARTIAL — durasi terkonfirmasi, nilai sebagai sinyal DITOLAK.**

Rekonstruksi lolos sanity gate (rasio 1,90x, episode terakhir mulai 2025-11-14 @ $94.668 — persis klaim video). Durasi 3 bear terakhir mean 13,5 bulan mendekati klaim "13 bulan", **tapi n=3 dengan spread 4 bulan** (10,9-14,9). Klaim inti — flip menandai resumsi bull — **tidak lolos**: di **n=4** pasangan, flip cenderung **terlambat** dari unlock struktural (median -13 hari mentah, -26 hari versi terkonfirmasi; 0/4 leading di versi yang realistis dipakai live), sementara 200D MA reclaim mendahului unlock 23-51 hari konsisten 4/4.

**Rekomendasi:** pakai cohort 6m-12m RP sebagai **kalender/konteks** (berapa lama lagi tekanan supply top-buyer ini ada) — bukan trigger. Untuk transisi K4→K5, framework tetap lebih baik dilayani 200D MA reclaim. Celah resolusi di dalam LTH cohort **belum** terisi.

**Konteks saat ini (2026-07-15):** episode berjalan sudah 243 hari (8,0 bulan), harga $65.098 vs cohort_RP $99.727 (-34,7% di bawah). Kalau pola 3 bear terakhir berulang, flip cenderung jatuh antara **Okt 2026 dan Feb 2027**.
