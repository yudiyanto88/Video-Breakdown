# Findings — Presisi VDD Multiple & Supply-Adjusted CDD di bear low + uji confound harga

**Sumber klaim:** Bitcoin Magazine Pro — "This Signalled Every Bitcoin Bottom — We're 4.9% Away, So Why Risk It" (2026-05-25), klaim B6 `[02:54]`–`[03:11]` dan B7 `[03:28]`–`[04:04]`
**Tanggal validasi:** 2026-08-06
**Script:** [`analyze_cdd_vdd_bottom_precision.py`](analyze_cdd_vdd_bottom_precision.py)
**Event table:** [`events_cdd_vdd_bottom_precision.csv`](events_cdd_vdd_bottom_precision.csv) (318 baris), [`events_cdd_vdd_precision_summary.csv`](events_cdd_vdd_precision_summary.csv)
**Data:** `data_master_all_metrics.csv`, window analisis inti **2011-07-16 s/d 2026-07-15 (n = 5.479 hari)** — mencakup 4 bear low terkonfirmasi

---

## Klaim yang diuji

**B6.** VDD Multiple di level bear-market-low = distribusi LTH/whale berhenti.
**B7.** Supply-Adjusted CDD di level yang historically = "unbelievable accumulation opportunity" — **pembicara sendiri mengakui failure mode**: di 2018 sinyal ini muncul tepat SEBELUM downward spike besar, bukan menandai low.

**Hipotesis kritik (inti validasi ini):** VDD adalah **value-weighted** (coin-days × harga USD). Saat harga turun 48%, nilai VDD ikut turun **tanpa perubahan perilaku holder sama sekali**. "LTH berhenti distribusi" dan "harga rendah sehingga coin-days yang sama bernilai lebih kecil dalam USD" menghasilkan pembacaan **identik**.

---

## Definisi & parameter (ditetapkan SEBELUM menghitung)

| Seri | Formula | Bobot |
|---|---|---|
| `vdd_mult_ma` | MA30(cdd × price) / MA365(cdd × price) — bentuk chart BMPro | **value-weighted** |
| `vdd_multiple` | kolom master apa adanya (lihat catatan data di bawah) | **value-weighted** |
| `sacdd_ma30` | MA30 dari `cdd / (lth_supply_btc + sth_supply_btc)` | unit-weighted |
| `sacdd_ma900` | MA900 dari seri yang sama (frame BMPro terlihat pakai MA900 & MA30) | unit-weighted |
| `cdd_mult_ma` | **twin price-stripped:** MA30(cdd) / MA365(cdd) — struktur rasio persis sama, harga dilepas | unit-weighted |
| `price_ratio` | **benchmark naif:** MA30(price) / MA365(price) — tanpa data umur koin sama sekali | HARGA MURNI |

- **Threshold a priori: persentil 5 dan 10 saja. TIDAK ada grid search.** Semua 6 seri × 2 threshold × 2 mode dilaporkan apa adanya — tidak ada varian yang dibuang.
- **Event:** hari **pertama** seri turun ke ≤ threshold; **cooldown 90 hari** sebelum event berikutnya boleh dihitung.
- **Hit (tepat sasaran):** |tanggal trigger − bear low terkonfirmasi| ≤ **60 hari**.
- **Failure mode:** drawdown **maksimum** 90 hari SESUDAH trigger ≤ **−20%** (min harga di jendela ÷ harga trigger − 1).
- **Anti-lookahead — dua mode dilaporkan berdampingan:**
  - **Mode A** = persentil full-history (**in-sample/lookahead — dilabel jelas**)
  - **Mode B** = persentil **trailing 4 tahun (1.461 hari, min 365)**, at-gate — ini yang benar-benar bisa diketahui di tanggal keputusan
  Drawdown & return selalu diukur SESUDAH tanggal trigger.
- **Ground truth:** 4 bear low terkonfirmasi — 2011-11-18, 2015-01-14, 2018-12-14, 2022-11-21. Low sementara **2026-06-30 ($58.460) BELUM terkonfirmasi**, dilaporkan terpisah.
- **Event dengan trigger > 2025-10-06** dikeluarkan dari presisi/recall — bear low cycle berjalan belum terkonfirmasi sehingga tidak bisa dinilai. Ditandai `scoreable=False` di CSV (27 dari 318 baris).

### Sanity check anchor 2026-05-25

| Kolom | Nilai data | Anchor | Status |
|---|---|---|---|
| `btc_price` | $77.172,08 | $77.172 | OK |
| `realized_price` | $54.171,61 | $54.172 | OK |
| `sth_cost_basis` | $77.909,65 | $77.910 | OK |
| `lth_cost_basis` | $48.649,79 | $48.650 | OK |
| `50_wma` | $94.325,20 | $94.325 | OK |
| `vdd_multiple` | **0,2307** | 0,533 | **MISMATCH** |

### ⚠ Catatan data penting (temuan sampingan, perlu diangkat ke Onchain-Dashboard)

Dua hal terverifikasi secara aljabar dari data master:

1. **`vdd_30d_ma` == MA30(`cdd` × `btc_price`) persis** (rasio min = maks = 1,000000). Jadi **VDD memang value-weighted** — komponen harga ada di dalamnya secara definisi, bukan dugaan.
2. **`vdd_multiple` di data master BUKAN MA30/MA365.** Kolom itu = **VDD HARIAN ÷ MA365(VDD)** (selisih maks 1,4e−14). Artinya seri harian yang **sangat berisik**: dalam satu minggu di sekitar tanggal video nilainya berayun 0,281 → 0,576 → 0,566 → 0,177 → 0,214 → **0,231 (2026-05-25)** → 0,420 → 0,375 → 0,690 → 0,664 → 0,276.

Karena itu **anchor 0,533 tidak bisa dicocokkan** — bukan karena datanya salah, tapi karena **tidak ada angka satu-hari yang bermakna** untuk seri ini. Primary di uji ini adalah `vdd_mult_ma` = MA30/MA365 (bentuk yang ditampilkan chart BMPro); nilainya di 2026-05-25 = **0,3533**. Kolom mentah `vdd_multiple` tetap diuji berdampingan sebagai sensitivity.

**Usulan (bukan penerapan):** tambahkan catatan di `data_dictionary.md` bahwa `vdd_multiple` adalah rasio harian, bukan VDD Multiple versi smoothed — supaya tidak ada script lain yang memperlakukannya sebagai seri chart.

### Ketersediaan data

`cdd` & `vdd_*` mulai 2009-01-03, `btc_price` 2010-07-17. Setelah warm-up MA365, window inti mulai **2011-07-16** → **4 bear low terkonfirmasi semuanya tercakup**. Satu pengecualian yang harus disebut: **`sacdd_ma900` butuh warm-up 900 hari sehingga baru mulai 2013-01-01 — seri itu TIDAK bisa melihat bear low 2011.** Uji lintas-cycle untuk seri itu tidak penuh.

---

## Hasil

### 1. Dekomposisi confound harga — seberapa besar VDD Multiple sebenarnya harga?

Regresi log-space, n = 5.479 hari:

| Model | R² |
|---|---|
| log(VDD Mult) ~ log(price_ratio) **saja** | **0,661** |
| log(VDD Mult) ~ log(cdd_mult) **saja** | 0,656 |
| log(VDD Mult) ~ keduanya | 0,965 |

| Pasangan | Spearman |
|---|---|
| VDD Mult vs price_ratio | **+0,836** |
| VDD Mult vs cdd_mult | +0,806 |
| sacdd_ma30 vs price_ratio | +0,449 |

**Komponen harga dan komponen coin-days menyumbang porsi yang praktis sama** ke variasi VDD Multiple (R² 0,661 vs 0,656). Ini belum membuktikan sinyalnya efek harga — yang menentukan adalah bagian berikutnya: **mana dari dua komponen itu yang membawa kemampuan menandai dasar.**

### 2. Presisi — Mode A (full-history persentil, IN-SAMPLE)

Event 2026 dikeluarkan (lihat definisi).

| Seri | Bobot | p | n event | Hit ±60d | Presisi | Recall 4 low | Fail DD≥20% | Median DD90 |
|---|---|---|---|---|---|---|---|---|
| `vdd_mult_ma` | value | 5 | 11 | 4 | **36,4%** | 4/4 | 3/11 | −14,7% |
| `vdd_mult_ma` | value | 10 | 14 | 5 | **35,7%** | 4/4 | 4/14 | −11,6% |
| `vdd_multiple` | value | 5 | 20 | 4 | 20,0% | 4/4 | 9/20 | −17,3% |
| `vdd_multiple` | value | 10 | 31 | 4 | 12,9% | 4/4 | 10/31 | −14,3% |
| `sacdd_ma30` | unit | 5 | 15 | 2 | 13,3% | 2/4 | 5/15 | −7,3% |
| `sacdd_ma30` | unit | 10 | 20 | 2 | 10,0% | 2/4 | 7/20 | −9,6% |
| `sacdd_ma900` | unit | 5 | 4 | 0 | 0,0% | 0/4 | 1/4 | −9,0% |
| `sacdd_ma900` | unit | 10 | 8 | 0 | 0,0% | 0/4 | 1/8 | −4,0% |
| **`cdd_mult_ma`** | **unit (price-stripped)** | 5 | 7 | 0 | **0,0%** | **0/4** | 5/7 | −24,9% |
| **`cdd_mult_ma`** | **unit (price-stripped)** | 10 | 18 | 0 | **0,0%** | **0/4** | 9/18 | −17,6% |
| **`price_ratio`** | **HARGA MURNI** | 5 | 5 | 4 | **80,0%** | **4/4** | 0/5 | −7,0% |
| **`price_ratio`** | **HARGA MURNI** | 10 | 9 | 4 | **44,4%** | **4/4** | 2/9 | −14,9% |

### 3. Presisi — Mode B (persentil TRAILING 4 tahun, AT-GATE / anti-lookahead)

| Seri | Bobot | p | n event | Presisi | Recall | Fail DD≥20% | Median DD90 |
|---|---|---|---|---|---|---|---|
| `vdd_mult_ma` | value | 5 | 8 | 25,0% | 2/4 | 2/8 | −12,8% |
| `vdd_mult_ma` | value | 10 | 10 | 30,0% | 3/4 | 3/10 | −11,2% |
| `vdd_multiple` | value | 5 | 18 | 22,2% | 3/4 | 9/18 | −19,0% |
| `vdd_multiple` | value | 10 | 28 | 10,7% | 3/4 | 9/28 | −14,1% |
| `sacdd_ma30` | unit | 5 | 8 | 0,0% | 0/4 | 1/8 | −8,8% |
| `sacdd_ma30` | unit | 10 | 12 | 0,0% | 0/4 | 2/12 | −7,7% |
| `sacdd_ma900` | unit | 5 | 4 | 0,0% | 0/4 | 0/4 | −5,4% |
| `sacdd_ma900` | unit | 10 | 6 | 0,0% | 0/4 | 0/6 | −4,0% |
| **`cdd_mult_ma`** | **price-stripped** | 5 | 8 | **0,0%** | 0/4 | 5/8 | −24,3% |
| **`cdd_mult_ma`** | **price-stripped** | 10 | 15 | **0,0%** | 0/4 | 8/15 | −22,4% |
| **`price_ratio`** | **HARGA MURNI** | 5 | 5 | **60,0%** | 3/4 | 1/5 | −13,0% |
| **`price_ratio`** | **HARGA MURNI** | 10 | 7 | 28,6% | 2/4 | 3/7 | −19,4% |

Mode B (yang jujur secara temporal) menurunkan semua angka, tapi **urutan peringkatnya tidak berubah**: harga murni > VDD (value-weighted) > sacdd > CDD price-stripped (nol).

### 4. Sebaran event per cycle (Mode A, p10) — independensi sample

| Seri | n | 2011 | 2015 | 2018 | 2022 | 2026 |
|---|---|---|---|---|---|---|
| `vdd_mult_ma` | 14 | 3 | 4 | 5 | 2 | 0 |
| `vdd_multiple` | 31 | 4 | 6 | 8 | 11 | 2 |
| `sacdd_ma30` | 20 | 5 | 6 | 5 | 4 | 0 |
| `sacdd_ma900` | 8 | **0** | 7 | 1 | 0 | 0 |
| `cdd_mult_ma` | 18 | 1 | 5 | 6 | 6 | 0 |
| `price_ratio` | 9 | 1 | 3 | 2 | 3 | 0 |

⚠ Sebarannya relatif merata untuk seri utama, **kecuali `sacdd_ma900`: 7 dari 8 event-nya berasal dari cycle-2015 saja** (dan 0 dari 2011 karena warm-up 900 hari). Hasil seri itu praktis satu-cycle — **jangan diperlakukan sebagai bukti lintas-cycle.**

### 5. Distribusi drawdown maksimum 90 hari (Mode A, p10) — kuantifikasi failure mode

| Seri | n | Min | p25 | Median | Maks | Event dengan DD ≥20% |
|---|---|---|---|---|---|---|
| `vdd_mult_ma` | 14 | −53,5% | −33,0% | −11,6% | +0,7% | **4** |
| `vdd_multiple` | 31 | −83,3% | −26,3% | −14,3% | +5,3% | **10** |
| `sacdd_ma30` | 20 | −83,7% | −26,2% | −9,6% | +0,4% | **7** |
| `sacdd_ma900` | 8 | −41,9% | −6,5% | −4,0% | −0,5% | 1 |
| `cdd_mult_ma` | 18 | −79,8% | −42,1% | −17,6% | +0,4% | **9** |
| `price_ratio` | 9 | −49,5% | −19,3% | −14,9% | +1,2% | 2 |

**Poin yang hilang kalau cuma melihat return rata-rata: kuartil bawah `vdd_mult_ma` adalah −33,0% dan yang terburuk −53,5%.** Sinyal ini bukan "kadang telat" — kadang ia menempatkan modal tepat sebelum separuh nilai hilang.

Daftar event lengkap `vdd_mult_ma` (Mode A, p10; termasuk 2 event 2026 yang tidak di-score):

| Trigger | Harga | Hari ke low | Hit | Max DD 90d | Tgl DD | Ret 90d |
|---|---|---|---|---|---|---|
| 2011-10-08 | $4 | −41 | YA | **−48,8%** | 2011-11-18 | +67,1% |
| 2012-01-07 | $7 | +50 | YA | **−37,9%** | 2012-02-18 | −27,4% |
| 2012-04-08 | $5 | +142 | — | +0,7% | 2012-04-10 | +41,4% |
| 2014-05-09 | $454 | −250 | — | −3,7% | 2014-05-11 | +29,2% |
| 2014-10-21 | $384 | −85 | — | **−53,5%** | 2015-01-14 | −43,7% |
| 2015-02-08 | $224 | +25 | YA | −2,2% | 2015-04-14 | +8,2% |
| 2015-05-23 | $239 | +129 | — | −7,3% | 2015-08-18 | −2,4% |
| 2018-04-02 | $7.166 | −256 | — | −17,5% | 2018-06-28 | −11,5% |
| 2018-07-02 | $6.604 | −165 | — | −6,5% | 2018-08-10 | +0,3% |
| 2018-10-01 | $6.610 | −74 | — | **−50,4%** | 2018-12-14 | −40,7% |
| 2019-01-04 | $3.902 | +21 | YA | −12,1% | 2019-02-07 | +25,7% |
| 2020-04-16 | $7.101 | +489 | — | −2,8% | 2020-04-21 | +29,5% |
| 2022-07-17 | $20.787 | −127 | — | −11,1% | 2022-09-21 | −8,3% |
| 2022-10-16 | $19.262 | −36 | YA | −18,1% | 2022-11-21 | +8,8% |
| *2026-02-22* | *$67.658* | *n/a* | *—* | *−5,3%* | *2026-02-24* | *+13,3%* |
| *2026-05-24* | *$77.066* | *n/a* | *—* | ***−24,1%*** | *2026-06-30* | *−15,5%* |

Perhatikan pola yang berulang: **hit dan failure sering terjadi di event yang SAMA.** 2011-10-08 dan 2012-01-07 dua-duanya "hit ±60 hari" **dan** diikuti drawdown 48,8% / 37,9%. Jadi "dekat dengan low" tidak berarti "aman masuk" — sinyalnya bisa benar soal lokasi dan tetap menghancurkan soal timing.

### 6. Reproduksi kasus 2018 — failure mode yang diakui pembicara: **TERKONFIRMASI**

Konteks harga: puncak periode 2018-01-06 $17.579 → bear low 2018-12-14 $3.281. Downward spike yang dimaksud: **2018-11-01 $6.395 → 2018-12-14 $3.281 = −48,7%**.

Trigger di jendela Sep–14 Nov 2018 (sebelum spike): **n = 7**, semuanya diikuti drawdown besar:

| Seri | p | Trigger | Harga | Max DD 90d |
|---|---|---|---|---|
| `vdd_multiple` | 5 | 2018-09-01 | $7.184 | **−46,7%** |
| `cdd_mult_ma` | 10 | 2018-09-26 | $6.476 | **−49,3%** |
| `vdd_mult_ma` | 5 | 2018-09-28 | $6.644 | **−50,6%** |
| `cdd_mult_ma` | 5 | 2018-09-28 | $6.644 | **−50,6%** |
| `vdd_mult_ma` | 10 | 2018-10-01 | $6.610 | **−50,4%** |
| `vdd_multiple` | 10 | 2018-10-05 | $6.629 | **−50,5%** |
| `sacdd_ma30` | 10 | 2018-10-13 | $6.354 | **−48,4%** |

**Pengakuan pembicara akurat — dan skalanya lebih besar dari yang dia sampaikan: bukan satu sinyal, tapi 7 trigger berturut-turut selama 6 minggu, semuanya diikuti drawdown 46–51%.**

Yang lebih mendasar, ini persentil **trailing** (at-gate) tiap seri di dua tanggal kunci:

| Seri | 2018-11-01 (sebelum spike) | 2018-12-14 (bear low sebenarnya) |
|---|---|---|
| `vdd_mult_ma` | **7,7** (sinyal NYALA) | **60,0** |
| `vdd_multiple` | 16,8 | 9,4 |
| `sacdd_ma30` | 20,3 | **98,1** |
| `cdd_mult_ma` | 12,9 | **99,9** |
| `sacdd_ma900` | 80,2 | 99,7 |
| `price_ratio` | 17,1 | **1,0** (benar) |

**Ini penjelasan mekanisnya, dan bagian paling penting dari seluruh validasi.** Metrik keluarga CDD terbaca **"sunyi" (persentil rendah) SEBELUM kapitulasi** dan **"kencang" (persentil 98–100) TEPAT DI bear low** — karena kapitulasi *adalah* peristiwa koin lama bergerak massal. Interpretasi "CDD/VDD di minimum = dasar" cenderung **membaca metriknya terbalik terhadap low sebenarnya.** Satu-satunya seri yang berperilaku benar di 2018-12-14 adalah `price_ratio` (persentil 1,0) — yaitu harga, bukan umur koin.

### 7. Head-to-head confound — **inti kritik terbukti**

Mode A p10:

| Seri | Bobot | n | Presisi | Recall | Fail DD20 |
|---|---|---|---|---|---|
| `vdd_mult_ma` | VALUE-weighted | 14 | 35,7% | 4/4 | 4/14 |
| `vdd_multiple` | VALUE-weighted | 31 | 12,9% | 4/4 | 10/31 |
| `sacdd_ma30` | unit-weighted | 20 | 10,0% | 2/4 | 7/20 |
| `sacdd_ma900` | unit-weighted | 8 | 0,0% | 0/4 | 1/8 |
| **`cdd_mult_ma`** | **unit (harga dilepas)** | 18 | **0,0%** | **0/4** | 9/18 |
| **`price_ratio`** | **HARGA MURNI** | 9 | **44,4%** | **4/4** | 2/9 |

Overlap trigger (±45 hari, Mode A p10): **7 dari 14 event VDD Multiple punya pasangan di `price_ratio`**, dan **11 dari 14 punya pasangan di `cdd_mult_ma`**.

**Pembacaannya:**
1. `cdd_mult_ma` adalah **twin persis** dari VDD Multiple dengan struktur rasio identik dan **hanya komponen harga yang dilepas**. Presisinya **runtuh dari 35,7% ke 0,0%, recall dari 4/4 ke 0/4.**
2. `price_ratio` — yang **tidak mengandung data umur koin sama sekali** — justru **mengungguli** VDD Multiple (44,4% vs 35,7% presisi, dan hanya 2/9 vs 4/14 event gagal).
3. Kesimpulannya: kemampuan VDD Multiple menandai dasar **cenderung datang dari komponen harga yang tertanam di dalamnya, bukan dari informasi perilaku holder.** Hipotesis kritik terkonfirmasi.

Satu kualifikasi yang harus jujur disebut: **`price_ratio` di sini adalah alat diagnostik, bukan sinyal yang direkomendasikan.** n-nya cuma 5–9 event, angka 80,0% di p5 mode A itu in-sample, dan mode B menurunkannya ke 60,0%. Nilainya sebagai pembanding — bukan sebagai indikator baru.

### 8. Cycle berjalan 2026 (BELUM terkonfirmasi — bukan bukti)

Harga 2026-06-30 = $58.460; hari terakhir data 2026-07-15 = $65.098.

| Seri | p | Trigger | Harga | Max DD 90d |
|---|---|---|---|---|
| `cdd_mult_ma` | 10 | 2026-01-18 | $93.650 | −32,9% |
| `vdd_multiple` | 10 | 2026-02-08 | $70.339 | −8,9% |
| `vdd_multiple` | 5 | 2026-02-14 | $69.816 | −8,2% |
| `vdd_mult_ma` | 10 | 2026-02-22 | $67.658 | −5,3% |
| `vdd_mult_ma` | 5 | 2026-03-07 | $67.257 | −8,1% |
| `sacdd_ma30` | 10 | 2026-03-15 | $72.806 | −16,5% |
| `cdd_mult_ma` | 10 | 2026-04-19 | $73.835 | −20,8% |
| `vdd_multiple` | 10 | 2026-05-15 | $79.064 | **−26,1%** |
| `vdd_multiple` | 5 | 2026-05-16 | $78.177 | **−25,2%** |
| **`vdd_mult_ma`** | **10** | **2026-05-24** | **$77.066** | **−24,1%** |

**`vdd_mult_ma` trigger pada 2026-05-24 — satu hari sebelum video di-upload — diikuti drawdown −24,1% ke $58.460 (2026-06-30).** Ini pola 2018 yang berulang secara live. Jendela 90 hari untuk beberapa event ini masih terpotong data (`truncated=True`), tapi ambang failure ≥20% **sudah terlampaui** di dalam data yang ada, jadi klasifikasinya tidak bergantung pada data yang belum tersedia. **Tetap: low 2026-06-30 belum terkonfirmasi, dan tidak ada satupun angka di section 1–7 yang memakainya.**

---

## Kesimpulan

**Verdict: NOT SUPPORTED untuk B6 dan B7 sebagai sinyal bottom. Kritik confound harga TERKONFIRMASI.**

**n dan sebaran:** VDD Multiple (MA30/MA365) menghasilkan **n = 14 event scoreable** pada Mode A p10, sebaran **cycle-2011 = 3, cycle-2015 = 4, cycle-2018 = 5, cycle-2022 = 2** (relatif merata, tidak didominasi satu cycle). Supply-Adjusted CDD MA30 n = 20 (5/6/5/4). Mode B at-gate menurunkan n ke 10 dan 12. **`sacdd_ma900` n = 8 tapi 7 di antaranya dari cycle-2015 saja dan 0 dari 2011 (warm-up 900 hari) — seri itu efektif satu-cycle dan tidak boleh dipakai sebagai bukti lintas-cycle.** Semua kesimpulan di bawah bersifat kecenderungan, bukan kepastian.

**1. Presisinya rendah dan failure-nya besar.** VDD Multiple menandai ±60 hari bear low pada **35,7% event (Mode A) / 30,0% (Mode B at-gate)** — sekitar dua dari tiga trigger cenderung meleset. Supply-Adjusted CDD MA30 lebih buruk: **10,0% presisi dan hanya menyentuh 2 dari 4 low** (0,0% dan 0/4 pada mode at-gate). Sementara **4 dari 14 event VDD Multiple diikuti drawdown ≥20% dalam 90 hari**, dengan kuartil bawah **−33,0%** dan terburuk **−53,5%**.

**2. Failure mode yang diakui pembicara bukan pengecualian — ia terkonfirmasi dan lebih besar dari pengakuannya.** Di 2018 bukan satu sinyal keliru, tapi **7 trigger berturut-turut selama Sep–Okt 2018**, semuanya diikuti drawdown **46–51%**. Dan yang paling menentukan: di bear low sebenarnya (2018-12-14) persentil trailing VDD Multiple justru **60,0** sementara `cdd_mult_ma` di **99,9** dan `sacdd_ma30` di **98,1**. **Metrik keluarga CDD terbaca sunyi SEBELUM kapitulasi dan kencang TEPAT DI low** — karena kapitulasi itu sendiri adalah koin lama bergerak massal. Membaca "CDD/VDD minimum = dasar" cenderung membaca metriknya terbalik terhadap low.

**3. Confound harga terbukti — ini temuan utamanya.** `vdd_30d_ma` terverifikasi **persis sama** dengan MA30(cdd × price), jadi komponen harga ada secara aljabar. Ketika struktur rasio yang persis sama dipakai **tanpa komponen harga** (`cdd_mult_ma` = MA30(cdd)/MA365(cdd)), presisinya **runtuh dari 35,7% ke 0,0% dan recall dari 4/4 ke 0/4** — konsisten di kedua mode threshold. Sebaliknya benchmark **harga murni** (`MA30(price)/MA365(price)`, tanpa data umur koin sama sekali) justru **mengungguli** VDD Multiple: **44,4% presisi, 4/4 low, 0/5 gagal di p5**. Jadi apa yang dibaca sebagai "LTH berhenti distribusi" cenderung sebagian besar adalah **"harga sedang jauh di bawah rata-rata setahunnya"** — persis seperti hipotesis kritiknya.

**4. Konsisten dengan Validasi 3.** Di sana `sacdd`, `cdd`, dan `vdd_multiple` sudah terbukti membentuk satu klaster redundan (phi +0,408 s/d +0,840), dan `vdd_mult` gagal memisahkan forward return di atas basis K4 (p = 0,514 @90d, p = 0,739 @180d). Validasi 4 menambah alasan mekanisnya: **klaster itu bukan cuma redundan satu sama lain, tapi sebagian besar informasinya adalah harga yang sudah kita punya dari sumber lain.**

**Rekomendasi:** jangan adopsi VDD Multiple maupun Supply-Adjusted CDD sebagai kondisi K4 atau sebagai konfirmasi bottom dalam bentuk apapun. Kalau suatu saat mau memakai metrik keluarga CDD, **wajib pakai versi yang komponen harganya dilepas** (`MA30(cdd)/MA365(cdd)`) supaya tidak menghitung ulang informasi harga sebagai "konfirmasi on-chain" — tapi berdasarkan uji ini versi itu sendiri **presisinya 0,0%**, jadi realistisnya keluarga metrik ini tidak layak dipakai untuk menandai dasar sama sekali.

**Dua hal terpisah yang layak diangkat ke Yudi:**
- **Data:** kolom `vdd_multiple` di `data_master_all_metrics.csv` adalah **rasio HARIAN** (VDD harian ÷ MA365), bukan VDD Multiple versi smoothed yang ditampilkan chart. Usul: catat di `data_dictionary.md` (usulan, bukan penerapan — perubahan KB dikerjakan di project Onchain-Dashboard).
- **Aturan umum:** setiap metrik on-chain yang **value-weighted** (dikalikan harga USD) wajib diuji lawan **twin price-stripped**-nya sebelum diperlakukan sebagai bukti perilaku holder. Template ini bisa dipakai ulang untuk metrik berbasis USD lain (realized cap flows, net realized P/L, dst.).
