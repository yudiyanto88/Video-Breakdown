# Ekstraksi Cara Berpikir — Session Analisis "Fear & Greed Index for Bitcoin"

**Session:** analisis video On-Chain Mind "How to Use the Fear & Greed Index for Bitcoin" (video 2025-02-23, dianalisis 2026-07-17)
**Konteks singkat:** pipeline `/analyze-video` — nonton, ekstrak insight, uji klaim, validasi lawan data historis on-chain, usulkan (bukan terapkan) perubahan ke Decision Framework BTC. Data F&G yang tersedia mulai 2018 → maksimal 2 cycle.

Dokumen ini untuk digabung dengan ekstraksi session lain. Tiap poin ditulis mandiri.

---

## BAGIAN A — Pola yang konsisten (cara berpikir, terlepas dari data spesifik)

### A1. Yang ini penalaran saya sendiri (kandidat ciri lintas-session)

- **Umbrella caveat sample-size dipasang lebih dulu, sekali, di atas segalanya.** Sebelum menilai insight satu per satu, saya identifikasi batas keras data (di sini: F&G baru ada sejak 2018 → n=2 cycle) dan menjadikannya konstrain payung: SEMUA kesimpulan berbasis data itu otomatis low-confidence, tanpa perlu diulang argumennya per-insight. Confidence selalu di-anchor ke sample size relatif terhadap threshold minimum yang dinyatakan (framework ini: minimum 3 cycle).

- **Setiap klaim disortir dulu: deskriptif vs prediktif/falsifiable — hanya yang falsifiable divalidasi ke data.** Klaim yang hanya mendeskripsikan konstruksi sesuatu ("harga sama, sentimen bisa beda") saya tandai tidak-actionable dan tidak saya uji. Klaim yang memprediksi pola berulang ("X mendahului Y") saya uji. Pertanyaan penyaring: "apa yang harus terjadi supaya klaim ini salah?" Kalau tidak ada jawaban konkret, klaim itu bukan kandidat validasi.

- **Saya cek bentuk fungsional PERSIS yang diklaim, bukan sekadar arah umumnya.** Saat klaim berbentuk "menurun di setiap X berikutnya" (monotonic), saya tes apakah datanya benar-benar monotonic — dan menemukan zigzag. Saya menolak mengesahkan versi ketat (monotonic) dan hanya mengesahkan versi longgar (arah besar menurun). Konsekuensinya: pola yang benar arah-besarnya tapi tidak monotonic TIDAK boleh dijadikan syarat formal dengan aturan ketat — dia jadi "context", bukan "signal/trigger".

- **Saya memetakan insight baru ke hierarki yang sudah ada, bukan membiarkannya jadi trigger berdiri sendiri.** Default saya: turunkan status insight yang menjanjikan menjadi "confirming context, never primary" — dibaca HANYA setelah kondisi primary terpenuhi, tidak pernah memveto atau mempercepat aksi. Sinyal formal (punya aturan/threshold/gate) adalah bar yang jauh lebih tinggi dan jarang saya rekomendasikan dari sampel kecil.

- **Sinyal yang verdict-nya berubah tergantung pilihan parameter = red flag, saya buang salah satunya.** Saat dua smoothing window (mis. SMA14 vs SMA30) memberi kesimpulan berlawanan di titik-titik kunci, saya tidak merata-ratakan atau melaporkan keduanya sebagai valid — saya perlakukan ketidakstabilan itu sebagai bukti kerapuhan dan memilih satu, lalu menyatakan yang dibuang secara eksplisit.

- **Saya cek robustness hasil terhadap definisi event/anchor, dan pisahkan artefak dari sinyal nyata.** Sebuah "sinyal" yang muncul hanya karena cara saya mendefinisikan titik acuan (mis. local low minor vs major swing low) saya klasifikasikan sebagai artefak metodologis, bukan temuan. Bila mengganti definisi ke yang lebih masuk akal menghapus sinyal, sinyal itu tidak nyata.

- **Angka agregat yang bisa didorong efek komposisi/alokasi selalu saya dekomposisi.** Saat backtest memberi hasil full-period yang bagus, saya curiga itu berasal dari alokasi lintas-periode (mis. bobot memindahkan budget ke era harga murah), bukan skill dalam-periode. Saya pecah per-cycle untuk mengisolasi efek sebenarnya, dan menilai klaim dari angka per-cycle, bukan angka gabungan.

- **Klaim tanpa metodologi terungkap atau tanpa angka: diuji, atau disingkirkan — tidak pernah diterima atas dasar otoritas.** "Indikator internal" yang komponennya tidak dijelaskan saya tandai non-testable dan kesampingkan (bukan "kemungkinan benar"). Klaim performa tanpa angka ("historically performed well") saya backtest; kalau hasilnya tidak material/tidak konsisten, saya sebut overstated meski sumbernya kredibel.

- **Sinyal saya baca satu-arah bila datanya asimetris.** Ketika kehadiran suatu pola menandai sesuatu tapi ketiadaannya tidak (karena ada preseden yang mencapai kondisi target tanpa pola itu), saya rumuskan eksplisit: "hadir = context pendukung; absen = bukan informasi." Saya tidak memperlakukan absennya sinyal bullish sebagai sinyal bearish, dan sebaliknya.

- **Lag/latensi operasional sinyal saya surface, bukan hanya hit-rate-nya.** Kalau sebuah pola baru bisa dikonfirmasi X hari setelah kejadian (mis. major low baru pasti ±45–60 hari kemudian), saya nyatakan itu sebagai keterbatasan pemakaian — sinyal yang akurat tapi telat punya nilai praktik berbeda dari yang real-time.

- **Koreksi dari user saya perlakukan sebagai hipotesis untuk diuji-ulang dengan data, bukan instruksi untuk di-stempel.** Ketika user mengoreksi definisi acuan analisis, saya jalankan ulang komputasinya dengan acuan baru dan laporkan APA yang berubah pada hasil (termasuk kalau itu menghapus temuan sebelumnya) — bukan sekadar "betul, Anda benar".

- **Saya bedakan temuan yang berdiri di atas validasi closed vs yang lahir dari diskusi, dan tandai asal-usulnya saat mengusulkan ke artefak permanen.** Usulan yang berasal dari brainstorming dengan user (bukan dari validasi data yang tuntas atau dari sumber yang dianalisis) saya beri label eksplisit "berasal dari diskusi, sample lebih kecil" di dalam teksnya, supaya pembaca framework tahu bobot buktinya berbeda.

### A2. Yang ini di-prescribe oleh workflow project (akan muncul di setiap session Content-Breakdown — bukan ciri penalaran murni)

- Struktur pipeline bertahap (watch → extract → categorize → test → verify → write) dan pemakaian sub-agent per tahap — ditetapkan command `/analyze-video`.
- Bucket kategorisasi insight ([BARU]/[KONFIRMASI]/[KONFLIK]/[INDIKATOR CUSTOM]/[STRATEGI]) — ditetapkan CLAUDE.md.
- Aturan "usulkan, jangan terapkan" ke Decision Framework, dan gate finalisasi (tidak update index lintas-video sampai user bilang final) — ditetapkan CLAUDE.md/command.
- Prinsip "jangan setuju karena nama besar" dan flag threshold absolut vs pola relatif — dinyatakan CLAUDE.md (walau eksekusi penyaringannya saya lakukan, lihat A1).

> Catatan untuk proses merge: kalau session lain BUKAN dari project ini dan pola A1 tetap muncul, itu memperkuat bahwa A1 adalah ciri penalaran, bukan sekadar patuh scaffold. Kalau pola A2 muncul di project lain, kemungkinan itu kebetulan konvergen atau memang scaffold serupa.

---

## BAGIAN B — Keputusan spesifik ke session ini (mungkin berubah di kondisi/topik lain)

- **Pemetaan "F&G hidup di mana di framework".** Saya tetapkan F&G Index hanya relevan di satu tempat (staging deploy K5) karena di situlah framework aktual menaruhnya. Sebagian besar isi video jadi bersifat konfirmasi desain yang sudah ada. Pemetaan ini spesifik ke indikator F&G + framework K-node ini; indikator lain punya titik-sentuh berbeda.

- **Pilihan SMA30 (bukan SMA14) sebagai window yang dipertahankan.** Diputuskan dalam session ini berdasarkan (a) SMA14 flip verdict di titik kunci pada data ini, dan (b) preferensi user. Bukan aturan universal — hanya hasil untuk metrik + data ini.

- **Verdict spesifik hasil validasi (kemungkinan berubah bila data cycle bertambah):**
  - F&G SMA30 memuncak ~10 bulan sebelum price top di 2/2 cycle; top final terbentuk dengan sentimen sudah dingin → layak jadi confirming context K1/K3.
  - SMA30 sebagai TRIGGER K5 ditolak (miss 3 dari 5 deploy event historis, lag 15–32 hari) → raw daily F&G dipertahankan.
  - Sentiment-weighted DCA: outperformance +4.3% (cycle lama) dan +0.3% (cycle baru) → tidak material/tidak konsisten, klaim video overstated.
  - Bottom divergence F&G SMA30: 1 hit (2022), 1 absent (2018), 0 false positive → confirming context K4 satu-arah.
  Semua verdict ini berlabel n=2 dan bisa berubah bila cycle berikutnya berbeda.

- **Evaluasi retrospektif market-call yang terikat waktu.** Market call video (Feb 2025) bisa dinilai retrospektif justru karena ~17 bulan sudah berlalu saat analisis. Ini keputusan yang hanya berlaku untuk klaim time-bound yang sudah cukup tua untuk dilihat hasilnya; klaim serupa yang masih baru tidak bisa diperlakukan sama.

- **Status "belum bisa dinilai" untuk kondisi market yang masih berjalan.** Bear 2025-26 masih berlangsung saat analisis → divergence-nya saya tandai "belum bisa dinilai" dan tidak dihitung sebagai hit/miss. Ini murni artefak titik-waktu session; di masa depan status ini akan berubah.

- **Keputusan out-of-sample dimungkinkan oleh rentang data saat itu.** Klaim video (dibuat 2021-centric) bisa diuji out-of-sample terhadap cycle 2024-2025 karena data sudah memanjang sampai 2026 pada saat analisis. Ketersediaan window out-of-sample ini spesifik ke kapan session dijalankan.

- **Parameter backtest yang saya pilih ad hoc untuk menguji klaim tak-berangka.** Skema bobot DCA (2x/1.5x/1x/0.5x per bucket F&G) dan rekonstruksi window K5 (STH RP cross RP → tutup 3 hari di atas AVIV Upper) adalah operasionalisasi yang saya karang agar klaim kualitatif video bisa diangkakan. Pilihan spesifiknya kontekstual; prinsip di baliknya (operasionalkan klaim vague jadi sesuatu yang bisa dites) ada di A1.
