# Findings - Flip eksplosif % STH in Profit sebagai trigger awal bull market

**Tanggal validasi:** 26 Agustus 2026
**Script:** `analyze_sth_profit_flip_trigger.py`
**Event table:** `events_sth_profit_flip_trigger.csv`
**Data:** `data_master_all_metrics.csv` - 2010-07-17 s/d **2026-07-15** (n = 5.843 hari)

> **Caveat data paling penting:** data master berhenti di **2026-07-15**, sementara video membahas rally 19-25 Agustus 2026 ($63k ke $80k+). **Flip STH yang diklaim video ADA DI LUAR data kita** - yang diuji di sini pola historisnya, bukan kejadian Agustus 2026 itu sendiri. Semua pernyataan tentang "sekarang" merujuk 2026-07-15.

---

## Ringkasan sederhana

Klaim video - "hampir semua short-term holder flip balik ke profit = pola khas awal bull market" - **hanya sebagian benar, dan sebagai sinyal berdiri sendiri terlalu lemah untuk dipakai**. Dari **n=9** flip eksplosif sepanjang 2010-2026, median return 1 tahunnya memang bagus (+99,5%), tapi **3 dari 9 diikuti drawdown >=25% dalam 90 hari** dan satu di antaranya (Juli 2014) berakhir -61% dalam setahun.

Yang jauh lebih memisahkan bukan flip-nya, tapi **struktur level saat flip terjadi**: 4 dari 4 flip yang terjadi saat struktur **T** (STH RP < RP, artinya sudah di Z1) diikuti unlock struktural dalam 180 hari; **0 dari 5** flip yang terjadi saat struktur **N** diikuti unlock. Kondisi tambahan `pct_sth_in_profit > pct_lth_in_profit` (KB Supply in Profit 1.8) **TIDAK memisahkan** hit dari false positive - semua false positive justru ada di dalam kelompok itu.

**Kondisi 2026 saat ini = struktur N** (STH RP $67.143 > RP $52.740, gap 27%). Kalau flip Agustus 2026 benar terjadi, secara historis ia jatuh di **kelompok N - kelompok yang 0/5 diikuti unlock struktural**.

---

## Definisi event (dikunci sebelum menghitung)

- **Event flip** = hari pertama `pct_sth_in_profit` > **80%**, dengan syarat dalam **<=60 hari kalender sebelumnya** pernah ada `pct_sth_in_profit` < **10%**
- **Cooldown 180 hari** antar event
- Periode: 2010-07-17 s/d 2026-07-15
- **Anti-lookahead:** semua nilai keputusan (pct STH/LTH in profit, struktur, sth_mvrv) diambil **di hari event**. Return & drawdown adalah ground truth, bukan input gate
- **Unlock struktural** = definisi DF v2 bagian 0: STH RP cross **naik** melewati RP, didahului >=30 hari berturut struktur T. Terdeteksi 4 kali: 2012-04-19, 2015-11-03, 2019-05-07, 2023-03-01
- **False positive** = close terendah dalam 90 hari <= -25% dari close hari event

---

## (a) n total & sebaran per cycle

**n total = 9 event**

| Cycle | n | Tanggal |
|-------|---|---------|
| 2013 | 3 | 2012-01-01, 2014-07-02, 2015-07-10 |
| 2017 | 1 | 2019-03-16 |
| 2021 | 3 | 2020-01-28, 2023-01-14, 2023-10-20 |
| 2025 | 2 | 2024-10-15, 2025-05-08 |

**Independensi:** 9 event tapi hanya **4-5 siklus independen**. Cycle 2013 dan 2021 masing-masing menyumbang 3 event - event dalam satu siklus berkorelasi. Tidak ada satu siklus yang mendominasi arah kesimpulan (2013 punya 1 hit + 1 false positive; 2021 juga 1 hit + 1 false positive), tapi **sample-nya kecil**.

---

## (b) Outcome per event (at-gate)

| Cycle | Event | Flip (hari) | STH% | LTH% | Struktur | ret 90d | ret 180d | ret 365d | maxdd 90d | Unlock <=180d |
|-------|-------|-------------|------|------|----------|---------|----------|----------|-----------|--------------|
| 2013 | 2012-01-01 | 39 | 82,8 | 69,8 | **T** | -6,9% | +25,9% | +157,2% | -19,8% | 2012-04-19 |
| 2013 | 2014-07-02 | 50 | 81,7 | 81,0 | N | -40,9% | -52,2% | **-61,1%** | **-42,9%** | TIDAK |
| 2013 | 2015-07-10 | 39 | 89,8 | 54,1 | **T** | -14,9% | +50,4% | +127,8% | **-26,3%** | 2015-11-03 |
| 2017 | 2019-03-16 | 37 | 82,4 | 54,6 | **T** | +114,2% | +159,5% | +32,5% | -3,3% | 2019-05-07 |
| 2021 | 2020-01-28 | 33 | 89,0 | 81,2 | N | -17,9% | +6,0% | +224,9% | **-48,4%** | TIDAK |
| 2021 | 2023-01-14 | 47 | 89,7 | 60,0 | **T** | +45,5% | +50,2% | +99,5% | -3,5% | 2023-03-01 |
| 2021 | 2023-10-20 | 39 | 82,0 | 75,5 | N | +39,2% | +106,5% | +130,3% | +0,8% | TIDAK |
| 2025 | 2024-10-15 | 37 | 88,5 | 94,2 | N | +41,0% | +24,9% | +65,3% | -0,7% | TIDAK |
| 2025 | 2025-05-08 | 28 | 89,2 | 100,0 | N | +11,4% | -1,6% | -22,4% | -2,1% | TIDAK |

Agregat: median ret 90d **+11,4%**, 180d **+25,9%**, 365d **+99,5%**; median maxdd 90d **-3,5%** (min -48,4%).

**Diikuti unlock struktural <=180 hari: 4 dari 9 (44%).**

---

## (c) False positive

**3 dari 9 (33%)** diikuti drawdown >=25% dalam 90 hari: **2014-07-02** (-42,9%), **2015-07-10** (-26,3%), **2020-01-28** (-48,4%).

Catatan penting: 2015-07-10 sekaligus **hit** (diikuti unlock 2015-11-03) DAN false positive drawdown. Flip bisa benar arah dalam 1 tahun tapi tetap sangat mahal di 90 hari pertama - persis pola bear rally di KB Supply in Profit 1.6.

---

## (d) Apakah kondisi `pct_sth_in_profit > pct_lth_in_profit` memisahkan? - TIDAK

| Kondisi | n | unlock <=180d | false positive | median ret 90d | median ret 365d |
|---------|---|--------------|----------------|----------------|-----------------|
| STH > LTH (**YA**) | 7 | 4 | **3** | -6,9% | +127,8% |
| STH <= LTH (tidak) | 2 | 0 | 0 | +26,2% | +21,4% |

Semua false positive ada di kelompok "signature nyala". Kondisi ini **gagal sebagai filter** - dia lebih menandai "pasar masih di bear dalam" (LTH ikut rugi) daripada "ini bull sungguhan". n kelompok pembanding cuma 2, jadi tidak bisa disimpulkan lebih jauh dari itu.

---

## Temuan tak terduga (lebih kuat daripada hipotesis awal): struktur at-gate

| Struktur di hari flip | n | unlock <=180d | false positive | median ret 90d | median ret 365d |
|-----------------------|---|--------------|----------------|----------------|-----------------|
| **T** (STH RP < RP) | 4 | **4/4** | 1 | +19,3% | +113,7% |
| **N** (STH RP > RP) | 5 | **0/5** | 2 | +11,4% | +65,3% |

Pemisahan ini bersih, tapi sebagian **mekanis**: unlock formal butuh struktur T dulu supaya cross-ke-atas bisa terjadi (lihat `findings_unlock_reachability_struktur_n.md`). Nilai praktisnya tetap ada: flip STH di struktur N cenderung **tidak** menandai akhir bear, dan return 365d-nya jauh lebih tersebar (-61,1% s/d +224,9%).

---

## Sensitivitas threshold (3 varian, semua dilaporkan)

| Varian | n | Catatan |
|--------|---|---------|
| <10% ke >80% dalam <=60d (**baseline**) | 9 | - |
| <5% ke >80% dalam <=60d | 9 | set hampir identik (2015-07-10 bergeser ke 2015-10-17) |
| <10% ke >80% dalam <=90d | 10 | tambah 2021-10-01 |
| <10% ke >90% dalam <=60d | 7 | hilang event 2012 & 2014 |

Kesimpulan sama di ketiga varian: sebagian hit, sebagian gagal keras. **Tidak ada varian yang "menyelamatkan" klaim** - jadi hasil ini bukan produk overfit, tapi juga bukan sinyal yang lolos.

---

## State check - hari terakhir data (2026-07-15)

| Metrik | Nilai |
|--------|-------|
| `btc_price` | $65.097,92 |
| `sth_mvrv` | 0,9695 |
| `pct_sth_in_profit` | **45,00%** |
| `pct_lth_in_profit` | 59,23% |
| `percent_btc_in_profit` | 56,88% |
| `sth_cost_basis` (STH RP) | $67.143,31 |
| `realized_price` (RP) | $52.739,64 |
| `true_market_mean_price` | $76.023,01 |
| `lth_cost_basis` (LTH RP) | $49.890,36 |
| `price_at_aviv_mean` | $96.970,11 |
| `cvdd` | $49.106,19 |
| Struktur | **N** (STH RP > RP) |
| Harga vs STH RP | 97,0% dari STH RP |
| Terakhir `pct_sth_in_profit` < 10% | **2026-06-30** |
| Min `pct_sth_in_profit` 180 hari terakhir | **0,0%** |

Artinya: **prasyarat flip (<10%) memang baru terpenuhi 2026-06-30**, jadi flip Agustus 2026 yang diceritakan video kemungkinan besar akan terdaftar sebagai event ke-10 begitu data ter-update. Tapi struktur di 2026-07-15 masih **N**, dan rasio STH RP/RP masih 1,27x - jauh dari inversi.

---

## Cek Standar Validasi

1. **Definisi event** - eksplisit, dikunci sebelum menghitung, cooldown 180 hari. OK
2. **n dilaporkan** - n=9 total, sebaran per cycle 3/1/3/2, **hanya 4-5 siklus independen**. OK
3. **Anti-lookahead** - semua nilai gate dari hari event; return/drawdown hanya ground truth. OK
4. **Independensi** - disebut: cycle 2013 & 2021 masing-masing 3 event; tidak ada satu siklus yang mendominasi arah. OK
5. **Data mulai belakangan** - tidak berlaku (semua kolom full-history). Tapi **data berhenti 2026-07-15**, rally Agustus 2026 di luar jangkauan. OK
6. **Overfit** - 3 varian threshold diuji, semua dilaporkan, kesimpulan tidak berubah. OK

---

## Verdict

**SEBAGIAN TERKONFIRMASI, TAPI TIDAK CUKUP SEBAGAI SINYAL BERDIRI SENDIRI.** Flip <10% ke >80% cenderung diikuti return 1 tahun positif (median +99,5%, n=9), tapi hit rate ke unlock struktural hanya **4/9** dan **3/9 diikuti drawdown >=25% dalam 90 hari**. Kondisi tambahan STH-profit > LTH-profit yang diusulkan KB 1.8 **gagal memisahkan** hit dari false positive. Pemisah yang benar-benar bekerja adalah **struktur at-gate** (T: 4/4 unlock; N: 0/5) - dan kondisi 2026-07-15 adalah **N**. Rekomendasi: **jangan naikkan flip STH jadi gate** di framework; pakai sebagai confirming context saja, dan hanya kalau struktur sudah T. **n=9 dari 4-5 siklus independen - low confidence.**
