# Findings — MA200/365 cross di exchange flow agregat (V2, PROXY)

**Tanggal:** 2026-09-10
**Script:** [`analyze_ma200_365_cross_exchange_flow.py`](analyze_ma200_365_cross_exchange_flow.py)
**Event table:** [`events_ma200_365_cross_exchange_flow.csv`](events_ma200_365_cross_exchange_flow.csv)

---

## ⚠ INI PROXY — BUKAN UJI KLAIM ASLINYA

Exchange Whale Ratio = rasio 10 inflow terbesar terhadap total inflow di **satu** exchange (Binance). Dataset kita **tidak punya** data per-exchange maupun konsentrasi per-transaksi (`data_dictionary.md` § "Yang TIDAK ada di data kita": *"Data per-exchange (Binance flow, ...) — kita cuma punya agregat"*). Yang ada cuma **magnitude agregat** seluruh exchange.

**Hasil apapun di dokumen ini TIDAK memvonis klaim EWR pembuat post.** Yang dijawab hanya: *apakah cross MA panjang (200/365) di metrik exchange-flow agregat punya nilai prediktif sama sekali?*

---

## Definisi event (eksplisit)

- **Event** = hari `t` di mana SMA200(x) memotong SMA365(x) **dari atas ke bawah**
- **Syarat at-gate pra-registrasi:** SMA200(`t`) di 5% teratas nilai SMA200 pada jendela **trailing** 365 hari (`t-365..t`) — trailing, bukan centered, supaya bebas lookahead
- **Merge/cooldown:** event dalam 365 hari sejak event sebelumnya dibuang, ambil yang pertama
- **Ground truth:** forward return `btc_price` di +90 / +180 / +365 hari dari `t`
- **Baseline:** median forward return unconditional semua hari di rentang data yang sama
- **Dua varian x saja:** (A) `inflow`; (B) `inflow / total_balance`

**Ambang a priori (ditetapkan sebelum melihat hasil):** sinyal dianggap punya nilai kalau median forward-180d ≥ baseline + 15pp. n < 4 → anekdotal, tidak boleh diklaim.

### Gate pra-registrasi ternyata degenerate — dan itu dilaporkan apa adanya

Dengan gate "SMA200 di top 5% trailing 365d", **0 event** di kedua varian (dari 35 dan 19 cross-down mentah). Sebabnya **struktural, bukan hasil**: di hari cross-down, SMA200 baru saja jatuh **di bawah** SMA365 (= rata-rata 365 hari dari deret yang sama), jadi hampir mustahil nilainya sekaligus berada di 5% teratas trailing 365 hari. Karena spesifikasi gate ini tidak bisa menghasilkan sample apa pun, dipakai **mode fallback tanpa gate level** — diumumkan terbuka di sini, dan hanya satu fallback yang dicoba (bukan pencarian varian sampai hasilnya enak).

---

## Ketersediaan data (§ STANDAR VALIDASI butir 5)

| Kolom | Non-NA | Rentang |
|-------|--------|---------|
| `inflow`, `outflow`, `net_flow`, `total_balance` | 5.839 hari | 2010-07-17 → **2026-07-11** |
| `btc_price` | 5.897 hari | 2010-07-17 → 2026-09-07 |
| `data_exchange.csv` (fallback file) | — | 2010-07-16 → **2026-07-11** |

**Kolom exchange flow BERHENTI di 2026-07-11 — 58 hari terakhir kosong.** Kondisi terkini (Sep 2026, konteks post) **tidak bisa** dinilai dengan metrik ini. Laporan claim-tester terverifikasi.

**Baseline unconditional (median forward return semua hari):**

- Rentang penuh 2010-07-17..2026-07-11: +90d = **+12,7%**, +180d = **+36,9%**, +365d = **+97,9%**
- Rentang 2015+: +90d = +8,7%, +180d = +30,4%, +365d = +78,0%

---

## Hasil

### Varian A — x = `inflow` (fallback tanpa gate)

n = **10** | sebaran per cycle: 2011:1, 2013:1, 2017:3, 2021:3, 2025:2

| Event | Cycle | Price | Bottom ref | Jarak | Posisi | fwd90 | fwd180 | fwd365 |
|-------|-------|-------|------------|-------|--------|-------|--------|--------|
| 2012-03-29 | 2011 | 5 | 2011-11-18 | +132 | sesudah | +37,9% | +151,4% | +1781,3% |
| 2014-09-04 | 2013 | 490 | 2015-01-14 | −132 | sebelum | −23,3% | −42,3% | −52,9% |
| 2016-12-21 | 2017 | 837 | 2015-01-14 | +707 | sesudah | +34,6% | +219,6% | +1788,1% |
| 2018-06-04 | 2017 | 7.504 | 2018-12-14 | −193 | sebelum | −2,7% | −43,5% | +2,8% |
| 2019-06-21 | 2017 | 10.103 | 2018-12-14 | +189 | sesudah | +1,8% | −27,9% | −7,4% |
| 2020-09-29 | 2021 | 10.849 | 2021-07-20 | −294 | sebelum | +149,4% | +414,4% | +283,0% |
| 2021-09-30 | 2021 | 43.890 | 2021-07-20 | +72 | sesudah | +5,9% | +8,1% | −55,7% |
| 2022-11-28 | 2021 | 16.211 | 2022-11-21 | +7 | sesudah | +45,3% | +65,8% | +133,4% |
| 2024-02-17 | 2025 | 51.661 | 2022-11-21 | +453 | sesudah | +29,8% | +11,5% | +86,1% |
| 2026-06-07 | 2025 | 63.290 | 2026-06-30 | −23 | sebelum | +26,2% | — | — |

- +90d: median **+28,0%** (n=10) → **+15,3pp** vs baseline penuh
- +180d: median **+11,5%** (n=9) → **−25,4pp** vs baseline penuh
- +365d: median **+86,1%** (n=9) → **−11,8pp** vs baseline penuh
- **Ambang a priori (+180d ≥ baseline+15pp): TIDAK LULUS (−25,4pp)**
- Posisi vs bottom: 4 sebelum / 6 sesudah, median |jarak| 160 hari

### Varian B — x = `inflow / total_balance` (fallback tanpa gate)

n = **10** | sebaran per cycle: 2013:2, 2017:3, 2021:3, 2025:2

| Event | Cycle | Price | Bottom ref | Jarak | Posisi | fwd90 | fwd180 | fwd365 |
|-------|-------|-------|------------|-------|--------|-------|--------|--------|
| 2013-09-13 | 2013 | 141 | 2013-04-16 | +150 | sesudah | +520,3% | +352,5% | +240,1% |
| 2014-12-10 | 2013 | 345 | 2015-01-14 | −35 | sebelum | −15,4% | −33,8% | +20,3% |
| 2016-12-17 | 2017 | 794 | 2015-01-14 | +703 | sesudah | +36,6% | +213,7% | +2334,5% |
| 2018-03-02 | 2017 | 11.188 | 2018-12-14 | −287 | sebelum | −33,2% | −37,1% | −65,2% |
| 2019-06-16 | 2017 | 8.993 | 2018-12-14 | +184 | sesudah | +15,0% | −16,8% | +5,6% |
| 2020-08-01 | 2021 | 11.815 | 2021-07-20 | −353 | sebelum | +14,8% | +182,7% | +237,9% |
| 2021-09-09 | 2021 | 46.405 | 2021-07-20 | +51 | sesudah | +8,9% | −16,5% | −53,7% |
| 2022-11-27 | 2021 | 16.420 | 2022-11-21 | +6 | sesudah | +41,1% | +62,8% | +127,0% |
| 2024-09-27 | 2025 | 65.801 | 2026-06-30 | −641 | sebelum | +45,5% | +32,1% | +66,7% |
| 2026-06-07 | 2025 | 63.290 | 2026-06-30 | −23 | sebelum | +26,2% | — | — |

- +90d: median **+20,6%** (n=10) → +7,9pp vs baseline penuh
- +180d: median **+32,1%** (n=9) → **−4,8pp** vs baseline penuh
- +365d: median **+66,7%** (n=9) → −31,2pp vs baseline penuh
- **Ambang a priori: TIDAK LULUS (−4,8pp)**
- Posisi vs bottom: 5 sebelum / 5 sesudah, median |jarak| 167 hari

---

## Hipotesis + verdict

**H1 — cross SMA200/365 di exchange flow agregat punya edge forward-180d ≥ baseline+15pp.**
**VERDICT: DITOLAK di kedua varian** (−25,4pp dan −4,8pp). Angka +90d sempat terlihat positif di varian A (+15,3pp), tapi ambang a priori dipasang di 180d sebelum melihat hasil, dan menggeser ke horizon yang kebetulan enak = overfitting.

**H2 — "cooldown / roll-over MA panjang = penanda akhir bear".**
**VERDICT: TIDAK DIDUKUNG di proxy ini.** Posisi event terhadap cycle bottom praktis lempar koin (4:6 dan 5:5), median jarak absolut ~160–167 hari. Sebaran ekstrem: dari −641 hari (sebelum bottom) sampai +707 hari (sesudah bottom).

**Konteks siklus berjalan (bukan klaim):** kedua varian menghasilkan event 2026-06-07, yaitu 23 hari **sebelum** bottom sementara 2026-06-30. Menarik, tapi n=1 per varian dan tanpa dukungan statistik agregat — jangan dipakai sebagai sinyal.

---

## Batasan

1. **Proxy, bukan EWR.** Ini pembatas terpenting. Magnitude inflow agregat ≠ konsentrasi inflow whale di satu exchange. Klaim pembuat post tetap `NEEDS-DATA-WE-DONT-HAVE`.
2. **Data flow berhenti 2026-07-11** — kondisi terkini tidak bisa dinilai.
3. **n = 10 per varian, tidak independen penuh** — cycle 2017 dan 2021 masing-masing menyumbang 3 event. Baseline forward return juga dihitung dari deret harga yang sama (overlapping windows), sehingga uncertainty riilnya lebih besar dari yang tampak.
4. **Baseline BTC secara historis sangat positif** (median +36,9% per 180 hari). Sinyal apa pun harus mengalahkan itu, dan sinyal bearish memang punya beban berat di sini — ini dilaporkan sebagai konteks, bukan pembelaan.
5. **Gate pra-registrasi degenerate** → dipakai satu fallback yang diumumkan. Tidak ada varian ketiga/keempat yang dicoba.

---

## Verdict akhir

**NEGATIF, dan hasil negatif = hasil valid.** Di dataset kita, cross SMA200 ke bawah SMA365 pada metrik exchange-flow agregat **cenderung tidak punya nilai prediktif** untuk forward return 180 hari (gagal ambang a priori di kedua varian; n=10 per varian, tersebar 4 siklus), dan **tidak** bisa dipakai sebagai penanda akhir bear (posisi terhadap bottom acak). **Ini tidak memvonis klaim Exchange Whale Ratio pembuat post** — metrik yang dia pakai tidak ada di dataset kita. Yang bisa dikatakan: gagasan generik "MA panjang di metrik exchange rolling over = sinyal" tidak lolos uji di versi agregat yang kita punya.
