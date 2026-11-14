# Validasi: Cross Price vs Fair Value sebagai penanda regime change

**Insight diuji:** [STRATEGI]/[INDIKATOR CUSTOM] Cross Price vs Fair Value sebagai penanda perubahan rezim — cross-down/cross-up ditampilkan di Gambar 2 sebagai sinyal regime-change (leg turun 2022, pemulihan 2023, penurunan & titik terkini 2025-26).

**Tanggal validasi:** 2026-07-29
**Script:** `analyze_volatility_channel_fair_value_cross.py`
**Data event:** `events_volatility_channel_fair_value_cross.csv`

---

## Definisi kerja

Karena formula "Fair Value" vendor tidak diketahui persis, dipakai proxy yang sudah tersedia di `data_master_all_metrics.csv` — tidak perlu menebak formula volatility-band:

- **Proxy utama:** `true_market_mean_price` (Cointime true market mean) — dipilih karena konsepnya paling dekat dengan "central price average" yang dideskripsikan vendor sebagai trend indicator
- **Proxy sensitivitas:** `200_wma` (200-week moving average) — pembanding, konsep serupa tapi lebih lambat/lag lebih besar
- Kedua proxy tersedia sejak 2010 (full history, tidak ada isu data mulai belakangan)
- **Event:** raw sign-change — setiap kali `btc_price` melintasi proxy (dari atas ke bawah = cross-down, dari bawah ke atas = cross-up), dihitung sebagai satu event tanpa cooldown tambahan (cross adalah kejadian diskrit, tapi whipsaw diukur terpisah di bawah)
- **Whipsaw:** cross yang arahnya terbalik (cross balik ke arah semula) dalam ≤30 hari sejak cross tersebut
- **Regime change (genuine):** cross yang arahnya bertahan >90 hari sebelum cross balik berikutnya
- Sisanya (>30 hari tapi ≤90 hari) diklasifikasi **ambiguous**

## Hasil

| Proxy | n total (down/up) | Sebaran cycle terbesar | % whipsaw (≤30 hari) | % regime change (>90 hari) | % ambiguous |
|---|---|---|---|---|---|
| true_market_mean_price | 104 (52/52) | 2013-15: 41 event (39% dari total) | 72,1% | 10,6% (n=11) | 16,3% |
| 200_wma | 69 (34/35) | 2013-15: 31 event (45% dari total) | 81,2% | 10,1% (n=7) | 8,7% |

**Independensi sample:** hampir separuh dari seluruh cross (39-45%) terjadi di satu periode volatil tunggal (2013-15) — sample sangat tidak independen lintas cycle, hasil dominan dibentuk oleh satu era harga BTC yang jauh lebih volatil dibanding era-era belakangan.

**Perbandingan dengan trigger K-node established** (direplikasi persis dari `analyze_k3_stage_comparison.py`, window match ±30 hari terhadap: AVIV Upper cross-down streak≥7 hari untuk K1/K3, STH RP cross RP untuk transisi Z1→Z2):
- true_market_mean_price: dari 11 "regime change" genuine, **2 (18,2%) berdekatan** dengan trigger K-node yang sudah ada
- 200_wma: dari 7 "regime change" genuine, **0 (0%) berdekatan**

## Verdict

Klaim vendor bahwa cross Price-vs-Fair-Value menandai regime change **tidak reliable** — base rate whipsaw sangat tinggi (72-81% dari seluruh cross, n=104 dan n=69) berarti mayoritas cross terbalik lagi dalam 30 hari, kontras dengan narasi Gambar 2 yang hanya menampilkan beberapa cross "bersih" (2 cross-down + 2 cross-up terpilih dari total puluhan). Cek data mentah 2026 menunjukkan banyak cross beruntun dalam hitungan hari (whipsaw), bukan pola rapi "2 down lalu 1 up" seperti digambarkan di chart — konsisten dengan cherry-picking visual oleh pembuat chart.

Namun sinyal ini juga **tidak largely redundant** dengan trigger K-node yang sudah established di framework (overlap hanya 0-18%) — kalau reliable, secara teori bisa menambah informasi baru. Masalahnya justru base rate whipsaw yang tinggi: di titik cross terjadi, tidak bisa dibedakan real-time mana yang whipsaw (72-81% kemungkinan) vs genuine regime change (10-11%) — sehingga praktis sulit dipakai sebagai sinyal actionable tanpa konfirmasi tambahan.

---

**[VALIDASI — 2026-07-29, CLOSED]** Cross Price vs proxy Fair Value (true_market_mean_price/200_wma) mayoritas whipsaw (72-81% dari n=104/69 cross sepanjang histori penuh, reversed ≤30 hari) — bukan penanda regime-change yang reliable. Hanya 10-11% (n=11/104, n=7/69) bertahan >90 hari sebagai genuine regime change, dan dari situ cuma 0-18% (n=2/11, n=0/7) berdekatan ±30 hari dengan trigger K-node established — jadi **tidak largely redundant**, tapi base rate whipsaw tinggi membuat sinyal ini sulit diandalkan real-time. Sebaran didominasi siklus 2013-15 (39-45% dari total n) — independensi sample lemah, hasil dominan dibentuk satu era volatil.
