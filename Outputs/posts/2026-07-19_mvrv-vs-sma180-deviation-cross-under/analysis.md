# MVRV Deviation Cross-Under (mvrv_ratio vs SMA180)
**Sumber/Akun:** internal — chart buatan sesi riset Onchain-Dashboard (dry-run test pipeline /analyze-post)
**Tanggal post:** tidak diketahui — dipakai tanggal analisis
**Tanggal analisis:** 2026-07-19
**URL:** -

---

## Ringkasan

Input foto-saja: satu chart internal bergaya checkonchain yang menampilkan sinyal cross-under MVRV Ratio ke bawah SMA180-nya sebagai "severity flag" (panel harga + panel MVRV vs SMA180, 2010–2026, 11 titik cross ditandai). Sinyal ini sudah terpasang di Decision_Framework v2 (alarm bear cepat #4, K2 veto #3), jadi sebagian besar isi chart bersifat konfirmasi — dan karena chart-nya turunan dari KB MVRV § 6C sendiri, konfirmasinya circular, bukan bukti independen. Satu hal yang benar-benar diuji: deskripsi sumber melabeli event 2019/2024/2026 sebagai "non-peak, jinak", bertentangan dengan tabel KB. Hasil validasi: **KB benar, label sumber salah** — ketiga event itu ganas (−19% s/d −30%), dan pembeda yang bekerja adalah recency Z5 + status bear-confirmed, bukan jarak visual ke cycle peak. Bonus: validasi ini sekaligus menyediakan bahan rekonsiliasi count 11-vs-16 yang pending di Governance v2 butir 4c.

---

## Insight Inventory

### [KONFIRMASI] MVRV Ratio cross-under SMA180 sebagai penanda koreksi serius
- **Insight:** Sebagian besar titik cross-under jatuh persis/tak lama setelah 4 cycle peak (Gambar 1). Mendukung sinyal yang sudah ada di framework (alarm cepat #4, K2 veto #3).
- **Indikator terkait:** MVRV Ratio, SMA180(MVRV Ratio)
- **Relevan ke:** Status Pasar § 0 (alarm cepat #4), K2 veto #3
- **Test klaim:** Circular confirmation — angka subtitle chart identik verbatim dengan KB § 6C.2, jadi chart ini turunan KB, bukan sumber independen. Precision 0.82 berarti 2/11 false; parameter fitted dari grid search 38 konfigurasi (in-sample), performa forward hampir pasti lebih rendah.
- **Perlu validasi Claude Code:** Tidak — established di KB § 6C.2, sudah terpasang di framework.

### [KONFIRMASI] Cross-under dekat kunjungan Z5 terakhir lebih berbahaya daripada yang jauh
- **Insight:** Pola visual: cross dekat peak diikuti penurunan panjang; deskripsi sumber melabeli event non-peak (2015, 2019, 2023, 2024, 2026) "lebih jinak" (Gambar 1). Arah sejalan dengan kualifikasi recency Z5 di framework, TAPI daftar contohnya bentrok dengan tabel KB § 6C.2.
- **Indikator terkait:** MVRV vs SMA180 + hari sejak Z5 (harga ≥ AVIV Upper)
- **Relevan ke:** Alarm cepat #4, K2 veto #3 (komponen "Z5 ≤~120 hari")
- **Test klaim:** Dua sumber internal tidak sepakat mengklasifikasi event yang sama — persis jenis ambiguitas definisi-event yang jadi akar pending Governance 4c. Threshold ≤~120 hari provisional, fitted pada n=11.
- **Perlu validasi Claude Code:** Ya — apakah 2019/2024/2026 jinak (versi chart) atau ganas (versi KB)?

**[VALIDASI — 2026-07-19, CLOSED]** Replikasi penuh definisi § 6C.1 menghasilkan persis n=11 event (C1=3, C2=1, C3=3, C4=4), precision 0,82 dan median dd −30,5% — cocok dengan KB. Verdict: KB § 6C.2 BENAR, label chart salah — event 2019 (−30,5%), 2024 (−19,1%), dan 2026 (−24,5%, window belum penuh tapi sudah melewati batas 15%) semuanya ganas, bukan jinak; hanya 2015 dan 2023 (>600 hari sejak Z5) yang benar-benar jinak (−5%). Pembeda yang bekerja adalah recency Z5 + status bear-confirmed, bukan jarak ke cycle peak; catatan: boundary 75 hari fitted tepat di event 2019 (75,0 hari), n kecil dari 4 cycle. Rekonsiliasi 11-vs-16: definisi ketat = 11, persistensi-saja = 30, raw = 85 — angka 16 cenderung varian syarat regime yang lebih longgar di script review.
Detail: [`findings_z5_recency_classification.md`](findings_z5_recency_classification.md)

### [KONFIRMASI — re-bucket dari [BARU]] Kuantifikasi severity: precision 0.82, lift 1.7x, median dd lanjutan −31%
- **Insight:** Subtitle chart menyebut "11 cross dalam 15 tahun, precision 0.82 (lift 1.7x base rate), median lanjutan dd −31%" (Gambar 1).
- **Indikator terkait:** MVRV Ratio, SMA180(MVRV Ratio)
- **Relevan ke:** General (kalibrasi ekspektasi saat sinyal nyala)
- **Test klaim:** Label [BARU] dari Stage 1 salah — angka-angka ini ada verbatim di KB MVRV v1.4 § 6C.2; chart menyalin KB, bukan menambah informasi. Item yang benar-benar terbuka (count 11-vs-16) adalah pending Governance 4c, dikerjakan di project Onchain-Dashboard.
- **Perlu validasi Claude Code:** Tidak — angka KB sendiri; bahan rekonsiliasi sudah tersedia dari validasi insight ke-2.

### [KONFLIK] Framing cross-under mentah sebagai severity flag standalone
- **Insight:** Chart menampilkan cross-under sebagai flag tunggal "koreksi ganas" — mengundang pemakaian sebagai konfirmasi bear mandiri (Gambar 1).
- **Konflik dengan:** K2 veto #3 ("penghenti pembelian, JANGAN dipakai konfirmasi bear"), catatan K3 (confirming context saja, dilarang masuk gate), pool alarm cepat 2-dari-4.
- **Alasan konflik:** Peran berbeda (standalone bear-confirmer vs komponen pool/veto) — dan pemakaian standalone sudah teruji GAGAL di data (12/16 firing terkualifikasi recover ke ATH baru). Kadar konflik rendah: footer chart sendiri menulis "bukan syarat formal framework saat ini".
- **Rekomendasi:** Abaikan framing standalone-nya. Kalau chart dipertahankan sebagai visual monitoring, tambahkan anotasi persistensi ≥7 hari + syarat Z5 ≤~120 hari supaya tidak menyesatkan pembaca masa depan.

---

## Flag Prioritas

1. **Koreksi label sumber (insight #2)** — deskripsi "2019/2024/2026 jinak" terbukti salah; kalau chart ini dipakai lagi sebagai referensi visual, jangan warisi label itu. Pembeda yang benar: recency Z5 + bear-confirmed.
2. **Bahan rekonsiliasi Governance 4c** — enumerasi L0=85 / L1=30 / STRICT=11 siap dipakai untuk menutup item pending count 11-vs-16 di project Onchain-Dashboard (butuh baca `opus_bear_confirmed_v2_mvrv.py` untuk replikasi persis angka 16).

---

## Yang Langsung Diabaikan

- Angka posisi harga per titik cross di chart ($0.9 s/d $77k) — hanya lokasi visual, low confidence dari resolusi gambar, tidak dipakai sebagai anchor (dan sudah tergantikan oleh tabel event hasil validasi).
