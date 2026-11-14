# Realized Profit Collapse dalam Konteks Bull — Sinyal Floor atau Bukan?

**Sumber awal:** Video On-Chain Mind, 2025-01-27, item [KONFIRMASI]
**Sesi validasi:** 2026-07-12
**Status: CLOSED**
**Script:** `analyze_realized_profit_collapse.py` | **Tabel event:** `events_realized_profit_collapse.csv`

## Ringkasan
Video: realized profit anjlok dari ~$10B/hari (puncak Des 2024 dekat $100K) ke $2-3B/hari
(Jan 2025) → "heavy selling sudah lewat, floor terbentuk". Diuji pakai `rrp` (relative
realized profit — dinormalisasi market cap, comparable antar cycle; USD absolut tidak),
SMA7, full history 2010-2026.

## Definisi event (ditetapkan sebelum lihat hasil, at-gate / tanpa lookahead)
- `rrp_sma7(t) ≤ 0.30 × peak60(t)` — drop ≥70% dari local peak, peak60 = rolling max 60d
  berakhir di t
- Konteks bull: `btc_price > realized_price` (proxy Z3+)
- Filter noise: peak60 ≥ expanding median rrp_sma7 sampai t (at-gate)
- Event = hari pertama kondisi true, cooldown 60d
- Ground truth 90 hari: "floor OK" = max drawdown < 15% DAN fwd90 > 0;
  false positive keras = close di bawah RP dalam 90d

## Hasil — **n=44 event** (c2013=11, c2017=11, c2021=13, c2024=9)

| Metrik | Event (n=44) | Baseline semua hari harga>RP (n=4.875, day-level) |
|---|---:|---:|
| "Floor OK" rate | **19/44 = 43%** | 49% |
| Median max drawdown 90d | **−16.6%** | −13.7% |
| Median fwd60 / fwd90 | +7.0% / **+3.9%** | — / +11.5% |
| Turun sampai bawah RP dalam 90d | 6/44 = 14% | — |

Event realized-profit-collapse **TIDAK lebih baik dari baseline** — malah sedikit lebih
buruk di semua metrik. Median max drawdown −16.6% sudah gagal kriteria "floor" (<15%) di
median-nya sendiri. Hit rate per cycle konsisten jelek: c2013 5/11, c2017 5/11, c2021 5/13,
c2024 4/9 — bukan artefak satu cycle.

### Kenapa gagal secara mekanis
Realized profit kolaps dalam konteks harga>RP terjadi di DUA situasi yang berlawanan:
(a) dip sehat mid-bull (2016-09, 2019-05, 2024-02 — floor benar), dan
(b) tepat SETELAH cycle top, saat seller kehabisan profit karena harga sudah jatuh
(2017-12-25 → maxDD −50%, 2021-11-23 → −39%, 2021-04-05 → −46%, 2022-04-20 → −54%).
Metrik ini tidak bisa membedakan "selling exhausted karena floor" vs "profit menguap
karena top sudah lewat". Persis ambiguitas yang framework hindari dengan trajectory-based
zoning.

### Uji real-time klaim video sendiri
Event 2024-12-31 ($93.4K) — persis setup yang dibahas video ($10B→$2-3B, Des→Jan):
maxDD 90d = **−15.9%**, fwd90 = **−11.6%**. Klaim "floor terbentuk" gagal di kejadian yang
sedang dibicarakan videonya sendiri (koreksi Feb-Apr 2025 ke ~$76K menyusul).

## Uji inkremental vs K2 kondisi #2 (STH-SOPR <0.97 belum >14d + aSOPR >0.95)
- 27/44 event sudah bertepatan dengan K2 cond #2 aktif dalam ±14 hari → mayoritas overlap.
- 17/44 event TANPA K2 cond #2 di dekatnya: 11/17 floor OK (65%), tapi subset dengan K2
  cond #2 cuma 8/27 (30%). Split post-hoc ini menarik tapi n kecil dan TIDAK diuji sebagai
  hipotesis a-priori — sesuai aturan anti-overfit, tidak dijadikan rule. Yang jelas: sebagai
  sinyal standalone, event ini di bawah baseline, jadi tidak ada nilai inkremental yang
  bisa ditambahkan ke K2.

## Kesimpulan final
**REJECT.** Label [KONFIRMASI] dari video tidak terbukti: realized profit collapse saat
harga>RP hanya menghasilkan "floor" 43% dari waktu (n=44, 4 cycle) — lebih buruk dari
baseline 49% hari biasa di kondisi sama, dengan tail risk besar (4 event berujung drawdown
39-54% karena pola yang sama muncul tepat setelah cycle top). Tidak ada nilai inkremental
di atas K2 kondisi #2. Kejadian spesifik yang dibahas video (Des 2024→Jan 2025) sendiri
diikuti drawdown −15.9% dan fwd90 −11.6%. Tidak ada perubahan framework diusulkan.

## Keterbatasan
- Baseline day-level tidak independen (serial correlation) — dipakai hanya sebagai
  pembanding kasar; kesimpulan utama dari event-level n=44 yang tersebar merata 4 cycle.
- Threshold (70% drop, window 60d, DD 15%) dipakai satu varian sesuai spesifikasi tugas,
  tidak di-tune — hasil negatif bukan karena cherry-picking parameter.
- `rrp` kita relative-to-market-cap (Glassnode-sourced); chart video pakai USD absolut
  CryptoQuant — normalisasi kita justru lebih fair antar cycle, dan tetap gagal.
