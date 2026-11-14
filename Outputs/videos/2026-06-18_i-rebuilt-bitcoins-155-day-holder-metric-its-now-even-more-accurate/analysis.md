# I Rebuilt Bitcoin's 155-Day Holder Metric: It's Now Even More Accurate
**Channel:** Bitcoin Magazine Pro (host: Matt Crosby)
**Tanggal video:** 2026-06-18
**Tanggal analisis:** 2026-07-30
**Link:** https://www.youtube.com/watch?v=4QYJCJyoAyQ

---

## 🚩 FLAG — STOP DAN LAPOR

**Ajakan mengganti boundary cohort LTH secara wholesale (155 hari statis → 114 hari dinamis).** Ini masuk butir 2 "KAPAN HARUS STOP DAN LAPOR" — basis definisi yang fundamental berbeda dengan pendekatan yang ada, bukan penambahan sinyal. Kalau diadopsi, yang berubah basisnya: `sth_cost_basis` & `lth_cost_basis` (Zone Dimensi 1 → seluruh label zona), `sth_mvrv` (K1 #3, K2 gate 0,80–0,97), `lth_mvrv` (K4 kondisi 1), `lth_sopr` (K4 kondisi 2), `sth_sopr` MA90/MA60 (alarm bear #2, trigger K1, K1 #4), `pct_sth_in_profit`/`pct_lth_in_profit` (K1 #5, K2 veto 1&2, K4 kondisi 3). Bentrok dengan § Governance butir 2 (framework dibekukan per siklus) dan butir 3.

**Sudah divalidasi — dampaknya AKADEMIS, bukan konflik serius.** Bracket HODL-wave menunjukkan geseran boundary hanya mengubah **0,49% label struktur Zone Dimensi 1** (24 dari 4.944 hari) dan tanggal trigger Z2 bergeser 0–6 hari di 4 dari 5 episode. Alasannya: deviasi LTH RP besar di euforia (+18,1% saat MVRV>2,5) tapi hampir nol di bear (+1,3% saat MVRV<1) — dan justru di bear-lah LTH RP dipakai framework kita. Detail: [`findings_lth_rp_boundary_sensitivity.md`](findings_lth_rp_boundary_sensitivity.md)

**Rekomendasi:** tolak adopsi basis kohort, ambil hanya metodologi normalisasinya. Tiga hal yang memperkuat: (1) **Matt sendiri tidak melakukannya** — di papernya dia pertahankan static-155 sebagai supply classifier, 114 hanya propensity diagnostic; (2) angka 114 tidak unik ("re-derivation does not uniquely pin the number"); (3) caveat n=3 ditulis penulisnya sendiri.

**Tidak ada konflik dengan hard constraint LTV** — video tidak membahas leverage sama sekali.

**Temuan sampingan yang lebih penting dari video ini** (internal framework, bukan dari video): leg `aSOPR < 0,93 selama ≥7 hari berturut` di **K4 kondisi 2 tidak pernah terpenuhi satu kali pun** di 5.843 hari data — streak terpanjang 6 hari (Sep 2011). Kondisi 2 K4 mati secara mekanis, setara temuan "kondisi #1 K2 lama mati". Penempelannya dikerjakan di project Onchain-Dashboard.

---

## Ringkasan

Video 16 menit dari Matt Crosby (Bitcoin Magazine Pro) yang mempresentasikan research paper pertamanya: rekonstruksi ulang boundary long-term holder. Argumen dasarnya — angka **155 hari** yang dipakai seluruh industri sejak Maret 2020 berasal dari satu riset Glassnode di titik waktu tertentu, dan Bitcoin sudah berubah banyak sejak itu (active addresses turun, ETF & treasury company memegang tanpa batas waktu). Dia menghitung ulang boundary sebagai umur pertama di mana 14-day forward spend probability turun di bawah threshold q* dan bertahan 14 hari berturut, dengan lookback rolling 4 tahun — hasilnya **114 hari per 16 Jun 2026, 27% lebih rendah**.

Papernya menunjukkan boundary ini tidak pernah konstan: ~105–120 hari sepanjang 2013–2018, melonjak ke 150–231 hari pada 2018–2022 (puncak 231 di Des 2021), lalu kembali ke 114. Kesimpulan Matt sendiri: **"155-day constant" itu fitur dari episode 2018–2022, bukan level run-on** — dan 114 hari sekarang adalah kembali ke band pre-episode, bukan fenomena yang diciptakan ETF.

Di luar boundary, ada tiga kontribusi lain: (1) **filtered realized price** — RP setelah membuang coinbase, dust, OP_RETURN, dan inscriptions, dengan aturan pemakaian per-metrik yang eksplisit di Table 1; (2) **metodologi trailing-Z → historical quantile** yang mengubah LTH-SOPR dan STH-MVRV jadi seri bounded 0–1; (3) **quantile band rolling 4 tahun** di sekitar filtered RP sebagai koridor harga — analog fungsional AVIV Mean/Upper di framework kita. Market call-nya: harga ~$65k = persentil ~20 dari regime 4-tahun, LTH-SOPR quantile di 0,6th percentile, "clearly in deep value territory".

Yang membedakan video ini dari sumber lain di korpus kita: **semua formula, filter, dan chart dipublikasi terbuka** di mattcrosby.pro, dan penulisnya menulis caveat-nya sendiri dengan jujur (n=3, base normalisasi drift, angka 114 tidak unik, dan dia sendiri memilih tidak mengadopsi 114 sebagai supply classifier). Ironisnya caveat-caveat itu justru bagian paling berguna dari videonya — dan empat validasi yang kami jalankan di bawah cenderung mendukung sikap hati-hati penulisnya sendiri, bukan klaim positifnya.

---

## Insight Inventory

### [BARU] Dynamic LTH boundary 114 hari (rolling 4 tahun) menggantikan static 155
- **Insight:** Boundary dihitung ulang **harian** = umur pertama di mana smoothed 14-day forward spend probability turun di bawah q* dan bertahan di bawahnya 14 hari berturut, lookback 1.460 hari. Per 16 Jun 2026 = **114 hari, 27% lebih rendah** dari static 155. `[04:43]`–`[05:05]`, `[15:10]`; metodologi §4.2 paper di Lampiran `[02:03]`, Figure 1 di `[02:35]`
- **Indikator terkait:** definisi cohort LTH/STH — dasar dari LTH-MVRV, STH-MVRV, LTH-SOPR, STH-SOPR, LTH/STH RP, Supply in Profit LTH/STH, LTH/STH-NUPL
- **Relevan ke:** SEMUA — Zone Dimensi 1, K1 #3, K2 gate valuasi, K4 kondisi 1 & 2, K5 unlock
- **Test klaim:** Basis empirisnya panjang (2013–2026, ~4 cycle) jadi bukan soal sample size — masalahnya boundary ini **non-stationary by design** (105 → 231 → 114). Metrik yang dibangun di atas basis yang definisinya berubah harian kehilangan komparabilitas lintas-cycle, yang justru pondasi cara framework membaca pola relatif. Ada juga endogeneity: boundary naik persis di bull peak, artinya definisi berubah di titik yang mau diukur. Titik lemah paling tajam: **penulis sendiri tidak mengadopsinya** sebagai supply classifier.
- **Perlu validasi Claude Code:** Tidak — tidak feasible, butuh raw UTXO (hazard per umur koin tidak ada di dataset; HODL wave paling halus `3m-6m` menelan 114 maupun 155). Dampaknya diuji lewat proxy — lihat insight LTH RP di bawah.

### [BARU] Mekanisme: seluruh kurva spend-probability turun, bukan cohort-nya yang berubah
- **Insight:** Boundary turun bukan karena orang memegang lebih sebentar, tapi karena seluruh kurva spend probability turun — level propensity sama tercapai di umur koin lebih muda. Penyebab yang disebut: active addresses turun (Bitcoin makin sedikit dipakai sebagai P2P cash), ETF + treasury companies hold indefinitely. `[00:46]`–`[01:08]`, `[05:27]`; Figure 1 caption di Lampiran `[02:35]`
- **Indikator terkait:** spend probability / hazard rate, active addresses, ETF flow
- **Relevan ke:** general — asumsi struktural di balik semua metrik cohort
- **Test klaim:** Penjelasan mekanistiknya plausibel dan konsisten arah dengan `liveliness` yang kita punya, tapi **penyebabnya narasi kausal tanpa uji** — active addresses dan ETF flow dua-duanya eksplisit tidak ada di dataset kita. Klaim ini salah kalau turunnya kurva ternyata artefak komposisi (custodial/exchange consolidation memindahkan koin ke sedikit UTXO besar yang jarang gerak) alih-alih perubahan perilaku holder.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia.

### [KONFIRMASI] Angka 155 hari memang arbitrary dan pernah bergerak jauh
- **Insight:** Boundary ~105–120 hari sepanjang 2013–2018, melonjak ke band 150–231 pada 2018–2022 (**puncak 231 hari, Des 2021**), balik ke 114 di 2026. Penulis: "155-day constant" itu fitur episode 2018–2022 spesifik, bukan level run-on (p ≤ 0,04), dan 114 sekarang = kembali ke band pre-episode, bukan fenomena ETF. Lampiran §6.1 `[04:14]`; Figure 2 `[05:19]`–`[06:25]`
- **Indikator terkait:** LTH/STH boundary
- **Relevan ke:** general — mengkonfirmasi tiga catatan yang sudah ada di KB kita sendiri: `Price_Level KB` §6 ("definisi 155-hari arbitrary, bisa berubah oleh provider"), `nupl KB` baris 723, `sopr KB` baris 826
- **Test klaim:** Konfirmasi yang sehat, tapi perhatikan ironi struktural: **kalau 155 arbitrary, 114 juga arbitrary** (penulis mengakuinya sendiri) — jadi ini menguatkan prinsipnya, bukan angka penggantinya. Titik lemah: klaim p ≤ 0,04 diuji pada seri yang sangat autokorelasi (boundary harian bergerak lambat), jadi effective sample jauh lebih kecil dari jumlah harinya — p-value seperti ini cenderung terlalu optimis.
- **Perlu validasi Claude Code:** Tidak — sudah established sebagai prinsip framework.

### [BARU] Penulis sendiri menolak 114 sebagai supply classifier — hanya propensity diagnostic
- **Insight:** Di §6 (Figure 3) penulis menyimpulkan: **baca boundary 114-hari sebagai propensity diagnostic, pertahankan static-155 sebagai supply classifier yang konservatif**. Alasannya: gap dormant supply share (dynamic 85,07% vs static-155 82,7%) itu sebagian efek definisi + sebagian supply ageing — boundary lebih rendah secara mekanis mereklasifikasi lebih banyak koin jadi dormant. Pada definisi static-155, share sekarang "roughly tied with 2024 rather than a clear record". Lampiran Figure 3 `[07:14]`–`[07:47]`
- **Indikator terkait:** Supply in Profit LTH, LTH supply share
- **Relevan ke:** K1 #5 (Supply in Profit >90% dan mulai turun), K4 kondisi 3
- **Test klaim:** Ini insight paling penting di seluruh video untuk keputusan kita, dan ironisnya bukan klaim positif melainkan pembatasan diri penulis. Efeknya **mendefuse flag STOP** — kita tidak menolak sesuatu yang penulisnya anjurkan; dia sendiri memakai 155 untuk klasifikasi supply. Konsekuensi langsung: K1 #5 dan K4 kondisi 3 tidak perlu disentuh. Klaim ini "salah" hanya kalau dia mengubah posisi ke depan.
- **Perlu validasi Claude Code:** Tidak — pernyataan metodologis, bukan klaim empiris. Wajib dikutip sebagai penyeimbang flag STOP.

### [BARU] Angka 114 tidak unik — q* dikalibrasi ke satu tanggal Glassnode 2020
- **Insight:** Threshold q* = **3,0% per 14 hari** dipilih supaya konstruksi mereproduksi tanggal kalibrasi Glassnode Maret 2020 — dan hasilnya pun meleset (**157 hari**, bukan 155; penulis mengaku "a couple days off"). Heading di bawah Figure 1: "**re-derivation does not uniquely pin the number**". `[02:03]`, Figure 1 `[02:35]`, `[01:56]`–`[02:20]`
- **Indikator terkait:** LTH boundary, hazard estimation
- **Relevan ke:** general — robustness parameter
- **Test klaim:** Ini pengakuan overfitting-lite yang jujur: seluruh angka 114 adalah fungsi dari **satu free parameter yang di-anchor ke satu tanggal tunggal** — satu titik kalibrasi, bukan tiga cycle. Menyentuh STANDAR VALIDASI butir 6 langsung. Klaim ini rapuh kalau sensitivity q* ±0,5pp menggeser boundary lebih dari ~15 hari — dan paper tidak menunjukkan itu di frame yang kita punya.
- **Perlu validasi Claude Code:** Tidak — tidak feasible, butuh raw UTXO untuk mereproduksi sensitivity q*.

### [BARU] Window 1.460 hari tidak terisi penuh sebelum 2014
- **Insight:** Penulis flag sendiri bahwa rolling window 1.460 hari tidak bisa terisi penuh untuk ~4 tahun pertama sejak genesis; nilai 2012–2013 jalan di window lebih pendek dan ditandai **window-truncated**. Band baru established di window terisi penuh **dari 2014 ke depan**. Lampiran §6.1 `[04:14]`
- **Indikator terkait:** dormancy boundary
- **Relevan ke:** general — batas sampel historis
- **Test klaim:** Disclosure metodologis yang benar dan menaikkan kredibilitas penulis. Konsekuensi praktis: klaim "band ~105–120 hari sepanjang 2013–2018" sebagian bersandar pada periode truncated, jadi bukti "155 adalah anomali episode" efektif berbasis **2014 ke atas saja** — memangkas cycle 2011–2013 dari sample. Efektif ~3 cycle, tepat di batas minimum framework.
- **Perlu validasi Claude Code:** Tidak — caveat konstruksi, bukan klaim pasar.

### [BARU] Metodologi Glassnode tidak sepenuhnya publik (entity adjustment)
- **Insight:** Penulis gagal mereplikasi persis angka Glassnode karena "a lot of entity adjustment going on and some peculiarities in their methodology, which wasn't made entirely publicly available"; revisit 2024 juga "their exact methodology is hidden". Dia anchor ke publikasi 2020 dan bekerja mundur dengan formula publik. `[01:56]`–`[02:20]`, `[02:43]`, `[14:22]`
- **Indikator terkait:** semua metrik cohort dari Glassnode/ChartInspect
- **Relevan ke:** general — provenance data framework
- **Test klaim:** Catatan permanen untuk pipeline kita, bukan insight pasar: data kohort yang kita pakai mengandung entity adjustment yang tidak bisa direplikasi, jadi **setiap perbandingan angka Matt vs angka kita punya floor error yang tidak bisa dihilangkan**. Relevan langsung ke aturan "angka dari frame = low confidence" — bukan cuma karena resolusi, tapi karena base-nya beda.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia.

### [BARU] Boundary ULTH bergerak berlawanan arah — distribusi holder membentuk "barbell"
- **Insight:** Ultra-long-term holder threshold (spend probability 3% → ~0,3%, butuh 4+ tahun) **NAIK dari 1.480 hari (2020) ke 1.686 hari (2026)** — arah berlawanan dengan LTH boundary yang turun 157→114. Penulis menyatakan ini bukan artefak estimation window. `[02:20]`–`[02:43]`; Figure 1 panel kanan `[02:35]`; §6.1 `[04:14]`
- **Indikator terkait:** ULTH boundary, dormancy
- **Relevan ke:** general — struktur holder base
- **Test klaim:** Pengamatan menarik dan internally consistent (polarisasi), tapi tidak actionable: tidak ada K-node yang beroperasi di horizon 4+ tahun. Titik lemah: arah berlawanan bisa sebagian mekanis — kalau lebih banyak koin diklasifikasi dormant lebih cepat, tail distribusi umur otomatis memanjang. Bukti pembanding penulis tidak terlihat di frame.
- **Perlu validasi Claude Code:** Tidak — tidak feasible, butuh raw UTXO.

### [BARU] Pemisahan "long-term holder" vs "long-term spender": Q(0.90) = 213 hari (ATH)
- **Insight:** Selain dormancy boundary, penulis membuat **Q(0.90) spending boundary** = titik di mana 90% transaksi yang akan pernah terjadi sudah terjadi. Nilainya **213 hari (expanding, all-time high)** dan **329 hari (rolling)**. Bergerak **inverse** terhadap dormancy boundary. Argumennya: banyak BTC di address LTH mungkin tidak akan pernah dibelanjakan lagi. `[05:49]`–`[06:37]`; Figure 2 `[05:19]`–`[06:25]`
- **Indikator terkait:** spending boundary, spend velocity, dormancy
- **Relevan ke:** general — belum ada padanan di framework
- **Test klaim:** Konsepnya menarik tapi belum ada klaim actionable yang menyertainya — penulis cuma menunjukkan inverse correlation dengan dormancy boundary, yang sebagian **tautologis** (dua-duanya turunan dari kurva hazard yang sama; kalau kurva turun serentak, satu quantile naik dan satunya turun secara mekanis). Supaya jadi insight sungguhan dia harus menunjukkan Q(0.90) memprediksi sesuatu yang dormancy boundary tidak — itu tidak ditunjukkan.
- **Perlu validasi Claude Code:** Tidak — tidak feasible, butuh raw UTXO.

### [BARU] Metrik dinamis menandai distribusi LTH di puncak 2021 lebih tajam daripada static-155
- **Insight:** Saat peak 2021, dormant supply share versi dinamis drop signifikan lebih dalam daripada garis static-155, karena boundary saat itu naik ke 231 hari. Klaim: definisi dinamis lebih reaktif menandai fase distribusi LTH di puncak siklus. `[07:24]`–`[07:46]`; Figure 3 `[07:14]`
- **Indikator terkait:** LTH supply share, Supply in Profit LTH
- **Relevan ke:** K1 (sinyal distribusi di puncak), K3
- **Test klaim:** **Confounded by construction** — boundary dinamis naik ke 231 hari persis di Des 2021, jadi drop yang lebih tajam itu sebagian efek reklasifikasi, bukan sinyal distribusi yang lebih jelas. Penulis sendiri sudah memakai logika ini untuk gap dormant share di insight sebelumnya; seharusnya berlaku juga di sini. **n = 1 peak (2021)** untuk klaim spesifiknya.
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog. Versi dinamis tidak feasible; proxy age-band (share supply ≥3m vs ≥6m di sekitar peak 2021 & Okt 2025) feasible via HODL waves tapi menjawab pertanyaan berbeda. Prioritas rendah karena K1/K3 sedang tidak aktif.

### [BARU] Divergensi LTH velocity vs liveliness sejak pertengahan 2024
- **Insight:** LTH velocity turun ke **0,0788% per hari** pada filtered base — deep di lower tail, first drawdown of its magnitude. **Tapi liveliness justru NAIK sejak pertengahan 2024.** Penjelasan penulis: velocity didominasi rare ancient movements, liveliness age-weighted. Lampiran Figure 3 `[07:14]`–`[07:47]`; `[08:09]`
- **Indikator terkait:** LTH velocity, liveliness, dormancy
- **Relevan ke:** general — belum ada di framework
- **Test klaim:** Kita punya `liveliness` tapi **tidak punya "LTH velocity" versi Matt** (butuh basis filtered/dynamic). Penjelasannya hampir tautologis dari definisi kedua metrik — jadi divergensinya cenderung artefak konstruksi, mirip verdict preseden `findings_mvrv_rolling1y_vs_aviv.md` ("artefak struktural dari perbedaan reaktivitas formula"). Nilai marginal rendah.
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog, prioritas rendah. Proxy terdekat: `cdd` / `vdd_multiple` vs `liveliness`.

### [INDIKATOR CUSTOM] Filtered Realized Price (flt) — RP setelah buang coinbase, dust, unspendable, inscriptions
- **Insight:** RP standar dianggap tidak merepresentasikan cost basis sesungguhnya karena mencampur: **block coinbase** (bukan transaksi, dan berisiko double-count saat miner memindahkannya), **dust** (UTXO yang biaya kirimnya melebihi nilainya), **OP_RETURN / zero-value** (provably unspendable), dan **inscriptions/ordinals** sejak 2023. Hasil: filtered RP sedikit **lebih tinggi** dari RP standar. Reading di video: RP(flt) $58.468 vs harga $65.610 (**low confidence dari resolusi frame**). `[03:06]`–`[04:19]`, `[08:09]`–`[08:54]`
- **Indikator terkait:** Realized Price, Realized Cap, LTH RP, STH RP
- **Relevan ke:** **Zone Structure v2** — RP adalah batas ZC/ZD, STH RP batas ZD/Z3. Geser RP = geser zona.
- **Test klaim:** Dekomposisinya jelas: flt = RP standar minus coinbase minus dust, di atas Tier 0 yang dibuang di kedua base. Arah hasilnya (flt > std) adalah **konsekuensi aritmatika dari filter**, bukan temuan — coinbase output adalah koin tertua dengan cost basis mendekati nol, membuangnya menaikkan rata-rata. Yang penting buat kita bukan angka $58.468 (base beda, tidak comparable) tapi magnitudonya: RP adalah batas ZC/ZD, jadi geseran beberapa persen menggeser label zona di hari-hari batas.
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog. Uji sensitivitas label zona terhadap perturbasi RP (+2%/+5%/+10%): berapa persen hari berpindah antara ZC dan ZD, dan apakah tanggal trigger lantai waktu K4 bergeser >7 hari. Sebagian terjawab lewat validasi quantile band di bawah (band = `quantile(P/RP) × RP`, invarian terhadap penskalaan RP).

### [INDIKATOR CUSTOM] Table 1 — tiga tier eksklusi dengan aturan pemakaian per-metrik
- **Insight:** **Tier 0** (selalu dibuang di std maupun flt) = zero-value output & OP_RETURN, provably unspendable. **std** = semua spendable UTXO, coinbase & dust dipertahankan → untuk supply, realized price/cap, angka yang comparable eksternal. **flt** = std minus coinbase, minus dust by output type (≤546 sats pubkeyhash/pubkey/other; ≤540 scripthash; ≤294 witness_v0_keyhash; ≤330 witness_v0_scripthash & taproot) → untuk SOPR, spending thresholds, valuation bands, behavioural boundary. Lampiran Table 1 `[12:26]`
- **Indikator terkait:** semua — ini aturan base data
- **Relevan ke:** general
- **Test klaim:** Disiplin metodologis yang bagus, dan konsekuensinya harus dicatat keras: **angka flt tidak comparable dengan angka vendor manapun**, termasuk data kita. Setiap angka Matt yang berbasis flt (RP flt, LTH-RP dinamis, quantile band, LTH-SOPR quantile, STH-MVRV quantile) tidak boleh dipakai sebagai anchor level di framework kita — hanya metodologinya yang bisa dipinjam. Titik lemah kecil: threshold dust hard-coded (546/540/294/330 sats) adalah aturan relay Bitcoin Core **saat ini** yang diterapkan mundur ke seluruh sejarah — anakronistik untuk era awal.
- **Perlu validasi Claude Code:** Tidak — definisi metodologi. Tapi jadikan aturan baca permanen: semua angka flt = tidak comparable dengan dataset kita.

### [KONFIRMASI] Implementasi mereproduksi referensi publik dalam 0,2% lintas tiga market era
- **Insight:** Teks di atas Table 1: implementasi mereka mereproduksi realized price / cohort supply / realized cap referensi publik **dalam 0,2% lintas tiga market era**. Lampiran `[12:26]`
- **Indikator terkait:** Realized Price, Realized Cap, cohort supply
- **Relevan ke:** general — prasyarat sebelum angka apapun dari paper bisa dibandingkan ke dataset kita
- **Test klaim:** Kontrol kualitas yang benar dan meningkatkan kepercayaan pada base **std** miliknya. Tapi 0,2% itu untuk base std, **bukan** untuk flt maupun boundary dinamis — jadi tidak boleh dibaca sebagai validasi klaim utama video. Tidak bisa diverifikasi independen tanpa akses kode penuh. Catatan: validasi kami menemukan `lth_cost_basis` vendor kita ($49.445 per 2026-06-16) praktis identik dengan angka static-155 Matt ($49.434, beda 0,02%) — bukti tidak langsung bahwa base std-nya memang sepadan.
- **Perlu validasi Claude Code:** Tidak — verifikasi implementasi pihak ketiga.

### [BARU] LTH Realized Price dinamis 13,9% di atas versi static-155
- **Insight:** Figure 5: **LTH-RP dinamis (iso 1460d) $56.290** vs **LTH-RP static-155 $49.434** — dynamic cost basis duduk **13,9% lebih tinggi**. Penyebabnya boundary lebih rendah menarik lebih banyak koin (cost basis lebih tinggi/lebih baru) ke cohort LTH; filtered base juga membuang coinbase/dust yang terkonsentrasi di supply paling tua. Lampiran Figure 5 `[08:53]`–`[09:09]`
- **Indikator terkait:** LTH Realized Price, LTH-MVRV
- **Relevan ke:** **Zone Dimensi 1** — struktur C (Konvergen) mensyaratkan jarak STH RP–RP **dan** RP–LTH RP dua-duanya < 2%. Geseran 13,9% mengubah kapan struktur C terdeteksi → menyentuh trigger Z2 dan awal K5.
- **Test klaim:** Ini insight paling relevan struktural sekaligus paling rapuh: 13,9% itu **campuran dua efek** — geser boundary (155→114) DAN pindah base (std→flt) — dan penulis tidak memisahkannya. Kita tidak tahu berapa yang murni efek boundary.
- **Perlu validasi Claude Code:** Ya — sudah diuji sebagai upper-bound proxy lewat HODL waves.

**[VALIDASI — 2026-07-30, CLOSED]** Klaim +13,9% **tidak reproduce dari geseran boundary saja**: di tanggal yang sama (2026-06-16), `LTH_RP(≥3m, ~91d)` cuma **+3,2%** di atas vendor 155d, dan bracket penuh 91d–182d hanya **6,4%** — padahal 91 hari lebih ekstrem dari 114. Sisa gap cenderung datang dari konstruksi "iso 1460d" dan/atau base flt, bukan geseran boundary. Dampak ke framework kecil: label struktur Zone Dimensi 1 berubah hanya **0,49%** hari (24 dari 4.944) untuk ≥3m dan **0,26%** untuk ≥6m; tanggal trigger Z2 bergeser 0–6 hari di 4 dari 5 episode (satu outlier +102 hari, Jan 2019); cross-up STH RP>RP tidak terpengaruh sama sekali. **n = 4.944 hari, 5 cycle; perubahan label terkonsentrasi di 2019-21 (20 dari 24 hari).** Catatan batasan: 114 dan 155 dua-duanya di dalam band `3m-6m`, jadi ini upper bound, bukan replikasi.
Detail: [`findings_lth_rp_boundary_sensitivity.md`](findings_lth_rp_boundary_sensitivity.md)

### [INDIKATOR CUSTOM] Trailing-Z → historical quantile sebagai normalisasi umum (bounded 0–1)
- **Insight:** Metodologi generik: ambil metrik → ubah jadi **trailing Z-score** (rolling 1.460 hari) → petakan ke **persentil historisnya** → seri bounded 0–1. Tujuan eksplisit: "I wanted the highs and lows to be in a much closer cluster, a much tighter range". Diterapkan ke LTH-SOPR (Figure 7) dan STH-MVRV (Figure 10). `[04:43]`–`[05:05]`, `[09:18]`–`[09:41]`
- **Indikator terkait:** metodologi — bisa ditempel ke metrik apapun
- **Relevan ke:** general — bersinggungan langsung dengan prinsip inti framework ("threshold absolut tidak reliable antar cycle, pakai pola relatif")
- **Test klaim:** Ini **bukan indikator baru**, ini transformasi dua tahap (rolling standardization → rank/percentile mapping) yang bisa ditempelkan ke metrik apapun yang sudah kita punya — jadi bisa diuji penuh dengan data sendiri, tanpa perlu base flt. Titik lemah struktural: quantile mapping **membuang informasi magnitudo** — "0,6th percentile" tidak membedakan capitulation ringan dari ekstrem. Preseden CLOSED (`findings_mvrv_rolling1y_vs_aviv.md`) sudah mengajari satu pelajaran yang berlaku di sini: skala antar metode tidak setara, jadi percentile Matt tidak boleh disamakan dengan percentile hitungan kita.
- **Perlu validasi Claude Code:** Ya — diuji lewat penerapan konkretnya di dua insight berikut, bukan secara abstrak.

### [BARU] LTH-SOPR trailing-Z quantile mengklaim menandai top & bottom siklus
- **Insight:** Klaim: seri ini "absolutely nailed the Bitcoin tops and bottoms pretty much to perfection", dan **setiap bear market bottom termasuk COVID dip** jatuh ke lower quantile. Zona hijau >~0,8, merah <~0,1. Reading saat video: **0,6th percentile, "among the most oversold on record"**. `[09:18]`–`[10:07]`; Figure 7 `[09:25]`–`[09:58]`
- **Indikator terkait:** LTH-SOPR
- **Relevan ke:** **K4 kondisi 2** (aSOPR <0,93 ≥7 hari DAN LTH-SOPR <0,50) — kandidat pengganti threshold absolut. Juga jalur K4-tanpa-Z1 (kasus COVID 2020).
- **Test klaim:** Klaim "to perfection" adalah klaim **visual tanpa definisi event, tanpa n**, dan penulisnya sendiri mengoreksinya dua kalimat kemudian (lihat insight berikutnya) — jadi sudah overstated by the speaker's own testimony. Yang tetap berharga: sisi bottom-nya menyentuh threshold absolut `LTH-SOPR < 0,50`, persis jenis threshold yang framework curigai. Klaim ini salah kalau versi quantile tidak memberi lead time / presisi lebih baik, atau nyala di terlalu banyak hari non-bottom. n = 4–5 bear bottom, tepat di batas minimum.
- **Perlu validasi Claude Code:** Ya — sudah diuji, prioritas tertinggi (K4 aktif).

**[VALIDASI — 2026-07-30, CLOSED]** Diuji di data kita (base std + 155d, bukan base flt Matt — yang diuji metodologinya, bukan angkanya). Versi quantile menangkap **4/4 bear bottom vs 2/4** untuk `lth_sopr<0,50`, tapi harganya mahal: nyala **18,3% hari** (vs 2,5%), whipsaw (6,3% jendela 30-hari memuat q<0,10 dan q>0,90 sekaligus), dan **41% labelnya berubah** tergantung expanding vs full-history percentile — "COVID ditandai to perfection" cenderung produk repainting, persis yang Matt klaim tidak terjadi. Lead time-nya 145–365 hari sebelum bottom, bukan presisi. Substitusi ke K4 kondisi 2 mengubah **nol hari-K4** di semua bear, karena leg `aSOPR<0,93 ≥7 hari` tidak pernah terpenuhi sepanjang 5.843 hari data. **n = 4 bottom testable (2018-19, COVID 2020, 2022, 2025-26 belum final); bottom 2011 & 2015 tidak bisa diuji karena warm-up 1.825 hari.** Verdict: REJECT.
Detail: [`findings_lth_sopr_quantile_vs_k4.md`](findings_lth_sopr_quantile_vs_k4.md)

### [BARU] Kegagalan yang diakui sendiri: double-peak cycle dan peak Oktober 2025
- **Insight:** Penulis mengakui seri ini gagal di dua tempat: "that double peak cycle maybe not", dan di siklus terakhir **bukan peak Oktober 2025 yang ditandai, melainkan peak Juli di $120.000**. `[09:41]`–`[10:07]`
- **Indikator terkait:** LTH-SOPR quantile
- **Relevan ke:** K1 — kalau dipakai sebagai top signal, timing miss beberapa bulan di siklus paling dekat
- **Test klaim:** Pengakuan ini mahal nilainya karena **membatalkan klaim "bisa memilih cycle peak"** dan menurunkan insight sebelumnya dari "nailed" ke "mixed". Dua mode kegagalannya (double-peak, miss peak final) persis sama karakternya dengan false positive Mei 2021 yang framework sudah terima sadar di K3 — jadi metode Matt tidak menawarkan perbaikan di sisi top, hanya memindahkan errornya.
- **Perlu validasi Claude Code:** Ya — sudah diuji sebagai sub-pertanyaan yang menempel di validasi LTH-SOPR.

**[VALIDASI — 2026-07-30, CLOSED]** Negatif, dan lebih buruk dari yang diakui Matt. Di data kita episode `q>0,90` berlangsung **2023-12-24 s/d 2025-11-25 = 703 hari**, menelan kedua peak 2025 sekaligus — pertanyaan "Jul atau Okt" tidak punya jawaban bermakna dari seri ini. (Arahnya condong ke Jul/Ags: q max Jun–Ags 2025 = 1,000 vs Sep–Nov = 0,949 — sesuai klaim Matt, tapi bukan timing signal.) K1 aktual memberi tanggal: 2025-02-02, 2025-06-05, 2025-06-20, 2025-08-19. Perusak tambahan: ada episode `q>0,90` pada **2026-04-05 – 2026-06-21**, justru saat harga jatuh $81k→$63k mendekati bottom — zona "atas" menyala di tengah kapitulasi. **n = 2 peak 2025 + 1 false episode 2026.**
Detail: [`findings_lth_sopr_quantile_vs_k4.md`](findings_lth_sopr_quantile_vs_k4.md)

### [BARU] Caveat penulis: normalisation base drift → arah informatif, magnitude tidak comparable
- **Insight:** Teks di atas Figure 7: gauge menunjukkan step-down (raw Z print euforia 2017, 2021, 2024-25 menurun) — **tapi penulis flag "suggestive only: the trailing-1,460-day normalisation base drifts, so the direction is informative while the precise magnitudes are not stationary-comparable"**. Lampiran Figure 7 `[09:25]`–`[09:58]`
- **Indikator terkait:** LTH-SOPR quantile, semua seri trailing-Z
- **Relevan ke:** general — membatasi pemakaian angka quantile sebagai threshold
- **Test klaim:** Caveat ini benar dan **melemahkan fondasi seluruh bagian quantile**: kalau magnitudo tidak stationary-comparable, membandingkan "0,6th percentile hari ini" dengan "0,6th percentile 2018" tidak sah — padahal itu persis cara metrik ini dipakai untuk market call-nya. Arah step-down euforia sejalan dengan syarat awal K1/K3 kita (MVRV & aSOPR diminishing per ATH), jadi ini konfirmasi lemah untuk sesuatu yang sudah kita punya, dengan alat yang penulisnya sendiri bilang tidak boleh dipakai untuk magnitudo.
- **Perlu validasi Claude Code:** Tidak — sudah established (diminishing per ATH terkunci di K1/K3). Caveat ini ditempel ke hasil validasi quantile di atas, yang memang menemukan drift-nya besar (nominal "10th percentile" ternyata nyala 18,3% hari).

### [BARU] STH-MVRV trailing-Z quantile — lebih banyak sinyal tapi lebih noisy
- **Insight:** Metodologi sama diterapkan ke STH-MVRV. Klaim: spike besar ke atas bertepatan dengan big upside move, capitulation besar ke bawah bertepatan dengan major turning point. Penulis mengakui "it's not nailing the exact peaks". Dari Figure 10, seri bolak-balik antara 0 dan 1 beberapa kali per tahun. Reading saat video: **29,8th percentile**. `[10:07]`–`[10:53]`; Figure 10 `[10:15]`–`[10:47]`
- **Indikator terkait:** STH-MVRV
- **Relevan ke:** **K1 #3** dan **K2 gate valuasi** (STH-MVRV band 0,80–0,97)
- **Test klaim:** Pengakuan "lebih noisy" itu penting: menambah sinyal tanpa menambah presisi = menurunkan precision. Pertanyaannya berbeda dari K4 karena ini **band dua sisi** — apakah versi quantile mempertahankan sifat band (diskon sehat, bukan wilayah bear) atau justru menghapus batas bawah 0,80 yang fungsinya memisahkan bull dip dari bear? Klaim ini tidak berguna kalau versi quantile menyalakan gate di hari-hari bear dalam.
- **Perlu validasi Claude Code:** Ya — sudah diuji, prioritas tinggi (K2 relevan untuk deployment ke depan).

**[VALIDASI — 2026-07-30, CLOSED]** REJECT tegas. **|phi| = 0,817 > 0,8** → gagal lapis 2 Governance, ini reparametrisasi bukan sinyal baru (Jaccard overlap 75,9%). Lebih buruk lagi: 95 hari tambahan yang **hanya** dibuka gate percentile punya median forward return 90 hari **−14,4%** (62,1% negatif) — terburuk dari semua kelompok — sementara 175 hari yang dibuangnya justru **+5,4%**. Pemetaan percentile↔absolut juga tidak stabil: q@`sth_mvrv`=0,80 bergerak 0,027–0,133 antar cycle (faktor 5×). **n = 4.018 hari, 4 cycle efektif (2017-18, 2019-21, 2022-24, 2025-26); 2011 & 2015 tidak bisa diuji karena warm-up, dan 2015-16 hampir kosong (gate q cuma 1 hari).** Band absolut 0,80–0,97 dipertahankan.
Detail: [`findings_sth_mvrv_quantile_vs_k2_gate.md`](findings_sth_mvrv_quantile_vs_k2_gate.md)

### [INDIKATOR CUSTOM] Rolling 4-year flt-MVRV quantile bands — analog fungsional AVIV Mean/Upper
- **Insight:** Band q05/q10/q20 – q80/q90/q95 dari rasio harga terhadap filtered realized price, basis rolling 4 tahun. Legend Figure 11 (**low confidence dari resolusi frame**): q95 $131.523 · q90 $124.582 · q80 $118.473 · q20 $65.631 · q10 $50.764 · q05 $47.280 · RP(flt) $58.468 · price $65.610. Caption: "Price sits near the 20th percentile of the trailing four-year regime." `[10:53]`–`[12:01]`; Figure 11 `[11:04]`–`[11:53]`
- **Indikator terkait:** filtered RP, MVRV — paralel dengan **AVIV Mean / AVIV Upper** di framework
- **Relevan ke:** **Zone Structure v2** — AVIV Mean = batas Z3/Z4, AVIV Upper = batas Z4/Z5 dan trigger eksekusi K1 serta akhir K5
- **Test klaim:** Dekomposisinya: ini pada dasarnya **rasio Price/RP yang dinormalisasi ke persentil rolling 4 tahun** — yaitu MVRV, dengan RP versi flt sebagai denominator. Framework sudah punya alat yang mengerjakan pekerjaan sama. Preseden CLOSED (`findings_mvrv_rolling1y_vs_aviv.md`) sudah menjawab pertanyaan hampir identik untuk window 1 tahun: ballpark align tapi skala tidak setara, divergensi artefak reaktivitas formula, tidak ada K-node baru.
- **Perlu validasi Claude Code:** Ya — sudah diuji, prioritas rendah justru karena preseden.

**[VALIDASI — 2026-07-30, CLOSED]** Confirming lemah, tidak ada K-node baru — sejalan preseden window-1-tahun. Band atas berkorelasi **0,9992 (log-level)** dengan AVIV Upper, praktis kelipatan tetap (q90/AVIV Upper: 1,25 di 2017 & Apr-2021, turun ke 1,10 di 2025). Band bawah bukan lantai: harga **menembus q05 di ketiga bottom final**, sementara P/CVDD cuma 0,98–1,07. `P/CVDD<1,10` nyala 100 hari, **97 di antaranya sudah tercakup P<q10** → band bawah superset yang lebih longgar, bukan info baru. Klaim video **reproduce**: pada 2026-06-16 persentil aktual **0,201**, label zona kita ZD (Dip dalam). **Temuan mekanis yang paling berguna:** band = `quantile(P/RP) × RP`, jadi **invarian terhadap penskalaan base RP** (diuji: RP ×1,094 → deviasi q90 0,0000%) — seluruh kerja "filtered realized price" praktis tidak mengubah output band ini. **n = 5 puncak + 4 bottom (3 final + 1 bottom-so-far), 3–4 cycle; band valid sejak 2014-07-16.**
Detail: [`findings_rolling4y_price_rp_bands_vs_aviv.md`](findings_rolling4y_price_rp_bands_vs_aviv.md)

### [BARU] Klaim "tidak repainting"
- **Insight:** "These aren't repainting historically. This is based on real on-chain fundamental Bitcoin data." `[11:15]`
- **Indikator terkait:** quantile bands, semua seri quantile
- **Relevan ke:** general — menyentuh STANDAR VALIDASI butir 3 (anti lookahead)
- **Test klaim:** Klaim ini **tidak perlu dipercaya, cukup dipaksakan sebagai constraint di implementasi kita sendiri**. Titik lemahnya konkret: "rolling 4 tahun" mencegah repainting di level window, tapi pemetaan Z → "historic quantile" gampang bocor kalau persentilnya dihitung terhadap seluruh sejarah termasuk masa depan — persentil hari 2015 berubah setiap kali ada data baru = repainting definisi. Frame video tidak cukup untuk memastikan mana yang dipakai penulis.
- **Perlu validasi Claude Code:** Ya — sudah diuji, dititipkan ke validasi LTH-SOPR.

**[VALIDASI — 2026-07-30, CLOSED]** Bias lookahead terukur **besar**: mean |q_full − q_exp| = 0,0871, max **0,4818**, dan hari di bawah 0,10 berbeda **41,0%** antara versi expanding (jujur) dan full-history (repainting). Paling tajam di COVID: versi repainting nyala 2020-03-12 – 2020-03-29 (18 hari, lead nol) sementara versi jujur sudah nyala sejak 2019-10-15. **Artinya "COVID ditandai to perfection" cenderung produk repainting.** Kami tidak bisa memastikan versi mana yang dipakai Matt, tapi selisihnya cukup besar sehingga klaim "tidak repainting" wajib diverifikasi sendiri, tidak diterima apa adanya. **n = 4.018 hari periode overlap.**
Detail: [`findings_lth_sopr_quantile_vs_k4.md`](findings_lth_sopr_quantile_vs_k4.md)

### [BARU] Caveat n=3 yang ditulis penulis sendiri di Section 7
- **Insight:** Section 7 ("Weighting, Lookback, and Out-of-Sample Robustness") menyebut eksplisit: "**the n=3 caveat stated in Section 1 governs throughout: with three bear lows and three bull tops, a range of 0.036 versus … has limited power to declare a general winner** as these are suggestive single-asset patterns". Lampiran `[11:04]`–`[11:53]`
- **Indikator terkait:** semua metrik di paper
- **Relevan ke:** general
- **Test klaim:** Persis di batas aturan CLAUDE.md ("<3 cycle → low-confidence"; framework sendiri sadar 3–4 cycle = sampel kecil). Konsekuensi: **semua klaim akurasi komparatif di video ini (rolling-4y vs all-time cumulative, dinamis vs static) berdiri di n=3 dan tidak boleh jadi dasar mengubah threshold apapun** — sejalan Governance butir 2 & 3. Penulis lebih jujur dari kebanyakan sumber: caveat ini datang dari dia, bukan dari kita.
- **Perlu validasi Claude Code:** Tidak — sudah established sebagai prinsip framework.

### [STRATEGI] Market call Jun 2026: "clearly in deep value territory"
- **Insight:** Kesimpulan video: semua metrik pada boundary baru "are all pointing towards us being clearly in deep value territory". Bukti: LTH-SOPR quantile **0,6th percentile** ("among the most oversold on record", "on par with that $60.000 reading, practically the lowest levels ever"); harga di **persentil ~20** band 4-tahun pada ~$65k; STH-MVRV **29,8th percentile**. `[09:41]`–`[10:07]`, `[11:15]`, `[15:32]`
- **Indikator terkait:** LTH-SOPR quantile, STH-MVRV quantile, flt-MVRV quantile bands
- **Relevan ke:** status pasar saat ini — K4 / ZC / lantai waktu. Konteks: bear pasca peak Okt 2025 ~$120k+, harga saat film ~$65k.
- **Test klaim:** Tiga reading yang disajikan sebagai satu kesimpulan sebenarnya **sangat tidak sejalan**: 0,6 vs 20 vs 29,8 percentile — dari metodologi normalisasi yang **sama**. Kalau tiga metrik dari transformasi yang sama memberi sebaran selebar itu, itu bukan konfirmasi berlapis, itu indikasi transformasinya sensitif ke pilihan metrik input. Secara arah "deep value" tidak bertentangan dengan posisi kita, tapi **market call bukan insight** dan tidak boleh mempengaruhi count K4 — count K4 dihitung dari 4 kondisi kita sendiri.
- **Perlu validasi Claude Code:** Tidak — market call naratif, time-bound. (Bagian persentil-20-nya kebetulan sudah tervalidasi reproduce lewat validasi quantile band: 0,201 pada 2026-06-16, label zona kita ZD.)

### [STRATEGI] Rookies vs veterans — memecah cohort LTH berdasarkan kualitas timing
- **Insight:** Arah riset berikutnya (belum dibangun): memisahkan LTH jadi "rookies" (beli di puncak bull lalu terpaksa hold) vs "veterans" (beli di bottom), untuk mengikuti "genuine smart money". Kredit ke **Johan (The Bitcoin Layer)** dan **Nim (Bitcoin Research Cave)**. `[13:11]`–`[13:58]`
- **Indikator terkait:** LTH cohort splitting, LTH-MVRV, LTH-NUPL
- **Relevan ke:** K4 kondisi 1 (LTH-MVRV <1,0)
- **Test klaim:** Belum dibangun, jadi tidak ada klaim yang bisa dites — ini roadmap. Nilainya: **mengkonfirmasi kritik yang sudah ada di `nupl_knowledge_base v1.4.md` baris 710** ("LTH != smart money. LTH hanyalah 'belum jual selama 155 hari' — bisa jadi hodler yakin, bisa jadi hodler yang stuck"). Kalau kelak dibangun, pertanyaan test-nya sudah jelas: apakah sub-kohort "veteran" memberi sinyal berbeda dari LTH agregat setelah dikoreksi untuk fakta bahwa "beli di bottom" hanya bisa diketahui ex post — **survivorship + lookahead risk melekat di definisi kohortnya**.
- **Perlu validasi Claude Code:** Tidak — belum ada metrik, dan dekomposisi kohort by entry-price tidak feasible (butuh UTXO-level cost basis per address).

### [STRATEGI] Open source penuh — semua formula, filter, dan chart interaktif dipublikasi
- **Insight:** Seluruh formula, filter, dan data dipublikasi di mattcrosby.pro (paper + interactive charts per metrik), eksplisit mengundang replikasi: "if any of you guys can come up with better methodology, do I truly welcome it… I don't want to personally benefit from this." `[12:01]`–`[12:48]`, `[14:47]`–`[15:10]`
- **Indikator terkait:** semua
- **Relevan ke:** general — testability sumber
- **Test klaim:** Bukan insight pasar, tapi relevan untuk cara kita menilai sumber. Kontras tajam dengan preseden di index kita — "Risk indicators internal On-Chain Mind (komponen tidak diungkap)" → tidak testable, black box. Di sini semua komponen terbuka, jadi klaimnya **falsifiable in principle**, dan itu menaikkan bobot kepercayaan pada disclosure caveat-nya — yang kebetulan justru bagian paling berguna dari videonya. Tetap tidak mengubah fakta bahwa base flt tidak comparable dengan data kita.
- **Perlu validasi Claude Code:** Tidak — meta, bukan klaim empiris.

### [KONFIRMASI] Normalisasi rolling-quantile sejalan filosofis dengan prinsip "pola relatif, bukan threshold absolut"
- **Insight:** Alasan penulis membuat seri bounded 0–1 adalah masalah yang sama yang sudah diakui framework: nilai absolut satu metrik tidak comparable antar siklus. Rolling-quantile adalah bentuk formal dari solusi yang framework pakai secara informal (diminishing per ATH, pola relatif). `[04:43]`–`[05:05]`, `[09:18]`
- **Indikator terkait:** semua
- **Relevan ke:** general — prinsip utama framework
- **Test klaim:** Konfirmasi yang sah dan ini kontribusi terbaik video untuk kita — tapi dengan tegangan internal yang penulisnya sendiri akui: rolling-quantile menghilangkan ketergantungan pada angka tetap, **namun base normalisasinya drift** sehingga magnitudo tidak stationary-comparable. Artinya rolling-quantile **memindahkan** masalah, tidak menghapusnya: dari "threshold absolut tidak stabil antar cycle" ke "base normalisasi tidak stabil antar cycle".
- **Perlu validasi Claude Code:** Tidak sebagai insight terpisah — sudah tercakup di validasi LTH-SOPR dan STH-MVRV.

**[VALIDASI — 2026-07-30, CLOSED]** Tegangan yang diduga terkonfirmasi di data kita: nominal "10th percentile" pada seri expanding LTH-SOPR ternyata nyala **18,3% hari**, dan pemetaan percentile↔absolut STH-MVRV bergeser faktor 5× antar cycle (q@0,80 = 0,027–0,133). **Rolling-quantile memang memindahkan instabilitas, bukan menghapusnya.** Dua penerapan konkretnya di data kita dua-duanya REJECT. **n = 4.018 hari, 4 cycle efektif.** Prinsip "pola relatif" tetap benar; implementasi rolling-quantile spesifik ini bukan cara yang lebih baik untuk mengekspresikannya di framework kita.
Detail: [`findings_lth_sopr_quantile_vs_k4.md`](findings_lth_sopr_quantile_vs_k4.md) · [`findings_sth_mvrv_quantile_vs_k2_gate.md`](findings_sth_mvrv_quantile_vs_k2_gate.md)

### [KONFLIK] Klaim "on-chain BISA memilih cycle peak kalau pakai basis reaktif"
- **Insight:** "Everyone talks about on-chain data not being able to pick the cycle peaks, but again, if we look at it in a more reactive basis, on a variable length threshold, it's very very actionable" — dan mencatat threshold band atas "are thresholds that we reached in this cycle". `[11:38]`–`[12:01]`
- **Konflik dengan:** Desain K1, yang sengaja **tidak** mencoba memilih peak. K1 pakai OR-gate reaktif (harga turun dari Z5 ke Z4 ATAU gap MA90−MA60 STH-SOPR turun ≥14 hari), menerima window sinyal→deadline menyempit tiap siklus (~30 hari 2017 → 6 hari 2025), dan menerima false positive tipe Mei 2021 di K3 sebagai risiko sadar.
- **Alasan konflik:** Klaim ini **dibantah oleh datanya sendiri** — penulis mengakui metode ini menandai Jul 2025, bukan peak Okt 2025, dan gagal di double-peak cycle. Band-nya juga di-fit ke data siklus ini sendiri (rolling 4 tahun mencakup peak siklus ini). Kalau diadopsi mentah, ini mendorong ke keputusan prediktif — berlawanan dengan arsitektur trigger-reaktif framework.
- **Rekomendasi:** **Abaikan.** Klaim retoris di akhir segmen, bukan temuan; bukti pendukungnya nol dan penulisnya sendiri sudah mengoreksinya. Validasi kami memperburuk: episode `q>0,90` berlangsung 703 hari menelan kedua peak 2025, dan menyala lagi saat kapitulasi Apr–Jun 2026.

### [KONFLIK] Mengganti boundary cohort wholesale akan mereset seluruh kalibrasi threshold framework
- **Insight:** "Anyone can update their own metrics to use this new variable long-term holder boundary to create even better data." `[14:47]`–`[15:10]`
- **Konflik dengan:** (a) seluruh angka threshold di Decision Framework v2 — semuanya dikalibrasi pada cohort 155-hari; (b) **§ Governance butir 2** (framework dibekukan per siklus; sinyal baru naik kelas hanya lewat protokol 4 lapis) dan **butir 3** (semua threshold = panduan arah dari 3–4 siklus); (c) kebutuhan basis definisi konsisten untuk perbandingan lintas-cycle — sedangkan boundary ini berubah tiap hari dan pernah bergerak 105 → 231 → 114.
- **Alasan konflik:** Ini bukan penambahan sinyal, ini **penggantian unit pengukuran di bawah hampir semua sinyal yang sudah divalidasi**. Semua `n` dan semua findings existing akan kehilangan basis. Diperingan oleh tiga hal: penulis sendiri tidak mengadopsinya, angka 114 tidak unik, dan caveat n=3 dari penulisnya sendiri.
- **Rekomendasi:** **Tolak adopsi basis kohort; ambil hanya metodologi normalisasinya** (yang ternyata juga REJECT setelah diuji). Sudah divalidasi — dampaknya akademis, lihat blok di bawah dan section FLAG di atas.

**[VALIDASI — 2026-07-30, CLOSED]** Dampak diukur lewat bracket HODL-wave: label struktur Zone Dimensi 1 berubah hanya **0,49%** hari (24 dari 4.944) untuk cutoff ≥3m dan **0,26%** untuk ≥6m — jauh di bawah ambang 2% yang ditetapkan di muka sebagai batas "akademis". Tanggal trigger Z2 bergeser 0–6 hari di 4 dari 5 episode (outlier: episode Jan 2019 hilang, muncul +102 hari kemudian di versi ≥3m); cross-up STH RP>RP tidak terpengaruh sama sekali. **n = 4.944 hari, 5 cycle; perubahan terkonsentrasi di 2019-21 (20 dari 24 hari) → didominasi satu cycle.** Alasan dampaknya kecil: deviasi LTH RP besar di euforia (+18,1% saat MVRV>2,5) tapi hampir nol di bear (+1,3% saat MVRV<1) — dan justru di bear-lah framework kita memakai LTH RP. **Verdict: flag STOP akademis, bukan konflik serius.** Catatan: kesimpulan ini tidak otomatis berlaku kalau kelak framework menambah sinyal yang bergantung LTH RP di fase euforia.
Detail: [`findings_lth_rp_boundary_sensitivity.md`](findings_lth_rp_boundary_sensitivity.md)

---

## Flag Prioritas

1. **`aSOPR < 0,93 selama ≥7 hari` di K4 kondisi 2 tidak pernah terpenuhi di 5.843 hari data** (streak max 6 hari, Sep 2011) — temuan internal yang muncul saat memvalidasi video ini, bukan dari videonya. Kondisi 2 K4 mati secara mekanis, setara temuan "kondisi #1 K2 lama mati". Ini yang paling mendesak dibahas karena K4 adalah K-node aktif kita sekarang. Penempelan/perbaikan dikerjakan di Onchain-Dashboard.
2. **Flag STOP boundary dinamis — sudah turun kelas jadi akademis (0,49% label berubah).** Perlu keputusanmu untuk menutupnya secara formal: tolak adopsi basis kohort, ambil metodologi saja. Tiga argumen pendukung sudah datang dari penulisnya sendiri.
3. **Metodologi trailing-Z → quantile: REJECT di dua penerapan, tapi pelajarannya berguna.** Rolling-quantile memindahkan instabilitas (dari threshold absolut ke base normalisasi), tidak menghapusnya — nominal "10th percentile" nyala 18,3% hari, dan pemetaan percentile↔absolut bergeser faktor 5× antar cycle. Ini argumen empiris pertama di korpus kita untuk **mempertahankan** threshold absolut yang sudah dikalibrasi, bukan menggantinya dengan normalisasi rolling.
4. **Band = `quantile(P/RP) × RP` invarian terhadap penskalaan base RP.** Temuan mekanis yang membatalkan sebagian premis videonya sendiri: seluruh kerja "filtered realized price" praktis tidak mengubah output quantile band. Berguna sebagai aturan umum saat menilai klaim price-band dari sumber manapun ke depan.
5. **Klaim "tidak repainting" wajib diverifikasi sendiri, jangan diterima apa adanya.** Selisih expanding vs full-history percentile mencapai 41% hari di data kita, dan justru di COVID — kasus yang paling sering dipakai sebagai bukti akurasi — selisihnya paling ekstrem.
6. **Sumber ini worth diikuti.** Open-source penuh, caveat ditulis sendiri, dan penulisnya menolak overclaim di titik yang paling menggoda untuk overclaim. Kontras dengan black-box indicator dari sumber lain di index kita. Roadmap "rookies vs veterans" layak dipantau — kalau dibangun, itu menyentuh kritik "LTH != smart money" yang sudah ada di KB kita.

---

## Yang Langsung Diabaikan

| Item | Timestamp | Alasan |
|---|---|---|
| Promosi mattcrosby.pro sebagai "test site untuk Bitcoin Magazine Pro" | `[12:25]`–`[12:48]` | promo produk; bagian open-source-nya sudah diambil sebagai insight terpisah |
| "Bear markets are for building", "taking the opportunity throughout this bear market" | `[12:48]`–`[13:11]` | naratif, tidak actionable |
| "This is my first ever publicly published research piece, so be nice" | `[15:32]`–`[15:55]` | disclaimer sosial |
| "England are going to win the World Cup" | `[15:55]` | — |
| "I did spend too much time to admit working on this" | `[00:00]` | hook |
| Screenshot Bitcoin core `core.h` di GitHub | Lampiran `[08:03]` | ilustrasi definisi dust; substansinya sudah masuk Table 1 |
| Screenshot Blockchain.com mempool transaction count | Lampiran `[03:41]` | ilustrasi argumen; substansinya sudah masuk filtered RP |

---

## Catatan sumber

Semua angka bernomor dolar dan persentil dari paper (Figure 1/2/3/5/7/10/11, Table 1) dibaca dari frame video → **low confidence dari resolusi frame**, tidak dipakai sebagai anchor kesimpulan. Selain itu base data Matt (**flt** + boundary dinamis) **tidak comparable** dengan dataset kita (**std** + 155 hari) — semua validasi di atas menguji **metodologinya di atas data kita**, bukan mereplikasi angkanya.
