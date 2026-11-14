# Uji Hipotesis: STH Mendominasi 78% Negative Realized Cap Flow → "Pasar Tanpa Structural Guidance"

- **Asal klaim:** video "The Real Reason Bitcoin Keeps Bleeding" (On-Chain Mind, 2026-06-23) — "STH menyumbang ~78% negative realized capital flow; band 1–3 bulan terbesar ~$64M/hari; sebulan terakhir STH -$12.5B vs LTH -$4.5B (~3x); conviction holders dormant → pasar tanpa structural guidance"
- **Tanggal uji:** 2026-07-13
- **Data:** `sth_realized_cap_usd`, `lth_realized_cap_usd`, `realized_cap_usd`, `realized_cap_<band>` (HODL waves, 12 band), `lth_sopr`, `btc_price` dari `data_master_all_metrics.csv` (Onchain-Dashboard). Full history 2010-07-17+, semua cycle terjangkau
- **Script:** `analyze_sth_share_of_flow.py` (net cohort delta + timing) dan `analyze_sth_share_of_flow_bands.py` (replikasi metode video via age bands). Tabel pendukung: `_sth_share_bear_windows.csv`

## Definisi (ditetapkan sebelum lihat hasil)

- **Flow 30 hari (f30)** = RC[t] − RC[t−30] per cohort/band — dipilih karena angka video sendiri berbasis "sebulan terakhir". Hari outflow = total f30 < 0 (n=1.589 hari full history).
- **STH share of negative flow**, dua pendekatan:
  1. **Net cohort:** min(sth_f30,0) / [min(sth_f30,0) + min(lth_f30,0)] — hanya terdefinisi saat ada flow negatif.
  2. **Band-level** (paling dekat ke metode video): f30 per age band, jumlahkan yang negatif; STH proxy = band <3m ("narrow") dan <6m ("wide", terdekat ke batas 155 hari yang jatuh di tengah band 3m–6m). Kolom band di master = persen dari RC, dikonversi ke USD dulu.
- **H2 event (maks 2 varian, anti overfit, at-gate):** dalam bear window (top → bottom+90d), first date LTH share (net cohort, MA7) ≥ 40% (varian ≥ 50%) dengan syarat hari outflow. Dibandingkan vs tanggal bottom dan vs first date LTH-SOPR < 0.50 (raw & MA7) — sinyal K4.
- Bear windows: C1 2013-11-30→2015-01-14, C2 2017-12-17→2018-12-15, C3 2021-11-10→2022-11-21, C4 2025-10-06→berjalan (bottom belum dikonfirmasi).
- **Catatan mekanis (diketahui sebelum uji):** delta RC per cohort/band tercemar maturation flow — coin usia 155 hari pindah STH→LTH di cost basis lama TANPA transaksi pasar; LTH yang jual mengurangi LTH RC dan menambah STH RC di harga baru. Jadi "flow per cohort" bukan murni jejak selling.

## Hipotesis & Hasil

| Hipotesis | Verdict | Ringkasan |
|-----------|---------|-----------|
| H1: STH share 78% adalah anomali yang informatif | **NOT-SUPPORTED** | Dominasi STH adalah **kondisi default, bukan anomali**. Band-level (metode video): median historis STH share (wide <6m) di hari outflow = **88.5%**; reading tanggal video 84.5% = **persentil 46** — persis tengah distribusi. Narrow (<3m): 42.0% = persentil 37. Net cohort lebih ekstrem lagi: median = **100%** (LTH f30 biasanya POSITIF karena maturation inflow); reading video-date 100% = persentil 25. Median per bear: C1 63.5%, C2 92.7%, C3 80.0%, C4 94.8% — STH SELALU mendominasi negative flow di semua bear |
| H2: kenaikan LTH share mendahului cycle bottom, lebih awal dari LTH-SOPR < 0.50 (K4) | **NOT-SUPPORTED** | First-hit LTH share MA7 ≥ 40%: C1 +87 hari sebelum bottom, C2 +23 hari, C3 +2 hari — **timing tidak konsisten, n=3 bottom saja**. Vs LTH-SOPR MA7 < 0.50: C2 19 hari lebih awal, C3 1 hari LEBIH LAMBAT — praktis koinsiden (episode kapitulasi LTH yang sama). Satu-satunya kasus "lebih awal" (C1, 3 bulan) justru premature: harga masih turun **-54%** lagi sampai bottom. Max LTH share malah sering terjadi SETELAH bottom (C1: Mar 2015, C3: Jan 2023). Varian ≥ 50% memberi pola sama. Tidak ada informasi tambahan yang reliable di atas K4 |
| H3: verifikasi angka video (STH -$12.5B vs LTH -$4.5B, ~3x; band 1-3m ~$64M/hari) | **PARTIAL** | **Total cocok hampir persis:** realized cap 30d per 2026-06-23 = **-$14.68B** vs klaim video "~$14B". Split cohort TIDAK tereplikasi dari data kita: net cohort = STH -$50.7B / LTH **+$36.1B** (maturation mendominasi); band-level gross negative = <6m -$48.5B vs ≥6m -$8.9B (rasio **5.4x**, share 84.5%). Angka video (-12.5/-4.5, 2.8x) kemungkinan dari metrik flow yang sudah aging-adjusted — tidak ada di data kita. "$64M/hari band 1-3m terbesar" tidak cocok sama sekali: data kita band 1m-3m -$459M/hari, dan band terbesar justru **3m-6m** (-$812M/hari). Arah kualitatif (STH >> LTH) konsisten, magnitudo tidak |

## Detail penting

- **n:** H1 dihitung dari 1.589 hari outflow lintas 5 cycle (C1 238, C2 310, C3 325, C4 170 hari di bear window) — sample memadai untuk distribusi. **H2 hanya n=3 cycle bottom** — kecil, dan hasilnya pun sudah negatif; hari-hari dalam satu episode kapitulasi saling berkorelasi (satu event per cycle efektifnya).
- **Kecurigaan mekanis TERKONFIRMASI, malah lebih kuat dari dugaan:** dengan net cohort delta, LTH realized cap 30-hari biasanya NAIK saat bear (maturation inflow > LTH spending) sehingga 100% negative flow "berasal dari STH" by construction. Dengan band-level pun median historis 88.5%. Angka ~78-85% bukan sinyal kondisi khusus — itu cara metrik ini selalu terlihat saat outflow.
- **Status C4 (bear berjalan):** LTH share sempat spike ke 71% pada 2025-12-23 (hanya 3 hari ≥ 40%) di harga $87.448 — harga setelahnya masih turun -33% ke $58.460 (2026-06-30). LTH-SOPR belum pernah < 0.50 bear ini (min raw 0.623 pada 2026-06-30). Dua lensa sama-sama bilang kapitulasi LTH gaya 2015/2018/2022 belum terjadi — konsisten dengan status K4.
- Interpretasi naratif video ("new entrants churning antar mereka sendiri", "no structural guidance → choppy") tidak falsifiable sebagaimana dirumuskan; komponen empirisnya yang bisa diuji adalah dua hipotesis di atas, dan keduanya gagal.
- Limitasi: metrik persis yang dipakai video (realized cap flow per cohort, tampaknya aging-adjusted) tidak ada di dataset kita — replikasi memakai dua proxy terbaik yang tersedia (net cohort delta & band delta). Kedua proxy konvergen ke kesimpulan yang sama untuk H1/H2, jadi limitasi ini tidak mengubah verdict; hanya H3 (magnitudo split) yang tidak bisa dinilai penuh.

## Verdict akhir

**REJECT** (sebagai insight actionable). Dominasi STH atas negative realized cap flow adalah properti mekanis metrik — median historis 88.5% (band-level) sampai 100% (net cohort) di hari outflow, dan reading saat tanggal video ada di persentil 37–52 alias normal. Sisi yang berpotensi informatif (kenaikan LTH share sebagai penanda bottom) tidak konsisten (**n=3**), praktis koinsiden dengan LTH-SOPR < 0.50 di 2 dari 3 cycle, dan di cycle satunya premature dengan -54% drawdown tambahan. Satu-satunya yang terverifikasi: total realized cap turun ~$14B/bulan per tanggal video (kita: -$14.68B). Tidak ada yang perlu masuk framework; K4 (LTH-SOPR < 0.50) tetap lensa yang lebih bersih untuk hal yang sama.
