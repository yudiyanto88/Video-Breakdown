# Findings: Rally ~100 Hari Pasca-Bottom (Z1→Z2 Unlock Objektif)

**Video sumber:** Bitcoin Magazine Pro, "Bitcoin Bottom Signal (Less Than 2 Weeks Away)", 2026-07-02
**Tanggal analisis:** 2026-07-28
**Script:** `analyze_post_bottom_rally_speed.py`
**Data:** `data_master_all_metrics.csv`, kolom `btc_price`, `sth_cost_basis`, `realized_price`

## Klaim yang diuji
Pembicara klaim di 3 bear market terakhir, begitu bottom terkonfirmasi, harga naik signifikan (+50% s/d +250%) dalam ~100 hari (contoh: 31 Des 2022, 100 hari $15-16k → $30k; ~$3,000 → ~$14,000 (+250%); ~$230 → $460+ (+100%)).

## Catatan metodologi penting
Video memilih tanggal "bottom" secara **subjektif/hindsight** (mis. 31 Des 2022, padahal harga absolut terendah cycle itu sudah terjadi ~Nov 2022). Validasi ini **tidak memakai** definisi subjektif itu — dipakai definisi objektif framework: **Z1→Z2 unlock** (STH RP cross naik RP), identik dengan event di findings insight #7, karena ini confirming signal yang tersedia real-time (bukan dipilih ex-post dari harga rendah yang baru diketahui belakangan). Konsekuensinya: "hari ke-0" di sini biasanya BUKAN hari harga absolut terendah, melainkan beberapa minggu setelahnya (lihat `findings_ma_reclaim_vs_z1z2_unlock.md`) — jadi angka hari-ke-target di sini secara struktural cenderung LEBIH PENDEK dibanding kalau dihitung dari harga absolut terendah.

## Definisi event
- Episode = 4 tanggal Z1→Z2 unlock historis (sama dengan findings insight #7): 2012-04-19, 2015-11-03, 2019-05-07, 2023-03-05.
- t50 = hari kalender sampai `btc_price` pertama kali ≥1.5x harga di tanggal unlock.
- t100 = hari kalender sampai `btc_price` pertama kali ≥2.0x harga di tanggal unlock.
- pct_gain_100d = % perubahan harga persis 100 hari kalender setelah tanggal unlock (dibandingkan langsung ke klaim "~100 hari" video).

## Hasil — n = 4 episode (independen antar cycle, tapi tiap cycle cuma 1 titik data)

| Episode | Harga @ unlock | Hari ke +50% | Hari ke +100% | % gain persis di hari-100 |
|---|---|---|---|---|
| 2012-04-19 | $5.14 | 88 | 105 | +71.1% |
| 2015-11-03 | $404.61 | 221 | 414 | **-6.5%** |
| 2019-05-07 | $5,778.25 | 19 | 50 | +80.7% |
| 2023-03-05 | $22,429.49 | 233 | 303 | +15.7% |

- t50: rentang **19-233 hari** (bukan konsisten ~100 hari)
- t100: rentang **50-414 hari**
- Episode 2015 bahkan masih **turun 6.5%** di hari ke-100 pasca unlock — jauh dari klaim "+50-250% dalam ~100 hari"

## Verdict
Dengan n=4 episode historis dan definisi bottom yang objektif (bukan hindsight), klaim "rally ~100 hari pasca-bottom" **tidak terbukti konsisten** — sebarannya sangat lebar (t50: 19-233 hari; t100: 50-414 hari), dan satu dari empat episode (2015) bahkan masih negatif di hari ke-100. Hanya episode 2012 yang mendekati pola "~100 hari" video (t100=105 hari, +71% di hari-100). Episode 2019 jauh lebih cepat (t100=50 hari) dan episode 2023 jauh lebih lambat (t100=303 hari). Ini **hasil negatif yang valid** — klaim video kemungkinan besar produk dari memilih contoh yang cocok secara selektif (cherry-picking dari 3 contoh anekdotal di video, dengan tanggal bottom yang dipilih hindsight), bukan pola yang robust ketika diuji dengan definisi bottom yang konsisten dan objektif lintas 4 cycle. Catatan independensi: tiap episode 1 titik data per cycle bear market, jadi n=4 di sini benar-benar mewakili 4 cycle terpisah (bukan sample yang saling berkorelasi dalam satu cycle) — tapi tetap n kecil secara absolut.

Bahasa probabilistik: rally pasca-bottom cenderung terjadi, tapi kecepatannya sangat bervariasi antar cycle dan TIDAK bisa diasumsikan ~100 hari.
