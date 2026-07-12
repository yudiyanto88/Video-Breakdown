# Bitcoin Whales Are Accumulating Right Now
**Channel:** On-Chain Mind
**Tanggal video:** 2025-01-27
**Tanggal analisis:** 2026-07-12
**Link:** https://youtu.be/eavpxyuWrvE

---

## Ringkasan

Video pendek (7:07) berbasis chart CryptoQuant yang membaca kondisi market akhir Januari 2025 (pasca rally $100K Desember 2024, sekitar inaugurasi Trump). Struktur argumennya tiga lapis: (1) large investors/whales sedang akumulasi — monthly growth rate holdings berbalik dari -0.25% (14 Jan) ke +2% (17 Jan), dan sejak November whale menambah 16.2M → 16.4M BTC sementara retail turun 1.75M → 1.69M; (2) sell pressure sudah reda — daily realized profit anjlok dari ~$10B/hari di puncak Desember ke $2-3B/hari, dan trader profit margin turun dari ~60% ke hampir nol, level yang menurut channel historis identik dengan price floor; (3) TAPI demand melambat — Apparent Demand masih ekspansi namun lajunya turun 279k → 75k BTC, dan "Demand Momentum" (indikator custom: Δ30d STH supply − Δ30d LTH supply) anjlok 1.7M → 100k BTC. Kesimpulan channel: floor kemungkinan terbentuk, tapi rally berikutnya conditional pada demand yang re-accelerate. Ditutup segmen singkat ETH (supply inflationary lagi, -43% vs BTC).

Dua klaim inti divalidasi lawan data historis 4 cycle — **dua-duanya REJECT**: realized profit collapse tidak lebih baik dari baseline sebagai sinyal floor (dan gagal real-time di kejadian yang video ini sendiri bahas — koreksi Feb-Apr 2025 ke ~$76K menyusul), dan Demand Momentum terbukti redundant (≈ 2× momentum STH supply) dengan klaim gate yang arahnya justru terbalik.

---

## Insight Inventory

### [BARU] Whale monthly holdings growth berbalik tajam sebelum inaugurasi Trump
- **Insight:** Monthly growth rate holdings large investors melompat dari -0.25% (14 Jan) ke +2% (17 Jan) — tertinggi sejak pertengahan Desember. Klaim: perilaku whale adalah driver utama demand dan harga.
- **Indikator terkait:** Total Whale Holdings 30-day % change + EMA(30) (CryptoQuant) — tidak ada di framework; framework tidak punya metric cohort/entity-based sama sekali.
- **Relevan ke:** General — paling dekat sebagai kandidat confirming context K2/K5.
- **Test klaim:** Basis cuma satu episode 3 hari (n=1 event, jauh di bawah 3 cycle) → low-confidence. Klaim kausal "whale = driver harga" tidak diuji di video, cuma korelasi visual satu window. Titik lemah struktural: metric whale CryptoQuant rawan artefak entity-clustering — ETF custodian dan exchange cold wallet ikut terhitung whale, jadi "whale accumulating" bisa saja retail yang beli lewat ETF. Klaim salah kalau spike growth serupa di episode lain tidak diikuti kenaikan harga — video tidak menguji itu.
- **Perlu validasi Claude Code:** Tidak — data whale cohort tidak tersedia di dashboard (masuk daftar NEEDS-DATA-WE-DONT-HAVE di data_dictionary), tidak ada proxy setara di keluarga Glassnode.

### [BARU] Divergence whale vs retail: whale akumulasi, retail distribusi
- **Insight:** Sejak 4 November: whale 16.2M → 16.4M BTC (+200k), retail 1.75M → 1.69M BTC (-60k). Klaim: divergence ini driving force kenaikan harga terakhir.
- **Indikator terkait:** Larger Investors vs Retail holdings (CryptoQuant) — tidak ada di framework.
- **Relevan ke:** General; kalau valid pun sifatnya confirming context fase bull, bukan primary signal.
- **Test klaim:** Satu episode ~3 bulan, n=1 → low-confidence. Magnitude lemah sebagai "driving force" (net kecil relatif volume harian), atribusi kausal tidak diuji. Artefak sama dengan insight #1: perpindahan coin dari address kecil ke custodian besar tercatat "retail jual, whale beli" padahal secara ekonomi bisa jadi retail yang tetap pegang exposure via ETF.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia.

### [KONFIRMASI] Realized profit anjlok $10B → $2-3B/hari = heavy selling sudah lewat
- **Insight:** Di puncak profit-taking Desember (harga dekat $100K) daily realized profit ~$10B/hari; per Januari turun ke ~$2-3B/hari. Interpretasi: sebagian besar heavy selling di belakang, pasar masuk fase tenang yang jadi pijakan leg naik berikutnya.
- **Indikator terkait:** Realized Profit/Loss harian USD (CryptoQuant) — varian USD tidak ada di framework; padanan konsep: aSOPR reset (K2 kondisi #2).
- **Relevan ke:** K2 kondisi #2.
- **Test klaim:** Angka $10B/$2-3B absolut USD, tidak comparable antar cycle — versi teruji harus dinormalisasi market cap (`rrp`). Kelemahan inti: realized profit collapse terjadi di dua situasi berlawanan — dip sehat mid-bull ATAU tepat setelah cycle top (seller kehabisan profit karena harga sudah jatuh). Metric ini sendirian tidak bisa membedakan keduanya.
- **Perlu validasi Claude Code:** Ya — sudah divalidasi:

**[VALIDASI — 2026-07-12, CLOSED]** verdict: **REJECT** — event rrp SMA7 drop ≥70% dari peak 60d saat harga>RP hanya menghasilkan "floor" (maxDD<15% & fwd90>0) 19/44 kali (43%), di bawah baseline 49%, dengan median maxDD −16.6%; pola yang sama muncul tepat setelah cycle top (Des 2017 −50%, Nov 2021 −39%, Apr 2022 −54%). Event Des 2024 yang dibahas video sendiri diikuti maxDD −15.9% dan fwd90 −11.6% (koreksi Feb-Apr 2025 ke ~$76K). 27/44 event overlap dengan K2 kondisi #2 — tidak ada nilai inkremental. n=44 event, 4 cycle merata. Detail: [`findings_realized_profit_collapse.md`](findings_realized_profit_collapse.md)

### [KONFIRMASI] Trader profit margin ~60% → ~0 = level historis price floor
- **Insight:** "Traders' on-chain realized profit margin" turun dari ~60% (overheated, Nov-Des) ke hampir nol pertengahan Januari. Klaim: di level ini traders tidak punya insentif jual → sell pressure turun → indikasi floor.
- **Indikator terkait:** Profit/Loss Margin + SMA(30) (CryptoQuant). Dekomposisi: Margin = (Price − Realized Price)/Realized Price = MVRV − 1 versi kohort trader ≈ STH-MVRV − 1. Margin ~0 ≈ STH-MVRV ≈ 1.0 — re-skin dari konsep yang sudah aktif di framework.
- **Relevan ke:** K2 kondisi #1 (STH-MVRV < 0.95 saat dip); sekunder K1 sinyal #3.
- **Test klaim:** Konsep established — sudah dipakai framework dan sudah dibahas video 2025-01-22 (STH Cost Basis sebagai confirming signal, tercatat di video_index). "60% = overheated" adalah threshold absolut → catat nilainya, framework pakai pola relatif. Klaim salah kalau harga tembus jauh di bawah STH cost basis setelah margin nol — memang terjadi tiap bull dip berubah bear (Nov 2021), makanya framework memperlakukan STH-MVRV sebagai satu dari lima kondisi, bukan sinyal tunggal.
- **Perlu validasi Claude Code:** Tidak — established, tidak perlu tes ulang.

### [BARU] Apparent Demand masih ekspansi tapi laju turun drastis (279k → 75k BTC)
- **Insight:** Apparent Demand (30d) masih di teritori ekspansi, tapi laju turun dari 279k BTC (awal Des) ke 75k BTC. Klaim: rally sustainable butuh demand growth pick up dulu.
- **Indikator terkait:** Apparent Demand (30d) (CryptoQuant) — tidak ada di framework aktif.
- **Relevan ke:** General — sisi demand tidak dimodelkan eksplisit di framework.
- **Test klaim:** Hipotesis deceleration Apparent Demand **sudah diuji dua kali dan REJECT dua-duanya** (versi mentah dan versi kondisional-per-zona — lihat `Onchain-Dashboard/research/findings/video-breakdown/apparent_demand_hypothesis_findings.md`): hasil rapuh dan kontradiktif lintas cycle. Rekonstruksi kita (issuance − Δ supply 1yr+) sudah terverifikasi setara, jadi ini bukan soal beda data — hipotesisnya memang sudah tumbang.
- **Perlu validasi Claude Code:** Tidak — sudah diuji dan reject; jangan tes ulang tanpa formulasi yang secara struktural baru.

### [INDIKATOR CUSTOM] Demand Momentum anjlok 1.7M → 100k BTC
- **Insight:** "Demand Momentum" turun dari 1.7M ke 100k BTC (awal Des → akhir Jan). Klaim: buying pressure melambat drastis; tanpa rebound momentum, harga sulit dapat traksi.
- **Indikator terkait:** Demand Momentum (CryptoQuant). Dekomposisi (dari footnote chart): DM = Δ30d(Short-term Supply) − Δ30d(Long-term Supply). Karena STH + LTH ≈ total supply, DM ≈ 2×Δ30(STH supply) − issuance — efektifnya momentum STH supply yang di-rescale, bukan informasi dari dua sumber independen.
- **Relevan ke:** General; bersinggungan logika LTH→STH transfer di Z3-Z5.
- **Test klaim:** Klaim gate "tanpa rebound momentum harga sulit naik" tidak pernah diuji kuantitatif di video (satu window Des-Jan, n=1 → low-confidence). Kandidat counterexample: rally supply-squeeze awal bull saat LTH belum distribusi.
- **Perlu validasi Claude Code:** Ya — sudah divalidasi:

**[VALIDASI — 2026-07-12, CLOSED]** verdict: **REJECT + REDUNDANT** — DM secara aljabar identik dengan 2×Δ30d STH supply minus issuance (corr 0.994, residual 0), bukan indikator baru. Klaim gate-nya terbalik: di Z3-Z4, state DM-collapsed justru punya median fwd90 +19.6% vs +6.3% saat DM-rebound, dan 16 dari 26 rally ≥20%/90d full-history dimulai saat DM masih collapsed (14/26 saat DM negatif — termasuk COVID-bottom Mar 2020 dan rally Feb 2025 tepat setelah video ini). n=30 event / 26 rally episode, tersebar merata 4 cycle. Detail: [`findings_demand_momentum.md`](findings_demand_momentum.md)

### [STRATEGI] Supply-side sudah beres, demand-side jadi syarat rally
- **Insight:** Framing dua sisi: floor dikonfirmasi dari supply-side (profit-taking exhaustion), trigger rally dikonfirmasi dari demand-side (Apparent Demand + Demand Momentum). Framework saat ini murni supply-side/cost-basis — tidak punya "demand-side gate".
- **Relevan ke:** General. Bukan konflik dengan keputusan terkunci — komplemen, bukan pengganti zone-based + K-node. Tidak menyentuh hard constraint LTV.
- **Test klaim:** Koheren secara naratif, tapi kedua instrumen demand-side-nya sudah tumbang: Apparent Demand reject 2× (insight #5), Demand Momentum reject + redundant (insight #6). Tanpa instrumen operasional yang lolos uji, strategi ini tinggal narasi.
- **Perlu validasi Claude Code:** Tidak — strategi payung tidak bisa diuji langsung; nasibnya mengikuti hasil uji instrumennya, dan keduanya gagal.

### [BARU] ETH inflationary lagi: supply +500k sejak April 2024, -43% vs BTC
- **Insight:** ETH underperform -43% vs BTC sejak akhir 2023; supply naik +500k ETH sejak April 2024, kembali ke level pre-Merge — menggerus narasi deflasi pasca-Merge (Sep 2022).
- **Indikator terkait:** ETH Total Supply + Total Fees Burned (CryptoQuant) — di luar scope.
- **Relevan ke:** Tidak ada — framework BTC-only.
- **Test klaim:** Faktual dan mungkin benar, tapi tidak actionable untuk keputusan apapun di framework; tidak ada data ETH di dashboard.
- **Perlu validasi Claude Code:** Tidak — masuk "Yang Langsung Diabaikan".

---

## Flag Prioritas

1. **Realized profit collapse GAGAL sebagai sinyal floor — termasuk di kejadian yang video ini sendiri bahas** — insight yang awalnya masuk [KONFIRMASI] (sejalan logika aSOPR reset) ternyata reject di data: hit rate 43% di bawah baseline 49%, dan setup Des 2024→Jan 2025 yang dibicarakan video diikuti koreksi ke ~$76K. Mekanismenya jelas: metric ini tidak bisa membedakan "selling exhausted karena floor" vs "profit menguap karena top baru lewat". Konfirmasi bagus bahwa K2 tetap butuh kombinasi kondisi, bukan single-metric — worth didiskusikan sebagai catatan kewaspadaan kalau narasi "realized profit sudah turun = aman" muncul lagi.
2. **Demand Momentum = 2× STH supply momentum, dan klaim gate-nya terbalik** — dekomposisi aljabar exact + hasil uji yang arahnya kebalikan dari klaim (DM collapsed justru forward return lebih baik; mayoritas rally lahir saat DM flat/negatif). Berguna sebagai referensi cepat kalau indikator "demand momentum" CryptoQuant ini muncul lagi di video lain.
3. **Whale/retail cohort data sebagai blind spot yang disadari** — dua insight whale tidak bisa diuji karena dashboard tidak punya data cohort entity-based, dan metric-nya sendiri rawan artefak ETF custodian. Bukan urgent (bukan primary signal), tapi worth dicatat sebagai keterbatasan yang diketahui, bukan yang terlewat.

---

## Yang Langsung Diabaikan

- **ETH inflationary (insight #8)** — di luar scope framework BTC-only, tidak ada data ETH di dashboard.
- **Narasi katalis "Trump inauguration"** — atribusi kausal tanpa mekanik on-chain; angka timing-nya sudah tercatat di insight #1.
- **Apparent Demand deceleration (insight #5)** — bukan diabaikan karena tidak relevan, tapi karena sudah diuji 2× dan reject; tidak dites ulang tanpa formulasi baru.
- Intro/outro hype ("massive power shift", "edge of another rally") — framing dramatis, substansinya sudah tercakup di inventory.
