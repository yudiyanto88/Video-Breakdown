# Is The Bitcoin Bear Market Over?
**Channel:** On-Chain Mind
**Tanggal video:** 2026-08-25
**Tanggal analisis:** 2026-08-26
**Link:** https://www.youtube.com/watch?v=dacdmlQDAS4

---

## 🚩 FLAG — perlu keputusan Yudi

**STOP-1 — Unlock status bear DF v2 mekanis tidak bisa bunyi di cycle ini.**
DF v2 §0 mendefinisikan akhir-bear sebagai *STH RP cross naik melewati RP* (masuk Z2). Validasi P2 memastikan: bear 2025–26 adalah **bear siklus penuh pertama dalam 16 tahun dengan 0 hari struktur T** — min rasio STH RP/RP = **1,272**, sementara empat bear sebelumnya semuanya turun ke 0,842–0,924. Kalau ordering tidak pernah terbalik, cross-ke-atas tidak bisa terjadi → **status bear tidak pernah dibuka → K5 tidak akan pernah start**, berapapun tinggi harganya. Video menyodorkan gauge pengganti (harga reclaim STH RP) untuk pertanyaan yang framework kita memang belum punya jawabannya di struktur N. Gauge video-nya sendiri lemah (validasi 4 Agu 2026: 1 dari 8 reclaim, 12%), tapi gap framework-nya nyata. Rekomendasi dari validasi: **jangan ganti definisi unlock** — ketiga kandidat pengganti hit rate-nya cuma 25–29% — tapi pertimbangkan jalur darurat untuk sisi K5, sejenis yang sudah ada di K4-tanpa-Z1. Ini pending item (b) di Governance DF v2 yang sekarang punya bukti kuantitatif.

**STOP-2 — Adaptive Trend Model: flag STOP dari 11 Agu 2026 masih terbuka dan sekarang lebih mendesak.**
Video 11 Agu menyebut flip level $78K/$67K; video ini ~$68,3K dan sudah flip bullish. Level flip bergeser tanpa penjelasan mekanik → tidak reproducible dari luar, tidak bisa difalsifikasi. Sistem TA price-based ini sekarang bilang bullish sementara K-node bilang tunggu — konflik operasional yang belum diselesaikan sejak 12 Agu.

**⚠️ Caveat data yang berlaku untuk SEMUA validasi di bawah.** `data_master_all_metrics.csv` berhenti di **2026-07-15** (harga $65.098), sementara video membahas rally 19–25 Agustus 2026 ($63K → $80K+). **Kejadian yang diklaim video ada di luar data kita.** Semua validasi di sini adalah uji pola historis; semua "state saat ini" merujuk 2026-07-15, bukan tanggal video.

---

## Ringkasan

Video 9 menit yang menjawab satu pertanyaan: apakah rally $63K → $80K+ (19–25 Agustus 2026, +25%) menandakan bear market sudah selesai. Karakternya beda dari OCM biasanya — separuh pertama makro dan derivatif, baru separuh kedua on-chain.

Argumennya disusun sebagai rantai sebab-akibat: 19 Agustus, Treasury Secretary Bessent umumkan buyback obligasi 10–30 tahun digandakan (~$2B → ~$4B per operasi), dollar melemah, BTC dan gold naik 4–5%. Dorongan itu cukup untuk menembus $67K — batas atas range 6 minggu yang menurut pembicara terkunci karena median cost basis tahun berjalan ada di ~$64K. Di atas $67K menumpuk klaster short-liquidation hasil trader yang berulang kali short top range; begitu tembus, ~$3B short terlikuidasi dalam 24 jam (~92% dari total likuidasi, vs $264 juta long), BTC +8% dalam jendela yang sama.

Bagian yang dianggap pembicara paling penting justru sesudahnya: candle vertikalnya memang liquidation-driven, tapi funding tetap kalem, futures basis terkompresi, spot memimpin futures — dan ETF spot menyerap ~$2B dalam 4 hari (~$2,7B MTD, bulan terkuat sejak puncak bull Oktober), setara ~3,4× issuance harian. Jadi bacanya bukan biner "squeeze palsu vs rally asli" melainkan dua tahap: dorongan mekanis membuka jalan, modal riil menahannya.

Sisi on-chain: STH Realized Price di $68.500 — level yang sepanjang bear ini jadi resistance dan sudah menolak harga dua kali. Rata-rata pembeli baru bergerak dari underwater ke +14% profit dalam hitungan hari (STH-MVRV ≈ 1,14), dan % STH supply in profit meledak dari <5% di awal Juli ke >80%. Pembicara menutup dengan indikator custom-nya (Adaptive Trend flip bullish, Ω-Score di high-90s = overheated) dan satu kriteria uji eksplisit: yang menentukan bukan apakah BTC bisa print $85K besok, tapi apa yang terjadi di pullback pertama — konsolidasi mid-$70K dengan cost basis tetap di bawahnya = regime change; tembus balik $68K = mayoritas move ini memang cuma short tersqueeze.

---

## Insight Inventory

### [KONFIRMASI] Flip eksplosif % STH supply in profit sebagai pola awal bull
- **Insight:** % STH supply in profit meledak dari <5% di awal Juli ke >80% sekarang `[06:16]`–`[06:37]`. Pembicara menyebut ini "persis tipe flip profitabilitas eksplosif yang kamu mau lihat di awal bull market", dan menunjukkan chart 2022–2026 di mana awal bull sebelumnya juga menghasilkan kenaikan profitabilitas terbesar `[06:37]`–`[06:53]`.
- **Indikator terkait:** % STH Supply in Profit (level & rate of change)
- **Relevan ke:** K4 kondisi #3 (STH profit <10% — terpenuhi awal Juli, sekarang tidak lagi), veto K2 #1, dan transisi ke K5
- **Test klaim:** KB `supply_in_profit_loss v1.4` §1.7 baru mencatat n=2 (2018: 0%→55,6%/90hr; 2022: 0%→92%/60hr) — low-confidence menurut aturan framework sendiri, dan belum dioperasikan sebagai trigger di DF v2. Titik lemah terbesar: KB §1.6 menunjukkan lonjakan besar juga terjadi di bear rally yang GAGAL (2018 Mar 46,7%; 2019 Jul 64,5%; 2022 Mar 70,8% — semuanya diikuti leg turun). Supaya klaim salah: flip serupa ditemukan mendahului leg turun sama seringnya dengan mendahului bull.
- **Perlu validasi Claude Code:** Ya — flip <10% → >80% dalam ≤60 hari, hit rate ke unlock struktural, false positive rate, dan apakah signature KB §1.8 (STH profit > LTH profit) memisahkan hit dari miss.

**[VALIDASI — 2026-08-26, CLOSED]** Flip `pct_sth_in_profit` <10% → >80% dalam ≤60 hari terjadi **n=9** kali (2013: 3, 2017: 1, 2021: 3, 2025: 2 — hanya 4–5 siklus independen). Median return 365 hari memang +99,5%, tapi hit rate ke unlock struktural cuma **4/9** dan **3/9 diikuti drawdown ≥25% dalam 90 hari** (terburuk −48,4%). Kondisi tambahan STH-profit > LTH-profit **gagal memisahkan** — semua false positive justru ada di kelompok itu; yang benar-benar memisahkan adalah struktur at-gate (T: 4/4 unlock, N: 0/5), dan kondisi 2026-07-15 adalah **N**. Verdict: sebagian terkonfirmasi, **tidak layak jadi gate — confirming context saja**.
Detail: [`findings_sth_profit_flip_trigger.md`](findings_sth_profit_flip_trigger.md)

### [KONFIRMASI] STH Realized Price = support di bull, resistance di bear
- **Insight:** BTC diperdagangkan di bawah STH RP praktis sepanjang bear ini — pembeli baru underwater. Cost basis itu sekarang $68.500, disebut cenderung jadi support di bull dan resistance di bear, dan sudah ditolak bersih dari bawah dua kali selama bear ini `[05:29]`–`[05:53]`.
- **Indikator terkait:** STH Realized Price
- **Relevan ke:** Zone boundary Z1/Z1b/ZD/Z3; Price KB mencatat "Price > STH RP sustained" sebagai konfirmasi start-of-bull berbobot tinggi
- **Test klaim:** Sudah divalidasi 4 Agu 2026 (n=13 event di 5 bear, `findings_sth_rp_resistance_bear.md`): terkonfirmasi kuat sebagai perilaku resistance, drawdown 30d median −24,2% setelah event ditolak. Dua rejection yang disebut video cocok dengan event 2026-01-14 dan 2026-04-26 di tabel itu. Tidak ada yang baru.
- **Perlu validasi Claude Code:** Tidak — sudah established & CLOSED.

### [KONFIRMASI] Recent buyer dari underwater → +14% profit dalam hitungan hari
- **Insight:** Rata-rata pembeli baru bergerak dari underwater → break-even → +14% profit dalam beberapa hari `[06:06]`–`[06:16]`. Ini pada dasarnya pembacaan STH-MVRV ≈ 1,14.
- **Indikator terkait:** STH-MVRV
- **Relevan ke:** K2 gate valuasi (band STH-MVRV 0,80–0,97)
- **Test klaim:** Restatement aritmetik dari harga ÷ STH cost basis, bukan klaim empiris — tidak ada yang bisa salah kecuali angkanya. Implikasi framework justru berlawanan dari nada video: STH-MVRV 1,14 berarti **K2 tertutup** (sudah premium, bukan diskon) — konsisten dengan Ω-Score video sendiri yang bilang overheated. Per 2026-07-15 `sth_mvrv` masih 0,9695 (di dalam band), jadi angka 1,14 adalah kondisi pasca-rally yang belum ada di data kita.
- **Perlu validasi Claude Code:** Tidak — definisional. State check tercatat di `findings_sth_profit_flip_trigger.md`.

### [BARU] Anatomi rally dua tahap: mekanis dulu, modal riil menyusul
- **Insight:** Pembicara memisahkan dua fase secara eksplisit: candle vertikalnya jelas liquidation-driven, TAPI "some serious non-derivative real capital has clearly stepped in behind it since" `[05:18]`–`[05:29]`. Cara bacanya bukan biner squeeze-palsu vs rally-asli, melainkan urutan — dorongan mekanis membuka jalan, permintaan spot menahannya.
- **Indikator terkait:** ETF net flow + funding/basis + liquidation (gabungan); proxy di data kita: `realized_cap_usd`
- **Relevan ke:** general / status pasar; menyambung langsung ke temuan 4 Agu (7 dari 8 reclaim STH RP di bear gagal)
- **Test klaim:** Ini klaim paling bernilai dari blok non-on-chain karena bentuknya pembeda, bukan narasi: rally yang bertahan seharusnya diikuti masuknya modal riil, rally squeeze murni tidak. Berbeda dari ETF flow (tidak ada di data kita, dan seri-nya baru sejak Jan 2024 = <1 cycle), proxy realized cap ada full history. Supaya klaim salah: realized cap naik sama saja di rally yang gagal maupun yang bertahan.
- **Perlu validasi Claude Code:** Ya — apakah Δ`realized_cap_usd` at-gate memisahkan reclaim STH RP yang bertahan dari yang gagal?

**[VALIDASI — 2026-08-26, CLOSED]** **TIDAK KONKLUSIF.** Dari 13 event sentuhan STH RP di bear (2011: 1, 2013: 3, 2017: 4, 2021: 3, 2025: 2 censored), cuma **1 yang BERTAHAN** (2023-01-11) — threshold apapun akan overfit ke satu titik. Δ`realized_cap_usd` at-gate **tidak memisahkan sama sekali** (12/12 event GAGAL punya nilai ≥ event BERTAHAN), dan arahnya justru berlawanan: event BERTAHAN punya pertumbuhan realized cap 14/30 hari **paling rendah** dari 13 event; dua bear rally yang gagal keras (2011-12-31, 2014-05-30) justru tertinggi. Verdict: tidak ditolak maupun diterima — **jangan masukkan ke framework**.
Detail: [`findings_realized_cap_growth_reclaim_filter.md`](findings_realized_cap_growth_reclaim_filter.md)

### [BARU] Funding kalem + basis terkompresi + spot memimpin = squeeze berkualitas
- **Insight:** Selama squeeze awal, funding rate tetap "remarkably restrained", futures basis justru terkompresi, dan spot buying memimpin futures `[03:38]`–`[04:02]`. Logikanya: kalau ini cuma degen menumpuk leverage setelah short tersapu, funding dan premium futures seharusnya meledak — tapi tidak. Struktur derivatif dipakai sebagai filter kualitas rally naik.
- **Indikator terkait:** Funding rate, futures basis, spot-vs-futures lead
- **Relevan ke:** K2 / K5 — framework sudah pakai funding <0 sebagai pengubah ukuran tranche K2, tapi belum sebagai filter kualitas rally naik
- **Test klaim:** Bentuknya falsifiable, itu kelebihannya. Tapi hanya 1 dari 3 komponen yang bisa diuji di data kita — futures basis dan spot-vs-futures lead tidak ada kolomnya, dan `funding_rate`/`total_oi` baru mulai 2020 (≈1,5 cycle). Supaya salah: spike besar dengan funding rendah ternyata tidak berbeda outcome-nya dari spike dengan funding tinggi.
- **Perlu validasi Claude Code:** Ya — split spike ≥+7% berdasarkan funding & Δ OI at-gate, bandingkan forward return.

**[VALIDASI — 2026-08-26, CLOSED]** **TIDAK TERKONFIRMASI — arah data justru berlawanan.** Dari **n=39** spike harian ≥+7% sejak 2020-03-31 (20 bull 2020-21, 9 bear 2022, 9 bull 2023-25, 1 bear 2025-26), kombinasi "funding rendah + OI rendah" yang video sebut berkualitas malah median return 30 hari **−7,6%** / drawdown −12,5%, sementara kombinasi "leverage" +11,1% / −3,9%. Korelasi rank funding vs outcome positif lemah (+0,12 s/d +0,29). Tapi **51% sample dari bull 2020-21 saja**, jadi yang terukur kemungkinan besar efek regime, bukan efek funding. **Funding/OI mulai 2020 = ~1,5 siklus — low-confidence permanen.** Verdict: jangan pakai funding sebagai filter kualitas rally; posisi DF v2 sekarang (funding = pengubah ukuran tranche K2, bukan pembuka pintu) tetap yang paling defensible.
Detail: [`findings_funding_filter_spike_quality.md`](findings_funding_filter_spike_quality.md)

### [BARU] Median cost basis tahun berjalan (~$64K) sebagai anchor harga
- **Insight:** BTC terkunci ~6 minggu di $62K–$67K karena median cost basis untuk tahun berjalan ada di ~$64K — harga "literally pinned around this anchor" `[01:41]`–`[02:01]`.
- **Indikator terkait:** Median cost basis YTD (turunan cost basis distribution) — bukan RP / STH RP / LTH RP
- **Relevan ke:** general; konseptual dekat dengan level cost-basis di zone structure, tapi basis perhitungan berbeda (median cohort tahun berjalan, bukan volume-weighted seluruh supply atau <155 hari)
- **Test klaim:** Mekanik anchor-nya masuk akal, tapi klaimnya dibuat dari 1 episode dan metriknya tidak kita punya — data kita hanya rata-rata (`realized_price`, `sth_cost_basis`), bukan median distribusi. Kelemahan struktural: anchor selalu bisa ditemukan post-hoc di dekat harga yang sedang range-bound, karena cost basis memang mengejar harga secara konstruksi.
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog. Pertanyaan: pakai proxy `median(btc_price, trailing 365d)`, `realized_price`, dan `sth_cost_basis` — berapa % hari harga berada dalam ±5% dari masing-masing anchor, dan berapa panjang median episode "pinned" (≥21 hari berturut), per cycle? (Catat eksplisit: median-price ≠ median cost basis — proxy, bukan replikasi.)

### [BARU] Klaster cost basis STH $62K–$67K sebagai penjelas range konsolidasi
- **Insight:** Chart "STH Distribution" (heatmap distribusi cost basis short-term holder) menunjukkan klaster supply padat persis di $62K–$67K, dipakai menjelaskan kenapa range itu jadi zona magnet `[01:45]`–`[02:00]`. Ini pembacaan bentuk distribusi, bukan garis rata-rata.
- **Indikator terkait:** STH Cost Basis Distribution / URPD-style heatmap
- **Relevan ke:** general — framework hanya memakai nilai agregat (STH RP), belum bentuk distribusinya
- **Test klaim:** Heatmap per price-bucket tidak ada di data kita. Klaimnya juga sebagian sirkular: coin yang dibeli selama 6 minggu range memang otomatis punya cost basis di dalam range itu. Level $62K–$67K dibaca dari anotasi frame — low confidence dari resolusi frame.
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog. Proxy age-band: bangun cost basis per band (1w–1m, 1m–3m, 3m–6m) dari `realized_cap_*`/`supply_*`; apakah dispersi antar-band yang menyempit mendahului periode range-bound? (Sebagian sudah disentuh `findings_cohort_6m12m_realized_price.md`, 4 Agu 2026.)

### [BARU] Kompresi volatility ke rekor rendah → ekspansi imminent, arah netral
- **Insight:** Realized volatility terkompresi ke salah satu level terendah dalam sejarah, dan "hanya soal waktu sebelum meledak ke salah satu arah" `[02:01]`–`[02:30]`. Framing umum: BTC bergantian antara fase choppy dan re-rating eksplosif dua arah — kompresi memberi timing, bukan arah.
- **Indikator terkait:** Realized volatility ("Fractals" volatility dashboard)
- **Relevan ke:** general / status pasar
- **Test klaim:** Sebagai kalimat, **hampir tidak bisa difalsifikasi** — "meledak salah satu arah, suatu saat" selalu benar. Yang bisa diuji cuma versi terkuantifikasi. Volatility clustering memang efek statistik mapan, jadi kalaupun terbukti, nilai tambahnya kecil karena tidak memberi arah — paling banter modifier timing, bukan gate. Pembicara sendiri mengakui ini bukan kesimpulan jenius.
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog. Pertanyaan: RV30 masuk persentil ≤10 (rolling 4 tahun), cooldown 60 hari — median |return| 30/60 hari sesudah vs baseline hari acak, dan apakah arahnya benar-benar 50/50 (uji binomial)?

### [BARU] Treasury buyback doubling sebagai pemicu makro rally
- **Insight:** 19 Agustus, Treasury Secretary Bessent umumkan buyback obligasi 10–30 tahun minimal digandakan, ~$2B → ~$4B per operasi `[00:49]`–`[01:39]`. Mekanik yang diklaim: kalau yield tidak dibiarkan mencerminkan risiko fiskal sepenuhnya, tekanannya pindah ke dollar → menghidupkan lagi debasement / financial repression trade → bullish BTC. Pembicara eksplisit menyebut ini bukan QE klasik tapi tetap katalis positif.
- **Indikator terkait:** Tidak ada indikator on-chain — makro/fiskal murni
- **Relevan ke:** general (framework tidak punya input makro sama sekali)
- **Test klaim:** n=1 kejadian, atribusi kausal post-hoc — narasi disusun setelah harga naik, tanpa kontrol untuk skenario "buyback diumumkan tapi harga tidak naik". Rantai mekaniknya punya minimal 3 sambungan yang masing-masing bisa putus, tidak satupun diuji di video. Dan bertabrakan dengan temuan channel yang sama 10 hari sebelumnya (`2026-08-15_bitcoin-news-doesnt-actually-move-the-price`): kategori macro news punya hit rate 38% di hari-0 tapi luruh ke 12% dalam 7 hari, n=8. Supaya klaim salah cukup: harga naik ke $80K tanpa pengumuman ini — yang tidak bisa dibedakan, karena squeeze mekanis + kompresi vol sudah cukup menjelaskan.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (tidak ada kolom DXY, yield, maupun label news event).

### [BARU] Inverse DXY sebagai jembatan makro → BTC & gold
- **Insight:** Chart inverse DXY di-overlay ke harga BTC: dollar melemah → gold dan BTC naik bersamaan, masing-masing +4–5% `[01:21]`–`[01:33]`.
- **Indikator terkait:** DXY (inverted), gold, BTC
- **Relevan ke:** general
- **Test klaim:** Overlay dua garis pada jendela beberapa hari adalah bentuk cherry-pick paling murah — korelasi BTC vs DXY tidak stabil lintas periode dan sering berbalik tanda. Tidak ada uji lead/lag, tidak ada base rate. Angka +4–5% low confidence.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (tidak ada kolom DXY/gold).

### [BARU] Klaster short liquidation di atas range sebagai petunjuk arah break
- **Insight:** Trader berulang kali short di top range, membangun kantong besar level short-liquidation di ~$65K–$67K. Begitu $67K tembus, market "menginjak ranjau" `[02:30]`–`[02:57]`. Peta likuidasi dipakai sebagai petunjuk arah break mana yang lebih mungkin eksplosif.
- **Indikator terkait:** Liquidation heatmap / profile
- **Relevan ke:** general — tidak ada padanan di framework
- **Test klaim:** Liquidation heatmap adalah estimasi vendor, bukan data settle, dan kantong likuidasi selalu ada di kedua sisi range — memilih sisi yang kebetulan kena adalah hindsight. Baru bernilai kalau ditunjukkan bahwa asimetri klaster memprediksi arah break SEBELUM kejadian, dengan n memadai.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (tidak ada data likuidasi; hanya `funding_rate` & `total_oi` sejak 2020).

### [BARU] Rekor short squeeze sebagai penjelas mekanis vertical candle
- **Insight:** ~$3B short crypto terlikuidasi dalam 24 jam vs hanya ~$264 juta long → ~92% likuidasi adalah short `[02:57]`–`[03:38]`. BTC saja >$1B short terlikuidasi dalam satu jam, harga +8% di jendela yang sama. Diklaim short liquidation terbesar dalam sejarah BTC, hanya kalah dari rekor gabungan long+short di crash 10 Oktober.
- **Indikator terkait:** Aggregated liquidation history, long/short liquidation ratio
- **Relevan ke:** general
- **Test klaim:** Klaim "terbesar dalam sejarah" langsung dikoreksi chart-nya sendiri (Okt 2025 lebih besar secara keseluruhan) — jadi "terbesar" hanya setelah difilter jadi shorts-only, kategori yang dipilih setelah melihat hasil. Angka $3B/$264jt/92% dari overlay frame = low confidence, dan angka likuidasi agregat notoriously over/under-reported tergantung exchange API. Nilai forward-looking-nya nol: squeeze menjelaskan candle yang sudah terjadi, bukan yang berikutnya.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (likuidasi & intraday).

### [BARU] ETF net inflow sebagai konfirmasi demand riil
- **Insight:** US spot BTC ETF menyerap ~$2B antara 17–21 Agustus — minggu terkuat sejak Oktober tahun lalu — dan Agustus jadi bulan inflow terkuat sejak puncak bull Oktober, ~$2,7B net inflow MTD `[04:26]`–`[04:53]`.
- **Indikator terkait:** ETF net flow harian/bulanan
- **Relevan ke:** general — tidak ada metrik flow di framework
- **Test klaim:** Arahnya masuk akal (flow non-derivatif ≠ leverage), tapi ETF flow baru ada sejak Jan 2024 — **kurang dari 1 cycle**, jadi bahkan kalau datanya ada, tidak lolos ambang 3-cycle framework. "Minggu terkuat sejak Okt" juga sensitif ke pemilihan jendela (4 hari, bukan minggu kalender). $2,7B MTD dibaca dari label frame = low confidence.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia. Proxy terdekat `apparent_demand` sudah REJECT dua kali (`apparent_demand_hypothesis_findings.md`) — jangan diusulkan ulang.

### [BARU] Rasio pembelian ETF terhadap issuance harian (3,4×)
- **Insight:** Normalisasi flow terhadap supply baru: issuance ~450 BTC/hari; ETF membeli >1.500 BTC/hari rolling bulanan → ~3,4× issuance harian diserap ETF saja `[04:53]`–`[05:15]`.
- **Indikator terkait:** ETF net purchase / daily issuance (rasio turunan)
- **Relevan ke:** general
- **Test klaim:** Rasio ini enak didengar tapi analitis lemah: issuance bukan satu-satunya sumber supply — supply dominan datang dari holder lama yang menjual, besarnya berkali lipat 450 BTC/hari. "3,4× issuance" karena itu bukan ukuran net demand, dan rasio serupa pernah tinggi di periode harga turun. Angka 1.521 BTC/hari low confidence dari frame.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia, dan kelemahan konseptualnya sudah cukup untuk menolak terlepas dari data.

### [BARU] "ETF bukan pembeli terbesar di pasar ini"
- **Insight:** Sisipan satu kalimat `[05:15]`–`[05:18]` — masih ada kohort permintaan lain yang lebih besar dari ETF, tapi tidak disebut siapa dan tidak ditunjukkan datanya.
- **Indikator terkait:** tidak disebut
- **Relevan ke:** general
- **Test klaim:** Klaim telanjang tanpa angka, tanpa nama kohort. Tidak bisa diuji, tidak bisa difalsifikasi. Dicatat hanya karena kalau benar, bobot argumen ETF di atas berubah.
- **Perlu validasi Claude Code:** Tidak — tidak actionable, data juga tidak ada.

### [INDIKATOR CUSTOM] Adaptive Trend Model — flip bullish, level flip ~$68,3K
- **Insight:** Model trend proprietary OCM flip bullish ~6 hari lalu, BTC +15,9% sejak flip; label layar `Bullish · 6d · +15.9%`, `Flip $68,3xx` `[07:05]`–`[07:20]`. Stance: "the overall trend is definitely still bullish until proven otherwise and invalidated".
- **Indikator terkait:** Adaptive Trend Model (custom, price-based)
- **Relevan ke:** general — paralel fungsional dengan gate K1/K3 tapi berbasis price, bukan cost basis
- **Test klaim:** Komponen tidak diungkap → tidak bisa didekomposisi maupun direproduksi. "Bullish until invalidated" tanpa aturan invalidasi eksplisit = tidak falsifiable. Level flip bergeser dari $78K/$67K (video 11 Agu) ke ~$68,3K (video ini) tanpa penjelasan mekanik. Statistik "+15,9% sejak flip" adalah performance sejak titik yang dipilih setelah kejadian, bukan track record. Angka dari label frame = low confidence.
- **Perlu validasi Claude Code:** Tidak — formula tidak diungkap, tidak reproducible. **Flag STOP dari 12 Agu 2026 masih terbuka; jangan tambah bobot sampai diputuskan.**

### [INDIKATOR CUSTOM] Short-Term Ω-Score (Omega Score)
- **Insight:** Komposit buatan channel yang menggabungkan "dozens of major short-term metrics" ke skala 0–100; reading sekarang di high-90s = market sangat panas jangka pendek, sehingga "some kind of mean reversion is due at some point" `[07:20]`–`[07:40]`. Komponen tidak diungkap.
- **Indikator terkait:** Ω-Score short-term (custom composite, black box)
- **Relevan ke:** general — "overheated jangka pendek" tidak punya padanan langsung di framework (K6 dipicu local high, bukan skor panas)
- **Test klaim:** Black box dengan banyak komponen tak diungkap tidak bisa diaudit, dan "high-90s → mean reversion is due" tanpa horizon waktu tidak terfalsifikasi (mean reversion selalu terjadi, cepat atau lambat). Yang menarik: arah kesimpulannya sejalan dengan STH-MVRV 1,14 yang ada di atas band gate K2 — informasinya kemungkinan besar sudah terkandung di metrik yang kita punya. Sekelas dengan "risk indicators" OCM yang sudah tercatat tidak testable.
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog, dan hanya sebagai proxy. Pertanyaan: apakah `sth_mvrv` di persentil ≥95 (rolling 4 tahun) cenderung diikuti pullback ≥5% dari high lokal dalam 14 hari — hit rate, n, sebaran per cycle? Relevan ke timing entry K5, bukan gate.

### [STRATEGI] Menambah posisi di dip pada key cost basis levels
- **Insight:** Untuk yang merasa ketinggalan rally, level yang dia sendiri incar untuk menambah exposure adalah STH Realized Price dan "Bitcoin's true market mean", ditunjukkan lewat chart "Cost Basis Fan" `[07:40]`–`[08:01]`. Entry di level cost basis saat pullback, bukan mengejar harga.
- **Indikator terkait:** STH Realized Price, True Market Mean (padanan framework: AVIV Mean)
- **Relevan ke:** K5 (tunggu pullback ≥5%, deploy di Z2/Z3) dan K2 — sejalan arah, beda mekanisme: framework mensyaratkan gate + veto + cap LTV, video hanya menyebut level
- **Test klaim:** Prinsipnya sejalan dengan K5. Yang perlu diuji: presenter pakai true market mean sedangkan kita pakai AVIV Mean — `true_market_mean_price` ada sebagai kolom terpisah, jadi ini pertanyaan empiris. Risiko: menambah exposure di STH RP saat status bear belum dibuka persis skenario yang menghasilkan drawdown median −24,2% di temuan 4 Agu. Kalau diterjemahkan ke loan, hard limit LTV tetap berlaku penuh — tidak ada di video ini yang menyentuh atau membenarkan pelonggaran LTV.
- **Perlu validasi Claude Code:** Ya — level mana yang paling sering menangkap pullback ≥5% di early bull?

**[VALIDASI — 2026-08-26, CLOSED]** Dari **n=21 pullback ≥5%** di 4 jendela early-bull (6/6/3/6 per cycle, hanya 4 cycle independen), **STH RP menangkap 5/21 dalam ±3% dan 10/21 dalam ±5%** (trough median berhenti +2,4% di atas level, median overshoot ke bawah −4,9%), True Market Mean cuma 1/21, dan **AVIV Mean 0/21** — alasannya struktural: sepanjang early bull AVIV Mean duduk 25–36% **di atas** harga, jadi dia target, bukan lantai dip. Verdict: klaim video **sebagian terkonfirmasi** (STH RP ya, true market mean tidak); memperkuat K5 yang ada, plus tambahan praktis: pasang tranche K5 di STH RP dengan buffer ~5% ke bawah.
Detail: [`findings_pullback_catcher_level_early_bull.md`](findings_pullback_catcher_level_early_bull.md)

### [STRATEGI] Uji regime change di pullback pertama, dengan invalidasi eksplisit
- **Insight:** Pertanyaan yang dianggap penting bukan "bisakah BTC print $85K besok", melainkan apa yang terjadi di pullback layak pertama `[08:01]`–`[08:45]`. Dua cabang dinyatakan di muka: (1) konfirmasi — harga konsolidasi di mid-$70K dengan key cost basis tetap di bawahnya → recent buyer tetap profit → resistance berubah jadi support pertama kali di cycle ini; (2) invalidasi — permintaan ETF & spot mengering, harga tembus balik $68K ke bawah → berarti porsi besar move ini memang cuma short tersqueeze.
- **Indikator terkait:** STH RP / true market mean, ETF net flow
- **Relevan ke:** general / status pasar; bersinggungan langsung dengan flag STOP-1
- **Test klaim:** Bagian terkuat video secara metodologis — presenter menyebut kondisi yang akan membuktikan dirinya salah. Kriteria ini layak dipakai sebagai template falsifikasi, bukan sebagai sinyal. Kelemahannya: "mid-$70K" dan "$68K" adalah threshold absolut untuk cycle ini saja, sementara framework pakai pola relatif — terjemahkan dulu ke bentuk relatif ("harga bertahan di atas STH RP" + "STH RP mulai naik"), bukan ke angka.
- **Perlu validasi Claude Code:** Tidak — substansi ujinya sudah tercakup penuh di validasi flag STOP-1 (`findings_unlock_reachability_struktur_n.md`) dan validasi realized cap.

### [STRATEGI] Causal chain framing, bukan "random crypto pump"
- **Insight:** Metode analisis eksplisit: tiap move besar dipecah jadi rantai sebab-akibat berurutan — katalis makro → breakout teknikal $67K → likuidasi short terbesar → forced buying → akselerasi breakout `[04:02]`–`[04:26]`. Pembicara menekankan ini "makes a lot more sense than just calling this random volatility".
- **Indikator terkait:** gabungan makro + level teknikal + likuidasi + flow
- **Relevan ke:** general (metodologi, bukan sinyal)
- **Test klaim:** Rantai ini disusun setelah hasilnya diketahui; tiap sambungan dipilih karena cocok dengan outcome. Nilai penjelasnya tinggi, nilai prediktifnya nol — dan channel yang sama sudah menunjukkan (video 15 Agu) bahwa atribusi berita ke pergerakan harga umumnya luruh dalam 7 hari.
- **Perlu validasi Claude Code:** Tidak — naratif post-hoc, tidak actionable.

### [STRATEGI] Confluence tiga lensa + stance probabilistik
- **Insight:** Penutup: "I'm not sitting here calling that the bull market is definitely back. But from a macro, technical, and an onchain perspective, this is exactly what the start of one looks like" `[08:45]`–`[08:57]`. Klaim baru dianggap kuat kalau tiga lensa menunjuk arah sama, dan kesimpulan disampaikan probabilistik.
- **Indikator terkait:** —
- **Relevan ke:** general (metodologi)
- **Test klaim:** Bahasa probabilistiknya sehat, tapi tiga lensa itu **tidak independen** di kasus ini — makro, teknikal, dan on-chain semuanya membaca gerakan harga 5 hari yang sama, jadi "confluence"-nya sebagian besar adalah satu bukti dihitung tiga kali. Protokol Governance kita (lapis 2: independensi antar-gate, |phi| < 0,3) ada persis untuk mencegah ini.
- **Perlu validasi Claude Code:** Tidak — framing naratif, tidak ada klaim testable sendiri.

### [KONFLIK] Retest STH RP sebagai "gauge paling penting" regime change
- **Insight:** "Retesting this as support now is one of the most important gauges of whether this is genuinely a new bull market or just the start of another massive leg lower" `[05:53]`–`[06:06]` — level $68.500 dijadikan penentu dominan status bull/bear, diulang di penutup `[08:12]`–`[08:32]`.
- **Konflik dengan:** (a) DF v2 §0 — "Status bear berakhir (unlock): STH RP cross naik melewati RP (masuk Z2)", yaitu flip ordering antar level, bukan posisi harga terhadap STH RP; (b) `Price_Level_knowledge_base v1.4` §6.3/§6.5 — STH RP diberi **weight RENDAH sebagai standalone trigger** (60 episode false signal, high frequency & noise), §5.2 mencatat STH RP bisa sticky di level tinggi saat low-volume drift.
- **Alasan konflik:** Framework sengaja memindahkan definisi akhir-bear dari price-vs-level ke struktur ordering justru karena price-vs-STH-RP terlalu berisik. Validasi kita sendiri 4 Agu 2026: Signal D (close > STH RP ≥3 hari) hanya 1 dari 8 kali mendahului unlock (12%), 7 dari 8 balik ke bawah dalam 90 hari. Klaim video menaikkan sinyal yang sama itu jadi gauge primer.
- **Rekomendasi:** **Diskusikan lebih lanjut dengan Yudi** — bukan penolakan otomatis. Bukan karena gauge video-nya benar (bukti kita bilang lemah), tapi karena validasi STOP-1 menunjukkan framework kita sendiri tidak punya jalur unlock yang bisa bunyi di struktur N. Video menyodorkan gauge yang salah untuk pertanyaan yang memang belum terjawab.

**[VALIDASI — 2026-08-26, CLOSED]** Gap terkonfirmasi dan lebih tajam dari dugaan: bear 2025-26 adalah **bear siklus penuh pertama dalam 16 tahun** dengan **0 hari struktur T** (min STH RP/RP = **1,272**, vs 0,842–0,924 di empat bear sebelumnya), jadi unlock formal DF v2 **mekanis tidak bisa bunyi** dan K5 tidak bisa start. Koreksi atas dugaan awal: bear 2017 **pernah** T (59 hari, Jan–Mar 2019); yang 0 hari T adalah **window mid-cycle 2019-06 s/d 2020-05** (kembar kasus K4-tanpa-Z1). Ketiga kandidat pengganti gagal — hit rate 25–29% (n=7/4/7 di bear window), varian (iii) identik dengan (i), dan keunggulan (i) atas unlock formal (20–29 hari lebih cepat) cuma berdiri di **n=2**. Verdict: **jangan ganti definisi unlock; usulkan jalur darurat sejenis K4-tanpa-Z1 untuk sisi K5**.
Detail: [`findings_unlock_reachability_struktur_n.md`](findings_unlock_reachability_struktur_n.md)

---

## Flag Prioritas

1. **Unlock tidak reachable di struktur N (STOP-1)** — bear 2025-26 adalah bear siklus penuh pertama dalam 16 tahun tanpa satu hari pun struktur T. Selama definisi unlock DF v2 tidak diberi jalur alternatif, K5 mati di cycle ini apapun yang terjadi pada harga. Ini keputusan struktural, bukan tuning.
2. **Flip STH profit di struktur N historisnya 0/5** — temuan lintas-validasi paling penting: flip <10%→>80% memang median +99,5% dalam 365 hari, tapi yang memisahkan hit dari false positive bukan magnitude flip-nya melainkan struktur at-gate (T: 4/4 unlock, N: 0/5). Per 2026-07-15 kita di N. Jadi narasi paling persuasif di video belum punya dukungan struktural di data kita.
3. **Adaptive Trend Model flip bullish, flag STOP 12 Agu masih terbuka (STOP-2)** — sekarang sistem price-based itu bilang bullish sementara K-node bilang tunggu. Konflik operasionalnya jadi konkret, bukan hipotetis lagi.
4. **STH RP sebagai lantai pullback K5** — validasi P4 memberi tambahan praktis yang langsung bisa dipakai: 10/21 pullback early-bull berhenti dalam ±5% dari STH RP, median overshoot −4,9%; AVIV Mean 0/21 karena posisinya 25–36% di atas harga sepanjang early bull. Tranche K5 di STH RP dengan buffer ~5% ke bawah layak dipertimbangkan.
5. **Caveat data 6 minggu** — data master berhenti 2026-07-15 sementara video membahas 19–25 Agustus. Semua verdict di atas adalah uji pola historis, bukan pembacaan kondisi sekarang. Update data sebelum keputusan apapun diambil berdasarkan analisis ini.

---

## Yang Langsung Diabaikan

- **Prediksi "$85.000 besok"** `[08:05]` — dipakai pembicara sendiri sebagai contoh pertanyaan yang tidak penting, bukan klaim.
- **Klaim hindsight "an exceptionally well-timed call"** soal panggilan volatility minggu sebelumnya `[02:10]`–`[02:18]` — swa-penilaian, bukan mekanik; substansinya sudah masuk insight kompresi volatility.
- **Rasio ETF vs issuance (3,4×)** — sudah masuk inventory, tapi diabaikan untuk keperluan framework: issuance bukan sumber supply dominan, jadi rasio ini bukan ukuran net demand.
- **"ETF bukan pembeli terbesar"** — tidak bisa diuji, tidak bisa difalsifikasi, tidak menyebut kohort maupun angka.
