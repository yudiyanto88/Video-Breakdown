# Validasi: MVRV Exponential Peak/Trough Fit — "99.7%+ chance tidak dip di bawah RP"

**Sumber:** "EVERYONE Expects Bitcoin To Break This Line, It's Held 99% Of The Time" — Bitcoin Magazine Pro, 2026-07-09
**Script:** `analyze_mvrv_expfit_circularity.py`
**Events pendukung:** `events_mvrv_expfit_anchors.csv`
**Tanggal validasi:** 2026-07-28

---

## Klaim yang diuji

Video fit regresi eksponensial `MVRV = EXP(a + b x date)` terpisah untuk semua PEAK historis MVRV raw ratio dan semua TROUGH historis MVRV raw ratio, lintas seluruh sejarah BTC. Klaim utama: garis trough-fit baru saja crossing di atas MVRV=1 (implied trough hari ini ~1.005 vs MVRV aktual ~1.19-1.23) -> Bitcoin "kemungkinan besar" (99.7%+) TIDAK akan dip di bawah realized price cycle ini. Basis "probabilitas" ini: sepanjang sejarah BTC, cuma 17 hari (0.29%) MVRV pernah di bawah garis trough-fit, dan 9 hari (0.15%) di atas garis peak-fit.

---

## Definisi event (dipakai untuk replikasi)

- **PEAK per cycle** = titik MVRV raw ratio TERTINGGI dalam window bull-run cycle tsb (bukan titik harga ATH -- MVRV bisa peak sebelum harga ATH kalau realized price naik cepat, dan ini terkonfirmasi di data: 2024-25 MVRV peak ada di 2024-03-11 meski ATH harga baru terjadi Agustus 2025).
- **TROUGH per cycle** = titik MVRV raw ratio TERENDAH dalam window bear-market cycle tsb.
- Window cycle: 2011, 2013, 2017, 2021, 2024-25(berjalan) untuk peak; 2011, 2015, 2018, 2022 untuk trough. Ini SAMA PERSIS dengan cycle yang disebut eksplisit oleh video sendiri di transcript ("2011, 2013, 2017/2018, 2021/2022, current").
- **n = 5 titik peak, n = 4 titik trough.** Cycle saat ini (2024-2026) belum punya trough -- itu justru yang mau diprediksi, jadi tidak dimasukkan ke fit trough.

## Hasil replikasi independen

**(a) Titik anchor** (lihat `events_mvrv_expfit_anchors.csv`):

| Cycle | Tanggal | MVRV |
|---|---|---|
| Peak 2011 | 2011-06-04 | 7.87 |
| Peak 2013 | 2013-11-18 | 5.99 |
| Peak 2017 | 2017-12-07 | 4.98 |
| Peak 2021 | 2021-02-21 | 3.95 |
| Peak 2024-25 | 2024-03-11 | 2.77 |
| Trough 2011 | 2011-10-19 | 0.401 |
| Trough 2015 | 2015-01-14 | 0.568 |
| Trough 2018 | 2018-12-14 | 0.702 |
| Trough 2022 | 2022-11-09 | 0.760 |

**(b) Persentase hari historis** (n_total hari = 5843, data 2010-07-17 s/d 2026-07-15):
- Hari MVRV < trough_line: **20 hari (0.342%)** -- klaim video: 17 hari (0.29%). Close, replikasi kami konsisten kualitatif dengan klaim (sedikit beda karena data source/window berbeda).
- Hari MVRV > peak_line: **9 hari (0.154%)** -- klaim video: 9 hari (0.155%). Match persis.
- Implied trough line hari ini (2026-07-15): **1.0049** -- MVRV aktual: **1.234**. Konsisten dengan klaim video bahwa garis trough sudah crossing di atas 1.

Sejauh ini klaim video secara matematis TEREPLIKASI dengan cukup akurat -- perhitungan dasarnya bukan salah hitung.

**(c) Leave-one-out sensitivity test (INI YANG PALING PENTING):**

Fit trough hanya berbasis **4 titik data**. Kalau salah satu dari 4 titik itu dibuang, prediksi berubah drastis:

| Titik dibuang | Implied trough hari ini | Kesimpulan (>1 = "won't dip") |
|---|---|---|
| (baseline, semua 4) | 1.0049 | won't dip |
| Drop 2011 trough | **0.8922** | **WILL dip** |
| Drop 2015 trough | 1.0096 | won't dip |
| Drop 2018 trough | **0.9555** | **WILL dip** |
| Drop 2022 trough | 1.3000 | won't dip |

**2 dari 4 leave-one-out run (50%) membalik kesimpulan** dari "tidak akan dip" menjadi "akan dip" hanya dengan membuang SATU titik data. Membuang titik 2011 (titik tertua/paling ekstrem, MVRV=0.40) saja sudah cukup untuk membalik prediksi ke arah sebaliknya.

## Verdict

**NOT SUPPORTED sebagai basis prediksi probabilistik yang solid.**

- Angka "99.7%+ chance" dan replikasi persentase hari (0.29%/0.15%) itu sendiri **secara matematis kurang lebih benar** -- bukan salah hitung.
- TAPI angka itu menyesatkan sebagai ukuran "confidence" karena garis fit-nya dibangun dari **n=4 titik trough saja**, dan hasil leave-one-out menunjukkan prediksi **sangat tidak robust** -- flip ke kesimpulan berlawanan kalau 1 dari 4 titik dihapus. Persentase "hari di bawah garis" itu menghitung seberapa jarang harga historis menyimpang dari garis fit ITU SENDIRI, bukan probabilitas independen bahwa garis fit itu benar -- ini **circular**: garis dipaksa melewati dekat semua 4 titik trough (karena fit-nya memang dari titik-titik itu), jadi "wajar" kalau historis jarang menyimpang jauh dari garis. Statistik 0.29%/0.15% TIDAK mengukur ketidakpastian dari fakta bahwa garis dibangun dari sample sangat kecil.
- **n=4-5 titik untuk fit regresi lintas seluruh sejarah BTC (15+ tahun) adalah sample sangat kecil.** Wajib ditekankan: kesimpulan "99.7%+ chance" TIDAK didukung oleh jumlah observasi independen sebanyak itu -- observasi sebenarnya hanya 4 cycle bear market yang sudah lewat.
- Klaim tambahan video "severity dip mengecil tiap cycle" (dibahas terpisah di Topik 2 & 3) memang konsisten arahnya (SUPPORTED secara deskriptif, lihat findings terkait) -- tapi itu tidak otomatis membuat *garis fit* ini robust untuk prediksi kuantitatif presisi (1.005 vs 1.194).
- Bahasa yang tepat: pola makin tinggi-nya trough MVRV tiap cycle memang **cenderung** terjadi (4 dari 4 cycle yang selesai, konsisten arah), tapi mengklaim angka spesifik seperti "99.7%" atau "trough level = 1.005" dari fit 4 titik adalah overconfident -- presisi itu semu (false precision).

**n & sebaran:** 5 titik peak (1 per cycle: 2011, 2013, 2017, 2021, 2024-25), 4 titik trough (1 per cycle: 2011, 2015, 2018, 2022). Leave-one-out: 4 run, 2 flip verdict.
