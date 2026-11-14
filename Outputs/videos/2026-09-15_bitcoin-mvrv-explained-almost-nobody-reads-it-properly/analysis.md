# Bitcoin MVRV Explained (Almost Nobody Reads It Properly)
**Channel:** On-Chain Mind
**Tanggal video:** 2026-09-15
**Tanggal analisis:** 2026-09-16
**Link:** https://www.youtube.com/watch?v=NOqtqNy5GkE

> **FLAG STOP-1 (dibawa dari analisis 2026-08-25, sekarang aktif):** syarat bear selesai di DF v2 §0 (STH RP cross naik RP) mustahil secara mekanis di struktur N. Per 2026-09-15 sudah 0 hari struktur T dalam 345 hari sejak peak, dengan min STH RP/RP 1,272. Video ini menggambarkan skenario yang dikhawatirkan STOP-1 dan skenario itu sudah terjadi:
> - harga close di atas STH RP dan 200 DMA sejak 2026-08-19 (28 hari)
> - kandidat unlock (ii) nyala 2026-08-21 dan (i) nyala 2026-09-08, pertama kali di bear ini
> - MVRV Momentum bullish-valid sejak 2026-07-29
> - pembicara membaca "bull market is back"
>
> Framework tetap di Z3-bear = tunggu: K2 di luar band, K5 terkunci. Semua sinyal alternatif masih censored sampai sekitar 2026-11-16, dengan baseline historis 25–29% (n=4/7). **Butuh keputusan Yudi.** Tidak ada flag STOP baru: tidak ada insight yang bentrok hard constraint LTV, dan tidak ada strategi yang menggantikan zone + K-node.

---

## Ringkasan

Video edukasi (15:02) tentang MVRV. Isinya cara membaca MVRV lewat lima tampilan di dashboard On-Chain Mind, lalu bagian khusus tentang cohort STH.

**Definisi.** Realized cap = total cost basis network, "just over $1 trillion" (CSV $1,069T). MVRV = unrealized P/L agregat, bukan metrik harga.

**Lima tampilan MVRV:**
1. **Raw MVRV.** Peak tiap siklus makin rendah. Siklus ini "barely over 2.5" dan MVRV tidak pernah di bawah 1 di bear terakhir, yang menurut pembicara pertama kali dalam sejarah.
2. **Z-Score.** Pembicara mengoreksi rumusnya: (MC − RC)/σ(MC), bukan Z dari MVRV. Dia menilai Z-Score kurang berguna karena polanya mirip raw MVRV.
3. **Percentile.** Diklaim kebal diminishing peaks: p90 2013 disebut sama artinya dengan p90 hari ini.
4. **Momentum.** Laju perubahan MVRV. Crossover-nya diklaim "lead" perubahan tren. Sekarang disebut "right on the edge" hijau untuk pertama kali dalam lebih dari setahun.
5. **Distribution.** Ekor kanan histogram yang tipis diklaim jadi early warning distribusi.

**STH-MVRV.** Bagian ini diklaim paling taktis dan "remarkably consistent" antar siklus karena cohort reset tiap sekitar 5 bulan. Level 1,0 disebut jadi support di bull (2017) dan resistance di bear (2018, 2022, 2026). Klaim penutupnya: STH-MVRV baru reclaim 1,0 "convincingly" untuk pertama kali sejak Okt 2025, dan "in every other historical case" reclaim seperti itu menandai awal bull.

**Hasil validasi.** 4 validasi dijalankan dengan data sampai 2026-09-15:
- Rumus Z-Score versi video **benar**, dan KB MVRV §1 salah.
- Klaim percentile **gagal**: bull 2024-25 tidak pernah menyentuh p90 causal.
- Bullish momentum cross di bear non-Z1 **tidak punya edge** (2/12 HIT).
- "Reclaim pertama sejak Oktober" melewatkan episode Mei 2026 yang gagal. "Every other case" juga tidak didukung data (7/8 break Signal D di bear balik ke bawah).

---

## Insight Inventory

### [KONFIRMASI] Realized cap = cost basis network; MVRV = unrealized P/L agregat
- **Insight:** Realized cap menilai tiap UTXO di harga terakhir koin itu bergerak, jadi hasilnya cost basis agregat. MVRV 1 berarti rata-rata holder impas, <1 berarti underwater. "MVRV isn't a price metric" `[00:26]`–`[03:00]`. Angka realized cap "just over $1T" `[02:04]` cocok dengan CSV ($1,069T per 09-15).
- **Indikator terkait:** MVRV Ratio, Realized Cap
- **Relevan ke:** general (KB MVRV §1)
- **Test klaim:** Definisional. Ada satu penyederhanaan: realized cap disebut "modal yang benar-benar masuk", padahal realized cap juga naik kalau koin lama pindah tangan di harga lebih tinggi. Jadi realized cap itu proxy, bukan net inflow. Tidak ada klaim empiris yang bisa salah. Sudah dibahas di backlog 2026-06-23.
- **Perlu validasi Claude Code:** Tidak

### [KONFIRMASI] Unrealized profit = bahan bakar jual
- **Insight:** Holder jarang jual saat rugi dalam, kecuali capitulation. Saat untung 200–400%, dorongan realisasi profit makin besar `[03:00]`–`[03:53]`.
- **Indikator terkait:** MVRV Ratio
- **Relevan ke:** K1, syarat awal K3
- **Test klaim:** Mekanik sudah established di KB MVRV/SOPR. Titik lemahnya diakui video sendiri `[13:18]`: MVRV bisa tetap tinggi berbulan-bulan (KB §5.1 FM2: Sep 2017 MVRV 2,57–2,84, lalu harga masih +261%).
- **Perlu validasi Claude Code:** Tidak

### [KONFIRMASI] Raw MVRV >3–4 = top, <1 = value zone
- **Insight:** Threshold klasik yang "genuinely did work for many cycles" `[03:53]`–`[04:18]`. Pembicara sendiri lalu menyebutnya usang.
- **Indikator terkait:** MVRV Ratio
- **Relevan ke:** K1/Z5, ZC/K4
- **Test klaim:** **Threshold absolut.** Framework sudah pakai pola relatif (divergensi per-ATH, SMA180, momentum). Peak siklus tercatat 4,39 / 2,92 / 2,28 (KB §2.1), jadi ">3" hanya kena 2017 dari tiga siklus terakhir. "<1" tidak tercapai di bear 2025-26 (min P/RP 1,103). Ini konfirmasi failure mode yang sudah dikenal (KB §5.1 FM1).
- **Perlu validasi Claude Code:** Tidak

### [KONFIRMASI] Diminishing MVRV peaks tiap siklus
- **Insight:** Peak 2011 > 2013 > 2017 > 2021 > siklus ini, yang "barely got over 2.5" `[04:18]`–`[04:54]`. Menunggu angka lama = menunggu selamanya. Di penutup disebut "a feature, not a bug", tapi membuat posisi siklus makin sulit dibaca `[13:43]`. Frame menampilkan peak sekitar 8 / 6 / 5 / 4 / 2,7 dengan garis tren turun (low confidence dari resolusi frame).
- **Indikator terkait:** MVRV Ratio
- **Relevan ke:** syarat awal K1 dan K3
- **Test klaim:** n=5 siklus, sudah established (source_index 2025-01-22). "Barely over 2.5" cocok dengan max siklus di Mar 2024 (2,59–2,75), bukan final peak Okt 2025 (2,22–2,28). Pembicara mencampur keduanya, tapi tidak material. Klaim salah kalau siklus berikutnya punya peak lebih tinggi. Ekstrapolasi ke depan tetap n=3.
- **Perlu validasi Claude Code:** Tidak

### [KONFIRMASI] Baca posisi relatif terhadap sejarah, bukan angka absolut
- **Insight:** Kesimpulan pembicara dari diminishing peaks `[05:10]`–`[05:35]`
- **Indikator terkait:** MVRV Ratio (general)
- **Relevan ke:** prinsip utama DF v2, Governance butir 3
- **Test klaim:** Identik dengan prinsip framework. Titik lemahnya ada di solusi yang ditawarkan video: percentile mentah ternyata tidak men-detrend (lihat validasi [BARU] Percentile).
- **Perlu validasi Claude Code:** Tidak

### [KONFIRMASI] MVRV tidak pernah <1 di bear 2025-26, pertama kali dalam sejarah
- **Insight:** "We actually never even dip below one during our most recent bear. And this is the first time this has ever happened." Pembicara memperkirakan tren ini berlanjut `[05:10]`. Implisit, dia menganggap bear sudah selesai.
- **Indikator terkait:** MVRV Ratio, Realized Price
- **Relevan ke:** ZC (butuh P < RP), lantai waktu (close < RP), jalur Z1 K4 dan kondisi #1 (LTH-MVRV < 1), §0 syarat bear selesai
- **Test klaim:**
  - **"Pertama kali" benar.** Trough bear sebelumnya 0,401 / 0,568 / 0,702 / 0,760. Bear sekarang min P/RP 1,103 dan min LTH-MVRV 1,173, keduanya 2026-06-30 (`findings_stop1_update_2026_09.md`).
  - **"Tren berlanjut" = ekstrapolasi n=4** (backlog 2026-07-09 SUPPORTED, deskriptif). Kata yang tepat "cenderung", bukan pasti.
  - **"Bear sudah selesai" belum terbukti.** Status DF masih bear, dan low 06-30 masih sementara. Bagian ini digabung ke [KONFLIK] STH-MVRV reclaim di bawah.
  - Klaim salah kalau harga close di bawah RP (~$53.237, sekitar −31% dari harga sekarang) sebelum bear terbuka.
  - Implikasi ke framework: ZC, lantai waktu, dan K4 #1 cenderung tidak pernah aktif di siklus ini. Sudah terukur di backlog 08-05 dan 08-25.
  - Direklasifikasi dari [BARU] karena seluruh bagian deskriptifnya sudah terukur di backlog.
- **Perlu validasi Claude Code:** Tidak (angka terbaru sudah di-update lewat `findings_stop1_update_2026_09.md` bagian (e))

### [KONFIRMASI] MVRV Z-Score polanya mirip raw MVRV, kurang berguna
- **Insight:** Z-Score dibuat untuk meredam distorsi era awal, tapi polanya mirip raw MVRV dan ayunan besarnya sudah hilang, jadi "hasn't been particularly useful" `[06:02]`–`[06:28]`
- **Indikator terkait:** MVRV Z-Score
- **Relevan ke:** general. DF tidak memakai Z-Score sebagai gate.
- **Test klaim:** Konsisten dengan temuan KB bahwa Z rolling 1 tahun bukan sinyal independen. Tegangan ringan: KB masih memakai threshold Z absolut di Rule B2 (Z > 1,0), B5 (Z < −0,15), dan B6 (Z > 0,05), padahal peak Z turun 9,27 → 3,54 → 2,53. Tidak ada keputusan DF terkunci yang kena. Sudah dibahas backlog 2026-07-09.
- **Perlu validasi Claude Code:** Tidak sendiri. Aspek rumus dan lookahead sudah diuji di [BARU] Rumus Z-Score.

### [KONFIRMASI] Level = di mana, momentum = arah
- **Insight:** MVRV bisa "sehat" di 2, tapi kalau momentum baru rollover negatif, profitabilitas rata-rata sedang memburuk `[07:47]`–`[08:38]`
- **Indikator terkait:** MVRV Momentum
- **Relevan ke:** DF §0 alarm CEPAT sinyal 3 (bearish cross), pembuka episode K2
- **Test klaim:** Konseptual, persis logika framework. Tidak ada yang bisa salah selain definisi.
- **Perlu validasi Claude Code:** Tidak

### [KONFIRMASI] Crossover MVRV Momentum "lead" perubahan tren besar
- **Insight:** "Crossovers in this momentum view have tended to lead those big trend changes" `[08:52]`. Frame menampilkan panah di bullish cross sekitar 2015/16, 2019, 2023. Momentum sekarang disebut "right on the edge of transitioning back into the green again for the first time in over a year" `[08:58]`.
- **Indikator terkait:** MVRV Momentum (versi OCM, parameter tidak diungkap)
- **Relevan ke:** confirming context K4 (bullish cross di Z1), top-up dan penutupan episode K2
- **Test klaim:**
  - Tiga contoh dipilih retrospektif tanpa contoh gagal. Data KB §6C.1 menunjukkan cross lebih cenderung **konfirmasi telat, bukan leading**:
    - Bearish cross muncul +10 s/d +19 hari setelah peak (4/4).
    - Bullish cross di koreksi bull muncul median 23 hari setelah low.
    - Satu-satunya "lead" adalah bullish cross di Z1, 21–37 hari sebelum Signal D, bukan sebelum bottom harga.
  - Konteks sekarang belum pernah diuji: bear terkonfirmasi, di luar Z1, struktur N.
  - Label dipertahankan [KONFIRMASI], dengan koreksi "confirm, bukan lead".

**[VALIDASI — 2026-09-16, CLOSED]** Bullish cross MVRV Momentum (definisi KB 6C.1, dinilai di hari ke-7) selama bear di luar Z1 cenderung **bukan** penanda akhir bear.
- **n=16 event, 12 dinilai → 2 HIT (17%).** Kedua HIT dari bear 2011; bear 2013, 2017, dan 2021 **0/9**. Ada 4 event censored di 2025-26. Sebaran per cycle 3/1/5/3/4.
- Hasil ini di bawah kandidat (i) 29% dan setara Signal D like-for-like (14%) maupun base rate harian (14%). Median ret90 −14,6%.
- Satu-satunya pembeda: Signal D aktif di hari konfirmasi (2/3 vs 0/9). Tapi n=3 dan didominasi 2011, jadi low confidence.
- Cross sekarang (sah 2026-07-29) masuk kelompok **tanpa** Signal D.
- Versi momentum kita juga tidak "right on the edge": gap sudah positif 55 hari (+0,125), dan sempat positif di Okt 2025, Jan 2026, Mar–Mei 2026.

Detail: [`findings_bullcross_bear_nonz1.md`](findings_bullcross_bear_nonz1.md)

- **Perlu validasi Claude Code:** Ya — sudah diuji (di atas)

### [KONFIRMASI] LTH vs STH berlawanan; MVRV agregat mencampur jadi "mush"
- **Insight:** STH = koin yang bergerak dalam 155 hari terakhir, LTH = sisanya. Kata pembicara, 155 hari "isn't arbitrary" karena di titik itu koin secara statistik jauh lebih jarang dibelanjakan. Dua cohort berperilaku berlawanan `[09:54]`–`[10:33]`.
- **Indikator terkait:** STH-MVRV, LTH-MVRV
- **Relevan ke:** general; definisi STH RP / LTH RP di zone structure
- **Test klaim:**
  - **Bagian cohort:** established (KB MVRV §1, §6.2).
  - **"155 not arbitrary":** hanya benar untuk asal-usulnya, bukan stabilitasnya. Rekonstruksi di backlog 2026-06-18 menunjukkan batas bergeser 105–120 → 150–231 → 114 hari. Price_Level KB §6 juga mencatat angka ini "arbitrary".
  - Tidak dijadikan [KONFLIK] karena keputusan terkunci (06-18: pertahankan static-155) justru searah dengan video. Yang berbeda cuma catatan interpretasi di KB, dan dampak operasionalnya nol.
- **Perlu validasi Claude Code:** Tidak (data hazard spend per umur UTXO tidak tersedia)

### [KONFIRMASI] Raw STH-MVRV konsisten antar siklus karena cohort reset tiap ~5 bulan
- **Insight:** Beda dengan MVRV agregat, raw STH-MVRV "has remained remarkably consistent for many cycles" `[10:37]`. Alasannya, selalu ada "fresh wave of recent buyers with a fresh cost basis". Menurut pembicara, ini satu-satunya raw view yang tidak akan berubah `[14:21]`–`[14:36]`.
- **Indikator terkait:** STH-MVRV
- **Relevan ke:** gate valuasi K2 (band absolut 0,80–0,97)
- **Test klaim:**
  - **Benar untuk pivot 1,0 dan band di bawahnya.** Pivot 1,0 memang break-even secara konstruksi. Backlog 2026-06-18 menolak gate kuantil STH-MVRV dan mempertahankan band absolut 0,80–0,97, jadi klaim ini mendukung desain K2.
  - **Tidak benar untuk amplitudo.** Peak STH-MVRV turun 2,19 → 1,43 → 1,10 (KB §5.2 FM2), dan low bull dip bergeser 0,93 → 0,82. Threshold atas seperti "trim when well above one" tidak portable.
  - Direklasifikasi dari [KONFLIK] karena tidak ada keputusan terkunci yang dibantah.
- **Perlu validasi Claude Code:** Tidak (sudah tercakup 06-18 CLOSED dan KB §2.1/§2.7)

### [KONFIRMASI] STH-MVRV = 1 sebagai support di bull
- **Insight:** Cost basis STH dekat harga spot, jadi STH-MVRV berosilasi di sekitar 1. Di bull, STH-MVRV yang turun ke 1 berulang kali jadi dasar koreksi karena pembeli baru impas dan masuk lagi `[10:55]`–`[11:16]`. Contoh 2017 (7 panah di frame): pola ini bertahan sampai euforia mendorong STH-MVRV terlalu jauh di atas 1, sehingga "no cohort left underneath to defend it" `[11:23]`–`[11:49]`.
- **Indikator terkait:** STH-MVRV (setara harga vs STH RP)
- **Relevan ke:** batas Z3/ZD, gate K2 (0,80–0,97), staging K5
- **Test klaim:**
  - Bukti video hanya 1 siklus (2017) → **low-confidence dari sisi bukti video**.
  - Data kita lebih luas dan menunjukkan "lantai"-nya berupa **zona di bawah 1**, bukan tepat di 1:
    - KB §2.7: 12/15 bull dip turun di bawah 1 (2024–25 sampai 0,82–0,94).
    - Backlog 2026-08-25 P4: 10/21 pullback early-bull berhenti dalam ±5% STH RP, median overshoot −4,9%.
  - Karena itu gate K2 dipasang di 0,80–0,97.
  - Kasus gagal: mid-cycle 2021, STH-MVRV sampai 0,67 dan harga −53%. Beli "di 1" saat itu masih kena sekitar −30% lagi.
- **Perlu validasi Claude Code:** Tidak (tercakup KB §2.7 dan P4 CLOSED)

### [KONFIRMASI] STH-MVRV = 1 sebagai resistance di bear (2018, 2022, 2026)
- **Insight:** Di bear, rally STH-MVRV ke 1 berulang kali jadi puncak relief bounce karena pembeli baru lega bisa keluar impas. Pembicara menyebut 2018 "textbook" dan 2022 "carbon copy". Untuk 2026, sejak top Oktober "every attempt to reclaim that one level was sold straight into" `[11:52]`–`[13:18]`.
- **Indikator terkait:** STH-MVRV / STH RP
- **Relevan ke:** batas atas ZD, Signal D, wrap-up K4
- **Test klaim:**
  - Polanya sudah CLOSED kuat di backlog 2026-08-04: n=13 event di 5 bear, median drawdown 30 hari untuk event yang ditolak −24,2%.
  - Detail per episode di video dirapikan:
    - **2018:** data kita punya BREAK 2018-07-24 (4 hari), jadi tidak "couldn't hold above one" sepanjang tahun.
    - **2026:** data kita punya episode STH-MVRV > 1 selama 12 hari (2026-05-04..05-15, max 1,048), jadi tidak "pinned below" sepanjang tahun.
- **Perlu validasi Claude Code:** Tidak (selisih Mei 2026 sudah dicek di `findings_stop1_update_2026_09.md` bagian (d))

### [KONFIRMASI] MVRV bukan alat timing berdiri sendiri
- **Insight:** Raw MVRV bisa bertahan overheated berbulan-bulan atau di bawah 1 lama. MVRV memberi gambaran risk/reward per siklus, bukan arah minggu atau bulan depan `[13:35]`–`[13:59]`.
- **Indikator terkait:** MVRV Ratio
- **Relevan ke:** general (KB §5.1 FM2, §5.3B FM2)
- **Test klaim:** Tidak falsifiable secara berarti. Sejalan dengan desain multi-sinyal framework.
- **Perlu validasi Claude Code:** Tidak

### [BARU] Rumus MVRV Z-Score: (Market Cap − Realized Cap) / σ(Market Cap), bukan Z dari MVRV
- **Insight:** "The MVRV Z-Score isn't a Z-Score of the MVRV ratio". Rumus di layar: (Market Cap − Realized Cap) / Standard Deviation (Market Cap) `[05:35]`–`[06:14]`. Rumus ini bertentangan dengan dokumentasi KB MVRV v1.4 §1, yang menulis Z = (MVRV − mean)/stdev.
- **Indikator terkait:** MVRV Z-Score
- **Relevan ke:** koreksi dokumentasi KB MVRV (§1, §5.3B FM1, §9 #7), `data_dictionary.md`, dan Rule B2/B5/B6 di KB. Bukan keputusan DF.
- **Test klaim:**
  - Rumus video adalah definisi standar Mahmudov/Puell.
  - KB tidak konsisten dengan angkanya sendiri: dengan rumus KB, Z 9,24 di MVRV 4,39 butuh σ(MVRV) sekitar 0,29. Itu mustahil untuk seri yang rentangnya 0,4 sampai >5.
  - Pertanyaan turunan yang lebih penting untuk rule: apakah σ di kolom `mvrv_zscore` expanding atau full-sample (lookahead)?
  - Direklasifikasi dari [KONFLIK] karena yang dibantah catatan KB, bukan keputusan terkunci.

**[VALIDASI — 2026-09-16, CLOSED]** Kolom `mvrv_zscore` = (MC − RC) / σ **expanding**(MC), dengan korelasi 1,0000 dan median error 0,0095.
- Dari 4 varian yang dikunci di muka, hanya varian ini yang cocok. Rumus KB §1 (MVRV − mean)/σ meleset dengan median error sekitar 1,3.
- **Kolom ini causal.** A-full yang dihitung dengan data dipotong di 2021-11-08 = 3,529, sama dengan kolom (3,536). Nilai historis di KB (2017 9,24 / 2021 3,66 / 2025 2,53) juga stabil. Jadi threshold Z di KB B2/B5/B6 tidak mengandung lookahead dari rumus.
- Yang perlu dikoreksi:
  - rumus di KB §1
  - penjelasan "dilusi mean/stdev" di §5.3B FM1 dan §9 #7 (kompresi sebenarnya datang dari σ market cap USD yang terus membesar)
  - label "full-history" di `data_dictionary.md`
- Ini uji rumus, bukan uji event, jadi n = 5.905 hari dan sebaran per cycle tidak relevan.

Detail: [`findings_mvrv_zscore_formula.md`](findings_mvrv_zscore_formula.md)

- **Perlu validasi Claude Code:** Ya — sudah diuji (di atas). Koreksi KB dikerjakan di project Onchain-Dashboard, bukan di pipeline ini.

### [BARU] MVRV Percentile kebal diminishing peaks: "p90 2013 = p90 hari ini"
- **Insight:** Percentile tidak punya satuan, jadi "rescales itself to the asset's own evolving history". Karena itu 2013, 2017, 2021, dan hari ini dianggap bisa dibandingkan secara setara `[07:08]`–`[07:47]`. Klaim ini diulang di penutup sebagai tampilan favorit pembicara untuk posisi siklus `[14:13]`.
- **Indikator terkait:** MVRV Percentile
- **Relevan ke:** Z5/K1 dan K4/ZC, sebagai calon pengganti threshold absolut
- **Test klaim:**
  - Titik lemahnya struktural. Percentile mentah hanya transformasi monoton `mvrv_ratio` terhadap distribusinya sendiri, **tidak men-detrend**.
  - Sisi bawah sudah terbantah di backlog 2026-08-05: persentil causal di bear low sebelumnya 2,3 / 2,6 / 3,2, sementara bear sekarang minimum ~17.
  - Chart full-sample juga berisiko lookahead (rata-rata 4,6 pp).
  - Beda dengan BM Pro MVRV Quantile (backlog 08-05): BM Pro justru perlu amplitude decay adjustment.

**[VALIDASI — 2026-09-16, CLOSED]** Persentil MVRV causal (expanding, burn-in 365 hari) **tidak kebal** diminishing peaks. Kriteria falsifikasi yang ditetapkan di muka terpenuhi.
- **Di tanggal cycle peak**, persentil turun searah raw MVRV:
  - persentil 97,9 → 96,9 → 87,4 → 77,6
  - raw 5,17 → 4,39 → 2,85 → 2,29
- **Bull 2024-25 tidak pernah menyentuh p90** (0 hari, max 88,1). Bandingkan 59 / 100 / 102 hari di bull 2013 / 2017 / 2021.
- **n = 4 bull yang bisa diuji causal**, jadi sample kecil, tapi arahnya konsisten.
- Persentil hanya meredam kompresi: batas p90 turun sekitar 22%, sementara peak raw turun sekitar 56%.

Detail: [`findings_mvrv_percentile_diminishing_peaks.md`](findings_mvrv_percentile_diminishing_peaks.md)

- **Perlu validasi Claude Code:** Ya — sudah diuji (di atas)

### [BARU] Ekor kanan tipis distribusi MVRV = early warning distribusi sebelum harga berbalik
- **Insight:** Saat MVRV masuk ekor kanan histogram yang tipis, holder "have historically found it almost impossible not to sell". Sinyal ini diklaim "usually arrives prior to the price rolling over rather than after" `[09:12]`–`[09:52]`.
- **Indikator terkait:** MVRV Distribution
- **Relevan ke:** 5 sinyal peringatan K1, Z5
- **Test klaim:**
  - Video tidak memberi contoh historis sama sekali (n=0).
  - Kelemahannya sama dengan percentile: distribusi full-history diisi banyak hari >3 dari 2013/2017. Peak 2021 (2,85) dan 2025 (2,29) cenderung tidak masuk ekor tipis, jadi sinyal ini kemungkinan diam di dua top terakhir. Validasi percentile mendukung dugaan ini: peak 2025 hanya di persentil 77,6.
  - Klaim salah kalau top siklus terjadi tanpa MVRV masuk ekor.
  - Format yang sama dari channel ini pernah dibahas untuk SOPR (backlog 2026-08-04).
  - K1/Z5 tidak aktif sekarang.
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog. Pertanyaan: dengan persentil causal expanding `mvrv_ratio` (burn-in 365 hari), di setiap cycle peak (2011-06-08, 2013-11-29, 2017-12-16, 2021-11-08, 2025-10-06):
  - (a) berapa persentilnya
  - (b) adakah hari ≥p95 dalam 90 hari sebelum peak
  - (c) berapa lead time dari hari pertama ≥p95 ke peak
  - (d) berapa episode ≥p95 yang tidak diikuti peak dalam 180 hari

### [INDIKATOR CUSTOM] MVRV Percentile (Historical Percentile, dashboard OCM)
- **Insight:** Berapa persen sejarah Bitcoin yang MVRV-nya lebih rendah dari hari ini `[06:28]`–`[07:08]`. Frame menampilkan zona merah >~90% dan hijau <~10–15%. Nilai sekarang sekitar 35–40, low 2026 sekitar 15–20 (low confidence dari resolusi frame).
- **Indikator terkait:** MVRV Ratio
- **Relevan ke:** general; K1/Z5 dan K4/ZC kalau dipakai sebagai pembaca posisi siklus
- **Test klaim:**
  - **Dekomposisi:** rank persentil `mvrv_ratio` terhadap history. Tidak ada komponen baru.
  - Versi full-sample atau expanding tidak diungkap video. Angka layar terreplikasi persis dengan rank mentah full-history: P1 per 09-15 = 37,5, min 2026 = 17,0.
  - Chart historisnya memuat lookahead (backlog 08-05).
  - Klaim utamanya sudah diuji di [BARU] Percentile.
- **Perlu validasi Claude Code:** Tidak sendiri (digabung ke validasi Percentile)

### [INDIKATOR CUSTOM] MVRV Momentum versi OCM
- **Insight:** Osilator hijau/merah di sekitar 0, dari "short-term movement against the longer-term baseline" `[08:10]`. Metode persisnya (MA berapa, rasio atau selisih) tidak diungkap. Frame menampilkan periode merah panjang 2025–2026, dan nilai sekarang sekitar 0 (low confidence dari resolusi frame).
- **Indikator terkait:** MVRV Ratio
- **Relevan ke:** DF §0 sinyal 3, K2, K4
- **Test klaim:**
  - **Dekomposisi:** MA cepat vs baseline lambat dari `mvrv_ratio`. Kerabat MVRV Momentum DF v2 (SMA30 vs SMA30-of-SMA30), tapi parameternya belum tentu sama.
  - Bacaan OCM **tidak cocok** dengan versi kita. Versi kita bullish sejak 2026-07-23 (55 hari), dan sudah beberapa kali hijau dalam setahun terakhir (Okt 2025, Jan 2026, Mar–Mei 2026). Jadi "first time in over a year" tidak terreplikasi.
  - Bacaan status tetap harus pakai definisi kita (≥7 hari di kedua sisi).
- **Perlu validasi Claude Code:** Tidak sendiri (status versi kita dicek di `findings_stop1_update_2026_09.md` bagian (c))

### [INDIKATOR CUSTOM] MVRV Distribution (histogram + panel Current Status)
- **Insight:** Histogram berapa lama MVRV berada di tiap level `[09:12]`–`[09:31]`. Panel di frame: MVRV 1,43, bucket 1,40–1,60, 605 hari, 36,6% hari di bawah nilai sekarang (low confidence dari resolusi frame).
- **Indikator terkait:** MVRV Ratio
- **Relevan ke:** K1/Z5 (ekor kanan)
- **Test klaim:** **Dekomposisi:** histogram `mvrv_ratio`. "% days below" sama dengan persentil raw full-history, jadi duplikat Percentile. Angka panel terreplikasi dari CSV kita: 36,7% hari di bawah 1,43 dan 605 hari di bucket 1,40–1,60. Artinya OCM memakai data sumber yang setara.
- **Perlu validasi Claude Code:** Tidak (sanity check sudah ditempel di validasi Percentile)

### [KONFLIK] STH-MVRV reclaim 1,0 = awal bull "in every other historical case" (termasuk market call Sep 2026)
- **Insight:**
  - Sepanjang 2018, rejection di 1 berlangsung sampai 2019, "when price finally broke back above it which marked the start of the next bull market". Pola 2022→2023 disebut sama `[12:36]`–`[12:58]`.
  - Untuk 2026: "for the first time since October, we've actually convincingly broke back above one. And in every other historical case, that reclaim has marked the start of the next bull" `[13:20]`–`[13:31]`.
  - Ditambah momentum "on the edge" hijau `[08:58]`, dengan kesimpulan "we might be able to confirm that the bull market is indeed back". Pembicara menutup dengan "only time will tell".
- **Konflik dengan:**
  - DF v2 §0: status bear berakhir = STH RP cross naik RP (ordering struktur), bukan posisi harga terhadap STH RP.
  - Price_Level KB §6.3/§6.5: STH RP berbobot rendah sebagai trigger tunggal.
  - Findings backlog 2026-08-04: Signal D di bear 1/8 diikuti unlock.
- **Alasan konflik:**
  - STH-MVRV > 1 secara definisi sama dengan harga > STH RP (1,0776 vs 1,0788 per 09-15). Jadi klaim video menaikkan Signal D jadi penanda regime, padahal framework sengaja pindah ke ordering struktur karena sinyal harga-vs-STH-RP terlalu berisik.
  - Klaim "every other case" tidak menyebut kegagalan, dan video hanya memberi 2 contoh → **low-confidence**. "Convincingly" juga tidak didefinisikan.
  - Kedua contoh sukses (2019, 2023) terjadi di **struktur T**. Di backlog 08-25, flip STH profit memisahkan hasil per struktur: T 4/4 unlock, N 0/5. Reclaim sekarang terjadi di struktur N (STH RP/RP 1,337), jadi tidak ada analog sukses di bear siklus penuh.
  - Keluarga klaim yang sama dari channel ini sudah jadi [KONFLIK] di backlog 2026-08-25.

**[VALIDASI — 2026-09-16, CLOSED]** Per 2026-09-15 struktur masih N penuh (0 hari T dalam 345 hari, min STH RP/RP 1,272), jadi unlock formal masih mustahil secara mekanis.
- **Sinyal alternatif yang sudah nyala:**
  - close > STH RP dan > 200 DMA sejak 2026-08-19 (streak 28 hari)
  - kandidat (ii) nyala 08-21 (slope marginal +$23)
  - kandidat (i) nyala 09-08
- Semuanya **censored** sampai sekitar 2026-11-16. Baseline historis 25–29% (n=4/7).
- **STH-MVRV >1 sekarang 28 hari (max 1,151).** Tapi "first time since October" melewatkan episode Mei 2026 (12 hari, max 1,048) yang gagal. Episode sekarang memang yang terpanjang dan tertinggi sejak peak.
- **"Every other historical case" tidak didukung data:** 7/8 break Signal D di bear balik ke bawah STH RP dalam 90 hari (n=8 di 5 bear, backlog 08-04).
- Zona Z3. Gate K2 di luar band (STH-MVRV 1,078).

Detail: [`findings_stop1_update_2026_09.md`](findings_stop1_update_2026_09.md) · validasi momentum terkait: [`findings_bullcross_bear_nonz1.md`](findings_bullcross_bear_nonz1.md)

- **Rekomendasi:** Diskusikan lebih lanjut dengan Yudi, digabung ke STOP-1. Sebagai gauge regime, klaim ini cenderung ditolak. Tapi celah framework yang disentuhnya nyata dan sekarang aktif: ketiga kandidat alternatif nyala bersamaan untuk pertama kali di bear ini, sementara DF tidak punya jalur keluar dari status bear di struktur N.

### [STRATEGI] Rhythm trade STH-MVRV
- **Insight:** Di bull, "buying dips at that level and trimming when it stretches well above one" `[11:14]`–`[11:21]`. Di bear, "selling the rallies into this level rather than chasing them" `[12:14]`–`[12:19]`. Disebut "one of the most reliable rhythm trades in onchain analysis".
- **Indikator terkait:** STH-MVRV
- **Relevan ke:** K2 (beli dip, band 0,80–0,97), K1 (jual BTC hanya dari Z5), K6 (bayar loan dari cash, bukan jual BTC), K3 (short hanya hedge)
- **Test klaim:**
  - **Sisi bear:** didukung data (n=13, backlog 08-04).
  - **Sisi bull:** bukti video 1 siklus (2017) → low-confidence. Level belinya kepagian: 12/15 dip turun di bawah 1, dengan overshoot median −4,9%. "Well above one" tidak didefinisikan dan tidak portable (peak STH-MVRV 2025 cuma 1,10).
  - **Pemetaan ke framework:**
    - Beli dip sudah terwakili K2.
    - Trim mid-cycle tidak ada di framework, dan bertentangan dengan K1/K6.
    - Jual rally di bear = framework memilih tunggu.
  - Tidak menyentuh LTV (video tidak menyebut leverage). Ini overlay taktis satu indikator, bukan pengganti zone + K-node → **bukan STOP**.
  - Satu terjemahan yang berguna dari sisi bear: "jangan kejar rally ke STH RP saat status bear". Ini sudah jadi perilaku Z3-bear = tunggu.
- **Perlu validasi Claude Code:** Tidak (kedua sisi sudah CLOSED: backlog 08-04; backlog 08-25 P4 + KB §2.7)

### [STRATEGI] Hierarki alat pembicara
- **Insight:** Raw MVRV dan Z-Score makin jarang dipakai. Percentile dipakai untuk posisi siklus, raw STH-MVRV untuk keputusan taktis `[14:00]`–`[14:36]`.
- **Indikator terkait:** MVRV Ratio, MVRV Z-Score, MVRV Percentile, STH-MVRV
- **Relevan ke:** general (metodologi)
- **Test klaim:**
  - Preferensi pribadi, tidak falsifiable sebagai hierarki.
  - Pilar percentile-nya melemah setelah validasi: bull 2024-25 tidak pernah menyentuh p90.
  - DF sudah memakai raw MVRV dalam bentuk relatif (SMA180, momentum, divergensi per-ATH), jadi sejalan dengan prinsip video tanpa perlu percentile.
  - Adopsi alat baru harus lewat protokol Governance.
- **Perlu validasi Claude Code:** Tidak

### [STRATEGI] Narasi diminishing returns karena Bitcoin makin besar, likuid, dan institusional
- **Insight:** Bitcoin "is larger and it's more liquid and it's more institutionally held", jadi tidak lagi overextended sejauh dulu terhadap cost basis-nya `[04:44]`–`[05:00]`
- **Indikator terkait:** MVRV Ratio
- **Relevan ke:** general
- **Test klaim:** Causal claim naratif, tidak bisa difalsifikasi dengan data kita. Duplikat source_index 2025-01-22 ("tidak actionable") dan backlog 2026-07-13.
- **Perlu validasi Claude Code:** Tidak

### [KONFIRMASI] MVRV kembali >1 dari bawah + momentum naik = sinyal bear selesai paling bersih
- **Insight:** "When the raw number crosses back above one from below and the momentum is accelerating upwards, that has historically been one of the cleanest signals that the bear market is genuinely over rather than just bouncing" `[08:40]`–`[08:50]`
- **Indikator terkait:** MVRV Ratio + MVRV Momentum
- **Relevan ke:** DF §0 (syarat bear selesai), K4 selesai / K5 mulai
- **Test klaim:**
  - Contohnya implisit 2015, 2019, 2023, sekitar 3 siklus.
  - Komponennya sudah ada: KB Rule B6 (MVRV > 1 setelah lama di bawah 1, 2/2) dan KB 6C.1 (bullish cross di Z1). Tapi kombinasinya tidak dikodekan di DF.
  - Kata "cleanest" rawan false positive di relief rally bear. Contoh yang mungkin: MVRV kembali >1 di sekitar pertengahan 2022, lalu turun lagi ke 0,78 di Nov 2022. Belum dihitung.
  - B6 mensyaratkan periode <1 minimal 30 hari; video tidak.
  - **Nilai operasional untuk siklus ini nol**, karena MVRV tidak pernah <1.
- **Perlu validasi Claude Code:** Ya — belum diuji, backlog. Event = `mvrv_ratio` cross naik 1,0 setelah ≥30 hari di bawah 1,0, dengan gap MVRV Momentum (SMA30 − SMA30-of-SMA30) positif di hari cross, cooldown 90 hari. Pertanyaan: berapa event per siklus (2011–2023) yang dalam 90 hari kembali <1,0 atau drawdown ≥20%, dan berapa yang terjadi ≥ reclaim permanen −30 hari (definisi `findings_unlock_reachability_struktur_n.md`)?

---

## Flag Prioritas

1. **STH-MVRV reclaim / market call "bull is back" → STOP-1.** Untuk pertama kali di bear ini, ketiga kandidat unlock alternatif nyala bersamaan: close > STH RP 28 hari, kandidat (i) dan (ii), dan > 200 DMA. MVRV Momentum juga sudah bullish-valid. DF tetap tidak punya jalur keluar dari status bear di struktur N. Keputusannya: biarkan framework menunggu sampai sinyal selesai censored (sekitar 2026-11-16), atau bahas definisi unlock alternatif sekarang? Baseline historis kandidat cuma 25–29%, dan satu-satunya analog struktur N (mid-cycle 2019-20) bercampur.
2. **Rumus Z-Score di KB MVRV §1 salah.** Terbukti konklusif (korelasi 1,0000 dengan rumus video, σ expanding). Kabar baiknya, threshold Z di KB B2/B5/B6 tidak ter-lookahead. Tapi rumus, penjelasan mekanisme (§5.3B FM1, §9 #7), dan label `data_dictionary.md` perlu dikoreksi di project Onchain-Dashboard.
3. **Bullish momentum cross di bear non-Z1 tidak punya edge** (2/12, 0/9 di luar 2011). Cross yang sekarang (sah 07-29, tanpa Signal D) jangan dibaca sebagai konfirmasi akhir bear. Hasil KB 6C.1 untuk Z1 (4/4) tidak bisa digeneralisasi ke struktur N.
4. **MVRV Percentile gagal sebagai pembaca posisi siklus antar cycle.** Bull 2024-25 max di p88,1, dan peak 2025 hanya di p77,6. Kalau suatu saat ada usulan mengganti threshold MVRV absolut dengan percentile, temuan ini jadi argumen penolak utama. Implikasinya juga ke klaim ekor kanan distribusi (backlog).

---

## Yang Langsung Diabaikan

- **Promosi onchainmind.io dan newsletter** `[07:47]`: CTA sponsor.
- **"Market cap = vanity metric", "$1 trillion is a hell of a lot"** `[02:09]`–`[02:34]`: framing retoris. Angka realized cap sudah dicatat di insight definisi.
- **"Everyone has a price… a few thousand % gains"** `[03:33]`: ilustrasi retoris, mekaniknya sudah tercatat di "bahan bakar jual".
- **"MVRV sudah ada sejak ~2018"** `[00:31]`: trivia sejarah.
- **Harga $77.000 saat rekaman** `[00:59]`: konteks (CSV 09-15: $76.784).
- **Outro "let me know in the comments"** `[14:38]`: CTA.
