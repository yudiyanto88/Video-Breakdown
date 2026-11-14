# Findings — Realized Cap HODL Waves agregat band ≥3 bulan sebagai sinyal bear bottom

**Sumber klaim:** Bitcoin Magazine Pro — "This Signalled Every Bitcoin Bottom — We're 4.9% Away, So Why Risk It" (2026-05-25), `[00:06]`–`[01:31]`, `[10:47]`
**Tanggal validasi:** 2026-08-06
**Script:** [`analyze_rc_hodl_waves_ge3m.py`](analyze_rc_hodl_waves_ge3m.py)
**Event table:** [`events_rc_hodl_waves_ge3m.csv`](events_rc_hodl_waves_ge3m.csv), [`events_rc_hodl_waves_ge3m_peaks_b2.csv`](events_rc_hodl_waves_ge3m_peaks_b2.csv)
**Data:** `data_master_all_metrics.csv`, 2010-07-17 s/d 2026-07-15 (n = 5.843 hari harga valid)

---

## Klaim yang diuji

**B1.** Realized Cap HODL Waves, agregat band umur ≥3 bulan, saat ini ~84% — dan setiap kali level ini tercapai historically bertepatan dengan bear market low: *"literally the bear market lows practically every single time"*.

**B2 (turunan, seri yang sama dibalik).** Band <3 bulan yang spiking = bull market peak.

**B3 (byproduct).** Judul video "We're 4.9% Away" = jarak reading saat ini ke puncak reading bear sebelumnya, bukan 4,9% penurunan harga.

---

## Definisi event (ditetapkan SEBELUM menghitung)

- **Seri:** `rc_ge3m = 100 − (realized_cap_0-1d + realized_cap_1d-1w + realized_cap_1w-1m + realized_cap_1m-3m)`
  Dibangun dari 12 kolom band yang jumlah per barisnya persis 100,0000 (diverifikasi min=max=100,0000).
  ⚠ Kolom `realized_cap_1w` dan `realized_cap_1_2y` **sengaja dikeluarkan** — keduanya input RHODL yang nilainya duplikat dari `realized_cap_1d-1w` dan `realized_cap_1y-2y`; ikut menjumlahkan akan double-count.
- **Trigger absolut:** `rc_ge3m ≥ 84` (angka yang disebut pembicara).
- **Trigger relatif:** persentil trailing 4 tahun ≥ 95 (at-gate, hanya memakai data yang tersedia di tanggal itu — anti-lookahead).
- **Episode:** gap >30 hari antar hari trigger = episode baru.
- **Ground-truth bear low:** 2011-11-18, 2015-01-14, 2018-12-14, 2022-11-21 (4 low terkonfirmasi) + 2026-06-30 sebagai low **sementara/belum terkonfirmasi** (data berakhir 2026-07-15, jadi ini bukan bukti).
- **Window ground-truth:** ±60 hari.

**Sanity check anchor:** rc_ge3m 2026-05-25 = 83,631% (klaim pembicara ~84%) dan 2026-06-21 = 84,221%. Rekonstruksi kami cocok — **metrik ini fully reproducible dari data master, bukan black box.**

---

## Hasil

### 1. Recall — apakah bear low benar-benar terjadi di reading ≥84%?

| Bear low | rc_ge3m di hari low | Persentil (seluruh sejarah) | Maks dalam ±60 hari | ≥84 di hari low? |
|---|---|---|---|---|
| 2011-11-18 | **78,40%** | 81,2 | 81,30% | **TIDAK** |
| 2015-01-14 | **77,57%** | 78,0 | 81,64% | **TIDAK** |
| 2018-12-14 | **76,98%** | 76,9 | 79,93% | **TIDAK** |
| 2022-11-21 | **85,95%** | 98,2 | 88,57% | YA |
| 2026-06-30 *(belum terkonfirmasi)* | 84,37% | 95,3 | 84,71% | YA |

**Hanya 1 dari 4 bear low terkonfirmasi yang memenuhi threshold 84%.** Tiga bear low pertama berada di 77–78%, yaitu 6–7 poin di bawah angka yang disebut pembicara — dan tidak pernah menyentuh 84% bahkan dalam window ±60 hari. Klaim *"practically every single time"* **tidak didukung data**: yang benar adalah "satu kali dari empat, plus satu yang belum bisa dinilai".

### 2. Precision — dari semua hari yang memenuhi threshold, berapa yang dekat bear low?

| Aturan | n hari trigger | % dari sejarah | Precision (4 bear terkonfirmasi) |
|---|---|---|---|
| Absolut ≥84 | 397 | 6,8% | **28,5%** (113/397) |
| Persentil 4y ≥95 (at-gate) | 489 | 8,4% | **42,3%** (207/489) |

Sebaran hari trigger absolut ≥84 per cycle — **tiga dari empat cluster nol persen dekat bear low**:

| Cycle | n | Rentang | Dalam ±60d bear low |
|---|---|---|---|
| 2015 | 147 | 2015-05-21 .. 2015-10-26 | **0** |
| 2018 | 27 | 2019-03-06 .. 2019-04-01 | **0** |
| 2022 | 192 | 2022-09-05 .. 2023-10-26 | 113 |
| 2026 | 31 | 2026-06-15 .. 2026-07-15 | 0 |

Episode per episode (threshold 84):

| Episode | Durasi | Maks | Jarak awal episode ke bear low terdekat |
|---|---|---|---|
| 2015-05-21 .. 2015-10-26 | 147d | 87,27% | 127d **setelah** low 2015 |
| 2019-03-06 .. 2019-04-01 | 27d | 84,49% | 82d **setelah** low 2018 |
| 2022-09-05 .. 2023-01-12 | 130d | 88,57% | 77d sebelum low 2022 |
| 2023-02-12 .. 2023-03-25 | 42d | 85,58% | 83d setelah low 2022 |
| 2023-09-28 .. 2023-10-26 | 20d | 85,18% | 311d setelah low 2022 |
| 2026-06-15 .. 2026-07-15 | 31d | 84,71% | 15d (low belum terkonfirmasi) |

Yang paling merusak: **episode 2015 (147 hari, maks 87,27%) muncul 4 bulan SETELAH bear low 2015 sudah lewat**, dan episode Sep–Okt 2023 (85,18%) muncul saat harga sudah dalam bull recovery. Reading tinggi karena itu tidak memisahkan "dasar bear" dari "konsolidasi pasca-bear" maupun "awal bull".

### 3. Drift struktural — apakah threshold absolut punya dasar?

Puncak `rc_ge3m` per bear era (dari cycle peak ke bear low):

| Bear era | Puncak | Tanggal |
|---|---|---|
| 2011 | 78,40% | 2011-11-18 |
| 2015 | 78,56% | 2014-11-27 |
| 2018 | 79,50% | 2018-11-28 |
| 2022 | **88,57%** | 2022-10-25 |
| 2025-26 (ongoing) | 84,71% | 2026-07-13 |

Urutan: 78,4 → 78,6 → 79,5 → 88,6 → 84,7. **Tidak monoton**, dan lompatan 2018→2022 sebesar 9 poin jauh lebih besar dari drift bertahap tiga cycle sebelumnya. Ini menegaskan aturan CLAUDE.md soal threshold absolut: angka 84% bukan konstanta struktural, ia artefak dari cycle 2022 saja.

Aturan relatif (persentil 4y ≥95) memang menaikkan precision dari 28,5% → 42,3% dan menangkap bear 2011 & 2015 yang di-miss threshold absolut — tapi **gagal total di bear 2018** (tidak pernah trigger) dan **belum trigger sama sekali di 2026**. Jadi tidak ada varian yang lolos di semua cycle. Hanya 2 varian diuji (absolut & persentil), keduanya dilaporkan apa adanya — tidak ada grid search.

### 4. Lead/lag — apakah ada nilai timing?

| Bear low | Trigger absolut ≥84 pertama | Lead | Trigger persentil-95 pertama | Lead |
|---|---|---|---|---|
| 2011-11-18 | tidak pernah | — | 2011-10-20 | +29d |
| 2015-01-14 | tidak pernah | — | 2014-09-22 | +114d |
| 2018-12-14 | tidak pernah | — | tidak pernah | — |
| 2022-11-21 | 2022-09-05 | +77d | 2022-07-06 | +138d |
| 2026-06-30 *(tentatif)* | 2026-06-15 | +15d | tidak pernah | — |

Lead time yang tersedia berkisar 15–138 hari dengan hanya 2 observasi per varian. Dispersi selebar itu dengan n=2 tidak bisa dipakai untuk timing apapun.

### 5. B2 — sisi top (band <3 bulan)

| Cycle peak | Puncak lokal `100 − rc_ge3m` | Lag vs peak | AVIV Upper streak-end (Price Level KB §3.1) |
|---|---|---|---|
| 2011-06-08 | 98,09% @ 2011-07-13 | +35d | — |
| 2013-11-30 | 91,18% @ 2014-01-15 | +46d | — |
| 2017-12-16 | 85,60% @ 2018-01-07 | +22d | +31d |
| 2021-11-08 | 63,26% @ 2021-05-12 | **−180d** | +18d |
| 2025-10-06 | 41,49% @ 2025-11-23 | +48d | +9d |

Dua masalah fatal. Pertama, nilai puncaknya **runtuh monoton** dari 98% (2011) ke 41% (2025) — share band muda mengecil terus seiring supply matang, sehingga tidak ada level yang berlaku lintas cycle. Kedua, puncak lokal ini **hanya bisa diidentifikasi setelah fakta** (butuh window ±180 hari untuk tahu itu puncak), jadi nilai timing at-gate = nol. Di 2021 puncaknya bahkan terjadi 6 bulan **sebelum** cycle peak. Sebagai pembanding, AVIV Upper streak-end memberi lag +9 s/d +31 hari yang konsisten dan tersedia real-time.

### 6. B3 — arti "4.9%" di judul

| | Nilai |
|---|---|
| rc_ge3m 2026-05-25 | 83,63% |
| Puncak Bear 2022 | **88,57%** |
| Selisih | **+4,94 poin** (+5,91% relatif) |

**Interpretasi B3 terkonfirmasi, dengan presisi:** yang dimaksud "4,9%" adalah **4,94 poin persentase** menuju puncak reading bear 2022 — bukan 4,9% penurunan harga, dan bukan 4,9% relatif. Judul video karena itu mudah disalahbaca sebagai target harga. Perlu dicatat juga bahwa pembanding yang dia pakai (88,57%, bear 2022) adalah **outlier tertinggi dalam sejarah metrik ini** — tiga bear sebelumnya puncaknya hanya 78–80%, jauh di bawah reading hari ini. Terhadap tiga bear itu, reading 83,63% justru sudah **melewati** puncak mereka 4–5 poin.

---

## Kesimpulan

**NOT SUPPORTED sebagai klaim yang dinyatakan.** Klaim *"setiap bear market low"* gagal recall (**1 dari 4 bear low terkonfirmasi**, low 2011/2015/2018 semuanya di 77–78%, tidak pernah menyentuh 84% bahkan dalam ±60 hari) dan gagal precision (**28,5%** dari 397 hari trigger; cluster 2015, 2018, dan 2026 nol persen dekat bear low, dan episode 147 hari di 2015 muncul 4 bulan setelah low-nya lewat). Threshold 84% tidak punya dasar struktural — puncak per bear bergerak 78,4 / 78,6 / 79,5 / 88,6 dan tidak monoton, sehingga angka itu praktis merupakan artefak cycle 2022 saja. Varian relatif (persentil trailing 4 tahun ≥95) lebih baik (precision 42,3%) tapi gagal total di bear 2018 dan belum trigger di 2026, jadi tidak ada varian yang konsisten lintas cycle.

**Sisi top (B2) juga tidak menambah nilai:** puncak share band muda runtuh monoton 98% → 41% lintas cycle sehingga tidak ada level yang portabel, dan puncaknya hanya teridentifikasi setelah fakta (di 2021 bahkan 180 hari sebelum cycle peak). AVIV Upper sustained-breach yang sudah ada di framework memberi lag +9 s/d +31 hari secara konsisten dan tersedia real-time.

**Yang tetap berguna:** metrik ini **fully reproducible dari data master kita** (cocok dengan angka pembicara sampai 2 desimal), jadi kalau kelak ada versi yang diformulasi ulang secara relatif, kita bisa mengujinya tanpa perlu data eksternal. Dan arah kasarnya tidak salah — reading tinggi memang menandakan aktivitas mengering; yang salah adalah mengubahnya jadi threshold dan mengklaim presisi timing yang tidak dimilikinya.

**n dan sebaran:** 4 bear low terkonfirmasi (2011, 2015, 2018, 2022) + 1 low sementara 2026-06-30 yang **belum bisa dinilai** karena data berakhir 2026-07-15. Hasil precision didominasi cycle 2022 (192 dari 397 hari trigger, dan satu-satunya cycle dengan hit). Sebaran setipis ini berarti seluruh temuan di atas cenderung, bukan pasti — tapi arahnya konsisten di semua potongan yang diuji.

**Rekomendasi:** jangan adopsi sebagai trigger K4 maupun confirming context. Boleh dipakai sebagai narasi kualitatif "aktivitas mengering" saja, tanpa angka.
