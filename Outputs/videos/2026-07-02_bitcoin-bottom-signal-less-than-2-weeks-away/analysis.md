# Bitcoin Bottom Signal (Less Than 2 Weeks Away)
**Channel:** Bitcoin Magazine Pro
**Tanggal video:** 2026-07-02
**Tanggal analisis:** 2026-07-28
**Link:** https://www.youtube.com/watch?v=FHKoQYHyqCU

**🚩 Flag dari Stage 2 (claim-tester) — dilaporkan ke Yudi di chat, keputusan: catat saja, tidak ada tindak lanjut khusus.** Insight [STRATEGI] di video ini (confluence-based scaling-in) dinilai secara struktural berbeda dari pendekatan zone-based + K-node framework (tanpa gate/veto, tanpa hard LTV, tanpa zone sequencing). Ini bukan konflik langsung dengan keputusan terkunci manapun (topik video di luar domain indikator aktif framework), tapi cukup fundamental untuk ditandai. Lihat bucket [STRATEGI] di bawah.

---

## Ringkasan

Video 14 menit dari Bitcoin Magazine Pro yang mengklaim bottom sekunder BTC "kurang dari 2 minggu lagi" (sekitar 10-12 Juli 2026), berdasarkan "confluence" banyak sinyal: time-based capitulation fractal (day-count dari initial shock ke secondary low), Coinbase/"Crosby" ratio di level ekstrem, RSI weekly bullish divergence (BTC & MSTR), 50-week/100-week MA death cross, active address sentiment indicator (proprietary channel), MSTR NAV premium di bawah 1, dan disinggung sekilas production cost. Video ini **sama sekali tidak menyentuh indikator aktif framework** (MVRV, SOPR, Supply in Profit/Loss, Realized Price family, RHODL) — seluruh isinya TA klasik + proxy ekuitas MSTR + indikator custom channel sendiri. Karena hari ini sudah 2026-07-28 (26 hari setelah upload, cukup untuk mengecek beberapa prediksi tanggal spesifik), 4 dari 14 insight bisa diuji langsung lawan data historis; sisanya di luar cakupan dataset on-chain kita (RSI, MSTR, active address, production cost tidak di-track di `data_master_all_metrics.csv`).

---

## Insight Inventory

### [INDIKATOR CUSTOM] Time-based capitulation fractal (day-count shock→low)
- **Insight:** Selain price-based capitulation, ada "time-based capitulation" — jumlah hari dari initial sell-off shock ke secondary/final low tiap bear market (2022: 156 hari; 2018-19: 126 hari; 2015: lebih lama, masuk September), di-overlay ke price action saat ini untuk memproyeksikan bottom 12 Juli 2026. [00:02]-[02:12]
- **Indikator terkait:** Day-count pattern matching, bukan indikator standar
- **Relevan ke:** K4 (timing bear bottom) — filosofinya mirip "lantai waktu" K4 di framework, tapi anchor beda (dihitung dari initial shock, bukan dari cycle peak)
- **Test klaim:** Dasarnya cuma 3 cycle, salah satunya (2015) angkanya tidak presisi ("lebih lama"). Definisi "initial shock" sangat subjektif — tidak ada trigger on-chain baku, jadi mudah digeser sampai angka cocok (overfitting risk tinggi). Threshold day-count ini murni kalender/absolut.
- **Perlu validasi Claude Code:** Ya — cek falsifiability prediksi tanggal 12 Juli 2026.

**[VALIDASI — 2026-07-28, CLOSED]** Data hanya tersedia sampai 2026-07-15, menutupi 11 dari 15 hari window prediksi (±1 minggu dari 12 Juli) — verdict bersifat sementara/partial. Sejauh data ada: harga TIDAK membuat lower-low baru di dalam window (low window $61.9K pada 13 Juli vs low pre-window $58.5K pada 30 Juni) dan sudah naik ke $65.1K per 15 Juli — konsisten dengan (bukan membuktikan) klaim video, n=1 episode saja. Detail: [`findings_capitulation_fractal_falsifiability.md`](findings_capitulation_fractal_falsifiability.md)

### [INDIKATOR CUSTOM] "Bitcoin Crosby ratio" (kemungkinan mistranskripsi Coinbase Premium ratio)
- **Insight:** Rasio ini (nama tidak jelas di transcript, kemungkinan Coinbase Premium ratio) turun ke salah satu level terendah sepanjang sejarah di daily maupun weekly, sebanding cuma dengan 2018 bear low (juga disebut dekat 2012 & 2015 low). [02:12]-[02:31], [09:52]-[10:49]
- **Indikator terkait:** Kemungkinan Coinbase Premium Index — bukan bagian indikator aktif framework
- **Relevan ke:** K4 (confirming context bottom)
- **Test klaim:** Nama salah transkripsi sendiri jadi red flag kualitas ekstraksi ASR. Perbandingan "terendah sepanjang sejarah" lintas era (2012 vs sekarang) rawan menyesatkan karena struktur likuiditas/jumlah exchange sudah sangat berbeda.
- **Perlu validasi Claude Code:** Tidak berlaku — Coinbase Premium adalah data per-exchange, di luar cakupan `data_master_all_metrics.csv` (kita cuma punya agregat).

### [INDIKATOR CUSTOM] Active address sentiment indicator (proprietary Bitcoin Magazine Pro)
- **Insight:** Indikator proprietary channel — garis oranye yang cross ke atas lower deviation band, historisnya cukup sering menandai area bear market low (diakui pembicara sendiri "tidak sempurna"). [08:41]-[09:40]
- **Indikator terkait:** Kemungkinan basisnya active address on-chain diproses jadi z-score/deviation band
- **Relevan ke:** K4 (confirming signal bottom)
- **Test klaim:** Active address tidak di-track di dataset kita. Konsep "network activity sebagai sinyal bottom" mirip `apparent_demand` yang sudah diuji dua kali di project ini (versi mentah & kondisional per-zona) dan **REJECT** — hasil rapuh/kontradiktif lintas cycle. Preseden negatif yang relevan meski bukan indikator identik.
- **Perlu validasi Claude Code:** Tidak berlaku — data tidak tersedia. Catatan: preseden `apparent_demand` REJECT jadi konteks skeptis tambahan.

### [INDIKATOR CUSTOM] Bitcoin-as-%-of-global-capital bear market duration
- **Insight:** Alih-alih durasi bear dalam USD-terms (~1 tahun untuk 2 dari 4 bear terakhir), pembicara menormalisasi BTC sebagai % dari "global capital" — dua bear terakhir jadi ~367-378 hari, bear sebelumnya lebih panjang (~600 hari). Titik top juga beda tanggal dari top harga USD (14 Juli 2025 vs 6 Okt 2026 — angka dari narasi video, low confidence). [03:23]-[04:13]
- **Indikator terkait:** BTC market-cap-as-%-of-global-money-supply — normalisasi custom
- **Relevan ke:** general, berpotensi tumpang tindih konsep dengan K4 "lantai waktu"
- **Test klaim:** Sample kecil — cuma "2 bear terakhir" disebut angka konkret, sisanya samar tanpa angka, di bawah standar minimum 3 cycle framework.
- **Perlu validasi Claude Code:** Tidak berlaku — butuh data kapitalisasi pasar global lintas-aset, di luar cakupan dataset on-chain kita.

### [BARU] RSI weekly bullish divergence di bear market low
- **Insight:** Harga BTC set lower low, tapi RSI weekly set higher low (bullish divergence) — konsisten muncul di 2015 dan siklus saat ini, kecuali di 2018 (exception diakui sendiri oleh pembicara). [05:31]-[06:33]
- **Indikator terkait:** RSI (weekly) — bukan bagian indikator aktif framework
- **Relevan ke:** K4 (confirming context bottom)
- **Test klaim:** RSI tidak di-track di dataset kita. Dari ~3 kasus yang disebut (2015, 2018, sekarang), 1 sudah gagal menurut pengakuan sendiri pembicara — closer ke "kadang benar, kadang tidak" daripada pola reliable.
- **Perlu validasi Claude Code:** Tidak berlaku — RSI tidak di-track di dataset on-chain kita.

### [BARU] 50-week/100-week MA death cross menandai approx bear low
- **Insight:** Death cross MA 50-minggu/100-minggu historisnya kurang-lebih menandai area bear market low (2015, 2018-19, 2022). Proyeksi cross berikutnya: 10 Juli 2026. [04:20]-[05:31]
- **Indikator terkait:** Moving average (TA klasik) — bukan bagian framework
- **Relevan ke:** K4 (entry timing bear bottom)
- **Test klaim:** 3 cycle dasar, di batas minimum. Death cross secara struktur adalah lagging indicator — MA lambat baru cross setelah harga sudah jatuh jauh, jadi "menandai bear low" bisa cuma kebetulan timing, bukan predictive value nyata.
- **Perlu validasi Claude Code:** Ya — kolom `100_wma` tidak tersedia di dataset kita, jadi diuji pakai proxy `50_wma`/`200_wma` (bukan uji langsung klaim asli).

**[VALIDASI — 2026-07-28, CLOSED]** Kolom 100_wma tidak tersedia; diuji pakai proxy 50wma/200wma (n=1 death cross historis, 2023-02-16, terjadi 87 hari SETELAH bottom harga sebenarnya — lagging, bukan leading). Per 2026-07-15 gap 50wma/200wma masih 38.9% dan proyeksi linear mengarah ke akhir 2026/awal 2027, meleset ~6 bulan dari klaim "10 Juli 2026". Klaim tanggal spesifik tidak didukung data proxy; klaim asli 50w/100w tetap tidak bisa diverifikasi (data tidak tersedia). Detail: [`findings_ma_death_cross_falsifiability.md`](findings_ma_death_cross_falsifiability.md)

### [BARU] 200-day/365-day/200-week MA reclaim sebagai konfirmasi bull market kembali
- **Insight:** Reclaim di atas 200-day MA (~$70K saat itu) dan 365-day MA (~mid $80K) dipakai sebagai level konfirmasi keluar bear market; juga masih di bawah 200-week MA sebagai syarat tambahan. [04:24]-[04:31], [12:26]-[12:51]
- **Indikator terkait:** Moving average (TA klasik) — bukan bagian framework
- **Relevan ke:** K5/K6 transisi (analog konsep "unlock bear" di framework, tapi via MA bukan STH RP cross RP)
- **Test klaim:** Belum established di framework (framework pakai STH RP cross RP, bukan MA teknikal). Data tersedia (200_dma, 200_wma), jadi bisa diuji langsung sebagai leading/lagging proxy terhadap unlock objektif.
- **Perlu validasi Claude Code:** Ya.

**[VALIDASI — 2026-07-28, CLOSED]** n=4 episode Z1→Z2 unlock historis (2012, 2015, 2019, 2023). 200-day MA reclaim konsisten mendahului unlock STH RP/RP sekitar 23-51 hari (n=4, semua negatif/lead). 200-week MA kurang konsisten (n=3 valid, rentang -119 s/d +12 hari; 1 episode tanpa event reclaim sama sekali karena harga tak pernah turun di bawah 200wma saat crash 2018). 200dma berguna sebagai leading proxy tapi jarak lead-nya tidak konstan, tak bisa untuk timing presisi. Detail: [`findings_ma_reclaim_vs_z1z2_unlock.md`](findings_ma_reclaim_vs_z1z2_unlock.md)

### [BARU] MSTR RSI weekly bullish divergence, mirroring pola BTC
- **Insight:** MSTR (proxy ekuitas BTC) menunjukkan pola RSI divergence sama seperti BTC — lower low di harga, higher low di RSI. [06:35]-[07:00]
- **Indikator terkait:** RSI pada MSTR — bukan on-chain BTC
- **Relevan ke:** general (confirming context lintas-aset)
- **Test klaim:** "Mirroring" adalah asumsi yang butuh pembuktian terpisah, bukan given — MSTR punya noise structural sendiri (leverage, capital raise, index inclusion flows).
- **Perlu validasi Claude Code:** Tidak berlaku — harga saham MSTR + RSI di luar cakupan dataset on-chain kita.

### [BARU] MSTR sebagai leading indicator untuk top & bottom BTC
- **Insight:** MSTR historisnya memimpin BTC beberapa minggu di top maupun bottom siklus (contoh: MSTR rally besar 30 Des sementara BTC breakout baru mid-Januari; MSTR topped out Feb 2025 vs BTC ATH beberapa bulan kemudian). [07:02]-[07:52]
- **Indikator terkait:** MSTR price action sebagai proxy sentimen risk-on/off
- **Relevan ke:** K1 (top warning) & K4 (bottom warning), general
- **Test klaim:** Butuh data harga MSTR historis, tidak ada di dataset kita. Klaim "leading beberapa minggu" rawan lookahead-bias kalau diuji tanpa disiplin at-gate.
- **Perlu validasi Claude Code:** Tidak berlaku — data harga saham MSTR di luar cakupan dataset on-chain.

### [BARU] MSTR NAV premium (enterprise-value based) turun di bawah 1
- **Insight:** mNAV MSTR (dari enterprise value: market cap + preferred + debt − cash, dibagi kepemilikan BTC) baru-baru ini turun di bawah 1.0 — "membeli $1 BTC dengan kurang dari $1". [08:01]-[08:37]
- **Indikator terkait:** MSTR mNAV — bukan on-chain BTC metric
- **Relevan ke:** general (proxy valuasi lintas-aset)
- **Test klaim:** Butuh data korporat MSTR (EV, holdings, market cap), sepenuhnya di luar cakupan dataset. Risiko tambahan (dilusi saham, capital raise, kebijakan treasury) tidak berkorelasi langsung dengan siklus on-chain.
- **Perlu validasi Claude Code:** Tidak berlaku — data korporat MSTR di luar cakupan dataset.

### [BARU] Production cost sebagai valuation floor
- **Insight:** BTC saat ini diperdagangkan di bawah "production cost" (biaya produksi/mining) — kejadian langka historis, semua contoh sebelumnya persis menandai bear market low. Disinggung sekilas, tanpa metodologi jelas. [10:49]-[11:15]
- **Indikator terkait:** Cost-of-production model (mis. hashrate/energy-based) — metodologi tidak dijelaskan
- **Relevan ke:** K4 (analog semangat CVDD di framework, tapi metrik beda basis)
- **Test klaim:** Miner metrics tidak di-track di dataset. Bahkan andai data ada, klaim sendiri tidak cukup terspesifikasi untuk diuji (model biaya mana: all-in cost rata-rata, marginal miner, atau cost curve tertentu?).
- **Perlu validasi Claude Code:** Tidak berlaku — data tidak tersedia dan klaim tidak punya metodologi jelas.

### [BARU] Rally cepat pasca-bottom (historically ~100 hari)
- **Insight:** Di 3 bear market terakhir, begitu bottom terkonfirmasi, harga BTC naik signifikan dalam waktu relatif singkat (~100 hari): Des 2022 ($15-16K→$30K), siklus sebelumnya ($3K→~$14K, +250%), siklus sebelumnya lagi ($230→$460+). [12:56]-[13:40]
- **Indikator terkait:** Price momentum pasca-low, historical rate-of-recovery
- **Relevan ke:** K4→K5 transisi (urgency deploy), general
- **Test klaim:** Dasar cuma 3 cycle, definisi "bottom start" tidak presisi di video (dipilih hindsight). Perbandingan % kenaikan lintas era rawan misleading karena base harga sangat kecil di era awal.
- **Perlu validasi Claude Code:** Ya — pakai definisi bottom objektif (Z1→Z2 unlock), bukan definisi subjektif video.

**[VALIDASI — 2026-07-28, CLOSED]** n=4 episode Z1→Z2 unlock historis (bottom didefinisikan objektif, bukan hindsight seperti di video). Kecepatan rally sangat bervariasi: hari ke +50% berkisar 19-233 hari, hari ke +100% berkisar 50-414 hari; episode 2015 bahkan masih -6.5% di hari ke-100. Klaim "~100 hari" TIDAK konsisten lintas cycle — hasil negatif yang valid, kemungkinan besar produk cherry-picking 3 contoh anekdotal di video dengan tanggal bottom yang dipilih hindsight. Detail: [`findings_post_bottom_rally_speed.md`](findings_post_bottom_rally_speed.md)

### [KONFIRMASI] Skeptisisme terhadap narasi durasi bear "selalu ~1 tahun"
- **Insight:** Pembicara secara eksplisit mengkritik narasi umum "bear market selalu ~1 tahun" — hanya 2 dari 4 bear market terakhir yang benar-benar sekitar 1 tahun, dan itu pun cuma dalam USD-terms. Pembicara sendiri menyebut argumen seasonality "dubious... considering we have such a small sample size". [02:59]-[03:23], [11:15]-[12:16]
- **Indikator terkait:** general (durasi bear market / seasonality)
- **Relevan ke:** general — selaras dengan prinsip framework sendiri soal skeptisisme sample kecil dan threshold non-absolut
- **Test klaim:** Sudah established di framework (K4 "lantai waktu" pakai ambang relatif ≥9 bulan sejak peak, bukan "1 tahun tetap").
- **Perlu validasi Claude Code:** Tidak — sudah established, tidak perlu diuji ulang.

### [STRATEGI] Confluence-based bottom-calling → scaling in sekarang meski belum ada konfirmasi presisi
- **Insight:** Pendekatan investasi pembicara: gabungkan banyak sinyal lintas-kategori (time-capitulation fractal, RSI, MA death cross, MSTR + NAV premium, active address, production cost) — kalau semuanya "confluence" mengarah ke exhaustion downside, itu cukup jadi dasar untuk mulai scaling in walau tidak tahu tanggal bottom presisinya. Bukan zone-based/K-node — murni confluence multi-indikator TA + on-chain sederhana. [11:48]-[12:26], [13:50]
- **Indikator terkait:** Kombinasi semua indikator di atas (bukan satu indikator tunggal)
- **Relevan ke:** general — pendekatan alternatif untuk K4 (akumulasi bear bottom), berbeda struktur dari gate/veto framework
- **Test klaim:** Strategi ini menggabungkan sinyal TA klasik, proxy equity, day-count fractal kalender, dan production cost sebagai "confluence" tanpa struktur gate/veto, tanpa zone-based sequencing, dan tanpa disiplin hard LTV limit — beda fundamental secara arsitektur dari cara framework bekerja. Falsifiability lemah: "confluence banyak sinyal" gampang dirasionalisasi retroaktif; kalau sebagian benar sebagian salah, strategi tetap bisa diklaim "berhasil" tanpa kriteria gagal yang jelas.
- **Perlu validasi Claude Code:** Tidak — ini soal perbedaan filosofi pengambilan keputusan, bukan yang bisa dites numerik. Dilaporkan sebagai flag STOP ke Yudi di chat sebelum Stage 3; keputusan: catat saja di sini, tidak ada tindak lanjut lebih lanjut untuk saat ini.

---

## Flag Prioritas

1. **200-day MA reclaim sebagai leading proxy terhadap unlock Z1→Z2 (n=4, lead konsisten 23-51 hari)** — satu-satunya insight tervalidasi dari video ini yang punya sinyal cukup konsisten (walau n kecil) untuk dipertimbangkan sebagai confirming context tambahan di K-node terkait exit bear, meski bukan pengganti STH RP cross RP.
2. **Rally ~100 hari pasca-bottom: hasil negatif kuat (t100 berkisar 50-414 hari, n=4)** — bagus untuk arsip sebagai counter-narrative kalau ada sumber lain mengklaim "kecepatan rally pasca-bottom" yang serupa di masa depan.
3. **Prediksi tanggal spesifik (12 Juli capitulation fractal, 10 Juli MA death cross) — keduanya perlu dicek ulang dengan data lebih lengkap** setelah `data_master_all_metrics.csv` di-update melewati 2026-07-19, karena validasi sekarang masih partial/proxy.

---

## Yang Langsung Diabaikan

- RSI (daily & weekly), MSTR RSI, MSTR sebagai leading indicator, MSTR NAV premium, active address sentiment indicator, "Bitcoin Crosby/Coinbase ratio", production cost floor, BTC-as-%-global-capital duration — semuanya tidak bisa divalidasi karena datanya di luar cakupan `data_master_all_metrics.csv` (bukan on-chain BTC metric, atau data per-exchange/korporat yang tidak kita track). Dicatat di bucket masing-masing di atas sebagai backlog konseptual, tapi tidak actionable untuk pipeline validasi ini.
