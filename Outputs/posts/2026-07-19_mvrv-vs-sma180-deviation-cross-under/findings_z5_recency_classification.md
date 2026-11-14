# Findings — Cross-under MVRV vs SMA180: klasifikasi recency Z5 (2019/2024/2026 jinak atau ganas?)

**Tanggal:** 2026-07-19
**Script:** `analyze_z5_recency_classification.py` | **Event table:** `events_z5_recency_classification.csv`
**Data:** `data_master_all_metrics.csv` (Onchain-Dashboard, read-only), 2010-07-17 s/d 2026-07-15 (5.843 hari)

---

## Ringkasan

Chart sumber melabeli event 2019, 2024, 2026 sebagai "fase non-peak, jinak". KB MVRV v1.4 § 6C.2 justru memasukkan mereka ke grup "SEMUA lanjut −19% s/d −48%". Hasil uji: **KB benar, label chart salah** — ketiga event lanjut drawdown −19% s/d −30% dalam 120 hari. Satu-satunya event yang benar-benar jinak adalah 2015 (−4,8%) dan 2023 (−5,6%), keduanya grup ">600 hari sejak Z5". Pembeda yang bekerja bukan "dekat/jauh dari cycle peak" melainkan **recency Z5** — dan event 2026 menunjukkan threshold ≤75 hari saja tidak cukup tanpa klausul "ATAU bear sudah terkonfirmasi".

---

## Definisi event (eksplisit)

- **Regime:** `mvrv_ratio` ≥ SMA180(`mvrv_ratio`) = above; di bawahnya = below. SMA180 murni backward-looking (min 180 hari data).
- **Event STRICT (aturan § 6C.1/6C.2):** hari pertama regime pindah above → below, dengan (a) below bertahan ≥7 hari berturut-turut, DAN (b) run above tepat sebelumnya ≥7 hari.
- **Aturan merge antar-episode:** tidak ada cooldown waktu tambahan. Merge terjadi struktural — dua below-run yang dipisah above-run <7 hari otomatis tergabung jadi satu episode, karena cross kedua gugur di syarat (b). Dua event terpisah hanya mungkin bila ada pemulihan above ≥7 hari penuh di antaranya.
- **AVIV Upper** = `price_at_aviv_mean + 0.5 × (price_at_aviv_plus_1_sigma − price_at_aviv_mean)` (formula established, data_dictionary + pola `analyze_k3_stage_comparison.py`).
- **Days-since-Z5:** hari sejak terakhir `btc_price` ≥ AVIV Upper, dihitung HANYA dari data ≤ tanggal event (at-gate, anti-lookahead).
- **Ground truth:** max forward drawdown 120 hari dari harga close tanggal cross. Kriteria "ganas" versi KB: dd ≥15%.
- Catatan lookahead yang diterima framework: band AVIV dari provider dihitung mean/SD full-history — sama dengan pola script established. Konfirmasi persistensi 7 hari berarti secara real-time sinyal baru "sah" di hari ke-7 setelah cross; tanggal event tetap tanggal cross (konsisten dengan KB).

---

## Hasil

### n dan sebaran per cycle

**n = 11 event STRICT** (persis mereplikasi angka "11 kejadian dalam 15 tahun" di KB § 6C.2 dan 11 titik di chart sumber — harga saat cross cocok semua dengan anotasi chart). Sebaran: C1 2011-2015 = 3, C2 2015-2018 = 1, C3 2019-2022 = 3, C4 2023-kini = 4.

### Tabel event lengkap

| Cross date | Cycle | Harga cross | Above-run sebelum | Days since Z5 | Max DD 120d | dd ≥15%? |
|---|---|---|---|---|---|---|
| 2011-03-16 | C1 | $0.86 | 63d | belum pernah (data AVIV mulai 2010) | −20,9% | Ya |
| 2013-05-01 | C1 | $116 | 13d | 22 | −41,0% | Ya |
| 2013-12-16 | C1 | $702 | 65d | 16 | −48,1% | Ya |
| 2015-08-18 | C2 | $221 | 63d | 626 | −4,8% | **Tidak** |
| 2019-09-23 | C3 | $9.866 | 174d | 75 | −30,5% | Ya |
| 2021-04-18 | C3 | $56.338 | 354d | 0 | −47,0% | Ya |
| 2021-12-03 | C3 | $53.762 | 63d | 12 | −34,7% | Ya |
| 2023-08-17 | C4 | $26.668 | 217d | 634 | −5,6% | **Tidak** |
| 2024-06-13 | C4 | $66.780 | 29d | 24 | −19,1% | Ya |
| 2025-10-10 | C4 | $113.039 | 8d | 1 | −44,4% | Ya |
| 2026-05-17 | C4 | $77.418 | 13d | 220 | −24,5%* | Ya* |

\* Window 120 hari event 2026-05-17 belum penuh (baru ~59 hari data s/d 2026-07-15). Status dd ≥15% sudah FINAL (−24,5% sudah melewati batas, dd hanya bisa makin dalam); magnitude −24,5% masih bisa bertambah.

Precision keseluruhan: **9/11 = 0,82** lanjut dd ≥15% (base rate hari acak = 0,49; lift ~1,7x). Median kelanjutan semua 11 event: −30,5%. Kedua angka mereplikasi KB (0,82 / −31%).

### Klasifikasi recency Z5

| Grup | n | Hasil | Median DD |
|---|---|---|---|
| ≤75 hari sejak Z5 | 7 (2013×2, 2019, 2021×2, 2024, 2025) | **7/7 lanjut dd ≥15%**, rentang −19,1% s/d −48,1% | −41,0% |
| 75–600 hari (gap) | 1 (2026-05-17, 220 hari — tapi bear terkonfirmasi) | 1/1 lanjut, −24,5% (provisional) | −24,5% |
| >600 hari (recovery/early bull) | 2 (Agu 2015, Agu 2023) | **0/2** — keduanya hanya −5% | −5,2% |
| Belum pernah Z5 (batas data) | 1 (Mar 2011) | 1/1 lanjut, −20,9% | −20,9% |

---

## Hipotesis dan verdict

**H1 (versi chart): event 2019, 2024, 2026 = fase non-peak, jinak.** → **DITOLAK.** 2019: −30,5%. 2024: −19,1%. 2026: −24,5% (provisional, sudah pasti melewati batas 15%). Ketiganya "ganas" menurut kriteria KB. "Jauh dari cycle peak" ≠ jinak: 2024 hanya 24 hari dari kunjungan Z5 terakhir (local top Mar 2024) meski bukan cycle peak.

**H2 (versi KB § 6C.2): grup ≤75 hari (atau bear terkonfirmasi) SEMUA lanjut −19% s/d −48%.** → **KONFIRMASI.** 7/7 grup ≤75 hari lanjut, rentang persis −19,1% s/d −48,1%. Event 2026 (220 hari dari Z5) tetap ganas karena bear sudah terkonfirmasi — klausul "ATAU bear terkonfirmasi" di KB terbukti perlu; threshold hari saja tidak cukup. Catatan tabel KB: 2026 masuk grup itu lewat jalur bear-confirmed, bukan lewat ≤75 hari (days-since-Z5 aktualnya 220).

**H3 (implisit KB): grup >600 hari = false signal.** → **KONFIRMASI.** 2015 dan 2023 keduanya hanya −5%, satu-satunya 2 event jinak dari 11.

### Rekonsiliasi count 11-vs-16 (Governance v2 butir 4c)

- Definisi longgar **L0** (semua raw cross above→below, tanpa syarat): **n = 85**
- Definisi **L1** (persistensi below ≥7 hari saja, tanpa syarat regime sebelumnya ≥7 hari): **n = 30** (19 event tambahan gugur di strict karena above-run sebelumnya hanya 1–6 hari; daftar lengkap di output script)
- Definisi **STRICT** (persistensi + regime ≥7 hari): **n = 11**

Angka 16 dari `opus_bear_confirmed_v2_mvrv.py` berada di antara 11 dan 30 → konsisten dengan hipotesis KB "beda cara hitung episode/streak": kemungkinan besar script review memakai syarat regime-sebelumnya yang lebih longgar (atau tanpa syarat itu, plus merge berbeda). Varian prior-run yang dicoba (≥2/≥3/≥4/≥5 hari → 21/19/14/12 event) tidak ada yang tepat 16, jadi replikasi persis butuh baca script review itu langsung — di luar scope validasi ini. Yang penting: **angka 11 di KB dan chart sumber terreplikasi persis dengan definisi § 6C.1 yang tertulis.**

---

## Rigor notes

- **n = 11 total, hanya 4 cycle** — grup ≤75 hari didominasi pasangan cycle sama (2013×2, 2021×2); C4 menyumbang 4/11 event. Sample kecil, event dalam satu cycle berkorelasi.
- **Boundary 75 hari tepat jatuh di data point 2019 (persis 75,0 hari)** — threshold ini fitted, bukan struktural; KB sendiri sudah mengakuinya provisional. Jangan diperlakukan sebagai angka keras.
- Event 2026-05-17: window forward belum penuh — magnitude provisional, verdict biner sudah final.
- Event 2011: AVIV data mulai 2010, jadi "belum pernah Z5" bisa artefak batas data.
- Anti-lookahead dijaga: days-since-Z5 at-gate; SMA180 backward-looking; hanya window ground-truth yang melihat ke depan.

---

## Verdict akhir

**KONFIRMASI untuk KB § 6C.2, KOREKSI untuk label chart sumber.** Event 2019, 2024, 2026 TIDAK jinak — semuanya lanjut drawdown −19% s/d −30% dalam 120 hari (2026 provisional di magnitude, final di verdict biner). Pembeda ganas-vs-jinak yang didukung data adalah recency Z5 + status bear-confirmed, bukan jarak visual ke cycle peak. Hanya 2 dari 11 event yang jinak (2015, 2023 — keduanya >600 hari sejak Z5). Diskrepansi count 11-vs-16 cenderung berasal dari syarat regime-sebelumnya ≥7 hari yang tidak dipakai script review; definisi § 6C.1 tertulis menghasilkan persis 11.
