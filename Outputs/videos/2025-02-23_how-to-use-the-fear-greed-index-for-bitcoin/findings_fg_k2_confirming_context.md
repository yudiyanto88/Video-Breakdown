# Findings — F&G raw < 30 sebagai Confirming Context K2

**Tanggal validasi:** 2026-07-12
**Asal insight:** Diskusi dengan Yudi setelah update K1/K3/K4 — pertanyaan: kenapa F&G < 30 tidak masuk sebagai kondisi K2? Bukan klaim dari video, murni eksplorasi lanjutan topik F&G.
**Data:** `data_master_all_metrics.csv` (kolom `Fear & Greed`, `btc_price`). F&G mulai 2018-02-01 → n=2 cycle.

---

## Pertanyaan

K2 (masuk di bull dip) tidak memakai F&G sebagai kondisi, berbeda dari K5 yang memakainya sebagai staging trigger. Apakah F&G < 30 punya discriminating power antara bull dip (recover) vs bear onset (tidak recover) di K2? Kalau tidak, apakah tetap layak masuk sebagai confirming context (bukan syarat)?

## Metode — Bagian 1: bull dip vs bear onset

Bandingkan 5 bull dip (recover ke high baru dalam cycle yang sama) vs 2 bear onset (dip pasca cycle top, tidak recover) — nilai minimum raw F&G dan jumlah hari F&G < 30 selama episode.

## Hasil — Bagian 1

| Episode | Min raw F&G | Hari F&G < 30 |
|---|---|---|
| Bull dip COVID Mar-2020 | 8 | 38 |
| Bull dip Mei-Jul 2021 (-55%) | 10 | 71 |
| Bull dip Sep 2021 (-25%) | 20 | 10 |
| Bull dip Aug 2024 (-30%) | 17 | 21 |
| Bull dip Feb-Apr 2025 (-30%) | 10 | 22 |
| **Bear onset Des 2021-Jan 2022** | **10** | **54** |
| **Bear onset Nov-Des 2025** | **10** | **68** |

F&G < 30 ter-trigger di 7/7 episode, kedalaman serupa (min 8-20 vs 10). **Tidak ada discriminating power** — bull dip dan bear onset dua-duanya selalu menyentuh extreme fear. Kondisi yang selalu true di dua skenario tidak menambah informasi kalau dipakai sebagai syarat formal.

## Metode — Bagian 2: kehadiran vs ketiadaan F&G < 30 di seluruh dip bull ≥8%

Scan semua drawdown ≥8% dari running high dalam 3 rentang bull (2019, 2020-2021, 2023-2025), catat apakah F&G sempat < 30, max drawdown, dan lama recovery.

## Hasil — Bagian 2

**Tanpa F&G < 30** (min F&G 37-89): Mei/Jun/Sep 2020, Nov/Des 2020, Jan/Feb/Mar 2021, Okt 2021, Jan 2024, Des 2024, Jun 2025 — semua recover cepat (4-48 hari), DD -8% s/d -25%.

**Dengan F&G < 30** (min F&G 5-28): Jun 2019 (berujung bear), Apr 2021 (-53%, 184 hari), Mar 2024 (-26%, 235 hari), Feb 2025 (-28%, 105 hari), Aug 2025 (-12%, 47 hari) — dip lebih dalam dan lebih panjang, termasuk satu episode yang gagal recover (Jun 2019 → bear).

## Verdict

**PARTIAL — tidak discriminating sebagai syarat, tapi informatif sebagai gauge intensitas.** F&G < 30 tidak bisa membedakan bull dip dari bear onset (keduanya selalu menyentuhnya) — jadi tidak layak masuk hitungan 5 kondisi K2 atau confidence tier. Tapi dia punya makna dua arah yang berguna sebagai context:

1. **Kehadiran F&G < 30** = penanda kelas dip yang dalam (historis -21% s/d -53%, recovery berbulan-bulan) — bukan aman untuk masuk, malah sinyal untuk cek 5 kondisi lebih ketat karena semua episode gagal (termasuk bear onset) ada di kelompok ini.
2. **Ketiadaan F&G < 30** TIDAK boleh dibaca sebagai "belum waktunya masuk" — mayoritas bull dip terbaik dan tercepat historis tidak pernah menyentuh F&G 30.

n=7 episode dip dalam kategori bull/bear, n≈19 episode drawdown ≥8% untuk bagian 2 — kedua kelompok kecil, F&G cuma 2 cycle.

## Implikasi ke framework (rekomendasi, bukan perubahan)

- Ditambahkan sebagai confirming context di K2 v1.1 — tidak masuk 5 kondisi, tidak mengubah confidence tier atau tabel deploy.
- Pembeda bull dip vs bear onset tetap sepenuhnya bertumpu pada 5 kondisi yang sudah ada (terutama #2, #4, #5 yang punya struktur gagal-bisa-gagal di bear onset) — F&G tidak menggantikan atau menambah kekuatan pembeda itu.
