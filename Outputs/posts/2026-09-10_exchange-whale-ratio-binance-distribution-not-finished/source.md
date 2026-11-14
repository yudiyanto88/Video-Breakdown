# BTC whale distribution belum selesai — Exchange Whale Ratio Binance (SMA 200/365)
**Sumber/Akun:** tidak diketahui (tweet di-paste Yudi tanpa handle; chart di-generate dari CryptoQuant)
**URL:** -
**Tanggal post:** tidak diketahui → dipakai tanggal analisis **2026-09-10**. Cross-check: label harga di chart `$78.4K` konsisten dengan `btc_price` di `data_master_all_metrics.csv` sekitar 2026-09-07 ($78.905) — jadi post kemungkinan besar dibuat 7–10 Sep 2026, bukan lebih lama.
**Jenis input:** tweet (teks) + 1 foto chart

---

## Teks post

> $BTC whale distribution doesn't look finished yet.
>
> Whale activity on Binance is still elevated, and the 200D/365D averages haven't rolled over like they did during previous resets.
>
> Until that cooldown starts, the bearish case stays on the table.

## Gambar 1 — Bitcoin: Exchange Whale Ratio - Binance (CryptoQuant)

- **Metrik:** Exchange Whale Ratio (EWR) untuk exchange **Binance saja**, di-plot bareng Price USD.
  Legend memuat 6 series, tapi 3 di antaranya **dicoret (di-toggle OFF)** dan tidak digambar: `Exchange Whale Ratio` (raw), `Exchange Whale Ratio-SMA(30)`, `Exchange Whale Ratio-SMA(100)`.
  Series yang benar-benar tampil hanya **3**: `Price USD` (garis hitam solid, sumbu kanan log), `Exchange Whale Ratio-SMA(200)` dan `Exchange Whale Ratio-SMA(365)` (dua garis putus-putus ungu/biru, sumbu kiri).
  Catatan definisi CryptoQuant: EWR = rasio 10 inflow transaksi terbesar terhadap total inflow ke exchange itu. Nilai tinggi = porsi inflow didominasi entitas besar ("whale").
- **Platform chart:** CryptoQuant (watermark + copyright di kanan bawah).
- **Timeframe:** ~akhir 2018 sampai edge kanan ≈ September 2026. Tick tahun terbaca: 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026.
- **Sumbu:** kiri = EWR, skala 0.15–0.50 linear. Kanan = harga BTC, skala **log**, label $4K / $6K / $8K / $10K / $20K / $40K / $60K / $100K + label harga terakhir `$78.4K`.
- **Anotasi pembuat:** ada 4 kelompok anotasi manual (bukan bagian chart CryptoQuant).
  1. **3 batang vertikal abu-abu** (band waktu) di ~Jun 2020, ~Des 2022, ~Mei 2025.
  2. **3 lingkaran merah** persis di batang abu-abu itu, ditaruh di titik di mana **SMA(200) dan SMA(365) bertemu/menyilang di puncak lokal**.
  3. **3 panah hitam** turun-ke-kanan yang berangkat dari tiap lingkaran, menunjukkan periode **penurunan berkepanjangan** kedua SMA setelahnya — inilah yang tweet sebut "reset"/"cooldown".
  4. **1 oval biru muda** di ujung kanan (kondisi sekarang) + **panah kecil menunjuk ke bawah** — menandai bahwa SMA baru saja menekuk sedikit di edge, TAPI belum jadi penurunan berkepanjangan seperti 3 kejadian sebelumnya. Ini pembanding visual untuk klaim "haven't rolled over yet".
- **Angka terbaca** *(semuanya **low confidence dari resolusi gambar** — hasil kalibrasi piksel terhadap tick sumbu, jangan dipakai sebagai anchor kesimpulan)*:
  | Anotasi | Perkiraan tanggal | Perkiraan level EWR-SMA | Harga BTC saat itu (dari chart) |
  |---|---|---|---|
  | Lingkaran 1 | ~Jun 2020 | ~0.28–0.29 | ~$9–10K |
  | Lingkaran 2 | ~Des 2022 | ~0.29–0.30 | ~$16–17K |
  | Lingkaran 3 | ~Mei 2025 | ~0.40–0.41 | ~$95–100K |
  | Kondisi sekarang (oval biru) | ~Sep 2026 | ~0.45–0.48 (puncak ~0.48) | $78.4K (label chart) |
  | Palung SMA terendah pasca-2023 | ~akhir 2023 | ~0.185–0.20 | ~$30K |
- **Apa yang ditunjukkan chart (deskriptif, belum interpretasi):**
  - EWR-SMA(200) dan SMA(365) Binance bergerak dalam **uptrend sekuler** sejak ~akhir 2023: naik dari palung ~0.19 ke ~0.47–0.48 sekarang, hampir tanpa jeda besar.
  - Setiap puncak yang dilingkari **lebih tinggi dari puncak sebelumnya**: ~0.28 (2020) → ~0.29 (2022) → ~0.41 (2025) → ~0.48 (sekarang, belum jadi puncak terkonfirmasi). Level sekarang adalah yang **tertinggi di seluruh rentang chart**.
  - Pola yang dilingkari pembuat identik di 3 kejadian: SMA(200) dan SMA(365) konvergen/menyilang di puncak lokal → keduanya turun berbulan-bulan.
  - Konteks harga setelah tiap lingkaran (terbaca dari garis hitam): setelah Jun 2020 harga **naik keras** (~$9K → $60K+); setelah Des 2022 harga **naik** dari area bottom (~$16K → $30K+); setelah Mei 2025 harga masih **naik dulu** ke puncak ~$110K sebelum akhirnya turun ke ~$60K di 2026 dan rebound ke $78.4K.
  - Di edge kanan, garis hitam (harga) turun dari puncak ~$100K ke ~$60K lalu rebound ke $78.4K, sementara SMA EWR terus **naik** sepanjang penurunan harga 2026 itu.
