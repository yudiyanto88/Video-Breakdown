# Findings - Level mana yang paling sering menangkap dip di early bull?

**Tanggal validasi:** 26 Agustus 2026
**Script:** `analyze_pullback_catcher_level_early_bull.py`
**Event table:** `events_pullback_catcher_level_early_bull.csv`
**Data:** `data_master_all_metrics.csv` - 2010-07-18 s/d 2026-07-15 (n = 5.842 hari)

---

## Ringkasan sederhana

**Klaim video sebagian terkonfirmasi, dengan koreksi penting.** Pembicara menyebut dua level untuk add exposure saat dip di awal bull: **STH RP** dan **"true market mean"**. Data mendukung **STH RP** (menangkap 5 dari 21 pullback dalam +-3%, naik jadi 10/21 dalam +-5%) tapi **tidak mendukung true market mean** (1/21 dalam +-3%, dan tetap 1/21 dalam +-5%).

Temuan yang paling relevan untuk framework kita: **AVIV Mean menangkap 0 dari 21 pullback**. Alasannya struktural, bukan kebetulan - sepanjang jendela early-bull, AVIV Mean duduk **25-36% DI ATAS harga** (median per cycle: -36,2%, -25,9%, -5,1%, -27,2%). Di fase K5, AVIV Mean bukan lantai dip, dia **atap/target** (batas Z3/Z4). Jadi kalau ada yang memakai AVIV Mean sebagai level "catch the dip" di early bull, itu salah tempat - dan DF v2 memang **tidak** menyuruh begitu (K5 pakai aturan "pullback >=5% dari high lokal", bukan level).

---

## Definisi (dikunci sebelum menghitung)

- **Jendela early-bull** = tanggal unlock struktural (STH RP cross naik melewati RP, DF v2 bagian 0) s/d hari ke-3 dari streak pertama close > AVIV Upper >=3 hari berturut - **persis definisi "K5 selesai"** di DF v2
- **AVIV Upper** = `price_at_aviv_mean + 0.5 * (price_at_aviv_plus_1_sigma - price_at_aviv_mean)` (formula resmi framework, tidak dihitung ulang)
- **Pullback** = episode. Running high = max close sejak awal jendela. Episode DIBUKA saat close <= 0,95 x running high; trough = close terendah selama episode; episode DITUTUP saat close kembali di atas running high saat episode dibuka. **Satu episode = satu event** (sekaligus aturan merge: tidak ada dua episode tumpang tindih)
- **"Tertangkap level X"** = |trough_close / X(hari trough) - 1| <= 3%. Nilai level diambil **di hari trough** (at-gate untuk level, tidak ada nilai dari masa depan)
- **Overshoot ke bawah** = (trough_close / X - 1) x 100 saat trough di bawah X

**Jendela yang terbentuk (4 cycle):**

| Jendela | Durasi | Harga awal -> akhir |
|---------|--------|---------------------|
| 2012-04-19 -> 2013-04-09 | 355 hari | $5 -> $231 |
| 2015-11-03 -> 2017-05-03 | 547 hari | $405 -> $1.531 |
| 2019-05-07 -> 2019-07-10 | 64 hari | $5.778 -> $12.125 |
| 2023-03-01 -> 2024-02-29 | 365 hari | $23.649 -> $61.193 |

---

## n pullback & sebaran per cycle

**n total = 21 pullback >=5%** dari 4 jendela early-bull.

| Jendela | n pullback | median depth |
|---------|-----------|--------------|
| 2011 -> 2012 | 6 | -9,1% |
| 2013 -> 2015 | 6 | -25,7% |
| 2017 -> 2019 | **3** | -12,8% |
| 2021 -> 2023 | 6 | -15,2% |

**Independensi:** 21 pullback tapi hanya **4 early-bull independen**. Jendela 2019 cuma 64 hari (K5 lewat sangat cepat) sehingga cuma menyumbang 3 pullback, dan **0 catch untuk ketiga level** - jadi hasil "STH RP menang" praktis bersandar pada 3 cycle: 2012 (1/6), 2015-17 (2/6), 2023-24 (2/6). Tidak ada satu cycle yang mendominasi, tapi tiap cycle cuma menyumbang 1-2 hit.

---

## Hasil utama

| Level | Catch (+-3%) | dari n | hit % | median deviasi trough vs level | median overshoot ke bawah | n overshoot |
|-------|--------------|--------|-------|-------------------------------|---------------------------|-------------|
| **STH RP** | **5** | 21 | **24%** | **+2,4%** | **-4,9%** | 8 |
| True Market Mean | 1 | 21 | 5% | +11,8% | -18,8% | 6 |
| AVIV Mean | 0 | 21 | 0% | -34,0% | -37,6% | 18 |

Baca median deviasi: trough pullback rata-rata berhenti **+2,4% di atas STH RP** (sangat dekat), **+11,8% di atas true market mean** (masih jauh di atas), dan **-34,0% di bawah AVIV Mean** (level-nya jauh di atas kepala).

**Median overshoot ke bawah STH RP = -4,9%** (dari 8 kali trough menembus STH RP). Artinya kalau memakai STH RP sebagai level beli, ekspektasi realistisnya: sering kena, tapi **siap-siap tertembus ~5% ke bawah**, dan pernah sampai -10,2% (2023-07-18) dan -6,0% (2017-03-08).

### Hit per cycle

| Cycle | STH RP | True Market Mean | AVIV Mean |
|-------|--------|------------------|-----------|
| 2011 -> 2012 | 1/6 | 0/6 | 0/6 |
| 2013 -> 2015 | 2/6 | 1/6 | 0/6 |
| 2017 -> 2019 | 0/3 | 0/3 | 0/3 |
| 2021 -> 2023 | 2/6 | 0/6 | 0/6 |

**STH RP satu-satunya level yang bekerja di >1 cycle.** True market mean cuma sekali (2016-05-19), dan itu bertepatan dengan pullback dangkal (-6,7%) di mana STH RP dan TMM kebetulan hampir berhimpit.

### Sensitivitas toleransi (3 varian, semua dilaporkan)

| Level | +-3% | +-5% | +-7% |
|-------|------|------|------|
| **STH RP** | 5 | **10** | **11** |
| True Market Mean | 1 | 1 | 3 |
| AVIV Mean | 0 | 1 | 2 |

Kesimpulan tidak berubah di ketiga toleransi - STH RP unggul di semuanya, dan pada +-5% dia menangkap **hampir separuh (10/21)** pullback. Ini bukan hasil cherry-pick satu toleransi.

### Konteks - posisi level relatif harga sepanjang jendela

| Jendela | median harga vs STH RP | vs True Market Mean | vs AVIV Mean |
|---------|------------------------|---------------------|--------------|
| 2012-04 -> 2013-04 | +18,8% | +36,7% | **-36,2%** |
| 2015-11 -> 2017-05 | +11,0% | +19,0% | **-25,9%** |
| 2019-05 -> 2019-07 | +42,2% | +26,8% | -5,1% |
| 2023-03 -> 2024-02 | +11,0% | -0,4% | **-27,2%** |

Ini yang menjelaskan semuanya: di early bull harga bergerak **~11-19% di atas STH RP** (jarak yang bisa ditutup oleh pullback 5-20%), tapi **25-36% di bawah AVIV Mean** (jarak yang cuma bisa ditutup oleh crash, bukan pullback rutin).

---

## Cek Standar Validasi

1. **Definisi event** - jendela, pullback, trough, dan aturan merge dikunci di muka; jendela pakai definisi K5 milik DF v2 sendiri. OK
2. **n dilaporkan** - n=21 pullback, sebaran per cycle 6/6/3/6, **hanya 4 early-bull independen**. OK
3. **Anti-lookahead** - nilai level diambil di hari trough, bukan dari masa depan. (Identifikasi trough sendiri retrospektif - ini uji "level mana yang jadi lantai", bukan strategi eksekusi real-time; disebut eksplisit.) OK
4. **Independensi** - disebut: tiap cycle cuma menyumbang 1-2 hit; jendela 2019 terlalu pendek (3 pullback, 0 catch). OK
5. **Data mulai belakangan** - tidak berlaku, semua kolom full-history. OK
6. **Overfit** - 3 toleransi diuji dan semua dilaporkan; urutan level tidak berubah. OK

---

## Verdict

**KLAIM VIDEO SEBAGIAN TERKONFIRMASI - STH RP ya, true market mean tidak.** Dari **n=21 pullback >=5%** di 4 jendela early-bull (sebaran 6/6/3/6, **hanya 4 cycle independen**), STH RP menangkap **5/21 dalam +-3%** dan **10/21 dalam +-5%**, dengan trough median berhenti **+2,4% di atas** level dan median overshoot ke bawah **-4,9%**. True Market Mean cuma 1/21, AVIV Mean **0/21**. Untuk framework: ini **memperkuat, bukan mengubah**, aturan K5 yang sekarang - tapi memberi satu tambahan praktis yang berguna: **STH RP adalah level referensi terbaik untuk menempatkan tranche K5 di dalam pullback, dengan buffer ~5% ke bawah**, sedangkan AVIV Mean di fase ini adalah target ke atas, bukan lantai dip. **n=21 dari 4 cycle - low-to-medium confidence.**
