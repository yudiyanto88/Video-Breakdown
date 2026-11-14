# Findings — Regime Filter 3 Level (STH RP + 200D MA + 365D MA)

**Tanggal validasi:** 4 Agustus 2026
**Script:** `analyze_regime_filter_3_level.py`
**Event table:** `events_regime_filter_3_level.csv`, `events_regime_filter_3_level_sisi_turun.csv`, `events_regime_filter_3_level_reclaim.csv`
**Data:** `data_master_all_metrics.csv` (2010-07-17 s/d 2026-07-15, n = 5.843 hari)

---

## Ringkasan sederhana

Filter tiga level ini ternyata **sangat bersih tapi sangat lambat**. Tidak sekalipun salah bunyi (0 false positive dari 20 event / 6 klaster) — termasuk **lolos ujian Mei 2021** yang selama ini bikin alarm cepat framework misfire. Tapi harganya mahal: sinyalnya baru nyala median **119 hari setelah peak, saat drawdown sudah -19% s/d -84%**, jauh di belakang alarm bear CEPAT framework (+4 hari di Okt 2025). Nilainya sebagai *konfirmator akhir*, bukan pengganti alarm cepat.

**Catatan data:** ma200 & ma365 dihitung sendiri sebagai rolling mean (**bukan centered**, anti-lookahead), `min_periods` penuh. ma200 valid mulai 2011-02-01, **ma365 baru valid 2011-07-16** — jadi cycle 2011 tidak bisa diuji penuh di sisi turun. Cross-check ma200 hitung-sendiri vs kolom `200_dma`: korelasi 1,00000, median abs diff 0,00%.

---

## Definisi event (dikunci sebelum menghitung)

- **REGIME-OFF:** hari pertama dari streak ≥5 hari berturut `btc_price < min(sth_cost_basis, ma200, ma365)`. Cooldown 90 hari antar event
- **REGIME-ON / reclaim per level:** close di atas level ≥3 hari berturut
- **False positive:** setelah REGIME-OFF, harga mencetak **ATH baru dalam 180 hari** (ATH = running max s/d tanggal event)
- **Unlock struktural:** sama seperti `findings_cohort_6m12m_realized_price.md` (n=4: 2012/2015/2019/2023)
- **Cycle peak:** max `btc_price` per window cycle → 2011-06-08 $29,60 | 2013-11-29 $1.156 | 2017-12-16 $19.538 | 2021-11-08 $67.525 | 2025-10-06 $124.715

---

## Hipotesis A — sisi turun: seberapa cepat sinyal bear nyala? → LAMBAT (n=5)

| Cycle | Peak | REGIME-OFF | Lag | Drawdown dari peak | Catatan |
|-------|------|------------|-----|--------------------|---------|
| 2011 | 2011-06-08 | 2011-10-05 @ $4,87 | 119 hari | **-83,5%** | ma365 baru valid 2011-07-17 → lag minimum artifisial |
| 2013 | 2013-11-29 | 2014-08-14 @ $510 | **258 hari** | -55,9% | |
| 2017 | 2017-12-16 | 2018-05-26 @ $7.395 | 161 hari | -62,2% | |
| 2021 | 2021-11-08 | 2022-01-02 @ $47.320 | 55 hari | -29,9% | |
| 2025 | 2025-10-06 | **2025-11-12 @ $101.695** | 37 hari | -18,5% | |

**n = 5 cycle, median lag 119 hari.** Rentang lebar (37-258 hari) — bukan pola ketat.

**Klaim spesifik video terkonfirmasi:** "bear terkonfirmasi ~$102.000 Nov 2025" → mesin event kita menghasilkan **2025-11-12 @ $101.695**. Cocok hampir persis.

**Pembanding framework:** alarm bear CEPAT bunyi **+4 hari setelah peak** di Okt 2025 (Decision_Framework v2 § 0). Alarm cepat cycle lain **tidak dihitung ulang** di sini — jadi perbandingan lintas-cycle belum lengkap, disebutkan eksplisit sesuai standar rigor. Untuk cycle 2025 saja: filter 3-level tertinggal **33 hari / 18,5 poin persen drawdown** di belakang alarm cepat.

---

## Hipotesis B (ujian sebenarnya) — false positive → LULUS BERSIH, TAPI n INDEPENDEN CUMA 6

**n = 20 REGIME-OFF event | FALSE POSITIVE = 0 (0%) | bear beneran = 20.**

⚠️ **Independensi:** 20 event itu mengelompok jadi **6 klaster bear** (gap >365 hari antar klaster): 2011-12, 2014-15, 2018-19, 2020 COVID, 2022, 2025-26. Jadi uji false-positive ini efektif berbasis **n=6 episode independen, bukan n=20**. Ini caveat terbesar dari hasil yang kelihatan sempurna.

**Cek eksplisit dua kasus rawan:**

- **Mei 2021 → TIDAK nyala.** Hanya **2 hari dari 123** yang close di bawah ketiga level (2021-07-19 dan 2021-07-20), jauh dari syarat 5 hari berturut. Filter ini **lolos ujian yang bikin alarm cepat framework salah bunyi.** Ini kelebihan nyata dan spesifik.
- **Mar 2020 (COVID) → NYALA** (2020-03-08 @ $8.109). Secara definisi tugas (ATH baru dalam 180 hari) ini **bukan** false positive — ATH lama $19.538 baru ditembus Des 2020. **Tapi secara ekonomi ini false positive telak:** forward return dari tanggal sinyal = +19,3% (90d), +29,3% (180d), **+545,1% (365d)**. Keluar di sinyal ini = keluar tepat sebelum bull run terbesar. Definisi "ATH dalam 6 bulan" menutupi kerugian ini — dilaporkan apa adanya, tidak diselamatkan dengan mengubah definisi.

**Forward return dari SEMUA tanggal regime-off** (uji "seberapa mahal keluar di sini?"):

| Horizon | n | Median | Positif |
|---------|---|--------|---------|
| 90 hari | 19 | -3,2% | 9/19 |
| 180 hari | 18 | **+11,2%** | 10/18 |
| 365 hari | 17 | **+70,5%** | 13/17 |

Artinya: median 1 tahun setelah sinyal bear ini nyala, harga sudah **+70%**. Sinyalnya bersih dalam arti "tidak salah menyebut bear", tapi **terlalu telat untuk dipakai keluar** — konsisten dengan lag median 119 hari di hipotesis A.

---

## Hipotesis C — urutan reclaim → KLAIM VIDEO TERKONFIRMASI 4/4

Trough cycle ditentukan **ex-post** (ini studi urutan deskriptif, bukan sinyal live — disebutkan eksplisit).

| Cycle | Trough | STH RP reclaim | 200D MA reclaim | 365D MA reclaim | Unlock |
|-------|--------|----------------|-----------------|-----------------|--------|
| 2011 | 2011-11-18 $2,05 | 2011-12-31 | 2012-01-14 | 2012-01-05 | 2012-04-19 |
| 2013 | 2015-01-14 $178 | 2015-03-10 | 2015-06-29 | 2015-10-22 | 2015-11-03 |
| 2017 | 2018-12-14 $3.281 | 2019-03-28 | 2019-04-02 | 2019-05-03 | 2019-05-07 |
| 2021 | 2022-11-21 $15.774 | 2023-01-11 | 2023-01-13 | 2023-03-14 | 2023-03-01 |
| 2025 | 2026-06-30 $58.460 | belum | belum | belum | BELUM |

- **STH RP selalu reclaim duluan: 4/4.** Klaim urutan video (STH RP dulu, baru 365D MA) **terkonfirmasi di semua cycle terukur (n=4).**
- **365D MA reclaim terakhir di 3/4** (2011 pengecualian: 365D MA sebelum 200D MA).

**Jarak reclaim ke unlock struktural (positif = mendahului):**

| Cycle | STH RP | 200D MA | 365D MA |
|-------|--------|---------|---------|
| 2011 | +110 | +96 | +105 |
| 2013 | +238 | +127 | **+12** |
| 2017 | +40 | +35 | **+4** |
| 2021 | +49 | +47 | **-13** |

**Ini temuan pentingnya:** **365D MA reclaim praktis KOINSIDEN dengan unlock struktural** di tiga cycle modern (+12, +4, -13 hari). Ia tidak memberi lead time — ia konfirmasi ulang hal yang sama. Sebaliknya STH RP reclaim datang **40-238 hari lebih awal**, tapi `findings_sth_rp_resistance_bear.md` menunjukkan reclaim pertama itu sering palsu (88% balik ke bawah dalam 90 hari).

---

## Verdict akhir

**PARTIAL — filternya valid tapi perannya berbeda dari yang diklaim.**

Sisi turun: sinyal 3-level bersih (0 false positive, **n=6 klaster independen** dari 20 event) dan **lolos ujian Mei 2021** — sesuatu yang alarm cepat framework gagal. Tapi lag-nya median **119 hari setelah peak (n=5 cycle, rentang 37-258 hari)** dengan drawdown -18,5% s/d -83,5%, dan median forward return 365 hari dari sinyal justru **+70,5%** — terlalu telat untuk dipakai keluar. Kasus COVID Mar 2020 nyala dan diikuti +545% dalam setahun (bukan false positive menurut definisi ATH-180d, tapi mahal secara ekonomi).

Urutan reclaim yang diklaim video **terkonfirmasi 4/4** (STH RP selalu duluan). Tapi 365D MA reclaim jatuh **koinsiden dengan unlock struktural** (+12/+4/-13 hari di tiga cycle modern) sehingga **tidak menambah lead time** — beda jauh dari 200D MA reclaim yang sudah CLOSED dengan lead 23-51 hari.

**Rekomendasi:** perlakukan "close di bawah ketiga level ≥5 hari" sebagai **veto/konfirmator kelas berat** (kalau nyala, hampir pasti bear beneran) — bukan sebagai alarm masuk/keluar. Alarm bear CEPAT framework tetap primary. 365D MA **tidak layak** ditambahkan sebagai sinyal unlock baru, karena isinya sama dengan unlock yang sudah ada.

**Kondisi sekarang (2026-07-15):** price $65.098 vs STH RP $67.143, 200D MA $73.534, 365D MA $88.728 — masih di bawah ketiganya, regime-off masih aktif (event terakhir 2026-05-16).
