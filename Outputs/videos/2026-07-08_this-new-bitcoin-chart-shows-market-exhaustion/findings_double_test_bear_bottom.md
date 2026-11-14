# Uji Hipotesis: Pola "Double Test" Lower Support Band per Bear Market

- **Asal klaim:** video "This New Bitcoin Chart Shows Market Exhaustion" (Joao Wedson / Alphractal, 2026-07-08) — di bear market harga cenderung menguji lower support band DUA kali membentuk "consolidated bottom" (pembicara sendiri inkonsisten: 2x, 1x, 2x); bear berjalan baru test sekali → ekspektasi retest kedua. Relevan ke K4: worth-kah menahan tranche DCA menunggu "test kedua"?
- **Tanggal uji:** 2026-07-13
- **Data:** `btc_price`, `sth_cost_basis`, `realized_price`, `cvdd` dari `data_master_all_metrics.csv` (Onchain-Dashboard)
- **Script:** `analyze_double_test_bear_bottom.py` (folder ini). Tabel episode: `_bear_test_episodes.csv`
- **Catatan proxy:** lower band SMB Alphractal black box. Proxy: (1) episode Z1 framework (price < STH RP DENGAN STH RP < RP), (2) varian dalam: price/CVDD < 1.15. Episode terpisah = >=30 hari di luar zona di antaranya.

## Definisi event (ditetapkan sebelum lihat hasil)

- "Test" = episode Z1 / episode P/CVDD<1.15, merge rule 30 hari. Semua at-gate (close hari itu).
- Bear windows: 2011-12 (context, data awal noisy), 2014-15, 2018-19, Covid-2020, 2022, 2025-26 (berjalan). Final bottom = low absolut close dalam window.
- Simulasi K4: pool 100, 4 tranche x 25 (proxy confidence 3-dari-4), jarak antar tranche >=30d, eksekusi di hari Z1; sisa pool masuk di Signal D (3 hari berturut close > STH RP setelah episode Z1 terakhir). Strategi A = mulai episode #1; Strategi B = tahan semua, mulai episode #2 (kalau tidak pernah datang → seluruh pool masuk di Signal D).

## Hipotesis & Hasil

| Hipotesis | Verdict | Ringkasan |
|-----------|---------|-----------|
| Bear cenderung double test lower band | **NOT-SUPPORTED** | Proxy Z1: 2014-15 = 2 episode, tapi 2018-19 = **1**, Covid = **0** (Z1 tidak pernah aktif — ordering tak terbalik), 2022 = **1**; context 2011-12 = 3. Proxy CVDD<1.15: 2011-12 = 1, 2014-15 = 2, 2018-19 = 1, Covid = 1, 2022 = 1. "Dua test" hanya kejadian di **1 dari 4 bear selesai** (2014-15) di kedua proxy — mayoritas bear cuma SATU test dalam |
| Final bottom terbentuk di test kedua (consolidated bottom) | **NOT-SUPPORTED** | Proxy CVDD: final bottom di episode #1 pada 4/4 bear yang punya episode (2011-12, 2014-15, 2018-19 @$3,281 Des 2018, Covid, 2022 @$15,774 Nov 2022). Satu-satunya "test kedua" nyata (Aug-Okt 2015) adalah HIGHER low +18.0% vs CVDD-episode #1 (Z1 proxy: lower low tipis -2.8%, jarak 200 hari) — retest, bukan tempat bottom terbentuk |
| Menahan tranche K4 menunggu "test kedua" memperbaiki avg entry | **NOT-SUPPORTED** | Strategi A menang/setara di **4/4 bear teruji**: avg entry B vs A = +13.8% (2011-12), **+3.1% (2014-15 — bahkan di satu-satunya bear yang test keduanya DATANG, menunggu tetap lebih mahal)**, +7.3% (2018-19, test kedua tidak pernah datang), +8.8% (2022, idem). Risiko test kedua tidak pernah datang: **2 dari 4 bear (50%)** pada proxy Z1 |

## Detail penting

- **n = 4 bear selesai + 1 berjalan** — sample kecil (klaim video sendiri n≈3-4 dan diakui inkonsisten). Tapi arah seragam lintas dua proxy dan simulasi.
- Keterbatasan proxy Z1 strict: ordering STH RP < RP sering terbalik TERLAMBAT — di 2014-15 dan 2018-19 low absolut bear jatuh SEBELUM episode Z1 pertama dimulai. Varian CVDD<1.15 menangkap low absolut lebih baik (final bottom selalu di dalam episode #1-nya).
- Status bear berjalan (per 2026-07-12: price $63,877, STH RP $67,589, RP $52,841, P/CVDD 1.30): **NOL** test menurut kedua proxy — Z1 belum pernah aktif (STH RP masih JAUH di atas RP, gap ~28%), CVDD belum tersentuh. Harga memang sudah 260 hari berturut di bawah STH RP (sejak 2025-10-10, satu blok tunggal), tapi secara framework K4 formal belum buka. Framing video "sudah test sekali, tunggu test kedua" tidak map ke struktur zona framework sama sekali.
- Implikasi K4: tabel DCA existing (deploy per confidence sejak Z1 aktif) sudah optimal vs strategi menunggu retest — jangan tahan tranche untuk "test kedua".

## Verdict akhir

**NOT SUPPORTED.** "Double test" bukan pola dominan: hanya 1 dari 4 bear selesai yang punya dua test (2014-15), dan test keduanya higher low +18% (CVDD) — bukan tempat final bottom. Final bottom terbentuk di episode dalam PERTAMA pada semua bear yang teruji. Simulasi K4: menunggu test kedua memperburuk avg entry di 4/4 bear (+3.1% s/d +13.8%), dengan risiko 50% test kedua tidak pernah datang. Rekomendasi: tolak modifikasi K4; DCA sesuai tabel begitu Z1 aktif.
