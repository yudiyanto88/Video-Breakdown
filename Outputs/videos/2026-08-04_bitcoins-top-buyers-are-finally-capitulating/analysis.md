# Bitcoin's Top Buyers Are Finally Capitulating
**Channel:** On-Chain Mind
**Tanggal video:** 4 Agustus 2026
**Tanggal analisis:** 4 Agustus 2026
**Link:** https://www.youtube.com/watch?v=BSFH8tFR2-k

*Tidak ada flag STOP. Video tidak menyinggung leverage, loan, atau LTV sama sekali — nol konflik dengan hard constraint. Arsitekturnya juga tidak fundamental berbeda: ia memakai keluarga metrik yang sama (cost basis + SOPR) dan kesimpulan operasionalnya ("akumulasi di zona capitulation, jangan kejar rally") selaras K4. Ada satu konflik lunak di level trigger — lihat [KONFLIK] X1.*

---

## Ringkasan

Video 12 menit yang argumennya bertumpu pada satu kohort: holder yang membeli 6–12 bulan lalu — dengan kata lain, pembeli puncak siklus. Pembicara membuka dengan tiga level regime miliknya (STH Realized Price $66.000, 200D MA, 365D MA $85.000) dan menyatakan bear terkonfirmasi di ~$102.000 pada November 2025 saat harga cross ke bawah yearly MA. Lalu ia menunjukkan cost basis heatmap: median cost basis 1 tahun ada persis di $64.000, harga yang terasa "nyangkut" belakangan ini — level yang menekan dari dua sisi karena di bawahnya holder rata-rata setahun merah dan menjual rally, di atasnya hijau dan membeli dip.

Inti videonya ada di paruh kedua: SOPR yang difilter khusus ke kohort 6m–1y. Reading-nya 16th percentile terhadap seluruh sejarah, dengan posisi hari ini di SOPR 0,635 — koin keluar dengan realized loss 36%. Distribusi frekuensi hariannya trimodal: klaster capitulation tempat kita sekarang (~0,60–0,65), klaster rugi ringan (~0,9) dari early top buyers yang keluar di $85–90.000 saat drop 30% pertama, dan klaster profit-taking (>1,15) dari yang beli sebelum puncak lalu jual ke dalam puncak. Versi kumulatifnya membaca ~70% hari setahun terakhir kohort ini menjual rugi, dan posisi hari ini di persentil 19% dari window setahun.

Kesimpulannya: di tiga bear terakhir kohort ini underwater rata-rata 13 bulan sebelum flip balik ke profit, dan flip itu menandai resumsi bull. Mulai underwater November 2025 → proyeksi capitulation selesai sekitar Desember 2026. Pembicara menutup dengan menegasikan presisinya sendiri: "I'm not looking for exact dates or exact prices."

Tiga validasi dijalankan. Hasilnya konsisten: **sumbernya sangat akurat di sisi fakta** (klaim $102.000 Nov 2025 reproduce persis di 2025-11-12 @ $101.695; kohort mulai underwater 2025-11-14 @ $94.668 vs klaim ~$95.000; durasi 3 bear terakhir mean 13,5 bulan vs klaim 13 bulan), **tapi dua metrik "baru" yang ditawarkannya tidak mengisi celah apapun** — flip kohort dan 365D MA reclaim sama-sama koinsiden-atau-lagging terhadap unlock struktural framework. Temuan paling actionable justru datang dari klaim sampingannya: STH RP memang berperilaku resistance di bear, dan angkanya menunjukkan **Signal D punya hit rate ~12%** sebagai penanda pembalikan asli.

---

## Insight Inventory

### [BARU] Kohort 6m–1y underwater rata-rata 13 bulan; flip menandai resumsi bull
- **Insight:** Kohort holder 6 bulan–1 tahun adalah pembeli puncak yang bertahan lewat sebagian besar ekstremitas bear. Di tiga bear terakhir kohort ini underwater rata-rata 13 bulan sebelum harga balik ke atas cost basis mereka, dan momen flip itu menandai resumsi bull market. Kohort ini mulai underwater November 2025 di ~$95.000 → proyeksi ~Desember 2026 `[03:31]`–`[04:16]`, `[11:40]`–`[11:57]`
- **Indikator terkait:** Realized Price kohort 6m–12m (age-banded)
- **Relevan ke:** K4 selesai / K5 mulai — dan kandidat penanda unlock-bear alternatif. Catatan: kohort 6–12 bulan seluruhnya berada **di dalam** cohort LTH framework (>155 hari); framework tidak punya resolusi apapun di dalam LTH
- **Test klaim:** n=3 (batas bawah yang framework anggap layak) dan "rata-rata 13 bulan" tanpa sebaran hampir tidak berguna untuk timing. Risiko sirkularitas: kalau bear berlangsung ~1 tahun, kohort yang beli di puncak otomatis kembali profit sekitar saat bear berakhir — "flip menandai resumsi bull" berpotensi tautologi (mendefinisikan ulang akhir bear, bukan memprediksinya). Uji pembedanya harus lead/lag terhadap unlock struktural. Bukan threshold absolut (pola relatif berbasis durasi) sehingga lolos aturan CLAUDE.md
- **Perlu validasi Claude Code:** Ya — durasi per episode + lead/lag terhadap unlock struktural + forward return vs baseline

**[VALIDASI — 4 Agustus 2026, CLOSED]** Rekonstruksi cohort 6m-12m RP dari HODL-wave band lolos sanity gate (rasio 1,90× RP; episode terakhir mulai 2025-11-14 @ $94.668 — persis klaim video). Durasi: 3 bear terakhir 10,9 / 14,7 / 14,9 bulan, mean 13,5 bulan (**n=3, spread 4 bulan**) — klaim "13 bulan" cocok, tapi rentang implied flip yang jujur adalah **Okt 2026 – Feb 2027**, bukan titik "Des 2026". Klaim intinya TIDAK LOLOS: di **n=4** pasangan (2011, 2014-15, 2018-19, 2022-23) flip cenderung **terlambat** dari unlock struktural (median −13 hari mentah, −26 hari versi terkonfirmasi; 0/4 leading di versi yang realistis dipakai live), kalah dari 200D MA reclaim yang mendahului unlock 23–51 hari konsisten 4/4. Forward return dari flip (n=5) di atas baseline tapi tipis (+130,8% vs baseline +99,7% di 365d). Pakai sebagai kalender/konteks, bukan trigger.
Detail: [`findings_cohort_6m12m_realized_price.md`](findings_cohort_6m12m_realized_price.md)

### [BARU] Regime filter 3-level: STH RP + 200D MA + 365D MA
- **Insight:** Harga di ATAS ketiganya = bull hidup; di BAWAH ketiganya = bear kembali. Bear terkonfirmasi ~$102.000 November 2025 saat cross ke bawah yearly MA, "and just closed the argument altogether". Urutan reclaim yang diklaim: STH RP dulu ($66.000), baru 365D MA ($85.000) `[00:33]`–`[01:03]`, `[10:33]`–`[10:49]`
- **Indikator terkait:** STH Realized Price, 200D MA, 365D MA
- **Relevan ke:** Status Pasar § 0 (alarm bear CEPAT & PRESISI), K5
- **Test klaim:** Sisi naik sudah tervalidasi sebagian (200D MA reclaim, CLOSED 2026-07-28: lead 23–51 hari ke unlock, n=4, tapi jarak lead tidak konstan). Titik lemah utama: MA panjang secara mekanis lagging — "bear terkonfirmasi di $102.000" berarti konfirmasi datang setelah drawdown ~18% dari puncak, sementara alarm bear CEPAT framework bunyi +4 hari setelah peak Okt 2025. Kalau jauh lebih lambat, nilainya bukan alarm melainkan penegas rendah-false-positive. Bukan threshold absolut (MA adaptif per cycle)
- **Perlu validasi Claude Code:** Ya — sisi turun (lag & drawdown per cycle), false positive (khususnya Mei 2021 & Mar 2020), urutan reclaim

**[VALIDASI — 4 Agustus 2026, CLOSED]** Filter 3-level bersih tapi lambat. Sisi turun: **n=5 cycle**, median lag **119 hari** setelah peak (rentang 37–258) dengan drawdown −18,5% s/d −83,5%; klaim spesifik video "bear terkonfirmasi ~$102.000 Nov 2025" terkonfirmasi persis (2025-11-12 @ $101.695), tapi tertinggal 33 hari di belakang alarm bear CEPAT framework (+4 hari, Okt 2025). False positive: 0 dari 20 event — tapi 20 event itu cuma **6 klaster bear independen**, dan filter ini **lolos ujian Mei 2021** (hanya 2 hari dari 123 di bawah ketiga level) sementara COVID Mar 2020 nyala lalu diikuti +545% dalam 365 hari. Median forward return 365 hari dari sinyal = +70,5%, jadi terlalu telat untuk dipakai keluar. Urutan reclaim yang diklaim (STH RP dulu, baru 365D MA) terkonfirmasi 4/4, tapi 365D MA reclaim jatuh **koinsiden dengan unlock struktural** (+12/+4/−13 hari di 3 cycle modern) sehingga tidak menambah lead time. Pakai sebagai veto/konfirmator kelas berat, bukan alarm.
Detail: [`findings_regime_filter_3_level.md`](findings_regime_filter_3_level.md)

### [BARU] STH Realized Price berfungsi sebagai RESISTANCE, bukan support, saat bear
- **Insight:** Di bear market STH RP sering jadi resistance ketimbang support, karena pembeli baru sedang underwater; begitu harga rally balik ke level yang mereka bayar, banyak dari mereka pakai kesempatan itu keluar di break-even. Setiap rally ke arah level ini harus diperlakukan hati-hati `[01:17]`–`[01:44]`
- **Indikator terkait:** STH Realized Price
- **Relevan ke:** ZD (batas atas zona), **Signal D** (harga > STH RP ≥3 hari = syarat wrap-up K4 → Z1b), aturan unlock bear
- **Test klaim:** Video menyajikannya sebagai regularitas tanpa satupun angka pendukung — tidak ada hit rate, jumlah episode, atau definisi "rally ke level itu". Dalam bentuk sekarang nyaris tidak bisa salah: di bear, harga per definisi di bawah STH RP, jadi setiap rally yang gagal otomatis "membuktikan" resistance sementara rally yang berhasil di-reframe jadi "unlock". Supaya falsifiable harus dikuantifikasi: berapa persen sentuhan STH RP dari bawah yang ditolak vs berhasil break. Konsisten dengan Price_Level KB § 6.3 (60 episode breach terpisah dalam 10 tahun)
- **Perlu validasi Claude Code:** Ya — hit rate break vs ditolak per cycle, biaya salah baca, dan berapa break yang benar-benar diikuti unlock struktural

**[VALIDASI — 4 Agustus 2026, CLOSED]** Klaim terkonfirmasi kuat dan langsung mengkalibrasi Signal D. Dari **n=13 event** "sentuhan STH RP dari bawah" selama bear (sebaran: 2011:1, 2013:3, 2017:4, 2021:3, 2025:2 — cycle 2025 masih berjalan/censored; hanya **5 bear independen**), 8 lolos definisi Signal D (close >STH RP ≥3 hari) tapi **7 dari 8 (88%) balik ke bawah STH RP dalam 90 hari dan hanya 1 dari 8 (12%) diikuti unlock struktural dalam 90 hari**. Event yang DITOLAK (n=5) menderita drawdown 30 hari median −24,2% (terburuk −47,4%); bahkan event BREAK pun median return 30 harinya −3,4%. Menaikkan syarat persistensi saja tidak menyelamatkan — break 31 hari (2011) dan 20 hari (2015) tetap gagal. Usulan: Signal D jangan dipakai sendirian untuk wrap-up K4 → Z1b, pasangkan dengan 200D MA reclaim.
Detail: [`findings_sth_rp_resistance_bear.md`](findings_sth_rp_resistance_bear.md)

### [BARU] One-year MEDIAN cost basis sebagai level "termacet"
- **Insight:** Median cost basis 1 tahun ada di $64.000 — persis harga yang terasa nyangkut sekarang. Median = titik di mana 50% koin diakuisisi di bawahnya dan 50% di atasnya. Level seperti ini bertindak sebagai support DAN resistance sekaligus: di bawahnya holder rata-rata setahun terakhir merah → rally dijual untuk balik modal; di atasnya hijau → dip dibeli untuk mempertahankan posisi. Pembicara menyebutnya "the fairest price in the market right now" `[02:30]`–`[03:31]`, `[11:07]`–`[11:24]`
- **Indikator terkait:** 1-Year Median Cost Basis (dari cost basis heatmap / distribusi UTXO)
- **Relevan ke:** general + zone structure — framework seluruhnya pakai cost basis **rata-rata** (RP, STH RP, LTH RP = realized cap / supply); median 1 tahun statistik berbeda dari keluarga yang sama
- **Test klaim:** Argumennya sirkular dan n=1. Video mengamati harga nyangkut di $64.000, menemukan median juga di $64.000, lalu menyimpulkan yang satu menjelaskan yang lain — tanpa contoh historis lain dan tanpa tes bahwa harga memang cenderung mengorbit level ini lebih lama dibanding level acak. Masalah kedua: median 1 tahun adalah kuantitas **bergerak yang ditarik ke arah harga** (kalau harga chop lama di $64k, koin yang baru dipindahkan menumpuk di sana dan median ikut turun ke sana) — jadi kolokasi harga-dan-median sebagian besar bisa artefak mekanis, bukan sebab-akibat
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog, **hanya lewat proxy**. Data median tidak tersedia (butuh distribusi UTXO penuh). Proxy yang mungkin: "1-year MEAN cost basis" dari penjumlahan band `realized_cap_*` / `supply_*` (0-1d s/d 6m-12m) — tapi mean ≠ median, dan justru di distribusi bimodal seperti bear ini bedanya paling besar, jadi hasil apapun tidak menjawab klaim aslinya secara langsung

### [BARU] Kohort 6m–1y berperilaku beda dari LTH agregat ("bukan holder terpintar")
- **Insight:** Pembicara eksplisit membedakan kohort ini dari veteran: "these aren't likely the seasoned veterans who have been around a cycle or three... they're not exactly the smartest holders and I think they're the ones that we would expect to capitulate" `[05:46]`–`[06:02]`
- **Indikator terkait:** SOPR kohort 6m–1y vs LTH-SOPR agregat
- **Relevan ke:** **K4 kondisi #2** (aSOPR <0,93 ≥7 hari DAN LTH-SOPR <0,50). Kalau benar, LTH-SOPR agregat bisa menutupi sub-kohort LTH muda yang sudah capitulate duluan — relevan langsung dengan temuan video 2026-06-23 bahwa LTH-SOPR belum pernah <0,50 di bear ini (min 0,623 per 2026-06-30)
- **Test klaim:** Hipotesisnya menarik dan relevan ke lubang yang sudah kita temukan sendiri, tapi dasar video untuk klaim ini murni retoris — nol data pembanding, LTH-SOPR agregat tidak pernah ditampilkan berdampingan dengan SOPR kohortnya
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia. SOPR per age band butuh spent-output volume per kohort umur; kita hanya punya `asopr`, `sth_sopr`, `lth_sopr`. Proxy lewat perubahan `supply_6m-12m` **ditolak**: penurunan supply band tercampur antara koin yang dijual dan koin yang sekadar menua keluar ke band 1y-2y, dan dua efek itu tidak bisa dipisahkan tanpa data flow. Catat sebagai hipotesis terbuka

### [BARU] Distribusi SOPR kohort bersifat trimodal — tiga gelombang penjual berbeda
- **Insight:** Bentuk distribusinya bukan satu bukit mulus tapi tiga gundukan terpisah dengan gap kosong, dan tiap puncak mewakili gelombang penjual berbeda: (1) ~0,60–0,65 tempat posisi hari ini = zona capitulation top buyers; (2) ~0,9 = rugi ringan, dari early top buyers yang keluar berbondong-bondong di $85–90.000 saat drop 30% pertama dari ATH; (3) hijau >1,15 = profit taking oleh yang membeli 6–12 bulan **sebelum** puncak lalu menjual ke dalam puncak — "a fantastic exit in hindsight, but very few of them managed it" `[08:07]`–`[09:40]`
- **Indikator terkait:** SOPR Distribution kohort 6m–1y (histogram frekuensi harian, window 1 tahun)
- **Relevan ke:** general / ZC / K4 — dekomposisi struktur penjual dalam satu bear
- **Test klaim:** Dua masalah. Pertama, window-nya cuma 1 tahun — dengan ~250–365 observasi harian dan bar sempit, "tiga gundukan dengan gap kosong" bisa muncul murni dari sampling dan pilihan lebar bucket; ubah bucket dari 0,04 ke 0,08 dan gap-nya bisa hilang (video tidak pernah menyebut sensitivitas ini). Kedua, tiga gundukan itu bisa jadi hanya cerminan tiga fase harga bear ini (ATH−30%, chop tengah, posisi sekarang) — mendeskripsikan lintasan harga yang sudah kita tahu, bukan mengungkap tiga populasi penjual independen. Atribusi ke "$85–90.000" adalah rekonstruksi naratif dari nilai SOPR, bukan pengukuran alamat
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (SOPR per age band), dan bahkan kalau ada, klaimnya n=1 cycle sehingga tidak layak masuk framework

### [BARU] Klaim implisit: reading seburuk ini selalu diikuti 12 bulan yang bagus
- **Insight:** "This is a bad reading. But it's also a familiar kind of bad reading. We visited this many times before in previous cycles, and we all know what followed in the 12 months after every single one of them" `[10:16]`–`[10:33]`
- **Indikator terkait:** SOPR kohort 6m–1y persentil rendah → forward return 12 bulan
- **Relevan ke:** K4 (agresivitas akumulasi)
- **Test klaim:** Pola klaim yang sudah **dua kali gagal** di project ini (Capital Bleeding −1,3% ternyata cuma persentil 48, NOT-SUPPORTED 2026-06-23; quantile LTH-SOPR "nailed tops and bottoms", 2026-06-18). Tiga cacat: (a) "we all know what followed" adalah appeal to shared memory, bukan pengukuran — tidak ada n, tidak ada tabel forward return; (b) bias seleksi arah — di aset yang trennya naik jangka panjang, hampir semua titik persentil rendah diikuti 12 bulan positif, jadi tesnya harus membandingkan lawan baseline forward return tanpa syarat; (c) video mencampur dua denominator (16th percentile = seluruh sejarah, 19% = kumulatif window 1 tahun) dan menyandingkannya di ringkasan `[11:24]` seolah setara — itu sudah keliru secara aritmetis sebelum sampai ke klaim forward return
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia untuk klaim sebagaimana dinyatakan. Semangat klaimnya sudah diserap ke validasi kohort 6m-12m (Hipotesis C) memakai proxy yang bisa dihitung, lengkap dengan baseline tanpa syarat — hasilnya: edge ada tapi tipis (+130,8% vs baseline +99,7% di 365 hari, n=5)

### [BARU] Pola berulang SOPR raw kohort 6m–1y
- **Insight:** Pada tampilan raw, fase hijau (SOPR >1) = kohort ini konsisten mengunci profit, terjadi sepanjang bull market dan fase konsolidasi. Fase merah dalam = beli puncak lalu jual rugi. "Playing out like clockwork again this cycle": beli puncak → realisasi sedikit rugi → capitulate penuh saat harga terus chop lebih rendah `[06:02]`–`[06:32]`
- **Indikator terkait:** SOPR kohort 6m–1y (raw)
- **Relevan ke:** ZC / Z1, K4
- **Test klaim:** Nyaris definisional, bukan temuan — SOPR sebuah kohort pembeli-puncak per konstruksi hijau saat harga di atas cost basis mereka dan merah saat di bawah. "Playing out like clockwork" hanya menyatakan bahwa harga naik di bull dan turun di bear. Tidak ada isi prediktif yang bisa difalsifikasi
- **Perlu validasi Claude Code:** Tidak — tautologis, plus data SOPR per kohort tidak tersedia

### [KONFIRMASI] Bear market Bitcoin rata-rata berlangsung ~1 tahun
- **Insight:** "The average Bitcoin bear market does seem to last approximately 1 year, give or take a few months" — dan justru karena itu kohort 6m–1y jadi kohort yang menentukan berapa lama bear berlangsung `[03:31]`–`[03:47]`
- **Indikator terkait:** durasi bear (kalender)
- **Relevan ke:** **K4 jalur lantai waktu** (≥9 bulan sejak cycle peak DAN close < RP → DCA 5% cash pool/bulan), tervalidasi 3/3 bear searah
- **Test klaim:** Framework kita sudah punya versi yang lebih ketat dan sudah tervalidasi, dengan catatan risiko konkret (worst case beli pertama 2014 masih turun −46%). Versi video lebih longgar dan tidak menambah presisi. "Rata-rata 1 tahun" dari 3–4 bear punya spread lebar — framework sudah sengaja memilih lantai 9 bulan justru untuk menghindari over-precision. Sudah dibahas berulang di sumber lain (video 2026-07-02 time-based capitulation fractal n=3; video 2026-06-09 pain by boredom)
- **Perlu validasi Claude Code:** Tidak — sudah established & tervalidasi

### [KONFIRMASI] Capitulation adalah proses berantre, bukan satu event
- **Insight:** "The market can sit down here for a lot longer than you'd expect because capitulation isn't just one event. It's kind of like a queue. More and more people join it as time wears on and the pain compounds" `[08:39]`–`[08:56]`
- **Indikator terkait:** SOPR kohort 6m–1y (durasi di klaster capitulation)
- **Relevan ke:** **K4** — desain DCA bertahap per bulan (15/25/35%) + lantai waktu 5%/bulan justru mengasumsikan bottoming adalah proses multi-bulan, bukan satu titik
- **Test klaim:** Naratif, tidak punya bentuk yang bisa difalsifikasi, tapi sepenuhnya selaras dengan desain K4. Sudah dibahas dari sisi berbeda di dua sumber sebelumnya ("weak vs broken" video 2026-06-09; verdict Capital Bleeding video 2026-06-23)
- **Perlu validasi Claude Code:** Tidak — established + tidak testable

### [KONFIRMASI] Price-based capitulation sudah sebagian besar terjadi; sisanya time-based
- **Insight:** "We've appeared to already had a lot of the price-based capitulation... and now it seems like we're looking at the remainder of the time-based capitulation because I feel like there's just slightly more time pain left to come for this cycle" `[06:32]`–`[07:03]`
- **Indikator terkait:** SOPR kohort 6m–1y (raw), durasi fase merah
- **Relevan ke:** ZC / Z1, K4 lantai waktu
- **Test klaim:** Pembicara sendiri menyatakan dasarnya "just from eyeballing it here" — pengakuan eksplisit bahwa ini bukan pengukuran. Sudah dibahas dua kali di sumber lain dan sudah diserap jadi K4 lantai waktu
- **Perlu validasi Claude Code:** Tidak — established, dan dasar klaimnya diakui non-kuantitatif oleh sumbernya sendiri

### [KONFIRMASI] Membaca SOPR lewat persentil historis, bukan threshold absolut
- **Insight:** Pembicara sengaja menampilkan SOPR kohort dalam bentuk persentil terhadap seluruh sejarahnya sendiri ketimbang angka mentah `[05:29]`–`[05:46]`
- **Indikator terkait:** SOPR family (transformasi persentil)
- **Relevan ke:** Prinsip utama framework ("threshold absolut tidak reliable antar cycle") dan **SOPR KB § 7.3** yang sudah mengunci percentile-based dynamic threshold lebih baik dari fixed threshold (STH-SOPR SMA15 < 10th percentile = 79% win rate, n=19)
- **Test klaim:** Sudah established. Satu peringatan yang sudah kita temukan sendiri dan berlaku juga ke video ini: transformasi persentil punya drift — label "persentil 10" nominal ternyata menyala di 18,3% hari (temuan video 2026-06-18). Jadi "persentil 16" yang disebut video harus dibaca sebagai indikatif, bukan presisi
- **Perlu validasi Claude Code:** Tidak — established

### [INDIKATOR CUSTOM] SOPR kohort 6m–1y tampilan persentil (reading 16th percentile)
- **Insight:** SOPR yang hanya menghitung koin yang dibeli 6–12 bulan lalu ("we're listening to the top buyers and nobody else"), diplot sebagai persentil terhadap seluruh sejarahnya. Reading saat video: 16th percentile — mereka menjual rugi dan capitulate cukup parah, tapi belum di level terdalam yang pernah tercatat, "but it's pretty close" `[05:29]`–`[05:46]`, `[11:24]`–`[11:40]`
- **Komponen dasar:** SOPR standar (value spent / value created) difilter ke satu age band + transformasi persentil historis. **Dua dari tiga komponen sudah ada di framework** — yang baru murni slice kohortnya (6m–1y), yang tidak setara dengan STH (<155 hari) maupun LTH (>155 hari)
- **Indikator terkait:** aSOPR, LTH-SOPR, STH-SOPR
- **Relevan ke:** K4 kondisi #2 (LTH-SOPR <0,50)
- **Test klaim:** Dekomposisinya bersih; masalahnya slice itulah yang tidak bisa kita hitung. Catatan penting: kohort 6m–12m adalah **himpunan bagian dari LTH** framework, jadi ini bukan indikator paralel melainkan zoom-in ke dalam LTH — kalau kelak datanya ada, ia berpotensi jadi refinement K4 kondisi #2, bukan indikator terpisah
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (butuh spent-output per age band)

### [INDIKATOR CUSTOM] SOPR Distribution (histogram frekuensi harian, window 1 tahun)
- **Insight:** Histogram yang menghitung berapa hari dalam setahun terakhir SOPR kohort mendarat di tiap level. Sumbu-x = nilai SOPR, sumbu-y = frekuensi hari; garis putus-putus di 1,000 = break-even. Kotak putih = posisi hari ini di **0,635**, artinya koin yang dijual keluar dengan **realized loss 36%** `[07:03]`–`[07:52]`
- **Komponen dasar:** distribusi frekuensi (histogram) dari deret SOPR kohort — bukan indikator baru, tapi cara visualisasi baru dari deret yang sama
- **Indikator terkait:** SOPR kohort 6m–1y
- **Relevan ke:** ZC / Z1, K4
- **Test klaim:** Window-nya cuma **1 tahun** (bukan seluruh sejarah) — pembandingnya adalah bear yang sedang berjalan itu sendiri, sehingga pernyataan tipe "terdalam kedua di periode ini" nyaris tanpa informasi. Persis kegagalan Capital Bleeding (video 2026-06-23). Ditambah sensitivitas terhadap lebar bucket yang tidak pernah disebut video. Panel "Current Status" dari frame (bucket 0.600–0.640, 18 days in range, 19,6% days below) = low confidence dari resolusi frame
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia, dan desain window-nya membuat hasilnya tidak bisa dibandingkan lintas cycle sekalipun ada data

### [INDIKATOR CUSTOM] SOPR Distribution Cumulative
- **Insight:** Versi running total dari histogram. Dua angka yang ditarik: (1) di garis break-even kurva duduk di ~70% → selama setahun terakhir, 7 dari 10 hari kohort ini menjual rugi; (2) posisi hari ini membaca 19% → kira-kira 4 dari 5 hari dalam setahun terakhir lebih baik dari hari ini secara spending `[09:40]`–`[10:16]`
- **Komponen dasar:** CDF dari histogram di atas — tidak menambah informasi baru, cuma pembacaan berbeda
- **Indikator terkait:** SOPR kohort 6m–1y
- **Relevan ke:** K4
- **Test klaim:** **Yang paling perlu dikoreksi:** angka **19%** (kumulatif, window 1 tahun) dan **16th percentile** (window seluruh sejarah) punya denominator berbeda, dan video menyandingkannya di ringkasan `[11:24]` seolah dua-duanya mengatakan hal yang sama. Keduanya tidak setara dan tidak boleh digabung jadi satu narasi keparahan. Angka "70% hari jual rugi selama setahun" sendiri hampir pasti benar tapi trivial — di bear market, tentu saja mayoritas hari kohort pembeli-puncak menjual rugi
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia

### [INDIKATOR CUSTOM] Cost Basis Heatmap
- **Insight:** Chart memetakan densitas seluruh UTXO di semua level harga — tiap koin "mengingat" harga terakhir ia bergerak, dan heatmap menumpuk semua memori itu. Warna makin terang = klaster akumulasi historis makin padat `[01:59]`–`[02:30]`
- **Komponen dasar:** secara konsep = URPD / cost-basis distribution dengan sumbu waktu
- **Indikator terkait:** URPD
- **Relevan ke:** general — peta support/resistance struktural
- **Test klaim:** Ini alat visualisasi, bukan klaim — tidak ada yang bisa salah atau benar. Sudah dibahas di video 2026-06-09 (URPD sebagai peta support/resistance berbasis supply density)
- **Perlu validasi Claude Code:** Tidak — data URPD/cost-basis-distribution sudah dikonfirmasi tidak tersedia di `data_master_all_metrics.csv` (backlog data, bukan backlog validasi), dan tidak ada klaim testable yang melekat

### [STRATEGI] "Treat rallies as rallies, not reversals" sampai dua level direbut kembali
- **Insight:** Selama harga di bawah STH RP ($66.000) dan 365D MA ($85.000), semua kenaikan diperlakukan sebagai rally, bukan reversal. "Everything between here and there is essentially just noise as far as the regime is concerned." Urutannya bertingkat: reclaim STH RP dulu, lalu 365D MA `[01:44]`–`[01:59]`, `[10:33]`–`[10:49]`
- **Indikator terkait:** STH RP, 365D MA
- **Relevan ke:** Status Pasar / K5 entry
- **Test klaim:** Sebagai sikap ini konservatif dan tidak bertentangan dengan apapun di framework — di ZC/Z1, aturan default framework memang TUNGGU/DCA bertahap. **Tapi ada peringatan interaksi:** kalau "tunggu reclaim $66k lalu $85k" dipakai literal, ia bisa **menunda K4** — padahal K4 dan lantai waktu justru dirancang untuk membeli DI BAWAH level-level itu. Valid sebagai disiplin anti-FOMO, tidak boleh dibaca sebagai izin menunda akumulasi sampai harga di atas $85.000
- **Perlu validasi Claude Code:** Tidak — substansi testable-nya sudah tercakup di dua validasi CLOSED di atas (STH RP resistance & regime filter 3-level)

### [STRATEGI] Klaster capitulation = "precisely where I want to be buying"
- **Insight:** Setelah menjelaskan klaster SOPR terendah sebagai zona capitulation top buyers, pembicara menyatakan "this is exactly what you want to see around bottoms... but this is precisely where I want to be buying" — sambil mengakui pasar bisa duduk di sana jauh lebih lama dari perkiraan `[08:21]`–`[08:56]`
- **Indikator terkait:** SOPR Distribution kohort 6m–1y
- **Relevan ke:** **K4** — selaras filosofi akumulasi bertahap di capitulation
- **Test klaim:** Pengakuan "bisa duduk lebih lama dari perkiraan" jujur dan konsisten dengan alasan framework memilih DCA bertahap ketimbang lump sum. Tidak ada klaim baru yang bisa diuji; yang beda cuma trigger yang dipakai
- **Perlu validasi Claude Code:** Tidak — selaras dengan yang sudah established

### [STRATEGI] Proyeksi tanggal: capitulation selesai sekitar Desember 2026
- **Insight:** Kohort 6m–1y mulai underwater November 2025 di sekitar $95.000. Kalau tingkat pain-nya serupa historis (13 bulan), bull market bisa resume sekitar Desember tahun ini `[04:16]`–`[04:32]`, `[11:57]`–`[12:13]`
- **Indikator terkait:** Realized Price kohort 6m–1y, hitungan kalender
- **Relevan ke:** K4 lantai waktu / K5 timing — falsifiable dengan tanggal jelas
- **Test klaim:** Format klaimnya identik dengan dua proyeksi tanggal yang sudah kita validasi sebelumnya dan hasilnya campur/meleset ("bottom 12 Juli 2026", n=3; "death cross 10 Juli 2026"). Aritmetikanya rapuh: rata-rata 13 bulan dari n=3 ditambahkan ke satu tanggal mulai yang ditentukan secara okuler, lalu dibulatkan jadi satu bulan target. Pembicara sendiri menegasikannya 90 detik kemudian
- **Perlu validasi Claude Code:** Tidak sebagai validasi terpisah — sudah tercakup di validasi kohort 6m-12m (Hipotesis A). **Hasilnya: rentang jujurnya Okt 2026 – Feb 2027**, dengan Des 2026 sebagai titik mean, bukan target

### [STRATEGI] Metodologi eksplisit: cari pola capitulation + fear, bukan tanggal/harga persis
- **Insight:** "As ever I'm not looking for exact dates or exact prices. I'm looking for classic top-buyer capitulation and widespread fear across the network and that is exactly what we're getting." Juga: "I don't have a crystal ball telling you when that capitulation will end. But I do know we're more likely near the end than the beginning" `[11:40]`–`[11:45]`, `[12:13]`–`[12:20]`
- **Indikator terkait:** —
- **Relevan ke:** general — sikap metodologis
- **Test klaim:** Prinsip yang benar dan sejalan dengan Governance framework butir 3 ("semua threshold = panduan arah, bukan presisi"). Tapi ada tension internal: video menghabiskan dua segmen membangun proyeksi tanggal spesifik lalu menutup dengan menyatakan tidak mencari tanggal spesifik. Saat menilai bobot video ini, pegang pernyataan ini sebagai posisi sebenarnya dan perlakukan proyeksi Desember sebagai ilustrasi
- **Perlu validasi Claude Code:** Tidak — prinsip metodologis, bukan klaim empiris

### [STRATEGI] Prinsip psikologi penjual
- **Insight:** "Nobody takes the 36% loss because they think the trade is finished. They take it because they think it's about to get worse, and that's capitulation in its purest form." Diperluas: orang hanya pernah menjual karena satu alasan — mereka pikir harga akan lebih rendah; yang berubah sepanjang siklus cuma berapa banyak orang yang mempercayainya serentak `[07:33]`–`[08:07]`
- **Indikator terkait:** SOPR (interpretasi umum)
- **Relevan ke:** general — landasan interpretif kenapa SOPR <1 dibaca sebagai capitulation
- **Test klaim:** Salah sebagai pernyataan universal — penjualan juga terjadi karena margin call, likuidasi paksa, rebalancing, kebutuhan likuiditas, dan tax-loss harvesting; tidak semuanya ekspresi keyakinan arah. Sebagai penyederhanaan retoris untuk menjelaskan capitulation tidak berbahaya, tapi ia adalah jembatan logis seluruh argumen video, jadi perlu dicatat bahwa fondasinya asumsi psikologis, bukan temuan
- **Perlu validasi Claude Code:** Tidak — naratif, tidak testable dengan data on-chain kita

### [KONFLIK] Kriteria "bull market kembali" berbasis posisi harga vs unlock struktural
- **Insight:** Pembicara mendefinisikan kembalinya bull market sebagai **harga merebut kembali STH RP ($66.000) lalu 365D MA ($85.000)** — "nothing changes on that front until we at least reclaim the short-term holder realized price... and then ultimately the yearly moving average". Ditambah penanda kedua: flip kohort 6m–1y kembali ke profit `[01:29]`–`[01:59]`, `[10:33]`–`[10:49]`, `[11:40]`–`[11:57]`
- **Konflik dengan:** Decision_Framework v2 § 0 — "Status bear berakhir (unlock): STH RP cross naik melewati RP (masuk Z2) — **BUKAN saat harga balik ke Z5**", dan K4-selesai / K5-mulai yang memakai trigger struktural yang sama
- **Alasan konflik:** Framework sengaja memakai kriteria **ordering antar level** (STH RP vs RP), bukan **posisi harga terhadap level**, dan aturannya eksplisit menolak versi berbasis posisi harga. Video memakai persis pendekatan yang ditolak itu. Tambahan: video menempatkan STH RP sebagai gerbang pertama, padahal Price_Level KB v1.4 § 6.3 mencatat STH RP paling sering disalahgunakan sebagai standalone trigger (60 episode false signal terpisah)
- **Rekomendasi:** **Diskusikan lebih lanjut dengan Yudi** — konflik ini **lunak, bukan pemicu STOP-rule**: arah kedua pendekatan sama, yang berbeda cuma waktu dan sensitivitas. Dan hasil Stage 3 sekarang sudah memberi jawaban empirisnya: reclaim STH RP datang 40–238 hari lebih awal dari unlock **tapi 88% palsu**; 365D MA reclaim justru **koinsiden** dengan unlock (+12/+4/−13 hari) sehingga tidak menambah apapun; flip kohort 6m-12m **lagging** (0/4 leading). Artinya tidak satupun dari tiga penanda alternatif video layak menggantikan atau bahkan melengkapi unlock struktural. Yang tetap layak sebagai leading proxy cuma 200D MA reclaim yang sudah CLOSED sebelumnya

---

## Flag Prioritas

1. **Signal D punya hit rate ~12%** — temuan paling actionable dari batch ini, dan kita akan segera membutuhkannya. Signal D (harga > STH RP ≥3 hari) adalah syarat wrap-up K4 → Z1b, tapi di 8 kali ia menyala selama bear, hanya 1 yang benar-benar mendahului unlock struktural dan 7 balik ke bawah dalam 90 hari. Menaikkan persistensi saja tidak menyelamatkan (break 31 hari dan 20 hari tetap gagal). Perlu diputuskan: pasangkan dengan 200D MA reclaim, atau terima hit rate-nya dan kompensasi lewat sizing.

2. **Tiga penanda alternatif akhir-bear semuanya gagal mengisi celah K4→K5** — ini yang saya minta diperhatikan sebagai satu paket, bukan tiga temuan terpisah. Flip kohort 6m-12m lagging (0/4), 365D MA reclaim koinsiden (+12/+4/−13), STH RP reclaim awal tapi 88% palsu. Kalau dua-tiganya diterima tanpa uji lead/lag, framework bisa pelan-pelan bergeser ke definisi bear-end berbasis harga tanpa keputusan sadar. Hasilnya: **tidak ada yang perlu diubah di § 0.**

3. **Rentang proyeksi akhir capitulation: Okt 2026 – Feb 2027, bukan "Des 2026"** — relevan untuk kalibrasi kesabaran K4 / lantai waktu. Episode berjalan sudah 243 hari (8,0 bulan) per 2026-07-15, harga −34,7% di bawah cohort_RP $99.727. Lantai waktu K4 (≥9 bulan sejak peak + close < RP) sudah aktif sejak Juli 2026.

4. **Filter 3-level lolos ujian Mei 2021** — satu-satunya kelebihan spesifik yang tidak dimiliki alarm bear CEPAT framework (hanya 2 hari dari 123 di bawah ketiga level). Tapi harganya lag median 119 hari dan median forward return 365 hari +70,5% dari sinyal. Layak jadi veto/konfirmator kelas berat, bukan alarm. Worth didiskusikan apakah nilai "rendah false positive" ini cukup untuk masuk sebagai confirming context.

5. **Sub-kohort LTH muda sebagai penjelasan kenapa LTH-SOPR <0,50 tidak pernah nyala** — hipotesis terbuka yang tidak bisa diuji dengan data kita (butuh SOPR per age band). Tapi relevansinya nyata: K4 kondisi #2 mungkin mustahil menyala di cycle ini (min LTH-SOPR 0,623 per 2026-06-30). Kalau LTH agregat memang diencerkan oleh koin 2-5 tahun yang tidak bergerak, threshold 0,50 mungkin perlu ditinjau ulang terlepas dari video ini.

6. **Inkonsistensi denominator di sumber (16th percentile vs 19%)** — bukan temuan framework, tapi catatan kualitas: video menyandingkan persentil seluruh-sejarah dengan persentil window-1-tahun seolah setara. Berguna sebagai kalibrasi seberapa hati-hati membaca angka dari channel ini ke depan.

---

## Yang Langsung Diabaikan

| Item | Timestamp | Alasan |
|---|---|---|
| Promosi onchainmind.io + "7-day free trial akan berakhir" | `[04:32]`–`[04:59]` | Sponsor/promosi produk |
| Penjelasan definisi dasar SOPR (harga beli vs harga jual, >1 untung, <1 rugi) | `[04:59]`–`[05:29]` | Definisional murni, sudah established di SOPR KB v1.4 |
| Instruksi cara membaca sumbu chart distribusi | `[07:03]`–`[07:33]` | Cara baca chart, bukan klaim |
| "We're more likely near the end than the beginning" | `[11:45]`–`[11:48]` | Pernyataan sentimen tanpa mekanik tambahan |
| Outro / musik penutup | `[12:20]`–`[12:41]` | — |

**Catatan kualitas sumber:** transcript di `[04:32]` berbunyi "about 30 months later" — ini ASR error; seluruh sisi video (`[04:01]`, `[11:40]`–`[12:13]`) konsisten menyebut **13 bulan** dan target Desember. ASR artifact lain: "soaper" = SOPR, "bare market" = bear market. Angka yang hanya terbaca dari frame (200D MA ≈ $70.000, panel Current Status, posisi klaster histogram) dilabel **low confidence dari resolusi frame** dan tidak dipakai sebagai anchor kesimpulan manapun.
