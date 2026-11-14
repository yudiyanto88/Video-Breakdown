# CLAUDE.md — On-Chain Content Intelligence
## Briefing untuk setiap sesi analisis konten (video, tweet, foto chart)

---

## TUGAS KAMU

Bedah konten analisis on-chain dari sumber luar, lalu ekstrak dan evaluasi insight-nya secara kritis. Tujuannya bukan bikin ringkasan — tapi cari tahu apakah ada sesuatu yang berguna, konflik, atau bisa memperkuat framework investasi yang sudah ada.

Dua jenis input, satu standar analisis yang sama:
- **Video** — channel On-Chain Mind, Tristan Colt (ChartInspect), Joao Wedson (Alphractal), atau lainnya
- **Tweet & foto chart** — post berisi analisis + gambar chart, atau beberapa foto chart saja yang dilampirkan Yudi di chat

Output disimpan sebagai folder self-contained di `Outputs/` — satu folder per sumber, berisi sumber asli + seluruh hasil analisisnya (lihat "FORMAT OUTPUT" di bawah).

**Cara jalanin:**
- `/analyze-video <url-video>` untuk video
- `/analyze-post` untuk tweet/foto (gambar dilampirkan di chat)
- **Routing otomatis:** kalau Yudi paste foto chart / screenshot tweet + minta analisis TANPA mengetik command → langsung jalankan alur `/analyze-post`. Kalau kasih URL video → alur `/analyze-video`.

Kedua command menjalankan alur yang sama (baca sumber → ekstrak → kategorikan → test klaim → validasi data ke Onchain-Dashboard → tulis output) lewat 3 sub-agent (`insight-extractor`, `claim-tester`, `data-verifier`) supaya tiap tahap fokus. Command cuma mengeksekusi aturan di file ini secara bertahap — bukan aturan terpisah. Kalau nganalisis manual tanpa command, tetap ikuti Step 1-3 di bawah.

---

## FRAMEWORK YANG DIPAKAI

Detail lengkap ada di `D:\Claude Code\Projects\Onchain-Dashboard\references\Decision_Framework v2.md`. Baca file itu dulu sebelum mulai analisis apapun.

Ringkasan cepat untuk referensi saat evaluasi:

- **Indikator aktif:** MVRV (Ratio, LTH, STH), aSOPR, LTH-SOPR, STH-SOPR (MA90 & MA60), Supply in Profit/Loss (total, STH, LTH), Realized Price family (RP, STH RP, LTH RP, AVIV Mean, AVIV Upper, CVDD), RHODL Ratio
- **Prinsip utama:** Threshold absolut tidak reliable antar cycle — framework pakai pola relatif. STH metrics selalu confirming, bukan primary. Hard LTV limits tidak bisa di-override sinyal apapun. Short hanya sebagai hedge.

---

## SEBELUM MULAI

Baca `D:\Claude Code\Projects\Onchain-Dashboard\references\Decision_Framework v2.md`. File itu berisi zone structure (Z1-Z5) dan semua K-node (K1-K6) secara lengkap. Kamu perlu paham isinya sebelum bisa evaluate apakah insight dari sumber manapun konflik atau memperkuat framework.

Kalau sumbernya membahas mekanik atau interpretasi indikator tertentu secara mendalam dan Decision Framework tidak cukup untuk evaluasi, baca KB yang relevan — semua dari `D:\Claude Code\Projects\Onchain-Dashboard\references\`. Jangan baca semua sekaligus — hanya yang dibutuhkan.

| File (di `D:\Claude Code\Projects\Onchain-Dashboard\references\`) | Isi |
|------|-----|
| `mvrv_Knowledge_Base v1.4.md` | MVRV Ratio, LTH-MVRV, STH-MVRV, MVRV Z-Score |
| `sopr_knowledge_base v1.4.md` | aSOPR, LTH-SOPR, STH-SOPR, MA gap signals |
| `nupl_knowledge_base v1.4.md` | NUPL, LTH-NUPL, STH-NUPL |
| `supply_in_profit_loss_knowledge_base v1.4.md` | Supply in Profit/Loss, STH/LTH profit % |
| `Price_Level_knowledge_base v1.4.md` | STH/LTH Realized Price, AVIV Mean/Upper, CVDD |

### Sumber data validasi

Kalau perlu validasi klaim lawan data historis, pakai:
- Data utama: `D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv` (105 kolom, gabungan semua metrik — biasanya cukup ini saja)
- Peta kolom: `D:\Claude Code\Projects\Onchain-Dashboard\references\data_dictionary.md` — baca dulu sebelum nulis script, supaya tahu kolom yang benar
- Pola script existing: `D:\Claude Code\Projects\Onchain-Dashboard\research\analyze_k3_stage_comparison.py` — ikuti gaya ini untuk definisi zona/AVIV, jangan hitung ulang formula sendiri

---

## CARA ANALISIS

### Step 1 — Baca sumber dan catat

**Untuk video:** nonton sampai selesai lewat skill `watch` (menghasilkan transcript + frame). Kalau `watch` gagal (video private, region-lock, atau sebab lain), STOP dan lapor ke Yudi — jangan lanjut dengan transcript kosong atau coba tebak isi video.

**Untuk tweet/foto chart:** baca teks post (kalau ada) dan setiap gambar dengan teliti. Simpan salinan setiap gambar ke folder output (`gambar_1.png`, `gambar_2.png`, ...) lalu tulis `source.md` — analog `transcript.md` — berisi header sumber + teks post verbatim + deskripsi terstruktur per gambar (metrik, platform chart, timeframe, anotasi pembuat, angka terbaca, apa yang ditunjukkan). Detail format di `.claude/commands/analyze-post.md`. STOP rule yang sama berlaku: gambar blur / chart tidak bisa diidentifikasi dengan yakin → STOP dan lapor, jangan menebak. Input foto-saja tanpa klaim: insight diekstrak dari apa yang ditunjukkan chart-nya sendiri (pola yang digambar, sinyal yang di-highlight anotasi).

Fokus pada:
- Indikator apa yang dibahas/ditampilkan
- Klaim atau kesimpulan apa yang dibuat pembicara/pembuat post
- Angka atau threshold spesifik yang disebut
- Apakah ada framework atau strategi yang mereka paparkan

### Step 2 — Kategorikan setiap insight

Untuk setiap insight substantif, masukkan ke salah satu bucket:

| Bucket | Artinya |
|--------|---------|
| **[BARU]** | Cara baca atau interpretasi yang belum ada di framework |
| **[KONFIRMASI]** | Mendukung sesuatu yang sudah ada |
| **[KONFLIK]** | Bertentangan dengan keputusan yang sudah dikunci |
| **[INDIKATOR CUSTOM]** | Indikator atau metric buatan channel ini sendiri |
| **[STRATEGI]** | Framework atau pendekatan investasi dari pembicara |

### Step 3 — Test setiap klaim

Sebelum label sesuatu sebagai [BARU] atau [KONFIRMASI], tanya dulu:
- Berapa cycle yang jadi dasar klaim ini? Kalau kurang dari 3, flag sebagai low-confidence
- Apakah ini threshold absolut? Kalau iya, flag bahwa framework sudah pakai pendekatan pola relatif, bukan angka tetap
- Kalau ini indikator custom — komponen dasarnya apa? Apakah kombinasi dari yang sudah ada?
- Apa yang perlu terjadi supaya klaim ini salah?

---

## FORMAT OUTPUT

Struktur `Outputs/`:

```
Outputs/
  source_index.md    ← index gabungan semua sumber
  videos/            ← satu folder per video
  posts/             ← satu folder per tweet/foto
```

Satu folder per sumber, **self-contained**: sumber asli + seluruh hasil analisis di satu tempat, tidak tergantung chat history.

**Video** — `Outputs/videos/YYYY-MM-DD_[judul-video-lengkap-kebab-case]/` (tanggal video, bukan tanggal analisis). Slug HARUS merepresentasikan judul video secara utuh (kebab-case, lowercase, tanpa tanda baca) — jangan dipersingkat atau dipotong ke beberapa kata kunci saja, meskipun judulnya panjang atau ada boilerplate seperti "How to Use X for Bitcoin".

Contoh: judul video "How to Use the Fear & Greed Index for Bitcoin" → `Outputs/videos/2025-02-23_how-to-use-the-fear-greed-index-for-bitcoin/`
Contoh: judul video "LTH-SOPR Update: What It Means Right Now" → `Outputs/videos/2026-07-06_lth-sopr-update-what-it-means-right-now/`

Isi folder video:
- `analysis.md` — analisis utama (template di bawah). Nama file SELALU `analysis.md`, bukan mengulang judul
- `transcript.md` — transkrip mentah video (sumber asli, disimpan supaya tidak perlu nonton ulang kalau video kelak dihapus/private). Wajib punya header: judul, channel, URL, tanggal video
- `findings_[topik].md` — satu file per insight yang divalidasi dengan data (Claude Code), dibuat saat validasi selesai. Contoh: `findings_mvrv_rolling1y_vs_aviv.md`
- `analyze_<topik>.py` — script throwaway yang dipakai untuk validasi (satu per topik yang diuji)
- `events_<topik>.csv` — CSV pendukung kalau validasi menghasilkan tabel event

**Tweet/foto** — `Outputs/posts/YYYY-MM-DD_[topik-kebab-case]/` (tanggal post; kalau tidak diketahui → tanggal analisis + catatan di `source.md`).

Isi folder post:
- `gambar_1.png`, `gambar_2.png`, ... — salinan SEMUA gambar sumber (wajib, supaya folder self-contained)
- `source.md` — pengganti `transcript.md`: header sumber (akun, URL, tanggal post, jenis input) + teks post verbatim + deskripsi terstruktur per gambar
- `analysis.md`, `findings_[topik].md`, `analyze_<topik>.py`, `events_<topik>.csv` — sama seperti folder video

Folder video lama yang pakai konvensi penamaan berbeda tidak perlu di-rename.

`Outputs/source_index.md` — index lintas-sumber, mencakup video maupun post (di root `Outputs/`, di luar folder manapun). Cek dulu sebelum label insight sebagai [BARU] — kalau sudah pernah dibahas sumber lain, sebutkan itu.

**Kapan update `source_index.md`:** BUKAN otomatis tiap kali `analysis.md` ditulis. Analisis biasanya masih didiskusikan/direvisi dulu bareng Yudi sebelum final. Update index cuma sekali, di akhir, setelah Yudi konfirmasi analisisnya sudah final — supaya tidak bolak-balik update untuk hal yang belum settle.

**Cap validasi:** maksimal 3-5 validasi high-value per sumber — prioritaskan insight yang paling menyentuh K-node aktif saat ini. Sisanya dicatat sebagai backlog: "Perlu validasi Claude Code: Ya — belum diuji, backlog". Validasi tambahan yang lahir dari diskusi lanjutan dengan Yudi (bukan dari batch awal) tidak kena cap ini.

**Backlog index:** di awal sesi analisis, cek folder mana di `Outputs/videos/` dan `Outputs/posts/` yang belum masuk `source_index.md` dan sebutkan ke Yudi sebagai backlog yang menunggu konfirmasi final.

---

### Template isi `analysis.md`:

*Catatan: template di bawah pakai header metadata versi video. Untuk post/foto, ganti 4 baris metadata jadi: Sumber/Akun, Tanggal post, Tanggal analisis, URL (format di `.claude/commands/analyze-post.md`) — dan referensi timestamp `[mm:ss]` diganti "Gambar N". Bagian lain identik.*

```markdown
# [Judul Video]
**Channel:** [nama channel]
**Tanggal video:** [tanggal upload]
**Tanggal analisis:** [tanggal hari ini]
**Link:** [URL video]

[Opsional — hanya kalau ada flag dari "KAPAN HARUS STOP DAN LAPOR": tampilkan di sini,
di paling atas, sebelum bagian lain. Kosongkan section ini kalau tidak ada flag.]

---

## Ringkasan

[Proporsional dengan isi video. Video pendek dan focused = beberapa kalimat.
Video panjang dengan banyak topik = beberapa paragraf. Tidak ada batas minimum
atau maksimum — sesuaikan dengan seberapa banyak yang perlu dijelaskan supaya
orang yang belum nonton bisa paham konteksnya.]

---

## Insight Inventory

Field di bawah dipakai untuk bucket [BARU], [KONFIRMASI], [INDIKATOR CUSTOM], dan
[STRATEGI] — semuanya sama. Sertakan timestamp `[mm:ss]` di insight kalau tersedia
dari transcript. [KONFLIK] pakai field sendiri (lihat di bawah).

### [BARU] [Judul singkat insight]
- **Insight:** [Deskripsi jelas, timestamp `[mm:ss]` kalau ada]
- **Indikator terkait:** [nama indikator]
- **Relevan ke:** [K-node atau zone mana, atau "general"]
- **Test klaim:** [Apa yang bisa salah dari interpretasi ini? Sample size-nya?]
- **Perlu validasi Claude Code:** [Ya / Tidak — kalau ya, sebutkan pertanyaan spesifiknya]

[Kalau insight ini sudah divalidasi Stage 3 (data-verifier), tempel blok ini persis
di bawah field di atas:]

**[VALIDASI — <tanggal>, CLOSED]** [Verdict 2-4 kalimat, sebut n & sebaran per cycle.]
Detail: [`findings_<topik>.md`](findings_<topik>.md)

### [KONFIRMASI] [Judul singkat insight]
- **Insight:** [Deskripsi jelas]
- **Indikator terkait:** [nama indikator]
- **Relevan ke:** [K-node atau zone mana, atau "general"]
- **Test klaim:** [Apa yang bisa salah dari interpretasi ini? Sample size-nya?]
- **Perlu validasi Claude Code:** [Ya / Tidak — kalau ya, sebutkan pertanyaan spesifiknya]

### [INDIKATOR CUSTOM] [Judul singkat insight]
- **Insight:** [Deskripsi jelas, sebutkan komponen dasarnya kalau bisa didekomposisi]
- **Indikator terkait:** [nama indikator]
- **Relevan ke:** [K-node atau zone mana, atau "general"]
- **Test klaim:** [Apa yang bisa salah dari interpretasi ini? Sample size-nya?]
- **Perlu validasi Claude Code:** [Ya / Tidak — kalau ya, sebutkan pertanyaan spesifiknya]

### [STRATEGI] [Judul singkat insight]
- **Insight:** [Deskripsi jelas]
- **Indikator terkait:** [nama indikator]
- **Relevan ke:** [K-node atau zone mana, atau "general"]
- **Test klaim:** [Apa yang bisa salah dari interpretasi ini? Sample size-nya?]
- **Perlu validasi Claude Code:** [Ya / Tidak — kalau ya, sebutkan pertanyaan spesifiknya]

### [KONFLIK] [Judul singkat insight]
- **Insight:** [Deskripsi jelas]
- **Konflik dengan:** [Keputusan mana di framework yang bertentangan]
- **Alasan konflik:** [Kenapa bertentangan]
- **Rekomendasi:** [Abaikan / Diskusikan lebih lanjut dengan Yudi]

[dst. untuk setiap insight — tidak ada batas jumlah]

---

## Flag Prioritas

Semua insight yang worth didiskusikan lebih dalam bareng Yudi (langsung di chat ini,
bukan pindah tool), diurutkan dari yang paling penting. Kalau videonya kaya insight,
flag semuanya. Kalau videonya tipis, mungkin tidak ada yang perlu di-flag sama sekali.

1. [Judul] — [Alasan singkat kenapa penting]
2. [Judul] — [Alasan singkat kenapa penting]
[dst.]

---

## Yang Langsung Diabaikan

[Insight yang tidak relevan untuk framework, dengan alasan singkat per item.
Kalau semua insight relevan, bagian ini bisa dikosongkan.]
```

---

## ATURAN TAMBAHAN

**Soal threshold absolut:** Kalau pembicara sebut angka spesifik (misal "MVRV di atas 3.5 = jual"), catat nilainya tapi tambahkan note bahwa framework sudah pakai pendekatan pola relatif, bukan angka tetap. Jangan rekomendasikan ganti pendekatan tanpa alasan struktural yang kuat.

**Soal indikator custom:** Identifikasi komponen dasarnya. Fear & Greed Cadence misalnya — itu pada dasarnya kombinasi apa? Kalau bisa didekomposisi ke indikator yang sudah ada di framework, catat itu.

**Soal sample size:** Kalau klaim didasarkan dari 1-2 cycle saja, flag eksplisit sebagai low-confidence. Framework ini sendiri sadar bahwa 3-4 cycle = sample kecil — lebih kecil dari itu tidak bisa jadi dasar keputusan.

**Jangan setuju karena nama besar.** On-Chain Mind, Tristan Colt, Joao Wedson, atau channel besar manapun adalah sumber yang bagus, tapi test tetap dilakukan. Cari titik lemah dari setiap klaim sebelum label sebagai valid.

**Bahasa output:** Bahasa Indonesia untuk narasi dan evaluasi. Technical terms tetap English (MVRV, SOPR, LTV, capitulation, dll).

**Insight dari diskusi dengan Yudi:** insight yang muncul dari diskusi (bukan langsung dari sumbernya) tetap boleh masuk `analysis.md` dan `source_index.md` — tandai eksplisit dengan anotasi "dari diskusi, bukan video/post".

**Angka dari frame video / foto chart:** angka yang dibaca dari frame video maupun gambar chart (tooltip, sumbu, label) dilabel "low confidence dari resolusi frame/gambar" dan jangan dipakai sebagai anchor untuk kesimpulan.

---

## STANDAR VALIDASI

Wajib dipegang setiap kali menguji klaim lawan data historis (data-verifier, atau siapapun yang nulis script validasi di pipeline ini):

1. **Definisi event eksplisit** sebelum menghitung: apa yang dihitung sebagai satu kejadian, window ground-truth berapa hari, aturan merge/cooldown antar kejadian berdekatan
2. **Laporkan `n` selalu** — total & sebaran per cycle. n kecil bukan alasan berhenti, tapi wajib disebut tebal di kesimpulan
3. **Anti lookahead bias** — nilai yang dipakai untuk "keputusan" harus tersedia di tanggal keputusan (at-gate), bukan diambil dari masa depan window
4. **Independensi sample** — event dari cycle yang sama berkorelasi, sebut kalau hasil didominasi satu cycle
5. **Data yang mulai belakangan** (Fear&Greed 2018+, funding rate/OI 2020+) — sebut eksplisit kalau uji lintas-cycle tidak penuh mungkin
6. **Jangan overfit threshold** — kalau coba >3-4 varian dan cuma satu "berhasil", itu overfitting, laporkan sebagai negatif

Dua aturan tambahan yang berlaku di semua validasi:
- **Hasil negatif = hasil valid.** Jangan "menyelamatkan" klaim dengan mengubah definisi event sampai hasilnya bagus.
- **Bahasa probabilistik** — "cenderung", bukan "pasti".

---

## KAPAN HARUS STOP DAN LAPOR

Kalau ketemu salah satu dari ini, catat sebagai flag khusus di bagian atas file output:

- Insight yang secara langsung bertentangan dengan hard constraint LTV
- Framework atau strategi dari pembicara yang secara fundamental berbeda dengan pendekatan zone-based + K-node yang sudah ada

Flag ini ditampilkan langsung ke Yudi di chat (jangan tunggu sampai akhir pipeline) sebelum diputuskan apakah framework perlu direvisi — bukan dibawa ke tool lain.

Penempelan insight tervalidasi ke Decision Framework dikerjakan di project Onchain-Dashboard — bukan bagian pipeline ini.

---

## DEFINITION OF DONE

Analisis dianggap selesai kalau:

- Sumber tersimpan lengkap: video → `transcript.md` dengan header (judul, channel, URL, tanggal video); post → salinan `gambar_*.png` + `source.md` dengan header (akun, URL, tanggal post, jenis input)
- Semua insight substantif masuk bucket dengan field "Test klaim" terisi
- Tiap validasi yang selesai punya blok `[VALIDASI]` inline + file `findings_<topik>.md`
- Semua script validasi jalan tanpa error, dan angka di `analysis.md` cocok dengan `findings_<topik>.md`
- `n` + sebaran per cycle disebut di tiap verdict validasi
- Nama folder = tanggal sumber + slug LENGKAP (bukan dipotong/disingkat), di subfolder yang benar (`videos/` atau `posts/`)
- `source_index.md` BELUM diupdate

Tutup respons dengan pengingat: **"source_index.md belum diupdate — bilang kalau analisis ini sudah final."**
