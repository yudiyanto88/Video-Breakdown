---
description: Bedah video on-chain end-to-end sesuai workflow CLAUDE.md — nonton, ekstrak & kategorikan insight, test klaim, validasi data (lintas-project ke Onchain-Dashboard), simpan hasil. Tidak pernah mengubah Decision_Framework.
argument-hint: <url-atau-path-video> [channel opsional]
---

# Analyze Video Pipeline

Argumen: `$ARGUMENTS` — argumen pertama = URL/path video, sisanya (kalau ada) = channel (On-Chain Mind / Tristan Colt / lainnya).

Kamu adalah **orchestrator**. Jalankan operasionalisasi dari `CLAUDE.md` project ini — command ini TIDAK mengubah aturan CLAUDE.md, cuma mengeksekusinya sebagai pipeline bertahap dengan sub-agent supaya tiap tahap fokus. Prinsip utama tetap sama: **insight ini diusulkan, bukan langsung diterapkan ke Decision Framework**.

Buat task list (TaskCreate) untuk stage di bawah supaya progres kelihatan.

---

## Stage 0 — Watch

1. Tentukan `<slug>` dari judul video LENGKAP (kebab-case, lowercase, jangan dipersingkat/dipotong — ikuti aturan penamaan di `CLAUDE.md` bagian "FORMAT OUTPUT") dan `<tanggal-video>` (dari metadata video, bukan hari ini)
2. Buat folder `Outputs/<tanggal-video>_<slug>/`
3. Invoke skill `watch` dengan argumen video
4. Simpan transcript ke `Outputs/<tanggal-video>_<slug>/transcript.md` — sertakan header: judul, channel, URL, tanggal video
5. Kalau watch gagal (private/region-lock/dll), STOP dan laporkan — jangan lanjut dengan transcript kosong

## Stage 1 — Ekstrak & kategorikan (sub-agent `insight-extractor`)

Spawn sub-agent `insight-extractor` (synchronous). Prompt berisi: path transcript, channel (kalau disebutkan di `$ARGUMENTS`), instruksi baca `CLAUDE.md` + Decision Framework + `Outputs/video_index.md`.

Hasil: daftar insight per bucket `[BARU]/[KONFIRMASI]/[KONFLIK]/[INDIKATOR CUSTOM]/[STRATEGI]`, belum diuji.

## Stage 2 — Test klaim (sub-agent `claim-tester`)

Spawn sub-agent `claim-tester` (synchronous). Prompt berisi seluruh daftar insight dari Stage 1.

Hasil per insight: "Test klaim" + "Perlu validasi Claude Code: Ya/Tidak" (+ pertanyaan spesifik kalau Ya) + flag STOP kalau ada yang bentrok hard constraint atau framework fundamental berbeda.

**Kalau ada flag STOP:** tampilkan di chat SEKARANG (jangan tunggu sampai akhir pipeline) — ini butuh keputusan Yudi sebelum lanjut, bukan sesuatu yang bisa diproses otomatis.

## Stage 3 — Validasi data (sub-agent `data-verifier`)

Untuk insight yang diflag "Perlu validasi Claude Code: Ya" (maksimal 3 per video — kalau lebih, prioritaskan yang paling menyentuh K-node aktif saat ini, sisanya masuk output sebagai "Perlu validasi Claude Code: Ya — belum diuji, backlog"):

Spawn sub-agent `data-verifier` (synchronous, satu spawn bisa menangani beberapa insight). Prompt berisi: insight + pertanyaan spesifik dari claim-tester + path folder video ini (`Outputs/<tanggal-video>_<slug>/`).

Hasil per insight: blok `[VALIDASI — <tanggal>, CLOSED]` siap ditempel + file `findings_<topik>.md` tersimpan **di dalam folder video ini** (`Outputs/<tanggal-video>_<slug>/findings_<topik>.md`, bukan di folder terpisah).

## Stage 4 — Tulis output (kamu sendiri, orchestrator)

Tulis `Outputs/<tanggal-video>_<slug>/analysis.md` — **ikuti PERSIS template di `CLAUDE.md`** (bagian "Template isi `analysis.md`"): Ringkasan, Insight Inventory per bucket (dengan Test klaim + Perlu validasi Claude Code, dan blok `[VALIDASI]` inline untuk yang sudah divalidasi Stage 3 — link ke `findings_<topik>.md` pakai path relatif, bukan subfolder), Flag Prioritas, Yang Langsung Diabaikan.

Contoh gaya yang sudah established: `Outputs/2025-01-22_bitcoin-ath-what-next/analysis.md` — ikuti gaya penulisan ini (padat, angka konkret, tidak berlebihan).

## Stage 5 — STOP (gated)

Pipeline SELESAI di sini. **JANGAN update `Outputs/video_index.md` dan JANGAN mengedit `Decision_Framework v1.md` di Onchain-Dashboard atau file KB apapun** — walau ada insight [BARU] yang tervalidasi kuat.

`video_index.md` sengaja BELUM diupdate di tahap ini — isi `analysis.md` masih bisa berubah kalau ada diskusi/revisi lanjutan dengan Yudi (kategori insight geser, verdict validasi direvisi, dll). Update `video_index.md` cuma dilakukan SEKALI, di akhir, setelah Yudi bilang analisis ini final — bukan otomatis tiap kali `analysis.md` ditulis/diedit. Ini supaya tidak bolak-balik update index untuk hal yang belum settle.

Tutup dengan ringkasan singkat: link file output, jumlah insight per bucket, dan (kalau ada) flag STOP dari Stage 2 ditampilkan ulang di chat. Tutup juga dengan pengingat: **"video_index.md belum diupdate — bilang kalau analisis ini sudah final."**

## Stage 6 — Finalisasi (baru dijalankan kalau Yudi bilang "final"/"sudah oke"/setara)

Ini TIDAK otomatis lanjut dari Stage 5 — nunggu sinyal eksplisit dari Yudi di chat setelah diskusi/revisi selesai.

Begitu dapat sinyal final: baca `analysis.md` versi TERAKHIR (bukan versi awal Stage 4, kalau sudah direvisi), lalu **append satu baris per insight** ke `Outputs/video_index.md` (format tabel sudah ada di file itu). Kolom terakhir isi path folder (`<tanggal-video>_<slug>/analysis.md` atau `<tanggal-video>_<slug>/findings_<topik>.md`).
