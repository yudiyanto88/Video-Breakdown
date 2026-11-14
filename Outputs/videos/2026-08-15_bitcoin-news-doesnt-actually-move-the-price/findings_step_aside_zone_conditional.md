# Findings — Step-aside pasca-shock: replikasi realistis & varian zone-conditional

**Insight asal:** K-3 (menghindari volatility itu mahal) + konflik X-1 (kesimpulan video vs K1/K3)
**Sumber:** Look Into Bitcoin, "Bitcoin News Doesn't Actually Move The Price" (2026-08-15), `[09:46]`–`[10:52]`, `[11:54]`
**Script:** [`analyze_step_aside_zone_conditional.py`](analyze_step_aside_zone_conditional.py) (+ helper [`shock_zone_lib.py`](shock_zone_lib.py))
**Event table:** [`events_step_aside_triggers.csv`](events_step_aside_triggers.csv)
**Tanggal validasi:** 2026-08-20

---

## Definisi event & aturan backtest

- Down-shock = `log ret <= -3 × vol30 at-gate` (definisi shock yang sama dengan validasi lain, dibatasi ke sisi bawah)
- Aturan step-aside: begitu trigger nyala, **keluar penuh ke cash selama N hari kalender** (N = 5 dan 10), lalu masuk lagi. Trigger yang muncul saat sedang di luar memperpanjang periode keluar, tidak menumpuk.
- Semua trigger **at-gate** — tidak ada informasi dari masa depan.
- Pembanding "HINDSIGHT top-15" mereplikasi metode video secara harfiah: 15 hari dengan `|move|` terbesar dipilih **ex-post** dari seluruh sample, lalu diasumsikan investor tahu untuk keluar. Ini varian yang tidak bisa diimplementasikan; dimasukkan justru untuk mengukur berapa besar sumbangan hindsight terhadap hasil video.
- Biaya transaksi diuji di 0 bps dan 20 bps per switch.

## Sample

Trigger per cycle:

| Cycle | down-shock | any-shock | trigger Z5/K1 | trigger alarm bear |
|---|---:|---:|---:|---:|
| C1 2010-2015 | 28 | 61 | 4 | 17 |
| C2 2015-2018 | 21 | 43 | 4 | 16 |
| C3 2018-2022 | 17 | 32 | 8 | 11 |
| C4 2022-2026 | 14 | 34 | 6 | 7 |

Full ≥2013: **66 trigger down-shock**, 139 any-shock, 22 Z5/K1, 42 alarm bear.

---

## Q1 — Replikasi klaim video

Klaim video: step-aside 5 hari atas 15 shock terbesar → CAGR **33,2%** vs buy & hold **66,8%**, selisih **−33,6pp** (BTC, dari 2015).

Hasil di data kita, periode 2015-01-01 s/d 2026-07-15 (buy & hold CAGR = 58,4%, MDD −83,2%):

| Aturan | N | CAGR | MDD | ΔCAGR vs B&H |
|---|---:|---:|---:|---:|
| HINDSIGHT top-15 (metode video) | 5 | 48,3% | −84,3% | **−10,2pp** |
| HINDSIGHT top-15 (metode video) | 10 | 39,2% | −87,0% | **−19,3pp** |
| step-aside SEMUA down-shock | 5 | 66,0% | −75,2% | +7,5pp |
| step-aside SEMUA down-shock | 10 | 70,9% | −79,0% | +12,4pp |
| step-aside ANY-shock (naik+turun) | 5 | 57,5% | −75,2% | −0,9pp |
| step-aside ANY-shock (naik+turun) | 10 | 49,4% | −78,8% | −9,1pp |

**Arah klaim video tereplikasi, magnitudonya tidak.** Metode hindsight top-15 memang kalah (−10,2pp di N=5, −19,3pp di N=10), tapi jauh dari −33,6pp yang disebut video. Selisih ini kemungkinan besar dari perbedaan definisi "shock day", tanggal mulai persis, dan sumber harga. **Kesimpulan kualitatifnya bertahan: melewatkan hari-hari bergerak terbesar itu mahal.**

**Tapi versi realistisnya justru menang.** Step-aside yang dipicu down-shock secara mekanis (tanpa hindsight) mengalahkan buy & hold di **8 dari 8 skenario** yang diuji, median ΔCAGR **+11,7pp**. Ini kebalikan dari kesimpulan yang orang ambil dari video.

Yang membedakan: aturan hindsight keluar di hari `|move|` terbesar **termasuk yang ke atas** — jadi ikut melewatkan god candle. Aturan realistis hanya keluar setelah pergerakan **ke bawah**. Konfirmasinya ada di baris ANY-shock: begitu shock naik ikut memicu keluar, keunggulannya hilang (−0,9pp di N=5, −9,1pp di N=10). **Jadi mekanisme sebenarnya bukan "menghindari volatility itu mahal", tapi "menghindari volatility ke ATAS itu mahal".**

## Q2 — Varian zone-conditional (untuk menutup konflik X-1)

| Aturan | N | menang CAGR di | median ΔCAGR |
|---|---:|---|---:|
| step-aside SEMUA down-shock | 5/10 | **8 dari 8 skenario** | **+11,7pp** |
| step-aside ANY-shock (naik+turun) | 5/10 | 2 dari 8 | −6,2pp |
| step-aside HANYA Z5 / window K1 | 5/10 | 2 dari 8 | **−2,9pp** |
| step-aside HANYA alarm bear raw | 5/10 | 3 dari 8 | −1,1pp |
| HINDSIGHT top-15 (video) | 5/10 | 1 dari 8 | −11,7pp |

**Varian (a) — step-aside hanya di Z5 / window K1: cenderung TIDAK memberi keunggulan.** Median −2,9pp, menang hanya 2 dari 8 skenario, n=22 trigger. Di skenario mulai-2015 dan mulai-2017 rugi konsisten (−7,5pp dan −8,8pp di N=5).

**Varian (b) — step-aside hanya saat alarm bear cepat bunyi: INCONCLUSIVE karena replikasi alarmnya gagal, bukan karena hasilnya negatif.** Replikasi alarm bear cepat v2 §0 menghasilkan kondisi ON di **63,4% hari** (versi raw 2-dari-4) sampai **94,3% hari** (versi literal dengan persistensi/unlock). Alarm yang menyala di mayoritas hari praktis tidak membedakan apa-apa dari aturan tanpa syarat. **Ini keterbatasan replikasi saya, bukan temuan tentang framework** — kemungkinan besar ada komponen aturan alarm v2 yang tidak berhasil saya terjemahkan dari teks ke kode. Perlu dicek ulang di project Onchain-Dashboard sebelum dipakai untuk apapun.

## Q3 — Sensitivitas & independensi sample

**Per cycle (aturan step-aside SEMUA down-shock, N=5):**

| Cycle | B&H CAGR | step-aside CAGR | Δ | n trigger |
|---|---:|---:|---:|---:|
| C1 2013-2015 | 301,5% | 442,0% | **+140,5pp** | 14 |
| C2 2015-2018 | 97,5% | 61,5% | **−36,0pp** | 21 |
| C3 2018-2022 | 49,1% | 77,7% | +28,7pp | 17 |
| C4 2022-2026 | 47,5% | 64,5% | +17,0pp | 14 |

**Menang di 3 dari 4 cycle, kalah telak di satu (C2).** Keunggulan full-sample sangat bergantung C1 — dan C1 di sini hanya 2 tahun data (2013-01 s/d 2015-01) dengan CAGR 300%+, era yang tidak akan berulang. Ini alasan utama untuk tidak memperlakukan hasil Q1 sebagai strategi.

**Sensitivitas tanggal mulai (step-aside down-shock N=5):** mulai 2013 → +16,7pp; mulai 2015 → +7,5pp; mulai 2017 → +13,5pp. Arahnya stabil positif, magnitudonya bergerak 2×.

**Sensitivitas biaya:** dengan 20 bps per switch (mulai 2015), keunggulan turun dari +7,5pp ke **+4,8pp** di N=5 dan +12,4pp ke +9,9pp di N=10. Dengan 66 trigger sepanjang 13,5 tahun, biaya bukan pembunuh utama — tapi ini mengasumsikan eksekusi sempurna di harga close, yang tidak realistis persis setelah hari −10%.

**Max drawdown:** step-aside down-shock N=5 menurunkan MDD dari −83,2% ke −75,2% (mulai 2015). Perbaikan 8pp — nyata tapi tidak mengubah kelas risiko.

---

## Kesimpulan

**K-3 dalam bentuk yang diucapkan video cenderung DIDUKUNG hanya untuk metode yang video pakai (hindsight top-15: −10,2pp s/d −19,3pp, n=15), dan cenderung TIDAK didukung untuk versi realistisnya** (step-aside down-shock menang 8/8 skenario, median +11,7pp, n=66 trigger). Perbedaannya bukan detail teknis: aturan video ikut melewatkan hari naik terbesar, aturan realistis tidak.

**Konflik X-1 tidak selesai jadi kemenangan salah satu pihak, tapi jadi pemisahan yang lebih tajam:**

1. Kesimpulan video ("keluar pasar itu mahal") **valid untuk timing yang dipicu magnitude pergerakan tanpa memandang arah** — dan itu memang bukan yang framework lakukan.
2. Varian yang paling dekat dengan K1 (step-aside hanya di Z5 / window K1) **kalah, median −2,9pp, n=22.** Jadi validasi ini **tidak memberi dukungan empiris untuk K1 sebagai alat menaikkan CAGR.** Tapi perlu dicatat batas ujinya: yang diuji adalah **exit 100% selama 5-10 hari**, sementara K1 adalah **jual parsial 20-30% dengan horizon bulanan** dan tujuan utamanya melunasi loan, bukan mengalahkan buy & hold. Uji ini bukan uji K1; dia hanya menutup satu jalur pembenaran yang mungkin dikira ada.
3. Varian alarm bear **inconclusive** karena replikasi alarm gagal (ON di 63-94% hari).

**Sebaran per cycle wajib dibaca:** hasil positif step-aside down-shock didominasi C1 (+140,5pp dari 2 tahun data era 2013-2014). Tanpa C1, gambarannya jauh lebih lemah: C2 −36,0pp, C3 +28,7pp, C4 +17,0pp. **Ini bukan strategi yang layak diadopsi** — n=66 trigger, satu cycle mendominasi, dan performanya berbalik total di satu cycle penuh.

**Satu hal yang tetap berdiri terlepas dari semua di atas:** kesimpulan "menghindari volatility itu mahal" **tidak boleh dipakai sebagai argumen melunakkan tangga staged cut LTV 58-65%.** Tangga itu mekanisme solvensi (menghindari likuidasi paksa), bukan upaya mengalahkan buy & hold — fungsi tujuannya berbeda, dan video tidak menguji leverage sama sekali.
