# Findings — Uji independensi checklist konfluensi 6 metrik

**Sumber klaim:** Bitcoin Magazine Pro — "This Signalled Every Bitcoin Bottom — We're 4.9% Away, So Why Risk It" (2026-05-25), klaim S4 (struktur checklist sepanjang video)
**Tanggal validasi:** 2026-08-06
**Script:** [`analyze_confluence_independence.py`](analyze_confluence_independence.py)
**Event table:** [`events_confluence_independence.csv`](events_confluence_independence.csv), [`events_confluence_incremental.csv`](events_confluence_incremental.csv)
**Data:** `data_master_all_metrics.csv`, 2010-07-17 s/d 2026-07-15 (n = 5.843 hari; n = 5.479 setelah warm-up persentil)

---

## Klaim yang diuji

**S4.** Pembicara memakai checklist 6 metrik sebagai konfluensi bukti bottom: (1) HODL Waves band lama, (2) LTH Supply ATH, (3) Supply Adjusted CDD minimum, (4) VDD Multiple minimum, (5) Whale Shadows agregat minimum, (6) SOPR seller menipis.

**Hipotesis kritik:** keenamnya turunan data **umur koin** yang sama, sehingga 6 "konfirmasi" bukan 6 bukti independen.

Uji ini menjalankan protokol **Governance Decision Framework §1** (independensi |phi| < 0,3), jadi hasilnya generalisable untuk semua pitch "konfluensi" berikutnya — bukan cuma mengkritik video ini.

---

## Definisi & parameter (ditetapkan SEBELUM menghitung)

| Komponen | Kolom | Arah "sinyal nyala" |
|---|---|---|
| HODL Waves band lama | `rc_ge3m` (cara Validasi 1: 100 − 4 band <3 bulan) | tinggi = bullish |
| LTH Supply ATH | `lth_supply_btc` | tinggi = bullish |
| Supply Adjusted CDD | `sacdd = cdd / (lth_supply_btc + sth_supply_btc)` | rendah = bullish |
| VDD Multiple | `vdd_multiple` | rendah = bullish |
| SOPR seller menipis | `asopr` | rendah = bullish |
| **Whale Shadows** | **TIDAK ADA** | proxy `cdd` mentah |

- **Threshold DITETAPKAN DI DEPAN:** persentil **≤10** untuk arah rendah, **≥90** untuk arah tinggi. **Tidak ada grid search, tidak ada varian lain yang dicoba.**
- **Anti-lookahead:** persentil dihitung **trailing 4 tahun** (window berakhir di hari itu, `min_periods` 365). Forward return diukur SESUDAH tanggal flag.
- **phi** = korelasi Pearson antar dua variabel biner; ambang Governance |phi| ≥ 0,30.
- **Pembanding K4** (Decision Framework v2): (i) `lth_mvrv` < 1,0; (ii) `asopr` < 0,93 **DAN** `lth_sopr` < 0,50; (iii) `percent_btc_in_profit` < 50% **DAN** `pct_sth_in_profit` < 10%; (iv) `btc_price/cvdd` < 1,10.
- ⚠ Kolom `realized_cap_1w` & `realized_cap_1_2y` **sengaja dikeluarkan** dari `rc_ge3m` (duplikat input RHODL).

### Komponen ke-6: NEEDS-DATA-WE-DONT-HAVE

**Whale Shadows / Revived Supply tidak ada di `data_master_all_metrics.csv` maupun di data dictionary** — dictionary secara eksplisit menyebut "Whale/entity metrics" sebagai kategori yang tidak kita punya. Yang dipakai di sini `cdd` mentah sebagai **stand-in berlabel PROXY**; ini bukan rekonstruksi metriknya, dan setiap kesimpulan yang menyangkut komponen ini harus dibaca sebagai indikatif saja.

**Sanity check anchor 2026-05-25 — semua OK:** btc_price $77.172, asopr 1,0056, lth_mvrv 1,5863, lth_sopr 1,2587, percent_btc_in_profit 61,82%, rc_ge3m 83,631% (cocok dengan Validasi 1).

**Ketersediaan data:** semua kolom mulai 2010-07-17 (`cdd` & `vdd_multiple` malah 2009-01-03). **Uji lintas 4 cycle penuh mungkin.**

---

## Hasil

### 1. Korelasi Spearman atas level harian — di sini hipotesis kritiknya kuat

Semua komponen sudah diarahkan "besar = bullish-bottom":

| | hodl_ge3m | lth_supply | sacdd | vdd_mult | asopr | cdd_proxy |
|---|---|---|---|---|---|---|
| **hodl_ge3m** | 1,000 | 0,521 | 0,160 | 0,474 | 0,437 | 0,026 |
| **lth_supply** | 0,521 | 1,000 | −0,169 | 0,182 | 0,099 | −0,426 |
| **sacdd** | 0,160 | −0,169 | 1,000 | **0,747** | 0,339 | **0,939** |
| **vdd_mult** | 0,474 | 0,182 | **0,747** | 1,000 | **0,625** | **0,600** |
| **asopr** | 0,437 | 0,099 | 0,339 | **0,625** | 1,000 | 0,265 |
| **cdd_proxy** | 0,026 | −0,426 | **0,939** | **0,600** | 0,265 | 1,000 |

**Rata-rata |ρ| pairwise (15 pasang) = 0,401**, maks 0,939, min 0,026.

Per cycle — **stabil, bukan artefak satu periode**:

| Cycle | n | Rata-rata \|ρ\| | Maks |
|---|---|---|---|
| 2011 | 899 | 0,363 | 0,958 |
| 2015 | 1.461 | 0,422 | 0,982 |
| 2018 | 1.461 | 0,522 | 0,998 |
| 2022 | 1.461 | 0,433 | 1,000 |
| 2026 | 561 | 0,402 | 1,000 |

**Di level harian, hipotesis kritik terkonfirmasi kuat.** Yang paling telanjang: `sacdd` vs `cdd_proxy` ρ = 0,939 — benar secara aljabar (`sacdd` = `cdd` dibagi supply yang bergerak lambat), jadi keduanya praktis metrik yang sama. `vdd_multiple` juga terikat ke keduanya (0,747 dan 0,600). **Tiga dari enam komponen adalah satu klaster CDD.**

### 2. Flag biner + matriks phi — checklist pembicara

Frekuensi flag nyala (n = 5.479 hari valid, 2011-07-16 s/d 2026-07-15):

| Komponen | Hari nyala | % |
|---|---|---|
| hodl_ge3m | 769 | 14,04% |
| **lth_supply** | **3.344** | **61,03%** |
| sacdd | 378 | 6,90% |
| vdd_mult | 578 | 10,55% |
| asopr | 489 | 8,92% |
| cdd_proxy | 272 | 4,96% |

**Temuan sampingan yang penting: flag "LTH Supply ATH" nyala 61% dari seluruh hari.** `lth_supply_btc` adalah seri yang **trending naik secara struktural**, jadi persentil trailing-nya hampir selalu tinggi. Komponen yang benar 61% dari waktu praktis **tidak membawa informasi** apapun tentang bottom, terlepas dari korelasinya.

Matriks phi:

| | hodl_ge3m | lth_supply | sacdd | vdd_mult | asopr | cdd_proxy |
|---|---|---|---|---|---|---|
| **hodl_ge3m** | 1,000 | 0,253 | 0,058 | 0,173 | 0,148 | 0,021 |
| **lth_supply** | 0,253 | 1,000 | 0,037 | 0,087 | 0,062 | 0,017 |
| **sacdd** | 0,058 | 0,037 | 1,000 | **0,462** | −0,073 | **0,840** |
| **vdd_mult** | 0,173 | 0,087 | **0,462** | 1,000 | 0,053 | **0,408** |
| **asopr** | 0,148 | 0,062 | −0,073 | 0,053 | 1,000 | −0,063 |
| **cdd_proxy** | 0,021 | 0,017 | **0,840** | **0,408** | −0,063 | 1,000 |

**Pasangan dengan |phi| ≥ 0,30: 3 dari 15** — semuanya di dalam klaster CDD:
- `sacdd` vs `cdd_proxy` = **+0,840**
- `sacdd` vs `vdd_mult` = **+0,462**
- `vdd_mult` vs `cdd_proxy` = **+0,408**

**Rata-rata |phi| checklist pembicara = 0,184.**

### 3. Pembanding K4

Frekuensi kondisi K4 nyala:

| Kondisi | Hari | % |
|---|---|---|
| k4_lth_mvrv (<1,0) | 680 | 12,41% |
| k4_sopr (aSOPR<0,93 & LTH-SOPR<0,50) | 52 | 0,95% |
| k4_supply (SiP<50% & STH profit<10%) | 171 | 3,12% |
| k4_cvdd (Price/CVDD<1,10) | 103 | 1,88% |

| | k4_lth_mvrv | k4_sopr | k4_supply | k4_cvdd |
|---|---|---|---|---|
| **k4_lth_mvrv** | 1,000 | 0,186 | 0,184 | **0,368** |
| **k4_sopr** | 0,186 | 1,000 | 0,134 | 0,180 |
| **k4_supply** | 0,184 | 0,134 | 1,000 | 0,215 |
| **k4_cvdd** | **0,368** | 0,180 | 0,215 | 1,000 |

**Pasangan |phi| ≥ 0,30: 1 dari 6** (`k4_lth_mvrv` vs `k4_cvdd` = +0,368). **Rata-rata |phi| K4 = 0,211.**

### 4. Verdict independensi — hasil NEGATIF terhadap hipotesis kritik versi kerasnya

| Set | Rata-rata \|phi\| | Pasang ≥0,30 |
|---|---|---|
| Checklist pembicara | **0,184** | 3 dari 15 |
| K4 framework | **0,211** | 1 dari 6 |

**Diukur dengan rata-rata |phi| flag biner, checklist pembicara TIDAK lebih berkorelasi-internal dibanding K4** (rasio 0,87x). Ini **hasil negatif terhadap hipotesis kritik** dan dilaporkan apa adanya — tidak ada definisi yang diubah untuk membalikkannya.

Tiga hal yang harus dibaca bersama angka ini supaya tidak menyesatkan:

1. **Rata-rata menyembunyikan struktur klaster.** 15 pasang checklist mencakup banyak pasangan mendekati nol dari trio yang relatif independen (hodl_ge3m, lth_supply, asopr). Yang penting bukan rata-ratanya tapi bahwa **3 dari 6 komponen membentuk satu klaster redundan** (|phi| 0,408–0,840). Realistisnya checklist "6 metrik" ini berisi **~4 sinyal berbeda**, dan salah satunya (lth_supply) nyala 61% waktu sehingga informasinya mendekati nol → efektifnya **~3 sinyal**.
2. **phi tertekan oleh base rate yang jauh berbeda.** Flag K4 jauh lebih jarang (0,95%–12,4%) daripada flag checklist (4,96%–61,0%). Pada base rate rendah, phi maksimum yang bisa dicapai dua flag secara matematis lebih terbatas — jadi perbandingan langsung rata-rata |phi| antara dua set dengan frekuensi sangat berbeda **bukan apple-to-apple**. Kesimpulan yang aman: **K4 tidak terbukti lebih baik maupun lebih buruk lewat metrik ini.**
3. **Di level harian (bukan flag), checklist jauh lebih terikat** — rata-rata |ρ| 0,401, konsisten 0,36–0,52 di kelima potongan cycle. Struktur "satu keluarga data umur koin" itu nyata; yang tidak terbukti adalah bahwa hal itu membuat flag-nya menyala bersamaan lebih sering dibanding K4.

### 5. Uji inkremental (Governance lapis 3) — di sini checklist gagal telak

Basis uji: hari-hari di mana **K4 count ≥2**, **n = 171 hari**.

| Cycle | n | Rentang |
|---|---|---|
| 2011 | 16 | 2011-10-19 .. 2012-04-03 |
| 2015 | 30 | 2015-01-03 .. 2015-08-25 |
| 2018 | 48 | 2018-11-22 .. 2020-03-12 |
| 2022 | 77 | 2022-08-30 .. 2023-01-10 |

⚠ **Independensi sample:** 171 hari itu bukan 171 observasi independen. Mereka mengelompok jadi **10 episode kontinu**, dan praktis hanya **4 cluster cycle** — didominasi 2022 (77 hari, 45%) dan 2018 (48 hari, 28%). Effective n mendekati 4, bukan 171.

Hasil (Mann-Whitney U dua sisi; flag at-gate, forward return diukur sesudahnya):

| Komponen | Horizon | n ON | n OFF | Median ON | Median OFF | Selisih | p | Memisahkan? |
|---|---|---|---|---|---|---|---|---|
| hodl_ge3m | 90d | 116 | 55 | 33,7% | 40,5% | −6,8% | 0,600 | tidak |
| hodl_ge3m | 180d | 116 | 55 | 59,6% | 169,7% | **−110,2%** | <0,001 | YA *(arah salah)* |
| lth_supply | 90d | 147 | 24 | 31,1% | 52,3% | **−21,1%** | <0,001 | YA *(arah salah)* |
| lth_supply | 180d | 147 | 24 | 63,2% | 193,6% | **−130,3%** | <0,001 | YA *(arah salah)* |
| sacdd | 90d/180d | 15 | 156 | — | — | — | — | n terlalu kecil |
| vdd_mult | 90d | 38 | 133 | 33,1% | 36,6% | −3,5% | 0,514 | tidak |
| vdd_mult | 180d | 38 | 133 | 70,9% | 72,3% | −1,4% | 0,739 | tidak |
| asopr | 90d | 97 | 74 | 29,0% | 47,3% | **−18,3%** | 0,003 | YA *(arah salah)* |
| asopr | 180d | 97 | 74 | 72,0% | 74,4% | −2,4% | 0,969 | tidak |
| cdd_proxy | 90d/180d | 12 | 159 | — | — | — | — | n terlalu kecil |

**4 dari 12 uji signifikan (p<0,05), dan keempatnya lolos koreksi Bonferroni (α = 0,0042) — tapi SEMUANYA berarah salah.** Setiap komponen yang benar-benar memisahkan forward return justru memisahkannya ke arah **lebih rendah** saat flag menyala. Contoh paling ekstrem: saat `lth_supply` nyala, median forward return 180 hari 63,2% vs 193,6% saat mati.

Penjelasan mekanisnya konsisten dengan Validasi 1: **komponen-komponen ini lagging.** `rc_ge3m` puncaknya muncul setelah bear low lewat (Validasi 1 menemukan episode 147 hari di 2015 yang mulai 4 bulan sesudah low). `lth_supply` mencapai puncaknya di akhir fase akumulasi. Jadi ketika flag-nya nyala, sebagian besar pergerakan naik dari dasar sudah terjadi — sisa upside-nya lebih kecil. **Menambahkannya ke K4 bukan cuma tidak membantu, tapi cenderung menunda deploy ke titik yang lebih buruk.**

Dua komponen (`sacdd`, `cdd_proxy`) tidak bisa diuji karena hanya nyala 12–15 hari dari 171 hari basis — **n terlalu kecil, bukan hasil negatif maupun positif.**

---

## Kesimpulan

**Verdict: tidak satupun dari 5 komponen pembicara yang layak ditambahkan ke K4.** Uji inkremental Governance lapis 3 gagal total: dari 12 uji (5 komponen × 2 horizon, 2 komponen tidak bisa diuji karena n<20), **4 memisahkan secara signifikan dan lolos Bonferroni — tapi keempatnya ke arah yang salah**, yaitu forward return justru **lebih rendah** saat flag menyala (`lth_supply` −21,1% @90d dan −130,3% @180d; `hodl_ge3m` −110,2% @180d; `asopr` −18,3% @90d). Konsisten dengan sifat lagging metrik-metrik ini: saat sinyalnya nyala, sebagian besar pergerakan dari dasar sudah lewat.

**Hipotesis kritik "6 konfirmasi bukan 6 bukti independen" terkonfirmasi sebagian.** Di level harian keenamnya memang saling terikat kuat — rata-rata |ρ| Spearman **0,401**, stabil 0,36–0,52 di kelima potongan cycle — dan **tiga dari enam (Supply-Adjusted CDD, VDD Multiple, CDD proxy) membentuk satu klaster redundan** dengan |phi| 0,408 sampai **0,840**. Ditambah fakta bahwa flag "LTH Supply ATH" **nyala 61% dari seluruh hari** (serinya trending naik secara struktural, jadi persentil trailing-nya hampir selalu tinggi), checklist "6 metrik" ini realistisnya berisi **sekitar 3 sinyal yang benar-benar berbeda**.

**Tapi versi keras hipotesisnya TIDAK terbukti — hasil negatif, dilaporkan apa adanya.** Diukur dengan rata-rata |phi| flag biner, checklist pembicara justru **0,184 vs K4 0,211** — jadi checklist **tidak terukur lebih berkorelasi-internal** dibanding K4 (rasio 0,87x). Perbandingan ini perlu dibaca hati-hati karena base rate kedua set sangat berbeda (flag K4 0,95%–12,4%, flag checklist 4,96%–61,0%) sehingga phi K4 tertekan naik secara mekanis. Kesimpulan yang aman: **K4 tidak terbukti lebih independen lewat metrik ini** — dan itu sendiri catatan berguna untuk framework kita sendiri, karena pasangan `k4_lth_mvrv` vs `k4_cvdd` juga melewati ambang di **+0,368**.

**n dan sebaran:** matriks korelasi dihitung atas **n = 5.479 hari (2011-07-16 s/d 2026-07-15)** setelah warm-up persentil, mencakup 4 cycle penuh — tidak ada masalah data yang mulai belakangan. Uji inkremental berjalan atas **n = 171 hari** dengan K4 count ≥2, tapi hari-hari itu mengelompok jadi **10 episode kontinu dan praktis hanya 4 cluster cycle** (2011 n=16, 2015 n=30, 2018 n=48, 2022 n=77 — 2022 & 2018 sendiri 73%). Effective n karena itu mendekati 4, bukan 171 — seluruh temuan uji inkremental cenderung, bukan pasti.

**Komponen ke-6 (Whale Shadows / Revived Supply) = NEEDS-DATA-WE-DONT-HAVE.** Tidak ada di data master maupun data dictionary. Yang dipakai `cdd` mentah berlabel proxy — dan proxy itu ternyata masuk klaster redundan bersama `sacdd` (phi +0,840), yang setidaknya memberi indikasi bahwa metrik keluarga CDD apapun cenderung tidak menambah bukti baru.

**Yang bisa dibawa keluar sebagai aturan umum (ini nilai utama validasi ini):** setiap pitch "konfluensi N metrik" ke depan harus lewat tiga lapis yang sama — (1) korelasi level harian, (2) phi antar flag biner dengan threshold ditetapkan di depan, (3) uji inkremental di atas basis sinyal yang sudah ada. Video ini gagal di lapis 3 meskipun lolos-tipis di lapis 2, dan itu urutan kegagalan yang cenderung berulang: metrik yang berkorelasi ringan tapi lagging akan tampak "menambah konfirmasi" padahal ia hanya mengulang informasi lama dengan jeda.

**Rekomendasi:** jangan adopsi satupun komponen sebagai kondisi K4. Catat protokol tiga-lapis di atas sebagai template uji konfluensi standar. Terpisah dari itu, angkat ke diskusi dengan Yudi: pasangan K4 `lth_mvrv<1,0` vs `Price/CVDD<1,10` punya **phi +0,368** (di atas ambang Governance 0,30) — ini temuan tentang framework kita sendiri, bukan tentang video, dan layak dicek ulang di project Onchain-Dashboard.
