# Findings — DCA Backtest Claim & Stabilitas Calmar Ratio Lintas Cycle

**Video:** This Strategy Beat Bitcoin DCA by 20x (On-Chain Mind, 2026-07-28)
**Tanggal validasi:** 2026-07-29
**Script:** [`analyze_dca_backtest_and_calmar.py`](analyze_dca_backtest_and_calmar.py)
**CSV:** [`events_dca_backtest_calmar.csv`](events_dca_backtest_calmar.csv)
**Data:** `data_master_all_metrics.csv` kolom `btc_price`, 2010-07-17 s/d 2026-07-15, kontinu tanpa gap (n=5.843 hari)

---

## Insight #1 — Klaim backtest DCA video ($10k → $446k, CAGR ~36%, MaxDD ~83%)

**Definisi event:** kontribusi periodik tetap dari 2014-01-01 s/d 2026-07-15 (data terakhir tersedia, dekat tanggal video). Dua varian cadence dicoba karena presenter tidak menyebutkan cadence pasti: mingguan (tiap 7 hari kalender) dan bulanan (tanggal 1 tiap bulan). Portfolio di-mark-to-market **harian** supaya max drawdown menangkap crash intra-periode. Max drawdown dihitung dari peak **nilai portofolio kumulatif** (bukan harga BTC mentah) — metode ini melunakkan drawdown dibanding buy-and-hold murni karena kontribusi baru terus menambah basis, konsisten dengan cara kerja kalkulator DCA pada umumnya. CAGR dihitung dengan `(final/contributed)^(1/years)-1` (metode retail sederhana) karena ini yang tampaknya dipakai presenter — XIRR (money-weighted) dilaporkan sebagai pembanding, bukan pengganti.

| Varian | Total Return | CAGR (simple) | XIRR | Max DD | n kontribusi |
|---|---|---|---|---|---|
| Mingguan | 4.449% | 35,6% | 55,4% | -82,9% | 655 |
| Bulanan | 4.448% | 35,6% | 55,2% | -82,9% | 151 |
| **Klaim video** | **~4.000%** | **~36%** | — | **~83%** | — |

**Sensitivity check** (bukan mencari yang cocok — cuma cek stabilitas terhadap pergeseran start date beberapa bulan, cadence bulanan):
- start 2014-04-01 → total return 4.351%, CAGR 36,2%, MaxDD -82,9%
- start 2013-10-01 → total return 4.914%, CAGR 35,8%, MaxDD -83,0%

**Toleransi vs klaim video (±15%):** Mingguan — total return diff +11,2%, CAGR diff -1,1%, MaxDD diff -0,1% → **MATCH**. Bulanan — hasil nyaris identik → **MATCH**.

### Verdict #1: KONFIRMASI

Angka backtest DCA yang disebut presenter reproducible dari data harga BTC riil di kedua varian cadence (hasilnya nyaris identik satu sama lain, beda <0,1pp), match dalam toleransi ±15% di ketiga metrik (total return, CAGR, max drawdown), dan stabil terhadap pergeseran start date ±3-6 bulan. n=2 varian cadence + 2 sensitivity check start date — cukup untuk menyimpulkan angka ini bukan cherry-picked start date yang eksesif presisi.

---

## Insight #2 — Calmar Ratio (0,44) sebagai tolok ukur stabil DCA/BTC

**Definisi event:** CAGR dan Max Drawdown BTC **buy-and-hold lump-sum** (bukan equity curve DCA insight #1 — dipilih karena kontribusi DCA lintas-cycle tercampur dan tidak bisa dipecah bersih per-cycle) dihitung per cycle penuh, memakai konvensi cycle boundary **bottom-to-bottom yang sudah established** di project Onchain-Dashboard (`research/framework_review_2026-07/backtest_k5nz/run_backtest.py`) — bukan definisi baru, supaya konsisten dengan backtest lain di project ini.

| Cycle | Periode | Harga awal→akhir | CAGR | Max DD | Calmar |
|---|---|---|---|---|---|
| S1 2013-2015 | 2013-01-01 → 2015-01-14 (2,03y) | $13,36 → $178,50 | 257,7% | -84,6% | **3,047** |
| S2 2015-2018 | 2015-01-15 → 2018-12-15 (3,92y) | $210,05 → $3.290,85 | 101,9% | -83,2% | **1,225** |
| S3 2018-2022 | 2018-12-16 → 2022-11-21 (3,93y) | $3.303,16 → $15.774,48 | 48,8% | -76,6% | **0,637** |
| S4 2022-sekarang* | 2022-11-22 → 2026-07-15 (3,64y) | $16.205,82 → $65.097,92 | 46,5% | -53,1% | **0,875** |

*S4 belum selesai — cycle terbuka, CAGR & Max DD masih bisa berubah signifikan.

**n=4 cycle**, mean Calmar=1,446, rentang 0,637–3,047 (~5x variasi), std=1,094.

**Konteks:** window tunggal 2014-2026 (window yang dipakai presenter) sebagai lump-sum single-window menghasilkan CAGR 42,6%, MaxDD -83,2%, Calmar 0,512 — dekat dengan klaim video 0,44 (selisih karena video memakai equity curve DCA yang max-drawdown-nya sedikit lebih lunak akibat kontribusi baru terus menambah basis selama periode berjalan).

### Verdict #2: NEGATIF

Calmar Ratio BTC **tidak stabil** lintas cycle — bervariasi ~5x antar cycle (0,637 di 2018-2022 hingga 3,047 di 2013-2015). Angka 0,44/0,512 yang disebut video adalah artefak window 12-tahun spesifik yang mereka pilih (kebetulan mencakup satu drawdown besar 2018 sambil merata-ratakan CAGR lewat compounding jangka panjang), **bukan karakteristik BTC yang konsisten per-cycle**. Calmar Ratio BTC cenderung menurun dari cycle ke cycle (3,05 → 1,23 → 0,64 → 0,88), konsisten dengan pola diminishing-returns yang sudah dikenal di framework, tapi dengan n=4 ini masih indikatif, bukan konklusif.

**Flag sample size & independensi:** n=4 cycle ada di ambang batas minimum kepercayaan framework (3-4 cycle), dan S4 masih terbuka sehingga Calmar-nya bisa bergeser sebelum cycle ini selesai. S1 dan S2 juga tidak sepenuhnya independen — keduanya sama-sama mencerminkan fase pertumbuhan market cap kecil→besar yang sama secara struktural, bukan dua sampel acak yang bebas satu sama lain.

**Implikasi untuk Decision Framework:** relevan ke Governance poin 4 (backtest mesin utuh vs HODL/DCA yang masih pending) — kalau Calmar Ratio dipakai sebagai salah satu metrik evaluasi di masa depan, jangan pakai satu angka window-tunggal sebagai acuan; laporkan sebaran per-cycle karena variasinya besar.

---

## Di luar scope (tidak divalidasi — alasan eksplisit)

- **Strategi "Trading Cross" / Z-Score Probability Waves** — formula dan window SD tidak diungkap presenter (black-box). Mereproduksi tanpa tahu parameter pasti berarti menebak sampai "cocok" dengan hasil video — itu overfitting yang dilarang STANDAR VALIDASI poin 6. Tidak dicoba.
- **Leg Gold dan S&P 500** dari perbandingan video — `NEEDS-DATA-WE-DONT-HAVE`, dashboard on-chain kita BTC-only.
- **Monte Carlo 10.000 simulasi reshuffling** — bergantung pada strategi black-box di atas, tidak bisa direplikasi secara independen.

## Bahasa probabilistik & catatan penutup

Klaim performa historis DCA (insight #1) **cenderung akurat** dan reproducible dari data riil — bukan angka yang dikarang atau cherry-picked secara eksesif. Namun klaim implisit bahwa Calmar 0,44 mencerminkan karakteristik "buruk" DCA/BTC secara umum **cenderung tidak didukung** data lintas-cycle — angka itu spesifik untuk window 12-tahun yang dipilih presenter, dan bisa jadi 2-5x lebih baik atau lebih buruk tergantung cycle mana yang dilihat.
