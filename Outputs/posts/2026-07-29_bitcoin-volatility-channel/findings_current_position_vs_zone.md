# Validasi: Posisi harga terkini vs zona resmi framework

**Insight diuji:** [KONFIRMASI] Posisi harga terkini (dekat/dalam band Support) dibaca sebagai sinyal potensi bottom sedang terbentuk — narasi vendor "excellent accumulation period" untuk kondisi saat ini.

**Tanggal validasi:** 2026-07-29
**Script:** `analyze_current_position_vs_zone.py`
**Data event:** snapshot tunggal, tidak ada CSV pendukung (bukan event study)

---

## Data snapshot (2026-07-15, tanggal terakhir tersedia di `data_master_all_metrics.csv`)

| Metrik | Nilai |
|---|---|
| BTC Price | $65.097,92 |
| STH Realized Price | $67.143 |
| Realized Price (RP) | $52.740 |
| LTH Realized Price | $49.890 |
| AVIV Mean | $96.970 |
| MVRV Ratio | 1,234 |
| STH-MVRV | 0,970 |
| Supply in Profit | 56,88% |
| aSOPR | 0,991 |
| LTH-SOPR | 0,725 |

**Sanity-check OCR:** `btc_price` aktual data ($65.097,92) vs angka terbaca dari chart vendor ($64.625,10 di Gambar 1 / $64.491,81 di Gambar 2) — selisih ~+0,7-0,9%, masih dalam batas wajar untuk pembacaan low-confidence dari resolusi gambar. **OCR chart masuk akal**, meski tetap tidak dipakai sebagai anchor kesimpulan.

## Penentuan zona resmi

Struktur pasar saat ini = **N (Normal)** — gap STH RP vs RP sebesar +27,3% (STH RP $67.143 vs RP $52.740), jauh dari kondisi konvergen (yang biasanya menandai fase kapitulasi dalam). Price ($65.098) berada di antara RP ($52.740) dan STH RP ($67.143) → per Zone Structure v2 di `Decision_Framework v2.md`, ini masuk **Zona ZD (Dip Dalam)** — bukan ZC atau Z1 (capitulation).

Per tabel zona v2, aksi resmi di ZD = "K2 (kalau status bull) / tunggu (kalau alarm bear cepat bunyi)".

**Alarm bear cepat** (best-effort reconstruction — sinyal 1 & 2 direplikasi persis dari logic existing, sinyal 3 & 4 disederhanakan; **hasil ini flagged low-confidence, bukan state machine resmi yang tervalidasi penuh**): pool count 2/4 sinyal aktif (sinyal 2: STH-SOPR gap dari peak; sinyal 3: MVRV momentum bearish) → status **BUNYI** → aksi resmi = **TUNGGU**, bukan deploy.

**Independen dari status alarm**, K2 Veto 1 resmi (Supply in Profit ≤60%) → **TRIGGERED** (56,88% ≤ 60%, ini threshold resmi bukan approksimasi) — veto ini secara eksplisit melarang entry K2 apapun status gate lain. Veto 2 & 3 clear (tidak dicek detail di sini karena Veto 1 sudah cukup untuk kesimpulan "jangan entry").

## Verdict

Narasi vendor "harga dekat/dalam band Support → bottom forming, excellent accumulation period" **tidak align** dengan bacaan framework resmi di tanggal yang sama:

1. Zona resmi = ZD (Dip Dalam), bukan ZC/Z1 (capitulation) — struktur pasar masih "Normal", belum menunjukkan tanda kapitulasi dalam yang biasanya menyertai bottom cycle-defining
2. Alarm bear cepat (meski low-confidence) menunjukkan status BUNYI → aksi resmi adalah TUNGGU, bukan mulai akumulasi
3. K2 Veto 1 resmi (Supply in Profit 56,88% ≤ 60%) **TRIGGERED** — ini bukan sinyal soft, tapi larangan eksplisit untuk entry K2 terlepas dari kondisi lain

Kesimpulan: klaim "excellent accumulation" minimal **prematur** relatif terhadap bacaan on-chain framework saat ini, dan salah satu hard gate (Veto 1) secara aktif melarang entry sekarang.

---

**[VALIDASI — 2026-07-29, CLOSED]** Per data terbaru (2026-07-15, btc_price≈$65.098, cocok dengan OCR chart vendor ±0,7-0,9%), zona resmi framework adalah **ZD (Dip Dalam)** — bukan ZC/Z1 capitulation seperti tersirat narasi vendor "excellent accumulation". Best-effort reconstruction alarm bear cepat menunjukkan pool 2/4 sinyal aktif (BUNYI, flagged low-confidence untuk sinyal 3), sehingga aksi resmi zona ZD adalah TUNGGU; terlepas dari itu, **K2 Veto 1 resmi (Supply in Profit 56,88% ≤60%) TRIGGERED**, yang secara eksplisit melarang entry K2 apapun kata gate lain. Klaim vendor "bottom forming, excellent accumulation" tidak align dengan bacaan framework resmi saat ini.
