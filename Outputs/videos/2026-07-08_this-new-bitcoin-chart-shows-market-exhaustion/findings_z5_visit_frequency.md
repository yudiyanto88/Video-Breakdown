# Uji Hipotesis: Frekuensi/Durasi Visit Zona Resistance Menurun Menjelang Cycle Top

- **Asal klaim:** video "This New Bitcoin Chart Shows Market Exhaustion" (Joao Wedson / Alphractal, 2026-07-08) — seiring bull cycle berjalan, harga makin jarang mengunjungi zona resistance struktural (upper band SMB) = melemahnya momentum / sign of weakness
- **Tanggal uji:** 2026-07-13
- **Data:** `btc_price`, `aviv_ratio`, `mvrv_ratio`, `asopr` dari `data_master_all_metrics.csv` (Onchain-Dashboard)
- **Script:** `analyze_z5_visit_frequency.py` (folder ini). Tabel episode: `_z5_episodes.csv`
- **Catatan proxy:** SMB Alphractal proprietary/black box — tidak bisa direplikasi. Uji ini pakai PROXY zona resistance framework: Z5 = price >= AVIV Upper (+0.5 SD, formula established mengikuti `research/analyze_k3_stage_comparison.py`). Hasil berlaku untuk band KITA, bukan band Alphractal.

## Definisi event (ditetapkan sebelum lihat hasil)

- AVIV Upper = `(HIST_MEAN + 0.5*HIST_STD) * true_market_mean`, mean/std dari `aviv_ratio` full-history. Lookahead caveat: band pakai statistik full-history (cara framework/ChartInspect menampilkannya) — konsisten dengan pemakaian framework, tapi bukan band murni at-gate.
- **Episode Z5** = run hari berturut close >= AVIV Upper; dua run dipisah <=7 hari di bawah band digabung jadi satu episode. Episode dianggap selesai (at-gate) 7 hari setelah hari terakhir di Z5.
- **Deteksi "durasi menurun" (at-gate):** episode pertama dalam cycle yang durasinya < episode sebelumnya, terdeteksi saat episode itu selesai (+7d konfirmasi).
- Pembanding timing: dua syarat awal K1 (MVRV & aSOPR-MA7 diminishing per ATH cluster, gap cluster <=30d), deteksi at-gate = ATH day pertama di cluster dengan MVRV & aSOPR-MA7 lebih rendah dari max cluster sebelumnya.
- Data AVIV efektif mulai 2011-02 → **n = 3 full bull cycle** (2016-17, 2020-21, 2023-25) + 2012-13 & 2019 sebagai context.

## Hipotesis & Hasil

| Hipotesis | Verdict | Ringkasan |
|-----------|---------|-----------|
| Durasi/frekuensi episode Z5 menurun monotonic menjelang top | **NOT-SUPPORTED** | Monotonic decline: **0 dari 3 cycle** (juga tidak di 2012-13). Urutan durasi episode substantif: 2016-17: 9→91→**303d**; 2020-21: 210→**127d**; 2023-25: 135→18→143→**176d**. Density hari-in-Z5 per episode juga tidak menurun konsisten (2017: 0.77→0.96 NAIK; 2021: 1.00→0.88; 2025: 0.985→0.91→0.977 flat) |
| Top final terbentuk di episode lebih pendek/jarang dibanding episode sebelumnya | **NOT-SUPPORTED (2/3 kebalikan)** | Top 2017 di episode TERPANJANG cycle (303d); top 2025 di episode TERPANJANG cycle (176d, ep #7 dari 8, 2025-04-22 s/d 2025-10-14). Hanya 2021 yang cocok arah klaim: top di episode 127d setelah episode 210d. Yang menyusut drastis adalah episode SETELAH top (2025: ep#8 cuma 2 hari) — trivially retrospektif |
| Deteksi frekuensi-menurun menambah lead time vs syarat awal K1 | **NOT-SUPPORTED** | Struktural: durasi episode baru diketahui saat episode BERAKHIR = AVIV Upper cross-down = trigger OR-gate K1/K3 Stage 1 sudah bunyi. Sinyal ini inherently koinsiden-atau-lebih-lambat dari trigger existing. Empiris: deteksi 2021 baru 2021-12-10 (**32 hari SETELAH top**); di 2023-25 deteksi 2024-08-08 (lead 424d) tapi false alarm — dua episode LEBIH PANJANG menyusul (143d, 176d). Syarat awal K1 aktif jauh lebih awal: 2021-02-08 dan 2024-11-06 (lead 273d & 334d ke top) |

## Detail penting

- **n = 3 full cycle** dengan AVIV (+1 context) — sample kecil, tapi arah temuan seragam: struktur di data justru episode Z5 makin PANJANG saat bull matang, lalu mati mendadak setelah top. Pola "visit makin jarang" tidak muncul di band AVIV Upper.
- Episode pendek 1-4 hari (Aug 2020, Des 2023-Jan 2024) adalah noise sentuhan pertama band di AWAL bull — kebalikan dari narasi video.
- Yang konsisten dengan video hanya perilaku post-top: revisit setelah cycle top selalu pendek (2025: 2 hari). Tapi cuma bisa dibaca setelah kejadian — tidak actionable.
- Independensi: ketiga cycle penuh menolak monotonic decline, bukan didominasi satu cycle.
- Mungkin band SMB Alphractal (lebih tinggi/curam dari AVIV Upper) memang menunjukkan pola visit menurun — tidak bisa diverifikasi. Yang bisa disimpulkan: pola tersebut TIDAK transfer ke zona resistance framework, tidak ada yang bisa diadopsi.

## Verdict akhir

**NOT SUPPORTED (via proxy AVIV Upper).** Klaim frekuensi-visit-menurun tidak tereplikasi di Z5 framework: 0/3 cycle monotonic, 2/3 top justru terbentuk di episode Z5 terpanjang cycle-nya, dan secara struktural sinyal ini tidak bisa lebih cepat dari AVIV Upper cross-down yang sudah jadi trigger K1/K3. Konsep "diminishing" versi framework (MAGNITUDE MVRV/aSOPR per ATH) tetap unggul — aktif 273-334 hari sebelum top di 2 cycle terakhir. Tidak ada yang perlu diubah/ditambah ke framework.
