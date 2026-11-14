# Findings — Bear bottom selalu terjadi di bawah LTH Realized Price?

**Sumber klaim:** Bitcoin Magazine Pro — "This Signalled Every Bitcoin Bottom — We're 4.9% Away, So Why Risk It" (2026-05-25), `[07:30]`–`[07:48]`
**Tanggal validasi:** 2026-08-06
**Script:** [`analyze_bear_bottom_vs_lth_rp.py`](analyze_bear_bottom_vs_lth_rp.py)
**Event table:** [`events_bear_bottom_vs_lth_rp.csv`](events_bear_bottom_vs_lth_rp.csv), [`events_bear_bottom_vs_lth_rp_episodes.csv`](events_bear_bottom_vs_lth_rp_episodes.csv)
**Data:** `data_master_all_metrics.csv`, 2010-07-17 s/d 2026-07-15 (n = 5.843 hari)

---

## Klaim yang diuji

**B8.** *"Every single Bitcoin bear market has had its bottom out occurring beneath this level, and we haven't done that yet"* — level yang dimaksud **LTH Realized Price** (`lth_cost_basis`), ~$48.600 pada 2026-05-25.

**Catatan soal insentif sumber:** pembicara mengangkat klaim ini justru untuk **menolak bobotnya**. Jadi ini klaim yang berdiri melawan bias sumbernya sendiri — kalau lolos uji, nilainya lebih tinggi daripada klaim yang mendukung narasinya.

---

## Definisi event (ditetapkan SEBELUM menghitung)

- **Rasio uji (a):** `btc_price / lth_cost_basis`; trigger = rasio < 1,00
- **Pembanding (b):** `sth_cost_basis / lth_cost_basis` < 1,00 — Price Level KB §4.1 (*nol false positive 10 tahun*)
- **Pembanding (c):** `btc_price / cvdd` < 1,05 — Price Level KB §4.2 (*6/6 bear bottom*)
- **Episode:** gap >30 hari antar hari trigger = episode baru
- **"Dekat bear low":** episode dalam ±90 hari dari bear low; level-hari pakai ±60 hari
- **Ground-truth bear low:** 2011-11-18, 2015-01-14, 2018-12-14, 2022-11-21 (4 terkonfirmasi) + 2026-06-30 sebagai low **sementara/belum terkonfirmasi** (data berakhir 2026-07-15 — bukan bukti)
- **Bear era:** [cycle peak .. bear low], plus versi diperpanjang [.. bear low + 180 hari] supaya rule (b) diperlakukan adil (KB mencatat (b) memang cenderung trigger *setelah* low)
- **Tidak ada grid search:** ketiga threshold diambil apa adanya dari video / Price Level KB

**Sanity check anchor 2026-05-25 — semua OK:** btc_price $77.172, lth_cost_basis $48.650, cvdd $48.644, sth_cost_basis $77.910.

---

## Hasil

### 1. Ketersediaan data

`lth_cost_basis` non-null & >0 sejak **2010-07-17**, sama dengan `btc_price`, `sth_cost_basis`, `cvdd` (n = 5.843 hari). **Keempat bear low terkonfirmasi tercakup penuh** — tidak ada masalah "data mulai belakangan" di uji ini. Yang tidak tersedia hanya era pra-2010, jadi n maksimum tetap 4.

### 2. Recall — apakah tiap bear low benar-benar di bawah LTH RP?

| Bear low | Harga di low | LTH RP | Price / LTH RP | Di bawah? | Min rasio ±60 hari |
|---|---|---|---|---|---|
| 2011-11-18 | $2 | $4 | **0,583** | YA | 0,580 @ 2011-11-23 |
| 2015-01-14 | $178 | $305 | **0,585** | YA | 0,585 @ 2015-01-14 |
| 2018-12-14 | $3.281 | $4.481 | **0,732** | YA | 0,732 @ 2018-12-14 |
| 2022-11-21 | $15.774 | $20.651 | **0,764** | YA | 0,754 @ 2022-11-09 |
| 2026-06-30 *(belum terkonfirmasi)* | $58.460 | $49.789 | **1,174** | **TIDAK** | 1,174 |

**Recall 4/4 bear low terkonfirmasi** — di hari low maupun dalam window ±60 hari. Dan **bagian kedua klaim juga akurat**: bear 2025-26 sejauh ini belum pernah menyentuh level itu (minimum rasio 1,174 pada 2026-06-30), jadi *"we haven't done that yet"* benar per data.

Perlu dicatat: **kedalaman penetrasinya drift naik** — 0,58 / 0,59 di dua bear pertama, 0,73 / 0,76 di dua bear terakhir. Yang portabel adalah **tandanya (di bawah 1,0)**, bukan seberapa dalam.

### 3. False positive — berapa sering Price < LTH RP terjadi di luar bear bottom?

Total **680 hari** dari 5.843 (**11,64%** sejarah), terpecah jadi **6 episode**:

| Episode | Hari | Min rasio | Bear low terdekat | Jarak | Dalam ±90d? |
|---|---|---|---|---|---|
| 2011-11-14 .. 2012-04-16 | 110 | 0,580 | Bear 2011 | 0d | YA |
| 2015-01-03 .. 2015-10-25 | 295 | 0,585 | Bear 2015 | 0d | YA |
| 2018-11-22 .. 2019-04-01 | 131 | 0,732 | Bear 2018 | 0d | YA |
| **2020-03-12 .. 2020-03-12** | **1** | 0,998 | Bear 2018 | 454d | **TIDAK — FP** |
| **2022-06-18 .. 2022-07-12** | **7** | 0,954 | Bear 2022 | 132d | **TIDAK — FP** |
| 2022-08-26 .. 2023-01-13 | 136 | 0,754 | Bear 2022 | 0d | YA |

**Hanya 2 dari 6 episode (8 dari 680 hari = 1,2%) di luar ±90 hari bear low.** Jauh lebih bersih dari Validasi 1 (rc_ge3m: precision 28,5%, 3 dari 4 cluster nol persen).

Sebaran per cycle: 2011 (110 hari), 2015 (295), 2018 (132), 2022 (143) — **keempat cycle terwakili**, tidak didominasi satu cycle. Precision level-hari (±60d) = 46,8% (318/680); angka ini rendah karena episodenya panjang (rule tetap nyala berbulan-bulan setelah low lewat), bukan karena nyala di tempat yang salah.

Biaya praktis kedua false positive (forward return dari hari pertama episode, at-gate):

| Episode mulai | +90d | +180d | +365d | Status |
|---|---|---|---|---|
| 2020-03-12 | +104,3% | +109,3% | **+1.084,0%** | FP (COVID crash, 1 hari) |
| 2022-06-18 | +4,4% | −8,5% | +38,9% | FP (masih di dalam bear 2022) |

Untuk keperluan **akumulasi**, kedua "false positive" ini justru bukan kerugian — keduanya berakhir positif di horizon 365 hari, dan yang 2020 malah salah satu titik beli terbaik dalam sejarah. Untuk **short/timing exit** ceritanya beda, tapi di sisi beli biaya salah-bunyi mendekati nol.

### 4. Head-to-head dengan rule established framework

Trigger pertama per bear era (era ketat [peak..low]):

| Bear | (a) Price < LTH RP | (b) STH/LTH < 1,0 | (c) Price/CVDD < 1,05 | Urutan |
|---|---|---|---|---|
| 2011 | **2011-11-14** (lead +4d) | tidak trigger *(era +180d: 2011-12-10)* | 2011-11-18 (0d) | **a → c → b** |
| 2015 | **2015-01-03** (+11d) | tidak trigger *(2015-02-05)* | 2015-01-14 (0d) | **a → c → b** |
| 2018 | **2018-11-22** (+22d) | tidak trigger *(2019-01-29)* | 2018-12-13 (+1d) | **a → c → b** |
| 2022 | **2022-06-18** (+156d) | 2022-11-01 (+20d) | 2022-11-09 (+12d) | **a → b → c** |

- **(a) trigger di 4/4 bear era; (c) 4/4; (b) hanya 1/4** dalam era ketat (karena (b) memang cenderung nyala *setelah* low). Dengan era diperpanjang +180 hari, ketiganya jadi 4/4 — versi paling adil untuk pembanding.
- **(a) jadi trigger PERTAMA di 4/4 bear era.** Duluan dari (c): **4, 11, 21, 144 hari**. Duluan dari (b): **26, 33, 68, 136 hari**.
- Jawaban pertanyaan "redundan atau tidak": **(a) TIDAK belakangan — ia selalu duluan.** Tapi lihat §5 sebelum menyimpulkan ia layak jadi cross-check ketiga.

Lead terhadap bear low aktual: **+4, +11, +22, +156 hari** (median ~16 hari). Dispersi selebar itu dengan **n=4** berarti (a) cenderung sinyal **koinsiden sampai sedikit-mendahului**, bukan sinyal timing.

### 5. Independensi basis — apakah (a) benar-benar "basis ketiga"?

| | (a) Price<LTH RP | (b) STH/LTH<1,0 | (c) Price/CVDD<1,05 |
|---|---|---|---|
| Hari trigger | 680 | 621 | 54 |

- Spearman level harian: **ρ(a,b) = 0,964**, **ρ(a,c) = 0,841**
- **Seluruh 54 hari (c) berada di dalam (a) — 100% subset penuh**
- 482 dari 621 hari (b) berada di dalam (a) — 77,6%

Ini membatalkan framing "cross-check basis-berbeda". (a) dan (b) **berbagi penyebut yang sama persis** (LTH RP), jadi secara konstruksi bukan dua pengukuran independen. Dan (c) seluruhnya termuat di dalam (a) — artinya (a) adalah **selubung kasar (coarse envelope)** yang lebih luas dan lebih dini, bukan bukti tambahan dari sudut lain.

Konteks yang perlu ditandai untuk sekarang: **LTH RP dan CVDD hampir berimpit hari ini** — LTH RP/CVDD = 1,016 pada 2026-07-15 (median historis 1,09). Di cycle ini "turun di bawah LTH RP" dan "Price/CVDD mendekati 1,0" praktis menunjuk level harga yang sama, menaikkan risiko double-counting kalau keduanya dipakai berdampingan.

### 6. Kondisi sekarang

| Tanggal | Harga | LTH RP | Price/LTH RP | STH/LTH | Price/CVDD | Butuh turun berapa? |
|---|---|---|---|---|---|---|
| 2026-05-25 | $77.172 | $48.650 | **1,586** | 1,601 | 1,586 | −37,0% |
| 2026-07-15 *(hari terakhir data)* | $65.098 | $49.890 | **1,305** | 1,346 | 1,326 | −23,4% |
| Minimum bear 2025-26 sejauh ini | $58.460 @ 2026-06-30 | $49.789 | **1,174** | — | — | — |

Ketiga rule (a), (b), (c) **belum ada yang trigger sama sekali** di bear 2025-26.

---

## Kesimpulan

**SUPPORTED sebagai fakta historis, TIDAK layak diadopsi sebagai kondisi K4 baru.** Klaim B8 lolos uji faktual dengan bersih: **4/4 bear low terkonfirmasi (2011, 2015, 2018, 2022) terjadi di bawah LTH Realized Price** (rasio 0,583 / 0,585 / 0,732 / 0,764), dan bagian keduanya juga akurat — bear 2025-26 belum pernah menyentuhnya (minimum 1,174 pada 2026-06-30). False positive-nya tipis: **hanya 2 dari 6 episode (8 dari 680 hari trigger) di luar ±90 hari bear low**, dan keduanya (COVID Mar-2020 satu hari, Jun-2022 tujuh hari) berakhir positif di horizon 365 hari sehingga biayanya untuk sisi beli mendekati nol. Sebaran menutupi keempat cycle.

**Head-to-head-nya menghasilkan jawaban yang lebih halus dari dua opsi di pertanyaan.** (a) bukan "belakangan dari (b) & (c)" — ia justru **trigger PERTAMA di 4/4 bear era**, duluan 4–144 hari dari (c) dan 26–136 hari dari (b). Namun ia **juga bukan basis ketiga yang independen**: ρ(a,b) = 0,964 karena berbagi penyebut LTH RP, dan **seluruh 54 hari trigger (c) termuat 100% di dalam (a)**. Yang sebenarnya kita punya adalah **satu keluarga sinyal berlapis** — (a) selubung terluar & terdini (680 hari), (b) menengah (621 hari), (c) inti paling ketat (54 hari) — bukan tiga bukti dari sudut berbeda. Menambahkan (a) sebagai kondisi K4 kelima karena itu cenderung **menaikkan count tanpa menambah informasi**, persis kegagalan yang mau dicegah protokol independensi.

**Nilai yang tersisa dan nyata:** (a) berguna sebagai **precondition / early-warning gate** — "K4 belum boleh dianggap matang selama Price masih di atas LTH RP" — bukan sebagai kondisi yang ikut dihitung. Dalam peran itu ia memberi peringatan 4–156 hari sebelum low (median ~16 hari) tanpa membebani count K4. Peran ini langsung terpakai sekarang: pada 2026-07-15 harga masih **23,4% di atas** LTH RP, dan tidak satupun dari (a)/(b)/(c) trigger.

**Kaveat wajib:** **n = 4 bear low terkonfirmasi** — di bawah ambang yang framework ini sendiri anggap cukup, jadi seluruh temuan di atas cenderung, bukan pasti. Kedalaman penetrasi drift naik (0,58 → 0,76), sehingga hanya *tandanya* yang portabel. Satu risiko struktural untuk cycle ini: **LTH RP hampir berimpit dengan CVDD sekarang (1,016 vs median historis 1,09)** — (a) dan (c) untuk sementara menunjuk level harga yang praktis sama.

**Rekomendasi:** catat sebagai **precondition/early-warning untuk K4, bukan kondisi K4 kelima**. Diskusikan dengan Yudi apakah pantas dinaikkan jadi entri KB Price Level (kandidat §4.x) dengan label eksplisit "selubung terluar dari keluarga (a)/(b)/(c), bukan sinyal independen".
