# Findings — Clustering shock & profil peluruhan volatility

**Insight asal:** B-5 (shock datang berkelompok) + B-6 (decay volatility pasca-shock ~10-20 hari)
**Sumber:** Look Into Bitcoin, "Bitcoin News Doesn't Actually Move The Price" (2026-08-15), `[03:10]`–`[03:58]`, `[06:06]`–`[08:07]`
**Script:** [`analyze_shock_clustering_decay.py`](analyze_shock_clustering_decay.py) (+ helper [`shock_zone_lib.py`](shock_zone_lib.py))
**Event table:** [`events_shock_clustering.csv`](events_shock_clustering.csv)
**Tanggal validasi:** 2026-08-20

---

## Definisi event

Sama persis dengan [`findings_shock_distribution_by_zone.md`](findings_shock_distribution_by_zone.md): PRIMARY `|log ret| >= 3 × vol30 at-gate`, VARIAN `|log ret| >= 8%` fixed. Dua varian saja.

Sebaran shock PRIMARY per cycle: **C1 n=61 · C2 n=43 · C3 n=32 · C4 n=34** (total 170; 139 sejak 2013). Merata, tidak ada dominasi era.

---

## Q1/Q2 — Clustering: P(shock lagi dalam h hari | hari ini shock)

Klaim video untuk BTC: **47% vs 29%** (horizon 5 hari).

Baseline dihitung dua cara sesuai permintaan: **(a) unconditional shock rate**, dan **(b) block-shuffle yang mempertahankan jumlah shock per tahun** — supaya komposisi era tidak terhitung sebagai clustering.

| Scope | Definisi | h | n shock | P(cond) | base (a) | base (b) shuffle | lift vs (b) |
|---|---|---:|---:|---:|---:|---:|---:|
| Full 2010-2026 | PRIMARY | 5 | 170 | 25,3% [19-32] | 12,5% | 13,4% [9-18] | **+11,9pp** |
| Full 2010-2026 | PRIMARY | 10 | 170 | 35,3% [29-43] | 22,6% | 25,0% [19-31] | +10,3pp |
| ≥2013 | PRIMARY | 5 | 139 | 25,9% [19-34] | 12,1% | 13,0% [8-18] | **+12,9pp** |
| ≥2013 | PRIMARY | 10 | 139 | 36,0% [28-44] | 21,8% | 24,5% [18-31] | +11,5pp |
| ≥2013 | VARIAN 8% | 5 | 269 | 53,5% [48-59] | 19,6% | 36,5% [32-41] | +17,1pp |
| ≥2013 | VARIAN 8% | 10 | 269 | 67,7% [62-73] | 30,1% | 55,4% [52-59] | +12,2pp |

**Robustness — buang efek trivial "shock kemarin → shock hari ini"** dengan menghitung shock lain hanya di window t+2..t+h (t+1 dikeluarkan), PRIMARY, ≥2013:

| Window | n | P(cond) | base (hari acak) | lift |
|---|---:|---:|---:|---:|
| t+2..t+5 | 139 | 14,4% | 9,9% | +4,5pp |
| t+2..t+10 | 139 | 27,3% | 20,0% | +7,4pp |

**Hasil: clustering cenderung DIDUKUNG secara arah, tapi magnitudonya lebih kecil dari yang ditampilkan video.** Lift +11,9pp s/d +12,9pp terhadap baseline shuffle (bukan +18pp seperti 47% vs 29% di video), dan setelah membuang hari langsung-berturutan lift-nya tinggal **+4,5pp di horizon 5 hari**. Artinya sebagian besar "clustering" adalah fenomena 1-2 hari berdekatan, bukan gelombang seminggu.

Catatan penting soal baseline: perbedaan antara base (a) dan base (b) besar sekali di varian 8% (19,6% vs 36,5%) — itu bukti langsung bahwa **komposisi era menyumbang porsi besar dari "clustering" kalau baseline-nya naif.** Angka video kemungkinan memakai baseline gaya (a). Dengan baseline yang benar, efeknya menyusut kira-kira setengahnya.

## Q3 — Profil peluruhan volatility pasca-shock

Rata-rata `|log return|` harian di t+1..t+30, dinormalisasi ke mean `|log return|` trailing 90 hari **at-gate** (1,0 = hari normal). Ambang yang diminta: 1,2×.

**≥2013, PRIMARY, n=139:**

| k (hari setelah shock) | 0 | 1 | 2 | 3 | 4 | 5 | 7 | 10 | 14 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mean | 5,26 | 2,23 | 1,63 | 1,24 | 1,59 | 1,90 | 1,80 | 1,24 | 1,68 | 1,26 | 1,15 |
| median | 4,71 | 1,45 | 1,08 | 0,88 | 1,02 | 1,24 | 1,20 | 0,89 | 0,98 | 0,74 | 0,71 |
| mean smooth-5 | 3,04 | 2,59 | 2,39 | 1,72 | 1,63 | 1,66 | 1,65 | 1,35 | 1,53 | 1,41 | 1,27 |

Hari pertama mean turun di bawah 1,2× = **k=26**. Hari pertama median turun di bawah 1,2× = **k=2**. Versi smooth-5 **tidak pernah** turun di bawah 1,2× dalam 30 hari.

**Hasil: klaim B-6 versi "flat setelah ~20 hari" cenderung TIDAK didukung dalam bentuk yang bersih.** Kurvanya jauh lebih berisik dari yang ditampilkan video: turun tajam di k=1-3, lalu **naik lagi** di k=4-7 (1,59-1,90×), turun di k=10, naik lagi di k=14. Ini konsisten dengan clustering (Q1) — shock susulan muncul justru di minggu pertama-kedua, bukan peluruhan mulus.

Jurang antara mean dan median adalah temuan tersendiri: **median sudah kembali normal di k=2-3, tapi mean tetap tinggi sampai k>25.** Artinya *tipikal* hari setelah shock sudah tenang dengan cepat; yang membuat rata-rata tinggi adalah minoritas kasus yang berlanjut jadi episode panjang. Untuk manajemen risiko, mean-lah yang relevan — **horizon stres yang aman untuk diasumsikan adalah ~3-4 minggu, bukan 2 minggu seperti kesan dari video.**

**Q4 — Decay per zona shock (≥2013, PRIMARY):**

| Grup zona | n | k=1 | k=3 | k=5 | k=10 | k=20 | k=30 | pertama <1,2× (mean) |
|---|---:|---|---|---|---|---|---|---|
| ZC/Z1/Z1b (bawah) | 15 | 3,13 | 1,58 | 1,66 | 1,44 | 0,90 | 0,97 | k=8 |
| ZD/Z3 (tengah) | 78 | 1,80 | 0,95 | 2,05 | 1,29 | 1,20 | 1,10 | k=3 |
| Z4/Z5 (atas) | 38 | 2,63 | 1,67 | 1,58 | 1,08 | 1,62 | 1,26 | k=10 |

**n=15 untuk grup bawah — terlalu kecil untuk kesimpulan.** Yang bisa disebut: tidak ada tanda bahwa peluruhan di zona bawah lebih lama dari zona atas; kalau ada, arahnya justru sebaliknya (bawah pulih di k=8, atas di k=10). Tapi dengan n segini, ini tidak bisa dipakai.

**Decay per arah shock (≥2013):** DOWN-shock (n=66) turun di bawah 1,2× di k=3; UP-shock (n=73) di k=11. Versi smooth: DOWN k=18, UP tidak pernah. Tidak ada pola yang cukup stabil untuk dipegang.

## Q5 — Kondisional setelah satu hari turun ≥10% (yang paling actionable untuk LTV)

n hari (≥2013) = **65**, setelah merge cooldown 5 hari = **49 episode**.

**Sebaran per cycle sangat timpang: C1 n=15 · C2 n=18 · C3 n=15 · C4 n=1.** Hanya **satu** kejadian −10%/hari di cycle berjalan (2022-2026). Ini pembatas terbesar dari validasi ini dan wajib dibaca sebelum angka apapun di bawah.

Drawdown kumulatif terburuk setelah hari −10% (versi episode, n=49):

| Horizon | p50 | p80 | p95 | worst |
|---|---|---|---|---|
| 5 hari | −3,8% | −13,0% | −24,0% | −49,8% |
| 10 hari | −5,0% | −19,5% | −30,9% | −58,4% |

Pembanding hari acak (≥2013, n=4.943):

| Horizon | p50 | p80 | p95 | worst |
|---|---|---|---|---|
| 5 hari | −1,7% | −6,1% | −14,3% | −61,0% |
| 10 hari | −3,0% | −9,4% | −20,0% | −70,3% |

**Setelah hari −10%, ekor kirinya kira-kira 1,7× lebih dalam dari hari acak di p95** (−24,0% vs −14,3% di 5 hari). Efeknya nyata tapi tidak dramatis.

**Implikasi LTV — kondisional setelah sudah kena −10% sehari, berapa sering LTV terdorong ke rung berikutnya dalam 10 hari:**

| Dari cap | ke 58% | ke 60% | ke 65% |
|---|---|---|---|
| **45%** | butuh −22,4% lagi → **20%** kejadian | −25,0% → 15% | −30,8% → 8% |
| **48%** | butuh −17,2% lagi → **25%** kejadian | −20,0% → 23% | −26,2% → 12% |

**Ini angka yang paling penting dari seluruh validasi ini:** sekali BTC mencetak hari −10%, **kalau posisi ada di cap 45%, sekitar 1 dari 5 kejadian akan mendorong LTV menembus 58% dalam 10 hari berikutnya. Di cap 48%, sekitar 1 dari 4.** Basisnya n=49 episode dengan hanya 1 di cycle berjalan.

---

## Kesimpulan

**B-5 (clustering) cenderung DIDUKUNG secara arah tapi magnitudonya kira-kira setengah dari yang ditampilkan video** — lift +12,9pp terhadap baseline shuffle (≥2013, h=5, n=139), menyusut ke +4,5pp setelah hari langsung-berturutan dibuang. Selisih besar antara baseline naif dan baseline shuffle (19,6% vs 36,5% di varian 8%) menunjukkan angka video kemungkinan melebih-lebihkan efeknya karena baseline yang tidak mengontrol komposisi era.

**B-6 (peluruhan bersih ~10-20 hari) cenderung TIDAK didukung.** Kurva mean naik-turun sampai k>25 dan baru turun di bawah 1,2× di k=26 (n=139); versi smooth tidak pernah. Median memang pulih cepat (k=2), jadi kesimpulan yang jujur: *tipikal* hari setelah shock cepat tenang, tapi ekornya panjang. Horizon stres yang layak diasumsikan **~3-4 minggu, bukan 2 minggu**.

**Sebaran per cycle:** shock PRIMARY merata (61/43/32/34), tapi analisis −10%/hari sangat timpang (15/18/15/**1**) — hasil Q5 praktis merepresentasikan tiga cycle lama, hampir tidak ada dari cycle berjalan. Baca semua angka LTV di Q5 sebagai batas atas historis, bukan estimasi untuk kondisi sekarang.

**Yang tidak bisa dijawab:** perbedaan peluruhan antar zona (n=15 di grup bawah), dan replikasi angka spesifik video 47%/29% (definisi shock presenter tidak diungkap, jadi bukan perbandingan apple-to-apple).
