# Findings — Base rate hari per zona v2 & kapasitas sizing

**Insight yang diuji:** [BARU] Kalibrasi ukuran aksi ke base rate frekuensi sinyal (#21), sebagian #10 (linear ramp sizing)
**Sumber klaim:** Bitcoin Magazine Pro — "The FREE & SIMPLE Strategy That Beats Bitcoin (It Just Flashed Again)", 5 Agt 2026, lisan `[05:20]-[05:42]`
**Tanggal validasi:** 6 Agustus 2026
**Script:** [`analyze_zone_base_rate_sizing.py`](analyze_zone_base_rate_sizing.py)
**Event table:** [`events_zone_base_rate.csv`](events_zone_base_rate.csv)
**Data:** `data_master_all_metrics.csv`, baris terakhir **2026-07-15**

> ⚠ **Selisih tanggal:** data berakhir 2026-07-15, video terbit 2026-08-05 — selisih ~3 minggu.

---

## Klaim yang diuji

Prinsip desain dari video, `[05:20]-[05:42]`: *"about 12% of Bitcoin's days are in this sell region.
Over one in 10. There's quite a lot of time that you're going to be taking profit. So it doesn't want
to be a monumental amount."* Karena itu trim maksimum dikalibrasi cuma 0,75%/hari.

**Prinsipnya:** ukuran aksi per sinyal harus dikalibrasi ke seberapa sering sinyal itu nyala.

**Kenapa relevan.** Framework menetapkan sizing K1 (20-30% sekali), K4 (15/25/35% cash pool per bulan),
dan lantai waktu (5%/bulan) **tanpa referensi eksplisit ke base rate zona** — padahal angkanya ada
(Decision_Framework v2 menyebut Z5 = 703 hari historis).

Catatan claim-tester yang ikut diuji: prinsip ini masuk akal untuk aksi **kontinu/berulang** (K4, lantai
waktu), tapi **tidak otomatis berlaku ke K1** yang event-driven sekali jalan (~1 per cycle).

---

## Definisi

- Zona v2 dan `k4_count` **tidak dihitung ulang** — script meng-import `btlib.build_all()` (read-only)
  supaya identik dengan backtest established. Onchain-Dashboard tidak dimodifikasi
- Sampel efektif **2011-02-09 s/d 2026-07-15, n = 5.578 hari** (btlib membuang baris tanpa kolom AVIV)
- Lantai waktu disalin dari `opus_time_floor_validation.py`: lag 270 hari sejak cycle peak, kondisi
  close < RP, stop = Signal D (P > STH RP ≥3 hari). Versi **causal** (peak = running max) dihitung
  sebagai kontrol anti-lookahead

---

## (a) Base rate hari per zona v2

| Cycle | hari | ZC | ZD | Z1 | Z1b | Z2 | Z2t | Z3 | Z4 | Z5 |
|---|---|---|---|---|---|---|---|---|---|---|
| S0 pra-2013 *(supl.)* | 634 | 89 | 74 | 28 | 30 | 10 | 69 | 292 | 42 | 0 |
| S1 2013-2015 | 744 | 37 | 297 | 0 | 0 | 0 | 0 | 306 | 88 | 16 |
| S2 2015-2018 | 1.431 | 42 | 303 | 186 | 60 | 15 | 17 | 457 | 108 | 243 |
| S3 2018-2022 | 1.437 | 132 | 473 | 62 | 6 | 51 | 29 | 336 | 123 | 225 |
| S4 2022-now *(belum selesai)* | 1.332 | 0 | 477 | 50 | 2 | 28 | 34 | 278 | 244 | 219 |
| **TOTAL** | **5.578** | 300 | 1.624 | 326 | 98 | 104 | 149 | 1.669 | 605 | **703** |
| **% semua hari** | 100% | 5,4% | 29,1% | 5,8% | 1,8% | 1,9% | 2,7% | 29,9% | 10,8% | **12,6%** |

**Cek silang: Z5 = 703 hari — persis cocok** dengan angka yang tercantum di Decision_Framework v2 § 1.

**Base rate "sell region": Z5 = 12,6%** — praktis identik dengan klaim video "about 12% of Bitcoin's days
are in this sell region". (Z4 + Z5 = 23,4%.)

**Jumlah kunjungan** (blok kontinu) per zona sepanjang sejarah: Z5 **40** · Z4 98 · Z3 102 · ZD 103 ·
ZC 20 · Z1 **13** · Z1b 20 · Z2 **8** · Z2t 14.

---

## (b) Hari per level `k4_count` dan hari K4 benar-benar aktif

| Cycle | cnt0 | cnt1 | cnt2 | cnt3 | cnt4 | Z1 & cnt≥2 | noZ1 & cnt≥3 | **K4 aktif** | P/CVDD≤1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 *(supl.)* | 492 | 134 | 5 | 3 | 0 | 0 | 0 | **0** | 0 |
| S1 2013-2015 | 695 | 40 | 8 | 1 | 0 | 0 | 1 | **1** | 1 |
| S2 2015-2018 | 1.120 | 280 | 24 | 7 | 0 | 7 | 7 | **14** | 0 |
| S3 2018-2022 | 1.236 | 146 | 39 | 16 | 0 | 21 | 6 | **27** | 2 |
| S4 2022-now | 1.263 | 21 | 44 | 4 | 0 | 48 | 0 | **48** | 0 |

`cnt4 = 0` di **semua** cycle — konsisten dengan temuan V1 (kondisi K4 #2 tidak pernah nyala).

Catatan: 48 hari K4 aktif di S4 semuanya **ekor bear 2022** (Des-2022 / Jan-2023), bukan bear berjalan.

---

## (c) Lantai waktu

| Cycle | peak (ex-post) | start | stop / Signal D | hari aktif | kontrol causal: start | hari |
|---|---|---|---|---|---|---|
| S0 *(supl.)* | 2011-06-08 | 2012-03-04 | 2012-03-06 | 1 | 2012-03-04 | 1 |
| S1 2013-2015 | 2013-11-29 | 2014-10-04 | 2015-01-14 | **36** | 2014-10-04 | 36 |
| S2 2015-2018 | 2017-12-16 | 2018-11-19 | 2018-12-15 | **26** | 2018-11-19 | 26 |
| S3 2018-2022 | 2021-11-08 | 2022-08-19 | 2022-11-21 | **90** | 2022-08-19 | 90 |
| S4 2022-now | 2025-10-06 | — | — | **0** | — | 0 |

Versi causal **identik** dengan versi ex-post di keempat cycle → **lantai waktu tidak sensitif terhadap
cara peak ditentukan**. Ini hasil yang bagus untuk anti-lookahead.

---

## (d) Kapasitas sizing — jawaban operasional

**Konversi:** rate bulanan / 30,44 = rate harian. Prioritas K4 (count 2/3/4 → 15/25/35%) di atas lantai
waktu (5%). Flag ekstrem P/CVDD ≤ 1,0 → tarik 50% sisa pool hari itu.

Mode A (% dari pool awal, bisa habis di 100%) dilaporkan sebagai hasil utama; Mode B (% dari sisa)
sebagai kontrol.

| Bear | hari deploy aktif | kapasitas terpakai **di titik low** | di akhir window | **habis sebelum low?** | Mode B |
|---|---|---|---|---|---|
| 2014-15 | 37 | **53,4%** | 53,4% | **TIDAK** | 53,3% |
| 2018 | 27 | **7,6%** | 8,4% | **TIDAK** | 8,1% |
| 2022 | 91 | **82,4%** | 82,4% | **TIDAK** | 79,8% |
| **2025-26 (berjalan)** | **0** | **0,0%** | 0,0% | **TIDAK** | 0,0% |

**Hari flag ekstrem:** 2015-01-14 (1×), 2022-11-09 & 2022-11-21 (2×) — dua-duanya persis di area bottom,
jadi tarikan 50% sisa pool jatuh di tempat yang benar.

### Diagnostik bear berjalan (per 2026-07-15)

- Cycle peak 2025-10-06 @ $124.715
- Jam 9 bulan (270 hari) **sudah lewat** (2026-07-03), tapi syarat kedua lantai waktu (close < RP)
  **belum terpenuhi** — $65.098 vs RP $52.740
- Zona hari terakhir = **ZD** (struktur N), `k4_count` = 0, alarm bear cepat **aktif**

→ **Tidak ada satu pun jalur deploy K4 / lantai waktu yang nyala di bear ini sejauh ini.**

---

## Kesimpulan

**Prinsip video KONFIRMASI secara aritmetika, tapi tidak menuntut perubahan sizing K4 — masalahnya justru
kebalikannya.**

**1. Base rate ada dan angkanya cocok.** Z5 = 12,6% (703 hari) praktis identik dengan "12% of days" yang
disebut video, dan klaim 703 hari di Decision_Framework v2 terverifikasi persis. Jadi prinsip "kalibrasi
ukuran aksi ke frekuensi sinyal" **bisa** diterapkan ke framework kita, karena base rate-nya sudah terukur.

**2. Untuk aksi kontinu (K4, lantai waktu), sizing sekarang TIDAK terlalu agresif — malah cenderung
terlalu pelit.** Kapasitas cash pool **tidak pernah habis sebelum cycle low** di 3 bear selesai; terpakai
53,4% (2014-15), **hanya 7,6% (2018)**, 82,4% (2022). Bear 2018 adalah kasus paling telanjang: cuma
**27 hari deploy aktif** sepanjang bear 365 hari, artinya **>92% cash pool masih menganggur di titik
bottom**. Bahaya operasional yang nyata **bukan** "kehabisan amunisi terlalu cepat", melainkan **sinyal
terlalu jarang nyala sehingga pool tidak sempat terpakai**.

**3. Catatan claim-tester terkonfirmasi.** Prinsip ini masuk akal untuk aksi berulang (K4, lantai waktu)
tapi **tidak otomatis berlaku ke K1**, yang event-driven sekali jalan (~1 per cycle; 40 kunjungan Z5
dalam 15 tahun terbagi ke 4 cycle). Untuk aksi sekali-jalan, yang relevan adalah biaya salah waktu,
bukan base rate harian.

---

## Flag n & independensi (tebal, sesuai Standar Validasi poin 2, 4, 5)

- **n = 4 cycle established (S4 belum selesai) + 1 suplemen pra-2013**; **n = 3 bear selesai** untuk
  simulasi kapasitas
- Hari-hari dalam satu zona **sangat berkorelasi** (blok kontinu) — base rate harian **bukan** n
  independen. Unit yang jujur adalah jumlah kunjungan per cycle: Z1 cuma **13 kunjungan** seumur data,
  Z2 cuma **8**
- Sampel efektif mulai **2011-02-09**, bukan 2010-07-17, karena btlib membuang baris tanpa kolom AVIV
- Simulasi kapasitas mengasumsikan cash pool sudah terisi penuh di awal bear — di praktik, pool bergantung
  pada eksekusi K1 sebelumnya (risiko struktural yang sama yang diakui video sebagai mode kegagalan mereka)
