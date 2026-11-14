# Findings — Distribusi shock day per zona v2

**Insight asal:** B-7 — "Shock terbesar terkonsentrasi saat harga sedang jatuh"
**Sumber:** Look Into Bitcoin, "Bitcoin News Doesn't Actually Move The Price" (2026-08-15), `[08:54]`–`[09:41]`
**Script:** [`analyze_shock_distribution_by_zone.py`](analyze_shock_distribution_by_zone.py) (+ helper [`shock_zone_lib.py`](shock_zone_lib.py))
**Event table:** [`events_shock_by_zone.csv`](events_shock_by_zone.csv)
**Tanggal validasi:** 2026-08-20

---

## Definisi event (dikunci sebelum menghitung)

- `r_t = ln(P_t / P_t-1)`
- `vol_t = std(r, 30 hari yang berakhir di t-1)` — **at-gate**, hari shock dikeluarkan dari window vol (anti lookahead)
- **PRIMARY:** shock jika `|r_t| >= 3 * vol_t`
- **VARIAN (satu-satunya pembanding):** shock jika `|r_t| >= 8%` fixed
- Hanya 2 varian dites. Tidak ada varian ketiga — sesuai aturan anti-overfit.
- Untuk pertanyaan ini dipakai **shock day** (flag harian mentah), bukan event-merged, karena pertanyaannya memang tentang *kepadatan hari* per zona. Merge cooldown 5 hari dipakai di validasi lain.
- Zona v2 mengikuti tabel Decision Framework v2 §1 persis (struktur N/C/T × posisi harga vs RP / STH RP / AVIV Mean / AVIV Upper). **Sanity check lolos:** implementasi menghasilkan tepat **703 hari Z5**, angka yang sama yang tercatat di framework v2 §1.

## Sample

Total periode 2010-07-17 s/d 2026-07-15 = 5.843 hari. Shock PRIMARY = **170 hari** (2,91 per 100 hari).

Sebaran per cycle: **C1 2010-15 n=61 · C2 2015-18 n=43 · C3 2018-22 n=32 · C4 2022-26 n=34.**
Tidak ada cycle yang mendominasi (maks 36%). Porsi shock pra-2013 = 18,2% dari total (31 dari 170), sementara porsi hari pra-2013 = 15,4% — jadi era awal hanya sedikit over-represented, tidak distortif. Semua tabel di bawah juga dilaporkan versi ≥2013 (n=139 shock).

---

## Q1 — Shock per 100 hari per zona (≥2013, PRIMARY)

| Zona | hari | shock | per 100 hari | down | up | down:up | % down |
|---|---:|---:|---:|---:|---:|---:|---:|
| ZC (capitulation) | 211 | 8 | 3,79 | 7 | 1 | 7,00 | 88% |
| ZD (dip dalam) | 1.451 | 45 | 3,10 | 33 | 12 | 2,75 | 73% |
| Z1 (bear bottom) | 298 | 4 | 1,34 | 4 | 0 | ∞ | 100% |
| Z1b | 68 | 3 | 4,41 | 0 | 3 | 0,00 | 0% |
| Z2 (konvergensi) | 94 | 4 | 4,26 | 1 | 3 | 0,33 | 25% |
| Z2t | 80 | 4 | 5,00 | 0 | 4 | 0,00 | 0% |
| Z3 | 1.377 | 33 | 2,40 | 6 | 27 | 0,22 | 18% |
| Z4 | 662 | 21 | 3,17 | 12 | 9 | 1,33 | 57% |
| Z5 | 703 | 17 | 2,42 | 3 | 14 | 0,21 | 18% |

Digrupkan (≥2013, PRIMARY):

| Grup | hari | shock | per 100 hari | down | up |
|---|---:|---:|---:|---:|---:|
| BEAR BAWAH (ZC/Z1/Z1b) | 577 | 15 | 2,60 | 11 | 4 |
| MID (ZD/Z3) | 2.828 | 78 | 2,76 | 39 | 39 |
| ATAS (Z4/Z5) | 1.365 | 38 | 2,78 | 15 | 23 |

**Hasil Q1: klaim B-7 versi "frekuensi" cenderung TIDAK didukung.** Setelah dinormalisasi ke panjang zona, kepadatan shock praktis **datar** lintas grup zona: 2,60 vs 2,76 vs 2,78 per 100 hari. Zona bawah bukan tempat shock lebih sering. Zona dengan rate tertinggi justru Z2t (5,00) dan Z1b (4,41) — dua zona transisi pendek dengan n=3-4, jadi angkanya tidak berarti apa-apa.

Varian fixed 8% memberi gambaran berbeda dan lebih dekat ke narasi video: ZC 10,43 per 100 hari vs Z3 4,07 vs Z1 3,02. Ini **ekspektasi mekanis**, bukan temuan: ambang absolut 8% otomatis lebih sering tersentuh di lingkungan volatility tinggi (ZC), sementara ambang 3× vol30 menyesuaikan diri dengan volatility kontemporer. Perbedaan dua definisi ini sendiri yang informatif: **shock "besar dalam ukuran absolut" memang menumpuk di capitulation; shock "besar relatif terhadap kondisi saat itu" tidak.**

## Q2 — Arah shock (down vs up) per zona

Di sinilah zona benar-benar membedakan, dan sangat kuat:

- **ZC: 88% down** (7 dari 8), ZD: 73% down (33 dari 45), Z1: 100% down (4 dari 4)
- **Z3: 18% down** (6 dari 33), **Z5: 18% down** (3 dari 17), Z2t: 0% down (0 dari 4)
- Z4 di tengah: 57% down (12 dari 21)

Rasio down:up bergerak dari **7,0 di ZC** ke **0,21 di Z5**. Pola ini konsisten di kedua definisi shock (varian 8%: ZC 2,14 vs Z5 0,30) dan di full-history maupun ≥2013.

**Hasil Q2: versi terkoreksi dari B-7 cenderung DIDUKUNG.** Yang benar bukan "shock lebih sering saat harga jatuh", tapi **"probabilitas shock berikutnya mengarah ke bawah sangat bergantung zona"**. Di zona bawah shock hampir selalu ke bawah; di zona atas hampir selalu ke atas. Ini konsisten dengan volatility clustering + arah trend, dan tidak butuh penjelasan berbasis berita sama sekali.

## Q3 — Headroom LTV: drawdown 3-hari dari titik entry (≥2013)

Persentil drawdown kumulatif 3 hari ke depan, dihitung dari setiap hari di zona tersebut (bukan hanya hari shock):

| Window | n hari | p50 | p80 | p95 | p99 | worst |
|---|---:|---:|---:|---:|---:|---|
| K2 loan (ZD+Z3+Z4) | 3.489 | −0,89% | −4,26% | −10,66% | −18,45% | −43,55% (2013-04-10) |
| K2 hanya ZD (dip terdalam yang diizinkan) | 1.450 | −1,32% | −5,01% | −10,63% | −18,58% | −41,08% (2020-03-11) |
| K5 loan (Z2+Z2t+Z3) | 1.551 | −0,62% | −3,28% | −8,50% | −16,57% | −26,23% (2013-04-13) |

Drop yang dibutuhkan untuk melompat dari cap LTV ke tiap rung, dan seberapa sering drawdown 3-hari sedalam itu terjadi di window K2 (≥2013):

| Dari cap | ke rung-1 58% | ke wajib-jual 60% | ke rung-2 62% | ke rung-3 65% |
|---|---|---|---|---|
| **45%** | butuh −22,4% → 0,57% hari (20 hari) | −25,0% → 0,40% (14 hari) | −27,4% → 0,26% (9 hari) | −30,8% → 0,20% (7 hari) |
| **48%** | butuh −17,2% → 1,26% hari (44 hari) | −20,0% → 0,83% (29 hari) | −22,6% → 0,57% (20 hari) | −26,2% → 0,32% (11 hari) |

**Ladder jump — kalau rung-1 (58%) tersentuh, seberapa sering langsung lewat rung berikutnya (window K2):**

| Cap | n hari sentuh 58% | juga lewat 60% | juga lewat 62% | juga lewat 65% |
|---|---:|---|---|---|
| 45% | 20 | 14 (70%) | 9 (45%) | 7 (35%) |
| 48% | 44 | 29 (66%) | 20 (45%) | 11 (25%) |

**Hasil Q3: tangga staged cut memang bisa dilompati, dan itu bukan kejadian langka begitu rung pertama tersentuh.** Secara unconditional, drawdown 3-hari yang cukup untuk menyentuh 58% dari cap 45% terjadi di 0,57% hari — jarang. Tapi **begitu 58% tersentuh, ~2 dari 3 kali harga juga menembus 60% dalam window 3-hari yang sama, dan ~1 dari 3 kali sampai 65%.** Ini pembenaran kuantitatif untuk aturan framework bahwa order tangga harus **dipasang di muka**, bukan dieksekusi manual saat kejadian.

Cap 48% jelas lebih rapuh dari 45%: jumlah hari yang menyentuh rung-1 naik dari 20 ke 44 (2,2×), dan kejadian tembus 60% naik dari 14 ke 29.

Sebaran hari-hari berbahaya itu (dd3 ≤ −22,4%, zona window K2) sangat era-dependent: **C1 n=14 · C2 n=2 · C3 n=4 · C4 n=0.** 14 dari 20 kejadian ada di 2013 saja. Tidak ada satupun di cycle berjalan. Ini **bukan** alasan melonggarkan tangga (n per cycle terlalu kecil), tapi wajib disebut sebagai konteks.

## Cross-check klaim framework "92 kejadian turun ≥13% dalam ≤3 hari"

Dari data yang sama (semua zona): **236 hari** dengan dd3 ≤ −13% full-history (160 sejak 2013). Setelah merge cooldown 5 hari → **98 episode** full-history, **71 episode** sejak 2013.

Angka 92 di framework kemungkinan besar berasal dari definisi episode-merged full-history — 98 vs 92 cukup dekat mengingat aturan merge bisa sedikit berbeda. **Kalibrasi framework cenderung tervalidasi ulang secara independen.**

---

## Kesimpulan

**B-7 dalam bentuk yang diucapkan video (shock terkonsentrasi saat harga jatuh) cenderung TIDAK didukung sebagai pernyataan frekuensi**, tapi **versi arahnya cenderung DIDUKUNG kuat**. n=139 shock (≥2013), sebaran per cycle merata (61/43/32/34 full-history), tidak ada dominasi era.

Tiga hal yang dibawa keluar:
1. **Kepadatan shock datar lintas zona** (2,60-2,78 per 100 hari) — zona akumulasi bukan zona yang lebih sering kena shock, jadi tidak ada alasan menahan DCA K4 hanya karena "zona bawah rawan shock".
2. **Arah shock sangat zona-dependent** (down:up 7,0 di ZC vs 0,21 di Z5). Ini yang praktis: di ZC/ZD, shock yang datang cenderung ke bawah — relevan untuk sizing tranche, bukan untuk membatalkan deploy.
3. **Tangga staged cut LTV bisa dilompati**: begitu 58% tersentuh, ~66-70% kejadian juga menembus 60% di window 3-hari yang sama. Cap 48% ~2× lebih sering masuk zona itu dibanding cap 45%.

**Caveat wajib:** semua sel per-zona di luar ZD/Z3/Z4/Z5 punya n=3-8 dan tidak boleh dibaca sebagai angka. Pola arah down:up bertahan di kedua definisi shock, jadi itu yang paling bisa diandalkan; angka rate per 100 hari di zona kecil tidak.
