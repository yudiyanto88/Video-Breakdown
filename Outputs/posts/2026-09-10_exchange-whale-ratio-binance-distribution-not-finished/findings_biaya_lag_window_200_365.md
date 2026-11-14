# Findings — Biaya lag window 200/365 (V3)

**Tanggal:** 2026-09-10
**Script:** [`analyze_biaya_lag_window_200_365.py`](analyze_biaya_lag_window_200_365.py)
**Event table:** [`events_biaya_lag_window_200_365.csv`](events_biaya_lag_window_200_365.csv)
**Data:** `data_master_all_metrics.csv`, 2010-07-17 s/d 2026-09-07 (5.897 hari) — 4 siklus penuh + 1 berjalan

---

## Ringkasan sederhana

Pembuat post sengaja mematikan raw/SMA30/SMA100 dan cuma memakai SMA200/SMA365. Pertanyaan umumnya: **apakah metrik ber-window 200–365 hari layak jadi primary signal, atau maksimal confirming?**

Jawaban dari data: **maksimal confirming**. Cross SMA200 ke bawah SMA365 baru menyala rata-rata 170–235 hari setelah cycle peak, saat drawdown 35–63% **sudah terjadi**. Sebagai pemicu keputusan itu terlalu mahal.

**SIFAT UJI: pengukuran deskriptif lag, BUKAN backtest sinyal.** Titik referensi (bottom siklus, hari pertama Z1, hari unlock Z2) sebagian post-hoc — memang disengaja, karena yang diukur justru seberapa terlambat cross-nya. Angka di sini **tidak boleh** dibaca sebagai edge.

---

## Definisi event (eksplisit)

- **Event** = hari `t` di mana SMA200(x) memotong SMA365(x) **ke bawah**
- **Merge/cooldown** 365 hari
- **Dua varian x saja:** `mvrv_ratio`, `btc_price`

**Yang diukur dari tiap `t`:**

- (a) jarak ke cycle bottom aktual (nearest, bertanda; + = `t` sesudah bottom) dan ke bottom berikutnya
- (b) jarak ke hari pertama **Z1** setelah `t` — Z1 = `sth_cost_basis < realized_price` **DAN** `btc_price < sth_cost_basis`
- (c) jarak ke hari **unlock Z2** setelah `t` — STH RP cross naik melewati RP
- (d) konteks biaya: jarak dari cycle peak terakhir ke `t`, dan drawdown yang **sudah** terjadi sampai `t`

Penanda siklus memakai definisi identik V1 (peak = ATH diikuti ≥180 hari tanpa ATH baru & DD ≤ −30%):

- Peak: 2011-06-08, 2013-04-09, 2013-11-29, 2017-12-16, 2021-04-13, 2021-11-08, 2025-10-06
- Bottom: 2011-11-18, 2013-04-16, 2015-01-14, 2018-12-14, 2021-07-20, 2022-11-21, **2026-06-30 (sementara)**
- Total hari Z1 di seluruh sejarah: 350 | total hari unlock: **hanya 6** (mendukung temuan V1)

---

## n dan sebaran per cycle

| Varian | n (setelah cooldown) | 2011 | 2013 | 2017 | 2021 | 2025 |
|--------|----------------------|------|------|------|------|------|
| `mvrv_ratio` | 6 (dari 8 mentah) | 1 | 1 | 1 | 2 | 1 |
| `btc_price` | 6 (dari 6 mentah) | 1 | 1 | 1 | 2 | 1 |

**n = 6 per varian, tersebar merata 5 siklus — tidak didominasi satu siklus, tapi tetap sample kecil.**

---

## Hasil

### Varian x = `mvrv_ratio`

| Event | Cycle | Peak ref | Hari dari peak | DD sudah terjadi | Bottom terdekat | Jarak | Hari ke Z1 | Hari ke unlock |
|-------|-------|----------|----------------|------------------|-----------------|-------|------------|----------------|
| 2011-09-23 | 2011 | 2011-06-08 | 107 | −81,2% | 2011-11-18 | −56 | 78 | 209 |
| 2013-10-21 | 2013 | 2013-04-09 | 195 | −18,2% | 2013-04-16 | +188 | 472 | 743 |
| 2018-03-13 | 2017 | 2017-12-16 | 87 | −52,4% | 2018-12-14 | −276 | 322 | 420 |
| 2020-02-27 | 2021 | 2017-12-16 | 803 | −54,8% | 2018-12-14 | +440 | 978 | 1098 |
| 2021-09-06 | 2021 | 2021-04-13 | 146 | −17,1% | 2021-07-20 | +48 | 421 | 541 |
| 2024-10-25 | 2025 | 2021-11-08 | 1082 | **−1,4%** | 2026-06-30 | −613 | — | — |

- Median hari dari peak ke cross: **170 hari**, drawdown yang sudah terjadi median **−35,3%**
- Cross vs bottom terdekat: median **−4 hari** (3 sebelum / 3 sesudah) — praktis acak
- Cross → bottom berikutnya: median **446 hari** (n=6)
- Cross → hari pertama Z1: median **421 hari** (n=5); Z1 sudah aktif di hari cross: **0/6**
- Cross → unlock Z2: median **541 hari** (n=5)

**False positive telak:** 2024-10-25 menyala saat drawdown baru −1,4% dari peak Nov 2021 — dan setelah itu harga justru rally ke ATH baru Oktober 2025. Ini contoh nyata sinyal MA panjang yang menyala di tengah bull.

### Varian x = `btc_price`

| Event | Cycle | Peak ref | Hari dari peak | DD sudah terjadi | Bottom terdekat | Jarak | Hari ke Z1 | Hari ke unlock |
|-------|-------|----------|----------------|------------------|-----------------|-------|------------|----------------|
| 2012-01-29 | 2011 | 2011-06-08 | 235 | −81,8% | 2011-11-18 | +72 | 16 | 81 |
| 2014-09-12 | 2013 | 2013-11-29 | 287 | −58,9% | 2015-01-14 | −124 | 146 | 417 |
| 2018-08-08 | 2017 | 2017-12-16 | 235 | −67,7% | 2018-12-14 | −128 | 174 | 272 |
| 2020-03-23 | 2021 | 2017-12-16 | 828 | −66,7% | 2018-12-14 | +465 | 953 | 1073 |
| 2022-05-23 | 2021 | 2021-11-08 | 196 | −56,9% | 2022-11-21 | −182 | 162 | 282 |
| 2026-02-21 | 2025 | 2025-10-06 | 138 | −45,5% | 2026-06-30 | −129 | — | — |

- Median hari dari peak ke cross: **235 hari**, drawdown yang sudah terjadi median **−62,8%**
- Cross vs bottom terdekat: median **−126 hari** (4 sebelum / 2 sesudah)
- Cross → bottom berikutnya: median **156 hari** (n=6)
- Cross → hari pertama Z1: median **162 hari** (n=5); Z1 sudah aktif di hari cross: **0/6**
- Cross → unlock Z2: median **282 hari** (n=5)

---

## Hipotesis + verdict

**H1 — window 200/365 layak jadi primary signal untuk mendeteksi awal bear.**
**VERDICT: DITOLAK.** Sebagai peringatan awal bear, cross baru datang 170 hari (MVRV) / 235 hari (harga) setelah peak, dengan −35% / −63% drawdown sudah terjadi. Bandingkan dengan alarm bear CEPAT framework (§ 0 Decision Framework v2) yang di Okt 2025 bunyi +4 hari setelah peak. Selisihnya bukan puluhan hari, tapi **ratusan hari dan puluhan persen**.

**H2 — window 200/365 setidaknya berguna sebagai penanda konfirmasi / titik balik.**
**VERDICT: SEBAGIAN, dengan syarat.** Varian `btc_price` cenderung mendahului bottom berikutnya median 156 hari dan mendahului hari pertama Z1 median 162 hari — jadi ia menyala di paruh bawah bear, bukan di akhir. Ia bisa jadi konteks konfirmasi "bear sudah matang", **bukan** pemicu aksi. Varian `mvrv_ratio` jauh lebih longgar (median 446 hari ke bottom berikutnya) dan punya satu false positive di bull (2024-10-25).

**H3 — cross MA panjang bisa dipakai menandai akhir bear (tesis "cooldown" pembuat post).**
**VERDICT: TIDAK DIDUKUNG.** Jarak cross ke unlock Z2 median 282 hari (`btc_price`) / 541 hari (`mvrv_ratio`), dan Z1 bahkan **belum pernah aktif** di hari cross di 12 dari 12 event. Cross terjadi jauh sebelum struktur bear bottom benar-benar terbentuk.

---

## Konteks siklus berjalan

- `btc_price` SMA200/365 cross ke bawah: **2026-02-21**, 138 hari setelah peak 2025-10-06, saat drawdown −45,5% sudah terjadi. Bottom sementara datang 129 hari kemudian (2026-06-30).
- `mvrv_ratio` SMA200/365 cross ke bawah: **2024-10-25** — false positive, jauh sebelum siklus berbalik.

Artinya: kalau tahun ini seseorang menunggu konfirmasi 200/365 sebelum bertindak, hampir separuh drawdown sudah lewat sebelum sinyal muncul.

---

## Batasan

1. **n = 6 per varian** — kecil, walaupun tersebar merata di 5 siklus.
2. **Post-hoc by design.** Bottom, Z1, dan unlock adalah penanda yang baru diketahui belakangan. Ini sah karena tujuannya mengukur lag, tapi angka di sini **tidak** boleh dipakai sebagai bukti edge.
3. **Event COVID (2020-02-27 / 2020-03-23)** terhubung ke peak ref 2017-12-16 sehingga "hari dari peak" jadi 803/828 hari — outlier struktural yang menaikkan median jarak ke bottom/Z1/unlock. Median tetap dilaporkan apa adanya, tapi baca dengan sadar.
4. **Bottom 2026-06-30 bersifat sementara** — siklus belum selesai, jadi semua angka event 2025/2026 bisa berubah.
5. Uji ini **tidak** menguji varian window lain (misal 100/200 atau 50/200). Sengaja dibatasi dua varian x untuk menghindari overfitting.

---

## Verdict akhir

**Metrik ber-window 200–365 hari cenderung MAKSIMAL CONFIRMING, tidak layak jadi primary signal.** Cross SMA200/SMA365 menyala median 170 hari (`mvrv_ratio`) sampai 235 hari (`btc_price`) setelah cycle peak, dengan drawdown −35,3% dan −62,8% sudah terjadi (n=6 per varian; sebaran 2011:1, 2013:1, 2017:1, 2021:2, 2025:1). Ia juga tidak berguna sebagai penanda akhir bear: Z1 belum aktif di hari cross pada 12/12 event, dan unlock Z2 baru datang median 282–541 hari kemudian. Temuan ini **memperkuat** prinsip framework yang sudah ada (STH metrics & sinyal lambat = confirming, bukan primary) dan menjadi alasan struktural kenapa keputusan pembuat post untuk hanya menampilkan SMA200/SMA365 cenderung membuat pembacaannya **sistematis terlambat**, terlepas dari benar-tidaknya metrik EWR-nya.
