# Findings — SMA30D vs Raw F&G untuk Trigger K5 Staging

**Tanggal validasi:** 2026-07-12
**Video:** How to Use the Fear & Greed Index for Bitcoin — On-Chain Mind, 2025-02-23
**Script:** `analyze_fg_sma30_vs_raw_k5.py` | **Tabel event:** `events_k5_pullback_fg_triggers.csv`
**Data:** `data_master_all_metrics.csv`. F&G mulai 2018-02-01 → **n kecil, wajib disebut di verdict.**

---

## Pertanyaan

Klaim video: SMA30D F&G lebih baik untuk baca trend sentimen. Framework K5 pakai raw F&G < 50 sebagai trigger deploy 50-60% saat pullback ≥5%. Apakah mengganti/menambah SMA30D < 50 worth it?

## Metode

- **Window K5 direkonstruksi sesuai Decision Framework v1:** mulai saat STH RP (`sth_cost_basis`) cross naik melewati RP (`realized_price`); tutup saat harga close di atas AVIV Upper 3 hari berturut-turut. AVIV Upper = `price_at_aviv_mean + 0.5*(price_at_aviv_plus_1_sigma - price_at_aviv_mean)` (formula sesuai data_dictionary / pola `analyze_k3_stage_comparison.py`). Setelah tutup, K5 hanya bisa aktif lagi setelah reset bear (STH RP < RP). State awal Feb 2018 = pasca-top (done).
- **Event pullback:** mulai saat drawdown dari running high window ≤ -5%, selesai saat running high baru; event yang mulai <14 hari setelah event sebelumnya di-merge.
- **Trigger dibandingkan:** hari pertama dalam event dengan raw F&G < 50, vs hari pertama dengan SMA30(F&G) < 50. Anti lookahead: kedua nilai tersedia di tanggal keputusan.

## Hasil

Window K5 terekonstruksi: **2019-05-07 → 2019-07-10** dan **2023-03-01 → 2024-02-29** (window 2024+ tidak ada — belum ada reset STH RP < RP sampai 2026-07-12). **n event pullback ≥5% = 5** (1 dari 2019, 4 dari 2023-24 → didominasi satu cycle).

| Event start | Local high | Max DD | Raw <50 (harga) | SMA30 <50 (harga) | Lag SMA | Selisih harga |
|---|---|---|---|---|---|---|
| 2019-05-17 | $8,186 | -11.1% | 2019-06-04 ($7,716) | **MISS** | - | - |
| 2023-03-03 | $23,649 | -14.5% | 2023-03-05 ($22,429) | **MISS** | - | - |
| 2023-04-19 | $30,496 | -17.5% | 2023-05-12 ($26,820) | 2023-06-13 ($25,955) | 32d | -3.2% |
| 2023-07-18 | $31,481 | -20.0% | 2023-08-06 ($29,079) | 2023-08-21 ($26,177) | 15d | -10.0% |
| 2023-11-21* | $37,906 | -5.5% | 2024-01-24 ($40,118) | **MISS** | - | - |

\* Event chain merged Nov 2023–Feb 2024; trigger raw terjadi di sub-pullback Jan 2024 (high $47,081 @ 2024-01-08 → low $39,564 @ 2024-01-22, -16%).

- **Raw trigger: 5/5 event. SMA30 trigger: 2/5 event** — miss 3 event sepenuhnya (tidak ada deploy sama sekali).
- Biaya miss besar: event 2023-03 raw deploy $22,429 → window tutup di $61,193; event Jan-2024 raw deploy $40,118 → $61,193 di akhir Feb (lalu $73K Maret). SMA30 melewatkan semuanya karena rata-rata 30 hari di fase bull jarang turun ke bawah 50.
- Saat SMA30 sempat trigger (2 event pullback terdalam, -17.5% dan -20%), harga deploy memang 3.2–10% lebih rendah — tapi dengan lag 15–32 hari, dan itu kebetulan pullback yang terus turun. Tidak ada kasus raw whipsaw yang "diselamatkan" SMA30 — raw tidak menghasilkan false deploy di data ini (deploy raw selalu lebih murah atau setara vs harga akhir window).

## Verdict

**NOT SUPPORTED untuk mengganti raw F&G < 50 di K5 staging.** SMA30 <50 miss 3 dari 5 event (60%) dan lag 15–32 hari di sisanya; keuntungan harga 3–10% saat kebetulan kena tidak sebanding dengan risiko tidak deploy sama sekali di awal bull. Raw F&G <50 tetap trigger yang tepat. Klaim video sendiri (SMA30 untuk baca TREND) tidak salah — salahnya kalau dipakai sebagai trigger. **n=5 event, 4/5 dari satu cycle (2023-24), F&G hanya 2 cycle — sample sangat kecil.**

## Implikasi ke framework (rekomendasi, bukan perubahan)

- K5 staging TIDAK diubah: tetap raw F&G < 50.
- SMA30 F&G boleh dipakai sebagai alat baca konteks/trend sentimen (macam pemakaian di findings_fg_peak_vs_price_peak.md), bukan komponen trigger.
