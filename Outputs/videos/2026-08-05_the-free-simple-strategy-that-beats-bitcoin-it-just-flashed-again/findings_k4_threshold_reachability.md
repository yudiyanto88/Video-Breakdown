# Findings — Reachability threshold K4 lintas cycle (rising troughs)

**Insight yang diuji:** [BARU] Trough MVRV tiap cycle makin TINGGI ("each trough higher")
**Sumber klaim:** Bitcoin Magazine Pro — "The FREE & SIMPLE Strategy That Beats Bitcoin (It Just Flashed Again)", 5 Agt 2026, FAQ slide `[11:41]` + lisan `[02:35]-[02:50]`
**Tanggal validasi:** 6 Agustus 2026
**Script:** [`analyze_k4_threshold_reachability.py`](analyze_k4_threshold_reachability.py)
**Event table:** [`events_k4_threshold_reachability.csv`](events_k4_threshold_reachability.csv)
**Data:** `data_master_all_metrics.csv`, baris terakhir **2026-07-15**

> ⚠ **Selisih tanggal:** data berakhir 2026-07-15, video terbit 2026-08-05 — selisih ~3 minggu.
> Semua pembacaan "saat ini" di bawah = per 2026-07-15, bukan per tanggal video.

---

## Klaim yang diuji

Video mengklaim trough MVRV tiap cycle makin tinggi. Lisan `[02:35]-[02:50]`: *"if you look at
the 2015 bear market low, we were very much beneath the realized price. 2019, a little bit less.
2022, a little bit less."* Basis klaim video: **n=3 bear low, kualitatif, tanpa satu pun angka numerik.**

**Kenapa ini penting untuk framework.** Decision Framework v2 mengkodekan sisi ATAS amplitude decay
(syarat awal K1/K3: "MVRV di setiap ATH baru lebih rendah dari ATH sebelumnya") tapi TIDAK sisi bawah.
Padahal keempat kondisi K4 semuanya **threshold absolut**:

1. LTH-MVRV < 1,0
2. aSOPR < 0,93 ≥7 hari DAN LTH-SOPR < 0,50
3. Supply in Profit < 50% DAN STH profit < 10%
4. Price/CVDD < 1,10 (flag ekstrem ≤ 1,0)

Kalau trough naik struktural, K4 bisa gagal arm bukan karena pasar belum murah, tapi karena
penggarisnya usang.

---

## Definisi event

- **Cycle** = konvensi bottom-to-bottom yang sudah established di
  `research/framework_review_2026-07/backtest_k5nz/run_backtest.py`
- **Bear** = cycle peak → cycle bottom. **1 bear = 1 observasi per metrik** (nilai minimum dalam window)
- Kondisi K4 disalin **verbatim** dari `btlib.build_all()` — tidak dihitung ulang
- aSOPR / LTH-SOPR dilaporkan sebagai **MA7**; nilai harian mentah disertakan sebagai pembanding
- **Anti-lookahead:** ini uji deskriptif, tidak ada gate keputusan. Batas window ditentukan ex-post
  karena itu bawaan pertanyaan ("berapa minimum dalam satu bear") — disebut eksplisit, bukan disembunyikan

**Window bear yang dipakai:**

| Bear | Peak | Bottom | Hari | Drawdown |
|---|---|---|---|---|
| B0 2011 *(suplemen)* | 2011-06-08 $30 | 2011-11-18 $2,05 | 164 | −93,1% |
| B1 2014-15 | 2013-11-29 $1.156 | 2015-01-14 $178,50 | 412 | −84,6% |
| B2 2018 | 2017-12-16 $19.538 | 2018-12-14 $3.281 | 365 | −83,2% |
| B3 2022 | 2021-11-08 $67.525 | 2022-11-21 $15.774 | 379 | −76,6% |
| **B4 berjalan** | 2025-10-06 $124.715 | *low sementara* 2026-06-30 $58.460 | 283 | −53,1% |

**n = 3 bear selesai + 1 berjalan + 1 suplemen (2011).**

---

## Hasil (a) — Minimum per bear

`*` = threshold K4 tersentuh

| Metrik | Threshold | B0 2011 | B1 2014-15 | B2 2018 | B3 2022 | B4 berjalan |
|---|---|---|---|---|---|---|
| MVRV Ratio | — | 0,401 | 0,568 | 0,702 | 0,760 | 1,101 |
| LTH-MVRV | 1,00 | 0,583* | 0,585* | 0,732* | 0,754* | 1,174 |
| Supply in Profit % | 50 | 43,5* | 39,3* | 39,9* | 44,5* | 45,6* |
| STH in Profit % | 10 | 0,0* | 0,0* | 0,0* | 0,0* | 0,0* |
| aSOPR (MA7) | 0,93 | 0,821* | 0,918* | 0,862* | 0,893* | 0,959 |
| LTH-SOPR (MA7) | 0,50 | 3,223 | 0,559 | 0,439* | 0,449* | 0,733 |
| Price/CVDD | 1,10 | 1,014* | 0,966* | 1,003* | 0,982* | 1,194 |

Minimum **harian mentah** (bukan MA7), urut B0→B4:
- aSOPR: 0,596 / 0,789 / 0,704 / 0,740 / 0,806
- LTH-SOPR: 0,258 / 0,447 / 0,343 / 0,363 / 0,623

### Verdict hipotesis 1 — TERBELAH

**Monoton naik B1→B2→B3** (mendukung klaim video):
- MVRV Ratio: 0,568 → 0,702 → 0,760 **YA** (0,401 di 2011 jadi titik ke-4 yang konsisten)
- LTH-MVRV: 0,585 → 0,732 → 0,754 **YA**
- Supply in Profit: 39,3 → 39,9 → 44,5 **YA**

**TIDAK monoton** (membantah klaim video kalau digeneralisasi):
- aSOPR MA7: 0,918 → 0,862 → 0,893
- LTH-SOPR MA7: 0,559 → 0,439 → 0,449
- Price/CVDD: 0,966 → 1,003 → 0,982
- STH profit: mentok lantai 0% di semua bear — tidak informatif

**Bacaan struktural.** Yang naik semuanya metrik **valuasi**; yang tidak naik semuanya **rasio perilaku**
(SOPR) atau **floor model** (CVDD). Dua kelompok terakhir mean-reverting secara konstruksi, jadi memang
tidak punya alasan struktural untuk drift naik. Klaim video cenderung benar untuk apa yang sebenarnya
dia ukur (MVRV), tapi tidak boleh digeneralisasi ke seluruh keluarga metrik bottom.

---

## Hasil (b) + (c) — Hari kondisi K4 per bear

| Bear | hari | C1 | C2 | C3 | C4 | ≥2 | ≥3 | =4 | P/CVDD≤1,0 |
|---|---|---|---|---|---|---|---|---|---|
| B0 2011 *(supl.)* | 164 | 5 | **0** | 36 | 1 | 4 | 1 | **0** | 0 |
| B1 2014-15 | 412 | 12 | **0** | 46 | 1 | 9 | 1 | **0** | 1 |
| B2 2018 | 365 | 24 | **0** | 18 | 9 | 17 | 6 | **0** | 0 |
| B3 2022 | 379 | 90 | **0** | 22 | 12 | 26 | 7 | **0** | 2 |
| **B4 berjalan** | 283 | **0** | **0** | 16 | **0** | **0** | **0** | **0** | 0 |

### Verdict hipotesis 2 — NEGATIF untuk C2, peringatan untuk bear berjalan

**1. Kondisi K4 #2 nol hari nyala di SELURUH sejarah.** Konjungsi "aSOPR < 0,93 selama ≥7 hari
berturut DAN LTH-SOPR < 0,50 di hari yang sama" tidak pernah bertemu — walaupun LTH-SOPR MA7 memang
tembus 0,50 di 2018 dan 2022. Konsekuensi langsung: **count K4 maksimum empiris = 3**, dan tier
`count = 4` (DCA 35%/bulan + income langsung masuk) adalah **tier mati** — belum pernah sekali pun terjadi
dalam 15 tahun data.

Ini paralel dengan temuan yang sudah pernah terjadi di framework: kondisi #1 K2 lama (rasio
LTH/STH-MVRV) juga terbukti mati secara matematis dan sudah dicabut di v2.

**2. Di bear 2022 tidak ada threshold individual yang gagal tersentuh.** Keempat metrik individual
menyentuh thresholdnya (C1 90 hari, C3 22 hari, C4 12 hari). Jadi klaim "penggaris K4 sudah usang"
**belum terbukti di 2022** — yang gagal cuma konjungsi C2, bukan level absolutnya.

**3. Di bear 2025-26, 3 dari 4 kondisi belum pernah nyala.** C1, C2, C4 = 0 hari. LTH-MVRV minimum
1,174 (butuh −15% lagi untuk tembus 1,0); Price/CVDD minimum 1,194 (butuh −8% lagi untuk tembus 1,10).
Count belum pernah ≥2 → **K4 belum pernah punya izin deploy di bear ini** per 2026-07-15.

---

## Kesimpulan

Klaim video **cenderung benar untuk sisi valuasi** (MVRV, LTH-MVRV, Supply in Profit naik monoton
lintas 3 bear) tapi **tidak berlaku** untuk SOPR dan CVDD yang mean-reverting secara konstruksi.

Temuan yang lebih penting daripada klaim aslinya: **kondisi K4 #2 mati secara empiris** — nol hari nyala
di 4 bear + suplemen 2011, membuat tier `count=4` tidak bisa dicapai.

**Flag sample size (tebal, sesuai Standar Validasi poin 2 & 4):** **n = 3 bear selesai** (2014-15,
2018, 2022) — tepat di ambang minimum framework. Ketiganya **tidak sepenuhnya independen**: mereka
merepresentasikan satu tren pematangan pasar yang sama, bukan tiga eksperimen terpisah. Bear berjalan
2025-26 belum selesai sehingga **tidak boleh** dipakai sebagai konfirmasi lanjutan — arah trough-nya
masih bisa berubah.

**Usulan (bukan penerapan — penempelan ke framework dikerjakan di project Onchain-Dashboard):**
diskusikan pemecahan C2 jadi dua kondisi terpisah, atau rekalibrasi tier sizing K4 ke count maksimum 3.
