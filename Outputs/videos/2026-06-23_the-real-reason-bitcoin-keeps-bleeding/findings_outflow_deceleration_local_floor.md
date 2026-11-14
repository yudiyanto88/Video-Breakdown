# Uji Hipotesis: Deselerasi Outflow Realized Cap → Precondition Local Floor

- **Asal klaim:** video "The Real Reason Bitcoin Keeps Bleeding" (On-Chain Mind, 2026-06-23) — "outflow turun dari ~$1B/hari ke ~$94M/hari; exhaustion of selling is almost always the precondition for at least a local floor"
- **Tanggal uji:** 2026-07-13
- **Data:** `realized_cap_usd`, `asopr` dari `data_master_all_metrics.csv` (Onchain-Dashboard)
- **Script:** `analyze_realized_cap_outflow_deceleration.py` (folder ini). Tabel event: `_decel_events_50pct.csv`
- **Precedent relevan:** Apparent Demand deceleration sudah REJECT dua kali (`research/findings/video-breakdown/video_whale-accumulation-2025/apparent_demand_hypothesis_findings.md` di Onchain-Dashboard)

## Definisi event (ditetapkan sebelum lihat hasil)

- flow = delta harian `realized_cap_usd`; MA30, dinormalisasi % realized cap per hari supaya comparable lintas era.
- Rezim outflow = rangkaian MA30 < 0 (merge gap <=7 hari); filter signifikansi peak <= -0.02%/hari (6 rezim noise dibuang).
- **Deceleration event (at-gate):** MA30 masih negatif tapi magnitude menyusut >=50% dari running peak outflow rezim (robustness: 30% dan 70%). Re-arm hanya setelah low rezim baru.
- **Local floor:** low 30 hari setelah event, valid kalau tidak ditembus 60 hari (varian 90 hari) setelahnya. False positive = floor gagal + leg-down >15% di bawah low30 dalam 180 hari.

## Hipotesis & Hasil

| Hipotesis | Verdict | Ringkasan |
|-----------|---------|-----------|
| Deselerasi outflow → local floor <=30 hari ("almost always") | **NOT-SUPPORTED** | Hit rate floor-60d: **43%** (9/21, threshold 50%); robustness 30%/70%: 44%/50%. Floor-90d cuma 24-40%. **Base rate hari ACAK dalam rezim outflow yang sama = 60%** — event deselerasi malah LEBIH JELEK dari beli asal-asalan di dalam rezim outflow |
| False positive rendah | **NOT-SUPPORTED** | 8/21 false positive keras (floor gagal + leg-down >15%), termasuk persis kandidat yang diprediksi: 2018-02/2018-04/2018-09 (pre-November crash) dan 2022-07. Median drawdown TAMBAHAN 180 hari setelah event: **-37.4%** |
| Informasi baru vs aSOPR recovery (K4 kondisi 2 family) | **NOT-SUPPORTED** | Event nyaris koinsiden dengan aSOPR MA7 balik >=0.99: median lag **2 hari**, 17/21 dalam ±14 hari, 19/21 dalam ±30 hari. aSOPR MA7 median saat event = 0.990. Tidak ada info baru |

## Detail penting

- **n=21 event** (threshold 50%) tersebar 5 cycle — sample cukup, hasil bukan karena kekurangan data.
- Robust lintas threshold: 30%/50%/70% semua memberi hit rate 43-50%, semua di bawah base rate 60%. Bukan kasus "threshold salah pilih".
- Ada asimetri logika di klaim video: "exhaustion of selling adalah precondition floor" (necessary) hampir tautologis — di dekat floor mana pun outflow pasti menyusut secara konstruksi. Yang berguna untuk keputusan adalah arah sebaliknya (deselerasi → floor, sufficient), dan itu yang gagal total di data.
- Status sekarang: peak outflow rezim ini -$973M/hari (2026-02-18), MA30 per 2026-07-12 -$397M/hari (shrink 58%); di tanggal video -$489M/hari. Angka "$94M/hari" di video kemungkinan snapshot delta harian, bukan MA30 — lebih noisy lagi.
- Konsisten dengan precedent REJECT Apparent Demand deceleration: sinyal "perlambatan laju" pada metrik flow on-chain kembali gagal sebagai timing signal.

## Verdict akhir

**REJECT.** "Almost always" tidak benar (43-50% hit rate, di bawah base rate 60% hari acak dalam rezim outflow); 8/21 false positive termasuk pre-crash November 2018 dan pre-Juni 2022; dan event-nya koinsiden dengan aSOPR recovery yang sudah dipantau framework. Jangan masuk framework.
