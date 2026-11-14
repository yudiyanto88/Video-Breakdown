# The FREE & SIMPLE Strategy That Beats Bitcoin (It Just Flashed Again)
**Channel:** Bitcoin Magazine Pro (Matt Crosby, Director of Research & Analytics)
**Tanggal video:** 2026-08-05
**Tanggal analisis:** 2026-08-06
**Link:** https://youtu.be/2XLmK_TDOgc

> ## 🛑 STOP — perlu dibahas sebelum diputuskan
>
> Video ini memaparkan **sistem alokasi modal siklus-penuh yang lengkap dan berdiri sendiri**
> ([STRATEGI] Zone map 4-regime + [KONFLIK] Mekanik exit kontinu): satu indikator (MVRV Quantile
> percentile) mengatur seluruh keputusan — kapan setoran mingguan beli BTC, kapan ditahan jadi cash
> reserve, kapan stack di-trim, kapan reserve di-deploy. Tidak ada gate, veto, syarat awal, ordering
> level, maupun event trigger. 100% spot.
>
> **Kenapa memenuhi trigger STOP:** sistem ini menempati pekerjaan yang sama dengan K1 + K2 + K4 + K5
> sekaligus, tapi dengan filosofi yang secara fundamental berbeda dari pendekatan zone-based + K-node —
> single-signal vs multi-sinyal berlapis, ramp kontinu harian vs step function event-driven, dan **tanpa
> dimensi leverage sama sekali** (tidak ada padanan untuk K2/K5/K6 maupun tangga Hard Limits LTV
> 45/48/55/58-65). Pembicara juga memposisikannya sebagai titik awal menyeluruh `[03:31]` ("if you do not
> know what you're doing with your Bitcoin investing, this is probably not a bad place to start"), bukan
> sebagai alat pelengkap.
>
> **Yang BUKAN masalah:** tidak ada pelanggaran hard constraint LTV — sistemnya tidak pernah menyentuh
> loan. Trigger yang kena adalah trigger kedua, bukan yang pertama.
>
> **Rekomendasi:** JANGAN adopsi sebagai sistem, dan jangan impor satu pun angka parameternya
> (10/85/90 · trim 0,75%/hari · reserve 10%/hari · floor 50%) — semuanya hasil grid search in-sample pada
> satu path harga (lihat [KONFLIK] Kalibrasi parameter), gagal di lapis-1 protokol Governance v2
> ("threshold a priori tanpa grid search"). Yang layak didiskusikan hanya dua **prinsip** yang bisa
> berdiri lepas dari indikator mereka: (a) sizing dikalibrasi ke base rate frekuensi sinyal, (b) bentuk
> ramp kontinu sebagai pengganti step function di batas zona. Keduanya wajib lewat 4 lapis Governance
> sendiri dan tidak boleh menyentuh sisi loan.
>
> **Konteks yang bikin ini bukan detail kosmetik:** mesin framework menempatkan pasar di **ZD**
> (2026-07-15: harga $65.098 · RP $52.740 · STH RP $67.143 — harga masih 23% di atas RP), sementara
> indikator video membaca "bottom zone" (percentile 8%). Perbedaan pembacaan ini adalah inti dari apa
> yang perlu diputuskan.

---

## Ringkasan

Video 12 menit yang merilis chart gratis baru di bitcoinmagazinepro.com — **MVRV Quantile Bands** — lalu
memaparkan sistem alokasi lengkap yang dibangun di atasnya. Indikatornya mengambil MVRV Ratio mentah,
mem-fit **amplitude decay model** yang memperhitungkan "rising bottoms and declining peaks", lalu
mengkonversi tiap pembacaan jadi **percentile 0-100 terhadap seluruh sejarah** (0 = hari termurah,
100 = termahal). Reading saat video dibuat: **8%** — yang menurut Matt "comparable to when Bitcoin is
pretty much bottoming out in every single bear cycle".

Sistemnya sendiri sederhana dan seluruhnya spot: di bawah p10 beli agresif dengan menarik cash reserve;
p10-85 DCA normal; p85-90 setoran mingguan ditahan jadi reserve (berhenti beli BTC); di atas p90 tambah
trim stack maksimum 0,75%/hari. Kedua sisi ramp linear terhadap kedalaman. Ada floor: trim berhenti kalau
BTC akan jatuh di bawah 50% of book. Dua mode ditawarkan — "sell mode" (dengan trim) dan "accumulation
mode" (trim dimatikan, untuk yang tidak mau jual).

Klaim performanya besar dan disajikan dengan disclosure yang di atas rata-rata konten sejenis: 0,1% fee,
one-bar fill lag, 20% capital gains tax pada **setiap** trade profitable. Hasilnya — $1.000 seed +
$100/minggu sejak Jan 2014 → blind DCA 46,8 BTC / IRR 54,0%, accumulation 49,1 BTC / 54,7%, sell mode
73,9 BTC / 64,0% setelah bayar $1.026.987 pajak. Diuji di 39 start date kuartalan: sell mode positif 100%,
accumulation 74%.

Yang dibahas di bawah: mana dari klaim itu yang bertahan setelah diuji ke data kita sendiri, mana yang
runtuh, dan mana satu-dua prinsip yang layak diambil tanpa mengimpor indikatornya.

---

## Insight Inventory

### [INDIKATOR CUSTOM] MVRV Quantile Bands
- **Insight:** Indikator baru bikinan Bitcoin Magazine Pro, gratis. MVRV Ratio → fit amplitude decay
  model → konversi ke percentile 0-100 terhadap seluruh sejarah, "adjusted for cycle compression".
  Dua panel: harga + Realized Price + band 5th-95th percentile; panel bawah oscillator percentile.
  `[00:12]`, `[01:19]-[01:45]`, slide `[02:05]`, FAQ slide `[11:41]`. **Dekomposisi:** MVRV Ratio
  (sudah ada di framework) → detrend/amplitude-decay fit → percentile rank historis. Bukan indikator
  baru dari nol — ini transformasi statistik atas MVRV Ratio.
- **Indikator terkait:** MVRV Ratio, Realized Price
- **Relevan ke:** general; berpotensi menyentuh K1 (syarat awal MVRV diminishing), K4 (kondisi #1),
  veto K2 #3
- **Test klaim:** Titik lemah terbesar ada di frase "percentile of **all history**" — kalau rank dihitung
  full-sample (bukan expanding/causal), setiap pembacaan historis mengandung informasi masa depan →
  lookahead bias struktural. Parameter fit decay tidak diungkap, dan model yang di-fit ke seluruh sejarah
  otomatis "tahu" bahwa peak menurun — itu juga in-sample. Tetangga dekat "MVRV Z-Score rolling 1y"
  (On-Chain Mind 2025-01-22) yang sudah CLOSED: tidak align 1:1 dengan AVIV.
- **Perlu validasi Claude Code:** Ya — digabung ke validasi percentile causal di bawah.

**[VALIDASI — 6 Agustus 2026, CLOSED]** Reproduksi angka "percentile 8%" **INCONCLUSIVE** — dua proxy
causal (expanding rank mentah & expanding-OLS detrended) membaca **21,4-22,6** per 2026-07-15, jadi selisih
ke 8 cenderung berasal dari asumsi decay model BM Pro, bukan data mentah; sesuai aturan berhenti tidak ada
varian ketiga yang dicoba. **Lookahead bias struktural terkonfirmasi ada**: selisih causal vs full-sample
rata-rata 4,6pp (raw) dan 10,5pp (detrended), ekor sampai ±50-67pp — pembacaan historis tidak replikabel
real-time. **n = 9-10 episode** (bukan 372-1.160 hari), sebaran 2011/2014-15/2018/2020/2022.
Detail: [`findings_mvrv_percentile_causal.md`](findings_mvrv_percentile_causal.md)

### [KONFIRMASI] Raw MVRV: angka sama artinya beda antar cycle
- **Insight:** FAQ verbatim slide `[11:41]`: "The raw ratio tells you market value relative to realized
  value today, but the same number can mean different things in different cycles. The quantile approach
  converts each reading into a percentile of all history, adjusted for cycle compression."
- **Indikator terkait:** MVRV Ratio
- **Relevan ke:** general — persis prinsip utama Decision Framework v2 dan Governance poin 3
- **Test klaim:** Yang dikonfirmasi adalah **diagnosisnya**, bukan **obatnya**. Framework menjawab masalah
  yang sama dengan MVRV vs SMA180 + MVRV Momentum cross — keduanya causal/at-gate. BM Pro menjawabnya
  dengan percentile rank terhadap seluruh sejarah, yang kalau full-sample justru melanggar Standar
  Validasi poin 3. Kesamaan filosofis di sini **tidak boleh** dipakai untuk melegitimasi mekaniknya.
- **Perlu validasi Claude Code:** Tidak — established.

### [KONFIRMASI] Amplitude decay: peak MVRV tiap cycle makin rendah
- **Insight:** FAQ slide `[11:41]`: "each cycle's MVRV peak has been lower than the last". Lisan
  `[01:34]-[01:45]`: "fairly predictable rising bottoms and declining peaks". Model men-fit kontraksi ini
  secara langsung.
- **Indikator terkait:** MVRV Ratio
- **Relevan ke:** K1 & K3 (syarat awal: MVRV di setiap ATH baru lebih rendah dari sebelumnya)
- **Test klaim:** Duplikat dari insight tervalidasi 2025-01-22 (n=5, established). Tidak ada angka baru
  di video ini. Nilai tambahnya cuma bahwa BM Pro meng-hardcode-nya ke dalam model.
- **Perlu validasi Claude Code:** Tidak — established.

### [BARU] Trough MVRV tiap cycle makin TINGGI (rising bottoms)
- **Insight:** Sisi yang jarang disebut dari decay: "each trough higher" (FAQ slide `[11:41]`). Bukti
  lisan `[02:35]-[02:50]`: "if you look at the 2015 bear market low, we were very much beneath the
  realized price. 2019, a little bit less. 2022, a little bit less."
- **Indikator terkait:** MVRV Ratio, Realized Price, LTH-MVRV
- **Relevan ke:** **K4** (kondisi #1 LTH-MVRV <1,0; #4 Price/CVDD <1,10; flag ekstrem ≤1,0), **ZC**, **Z1**
- **Test klaim:** Framework mengkodekan sisi ATAS decay tapi tidak sisi bawah. Kalau trough naik
  struktural, keempat threshold absolut K4 makin sulit tersentuh tiap cycle → K4 bisa gagal arm bukan
  karena pasar belum murah, tapi karena penggarisnya usang. Basis klaim video **n=3 bear low, kualitatif,
  tanpa satu pun angka**. Sebagian kenaikan trough bisa artefak dari fit decay-nya sendiri — model
  di-fit untuk menghasilkan rising bottoms, lalu dipakai membuktikan rising bottoms (sirkular).
- **Perlu validasi Claude Code:** Ya — prioritas #1.

**[VALIDASI — 6 Agustus 2026, CLOSED]** Klaim "trough tiap cycle makin tinggi" **terbelah**: monoton naik
untuk metrik valuasi (MVRV min 0,568→0,702→0,760; LTH-MVRV 0,585→0,732→0,754; Supply in Profit
39,3→39,9→44,5 — **n=3 bear selesai**: 2014-15, 2018, 2022) tapi **tidak** untuk aSOPR (0,918→0,862→0,893),
LTH-SOPR (0,559→0,439→0,449), dan Price/CVDD (0,966→1,003→0,982) yang mean-reverting secara konstruksi.
Temuan sampingan yang lebih penting: **kondisi K4 #2 nol hari nyala di seluruh 4 bear + suplemen 2011**,
sehingga count=4 (DCA 35%/bulan) adalah tier yang secara empiris tidak bisa dicapai. Di bear berjalan
2025-26 (per 2026-07-15) 3 dari 4 kondisi belum pernah nyala dan count belum pernah ≥2.
Detail: [`findings_k4_threshold_reachability.md`](findings_k4_threshold_reachability.md)

### [BARU] Percentile 8% tercapai sebelum harga menyentuh Realized Price
- **Insight:** Slide `[02:05]`: "Current Percentile: 8%" per 5 Agt 2026. Lisan `[02:08]-[02:19]`: level
  ini "comparable to when Bitcoin is pretty much bottoming out in every single bear cycle". Lalu
  `[02:44]-[02:50]`: "We're reaching these levels **before** we've actually reached the realized price."
- **Indikator terkait:** MVRV Quantile percentile, Realized Price
- **Relevan ke:** **ZC / Z1 / K4 / lantai waktu** — indikator ini bilang "bottom-zone" lebih awal dari
  zona ZC framework (yang butuh P < RP)
- **Test klaim:** Dua hal berbeda dicampur — market call time-bound "8% hari ini" yang tidak falsifiable
  secara umum, dan klaim struktural "trough tercapai pada posisi harga-vs-RP yang makin tinggi" yang bisa
  diuji dengan kolom kita sendiri. Titik lemah utama: dengan MVRV ≈1,23, rank mentah terhadap sejarah
  cenderung jauh di atas 8% — artinya hampir seluruh "8%" dihasilkan oleh penyesuaian decay, yaitu oleh
  asumsi model. Angka 8% dibaca dari frame — low confidence dari resolusi frame.
- **Perlu validasi Claude Code:** Ya — prioritas #2.

**[VALIDASI — 6 Agustus 2026, CLOSED]** **P/RP di bear low naik monoton** (0,568 → 0,702 → 0,777, **n=3
bear selesai**) — klaim struktural video didukung. Tapi **hari P<RP tidak menurun monoton** (37 → 27 →
128), dan pola "reading <10 tercapai saat P masih di atas RP" cuma terjadi di **8 dari 419 hari (1,9%)**
dengan proxy raw — semuanya di 2011; dengan proxy detrended jadi 19,4% tapi rentangnya berhenti di 2014.
Bukan karakter yang stabil. **Bear berjalan 2025-26 belum pernah menyentuh <10** dengan proxy kami (min
16,9) dan **harga belum pernah menyentuh RP sekalipun** sejak peak 2025-10-06 (P/RP terendah 1,101) —
jadi klaim "sekarang sudah di level bottoming" tidak terkonfirmasi dari data kami per 2026-07-15 (~3
minggu lebih tua dari video).
Detail: [`findings_mvrv_percentile_causal.md`](findings_mvrv_percentile_causal.md)

### [BARU] Threshold percentile FAQ: <25 = akumulasi bear, <10 = "only near major cycle lows"
- **Insight:** FAQ verbatim slide `[11:41]`: "readings below the 25th percentile have coincided with bear
  market accumulation ranges, and readings below the 10th percentile have appeared **only** near major
  cycle lows."
- **Indikator terkait:** MVRV Quantile percentile
- **Relevan ke:** K4, ZC, Z1
- **Test klaim:** Ini threshold absolut yang ditempel di atas skala relatif — pola yang CLAUDE.md minta
  di-flag. Kata "**only**" membuatnya klaim zero-false-positive yang sangat mudah dipatahkan: satu saja
  episode <10 yang jauh dari cycle low sudah cukup. FAQ tidak menyebut n sama sekali, dan karena skalanya
  percentile, "<10% hari" secara definisi terjadi ~10% waktu (~600 hari) — "hanya dekat major cycle low"
  jadi klaim yang secara aritmetis butuh 600 hari itu terkonsentrasi di 3-4 jendela.
- **Perlu validasi Claude Code:** Ya — digabung ke validasi percentile causal.

**[VALIDASI — 6 Agustus 2026, CLOSED]** Kata "**only**" **hampir benar untuk p10, lemah untuk p25**. Di
p10: 98,1% (proxy raw) s/d 99,7% (detrended) hari berada dalam ±180 hari dari cycle low — tapi **1-2 dari
9 episode adalah false positive**, paling menonjol COVID crash 2020-03-12 (jarak **453 hari** dari cycle
low terdekat) dan Agt-2015 (216 hari). "Hampir selalu" lebih jujur daripada "only". Di p25 jadi **4-5 dari
9-10 episode** tidak dekat cycle low → framing "bear market accumulation range" jauh lebih longgar dari
yang tersirat. **n = 9-10 episode**, didominasi cycle 2014-15 dan 2022.
Detail: [`findings_mvrv_percentile_causal.md`](findings_mvrv_percentile_causal.md)

### [BARU] Band 5th-95th percentile: break atas = fase akhir bull, break bawah = capitulation low
- **Insight:** FAQ verbatim slide `[11:41]`: "The shaded bands cover the 5th to 95th percentile of history.
  Breaks above the top band have marked the final phase of bull markets, and breaks below the bottom band
  have marked capitulation lows."
- **Indikator terkait:** MVRV Quantile bands, harga
- **Relevan ke:** **Z5 / K1** (break atas ≈ P ≥ AVIV Upper) dan **ZC / K4** (break bawah ≈ capitulation)
- **Test klaim:** Secara fungsional ini band harga alternatif untuk AVIV Mean/Upper, dan pertanyaannya
  identik dengan yang sudah **CLOSED negatif** di `findings_mvrv_rolling1y_vs_aviv.md` (band turunan MVRV
  tidak align 1:1 dengan AVIV; divergensi = artefak reaktivitas formula). Beban pembuktian ada di pihak
  yang mengusulkan. Video tidak menyebut n break sama sekali, dan "final phase of bull" adalah label
  post-hoc yang lentur — fase akhir bisa berlangsung 6 bulan.
- **Perlu validasi Claude Code:** Ya — **belum diuji, backlog**. Nilai marjinalnya rendah karena
  pertanyaan sejenis sudah CLOSED negatif, dan hasilnya bergantung pada proxy percentile yang sudah
  dinyatakan inconclusive. Kalau kelak dijalankan: bandingkan tanggal cross proxy >95 vs cross AVIV Upper
  di 2013/2017/2021 — selisih hari per cycle, apakah tandanya konsisten.

### [KONFIRMASI] Percentile rendah ≠ bottom presisi — 2022 turun 20% lagi
- **Insight:** `[02:20]-[02:34]`: di 2022 bottom percentile mulai tersentuh saat BTC ~$18.000, harga lanjut
  turun ke ~$15.000 — "so we did go 20% lower. That's not out of the question."
- **Indikator terkait:** MVRV Quantile percentile
- **Relevan ke:** **K4** dan **lantai waktu**
- **Test klaim:** Direklasifikasi dari [BARU] ke [KONFIRMASI] — framework sudah mengkodekan ini persis
  dan dengan angka yang lebih keras: justifikasi sizing lantai waktu 5%/bulan memakai "worst case beli
  pertama 2014 masih turun −46%" (n=3/3 bear searah). Klaim video **n=1 cycle, −20%** jadi lebih lemah
  dari yang sudah kita punya. Nilainya cuma sebagai konfirmasi eksternal bahwa pihak lain sampai ke
  pengaman yang sama.
- **Perlu validasi Claude Code:** Tidak — established; angka undershoot per bear keluar sebagai by-product
  validasi percentile causal.

**[VALIDASI — 6 Agustus 2026, CLOSED]** Terkonfirmasi dengan angka yang lebih lengkap: reading <10 pertama
**bukan** titik terbawah — masih ada drawdown lanjutan **−16,3% s/d −68,6%** dan **20-158 hari** sebelum
bear low. **n=4 bear** (2011 supl., 2014-15, 2018, 2022); sebaran sangat lebar dan **didominasi observasi
2011** di ujung ekstrem.
Detail: [`findings_mvrv_percentile_causal.md`](findings_mvrv_percentile_causal.md)

### [STRATEGI] Zone map 4-regime berbasis percentile
- **Insight:** Dari slide `[04:10]-[07:40]`, sistem alokasi penuh yang dipicu **semata-mata oleh nilai
  percentile**, tanpa event trigger, ordering level, atau konfirmasi perilaku:

  | Regime | Percentile | % of days | Aksi |
  |---|---|---|---|
  | Buy hard | < 10 | 12,6% | deposit rutin + penarikan reserve |
  | Plain DCA | 10-85 | 66,9% | deposit beli BTC, reserve tidak disentuh |
  | Pause | 85-90 | 4,9% | deposit masuk reserve cash (berhenti beli BTC) |
  | Pause + trim | > 90 | 11,8% | deposit ke reserve + stack di-trim |

  Lisan pendukung: `[04:12]-[04:22]`, `[04:26]-[04:34]`, `[05:44]-[05:50]`.
- **Indikator terkait:** MVRV Quantile percentile (indikator tunggal — sistem ini **single-signal**)
- **Relevan ke:** paralel dengan seluruh mesin K1/K2/K4/K5/lantai waktu sekaligus
- **Test klaim:** Kekuatannya nyata — selalu punya jawaban tiap hari, tidak bisa "diam" seperti kasus 2020
  di framework lama. Tapi kelemahan strukturalnya juga nyata: satu indikator = satu titik kegagalan, dan
  tiga boundary (10/85/90) plus distribusi hari semuanya turunan dari indikator yang sama yang di-fit
  in-sample. Sample = 1 path harga 2014-2026 (~3 cycle), dan seluruh distribusi hari otomatis "benar"
  secara definisi karena skalanya percentile. Klaim salah kalau: dijalankan pada indikator versi causal,
  hasilnya tidak lagi mengalahkan blind DCA.
- **Perlu validasi Claude Code:** Tidak — replikasi penuh butuh parameter decay yang tidak diungkap;
  mereplikasi sampai angkanya cocok = overfitting yang dilarang Standar Validasi poin 6.
  **Ditandai STOP** (lihat flag di atas) — ini keputusan diskusi, bukan keputusan data.

### [STRATEGI] Linear ramp sizing
- **Insight:** Verbatim slide `[04:10]-[07:40]`: "Both sides scale linearly with depth past the boundary."
  **Beli:** "zero at percentile 10, half at 5, and the full 10% of whatever cash sits in the reserve once
  the oscillator reaches 0" — peak 10% reserve **per hari**. **Jual:** "zero at percentile 90, half at 95,
  and the full 0.75% of the stack at 100" — peak 0,75% stack **per hari**.
- **Indikator terkait:** MVRV Quantile percentile
- **Relevan ke:** **K4** (DCA berjenjang 15/25/35%/bulan berdasar count), **lantai waktu** (5%/bulan),
  **K1** (jual 20-30% lump)
- **Test klaim:** Satuannya berbeda kelas — 10% reserve/hari di p0 vs 15/25/35% cash pool **per bulan** di
  K4. Dikonversi kasar, 10%/hari selama seminggu ≈ 52% reserve terpakai; sistem video jauh lebih agresif
  di dasar tapi hanya di hari-hari paling ekstrem. Yang menarik bukan angkanya melainkan **bentuknya**:
  ramp kontinu menghilangkan diskontinuitas di batas (tidak ada lompatan 0→15% saat count naik dari 1 ke
  2) dan otomatis tahan terhadap revisi data provider — justru menjawab kekhawatiran Governance poin 3
  ("jangan eksekusi karena selisih tipis di batas"). Angka ramp-nya sendiri hasil grid search, jadi tidak
  boleh diimpor apa adanya.
- **Perlu validasi Claude Code:** Ya — **belum diuji, backlog**. Ini eksperimen desain framework (bukan
  verifikasi klaim video) dan pantas menunggu Governance poin 4 (backtest mesin utuh) selesai dulu.
  Pertanyaan: pada jendela K4 historis, apakah mengganti step 15/25/35%-per-bulan dengan ramp linier
  terhadap count (atau terhadap kedalaman Price/CVDD) mengubah harga beli rata-rata dan BTC terakumulasi
  secara material?

### [STRATEGI] Floor 50% — trimming berhenti kalau BTC akan jatuh di bawah 50% of book
- **Insight:** `[07:11]-[07:42]` + slide: "Trimming stops if BTC would fall below 50% of the book."
  Alasan campuran monetary + filosofis: "you never want to sell **all** of your Bitcoin... why are we even
  here if all we're trying to do is maximize our fiat? No, I'm trying to maximize my Bitcoin."
- **Indikator terkait:** —
- **Relevan ke:** **K1** ("jual 20-30% BTC → USDT") — arah yang sama, mekanisme beda: framework batasi
  lewat persentase per event, video batasi lewat hard floor komposisi portofolio
- **Test klaim:** Ini asumsi tetap yang **tidak pernah di-grid-search** — disebut di judul heatmap sendiri
  ("50% floor") sebagai konstanta di semua sel, jadi seluruh angka edge +10,1 pp bersifat kondisional pada
  floor 50% dan sensitivitasnya tidak diketahui. Ironisnya ini justru satu-satunya parameter yang alasannya
  bukan optimisasi melainkan prinsip — paling jujur secara metodologis sekaligus paling tidak teruji. n=0
  uji sensitivitas. Framework kita punya padanan implisit yang lebih konservatif: K1 hanya menjual 20-30%,
  sehingga floor efektifnya jauh di atas 50%.
- **Perlu validasi Claude Code:** Tidak — tidak bisa diuji tanpa replikasi penuh sistem video.

### [STRATEGI] Reserve mechanism — pause + trim jadi amunisi bottom
- **Insight:** `[06:28]-[06:52]`: di atas p85 deposit tidak beli BTC tapi masuk reserve; ditambah hasil
  trim di atas p90; reserve inilah yang dideploy agresif saat percentile <10.
- **Indikator terkait:** MVRV Quantile percentile
- **Relevan ke:** **K1 → K4** (hasil jual 20-30% di K1 jadi USDT, dipakai K4) — konseptual sama persis
  dengan framework. Ini bagian paling kompatibel dari seluruh sistem.
- **Test klaim:** Lebih dekat [KONFIRMASI] daripada strategi baru — perbedaannya cuma reserve BM Pro
  terisi otomatis dan kontinu, sedangkan framework mengisinya lewat satu event K1. Dari slide `[10:46]`
  panel "Cash reserve (% of book)": reserve terbangun 4× — 2014 (artefak seed), 2017-18 (~50%), 2021-22
  (~72%), 2024-26 (~62%, sedang drawdown ke ~20%). **Angka puncak low confidence dari resolusi frame,
  jangan jadi anchor.** Yang layak dicatat: reserve mereka baru turun ke ~20% padahal indikatornya sudah
  p8 — artinya sistemnya sendiri belum menganggap ini dasar, nuansa yang hilang dari narasi "it just
  flashed again".
- **Perlu validasi Claude Code:** Tidak — mekanik internal sistem mereka, bukan klaim tentang perilaku BTC.

### [STRATEGI] Dua mode: sell mode vs accumulation mode
- **Insight:** Slide `[04:10]`: "Accumulation mode is identical with the trim switched off." Lisan
  `[03:41]-[03:50]`: buat yang "never sell your Bitcoin", sistem tetap dipakai — pause DCA di atas p85
  tetap membangun reserve, cuma tidak ada trim. Klaim: masih outperform blind DCA.
- **Indikator terkait:** MVRV Quantile percentile
- **Relevan ke:** pilihan desain langsung — accumulation mode jauh lebih dekat ke K4/lantai waktu
  (spot only, tidak jual)
- **Test klaim:** Pemisahan yang jujur dan penting, karena mode yang relevan untuk profil Yudi ada di
  antara keduanya. Dan justru mode accumulation-lah yang hasilnya **paling lemah**: 1,05× saja, max DD
  praktis tidak berubah (−83,2% vs −83,5%), dan **26% start date negatif**. Artinya seluruh daya tarik
  "beats Bitcoin" datang dari **leg jual + asumsi pajak 20%**, bukan dari kecerdasan indikatornya dalam
  mengatur pembelian.
- **Perlu validasi Claude Code:** Tidak — pernyataan tentang sistem mereka; implikasinya masuk Flag Prioritas.

### [STRATEGI] Grid search parameter (heatmap 5×5 dua sisi)
- **Insight:** Slide `[10:12]`: "Taxed median edge over blind DCA (pp) — 39 start dates 2014-2023, 50%
  floor. Orange box marks the chosen cell". Lisan `[09:23]-[09:38]`: "We tested every single combination
  possible. These are the optimal strategies." Sisi jual dipilih boundary 90 / trim 0,75% = **+10,1 pp**;
  sisi beli dipilih zone 10 / reserve 10% = **+10,1 pp**.
- **Indikator terkait:** MVRV Quantile percentile
- **Relevan ke:** general / Governance
- **Test klaim:** Dari sisi transparansi ini di atas rata-rata — heatmap ditampilkan penuh, **sel terpilih
  bukan maksimum absolut** (93/1,0% juga +10,1; 5/10% dan 10/5% justru +10,2), dan presenter menyebut
  risiko overfit `[07:49]`. Tapi transparansi bukan obat untuk in-sample optimization: ~50 kombinasi diuji
  pada **satu path harga**. Sinyal diagnostik yang berguna ada di asimetri — sisi beli plateau lebar
  (+9,0 s/d +10,2 di hampir semua sel) = parameter tidak kritis, cenderung robust; sisi jual sensitif
  (+3,4 s/d +10,1, faktor 3×) = **di situlah risiko overfit terkonsentrasi, dan itu persis leg yang
  menghasilkan seluruh outperformance**. Angka = median edge; sebaran per start date tidak ditampilkan.
- **Perlu validasi Claude Code:** Tidak — tidak bisa direplikasi tanpa indikator sumbernya. Masuk sebagai
  catatan metodologis + dasar [KONFLIK] di bawah.

### [STRATEGI] Robustness eksekusi: hari/jam beli tidak material
- **Insight:** `[06:06]-[06:26]`: baseline pakai open weekly candle (tengah malam Senin), tapi juga diuji
  di US open dan pembelian acak Senin-Jumat — "fairly negligible differences in returns". Juga disebut
  varian deposit bulanan vs mingguan dan seed lebih besar.
- **Indikator terkait:** —
- **Relevan ke:** general — standar validasi pipeline ini (sensitivitas eksekusi)
- **Test klaim:** Cenderung benar secara a priori (untuk horizon 12 tahun, timing intra-minggu adalah
  noise) dan sudah didukung tidak langsung oleh validasi kita sendiri:
  `findings_dca_backtest_and_calmar.md` menunjukkan cadence mingguan vs bulanan beda <0,1 pp di CAGR.
  Tapi tidak ada satu angka pun disajikan ("fairly negligible") sehingga presisinya tidak bisa dinilai.
- **Perlu validasi Claude Code:** Tidak — sebagian sudah terkonfirmasi lewat findings 2026-07-28 (cadence);
  sisanya **tidak bisa diuji: data kita harian saja, tidak ada intraday**.

### [STRATEGI] Out-of-sample 39 start date: sell mode positif 100%, accumulation 74%
- **Insight:** Slide `[09:36]`: "Every start date, quarterly, 2014 to 2023 — sell mode positive on 100% of
  39, accumulation on 74%". Y = IRR advantage over blind DCA (pp). Biru (sell mode, after 20% tax):
  ~+9,5 s/d +11 pp untuk start 2014-2020, turun ~+6 pp untuk start 2021-2022, naik ~+8,5 pp start 2023 —
  selalu positif. Oranye (accumulation): **negatif** (~−0,2 s/d −0,6 pp) untuk start 2015-06 s/d 2016-12
  (~6-7 bar), sisanya +1 s/d +6 pp.
- **Indikator terkait:** MVRV Quantile percentile
- **Relevan ke:** general — menyentuh Governance poin 4 (backtest mesin utuh vs HODL/DCA, masih pending)
- **Test klaim:** Label "out-of-sample" menyesatkan: 39 start date kuartalan adalah **window overlapping
  dari satu path harga tunggal 2014-2026** — start 2014-Q1 dan 2014-Q2 berbagi >99% observasi, jadi n
  efektifnya mendekati 3 cycle, bukan 39. Parameter juga dikalibrasi pada path yang sama yang dipakai
  mengklaim outperformance, sehingga "100% positif" adalah pernyataan tentang **konsistensi internal**,
  bukan generalisasi. Pola bar-nya sendiri membocorkan ketergantungan regime: edge turun ke ~+6 pp untuk
  start 2021-2022 — window yang paling didominasi bear terbaru.
- **Perlu validasi Claude Code:** Tidak (untuk klaim 100%/74%) — tidak reproducible tanpa indikator. Yang
  reproducible cuma leg blind DCA-nya.

### [STRATEGI] Tabel hasil final — $1.000 seed + $100/minggu sejak Januari 2014
- **Insight:** Slide `[10:46]`, asumsi "0.1% fees, one-bar fill lag, 20% CGT on realised gains":

  | Metrik | Blind DCA | Accumulation | Sell mode (taxed) |
  |---|---|---|---|
  | Total paid in | $66.700 | $66.700 | $66.700 |
  | Final value | $2.968.017 | $3.115.675 | $5.794.249 |
  | Multiple of blind | 1,00× | 1,05× | 1,95× |
  | IRR | 54,0% | 54,7% | 64,0% |
  | BTC held | 46,8 | 49,1 | 73,9 |
  | Max drawdown | −83,5% | −83,2% | −70,4% |
  | Trade jual | 0 | 0 | 715 |
  | Pajak dibayar | $0 | $0 | $1.026.987 |

- **Indikator terkait:** MVRV Quantile percentile
- **Relevan ke:** general / Governance poin 4
- **Test klaim:** **Inkonsistensi:** slide bilang "$1,000 seed"; lisan `[05:50]` + `[09:52]` bilang
  "starting with $100". Tabel **internally consistent** — ketiga baris menyiratkan harga akhir BTC yang
  sama (≈$63,42k), jadi bukan angka karangan; yang belum terverifikasi adalah apakah leg blind DCA-nya
  cocok dengan data riil. **n=1 run, satu start date, satu path** — semua caveat sample size berlaku penuh,
  dan IRR 64% vs 54% terlihat dramatis tapi seluruh selisihnya bergantung pada leg jual + asumsi pajak
  flat 20%.
- **Perlu validasi Claude Code:** Ya — prioritas #4, scoped ke leg blind DCA saja.

**[VALIDASI — 6 Agustus 2026, CLOSED]** Leg **blind DCA reproducible**: seed $1.000 (2014-01-01) +
$100/minggu s/d 2026-07-15 menghasilkan **47,08 BTC / $66.500 setoran / XIRR 54,7% / maxDD −82,9%** (varian
dengan fee 0,1% + one-bar lag: 46,93 BTC, 54,6%, −82,9%) — semuanya dalam **±2%** dari klaim video setelah
dikoreksi selisih data ~3 minggu. **Inkonsistensi slide-vs-lisan terselesaikan ke sisi SLIDE**: $66.700
hanya bulat dengan seed $1.000 (657 setoran, terakhir 2026-07-29, tepat sebelum video terbit); seed $100
menuntut setoran sampai 2026-09-30 — mustahil. **n = 1 window historis, 4 konfigurasi; maxDD −83%
didominasi satu cycle (bear 2018)**. Dua leg lain tidak direplikasi (parameter black-box) — jadi klaim
outperformance 1,95× **tetap belum terverifikasi**; yang terverifikasi hanya bahwa baseline pembandingnya
kredibel.
Detail: [`findings_dca_leg_reproduction.md`](findings_dca_leg_reproduction.md)

### [BARU] Sell mode memangkas max DD −83,5% → −70,4%; accumulation praktis nol
- **Insight:** Dari tabel slide `[10:46]`: max DD blind DCA −83,5%, accumulation −83,2% (praktis tidak
  berubah), sell mode −70,4%. Artinya **pengurangan drawdown datang dari trim, bukan dari pause-DCA**.
- **Indikator terkait:** MVRV Quantile percentile
- **Relevan ke:** **K1** (alasan jual 20-30% di puncak sebagian adalah manajemen drawdown), general
- **Test klaim:** Ini temuan paling relevan secara praktis dan sekaligus paling merugikan narasi video.
  Kalau preferensinya accumulation mode, sistem ini memberi +5% nilai akhir dan **0,3 poin** perbaikan
  drawdown — tidak material dibanding kompleksitas yang ditambahkan. Angka −83,5% juga bukan properti
  strategi melainkan **properti BTC**: kita sudah mengukur −82,9% untuk equity curve DCA mingguan
  2014-2026 (findings 2026-07-28), jadi baris itu cross-check dan cenderung akurat. Bahkan −70,4% masih
  jauh di atas ambang psikologis manapun, jadi "pengurangan risiko" di sini bersifat kosmetik. n=1 run.
- **Perlu validasi Claude Code:** Tidak — baris DCA-nya sudah ter-cross-check lewat validasi leg DCA;
  baris sell mode butuh replikasi penuh yang tidak tersedia. Tetap masuk Flag Prioritas diskusi.

### [STRATEGI] Mode kegagalan yang diakui: strategi butuh reserve terbangun dulu
- **Insight:** `[08:55]-[09:19]`: satu-satunya fase yang **tidak** outperform adalah start date di sekitar
  bottom bear 2014-2016, "because you haven't built up a cash reserve yet. So you're competing with blind
  DCA but then not having the cash reserve to actually deploy more at these cycle lows."
- **Indikator terkait:** MVRV Quantile percentile
- **Relevan ke:** **K4 / K5 / lantai waktu** — framework juga bergantung pada cash pool yang harus sudah ada
- **Test klaim:** Direklasifikasi dari [BARU] ke [STRATEGI] — ini pengakuan tentang sistem mereka, bukan
  insight baru tentang perilaku BTC. Nilainya diagnostik: sistem hanya unggul kalau sudah melewati minimal
  satu puncak untuk mengisi reserve, artinya edge-nya adalah **fungsi dari cold-start**, bukan dari kualitas
  sinyal. Juga contoh telanjang masalah independensi: 6-7 dari 39 bar negatif semuanya dari satu jendela
  cycle yang sama. Paralel langsung ke framework: K4 juga bergantung pada K1 sudah dieksekusi.
- **Perlu validasi Claude Code:** Tidak — tidak menghasilkan hipotesis testable terhadap data on-chain kita.

### [STRATEGI] Asumsi biaya & pajak
- **Insight:** `[04:51]-[05:05]` dan `[08:16]-[08:37]`: 0,1% fee per sale, 20% CGT pada **setiap** trade
  profitable, one-bar fill lag. Eksplisit: "This isn't taking into account any thresholds of capital gains
  allowance or setting your losses, etc. This is 20% on every single profitable sale you ever make."
  715 trade jual, total pajak $1.026.987.
- **Indikator terkait:** —
- **Relevan ke:** general
- **Test klaim:** Disclosure-nya jauh lebih baik dari video 2026-07-28 (yang tidak menyebut fee sama
  sekali) dan asumsinya konservatif ke arah yang benar — kalau ada bias, arahnya melebih-lebihkan biaya.
  Tapi ada yang tidak dibahas: 715 taxable event adalah **beban administratif nyata**, 20% flat bukan tarif
  yurisdiksi Yudi, dan **slippage/spread untuk 715 eksekusi kecil tidak dihitung sama sekali** — begitu
  juga opportunity cost reserve $1,1 juta yang menganggur tanpa yield.
- **Perlu validasi Claude Code:** Tidak — asumsi akuntansi/pajak, bukan klaim tentang data on-chain.

### [BARU] Kalibrasi ukuran trim berdasar base rate frekuensi sinyal
- **Insight:** `[05:20]-[05:42]`: alasan trim maksimum cuma 0,75%/hari adalah karena "about 12% of
  Bitcoin's days are in this sell region. Over one in 10. There's quite a lot of time that you're going to
  be taking profit. So it doesn't want to be a monumental amount." Diperkuat `[05:17]`: "we can be at new
  all-time highs looking very overvalued and still double."
- **Indikator terkait:** MVRV Quantile percentile
- **Relevan ke:** **K1** (jual 20-30%), **K4**, **lantai waktu**, general
- **Test klaim:** Ini prinsip paling transferable dari seluruh video dan satu-satunya yang bisa
  **memperbaiki** framework tanpa mengimpor indikator mereka. Framework menetapkan sizing K1 dan K4 tanpa
  referensi eksplisit ke base rate zona — padahal angkanya sudah ada dan tercantum di Decision Framework
  sendiri (Z5 = 703 hari). Titik lemahnya: prinsip ini masuk akal untuk aksi kontinu (per hari), tapi K1
  adalah aksi **event-driven sekali jalan** yang base rate-nya ~1 per cycle — jadi tidak otomatis berlaku
  ke K1. n = argumen desain, bukan klaim empiris.
- **Perlu validasi Claude Code:** Ya — prioritas #5, sebagai input desain.

**[VALIDASI — 6 Agustus 2026, CLOSED]** Prinsip **terverifikasi secara aritmetika**: Z5 = **703 hari =
12,6%** dari 5.578 hari (2011-02 → 2026-07), persis cocok dengan angka di Decision_Framework v2 dan
praktis identik dengan "12% of days" yang disebut video. Tapi implikasinya untuk framework kita
**kebalikan dari kekhawatiran awal**: kapasitas cash pool K4 + lantai waktu **tidak pernah habis sebelum
cycle low** di **n=3 bear selesai** — terpakai 53,4% (2014-15, 37 hari deploy), **hanya 7,6% (2018, 27
hari)**, 82,4% (2022, 91 hari). Risiko nyatanya bukan kehabisan amunisi, tapi **sinyal terlalu jarang
nyala**. Di bear berjalan 2025-26 (per 2026-07-15) **0 hari deploy** — k4_count=0, zona ZD, dan lantai
waktu masih terblokir syarat close<RP walau jam 9 bulan sudah lewat 2026-07-03. Prinsip ini berlaku untuk
aksi kontinu, **bukan** untuk K1 yang event-driven sekali per cycle.
Detail: [`findings_zone_base_rate_sizing.md`](findings_zone_base_rate_sizing.md)

### [KONFIRMASI] Di atas p85 = pause, bukan sell all — overvalued bisa 10× dulu
- **Insight:** `[04:34]-[04:46]`: "even when we're starting to get a little bit overvalued, you know, we
  might be overvalued at a few thousand dollars before we rally 10x. So yes, we are accumulating up until
  the 85th percentile."
- **Indikator terkait:** MVRV Quantile percentile
- **Relevan ke:** **K1** (jual hanya 20-30%, bukan seluruhnya), **K2** (masih beli dip di dalam bull)
- **Test klaim:** Sudah cross-confirmed dari sumber lain di `source_index.md` (2025-02-23, "Extreme greed
  pertama bukan sinyal exit", 2/2 cycle, upside +183% s/d +836%). Konfirmasi ketiga dari channel berbeda
  menaikkan keyakinan tapi **bukan sampel independen baru** — semuanya membaca 3-4 cycle BTC yang sama.
  Catatan: diminishing amplitude berarti upside lanjutan **cenderung menyusut** tiap cycle, jadi jangan
  diperlakukan sebagai jaminan.
- **Perlu validasi Claude Code:** Tidak — established, sudah CLOSED lewat validasi F&G peak.

### [KONFLIK] Kalibrasi parameter lewat grid search penuh
- **Insight:** `[09:23]-[09:38]`: "We tested every single combination possible. These are the optimal
  strategies." Heatmap `[10:12]` menunjukkan grid 5×5 di dua sisi = ~50 kombinasi parameter, lalu sel
  dengan edge tertinggi dipilih.
- **Konflik dengan:** **Decision Framework v2 § Governance poin 1**, protokol usulan sinyal baru lapis
  pertama: "threshold a priori **tanpa grid search**". Juga CLAUDE.md § STANDAR VALIDASI poin 6.
- **Alasan konflik:** Parameter final (boundary 10/85/90, trim 0,75%/hari, reserve 10%/hari, floor 50%)
  adalah hasil optimisasi in-sample di deret harga **yang sama** dengan yang dipakai mengklaim
  outperformance. "39 start date" tidak memperbaiki ini karena overlapping dari satu path. Sisi jual
  sensitif (edge 3,4 → 10,1 antar sel) = persis leg yang menghasilkan seluruh keunggulan sistem.
  Nuansa yang harus ikut dicatat: heatmap ditampilkan penuh, sel terpilih bukan maksimum absolut, sisi
  beli plateau lebar, presenter sadar risiko — praktik yang lebih baik dari kebanyakan konten sejenis,
  tapi tetap tidak lolos lapis-1 protokol kita.
- **Rekomendasi:** **Abaikan angka parameternya** — jangan impor 10/85/90 / 0,75% / 10% / 50% ke framework
  dalam bentuk apa pun. **Pertahankan prinsipnya** (base-rate sizing, bentuk ramp) sebagai kandidat
  diskusi yang harus lewat 4 lapis Governance sendiri.

### [KONFLIK] Mekanik exit kontinu vs K1 event-driven
- **Insight:** Video menjual 0,75% stack/hari secara ramp sepanjang ~11,8% hari (>p90), dipicu hanya oleh
  satu angka valuasi. Framework K1 menjual 20-30% sekaligus pada OR-gate event (harga turun dari Z5 ke Z4
  ATAU gap MA90−MA60 STH-SOPR memuncak dan turun ≥14 hari), dengan syarat awal, 5 sinyal peringatan, dan
  peringatan eksplisit "jangan tunda" karena window menyempit (~30 hari di 2017 → bisa 6 hari di 2025).
- **Konflik dengan:** **K1** (trigger + sizing + urgensi), dan lebih luas dengan arsitektur zone-based
  multi-sinyal Decision Framework v2 § 1.
- **Alasan konflik:** (a) **jumlah sinyal** — 1 indikator vs syarat awal + 5 sinyal + OR-gate; (b) **bentuk
  aksi** — ramp harian vs lump event; (c) **urgensi** — sistem video santai (sudah trim berbulan-bulan
  sebelum puncak), framework K1 justru menekankan kecepatan; (d) **dimensi leverage hilang total** —
  sistem video 100% spot, jadi K2/K5/K6 dan seluruh tabel Hard Limits LTV tidak punya padanan. Ini bukan
  pelanggaran hard LTV limit (tidak ada leverage = tidak ada pelanggaran), tapi berarti mengadopsinya =
  membuang seluruh lapisan manajemen loan yang justru jadi sumber risiko terbesar portofolio.
- **Rekomendasi:** **Diskusikan lebih lanjut dengan Yudi** — bukan sebagai kandidat pengganti, tapi untuk
  memutuskan apakah ada satu elemen yang layak diadopsi terbatas (trim kontinu kecil di Z5 sebagai
  pelengkap K1, bukan pengganti). Kalau diadopsi, wajib lewat 4 lapis Governance dan **tidak boleh
  menyentuh sisi loan**.

---

## Flag Prioritas

1. **Kondisi K4 #2 mati secara empiris** — nol hari nyala di 4 bear + suplemen 2011, membuat tier
   `count=4` (DCA 35%/bulan) tidak bisa dicapai. Ini temuan sampingan dari validasi rising-troughs tapi
   dampaknya lebih besar dari klaim aslinya: framework punya tier yang tidak pernah bisa hidup. Paralel
   dengan kondisi #1 K2 lama yang sudah dicabut di v2. Penempelan perbaikannya di project Onchain-Dashboard.

2. **Kapasitas cash pool K4 tidak pernah terpakai habis — masalahnya sinyal terlalu jarang nyala.**
   Terpakai 53,4% (2014-15), **7,6% (2018)**, 82,4% (2022). Bear 2018: cuma 27 hari deploy aktif sepanjang
   365 hari bear → >92% pool menganggur di titik bottom. Ini membalik asumsi awal tentang risiko sizing:
   yang berbahaya bukan agresivitas, tapi kelangkaan izin deploy.

3. **Bear berjalan 2025-26: nol jalur deploy nyala per 2026-07-15.** k4_count=0, zona ZD, harga belum
   pernah menyentuh RP sekalipun (P/RP terendah 1,101), dan lantai waktu terblokir syarat close<RP walau
   jam 9 bulan sudah lewat 2026-07-03. Sementara itu indikator video sudah membaca "bottom zone". Dua
   pembacaan yang berbeda material tentang di mana kita berada — ini yang paling mendesak dibahas.

4. **Angka headline "8%" sebagian besar adalah output asumsi, bukan data.** Proxy causal kami membaca
   21-23. Selisih ~13-15 poin datang dari model decay yang parameternya tidak diungkap. Ditambah lookahead
   bias struktural (rata-rata 4,6-10,5 pp, ekor sampai ±50-67 pp), chart historis yang dipakai membenarkan
   klaim itu tidak replikabel real-time.

5. **Seluruh daya tarik "beats Bitcoin" datang dari leg jual, bukan dari pengaturan pembelian.**
   Accumulation mode cuma 1,05× dengan perbaikan drawdown 0,3 poin dan 26% start date negatif. Untuk
   profil spot-heavy, sistem ini menambah kompleksitas besar untuk keuntungan yang tidak material.

6. **Prinsip base-rate sizing layak dibahas untuk K4/lantai waktu** — bukan untuk K1. Base rate framework
   sudah terukur (Z5 = 703 hari = 12,6%, terverifikasi persis), jadi prinsipnya bisa diterapkan. Tapi
   arah perbaikannya kemungkinan besar **menaikkan** frekuensi izin deploy, bukan mengecilkan ukuran aksi.

7. **Bentuk ramp kontinu vs step function di batas zona** — menghilangkan diskontinuitas dan tahan revisi
   data provider, menjawab kekhawatiran Governance poin 3. Backlog, pantas menunggu backtest mesin utuh.

---

## Yang Langsung Diabaikan

- **Promosi chart gratis & subscription BM Pro** `[00:03]-[00:12]`, `[11:22]-[11:48]` — indicator alerts,
  TradingView scripts, akses API. Tidak ada substansi analitis.
- **Narasi "jangan berpikir biner buy/sell, pikirkan probabilitas"** `[02:52]-[03:10]` — framing
  motivasional; substansinya sudah tertangkap di zone map.
- **Disclaimer & framing "if you don't know what you're doing, this is a good place to start" / "will it
  work forever? Maybe not"** `[03:12]-[03:35]`, `[10:59]-[11:22]` — jujur tapi tidak mengandung mekanik.
- **Klaim "hari/jam beli tidak material" sisi intraday** — tidak bisa diuji, data kita harian saja.
- **Angka puncak reserve dari grafik (~50%/72%/62%)** — low confidence dari resolusi frame, tidak dipakai
  sebagai anchor kesimpulan manapun.

**Catatan cross-check yang disimpan (bukan insight):** tooltip di slide `[02:05]` memberi dua pasangan
(tanggal, MVRV, RP) yang berguna untuk memastikan definisi MVRV/RP BM Pro sama dengan yang dipakai
dashboard — Aug 2024: BTC $59.060 / MVRV 1,88 / RP $31.414; Mar 2023: BTC $23.470 / MVRV 1,18 / RP $19.860.
Angka dari frame, low confidence.
