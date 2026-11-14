# Bitcoin News Doesn't Actually Move The Price
**Channel:** Look Into Bitcoin (Formerly Bitcoin Magazine Pro)
**Tanggal video:** 2026-08-15
**Tanggal analisis:** 2026-08-20
**Link:** https://www.youtube.com/watch?v=w2j9rnkDnc4

---

## Ringkasan

Video 13:33 yang keluar dari pola biasa channel ini: bukan bedah indikator on-chain, tapi riset empiris soal apakah berita benar-benar menggerakkan harga BTC. Pemicunya rentetan headline bearish di dua minggu pertama Agustus 2026 — wallet hack $116jt, Strategy jual $105jt, Clarity Act ditunda lagi, chain split, MARA akui jual >$1,6 miliar BTC, Riot pivot $9,1 miliar ke AI data center, dan Trezor data breach di hari syuting — sementara harga justru naik dan volatility tidak bergerak.

Presenter mengumpulkan 184 event berita besar dari Timeline of Bitcoin dan History of Bitcoin (Wikipedia) plus riset sendiri, mengklasifikasikannya ke 6 kategori, lalu menjalankan uji yang sama pada BTC, S&P 500, dan gold (sejak 1972). Empat temuan utamanya: (1) hari berita punya distribusi return dengan pusat identik tapi ekor lebih gemuk — berita menaikkan varians, bukan arah; (2) pengaruh volatility-nya luruh dalam ~2 minggu di ketiga aset; (3) shock justru sedikit *memperpanjang* trend BTC (36% flip 30-hari vs 46% hari acak), sementara di S&P/gold murni coin flip; (4) melewatkan 15 hari shock terbesar 10 tahun terakhir menurunkan CAGR dari 66,8% ke 33,2%. Kesimpulannya: fundamental analysis berbasis berita bukan metode pengambilan keputusan yang reliable, dan menghindari volatility mahal sekali.

Untuk framework kita nilainya bukan di penambahan indikator — video ini nol indikator on-chain. Nilainya di tiga tempat: konfirmasi negatif atas keputusan framework untuk tidak memakai input berita sama sekali, angka-angka soal perilaku shock yang menyentuh kalibrasi buffer LTV, dan satu tensi retoris dengan K1/K3 yang perlu dipisahkan baik-baik. Empat klaim price-only-nya bisa direplikasi dengan data kita dan sudah divalidasi di bawah — hasilnya campuran: dua bertahan sebagian, dua tidak.

---

## Insight Inventory

### [BARU] Shock cenderung memperpanjang trend, bukan membalikkannya
- **Insight:** Diukur dengan probabilitas 30-day trend flip, setelah shock day BTC hanya 36% flip vs 46% di hari acak — shock justru menurunkan peluang perubahan trend. S&P 500 (51% vs 49%) dan gold (49% vs 51%) murni coin flip, jadi ini efek khas BTC. Penjelasan presenter: berita bearish datang bersama price action bearish, jadi memperkuat arah yang sudah jalan `[06:38]`–`[07:14]`. *Angka low confidence dari resolusi frame.*
- **Indikator terkait:** tidak ada indikator on-chain — realized volatility & arah trend 30 hari
- **Relevan ke:** K2 (jangan gugurkan episode dip karena satu hari shock), alarm bear CEPAT § 0, K3
- **Test klaim:** Titik lemah utamanya definisi — "30-day trend flip" tidak dijelaskan cara ukurnya, dan kalau trend diukur dari trailing return yang mengikutsertakan hari shock, hasilnya bias mekanis ke continuation. Shock day juga bukan sample independen: menurut klaim video sendiri shock datang berkelompok, jadi n=348 jauh dari 348 observasi bebas. Yang menaikkan kredibilitasnya: kontrol lintas-aset — kalau ini murni artefak metode, seharusnya muncul juga di S&P/gold.
- **Perlu validasi Claude Code:** Ya — flip rate pasca-shock lawan matched baseline (hari non-shock dengan tanda trend at-gate sama), distratifikasi arah shock & cycle.

**[VALIDASI — 2026-08-20, CLOSED]** Angka video tereplikasi hampir persis (36,0% vs baseline matched 47,5%, selisih −11,6pp; n=139 shock ≥2013, sebaran per cycle 61/43/32/34 full-history, tanpa dominasi era) dan bertahan terhadap dua uji yang paling mungkin membunuhnya — koreksi at-gate hanya menggeser 0,7pp, dan event-merging (n=106) justru menguatkan ke −13,5pp. Tapi efeknya **runtuh di definisi shock kedua** (ambang fixed 8% → selisih −0,5pp) dan **hampir seluruhnya berasal dari UP-shock** (−17,2pp) bukan DOWN-shock (−5,3pp); sel yang paling actionable — shock turun saat trend masih naik, n=27 — selisihnya praktis nol (−1,8pp). Verdict: tereplikasi tapi cenderung tidak layak jadi input keputusan.
Detail: [`findings_shock_trend_continuation.md`](findings_shock_trend_continuation.md)

### [BARU] Shock datang berkelompok, bukan acak
- **Insight:** Share of shocks yang diikuti shock lain dalam 5 hari, actual vs jika acak: BTC 47% vs 29%, S&P 500 43% vs 26%, gold 41% vs 26% `[07:26]`–`[08:07]`. Mekanisme yang diberikan presenter untuk Agustus 2026: treasury company jual → miner kehilangan percaya diri & pivot → offloading besar lain → orang cari exploit hardware wallet. *Angka low confidence dari resolusi frame.*
- **Indikator terkait:** realized volatility
- **Relevan ke:** K2 (spacing tranche ~2 minggu / tiap −7%), staged cut LTV
- **Test klaim:** Arahnya hampir pasti benar — volatility clustering adalah salah satu regularitas paling robust di semua kelas aset (dasar seluruh keluarga model GARCH), dan kemunculannya di tiga aset persis yang diharapkan dari fenomena struktural. Yang perlu hati-hati baseline "if random"-nya: kalau dihitung dari unconditional shock rate tanpa mengontrol komposisi era, sebagian gap bisa mekanis. Penjelasan naratif presenter (rantai treasury → miner → exploit) adalah storytelling post-hoc dan sebaiknya diabaikan.
- **Perlu validasi Claude Code:** Ya — P(shock lagi dalam 5/10 hari | shock) vs dua baseline (unconditional + block-shuffle yang mempertahankan jumlah shock per tahun).

**[VALIDASI — 2026-08-20, CLOSED]** Cenderung didukung secara arah tapi magnitudonya kira-kira setengah dari yang ditampilkan video: lift +12,9pp terhadap baseline shuffle (≥2013, h=5, n=139 shock; sebaran cycle 61/43/32/34), menyusut ke **+4,5pp** setelah hari langsung-berturutan dibuang — jadi sebagian besar "clustering" adalah fenomena 1-2 hari, bukan gelombang seminggu. Selisih besar antara baseline naif dan baseline shuffle (19,6% vs 36,5% di varian 8%) menunjukkan angka video cenderung melebih-lebihkan efeknya karena baseline yang tidak mengontrol komposisi era.
Detail: [`findings_shock_clustering_decay.md`](findings_shock_clustering_decay.md)

### [BARU] Volatility pasca-shock luruh dalam ~10-20 hari trading, seragam lintas aset
- **Insight:** Chart "After a big move, how long does the disturbance last?" — S&P 500 (n=812 shocks), gold (n=824), BTC (n=348): spike ke ~6× normal daily move di hari 0, turun ke ~1,2-1,5× dalam ~10 hari trading, praktis flat di 1× setelah ~20 hari `[06:06]`–`[06:33]`. Untuk news event spesifik (n=184) garis kembali masuk pita random di sekitar hari +10 s/d +15 `[03:10]`–`[03:50]`. *Angka low confidence dari resolusi frame.*
- **Indikator terkait:** realized volatility
- **Relevan ke:** general + buffer LTV (horizon stres berapa lama)
- **Test klaim:** Ini pengukuran ulang stylized fact (mean reversion realized volatility), dan konsistensi lintas tiga aset dengan n besar membuatnya kredibel secara arah. Yang perlu diuji bukan "apakah benar" tapi "berapa angkanya untuk BTC di data kita", karena horizon peluruhan itulah yang menentukan berapa lama posisi ber-leverage ada di zona berbahaya. Angka "~6× di hari 0" jangan dipakai sebagai anchor — sebagian tautologis karena hari-0 dipilih justru karena besar.
- **Perlu validasi Claude Code:** Ya — mean `|log return|` t+1..t+30 dinormalisasi ke vol 90 hari at-gate; di hari ke berapa turun di bawah 1,2×?

**[VALIDASI — 2026-08-20, CLOSED]** Cenderung TIDAK didukung dalam bentuk yang bersih. Kurva mean naik-turun sepanjang 30 hari (k=3: 1,24× → k=5: 1,90× → k=10: 1,24× → k=14: 1,68×) dan baru turun permanen di bawah 1,2× di **k=26**; versi smooth-5 tidak pernah (n=139 shock ≥2013; sebaran cycle 61/43/32/34). Median memang pulih cepat (k=2), jadi bacaan yang jujur: *tipikal* hari setelah shock cepat tenang, tapi ekornya panjang. Untuk manajemen risiko yang relevan mean — **horizon stres yang layak diasumsikan ~3-4 minggu, bukan 2 minggu.** Perbedaan peluruhan antar zona tidak bisa dijawab (n=15 di grup ZC/Z1/Z1b).
Detail: [`findings_shock_clustering_decay.md`](findings_shock_clustering_decay.md)

### [BARU] Shock terbesar terkonsentrasi saat harga sedang jatuh
- **Insight:** Dari 15 largest single-day shocks per aset (BTC ~2012-2026, S&P & gold 1970-2026), mayoritas ke sisi downside dan terjadi saat harga sedang plummeting; "most markets grind to the upside and it's very rare you get a huge shock to the upside" `[08:54]`–`[09:41]`. BTC punya pengecualian occasional god candle ke atas, terutama di era awal.
- **Indikator terkait:** realized volatility
- **Relevan ke:** ZC / Z1 (fase capitulation), K4, hard limits LTV
- **Test klaim:** Secara arah hampir tautologis untuk aset apapun dengan drift positif dan volatility clustering. Kelemahan versi presenter: "15 largest" adalah sample yang dipilih ex-post dan sangat kecil; untuk BTC sebagian besarnya kemungkinan dari era 2013-2015 yang likuiditasnya tidak sebanding, dan presenter sendiri mengakui distorsi era awal `[09:55]`. Nilai sebenarnya bukan klaim naratifnya tapi versi terkuantifikasi per zona — kalau shock besar memang menumpuk di ZC/Z1, itu berarti risiko gap terbesar muncul justru saat framework paling agresif membeli.
- **Perlu validasi Claude Code:** Ya — distribusi shock per zona v2 dinyatakan sebagai shock per 100 hari zona (bukan jumlah mentah), plus down:up per zona, plus persentil 95 drawdown 3-hari di zona tempat loan aktif.

**[VALIDASI — 2026-08-20, CLOSED]** Versi "frekuensi" cenderung TIDAK didukung: setelah dinormalisasi ke panjang zona, kepadatan shock praktis **datar** — 2,60 (ZC/Z1/Z1b) vs 2,76 (ZD/Z3) vs 2,78 (Z4/Z5) per 100 hari (n=139 shock ≥2013; sebaran cycle 61/43/32/34, pra-2013 hanya 18,2% dari total). Yang cenderung DIDUKUNG kuat adalah versi arahnya: rasio down:up bergerak dari **7,0 di ZC** (88% down) ke **0,21 di Z5** (18% down), konsisten di kedua definisi shock. Jadi zona tidak memprediksi *seberapa sering* shock datang, tapi sangat memprediksi *ke arah mana*.
Detail: [`findings_shock_distribution_by_zone.md`](findings_shock_distribution_by_zone.md)

### [BARU] Distribusi hari berita: pusat sama, ekor lebih gemuk
- **Insight:** Histogram daily move dalam multiples of normal volatility: news days (n=184) punya pusat distribusi hampir identik dengan all other days (n=5.899); yang beda hanya ekornya, lebih gemuk di luar ±2σ `[04:04]`–`[04:44]`. Artinya berita tidak menggeser expected return, hanya menaikkan probabilitas outlier dua arah. *Angka low confidence dari resolusi frame.*
- **Indikator terkait:** realized volatility distribution
- **Relevan ke:** general + hard limits LTV (risiko tail, bukan risiko arah)
- **Test klaim:** Ini efektifnya restatement dari stylized fact standar dan konsisten dengan bentuk lemah efisiensi pasar — bukan temuan baru, dan tidak actionable sebagai sinyal karena ekor gemuknya dua arah. Implikasi praktisnya (buffer LTV harus tahan tail move yang tidak terprediksi) sudah ter-hardcode di framework lewat statistik "92 kejadian harga turun ≥13% dalam ≤3 hari". Perlu dicatat: dengan n=184 lawan n=5.899, pergeseran pusat yang kecil memang tidak akan terdeteksi — ini bukti absence, bukan absence of effect.
- **Perlu validasi Claude Code:** Tidak — butuh label news day yang tidak tersedia di sisi kita, dan implikasi praktisnya sudah established di framework.

### [BARU] Protocol news satu-satunya kategori dengan dampak bertahan >7 hari
- **Insight:** Outlier hit rate per kategori (baseline normal day 7%), "on the day" → "next 7 days": Hostile (n=31) 15%→13%; Regulation (n=20) 20%→~5%; Adoption (n=61) 11%→8%; **Protocol (n=20) 10%→20% — satu-satunya yang naik**; Enforcement (n=17) 12%→~6%; Macro (n=8) 38%→12% `[04:44]`–`[05:33]`. *Angka low confidence dari resolusi frame.*
- **Indikator terkait:** tidak ada — klasifikasi kategori buatan presenter
- **Relevan ke:** general
- **Test klaim:** Ini klaim terlemah di seluruh video. n=20 dengan hit rate 20% = 4 kejadian; di bawah baseline 7%, peluang dapat ≥4 dari 20 secara kebetulan sekitar 9% — sudah marginal *sebelum* dikoreksi multiple comparison, dan di sini ada 6 kategori × 2 horizon = 12 perbandingan, jadi menemukan satu yang "naik" adalah ekspektasi murni statistik. Tambahan: label kategori subjektif, dan protocol event (halving, upgrade besar) terkonsentrasi di fase siklus tertentu — confound siklus tidak dikontrol. Klaim ini gugur begitu satu-dua event direklasifikasi.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (label kategori + threshold "abnormal" tidak diungkap), dan ditolak atas dasar sample size + multiple comparison terlepas dari ketersediaan data.

### [BARU] Macro news = hit volatility tertinggi di hari-0, luruh paling cepat
- **Insight:** Macro punya outlier hit rate tertinggi di hari kejadian (38%, ~5× baseline 7%) tapi jatuh ke 12% setelah 7 hari — "macro has a huge volatile influence in the immediate future, it's pretty much gone a week later" `[05:33]`–`[05:42]`. *Angka low confidence dari resolusi frame.*
- **Indikator terkait:** —
- **Relevan ke:** general; menyentuh operasional K2/K5 (jangan menunda/mempercepat tranche karena event macro)
- **Test klaim:** n=8. Angka 38% berarti 3 dari 8 kejadian; ganti satu event saja dan hit rate melompat ke 25% atau 50%. Tidak ada dasar memperlakukan ini sebagai temuan, apalagi input keputusan. Arah kesimpulannya kebetulan sejalan dengan intuisi umum, tapi kesesuaian dengan intuisi bukan bukti.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia, dan n=8 jauh di bawah ambang minimum framework.

### [KONFIRMASI] News/fundamental analysis bukan basis keputusan yang reliable
- **Insight:** Kesimpulan utama video: mengandalkan analisis berita (macro, announcement, protocol upgrade, security, regulatory) sebagai sumber edge "doesn't really seem like a reliable method of decision making, not just in Bitcoin, but throughout traditional markets as well"; memprediksi trend change dari news event "practically impossible... no more accurate than a coin flip" `[08:15]`–`[08:31]`, `[10:52]`–`[11:33]`.
- **Indikator terkait:** — (justru ketiadaan indikator)
- **Relevan ke:** general — mengkonfirmasi desain framework yang sepenuhnya on-chain dan sengaja tidak memasukkan input berita di K1-K6 maupun alarm bear § 0
- **Test klaim:** Konfirmasi negatif atas sesuatu yang framework memang tidak pakai — nilainya menutup pintu, bukan membuka. Batas logisnya perlu dicatat: video membuktikan bahwa *memprediksi arah dari berita* tidak reliable, BUKAN bahwa berita tidak punya efek — klaim ekor gemuk di atas justru menunjukkan efek nyata di varians. Bacaan yang benar: berita tidak masuk sebagai input sinyal, tapi tetap relevan sebagai input manajemen risiko / timing eksekusi.
- **Perlu validasi Claude Code:** Tidak — sudah established sebagai desain framework.

### [KONFIRMASI] Berita hanya bikin volatility jangka pendek, arah tidak ikut
- **Insight:** Studi lama Look Into Bitcoin (video 5 September 2023): hari acak → 53% peluang harga lebih tinggi 10 hari kemudian; hari berita → 56% `[01:46]`–`[02:12]`. Presenter menyebutnya "basically noise, it's random". Studi baru (n=184, 15+ tahun) mengulang kesimpulan yang sama. *Angka dari frame video lama, low confidence.*
- **Indikator terkait:** —
- **Relevan ke:** general — mendukung prinsip bahwa sinyal keputusan harus berasal dari struktur cost-basis/valuasi, bukan katalis
- **Test klaim:** Selisih 53% vs 56% dengan n=184 sama sekali tidak signifikan — standard error proporsi di n=184 sekitar 3,7pp, jadi selisih 3pp praktis nol. Presenter sendiri menyimpulkan "basically noise", jadi tidak ada over-claiming. Yang perlu dicatat: konsistensi hasil 2023 vs 2026 bukan replikasi independen — datasetnya bertumpang tindih hampir seluruhnya, jangan dihitung sebagai dua bukti.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (butuh label news day), dan kesimpulannya sudah selaras dengan desain framework.

### [KONFIRMASI] Menghindari volatility sangat mahal — hold melewati drawdown menang
- **Insight:** BTC 10 tahun terakhir (dari 2015): melewatkan 15 shock day terbesar dengan "step aside 5 hari" → CAGR 33,2% vs buy & hold 66,8%, tertinggal 33,6 pp `[09:46]`–`[10:52]`. Kurva growth-of-$1 menunjukkan semua varian step aside (5 hari / 10 hari / 1 bulan) di bawah stay invested untuk ketiga aset, gap paling ekstrem di BTC. Alasannya: "reacting to shocks means sitting out the recovery as often as the fall". *Angka low confidence dari resolusi frame.*
- **Indikator terkait:** —
- **Relevan ke:** K4 jalur lantai waktu (DCA jalan terus walau count <2), K4 jalur utama (deploy justru di drawdown), rasional framework yang tidak pernah exit 100% BTC
- **Test klaim:** Ini varian dari studi "missing the best days" yang punya masalah metodologis terkenal, tapi versi presenter sedikit lebih adil karena aturannya reaktif (keluar SETELAH shock), bukan omniscient. Yang tersisa: (1) hanya 15 hari terbesar dipilih ex-post — implementasi nyata tidak tahu mana yang top-15; (2) start date 2015 sangat menguntungkan buy & hold (dekat dasar pasca-2014), CAGR 66,8% sensitif terhadap tanggal mulai; (3) karena shock berkelompok, "step aside 5 hari" hampir dijamin melewatkan rebound — jadi sebagian hasilnya konsekuensi mekanis, bukan temuan independen.
- **Perlu validasi Claude Code:** Ya — replikasi step-aside versi realistis tanpa hindsight, plus varian yang hanya aktif di kondisi tertentu (Z5 / window K1, alarm bear).

**[VALIDASI — 2026-08-20, CLOSED]** Arah klaim tereplikasi untuk metode yang video pakai — hindsight top-15 kalah di 7 dari 8 skenario (mulai 2015, N=5: −10,2pp; N=10: −19,3pp), walau jauh dari −33,6pp yang disebut video. **Tapi versi realistisnya justru menang:** step-aside yang dipicu down-shock secara mekanis mengalahkan buy & hold di **8 dari 8 skenario**, median +11,7pp (n=66 trigger ≥2013; per cycle 28/21/17/14). Mekanisme sebenarnya bukan "menghindari volatility itu mahal" tapi "menghindari volatility ke ATAS itu mahal" — begitu shock naik ikut memicu keluar (ANY-shock), keunggulannya hilang (−0,9pp s/d −9,1pp). **Bukan strategi yang layak diadopsi:** hasilnya didominasi C1 (+140,5pp dari 2 tahun era 2013-14) dan berbalik total di C2 (−36,0pp).
Detail: [`findings_step_aside_zone_conditional.md`](findings_step_aside_zone_conditional.md)

### [KONFIRMASI] Anekdot Agustus 2026: rentetan berita bearish, harga tetap naik
- **Insight:** Dua minggu pertama Agustus 2026 memuat wallet hack $116jt, Strategy jual $105jt, Clarity Act ditunda lagi, chain split, MARA akui jual >$1,6 miliar BTC, Riot pivot $9,1 miliar ke AI data center, dan Trezor data breach — semua bearish, tapi harga naik dan tidak terlihat kenaikan volatility di chart Bitcoin Volatility (5Y) `[00:03]`–`[01:29]`.
- **Indikator terkait:** realized volatility
- **Relevan ke:** general (ilustratif, bukan bukti)
- **Test klaim:** n=1 episode, dipilih justru karena menarik — ini hook pembuka, bukan bukti, dan presenter memakainya lalu langsung pindah ke data. Perlakukan sebagai konteks naratif.
- **Perlu validasi Claude Code:** Tidak — n=1, murni naratif.

### [KONFIRMASI] Bias seleksi diakui sendiri oleh presenter
- **Insight:** Dataset berita berasal dari Timeline of Bitcoin (Wikipedia, hanya sampai 2021), History of Bitcoin (sampai 2024), sisanya riset sendiri; presenter mengakui hanya "notable news stories" yang bertahan di record, jadi ada survivorship/selection bias. Kompensasinya: ditambahkan sejumlah highly volatile day terlepas ada/tidaknya berita `[02:29]`–`[02:46]`, `[05:50]`–`[06:25]`.
- **Indikator terkait:** —
- **Relevan ke:** general — sejalan dengan STANDAR VALIDASI framework (definisi event eksplisit, laporkan n, jujur soal keterbatasan data)
- **Test klaim:** Kejujuran metodologis ini alasan menaikkan bobot video ini di atas konten sejenis, tapi pengakuan bias tidak menghapus biasnya. Arah bias-nya spesifik: dataset berisi berita yang *diingat sejarah*, dan berita diingat sejarah antara lain karena harganya bergerak besar — jadi sampel condong ke event berdampak, yang seharusnya membuat efek terlihat LEBIH besar dari sebenarnya. Karena hasilnya tetap "tidak ada efek arah", bias ini justru memperkuat kesimpulan nol.
- **Perlu validasi Claude Code:** Tidak — catatan metodologis, bukan klaim testable.

### [KONFLIK] "Sitting out volatility = underperform" vs K1 (jual 20-30%) dan K3 (short 30%)
- **Insight:** Video menyimpulkan secara umum bahwa keluar dari pasar untuk menghindari volatility — bahkan hanya 5 hari — menghasilkan underperformance besar (BTC: −33,6 pp CAGR), dan bahwa "it is very difficult to time the market... and outperform Bitcoin" `[10:52]`, `[11:54]`.
- **Konflik dengan:** K1 (lunasi loan + jual 20-30% BTC saat trigger puncak siklus) dan K3 (buka short 30% saat alarm PRESISI Stage 2) — dua-duanya bentuk market timing dengan periode keluar/hedge yang bisa berbulan-bulan.
- **Alasan konflik:** Tensinya ada di level kesimpulan, bukan mekanisme. Video menguji timing yang dipicu **news/shock day** (reaktif, event-driven, horizon 5-30 hari, exit 100%); framework melakukan timing yang dipicu **struktur valuasi on-chain** (MVRV/aSOPR diminishing per ATH, posisi vs AVIV Upper, gap STH-SOPR), horizon bulanan, dan hanya parsial (20-30%, tidak pernah exit total). Video tidak menguji exit berbasis valuasi sama sekali — jadi belum tentu membantah K1/K3, tapi kesimpulan lisannya digeneralisasi ke "market timing" secara umum.
- **Rekomendasi:** Diskusikan lebih lanjut dengan Yudi.

**[VALIDASI — 2026-08-20, CLOSED]** Konflik tidak selesai jadi kemenangan salah satu pihak, tapi jadi pemisahan yang lebih tajam. Varian step-aside yang paling dekat dengan K1 (hanya aktif di Z5 / window K1) **kalah — median −2,9pp, menang cuma 2 dari 8 skenario, n=22 trigger.** Jadi validasi ini **tidak memberi dukungan empiris untuk K1 sebagai alat menaikkan CAGR** — tapi batas ujinya penting: yang diuji adalah exit 100% selama 5-10 hari, sementara K1 adalah jual parsial 20-30% horizon bulanan yang tujuan utamanya melunasi loan. Ini bukan uji K1; dia hanya menutup satu jalur pembenaran yang mungkin dikira ada. Varian alarm bear **inconclusive** karena replikasi alarmnya gagal (kondisi ON di 63-94% hari — kemungkinan ada komponen aturan v2 yang tidak berhasil diterjemahkan ke kode, perlu dicek di Onchain-Dashboard).
Detail: [`findings_step_aside_zone_conditional.md`](findings_step_aside_zone_conditional.md)

### [INDIKATOR CUSTOM] Klasifikasi 6-kategori news event + "outlier hit rate"
- **Insight:** Presenter membangun taksonomi berita sendiri (Hostile, Regulation, Adoption, Protocol, Enforcement, Macro) dan metrik "outlier hit rate" = persentase hari yang menghasilkan abnormal move, dibandingkan baseline normal day 7%, diukur di dua horizon (on the day vs next 7 days) `[04:44]`–`[05:33]`.
- **Indikator terkait:** realized volatility (untuk normalisasi), bukan metrik on-chain
- **Relevan ke:** general
- **Test klaim:** Dekomposisinya: (1) label kategori manual & subjektif, tanpa aturan pelabelan yang diungkap; (2) daily return dinormalisasi ke "normal volatility" — window normalisasi tidak disebut, dan kalau memakai volatility full-sample itu lookahead bias; (3) threshold "abnormal move" tidak diungkap angkanya sama sekali, padahal seluruh hasil per-kategori bergantung penuh padanya. Tidak reproducible, dan tidak punya komponen on-chain apapun — tidak bisa didekomposisi ke indikator framework. Baseline "normal day 7%" satu-satunya angka jangkar, dan itu konsisten dengan threshold sekitar ±1,8-2σ, tapi ini tebakan.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia DAN definisi metrik tidak diungkap sehingga tidak reproducible bahkan kalau datanya ada.

### [INDIKATOR CUSTOM] "Bitcoin Volatility" chart Look Into Bitcoin
- **Insight:** Chart proprietari Look Into Bitcoin: harga BTC + band volatility di horizon 1 minggu / 2 minggu / 1 bulan / 3 bulan / 6 bulan / 1 tahun, dipakai untuk menunjukkan volatility tetap rendah sepanjang rentetan berita Agustus 2026 `[00:54]`, `[00:51]`–`[01:13]`.
- **Indikator terkait:** realized volatility
- **Relevan ke:** general (framework saat ini tidak memakai realized volatility sebagai input di K-node manapun)
- **Test klaim:** Dekomposisi lengkap dan sederhana: realized volatility rolling multi-window (7/14/30/90/180/365 hari) dari harga close, tanpa komponen on-chain sama sekali. Bisa direkonstruksi 100% dari `btc_price` di data kita kapan saja. Tapi di video ini dipakai murni sebagai visual pendukung anekdot — tidak ada klaim prediktif yang menyertainya, jadi tidak ada yang bisa diuji.
- **Perlu validasi Claude Code:** Tidak — tidak ada klaim testable yang melekat; sepenuhnya derivable dari data yang sudah ada kalau nanti dibutuhkan sebagai konteks.

### [STRATEGI] Buy & hold melewati shock sebagai default; disiplin > reaksi
- **Insight:** Posisi eksplisit presenter: karena trend change pasca-news tidak bisa diprediksi (coin flip) dan menghindari volatility mahal, pendekatan default adalah tetap invested dan menahan drawdown — "trying to avoid that volatility, even just for 5 days at a time, is going to result in you massively underperforming just holding on, even through those drawdowns" `[11:54]`–`[12:16]`.
- **Indikator terkait:** —
- **Relevan ke:** K4 (lantai waktu & DCA di drawdown), rasional exit parsial di K1
- **Test klaim:** Sebagai prinsip ini sudah tertanam di framework (tidak pernah exit 100%, K4 lantai waktu jalan terus melewati drawdown, K6 pakai cash bukan jual BTC). Yang membedakan framework dari "pure hold" bukan penolakan terhadap hold, tapi penambahan aturan valuasi di ekstrem — dan video tidak menguji itu. Sebagai strategi standalone dia juga mengabaikan seluruh dimensi leverage, yang justru pusat risiko di framework kita.
- **Perlu validasi Claude Code:** Tidak — sudah established; irisan testable-nya sudah masuk validasi step-aside di atas.

### [STRATEGI] Roadmap "protocol backed 100% by data" + maturation thesis
- **Insight:** Look Into Bitcoin menyatakan sedang membangun metodologi investasi yang sepenuhnya berbasis data & bukti faktual, dirancang untuk horizon dekade, dan risetnya akan mencakup commodity & equity markets karena "ultimately that's where Bitcoin is likely to trend to, trading more like these indexes or precious metals" `[12:16]`–`[12:51]`.
- **Indikator terkait:** — (pernyataan arah riset)
- **Relevan ke:** general. Bersinggungan dengan entri lama di `source_index.md`: "Narasi institutional demand → volatility turun" ([STRATEGI], On-Chain Mind 2025-01-22) — dua sumber berbeda sama-sama memprediksi BTC makin berperilaku seperti aset makro tradisional, lewat argumen berbeda.
- **Test klaim:** Bagian roadmap tidak punya konten yang bisa diuji — belum ada metodologi yang dipublikasikan, jadi ini pengumuman, bukan klaim. Yang punya isi adalah maturation thesis-nya, dan itu implisit meramalkan volatility BTC meluruh lintas siklus. Waktu muncul dari On-Chain Mind, ini di-mark tidak actionable; sekarang ada alasan menaikkannya: kalau magnitudo shock harian/3-harian benar-benar mengecil per cycle, asumsi di balik tangga staged cut LTV (basis 92 kejadian ≥13%/3 hari) perlu dicek apakah masih mewakili era sekarang atau didominasi era lama. Klaim ini salah kalau persentil 95 drawdown 3-hari per cycle datar atau naik.
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog. Pertanyaannya: realized vol 365 hari + persentil 95 drawdown 3-hari per cycle, apakah menurun monoton? Dan dari 92 kejadian "turun ≥13% dalam ≤3 hari", berapa sebarannya per cycle?

> *Catatan dari validasi lain yang menyentuh ini:* dua sinyal awal sudah muncul walau bukan dari uji yang dirancang untuk pertanyaan ini. Pertama, hari dengan drawdown 3-hari ≤ −22,4% di window K2 tersebar **C1 n=14 · C2 n=2 · C3 n=4 · C4 n=0** ([`findings_shock_distribution_by_zone.md`](findings_shock_distribution_by_zone.md)). Kedua, hari turun ≥10% tersebar **C1 n=15 · C2 n=18 · C3 n=15 · C4 n=1** ([`findings_shock_clustering_decay.md`](findings_shock_clustering_decay.md)). Arahnya konsisten dengan maturation thesis, tapi n per cycle terlalu kecil untuk kesimpulan — dan ini **bukan** alasan melonggarkan tangga staged cut.

### [STRATEGI] Metodologi lintas-aset sebagai kontrol (BTC vs S&P 500 vs gold)
- **Insight:** Sebagai pendekatan riset, presenter selalu menjalankan uji yang sama pada tiga aset (BTC, S&P 500, gold sejak 1972 pasca-Bretton Woods) untuk memisahkan mana yang khas BTC dan mana yang perilaku pasar umum `[04:11]`, `[05:42]`, `[08:54]`–`[09:04]`.
- **Indikator terkait:** —
- **Relevan ke:** general — metodologi yang bisa dipinjam untuk protokol validasi framework
- **Test klaim:** Ini kekuatan metodologis terbesar video dan layak diadopsi sebagai prinsip, bukan sebagai temuan. Efek langsungnya di video ini: menaikkan kredibilitas klaim trend-continuation (satu-satunya hasil yang menyimpang dari kontrol) dan menurunkan kebaruan clustering/decay (identik di tiga aset = stylized fact, bukan temuan BTC). Kita tidak bisa mereplikasi karena tidak punya data S&P/gold.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia.

---

## Flag Prioritas

1. **Tangga staged cut LTV bisa dilompati — dan itu terkuantifikasi sekarang.** Begitu rung-1 (58%) tersentuh, ~66-70% kejadian juga menembus 60% dalam window 3-hari yang sama, ~1 dari 3 sampai 65%. Cap 48% masuk zona itu ~2× lebih sering dari cap 45% (44 hari vs 20 hari). Ini pembenaran kuantitatif langsung untuk aturan "order dipasang di muka", dan argumen konkret memilih cap 45% ketimbang 48%.
2. **Setelah satu hari −10%, ~1 dari 5 kejadian (cap 45%) atau ~1 dari 4 (cap 48%) mendorong LTV menembus 58% dalam 10 hari.** Angka paling actionable dari seluruh batch ini. Basisnya n=49 episode, tapi **hanya 1 di cycle berjalan** — baca sebagai batas atas historis.
3. **Horizon stres pasca-shock lebih panjang dari kesan video: ~3-4 minggu, bukan 2 minggu** (mean baru turun di bawah 1,2× di k=26, n=139). Kalau ada asumsi internal soal berapa lama posisi ber-leverage "aman kembali" setelah hari buruk, angkanya perlu digeser.
4. **Konflik X-1 dan batasnya.** Kesimpulan "menghindari volatility itu mahal" tidak boleh dipakai melunakkan tangga staged cut 58-65% — tangga itu mekanisme solvensi, bukan strategi return, dan video tidak menguji leverage sama sekali. Perlu diputuskan: apakah framework perlu catatan eksplisit bahwa exit hanya dipicu struktur valuasi, tidak pernah oleh berita/shock day?
5. **Arah shock sangat zona-dependent, frekuensinya tidak** (down:up 7,0 di ZC vs 0,21 di Z5, sementara kepadatan datar 2,60-2,78 per 100 hari). Artinya: tidak ada alasan menahan DCA K4 karena "zona bawah rawan shock" — yang berbeda cuma arahnya, dan itu memang yang diharapkan saat membeli di bawah.
6. **Replikasi alarm bear CEPAT gagal (ON di 63-94% hari).** Kemungkinan besar kesalahan penerjemahan aturan v2 ke kode, bukan masalah framework — tapi perlu dicek di Onchain-Dashboard, karena kalau ternyata alarm memang senyala itu, artinya berbeda.
7. **Maturation thesis naik dari "tidak actionable" jadi layak diuji** (backlog). Dua sinyal awal sudah muncul: hari −10% tersebar 15/18/15/**1** per cycle, dan drawdown 3-hari ekstrem 14/2/4/**0**. Kalau benar mengecil, kalibrasi 92-kejadian di balik tangga staged cut perlu dibahas ulang — dibahas, bukan dilonggarkan.

---

## Yang Langsung Diabaikan

- **Klaim per-kategori berita (Protocol 10%→20%, Macro 38%→12%)** — n=8 s/d n=61 dengan 12 perbandingan sekaligus; menemukan satu kategori yang "naik" adalah ekspektasi statistik murni, bukan temuan. Ditolak terlepas dari ketersediaan data.
- **Metrik "outlier hit rate"** — threshold "abnormal" tidak pernah diungkap angkanya, jadi tidak reproducible bahkan seandainya daftar event-nya ada.
- **Rantai kausal Agustus 2026** (treasury jual → miner pivot → offloading → exploit hardware wallet) — storytelling post-hoc; mekanisme sebenarnya volatility persistence + deleveraging, bukan rantai berita.
- **Reassurance soal Trezor breach** `[02:12]`–`[02:29]` — opini tanpa mekanik.
- **Sindiran ke Saylor soal "volatility is vitality"** `[08:31]`–`[08:49]` — retorika; sisi substantifnya disebut sambil lalu tanpa data.
- **Selisih 53% vs 56% dari studi 2023** — dengan n=184, standard error ~3,7pp; selisih 3pp praktis nol. Presenter sendiri menyebutnya noise.
