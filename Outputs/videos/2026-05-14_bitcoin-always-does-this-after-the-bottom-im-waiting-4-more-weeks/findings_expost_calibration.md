# Findings — Kalibrasi ex-post call Matt Crosby (video 2026-05-14)

**Tanggal validasi:** 5 Agustus 2026
**Script:** [`analyze_expost_calibration.py`](analyze_expost_calibration.py)
**Event CSV:** [`events_expost_calibration.csv`](events_expost_calibration.csv)
**Data:** `data_master_all_metrics.csv`, **berakhir 2026-07-15** (62 hari setelah tanggal video)

> **Sifat validasi ini:** deskriptif, bukan uji mekanik indikator. Satu episode = **n=1**.
> Tidak ada klaim statistik yang bisa ditarik dari sini — gunanya semata untuk mengkalibrasi
> seberapa berat menimbang sumber ini ke depan.

> **PARTIAL:** window 8 minggu tertutup; forward return 60 hari dari sentuhan awal Juni
> **belum tertutup**. Semua yang belum tertutup ditandai eksplisit.

---

## (a) Verifikasi angka yang disebut di video — per 2026-05-14

| Yang disebut video | Nilai aktual 2026-05-14 | Cocok? |
|---|---|---|
| STH-RP "sekitar $79.000" | `sth_cost_basis` = **$78.585** | **Ya**, akurat |
| Harga saat rekaman (~$78,7–79,7k dari frame) | close **$81.060**; rentang 7 hari $79.455–$81.868 | Wajar — dia merekam saat pullback intraday |
| 200 DMA sebagai titik rejection | `200_dma` = **$82.124** (harga = 98,7% dari 200DMA) | **Ya**, harga persis di bawahnya |
| "1-year MA" sebagai deciding point | 365D MA rolling = **$95.694** (harga = 84,7%) | Ya, jauh di atas — konsisten dengan "belum break" |
| "we got close to this 200-weekly MA" | `200_wma` = **$60.964**, jauh **di bawah** harga | **Tidak** — kemungkinan slip lisan (sudah ditandai Stage 1) |

Konteks framework 2026-05-14: `realized_price` $54.254 · AVIV Mean $98.905 · AVIV Upper $113.537 · **zona = Z3**.

---

## (b) Call "top mid-Mei, lalu beberapa minggu turun" — **KENA**

- Close tertinggi **setelah** 2026-05-14: **$79.064 @ 2026-05-15**. Harga tidak pernah lagi melampaui close hari video.
- Trajectory dari close hari video ($81.060):

| Horizon | Close | Perubahan | Zona |
|---|---|---|---|
| +2 minggu (2026-05-28) | $73.579 | −9,2% | ZD |
| +4 minggu (2026-06-11) | $63.575 | −21,6% | ZD |
| +6 minggu (2026-06-25) | $59.450 | −26,7% | ZD |
| +8 minggu (2026-07-09) | $63.369 | −21,8% | ZD |

- Max drawdown dari close hari video: **−27,9%** (low $58.460 @ 2026-06-30).

**Catatan koreksi:** klaim presisi "highest closing price yang kita lihat pada 10 Mei" **tidak akurat** —
highest close di window ±30/45/60/90 hari sekitar tanggal itu jatuh pada **11 Mei 2026 ($81.868)**, bukan 10 Mei.
Selisih satu hari tidak material untuk arah call-nya, tapi relevan karena presisi "almost to the exact day"
adalah bagian dari argumen chart DXY-YoY-offset-100-hari (IC3).

---

## (c) Base case "$60.000 adalah low, >50% chance" — **MELESET (tipis)**

- Minimum close setelah video: **$58.460 @ 2026-06-30** → **$60.000 tertembus**.
- Hari close < $60.000: **3** (25–30 Juni 2026).
- Hari close di mid-$50k ($55.000–$59.999): **3** → skenario yang dia beri probabilitas **20–25%** ternyata **terjadi**.
- Hari close < $55.000: **0**.
- Anchor "low Februari ~$60k": min close Jan–Mar 2026 = **$62.840 @ 2026-02-05** (bukan tepat $60k) → tertembus **−7,0%**.

Jadi: base case-nya pecah, tapi hanya 3 hari dan hanya −2,6% di bawah angka yang dia sebut.
Skenario ekor yang dia beri 20–25% justru yang terealisasi. Ini kalibrasi yang **wajar**, bukan miss besar.

---

## (d) "DCA agresif di ~$70.000" — **level tersentuh, timing-nya belum terbukti untung**

- Sentuhan pertama close ≤ $70.000: **2026-06-02 @ $66.699**. Total hari close ≤ $70.000: **44** (s/d akhir data).
- Forward return 30 hari dari 2026-06-02: **−7,4%** ($61.793 @ 2026-07-02).
- Forward return 60 hari: **BELUM TERTUTUP (PARTIAL)** — baru 43 hari; sejauh ini −2,4% per 2026-07-15.

Artinya harga memberikan level yang dia mau, lalu **terus turun ~7% lagi** dalam sebulan berikutnya —
persis skenario yang framing "win-win" di video tidak akui sebagai kekalahan.

---

## (e) Zona resistance $81.000–$85.000 — **tidak pernah diuji ulang**

- Hari close di band $81k–$85k setelah 2026-05-14: **0**. Episode masuk band: **0**.
- Hari close > $85.000: **0**. Break bertahan ≥3 hari: **tidak**.

Harga langsung menjauh ke bawah, jadi zona ini tidak pernah dites lagi. Klaimnya **tidak terfalsifikasi
maupun terkonfirmasi** — dan itu sendiri menunjukkan kenapa level harga absolut yang lebar (~5%)
sulit dinilai: ia hanya "bekerja" pada satu sentuhan yang sudah lewat.

---

## (f) Posisi per tanggal data terakhir (2026-07-15)

| Metrik | Nilai | Rasio harga |
|---|---|---|
| `btc_price` | $65.098 | — |
| `sth_cost_basis` (STH RP) | $67.143 | **0,970× — harga DI BAWAH STH RP** |
| `realized_price` (RP) | $52.740 | 1,234× |
| `lth_cost_basis` (LTH RP) | $49.890 | — |
| `200_dma` | $73.534 | 0,885× |
| 365D MA (rolling) | $88.728 | 0,734× |
| `200_wma` | $62.945 | — |
| `cvdd` | $49.106 | 1,326× |
| AVIV Mean / Upper | $96.970 / $110.962 | — |
| **Zona framework** | **ZD** | — |

Distribusi zona harian 2026-05-15 → akhir data: **ZD 61 hari, Z3 1 hari**.
Reclaim STH RP yang dirayakan pasar di awal Mei sudah **hilang seluruhnya** — harga kembali di bawah STH RP.

---

## Kesimpulan

Dari 5 call yang bisa dinilai: **2 kena (arah top mid-Mei & beberapa minggu turun; STH-RP jadi resistance,
bukan support), 1 meleset tipis (base case $60k tertembus 3 hari, −2,6%), 1 tersentuh tapi belum terbukti
menguntungkan (DCA $70k → −7,4% dalam 30 hari), 1 tidak pernah diuji ulang (zona $81–85k).** **n=1 episode**,
jadi ini kalibrasi deskriptif, bukan hit rate.

Yang paling berguna dipetik: **arah makronya benar, angka absolutnya tidak** — dan justru bagian yang dia
sebut paling presisi ("almost to the exact day", 10 Mei) yang salah satu hari, sementara skenario ekor
20–25% yang dia anggap tidak mungkin justru terjadi. Konsisten dengan prinsip framework: sumber ini
**cenderung** berguna untuk arah/konteks, tidak untuk anchor angka.

Semua angka yang dibaca dari frame video (STH-RP $79.000, 200-week MA ~$57k, drawdown −35%, spike fractal
~$95k) tetap berlabel **low confidence dari resolusi frame** dan tidak dipakai sebagai anchor kesimpulan.
