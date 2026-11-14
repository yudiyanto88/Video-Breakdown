# Findings — Sensitivitas Zone Structure terhadap geseran boundary LTH

**Tanggal validasi:** 2026-07-30
**Sumber klaim:** Video "I Rebuilt Bitcoin's 155-Day Holder Metric" — Bitcoin Magazine Pro (Matt Crosby), 2026-06-18, Figure 5 [08:53]–[09:09] + ajakan adopsi [14:47]–[15:10]
**Script:** [`analyze_lth_rp_boundary_sensitivity.py`](analyze_lth_rp_boundary_sensitivity.py)
**Tabel event:** [`events_zone_label_changes.csv`](events_zone_label_changes.csv)

---

## Klaim yang diuji

Dua hal sekaligus:
1. **Klaim Matt:** LTH Realized Price versi boundary dinamis duduk **13,9% di atas** versi static-155 ($56.290 vs $49.434).
2. **Flag STOP #28:** kalau boundary LTH digeser, seberapa besar dampaknya ke Zone Structure v2 Dimensi 1 dan trigger Z2/K5?

**Verdict: flag STOP #28 = AKADEMIS, bukan konflik serius.** Klaim 13,9% tidak reproduce dari geseran boundary saja.

---

## Batasan yang berlaku — baca dulu

Data kita adalah **base "std" + boundary statis 155 hari**. Tanpa raw UTXO kita tidak bisa mereplikasi base "flt" maupun boundary dinamis 114 hari.

**Batasan keras yang membatasi seluruh angka di bawah:** 114 hari DAN 155 hari **dua-duanya jatuh di dalam band HODL-wave `3m-6m`**. Jadi perbandingan `LTH_RP(≥3m)` vs `LTH_RP(≥6m)` adalah **bracket / upper bound**, BUKAN replikasi boundary 114 hari. Efek geseran 155→114 hari yang sebenarnya **jauh lebih kecil** dari angka bracket di bawah.

---

## Metodologi

Cost basis kohort direkonstruksi dari HODL waves. Kolom `supply_<band>` dan `realized_cap_<band>` adalah **share persen**, jadi:

```
cost_basis(kohort) = (Σ rc_share / Σ sup_share) × realized_price
```

- `LTH_RP(≥3m)` = band `3m-6m, 6m-12m, 1y-2y, 2y-3y, 3y-5y, 5y-7y, 7y-10y, 10y+`
- `LTH_RP(≥6m)` = mulai dari `6m-12m`

**Sanity check:** rekonstruksi seluruh band = `realized_price` persis (mean/min/max rasio = 1,000000).

Periode: 2013-01-01 – 2026-07-15 (**n = 4.944 hari**).

---

## Hasil

### (a) Magnitudo deviasi LTH RP

Median deviasi terhadap vendor `lth_cost_basis` (155d): **≥3m +8,6%** · **≥6m −2,8%** · ≥1y −24,1%. Spread ≥3m vs ≥6m median 12,9%.

Per cycle (median deviasi ≥3m / spread 3m–6m):

| Cycle | dev ≥3m | spread 3m–6m |
|---|---|---|
| 2013-15 | +14,6% | 21,7% |
| 2016-18 | +10,4% | 13,9% |
| 2019-21 | +7,6% | 10,7% |
| 2022-24 | +4,0% | 5,9% |
| 2025-26 | +13,5% | 20,3% |

**Deviasi paling besar saat euforia, hampir nol saat bear:** MVRV>2,5 → ≥3m +18,1%; MVRV<1 (bear) → hanya **+1,3%**.

### Snapshot 2026-06-16 (tanggal yang sama dengan Figure 5 Matt)

| Seri | Nilai | vs vendor |
|---|---|---|
| vendor `lth_cost_basis` | $49.445 | — |
| Matt "LTH-RP static 155" (dari frame, low confidence) | $49.434 | beda 0,02% |
| `LTH_RP(≥3m, ~91d)` | $51.047 | **+3,2%** |
| `LTH_RP(≥6m, ~182d)` | $47.970 | −3,0% |
| Matt "LTH-RP dinamis (iso 1460d)" (dari frame) | $56.290 | +13,9% |

Vendor kita praktis identik dengan angka static-155 Matt (beda 0,02%) — bagus, base std kita sepadan.

Tapi geseran boundary ke **91 hari** — lebih ekstrem dari 114 hari — hanya menghasilkan **+3,2%** di data kita. Bracket penuh 91d–182d cuma **6,4%**. **Sisa gap Matt (13,9%) cenderung datang dari konstruksi "iso 1460d" miliknya dan/atau perbedaan base std→flt, bukan dari geseran boundary murni.**

### (b) Label struktur Zone Dimensi 1

Baseline vendor: **N = 4.404 · C = 94 · T = 446**

| Substitusi | Hari berubah | % | Rincian |
|---|---|---|---|
| vendor → ≥3m | **24** dari 4.944 | **0,49%** | C→N 12, C→T 12 |
| vendor → ≥6m | **13** dari 4.944 | **0,26%** | semua C→N |

Sebaran per cycle (≥3m): 2013-15 = 4 · 2019-21 = 20 · sisanya 0. **Didominasi satu cycle (2019-21: 20 dari 24 hari).**

Jumlah hari struktur **C (Konvergen)**: 94 (vendor) · 70 (≥3m) · 81 (≥6m).

### (c) Trigger Z2

Cross-up STH RP melewati RP (aturan unlock bear) **tidak tergantung LTH RP sama sekali** → tanggalnya identik di semua versi: **2015-11-03, 2019-05-07, 2023-03-01, 2023-03-05**.

Geseran tanggal MULAI episode Z2 (label C & Price < AVIV Mean):

| Versi | Geseran per episode (hari) |
|---|---|
| ≥3m | 0, 0, **+102**, 0, 0 |
| ≥6m | +4, 0, +6, +3, 0 |

Satu-satunya geseran serius: episode **2019-01-19** hilang di versi ≥3m (baru muncul 2019-05-01).

---

## Verdict

**AKADEMIS, bukan konflik serius.** Kriteria yang ditetapkan di muka: <2% label berubah = akademis, >15% = serius. Hasil: **0,49%** (≥3m) dan **0,26%** (≥6m) — jauh di bawah ambang. Tanggal trigger Z2 stabil (0–6 hari) di 4 dari 5 episode.

**n = 4.944 hari, 5 cycle; perubahan label terkonsentrasi di 2019-21 (20 dari 24 hari) → hasil didominasi satu cycle.**

### Nuansa yang menjelaskan kenapa dampaknya kecil

Deviasi LTH RP **naik tajam di euforia** (+18,1% saat MVRV>2,5) tapi **hampir nol di bear** (+1,3% saat MVRV<1) — dan justru di bear-lah LTH RP dipakai untuk deteksi struktur C dan trigger Z2. Jadi argumen "kita tidak perlu adopsi boundary dinamis" **cenderung didukung data**, bukan karena boundary tidak penting, tapi karena efeknya kecil justru di fase yang framework kita pakai.

Catatan lanjutan: kalau kelak framework menambah sinyal yang bergantung pada LTH RP **di fase euforia** (Z4/Z5, K1/K3), sensitivitas boundary akan jauh lebih tinggi dan kesimpulan "akademis" ini tidak otomatis berlaku di sana.
