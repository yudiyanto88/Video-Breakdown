# Findings — LTH supply-in-loss threshold menurun per cycle?

**Video:** Bitcoin Just Hit Its Most Reliable Bottom Signal (On-Chain Mind, 2026-06-09)
**Tanggal validasi:** 2026-07-19
**Data:** `data_master_all_metrics.csv`, kolom `pct_lth_in_loss`
**Script:** `analyze_bottom_signals.py`
**Event CSV:** `events_v1_lth_loss_by_cycle.csv`

## Klaim video
Ambang MAX LTH-supply-in-loss di true bottom menurun tiap cycle: 2015 >50% → 2019 ~45% → 2022 ~40%; sekarang ~41% dinilai "tinggi untuk stage maturity ini". Klaim ini dipakai sebagai bukti bahwa metrik LTH-in-loss natural trending lower dan mendukung prinsip pola-relatif.

## Definisi event
Untuk tiap cycle bottom (harga terendah: 2011-11-18, 2015-01-14, 2018-12-14, 2022-11-21), ambil nilai MAKSIMUM `pct_lth_in_loss` dalam window ±60 hari (121 hari-observasi) sekitar tanggal low.

## Hasil (n=4 cycle)

| Cycle | MAX pct_lth_in_loss | Tgl max | LTH-loss di tanggal low |
|-------|--------------------|---------|------------------------|
| 2011 | 32.17% | 2012-01-17 | 22.22% |
| 2015 | 45.06% | 2015-01-14 | 45.06% |
| 2018 | 45.92% | 2019-02-07 | 44.60% |
| 2022 | 44.56% | 2022-12-30 | 43.78% |

## Interpretasi
- Tiga cycle terakhir praktis **flat ~44–46%**, bukan tangga menurun. Urutan 2015 (45.1%) < 2018 (45.9%) > 2022 (44.6%) — selisih di bawah noise, tidak monotonic.
- Angka video "2015 >50%" TIDAK cocok dengan `pct_lth_in_loss`. Kemungkinan video merujuk metrik LTH yang beda-definisi (mis. supply-weighted vs coin-count), atau membaca chart dengan cohort/definisi berbeda dari data kita.
- 2011 (32%) kemungkinan artefak kohort LTH era-awal (LTH belum matang, supply < 3.5jt).
- n=4 cycle = **sample sangat kecil**; 2011 sering jadi outlier.

## Verdict
**[VALIDASI — 2026-07-19, CLOSED]** REJECTED: klaim ambang LTH-supply-in-loss menurun tiap cycle tidak terdukung pada `pct_lth_in_loss`. MAX dalam ±60d tiga cycle terakhir justru flat ~44-46% (2015: 45.1% < 2018: 45.9% > 2022: 44.6%), selisih di bawah noise; 2011 hanya 32% (kemungkinan artefak kohort awal). n=4 cycle = sample sangat kecil. Nilai bottom yang stabil ~45% justru konsisten dengan prinsip pola-relatif framework (pola berulang), bukan drift menurun seperti klaim video.
