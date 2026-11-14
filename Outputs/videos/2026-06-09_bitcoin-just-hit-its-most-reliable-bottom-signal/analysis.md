# Bitcoin Just Hit Its Most Reliable Bottom Signal
**Channel:** On-Chain Mind
**Tanggal video:** 2026-06-09
**Tanggal analisis:** 2026-07-19
**Link:** https://www.youtube.com/watch?v=mlp_W8oTD-c

---

## Ringkasan

Video ini berargumen bahwa Bitcoin (saat rekaman ~$62k) sedang berada di salah satu level on-chain paling penting dalam sejarahnya: titik di mana supply in profit dan supply in loss tepat 50/50. Pembicara mengklaim split 50/50 ini "telah menandai dasar setiap major bear market sejak 2010" dan menjadikannya sebagai sinyal bottom paling reliabel — sekaligus dasar untuk membantah prediksi harga $20k–$30k sebagai "mathematically unsound".

Argumennya dibangun bertingkat lewat beberapa chart On-Chain Mind: (1) Total Supply in Profit/Loss di 50/50 dengan framing kelangkaan (bottom 7% of all readings); (2) LTH Supply in Loss ~41% yang disebut tinggi untuk maturity sekarang, dengan klaim ambang bottom menurun tiap cycle; (3) "Cash extracted" (realized profit) rolling 30-hari yang kolaps ~10x dari puncak cycle; (4) URPD / density view yang menunjukkan wall of support di low-$60k dan supply tipis di $45–55k; dan (5) "break level" — simulasi berapa % supply akan in loss di harga hipotetis (di $50k → 57% loss, di $43k → 60% loss), yang keduanya lebih buruk dari apapun dalam sejarah. Kesimpulan pembicara: pasar "weak" tapi belum "broken", capitulation kemungkinan berbasis waktu ("pain by boredom") bukan harga, dan bottoming process kemungkinan butuh lebih banyak waktu.

Lima klaim inti diuji lawan data historis (`data_master_all_metrics.csv`, n=4 cycle bottom). Hasilnya sebagian besar **tidak mendukung framing video**: klaim ambang LTH-loss menurun per cycle REJECTED (justru flat ~45%), 50/50 sebagai sinyal standalone REJECTED (coin-flip, precision 50% — tapi valid sebagai komponen komposit K4), collapse realized-profit REJECTED sebagai timing signal (non-spesifik, high false-positive), dan velocity supply-in-loss REJECTED kuat (lebih sering awal crash, bukan floor). Satu klaim CONFIRMED: >70% supply-in-loss memang belum pernah terjadi (ceiling historis ~63.8%). Nilai video bagi framework terutama sebagai **konfirmasi tidak langsung**: metrik intinya sudah tertanam di K4, dan hasil validasi memperkuat desain komposit framework ketimbang menawarkan sinyal standalone baru.

---

## Insight Inventory

### [KONFIRMASI] 50/50 Supply in Profit/Loss sebagai capitulation floor
- **Insight:** Saat tepat setengah supply in profit dan setengah in loss (50/50), itu disebut menandai dasar setiap major bear market sejak 2010 — dibingkai sebagai "most reliable bottom signal" yang berdiri sendiri `[00:03]`–`[01:41]`, diulang `[13:43]`.
- **Indikator terkait:** Supply in Profit/Loss (total)
- **Relevan ke:** K4 kondisi #3 (Supply in Profit <50% DAN STH profit <10%); zone ZC/Z1
- **Test klaim:** Framework sudah pakai ambang <50% ini, tapi sebagai 1 dari 4 kondisi komposit K4, bukan sinyal tunggal "most reliable". Titik lemah: sebagai standalone, supply-in-profit bisa menyentuh ~50% di koreksi tengah-bull / crash likuiditas yang bukan true bottom. Sample "setiap major bear sejak 2010" = ~4 cycle → kecil. Ambang 50% adalah threshold absolut (kebetulan sudah dipakai framework).
- **Perlu validasi Claude Code:** Ya — depth per cycle + true/false positive rate standalone.

**[VALIDASI — 2026-07-19, CLOSED]** Framing "most reliable standalone" REJECTED; penggunaan `<50%` sebagai kondisi komposit K4 JUSTIFIED. Di tiap cycle low supply-in-profit turun di bawah 50% (ke ~39–45%, bukan berhenti di 50/50), jadi valid sebagai kondisi necessary. Tapi sebagai sinyal standalone, crossing <50% cuma coin-flip (4 TP / 4 FP, precision 50%, n=8 crossing / 4 cycle) — sering menyala di tengah bear (2014-09) atau crash likuiditas (2020-03 COVID) yang bukan the-low. Detail: [`findings_supply_in_profit_5050.md`](findings_supply_in_profit_5050.md)

### [KONFIRMASI] Threshold LTH-supply-in-loss turun tiap cycle (relative, bukan absolut)
- **Insight:** Ambang LTH supply in loss yang menandai true bottom disebut menurun tiap cycle: 2015 >50%, 2019 ~45%, 2022 ~40%; sekarang ~41% dinilai "tinggi untuk stage maturity ini". Secara mekanis makin sulit mendorong seluruh cohort LTH ke loss saat harga naik antar tahun `[05:35]`–`[06:53]`, diulang `[14:08]`.
- **Indikator terkait:** LTH Supply in Loss (`pct_lth_in_loss`)
- **Relevan ke:** K4 (LTH metrics); prinsip inti framework "threshold absolut tidak reliable antar cycle, pakai pola relatif"
- **Test klaim:** Hanya 3–4 titik data (satu per cycle) = sample sangat kecil, tren menurun bisa noise. Angka spesifik (>50/45/40) dibaca dari chart video → perlu verifikasi ke data. Mirror pola "diminishing MVRV peaks" yang sudah [KONFIRMASI] di index. Salah bila angka historis tidak reproduce atau tidak monotonic.
- **Perlu validasi Claude Code:** Ya — MAX `pct_lth_in_loss` ±60d tiap cycle bottom, apakah menurun.

**[VALIDASI — 2026-07-19, CLOSED]** REJECTED: klaim ambang LTH-supply-in-loss menurun tiap cycle tidak terdukung. MAX `pct_lth_in_loss` dalam ±60d tiga cycle terakhir justru flat ~44–46% (2015: 45.1% < 2018: 45.9% > 2022: 44.6%), selisih di bawah noise; 2011 hanya 32% (kemungkinan artefak kohort awal). Angka video "2015 >50%" tidak cocok dengan `pct_lth_in_loss` (kemungkinan definisi metrik LTH berbeda). n=4 cycle. Nilai bottom yang stabil ~45% justru konsisten dengan prinsip pola-relatif framework, bukan drift menurun seperti klaim video. Detail: [`findings_lth_loss_threshold_per_cycle.md`](findings_lth_loss_threshold_per_cycle.md)

### [BARU] Rarity/percentile framing: 50% split = bottom 7% of all readings
- **Insight:** BTC menghabiskan ~93% harinya dengan >50% supply in profit; turun di bawah 50% berarti masuk 7% terbawah dari seluruh reading historis — jadi kondisi langka, bukan hari biasa `[01:15]`–`[02:35]`.
- **Indikator terkait:** Supply in Profit/Loss (total), distribusi/percentile
- **Relevan ke:** general / K4 (kontekstualisasi seberapa ekstrem kondisi)
- **Test klaim:** Deskriptif, mudah dicek. Angka 93/7 sensitif terhadap rentang tanggal (BTC bias ke profit karena lebih banyak waktu di bull/recovery). Bukan threshold keputusan, cuma konteks kelangkaan.
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog (low-priority; verifikasi % hari `percent_btc_in_profit` <50% ≈ 7%).

### [BARU] Velocity supply-in-loss sebagai sinyal dekat-capitulation
- **Insight:** Supply in loss melonjak ~16 poin dari ~34% (sebulan lalu) ke >50% hari ini; ekspansi cepat unrealized pain ini disebut menandakan pasar sangat dekat capitulation floor `[03:21]`–`[03:40]`, diulang `[13:59]`.
- **Indikator terkait:** Supply in Loss (total), rate-of-change 30 hari
- **Relevan ke:** K4 / ZC — reading kecepatan, bukan level
- **Test klaim:** Lonjakan cepat supply-in-loss juga terjadi di AWAL setiap crash tajam (Mar 2020, Mei 2021) yang belum tentu bottom — velocity tinggi bisa berarti "baru mulai jatuh". Threshold ~16 poin belum tentu robust. Salah bila banyak episode +16 poin/30 hari diikuti penurunan lanjutan besar.
- **Perlu validasi Claude Code:** Ya — ROC 30-hari `percent_btc_in_loss`, forward drawdown + kedekatan ke cycle low.

**[VALIDASI — 2026-07-19, CLOSED]** REJECTED kuat: klaim "lonjakan cepat supply-in-loss (~+16 poin/30 hari) = dekat capitulation floor" tidak terdukung. Dari 43 episode ROC30 ≥+15 poin (2011=7 / 2015=10 / 2018=14 / 2022+=12), cuma 2 yang dekat cycle low (±60d, keduanya di 2018); mayoritas justru diikuti downside lanjutan (median forward drawdown −13% s/d −17%, terburuk −75%). Ekspansi cepat supply-in-loss cenderung menandai AWAL crash, bukan dekat-dasar. n=43 episode. Detail: [`findings_velocity_supply_loss.md`](findings_velocity_supply_loss.md)

### [BARU] Same-price / different-LTH-loss karena graduation cohort
- **Insight:** Di harga low-60s Februari hanya ~27% LTH supply in loss; di harga yang sama sekarang >40% underwater. Sebabnya: banyak koin yang dibeli di puncak cycle lalu baru menyeberang 155 hari dan "graduate" ke status LTH, menyeret angka loss LTH naik meski harga sama `[04:52]`–`[05:23]`.
- **Indikator terkait:** LTH Supply in Loss; cohort aging (155 hari)
- **Relevan ke:** general — mekanik komposisi cohort LTH; path-dependence
- **Test klaim:** Penjelasan mekanik yang masuk akal secara struktural (sesuai definisi LTH 155-hari), tapi sulit diisolasi bersih tanpa data cohort per-tanggal-akuisisi. Data kita punya `pct_lth_in_loss` dan HODL waves, bukan graduation flow eksplisit — verifikasi hanya bisa korelasional, bukan kausal. Marginal ke K-node aktif (lebih penjelasan "kenapa angka begini").
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog (data cohort-by-acquisition tidak tersedia; verifikasi penuh tidak mungkin).

### [INDIKATOR CUSTOM] "Cash extracted" (realized profit) — slope flattening sebagai bottom signal
- **Insight:** "Cash extracted" = total cash ditarik dari ekosistem BTC (~$1T realized profit kumulatif). Yang penting bukan angkanya tapi slope-nya yang mendatar tajam; pada basis rolling 30-hari turun dari ~$55B (peak cycle) ke ~$3B sekarang (~10x lebih kecil). Collapse profit-taking ini disebut textbook bottom-forming `[07:05]`–`[08:04]`, diulang `[14:16]`.
- **Indikator terkait:** Realized Profit (kumulatif & rolling 30-day) — famili SOPR/realized value
- **Relevan ke:** K4 / bottom detection
- **Dekomposisi:** Realized Profit (cumulative sum) + turunan rolling 30-hari. Bukan indikator eksotis — kombinasi realized value yang sudah ada di keluarga SOPR/Realized Price.
- **Test klaim:** Rolling-30d realized profit kolaps di SETIAP fase harga jatuh (tidak ada yang jual untung saat merah) — "slope flat" bisa muncul di banyak koreksi, bukan eksklusif bottom. Data caveat: tidak ada realized profit gross USD, perlu proksi.
- **Perlu validasi Claude Code:** Ya — rolling-30d realized profit, false-positive rate + lead/lag ke cycle low.

**[VALIDASI — 2026-07-19, CLOSED]** REJECTED sebagai sinyal timing standalone (proksi `daily_realized_profit_btc × btc_price`, bukan gross realized profit Glassnode). Rolling-30d memang kolaps ke <2% dari peak di tiap cycle low (necessary-ish), tapi kolaps ≤10%-of-peak juga muncul di 8 episode lain yang semuanya BUKAN dekat bottom (0/8 TP) — non-spesifik, high false-positive. Trough juga cenderung telat 40–90 hari setelah price low (kecuali 2011). Berguna sebagai confirming context, bukan trigger. n=4 cycle bottom + 8 FP episode. Detail: [`findings_rp30d_collapse.md`](findings_rp30d_collapse.md)

### [INDIKATOR CUSTOM] "Break level" — simulasi supply in profit/loss di harga hipotetis
- **Insight:** "Break level" mensimulasikan berapa persen supply akan in profit/loss di harga hipotetis manapun (karena harga last-moved tiap koin diketahui). Sekarang 50/50. Model bilang: di $50k → 43% profit (57% loss); di $43k → 40% profit (60% loss). Kedua skenario lebih buruk dari apapun dalam sejarah BTC `[11:53]`–`[13:02]`. (Angka on-screen ~$62,730 / 49.2% in profit — low confidence dari resolusi frame.)
- **Indikator terkait:** URPD terintegrasi (supply-in-profit sebagai fungsi harga hipotetis)
- **Relevan ke:** K4 / ZC — stress-test seberapa dalam downside secara mekanis
- **Dekomposisi:** Cumulative distribution function dari URPD (supply-in-profit di harga X = fraksi koin dengan cost-basis < X). Turunan langsung URPD, bukan indikator terpisah.
- **Test klaim:** Konsep valid, tapi implementasi butuh full cost-basis distribution / URPD yang TIDAK ada di data kita. Angka spesifik low confidence dari frame.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (NEEDS-DATA: butuh URPD/cost-basis distribution). Bagian testable ("70% underwater belum pernah terjadi") diuji terpisah di [STRATEGI] bantahan $20k/$30k.

### [BARU] URPD sebagai peta support/resistance berbasis supply density
- **Insight:** URPD memetakan tiap koin di harga terakhir ia bergerak, menunjukkan berapa koin berpindah tangan di tiap level. Cluster besar = support/resistance. Saat ini support kuat ~$60–62k (ratusan ribu BTC, mayoritas holding 1–5 tahun); supply $45–55k sangat tipis, jadi jika $60k jebol harga bisa "scoop" cepat ke support besar berikutnya di low-$40k (~$43k) `[08:15]`–`[11:45]`, diulang `[14:26]`.
- **Indikator terkait:** URPD (Glassnode standard), holder-age overlay, density view
- **Relevan ke:** general — level support/resistance struktural
- **Test klaim:** URPD indikator standar Glassnode tapi tidak ada di daftar indikator aktif framework maupun data kita (kita punya HODL waves age-based, bukan distribusi per level harga). Level harga spesifik dibaca dari frame → low confidence, jangan jadi anchor. Cluster supply bisa bergeser (koin bergerak) → S/R tidak statis.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (URPD price-distribution tidak ada di dataset). Level spesifik hanya bisa dikonfirmasi forward.

### [BARU] Mekanik psikologis URPD (break-even seller vs refuse-to-sell)
- **Insight:** URPD bekerja sebagai S/R karena psikologi: bila harga mendekati cluster besar dari atas, holder di dekat break-even termotivasi jual untuk balik modal → resistance; bila mendekati dari bawah, holder menolak jual rugi bahkan menambah → support. Makin besar cluster, makin kuat efeknya `[10:26]`–`[11:16]`.
- **Indikator terkait:** URPD, cost-basis clustering
- **Relevan ke:** general — dasar mekanik kenapa cluster cost-basis jadi level
- **Test klaim:** Selaras logika Realized Price / cost-basis sebagai level yang sudah ada di framework (STH RP/RP/LTH RP), tapi diterapkan pada distribusi penuh, bukan satu garis rata-rata. Murni naratif, tidak menghasilkan sinyal actionable baru, dan tidak testable langsung.
- **Perlu validasi Claude Code:** Tidak — naratif/mekanik, tidak actionable, data URPD tidak tersedia.

### [STRATEGI] Bantahan target $20k/$30k sebagai "mathematically unsound"
- **Insight:** Seruan BTC ke $30k atau $20k dinilai keliru secara matematis: gerakan itu akan mendorong >3,5 juta BTC lagi ke loss, artinya >70% network underwater — level yang belum pernah terjadi ("off the scale"). Downside masih mungkin dan kelemahan nyata, tapi angka serendah itu tidak plausible menurut statistik `[13:02]`–`[13:41]`.
- **Indikator terkait:** Break level / Supply in Profit/Loss
- **Relevan ke:** general — argumen menolak prediksi harga rendah via mekanik on-chain
- **Test klaim:** Bagian testable tanpa URPD: apakah `percent_btc_in_loss` pernah ≥70%. Titik lemah argumen: "belum pernah terjadi" ≠ "tidak mungkin terjadi" — supply distribution tiap cycle beda; klaim 3,5jt BTC butuh URPD (tidak ada).
- **Perlu validasi Claude Code:** Ya (quick check) — historical max `percent_btc_in_loss`.

**[VALIDASI — 2026-07-19, CLOSED]** CONFIRMED (sebagian): >70% network underwater memang belum pernah terjadi — ceiling historis `percent_btc_in_loss` hanya ~63.8% (2015-08-24), dan cuma 12 hari yang pernah ≥60% (klaster Aug-2015 & Feb-2019). Reading mendekati/di atas 70% akan "off the scale" secara historis. Komponen URPD (3,5jt BTC di $20-30k) tidak bisa diuji — data URPD tidak tersedia. n=seluruh histori harian sejak 2010. Detail: [`findings_max_supply_in_loss.md`](findings_max_supply_in_loss.md)

### [STRATEGI] Time-based capitulation ("pain by boredom") + weak vs broken
- **Insight:** Pembicara mengharapkan capitulation berbasis waktu untuk sisa tahun ini ("pain by boredom") ketimbang murni berbasis harga jatuh; pasar cenderung chop di sekitar level 50% bukan bounce bersih. Bedakan pasar "weak" (sekarang) dari "broken"; struktur on-chain saat ini tipe yang secara historis terbentuk dekat major bear low — zona proses bottoming, belum tentu bottom persis hari ini `[03:43]`–`[04:01]`, `[06:45]`–`[06:56]`, `[13:41]`–`[15:36]`.
- **Indikator terkait:** Supply in Profit/Loss (total & LTH), realized profit
- **Relevan ke:** ZC/Z1, K4 — karakter proses bottoming
- **Test klaim:** Sudah established di framework sebagai K4 jalur/lantai waktu (≥9 bulan sejak cycle peak DAN close < RP → DCA), yang sudah tervalidasi 3/3 bear. "Weak vs broken" dan "chop di 50%" = pengamatan kualitatif, tidak actionable sebagai sinyal diskrit.
- **Perlu validasi Claude Code:** Tidak — sudah established (K4 lantai waktu) + sisanya naratif kualitatif.

---

## Flag Prioritas

1. **Konfirmasi tidak langsung ke K4, bukan sinyal baru** — Metrik inti video (Supply in Profit <50%) sudah tertanam di K4 kondisi #3. Validasi menunjukkan sebagai standalone hanya coin-flip (precision 50%), justru **memperkuat keputusan framework** memperlakukannya sebagai komponen komposit, bukan trigger tunggal. Ini poin paling penting: video tidak menawarkan sinyal actionable baru, tapi mengonfirmasi desain yang sudah ada.
2. **Tension framing "most reliable standalone" vs komposit** — Video menjual 50/50 sebagai sinyal bottom paling reliabel yang berdiri sendiri. Data menolak framing itu. Worth dicatat karena channel besar cenderung meng-over-sell single-metric narratives; framework kita sudah lebih konservatif di sini.
3. **Klaim LTH-loss menurun per cycle REJECTED** — Ini yang paling "menjual" di video (mendukung narasi "bottom near"), tapi `pct_lth_in_loss` justru flat ~45% tiga cycle terakhir, tidak menurun. Kalau angka video benar untuk metrik LTH versi lain, ada gap definisi yang perlu diklarifikasi sebelum dipercaya.
4. **Velocity supply-in-loss REJECTED kuat** — Lonjakan cepat supply-in-loss lebih sering menandai awal crash (forward drawdown −13% s/d −17%) daripada floor. Berguna sebagai reminder untuk tidak memperlakukan "pain cepat = dekat dasar".
5. **"Break level" / URPD menarik secara konsep tapi butuh data yang belum ada** — CDF dari cost-basis distribution adalah tool yang legit untuk stress-test downside. Kalau suatu saat data URPD/cost-basis-distribution masuk ke dashboard, "supply-in-profit sebagai fungsi harga" bisa jadi tambahan bernilai untuk K4/ZC. Backlog data, bukan backlog validasi.

---

## Yang Langsung Diabaikan

- **Promosi onchain.mind.io + 7-day free trial** `[08:04]`–`[08:15]` — sponsor/promosi, tidak relevan framework.
- **Musik penutup** `[15:42]`–`[15:48]`.
- **Mekanik psikologis URPD** — benar dan selaras logika cost-basis framework, tapi murni naratif, tidak menghasilkan sinyal/keputusan baru (dibiarkan di inventory sebagai konteks, bukan actionable).
