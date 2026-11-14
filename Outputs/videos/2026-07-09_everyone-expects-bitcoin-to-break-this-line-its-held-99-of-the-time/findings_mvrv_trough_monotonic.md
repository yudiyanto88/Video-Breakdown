# Validasi: Trough MVRV Naik Monoton Tiap Cycle

**Sumber:** "EVERYONE Expects Bitcoin To Break This Line, It's Held 99% Of The Time" — Bitcoin Magazine Pro, 2026-07-09
**Script:** `analyze_mvrv_trough_monotonic.py`
**Events pendukung:** `events_mvrv_trough_monotonic.csv`
**Tanggal validasi:** 2026-07-28

---

## Klaim yang diuji

Lembah (trough) MVRV raw ratio per cycle makin tinggi secara monoton tiap cycle berturut-turut (2011 < 2015 < 2018 < 2022 < ..., arah naik).

## Definisi event

TROUGH per cycle = titik MVRV raw ratio TERENDAH dalam window bear-market cycle tsb, window ditentukan dari tanggal cycle bottom yang sudah dikenal publik (sama dengan yang disebut video: 2011, 2015, 2018, 2022). Cycle saat ini (2024-2026) BELUM py trough terkonfirmasi (masih berjalan) -- tidak dimasukkan ke pengujian monotonic ini karena itu justru pertanyaan yang belum terjawab.

**n = 4 cycle selesai.**

## Hasil

| Cycle | Tanggal trough | MVRV trough |
|---|---|---|
| 2011 | 2011-10-19 | 0.401 |
| 2015 | 2015-01-14 | 0.568 |
| 2018 | 2018-12-14 | 0.702 |
| 2022 | 2022-11-09 | 0.760 |

Selisih berurutan: +0.167, +0.135, +0.058 -- SEMUA POSITIF. Urutan **monoton naik** untuk keempat cycle ini.

**Robustness check:** window trough diperlebar (window lebih longgar +/- beberapa bulan di tiap sisi) -- hasil trough date & value TIDAK berubah, urutan tetap monoton naik. Tidak sensitif terhadap pemilihan window.

## Verdict

**SUPPORTED secara deskriptif**, dengan catatan tebal:

- **n hanya 4 titik/cycle** -- ini adalah SEMUA cycle bear market lengkap yang tersedia di data historis BTC (2010-2026). Sample sangat kecil untuk klaim "akan SELALU monoton" ke depan -- baru 4 observasi independen (dan cycle-cycle ini juga tidak sepenuhnya independen satu sama lain, karena driven oleh trend struktural yang sama: makin banyak supply lama/lost/HODL makin tinggi harganya dibeli).
- Cycle saat ini (2024-2026) BELUM py trough -- klaim TIDAK BISA diverifikasi untuk cycle berjalan sampai bear market berikutnya benar-benar terjadi & titik terendahnya terkonfirmasi.
- Pola ini konsisten dengan argumen struktural video (makin banyak coin lama/lost yang dibeli di harga tinggi -> rata-rata cost basis makin "sticky" ke atas), jadi ada mekanisme kausal yang masuk akal, bukan cuma kebetulan numerik -- tapi bahasa yang tepat tetap "cenderung monoton", bukan "pasti monoton", mengingat n=4.
- Catatan penting: Topik 3 (severity dip RP dalam %) SECARA MATEMATIS ekuivalen dengan temuan ini (severity = 1 - MVRV_trough) -- jadi validasi Topik 2 & 3 BUKAN dua bukti independen, melainkan reframing dari pola dasar yang sama.

**n & sebaran:** 4 cycle (2011, 2015, 2018, 2022), 1 titik trough per cycle.
