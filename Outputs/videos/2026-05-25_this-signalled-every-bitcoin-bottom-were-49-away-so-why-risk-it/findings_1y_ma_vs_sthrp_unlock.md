# Findings — 1-Year Moving Average (klaim B9) vs aturan unlock framework (STH RP cross RP)

**Sumber klaim:** Bitcoin Magazine Pro — "This Signalled Every Bitcoin Bottom — We're 4.9% Away, So Why Risk It" (2026-05-25), klaim B9 `[11:01]`–`[11:11]`
**Tanggal validasi:** 2026-08-06
**Script:** [`analyze_1y_ma_vs_sthrp_unlock.py`](analyze_1y_ma_vs_sthrp_unlock.py)
**Event table:** [`events_1y_ma_vs_sthrp_unlock.csv`](events_1y_ma_vs_sthrp_unlock.csv), [`events_1y_ma_vs_sthrp_headtohead.csv`](events_1y_ma_vs_sthrp_headtohead.csv)
**Data:** `data_master_all_metrics.csv`, window analisis **2011-07-16 s/d 2026-07-15 (n = 5.479 hari)**

---

## Klaim yang diuji

**B9.** *"until we break that kind of one-year moving average around 95 and a half thousand dollars ish... we can't concretely say that this bear market is finished."*

**Kenapa ini bernilai untuk kita terlepas dari kualitas argumen videonya:** Decision Framework v2 §0 punya **aturan unlock sendiri — STH RP (`sth_cost_basis`) cross NAIK melewati RP (`realized_price`) — yang statusnya masih PENDING VALIDASI.** Head-to-head ini menguji aturan kita sendiri sekaligus aturan pembicara, dengan definisi event dan perlakuan konfirmasi yang **identik** supaya adil.

---

## Definisi & parameter (ditetapkan SEBELUM menghitung)

- **`ma365`** = SMA365(`btc_price`), dibangun sendiri. Pembanding: kolom siap pakai **`50_wma`** (350 hari).
- **Reclaim sah:** cross NAIK **pertama SESUDAH bear low** yang **bertahan ≥7 hari berturut-turut**.
- **Anti-lookahead:** konfirmasi "≥7 hari" baru bisa diketahui di hari ke-7. Karena itu dilaporkan **dua tanggal** — tanggal cross (hindsight) dan **tanggal actionable = cross + 6 hari** — dan **semua perhitungan upside memakai tanggal actionable serta harga di tanggal itu**, bukan harga di tanggal cross.
- **Aturan framework** (`sth_cost_basis` cross naik `realized_price`) diuji dengan **konfirmasi 7 hari yang persis sama**.
- **Whipsaw:** cross naik lalu jatuh lagi ke bawah garis dalam **≤30 hari**. Dihitung hanya untuk cross yang terjadi di dalam regime bear.
- **Regime bear** (tiga definisi, semua dilaporkan):
  - **A** = `btc_price` < `realized_price` (785 hari, 14,3%)
  - **B** = `sth_cost_basis` < `realized_price` — "struktur T" (621 hari, 11,3%)
  - **C** = A **atau** B (957 hari, 17,5%)

  ⚠ Regime diuji di hari **i−1** (tepat sebelum cross), bukan di hari cross. Kalau diuji di hari cross, aturan framework otomatis nol-cross di regime-B **secara definisi** — itu artefak, bukan temuan.
- **Ground truth:** bear low terkonfirmasi 2011-11-18, 2015-01-14, 2018-12-14, 2022-11-21. Cycle peak berikutnya untuk hitung sisa upside: 2013-11-30, 2017-12-16, 2021-11-08, 2025-10-06. Low sementara **2026-06-30 ($58.460) BELUM terkonfirmasi** — dilaporkan terpisah, tidak dipakai sebagai bukti.
- **Tidak ada grid search:** konfirmasi 7 hari dan whipsaw 30 hari masing-masing hanya satu varian, ditetapkan di depan. Perbandingan SMA365 vs `50_wma` adalah **cek definisi**, bukan tuning.

### Sanity check anchor 2026-05-25 — semua OK

| Kolom | Nilai | Anchor |
|---|---|---|
| `btc_price` | $77.172,08 | $77.172 ✓ |
| `realized_price` | $54.171,61 | $54.172 ✓ |
| `sth_cost_basis` | $77.909,65 | $77.910 ✓ |
| `lth_cost_basis` | $48.649,79 | $48.650 ✓ |
| `50_wma` | $94.325,20 | $94.325 ✓ |
| `ma365` (SMA365) | **$94.805,02** | pembicara: "95½ ribu-an" — mendekati |

### Ketersediaan data

`btc_price`, `realized_price`, `sth_cost_basis` semua mulai 2010-07-17. SMA365 baru siap **2011-07-16** — **bear low 2011-11-18 masih tercakup**, jadi keempat bear bisa diuji penuh. Tidak ada masalah "data mulai belakangan" di sini.

---

## Hasil

### 1. SMA365 vs `50_wma` — definisi mana yang dipakai pembicara? **Tidak penting**

| Ukuran | Nilai |
|---|---|
| Selisih relatif `ma365` vs `50_wma` | median **−1,30%**, p5 −3,68%, p95 +3,06%, maks abs 8,99% |
| Spearman level | **+0,9998** |
| Hari harga di atas garis | ma365 3.719 hari, 50_wma 3.681 hari |
| **Kesepakatan harian posisi di atas/bawah garis** | **99,09%** dari 5.479 hari |

Tanggal trigger per bear: **identik di 2011 dan 2018**, beda **2 hari di 2015** (2015-10-20 vs 2015-10-22) dan **1 hari di 2022** (2023-03-13 vs 2023-03-14).

**Pilihan definisi tidak mengubah kesimpulan apapun.** Angka pembicara ("94-ish"/"95½ ribu") konsisten dengan kedua definisi ($94.325 dan $94.805 di tanggal video) — tidak ada yang perlu dikoreksi soal angkanya.

### 2 & 3. Head-to-head per bear — reclaim 1Y MA vs STH RP cross RP

Semua angka memakai **tanggal actionable** (cross + 6 hari) dan harga di tanggal itu.

**bear-2011** — low 2011-11-18 @ $2 (peak berikutnya 2013-11-30 @ $1.136)

| Aturan | Cross | Actionable | Hari dr low | Harga act. | Naik dr low | Sisa ke peak |
|---|---|---|---|---|---|---|
| 1Y MA SMA365 | 2012-01-05 | 2012-01-11 | 54 | $7 | +236,5% | +16.360,7% |
| 1Y MA 50_wma | 2012-01-05 | 2012-01-11 | 54 | $7 | +236,5% | +16.360,7% |
| **FW STH RP × RP** | 2012-04-19 | 2012-04-25 | 159 | $5 | +150,4% | +22.017,8% |

**bear-2015** — low 2015-01-14 @ $178 (peak 2017-12-16 @ $19.538)

| Aturan | Cross | Actionable | Hari dr low | Harga act. | Naik dr low | Sisa ke peak |
|---|---|---|---|---|---|---|
| 1Y MA SMA365 | 2015-10-22 | 2015-10-28 | 287 | $305 | +70,7% | +6.312,2% |
| 1Y MA 50_wma | 2015-10-20 | 2015-10-26 | 285 | $287 | +60,8% | +6.709,2% |
| **FW STH RP × RP** | 2015-11-03 | 2015-11-09 | 299 | $380 | +113,1% | +5.037,5% |

**bear-2018** — low 2018-12-14 @ $3.281 (peak 2021-11-08 @ $67.525)

| Aturan | Cross | Actionable | Hari dr low | Harga act. | Naik dr low | Sisa ke peak |
|---|---|---|---|---|---|---|
| 1Y MA SMA365 | 2019-05-03 | 2019-05-09 | 146 | $6.190 | +88,7% | +990,8% |
| 1Y MA 50_wma | 2019-05-03 | 2019-05-09 | 146 | $6.190 | +88,7% | +990,8% |
| **FW STH RP × RP** | 2019-05-07 | 2019-05-13 | 150 | $7.812 | +138,1% | +764,4% |

**bear-2022** — low 2022-11-21 @ $15.774 (peak 2025-10-06 @ $124.715)

| Aturan | Cross | Actionable | Hari dr low | Harga act. | Naik dr low | Sisa ke peak |
|---|---|---|---|---|---|---|
| 1Y MA SMA365 | 2023-03-14 | 2023-03-20 | 119 | $27.809 | +76,3% | +348,5% |
| 1Y MA 50_wma | 2023-03-13 | 2023-03-19 | 118 | $28.044 | +77,8% | +344,7% |
| **FW STH RP × RP** | 2023-03-05 | 2023-03-11 | 110 | $20.620 | +30,7% | +504,8% |

**Ringkasan head-to-head (n = 4 bear):**

| Bear | 1Y-MA act. | FW act. | Selisih hari | Naik dr low 1Y-MA | Naik dr low FW | Selisih |
|---|---|---|---|---|---|---|
| 2011 | 2012-01-11 | 2012-04-25 | **−105** (1Y-MA duluan) | +236,5% | +150,4% | +86,1% |
| 2015 | 2015-10-28 | 2015-11-09 | **−12** (1Y-MA duluan) | +70,7% | +113,1% | −42,4% |
| 2018 | 2019-05-09 | 2019-05-13 | **−4** (1Y-MA duluan) | +88,7% | +138,1% | −49,4% |
| 2022 | 2023-03-20 | 2023-03-11 | **+9** (FW duluan) | +76,3% | +30,7% | +45,6% |

| Ukuran | 1Y MA | Framework (STH RP × RP) |
|---|---|---|
| Median hari sesudah bear low | **133** | 154,5 |
| **Median % naik dari low saat sinyal** | **+82,5%** | **+125,6%** |
| Median sisa upside ke puncak cycle | +3.651,5% | +2.900,9% |

**Bacaannya:** 1Y MA **cenderung sedikit lebih awal** (3 dari 4 bear, median **−8 hari**) dan masuk di harga yang median-nya **43 poin persentase lebih rendah di atas low** (+82,5% vs +125,6%). Tapi sebarannya liar dan arahnya **membalik** antar bear: di 2011 1Y-MA justru masuk **86 poin lebih tinggi**, di 2022 justru framework yang masuk **46 poin lebih rendah**. **Dengan n = 4 dan tanda yang berganti-ganti, tidak ada aturan yang bisa disebut unggul secara timing.** Angka "sisa upside ke puncak" (median 3.651% vs 2.901%) didominasi total oleh 2011 (+16.360% / +22.017%) dan **tidak layak diinterpretasi.**

Satu catatan penting: **kedua aturan sama-sama TELAT.** Median sinyal muncul 4–5 bulan sesudah bear low ketika harga sudah naik 82–126% dari dasar. Keduanya konfirmasi, bukan alat menangkap dasar — sesuai dengan cara framework memperlakukannya.

### 4. Whipsaw — **di sini bedanya tajam, dan ini yang menentukan gate vs context**

| Regime | Aturan | Cross naik | Whipsaw ≤30d | Rate |
|---|---|---|---|---|
| **A** (harga < RP) | 1Y MA SMA365 | 4 | 3 | **75,0%** |
| | 1Y MA 50_wma | 5 | 4 | **80,0%** |
| | FW STH RP × RP | 0 | 0 | — |
| **B** (STH RP < RP) | 1Y MA SMA365 | 6 | 4 | **66,7%** |
| | 1Y MA 50_wma | 7 | 5 | **71,4%** |
| | FW STH RP × RP | 5 | 1 | **20,0%** |
| **C** (A atau B) | **1Y MA SMA365** | **7** | **5** | **71,4%** |
| | 1Y MA 50_wma | 10 | 8 | **80,0%** |
| | **FW STH RP × RP** | **5** | **1** | **20,0%** |

Detail whipsaw 1Y MA (SMA365) di regime-C:

| Cross | Harga | Balik ke bawah | Bertahan |
|---|---|---|---|
| 2011-09-30 | $5 | 2011-10-05 | 5 hari |
| 2012-01-05 | $7 | 2012-01-17 | **12 hari** |
| 2012-01-19 | $6 | 2012-01-25 | 6 hari |
| 2015-10-17 | $272 | 2015-10-18 | 1 hari |
| 2015-10-20 | $271 | 2015-10-21 | 1 hari |

⚠ **Perhatikan baris 2012-01-05: itu cross yang LOLOS konfirmasi 7 hari dan dipakai sebagai "reclaim sah" di section 2 — tapi tetap jatuh lagi ke bawah garis di hari ke-12.** Jadi bahkan filter 7 hari **tidak cukup** untuk aturan ini. (Definisi tidak diubah setelah melihat hasil — ini dilaporkan apa adanya sebagai kelemahan aturan pembicara.)

Semua cross naik STH RP melewati RP sepanjang sejarah (aturan framework, **n = 5 total**):

| Cross | Harga | Nasib |
|---|---|---|
| 2012-04-19 | $5 | bertahan **1.022 hari** (balik 2015-02-05) |
| 2015-11-03 | $405 | bertahan **1.183 hari** (balik 2019-01-29) |
| 2019-05-07 | $5.778 | bertahan **1.274 hari** (balik 2022-11-01) |
| 2023-03-01 | $23.649 | **whipsaw — balik 3 hari kemudian** |
| 2023-03-05 | $22.429 | **masih bertahan sampai akhir data** |

Konteks — sepanjang **seluruh** sejarah tanpa filter regime:

| Aturan | Cross naik | Whipsaw ≤30d | Rate |
|---|---|---|---|
| 1Y MA SMA365 | **35** | 27 | **77,1%** |
| 1Y MA 50_wma | 36 | 27 | 75,0% |
| **FW STH RP × RP** | **5** | 1 | **20,0%** |

**Ini hasil paling tegas dari validasi ini.** 1Y MA cross **35 kali** sepanjang sejarah dengan **77,1% whipsaw** — ia garis yang sangat berisik. Aturan framework cross **5 kali saja** dengan **20% whipsaw**, dan tiga cross yang bertahan bertahan lebih dari **1.000 hari** masing-masing. **1Y MA cenderung layak sebagai context, tidak layak sebagai gate.**

### 5. Status di hari terakhir data (2026-07-15)

| Item | Nilai |
|---|---|
| `btc_price` | **$65.098** |
| SMA365 (`ma365`) | $88.728 → harga **DI BAWAH (−26,6%)** |
| `50_wma` | $87.461 → harga **DI BAWAH (−25,6%)** |
| `realized_price` | $52.740 |
| `sth_cost_basis` | $67.143 → rasio STH RP / RP = **1,273** |
| `lth_cost_basis` | $49.890 |

**Dua aturan sedang bertentangan:**
- **Aturan pembicara (price > 1Y MA): BELUM** — butuh **+36,3%** dari harga sekarang.
- **Aturan framework (STH RP > RP): "NYALA"** — tapi baca peringatan di bawah.

### 5b. ⚠ Aturan unlock framework **belum pernah re-arm di bear ini**

Sejak cycle peak **2025-10-06 (n = 283 hari)**:

| Ukuran | Nilai |
|---|---|
| Hari dengan **STH RP < RP** | **0** |
| Hari dengan **harga < RP** | **0** |
| Rasio STH RP / RP **minimum** | **1,272** (pada 2026-07-13) |

Sebaran hari STH RP < RP sepanjang sejarah: 2011 = 22, 2012 = 109, 2015 = 271, 2019 = 98, 2022 = 61, 2023 = 60 — **dan 2025/2026 = 0.**

**Artinya: aturan unlock framework masih "ON" terus sejak cross 2023-03-05 dan belum pernah mati di bear berjalan.** Aturan yang tidak pernah mati tidak bisa "menyala" — **saat ini ia tidak membawa informasi apapun tentang selesai atau belumnya bear ini.** Ini bukan temuan tentang video, ini temuan tentang framework kita sendiri, dan perlu dibawa ke diskusi terpisah.

Low sementara **2026-06-30 @ $58.460 — BELUM TERKONFIRMASI**, tidak dipakai di angka manapun di atas. Kenaikan dari low sementara ke hari terakhir data: **+11,4%**.

---

## Kesimpulan

**Verdict: PARTIALLY SUPPORTED sebagai context, NOT SUPPORTED sebagai gate.** Dan uji ini justru menemukan masalah yang lebih penting di aturan unlock framework kita sendiri.

**n dan sebaran: n = 4 bear — satu observasi per cycle (2011, 2015, 2018, 2022), tanpa pengulangan dalam cycle yang sama.** Ini sample sekecil yang bisa dibayangkan; tidak ada uji statistik yang dijalankan dan tidak ada yang layak dijalankan. Semua di bawah bersifat kecenderungan, bukan kepastian. Untuk whipsaw n lebih besar (35 cross 1Y MA, 5 cross framework sepanjang 5.479 hari) tapi 5 cross framework tetap tersebar hanya di 4 cycle — **effective n mendekati 4, bukan 5.**

**1. Klaim B9 benar sebagai deskripsi, tidak berguna sebagai aturan.** Di keempat bear, harga memang baru menembus 1Y MA secara bertahan **setelah** bear low lewat — jadi pernyataan "belum bisa dibilang bear selesai sebelum menembus 1Y MA" secara historis tidak pernah salah. Tapi itu **tautologi yang mahal**: sinyalnya datang median **133 hari sesudah low, saat harga sudah +82,5% dari dasar** (rentang +70,7% s/d +236,5%). Sebagai deskripsi keadaan, valid. Sebagai aturan tunggu, ia menunggu sampai sebagian besar pemulihan sudah terjadi.

**2. Sebagai gate, 1Y MA gagal karena whipsaw.** Di regime bear, **5 dari 7 cross naik (71,4%) jatuh lagi ke bawah dalam ≤30 hari** — dan **bahkan cross yang lolos konfirmasi 7 hari (2012-01-05) tetap jatuh lagi di hari ke-12.** Sepanjang seluruh sejarah rate whipsaw-nya **77,1% dari 35 cross**. Aturan framework, dengan definisi dan konfirmasi yang persis sama, cross **hanya 5 kali dengan 20% whipsaw**, dan tiga cross yang bertahan masing-masing bertahan **1.022 / 1.183 / 1.274 hari**. **Perbedaan ini konsisten dan cukup besar untuk disimpulkan dengan yakin: 1Y MA layak sebagai context, bukan gate.**

**3. Head-to-head timing: tidak ada pemenang.** 1Y MA lebih dulu di **3 dari 4 bear** (median **−8 hari**) dan masuk di harga median **+82,5% dari low** vs framework **+125,6%**. Tapi tandanya membalik antar bear (2011: 1Y-MA masuk **86 poin lebih tinggi**; 2022: framework masuk **46 poin lebih rendah**), jadi dengan n = 4 keunggulan median itu tidak bisa dibedakan dari kebetulan. **Yang bisa disimpulkan: keduanya sama-sama telat 4–5 bulan sesudah low, dan itu memang sifat aturan konfirmasi — bukan cacat.**

**4. Pilihan definisi MA tidak relevan.** SMA365 dan `50_wma` sepakat **99,09% dari 5.479 hari** (Spearman +0,9998), tanggal trigger identik di 2 dari 4 bear dan beda 1–2 hari di sisanya. Angka pembicara ("94-ish" / "95½ ribu") cocok dengan keduanya ($94.325 dan $94.805 di 2026-05-25). **Tidak perlu memperdebatkan definisinya.**

**5. Temuan terpenting justru tentang framework kita: aturan unlock STH RP × RP belum pernah re-arm.** Sejak cycle peak 2025-10-06, **STH RP tidak pernah sekalipun turun ke bawah RP — 0 dari 283 hari, rasio minimum 1,272**, dan harga juga tidak pernah turun ke bawah RP (0 hari). Cross naik terakhir terjadi **2023-03-05** dan bertahan sampai sekarang. **Aturan yang tidak pernah mati tidak bisa dipakai sebagai sinyal unlock** — di cycle ini ia strukturnya "sudah ON" sepanjang bear, sehingga informasinya nol. Bandingkan dengan tiga bear sebelumnya di mana regime "STH RP < RP" berlangsung 22–271 hari per bear dan aturannya benar-benar mati lalu hidup lagi.

**Rekomendasi:**
- **1Y MA:** boleh dicatat sebagai **context indicator** (konfirmasi struktur, bukan trigger). Jangan jadikan gate — whipsaw 71–77% terlalu tinggi. Kalau tetap mau dipakai, butuh filter jauh lebih ketat dari 7 hari (bahkan 12 hari pun gagal di 2012), dan itu artinya makin telat lagi.
- **Aturan unlock framework (status: masih PENDING VALIDASI):** hasil validasi ini **mendukung durabilitasnya** (5 cross, 20% whipsaw, tiga cross bertahan >1.000 hari) tapi **mengangkat masalah baru yang serius** — di bear berjalan aturan itu **belum pernah re-arm**. Perlu diangkat ke diskusi di project Onchain-Dashboard: apakah aturan unlock butuh syarat "harus pernah mati dulu" (arming condition) supaya tidak dibaca sebagai konfirmasi palsu ketika ia memang tidak pernah mati. **Ini usulan, bukan penerapan.**
- **Untuk situasi sekarang:** kedua aturan sedang bertentangan (1Y MA butuh +36,3%, aturan framework "ON" tapi tidak informatif). Kesimpulan yang aman: **tidak ada satupun dari dua aturan ini yang sedang memberi sinyal unlock yang bisa dipercaya per 2026-07-15.**
