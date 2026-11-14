# Findings — Proxy percentile MVRV causal & uji klaim "<10 only near cycle lows"

**Insight yang diuji:** [BARU] Percentile 8% saat ini ≈ bottoming out, tercapai sebelum harga menyentuh RP (#5) · konstruksi MVRV Quantile Bands (#1) · threshold FAQ <25 / <10 (#6) · percentile rendah ≠ bottom presisi (#8)
**Sumber klaim:** Bitcoin Magazine Pro — "The FREE & SIMPLE Strategy That Beats Bitcoin (It Just Flashed Again)", 5 Agt 2026, slide `[02:05]` + FAQ slide `[11:41]`
**Tanggal validasi:** 6 Agustus 2026
**Script:** [`analyze_mvrv_percentile_causal.py`](analyze_mvrv_percentile_causal.py)
**Event tables:** [`events_mvrv_percentile_episodes.csv`](events_mvrv_percentile_episodes.csv) · [`events_mvrv_percentile_bearlows.csv`](events_mvrv_percentile_bearlows.csv) · [`events_mvrv_percentile_first_below10.csv`](events_mvrv_percentile_first_below10.csv)
**Data:** `data_master_all_metrics.csv`, baris terakhir **2026-07-15**

> ⚠ **Selisih tanggal:** data berakhir 2026-07-15, video terbit 2026-08-05 — selisih ~3 minggu.
> Angka "Current Percentile 8%" di video tidak bisa direplikasi persis pada tanggalnya.

---

## Klaim yang diuji

1. **`[02:05]` + `[02:08]-[02:19]`** — "Current Percentile: 8%", dan level ini *"comparable to when
   Bitcoin is pretty much bottoming out in every single bear cycle"*
2. **`[02:44]-[02:50]`** — *"We're reaching these levels **before** we've actually reached the realized price"*
3. **FAQ slide `[11:41]`** — *"readings below the 25th percentile have coincided with bear market
   accumulation ranges, and readings below the 10th percentile have appeared **only** near major cycle lows"*
4. **`[02:20]-[02:34]`** — di 2022, bottom percentile tersentuh saat BTC ~$18k, harga lanjut turun ke ~$15k

**Titik lemah struktural yang diuji:** frase *"percentile of **all history**"*. Kalau rank dihitung
full-sample (bukan expanding/causal), setiap pembacaan historis mengandung informasi masa depan →
lookahead bias struktural, melanggar Standar Validasi poin 3.

---

## Definisi event

- Dua proxy **causal** dari `mvrv_ratio`:
  - **P1 raw** — expanding-window percentile rank
  - **P2 detrended** — OLS expanding `log(mvrv_ratio) ~ t` memakai data `[0..t]` saja, lalu percentile rank residual
- Versi **full-sample** dipakai **hanya sebagai cermin** untuk mengukur besar lookahead bias — bukan sebagai kandidat
- **Burn-in 365 hari** → proxy valid sejak 2011-07-17 (n = 5.478 hari)
- **Episode** = hari berurutan di bawah threshold, **merge kalau jeda < 30 hari**
- **"Dekat cycle low"** = ±180 hari (ditetapkan **a priori**, sebelum menghitung)
- Cycle low ground-truth (ex-post sah — ini ground truth, bukan gate keputusan): 2011-11-18,
  2015-01-14, 2018-12-15, 2022-11-21. Low sementara bear berjalan 2026-06-30 dilaporkan **terpisah**

---

## (a) Causal vs full-sample — besar lookahead bias

| Tanggal | MVRV | P1 causal | P1 full | Δ | P2 causal | P2 full | Δ | P/RP |
|---|---|---|---|---|---|---|---|---|
| 2015-01-14 | 0,568 | 2,3 | 0,7 | +1,7 | 2,9 | 0,6 | +2,3 | 0,568 |
| 2018-12-15 | 0,705 | 2,6 | 1,4 | +1,2 | 2,9 | 1,3 | +1,6 | 0,705 |
| 2022-11-21 | 0,777 | 3,2 | 2,5 | +0,7 | 3,5 | 2,1 | +1,4 | 0,777 |
| **2026-07-15** | **1,234** | **22,6** | 22,6 | 0,0 | **21,4** | 21,4 | 0,0 | 1,234 |

**Selisih di seluruh sampel:**
- P1: mean +1,3 pp · mean\|Δ\| **4,6 pp** · rentang −36,0 … +24,6 pp
- P2: mean +5,2 pp · mean\|Δ\| **10,5 pp** · rentang −66,8 … +52,7 pp

**Catatan penting.** Di **hari terakhir** selisihnya nol *by construction* (expanding window = full sample
pada titik akhir). Artinya lookahead bias **tidak merusak angka hari-ini** — ia merusak **chart historis**,
yang justru dipakai untuk membenarkan klaim "8% = bottom tiap bear". Untuk P2 (yang paling mirip
"amplitude decay model") biasnya bisa mencapai **puluhan poin percentile**.

### Aturan berhenti — dijalankan

P1 causal = **22,6**, P2 causal = **21,4**, vs klaim BM Pro = **8** → **tidak konvergen** (di luar ±5 pp).

Sesuai aturan berhenti yang ditetapkan di muka, reproduksi angka 8% dinyatakan **INCONCLUSIVE** dan
**tidak ada varian ke-3 atau ke-4 yang dicoba** (Standar Validasi poin 6 — mencoba varian sampai ketemu
angka target adalah overfitting).

**Konsekuensi tafsir:** dengan MVRV mentah 1,234, baik rank mentah maupun rank detrended-linear duduk di
~21-23. Selisih ~13-15 poin ke angka 8 **cenderung dihasilkan oleh asumsi model decay BM Pro, bukan oleh
data mentah**. Bagian (b)-(e) di bawah memakai **proxy kami**, bukan indikator BM Pro.

---

## (b) Bear low: P/RP dan hari di bawah Realized Price

| Bear | Low | P/RP @ low | hari P<RP **di dalam bear** | hari bear | hari P<RP (window cycle) |
|---|---|---|---|---|---|
| 2011 *(supl.)* | 2011-11-18 $2,05 | 0,412 | 70 | 164 | 71 |
| 2014-15 | 2015-01-14 $178,50 | 0,568 | 37 | 412 | 37 |
| 2018 | 2018-12-14 $3.281 | 0,702 | 27 | 365 | 301 |
| 2022 | 2022-11-21 $15.774 | 0,777 | 128 | 379 | 242 |
| **2025-26 (berjalan)** | *sementara* 2026-06-30 $58.460 | **1,101** | **0** | 283 | 52 † |

† 52 hari itu **ekor bear 2022** (Des-2022 / Jan-2023) yang jatuh di window cycle S4 — bukan bagian dari
bear berjalan.

- **P/RP di bear low naik monoton:** 0,568 → 0,702 → 0,777 (**n=3**). Mendukung klaim video.
- **Hari P<RP TIDAK menurun monoton:** 37 → 27 → 128. Membantah versi kuantitatif klaim.
- **Bear berjalan: harga belum pernah menyentuh RP sekalipun** sejak peak 2025-10-06 (P/RP terendah 1,101).

---

## (c) + (d) Pertama kali reading <10 di dalam tiap bear

| Bear | P1: first<10 | MVRV | P/RP | P>RP? | maxDD lanjutan | hari→low | P2: first<10 | P/RP | P>RP? |
|---|---|---|---|---|---|---|---|---|---|
| 2011 *(supl.)* | 2011-08-06 | 0,950 | 0,950 | tidak | −68,6% | 104 | 2011-07-17 | 1,815 | **YA** |
| 2014-15 | 2014-10-04 | 0,938 | 0,938 | tidak | −45,6% | 102 | 2014-04-10 | 1,106 | **YA** |
| 2018 | 2018-11-24 | 0,808 | 0,808 | tidak | −16,3% | 20 | 2018-11-24 | 0,808 | tidak |
| 2022 | 2022-06-16 | 0,892 | 0,892 | tidak | −22,6% | 158 | 2022-06-16 | 0,892 | tidak |
| **2025-26** | **TIDAK PERNAH** (min 16,9) | — | — | — | — | — | **TIDAK PERNAH** (min 15,7) | — | — |

**Klaim "reading rendah tercapai SEBELUM harga menyentuh RP":**
- Dengan P1: dari 419 hari <10, hanya **8 hari (1,9%)** terjadi saat P>RP — semuanya di 2011
- Dengan P2: **72 dari 372 hari (19,4%)**, rentang 2011-07-17 … 2014-11-07

Pola "<10 sebelum menyentuh RP" **pernah terjadi tapi langka**, dan sangat bergantung pada varian
detrending yang dipakai — **bukan karakter yang stabil**.

**Ini sekaligus menutup insight #8.** Reading <10 pertama **bukan** titik terbawah: masih ada drawdown
lanjutan **−16,3% s/d −68,6%** dan **20-158 hari** sebelum bear low. **n = 4 bear** (2011 supl., 2014-15,
2018, 2022); sebaran drawdown lanjutan sangat lebar dan **didominasi observasi 2011** di ujung ekstrem.
Framework sudah mengkodekan prinsip ini lebih keras lewat justifikasi sizing lantai waktu (worst case
beli pertama 2014 masih turun −46%, n=3/3 bear searah).

---

## (e) Uji kata "ONLY"

| Proxy / threshold | total hari | episode | % hari dalam ±180h dari cycle low | episode BUKAN dekat low |
|---|---|---|---|---|
| P1 < p10 | 419 (7,6%) | 9 | **98,1%** | **2 dari 9** (2015-08, 2020-03) |
| P2 < p10 | 372 (6,8%) | 9 | **99,7%** | **1 dari 9** (2014-04, 1 hari) |
| P1 < p25 | 1.160 (21,2%) | 9 | 80,9% | **4 dari 9** |
| P2 < p25 | 1.062 (19,4%) | 10 | 81,7% | **5 dari 10** |

Kalau low sementara 2026-06-30 ikut dihitung, false positive p25 turun jadi 2/9 dan 3/10 (dua episode
2026 jadi "dekat") — tapi **low itu belum terkonfirmasi**, jadi angka utama tetap yang memakai low
terkonfirmasi saja.

**False positive p10 yang paling menonjol:**
- **2020-03-12 (COVID crash)** — jarak **453 hari** dari cycle low terdekat
- **2015-08-18 … 08-27** — jarak **216 hari**

---

## Kesimpulan — tiga lapis

**1. Reproduksi angka 8% = INCONCLUSIVE (berhenti sesuai aturan).**
Proxy causal kami membaca **21,4-22,6** per 2026-07-15. Selisih ke 8 cenderung berasal dari asumsi model
decay yang parameternya tidak diungkap — artinya **angka headline video sebagian besar adalah output
asumsi, bukan output data mentah**.

**2. Lookahead bias struktural = TERKONFIRMASI ADA.**
Frase "percentile of all history" berarti chart historisnya memuat informasi masa depan. Selisih
causal-vs-full-sample rata-rata **4,6 pp (raw)** dan **10,5 pp (detrended)**, dengan ekor sampai ±50-67 pp.
Pembacaan historis "8% = bottom tiap bear" **tidak bisa direplikasi secara real-time** — pada tanggal-tanggal
itu, seorang investor yang memakai indikator ini secara causal akan melihat angka yang berbeda.

**3. Kata "only" = HAMPIR benar untuk p10, LEMAH untuk p25.**
Di p10, 98-99,7% hari berada dalam ±180 hari cycle low — tapi **1-2 dari 9 episode adalah false positive**,
jadi "only" terlalu absolut; **"hampir selalu"** lebih jujur. Di p25, sepertiga sampai separuh episode
tidak dekat cycle low → framing "bear market accumulation range" jauh lebih longgar daripada yang tersirat.

---

## Flag n, independensi & data (tebal, sesuai Standar Validasi poin 2, 4, 5)

- **Unit analisis yang jujur adalah episode (n = 9-10), bukan hari (n = 372-1.160)** — autokorelasi MVRV
  harian mendekati 1, jadi menghitung hari sebagai sample independen akan melebih-lebihkan kekuatan bukti
- **Sebaran episode <p10:** 2011 (1) · 2014-15 (2-3) · 2018 (1) · 2020 (0-1) · 2022 (3) —
  **didominasi cycle 2014-15 dan 2022**
- **Bear berjalan tidak pernah mencapai <10** dengan proxy kami (min 16,9 P1 / 15,7 P2), jadi klaim
  "sekarang sudah di level bottoming" **tidak terkonfirmasi dari data kami** per 2026-07-15
- Burn-in 365 hari → sampel efektif mulai 2011-07-17, bukan awal data
