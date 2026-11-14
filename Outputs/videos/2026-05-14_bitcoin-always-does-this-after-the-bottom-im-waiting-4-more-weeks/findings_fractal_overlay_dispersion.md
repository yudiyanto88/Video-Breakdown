# Findings — Falsifikasi metode bar-pattern fractal overlay (post-low)

**Tanggal validasi:** 5 Agustus 2026
**Script:** [`analyze_fractal_overlay_dispersion.py`](analyze_fractal_overlay_dispersion.py)
**Event CSV:** [`events_fractal_overlay_dispersion.csv`](events_fractal_overlay_dispersion.csv)
**Data:** `data_master_all_metrics.csv`, **berakhir 2026-07-15**

Yang diuji adalah **metodenya**, bukan salah satu fractal. Kalau jalur post-low antar cycle sangat
berbeda satu sama lain, overlay manapun tidak punya isi prediktif — terlepas dari fractal mana yang dipilih.

---

## Definisi event (ditetapkan sebelum menghitung)

- **ATH cycle** = max close dalam window cycle yang ditetapkan a priori (2011, 2013-15, 2017-19, 2021-23, 2025-26)
- **Cycle low** = min close antara ATH dan akhir window
- **Jalur post-low** = `P(t)/P(low)` untuk t = 0…180 hari kalender sejak cycle low
- Cycle 2025-26 **berjalan (censored)** — tidak dihitung setara 4 bear selesai

| Cycle | ATH | Cycle low | Hari ATH→low | Max DD |
|---|---|---|---|---|
| 2011 | $30 @ 2011-06-08 | $2 @ 2011-11-18 | 163 | −93,1% |
| 2013-15 | $1.156 @ 2013-11-29 | $178 @ 2015-01-14 | 411 | −84,6% |
| 2017-19 | $19.538 @ 2017-12-16 | $3.281 @ 2018-12-14 | 363 | −83,2% |
| 2021-23 | $67.525 @ 2021-11-08 | $15.774 @ 2022-11-21 | 378 | −76,6% |
| 2025-26 *(berjalan)* | $124.715 @ 2025-10-06 | $58.460 @ 2026-06-30 | 267 | −53,1% |

---

## 1. Dispersi jalur post-low — **sangat lebar (n=4 bear selesai)**

`P(t)/P(low)`, 1,00 = harga di cycle low:

| t | 2011 | 2013-15 | 2017-19 | 2021-23 | min | max | max/min |
|---|---|---|---|---|---|---|---|
| t+30 | 1,56 | 1,32 | 1,09 | 1,07 | 1,07 | 1,56 | **1,46×** |
| t+60 | 2,72 | 1,61 | 1,11 | 1,44 | 1,11 | 2,72 | **2,45×** |
| t+90 | 2,08 | 1,23 | 1,20 | 1,54 | 1,20 | 2,08 | **1,74×** |
| t+120 | 2,54 | 1,33 | 1,56 | 1,79 | 1,33 | 2,54 | **1,92×** |
| t+180 | 2,48 | 1,64 | 2,49 | 1,72 | 1,64 | 2,49 | 1,52× |

Di t+90, cycle yang paling lambat berada di **+20%** dari low sementara yang tercepat di **+108%** —
rentang lebih dari 1,7×. Di t+60 bahkan 2,45×. Tidak ada "bentuk khas" yang bisa disalin.

## 2. Korelasi pairwise log-return harian antar jalur post-low

| | 2011 | 2013-15 | 2017-19 | 2021-23 |
|---|---|---|---|---|
| **2011** | +1,000 | +0,176 | −0,003 | −0,145 |
| **2013-15** | +0,176 | +1,000 | −0,003 | −0,039 |
| **2017-19** | −0,003 | −0,003 | +1,000 | −0,030 |
| **2021-23** | −0,145 | −0,039 | −0,030 | +1,000 |

**6 pasang: median −0,017 · rentang −0,145 s/d +0,176.** Pergerakan harian antar jalur post-low
praktis **tidak berkorelasi sama sekali**.

## 3. Verdict — **NOT SUPPORTED (hasil negatif)**

Rentang t+90 = 1,74× dan median korelasi ≈ 0. **Overlay fractal post-low dari satu cycle ke cycle lain
cenderung tidak punya isi prediktif.** Hasil negatif adalah hasil valid — ini bukan kegagalan menemukan
sesuatu, ini temuan bahwa yang dicari tidak ada.

Konsisten dengan validasi sebelumnya `findings_post_bottom_rally_speed.md` (n=4 episode unlock Z1→Z2,
hari ke +50% berkisar 19–233 hari) — dua pendekatan berbeda, kesimpulan sama: **kecepatan pemulihan
post-low sangat bervariasi antar cycle.** Ini juga melemahkan versi kuat klaim B9 ("bear market tidak
pernah V-shaped"): 2011 mencapai 2,72× dalam 60 hari — cukup dekat ke V.

---

## 4. Ex-post — anchor video sudah tertembus

- Anchor yang dipakai video: low Februari 2026 = **$62.840 @ 2026-02-05** (video menyebutnya "~$60.000")
- Low terendah setelah video: **$58.460 @ 2026-06-30** → anchor **tertembus −7,0%**

Ini **cacat struktural metode, bukan nasib buruk**: overlay butuh tahu di mana low-nya, dan itu baru bisa
diketahui setelah fakta. Ketiga proyeksi fractal di video dipasang dari titik yang ternyata bukan low,
jadi seluruh timeline-nya bergeser sejak awal.

Jalur aktual dari anchor video vs ketiga fractal:

| t | aktual 2026 | 2011 | 2013-15 | 2017-19 | 2021-23 |
|---|---|---|---|---|---|
| t+30 | 1,07 | 1,56 | 1,32 | 1,09 | 1,07 |
| t+60 | 1,10 | 2,72 | 1,61 | 1,11 | 1,44 |
| t+90 | 1,30 | 2,08 | 1,23 | 1,20 | 1,54 |
| t+120 | **0,98** | 2,54 | 1,33 | 1,56 | 1,79 |
| t+180 | *(di luar data)* | 2,48 | 1,64 | 2,49 | 1,72 |

Pada t+120 (horizon terjauh yang tertutup data), harga aktual **0,98× anchor** — yaitu **di bawah** titik
yang video anggap sebagai low, sementara keempat fractal memproyeksikan 1,33×–2,54×. **Tidak ada satupun
fractal yang mendekati.**

Tambahan yang perlu dicatat: ketiga fractal di video **saling bertentangan** (rally sungguhan mid-Juni
versus chop sampai November 2026). Dengan tiga proyeksi yang berbeda arah, hampir semua outcome bisa
diklaim "sesuai salah satu fractal" setelah fakta — ini membuat metodenya sulit difalsifikasi
kecuali fractal mana yang berlaku dispesifikasi **sebelum** kejadian.

---

## Kesimpulan

**NOT SUPPORTED.** Dari **n=4 bear selesai** (2011, 2013-15, 2017-19, 2021-23 — satu per cycle, plus
cycle 2025-26 yang masih berjalan/censored), jalur post-low tersebar 1,2×–2,1× di t+90 dan korelasi
log-return harian antar jalur median −0,017. Metode bar-pattern overlay **cenderung tidak punya isi
prediktif**, dan tiga masalah tambahan memperburuknya: anchor baru diketahui setelah fakta (anchor video
sudah tertembus −7,0%), anchor bisa dipilih bebas (channel yang sama memakai anchor berbeda tujuh minggu
kemudian), dan ketiga fractal saling bertentangan sehingga hampir tidak bisa salah.

Hasil ini **reusable**: klaim fractal-overlay dari sumber manapun ke depan bisa dinilai cepat dengan
merujuk ke sini, tanpa perlu validasi ulang.
