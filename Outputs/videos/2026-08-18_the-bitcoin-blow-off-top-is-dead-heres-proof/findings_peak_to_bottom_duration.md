# Findings — Durasi Peak->Bottom & Gate K4 Lantai Waktu

**Video:** On-Chain Mind — "The Bitcoin Blow-Off Top Is Dead (Here's Proof)" (2026-08-18)
**Tanggal validasi:** 2026-08-19
**Script:** `analyze_peak_to_bottom_duration.py`
**Data pendukung:** `events_peak_to_bottom_duration.csv`
**Sumber data:** `data_master_all_metrics.csv` (`btc_price`, `realized_price`, `sth_cost_basis`)

---

## Ringkasan sederhana

Insight #5 video (bottom->peak ~35 bulan) dibalik arahnya, karena bottom baru diketahui ex-post
sehingga tidak bisa dipakai untuk keputusan. Yang bisa dipakai adalah **peak->bottom** — peak
sudah lewat (2025-10-06), jadi jam-nya sudah jalan.

Hasilnya justru lebih rapi daripada bottom->peak: **13,5 / 11,9 / 12,4 bulan** di 3 cycle utama
(spread cuma 1,6 bulan). Dan gate K4 lantai waktu (>=9 bulan sejak peak DAN close < RP) nyala
**0,8-3,4 bulan sebelum bottom aktual di 3/3 cycle utama** — konsisten terlalu cepat, tidak
pernah terlambat. Itu justru sesuai desain framework (DCA 5%/bulan, sisakan amunisi).

Per data terakhir (2026-07-15): sudah 9,3 bulan sejak peak, tapi harga $65.098 masih **di atas**
RP $52.740 — **gate lantai waktu belum nyala.**

---

## Definisi event (dikunci di muka)

- **PEAK** = close tertinggi yang dikonfirmasi tidak terlampaui selama >=365 hari berikutnya
  (bukan sekadar local high) — aturan ini otomatis membuang kandidat seperti Apr 2021
- **BOTTOM** = close terendah antara peak dan hari harga menembus ATH lama lagi
- **Gate lantai waktu** = hari pertama (t - peak >= 9 bulan kalender) DAN (close < RP). Nilai RP
  tersedia di hari itu -> tidak ada lookahead
- **n = 3 cycle utama tertutup + 1 berjalan**, plus 1 observasi era awal (peak Jun 2011) yang
  dilaporkan terpisah sebagai outlier

## Durasi peak -> bottom

| Peak | P_peak | Bottom | P_bottom | Drawdown | Hari | Bulan | Status |
|---|---|---|---|---|---|---|---|
| 2011-06-08 | $29,60 | 2011-11-18 | $2,05 | -93,1% | 163 | **5,4** | tertutup (era awal — outlier) |
| 2013-11-29 | $1.156,12 | 2015-01-14 | $178,50 | -84,6% | 411 | 13,5 | tertutup |
| 2017-12-16 | $19.538,13 | 2018-12-14 | $3.281,06 | -83,2% | 363 | 11,9 | tertutup |
| 2021-11-08 | $67.524,70 | 2022-11-21 | $15.774,48 | -76,6% | 378 | 12,4 | tertutup |
| 2025-10-06 | $124.714,85 | 2026-06-30* | $58.460,01* | -53,1%* | 267* | 8,8* | **BERJALAN** |

*bottom sementara per data 2026-07-15 — bisa berubah.

3 cycle utama: **mean 12,6 bulan, min 11,9, max 13,5, spread 1,6 bulan.** Observasi 2011
(5,4 bulan) dilaporkan terpisah — likuiditas & kualitas data 2011 sangat berbeda; kalau ikut
dihitung, mean turun ke 10,8 bulan dan rentang melebar ke 5,4-13,5.

---

## Hipotesis & verdict

### H1 — Durasi peak->bottom lebih stabil daripada bottom->peak
**Verdict: YA di 3 cycle utama.** Peak->bottom 11,9-13,5 bulan (spread 1,6 bulan / 13% dari
mean). Bandingkan bottom->peak: 24,4 / 35,1 / 34,8 / 34,5 bulan — 3 cycle terakhir memang rapat
(~35 bulan) tapi C0 meleset 10,7 bulan. Tambahan: peak->bottom punya keunggulan praktis —
titik awalnya (peak) bisa dikenali mendekati real time lewat K1/alarm bear, sedangkan bottom
baru diketahui berbulan-bulan setelahnya. **Tetap n=3 tertutup — sampel sangat kecil.**

### H2 — Gate K4 lantai waktu (>=9 bulan + close < RP) nyala terlalu cepat atau terlambat?
**Verdict: KONSISTEN TERLALU CEPAT (0,8-3,4 bulan sebelum bottom), tidak pernah terlambat, di
3/3 cycle utama.**

| Peak | Harga pertama close < RP | Bulan ke- | Streak terpanjang < RP | Total hari < RP | Gate nyala | Bulan ke- | Bottom | Gate vs bottom |
|---|---|---|---|---|---|---|---|---|
| 2011-06-08 | 2011-08-06 | 1,9 | 102 hari | 153 | 2012-03-08 | 9,0 | 2011-11-18 | **+111 hari (+3,6 bln, TERLAMBAT)** |
| 2013-11-29 | 2014-10-04 | 10,2 | 196 hari | 229 | 2014-10-04 | 10,2 | 2015-01-14 | -102 hari (-3,4 bln) |
| 2017-12-16 | 2018-11-19 | 11,1 | 134 hari | 134 | 2018-11-19 | 11,1 | 2018-12-14 | -25 hari (-0,8 bln) |
| 2021-11-08 | 2022-06-13 | 7,1 | 68 hari | 180 | 2022-08-19 | 9,3 | 2022-11-21 | -94 hari (-3,1 bln) |
| 2025-10-06 | **BELUM PERNAH < RP** | — | 0 | 0 | belum | — | berjalan | — |

Bacaan:
- Di 3 cycle utama, gate nyala **sebelum** bottom -> pembelian pertama masih kena penurunan
  lanjutan. Ini persis alasan framework memakai 5%/bulan (bukan 10%) dan mencatat "worst case
  beli pertama 2014 masih turun -46%". Divalidasi ulang di sini: gate 2014-10-04, bottom
  2015-01-14, 102 hari sesudahnya.
- Bulan pertama close < RP bervariasi lebar: 1,9 / 10,2 / 11,1 / 7,1 bulan. Di 2013-14 dan
  2017-18, syarat "close < RP" baru terpenuhi SETELAH lantai 9 bulan lewat, jadi **RP-lah yang
  jadi pengikat**, bukan lantai waktunya. Di 2021-22 sebaliknya — harga sudah di bawah RP sejak
  bulan 7,1, dan lantai 9 bulan yang menahan (menunda 2,2 bulan).
- Kasus 2011 adalah satu-satunya di mana lantai 9 bulan bikin **terlambat** (+3,6 bulan setelah
  bottom), karena seluruh bear-nya cuma 5,4 bulan. Risiko itu belum pernah terulang sejak 2013.
- **Durasi bertahan di bawah RP:** 196 / 134 / 68 hari (streak terpanjang) — bukan sentuhan
  sekejap, jadi gate cenderung tidak flicker.

### H3 — Sensitivitas: kalau peak C2 dipilih Apr 2021, apakah masih 12-13,4 bulan?
**Verdict: TIDAK — jatuh jauh di luar rentang.** Peak Apr 2021 = 2021-04-13 $63.551,33 ->
bottom 2022-11-21 = 587 hari = **19,3 bulan**, vs 12,4 bulan memakai peak Nov 2021. Rentang
3 cycle utama 11,9-13,5 bulan -> varian ini **DI LUAR**.
Tapi: aturan peak yang dipakai (close tertinggi yang tidak terlampaui >=365 hari) **secara
otomatis menolak Apr 2021**, karena harga menembusnya pada Okt 2021. Jadi ambiguitas ini
terselesaikan oleh definisi, bukan oleh pilihan analis. Efek ke gate: varian Apr-2021 membuat
gate nyala 2022-06-13, yaitu **161 hari sebelum bottom** (vs 94 hari) — makin cepat, makin
banyak amunisi terbakar sebelum dasar.

### H4 — Posisi pasar sekarang
**Verdict: gate lantai waktu BELUM nyala per 2026-07-15.**
- Peak 2025-10-06 $124.715; per 2026-07-15 harga $65.098, RP $52.740, STH RP $67.143
- Bulan sejak peak = **9,3** -> syarat waktu (>=9,0) **sudah terpenuhi**
- Syarat `close < RP` -> **BELUM** (harga masih ~23% di atas RP)
- Drawdown sejauh ini -53,1% (low sementara 2026-06-30 $58.460) — jauh lebih dangkal dari
  3 bear sebelumnya (-76,6% s/d -84,6%)
- Proyeksi jendela bottom dari 3 cycle utama (11,9-13,5 bulan sejak peak): **~2026-10-03 s/d
  2026-11-20**. Kalau observasi 2011 (5,4 bulan) ikut dihitung, batas bawah mundur ke 2026-03-19
  (yang sudah lewat) — artinya kemungkinan "bottom sudah terjadi" tidak bisa dikesampingkan.

---

## Catatan rigor

- **n = 3 cycle tertutup utama + 1 berjalan + 1 outlier era awal.** Empat cycle tetap sampel
  kecil; "12,6 bulan" bukan angka presisi, cuma pusat massa dari 3 observasi.
- **Dominasi:** rentang sempit 11,9-13,5 bulan sepenuhnya bergantung pada 3 observasi yang
  kebetulan berdekatan. Masuknya 2011 (5,4 bulan) langsung melebarkan spread jadi 8,1 bulan —
  jadi kerapatan itu **rapuh**, bukan hukum alam.
- **Anti-lookahead:** peak dikonfirmasi butuh 365 hari ke depan, jadi label "peak terkonfirmasi"
  memang ex-post. Tapi gate lantai waktu itu sendiri hanya memakai (tanggal, harga, RP) yang
  tersedia hari itu -> gate-nya bebas lookahead; yang perlu diasumsikan real-time cuma
  "peak sudah lewat", dan itu tugas K1/alarm bear.
- **Data lag:** master terakhir 2026-07-15 vs validasi 2026-08-19 — status "close < RP" bisa
  sudah berubah dalam sebulan terakhir. **Perlu cek ulang setelah data di-update.**

## Verdict akhir

**Durasi peak->bottom cenderung lebih berguna daripada bottom->peak versi video: 13,5 / 11,9 /
12,4 bulan (n = 3 cycle utama tertutup, mean 12,6, spread hanya 1,6 bulan), plus 1 outlier era
awal 2011 (5,4 bulan) dan 1 cycle berjalan (8,8 bulan per 2026-07-15).** Gate K4 lantai waktu
nyala 0,8-3,4 bulan **sebelum** bottom aktual di 3/3 cycle utama — konsisten cepat, tidak pernah
telat, sesuai desain DCA 5%/bulan. Satu-satunya kasus telat adalah 2011 (+3,6 bulan), di mana
seluruh bear hanya 5,4 bulan. Per data terakhir, syarat waktu sudah terpenuhi (9,3 bulan sejak
peak 2025-10-06) tapi syarat close < RP **belum**, jadi lantai waktu belum aktif.

**Usulan (bukan penerapan):** tidak ada perubahan gate. Cukup tambahkan catatan di teks K4
bahwa lantai waktu historis nyala ~1-3,5 bulan sebelum dasar, dan bahwa **RP-lah pengikat yang
sesungguhnya** di 2/3 cycle utama (2014, 2018) — lantai 9 bulan hanya mengikat di 2022.
