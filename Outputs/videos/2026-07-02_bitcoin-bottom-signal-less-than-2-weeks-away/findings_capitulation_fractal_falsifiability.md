# Findings: Time-Based Capitulation Fractal — Falsifiability Check

**Video sumber:** Bitcoin Magazine Pro, "Bitcoin Bottom Signal (Less Than 2 Weeks Away)", 2026-07-02
**Tanggal analisis:** 2026-07-28
**Script:** `analyze_capitulation_fractal_falsifiability.py`
**Data:** `data_master_all_metrics.csv`, kolom `btc_price`, sampai tanggal terakhir tersedia **2026-07-15**

## Klaim yang diuji
Pembicara memproyeksikan "time-based capitulation" / bottom sekunder sekitar **12 Juli 2026**, dihitung dari day-count sejak "initial shock" awal 2026, mereplikasi fractal 156 hari (2022) dan 126 hari (2018-19).

## Definisi event (ditetapkan sebelum lihat hasil)
- **Local low dalam window prediksi** = harga terendah `btc_price` pada 2026-07-05 s/d 2026-07-19 (±1 minggu dari prediksi).
- **Lower-low baru** = harga di window < harga terendah 30 hari kalender SEBELUM window (2026-06-05 s/d 2026-07-04).
- Anti-lookahead: hanya pakai data yang tersedia di file, tidak menebak data belum ter-update.

## Keterbatasan kritis: data terpotong
Data terakhir tersedia **2026-07-15** — window prediksi baru berjalan 11 dari 15 hari, terpotong 4 hari sebelum window selesai (2026-07-19). **Verdict di bawah bersifat sementara/partial.**

## Hasil
| Metrik | Nilai |
|---|---|
| ATH siklus ini | 2025-10-06 @ $124,715 |
| Local low di dalam window (sejauh data ada) | 2026-07-13 @ $61,910.01 |
| Local low 30 hari sebelum window | 2026-06-30 @ $58,460.01 |
| Window low < pre-window low (lower-low baru)? | Tidak |
| Harga hari terakhir data (2026-07-15) | $65,097.92 |
| Net naik dari window-low sampai hari terakhir data? | Ya |

Sejauh data tersedia (3 hari pertama pasca 12 Juli): harga TIDAK membuat lower-low baru di dalam window — level terendah bear market ini masih $58,460 (30 Juni), lebih rendah dari titik terendah di dalam window prediksi ($61,910, 13 Juli). Harga per 15 Juli sudah naik dari window-low.

## Verdict
Belum bisa difalsifikasi maupun dikonfirmasi penuh — data cutoff (2026-07-15) hanya mencakup 3 hari pertama dari window ±1 minggu. Sejauh diamati: tidak ada lower-low baru, harga net naik dari titik terendah window. Ini **konsisten dengan** (bukan membuktikan) klaim video, tapi n=1 episode (bear market 2026 ini saja) dan proyeksi "day-count fractal" sendiri berbasis cuma 2-3 contoh historis (156 hari 2022, 126 hari 2018-19, disinggung juga 2015) — sample terlalu kecil untuk klaim pola berulang yang solid. Perlu data lanjutan (setelah 2026-07-19) untuk verdict final — dicatat sebagai backlog.

Bahasa probabilistik: cenderung belum terfalsifikasi sejauh ini, bukan terkonfirmasi.
