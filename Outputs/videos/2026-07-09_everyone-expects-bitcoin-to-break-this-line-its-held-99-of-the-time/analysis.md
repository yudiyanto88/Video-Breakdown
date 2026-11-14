# EVERYONE Expects Bitcoin To Break This Line, It's Held 99% Of The Time
**Channel:** Bitcoin Magazine Pro
**Tanggal video:** 2026-07-09
**Tanggal analisis:** 2026-07-28
**Link:** https://youtu.be/UVFDWEXV5eM

---

## Ringkasan

Video ini membahas pola MVRV raw ratio (bukan Z-score) yang membentuk wedge/converging channel lintas cycle: puncak makin rendah, lembah makin tinggi tiap cycle. Pembicara fit garis regresi eksponensial terpisah untuk seluruh puncak dan seluruh lembah historis MVRV, lalu mengklaim garis trough-fit baru saja crossing di atas MVRV=1 — mengimplikasikan Bitcoin kemungkinan besar (diklaim "99.7%+ chance") tidak akan dip di bawah realized price cycle ini. Level implied trough ~$53,300, implied peak next cycle $136K-$272K tergantung realized price masa depan. Dia juga coba metode sama ke LTH-MVRV dan mengakui sendiri hasilnya jauh lebih lemah karena distorsi lost coins era awal.

Validasi Claude Code menemukan perhitungan dasar video (persentase hari) cukup akurat direplikasi, tapi metodologi fit-nya sendiri circular dan sangat rapuh (leave-one-out test membalik kesimpulan di 2 dari 4 skenario) — sehingga klaim "99.7%" tidak valid sebagai basis prediksi kuantitatif. Namun observasi arah yang lebih sederhana di baliknya (trough MVRV naik monoton, severity dip mengecil tiap cycle) tetap SUPPORTED secara deskriptif dengan n=4 cycle.

---

## Insight Inventory

### [KONFIRMASI] Diminishing MVRV peaks tiap cycle
- **Insight:** Puncak MVRV (raw ratio) makin rendah tiap cycle berturut-turut — pola wedge sisi atas. [00:53]-[01:07]
- **Indikator terkait:** MVRV Ratio
- **Relevan ke:** K1 (top zone), general
- **Test klaim:** Sudah established di Decision Framework (dipakai di K1/K3 sebagai syarat "MVRV di ATH baru lebih rendah dari ATH sebelumnya", n=5 dari video On-Chain Mind 2025-01-22). Video ini menambahkan cara ukur baru (line-fit) tapi kesimpulan arah sama — bukan insight baru.
- **Perlu validasi Claude Code:** Tidak (established, sudah dipakai sebagai gate).

### [BARU] MVRV troughs makin tinggi tiap cycle (sisi bawah wedge)
- **Insight:** Selain puncak makin rendah, lembah MVRV (raw ratio) juga makin tinggi tiap cycle berturut-turut — kontraksi dua arah membentuk wedge/converging channel penuh, bukan cuma sisi atas. [00:53]-[01:10]
- **Indikator terkait:** MVRV Ratio
- **Relevan ke:** ZC/Z1 (capitulation zone), K3/K4
- **Test klaim:** Framework belum mengkodifikasi "trough makin tinggi" sebagai sinyal terpisah. Sample n=4 cycle historis (2011/2015/2018/2022) — kecil, tapi arahnya konsisten tanpa exception di data yang tersedia.
- **Perlu validasi Claude Code:** Ya — apakah urutan trough MVRV benar-benar monoton naik antar cycle.

**[VALIDASI — 2026-07-28, CLOSED]** Trough MVRV raw ratio memang naik monoton di 4 cycle bear market yang tersedia (2011=0.40 → 2015=0.57 → 2018=0.70 → 2022=0.76), robust terhadap perubahan window. Verdict SUPPORTED secara deskriptif, tapi n=4 sangat kecil dan cycle berjalan belum punya trough untuk diuji.
Detail: [`findings_mvrv_trough_monotonic.md`](findings_mvrv_trough_monotonic.md)

### [INDIKATOR CUSTOM] Exponential trend-fit line pada peaks & troughs MVRV historis
- **Insight:** Fit garis regresi eksponensial `MVRV = EXP(a + b×date)` terpisah untuk semua puncak MVRV historis dan semua lembah MVRV historis (bukan per-cycle, seluruh sejarah BTC). Klaim: garis trough-fit baru crossing di atas MVRV=1 (fit terakhir 1.005, aktual 1.194 di 7/7/26) → Bitcoin kemungkinan besar tidak dip di bawah realized price cycle ini. Basis "probabilitas": 17 hari (0.29%) sepanjang sejarah MVRV di bawah garis trough-fit, 9 hari (0.15%) di atas garis peak-fit → "99.7%+ chance". Komponen dasar: murni `mvrv_ratio` (turunan `realized_price`/`btc_price`), bukan indikator baru — cuma curve-fit di atas titik ekstrem MVRV. [01:55]-[03:25], [08:31]-[08:50]
- **Indikator terkait:** MVRV Ratio (raw)
- **Relevan ke:** ZC/Z1, K3 exit, K4 entry
- **Test klaim:** Circularity dicurigai kuat — garis di-fit MELALUI titik ekstrem itu sendiri, jadi mayoritas hari historis wajar berada di antara dua garis (properti definisi fit, bukan predictive power independen). n fit cuma ~4-6 titik per sisi — jauh di bawah standar 3-4 cycle framework untuk klaim presisi. Threshold absolut ($53,300, $136K-$272K) eksplisit bertentangan dengan prinsip pola relatif framework.
- **Perlu validasi Claude Code:** Ya — replikasi fit, hitung ulang independen persentase hari, dan leave-one-out test untuk cek circularity/overfitting.

**[VALIDASI — 2026-07-28, CLOSED]** Perhitungan dasar video (persen hari di bawah/atas garis fit) terreplikasi cukup akurat, tapi fit garis trough hanya berbasis n=4 titik (2011/2015/2018/2022) dan leave-one-out test menunjukkan 2 dari 4 run MEMBALIK kesimpulan ("won't dip" jadi "will dip") kalau 1 titik dibuang. Statistik "99.7% chance" bersifat circular (mengukur kedekatan garis ke titik yang membentuknya sendiri), bukan confidence independen — verdict NOT SUPPORTED sebagai basis prediksi kuantitatif.
Detail: [`findings_mvrv_expfit_circularity.md`](findings_mvrv_expfit_circularity.md)

### [KONFLIK] Prediksi absolut "99.7%+ chance tidak dip di bawah RP"
- **Insight:** Klaim video memakai model curve-fit fixed sebagai basis probabilitas presisi (99.7%+) untuk memprediksi apakah harga akan menyentuh realized price cycle ini, direkomendasikan sebagai dasar keputusan ("waiting for $30-40K Bitcoin is incredibly hopeful"). [08:20]-[08:50]
- **Konflik dengan:** Prinsip utama framework — "threshold absolut tidak reliable antar cycle, pakai pola relatif" dan "threshold = panduan arah dari 3-4 siklus, bukan presisi".
- **Alasan konflik:** Framework sengaja menghindari klaim probabilitas presisi dari fixed threshold karena sample antar-cycle kecil. Video ini melakukan persis yang dihindari framework, dan validasi Stage 3 mengonfirmasi klaim ini circular (lihat blok validasi [INDIKATOR CUSTOM] di atas) — bukan cuma soal prinsip, tapi juga cacat metodologis konkret.
- **Rekomendasi:** Diabaikan sebagai basis prediksi presisi. Tidak memenuhi kriteria STOP CLAUDE.md (tidak menyentuh hard constraint LTV, tidak menawarkan framework alternatif ke zone-based/K-node) — claim-tester menilai ini konflik biasa untuk dicatat, bukan STOP-worthy.

### [BARU] Severity dip di bawah RP mengecil tiap cycle karena locked/lost supply
- **Insight:** Argumen mekanistik: makin banyak supply BTC terkunci di harga jauh lebih tinggi (dan lost coins dari era awal) tiap cycle → severity dip di bawah realized price makin kecil tiap cycle → volatility contracting sebagai tanda market "maturing". [07:38]-[08:24]
- **Indikator terkait:** Realized Price
- **Relevan ke:** general, ZC/Z1 (kedalaman capitulation)
- **Test klaim:** Argumen naratif untuk observasi trough MVRV naik (insight di atas) — testable lewat magnitude dip aktual (%) tiap cycle, bukan cuma arah MVRV.
- **Perlu validasi Claude Code:** Ya — cek monotonicity magnitude dip di bawah RP per cycle.

**[VALIDASI — 2026-07-28, CLOSED]** Severity dip di bawah realized price (dalam %) mengecil monoton kalau diukur sebagai trough terdalam per cycle penuh (n=4: 58.8% → 43.2% → 29.8% → 22.3%, COVID 2020 dikeluarkan sbg exogenous shock). Verdict SUPPORTED secara deskriptif dengan n=4 kecil — tapi catatan penting: hasil ini matematis identik dengan insight trough-MVRV-monoton di atas (severity = 1 − MVRV_trough), bukan bukti independen tambahan.
Detail: [`findings_rp_dip_severity.md`](findings_rp_dip_severity.md)

### [KONFIRMASI] Kritik terhadap "MVRV Z-score green zone = buy" sebagai simplistik
- **Insight:** Pembicara mengkritik pendekatan umum "MVRV Z-score green zone = buy" sebagai terlalu simplistik/"obvious", mengklaim pendekatan trend-fit raw MVRV lebih insightful. [00:02]-[00:26]
- **Indikator terkait:** MVRV Z-Score
- **Relevan ke:** general, K2/K4
- **Test klaim:** Framework sendiri sudah tidak pakai MVRV Z-score mentah sebagai gate tunggal — pakai band STH-MVRV relatif (0.80-0.97) + gate/veto multi-kondisi. Kritik video ini align dengan arah desain framework yang sudah ada.
- **Perlu validasi Claude Code:** Tidak — sudah konsisten dengan desain gate+veto K2 yang ada.

### [INDIKATOR CUSTOM] Trend-fit sama diterapkan ke LTH-MVRV/LTH RP — hasil negatif diakui sendiri
- **Insight:** Metode fit sama dicoba pada LTH-MVRV peaks, tapi pembicara mengakui fit jauh lebih lemah/noisy — "very hard to find a way that they actually predict with a great deal of accuracy" — karena LTH RP terdistorsi lost coins era sangat awal (2017 peak juga meleset). [06:34]-[07:37]
- **Indikator terkait:** LTH-MVRV, LTH Realized Price
- **Relevan ke:** K4 (Z1 gate #1: LTH-MVRV <1.0)
- **Test klaim:** Hasil negatif yang dilaporkan jujur oleh sumbernya sendiri — konsisten dengan prinsip CLAUDE.md "hasil negatif = hasil valid". Metodologi dasarnya sama dengan indikator custom trend-fit MVRV di atas (sudah divalidasi circular), jadi tidak perlu diuji ulang.
- **Perlu validasi Claude Code:** Tidak — hasil negatif sudah diakui sumbernya, metodologi dasar sudah dites di validasi trend-fit di atas.

---

## Flag Prioritas

1. **Exponential trend-fit MVRV (klaim "99.7%+")** — insight paling menarik perhatian dari video ini, tapi validasi menunjukkan circularity kuat (leave-one-out membalik kesimpulan di 2/4 skenario). Penting didiskusikan supaya angka $53,300/$136K-$272K ini TIDAK dianggap sebagai target presisi yang bisa diandalkan.
2. **Trough MVRV naik monoton + severity dip mengecil** — dua sisi dari observasi matematis yang sama (n=4 cycle), tapi arahnya konsisten dan bisa jadi confirming context tambahan untuk ekspektasi kedalaman ZC/Z1 di cycle ini (severity capitulation kemungkinan lebih dangkal dari cycle-cycle sebelumnya) — worth didiskusikan apakah layak jadi catatan directional di framework, bukan basis threshold baru.

---

## Yang Langsung Diabaikan

- **LTH Realized Price akan cross $50K "dalam seminggu-dua minggu"** [06:41]-[06:53] — observasi time-bound saat rekaman, sudah basi.
- **Target harga presisi next cycle ($136,273 → $233,000-$272,000)** [09:04]-[10:01] — turunan numerik dari indikator custom trend-fit yang sudah divalidasi circular; angka dari frame juga low-confidence (peak price terbaca beda antar frame dalam video yang sama: $136,273.33 vs pembulatan $136,000).
- **Closing remark "$37,400 on October 6th"** [10:44]-[10:48] — sarkasme retoris ke penonton, bukan klaim substantif.
