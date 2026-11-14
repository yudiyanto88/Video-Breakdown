# Findings — Confluence 200 DMA + STH RP sebagai resistance saat bear

**Tanggal validasi:** 5 Agustus 2026
**Script:** [`analyze_ma200_sthrp_confluence.py`](analyze_ma200_sthrp_confluence.py)
**Event CSV:** [`events_ma200_sthrp_confluence.csv`](events_ma200_sthrp_confluence.csv) · [`events_ma200_sthrp_confluence_alt.csv`](events_ma200_sthrp_confluence_alt.csv) · [`events_ma200_sthrp_crosscheck_signalD.csv`](events_ma200_sthrp_crosscheck_signalD.csv)
**Data:** `data_master_all_metrics.csv`, **berakhir 2026-07-15**

Menjawab Flag Prioritas #1 yang masih terbuka dari analisis `2026-08-04` (Signal D hit rate ~12%,
usulan dipasangkan dengan 200D MA). Video ini secara independen mengusulkan klaster resistance yang sama.

---

## Definisi event (ditetapkan sebelum menghitung)

- **Fase bear** — dua definisi dijalankan, keduanya dilaporkan:
  - **PRIMARY:** hari berlabel `ZC` / `Z1` / `Z1b` (Zone Structure v2) → **724 hari**
  - **SENSITIVITAS (ALT):** ditambah `ZD` → **2.348 hari**
- **Event** = `btc_price[t-1] < 200_dma[t-1]` **DAN** `btc_price[t] ≥ 200_dma[t]` pada hari bear
- **Merge** event dalam 30 hari jadi satu
- **DITOLAK** = close balik di bawah `200_dma` dalam 30 hari · **BREAK-TAHAN** = ≥30 hari di atas
- **At-gate, anti-lookahead:** gap confluence dihitung dari nilai pada tanggal event, bukan dari masa depan

---

## 1. Hasil definisi PRIMARY — n terlalu kecil untuk disimpulkan

**n = 2 event, keduanya dari cycle 2013-15.** Tidak ada satupun event di 2011, 2017-19, 2021-23, 2025-26.

| Cycle | Tanggal | Zona | Harga | 200DMA | STH RP | Gap at-gate | Outcome | ret30d | ret90d |
|---|---|---|---|---|---|---|---|---|---|
| 2013-15 | 2015-06-29 | Z1b | 256,67 | 252,54 | 248,68 | 1,50% | BREAK-TAHAN | +13,1% | −9,3% |
| 2013-15 | 2015-10-06 | Z1 | 246,89 | 246,31 | 247,01 | 0,28% | DITOLAK | +56,9% | +75,6% |

**Sebaran per cycle: 2013-15 = 2, semua cycle lain = 0.** Dengan n=2 dari satu cycle, definisi PRIMARY
**tidak bisa menjawab apapun** — dilaporkan apa adanya, bukan dibuang.

Penyebab strukturalnya masuk akal: di zona ZC/Z1/Z1b harga jauh di bawah semua cost-basis, jadi cross-up
200 DMA memang jarang terjadi.

---

## 2. Hasil definisi SENSITIVITAS (+ZD) — n=13, sebaran lintas 5 cycle

| Cycle | Jumlah event | DITOLAK | BREAK-TAHAN |
|---|---|---|---|
| 2011 | 1 | 1 | 0 |
| 2013-15 | 3 | 1 | 2 |
| 2017-19 | 3 | 3 | 0 |
| 2021-23 | 4 | 4 | 0 |
| 2025-26 | 2 | 2 | 0 |
| **Total** | **13** | **11 (85%)** | **2 (15%)** |

**Reclaim 200 DMA saat bear cenderung ditolak: 11 dari 13 (85%).** Dua yang bertahan berasal dari
cycle yang sama (2013-15) — hasilnya **didominasi satu cycle** di sisi positif, dan sisi negatifnya
tersebar merata di 5 cycle (jauh lebih meyakinkan).

Ini **mendukung arah klaim video** (B2/B4): rally yang menyentuh 200 DMA dari bawah saat bear
**cenderung** ditolak, bukan berlanjut.

---

## 3. Confluence at-gate — arahnya BERLAWANAN dengan dugaan, dan bukan bukti independen

Gap at-gate = `|200DMA − STH RP| / harga`:

| Kelompok | n | Rejection rate | ret30d median |
|---|---|---|---|
| KETAT ≤5% (dua level berhimpit) | 3 | **67%** | +13,1% |
| LEBAR >5% | 10 | **90%** | −6,5% |

Kalau "confluence dua level" benar-benar memperkuat resistance, kelompok KETAT harusnya **lebih sering
ditolak**. Yang terjadi justru sebaliknya (67% vs 90%), dan **n=3 vs n=10** terlalu timpang untuk
disimpulkan ke arah manapun. **Klaim "confluence = resistance lebih kuat" TIDAK didukung data.**

### Yang lebih menentukan: kedua level nyaris mengukur hal yang sama

Korelasi `200_dma` vs `sth_cost_basis`:

| Sampel | n hari | r (level log) | r (perubahan harian log) |
|---|---|---|---|
| Bear PRIMARY (ZC/Z1/Z1b) | 724 | **+0,999** | +0,996 |
| Bear ALT (+ZD) | 2.348 | **+0,998** | +0,946 |
| Semua hari | 5.843 | +0,998 | +0,503 |

**r level ≈ +0,999 selama bear.** 200 DMA dan STH Realized Price adalah dua rata-rata bergerak dari
harga yang sama dengan pembobotan berbeda — jadi "confluence" di sini **bukan dua bukti independen,
melainkan satu hal yang diukur dua kali.** Ini tidak akan lolos Governance butir 1 framework
(uji independensi |phi| < 0,3).

Catatan skala: gap `|200DMA − STH RP|/harga` selama bear PRIMARY punya median **19,2%** (p25 9,7% · p75 31,7%);
hanya **18%** hari yang gap-nya ≤5%. Jadi kedua level *berkorelasi hampir sempurna sebagai seri*, tapi
*jarak absolutnya* sering lebar — keduanya bisa benar bersamaan.

---

## 4. Uji silang ke 8 event Signal D — **ini temuan yang paling operasional**

Dari `findings_sth_rp_resistance_bear.md` (analisis 2026-08-04): 8 break STH RP lolos Signal D, **7 palsu, 1 asli**.
Pertanyaannya: kalau ditambah filter "harga juga di atas 200 DMA pada hari ke-3 break", apa yang tersaring?

| Cycle | Break date | Harga | 200 DMA | Harga/200DMA | Di atas 200DMA? | Break asli? |
|---|---|---|---|---|---|---|
| 2011 | 2012-01-02 | 5,22 | 7,36 | 70,9% | Tidak | Tidak |
| 2013 | 2014-06-01 | 626,54 | 649,32 | 96,5% | Tidak | Tidak |
| 2013 | 2015-03-12 | 295,72 | 336,82 | 87,8% | Tidak | Tidak |
| 2013 | 2015-06-18 | 249,35 | 259,23 | 96,2% | Tidak | Tidak |
| 2017 | 2018-07-29 | 8.191,77 | 8.589,95 | 95,4% | Tidak | Tidak |
| 2021 | 2022-03-29 | 47.444,25 | 48.323,30 | 98,2% | Tidak | Tidak |
| **2021** | **2023-01-13** | **19.929,30** | **19.515,92** | **102,1%** | **Ya** | **Ya** |
| 2025 | 2026-05-06 | 81.443,78 | 83.312,39 | 97,8% | Tidak | Tidak |

**Hasil:**
- Di atas 200 DMA pada hari ke-3 break: **1 dari 8**
- Break **palsu** yang tersaring keluar: **7 dari 7** — semuanya
- Break **asli** yang ikut terbuang: **0**
- Setelah filter: 1 event lolos, 1 di antaranya asli → hit rate naik dari **1/8 (12%)** ke **1/1 (100%)**

**Peringatan yang wajib dibaca bersama angka itu:** yang bertahan cuma **n=1 break asli**. "Hit rate 100%"
di atas basis n=1 tidak boleh dibaca sebagai keandalan — yang kuat di sini adalah sisi negatifnya
(**7/7 break palsu tersaring, tersebar di 4 cycle: 2011, 2013×3, 2017, 2021×2, 2025**), bukan sisi positifnya.
Filter ini **cenderung** menyingkirkan false positive; apakah ia juga akan meloloskan break asli berikutnya
belum bisa dijawab dari satu kejadian.

Perhatikan juga: event 2026-05-06 di baris terakhir adalah **persis reclaim yang dibahas di video ini**.
Filter 200 DMA akan menolaknya (harga 97,8% dari 200 DMA) — dan ex-post memang palsu (lihat
[`findings_expost_calibration.md`](findings_expost_calibration.md)).

---

## Kesimpulan

**Definisi PRIMARY: n=2, keduanya dari cycle 2013-15 — tidak konklusif.** Definisi sensitivitas (+ZD):
**n=13 tersebar di 5 cycle, 11 (85%) ditolak** → reclaim 200 DMA saat bear **cenderung** gagal, mendukung
arah klaim video.

Tapi klaim spesifik video — bahwa berhimpitnya STH RP + 200 DMA membuat resistance lebih kuat —
**tidak didukung**: kelompok gap ≤5% justru punya rejection rate lebih rendah (67%, n=3) daripada gap >5%
(90%, n=10), dan **korelasi kedua level selama bear r ≈ +0,999** berarti "confluence" adalah pengukuran
ganda, bukan dua bukti independen.

Nilai praktis terbesarnya ada di uji silang: **filter "harga di atas 200 DMA pada hari ke-3" menyingkirkan
7 dari 7 break STH RP palsu tanpa membuang 1 break asli (n=8 event, 5 cycle).** Ini layak diusulkan sebagai
filter tambahan untuk Signal D — dengan catatan tebal bahwa sisi "meloloskan yang asli" **bersandar pada n=1**.
