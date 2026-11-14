# Findings — 200-week MA sebagai cyclical floor / multi-year accumulation zone

**Video:** Bitcoin's Trend Is Bearish — Here's Where It Flips (On-Chain Mind, 2026-08-11)
**Tanggal validasi:** 2026-08-12
**Script:** `analyze_200wma_cyclical_floor.py`
**Event CSV:** `events_200wma_cyclical_floor.csv`

---

## Klaim yang diuji

Video mengklaim: (1) 200-week MA saat ini ~$63,800 dan harga persis di level ini; (2) 200-week MA sudah compounding "konsisten 30%/tahun" selama 4 tahun terakhir; (3) "setiap episode historis di mana harga menyentuh atau di bawah 200-week MA selalu jadi multi-year accumulation zone".

## Catatan data

`data_master_all_metrics.csv` mentok update di **2026-07-15** — gap 27 hari ke tanggal video (2026-08-11). Semua angka "current" pakai 2026-07-15 sebagai basis, dengan ekstrapolasi tren linear jangka pendek untuk sanity-check level tertentu ke tanggal video. Ekstrapolasi BUKAN pengganti data aktual — dicatat eksplisit di setiap angka yang diekstrapolasi.

## Definisi event (ditetapkan sebelum menghitung)

- `200_wma` = rolling 1400 hari kalender dari `btc_price`, matang mulai 2012-11-03.
- Event "price < 200wma" = raw run minimal 5 hari berturut-turut di bawah garis.
- Merge rule: dua run digabung jadi satu episode kalau gap antar-run < 14 hari.
- "Floor holds" = harga tidak pernah breach lebih dari 10% di bawah titik terendah (low) episode dalam 180 hari setelah episode berakhir. Kriteria ini ditetapkan sebelum melihat hasil.

## Hasil — daftar episode

| Episode | Durasi (hari) | Low | Tanggal low | Zone @start | Zone @low | Status floor |
|---|---|---|---|---|---|---|
| 2015-08-22 → 2015-09-27 | 37 | $210.59 | 2015-08-24 | Z1 | Z1 | HOLDS |
| 2020-03-14 → 2020-03-18 | 5 | $5,108.46 | 2020-03-16 | ZC | ZC | HOLDS |
| 2022-06-16 → 2022-07-26 | 41 | $18,973.10 | 2022-06-18 | ZC | ZC | **BREACH** |
| 2022-08-19 → 2023-03-16 | 210 | $15,774.48 | 2022-11-21 | ZC | Z1 | HOLDS |
| 2023-06-10 → 2023-06-16 | 7 | $25,172.51 | 2023-06-14 | ZD | ZD | HOLDS |
| 2023-08-17 → 2023-10-15 | 60 | $25,178.94 | 2023-09-11 | ZD | ZD | HOLDS |
| 2026-06-24 → 2026-07-03 | 10 | $58,460.01 | 2026-06-30 | ZD | ZD | INCOMPLETE (data forward <180d) |

**n = 7 episode total, n evaluable = 6** (episode 2026 masih ongoing/tidak cukup data forward, dikeluarkan dari evaluasi hit-rate).

## Hit rate

**5 HOLDS / 1 BREACH dari 6 episode evaluable = 83%.** Episode BREACH (Jun–Jul 2022, low $18,973) ditembus lebih dari 10% lebih dalam oleh crash FTX bulan November 2022 (low episode berikutnya $15,774, -16.9% dari low episode sebelumnya) — jadi klaim video "selalu jadi floor yang bertahan" **tidak 100% benar** secara historis.

## Independensi sample

Dari 6 episode evaluable, hanya **~4 siklus independen**: 2015 (bear tail-end), 2020 (COVID crash — isolated one-off), 2022 (bear market — 2 episode berkorelasi, keduanya bagian dari drawdown yang sama), 2023 (post-bear consolidation — 2 episode berkorelasi). Episode 2022 dan 2023 masing-masing punya 2 kejadian yang berasal dari fase market yang sama, bukan siklus independen — hasil didominasi oleh bear market 2022 secara khusus (1 dari 2 episode 2022 itu yang justru gagal).

## Overlap dengan struktur zona framework

Semua 7 episode overlap dengan zona akumulasi kita sendiri (ZC/Z1/ZD) — 100% overlap. Tapi breakdown-nya: **3 dari 7 episode cuma mencapai ZD (dip moderat)**, bukan ZC/Z1 (capitulation penuh). Artinya "harga di bawah 200wma" tidak otomatis berarti kondisi capitulation ekstrem di framework kita — kadang cuma dip biasa.

## CAGR 200-week MA

CAGR point-to-point 4 tahun terakhir: **29.1%/tahun** — dekat dengan klaim video (~30%). Tapi breakdown per-tahun **tidak konsisten**: +18.9%, +37.0%, +35.5%, +26.0%. Klaim "konsisten 30%/tahun" tidak presisi — variasi tahunan cukup lebar (rentang 19-37%), meski rata-rata jangka panjangnya memang mendekati 30%.

## Level saat ini

200wma @2026-07-15 (data terakhir) = $62,945 (-1.3% dari klaim video $63,800). Ekstrapolasi tren ke tanggal video (2026-08-11) = **$63,813** — cocok hampir persis dengan klaim $63,800.

---

## Verdict

**[VALIDASI — 2026-08-12, CLOSED]** Level 200-week MA (~$63,800) dan CAGR rata-ratanya (~29-30%/tahun) **terverifikasi akurat**, tapi klaim "konsisten 30%/tahun" tidak presisi (variasi YoY 19-37%). Klaim "selalu jadi accumulation floor yang bertahan" **hanya sebagian benar**: dari **n=6 episode evaluable (~4 siklus independen)**, **5 HOLDS / 1 BREACH (83%)** — episode BREACH (Jun-Jul 2022) ditembus lebih dalam oleh FTX collapse November 2022. Overlap dengan zona akumulasi (ZC/Z1/ZD) konsisten 100%, tapi 3/7 episode cuma capai ZD (dip moderat), bukan capitulation penuh — jadi "harga ≤200wma" bukan sinyal capitulation ekstrem yang reliable dengan sendirinya. Data mentok 2026-07-15 (gap 27 hari ke tanggal video, level saat ini pakai ekstrapolasi).
