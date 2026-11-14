# Demand Momentum (CryptoQuant) — Dekomposisi & Uji Gate "Tanpa Rebound Momentum Harga Sulit Naik"

**Sumber awal:** Video On-Chain Mind, 2025-01-27, item [INDIKATOR CUSTOM]
**Sesi validasi:** 2026-07-12
**Status: CLOSED**
**Script:** `analyze_demand_momentum.py` | **Tabel event:** `events_demand_momentum_collapsed.csv`

## Ringkasan
Video menunjukkan "Demand Momentum" turun dari 1.7M → 100k BTC dan mengklaim buying pressure
melambat; klaim kunci: *"without a rebound in momentum it's going to be tough for prices to
gain any serious traction"*. Definisi dari footnote chart: `DM = Δ30d(Short-term Supply) −
Δ30d(Long-term Supply)`. Direplikasi pakai cutoff 155-hari Glassnode (`sth_supply_btc`/
`lth_supply_btc`), full history 2010-2026.

## Hipotesis 1 — DM adalah indikator independen → **REJECT (redundant)**
Karena STH supply + LTH supply = total supply, secara aljabar
`DM = 2×Δ30(STH supply) − Δ30(total supply)`. Diverifikasi numerik: identitas exact
(max residual 0.000 BTC), korelasi `corr(DM, Δ30 STH supply) = 0.994` full history.
Komponen Δ30 total supply cuma issuance 30 hari (12k-346k BTC, makin kecil tiap halving) —
hampir konstan dalam window pendek.

**DM = STH supply 30-day momentum dengan skala 2x, dikurangi issuance.** Bukan informasi
baru — ini rotasi coin LTH→STH yang sudah implisit di supply metrics framework.

## Hipotesis 2 — Klaim gate: DM collapse di Z3-Z4 = forward return buruk, DM rebound = prasyarat naik → **REJECT**

Definisi (ditetapkan sebelum lihat hasil, semua at-gate / tanpa lookahead):
- `collapsed(t)`: DM < 20% dari rolling max 90d yang berakhir di t (drop >80% dari local peak), peak90 > 0
- `rebound(t)`: tidak collapsed DAN DM(t) > DM(t−14)
- Zona ikut framework: Z3 = RP ≤ price < AVIV Mean; Z4 = AVIV Mean ≤ price < AVIV Upper
  (AVIV Upper = mean + 0.5×(1σ − mean), pola `analyze_k3_stage_comparison.py`)
- Event = hari pertama masuk collapsed saat di Z3-Z4, cooldown 90d

### Day-level di Z3-Z4 (hari berurutan TIDAK independen)
| State | n hari | fwd30 med | fwd60 med | fwd90 med | %positif 90d |
|---|---:|---:|---:|---:|---:|
| COLLAPSED | 2.240 | +3.4% | +11.3% | **+19.6%** | 64% |
| REBOUND | 1.176 | +2.4% | +5.8% | **+6.3%** | 58% |
| Baseline semua Z3-Z4 | 4.172 | +3.2% | +9.1% | +14.2% | — |

Arahnya **KEBALIKAN** dari klaim video: hari-hari DM collapsed justru punya forward return
lebih baik daripada hari-hari DM rebounding. Masuk akal secara mekanis — DM tinggi = coin
lama pindah tangan besar-besaran (fase euphoria/distribusi), DM rendah = pasar tenang/akumulasi.

### Event-level (**n=30**; sebaran: c2013=8, c2017=6, c2021=9, c2024=7)
Median fwd30/60/90 = −4.0% / +0.7% / +6.5% — sedikit di bawah baseline Z3-Z4 di horizon
pendek, menormal di 90d. Paling banter "drag lemah 30 hari", bukan gate.

### False negative klaim (penentu) — **n=26 rally episode** ≥20% (max return dalam 90d ke depan), full history:
- **14/26 rally dimulai saat DM ≤ 0** (flat/negatif)
- **16/26 rally dimulai saat DM dalam state collapsed**
- Hanya 11/26 rally dimulai saat DM sedang naik vs 14 hari sebelumnya

Contoh: 2020-03-08 (DM −289k, sebelum rally COVID-bottom), 2023-06-05, 2024-05-01,
2025-02-24. Klaim "tanpa rebound momentum harga sulit naik" tumbang — mayoritas rally justru
lahir saat DM flat/negatif/collapsed.

### Konteks real-time video
Event terdekat dengan video: entry collapsed 2025-02-15 (DM 303k vs peak90 1.57M) →
fwd30 −13.9%, fwd90 +6.0%. Koreksi Feb-Apr 2025 memang terjadi, tapi rally episode
berikutnya (2025-02-24, +20% dalam 90d) dimulai justru SAAT DM masih collapsed — tanpa
rebound duluan.

## Kesimpulan final
**REJECT + REDUNDANT.** Sebagai indikator, DM cuma 2×momentum 30-hari STH supply minus
issuance (corr 0.994, identitas aljabar exact). Sebagai sinyal gate, klaimnya terbalik:
state collapsed malah punya forward return lebih baik dari state rebound di Z3-Z4, dan 16
dari 26 rally ≥20% dimulai saat DM collapsed. Deskripsi video ("buying pressure melambat")
akurat sebagai akuntansi rotasi supply, tapi tidak punya nilai prediktif sebagai prasyarat
rally. Tidak ada K-node atau rule baru diusulkan.

## Keterbatasan
- Cutoff STH/LTH kita 155-hari Glassnode; CryptoQuant kemungkinan pakai definisi
  short/long-term berbeda — logika dekomposisi tetap berlaku identik (short+long = total)
  apapun cutoff-nya.
- Day-level rows sangat berkorelasi serial; kesimpulan utama disandarkan ke event-level
  (n=30) dan rally-episode-level (n=26), tersebar merata di 4 cycle — tidak didominasi
  satu cycle.
- Definisi collapsed (threshold 80%/window 90d) dan rebound (14d) dipakai satu varian saja
  sesuai spesifikasi tugas, tidak di-tune.
