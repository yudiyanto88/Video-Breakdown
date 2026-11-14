# Findings: Cross-check independen zone saat ini vs klaim "extreme discount territory"

**Sumber klaim:** video Bitcoin Magazine Pro, 2026-07-13. Klaim: BTC baru masuk persentil ke-5 terbawah historis (model pembicara) → "unbelievable discount territory".

**Pendekatan:** BUKAN menguji model pembicara (sudah dicoba proxy di `findings_quantile_band_accuracy.md`) — sebaliknya cross-check independen pakai level & zone Decision Framework v2 kita sendiri di titik data terakhir yang tersedia (2026-07-15), tanpa mengubah/menambah threshold apapun.

## Hasil snapshot (2026-07-15)

| Level | Nilai |
|---|---|
| Price | $65,098 |
| STH RP (155d) | $67,143 |
| RP (full) | $52,740 |
| LTH RP | $49,890 |
| AVIV Mean | $96,970 |
| AVIV Upper (+0.5σ) | $110,962 |
| CVDD | $49,106 |

**Dimensi STRUKTUR**: N (Normal) — STH RP ($67,143) > RP ($52,740), gap 27.3% (jauh dari kondisi Konvergen <2%).

**Dimensi POSISI HARGA**: RP ≤ Price < STH RP → **Zone = ZD (Dip dalam)**, BUKAN Z1/ZC.

**Metrik pendukung:**
- mvrv_ratio = 1.234 (percentile rank full-history: **22.6th**, jauh dari bottom-5%)
- lth_mvrv = 1.305, sth_mvrv = 0.970
- percent_btc_in_profit = 56.9% (masih mayoritas untung, bukan capitulation)
- pct_sth_in_profit = 45.0%, pct_lth_in_profit = 59.2%
- Price/CVDD = 1.326 (percentile rank full-history: **9.3rd** — relatif rendah, tapi masih di atas 1.0/1.10 extreme flag)
- lth_sopr = 0.725, asopr = 0.991

**K4 4-kondisi check** (jalur utama, hanya berlaku penuh kalau Zone=Z1 — saat ini TIDAK):
1. LTH-MVRV < 1.0 → **FALSE** (1.305)
2. aSOPR<0.93 (7hr) & LTH-SOPR<0.50 → **FALSE** (aSOPR 7hr tidak semua <0.93, LTH-SOPR=0.725)
3. Supply-in-profit<50% & STH-profit<10% → **FALSE** (56.9%, 45.0%)
4. Price/CVDD<1.10 → **FALSE** (1.326)

**Count = 0/4.** Jalur utama K4 tidak aktif (Zone≠Z1). Jalur K4-tanpa-Z1 butuh count≥3 — count saat ini 0, jauh dari cukup.

**Konteks 90 hari terakhir** (bukan snapshot 1-hari terisolasi): price range $58,460-$81,868, mvrv_ratio range 1.101-1.509, struktur N konsisten sepanjang 90 hari, 86.7% hari price < STH RP tapi **0.0% hari price < RP** — artinya price sudah 90 hari berturut berada di zona ZD/Z3, tidak pernah menyentuh RP apalagi di bawahnya.

## Cek Standar Validasi
1. **Definisi event**: bukan uji lintas-cycle, satu snapshot point-in-time dibanding definisi zone/K4 yang SUDAH ADA (tidak ada threshold baru di-fit). ✓
2. **n**: n=1 titik data terakhir — **WAJIB ditekankan, bukan uji statistik**. Ditambah konteks 90 hari untuk menghindari kesan snapshot terisolasi.
3. **Anti-lookahead**: semua level dari hari itu sendiri (2026-07-15), tidak ada data masa depan.
4. **Independensi**: n/a (satu snapshot + 1 window konteks, bukan sample berulang).
5. **Data mulai belakangan**: tidak berlaku (semua kolom full-history).
6. **Overfit**: tidak ada threshold yang diubah — persis definisi Decision Framework v2.

## Verdict
Diagnosis independen framework kita **TIDAK align** dengan klaim pembicara. Zone saat ini = **ZD (Dip dalam)**, bukan Z1 (bear bottom) atau ZC (capitulation) — level dip yang cukup dalam tapi masih jauh dari extreme historis. Percentile rank mvrv_ratio (22.6th) dan Price/CVDD (9.3rd) sama-sama menunjukkan posisi rendah tapi TIDAK di bottom-5th-percentile secara harfiah, dan K4 count = 0/4 (tidak ada satupun kondisi bear-bottom aktif). Klaim "unbelievable discount territory" **tidak terkonfirmasi** oleh cross-check independen ini — framework kita membaca situasi lebih sebagai "dip dalam status bull/menunggu", bukan capitulation ekstrem. Catatan: ini satu titik data (n=1), diagnosis bisa berubah cepat kalau harga terus turun mendekati/di bawah RP ($52,740).

**[VALIDASI — 2026-07-29, CLOSED]** Cross-check independen (n=1 snapshot 2026-07-15 + konteks 90 hari) menunjukkan Zone = ZD (Dip dalam), K4 count = 0/4, mvrv_ratio percentile rank 22.6th & Price/CVDD percentile rank 9.3rd — semua menandakan dip moderat, BUKAN extreme/bottom-5th-percentile. Klaim pembicara "unbelievable discount territory" tidak terkonfirmasi oleh framework kita sendiri; catatan penting ini cuma satu titik waktu (n=1), bisa berubah cepat kalau harga turun lebih jauh mendekati RP ($52,740).
