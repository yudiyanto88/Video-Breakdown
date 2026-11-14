# Findings — STH-MVRV trailing-Z quantile vs gate valuasi K2

**Tanggal validasi:** 2026-07-30
**Sumber klaim:** Video "I Rebuilt Bitcoin's 155-Day Holder Metric" — Bitcoin Magazine Pro (Matt Crosby), 2026-06-18, [10:07]–[10:53] + Figure 10
**Script:** [`analyze_sth_mvrv_quantile_vs_k2_gate.py`](analyze_sth_mvrv_quantile_vs_k2_gate.py)

---

## Klaim yang diuji

Metodologi trailing-Z → historical quantile diterapkan ke STH-MVRV. Kandidat pengganti **gate valuasi K2** yang sekarang pakai band absolut `sth_mvrv 0,80–0,97`.

Catatan penting: ini **band dua sisi**, bukan threshold satu sisi. Batas bawah 0,80 fungsinya memisahkan bull dip dari bear dalam — jadi pertanyaannya berbeda dari K4.

**Verdict: REJECT tegas.**

---

## Batasan yang berlaku

Data kita **base "std" + boundary statis 155 hari**, bukan base "flt" + boundary dinamis milik Matt. Yang diuji metodologinya, bukan angkanya.

---

## Metodologi

Trailing-Z 1.460 hari dengan window berakhir **t−1** → expanding percentile terhadap z-history sampai **t−1 saja** (minimum 365 z-value). Anti-lookahead sesuai STANDAR VALIDASI butir 3.

Valid pertama **2015-07-16** → **cycle 2011 & 2015 tidak bisa diuji; uji lintas-cycle tidak penuh.**

---

## Hasil

### (a) Pemetaan percentile ↔ absolut TIDAK stabil antar cycle

| Cycle | q @ sth_mvrv = 0,80 | q @ 0,97 |
|---|---|---|
| 2015-16 | – (n=0) | 0,838 (n=19) |
| 2017-18 | 0,041 | 0,328 |
| 2019-21 | 0,084 | 0,357 |
| 2022-24 | 0,133 | 0,438 |
| 2025-26 | 0,027 | 0,398 |

Rentang q@0,80 = 0,027–0,133 (**faktor 5×**). q@0,97 = 0,328–0,438 tanpa 2015-16 (rentang 0,110). Pooled: q@0,80 = 0,085 · q@0,97 = 0,376.

**Ini memotong dua arah:** band absolut kita memang bergeser dalam ruang persentil, tapi band persentil juga bergeser dalam ruang sth_mvrv. Tidak ada yang stabil — jadi ini bukan argumen bahwa versi quantile lebih baik.

### (b) Gate absolut [0,80–0,97] vs gate percentile [0,08–0,38]

Kalibrasi pooled sekali, tanpa grid search (menghindari overfit — STANDAR VALIDASI butir 6). n = 4.018 hari.

| Cycle | abs | q | kedua | hanya abs | hanya q |
|---|---|---|---|---|---|
| 2015-16 | 43 | 1 | 1 | 42 | 0 |
| 2017-18 | 188 | 169 | 145 | 43 | 24 |
| 2019-21 | 244 | 260 | 238 | 6 | 22 |
| 2022-24 | 372 | 374 | 328 | 44 | 46 |
| 2025-26 | 244 | 191 | 188 | 56 | 3 |
| **TOTAL** | **1.091** | **995** | **900** | **191** | **95** |

**Keterbatasan metrik "false open" yang dilaporkan apa adanya:** implementasi literal alarm bear CEPAT ternyata nyala **90,5% hari** — karena unlock-nya (STH RP cross naik RP) cuma terjadi 6 kali sepanjang sejarah, sekali alarm nyala dia nyaris tidak pernah mati. Versi terbatas (mati juga kalau >365 hari tanpa pairing baru) memberi hasil sama. Metrik ini karena itu **tidak diskriminatif**, konsisten dengan catatan Decision Framework v2 bahwa aturan unlock masih PENDING validasi.

Sebagai gantinya dipakai proxy **hasil** — forward return 90 hari & max drawdown 90 hari:

| Kelompok hari | n | med fwd90 | mean fwd90 | med maxDD90 | % fwd90 < 0 |
|---|---|---|---|---|---|
| kedua gate nyala | 857 | −7,9% | +5,6% | −19,3% | 56,0% |
| hanya gate absolut | 175 | **+5,4%** | +22,1% | −11,9% | 44,0% |
| **hanya gate percentile** | **95** | **−14,4%** | +2,6% | −21,3% | **62,1%** |
| tidak ada gate | 2.801 | +16,3% | +29,4% | −9,8% | 33,3% |

95 hari tambahan yang **hanya** dibuka gate percentile punya median forward return **−14,4%** dan 62% negatif — terburuk dari semua kelompok. Sementara 175 hari yang **dibuang** versi percentile justru yang terbaik (+5,4%).

*(Hari-hari ini overlapping sehingga sangat berkorelasi; angka bersifat indikatif, bukan uji signifikansi statistik.)*

### (c) Independensi (Governance butir 1, lapis 2)

**|phi| = 0,817 > 0,8** → **gagal**. Ini reparametrisasi, bukan sinyal baru. Jaccard overlap 900/1.186 = **75,9%**.

---

## Verdict

**REJECT.** Gagal lapis 2 Governance (|phi| = 0,817), dan arah efek inkrementalnya negatif — hari yang ditambahkan lebih buruk, hari yang dibuang lebih baik.

**n = 4.018 hari, 4 cycle efektif** (2017-18, 2019-21, 2022-24, 2025-26). Cycle 2011 & 2015 tidak bisa diuji karena warm-up 1.825 hari, dan cycle 2015-16 hampir kosong (gate percentile cuma 1 hari) karena z-history baru 365 hari — jadi sebaran per cycle timpang.

Tidak ada usulan perubahan gate valuasi K2. Band absolut 0,80–0,97 dipertahankan.
