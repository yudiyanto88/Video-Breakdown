# Entity-Adjusted Relative Unrealized Loss & NUPL sebagai Context — Findings

**Sumber awal:** Video On-Chain Mind, 2025-01-22, item [BARU] Entity-Adjusted Relative Unrealized Loss
**Sesi validasi:** 2026-07-10 s/d 2026-07-11
**Status: CLOSED (dua sub-uji, dua-duanya closed)**

## Ringkasan
Video mengklaim metric loss yang dinormalisasi market cap (value-weighted) lebih akurat dibanding coin-count based Supply-in-Loss untuk mengukur severity koreksi. Dashboard sudah punya field setara: `nupl`, `sth_nupl`, `lth_nupl`. Diuji di dua konteks berbeda.

## Uji 1 — NUPL sebagai pengganti coin-count di K1/K4 (2026-07-10)

**K1 signal #5 (Supply in Profit >90% di puncak siklus), 6 cycle top:**
`percent_btc_in_profit` konsisten (95.5%-100%, range sempit). `nupl` total di titik yang sama menunjukkan pola diminishing peaks (0.798 → 0.765 → 0.704 → 0.649 → 0.626 → 0.590, turun ~26pp lintas siklus) — sama seperti masalah MVRV. **Coin-count lebih reliable, TIDAK diganti.**

**K4 condition #3 (Supply in Profit <50% di bear bottom), 2 bottom genuine:**
`percent_btc_in_loss` konsisten (53.7% vs 48.5%). `nupl` lebih variatif (-0.005 vs -0.194). **Coin-count tetap lebih stabil, TIDAK diganti.**

**Tapi untuk use-case ASLI video** (mengukur severity koreksi relatif, BUKAN trigger K1/K4) — 7 koreksi bull-market (Mei 2021 - Jan 2025): `pct_sth_in_loss` sangat noisy (51%-94%), `sth_nupl`/`nupl` jauh lebih interpretable (negatif hanya di 2 bear-bottom genuine, positif di semua koreksi mid-bull). Contoh: Jan 2025 dip, `pct_sth_in_loss` 56% (kelihatan severe) tapi `sth_nupl` +0.067 (STH net masih PROFIT).

**Kesimpulan Uji 1:** Coin-count dipertahankan untuk K1/K4 (jangan diganti). NUPL/STH-NUPL/LTH-NUPL berguna sebagai **context tambahan terpisah** untuk menilai severity relatif suatu koreksi — bukan pengganti trigger.

## Uji 2 — NUPL sebagai tie-breaker confidence scoring K2 (2026-07-11)

**Tujuan:** cek apakah NUPL/STH-NUPL bisa misahin genuine bull dip vs bear onset DALAM bucket confidence K2 yang sama (bukan kondisi ke-6 baru).

**Setup:** 19 K2 gate event historis (2010-2025, n≥5 per cycle spread cek), scoring 5 kondisi existing K2 (C1 STH-MVRV, C2 SOPR, C3 Supply, C4 LTH, C5 AVIV Mean bounce), ground truth: genuine bull dip (higher high tanpa K3 Stage2 dalam 60 hari) vs bear onset.

### Analisis awal (BIAS — jangan dipakai)
Versi pertama pakai `nupl_trough` (nilai NUPL terendah dalam window 60 hari ke depan dari gate date). Sempat nunjukkan separasi bersih di bucket Low (n=6). **DITEMUKAN LOOKAHEAD BIAS**: lag ke trough jauh lebih panjang di event BEAR_ONSET (rata-rata ~28 hari) vs GENUINE (~14 hari, banyak 0-2 hari) — nilai trough sebagian merefleksikan seberapa dalam/lama decline yang SUDAH terjadi, bukan info yang tersedia di titik keputusan.

### Analisis fix (VALID — pakai ini)
Diganti ke `nupl_at_gate` (nilai persis di tanggal gate, t=0) dan `nupl_3d_avg` (smoothing 3 hari, hard cap, tidak ada lookahead lebih jauh). Diverifikasi ulang manual dari raw CSV.

| Bucket | n | Bear onset range | Genuine range | Overlap? |
|---|---|---|---|---|
| Low | 6 (4 bear/2 genuine) | 0.077–0.592 | 0.538–0.579 | YA, genuine terbungkus penuh di dalam range bear |
| Medium | 10 (3 bear/7 genuine) | 0.574–0.790 | 0.500–0.779 | YA, overlap luas |
| High (at-gate) | 3 (2 bear/1 genuine) | 0.537–0.574 | 0.566 (n=1) | YA, genuine di tengah range bear |
| High (3d-avg) | 3 (2 bear/1 genuine) | 0.542–0.583 | 0.585 (n=1) | Tidak overlap, tapi n genuine=1 — tidak bisa diklaim konsisten |

**Tidak ada separating power di bucket manapun** yang punya ≥2 event di kedua sisi outcome (Low, Medium). Leave-one-out di Low mengonfirmasi: separasi gagal di kedua arah exclude, bukan cuma rapuh — memang tidak pernah ada di data yang bersih dari bias.

**Observasi tambahan:** range NUPL di seluruh 19 event sempit (0.45-0.79 di luar 1 outlier 2010) — konsekuensi struktural dari gate K2 sendiri yang hanya menyaring dip di Z3-Z5 (bull market masih sehat, NUPL "dipaksa" moderat-positif dari desain gate, bukan semata kegagalan NUPL).

**Kesimpulan Uji 2:** NUPL/STH-NUPL **TIDAK berguna sebagai tie-breaker** K2 confidence scoring di bucket manapun. Tidak ada kondisi ke-6 diusulkan.

## Kesimpulan gabungan
- NUPL/STH-NUPL/LTH-NUPL TIDAK menggantikan coin-count di K1 signal #5, K4 condition #3, atau jadi tie-breaker baru di K2.
- Satu-satunya use-case valid: **context tambahan terpisah** untuk menilai severity koreksi relatif (bukan trigger, bukan scoring).
- Status: CLOSED di semua sub-uji. Tidak ada perubahan ke Decision_Framework_v1.md.

## Pelajaran metodologi (generik, disimpan untuk validasi ke depan)
Hati-hati pakai trough/extremum forward-looking sebagai fitur predictive — itu lookahead bias by construction kalau window pencarian tidak dibatasi ke titik keputusan. Selalu pakai nilai di titik keputusan (at-gate) atau window smoothing pendek dengan hard cap ke depan (bukan pencarian minimum/maksimum tanpa batas).
