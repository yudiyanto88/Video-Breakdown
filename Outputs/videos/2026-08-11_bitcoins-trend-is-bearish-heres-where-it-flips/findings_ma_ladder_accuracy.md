# Findings — 200-day MA / yearly MA resistance ladder (cek akurasi angka)

**Video:** Bitcoin's Trend Is Bearish — Here's Where It Flips (On-Chain Mind, 2026-08-11)
**Tanggal validasi:** 2026-08-12
**Script:** `analyze_ma_ladder_accuracy.py`

---

## Klaim yang diuji

Video mengklaim harga saat ini di bawah 200-day MA (~$70,000) dan yearly/365-day MA (~$85,000), dibaca sebagai ladder resistance ($67-70K = short-term bias flip, $85K = macro trend confirmation).

Ini murni cek akurasi angka (kedua MA adalah indikator TA standar, bukan proprietary, dan kolomnya tersedia langsung/terhitung dari data kita) — bukan structural insight besar, sehingga tidak perlu analisis mendalam.

## Catatan data

`data_master_all_metrics.csv` mentok update di **2026-07-15** — gap 27 hari ke tanggal video (2026-08-11). Angka "current" pakai 2026-07-15 sebagai basis, dengan ekstrapolasi tren linear 60-hari untuk mendekati tanggal video.

## Hasil

| Metrik | Nilai @2026-07-15 (data terakhir) | Klaim video | Ekstrapolasi ke 2026-08-11 |
|---|---|---|---|
| 200-day MA (`200_dma`) | $73,534 | ~$70,000 | **$70,109** |
| Yearly MA (365-day, dihitung manual dari `btc_price` — tidak ada kolom siap pakai) | $88,728 | ~$85,000 | **$85,796** |

Harga BTC @2026-07-15 ($65,098) confirmed di bawah kedua MA.

## Sample

Ini bukan event study — hanya verifikasi titik angka tunggal (n=1, snapshot akurasi).

---

## Verdict

**[VALIDASI — 2026-08-12, CLOSED]** Cek akurasi angka saja (bukan structural insight): 200-day MA dan yearly (365-day) MA di data terakhir (2026-07-15, gap 27 hari ke tanggal video) masing-masing $73,534 dan $88,728; ekstrapolasi tren pendek ke tanggal video (2026-08-11) menghasilkan **$70,109** dan **$85,796** — keduanya cocok erat dengan klaim video (~$70,000 dan ~$85,000). Harga confirmed di bawah kedua MA. Angka video **terverifikasi akurat**.
