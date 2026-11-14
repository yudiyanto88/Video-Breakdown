# Findings — LTH-SOPR trailing-Z quantile vs threshold absolut K4

**Tanggal validasi:** 2026-07-30
**Sumber klaim:** Video "I Rebuilt Bitcoin's 155-Day Holder Metric" — Bitcoin Magazine Pro (Matt Crosby), 2026-06-18, [09:25]–[09:58]
**Script:** [`analyze_lth_sopr_quantile_vs_k4.py`](analyze_lth_sopr_quantile_vs_k4.py)
**Tabel event:** [`events_lth_sopr_quantile.csv`](events_lth_sopr_quantile.csv)

---

## Klaim yang diuji

Matt: LTH-SOPR yang diubah jadi trailing-Z lalu dipetakan ke historical quantile "menandai setiap bear market bottom, termasuk COVID dip, absolutely to perfection". Kandidat pengganti threshold absolut `lth_sopr < 0,50` di **K4 kondisi 2**.

Sub-klaim (#18): apakah versi quantile menandai peak Jul 2025 atau peak Okt 2025.

**Verdict: REJECT untuk adopsi ke K4 kondisi 2** — plus satu temuan sampingan yang lebih penting dari klaimnya sendiri.

---

## Batasan yang berlaku

Data kita adalah **base "std" + boundary statis 155 hari**. Tanpa raw UTXO kita tidak bisa mereplikasi base "flt" maupun boundary dinamis 114 hari milik Matt. **Yang diuji di sini metodologinya, bukan angkanya** — hasil ini tidak membuktikan maupun menyangkal angka spesifik yang ditampilkan di video.

---

## Metodologi & anti-lookahead

- `z(t) = (lth_sopr(t) − mean_1460d) / std_1460d`, window trailing **berakhir di t−1**
- `q_exp(t)` = persentil z terhadap z-history **sampai t−1 saja** (expanding, mid-rank), minimum 365 z-value
- `q_full` (full-history percentile — yang repainting) dihitung **hanya** untuk mengukur besarnya bias lookahead, bukan untuk kesimpulan

**Warm-up:** z valid pertama **2014-07-16**, q_exp valid pertama **2015-07-16** → bottom **2011 dan 2015 tidak bisa diuji sama sekali**.

### Definisi event bear bottom (ditetapkan sebelum menghitung)

1. Close terendah dalam window ±180 hari
2. Merge kandidat yang jaraknya <365 hari → ambil yang terendah
3. Filter drawdown ≥45% dari ATH berjalan
4. Bottom <180 hari dari ujung data ditandai **BOTTOM-SO-FAR** (belum final)
5. Window pencarian trigger ±365 hari, cooldown antar-episode 90 hari

---

## n & sebaran per cycle

7 event terdeteksi; **5 testable**; 1 di antaranya (2021-07-20) adalah **crash mid-cycle Mei–Jul 2021, bukan bear bottom siklus**.

**n efektif = 4:** 2018-19 (1) · COVID 2020 (1) · 2022 (1) · 2025-26 (1, belum final).

---

## Hasil

### (a) Timing — kedua sinyal nyala ratusan hari sebelum bottom

| Bottom | q_exp<0,10 pertama | offset | lth_sopr<0,50 pertama | offset | min q ±180d |
|---|---|---|---|---|---|
| 2018-12-14 | 2018-05-16 | −212 | 2018-06-27 | −170 | 0,000 |
| 2020-03-12 | 2019-03-13 | −365 | 2019-03-16 | −362 | 0,006 |
| 2022-11-21 | 2022-02-03 | −291 | 2022-06-21 | −153 | 0,000 |
| 2026-06-30 | 2026-02-05 | −145 | **tidak pernah** | — | 0,024 |

Klaim "absolutely to perfection" **cenderung artefak visual** dari chart 13 tahun yang dipadatkan — pada resolusi harian, lead time-nya 145–365 hari, bukan presisi.

Satu keunggulan nyata versi quantile: di bear 2025-26 `lth_sopr < 0,50` **tidak pernah nyala sama sekali**, sementara versi quantile nyala.

### (b) Selektivitas (periode adil 2015-07-16 – 2026-07-15, n = 4.018 hari)

| Sinyal | Hari | % | Episode | Hit | False alarm |
|---|---|---|---|---|---|
| q_exp<0,10 | 734 | **18,3%** | 5 | 4/4 | 1 (Ags–Okt 2015) |
| lth_sopr<0,50 | 100 | 2,5% | 4 | 2/4 | 1 (Ags–Okt 2015) |
| q_full<0,10 (repainting) | 438 | 10,9% | 4 | 4/4 | 0 |

Nominal "10th percentile" ternyata nyala **18,3% hari** — persentil expanding-nya drift, jadi labelnya menyesatkan. Trade-off jelas: coverage naik (4/4 vs 2/4), presisi turun (18,3% vs 2,5% hari).

### (c) Dampak ke K4 — temuan paling menentukan

**Leg `aSOPR<0,93 selama ≥7 hari berturut` tidak pernah terpenuhi sepanjang 5.843 hari data.** Streak terpanjang **6 hari (2011-09-13)**. Total hari `asopr<0,93` = 189; hari dengan streak ≥7 = **0**.

Konsekuensi: kondisi 2 K4 = 0 hari di semua bear, versi absolut maupun quantile.

| Bear | hari Z1 | c2 abs | c2 q | DCA-hari (count≥2) abs→q | max count abs→q |
|---|---|---|---|---|---|
| 2018-19 | 57 | 0 | 0 | 16 → 16 | 3 → 3 |
| COVID 2020 | 0 (Z1 tak terbentuk) | — | — | — | — |
| 2022-23 | 69 | 0 | 0 | 62 → 62 | 3 → 3 |
| 2025-26 | 0 (Z1 tak terbentuk) | — | — | — | — |

Distribusi tier identik: 2018-19 `{1:41, 2:10, 3:6}` · 2022-23 `{1:7, 2:51, 3:11}`. Jalur K4-tanpa-Z1 (count≥3) juga identik: 14/1/11/0.

**Substitusi mengubah NOL hari-K4 di semua bear. Count K4 di bear 2025-26 tidak berubah (tetap 0).**

### (d) Klaim #18 (peak Jul vs Okt 2025) — negatif

Episode `q_exp > 0,90` berlangsung **2023-12-24 s/d 2025-11-25 = 703 hari**, menelan kedua peak 2025 sekaligus → pertanyaan "Jul atau Okt" tidak punya jawaban bermakna dari seri ini.

(q_exp max Jun–Ags 2025 = 1,000; Sep–Nov 2025 = 0,949 — arahnya condong ke Jul/Ags sesuai klaim Matt, tapi ini bukan timing signal.)

K1 trigger aktual di data kita: **2025-02-02, 2025-06-05, 2025-06-20, 2025-08-19** — K1 memberi tanggal, quantile tidak.

Perusak tambahan: ada episode `q_exp > 0,90` pada **2026-04-05 – 2026-06-21**, justru saat harga jatuh $81k → $63k mendekati bottom. Zona "atas" menyala di tengah kapitulasi.

### (e) Bias lookahead — besar

- mean |q_full − q_exp| = 0,0871 · median 0,0423 · **max 0,4818** · Spearman 0,895
- Hari <0,10: dua-duanya 435 / hanya expanding **299** / hanya full-history 3 → **disagreement 41,0%**

Paling tajam di COVID: versi repainting nyala **2020-03-12 – 2020-03-29 (18 hari, lead nol)**, versi jujur (expanding) sudah nyala sejak 2019-10-15.

Artinya klaim "COVID ditandai to perfection" **cenderung produk repainting** — persis yang Matt klaim tidak terjadi ("these aren't repainting", [11:15]).

### (f) Stabilitas

250 dari 3.988 jendela 30-hari (**6,3%**) memuat q<0,10 DAN q>0,90 sekaligus. Bulanan 2026: April min 0,062 / max 0,976; Juni min 0,024 / max 0,961.

### Independensi (Governance butir 1)

|phi| (`lth_sopr<0,50` vs `q_exp<0,10`) = **0,338** → lapis 2 lolos, ini memang sinyal berbeda, bukan reparametrisasi.

Tapi **lapis 1 gagal** (threshold 0,10 diambil dari chart Matt, bukan a priori dari framework) dan **lapis 3 gagal** (uji inkremental: nol perubahan hari-K4).

---

## Verdict

**REJECT.** Versi quantile menangkap lebih banyak bottom (4/4 vs 2/4) tapi harganya mahal: nyala 18,3% hari, whipsaw 6,3% jendela 30-hari, dan 41% labelnya berubah tergantung expanding vs full-history percentile. Substitusi ke K4 kondisi 2 mengubah nol hari-K4.

**n = 4 bottom testable** (2018-19, COVID 2020, 2022, 2025-26 belum final); bottom 2011 & 2015 tidak bisa diuji karena warm-up 1.825 hari.

### Flag framework terpisah (bukan dari video)

`aSOPR < 0,93 selama ≥7 hari berturut` — leg pertama K4 kondisi 2 — **tidak pernah terpenuhi satu kali pun** di 5.843 hari data (streak max 6 hari, Sep 2011). Kondisi 2 K4 mati secara mekanis, setara temuan "kondisi #1 K2 lama mati". Penempelan/perbaikan ini dikerjakan di project Onchain-Dashboard, bukan wewenang pipeline ini.
