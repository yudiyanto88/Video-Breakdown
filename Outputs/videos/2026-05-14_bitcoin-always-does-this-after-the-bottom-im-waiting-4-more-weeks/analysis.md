# Bitcoin Always Does This After The Bottom — I'm Waiting 4 More Weeks
**Channel:** Bitcoin Magazine Pro (host: Matt Crosby)
**Tanggal video:** 14 Mei 2026
**Tanggal analisis:** 5 Agustus 2026
**Link:** https://youtu.be/qZWV8T5nibI

---

## 🚩 FLAG — perlu keputusan Yudi

Tidak ada konflik dengan hard constraint LTV. Video tidak menyinggung leverage sama sekali.
Dua hal masuk kategori "framework/strategi pembicara fundamental berbeda dari zone-based + K-node":

**STOP-1 — Waktu dipakai sebagai alasan MENUNDA beli, bukan sebagai PEMICU beli.**
Sikap video: "bottom sudah in di $60k, tapi saya belum beli — time-based capitulation belum selesai."
Itu kebalikan arah dari K4 jalur lantai waktu, yang memakai berlalunya waktu sebagai **izin mulai
mencicil** (≥9 bulan sejak cycle peak DAN close < RP → DCA 5% cash pool/bulan, spot only, jalan walau count <2).

**Konflik ini masih FILOSOFIS, belum operasional.** Validasi V4 mengoreksi catatan Stage 2 yang menyebut
lantai waktu "sudah aktif sejak Juli 2026": per akhir data (2026-07-15) hanya syarat waktunya yang
terpenuhi (9,3 bulan sejak peak 6 Okt 2025, sejak 2026-07-06), sementara syarat `close < RP` belum —
close $65.098 vs RP $52.740, rasio 1,23×, butuh turun ~19% lagi. Jadi **tidak ada DCA lantai waktu
yang sedang berjalan untuk ditunda.** Yang perlu dijaga: narasi "tunggu time capitulation" jangan
sampai pelan-pelan menggeser disiplin lantai waktu begitu ia benar-benar aktif nanti.

**STOP-2 — Arsitektur keputusan berbasis confluence makro, bukan struktur cost-basis.**
Sikap "cool off ahead" dibangun dari 5 pilar: High Yield Credit divergence + DXY YoY + Global M2
rate-of-change + AASI + technical resistance. **Tidak satupun indikator aktif framework** (MVRV, SOPR,
Supply in P/L, RP family, RHODL) muncul di video. Tambahan: 3 dari 5 pilar sama-sama ekspresi kondisi
likuiditas USD — kemungkinan besar satu bukti dihitung tiga kali, dan tidak akan lolos Governance
butir 1 (uji independensi |phi| < 0,3). Flag setara sudah diangkat di video `2026-07-02` (channel sama)
dan keputusannya waktu itu "catat saja" — diangkat lagi untuk konsistensi, bukan untuk dilitigasi ulang.

---

## Ringkasan

Matt Crosby merekam video ini tepat saat Bitcoin baru saja menembus STH Realized Price (~$78.600)
dari bawah setelah rally dari low Februari 2026, dan pasar mulai optimis. Argumen utamanya: reclaim itu
belum menyelesaikan apapun, karena harga langsung menabrak klaster resistance — zona horizontal
$81.000–$85.000, 200 DMA, dan STH-RP itu sendiri semuanya berhimpit di area yang sama.

Tesis inti video adalah pemisahan **price-based capitulation** dari **time-based capitulation**.
Menurutnya kapitulasi harga sebagian besar sudah terjadi (>50% chance $60.000 adalah low cycle ini),
tapi kapitulasi waktu — "genuinely just boring investors out of the market" — belum. Karena itu dia
tidak membeli di level saat itu meski percaya bottom sudah lewat, dan menunggu harga kembali ke
~$70.000 untuk DCA agresif. Dia sendiri mengakui posisi ini terdengar kontradiktif.

Bukti pendukungnya datang dari tiga arah. Pertama, chart komunitas "Drawdowns from ATH to Cycle Low"
yang menunjukkan cycle berjalan masih jauh lebih pendek dan dangkal dari bear sebelumnya. Kedua, tiga
overlay makro yang semuanya menunjuk puncak sekitar pertengahan Mei 2026 lalu turun: High Yield Credit
yang mulai divergen, DXY year-on-year yang di-invert dan di-offset 100 hari, dan laju ekspansi Global M2.
Ketiga, metode bar-pattern fractal — dia menyalin price action setelah lowest closing price bear 2015,
2018-19, dan 2022, lalu menempelkannya ke low 2026; dua dari tiga menunjuk pertengahan Juni sebagai
titik break, satu (2015) menunjuk November 2026.

Video ini berumur ~3 bulan saat dianalisis, jadi seluruh call bertanggalnya sudah bisa dinilai — dan
itu jadi salah satu dari empat validasi yang dijalankan. Ringkasnya: **arah makronya kena, angka
absolutnya tidak.** Harga memang topping tepat di sekitar tanggal video lalu turun −27,9%, tapi base case
"$60.000 = low" tertembus (low $58.460 @ 30 Juni), skenario ekor mid-$50k yang dia beri probabilitas
20–25% justru terjadi, dan DCA di $70.000 diikuti penurunan −7,4% dalam 30 hari berikutnya.

---

## Insight Inventory

### [BARU] Zona horizontal $81.000–$85.000 sebagai resistance cluster
- **Insight:** Zona merah $81k–$85k disebut "key turning point throughout the past few years" — berkali-kali jadi major support, terakhir jadi resistance. Harga saat rekaman tepat di bawahnya `[00:55]`–`[01:23]`
- **Indikator terkait:** price action murni (horizontal S/R), bukan indikator on-chain
- **Relevan ke:** general
- **Test klaim:** Threshold absolut murni dengan lebar ~5% — cukup lebar untuk hampir selalu "kena" begitu harga masuk area itu, jadi nyaris tidak bisa salah dalam bentuk sekarang. Dasarnya praktis satu cycle (n<3 → low-confidence). Framework sengaja pakai level yang bergerak per cycle (STH RP, RP, AVIV) justru supaya level tidak jadi angka mati yang basi begitu cost basis pasar bergeser. Supaya salah: harga break $85k dan bertahan tanpa rejection berarti.
- **Perlu validasi Claude Code:** Ya — digabung ke validasi kalibrasi ex-post

**[VALIDASI — 5 Agustus 2026, CLOSED]** Zona ini **tidak pernah diuji ulang** setelah video: 0 hari close di band $81k–$85k, 0 episode masuk band, 0 hari close > $85.000. Harga langsung menjauh ke bawah, jadi klaimnya tidak terkonfirmasi maupun terfalsifikasi — dan itu sendiri menunjukkan kenapa level harga absolut yang lebar sulit dinilai. **n=1 episode**, deskriptif.
Detail: [`findings_expost_calibration.md`](findings_expost_calibration.md)

### [BARU] 200 DMA sebagai titik rejection saat bear
- **Insight:** "the 200-day moving average is exactly where we've been rejected from" — rejection terjadi persis di 200 DMA yang saat itu berhimpit dengan zona $81–85k `[01:23]`–`[01:51]`
- **Indikator terkait:** 200-day MA (bukan indikator aktif framework)
- **Relevan ke:** general / ZD–Z3
- **Test klaim:** Sisi *reclaim* sudah CLOSED di `2026-07-02` (200 DMA reclaim mendahului unlock Z1→Z2 sebesar 23–51 hari, n=4). Yang belum diuji adalah sisi yang dipakai video ini: 200 DMA sebagai **resistance** saat bear. Kata "exactly" berlebihan — rejection di MA panjang selalu punya toleransi beberapa persen dan MA-nya sendiri bergerak tiap hari.
- **Perlu validasi Claude Code:** Ya — jadi inti validasi confluence

**[VALIDASI — 5 Agustus 2026, CLOSED]** **SUPPORTED.** Dengan definisi bear luas (ZC/ZD/Z1/Z1b, 2.348 hari), **n=13 event cross-up 200 DMA tersebar di 5 cycle** (2011:1, 2013-15:3, 2017-19:3, 2021-23:4, 2025-26:2) — **11 dari 13 (85%) ditolak** dalam 30 hari. Dua yang bertahan keduanya dari cycle 2013-15, jadi sisi positifnya didominasi satu cycle sementara sisi negatifnya tersebar merata. Dengan definisi bear ketat (ZC/Z1/Z1b) hanya ada **n=2 event, keduanya 2013-15** — tidak konklusif, dilaporkan apa adanya. Verifikasi angka: per 2026-05-14, 200 DMA = $82.124 dan harga = 98,7% dari itu — **klaim rejection-nya akurat**.
Detail: [`findings_ma200_sthrp_confluence.md`](findings_ma200_sthrp_confluence.md)

### [BARU] Confluence resistance tiga lapis: STH-RP + 200 DMA + zona $81–85k
- **Insight:** Ketiganya berada di area harga yang hampir sama sehingga diperlakukan sebagai satu klaster resistance. Ringkasan penutup mengulang ini persis, plus catatan "the short-term holder realized price, which we might dip beneath as well" `[12:04]`–`[12:32]`, `[12:30]`–`[12:50]`
- **Indikator terkait:** STH Realized Price + 200 DMA + horizontal S/R
- **Relevan ke:** batas ZD/Z3; **Signal D (K4 wrap-up)**
- **Test klaim:** Menyentuh langsung item terbuka framework — Flag Prioritas #1 dari analisis `2026-08-04` menemukan Signal D hit rate hanya ~12% (7 dari 8 break palsu) dan mengusulkan memasangkannya dengan 200 DMA; video ini secara independen mengatakan hal yang sama dari sisi resistance. Titik lemahnya: di bear, STH RP dan 200 DMA memang cenderung berdekatan (dua-duanya rata-rata harga beberapa bulan terakhir dengan bobot berbeda) — kalau korelasinya nyaris 1, "confluence" bukan konfirmasi independen melainkan pengukuran ganda.
- **Perlu validasi Claude Code:** Ya — prioritas tertinggi

**[VALIDASI — 5 Agustus 2026, CLOSED]** **Klaim confluence NOT SUPPORTED, tapi uji silangnya menghasilkan temuan operasional yang kuat.** Kelompok gap ≤5% justru punya rejection rate *lebih rendah* (67%, n=3) daripada gap >5% (90%, n=10) — kebalikan dari yang diklaim, dan n terlalu timpang untuk disimpulkan. Yang menentukan: **korelasi `200_dma` vs `sth_cost_basis` selama bear r ≈ +0,999** (level log, n=724 hari) — jadi "confluence" adalah satu hal yang diukur dua kali, tidak akan lolos Governance butir 1. **Temuan terpentingnya di uji silang:** memasang filter "harga di atas 200 DMA pada hari ke-3 break" ke 8 event Signal D historis menyingkirkan **7 dari 7 break palsu (tersebar di 4 cycle) tanpa membuang 1 break asli** — hit rate 12% → 100%, tapi sisi "meloloskan yang asli" **bersandar pada n=1**. Event 2026-05-06 yang dibahas video ini termasuk yang tersaring keluar, dan ex-post memang palsu.
Detail: [`findings_ma200_sthrp_confluence.md`](findings_ma200_sthrp_confluence.md)

### [BARU] Rally tajam yang menabrak resistance besar "usually unsustainable"
- **Insight:** Pergerakan naik hampir tanpa henti dari $60k ke ~$80k dinilai tidak berkelanjutan justru karena berhenti tepat di bawah klaster resistance `[01:51]`–`[02:17]`. Dia mengakui kekuatannya melebihi ekspektasinya sendiri
- **Indikator terkait:** price action
- **Relevan ke:** general
- **Test klaim:** "Usually" tanpa n, tanpa definisi "rally tajam" atau "resistance besar" — dalam bentuk ini tidak falsifiable. Risiko lebih besar: pernyataan ini bisa benar secara trivial di dalam bear (per definisi bear membuat lower highs, jadi hampir semua rally "gagal"), sehingga tidak menambah informasi di atas fakta "kita sedang bear".
- **Perlu validasi Claude Code:** Ya — sebagai sub-hipotesis validasi confluence

**[VALIDASI — 5 Agustus 2026, CLOSED]** **Terkonfirmasi lewat proxy, dengan catatan trivialitas.** Rejection rate 85% (11/13, 5 cycle) memang tinggi, tapi validasi tidak memisahkan efek "menabrak resistance" dari efek "sedang bear" — jadi klaim ini **cenderung** benar tanpa terbukti informatif. Ex-post untuk episode spesifik video: rally berhenti tepat di sana dan harga turun **−27,9%** dari close hari video.
Detail: [`findings_ma200_sthrp_confluence.md`](findings_ma200_sthrp_confluence.md)

### [BARU] Chart "Drawdowns from ATH to Cycle Low" — cycle ini baru ~200 hari, masih "considerable time to go"
- **Insight:** Kurva cycle berjalan berhenti di ~hari 200-an pada drawdown yang dia baca ~−35%, sementara tiga cycle lama memanjang ke 600–800 hari dan −75% s/d −85% `[03:13]`–`[03:42]`, `[07:45]`–`[08:05]`
- **Indikator terkait:** drawdown-from-ATH + elapsed days (chart komunitas, bukan milik channel)
- **Relevan ke:** **K4 lantai waktu**
- **Test klaim:** n=3 kurva pembanding, dan angkanya patut dicurigai. Cacat logika kedua lebih serius: membandingkan cycle yang **belum selesai** dengan tiga cycle yang **sudah selesai** adalah perbandingan censored vs completed — cycle berjalan otomatis terlihat "belum cukup lama/dalam" sampai ia selesai, apapun kenyataannya.
- **Perlu validasi Claude Code:** Ya

**[VALIDASI — 5 Agustus 2026, CLOSED]** **Arah benar, dua angka video salah.** Dari **n=4 bear selesai + 1 berjalan**: drawdown per tanggal video sebenarnya **−49,6%**, bukan ~−35% (selisih 15 pp terhadap ATH $124.715 @ 2025-10-06), dan durasi bear sebelumnya **163/411/363/378 hari**, bukan 600–800 — sumbu-x chart itu memang membentang 800+ hari, tapi itu panjang sumbu, bukan posisi cycle low. Tiga bear modern seragam di **363–411 hari** (kalau diikuti, cycle low jatuh sekitar Okt–Nov 2026), tapi cycle berjalan jauh lebih dangkal (**−53,1%** vs −76,6% terdangkal sebelumnya). Hubungan kedalaman↔durasi **tidak diinferensikan** (n=4, r=+0,812 didominasi satu titik 2011).
Detail: [`findings_drawdown_depth_duration.md`](findings_drawdown_depth_duration.md)

### [BARU] Inverse correlation DXY ↔ BTC sebagai macro overlay
- **Insight:** "very noticeable inverse correlation" — saat US Dollar Strength naik, BTC biasanya turun; cool-off DXY belakangan berbarengan dengan divergence high yield credit `[04:36]`–`[05:03]`
- **Indikator terkait:** DXY (macro), tidak ada di framework
- **Relevan ke:** general
- **Test klaim:** Korelasi makro ini tidak stabil — kuat di rezim tertentu dan menghilang di rezim lain, tapi video menyajikannya sebagai konstanta. Kata "causation" yang dipakai di segmen berdekatan tidak didukung apapun selain koinsidensi visual.
- **Perlu validasi Claude Code:** **Tidak — data tidak tersedia.** DXY bukan bagian `data_master_all_metrics.csv` (dataset kita murni on-chain BTC + F&G + derivatives)

### [BARU] Prinsip metodologis: pakai rate-of-change, bukan level, untuk seri yang trennya satu arah
- **Insight:** Dipakai dua kali. (a) DXY: karena fiat terus terdebase, level DXY kurang informatif — pakai basis year-on-year `[05:03]`–`[05:57]`. (b) Global M2: yang dia pakai adalah "rate of expansion and contraction", bukan chart level `[06:25]`–`[06:52]`
- **Indikator terkait:** DXY YoY, Global M2 rate-of-change
- **Relevan ke:** general
- **Test klaim:** Prinsipnya benar dan sebetulnya **sudah dipakai framework** — MVRV Momentum (SMA30 vs SMA30-dari-SMA30) dan gap MA90−MA60 STH-SOPR keduanya sinyal turunan/laju, bukan level. Jadi ini lebih dekat ke [KONFIRMASI] terselubung. Yang tetap perlu dicatat: transformasi rate-of-change memperbesar noise dan menambah parameter bebas (window mana?) — tiap pilihan window adalah derajat kebebasan yang bisa di-tune ke belakang.
- **Perlu validasi Claude Code:** Tidak — prinsipnya sudah established di framework, dan seri yang dimaksud video datanya tidak tersedia

### [BARU] Global M2 level ATH ≠ sinyal bullish BTC
- **Insight:** Global M2 baru saja ATH, tapi menurutnya itu bukan alasan bullish karena seri itu memang selalu naik; yang penting laju ekspansinya, dan laju itu memuncak sekitar pertengahan Mei 2026 lalu turun `[06:25]`–`[07:03]`
- **Indikator terkait:** Global M2 / global liquidity
- **Relevan ke:** general
- **Test klaim:** Argumen strukturalnya masuk akal (seri monoton naik tidak informatif sebagai level), tapi "incredibly predictive" disebut tanpa satupun angka, n, atau uji lead/lag. Dengan tiga parameter bebas (definisi laju, window, offset), sangat mudah menghasilkan chart yang tampak cocok secara retroaktif.
- **Perlu validasi Claude Code:** **Tidak — data tidak tersedia** (Global M2 tidak ada di dataset)

### [BARU] "Bear market tidak pernah V-shaped"; recovery datang saat orang berhenti berharap
- **Insight:** "It's not just Bitcoin specifically, in pretty much all markets it's very rarely almost a V-shaped recovery during a bear market" `[12:04]`–`[12:32]`. Versi mekaniknya `[10:10]`–`[10:39]`: bear selalu punya fake-out, chop, dan cukup waktu supaya orang bosan
- **Indikator terkait:** —
- **Relevan ke:** K4 (proses bottoming), general
- **Test klaim:** Bagian "recovery datang saat orang berhenti berharap" adalah pernyataan psikologis tanpa metrik, tidak falsifiable. Bagian yang testable sudah dijawab sebelumnya dan hasilnya justru **melemahkan** versi kuatnya.
- **Perlu validasi Claude Code:** Tidak mandiri — dititipkan di validasi fractal

**[VALIDASI — 5 Agustus 2026, CLOSED]** **Versi kuatnya NOT SUPPORTED.** Dari **n=4 bear selesai**, jalur post-low cycle 2011 mencapai **2,72× cycle low dalam 60 hari** — cukup dekat ke bentuk V. Konsisten dengan `findings_post_bottom_rally_speed.md` (n=4 episode unlock, hari ke +50% berkisar 19–233 hari). Kecepatan pemulihan **cenderung** sangat bervariasi antar cycle; "tidak pernah V-shaped" terlalu kuat.
Detail: [`findings_fractal_overlay_dispersion.md`](findings_fractal_overlay_dispersion.md)

---

### [KONFIRMASI] Time-based capitulation vs price-based capitulation sebagai dua komponen terpisah
- **Insight:** "along with the price-based capitulation, there is a time-based capitulation element to Bitcoin bear markets that I do just still think we haven't quite endured yet" `[02:45]`–`[03:13]`. Definisi eksplisit di penutup: time-based capitulation = "genuinely just boring investors out of the market" — beda dari capitulation harga tipe "kita akan drop ke 40k, 30k" `[11:35]`–`[12:04]`
- **Indikator terkait:** durasi kalender bear (bukan indikator)
- **Relevan ke:** **K4 jalur lantai waktu**
- **Test klaim:** Sudah established dan sudah tervalidasi dalam bentuk yang lebih ketat (lantai waktu K4: ≥9 bulan sejak peak + close < RP, 3/3 bear searah). Versi video lebih longgar dan tidak menambah presisi. **Konsep sama, arah aksi berlawanan** — framework memakai waktu sebagai pemicu, video sebagai penahan (lihat STOP-1). Tema berulang di 3 sumber sebelumnya (`2026-07-02`, `2026-08-04`, `2026-06-09`).
- **Perlu validasi Claude Code:** Tidak — established & tervalidasi

### [KONFIRMASI] STH Realized Price sebagai level kunci yang diperhatikan pasar
- **Insight:** STH-RP ~$79.000 dianggap "key major resistance point"; harga menembusnya dari bawah dan itu yang memicu optimisme pasar `[00:01]`–`[00:55]`. Dia menganggap reclaim itu belum menyelesaikan apapun
- **Indikator terkait:** STH Realized Price (indikator aktif framework, batas zona)
- **Relevan ke:** batas ZD/Z3 & Signal D (K4 wrap-up)
- **Test klaim:** Sudah CLOSED di `2026-08-04` dengan hasil yang justru mengurangi bobotnya: dari n=13 sentuhan STH RP dari bawah selama bear (5 bear independen), 8 lolos Signal D dan **7 dari 8 (88%) palsu**. KB Price Level § 6.3 juga mencatat STH RP sebagai metrik dengan false signal terbanyak. Angka $79.000 dibaca dari narasi/frame → low confidence.
- **Perlu validasi Claude Code:** Tidak — established; verifikasi angkanya diserap ke validasi ex-post

**[VALIDASI — 5 Agustus 2026, CLOSED]** Angka video **akurat**: `sth_cost_basis` per 2026-05-14 = **$78.585** (video bilang ~$79.000). Ex-post, reclaim yang dirayakan pasar itu **hilang seluruhnya** — per 2026-07-15 harga $65.098 vs STH RP $67.143 (**0,970×, di bawah**), dan distribusi zona harian sejak video adalah **ZD 61 hari, Z3 1 hari**. **n=1 episode**, tapi persis sesuai pola yang sudah divalidasi di `2026-08-04`.
Detail: [`findings_expost_calibration.md`](findings_expost_calibration.md)

### [KONFIRMASI] Kesadaran eksplisit soal sample size kecil
- **Insight:** "'this has always happened' when 'always' is two or three different data samples. It's not a very extensive history we really have for comparisons" `[04:09]`–`[04:36]`; diulang `[10:10]`–`[10:39]`
- **Indikator terkait:** —
- **Relevan ke:** general (Governance butir 3)
- **Test klaim:** Sikap yang benar dan selaras framework. Tapi ada tension internal: dia mengakui "always is two or three samples" lalu tetap membangun tiga fractal overlay dan proyeksi tanggal di atas sample tiga itu. Pengakuan tidak menghapus kelemahan sample size — ia memindahkannya ke catatan kaki.
- **Perlu validasi Claude Code:** Tidak — bukan klaim empiris

### [KONFIRMASI] "Be strategic, be emotionless and react to the data"
- **Insight:** Prinsip reaktif-bukan-prediktif di penutup `[13:01]`, meski praktik di video ini sebagian besar prediktif (proyeksi fractal + tanggal makro)
- **Indikator terkait:** —
- **Relevan ke:** general
- **Test klaim:** Naratif, tidak falsifiable. Sudah dibahas di `2026-07-13` (channel yang sama).
- **Perlu validasi Claude Code:** Tidak — tidak testable

---

### [INDIKATOR CUSTOM] AASI (Active Address Sentiment Indicator) — dip di bawah upper deviation band sebagai sinyal bearish
- **Insight:** AASI "recently dipped back down beneath this upper deviation band, which historically has preceded some more bearish periods of price action" `[02:17]`–`[02:45]`; dipakai lagi sebagai pilar confluence bearish `[11:08]`, `[12:04]`
- **Komponen dasar:** 28-day Active Address Change vs 28-day Price Change + deviation bands — pada dasarnya spread antara momentum aktivitas jaringan 28 hari dan momentum harga 28 hari, dinormalisasi jadi band deviasi. Reading 4 Mei 2026 dari frame: price $79.824, 28d active address change 16,79%, 28d price change 15,82% (**low confidence dari resolusi frame**)
- **Indikator terkait:** active address (tidak ada di `data_master_all_metrics.csv`)
- **Relevan ke:** K1/K3 (sisi peringatan turun)
- **Test klaim:** Masalah terbesarnya bukan datanya, melainkan **falsifiability**. Channel yang sama memakai indikator yang sama untuk sisi BAWAH (cross ke atas lower band = bear low, video `2026-07-02`) dan sisi ATAS (dip di bawah upper band = bearish, video ini). Satu indikator yang bisa membenarkan dua arah dalam 7 minggu praktis tidak bisa salah, kecuali dispesifikasi lebih dulu kondisi mana yang berlaku kapan. Preseden negatif relevan: konsep "aktivitas jaringan sebagai sinyal" sudah diuji dua kali lewat `apparent_demand` dan REJECT dua-duanya.
- **Perlu validasi Claude Code:** **Tidak — data tidak tersedia** (active addresses eksplisit di daftar "Yang TIDAK ada di data kita")

### [INDIKATOR CUSTOM] "High Yield Credit: Bitcoin Cycles" — divergence HY bond price vs BTC
- **Insight:** Saat appetite terhadap high-yield corporate bond naik (risk-on di TradFi), itu berbarengan dengan — dan menurutnya mungkin jadi kausa — periode bullish BTC. Belakangan terjadi divergence: HY credit mulai turun sementara BTC naik `[04:09]`–`[05:03]`, diulang `[11:08]`, ditampilkan lagi `[12:00]`+
- **Komponen dasar:** BTC price vs High Yield Corporate Bond Price, dipotong per "epoch" siklus (chart proprietary bitcoinmagazinepro.com; definisi epoch tidak diungkap)
- **Indikator terkait:** kredit HY (macro), tidak ada padanan di framework
- **Relevan ke:** general
- **Test klaim:** Dua cacat serius. Pertama, kata "causation" dipakai eksplisit untuk pola visual tanpa satupun uji — kesalahan kategori, bukan sekadar bahasa longgar. Kedua, karena definisi "epoch" dirahasiakan, klaimnya **tidak bisa direplikasi dan tidak bisa difalsifikasi siapapun di luar channel** — segmentasi yang bisa dipilih bebas adalah alat paling ampuh untuk membuat divergence apapun terlihat bermakna.
- **Perlu validasi Claude Code:** **Tidak — data tidak tersedia**

### [INDIKATOR CUSTOM] DXY Year-on-Year, di-invert, dengan 100-day forward offset
- **Insight:** Chart "expert bundle" TradingView: DXY YoY, dibalik, lalu di-offset 100 hari ke depan sebagai proksi leading BTC. Klaim: chart ini sudah beberapa minggu menunjuk "bear market rally into mid-May", dan "almost to the exact day" — highest closing price BTC 10 Mei 2026 berhimpit dengan puncak data point ini `[05:03]`–`[06:25]`
- **Komponen dasar:** DXY level → YoY → invert → shift +100 hari. Ketiga parameter adalah pilihan tuning
- **Indikator terkait:** DXY (macro)
- **Relevan ke:** general
- **Test klaim:** Klaim "berhimpit almost to the exact day" adalah **n=1 koinsidensi tunggal** yang dipresentasikan sebagai presisi. Dengan tiga derajat kebebasan (basis YoY, invert, offset 100 hari — kenapa 100 dan bukan 90 atau 120?), menemukan satu kecocokan tanggal hampir dijamin oleh konstruksi. Uji yang jujur harus menetapkan parameter a priori lalu mengukur akurasi di SEMUA puncak/palung historis.
- **Perlu validasi Claude Code:** **Tidak — data tidak tersedia** (DXY tidak ada di dataset); arah prediksinya diserap ke validasi ex-post

**[VALIDASI — 5 Agustus 2026, CLOSED]** Arah call-nya **kena**, klaim presisinya **tidak**. Harga memang topping tepat di sekitar tanggal video (close tertinggi setelah 14 Mei hanya $79.064 @ 15 Mei — tidak pernah lagi melampaui close hari video) lalu turun −9,2%/−21,6%/−26,7%/−21,8% di +2/4/6/8 minggu. Tapi highest close di window ±30/45/60/90 hari jatuh pada **11 Mei 2026 ($81.868)**, **bukan 10 Mei** — selisih satu hari, tidak material untuk arah tapi relevan karena presisi "to the exact day" adalah bagian dari argumennya. **n=1 episode.**
Detail: [`findings_expost_calibration.md`](findings_expost_calibration.md)

### [INDIKATOR CUSTOM] Global M2 rate-of-expansion/contraction sebagai leading indicator
- **Insight:** Versi rate-of-change dari global M2 disebut "incredibly predictive chart for upcoming price appreciation or depreciation", dan juga memuncak sekitar mid-Mei 2026 sebelum "multiple weeks of somewhat bearish downside price action" `[06:25]`–`[07:20]`
- **Komponen dasar:** Global M2 aggregate → laju perubahan; offset (kalau ada) tidak disebut angkanya
- **Indikator terkait:** global liquidity (macro)
- **Relevan ke:** general
- **Test klaim:** "Incredibly predictive" tanpa n, tanpa definisi lead time, tanpa daftar kegagalan. Dua indikator makro yang memberi tanggal puncak identik (mid-Mei) adalah petunjuk kuat bahwa keduanya mengukur hal yang sama — kondisi likuiditas USD — memperkuat kecurigaan double-counting di pilar confluence.
- **Perlu validasi Claude Code:** **Tidak — data tidak tersedia**

### [INDIKATOR CUSTOM] Metode bar-pattern fractal overlay (post-low, n=3)
- **Insight:** Alih-alih mengukur waktu dari ATH, dia mengukur **waktu sejak low ditetapkan**: ambil price action setelah lowest closing price bear sebelumnya, salin sebagai "bar pattern", tempel ke low 2026 `[07:45]`–`[08:16]`. Hasilnya: **2022** → naik ke mid-$90.000, resistance di 1-year MA, balik ke mid-$70.000 dalam ~1 bulan, rally sungguhan pertengahan Juni `[08:16]`–`[09:13]`; **2018-19** → tidak break convincing sampai pertengahan Juni `[09:13]`–`[09:42]`; **2015** → chop berulang Jun–Okt, break di atas ~$100.000 baru November 2026 `[09:42]`–`[10:10]`
- **Indikator terkait:** price action fractal, tidak ada di framework
- **Relevan ke:** K4 (timing bottom/akumulasi), K5
- **Test klaim:** Cacat fatalnya bukan n=3, tapi **anchor-nya baru diketahui setelah fakta**. Overlay butuh tahu di mana low-nya; kalau low-nya belum pasti, seluruh proyeksi bergeser. Tambahan: channel yang sama memakai anchor BERBEDA (initial shock → secondary low) tujuh minggu kemudian di `2026-07-02` — anchor yang bisa dipilih bebas = metode yang tidak bisa salah. Ketiga fractal juga saling bertentangan (rally mid-Juni vs chop sampai November), sehingga hampir semua outcome bisa diklaim "sesuai salah satu fractal".
- **Perlu validasi Claude Code:** Ya — uji METODE-nya, bukan salah satu fractal

**[VALIDASI — 5 Agustus 2026, CLOSED]** **NOT SUPPORTED — hasil negatif yang kuat.** Dari **n=4 bear selesai** (2011, 2013-15, 2017-19, 2021-23; satu per cycle, plus 2025-26 yang censored), jalur post-low ternormalisasi tersebar **1,20×–2,08× di t+90** (max/min 1,74×; di t+60 bahkan 2,45×), dan korelasi Pearson log-return harian antar jalur punya **median −0,017** (6 pasang, rentang −0,145 s/d +0,176) — praktis tidak berkorelasi. Ex-post, **anchor video sudah tertembus**: low Feb 2026 = $62.840 @ 2026-02-05, tapi harga membuat low $58.460 @ 2026-06-30 (−7,0%). Pada t+120 harga aktual **0,98× anchor** sementara keempat fractal memproyeksikan 1,33×–2,54× — **tidak ada satupun yang mendekati**. Hasil ini reusable untuk menilai klaim fractal-overlay dari sumber manapun ke depan.
Detail: [`findings_fractal_overlay_dispersion.md`](findings_fractal_overlay_dispersion.md)

---

### [STRATEGI] Bottom-call probabilistik dipisah dari keputusan entry
- **Insight:** ">50% chance that $60,000 was the lowest price we'll see" dan "the lows are in" — TAPI "I'm not buying here" `[02:45]`–`[03:13]`. Judul video sebelumnya dikutip persis: "Bitcoin's Bottom Is In… But I'm Not Buying Here". Dia menyadari sendiri ini terdengar kontradiktif
- **Indikator terkait:** —
- **Relevan ke:** K4 (aktivasi akumulasi)
- **Test klaim:** Secara metodologis pemisahan forecast dari aksi itu sehat. Masalahnya, kombinasi ">50% chance $60k adalah low" + "saya tidak beli di sini" menciptakan posisi yang **tidak bisa kalah secara retoris**: kalau harga naik ia benar soal bottom, kalau turun ia benar soal tidak beli. Nilai prediktifnya nol tanpa kriteria gagal eksplisit.
- **Perlu validasi Claude Code:** Ya — diserap ke validasi ex-post

**[VALIDASI — 5 Agustus 2026, CLOSED]** Sisi bottom-call **meleset tipis**, sisi "jangan beli di sini" **kena**. Harga tidak pernah lagi melampaui close hari video, dan turun −27,9% ke low $58.460 @ 2026-06-30 — jadi menahan beli terbukti tepat untuk episode ini. Tapi karena kedua sisi klaimnya dirancang tidak bisa kalah bersamaan, hasil ini **tidak bisa dibaca sebagai skill**. **n=1 episode.**
Detail: [`findings_expost_calibration.md`](findings_expost_calibration.md)

### [STRATEGI] Distribusi probabilitas eksplisit: 20–25% skenario mid-$50k
- **Insight:** "I think there's about a 20 to 25% chance that we could go around into the mid-$50,000 region. But I still think the base case is a $60,000 low" `[07:03]`–`[07:20]`
- **Indikator terkait:** —
- **Relevan ke:** Z1/ZC floor
- **Test klaim:** Menyebut probabilitas eksplisit lebih baik daripada bahasa kabur, tapi klaim probabilistik dengan satu realisasi tidak bisa di-score — kita cuma bisa mencatat arahnya.
- **Perlu validasi Claude Code:** Ya — diserap ke validasi ex-post

**[VALIDASI — 5 Agustus 2026, CLOSED]** **Base case pecah, skenario ekor terjadi.** Minimum close setelah video = **$58.460 @ 2026-06-30** → $60.000 tertembus (3 hari close di bawahnya, 25–30 Juni), dan ketiganya jatuh di rentang mid-$50k ($55.000–$59.999) — yaitu **skenario yang dia beri probabilitas 20–25% justru yang terealisasi**. Tidak ada close < $55.000. Anchor "low Februari ~$60k" sebenarnya $62.840, jadi tertembus −7,0%. Miss-nya kecil (−2,6% di bawah angka yang disebut, hanya 3 hari) — kalibrasi **wajar**, bukan miss besar. **n=1 episode.**
Detail: [`findings_expost_calibration.md`](findings_expost_calibration.md)

### [STRATEGI] DCA agresif di sekitar $70.000 — framing "win-win"
- **Insight:** "I either get some cheaper prices to continue aggressively dollar cost averaging in around hopefully that $70,000 region, or my Bitcoin stack is worth considerably more and we start marching higher" `[12:32]`–`[13:01]`
- **Indikator terkait:** —
- **Relevan ke:** K4 (DCA rate)
- **Test klaim:** Anchor harga absolut — persis pendekatan yang framework tolak, karena $70.000 tidak punya makna struktural apapun (bukan RP, bukan STH RP, bukan AVIV). Framing "win-win" juga menyembunyikan skenario kalah nyata: harga jatuh jauh di bawah $70.000 dan bertahan lama = beli terlalu awal dengan stack yang nilainya turun. Bandingkan lantai waktu K4 yang memakai pemicu struktural dengan sizing kecil (5%/bulan) justru supaya ada cadangan untuk double bottom.
- **Perlu validasi Claude Code:** Ya (bagian ex-post) — perbandingan sistematis DCA anchor-harga vs DCA lantai waktu masuk **backlog**

**[VALIDASI — 5 Agustus 2026, CLOSED]** Level tersentuh, **timing-nya belum terbukti menguntungkan**. Sentuhan pertama close ≤ $70.000 pada **2026-06-02 @ $66.699** (total 44 hari close ≤ $70.000 s/d akhir data). Forward return **30 hari: −7,4%** ($61.793 @ 2026-07-02). Forward return 60 hari **BELUM TERTUTUP (PARTIAL)** — data berakhir 2026-07-15, baru 43 hari, sejauh ini −2,4%. Jadi harga memberi level yang dia mau lalu terus turun ~7% lagi — persis skenario yang framing "win-win" tidak akui sebagai kekalahan. **n=1 episode.**
Detail: [`findings_expost_calibration.md`](findings_expost_calibration.md)

### [STRATEGI] Tesis siklus: "mini bear market" musim panas 2026, bukan bear setahun penuh
- **Insight:** Merujuk prediction video akhir 2025: mereka mengantisipasi "almost a mini bear market throughout the summer of 2026", bukan bear panjang tradisional `[07:20]`–`[07:49]`. Sekaligus menolak konsensus yang menargetkan bottom September–Oktober 2026 `[03:42]`–`[04:09]`
- **Indikator terkait:** 4-year cycle framing
- **Relevan ke:** general / K4–K5 timing
- **Test klaim:** Falsifiable tapi **belum jatuh tempo** — Sep–Okt 2026 masih di depan. Yang bisa dicatat sekarang cuma konsistensi internal: menyebut "mini bear" sambil menampilkan fractal 2015 yang berujung breakout baru November 2026 adalah dua tesis yang sulit dipegang bersamaan.
- **Perlu validasi Claude Code:** Ya — **belum diuji, backlog** (forward test; cek ulang setelah Oktober 2026)

### [STRATEGI] Confluence lintas-domain sebagai dasar sikap
- **Insight:** Sikap "cool off ahead" dibangun dari 5 pilar sekaligus: high yield credit divergence + DXY YoY + global M2 rate-of-change + AASI + technical resistance. Sambil tetap menyatakan "I'm still very bullish, but I just think we need to not get ahead of ourselves" `[11:08]`–`[11:35]`
- **Indikator terkait:** gabungan macro + custom on-chain + TA
- **Relevan ke:** general — **lihat STOP-2**
- **Test klaim:** Masalah utamanya **independensi**: HY credit spread, DXY, dan Global M2 semuanya ekspresi kondisi likuiditas/risk appetite USD; menghitungnya sebagai tiga bukti terpisah melebih-lebihkan keyakinan. Framework punya padanan disiplin di Governance butir 1 (uji independensi |phi| < 0,3) — confluence video ini tidak akan lolos lapis itu.
- **Perlu validasi Claude Code:** **Tidak — data tidak tersedia** untuk 4 dari 5 pilar; uji independensinya secara teknis tidak bisa dijalankan

### [STRATEGI] "This time is looking like it could be different, but not drastically different"
- **Insight:** Posisi tengah: mengakui cycle ini beda (tidak butuh drawdown −75/−85%), tapi menolak kesimpulan bahwa pola strukturalnya hilang seluruhnya `[11:35]`–`[12:04]`
- **Indikator terkait:** —
- **Relevan ke:** general
- **Test klaim:** Tidak falsifiable dalam bentuk apapun — kedua arah outcome kompatibel dengan pernyataan ini. Berguna sebagai sikap hati-hati, nol nilai prediktif.
- **Perlu validasi Claude Code:** Tidak — tidak testable

---

### [KONFLIK] Menunda akumulasi karena "time-based capitulation belum selesai"
- **Insight:** Dia percaya harga terendah kemungkinan besar sudah lewat, tapi menahan pembelian karena komponen waktu belum terpenuhi — akumulasi baru dilakukan kalau harga balik ke ~$70k `[02:45]`, `[12:32]`
- **Konflik dengan:** K4 jalur lantai waktu (Decision Framework v2 § K4) — ≥9 bulan sejak cycle peak DAN close < RP → DCA 5% cash pool/bulan **berjalan otomatis walau count <2**, spot only
- **Alasan konflik:** Framework dan video memakai observasi yang sama (bear punya dimensi waktu, bukan cuma harga) tapi menariknya ke aksi yang berlawanan. Framework: waktu berlalu = **izin mulai beli**, karena menunggu konfirmasi sempurna terbukti membuat framework diam dari $5k ke $60k (kasus 2020). Video: waktu belum cukup berlalu = **alasan menahan beli**. Framework sengaja membuang keputusan diskresioner "tunggu dulu" — `findings_time_floor_validation.md`: beli rata-rata +8–18% lebih mahal, tapi 10–15× lebih banyak hari deploy
- **Rekomendasi:** **Diskusikan dengan Yudi (STOP-1)** — bukan untuk mengubah K4, tapi untuk memastikan narasi eksternal seperti ini tidak dipakai sebagai alasan menunda DCA nanti. **Catatan koreksi dari validasi:** lantai waktu K4 **belum aktif** per akhir data (syarat waktu terpenuhi sejak 2026-07-06, syarat `close < RP` belum — butuh turun ~19% lagi), jadi konfliknya masih filosofis, belum operasional

### [KONFLIK] 365-day / 1-year MA sebagai "deciding point antara bull dan bear"
- **Insight:** Muncul empat kali. Kutipan on-screen dari video 10 hari sebelumnya: "A convincing break above the 365 day moving average would seal it for me" `[01:58]`–`[02:15]`. Lalu "it would reach resistance at this one-year moving average, historically what I would consider the almost dictating deciding point between bull and bear markets" `[08:16]`–`[08:45]`, diulang `[09:13]`–`[09:42]` dan `[13:01]`
- **Konflik dengan:** Decision Framework v2 § 0 — "**Status bear berakhir (unlock): STH RP cross naik melewati RP** (masuk Z2) — BUKAN saat harga balik ke Z5". Kriteria **ordering antar level cost-basis**, bukan posisi harga terhadap MA teknikal
- **Alasan konflik:** Kalau 365 DMA diadopsi sebagai penentu regime, definisi bear-end bergeser dari struktur cost-basis ke posisi harga. Bedanya dengan konflik serupa sebelumnya: kali ini **sudah ada jawaban empirisnya**. Validasi `2026-08-04`: 365D MA reclaim jatuh **koinsiden** dengan unlock struktural (+12/+4/−13 hari di 3 cycle modern) — tidak menambah lead time sama sekali; sementara 200D MA reclaim mendahului unlock 23–51 hari (4/4, `2026-07-02`). Jadi MA yang dipilih video sebagai "deciding point" justru yang paling tidak berguna dari dua MA yang tersedia
- **Rekomendasi:** **Abaikan sebagai usulan perubahan § 0** — sudah diuji dua kali dan gagal menambah nilai. Simpan sebagai confirming context lambat saja. Tidak perlu diskusi ulang kecuali Yudi ingin

### [KONFLIK] Threshold absolut sebagai anchor keputusan ($81–85k, $70k, $60k, $100k)
- **Insight:** Hampir semua level keputusan di video ini adalah harga absolut: resistance $81–85k, DCA trigger $70k, base-case low $60k, skenario mid-$50k, breakout target $100k (fractal 2015)
- **Konflik dengan:** Prinsip utama framework ("threshold absolut tidak reliable antar cycle — framework pakai pola relatif") + Governance butir 3
- **Alasan konflik:** Level harga USD tidak punya arti struktural lintas cycle dan tidak bisa dipetakan ke zona ZC/ZD/Z1–Z5 tanpa dikonversi ke rasio terhadap cost-basis (Price/RP, Price/STH, Price/CVDD). Konsekuensi konkretnya sudah terlihat dari validasi: base case "$60.000 low" tertembus akhir Juni 2026 — dan karena anchor-nya angka mati, tidak ada mekanisme adaptasi selain merevisi angkanya secara manual
- **Rekomendasi:** **Abaikan sebagai anchor keputusan.** Catat angkanya sebagai konteks pembacaan sumber saja. Kalau mau dipakai, konversi dulu ke rasio cost-basis lalu bandingkan ke tabel KB Price Level § 2.7 (bear bottom: Price/CVDD 0,98–1,16, Price/RP 0,70–0,91)

---

## Flag Prioritas

1. **Filter 200 DMA untuk Signal D** — validasi V2 menemukan bahwa memasang syarat "harga di atas 200 DMA pada hari ke-3 break STH RP" menyingkirkan **7 dari 7 break palsu tanpa membuang 1 break asli** (n=8 event, 5 cycle), menaikkan hit rate Signal D dari 12% ke 100%. Ini menjawab langsung Flag Prioritas #1 yang masih terbuka dari analisis `2026-08-04`. Tapi sisi "meloloskan yang asli" bersandar pada **n=1** — perlu diputuskan apakah cukup kuat untuk diusulkan sebagai perubahan Signal D, atau dicatat dulu sebagai kandidat.

2. **STOP-1: waktu sebagai penahan vs pemicu** — konflik filosofis dengan K4 lantai waktu. Belum operasional (lantai waktu belum aktif: butuh close < RP, masih 1,23×), tapi akan jadi relevan begitu harga turun ~19% lagi. Perlu kejelasan sikap sebelum itu terjadi, bukan sesudah.

3. **"Confluence" STH RP + 200 DMA adalah pengukuran ganda** — r ≈ +0,999 selama bear. Ini bukan cuma soal video ini; ini pola yang akan berulang tiap kali sumber manapun menyebut "dua indikator konfirmasi bersamaan" untuk dua metrik yang sama-sama turunan harga. Layak jadi refleks pengecekan standar.

4. **Metode fractal overlay sudah difalsifikasi — hasilnya reusable** — dispersi 1,20×–2,08× di t+90 dan korelasi log-return median −0,017 (n=4 bear). Klaim fractal-overlay dari sumber manapun ke depan bisa dinilai cepat dengan merujuk ke sini, tanpa validasi ulang. Worth dicatat sebagai referensi tetap.

5. **Kalibrasi Bitcoin Magazine Pro** — ini video BMP ke-8 di repo. Pola yang mulai konsisten dari tiga validasi ex-post: **arah/konteks makronya cenderung berguna, angka absolut dan klaim presisinya tidak.** Worth dipertimbangkan sebagai aturan baca tetap untuk channel ini.

6. **AASI dipakai dua arah dalam 7 minggu** — sisi bawah di `2026-07-02`, sisi atas di video ini. Datanya tidak tersedia jadi tidak bisa diuji, tapi pola "satu indikator membenarkan dua arah" layak dicatat sebagai tanda bahaya saat membaca channel ini.

---

## Yang Langsung Diabaikan

- **Promo Bitcoin Vegas, publikasi Bitcoin Magazine, interview & news desk mendatang** `[13:35]`–`[14:21]` — sponsor/promo, tidak ada isi analitis
- **Ajakan komentar & social media** `[14:21]`–`[14:36]`
- **Narasi "saya dapat banyak hate saat bilang X"** `[13:01]`–`[13:28]` — social proof / track-record framing tanpa mekanik. Satu-satunya bagian substantifnya (referensi break di bawah 1-year MA) sudah diserap ke KONFLIK 365 DMA
- **"we got close to this 200-weekly moving average"** `[01:23]`–`[01:51]` — dari data, 200-week MA per 2026-05-14 = $60.964, jauh **di bawah** harga $81.060. Kemungkinan slip lisan; tidak dipakai sebagai klaim
- **Observasi "people are starting to get more bullish/optimistic"** sebagai item berdiri sendiri — tidak ada metrik sentimen yang diukur; sudah tercakup di AASI yang punya mekanik
- **Sapaan pembuka & filler auto-caption** ("I worded that terribly", "[clears throat]", "tomfoolery", "the cruel mistress Bitcoin")

---

## Catatan data & keterbatasan

- **Data master berakhir 2026-07-15** — 62 hari setelah tanggal video. Window 8 minggu tertutup; forward return 60 hari dari sentuhan awal Juni **belum tertutup (PARTIAL)**
- **Angka low confidence dari resolusi frame** (tidak dipakai sebagai anchor kesimpulan): STH-RP $79.000 · reading AASI 16,79% / 15,82% · 200-week MA ~$57k · Global M2 ~$103T · drawdown −35% · durasi 600–800 hari · spike fractal 2022 ~$95k · fractal 2015 menyentuh ~$50-an ribu
- **Tidak bisa divalidasi sama sekali — data tidak tersedia:** DXY, DXY YoY, Global M2, active addresses (AASI), harga obligasi korporat HY. Semuanya di daftar "Yang TIDAK ada di data kita" (`data_dictionary.md`). Ini **backlog data**, bukan backlog validasi
- **Backlog validasi:** (a) forward test tesis "mini bear market" / konsensus bottom Sep–Okt 2026 — cek ulang setelah Oktober 2026; (b) perbandingan sistematis DCA anchor-harga vs DCA lantai waktu K4
