# This Strategy Beat Bitcoin DCA by 20x
**Channel:** On-Chain Mind
**Tanggal video:** 2026-07-28
**Tanggal analisis:** 2026-07-29
**Link:** https://www.youtube.com/watch?v=e0NAIj7tpgY

---

## Ringkasan

Video pendek (7:49) yang beda karakter total dari video-video On-Chain Mind sebelumnya di project ini (yang fokus MVRV/SOPR/F&G untuk positioning jangka panjang). Video ini memperkenalkan produk "strategy lab" mereka: indikator proprietary **Z-Score Probability Waves** (mean-reversion tool berbasis standard deviation dari baseline harga BTC yang adaptif, formula persis tidak diungkap) dan strategi trading turunannya, **"Trading Cross"** — entry saat probability wave cross di atas +1, exit saat cross balik ke bawah 0. Backtest 2014-2026: DCA BTC $10K→$446K (CAGR 36%, max drawdown 83%) vs Trading Cross $10K→$8 juta lebih (CAGR 72%, max drawdown 42,9%, Calmar ratio 1,68 vs DCA 0,44), juga dibandingkan ke Gold dan S&P 500. Ditutup dengan Monte Carlo 10.000 simulasi reshuffling daily return untuk klaim robustness (5th percentile outcome $463K, masih di atas DCA).

Ini murni strategi price-based (Z-score dari harga, tanpa on-chain data), jadi sebagian besar insight masuk bucket [INDIKATOR CUSTOM]/[STRATEGI] — bukan konfirmasi/konflik langsung terhadap indikator aktif framework (MVRV/SOPR/NUPL/dst).

---

## Insight Inventory

### [INDIKATOR CUSTOM] Z-Score Probability Waves
- **Insight:** Indikator proprietary On-Chain Mind — mean-reversion tool yang menghitung standard deviation harga BTC dari baseline yang bergerak/adaptif ("Bitcoin in 2015 and Bitcoin in 2025 are not the same asset... baseline moves"). Reading +2 = harga 2 SD di atas baseline normal, -2 = 2 SD di bawah. [00:50]–[01:20]
- **Indikator terkait:** Tidak ada padanan langsung di 5 indikator aktif framework (MVRV, aSOPR, LTH/STH-SOPR, Supply in Profit/Loss, Realized Price family, RHODL). Konsep umum mirip rolling z-score, tapi diterapkan ke harga mentah, bukan rasio valuation (market cap/realized cap) seperti MVRV.
- **Relevan ke:** general
- **Test klaim:** Formula dan window rolling tidak diungkap presenter (black-box) — sama seperti "Risk indicators" On-Chain Mind di video F&G sebelumnya. Tidak bisa dinilai apakah baseline-nya benar-benar adaptif atau cuma smoothing biasa. Cycle dasar tidak diketahui karena parameter kalibrasi tidak diungkap. Supaya klaim salah: presenter mengungkap window-nya lalu ternyata fixed (bukan adaptif) — akan membatalkan klaim "baseline yang bergerak".
- **Perlu validasi Claude Code:** Tidak — black-box, mereplikasi tanpa tahu parameter pasti berarti menebak sampai cocok dengan hasil video (overfitting, dilarang STANDAR VALIDASI poin 6).

### [STRATEGI] "Trading Cross" — entry/exit rule berbasis probability wave
- **Insight:** Entry saat probability wave cross di atas +1 ("entry demands proof" — sudah 1 SD penuh di atas baseline), exit saat cross balik ke bawah 0 ("exit demands nothing else"). Disebut "deliberately simple but asymmetric": entry ketat, exit longgar tanpa konfirmasi weakness — kebalikan perilaku retail (masuk karena hope, keluar telat karena hope). [01:42]–[02:11]
- **Indikator terkait:** Z-Score Probability Waves (turunan langsung)
- **Relevan ke:** general — murni price-momentum, tidak ada padanan di K1-K6 (semua berbasis on-chain valuation/behavioral metrics)
- **Test klaim:** Threshold absolut jelas (cross di atas +1, di bawah 0 adalah angka tetap yang ditempel di atas z-score yang katanya adaptif) — catat sebagai penyimpangan dari filosofi framework sendiri (pola relatif). Jumlah trade/cross event aktual sepanjang 2014-2026 tidak pernah disebutkan — n trade unknown. Supaya klaim salah: kalau direplikasi, hasil didominasi 1-2 cross besar di satu cycle tertentu, klaim "edge asymmetric yang robust" runtuh jadi cerita survivorship.
- **Perlu validasi Claude Code:** Tidak — formula black-box (sama seperti di atas), data harga BTC harian tersedia penuh tapi tanpa parameter pasti replikasi berarti menebak — overfitting.

### [STRATEGI] Klaim backtest performa (DCA vs Trading Cross vs Gold vs S&P 500)
- **Insight:** $10.000 awal (~2014-2026): DCA BTC → $446.000 (return 4.000%, CAGR 36%, max DD 83%); Gold → $32.000; S&P 500 → $40.000; Trading Cross → >$8 juta (return 80.000%, CAGR 72%, max DD 42,9%). Presenter menekankan efek compounding: menggandakan CAGR selama satu dekade menghasilkan gap yang "absurd" (20x, bukan 2x). [00:03]–[00:19], [02:44]–[03:53]
- **Indikator terkait:** Z-Score Probability Waves / Trading Cross
- **Relevan ke:** general — framework sendiri masih menunggu "backtest mesin utuh vs HODL/DCA" (Governance poin 4, Decision Framework v2 — masih pending)
- **Test klaim:** "Since 2014" tidak presisi (tanggal mulai eksak tidak disebut), cadence DCA tidak disebut, tidak ada disclosure fee/slippage untuk leg trading aktif, eksekusi at-close/intraday tidak jelas. Cycle dasar ~2014-2026 ≈ 3 cycle penuh + 1 belum selesai — borderline sample, dan cuma satu angka agregat 12 tahun (tidak ada breakdown per-cycle di video). Supaya klaim salah: replikasi leg DCA tidak match angka video, atau breakdown per-cycle menunjukkan hasil timpang (dominan satu bull run).
- **Perlu validasi Claude Code:** Ya (scoped, leg DCA saja — leg Trading Cross black-box tidak reproducible, leg Gold/S&P500 = NEEDS-DATA-WE-DONT-HAVE karena dashboard kita BTC-only).

**[VALIDASI — 2026-07-29, CLOSED]** Angka backtest DCA video ($10K→$446K, CAGR ~36%, max DD ~83%) **KONFIRMASI** — reproducible dari data BTC 2014-2026 di cadence mingguan maupun bulanan (n=2 varian cadence + 2 sensitivity check start date ±3-6 bulan), semua match dalam toleransi ±15% di ketiga metrik. Leg Trading Cross, Gold, dan S&P 500 tidak divalidasi (black-box / data tidak tersedia). Detail: [`findings_dca_backtest_and_calmar.md`](findings_dca_backtest_and_calmar.md)

### [STRATEGI] Drawdown math & narasi psikologis 83% drawdown DCA
- **Insight:** Trading Cross max drawdown 42,9% vs DCA 83%. Presenter menjelaskan makna praktis: 83% DD berarti $100K jadi $17K, perlu +490% untuk balik modal, dan ini titik di mana "pretty much everybody sells" — menjelaskan kenapa banyak orang gagal capture return DCA 4.000% meski secara backtest terlihat bagus. [04:13]–[04:39]
- **Indikator terkait:** tidak spesifik — mekanik drawdown matematis umum
- **Relevan ke:** general — paralel konseptual dengan alasan framework membatasi LTV & pakai staged-cut (sama-sama soal mengelola magnitude drawdown supaya "investable" secara psikologis, bukan cuma matematis)
- **Test klaim:** Bagian aritmatika (recovery % = 1/(1-loss%) - 1) benar dan tidak perlu data untuk diverifikasi. Klaim psikologis ("titik dimana orang capitulate") bersifat naratif/anekdotal, tidak falsifiable dengan data on-chain yang kita punya. 83% DD historis BTC konsisten dengan drawdown ATH-ke-bottom 2018 (~84%) dan 2022 (~77%) — bukan klaim baru.
- **Perlu validasi Claude Code:** Tidak — aritmatika tidak butuh data, bagian psikologis tidak actionable/tidak ada kolom data relevan.

### [STRATEGI] Monte Carlo reshuffling 10.000 simulasi untuk uji robustness
- **Insight:** 10.000 simulasi mereshuffle urutan daily return historis Trading Cross untuk memisahkan "genuine edge" dari "luck of sequencing". Hasil: 5th percentile outcome $463.000 (masih di atas DCA $446.000), median simulasi mendekati angka backtest asli → disimpulkan sebagai bukti robustness. [05:44]–[07:10]
- **Indikator terkait:** tidak spesifik — teknik validasi statistik generik (reshuffling/bootstrap), bukan indikator on-chain
- **Relevan ke:** general — metodologi berpotensi jadi referensi untuk standar validasi pipeline ini sendiri
- **Test klaim:** Reshuffling daily return mengasumsikan return **independent/i.i.d.**, padahal Trading Cross bersifat state-dependent (posisi long/flat bergantung trajectory z-score sebelumnya, dan BTC sendiri punya autocorrelation/trending regime). Ini berpotensi **overclaim robustness** — reshuffle bisa mempertahankan return besar yang sebenarnya berkorelasi dengan momentum yang sudah "dipakai" strategi state-dependent. Reshuffle tidak menambah cycle independen baru, cuma menyusun ulang return dari ~3 cycle yang sama — tidak menyelesaikan masalah sample size dasar. Supaya klaim salah: block-bootstrap (menjaga blok autocorrelation, bukan reshuffle harian penuh) menghasilkan 5th percentile di bawah DCA.
- **Perlu validasi Claude Code:** Tidak — tidak reproducible (black-box, price-only). Kritik metodologis (asumsi i.i.d. yang salah untuk strategi state-dependent) dicatat sebagai catatan kualitatif — lihat Flag Prioritas.

### [BARU] Calmar Ratio (CAGR ÷ Max Drawdown) sebagai metrik evaluasi risk-adjusted return
- **Insight:** Trading Cross Calmar = 1,68 vs DCA = 0,44 ("untuk tiap 1% pain, Trading Cross dapat 1,68% growth vs DCA cuma 0,44%" — ~4x kompensasi). Rule-of-thumb disebutkan: "anything above one is considered absolutely excellent." [04:41]–[05:44]
- **Indikator terkait:** Calmar Ratio (metrik finance standar, bukan buatan channel — tapi cara pakainya untuk evaluasi strategi ini baru untuk framework kita)
- **Relevan ke:** general — framework belum pernah eksplisit pakai Calmar ratio; relevan ke Governance poin 4 Decision Framework (backtest mesin utuh vs HODL/DCA, masih pending)
- **Test klaim:** "Di atas 1 = excellent" adalah threshold absolut (rule-of-thumb industri, bukan kalibrasi ke cycle BTC) — tapi dipakai untuk perbandingan relatif (1,68 vs 0,44), risikonya lebih rendah dibanding threshold absolut ala harga/MVRV. Dihitung dari satu backtest agregat 12 tahun (n=1 window) — tidak diketahui dari video apakah rasio ini stabil per-cycle.
- **Perlu validasi Claude Code:** Ya (scoped — bukan untuk Trading Cross yang black-box, tapi untuk cek apakah Calmar 0,44 representatif lintas cycle BTC, relevan ke Governance poin 4 framework).

**[VALIDASI — 2026-07-29, CLOSED]** Calmar Ratio BTC (CAGR ÷ Max Drawdown) **NEGATIF** sebagai tolok ukur stabil — bervariasi ~5x lintas 4 cycle bottom-to-bottom (0,637 di 2018-2022 hingga 3,047 di 2013-2015; n=4, cycle terakhir 2022-sekarang belum selesai, mean 1,45, std 1,09). Angka 0,44/0,512 yang disebut video adalah artefak window 12-tahun spesifik yang mereka pilih, bukan karakteristik BTC yang konsisten per-cycle — cenderung menurun dari cycle ke cycle konsisten dengan pola diminishing-returns framework, tapi n=4 masih indikatif. Detail: [`findings_dca_backtest_and_calmar.md`](findings_dca_backtest_and_calmar.md)

### [KONFIRMASI] Baseline adaptif lebih baik daripada threshold absolut untuk Bitcoin
- **Insight:** Presenter menekankan alasan pakai baseline yang bergerak (bukan harga tetap): "Bitcoin in 2015 and Bitcoin in 2025 are not the same asset. Volatility compressed, market cap grown by orders of magnitude" — baseline harus adaptif terhadap perubahan struktural aset, bukan level harga absolut fixed. [01:19]–[01:30]
- **Indikator terkait:** Z-Score Probability Waves (konsep umum), relevan juga secara filosofis ke AVIV Mean/Upper, MVRV Z-Score, Realized Price family di framework
- **Relevan ke:** general — prinsip utama framework ("threshold absolut tidak reliable antar cycle — framework pakai pola relatif")
- **Test klaim:** Mengkonfirmasi filosofi framework (baseline adaptif lebih tepat dari angka absolut), TAPI ada nuance penting: aturan entry/exit Trading Cross itu sendiri (cross di atas +1, di bawah 0) adalah threshold absolut yang ditempel DI ATAS z-score relatif — video ini sebenarnya mencampur pendekatan relatif (baseline adaptif) dengan pendekatan absolut (angka cutoff +1/0 tetap), jadi bukan konfirmasi murni 100%.
- **Perlu validasi Claude Code:** Tidak — observasi kualitatif, tidak ada angka spesifik untuk diuji, sudah sejalan dengan prinsip framework.

---

## Flag Prioritas

1. **"Trading Cross" sebagai potensi tactical sleeve terpisah** — secara fundamental beda pendekatan (price-momentum trading vs on-chain valuation zone-based), tapi presenter memposisikannya sebagai produk terpisah ("strategy lab"), bukan pengganti keputusan capital allocation/LTV utama. claim-tester menilai ini **bukan STOP-worthy**, tapi worth didiskusikan apakah ada ruang untuk tactical sleeve terpisah dari framework zone-based utama.
2. **Kritik metodologis Monte Carlo reshuffling** — asumsi i.i.d. pada reshuffling daily return kemungkinan tidak valid untuk strategi state-dependent seperti Trading Cross, berpotensi overclaim "robustness". Worth dicatat sebagai standar metodologi kalau pipeline ini kelak melakukan uji serupa (reshuffling naif vs block-bootstrap yang menjaga autocorrelation).
3. **Ketidakstabilan Calmar Ratio BTC lintas cycle (tervalidasi)** — relevan langsung ke Governance poin 4 Decision Framework yang masih pending (backtest mesin utuh vs HODL/DCA): kalau Calmar dipakai sebagai metrik evaluasi di masa depan, jangan pakai satu window tunggal — laporkan sebaran per-cycle.

---

## Yang Langsung Diabaikan

- [00:24]–[00:48]: Klaim kredibilitas metodologi presenter (bukan backtest yang dioptimasi sampai sempurna, dipakai real-time subscriber, ditest untuk "coba dipatahkan" di strategy lab) — framing/marketing, tidak mengandung mekanik on-chain atau data yang bisa diuji.
- [07:11]–[07:37]: Ajakan ke onchainmind.io untuk coba strategy lab & strategi lain — murni promosi.
