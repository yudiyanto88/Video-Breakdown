# CLAUDE.md — On-Chain Video Intelligence
## Briefing untuk setiap sesi analisis video

---

## TUGAS KAMU

Nonton video dari channel On-Chain Mind atau Tristan Colt (ChartInspect), lalu ekstrak dan evaluasi insight-nya secara kritis. Tujuannya bukan bikin ringkasan — tapi cari tahu apakah ada sesuatu yang berguna, konflik, atau bisa memperkuat framework investasi yang sudah ada.

Output disimpan sebagai folder di `Outputs/`, satu folder per video (lihat "FORMAT OUTPUT" di bawah).

**Cara jalanin:** pakai `/analyze-video <url-video>` — otomatis menjalankan seluruh alur di bawah (nonton → ekstrak → kategorikan → test klaim → validasi data ke Onchain-Dashboard → tulis output), lewat 3 sub-agent (`insight-extractor`, `claim-tester`, `data-verifier`) supaya tiap tahap fokus. Command ini cuma mengeksekusi aturan di file ini secara bertahap — bukan aturan terpisah. Kalau nganalisis manual tanpa command, tetap ikuti Step 1-3 di bawah.

---

## FRAMEWORK YANG DIPAKAI

Detail lengkap ada di `D:\Claude Code\Projects\Onchain-Dashboard\references\Decision_Framework v1.md`. Baca file itu dulu sebelum mulai analisis video apapun.

Ringkasan cepat untuk referensi saat evaluasi:

- **Indikator aktif:** MVRV (Ratio, LTH, STH), aSOPR, LTH-SOPR, STH-SOPR (MA90 & MA60), Supply in Profit/Loss (total, STH, LTH), Realized Price family (RP, STH RP, LTH RP, AVIV Mean, AVIV Upper, CVDD), RHODL Ratio
- **Prinsip utama:** Threshold absolut tidak reliable antar cycle — framework pakai pola relatif. STH metrics selalu confirming, bukan primary. Hard LTV limits tidak bisa di-override sinyal apapun. Short hanya sebagai hedge.

---

## SEBELUM MULAI

Baca `D:\Claude Code\Projects\Onchain-Dashboard\references\Decision_Framework v1.md`. File itu berisi zone structure (Z1-Z5) dan semua K-node (K1-K6) secara lengkap. Kamu perlu paham isinya sebelum bisa evaluate apakah insight dari video konflik atau memperkuat framework.

Kalau video membahas mekanik atau interpretasi indikator tertentu secara mendalam dan Decision Framework tidak cukup untuk evaluasi, baca KB yang relevan — semua dari `D:\Claude Code\Projects\Onchain-Dashboard\references\`. Jangan baca semua sekaligus — hanya yang dibutuhkan.

| File (di `D:\Claude Code\Projects\Onchain-Dashboard\references\`) | Isi |
|------|-----|
| `mvrv_Knowledge_Base v1.4.md` | MVRV Ratio, LTH-MVRV, STH-MVRV, MVRV Z-Score |
| `sopr_knowledge_base v1.4.md` | aSOPR, LTH-SOPR, STH-SOPR, MA gap signals |
| `nupl_knowledge_base v1.4.md` | NUPL, LTH-NUPL, STH-NUPL |
| `supply_in_profit_loss_knowledge_base v1.4.md` | Supply in Profit/Loss, STH/LTH profit % |
| `Price_Level_knowledge_base v1.4.md` | STH/LTH Realized Price, AVIV Mean/Upper, CVDD |

---

## CARA ANALISIS VIDEO

### Step 1 — Nonton dan catat

Nonton video sampai selesai. Fokus pada:
- Indikator apa yang dibahas
- Klaim atau kesimpulan apa yang dibuat pembicara
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

Satu folder per video di `Outputs/`, nama folder: `YYYY-MM-DD_[judul-video-lengkap-kebab-case]` (tanggal video, bukan tanggal analisis). Slug HARUS merepresentasikan judul video secara utuh (kebab-case, lowercase, tanpa tanda baca) — jangan dipersingkat atau dipotong ke beberapa kata kunci saja, meskipun judulnya panjang atau ada boilerplate seperti "How to Use X for Bitcoin".

Contoh: judul video "How to Use the Fear & Greed Index for Bitcoin" → `Outputs/2025-02-23_how-to-use-the-fear-greed-index-for-bitcoin/`
Contoh: judul video "LTH-SOPR Update: What It Means Right Now" → `Outputs/2026-07-06_lth-sopr-update-what-it-means-right-now/`

Isi tiap folder:
- `analysis.md` — analisis utama (template di bawah). Nama file SELALU `analysis.md`, bukan mengulang judul
- `transcript.md` — transkrip mentah video (sumber asli, disimpan supaya tidak perlu nonton ulang kalau video kelak dihapus/private)
- `findings_[topik].md` — satu file per insight yang divalidasi dengan data (Claude Code), dibuat saat validasi selesai. Contoh: `findings_mvrv_rolling1y_vs_aviv.md`

`Outputs/video_index.md` — index lintas-video (di root `Outputs/`, di luar folder manapun). Cek dulu sebelum label insight sebagai [BARU] — kalau sudah pernah dibahas video lain, sebutkan itu.

**Kapan update `video_index.md`:** BUKAN otomatis tiap kali `analysis.md` ditulis. Analisis biasanya masih didiskusikan/direvisi dulu bareng Yudi sebelum final. Update index cuma sekali, di akhir, setelah Yudi konfirmasi analisis videonya sudah final — supaya tidak bolak-balik update untuk hal yang belum settle.

---

### Template isi `analysis.md`:

```markdown
# [Judul Video]
**Channel:** [On-Chain Mind / Tristan Colt]
**Tanggal video:** [tanggal upload]
**Tanggal analisis:** [tanggal hari ini]
**Link:** [URL video]

---

## Ringkasan

[Proporsional dengan isi video. Video pendek dan focused = beberapa kalimat.
Video panjang dengan banyak topik = beberapa paragraf. Tidak ada batas minimum
atau maksimum — sesuaikan dengan seberapa banyak yang perlu dijelaskan supaya
orang yang belum nonton bisa paham konteksnya.]

---

## Insight Inventory

### [BARU] [Judul singkat insight]
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

**Jangan setuju karena nama besar.** Tristan Colt dan On-Chain Mind adalah sumber yang bagus, tapi test tetap dilakukan. Cari titik lemah dari setiap klaim sebelum label sebagai valid.

**Bahasa output:** Bahasa Indonesia untuk narasi dan evaluasi. Technical terms tetap English (MVRV, SOPR, LTV, capitulation, dll).

---

## KAPAN HARUS STOP DAN LAPOR

Kalau ketemu salah satu dari ini, catat sebagai flag khusus di bagian atas file output:

- Insight yang secara langsung bertentangan dengan hard constraint LTV
- Framework atau strategi dari pembicara yang secara fundamental berbeda dengan pendekatan zone-based + K-node yang sudah ada

Flag ini ditampilkan langsung ke Yudi di chat (jangan tunggu sampai akhir pipeline) sebelum diputuskan apakah framework perlu direvisi — bukan dibawa ke tool lain.
