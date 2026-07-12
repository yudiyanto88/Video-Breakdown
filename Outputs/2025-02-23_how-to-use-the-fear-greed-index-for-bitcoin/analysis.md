# How to Use the Fear & Greed Index for Bitcoin
**Channel:** On-Chain Mind
**Tanggal video:** 2025-02-23
**Tanggal analisis:** 2026-07-12
**Link:** https://www.youtube.com/watch?v=RBWUehoqfI0

---

## Ringkasan

Video pendek (8:18) edukasi soal Bitcoin Fear & Greed Index (sumber chart: CryptoQuant, dengan opsi SMA30D/90D/365D dan garis percentile). Konteks saat video: F&G di 61% ("neutral" versi channel), setelah dip singkat ke fear saat BTC ~$96K — padahal Desember 2024 F&G sempat peak ~81% di harga yang sama, poin bahwa harga sendirian tidak menentukan sentimen. Dua studi kasus historis jadi inti video: (1) rally 2021 — extreme greed pertama muncul jauh sebelum top (exit di situ = kehilangan ~4x kenaikan), dan peak F&G 92% terjadi saat BTC baru ~$30K, jauh sebelum price top final ketika index sudah cool off ke 70–80%; (2) bear 2022 — index nyangkut di extreme fear berbulan-bulan sambil harga terus turun, jadi F&G tidak berguna untuk timing exact bottom. Kesimpulan channel: F&G bagus sebagai alat baca sentimen dan untuk beli saat dip ke fear di tengah bull market, tapi bukan timing tool standalone — plus market call (Feb 2025) bahwa struktur masih bullish dan belum dekat major top berdasarkan "risk indicators" internal mereka yang tidak diungkap komponennya.

Relevansi ke framework: F&G hanya dipakai di satu tempat (K5 staging: pullback ≥5% + F&G < 50 → deploy 50–60%), jadi sebagian besar isi video bersifat konfirmasi desain yang sudah ada. Tiga insight divalidasi dengan data (hasil di inventory di bawah); catatan payung dari validasi: **data F&G baru mulai 2018-02 → maksimal 2 cycle — semua kesimpulan berbasis F&G otomatis low-confidence menurut standar framework sendiri (minimal 3 cycle)**.

---

## Insight Inventory

### [BARU] F&G peak mendahului price peak (sentiment divergence di top)
- **Insight:** Cycle 2021: peak F&G 92% saat BTC ~$30K; saat price peak final, index sudah cool off ke 70–80% ([03:18]–[03:38]). Pola: sentimen memuncak lebih dulu, harga top belakangan dengan sentimen yang sudah mendingin — struktural mirip pola diminishing MVRV/aSOPR yang jadi syarat awal K1/K3.
- **Indikator terkait:** Fear & Greed Index (+ SMA30D)
- **Relevan ke:** K1/K3 (kandidat confirming context), Z4/Z5
- **Test klaim:** Di video hanya 1 cycle (2021) — low-confidence. Bukan threshold absolut (pola relatif). Klaim salah kalau di cycle 2024–2025 F&G justru mencetak nilai tertinggi tepat di price peak final — bisa diuji out-of-sample karena data sudah sampai 2026.
- **Perlu validasi Claude Code:** Ya — apakah F&G peak selalu mendahului price peak di kedua cycle yang ada datanya, dan apakah pola diminishing per-ATH ala K1 berlaku.

**[VALIDASI — 2026-07-12, CLOSED]** Diuji di 2 cycle (F&G baru ada sejak 2018): F&G SMA30 memuncak ~10 bulan sebelum price top di KEDUA cycle (92.4 @ Jan-2021 → top Nov-2021 dgn F&G 74; 81.5 @ Des-2024 → top Okt-2025 dgn F&G 51), dan extreme greed pertama (≥75) muncul jauh di awal bull dengan sisa upside +836% (2019) / +183% (2023). Tapi versi ketat "F&G lebih rendah di SETIAP ATH baru" ala K1 TIDAK monotonic — jalurnya zigzag (mis. ATH Nov-2021 sentimennya lebih tinggi dari Apr-2021). Verdict: **SUPPORTED untuk struktur besar, PARTIAL untuk diminishing per-ATH** — n=2 cycle, layak jadi confirming context saja, bukan sinyal. Detail: [`findings_fg_peak_vs_price_peak.md`](findings_fg_peak_vs_price_peak.md).

**[EKSTENSI DARI DISKUSI — 2026-07-12, CLOSED] Sisi bottom (context K4):** usulan Yudi — F&G SMA30 membentuk bullish divergence dengan price menjelang bear bottom. Diuji (SMA30 saja, anchor major swing low ±45-60 hari): bear 2022 = regular bull div bersih (Jun $18,973/SMA30 11.9 → Nov $15,774/SMA30 27.3) tepat di bottom final; bear 2018 = pattern absent (SMA30 ikut lower low di capitulation Des 2018), tapi BUKAN false positive; bear 2025-26 = divergence sedang aktif (Nov-2025 → Feb-2026), belum bisa dinilai. Skor: 1 hit, 1 absent, 0 false positive (n=2 bear selesai). Sinyal satu arah: divergence hadir = context pendukung bottom-near, absen ≠ apa-apa. SMA14 dibuang (verdict flip vs SMA30 di titik kunci); anchor low minor dibuang (menghasilkan divergence palsu di ~$6.2K sebelum -48% di 2018). Kesimpulan diskusi: F&G SMA30 = **confirming context dua arah** — top (K1/K3) dan bottom (K4, hanya dibaca setelah kondisi primary K4 terpenuhi), never primary. Detail: [`findings_fg_sma30_bottom_divergence.md`](findings_fg_sma30_bottom_divergence.md).

### [BARU] SMA 30D dari F&G Index sebagai trend sentimen
- **Insight:** Selain daily reading, channel pakai 30-day SMA dari index untuk smooth fluktuasi jangka pendek dan baca trend sentimen ([00:48]–[01:01]). Tidak ada threshold/aturan pemakaian spesifik di video.
- **Indikator terkait:** Fear & Greed Index SMA30D
- **Relevan ke:** K5 (framework pakai raw F&G < 50 di staging deploy)
- **Test klaim:** Bukan klaim yang bisa salah dalam bentuk aslinya (cuma teknik smoothing). Versi operasional yang diuji: apakah SMA30D < 50 lebih baik dari raw < 50 sebagai trigger K5 — salah kalau SMA30D miss deploy window atau telat material.
- **Perlu validasi Claude Code:** Ya — bandingkan trigger raw vs SMA30D di event pullback ≥5% dalam window K5.

**[VALIDASI — 2026-07-12, CLOSED]** Window K5 direkonstruksi sesuai framework (STH RP cross RP → tutup 3 hari di atas AVIV Upper): 2019 & 2023-24, total 5 event pullback ≥5%. Raw F&G <50 trigger di 5/5 event; SMA30 <50 hanya 2/5 — miss 3 event sepenuhnya (termasuk deploy $22.4K Mar-2023 dan $40.1K Jan-2024 yang berakhir $61K+), dan saat kena pun lag 15–32 hari. Tidak ada whipsaw raw yang perlu difilter. Verdict: **NOT SUPPORTED — K5 staging tetap raw F&G < 50**; SMA30 hanya berguna sebagai alat baca trend/konteks, bukan trigger. n=5 event, 4/5 dari satu cycle. Detail: [`findings_fg_sma30_vs_raw_k5.md`](findings_fg_sma30_vs_raw_k5.md).

### [BARU] Extreme greed pertama bukan sinyal exit
- **Insight:** Rally 2021: extreme greed pertama muncul saat BTC ~$15K (caption menulis "$155,000" — jelas salah transkripsi; dari chart & konteks, ~$15K akhir 2020); exit di titik itu = kehilangan ~4x kenaikan berikutnya. Extreme greed bisa bertahan berbulan-bulan karena FOMO/retail frenzy ([02:56]–[04:04]).
- **Indikator terkait:** Fear & Greed Index
- **Relevan ke:** K1, Z4/Z5 — mendukung kenapa F&G memang tidak dipakai di sisi exit framework
- **Test klaim:** 1 cycle di video — low-confidence. Klaim berbentuk negatif ("jangan exit di sini") terhadap kesalahan yang framework memang tidak lakukan, jadi tidak actionable mandiri.
- **Perlu validasi Claude Code:** Tidak sebagai item mandiri — dititipkan sebagai sub-cek di validasi F&G peak di atas. Hasil: terkonfirmasi di kedua cycle (upside setelah extreme greed pertama +836% di 2019, +183% di 2023).

### [BARU] Path-dependence sentimen: harga sama, sentimen bisa beda total
- **Insight:** Des 2024 F&G ~81% saat BTC $96K; Feb 2025 BTC dip ke $96K lagi tapi index masuk fear ([01:43]–[02:15]). Sentimen dipengaruhi trend, momentum, volatility, makro — bukan level harga.
- **Indikator terkait:** Fear & Greed Index
- **Relevan ke:** general — sifat dasar F&G sebagai input K5
- **Test klaim:** Bukan klaim prediktif — deskripsi konstruksi index (memang multi-input). Nilai praktisnya: pengingat bahwa F&G < 50 di K5 adalah kondisi sentimen, bukan kondisi harga — fitur yang framework sudah manfaatkan.
- **Perlu validasi Claude Code:** Tidak — deskriptif, tidak actionable.

### [BARU] Neutral zone = regime konsolidasi / choppy range-bound
- **Insight:** Reading neutral (61% saat video) historis bertepatan dengan konsolidasi — choppy, range-bound, menunggu arah break ([05:28]–[05:55]).
- **Indikator terkait:** Fear & Greed Index (bucket Neutral)
- **Relevan ke:** general / Z3–Z4
- **Test klaim:** Maksimal 2 cycle data. Masalah definisi: 61 disebut "neutral" oleh channel, padahal di Alternative.me 61 sudah masuk Greed — bucket boundaries tidak standar antar provider, de facto threshold absolut dengan definisi goyah. Fungsi regime detection sudah dipegang zone structure (Z3/Z4 dari RP/AVIV) yang lebih solid.
- **Perlu validasi Claude Code:** Tidak — nilai tambah rendah, definisi bucket tidak stabil.

### [KONFIRMASI] Dip ke fear/extreme fear saat bull market = buying opportunity
- **Insight:** Saat bull, dip F&G ke fear/extreme fear sambil price action tetap kuat = entry bagus; fear-driven dips di bull cenderung short-lived ([05:03]–[05:25], diulang [07:40]–[07:49]).
- **Indikator terkait:** Fear & Greed Index
- **Relevan ke:** K5, Z2/Z3 — persis logika K5 staging yang sudah locked (pullback ≥5% + F&G < 50 → deploy 50–60%)
- **Test klaim:** 2 cycle (batas data F&G). Titik lemah: "short-lived" hanya berlaku selama regime bull benar — kalau bear onset (K3 Stage 2), K5 memang sudah dimatikan framework. Konfirmasi bersih.
- **Perlu validasi Claude Code:** Tidak — sudah established di K5.

### [KONFIRMASI] F&G tidak efektif untuk timing exact bottom di bear market
- **Insight:** Bear 2022: index bertahan di extreme fear berbulan-bulan sementara harga terus turun; menunggu sentiment shift = ketinggalan early recovery ([04:20]–[04:57]).
- **Indikator terkait:** Fear & Greed Index
- **Relevan ke:** K4, Z1 — mengkonfirmasi keputusan desain K4 yang tidak memakai F&G sama sekali (pakai LTH-MVRV, aSOPR/LTH-SOPR, Supply in Profit, Price/CVDD)
- **Test klaim:** Video pakai 1 cycle; data kita mencakup 2 bear (2018 sebagian + 2022) — tetap low-confidence, tapi membuktikan sebaliknya pun tidak mengubah apapun karena K4 sudah tidak pakai F&G.
- **Perlu validasi Claude Code:** Tidak.

### [KONFIRMASI] Sentiment alone bukan timing tool sempurna
- **Insight:** Meta-point penutup: extreme fear/greed bisa menandai turning point tapi tidak selalu align dengan high/low; mengandalkan F&G sendirian = missed opportunities ([06:48]–[07:11]).
- **Indikator terkait:** Fear & Greed Index
- **Relevan ke:** general — sejalan dengan posisi framework (F&G hanya salah satu kondisi staging K5, selalu dikombinasi pullback + sinyal lain, bukan primary)
- **Test klaim:** Naratif, tidak ada klaim empiris spesifik yang bisa difalsifikasi.
- **Perlu validasi Claude Code:** Tidak.

### [INDIKATOR CUSTOM] "Risk indicators" internal On-Chain Mind
- **Insight:** F&G 61% disebut "align well with our other risk indicators" → klaim "over halfway through this phase of the bull cycle" dan belum dekat major top ([05:55]–[06:15]). Komponen tidak diungkap sama sekali.
- **Indikator terkait:** Proprietary (black box), dikaitkan dengan F&G
- **Relevan ke:** general / Z3–Z4
- **Test klaim:** Tidak bisa didekomposisi, tidak bisa difalsifikasi — definisi indikatornya sendiri tidak tersedia. Sesuai aturan "jangan setuju karena nama besar": tanpa komponen, klaim turunannya tidak punya bobot evidencial. Abaikan sampai channel mengungkap komposisinya di video lain.
- **Perlu validasi Claude Code:** Tidak — tidak testable.

### [STRATEGI] Sentiment-weighted DCA
- **Insight:** DCA dibobot sentimen — perbesar beli saat fear/extreme fear, kurangi saat greed/extreme greed; klaim "historically performed well over multiple cycles" tanpa angka backtest ([02:32]–[02:48]).
- **Indikator terkait:** Fear & Greed Index
- **Relevan ke:** general — overlap parsial dengan K4/K5, bukan proposal pengganti framework
- **Test klaim:** "Multiple cycles" untuk F&G maksimal = 2 — overclaim ringan. Implisit pakai bucket absolut yang beda antar provider. Salah kalau backtest menunjukkan tidak beat uniform DCA secara konsisten.
- **Perlu validasi Claude Code:** Ya — backtest uniform vs sentiment-weighted DCA, dipecah per cycle.

**[VALIDASI — 2026-07-12, CLOSED]** Backtest DCA mingguan 2018-02 s/d 2026-07 (440 pembelian), bobot 2x/1.5x/1x/0.5x per bucket F&G, budget dinormalisasi: keunggulan BTC hanya +4.3% di Cycle A (2018-2022) dan +0.3% di Cycle B (2022-sekarang); varian agresif malah -0.1% di Cycle B. Angka full-period +7.4% menyesatkan — didorong efek alokasi lintas-cycle (bobot otomatis memindahkan budget ke era harga murah), bukan skill dalam-cycle; korelasi F&G vs forward return 52-minggu cuma -0.09. Verdict: **PARTIAL, cenderung NOT SUPPORTED untuk klaim kuat video** — tidak material (>5%) dan tidak konsisten. Tidak ada alasan menambahkan sentiment-weighting ke K4. n=2 cycle, Cycle B belum selesai. Detail: [`findings_fg_sentiment_weighted_dca.md`](findings_fg_sentiment_weighted_dca.md).

### [STRATEGI] Market call Feb 2025: struktur bullish, tunggu dip berikutnya
- **Insight:** Posisi channel per Feb 2025: market structure "very bullish", belum dekat major top, neutral = waiting period, dip ke fear berikutnya = beli ([06:06]–[06:23]).
- **Indikator terkait:** F&G + risk indicators internal (black box di atas)
- **Relevan ke:** general — konteks stance channel, bobot rendah
- **Test klaim:** Time-bound, sudah 17 bulan lewat. Retrospektif call-nya cukup akurat (bull berlanjut sampai top Okt-2025), tapi n=1 call benar ≠ metodologi terbukti, apalagi metodologinya tidak bisa diperiksa.
- **Perlu validasi Claude Code:** Tidak.

---

## Flag Prioritas

1. **F&G SMA30 sebagai confirming context dua arah** — [DIDISKUSIKAN 2026-07-12, disetujui Yudi] Sisi top: tervalidasi 2/2 cycle (SMA30 memuncak ~10 bulan sebelum price top, final top terbentuk dengan sentimen sudah dingin) → confirming context K1/K3. Sisi bottom (usulan Yudi): SMA30 bullish divergence vs price di major low → confirming context K4, 1 hit (2022) / 1 absent (2018) / 0 false positive, hanya dibaca setelah kondisi primary K4 terpenuhi. Keduanya n=2, never primary, tidak jadi syarat formal (pola per-ATH tidak monotonic; bottom divergence tidak selalu hadir).
2. **SMA30D vs raw F&G di K5** — hasil validasi justru kebalikan dari arah video: SMA30 sebagai trigger miss 60% deploy event. Berguna sebagai konfirmasi negatif bahwa K5 staging (raw < 50) sudah benar dan tidak perlu diutak-atik.
3. **Sentiment-weighted DCA overstated** — kalibrasi skeptisisme terhadap channel: klaim "performed well over multiple cycles" tidak tahan data (+0.3% di cycle terakhir). Bukti bahwa klaim tanpa angka dari channel ini tetap harus dites.

---

## Yang Langsung Diabaikan

- **"Risk indicators" internal** — black box penuh, komponen tidak diungkap, tidak bisa dievaluasi.
- **Neutral zone = konsolidasi** — definisi bucket tidak standar antar provider (61 = "neutral" versi channel, Greed versi Alternative.me); fungsi regime sudah dipegang zone structure yang lebih solid.
- **Path-dependence sentimen** — deskripsi konstruksi index, bukan insight actionable.
- **Market call Feb 2025** — time-bound, metodologi tidak bisa diperiksa.
- Definisi dasar F&G, ajakan subscribe, promosi newsletter, referensi Trump Inauguration — non-substantif.
