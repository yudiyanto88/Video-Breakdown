# Findings — Reproduksi leg blind DCA dari tabel hasil video

**Insight yang diuji:** [STRATEGI] Tabel hasil final backtest (#17) + klaim out-of-sample 39 start date (#16)
**Sumber klaim:** Bitcoin Magazine Pro — "The FREE & SIMPLE Strategy That Beats Bitcoin (It Just Flashed Again)", 5 Agt 2026, slide `[10:46]`
**Tanggal validasi:** 6 Agustus 2026
**Script:** [`analyze_dca_leg_reproduction.py`](analyze_dca_leg_reproduction.py)
**Data:** `data_master_all_metrics.csv`, baris terakhir **2026-07-15**

> ⚠ **Selisih tanggal:** data berakhir 2026-07-15, video terbit 2026-08-05 — selisih ~3 minggu.
> Ini diperhitungkan eksplisit di semua perbandingan di bawah.

---

## Klaim yang diuji

Tabel hasil final video (slide `[10:46]`), asumsi tertulis: *"$1,000 seed plus $100 a week from
January 2014 · 0.1% fees, one-bar fill lag, 20% CGT on realised gains"*.

| Metrik | Blind DCA | Accumulation | Sell mode (taxed) |
|---|---|---|---|
| Total paid in | $66.700 | $66.700 | $66.700 |
| Final value | $2.968.017 | $3.115.675 | $5.794.249 |
| IRR | 54,0% | 54,7% | 64,0% |
| BTC held | 46,8 | 49,1 | 73,9 |
| Max drawdown | −83,5% | −83,2% | −70,4% |

**Scope validasi:** hanya **leg blind DCA**. Dua leg lain (Accumulation & Sell mode) butuh indikator
MVRV Quantile Bands yang parameter decay-nya **tidak diungkap** — mencoba menebak parameter sampai
angkanya cocok adalah overfitting yang dilarang Standar Validasi poin 6. **Tidak dicoba sama sekali.**

**Inkonsistensi yang harus diselesaikan:** slide bilang "**$1,000 seed**"; lisan `[05:50]` dan `[09:52]`
bilang "starting with **$100** and depositing $100 every single week".

---

## Definisi event

- Seed sekali di **2014-01-01** + **$100 tiap 7 hari kalender** s/d 2026-07-15
  (setoran $100 pertama di hari yang sama dengan seed)
- Equity **mark-to-market harian**; max drawdown dari peak nilai portofolio kumulatif
- **XIRR** money-weighted (brentq, day-count 365,25) — metode **identik** dengan
  `findings_dca_backtest_and_calmar.md` supaya bisa dibandingkan lintas findings
- Dua varian biaya, **dua-duanya diambil dari asumsi yang ditulis di slide** (bukan grid search):
  - **F0** — tanpa fee, same-day fill
  - **F1** — fee 0,1% + one-bar fill lag
- 20% CGT **tidak berlaku** untuk leg blind DCA (tidak ada realised gain — tidak pernah jual)

---

## Hasil

| Varian | n setor | Total setor | BTC | Final value | XIRR | maxDD | Setoran terakhir |
|---|---|---|---|---|---|---|---|
| seed $1.000 (SLIDE) / F0 | 655 | $66.500 | **47,08** | $3.064.561 | 54,7% | −82,9% | 2026-07-15 |
| seed $1.000 (SLIDE) / F1 | 654 | $66.400 | 46,93 | $3.055.351 | 54,6% | −82,9% | 2026-07-08 |
| seed $100 (LISAN) / F0 | 655 | $65.600 | 45,90 | $2.987.872 | 55,4% | −82,9% | 2026-07-15 |
| seed $100 (LISAN) / F1 | 654 | $65.500 | 45,80 | $2.981.624 | 55,3% | −82,9% | 2026-07-08 |
| **Klaim video (per 2026-08-05)** | — | **$66.700** | **46,8** | **$2.968.017** | **54,0%** | **−83,5%** | ? |

---

## (e) Inkonsistensi slide-vs-lisan → **SLIDE yang benar**

**Uji aritmetika total setoran ($66.700):**

| Asumsi seed | Sisa untuk setoran mingguan | Jumlah setoran | Setoran terakhir jatuh | Masuk akal? |
|---|---|---|---|---|
| seed $1.000 | $65.700 | **657,0 (BULAT)** | **2026-07-29** | **YA** — tepat sebelum video terbit 2026-08-05 |
| seed $100 | $66.600 | 666,0 (bulat) | **2026-09-30** | **TIDAK** — setelah tanggal video |

**Cross-check kedua.** Total setoran kita per 2026-07-15:
- seed $1.000 → $66.500. Selisih ke $66.700 = **$200 = tepat 2 setoran mingguan = 14 hari** →
  **konsisten** dengan data kita berhenti ~3 minggu lebih awal
- seed $100 → $65.600. Selisih ke $66.700 = $1.100 = 11 setoran = 77 hari → butuh ~11 minggu ekstra,
  jatuh 2026-09-30 — **tidak konsisten**

**Verdict:** versi **slide ($1.000 seed) yang benar**; lisan `[05:50]`/`[09:52]` keseleo.

---

## (f) Harga BTC implied dari tabel video

| Kolom | Perhitungan | Implied price |
|---|---|---|
| Blind DCA | 2.968.017 / 46,8 | **$63.419** |
| Accumulation | (3.115.675 − 2.007) / 49,1 | **$63.415** |
| Sell mode | (5.794.249 − 1.107.111) / 73,9 | **$63.425** |

**Ketiga kolom internally consistent di ~$63.420** (sebaran $63.415-63.425) — verifikasi ulang catatan
claim-tester: **OK**. Tabelnya bukan angka karangan asal.

- Harga aktual `btc_price` 2026-07-15 = **$65.098** → implied **−2,58%** di bawahnya
- Sensitivitas pembulatan "46,8 BTC" (46,75-46,85) memberi rentang $63.351-$63.487 →
  **tidak menutup** selisih ke $65.098
- Konteks 30 hari terakhir data kita: 2026-06-15 $66.358 → 2026-07-15 $65.098 (−1,9%),
  min $58.460 / max $66.358

Harga $63,4k pada awal Agustus 2026 **plausible** mengingat rentang pergerakan itu, tapi **tidak bisa
diverifikasi** karena data kita berhenti duluan.

---

## Normalisasi apple-to-apple

Mengisolasi efek selisih ~3 minggu data + selisih harga akhir (bukan mengubah strategi) — BTC kita
dikalikan harga implied video $63.419:

| Varian | Nilai @ $63.419 | vs klaim $2.968.017 | ΔBTC vs 46,8 |
|---|---|---|---|
| seed $1.000 / F0 | $2.985.531 | **+0,6%** | +0,6% |
| **seed $1.000 / F1** | **$2.976.560** | **+0,3%** | **+0,3%** |
| seed $100 / F0 | $2.910.820 | −1,9% | −1,9% |
| seed $100 / F1 | $2.904.733 | −2,1% | −2,1% |

**Toleransi ±10% → keempat konfigurasi REPRODUCE.** Konfigurasi terbaik (seed $1.000 + F1 fee 0,1% +
one-bar lag — yaitu persis asumsi yang ditulis di slide): ΔBTC **+0,3%**, ΔSetor −0,4%, ΔIRR **+1,1%**,
ΔMaxDD −0,7%.

---

## Kesimpulan

**KONFIRMASI — leg blind DCA reproducible, dan inkonsistensi slide-vs-lisan terselesaikan ke sisi slide.**

Angka video bukan karangan: BTC 46,8 · IRR 54,0% · maxDD −83,5% semuanya jatuh dalam **±2%** dari hasil
kami setelah dikoreksi untuk selisih data 3 minggu dan selisih harga akhir 2,6%.

Konsisten juga dengan `findings_dca_backtest_and_calmar.md` (XIRR 55,4% untuk weekly DCA 2014-2026 tanpa
seed — menambahkan seed $1.000 di 2014 menurunkannya ke 54,7%, **arah yang benar**).

**Dua leg lain (Accumulation & Sell mode) TIDAK direplikasi** — parameternya black-box. Artinya klaim
outperformance 1,95x dan "100% dari 39 start date" **tetap belum terverifikasi**; yang terverifikasi
hanya bahwa **baseline pembandingnya kredibel**.

---

## Flag n (tebal, sesuai Standar Validasi poin 2 & 4)

- Ini **1 window historis tunggal** (2014-01-01 → 2026-07-15), 4 konfigurasi (2 seed × 2 asumsi biaya)
- Window mencakup 3 bear penuh (2014-15, 2018, 2022) + 1 bear berjalan
- **Angka maxDD −83% ditentukan hampir seluruhnya oleh satu cycle (bear 2018)** — jadi metrik risiko di
  tabel video itu bukan rata-rata lintas cycle, melainkan properti satu kejadian.
  **Jangan dipakai sebagai ekspektasi drawdown ke depan.**
