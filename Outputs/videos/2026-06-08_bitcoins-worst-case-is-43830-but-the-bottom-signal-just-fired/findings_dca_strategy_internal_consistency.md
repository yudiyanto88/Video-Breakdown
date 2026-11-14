# Findings — Konsistensi Internal Strategi DCA Presenter

**Tanggal validasi:** 2026-07-30
**Script:** `analyze_dca_strategy_internal_consistency.py`
**Event CSV:** `events_dca_strategy_internal_consistency.csv`

## Klaim yang diuji

Presenter (video yang sama, 2026-06-08) menyatakan basis akumulasi agresifnya adalah
"base-case downside cuma 5-6-7% lower low" dari level saat itu. Tapi model drawdown
proyeksi presenter SENDIRI (lihat `findings_bear_drawdown_model.md`) memproyeksikan
central case $55,311 dan worst case $43,830 dari ATH $126,219.03. Ini murni cek
konsistensi angka internal antar klaim di video yang sama — bukan validasi terhadap
ground truth eksternal.

## Perhitungan gap

Harga BTC pada 2026-06-08 (tanggal video) = **$63,029**.

| Skenario | Harga | Gap dari $63,029 |
|---|---|---|
| Klaim verbal presenter: -5% | $59,878 | -5% |
| Klaim verbal presenter: -7% | $58,617 | -7% |
| Model central case presenter ($55,311) | $55,311 | **-12.2%** |
| Model worst case presenter ($43,830) | $43,830 | **-30.5%** |

## Verdict

**[VALIDASI — 2026-07-30, CLOSED]** Klaim verbal presenter ("base-case downside cuma 5-7% lower low") **tidak konsisten** dengan model drawdown kuantitatif miliknya sendiri di video yang sama: central case model tersebut ($55,311) menyiratkan potensi turun **-12.2%** dari harga saat direkam ($63,029) — sekitar 2x lebih dalam dari klaim verbalnya — dan worst case model ($43,830) menyiratkan **-30.5%**, sekitar 5x lebih dalam. Ini adalah inkonsistensi internal murni (dua klaim dari presenter yang sama, di video yang sama, saling bertentangan secara matematis), bukan soal apakah proyeksinya benar terhadap data eksternal. Relevan sebagai flag kehati-hatian: argumen "asymmetric risk/reward" yang jadi basis strategi DCA presenter meremehkan downside risk dibanding model kuantitatif yang dia bangun sendiri di segmen sebelumnya pada video yang sama.
