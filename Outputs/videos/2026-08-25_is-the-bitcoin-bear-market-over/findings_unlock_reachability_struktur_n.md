# Findings - Apakah sinyal "unlock" DF v2 bisa dicapai kalau struktur tetap N?

**Tanggal validasi:** 26 Agustus 2026
**Script:** `analyze_unlock_reachability_struktur_n.py`
**Event table:** `events_unlock_reachability_struktur_n.csv`
**Data:** `data_master_all_metrics.csv` - 2010-07-17 s/d **2026-07-15** (n = 5.843 hari)

---

## Ringkasan sederhana

**Gap-nya nyata dan terkonfirmasi.** DF v2 bagian 0 mendefinisikan "status bear berakhir (unlock)" = STH RP cross naik melewati RP. Cross itu cuma mungkin kalau STH RP pernah turun **di bawah** RP dulu (struktur T). Bear 2025-26 sampai 2026-07-15 punya **0 hari struktur T** - rasio STH RP/RP tidak pernah turun di bawah **1,272**. Artinya sinyal unlock formal **secara mekanis tidak bisa bunyi** di bear ini, dan K5 tidak bisa start selama kondisinya begini.

Tapi jawaban untuk pertanyaan (a) **berbeda dari dugaan awal**: dari 5 bear siklus penuh, cuma **1 yang tidak pernah T yaitu 2025-26**. Bear 2017 (turunnya sampai Des 2018) **memang pernah T** - 59 hari, 2019-01-29 s/d 2019-03-28. Yang tidak pernah T adalah **window mid-cycle 2019-06 s/d 2020-05** (termasuk crash COVID) - tapi itu bukan bear siklus penuh, dan memang di sana tidak ada unlock formal sama sekali.

Tiga kandidat unlock pengganti yang diuji **semuanya hit rate-nya rendah** (25-29%) karena kebanyakan bunyi kepagian di bear 2011 dan 2013. Kandidat (i) baru terlihat rapi di dua bear terakhir saja (2017 & 2021: 2/2 HIT, dan 20-29 hari **lebih cepat** dari unlock formal) - **n=2, jelas terlalu kecil untuk dijadikan aturan.**

---

## Definisi (dikunci sebelum menghitung)

- **Cycle peak** (diverifikasi = max harga +-180 hari): 2011-06-08, 2013-11-29, 2017-12-16, 2021-11-08, 2025-10-06
- **Cycle low** = close terendah antara peak dan peak berikutnya
- **"Bear sebenarnya berakhir" = RECLAIM PERMANEN** = hari pertama setelah cycle low di mana close > `sth_cost_basis` DAN harga bertahan di atas `sth_cost_basis` **90 hari berturut** sesudahnya. Forward-looking, dipakai HANYA sebagai label kebenaran, bukan gate
- **Unlock formal** = STH RP cross naik melewati RP, didahului >=30 hari berturut struktur T
- **Kandidat pengganti** (at-gate murni, cooldown 180 hari), hanya 3 varian, tanpa grid search:
  - (i) close > `sth_cost_basis` >=21 hari berturut
  - (ii) close > `sth_cost_basis` >=3 hari DAN slope 30-hari `sth_cost_basis` > 0
  - (iii) (i) DAN close > `200_dma` di hari sinyal
- **Penilaian sinyal** (hanya sinyal di dalam bear window peak -> reclaim+60 hari): **HIT** kalau sinyal muncul >= (reclaim permanen - 30 hari) DAN dalam 90 hari sesudahnya harga tidak turun >=20% dari harga sinyal. Selain itu **MISS**

---

## (a) Berapa bear yang struktur N-nya tidak pernah putus?

**n = 5 bear siklus penuh (1 censored).** Yang tidak pernah menyentuh struktur T: **1 dari 5 = 2025-26 saja.**

| Cycle | Peak | Cycle low | Reclaim permanen | Hari bear | Hari T | % T | Min STH RP / RP |
|-------|------|-----------|------------------|-----------|--------|-----|-----------------|
| 2011 | 2011-06-08 | 2011-11-18 | 2012-11-03 | 515 | 131 | 25,4% | 0,890 (2012-02-22) |
| 2013 | 2013-11-29 | 2015-01-14 | 2015-10-13 | 684 | 251 | 36,7% | 0,842 (2015-06-14) |
| 2017 | 2017-12-16 | 2018-12-14 | 2019-03-28 | 468 | 59 | 12,6% | 0,924 (2019-03-28) |
| 2021 | 2021-11-08 | 2022-11-21 | 2023-01-11 | 430 | 72 | 16,7% | 0,903 (2023-01-08) |
| **2025** | 2025-10-06 | 2026-06-30 | **BELUM (censored)** | 283 | **0** | **0,0%** | **1,272 (2026-07-13)** |

Periode struktur T per cycle: 2011 = 2011-12-10 s/d 2012-04-18; 2013 = 2015-02-05 s/d 2015-10-13; 2017 = 2019-01-29 s/d 2019-03-28; 2021 = 2022-11-01 s/d 2023-01-11.

**Jawaban untuk dugaan "2019-2020 juga masuk kategori ini":** setengah benar. Kalau yang dimaksud **bear siklus 2017 (yang berakhir 2019)** - itu **pernah T** (59 hari). Tapi kalau yang dimaksud **window mid-cycle 2019-06-26 s/d 2020-05-01** (top $13k Juni 2019 sampai pasca-crash COVID), itu memang **0 hari T**, min STH RP/RP = **1,354**, dan **tidak ada unlock formal sama sekali** di window itu - meskipun harga sempat jatuh ke $4.837 (2020-03-12). Jadi lubang yang sama pernah terjadi sekali sebelumnya, tapi di penurunan mid-cycle, bukan bear siklus penuh. Ini kembar dari kasus 2020 yang sudah diakui DF v2 lewat jalur **K4-tanpa-Z1**.

**Kesimpulan (a): 2025-26 adalah bear siklus penuh PERTAMA dalam 16 tahun data yang struktur N-nya tidak pernah putus.** Jaraknya bahkan tidak dekat: min rasio 1,272 vs 0,842-0,924 di empat bear sebelumnya.

---

## (b) Jarak unlock formal ke bear end sebenarnya

Unlock formal terdeteksi 4 kali: **2012-04-19, 2015-11-03, 2019-05-07, 2023-03-01.**

| Cycle | Cycle low | Reclaim permanen | Unlock formal | Lag unlock - reclaim |
|-------|-----------|------------------|---------------|----------------------|
| 2011 | 2011-11-18 | 2012-11-03 | 2012-04-19 | **-198 hari** (unlock jauh lebih cepat) |
| 2013 | 2015-01-14 | 2015-10-13 | 2015-11-03 | +21 hari |
| 2017 | 2018-12-14 | 2019-03-28 | 2019-05-07 | +40 hari |
| 2021 | 2022-11-21 | 2023-01-11 | 2023-03-01 | +49 hari |
| 2025 | 2026-06-30 | **BELUM** | **TIDAK ADA** | n/a |

Pola: di tiga bear terakhir unlock formal datang **21-49 hari setelah** bear benar-benar berakhir - artinya lambat tapi konsisten searah. Di 2011 dia justru 198 hari **terlalu cepat** (bunyi April 2012 padahal harga baru benar-benar bertahan November 2012). **n=4, arahnya tidak seragam.**

---

## (c) Tiga kandidat unlock pengganti - hasil

### (i) close > STH RP >=21 hari berturut

Total sinyal seluruh sejarah (cooldown 180 hari) = 18; **di dalam bear window: n=7**.

| Cycle | Sinyal | Harga | Lag vs reclaim | maxdd 90d | ret 90d | Verdict |
|-------|--------|-------|----------------|-----------|---------|---------|
| 2011 | 2012-01-20 | $6 | -288d | -34,9% | -20,7% | MISS |
| 2011 | 2012-09-09 | $11 | -55d | -7,8% | +21,7% | MISS |
| 2013 | 2014-01-08 | $826 | -643d | -47,1% | -45,3% | MISS |
| 2013 | 2014-07-17 | $624 | -453d | -48,7% | -36,8% | MISS |
| 2013 | 2015-07-17 | $280 | -88d | -24,8% | -9,0% | MISS |
| 2017 | 2019-04-17 | $5.248 | +20d | 0,0% | +81,8% | **HIT** |
| 2021 | 2023-01-31 | $23.133 | +20d | -12,6% | +21,5% | **HIT** |

**HIT=2, MISS=5, hit rate 29%.** Sebaran per cycle: 2011 = 2, 2013 = 3, 2017 = 1, 2021 = 1.

### (ii) close > STH RP >=3 hari DAN slope 30-hari STH RP > 0

Total sinyal = 14; **di dalam bear window: n=4** (semuanya cuma di 2011 & 2013).

| Cycle | Sinyal | Lag vs reclaim | maxdd 90d | ret 90d | Verdict |
|-------|--------|----------------|-----------|---------|---------|
| 2011 | 2012-03-28 | -220d | -2,0% | +34,1% | MISS |
| 2011 | 2012-11-05 | +2d | +0,7% | +91,7% | **HIT** |
| 2013 | 2013-12-21 | -661d | -11,2% | -4,9% | MISS |
| 2013 | 2015-08-11 | -63d | -22,6% | +39,9% | MISS |

**HIT=1, MISS=3, hit rate 25%.** Sebaran per cycle: 2011 = 2, 2013 = 2 - **tidak menghasilkan sinyal sama sekali di bear 2017 dan 2021**, jadi tidak bisa diuji lintas 4 bear. Ini kelemahan serius.

### (iii) (i) DAN close > 200 DMA

**Hasilnya IDENTIK dengan (i)**: n=7, HIT=2, MISS=5, hit rate 29%, tanggal sama persis. Filter 200 DMA **tidak membuang satu pun** sinyal (setiap kali harga sudah 21 hari di atas STH RP di bear window, harga juga sudah di atas 200 DMA). Jadi (iii) **tidak menambah informasi apapun** - bukan kandidat terpisah dalam praktik.

### Suplemen: kandidat (i) vs unlock formal, sinyal terakhir tiap bear

| Cycle | Sinyal (i) terakhir | Unlock formal | Selisih |
|-------|---------------------|---------------|---------|
| 2011 | 2012-09-09 | 2012-04-19 | +143 hari (lebih lambat) |
| 2013 | 2015-07-17 | 2015-11-03 | -109 hari (lebih cepat, tapi salah/MISS) |
| 2017 | 2019-04-17 | 2019-05-07 | **-20 hari** (lebih cepat, HIT) |
| 2021 | 2023-01-31 | 2023-03-01 | **-29 hari** (lebih cepat, HIT) |
| 2025 | TIDAK ADA | TIDAK ADA | n/a |

Menariknya: **di dua bear terakhir kandidat (i) memberi sinyal benar 20-29 hari lebih cepat dari unlock formal.** Tapi n=2 dan di dua bear lama dia melahirkan 5 sinyal palsu dengan drawdown -25% s/d -49%. **Tidak layak dipromosikan jadi gate.**

---

## State bear 2025-26 (s/d 2026-07-15)

| Item | Nilai |
|------|-------|
| Peak -> hari terakhir data | 2025-10-06 -> 2026-07-15 (283 hari) |
| Hari struktur T | **0** |
| Min STH RP / RP | **1,272** (2026-07-13) |
| STH RP / RP hari terakhir | 1,273 |
| Streak close > STH RP hari terakhir | **0 hari** |
| Slope 30-hari STH RP | **-$5.485** (masih turun) |
| Close vs 200 DMA | $65.098 vs $73.534 (di bawah) |
| Cycle low sementara | 2026-06-30 |

Jadi per 2026-07-15: tidak ada satupun dari 3 kandidat yang nyala, dan unlock formal masih mustahil secara mekanis. Rally Agustus 2026 yang dibahas video **belum masuk data**; kalau rally itu bertahan, kandidat (i) baru bisa bunyi paling cepat sekitar 21 hari setelah close pertama di atas STH RP.

---

## Cek Standar Validasi

1. **Definisi event** - eksplisit + cooldown 180 hari; definisi reclaim permanen dikunci di muka. OK
2. **n dilaporkan** - bear siklus penuh n=5 (1 censored); sinyal di bear window: (i) n=7, (ii) n=4, (iii) n=7. **Semua sample kecil**. OK
3. **Anti-lookahead** - semua kandidat pakai input yang tersedia di hari sinyal (streak, slope 30 hari ke belakang, 200 DMA). Reclaim permanen forward-looking tapi hanya sebagai label kebenaran. OK
4. **Independensi** - hasil kandidat (i) **didominasi bear 2011 & 2013** (5 dari 7 sinyal, semua MISS). Dua HIT-nya cuma dari 2017 & 2021, satu-satu. OK
5. **Data mulai belakangan** - tidak berlaku (semua kolom full-history sejak 2010-07-17). OK
6. **Overfit** - persis 3 varian yang diminta, tidak ada grid search, semua dilaporkan termasuk yang gagal, dan (iii) dilaporkan redundan. OK

---

## Verdict

**GAP TERKONFIRMASI - dan lebih tajam dari dugaan awal.** Bear 2025-26 adalah **bear siklus penuh pertama dalam 16 tahun data** yang struktur N-nya tidak pernah putus (0 hari T dari 283 hari; min STH RP/RP = 1,272 vs 0,842-0,924 di empat bear sebelumnya). Karena unlock DF v2 didefinisikan sebagai cross-ke-atas, **sinyal itu secara mekanis tidak bisa bunyi** dan K5 tidak bisa start - persis lubang yang sama dengan penurunan mid-cycle 2019-2020 (0 hari T juga, tidak ada unlock formal walau harga jatuh ke $4.837).

**Tapi tidak ada satupun dari 3 kandidat pengganti yang lolos.** Hit rate 25-29% (n=7/4/7 di bear window), sinyal palsu kepagian sampai 643 hari sebelum bear benar-benar berakhir, dan varian (iii) identik dengan (i). Yang terlihat menjanjikan - kandidat (i) menyalip unlock formal 20-29 hari di bear 2017 & 2021 - berdiri di atas **n=2 saja**. Rekomendasi: **jangan ganti definisi unlock berdasarkan hasil ini.** Yang layak diusulkan ke Yudi adalah **jalur darurat sejenis K4-tanpa-Z1 untuk sisi K5** (misalnya: kalau bear sudah >=X bulan DAN struktur tidak pernah T, pakai gate alternatif dengan sizing dikurangi), bukan mengganti sinyal unlock-nya. **n kecil, low confidence.**
