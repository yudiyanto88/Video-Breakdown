# Findings — F&G SMA30 Bullish Divergence di Bear Bottom (Context K4)

**Tanggal validasi:** 2026-07-12
**Asal insight:** Diskusi dengan Yudi setelah validasi `findings_fg_peak_vs_price_peak.md` — bukan klaim langsung dari video. Ide: kalau F&G SMA30 diminishing di sisi top (context K1/K3), sisi bottom-nya adalah regular/hidden bullish divergence SMA30 vs price menjelang K4 confirm.
**Script:** `analyze_fg_bottom_divergence.py`
**Data:** `data_master_all_metrics.csv` (kolom `Fear & Greed`, `btc_price`). F&G mulai 2018-02-01 → **hanya 2 bear selesai (2018, 2022) + 1 berjalan (2025-26)**.

---

## Keputusan parameter (dari diskusi)

- **SMA30 saja** — SMA14 dibuang: di beberapa titik kunci (Sep→Nov 2022, Des 2025→Feb 2026) SMA14 memberi verdict berlawanan dengan SMA30; sinyal yang flip tergantung smoothing window terlalu parameter-sensitive.
- **Anchor = major swing low** (lokal min window ±45–60 hari), bukan low minor. Ini keputusan penting: dengan low minor (±20 hari), 2018 menghasilkan "divergence palsu" Sep→Okt 2018 di ~$6.2K sebelum harga ambles 48% — tapi itu artefak anchor, hilang saat pakai major low.

## Metode

- Major low = harga minimum dalam window ±45 dan ±60 hari (dua-duanya dicek), di dalam fase bottoming tiap bear.
- Regular bullish divergence = price lower low + SMA30 higher low. Hidden = price higher low + SMA30 lower low.
- Anti lookahead untuk nilai SMA30 (rolling, hanya data ≤ T). Catatan jujur: identifikasi "major low" sendiri baru bisa dikonfirmasi ±45-60 hari setelah kejadian — sinyal ini inherently lagging sebesar itu.

## Hasil

| Bear | Anchor 1 | Anchor 2 (bottom final) | Price | SMA30 | Verdict |
|---|---|---|---|---|---|
| 2018 | 2018-06-28, $5,914, SMA30 27.0 | 2018-12-14, $3,281, SMA30 16.4 | LL | LOWER | **Tidak ada divergence** |
| 2022 | 2022-06-18, $18,973, SMA30 11.9 | 2022-11-21, $15,774, SMA30 27.3 | LL | HIGHER | **Regular bull div** ✓ |
| 2025-26 (berjalan) | 2025-11-22, $84,748, SMA30 25.9 | 2026-02-05, $62,840, SMA30 28.9 | LL | HIGHER | Regular bull div — belum bisa dinilai |

- **2022: hit bersih.** Bahkan dengan anchor ±45 hari (yang masih menyertakan low Sep 2022 $18,491, SMA30 24.5), verdict-nya tetap sama — divergence berlapis menuju bottom final.
- **2018: pattern absent, BUKAN false positive.** Bottom final Des 2018 terbentuk dengan SMA30 ikut membuat lower low. (Caveat: 2018 = tahun pertama F&G eksis; SMA30 baru valid sejak Mar 2018.)
- Raw F&G di bottom final: 10 (2018), 21 (2022) — konsisten dengan observasi bahwa raw F&G sudah lebih tinggi saat bottom near/K4 confirm dibanding capitulation low sebelumnya (6 di Jun 2022).
- 2025-26: divergence Nov-2025 → Feb-2026 sedang aktif. Kalau bear ini selesai dengan bottom di sekitar Feb 2026, jadi hit ke-2; kalau masih ada leg turun dengan SMA30 lower low, jadi kasus mixed.

## Verdict

**PARTIAL — 1 hit, 1 absent, 0 false positive (n=2 bear selesai).** Karena tidak ada false positive dengan anchor major-low, sinyal ini aman dipakai satu arah: **kehadiran divergence = context pendukung bottom-near; ketiadaan divergence tidak berarti apa-apa** (2018 bottom tanpa divergence). Sample terlalu kecil dan sinyal lagging (butuh konfirmasi major low ±45-60 hari) — tidak memenuhi syarat jadi sinyal formal.

## Implikasi ke framework (rekomendasi, bukan perubahan)

- Layak dicatat sebagai **confirming context opsional untuk K4** — hanya dibaca SETELAH kondisi primary K4 (LTH-MVRV, aSOPR/LTH-SOPR, Supply in Profit, Price/CVDD) terpenuhi; tidak pernah jadi alasan mempercepat entry atau syarat yang bisa memveto K4.
- Simetris dengan pemakaian sisi top di `findings_fg_peak_vs_price_peak.md`: F&G SMA30 = confirming context dua arah (top: cooling-off saat ATH baru; bottom: bullish divergence di major low), never primary.
- Pakai SMA30 saja, anchor major swing low — jangan low minor (terbukti menghasilkan sinyal palsu di 2018).
