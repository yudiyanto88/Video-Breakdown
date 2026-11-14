# This New Bitcoin Chart Shows Market Exhaustion
**Channel:** Joao Wedson (Alphractal) — bukan On-Chain Mind / Tristan Colt
**Tanggal video:** 2026-07-08
**Tanggal analisis:** 2026-07-13
**Link:** https://youtu.be/0u409y3Rl0c

---

## Ringkasan

Video pendek (7:48) yang seluruhnya memperkenalkan SATU indikator proprietary Alphractal: **Structural Market Bands (SMB)**, dibuat oleh Rafael Tellis (researcher Alphractal). SMB terdiri dari dua zona band di atas dan di bawah harga — Structural Resistance (merah, Upper+Lower band) dan Structural Support (hijau, Upper+Lower band) — plus Structural Midline di tengah, dengan sinyal otomatis saat harga menembus band terluar. Komponen yang disebut: on-chain data, "old coins being moved" (kemungkinan; auto-caption menulis "altcoins"), Accumulation & Distribution Index milik Alphractal, on-chain cost basis, dan "a bit of math" — formula tidak diungkap sama sekali (black box).

Klaim-klaim utamanya: breach di bawah lower support band = bottom & zona beli terbaik; sentuhan zona resistance = pullback agresif; break ke atas upper resistance band = cycle top / local top (sinyal exhaustion); midline = intermediate support; dan satu klaim forward-looking — bear market cenderung menguji lower support band dua kali ("double test") sebelum bottom terkonsolidasi, dan karena bear berjalan baru test sekali, dia mengekspektasikan retest kedua (band ≈ $56K per tooltip 2026-06-27, low confidence dari resolusi frame).

Secara fungsional SMB paralel dengan zone structure Z1–Z5 framework (support bawah ≈ CVDD/STH RP, midline ≈ RP/AVIV Mean, resistance atas ≈ AVIV Upper), dikemas dalam satu chart proprietary. Dua klaim paling substantif divalidasi dengan data — **keduanya NOT SUPPORTED**.

---

## Insight Inventory

### [INDIKATOR CUSTOM] Structural Market Bands (SMB) — komposisi indikator
- **Insight:** Model band dua layer (Resistance Zone merah atas, Support Zone hijau bawah, Structural Midline) untuk mendeteksi "structural exhaustion". Sinyal otomatis: Above Resistance Signal / Below Support Signal.
- **Indikator terkait:** SMB (custom). Komponen yang disebut: on-chain data, "old coins being moved" (≈ CDD/VDD?), A&D Index Alphractal (proprietary juga), on-chain cost basis (≈ Realized Price family), "a bit of math".
- **Relevan ke:** general — struktur fungsional paralel zone Z1–Z5.
- **Test klaim:** Dekomposisi penuh tidak mungkin — black box di dalam black box (A&D Index juga proprietary). Level tooltip 2026-06-27 (Midline ~$47-48K, Res Upper ~$98-99K, Sup Lower ~$56K) low confidence dari resolusi frame, jangan dipakai sebagai anchor. Secara fungsional kemungkinan tidak menawarkan informasi yang belum ter-cover zone structure framework.
- **Perlu validasi Claude Code:** Tidak — formula tidak tersedia, padanan fungsional sudah established.

### [INDIKATOR CUSTOM] Breach lower Support Band = local/historical bottom & zona beli terbaik
- **Insight:** Setiap penembusan ke bawah lower support band bertepatan dengan local/historical bottom; zona hijau = region beli terbaik tiap cycle.
- **Indikator terkait:** SMB Support Zone (lower band).
- **Relevan ke:** Z1 / K4.
- **Test klaim:** Basis ~3-4 event bottom, tapi frasa "local bottom OR historical bottom" lentur — hampir semua breach dekat suatu local bottom secara definisi. Falsifiability lemah. Framework sudah punya padanan lebih tegas: Z1 (Price < STH RP dengan ordering terbalik) + flag Price/CVDD + tabel agresivitas K4.
- **Perlu validasi Claude Code:** Tidak — established sebagai Z1/K4, SMB tidak replicable.

### [INDIKATOR CUSTOM] Sentuhan Resistance Zone = selling pressure & pullback agresif
- **Insight:** Setiap sentuhan region merah cenderung diikuti pullback agresif; di cycle 2021 sentuhan berulang menandai local tops sebelum downtrend.
- **Indikator terkait:** SMB Resistance Zone.
- **Relevan ke:** Z4/Z5, K1/K3.
- **Test klaim:** Basis 3 cycle, tapi tidak dikuantifikasi (berapa % pullback? berapa false positive?). Zona ini ambigu dua arah — video sendiri menyebut "very strong traction happens" di zona yang sama. Fungsional analog Price mendekati AVIV Upper yang sudah jadi tulang punggung K1/K3.
- **Perlu validasi Claude Code:** Tidak — padanan established, klaim tidak terkuantifikasi.

### [KONFIRMASI] Frekuensi visit Resistance Zone menurun saat naik = sign of weakness
- **Insight:** Seiring bull berjalan, harga makin jarang mengunjungi zona resistance — dibaca sebagai melemahnya momentum. Paralel konsep diminishing returns di syarat awal K1/K3, tapi mekanik beda: framework mengukur magnitude (MVRV & aSOPR lebih rendah tiap ATH), video mengukur frekuensi/durasi visit.
- **Indikator terkait:** SMB Resistance Zone; proxy framework: AVIV Upper (Z5).
- **Relevan ke:** K1, K3 (syarat awal).
- **Test klaim:** Basis ~3 cycle. Sudut frekuensi genuinely berbeda dari magnitude dan testable dengan data framework (durasi episode Z5 per leg). Supaya salah: top final justru terjadi saat visit Z5 paling sering/paling lama.
- **Perlu validasi Claude Code:** Ya — apakah durasi/frekuensi episode Z5 menurun monotonic menjelang top, dan apakah menambah lead time vs syarat awal K1.

**[VALIDASI — 2026-07-13, CLOSED]** Verdict: **NOT SUPPORTED** (via proxy AVIV Upper). Diuji di 3 full cycle + 2 context: durasi episode Z5 TIDAK menurun monotonic di cycle manapun (0/3) — kebalikannya, top 2017 dan 2025 justru terbentuk di episode Z5 TERPANJANG cycle-nya (303d dan 176d); hanya 2021 yang cocok arah klaim (210d→127d). Secara struktural sinyal ini juga tidak bisa menambah lead time: durasi episode baru diketahui saat episode berakhir = AVIV Upper cross-down = trigger K1/K3 yang sudah ada, sementara syarat awal K1 (diminishing MVRV/aSOPR) aktif 273–334 hari sebelum top. Catatan: SMB Alphractal black box — hasil ini menyatakan polanya tidak transfer ke band framework; band aslinya tidak bisa diverifikasi. Detail: [`findings_z5_visit_frequency.md`](findings_z5_visit_frequency.md).

### [INDIKATOR CUSTOM] Break Upper Resistance Band = ATH / cycle top / local top
- **Insight:** Setiap break ke atas upper resistance band, Bitcoin membentuk ATH — dan "either a cycle top or a local top" (dipakai sebagai sinyal euphoria/exhaustion, judul video).
- **Indikator terkait:** SMB Upper Resistance Band + Above Resistance Signal.
- **Relevan ke:** Z5 / K1 — fungsional analog Price ≥ AVIV Upper.
- **Test klaim:** Titik lemah paling serius di video: "either a cycle top or a local top" praktis unfalsifiable — SETIAP high adalah salah satu dari keduanya. Sinyal yang tidak bisa salah bukan sinyal. Tidak ada spesifikasi N hari / drawdown minimal X%.
- **Perlu validasi Claude Code:** Tidak — unfalsifiable dalam bentuk sekarang; padanan established (Z5/K1 OR-gate).

### [INDIKATOR CUSTOM] Structural Midline sebagai cost basis / intermediate support
- **Insight:** Saat harga turun dari region merah, cenderung mengunjungi midline; di cycle 2021 midline menahan Corona dump dan menopang uptrend.
- **Indikator terkait:** SMB Structural Midline; fungsional mirip RP / AVIV Mean.
- **Relevan ke:** Z2/Z3, K2 kondisi #5.
- **Test klaim:** Bukti hanya dari cycle 2020–2021 → **low confidence** (<3 cycle). Framework sudah mengkodifikasi perilaku ini lebih presisi di K2 kondisi #5 (bounce dari AVIV Mean ≤ hari ke-4), sudah divalidasi. Bear market mana pun menembus midline tanpa bounce — klaim "support" hanya kondisional di bull.
- **Perlu validasi Claude Code:** Tidak — established sebagai K2 #5.

### [INDIKATOR CUSTOM] Upper Support Band sebagai floor struktural pasca local top 2021
- **Insight:** Setelah local tops 2021, area yang menahan harga adalah upper support band — "Bitcoin hasn't lost this region".
- **Indikator terkait:** SMB Support Zone (upper band).
- **Relevan ke:** general.
- **Test klaim:** n=1 episode → **low confidence berat**. Klaim "hasn't lost this region" hanya bertahan dalam window yang dipilih pembicara — bear 2022 jelas menembus jauh di bawah level support mana pun dari 2021 (cherry-picked timeframe).
- **Perlu validasi Claude Code:** Tidak — n=1, tidak replicable.

### [BARU] Pola "double test" lower support band per bear market
- **Insight:** Di bear market, harga cenderung menguji lower support band DUA kali membentuk "consolidated bottom". Pembicara sendiri menyebut sample inkonsisten (2x, 1x, 2x). Bear berjalan baru test sekali → ekspektasi retest kedua "like what happened in 2022".
- **Indikator terkait:** SMB Support Zone (lower band); proxy framework: episode Z1, Price/CVDD.
- **Relevan ke:** K4 / Z1 — kalau valid, menyentuh timing agresivitas DCA (worth-kah menahan tranche menunggu "test kedua").
- **Test klaim:** n≈3-4 bear dengan minimal satu pengecualian eksplisit yang pembicara akui sendiri → **low confidence**. Falsifiability jelas: bear bottom tanpa retest kedua, atau retest terjadi tapi bukan bottom final. Satu-satunya klaim genuinely baru + forward-looking di video.
- **Perlu validasi Claude Code:** Ya — hitung episode test per bear historis (dua proxy), posisi final bottom, dan simulasi K4: DCA sejak episode pertama vs menahan pool menunggu test kedua.

**[VALIDASI — 2026-07-13, CLOSED]** Verdict: **NOT SUPPORTED**. Diuji dua proxy (episode Z1 dan P/CVDD<1.15, pemisah 30 hari) di 4 bear selesai + 1 berjalan: "double test" cuma terjadi di 1/4 bear (2014-15), dan test keduanya higher low +18% (CVDD) — final bottom selalu terbentuk di episode dalam PERTAMA (4/4). Simulasi K4 (4 tranche × 25%): menahan pool menunggu "test kedua" memperburuk avg entry di 4/4 bear (+3.1% s/d +13.8%), dengan risiko 50% test kedua tidak pernah datang. Bear berjalan: menurut proxy framework justru NOL test — Z1 belum pernah aktif (STH RP $67.6K masih jauh di atas RP $52.8K per 2026-07-12), jadi framing video "sudah test sekali" tidak map ke struktur zona framework sama sekali. Rekomendasi: jangan modifikasi K4. Detail: [`findings_double_test_bear_bottom.md`](findings_double_test_bear_bottom.md).

### [STRATEGI] SMB sebagai alat mean-reversion: beli di Support Zone, waspada di Resistance Zone
- **Insight:** Pendekatan implisit pembicara: akumulasi saat harga di/bawah Support Zone (capitulation), anggap rally unsustainable di Resistance Zone, midline = fair value reference.
- **Relevan ke:** general — filosofi SEJALAN dengan zone-based Z1–Z5 (bukan fundamental berbeda → tidak memicu flag STOP). Beda murni implementasi: bands proprietary black-box vs Realized Price family yang transparan dan auditable.
- **Test klaim:** Bukan threshold absolut (bands dinamis), tidak bentrok prinsip pola relatif. SMB tidak menawarkan aksi yang belum dikodifikasi di K1–K6; framework menang di falsifiability.
- **Perlu validasi Claude Code:** Tidak — sudah ter-cover; komponen testable-nya sudah dites di dua insight bervalidasi di atas.

---

## Flag Prioritas

1. **Pola "double test" lower support band (NOT SUPPORTED)** — paling penting justru karena hasil negatifnya actionable: data menolak menahan tranche K4 untuk "test kedua" (memperburuk avg entry 4/4 bear), DAN status bear berjalan menurut framework adalah NOL test (Z1 belum pernah aktif) — berbeda total dari framing video "sudah test sekali". Kalau narasi "tunggu retest $56K" ini beredar, framework punya jawaban data untuk mengabaikannya.
2. **Frekuensi visit zona resistance (NOT SUPPORTED)** — temuan sampingnya berguna: di band framework, episode Z5 justru makin PANJANG saat bull matang (top 2017 & 2025 terbentuk di episode terpanjang cycle-nya). Konsep diminishing versi magnitude (MVRV/aSOPR per ATH) tetap unggul dengan lead 273–334 hari.
3. **SMB sebagai keluarga indikator** — tidak perlu diadopsi (black box, padanan fungsional lengkap sudah ada di Z1–Z5), tapi worth tahu bentuknya kalau channel Alphractal muncul lagi di feed: klaim-klaimnya kemungkinan variasi dari struktur band yang sama.

---

## Yang Langsung Diabaikan

- **Break upper band = "cycle top or local top"** — unfalsifiable; setiap high memenuhi salah satunya.
- **Upper support band sebagai floor 2021** — n=1, cherry-picked window (bear 2022 menembusnya).
- **Kredensial Rafael Tellis (PhD fisika atom/molekul)** — appeal to authority, bukan evidence.
- **"It shapes the price like something quite magical"** — hype tanpa mekanik.
- **Level tooltip band (Sup Lower ~$56K dst.)** — low confidence dari resolusi frame, dan tidak bisa diaudit karena formula tertutup.
