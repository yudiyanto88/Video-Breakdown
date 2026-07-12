# Findings — F&G Peak Mendahului Price Peak (Struktur Diminishing ala K1)

**Tanggal validasi:** 2026-07-12
**Video:** How to Use the Fear & Greed Index for Bitcoin — On-Chain Mind, 2025-02-23
**Script:** `analyze_fg_peak_vs_price_peak.py` | **Tabel event:** `events_fg_tops_ath.csv`
**Data:** `data_master_all_metrics.csv` (kolom `Fear & Greed`, `btc_price`). F&G mulai 2018-02-01 → **maksimal 2 cycle penuh (n=2)** — batas keras semua kesimpulan di sini.

---

## Pertanyaan

1. **(a)** Apakah F&G maksimum cycle selalu mendahului price peak? Berapa hari? Berapa F&G saat price peak?
2. **(b)** Apakah F&G (SMA30D) lebih rendah di setiap ATH baru dalam cycle — konsisten pola diminishing K1?
3. **(c)** Kapan extreme greed pertama (raw ≥ 75) per cycle, dan berapa upside dari titik itu ke price peak?

## Metode

- Cycle A = 2018-02-01 s/d 2022-11-21 (bear bottom), Cycle B = 2022-11-22 s/d 2026-07-12.
- F&G bolong 4 hari → ffill. SMA30D rolling, nilai di tanggal T hanya pakai data ≤ T (anti lookahead).
- **Top lokal** = max harga window ±45 hari + new cycle-high (≥99% running max) + drop ≥15% sesudahnya. **ATH cluster** (untuk b) = hari-hari new cycle-high, merge kalau gap <30 hari, wakil = harga tertinggi cluster.
- Extreme greed = raw F&G ≥ 75 (bucket standar alternate.me 75–100).

## Hasil

### (a) F&G peak vs price peak — terjadi di KEDUA cycle

| Cycle | F&G max (raw) | F&G SMA30 max | Price peak cycle | Lead SMA30→peak | F&G saat price peak |
|---|---|---|---|---|---|
| A (2018-2022) | 95 @ 2020-12-01, $18.8K (leg bull 2020-21)* | 92.4 @ 2021-01-10 (~$38-40K) | $67,525 @ 2021-11-08 | ~302 hari | raw 75, SMA30 74.0 |
| B (2022-skrg) | 94 @ 2024-11-22, $98.9K | 81.5 @ 2024-12-12 | $124,715 @ 2025-10-06 | ~298 hari | raw 71, SMA30 51.2 |

\* Raw max full Cycle A juga 95 di 2019-06-26 (mini-bull 2019, $12.8K). Untuk leg bull utama 2020-10 s/d 2021-11: raw ≥ 92 terjadi 46 hari antara 2020-11-19 s/d 2021-02-23 di harga $17K–$56K — klaim video "F&G 92 saat BTC ~$30K" cocok dengan periode ini (Jan 2021).

- F&G peak **selalu mendahului** price peak final, ~10 bulan di kedua cycle; saat price peak sentimen sudah cool off (74 di 2021 — persis klaim "70-80" video; 51 di 2025, bahkan lebih dingin).
- Bonus lintas-cycle: puncak SMA30 juga diminishing antar cycle (92.4 → 81.5), begitu juga F&G saat final top (74.0 → 51.2).

### (b) Diminishing per-ATH — TIDAK monotonic

SMA30 di tiap ATH cluster — Cycle A: 44.5 → 67.2 → 92.2 → 79.7 → 71.1 → **74.0** (Nov 2021 sedikit LEBIH TINGGI dari Apr 2021). Cycle B: 62.0 → 56.5 → 70.2 → 78.0 → 80.9 → 70.7 → 66.2 → **68.9** → 51.2 (Aug 2025 lebih tinggi dari Mei 2025).

Polanya bukan "turun di setiap ATH baru" ala sinyal K1 MVRV/aSOPR, melainkan: **F&G naik selama markup awal, memuncak di fase euphoria tengah cycle, lalu ATH-ATH terakhir dibuat dengan sentimen jauh lebih dingin dari puncak euphoria** — dengan zigzag di antaranya.

### (c) Extreme greed pertama ≠ sinyal top

| Cycle | Extreme greed pertama (raw ≥75) | Harga saat itu | Upside ke price peak | Jarak |
|---|---|---|---|---|
| A | 2019-05-11 (F&G 76) | $7,214 | **+836%** | 912 hari |
| B | 2023-12-05 (F&G 75) | $44,107 | **+183%** | 671 hari |

Extreme greed pertama muncul sangat awal — jual di situ berarti melewatkan mayoritas upside cycle.

## Verdict

**SUPPORTED (a & c), PARTIAL (b).** Struktur besar klaim video benar di 2 dari 2 cycle yang bisa diuji: F&G memuncak ~10 bulan sebelum price top, dan final top terbentuk dengan sentimen yang sudah cool off. Tapi versi ketatnya ("lebih rendah di SETIAP ATH baru" seperti syarat aktivasi K1) tidak berlaku — jalurnya zigzag, hanya arah besarnya yang turun. **n=2 cycle (F&G baru ada sejak 2018) — di bawah standar minimal 3 cycle framework; treat sebagai pola probabilistik lemah, bukan sinyal.**

## Implikasi ke framework (rekomendasi, bukan perubahan)

- F&G SMA30 yang jauh di bawah puncak euphoria-nya saat harga bikin ATH baru layak jadi **confirming context tambahan (bukan sinyal)** untuk K1/K3 — sifatnya sama dengan STH metrics: confirming, never primary.
- Jangan pakai bentuk "F&G turun di setiap ATH baru" sebagai syarat formal ala K1 — datanya tidak monotonic.
- Extreme greed pertama di awal bull TIDAK boleh dibaca sebagai alasan mengurangi posisi — historis masih ada +183% s/d +836% upside (n=2).
