# Bitcoin All-Time High: What's Next?
**Channel:** On-Chain Mind
**Tanggal video:** 2025-01-22
**Tanggal analisis:** 2026-07-06
**Link:** https://www.youtube.com/watch?v=DFdbG_aKCao

---

## Ringkasan

Video pendek (7:27) yang mengecek kesehatan market BTC di sekitar level ATH awal 2025 (harga $105K–$108K, Realized Price $41.4K, MVRV 1.32 per 16-Jan-2025). Fokus utamanya adalah "MVRV Z-Score Optimization" — channel membandingkan MVRV Z-score dihitung dengan window cumulative (seluruh histori) vs rolling 4-tahun, 2-tahun, dan 1-tahun, untuk mengatasi masalah "diminishing peaks" (puncak MVRV yang terus mengecil tiap cycle karena market makin matang). Dari situ mereka bikin price band (mean, ±1.5σ, ±2σ) berbasis rolling 1-tahun. Sisa video membahas STH cost basis, total supply in loss, dan metric "entity-adjusted relative unrealized loss" untuk menyimpulkan bahwa meski STH sedang unrealized loss, stress market saat ini jauh lebih rendah dibanding koreksi-koreksi sebelumnya.

---

## Insight Inventory

### [KONFIRMASI] Diminishing MVRV peaks tiap cycle
- **Insight:** MVRV ratio di puncak siklus terus menurun: 2011 (8.07x) → 2013/14 (6.00x) → 2017 (4.81x) → 2021 (3.98x) → 2024 (2.78x).
- **Indikator terkait:** MVRV Ratio (histori penuh)
- **Relevan ke:** K1 signal #1 ("MVRV turun di setiap ATH baru")
- **Test klaim:** n=5 cycle, di atas batas minimum 3–4 cycle yang disebut framework sendiri. Tapi video ini hanya bahas MVRV — aSOPR (signal #2 K1) sama sekali tidak disinggung, jadi tidak menambah confirming power untuk K1 secara penuh.
- **Perlu validasi Claude Code:** Tidak — sudah established di framework.

### [INDIKATOR CUSTOM] MVRV Z-Score dengan rolling window 1 tahun
- **Insight:** Channel mengklaim MVRV Z-score yang dihitung dari rolling window 1 tahun (bukan cumulative/4Y/2Y) lebih responsif menangkap turning point market, karena versi cumulative dan 4Y masih terdistorsi oleh volatilitas ekstrem cycle-cycle awal ("diminishing returns is still present" bahkan di window 4Y). Dari rolling 1Y ini mereka turunkan price band: Mean $91K, +2σ $113K, -1.5σ $75K (per 16-Jan-2025).
- **Indikator terkait:** MVRV Z-Score (variasi lookback window)
- **Relevan ke:** General — cara menormalisasi threshold antar cycle, prinsip yang sama dengan filosofi framework ("pola relatif, bukan threshold absolut")
- **Test klaim:** Klaim hanya didasarkan pada overlay chart visual, tidak ada angka hit-rate/backtest. Bisa didekomposisi: MVRV Z-Score = (Market Cap − Realized Cap) / stdev(Market Cap − Realized Cap), dengan mean & stdev dihitung dari window 1 tahun terakhir saja, bukan seluruh histori. Konsepnya mirip AVIV Mean/Upper di framework (juga basis relatif), tapi basis metric beda (MVRV Ratio vs Realized Price dari active investor).
- **Perlu validasi Claude Code:** Ya — cek apakah price band dari rolling 1Y MVRV Z-score (Mean $91K, +2σ $113K, -1.5σ $75K di 16-Jan-2025) align dengan nilai AVIV Mean/AVIV Upper framework di tanggal yang sama. Kalau align, ini jadi cross-check independen buat validasi batas zona Z4/Z5.

**[VALIDASI — 2026-07-07 s/d 2026-07-11, CLOSED]** Price band video tidak align 1:1 dengan AVIV Mean/Upper (skala sigma kedua metode tidak setara). Divergence check lanjutan (n=7 titik, formula dolar rolling-1Y vs AVIV z-position) menemukan divergensi terjadi tapi merupakan artefak struktural dari perbedaan reaktivitas formula, bukan sinyal regime independen. Tidak ada K-node/threshold baru diusulkan. Detail lengkap: [`findings_mvrv_rolling1y_vs_aviv.md`](findings_mvrv_rolling1y_vs_aviv.md).

### [BARU] Entity-Adjusted Relative Unrealized Loss (loss dinormalisasi market cap)
- **Insight:** Alih-alih mengukur jumlah BTC (coin count) yang sedang rugi, metric ini mengukur total unrealized loss (USD) relatif terhadap total market cap. Video menunjukkan bahwa meski supply-in-loss saat ini (2.6M BTC) terlihat signifikan dibanding baseline bull market (<4M BTC), secara relative-to-cap loss-nya cuma marginal — jauh di bawah level historis (COVID >10%, koreksi Jul–Sep 2024 cuma 4.33%).
- **Indikator terkait:** Turunan dari Supply in Profit/Loss (Supply KB v1.4), tapi dinormalisasi market cap.
- **Relevan ke:** K1 signal #5 ("Supply in Profit di atas 90% dan mulai turun") dan K4 kondisi #3 ("Total Supply in Profit di bawah 50%, STH profit di bawah 10%") — keduanya pakai % dari total supply/coin count, bukan value-weighted.
- **Test klaim:** Coin-count based Supply-in-Loss punya potensi masalah scale: market cap Bitcoin terus tumbuh, jadi raw BTC count yang underwater di across cycles tidak apple-to-apple dengan metric relative-value. Ini justru insight metodologis yang bisa memperkuat prinsip framework sendiri yang sudah sadar "threshold absolut tidak reliable antar cycle" — kemungkinan sebagian penyebabnya karena pakai coin-count, bukan value-weighted.
- **Perlu validasi Claude Code:** Ya — cek apakah data on-chain yang dipakai project dashboard sudah punya field "Relative Unrealized Loss" (value-weighted). Kalau ada, test apakah versi ini kasih threshold yang lebih konsisten antar cycle dibanding % Supply in Loss/Profit yang sekarang dipakai di K1 dan K4.

**[VALIDASI — 2026-07-10 s/d 2026-07-11, CLOSED]** Dashboard sudah punya field value-weighted setara (`nupl`/`sth_nupl`/`lth_nupl`). Tidak cocok menggantikan coin-count di K1 signal #5 atau K4 condition #3 (coin-count lebih konsisten antar siklus, NUPL kena diminishing-peaks sama seperti MVRV). Juga dites sebagai tie-breaker confidence scoring K2 — tidak ada separating power di bucket manapun (setelah fix lookahead bias). Satu-satunya use-case valid: context tambahan terpisah untuk menilai severity koreksi relatif. Detail lengkap: [`findings_entity_adjusted_loss_nupl.md`](findings_entity_adjusted_loss_nupl.md).

### [KONFIRMASI] STH Cost Basis / STH Realized Price sebagai confirming signal
- **Insight:** STH average cost basis $88.5K (16-Jan-2025), harga trading 21% di atasnya — konsep ini persis sama dengan STH RP di framework yang jadi bagian boundary zona Z1/Z1b dan salah satu confirming signal K2 (kondisi #5).
- **Indikator terkait:** STH Realized Price
- **Relevan ke:** Zone boundary umum, K2 kondisi #5 (tidak langsung)
- **Test klaim:** Angka absolut hanya berlaku di satu titik waktu, tidak generalizable — tapi konsepnya sudah established, tidak perlu tes ulang.
- **Perlu validasi Claude Code:** Tidak.

### [STRATEGI] Narasi "market makin matang, volatility turun karena institutional demand"
- **Insight:** Key takeaway channel: penurunan puncak MVRV/volatility tiap cycle disebabkan pertumbuhan institutional/ETF demand yang membuat market lebih stabil dan efisien.
- **Relevan ke:** General framing, tidak actionable ke K-node manapun.
- **Test klaim:** Ini causal claim (institutional demand → less volatility) yang tidak dibuktikan secara statistik di video — hanya observasi korelasional dari diminishing peaks. Tidak ada K-node yang bergantung pada penjelasan causal ini.
- **Perlu validasi Claude Code:** Tidak — tidak actionable, cukup dicatat sebagai konteks.

---

## Flag Prioritas

1. **Entity-Adjusted Relative Unrealized Loss** — punya potensi langsung memperbaiki robustness threshold K1 signal #5 dan K4 kondisi #3 antar cycle, karena mengatasi masalah scale yang melekat di coin-count based Supply-in-Loss.
2. **MVRV Z-Score rolling 1-tahun + price band** — berpotensi jadi cross-check independen untuk validasi batas zona Z4/Z5 (AVIV Mean/Upper), kalau angkanya align.
3. **Data diminishing MVRV peaks per cycle (angka konkret)** — worth disimpan sebagai referensi numerik tambahan untuk K1 signal #1, walau bukan insight baru.

---

## Yang Langsung Diabaikan

- Narasi causal soal institutional maturation menurunkan volatility — tidak actionable, tidak ada data pendukung kuat di luar observasi korelasional.
- Perbandingan Z-score cumulative vs 4Y/2Y rolling window — cuma proses eliminasi menuju kesimpulan 1Y window, tidak perlu dicatat terpisah dari insight #2 di atas.
