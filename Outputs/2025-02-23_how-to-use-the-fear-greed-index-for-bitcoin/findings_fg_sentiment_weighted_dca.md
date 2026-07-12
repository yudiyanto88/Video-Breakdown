# Findings — Backtest Sentiment-Weighted DCA (F&G)

**Tanggal validasi:** 2026-07-12
**Video:** How to Use the Fear & Greed Index for Bitcoin — On-Chain Mind, 2025-02-23
**Script:** `analyze_fg_sentiment_weighted_dca.py`
**Data:** `data_master_all_metrics.csv`. F&G mulai 2018-02-01 → **hanya 2 cycle, Cycle B masih berjalan (bear ongoing, harga $63.9K per 2026-07-12).**

---

## Pertanyaan

Klaim video: DCA berbobot sentimen (beli lebih banyak saat fear, kurangi saat greed) "historically performed well over multiple cycles" — tanpa angka. Apakah outperformance material (>5% BTC lebih banyak) DAN konsisten di kedua cycle?

## Metode

- Beli mingguan tiap Senin, 2018-02-05 s/d 2026-07-12 (n=440 pembelian).
- Uniform $100/minggu vs weighted: bobot dari raw F&G di HARI beli — <25→2.0x, 25-50→1.5x, 50-75→1.0x, ≥75→0.5x (anti lookahead: F&G tersedia di tanggal beli).
- Total budget dinormalisasi sama. Catatan: normalisasi ex-post, tapi metrik per-cycle (avg cost basis, BTC per $) scale-invariant sehingga tidak terdistorsi.
- Split: Cycle A = 2018-02..2022-11-21, Cycle B = 2022-11-22..sekarang.
- Satu varian sensitivity (bobot agresif 3.0/2.0/1.0/0.25) — dilaporkan apa adanya, bukan hunting threshold.

## Hasil

| Periode | n beli | % minggu F&G<50 | Avg cost uniform | Avg cost weighted | Keunggulan BTC |
|---|---|---|---|---|---|
| Full 2018-02..now | 440 | 57% | $15,993 | $14,887 | **+7.4%** |
| Cycle A 2018-2022 | 251 | 68% | $10,637 | $10,199 | **+4.3%** |
| Cycle B 2022-now | 189 | 44% | $48,263 | $48,112 | **+0.3%** |

Varian agresif: full +11.1%, Cycle A +5.8%, Cycle B **-0.1%** (malah kalah tipis).

- Angka full-period (+7.4%) menyesatkan: sebagian besar berasal dari efek alokasi lintas-cycle (Cycle A punya lebih banyak minggu fear DAN harga jauh lebih murah, jadi bobot otomatis memindahkan budget ke era harga murah). Per-cycle — ukuran skill yang sebenarnya — hasilnya +4.3% dan +0.3%.
- Mekanismenya lemah: korelasi F&G di hari beli vs return 52 minggu ke depan hanya -0.09 (n=388).
- Cycle B masih berjalan: pembelian berbobot 1.5-2x selama bear 2025-26 ($64-90K) belum ketahuan hasil akhirnya — verdict pakai harga sekarang.

## Verdict

**PARTIAL (cenderung NOT SUPPORTED untuk klaim kuat video).** Sentiment-weighted DCA tidak pernah materially lebih buruk dari uniform (downside-nya ~nol), tapi gagal dua-duanya kriteria: outperformance TIDAK material di level per-cycle (+4.3% dan +0.3%, di bawah ambang 5%) dan TIDAK konsisten (Cycle B praktis nol, varian agresif malah negatif). Klaim video "performed well over multiple cycles" overstated — yang benar: "sedikit lebih baik di cycle lama, netral di cycle baru". **n=2 cycle, Cycle B belum selesai.**

## Implikasi ke framework (rekomendasi, bukan perubahan)

- Tidak ada alasan menambahkan sentiment-weighting ke strategi akumulasi framework — K4 (DCA di Z1 dengan tranche + confidence) sudah jauh lebih tajam daripada tilt F&G ±0.5-2x sepanjang waktu.
- Kalaupun dipakai di luar framework (akumulasi pasif), ekspektasinya cuma perbaikan kecil dan tidak pasti, bukan edge.
