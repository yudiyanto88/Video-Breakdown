# Findings - Pertumbuhan Realized Cap sebagai filter kualitas rally di bear

**Tanggal validasi:** 26 Agustus 2026
**Script:** `analyze_realized_cap_growth_reclaim_filter.py`
**Event table:** `events_realized_cap_growth_reclaim_filter.csv`
**Sample event:** 13 event "sentuhan STH RP dari bawah di bear" dari validasi 2026-08-04 (`../2026-08-04_bitcoins-top-buyers-are-finally-capitulating/events_sth_rp_resistance_bear.csv`) - **definisi event TIDAK diubah**
**Data:** `data_master_all_metrics.csv` - 2010-07-17 s/d 2026-07-15

---

## Ringkasan sederhana

**TIDAK KONKLUSIF.** Klaim video ("rally yang bertahan diikuti masuknya modal riil; rally squeeze murni tidak") tidak bisa diuji secara bermakna dengan sample yang ada, karena **hanya ada 1 event dari 13 yang masuk kategori "BERTAHAN"** (2023-01-11, bear 2021). Satu titik data tidak bisa jadi dasar threshold apapun.

Lebih buruk lagi: satu-satunya event BERTAHAN itu punya pertumbuhan realized cap **at-gate yang NEGATIF** (-0,65% dalam 14 hari, -1,47% dalam 30 hari) - **paling rendah dari seluruh 13 event**. Jadi kalaupun ada pola, arahnya justru **berlawanan** dengan klaim video. Ini konsisten dengan mekanik realized cap: dia baru naik setelah koin ditransaksikan pada harga lebih tinggi, jadi dia **lagging**, bukan leading.

---

## Definisi (dikunci sebelum menghitung)

- Sample = 13 event sentuhan STH RP dari bawah di bear market (definisi dari validasi 2026-08-04, tidak diubah sedikitpun)
- **A. At-gate murni** (bisa jadi filter di hari event): `d_rc_pre14` / `d_rc_pre30` = % perubahan `realized_cap_usd` dari (t-14)/(t-30) ke t
- **B. Konfirmasi** (baru tersedia 14/30 hari setelah event - **BUKAN gate hari-H**): `d_rc_post14` / `d_rc_post30`
- Label outcome (dari file event lama): **BERTAHAN** = outcome BREAK DAN `balik_bawah_sthrp_dlm_90d` = False. **GAGAL** = sisanya
- `realized_cap_usd` tersedia full-history sejak 2010-07-17 - **tidak ada masalah data mulai belakangan** di uji ini

---

## Tabel lengkap (n=13)

| Cycle | Event | Outcome lama | Label | pre14% | pre30% | post14% | post30% | ret 30d |
|-------|-------|--------------|-------|--------|--------|---------|---------|---------|
| 2011 | 2011-12-31 | BREAK | GAGAL | +2,46 | +2,72 | +6,23 | +7,75 | +16,7% |
| 2013 | 2014-05-30 | BREAK | GAGAL | +3,14 | +3,26 | +4,05 | +5,56 | -3,2% |
| 2013 | 2015-03-09 | BREAK | GAGAL | -0,32 | -0,61 | +0,31 | -0,13 | -15,5% |
| 2013 | 2015-06-16 | BREAK | GAGAL | -0,01 | -0,58 | +0,28 | +0,73 | +10,7% |
| 2017 | 2018-07-24 | BREAK | GAGAL | +0,44 | -1,23 | -0,00 | -0,62 | -22,1% |
| 2017 | 2018-09-01 | DITOLAK | GAGAL | +0,63 | -0,39 | -0,55 | -0,90 | -8,0% |
| 2017 | 2018-11-07 | DITOLAK | GAGAL | -0,22 | -1,33 | -2,35 | -5,26 | -47,4% |
| 2017 | 2019-02-23 | DITOLAK | GAGAL | -0,51 | -1,43 | -0,33 | -0,59 | -4,3% |
| 2021 | 2022-03-27 | BREAK | GAGAL | +1,20 | +1,64 | +0,51 | +0,59 | -18,6% |
| 2021 | 2022-10-29 | DITOLAK | GAGAL | -0,11 | -0,59 | -1,51 | -4,24 | -22,1% |
| **2021** | **2023-01-11** | BREAK | **BERTAHAN** | **-0,65** | **-1,47** | **+0,60** | **+0,84** | **+20,6%** |
| 2025 | 2026-01-14 | DITOLAK | GAGAL | +0,29 | -0,05 | -0,44 | -2,34 | -29,0% (censored) |
| 2025 | 2026-04-26 | BREAK | GAGAL | -0,06 | -0,11 | +0,25 | +0,11 | -3,6% (censored) |

**Sebaran per cycle:** 2011 = 1 (0 BERTAHAN), 2013 = 3 (0), 2017 = 4 (0), 2021 = 3 (**1 BERTAHAN**), 2025 = 2 (0, keduanya censored).

---

## Apakah delta realized cap memisahkan BERTAHAN dari GAGAL?

| Metrik | BERTAHAN (n=1) | GAGAL (n=12) median | GAGAL rentang | Memisahkan? |
|--------|----------------|---------------------|---------------|-------------|
| `d_rc_pre14` (at-gate) | -0,65% | +0,14% | -0,51% s/d +3,14% | **TIDAK** - 12/12 event GAGAL punya nilai >= BERTAHAN |
| `d_rc_pre30` (at-gate) | -1,47% | -0,48% | -1,43% s/d +3,26% | **TIDAK** - 12/12 |
| `d_rc_post14` (konfirmasi) | +0,60% | +0,12% | -2,35% s/d +6,23% | **TIDAK** - 2/12 masih >= BERTAHAN |
| `d_rc_post30` (konfirmasi) | +0,84% | -0,36% | -5,26% s/d +7,75% | **TIDAK** - 2/12 masih >= BERTAHAN |

Versi konfirmasi (post14/post30) kelihatan "lebih baik" (cuma 2 dari 12 event GAGAL yang melewati ambang BERTAHAN), tapi: (a) **basisnya 1 event**, (b) nilai ambangnya (+0,60% / +0,84%) sangat kecil dan berada persis di tengah distribusi normal realized cap, (c) dua event GAGAL yang melewati ambang justru event dengan realized cap tumbuh **paling kencang** (2011-12-31: +7,75%; 2014-05-30: +5,56%) - keduanya rally bear yang gagal total. Artinya **realized cap tinggi TIDAK menjamin apa-apa**.

**Konteks distribusi:** perubahan `realized_cap_usd` 30 hari sepanjang sejarah punya persentil 10% = -1,78%, median = +2,42%, persentil 90% = +22,93%. Semua 13 event ada di rentang -5,26% s/d +7,75%, yaitu **di paruh bawah distribusi** - masuk akal, karena semua terjadi di bear market. Nilai 30 hari terakhir (2026-07-15) = **-1,28%** (persentil ~10-15%, artinya modal riil justru masih keluar).

---

## Kandidat 2025-26

| Event | Outcome | pre14 | pre30 | post14 | post30 |
|-------|---------|-------|-------|--------|--------|
| 2026-01-14 | DITOLAK | +0,29% | -0,05% | -0,44% | -2,34% |
| 2026-04-26 | BREAK, balik ke bawah | -0,06% | -0,11% | +0,25% | +0,11% |

Kedua-duanya **GAGAL** menurut label. Event 2026-04-26 kebetulan punya profil realized cap yang mirip dengan satu-satunya event BERTAHAN (pre negatif tipis, post positif tipis) - dan **tetap gagal**. Ini bukti langsung bahwa filter yang diusulkan tidak diskriminatif.

---

## Cek Standar Validasi

1. **Definisi event** - dipakai apa adanya dari validasi 2026-08-04, tidak diubah untuk menyelamatkan hasil. OK
2. **n dilaporkan** - n=13 total, **BERTAHAN cuma n=1**, sebaran per cycle 1/3/4/3/2. OK
3. **Anti-lookahead** - dipisah tegas antara versi at-gate (pre14/pre30) dan versi konfirmasi (post14/post30) yang **secara eksplisit BUKAN gate hari-H**. OK
4. **Independensi** - satu-satunya BERTAHAN berasal dari cycle 2021 saja; hasilnya **100% didominasi 1 event dari 1 cycle**. OK
5. **Data mulai belakangan** - tidak berlaku, `realized_cap_usd` full-history. Tapi 2 event 2025-26 **censored** (window 90 hari belum penuh). OK
6. **Overfit** - tidak ada threshold yang dicari-cari; justru dilaporkan bahwa threshold apapun di sini akan overfit ke 1 event. OK

---

## Verdict

**TIDAK KONKLUSIF - tidak bisa dipakai, dan tidak boleh dipoles.** Sample-nya cuma punya **1 event BERTAHAN dari 13** (2023-01-11, cycle 2021), jadi pemisahan apapun yang terlihat sebenarnya adalah threshold yang di-fit ke satu titik data. Delta `realized_cap_usd` at-gate (pre14/pre30) **jelas tidak memisahkan** - 12 dari 12 event GAGAL punya nilai sama atau lebih tinggi dari event BERTAHAN, dan arah nilainya justru berlawanan dengan klaim video. Versi konfirmasi (post14/post30) sedikit lebih rapi tapi ambangnya tipis (+0,6%/+0,8%) dan dua rally bear yang gagal keras justru punya pertumbuhan realized cap tertinggi. Rekomendasi: **hipotesis "modal riil sebagai filter rally" TIDAK ditolak maupun diterima - butuh sample bear-rally yang berhasil jauh lebih banyak, yang secara struktural baru akan tersedia setelah beberapa siklus lagi.** Jangan masukkan ke framework.
