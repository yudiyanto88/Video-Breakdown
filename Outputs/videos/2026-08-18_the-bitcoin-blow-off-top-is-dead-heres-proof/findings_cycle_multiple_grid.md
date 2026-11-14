# Findings — Grid Multiple 4-Cycle, Share Log-Return, Sensitivitas Tanggal Bottom

**Video:** On-Chain Mind — "The Bitcoin Blow-Off Top Is Dead (Here's Proof)" (2026-08-18)
**Tanggal validasi:** 2026-08-19
**Script:** `analyze_cycle_multiple_grid.py`
**Data pendukung:** `events_cycle_multiple_grid.csv`, `events_cycle_share_logreturn.csv`,
`events_cycle_multiple_sensitivity.csv`
**Sumber data:** `data_master_all_metrics.csv`, kolom `btc_price` saja

---

## Ringkasan sederhana

Aritmetika video **reproduce** — angka-angkanya benar untuk 3 cycle yang dia pakai. Masalahnya
bukan hitungan, tapi (a) cycle 2011-13 dibuang, dan (b) hasilnya rapuh terhadap pilihan tanggal
bottom. Begitu C0 dimasukkan, ketiga pola video patah: 12-bulan bukan "flat 2,3x" (C0 = 5,68x),
24-bulan bukan naik pelan (C0 = 336x), dan "final leg selalu ~11 bulan" hanya 0,4 bulan di C0.
Geser tanggal bottom +/-45 hari saja sudah menggoyang multiple 12-bulan sampai 33-59% — jauh di
atas ambang robust +/-20% yang ditetapkan di muka.

Satu bagian video yang bertahan: **gain memang mengecil dari cycle ke cycle**. Tapi itu
diminishing return biasa, bukan bukti "gain pindah ke depan".

---

## Definisi & metode

- Bottom/peak dideteksi sendiri dari `btc_price` (min/max dalam jendela pencarian per cycle)
- Multiple bulan-m = `close(bottom + m bulan kalender) / close(bottom)`; harga diambil dari
  close terakhir yang tersedia <= tanggal itu (tanpa lookahead)
- **Share log-return** = `ln(P_t/P_bottom) / ln(P_peak/P_bottom)` — menormalisasi amplitudo,
  supaya "front-loading" bisa dibedakan dari "sekadar diminishing"
- **t50** = bulan pertama share log-return >= 50%, dilaporkan absolut DAN sebagai fraksi
  panjang bottom->peak
- **Sensitivitas** tanggal bottom: 5 varian PRE-REGISTERED (-45, -15, 0, +15, +45 hari),
  P_bottom = close di tanggal geseran itu. Semua varian dilaporkan; tidak ada yang dipilih
  karena hasilnya rapi
- **n = 4 cycle**, C0 (2011-13) sengaja disertakan justru karena video membuangnya

## Tanggal siklus

| Cycle | Bottom | P_bottom | Peak | P_peak | Peak multiple | bottom->peak |
|---|---|---|---|---|---|---|
| C0 | 2011-11-18 | $2,05 | 2013-11-29 | $1.156,12 | 563,9x | 24,4 bln |
| C1 | 2015-01-14 | $178,50 | 2017-12-16 | $19.538,13 | 109,5x | 35,1 bln |
| C2 | 2018-12-14 | $3.281,06 | 2021-11-08 | $67.524,70 | 20,6x | 34,8 bln |
| C3 | 2022-11-21 | $15.774,48 | 2025-10-06 | $124.714,85 | 7,9x | 34,5 bln |

---

## Hipotesis & verdict

### H0 — Aritmetika video reproduce?
**Verdict: YA.** 12-bulan video 2,36/2,23/2,27x vs hitungan kami 2,41/2,17/2,27x. Peak multiple
video 107/21/~8x vs 109,5/20,6/7,9x. Final leg video 23,7/3,47/1,27x vs 23,87/3,51/1,27x.
Selisih <5% — konsisten dengan beda 1-2 hari tanggal bottom/peak. **Yang dipersoalkan bukan
hitungannya, tapi sampel & robustness-nya.**

### H1 — "Front-end flat ~2,3x di 12 bulan pertama"
**Verdict: GAGAL dengan 4 cycle, DAN tidak robust bahkan dengan 3 cycle.**

| Cycle | 6 bln | 12 bln | 18 bln | 24 bln | Peak | 24bln->peak | return leg akhir |
|---|---|---|---|---|---|---|---|
| C0 | 2,50x | **5,68x** | 59,78x | **335,99x** | 563,9x | **0,4 bln** | 1,68x |
| C1 | 1,61x | 2,41x | 3,70x | 4,59x | 109,5x | 11,1 bln | 23,87x |
| C2 | 2,65x | 2,17x | 2,85x | 5,87x | 20,6x | 10,8 bln | 3,51x |
| C3 | 1,70x | 2,27x | 4,45x | 6,24x | 7,9x | 10,5 bln | 1,27x |

C0 memberi **5,68x** di 12 bulan — 2,5x lipat dari "flat 2,3x". Klaim "3 kali berturut-turut"
menjadi "3 dari 4, dan yang keempat sangat jauh".

**Sensitivitas (ini yang paling merusak):** spread multiple 12-bulan akibat geser tanggal bottom
+/-45 hari — C0 55,1%, C1 58,8%, C2 33,1%, C3 36,9%. **Keempatnya di atas ambang +/-20%.**
Rentang multiple 12-bulan lintas 4 cycle x 5 varian = **0,99x s/d 5,68x** (n=20 kombinasi).
Bahkan kalau C0 dibuang seperti video: **0,99x s/d 2,67x** — yaitu "flat 2,3x" bisa jadi
"0,99x" (tidak naik sama sekali) hanya dengan menggeser bottom C1 45 hari lebih awal.
**"Flat 2,3x" TIDAK ROBUST.**

Spread horizon lain lebih parah lagi: 6-bulan sampai 68,1% (C2), 24-bulan sampai 92,7% (C0).

### H2 — "24-bulan multiple naik steady (4,55 -> 6,11 -> 6,25x)"
**Verdict: GAGAL.** C0 = 335,99x. Pola "naik pelan" hanya muncul kalau cycle terbesar dibuang.

### H3 — "Peak multiple runtuh order-of-magnitude" (107 -> 21 -> 8x)
**Verdict: BENAR, dan justru MAKIN kuat dengan C0.** 563,9 -> 109,5 -> 20,6 -> 7,9x —
monoton turun di 4/4 cycle, rasio antar cycle 5,1x / 5,3x / 2,6x. Ini satu-satunya klaim video
yang bertambah kuat ketika sampel dilengkapi. Tetap n=4 (sampel kecil).

### H4 — "Year 3 = kuburan return; final leg 24-bulan->peak selalu ~11 bulan"
**Verdict: GAGAL sebagai pola; BENAR sebagai observasi terpisah.** Jendela 24bln->peak: C0
**0,4 bulan**, C1 11,1, C2 10,8, C3 10,5. "Selalu ~11 bulan" adalah artefak dari 3 cycle yang
kebetulan berdurasi ~35 bulan; C0 berdurasi 24,4 bulan sehingga jendela itu nyaris nol. Return
leg akhir memang turun (C1 23,87x -> C2 3,51x -> C3 1,27x), tapi C0 justru cuma 1,68x — jadi
"decay monoton" pun tidak berlaku dengan 4 cycle.

### H5 — Front-loading nyata atau sekadar diminishing? (uji yang tidak dilakukan video)
**Verdict: TIDAK ADA BUKTI FRONT-LOADING yang konsisten.**

| Cycle | share 6bln | 12bln | 18bln | 24bln | t50 (bulan) | **t50 / durasi** |
|---|---|---|---|---|---|---|
| C0 | 14,4% | 27,4% | 64,6% | 91,8% | 16 | 0,66 |
| C1 | 10,2% | 18,7% | 27,9% | 32,4% | 29 | **0,83** |
| C2 | 32,2% | 25,7% | 34,6% | 58,5% | 23 | 0,66 |
| C3 | 25,6% | 39,6% | 72,2% | 88,5% | 15 | **0,43** |

Urut waktu, t50/durasi = 0,66 -> 0,83 -> 0,66 -> 0,43. **Tidak monoton.** Cycle 2015-17 justru
yang PALING back-loaded (0,83) padahal video memasukkannya ke kelompok "front-end stabil".
C3 memang paling front-loaded (0,43), tapi itu 1 observasi dari 4, dan C0 (2011-13, cycle
paling "blow-off" dalam narasi umum) justru sama dengan C2 di 0,66. Kesimpulan: yang berubah
lintas cycle terutama **amplitudo** (peak multiple runtuh), bukan bentuk kurvanya.

### H6 — "6-bulan bisa lebih besar dari 12-bulan"
**Verdict: BENAR tapi jarang — 1 dari 4 cycle.** Pada grid bulanan hanya C2 (2,65x di bulan 6
vs 2,17x di bulan 12). Angka "4x di bulan ke-6" yang disebut video untuk 2019 adalah **high
intramonth** (2019-06-26 $12.830 / $3.281 = 3,91x), bukan titik grid bulan-6 — memakai high
intramonth untuk satu sisi dan close bulanan untuk sisi lain melebih-lebihkan efeknya.

---

## Catatan rigor

- **n = 4 cycle.** Bahkan sebelum bicara robustness, ini terlalu kecil untuk menyimpulkan
  "blow-off top sudah mati". Framework sendiri menyatakan 3-4 cycle = panduan arah, bukan presisi.
- **Independensi:** keempat observasi berasal dari satu aset & satu rezim regulasi yang terus
  berubah; tidak ada yang benar-benar independen.
- **Anti-lookahead:** tidak relevan sebagai sinyal — semua metrik di sini hanya bisa dihitung
  ex-post (bottom & peak baru diketahui belakangan). Ini deskriptif, **bukan alat keputusan.**
- **Overfit:** hanya 5 varian tanggal bottom yang dicoba, ditetapkan di muka, semuanya
  dilaporkan. Tidak ada tanggal bottom yang dipilih karena hasilnya rapi.
- **Seleksi sampel:** membuang C0 mengubah 3 dari 5 klaim dari "gagal" jadi "berhasil". Ini
  bentuk survivorship/selection bias paling langsung.

## Verdict akhir

**Sebagian besar pola video tidak bertahan dengan sampel penuh (n = 4 cycle: C0, C1, C2, C3).**
"Flat ~2,3x di 12 bulan" gagal (C0 = 5,68x) DAN tidak robust — geser tanggal bottom +/-45 hari
menggeser angkanya 33-59% (ambang robust yang dipatok di muka: 20%), rentang penuh 0,99x-5,68x.
"24-bulan naik steady" gagal (C0 = 336x). "Final leg selalu ~11 bulan" gagal (C0 = 0,4 bulan).
Yang bertahan dan malah menguat adalah **runtuhnya peak multiple**: 563,9 -> 109,5 -> 20,6 ->
7,9x, monoton di 4/4 cycle. Uji share log-return (yang video tidak lakukan) menunjukkan
t50/durasi = 0,66 / 0,83 / 0,66 / 0,43 — **tidak monoton**, jadi tidak ada bukti "gain pindah
ke depan"; yang mengecil adalah amplitudonya.

**Implikasi framework:** tidak ada perubahan yang diusulkan. Metrik ini ex-post dan tidak
actionable. Nilai satu-satunya = memperkuat prinsip framework yang sudah ada bahwa **threshold
absolut tidak reliable antar cycle** — di sini bahkan multiple bottom-relatif pun tidak.
