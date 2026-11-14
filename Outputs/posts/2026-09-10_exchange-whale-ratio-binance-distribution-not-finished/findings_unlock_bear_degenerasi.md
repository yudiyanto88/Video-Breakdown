# Findings — Degenerasi aturan unlock status bear (V1)

**Tanggal:** 2026-09-10
**Script:** [`analyze_unlock_bear_degenerasi.py`](analyze_unlock_bear_degenerasi.py)
**Event table:** [`events_unlock_bear_degenerasi.csv`](events_unlock_bear_degenerasi.csv)
**Data:** `data_master_all_metrics.csv`, 2010-07-17 s/d 2026-09-07 (5.897 hari)

---

## Ringkasan sederhana

Decision Framework v2 § 0 bilang status bear baru berakhir kalau **STH RP naik memotong RP**. Masalahnya, cross itu cuma bisa terjadi kalau sebelumnya STH RP pernah turun **di bawah** RP (struktur T). Uji ini mengecek: di setiap bear window sejak 2011, apakah struktur T memang selalu terbentuk?

Jawabannya **tidak**. Di 3 dari 7 bear window struktur T tidak pernah terbentuk sama sekali — jadi trigger unlock tidak pernah punya kesempatan menyala, dan status bear terkunci sampai bertahun-tahun kemudian. Salah satu dari 3 window itu adalah **window yang sedang berjalan sekarang** (peak 2025-10-06).

---

## Definisi event (eksplisit, ditetapkan sebelum menghitung)

**Satu kejadian = satu bear window.**

- **Cycle peak** = hari ATH (running max harga) yang diikuti ≥180 hari tanpa ATH baru **DAN** drawdown minimum di dalam window ≤ −30%
- **Bear window** = `[peak_date .. tanggal ATH baru berikutnya]` (closed) atau `[peak_date .. 2026-09-07]` (ongoing)
- Tidak ada merge/cooldown antar window — tiap peak yang lolos kriteria dihitung terpisah

**Struktur T** = `sth_cost_basis < realized_price` (definisi § 1 Zone Structure v2).

**Trigger yang diukur — semua at-gate (nilai tersedia di tanggal keputusan):**

| Kode | Definisi |
|------|----------|
| U1 | hari `t` di mana `sth > rp` dan `sth(t-1) ≤ rp(t-1)`, setelah minimal 1 hari T di window itu |
| U7 | hari ke-7 berturut `sth > rp`, setelah minimal 1 hari T di window itu (signal keluar di hari ke-7) |
| ALT | harga close > `price_at_aviv_mean` 3 hari berturut (signal di hari ke-3), dicari setelah harga pernah close di bawah AVIV Mean di window itu |

**Dua varian durasi cross saja** (U1 dan U7) — sesuai § STANDAR VALIDASI butir 6, keduanya dilaporkan apa adanya.

**Catatan lookahead:** bottom window dipakai **hanya** sebagai titik referensi deskriptif untuk mengukur biaya keterlambatan, bukan input keputusan. Kolom AVIV memakai `price_at_aviv_mean` (per `data_dictionary.md`: AVIV Mean dalam USD, batas Z3/Z4 — "ini yang dipakai framework"), yang berbasis mean berjalan sehingga lebih aman dari lookahead dibanding pola full-history `mean/std` di `research/analyze_k3_stage_comparison.py`. Perbedaannya dicatat di Batasan.

---

## n dan sebaran per cycle

**n = 7 bear window** (6 closed + 1 ongoing).

| Cycle | Jumlah window | Peak |
|-------|---------------|------|
| 2011 | 1 | 2011-06-08 |
| 2013 | 2 | 2013-04-09, 2013-11-29 |
| 2017 | 1 | 2017-12-16 |
| 2021 | 2 | 2021-04-13, 2021-11-08 |
| 2025 | 1 (ongoing) | 2025-10-06 |

**n kecil dan tidak independen penuh:** dua window di cycle 2013 dan dua di cycle 2021 berasal dari siklus yang sama. Yang menyelamatkan uji ini: temuan utamanya **tidak** didominasi satu siklus — kasus degenerasi muncul di 2013, 2021, **dan** 2025.

---

## Hipotesis + verdict

### Hipotesis A — struktur T tidak selalu terbentuk di bear window

**VERDICT: TERKONFIRMASI (4/7 terbentuk, 3/7 tidak).**

| Cycle | Peak | Akhir window | Hari | DD | T terbentuk? | Hari T | T pertama | T terakhir |
|-------|------|--------------|------|-----|--------------|--------|-----------|------------|
| 2011 | 2011-06-08 | 2013-02-20 | 623 | −93,1% | YA | 131 | 2011-12-10 | 2012-04-18 |
| 2013 | 2013-04-09 | 2013-11-05 | 210 | −70,3% | **TIDAK** | 0 | — | — |
| 2013 | 2013-11-29 | 2017-02-23 | 1182 | −84,6% | YA | 271 | 2015-02-05 | 2015-11-02 |
| 2017 | 2017-12-16 | 2020-11-30 | 1080 | −83,2% | YA | 98 | 2019-01-29 | 2019-05-06 |
| 2021 | 2021-04-13 | 2021-10-19 | 189 | −53,1% | **TIDAK** | 0 | — | — |
| 2021 | 2021-11-08 | 2024-03-04 | 847 | −76,6% | YA | 121 | 2022-11-01 | 2023-03-04 |
| 2025 | 2025-10-06 | *ongoing* | 336 | −53,1% | **TIDAK** | 0 | — | — |

Polanya cenderung konsisten: T hanya terbentuk di bear **panjang** (623–1182 hari). Tiga window tanpa T semuanya ≤336 hari dengan drawdown 53–70% — cepat dan dalam, tapi tidak cukup lama untuk membuat cost basis holder baru jatuh di bawah cost basis seluruh pasar.

### Hipotesis B — kalau T tidak terbentuk, status bear "tergantung" lama

**VERDICT: TERKONFIRMASI, dan biayanya besar.**

Unlock dicari maju tanpa dibatasi akhir window:

| Cycle | Peak | T di window | Unlock U1 paling awal yang mungkin | Hari tergantung |
|-------|------|-------------|-----------------------------------|-----------------|
| 2013 | 2013-04-09 | TIDAK | 2015-11-03 | **938 hari** |
| 2021 | 2021-04-13 | TIDAK | 2023-03-01 | **687 hari** |
| 2025 | 2025-10-06 | TIDAK | belum ada (per 2026-09-07) | **336 hari, jalan terus** |

Implikasi paling tajam: status bear yang dibuka April 2013 baru bisa dicabut November 2015 — **seluruh blow-off top November 2013 dilewati dengan status "bear"**. Sama untuk peak April 2021: status bear baru bisa dicabut Maret 2023, jadi **puncak siklus November 2021 pun dilewati dengan status "bear"**.

### Hipotesis C — dua varian durasi cross (≥1 hari vs ≥7 hari)

**VERDICT: tidak ada bedanya untuk masalah degenerasi.**

| Cycle | Peak | U1 date | hari dari peak | naik dari bottom | U7 date | hari dari peak | naik dari bottom |
|-------|------|---------|----------------|------------------|---------|----------------|------------------|
| 2011 | 2011-06-08 | 2012-04-19 | 316 | +150,9% | 2012-04-25 | 322 | +150,4% |
| 2013 | 2013-04-09 | **NO SIGNAL** | — | — | **NO SIGNAL** | — | — |
| 2013 | 2013-11-29 | 2015-11-03 | 704 | +126,7% | 2015-11-09 | 710 | +113,1% |
| 2017 | 2017-12-16 | 2019-05-07 | 507 | +76,1% | 2019-05-13 | 513 | +138,1% |
| 2021 | 2021-04-13 | **NO SIGNAL** | — | — | **NO SIGNAL** | — | — |
| 2021 | 2021-11-08 | 2023-03-01 | 478 | +49,9% | 2023-03-11 | 488 | +30,7% |
| 2025 | 2025-10-06 | **NO SIGNAL** | — | — | **NO SIGNAL** | — | — |

Konfirmasi 7 hari cuma menambah 6–10 hari. Menaikkan/menurunkan syarat durasi **tidak menyentuh** akar masalah: kalau T tidak pernah ada, tidak ada cross untuk dikonfirmasi.

### Hipotesis D — trigger alternatif AVIV Mean lebih murah?

**VERDICT: TIDAK sesederhana itu — bergantung jenis bear; sebagai aturan at-gate ALT terlalu berisik di bear dalam.**

| Cycle | Peak | AVIV data wajar? | n firing ALT | Firing pertama sebelum bottom? | ALT pertama sesudah bottom | hari dari bottom | naik dari bottom |
|-------|------|------------------|--------------|-------------------------------|----------------------------|------------------|------------------|
| 2011 | 2011-06-08 | TIDAK (artefak) | 0 | — | NO SIGNAL | — | — |
| 2013 | 2013-04-09 | TIDAK (artefak) | 11 | tidak | 2013-04-20 | +4 | +84,9% |
| 2013 | 2013-11-29 | ya | 25 | **ya** | 2016-12-29 | +715 | +452,1% |
| 2017 | 2017-12-16 | ya | 74 | **ya** | 2019-06-22 | +190 | +218,9% |
| 2021 | 2021-04-13 | ya | 63 | tidak | 2021-08-07 | +18 | +49,5% |
| 2021 | 2021-11-08 | ya | 35 | **ya** | 2023-12-07 | +381 | +174,6% |
| 2025 | 2025-10-06 | ya | 0 | — | NO SIGNAL | — | — |

1. **Di bear dalam (T terbentuk):** ALT menyala 25–74 kali per window, firing pertamanya 300–715 hari **sebelum** bottom (dead-cat bounce) — tidak bisa dipakai sendirian. Di window yang sama unlock framework justru **lebih murah**: median kenaikan dari bottom saat U1 = **+76,1%** vs ALT-pertama-sesudah-bottom = **+218,9%** (n=3 window dengan data AVIV wajar; selisih median −142,8pp).
2. **Di bear pendek tanpa T (2013-04, 2021-04):** ALT menyala cepat setelah bottom — 4 hari (+84,9%) dan 18 hari (+49,5%), dan merupakan satu-satunya trigger yang menyala sama sekali.

Kedua aturan cenderung **komplementer, bukan saling gantikan**. Ini n=2 dan n=3 — **anekdotal, bukan bukti**.

---

## Kondisi window yang sedang berjalan (2026-09-07)

| Item | Nilai |
|------|-------|
| Peak | 2025-10-06 @ $124.715 |
| Umur window | 336 hari |
| Bottom sementara | 2026-06-30 @ $58.460 (−53,1%) |
| Harga terakhir | $78.905 (+35% dari bottom sementara) |
| STH RP | $70.965 |
| RP | $53.193 |
| AVIV Mean | $98.396 |
| Struktur | **N (normal)** — STH RP masih **+33,4% di atas** RP |
| Hari T | 0 |
| Unlock U1/U7 | NO SIGNAL |
| ALT (AVIV Mean 3d) | NO SIGNAL (harga masih di bawah AVIV Mean) |

STH RP harus turun ~25% relatif terhadap RP dulu supaya struktur T terbentuk. Selama itu belum terjadi, **status bear tidak punya jalan keluar mekanis di framework saat ini**.

Arah temuan ini kebetulan sejalan dengan tesis pembuat post ("distribusi belum selesai"), tapi lewat mekanisme yang sama sekali berbeda dan **bukan konfirmasi klaim EWR-nya**. Yang ditemukan di sini adalah lubang di aturan framework kita sendiri.

---

## Batasan

1. **n = 7, tidak independen penuh** — 2013 dan 2021 masing-masing menyumbang 2 window.
2. **Definisi cycle peak sensitif terhadap ambang.** Dengan gap ≥180 hari & DD ≤ −30% → 7 window. Dengan gap ≥365 hari → hanya 4 window closed (2011-06-08, 2013-11-29, 2017-12-16, 2021-11-08) dan di keempatnya T selalu terbentuk. Artinya degenerasi cenderung hanya muncul di koreksi besar intra-cycle. Window 2025-10-06 (336 hari) belum bisa dikategorikan mana pun — inilah ketidakpastian terbesar dari uji ini.
3. **Artefak data AVIV era 2010–2013.** `price_at_aviv_mean` di periode itu tercemar `aviv_ratio` ekstrem 2010 (5,5 dan 3,6), sehingga AVIV Mean berada jauh di atas harga hampir sepanjang 2011–2013 (window 2011 = 0 firing ALT). Window dengan peak < 2013-06 ditandai `aviv_reliable = False` di CSV dan tidak dipakai untuk kesimpulan AVIV.
4. **Perbedaan formula AVIV.** `analyze_k3_stage_comparison.py` memakai `mean/std` full-history `aviv_ratio` (in-sample, ada unsur lookahead); uji ini memakai kolom `price_at_aviv_mean` sesuai anjuran `data_dictionary.md`. Level absolutnya berbeda (per 2026-09-07: AVIV +0,5σ versi kolom = $112.129 vs versi script = $131.630).
5. Uji ini **tidak** menilai apakah timing unlock "benar" saat ia menyala — hanya apakah ia punya kesempatan menyala.

---

## Verdict akhir

**Aturan unlock "STH RP cross naik melewati RP" DEGENERATE di 3 dari 7 bear window (2013-04, 2021-04, dan window 2025-10 yang sedang berjalan) karena struktur T tidak pernah terbentuk.** Di dua kasus historis status bear akan tergantung 938 dan 687 hari, melewati ATH baru berikutnya. Varian durasi cross tidak relevan terhadap masalah ini. Tanda "⚠ pending validasi backtest final" di § 0 **cenderung memang beralasan**: aturan itu perlu jalur unlock kedua yang tidak bergantung struktur T. Kandidat paling sederhana (close > AVIV Mean 3 hari berturut) menyala cepat di dua window tanpa T (+4 dan +18 hari dari bottom) tapi terlalu berisik di bear dalam — kalau dipakai, harus sebagai jalur **bersyarat** (misal hanya aktif bila struktur T tidak pernah terbentuk sejak peak), bukan OR-gate polos. Ini **usulan, bukan penerapan** — perubahan framework dikerjakan di project Onchain-Dashboard.
