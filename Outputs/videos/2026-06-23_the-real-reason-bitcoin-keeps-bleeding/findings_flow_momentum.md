# Uji Hipotesis: Flow Momentum (MA30 vs MA90 Realized Capital Flow)

- **Asal klaim:** video "The Real Reason Bitcoin Keeps Bleeding" (On-Chain Mind, 2026-06-23) — MA30 flow < MA90 flow = structural demand melemah = "opportunity to start scaling in"; reading sekarang "averagely weak"
- **Tanggal uji:** 2026-07-13
- **Data:** `realized_cap_usd`, `net_realized_pl_usd` dari `data_master_all_metrics.csv` (Onchain-Dashboard)
- **Script:** `analyze_flow_momentum.py` (folder ini)

## Hipotesis & Hasil

| Hipotesis | Verdict | Ringkasan |
|-----------|---------|-----------|
| (a) Satu indikator dengan Capital Bleeding (rc30)? | **BEDA TAPI SEKELUARGA** | Pearson 0.805, Spearman 0.504, sign-agreement 64.5% — di bawah ambang 0.9, bukan duplikat persis. Momentum lebih cepat berbalik (leading rc30) |
| (b) First cross MA30<MA90 = saat "scaling in"? | **NOT-SUPPORTED — early entry katastrofik** | First cross setelah cycle top terjadi di -11% s/d -38% dari top, lalu drawdown TAMBAHAN sampai cycle bottom: **-75.1%** (2014-15, 382 hari), **-76.9%** (2018-19, 335 hari), **-70.7%** (2022, 353 hari). Bear sekarang: cross 2025-10-11 @ $110.810 → low sejauh ini $58.460 (**-47.2%** setelah cross, bear belum tentu selesai). n=3 bear lengkap + 1 berjalan, konsisten semua |
| (c) Redundan dengan `net_realized_pl_usd` (metrik existing)? | **REDUNDAN TOTAL** | Pearson MA30 flow vs MA30 net_realized_pl_usd = **0.9996** (raw), 0.98 (normalized), >=0.99 di tiap cycle. Momentum vs momentum = **0.9999**. Secara akunting memang delta realized cap ~ net realized P/L (coin di-repricing saat bergerak) |

## Detail penting

- Flow Momentum bukan informasi baru: identik dengan smoothing `net_realized_pl_usd` yang sudah ada di data kita. Kalau mau melihat "structural demand", cukup MA30/MA90 dari kolom existing.
- Klaim "negatif = opportunity to start scaling in" berbahaya kalau dibaca sebagai trigger: dalam 3 bear lengkap, first cross selalu ~1 tahun dan -70%+ sebelum bottom. Cross-down juga terjadi 3-5x per bear (whipsaw).
- Status: momentum di tanggal video -$311M/hari, per 2026-07-12 -$115M/hari. "Averagely weak" sebagai deskripsi kondisi — fine; sebagai sinyal entry — tidak.

## Verdict akhir

**REJECT** sebagai sinyal entry (early ~1 tahun, -70%+ additional drawdown historis) dan **redundan** dengan `net_realized_pl_usd` MA30 (r=0.9996-0.9999). Tidak menambah apa pun ke framework.
