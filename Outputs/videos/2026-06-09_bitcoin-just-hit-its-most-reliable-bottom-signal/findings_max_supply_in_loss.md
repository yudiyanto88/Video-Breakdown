# Findings — Apakah >70% supply-in-loss "belum pernah terjadi"?

**Video:** Bitcoin Just Hit Its Most Reliable Bottom Signal (On-Chain Mind, 2026-06-09)
**Tanggal validasi:** 2026-07-19
**Data:** `data_master_all_metrics.csv`, kolom `percent_btc_in_loss`
**Script:** `analyze_bottom_signals.py`

## Klaim video
Target harga $20k–$30k akan mendorong >3,5 juta BTC ke loss → >70% network underwater, level yang "belum pernah terjadi / off the scale", sehingga target serendah itu "mathematically unsound".

## Definisi event
Cari nilai MAKSIMUM all-time `percent_btc_in_loss` dan tanggalnya; hitung berapa hari yang pernah ≥60% dan ≥70%.

## Hasil
- **MAX all-time = 63.77%** pada **2015-08-24** (harga ~$211).
- Tidak pernah ≥70%.
- Hari dengan ≥60%: **12 hari**, terkonsentrasi di klaster Aug-2015 & Feb-2019.
- Komponen "3,5 juta BTC di $20–30k" butuh URPD / full cost-basis distribution → **NEEDS-DATA** (tidak tersedia di dataset kita), tidak diuji.

## Interpretasi
- Bagian yang testable (>70% belum pernah terjadi) benar: ceiling historis ~63.8%, dan >60% saja sangat langka (12 hari).
- Jadi reading mendekati/di atas 70% memang akan "off the scale" secara historis. Namun "belum pernah terjadi" ≠ "tidak mungkin terjadi" — distribusi supply tiap cycle berbeda; argumen ini konteks, bukan bukti floor.

## Verdict
**[VALIDASI — 2026-07-19, CLOSED]** CONFIRMED (sebagian): >70% network underwater memang belum pernah terjadi — ceiling historis `percent_btc_in_loss` hanya ~63.8% (2015-08-24), dan cuma 12 hari yang pernah ≥60% (klaster Aug-2015 & Feb-2019). Reading mendekati/di atas 70% akan "off the scale" secara historis. Komponen URPD (3,5jt BTC di $20-30k) tidak bisa diuji — data URPD tidak tersedia.
