# Mathematically Modelling The Future Of Bitcoin
**Channel:** Bitcoin Magazine Pro
**Tanggal video:** 2026-07-13
**Tanggal analisis:** 2026-07-29
**Link:** https://www.youtube.com/watch?v=eAo6ORyAq-w

> **Flag filosofis (bukan STOP, tapi worth didiskusikan):** Metodologi inti video ini — memfit garis log-linear ke puncak/lembah MVRV historis lalu mengekstrapolasi ke tanggal & harga presisi jauh ke masa depan (2028, 2029, 2045, bahkan 100 tahun) — secara pendekatan berlawanan dengan prinsip utama framework kita ("bereaksi terhadap sinyal relatif saat ini, bukan memprediksi harga/tanggal absolut"). Ini bukan hard-LTV conflict, dan pembicara sendiri eksplisit mengakui "no model works perfectly forward, better to react than predict" — jadi model prediktifnya dibingkai sebagai ilustrasi/hiburan bear-market, bukan pengganti mesin keputusan zone-based+K-node. Tidak perlu revisi framework, tapi baik untuk didiskusikan sebagai contoh kenapa kita sengaja tidak pakai pendekatan curve-fitting forward-looking semacam ini.

---

## Ringkasan

Video 14:46 menit dari Bitcoin Magazine Pro yang memperkenalkan model proyeksi harga BTC jangka panjang berbasis MVRV Ratio. Intinya: fit garis log-linear ke puncak/lembah MVRV historis, lalu hitung compounded annual growth rate (CAGR) Realized Price untuk mengekstrapolasi band ceiling/floor ke masa depan. Karena proyeksi garis lurus akan saling silang pada horizon sangat jauh (floor jadi lebih tinggi dari ceiling — masalah matematis), pembicara memperkenalkan "exponential amplitude decay model" yang memaksa ceiling & floor konvergen menuju Realized Price seiring waktu. Model ini dipakai untuk memproyeksikan harga di halving 2028 ($274K peak/$98K floor), tanggal puncak siklus berikutnya (12 September 2029, berdasarkan asumsi siklus 47-bulan top-to-top), sampai ilustrasi ekstrem 100 tahun ke depan dan tahun 2045 (dibandingkan target Michael Saylor $21 juta/BTC). Bagian kedua video membahas "quantile bands" — versi probabilistik dari model yang sama (persentil ke-5/ke-95), diklaim akurat "practically to perfection" termasuk saat diuji out-of-sample (training data dibatasi ke 2015/2019/2023), dan dipakai untuk menyimpulkan BTC saat ini berada di "unbelievable discount territory". Video ditutup dengan referensi ke paper pembicara sendiri soal dynamic long-term holder classification (Realized Price dihitung across berbagai age-band, bukan satu cutoff tetap), lalu segmen promosi Bitcoin Magazine Pro.

---

## Insight Inventory

### [BARU] Dynamic LTH classification — Realized Price across multiple age boundary families
- **Insight:** Dari paper referensi pembicara sendiri ("Dynamic Long-Term Holder Classification for Bitcoin"), Realized Price dihitung across berbagai age boundary families (0-30d, 30-90d, ..., 730d+) alih-alih satu cutoff usia tetap 155 hari yang dipakai framework kita untuk split STH/LTH.
- **Indikator terkait:** STH/LTH classification & Realized Price family (STH RP, LTH RP)
- **Relevan ke:** seluruh zone structure (STH RP & LTH RP = level pembatas ZD/Z1b/Z2/dst) — insight yang paling menyentuh backbone definisi framework
- **Test klaim:** Klaim bahwa continuum age-band "lebih akurat" dari cutoff tetap 155 hari itu argumen akademis yang masuk akal, tapi belum menunjukkan bukti bahwa itu menghasilkan sinyal zona yang material berbeda. 155 hari sendiri bukan angka sembarangan — konvensi industri yang mendekati titik perilaku holder historis berubah, bukan threshold harga absolut yang framework kita larang.
- **Perlu validasi Claude Code:** Ya

**[VALIDASI — 2026-07-29, CLOSED]** Menggeser cutoff STH/LTH dari 155 hari ke 90-180 hari menggeser tanggal crossing STH RP↔RP sekitar 10-22 hari (median, n=9 tanggal dari **4 episode regime independen**: 2011-12, 2015, 2019, 2022-23) — sample kecil, indikasi arah bukan bukti kuat. Cutoff 270 hari (proxy interpolasi kasar, bukan boundary data asli) berperilaku kualitatif berbeda — 6 dari 9 event bahkan tidak terdeteksi dalam window ±180 hari. Kesimpulan: granularitas cutoff 90-180 hari kemungkinan **low-impact** untuk zone structure kita yang beroperasi di skala bulan-tahun — tidak ada alasan kuat untuk mengubah 155-hari fixed cutoff. Detail: [`findings_dynamic_lth_boundary.md`](findings_dynamic_lth_boundary.md)

### [INDIKATOR CUSTOM] Log-linear best-fit trend line pada peak/trough MVRV
- **Insight:** Garis best-fit statistik (log-linear regression) menghubungkan puncak dan lembah historis MVRV Ratio, direplikasi sebagai custom indicator TradingView "BTC MVRV Projection", untuk mengekstrapolasi ke mana puncak/lembah MVRV berikutnya kemungkinan berada. [00:15]–[00:48]
- **Indikator terkait:** MVRV Ratio (turunan — trend line fitted ke peak/trough historis)
- **Relevan ke:** general (menyentuh filosofi K1 peak-reading & K4 bottom-reading)
- **Test klaim:** Basisnya cuma 4-5 titik puncak/lembah siklus historis — di bawah standar minimal framework sendiri (3-4 cycle = sample kecil). Tidak ada mekanisme kausal kenapa MVRV harus mengikuti garis regresi tertentu, dan band bisa direfit tiap ada data baru (moving target, sulit difalsifikasi).
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog (walk-forward test: fit pada n-1 peak/trough, cek residual predicted vs actual peak berikutnya, mengecil atau membesar antar cycle)

### [INDIKATOR CUSTOM] Training data window dipilih berdasar "best fit" subjektif (2012-2016 halving)
- **Insight:** Beberapa window training data diuji (2012/2016/2020 halving), lalu dipilih window "antara 2012-2016 halving" karena dianggap paling akurat fit-nya. [01:52]–[02:24]
- **Indikator terkait:** sama seperti trend line MVRV/RP CAGR di atas
- **Relevan ke:** general — catatan metodologis penting
- **Test klaim:** Ini persis pelanggaran STANDAR VALIDASI kita sendiri (aturan #6): "kalau coba >3-4 varian dan cuma satu berhasil, itu overfitting." Memilih window training karena "paling akurat secara subjektif" adalah overfitting-by-construction — masalah struktural, bukan sesuatu yang bisa "diperbaiki" dengan tes data historis lagi.
- **Perlu validasi Claude Code:** Tidak — sudah established sebagai red flag metodologis di framework kita sendiri.

### [INDIKATOR CUSTOM] Exponential amplitude decay model — ceiling/floor MVRV band konvergen ke Realized Price
- **Insight:** Solusi pembicara untuk masalah garis lurus proyeksi ceiling/floor yang akan saling silang jauh ke depan: model decay eksponensial yang memaksa kedua garis konvergen menuju Realized Price seiring waktu, supaya tidak pernah bersilangan. Ini basis metodologi seluruh proyeksi berikutnya di video. [03:43]–[05:22]
- **Indikator terkait:** MVRV Ratio band custom (mode "Amplitude decay" vs "Original" di indikator TradingView-nya)
- **Relevan ke:** general — mempengaruhi baca Z5 (ceiling)/Z1 (floor) far-forward
- **Test klaim:** Bentuk fungsi eksponensial & rate decay dipilih arbitrer (tidak dijelaskan kenapa eksponensial vs power-law), kemungkinan besar juga di-fit post-hoc mirip masalah training window di atas. Bukan indikator independen — murni curve-fitting di atas MVRV yang sudah ada, dengan falsifiability lemah karena decay rate bisa direfit tiap cycle.
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog (prioritas rendah; cek premis dasar: apakah amplitude MVRV peak memang menurun monoton across cycle 2013→2025)

### [INDIKATOR CUSTOM] Proyeksi harga halving 2028, tanggal presisi 12 Sept 2029, dan ultra-long-horizon (2045/100 tahun)
- **Insight:** Rangkaian angka spesifik dari model amplitude decay: halving 2028 → peak ~$274K/floor ~$98-100K (RP CAGR ~30%); 12 September 2029 → peak $371,557/floor ~$146K (berdasarkan asumsi siklus 47-bulan, lihat entri [KONFLIK] di bawah); ilustrasi 100 tahun → konvergen ke ~$1.7 miliar; 2045 → peak $4.4 juta/floor $3.3 juta vs target Saylor $21 juta. Pembicara sendiri mengakui "model ini pasti akan break di suatu titik." [05:22]–[09:43]
- **Indikator terkait:** turunan model amplitude decay + RP CAGR
- **Relevan ke:** general — horizon jauh di luar cakupan aktif framework (reaktif, bukan prediktif)
- **Test klaim:** Threshold absolut jauh ke masa depan, errornya compound dari training-window overfitting + decay rate arbitrer. Event 2028/2029/2045 belum terjadi — tidak ada data historis untuk diuji lawan. Proyeksi 100-tahun & 2045 eksplisit diakui sendiri sebagai ilustrasi, bukan klaim serius.
- **Perlu validasi Claude Code:** Tidak — event masa depan, data tidak tersedia untuk validasi; dicatat sebagai konteks saja.

### [INDIKATOR CUSTOM] Quantile bands methodology (persentil 5th/95th dari decaying MVRV trend lines)
- **Insight:** Alih-alih satu garis titik puncak/lembah, dibuat pita persentil berdasarkan decaying MVRV trend lines — pendekatan probabilistik terhadap posisi harga dalam distribusi historis, bukan target absolut tunggal. [09:43]–[10:30]
- **Indikator terkait:** turunan MVRV Ratio + realized price decay model
- **Relevan ke:** general — konsep pita mirip filosofi zone-based framework (Z1-Z5), meski basis kalkulasi beda total (curve-fit forward projection vs level RP/AVIV absolut saat ini)
- **Test klaim:** Band di-fit ke data historis yang sama yang dipakai untuk "cek akurasi" — akurasi in-sample nyaris tautologis kecuali diuji out-of-sample ketat.
- **Perlu validasi Claude Code:** Ya

### [INDIKATOR CUSTOM] Klaim akurasi quantile bands "practically to perfection" termasuk out-of-sample
- **Insight:** Diklaim akurat sepanjang sejarah BTC, termasuk saat training data dibatasi ke 2015/2019/2023 (out-of-sample), walau pembicara sendiri mengakui versi cutoff-2015 belum sampai kondisi sekarang dan cutoff-2019 tidak menangkap tepat bear low 2022. Dipakai untuk klaim BTC saat ini masuk persentil ke-5 terbawah historis → "unbelievable discount territory." [10:30]–[11:34]
- **Indikator terkait:** sama seperti di atas
- **Relevan ke:** general, langsung bersinggungan dengan diagnosis zona saat ini
- **Test klaim:** Klaim sudah mengandung kontradiksi sendiri (mengakui miss di bear low 2022 tapi tetap bilang "practically to perfection"). Sample out-of-sample cuma 3 titik cutoff yang overlap satu sama lain dan siklus yang sama — bukan independent test kuat.
- **Perlu validasi Claude Code:** Ya

**[VALIDASI — 2026-07-29, CLOSED]** Proxy percentile-band out-of-sample dari MVRV Ratio (bukan replikasi model decay pembicara persis) menunjukkan breach rate rendah (0-3.2%, n forward 1291-4213 hari per cutoff training 2015/2019/2023, 0-7 episode breach) — mendukung klaim kualitatif "band cukup akurat" secara umum, tapi TIDAK sekuat "practically to perfection" (cycle 2012-2016 breach rate 17%, jauh lebih tinggi). Klaim spesifik "saat ini masuk persentil ke-5 terbawah / unbelievable discount" **TIDAK terverifikasi**: mvrv_ratio terakhir (1.234, data 2026-07-15) jauh di atas band bawah (0.79-0.82) di semua cutoff & baseline in-sample. Detail: [`findings_quantile_band_accuracy.md`](findings_quantile_band_accuracy.md)

### [INDIKATOR CUSTOM] Rencana filtered/dynamic Realized Price (hapus inscriptions, unspendable, dust)
- **Insight:** Iterasi berikutnya yang direncanakan pembicara: pakai Realized Price yang difilter dari UTXO non-ekonomis (inscriptions, transaksi provably unspendable, dust), disebut mengubah Realized Price sebesar beberapa ribu dolar. [12:05]–[12:39]
- **Indikator terkait:** Realized Price versi filtered/dynamic — dekomposisi: RP standar dikurangi kontribusi UTXO non-ekonomis
- **Relevan ke:** general — RP adalah level kunci penentu batas zona, versi filtered berpotensi menggeser level batas kalau divalidasi
- **Test klaim:** Genuine refinement metodologis, tapi baru rencana — belum ada metodologi/angka final untuk diuji.
- **Perlu validasi Claude Code:** Tidak — data raw UTXO set tidak tersedia di dashboard kita (hanya kolom agregat). Catat sebagai item pantau kalau provider merilis kolom filtered-RP baru nanti.

### [KONFIRMASI] CAGR Realized Price turun tajam (klaim: 38% historis rata-rata → 0-8% saat ini)
- **Insight:** Compounded annual growth rate Realized Price saat ini (~0-8%) jauh di bawah rata-rata historis (~38%), karena harga setahun lalu mirip harga sekarang. Selaras dengan prinsip diminishing returns tiap cycle. [02:56]–[03:27]
- **Indikator terkait:** Realized Price CAGR (turunan RP)
- **Relevan ke:** general — selaras dengan prinsip diminishing MVRV/aSOPR peaks tiap ATH baru di K1
- **Test klaim:** Angka presisi "38%" sensitif terhadap window CAGR yang dipilih (rolling 1yr? peak-to-peak?) — berpotensi cherry-picked.
- **Perlu validasi Claude Code:** Ya

**[VALIDASI — 2026-07-29, CLOSED]** CAGR Realized Price saat ini (5.92%, data 2026-07-15) match kuat dengan klaim "0-8%". Klaim "rata-rata historis ~38%" cuma partial-match: median per-cycle (n=500-1440 hari/cycle) berkisar 15-74%, median pooled post-2012-halving 44.1% — order-of-magnitude sama dengan 38% tapi tidak presisi; MEAN gabungan (556.7%) sangat menyesatkan karena didominasi outlier 2010-2012 (harus dibaca median, bukan mean mentah). Detail: [`findings_rp_cagr_decline.md`](findings_rp_cagr_decline.md)

### [KONFIRMASI] "Lebih baik bereaksi daripada memprediksi"
- **Insight:** Pembicara sendiri eksplisit mengakui "no model is going to work perfectly going forward and it's always better to react rather than predict" — membingkai model proyeksinya sebagai "cara menghibur di bear market", bukan basis keputusan utama. [02:24]–[02:39]
- **Indikator terkait:** meta-statement, general philosophy
- **Relevan ke:** general — konsisten dengan prinsip framework "bereaksi terhadap sinyal relatif, bukan memprediksi harga/tanggal absolut"
- **Test klaim:** Pernyataan filosofis, bukan klaim numerik — genuinely align dengan prinsip framework, tidak perlu diuji ulang.
- **Perlu validasi Claude Code:** Tidak.

### [KONFLIK] Klaim siklus 47 bulan top-to-top sebagai dasar prediksi tanggal puncak presisi
- **Insight:** Jarak top-to-top dua siklus terakhir diklaim sama persis 47 bulan (2017→2021 dan 2021→2025), dipakai sebagai basis utama memprediksi puncak siklus berikutnya jatuh tepat 12 September 2029, dengan harga presisi $371,557. [07:01]–[07:50]
- **Konflik dengan:** Prinsip utama framework — "threshold absolut tidak reliable antar cycle, pakai pola relatif" (di sini diterapkan ke dimensi waktu/calendar interval, bukan harga, tapi pelanggarannya sama persis) dan Governance framework ("threshold = panduan arah dari 3-4 siklus, bukan presisi").
- **Alasan konflik:** n=2 interval cycle (2017→2021, 2021→2025) dipakai untuk derive tanggal + harga presisi tunggal — di bawah standar minimal framework sendiri (3-4 cycle = sample kecil, harus di-flag low-confidence eksplisit). "Persis 47 bulan" untuk 2 interval kemungkinan besar kebetulan, mengingat definisi "top" bisa bergeser beberapa minggu/bulan tergantung metodologi.
- **Rekomendasi:** Abaikan sebagai basis keputusan — dicatat sebagai referensi/contoh kasus overfitting n-kecil, bukan sinyal actionable. Backlog validasi: cek interval top-to-top untuk semua siklus BTC (2011, 2013, 2017, 2021, 2025) — kemungkinan interval-interval lebih awal jauh berbeda dari 47 bulan, sehingga kecocokan 2 data poin terakhir cuma kebetulan.

### [STRATEGI] Narasi "diminishing volatility karena institutional demand" sebagai justifikasi model decay
- **Insight:** Modal institusional membuat blow-off top makin kecil euforianya dan bear market makin kecil kehancurannya, sehingga price action makin konvergen ke Realized Price dari waktu ke waktu. [08:22]–[08:55]
- **Indikator terkait:** naratif makro, tidak terikat indikator on-chain spesifik
- **Relevan ke:** general
- **Test klaim:** Causal attribution ke "institutional demand" tidak bisa diverifikasi langsung — data whale/entity/ETF flow granular tidak ada di dashboard kita.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia untuk causal claim; underlying pattern (diminishing amplitude) sudah tercakup di validasi lain.

### [STRATEGI] Klaim track record: model berhasil di mana on-chain data lain gagal di bull market terakhir
- **Insight:** Model quantile band diklaim berhasil "di mana kebanyakan on-chain data points gagal" di bull market terakhir, meski tidak menangkap puncak persis 6 Oktober, tapi "nailed" level 110-120K di leg pertama. [11:34]–[12:05]
- **Indikator terkait:** quantile bands
- **Relevan ke:** general
- **Test klaim:** Klaim vague, tanpa definisi "berhasil"/"gagal" yang jelas atau metrik pembanding spesifik — self-serving promosi model milik sendiri, risiko survivorship bias klasik.
- **Perlu validasi Claude Code:** Tidak — klaim terlalu vague untuk didefinisikan sebagai event testable.

### [STRATEGI] Market call: harga saat ini masuk persentil ke-5 terbawah historis → "unbelievable discount territory"
- **Insight:** Berdasarkan quantile bands, pembicara menyatakan BTC baru masuk persentil ke-5 terbawah data historis, menyimpulkan ini "unbelievable discount territory" meski mengakui harga bisa turun lebih jauh. [11:16]–[11:34]
- **Indikator terkait:** quantile bands
- **Relevan ke:** Z1/ZC (bottom capitulation zone) — klaim mirip logika K4 tapi berbasis metodologi berbeda total
- **Test klaim:** Klaim actionable ini bergantung penuh pada validitas model pembicara. Perlu cross-check independen pakai zone/K-node framework kita sendiri.
- **Perlu validasi Claude Code:** Ya

**[VALIDASI — 2026-07-29, CLOSED]** Cross-check independen (n=1 snapshot 2026-07-15 + konteks 90 hari, pakai definisi zone/K4 Decision Framework kita sendiri tanpa mengubah threshold apapun) menunjukkan Zone = **ZD (Dip dalam)**, bukan Z1/ZC. K4 count = 0/4 (tidak ada kondisi bear-bottom aktif), mvrv_ratio percentile rank 22.6th, Price/CVDD percentile rank 9.3rd — semua menandakan dip moderat, bukan extreme/bottom-5th-percentile. Klaim "unbelievable discount territory" **tidak terkonfirmasi** oleh diagnosis independen framework kita. Detail: [`findings_current_zone_crosscheck.md`](findings_current_zone_crosscheck.md)

---

## Flag Prioritas

1. **[BARU] Dynamic LTH classification (multi-boundary Realized Price)** — satu-satunya insight yang menyentuh backbone zona kita (cutoff STH/LTH 155 hari) dengan alasan struktural yang masuk akal (paper referensi pembicara, bukan preferensi channel semata). Sudah divalidasi: low-impact untuk zone structure kita, tapi worth didiskusikan karena ini titik gesekan paling substantif secara metodologis di video.
2. **Cross-check zone saat ini (ZD, bukan Z1/ZC, K4 count 0/4)** — independen dari klaim pembicara, tapi berguna sebagai reality-check posisi kita saat ini di framework sendiri per 2026-07-15.
3. **Klaim siklus 47-bulan (n=2) → prediksi tanggal presisi** — good case-study soal kenapa kita sengaja tidak pakai fixed calendar cycle length sebagai basis keputusan; worth didokumentasikan eksplisit.
4. **CAGR Realized Price turun tajam (5.92%, data 2026-07-15)** — angka konkret yang align dengan prinsip diminishing returns framework, berguna sebagai referensi kuantitatif tambahan.

---

## Yang Langsung Diabaikan

- Proyeksi harga/tanggal presisi jauh ke masa depan (halving 2028, 12 Sept 2029, 2045, 100 tahun) — bukan actionable untuk pipeline reaktif kita, dan pembicara sendiri mengakui ini akan "break di suatu titik".
- Narasi causal "institutional demand → diminishing volatility" — tidak bisa diverifikasi, data whale/entity granular tidak tersedia.
- Klaim track record self-promosi model quantile band — terlalu vague untuk diuji.
- Segmen promosi Bitcoin Magazine Pro dan tangen personal soal World Cup — tidak relevan.
