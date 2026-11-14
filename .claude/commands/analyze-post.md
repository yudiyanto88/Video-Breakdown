---
description: Bedah tweet/post berisi analisis on-chain atau foto chart end-to-end sesuai workflow CLAUDE.md — baca & simpan sumber, ekstrak & kategorikan insight, test klaim, validasi data (lintas-project ke Onchain-Dashboard), simpan hasil. Tidak pernah mengubah Decision_Framework.
argument-hint: [topik/deskripsi singkat] — lampirkan gambar di chat; teks tweet di-paste kalau ada
---

# Analyze Post Pipeline (tweet & foto chart)

Argumen: `$ARGUMENTS` — topik/deskripsi singkat (opsional: nama akun/sumber, URL post). Gambar dilampirkan langsung di chat oleh Yudi; teks tweet (kalau ada) di-paste di chat.

Kamu adalah **orchestrator**. Pipeline ini identik dengan `/analyze-video` kecuali Stage 0 — sumbernya bukan video yang harus ditonton, tapi gambar chart / screenshot tweet yang dilampirkan di chat. Command ini TIDAK mengubah aturan `CLAUDE.md`, cuma mengeksekusinya bertahap dengan sub-agent yang sama. Prinsip utama tetap: **insight diusulkan, bukan langsung diterapkan ke Decision Framework**.

Buat task list (TaskCreate) untuk stage di bawah supaya progres kelihatan.

---

## Stage 0 — Baca & simpan sumber (pengganti watch)

1. Tentukan `<slug>` dari topik utama post (kebab-case, lowercase, representatif — kalau tweet punya klaim utama, pakai itu sebagai basis slug) dan `<tanggal-post>`:
   - Dari screenshot/teks tweet kalau tanggalnya terlihat
   - Kalau tidak terlihat → pakai tanggal analisis hari ini, dan catat "tanggal post tidak diketahui, dipakai tanggal analisis" di header `source.md`
2. Buat folder `Outputs/posts/<tanggal-post>_<slug>/`
3. **Simpan salinan SETIAP gambar yang dilampirkan** ke folder itu sebagai `gambar_1.png`, `gambar_2.png`, dst. (urutan sesuai lampiran). Folder harus self-contained: sumber asli + seluruh hasil analisis di satu tempat, tidak tergantung chat history — sama seperti folder video yang menyimpan `transcript.md`.
4. Baca setiap gambar dengan teliti, lalu tulis `Outputs/posts/<tanggal-post>_<slug>/source.md`:

```markdown
# [Judul/topik post]
**Sumber/Akun:** [nama akun/analis, atau "tidak diketahui"]
**URL:** [URL post, atau "-"]
**Tanggal post:** [tanggal, + catatan kalau fallback ke tanggal analisis]
**Jenis input:** [tweet + foto / foto saja]

---

## Teks post

[Teks tweet verbatim kalau ada. Kalau input foto-saja, tulis "(tidak ada teks — input foto saja)"]

## Gambar 1 — [nama chart yang teridentifikasi]

- **Metrik:** [metrik apa yang ditampilkan, semua garis/series]
- **Platform chart:** [checkonchain / ChartInspect / Alphractal / TradingView / tidak teridentifikasi]
- **Timeframe:** [rentang tanggal yang terlihat di sumbu X]
- **Anotasi pembuat:** [garis, panah, lingkaran, teks yang ditambahkan si pembuat — apa yang mau dia tunjukkan]
- **Angka terbaca:** [nilai-nilai yang terbaca dari chart — SEMUA dilabel "low confidence dari resolusi gambar", jangan dipakai sebagai anchor kesimpulan]
- **Apa yang ditunjukkan chart:** [deskripsi objektif pola/kondisi yang terlihat — belum interpretasi]

## Gambar 2 — [...]
[dst. untuk setiap gambar]
```

5. **STOP rule** (analog watch gagal di video): kalau gambar blur, terpotong, atau chart-nya tidak bisa diidentifikasi dengan yakin (metrik apa, timeframe apa) — STOP dan lapor ke Yudi, minta gambar yang lebih jelas atau konfirmasi. Jangan lanjut dengan tebakan.
6. Mode **foto-saja** (tanpa teks tweet/klaim): bagian "Teks post" kosong. Insight di Stage 1 diekstrak dari apa yang ditunjukkan chart-nya sendiri — pola apa yang digambar, sinyal apa yang di-highlight anotasinya, interpretasi apa yang tersirat dari cara chart itu disusun.

## Stage 1 — Ekstrak & kategorikan (sub-agent `insight-extractor`)

Spawn sub-agent `insight-extractor` (synchronous). Prompt berisi: path `source.md`, nama akun/sumber (kalau diketahui), instruksi baca `CLAUDE.md` + Decision Framework + `Outputs/source_index.md`, dan catatan bahwa sumbernya post/foto — referensi kutipan pakai "Gambar N", bukan timestamp.

Hasil: daftar insight per bucket `[BARU]/[KONFIRMASI]/[KONFLIK]/[INDIKATOR CUSTOM]/[STRATEGI]`, belum diuji.

## Stage 2 — Test klaim (sub-agent `claim-tester`)

Spawn sub-agent `claim-tester` (synchronous). Prompt berisi seluruh daftar insight dari Stage 1.

Hasil per insight: "Test klaim" + "Perlu validasi Claude Code: Ya/Tidak" (+ pertanyaan spesifik kalau Ya) + flag STOP kalau ada yang bentrok hard constraint atau framework fundamental berbeda.

**Kalau ada flag STOP:** tampilkan di chat SEKARANG (jangan tunggu akhir pipeline) — butuh keputusan Yudi sebelum lanjut.

## Stage 3 — Validasi data (sub-agent `data-verifier`)

Untuk insight yang diflag "Perlu validasi Claude Code: Ya" (maksimal 3-5 per post, pilih yang high-value — prioritaskan yang paling menyentuh K-node aktif saat ini, sisanya masuk output sebagai "Perlu validasi Claude Code: Ya — belum diuji, backlog"):

Spawn sub-agent `data-verifier` (synchronous, satu spawn bisa menangani beberapa insight). Prompt berisi: insight + pertanyaan spesifik dari claim-tester + path folder post ini (`Outputs/posts/<tanggal-post>_<slug>/`).

Hasil per insight: blok `[VALIDASI — <tanggal>, CLOSED]` siap ditempel + file `findings_<topik>.md` tersimpan **di dalam folder post ini**. Tabel event pendukung disimpan sebagai `events_<topik>.csv` di folder yang sama.

## Stage 4 — Tulis output (kamu sendiri, orchestrator)

Tulis `Outputs/posts/<tanggal-post>_<slug>/analysis.md` — **ikuti PERSIS template di `CLAUDE.md`** (bagian "Template isi `analysis.md`"), dengan metadata header versi post:

```markdown
# [Judul/topik post]
**Sumber/Akun:** [nama akun/analis]
**Tanggal post:** [tanggal post]
**Tanggal analisis:** [tanggal hari ini]
**URL:** [URL post, atau "-"]
```

Sisanya sama: Ringkasan, Insight Inventory per bucket (referensi pakai "Gambar N" menggantikan timestamp, blok `[VALIDASI]` inline untuk yang divalidasi Stage 3, link relatif ke `findings_<topik>.md`), Flag Prioritas, Yang Langsung Diabaikan.

## Stage 5 — STOP (gated)

Pipeline SELESAI di sini. **JANGAN update `Outputs/source_index.md` dan JANGAN mengedit `Decision_Framework v2.md` di Onchain-Dashboard atau file KB apapun** — walau ada insight [BARU] yang tervalidasi kuat.

`source_index.md` sengaja BELUM diupdate — isi `analysis.md` masih bisa berubah kalau ada diskusi/revisi lanjutan dengan Yudi. Update index cuma dilakukan SEKALI, di akhir, setelah Yudi bilang analisisnya final.

Tutup dengan ringkasan singkat: link file output, jumlah insight per bucket, dan (kalau ada) flag STOP dari Stage 2 ditampilkan ulang. Tutup dengan pengingat: **"source_index.md belum diupdate — bilang kalau analisis ini sudah final."**

## Stage 6 — Finalisasi (baru dijalankan kalau Yudi bilang "final"/"sudah oke"/setara)

TIDAK otomatis lanjut dari Stage 5 — nunggu sinyal eksplisit dari Yudi.

Begitu dapat sinyal final: baca `analysis.md` versi TERAKHIR, lalu **append satu baris per insight** ke `Outputs/source_index.md` — kolom Sumber diisi `Tweet` atau `Foto` sesuai jenis input, kolom Folder diisi path `posts/<tanggal-post>_<slug>/...`.
