# Bitcoin's Trend Is Bearish — Here's Where It Flips
**Channel:** On-Chain Mind
**Tanggal video:** 11 Agustus 2026
**Tanggal analisis:** 12 Agustus 2026
**Link:** https://youtu.be/dAv-by3Up_8

*Flag STOP (bukan konflik hard constraint, tapi perlu didiskusikan): toolkit video ini (regression channel, adaptive trend model, kernel envelope, echoes, velocity RSI) adalah sistem TA price-based yang berdiri sendiri dengan trigger konkret ($78.000/$67.000 untuk adaptive trend model) yang berfungsi paralel dengan gate K1/K3 kita — tapi berbasis price-technical, bukan on-chain cost-basis. Lihat [STRATEGI] "Rekonsiliasi multi-timeframe" untuk detail dan rekomendasi.*

---

## Ringkasan

Video 12 menit yang eksplisit dibingkai sebagai "technical analysis standpoint only" oleh pembicaranya sendiri — berbeda dari video-video On-Chain Mind sebelumnya yang biasanya bertumpu pada on-chain cost-basis metrics. Isinya adalah rundown lima tool proprietary channel ini (trend channel/regression, adaptive trend model, kernel envelope, echoes, velocity RSI) plus tiga moving average standar (200-day, yearly/365-day, 200-week), semuanya berbasis price action murni.

Kesimpulan taktisnya bearish di semua lini: trend channel turun dari $120.000 ke $58.000 (R²=0,84), adaptive trend model bearish 87 hari (flip di $78.000 pertengahan Mei, -18% sejak itu, butuh tembus $67.000 untuk flip balik), harga di bawah 200-day MA (~$70.000) dan yearly MA (~$85.000), echoes memproyeksikan -3,1% dalam 3 minggu (~$62.000), dan kernel envelope netral (harga persis di baseline $64.300). Tapi pembicara membingkai ini sebagai cerita berbeda dari sisi strategis/siklus: weekly velocity RSI ~14% (di bawah threshold 15% yang mereka klaim historically menandai generational bottom) dan harga persis di 200-week MA ($63.800, diklaim compounding 30%/tahun konsisten 4 tahun) — dibaca sebagai multi-year accumulation zone. Prinsip yang ditekankan berulang: tidak ada satu chart yang cukup sendirian, hanya confluence semua chart yang berarti.

Tiga validasi dijalankan (data mentok 2026-07-15, gap 27 hari ke tanggal video — semua angka "current" diverifikasi lewat proxy/ekstrapolasi pendek). Hasilnya: dua klaim numerik (200-week MA, MA ladder $70K/$85K) **akurat**, tapi klaim "selalu jadi floor" untuk 200-week MA **hanya sebagian benar** (83% hit rate, bukan 100%), dan yang paling penting — klaim "generational bottom" dari velocity RSI **kontradiksi langsung** dengan state on-chain kita sendiri (K4 count = 0/4, zona ZD bukan Z1/capitulation).

---

## Insight Inventory

### [INDIKATOR CUSTOM] Trend channel (regression channel)
- **Insight:** Regression channel yang ditarik dari $120.000 turun ke $58.000 sepanjang tahun ini, dengan R²=0,84 (84% variasi harga tertangkap garis tren). Price action-nya: series lower highs/lower lows (downtrend klasik), tapi baru-baru ini muncul satu higher low — dianggap "first crack of light" (bukan konfirmasi reversal, tapi prasyarat sebelum reversal bisa terjadi). `[00:31]`–`[02:09]`
- **Indikator terkait:** Linear regression trend channel + price structure (HH/LL reading) — komponen dasarnya murni price action geometris, tidak dikombinasikan dengan data on-chain apapun.
- **Relevan ke:** general — framework kita tidak pakai regression channel; endpoint channel dipilih manual/arbitrer sehingga tidak reproducible.
- **Test klaim:** Pemilihan titik awal/akhir channel arbitrer dan tidak deterministik — R²=0,84 hanya berarti fit-nya bagus untuk window yang mereka pilih, bukan bahwa channel itu prediktif. "First crack of light" tidak punya kriteria falsifiability eksplisit (kapan higher low ini dianggap gagal tidak disebutkan). Sample: 1 channel, 1 downtrend berjalan — tidak ada basis multi-cycle karena metodenya subjektif per-gambar.
- **Perlu validasi Claude Code:** Tidak — bukan on-chain, endpoint arbitrer sehingga tidak reproducible dari data kita, dan klaimnya tidak actionable secara spesifik untuk framework zone-based.

### [INDIKATOR CUSTOM] Adaptive trend model
- **Insight:** Regime-flip system trend-following, saat ini bearish 87 hari (flip di $78.000 pertengahan Mei, -18% sejak itu). Level flip BUKAN angka tetap — diset oleh volatilitas: makin tenang market dan makin sempit range harian, makin kecil jarak yang perlu ditempuh harga untuk membalik regime. Saat ini butuh tembus $67.000 untuk flip bullish. Diklaim tervalidasi cross-asset (ETH bullish sejak awal Juli; Tesla flip bearish Juni di $423, menghindari -15%) dengan model & rules identik tanpa refitting per aset. `[00:02]`, `[02:09]`–`[03:52]`
- **Indikator terkait:** Volatility-adaptive regime detection — formula tidak dijelaskan detail, konsepnya mirip breakout system dengan band yang mengembang/menyempit sesuai volatilitas realized.
- **Relevan ke:** general — secara fungsi mirip regime detection framework kita (alarm bear CEPAT/PRESISI § 0), tapi berbasis price/volatility murni, bukan on-chain (STH-SOPR gap, MVRV momentum cross).
- **Test klaim:** Formula proprietary, tidak bisa direplikasi dari kolom data kita manapun. Klaim "tervalidasi cross-asset tanpa refitting" tidak bisa dicek independen — kita tidak punya data ETH/Tesla, dan bahkan kalau ada, itu klaim milik channel bukan sesuatu yang testable balik. Level flip $78K/$67K adalah threshold absolut hasil formula tersembunyi — tidak ada cara verifikasi apakah -18% sejak flip itu representatif atau selective reporting.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (formula proprietary tidak bisa direplikasi; data ETH/Tesla juga tidak ada di dataset kita).

### [INDIKATOR CUSTOM] Kernel envelope
- **Insight:** Band atas-bawah di sekitar baseline yang dihitung pakai kernel regression (bobot lebih berat ke data terdekat, sehingga baseline "menekuk" mengikuti price action lokal, bukan lagging seperti MA biasa). Wick harga yang keluar dari envelope dibaca sebagai sinyal mean-reversion ke baseline lebih mungkin terjadi. Saat ini harga persis di tengah baseline ($64.300) — dibaca sebagai kondisi netral/boring, tidak ada stretch untuk di-fade di kedua arah. `[04:40]`–`[06:03]`
- **Indikator terkait:** Kernel regression band — pada dasarnya varian Bollinger Band/Keltner Channel dengan baseline kernel-weighted.
- **Relevan ke:** general — horizon sangat jangka pendek (short-term trading), tidak match horizon K-node manapun.
- **Test klaim:** Band proprietary, parameter (bandwidth, kernel type) tidak diketahui. Klaim "harga di tengah = netral" adalah observasi deskriptif snapshot satu titik waktu, bukan klaim yang testable lintas cycle.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (formula tidak diketahui, tidak bisa direplikasi).

### [INDIKATOR CUSTOM] Echoes (pattern-matching analog engine)
- **Insight:** Mencari momen historis (1 tahun terakhir) dengan kombinasi state trend+momentum+waktu yang mirip kondisi sekarang (bukan pattern-matching candlestick visual), lalu mengukur outcome 3 minggu setelahnya di semua momen analog itu. Median outcome saat ini: -3,1% dalam 3 minggu, membawa harga ke sekitar $62.000. `[06:16]`–`[07:40]`
- **Indikator terkait:** Analog/state-matching model — kemungkinan turunan dari trend channel + velocity RSI + adaptive trend model mereka sendiri, dikombinasikan jadi satu "state vector".
- **Relevan ke:** general — prediksi harga jangka pendek, tidak match K-node manapun.
- **Test klaim:** Window lookback hanya 1 tahun — kemungkinan besar analog yang ditemukan overlapping/autocorrelated (banyak berasal dari hari-hari berdekatan dalam bear market yang sama), jadi n efektif independen jauh lebih kecil dari n nominal. Median -3,1%/$62.000 adalah titik data tunggal untuk kondisi sekarang, bukan hasil test lintas banyak siklus. Definisi "state mirip" proprietary — tidak bisa direplikasi.
- **Perlu validasi Claude Code:** Tidak — state definition proprietary tidak bisa direkonstruksi dari kolom yang ada, dan window lookback 1 tahun terlalu pendek untuk klaim yang reliable meski bisa direplikasi.

### [INDIKATOR CUSTOM] Velocity RSI
- **Insight:** Varian RSI berbasis "directional pressure" (seberapa besar pergerakan konsisten mendorong satu arah), bukan raw price change seperti RSI standar — diklaim lebih tahan choppy/sideways market. Weekly velocity RSI saat ini ~14%, di bawah threshold 15% yang diklaim historically menandai "generational bottom" / setiap peluang akumulasi besar dalam sejarah Bitcoin. Sempat naik di atas 15% saat rally Mei ke $75.000, lalu turun kembali ke bawah 15% sekarang. `[00:02]`, `[07:40]`–`[08:41]`
- **Indikator terkait:** RSI variant berbasis directional pressure — secara fungsi paralel dengan cara framework menandai capitulation extreme (Supply in Profit, LTH-SOPR), tapi berbasis price momentum murni, bukan on-chain cost-basis.
- **Relevan ke:** K4 / Z1 (bear bottom accumulation).
- **Test klaim:** Threshold 15% adalah angka absolut — framework kita pakai pola relatif, bukan angka tetap. Untuk cycle saat ini baru satu observasi "generational bottom" yang belum terkonfirmasi outcome-nya; tidak disebutkan berapa kali historis threshold ini tembus di siklus-siklus sebelumnya (kalau <3 cycle = low-confidence). Falsifiability tidak jelas — tidak ada batas waktu kapan "generational bottom" dianggap gagal, rawan post-hoc rationalization.
- **Perlu validasi Claude Code:** Ya — cross-check klaim "historically cheap / generational bottom" terhadap sinyal on-chain independen kita.

**[VALIDASI — 12 Agustus 2026, CLOSED]** Cross-check independen K4 (4 kondisi bear-bottom framework) di 2026-07-15 (proxy, gap 27 hari ke tanggal video) menunjukkan **0/4 kondisi menyala** dan zona = **ZD (dip dalam)**, bukan Z1/capitulation — terakhir kali K4 count≥2 adalah 2023-01-10 (**1.282 hari** sebelumnya). Ini **kontradiksi** dengan narasi "generational bottom" video: harga memang turun ~48% dari ATH cycle ($124.714 → $65.098), tapi metrik on-chain kita (LTH-MVRV=1,305; LTH-SOPR=0,725; Supply in profit=56,9%; Price/CVDD=1,326) semuanya masih jauh dari level capitulation historis. **n=1 snapshot** (bukan event study) — tidak bisa memastikan kondisi persis di tanggal video karena gap data 27 hari, tapi perlu penurunan on-chain yang sangat tajam dan cepat untuk berubah dari ZD ke Z1 dalam waktu sesingkat itu.
Detail: [`findings_velocity_rsi_onchain_crosscheck.md`](findings_velocity_rsi_onchain_crosscheck.md)

---

### [BARU] Higher low sebagai prasyarat awal trend reversal
- **Insight:** Dalam struktur downtrend (lower highs/lower lows), munculnya satu higher low tidak mengonfirmasi reversal, tapi merupakan syarat pertama yang harus terjadi sebelum tren bisa berubah arah — tanpa itu, "kamu belum punya apa-apa". `[00:31]`
- **Indikator terkait:** Price structure reading (swing high/low sequencing) — bukan indikator numerik, murni pembacaan struktur harga klasik TA.
- **Relevan ke:** general — framework kita tidak menggunakan price-structure/swing high-low sebagai sinyal.
- **Test klaim:** Heuristik price-structure generik, tidak ada threshold terukur, tidak ada kriteria eksplisit kapan dianggap gagal atau berhasil. Nyaris tautologis ("syarat pertama, bukan bukti") sehingga sulit difalsifikasi. Bukan klaim dengan sample size tertentu karena tidak didefinisikan sebagai event yang bisa dihitung.
- **Perlu validasi Claude Code:** Tidak — murni naratif/deskriptif, tidak actionable secara spesifik, tidak ada event definition yang bisa diuji.

### [BARU] 200-day MA dan yearly MA sebagai resistance ladder
- **Insight:** Harga saat ini di bawah 200-day MA (~$70.000) dan yearly MA (~$85.000). Dibaca sebagai ladder resistance: area $67.000-$70.000 = level flip bias jangka pendek, $85.000 = level di mana macro trend baru bisa dianggap terkonfirmasi sepenuhnya bullish. `[03:52]`
- **Indikator terkait:** 200-day Moving Average, Yearly (365-day) Moving Average — indikator TA standar dan sangat umum, tidak dipakai di framework kita.
- **Relevan ke:** general — paling dekat konseptual dengan cara framework memakai AVIV Mean/Upper sebagai resistance ladder di Z4/Z5, tapi berbasis price MA, bukan cost-basis on-chain.
- **Test klaim:** $67-70K dan $85K adalah threshold absolut — framework pakai pendekatan relatif (STH RP/RP/AVIV). Angka-angka ini dibaca dari chart/frame video, sehingga low confidence dari resolusi frame sampai diverifikasi. Kolom `200_dma` memang ada di data kita (bukan proprietary), jadi klaim ini unik di antara indikator video ini karena bisa diverifikasi langsung. Belum jelas berapa cycle dasar klaim "ladder resistance" ini — kemungkinan cuma observasi snapshot cycle ini saja.
- **Perlu validasi Claude Code:** Ya, prioritas rendah (accuracy-check angka saja, bukan structural insight).

**[VALIDASI — 12 Agustus 2026, CLOSED]** Cek akurasi angka: 200-day MA dan yearly (365-day) MA di data terakhir (2026-07-15, gap 27 hari) masing-masing $73.534 dan $88.728; ekstrapolasi tren pendek ke tanggal video (2026-08-11) menghasilkan **$70.109** dan **$85.796** — keduanya cocok erat dengan klaim video (~$70.000 dan ~$85.000). Harga confirmed di bawah kedua MA. Angka video **terverifikasi akurat**. n=1 (bukan event study, murni cek angka titik).
Detail: [`findings_ma_ladder_accuracy.md`](findings_ma_ladder_accuracy.md)

---

### [KONFIRMASI] Prinsip confluence — tidak ada satu sinyal cukup sendirian
- **Insight:** Speaker menegaskan di awal dan akhir video: tidak ada satu metrik on-chain atau TA yang bisa dipakai sendirian sebagai keputusan. Satu chart saja cuma "cerita", tapi kalau semua chart mengarah ke arah yang sama, itu baru jadi "sinyal dengan confluence". Prinsip ini dipakai eksplisit untuk menjelaskan kenapa bearish tactical (trend channel, adaptive trend model, echoes, kernel envelope) tidak kontradiksi dengan bullish strategic (velocity RSI, 200-week MA) — keduanya menjawab pertanyaan berbeda di timeframe berbeda. `[00:31]`, `[10:30]`
- **Indikator terkait:** general (prinsip meta, bukan indikator spesifik)
- **Relevan ke:** general — mendukung langsung filosofi framework kita: OR-gate/veto multi-sinyal di K1-K6, alarm bear yang butuh multi-sinyal, dsb.
- **Test klaim:** Ini meta-prinsip metodologi, bukan klaim empiris spesifik yang bisa diuji lawan data historis. Sudah konsisten dengan cara kerja framework kita sendiri.
- **Perlu validasi Claude Code:** Tidak — sudah established secara struktural di framework kita, tidak perlu dites ulang.

### [KONFIRMASI] Validasi model lewat konsistensi cross-asset/cross-era tanpa refitting
- **Insight:** Speaker menjelaskan cara mereka menguji apakah adaptive trend model genuine atau sekadar curve-fit ke sejarah Bitcoin: jalankan model & rules identik (tanpa refitting per aset) ke aset lain (ETH, Tesla) dan lihat apakah tetap menghasilkan sinyal yang masuk akal. `[02:09]`–`[03:52]`
- **Indikator terkait:** general (metodologi validasi, bukan indikator spesifik)
- **Relevan ke:** general — paralel dengan protokol usulan sinyal baru di Decision Framework (uji konsistensi arah antar era, hindari grid search), walau instrumen ujinya beda (cross-asset vs cross-era).
- **Test klaim:** Klaim tentang metodologi channel sendiri, bukan klaim on-chain yang bisa kita uji. Bagus sebagai prinsip anti-overfitting umum, tapi tidak ada cara verifikasi independen karena kita tidak punya data harga ETH/Tesla.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia, dan ini soal metodologi channel bukan klaim on-chain yang relevan ke framework kita.

### [KONFIRMASI] 200-week MA sebagai cyclical floor / multi-year accumulation zone
- **Insight:** 200-week MA saat ini di $63.800, dan harga persis di level ini. Diklaim compounding underlying growth rate Bitcoin ~30%/tahun konsisten selama 4 tahun terakhir. Setiap episode historis harga menyentuh atau di bawah 200-week MA diklaim selalu jadi multi-year accumulation zone. `[08:41]`
- **Indikator terkait:** 200-week Moving Average — indikator TA sangat umum, tidak dipakai di framework kita.
- **Relevan ke:** K4 / Z1 — konsep "cyclical floor" ini secara fungsi mirip dengan LTH RP, CVDD, dan AVIV Mean sebagai level akumulasi multi-tahun di framework kita, meski 200-week MA adalah metrik price-based murni.
- **Test klaim:** Klaim paling kuat dan paling testable di video ini — kolom `200_wma` ada penuh di data kita. Tapi ada tiga bagian yang perlu dipisah: (1) level saat ini — verifiable langsung; (2) CAGR 30%/tahun — testable; (3) "selalu jadi floor" — klaim absolut yang perlu definisi event eksplisit. Kemungkinan basis ~4-5 episode historis, cukup untuk ≥3 cycle tapi masih sample kecil dengan risiko selection bias tinggi kalau "accumulation zone" didefinisikan longgar setelah tahu hasilnya.
- **Perlu validasi Claude Code:** Ya — data lengkap, overlap konsep dengan K4/Z1.

**[VALIDASI — 12 Agustus 2026, CLOSED]** Level 200-week MA (~$63.800) dan CAGR rata-ratanya (29,1%/tahun point-to-point) **terverifikasi akurat**, tapi klaim "konsisten 30%/tahun" tidak presisi (variasi YoY 18,9%-37,0%). Klaim "selalu jadi accumulation floor yang bertahan" **hanya sebagian benar**: dari **n=6 episode evaluable (~4 siklus independen: 2015, 2020 COVID, 2022 bear, 2023 post-bear)**, **5 HOLDS / 1 BREACH (83%)** — episode BREACH (Jun-Jul 2022, low $18.973) ditembus lebih dalam oleh crash FTX November 2022. Overlap dengan zona akumulasi framework kita (ZC/Z1/ZD) konsisten 100%, tapi **3 dari 7 episode cuma capai ZD (dip moderat)**, bukan capitulation penuh — jadi "harga ≤200wma" bukan sinyal capitulation ekstrem yang reliable dengan sendirinya. Data mentok 2026-07-15 (gap 27 hari ke tanggal video, level saat ini pakai ekstrapolasi tren pendek → $63.813, cocok dengan klaim).
Detail: [`findings_200wma_cyclical_floor.md`](findings_200wma_cyclical_floor.md)

---

### [STRATEGI] Rekonsiliasi multi-timeframe: tactical bearish vs strategic bullish
- **Insight:** Speaker eksplisit membingkai kesimpulan video sebagai dua horizon berbeda yang tidak kontradiktif: (1) Tactical/short-medium term — bearish, didukung trend channel, adaptive trend model, MA ladder, echoes (-3,1%/3 minggu), kernel envelope netral; (2) Strategic/cyclical — historically cheap, didukung velocity RSI (<15%, generational bottom box) dan 200-week MA (multi-year accumulation zone). Gunakan sinyal jangka pendek untuk taktik entry/exit dan sinyal jangka panjang untuk keyakinan strategis, tanpa memaksa keduanya jadi satu kesimpulan tunggal. `[08:41]`, `[10:08]`–`[10:30]`
- **Indikator terkait:** general (kombinasi semua indikator di atas, dipetakan ke dua horizon waktu)
- **Relevan ke:** general — mirip secara struktural dengan cara framework kita memisahkan gate taktis per K-node dari struktur zone besar (Z1-Z5).
- **Test klaim:** Sintesis dari insight-insight lain, bukan klaim independen baru. Yang perlu dicatat: seluruh toolkit video ini adalah sistem TA price-based yang berdiri sendiri, dengan trigger konkret (adaptive trend model punya level flip $78K/$67K) yang berfungsi mirip gate K1/K3 tapi berbasis price-momentum, bukan cost-basis on-chain — secara struktural berbeda dari pendekatan zone-based + K-node kita.

  **Flag STOP** (bukan kontradiksi eksplisit hard constraint LTV, tapi worth didiskusikan): "Adaptive trend model" khususnya menawarkan sistem regime-flip dengan trigger harga konkret untuk keputusan bullish/bearish yang berfungsi paralel dengan gate K1/K3 — tapi berbasis price-technical, bukan on-chain cost-basis. Perlu diputuskan apakah sistem TA ini dipakai murni sebagai confirming layer tactical (tidak menggantikan apapun di framework), atau berisiko menarik keputusan keluar dari disiplin zone-based kalau sinyalnya berbeda arah dengan K-node aktif. Validasi Stage 3 di atas justru mendukung disiplin zone-based: velocity RSI mengklaim "generational bottom" padahal K4 count on-chain kita 0/4 — kalau adaptive trend model dipakai layaknya gate, sinyal TA-nya bisa menyesatkan tanpa konfirmasi on-chain.
- **Perlu validasi Claude Code:** Tidak — sintesis naratif dari komponen yang sudah divalidasi di atas.

---

## Flag Prioritas

1. **Sistem TA proprietary channel ini (khususnya adaptive trend model) berfungsi paralel dengan gate K1/K3 kita, tapi berbasis price bukan on-chain** — flag STOP dari claim-tester, perlu diputuskan apakah dipakai murni sebagai confirming layer atau berisiko menarik keputusan keluar dari disiplin zone-based. Lihat [STRATEGI] "Rekonsiliasi multi-timeframe" di atas.

2. **Velocity RSI "generational bottom" kontradiksi langsung dengan on-chain state kita** — K4 count = 0/4, zona ZD (dip dalam) bukan Z1/capitulation, terakhir K4 count≥2 adalah 2023-01-10 (1.282 hari lalu). Ini yang paling penting dari seluruh video: narasi "strategic bullish" video ini TIDAK didukung sinyal on-chain kita sendiri di tanggal yang sama — worth dipegang sebagai pengingat kalau video-video TA-heavy lain membuat klaim serupa ke depan.

3. **200-week MA "selalu jadi floor" hanya 83% hit rate, bukan 100%** — episode BREACH (Jun-Jul 2022) ditembus lebih dalam oleh FTX collapse. Berguna sebagai kalibrasi: bahkan level TA yang paling kuat secara historis (200-week MA) bisa gagal saat ada exogenous shock besar — jangan treat sebagai floor absolut kalau dipakai sebagai referensi.

---

## Yang Langsung Diabaikan

| Item | Timestamp | Alasan |
|---|---|---|
| Promosi onchainmind.io + 7-day free trial | `[06:03]`–`[06:16]` | Sponsor/promosi produk |
| Link artikel strategi "94% portfolio tetap di bear market -45%" | `[02:09]` | Promosi produk, tidak dijelaskan detail mekaniknya di video ini |
| Outro / musik penutup | `[11:43]`–selesai | — |

**Catatan kualitas data:** `data_master_all_metrics.csv` mentok update di 2026-07-15, gap 27 hari ke tanggal video (2026-08-11). Semua angka "current" di validasi Stage 3 memakai data 2026-07-15 sebagai basis, dengan ekstrapolasi tren pendek untuk mendekati tanggal video pada metrik yang trennya smooth (MA family) — TIDAK diekstrapolasi untuk metrik yang tidak smooth (MVRV, SOPR, Supply in Profit). Angka harga dari transcript ($67.000, $70.000, $85.000, dll) dibaca dari narasi video, bukan frame — tidak dilabel low-confidence.

---

**source_index.md belum diupdate — bilang kalau analisis ini sudah final.**
