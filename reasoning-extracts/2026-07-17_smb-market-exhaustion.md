# Ekstraksi Cara Berpikir — Session Analisis Video On-Chain

**Session:** 2026-07-17, analisis video "This New Bitcoin Chart Shows Market Exhaustion" (Joao Wedson / Alphractal) via pipeline `/analyze-video`.
**Catatan:** Bagian A = pola yang saya yakini konsisten lintas data. Bagian B = keputusan yang spesifik ke kondisi/topik session ini. Tiap poin ditulis mandiri untuk digabung dengan ekstraksi session lain.

---

## A. Pola konsisten (independen dari data spesifik)

### A1. Kategorikan dulu, uji belakangan — jangan digabung
Bucket insight ([BARU]/[KONFIRMASI]/[KONFLIK]/[INDIKATOR CUSTOM]/[STRATEGI]) ditetapkan lebih dulu sebagai deskripsi, baru setelah itu klaim diuji kritis. Label "[BARU]" atau "[KONFIRMASI]" tidak pernah dipasang sebelum uji falsifiability + sample size dijalankan. Pemisahan ini dijaga secara struktural dengan menaruh ekstraksi dan pengujian di sub-agent berbeda supaya satu tahap tidak "bocor" bias ke tahap lain.

### A2. Falsifiability adalah filter primer
Pertanyaan yang selalu diajukan ke tiap klaim: "apa yang perlu terjadi supaya klaim ini SALAH?" Klaim yang tidak bisa dibuat salah diperlakukan sebagai titik lemah paling serius, bukan sebagai kekuatan. Contoh prinsip yang saya pegang: sebuah sinyal yang mencocoki semua kemungkinan hasil (mis. "ini menandai cycle top ATAU local top" — dan setiap high pasti salah satunya) bukan sinyal — tidak memberi informasi. Klaim seperti ini ditolak untuk validasi data karena tidak ada yang bisa diuji.

### A3. Sample size < 3 siklus = low confidence, di-flag eksplisit
Kalau dasar klaim kurang dari 3 siklus, saya tandai low-confidence secara eksplisit, bukan diam-diam mendiskon. Bahkan 3-4 siklus tetap dianggap sample kecil. Kalau pembicara sendiri menyebut datanya inkonsisten (mis. "kadang 2x, kadang 1x") lalu tetap menariknya jadi ekspektasi forward-looking, inkonsistensi yang diakui itu justru jadi bukti kuat untuk verdict low-confidence/negatif.

### A4. Indikator black-box → validasi lewat proxy transparan, dan nyatakan batasannya
Kalau indikator proprietary tidak bisa direplikasi (formula tertutup), saya tidak menyerah tapi juga tidak menerima klaimnya mentah. Saya cari proxy dari metrik transparan yang sudah tersedia, jalankan uji di proxy itu, lalu nyatakan tegas bahwa hasilnya berlaku untuk proxy — bukan untuk indikator aslinya. Verdict negatif via proxy dibingkai sebagai "pola tidak transfer ke metrik kita", bukan "indikator aslinya terbukti salah".

### A5. Sebelum melabeli sesuatu [BARU], cek apakah framework sudah mengkodifikasinya
Mayoritas "insight custom" runtuh jadi mekanik yang sudah ada begitu didekomposisi ke komponen dasar (mis. "cost basis on-chain" ≈ Realized Price family; "support band bawah" ≈ zona bawah existing; "midline sebagai support" ≈ mekanik bounce yang sudah divalidasi). Dekomposisi ke komponen dasar dilakukan dulu; label [BARU] hanya bertahan kalau tidak ada padanan fungsional.

### A6. Bedakan mekanisme, jangan berhenti di kesamaan permukaan
Ketika sebuah klaim tampak "mengonfirmasi" sesuatu yang sudah ada, saya cek apakah mekanismenya benar-benar sama. Contoh: "momentum melemah" bisa diukur lewat magnitude (nilai indikator lebih rendah tiap puncak) ATAU lewat frekuensi (seberapa sering harga menyentuh zona). Dua-duanya "diminishing" tapi mekaniknya beda — dan yang satu bisa ternyata benar sementara yang lain salah. Kesamaan arah narasi tidak cukup untuk menyimpulkan kesamaan sinyal.

### A7. Sinyal baru harus menambah lead time, bukan sekadar cocok secara retrospektif
Untuk sinyal timing, saya uji apakah ia bisa terdeteksi LEBIH AWAL dari trigger yang sudah dipakai. Kalau secara struktural sinyal baru hanya bisa dikonfirmasi pada atau setelah trigger existing berbunyi (mis. "durasi episode baru diketahui saat episode berakhir"), ia tidak menambah nilai berapa pun bagus korelasi retrospektifnya. Sinyal yang hanya terbaca setelah kejadian ditandai "tidak actionable".

### A8. Pre-register definisi event sebelum melihat hasil
Sebelum menghitung, definisi "event" (apa yang dihitung sebagai satu test/episode/sentuhan, aturan merge, window) ditetapkan lebih dulu. Ini mencegah definisi digeser agar cocok dengan hasil yang diinginkan (hindsight fitting). Kalau perlu, jalankan lebih dari satu varian definisi (mis. proxy ketat + proxy longgar) dan laporkan keduanya.

### A9. Verdict negatif tetap actionable
Hasil "NOT SUPPORTED" tidak dibuang sebagai nihil. Justru sering paling berguna: menjadi jawaban berbasis data untuk menolak narasi yang sedang beredar, atau menolak modifikasi framework yang kelihatan menggoda. Nilai temuan diukur dari apakah ia mengubah keputusan, bukan dari apakah ia positif.

### A10. Jangan tunduk pada otoritas atau hype
Kredensial pembicara (gelar, jabatan) dan bahasa hype ("magical", "very powerful") dibuang eksplisit sebagai non-evidence. Sumber yang bagus tetap diuji; nama besar tidak menggeser beban pembuktian.

### A11. Threshold absolut dicatat nilainya, tapi tidak diadopsi sebagai aturan
Kalau pembicara menyebut angka tetap, nilainya dicatat tapi disertai catatan bahwa pendekatan yang dipakai adalah pola relatif antar-siklus, bukan angka tetap — karena threshold absolut tidak reliable antar siklus. Adopsi angka tetap butuh alasan struktural kuat.

### A12. Deteksi cherry-picked timeframe
Klaim "level ini selalu bertahan / tidak pernah ditembus" diuji dengan memperpanjang window ke luar rentang yang dipilih pembicara. Kalau klaim hanya benar di window terpilih dan runtuh saat window diperluas, itu ditandai cherry-picked.

### A13. Kebersihan transkrip: flag kemungkinan mis-caption sebelum menguji kata
Kalau auto-caption menghasilkan istilah yang janggal secara domain (mis. sebuah kata teknis yang tidak masuk akal di konteksnya), saya flag sebagai kemungkinan salah transkrip dan tidak membangun/menguji klaim di atas kata mentah itu. Verifikasi visual (frame) dipakai untuk melengkapi transkrip yang meragukan.

### A14. Proposal ≠ adopsi — gating dijaga ketat
Output analisis diperlakukan sebagai usulan, bukan perubahan. Framework/keputusan yang sudah dikunci tidak pernah diedit dari pipeline ini. Index lintas-item tidak diupdate otomatis saat analisis ditulis — hanya setelah ada sinyal konfirmasi eksplisit bahwa analisis sudah final — supaya tidak bolak-balik mengubah sesuatu yang masih bisa direvisi.

### A15. Alokasikan slot validasi yang mahal ke klaim paling bernilai
Ketika kapasitas validasi terbatas (mis. maksimal 3), slot diberikan ke klaim yang (a) forward-looking, (b) genuinely baru, dan (c) menyentuh titik keputusan aktif. Klaim yang sudah established atau tidak testable tidak menghabiskan slot, walau kelihatan menarik.

### A16. Flag konflik struktural langsung, jangan tunggu akhir pipeline
Kalau ada klaim yang bertentangan dengan hard constraint atau berbeda fundamental dari pendekatan yang dipakai, itu diangkat ke permukaan segera dan terpisah — bukan dibenamkan di ringkasan akhir. Membedakan "beda implementasi tapi sefilosofi" (bukan konflik) dari "beda fundamental" (konflik) dilakukan eksplisit.

---

## B. Keputusan spesifik ke session ini

### B1. Identifikasi channel sebagai pihak ketiga
Video ini dari Joao Wedson / Alphractal, bukan dua channel acuan utama. Diperlakukan sebagai sumber "lainnya" — tidak mengubah kedalaman uji, tapi relevan dicatat karena bukan sumber yang biasa dibedah.

### B2. Hampir semua insight jatuh ke bucket [INDIKATOR CUSTOM]
Ini akibat sifat video: seluruh durasi membahas SATU indikator proprietary. Dominasi satu bucket adalah properti video ini, bukan pola umum — video lain dengan banyak topik akan tersebar ke banyak bucket.

### B3. Pemilihan proxy spesifik untuk indikator black-box
Untuk zona resistance dipakai proxy AVIV Upper (+0.5 SD, formula established); untuk lower support band dipakai dua proxy — zona bawah framework + rasio harga/CVDD < 1.15. Pilihan proxy ini didorong oleh komponen yang disebut indikator aslinya (cost basis on-chain), bukan default universal.

### B4. Snapshot kondisi market Juli 2026 dipakai untuk membantah framing video
Menurut proxy framework, bear yang sedang berjalan tercatat NOL test (zona bawah belum pernah aktif; STH Realized Price masih jauh di atas Realized Price). Ini bertentangan langsung dengan framing video "sudah test sekali, tunggu test kedua". Kesimpulan ini terikat ke kondisi harga/metrik pada tanggal analisis dan akan berubah seiring market bergerak.

### B5. Nilai band dari tooltip resolusi rendah → low confidence, tidak dijadikan anchor
Angka band yang terbaca dari frame video (resolusi rendah) sengaja tidak dipakai sebagai titik banding kuantitatif, hanya sebagai orientasi kasar. Keputusan ini spesifik karena satu-satunya sumber angka adalah screenshot, bukan data.

### B6. Desain simulasi K4 untuk menguji klaim "double test"
Untuk menguji apakah menahan tranche DCA menunggu "test kedua" menguntungkan, dibuat simulasi spesifik (4 tranche × 25%, exit di sinyal pemulihan) dan dibandingkan dua strategi. Desain ini dibuat khusus untuk klaim ini; parameternya bukan template umum.

### B7. Dua dari tiga slot validasi dipakai
Diputuskan tidak ada insight ketiga yang layak slot — sisanya sudah established atau tidak falsifiable. Rasio ini spesifik ke isi video, bukan aturan.
