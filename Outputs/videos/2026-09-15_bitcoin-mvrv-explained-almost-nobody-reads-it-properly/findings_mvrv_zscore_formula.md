# Findings — Rumus & kausalitas kolom `mvrv_zscore`

**Insight yang diuji:** X2 (koreksi dokumentasi; video vs KB MVRV v1.4 §1) · K6
**Sumber:** On-Chain Mind, 15 Sep 2026, `[05:40-06:10]`
**Tanggal validasi:** 16 September 2026
**Script:** [`analyze_mvrv_zscore_formula.py`](analyze_mvrv_zscore_formula.py)
**Data:** s/d 2026-09-15 (n = 5.905 hari)

## Ringkasan sederhana
Rumus di video yang benar, KB yang salah. Kolom `mvrv_zscore` = **(Market Cap − Realized Cap) / StDev(Market Cap)**, dengan stdev **expanding** (sejarah s/d tanggal itu saja) → **causal, tanpa lookahead**. Rumus KB §1 (MVRV − mean)/stdev tidak cocok. Label "full-history" di data_dictionary juga menyesatkan.

## Definisi (maks 4 varian, dikunci di muka)
- market_cap = mvrv_ratio × realized_cap_usd. Cross-check vs btc_price × (lth_supply_btc + sth_supply_btc): median |selisih| **0,001%** (n=5.905)
- Varian:
  - A-exp = (MC−RC)/σ_expanding(MC)
  - A-full = (MC−RC)/σ_full(MC)
  - B-exp = (MVRV−mean_exp)/σ_exp
  - B-full = (MVRV−mean_full)/σ_full
- ddof=1. "Cocok" = korelasi ≥0,99 DAN median |error| ≤0,05 pasca burn-in 365 hari (ditetapkan di muka)

## Kecocokan
| Varian | Corr (semua) | Med abs err | Corr (pasca burn-in) | Med abs err | Med rasio |
|---|---|---|---|---|---|
| **A-exp** | **1,0000** | **0,0088** | **1,0000** | **0,0095** | 1,004 |
| A-full | 0,300 | 0,790 | 0,345 | 0,724 | 2,082 |
| B-exp | 0,934 | 1,339 | 0,971 | 1,323 | 0,110 |
| B-full | 0,935 | 1,288 | 0,981 | 1,299 | 0,131 |

**Cocok: A-exp saja.**

## Nilai di tanggal kunci
| Tanggal | MVRV | mvrv_zscore | A-exp | A-full | B-exp | B-full |
|---|---|---|---|---|---|---|
| 2013-11-29 | 5,167 | 9,456 | 9,294 | 0,018 | 2,649 | 4,226 |
| 2017-12-16 | 4,387 | 9,268 | 9,237 | 0,412 | 2,539 | 3,245 |
| 2021-11-08 | 2,851 | 3,536 | 3,529 | 1,350 | 1,117 | 1,315 |
| 2022-11-21 | 0,777 | −0,316 | −0,318 | −0,142 | −1,194 | −1,292 |
| 2025-10-06 | 2,285 | 2,527 | 2,526 | 2,281 | 0,564 | 0,604 |
| 2026-09-15 | 1,443 | 0,769 | 0,773 | 0,773 | −0,454 | −0,454 |

## Bukti tambahan kausalitas
- A-full yang dihitung dengan data dipotong di 2021-11-08 = 3,529 (= A-exp, = kolom 3,536). Dengan data s/d 2026 = 1,350. Kolom **tidak ikut berubah**, jadi tidak di-recompute full-sample.
- Nilai yang tercatat di KB §2.1 vs kolom sekarang:

| Peak | KB | Kolom sekarang | A-exp |
|---|---|---|---|
| 2017 | 7,49-9,24 | 7,50-9,27 | 7,49-9,24 |
| 2021 | 2,96-3,66 | 2,96-3,67 | 2,96-3,66 |
| 2025 | 2,40-2,53 | 2,40-2,53 | 2,40-2,53 |

  Nilai historis stabil antar waktu penulisan.
- Beda label threshold kolom vs A-exp (pasca burn-in, dari 5.540 hari):

| Threshold | Hari beda label |
|---|---|
| Z > 1,0 | 21 (0,4%) |
| Z < −0,15 | 23 (0,4%) |
| Z > 0,05 | 10 (0,2%) |

  Hari terakhir < −0,15 = 2023-01-10 dan hari terakhir > 1,0 = 2026-01-28, identik di kolom dan A-exp.

## Implikasi (usulan, bukan penerapan)
- (i) **KB MVRV §1 perlu koreksi rumus** → (MC − RC)/σ(MC) dengan σ expanding s/d tanggal itu. **§5.3B FM1 dan §9 #7** menjelaskan kompresi lewat "dilusi historical mean/stdev seluruh dataset". Mekanisme itu keliru: tidak ada mean MVRV di rumus, yang ada stdev market cap USD yang terus bertambah. Kesimpulan "threshold ekstrem turun struktural" masih konsisten dengan data (9,27 → 3,54 → 2,53), tapi alasannya perlu ditulis ulang. `data_dictionary.md` "full-history" sebaiknya jadi "expanding (sejarah s/d tanggal itu)".
- (ii) Karena kolom causal, **threshold Z di KB B2 (>1,0), B5 (<−0,15), B6 (>0,05) dan 4B tidak mengandung lookahead** dari rumus. Keterbatasan in-sample lain (threshold dipilih ex-post) tetap berlaku.

## Standar Validasi
4 varian persis, tanpa tambahan · aturan "cocok" di muka · uji rumus, bukan event (n = hari; cycle tidak relevan) · burn-in 365 hari sama dengan V3.

## Verdict
**KONKLUSIF: rumus video benar, rumus KB §1 salah.** mvrv_zscore = (MC−RC)/σ_expanding(MC) (korelasi 1,0000, median error 0,0095). Kolom causal, jadi threshold Z di KB tidak ter-lookahead. Yang perlu dikoreksi adalah rumus & penjelasan mekanisme di KB §1, §5.3B FM1, §9 #7, dan label data_dictionary.
