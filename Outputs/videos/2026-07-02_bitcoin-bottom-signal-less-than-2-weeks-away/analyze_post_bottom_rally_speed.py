"""
Insight 12 - Rally speed pasca-bottom (~100 hari, +50-250%)
Video: "Bitcoin Bottom Signal (Less Than 2 Weeks Away)" - Bitcoin Magazine Pro, 2026-07-02

Klaim video: begitu bottom terkonfirmasi, di 3 bear market terakhir harga naik
+50% s/d +250% dalam ~100 hari (contoh: 31 Des 2022, 100 hari $15-16k -> $30k;
$3,000 -> ~$14,000 (+250%) di 100 hari; $230 -> $460+ (+100%) di 100 hari).

PENTING: video memilih tanggal "bottom" secara subjektif/hindsight (misal 31 Des 2022
padahal harga sudah bergerak beberapa minggu dari low absolut Nov 2022). Kita TIDAK
memakai definisi subjektif itu -- kita pakai definisi objektif framework: Z1->Z2 unlock
= sth_cost_basis cross naik melewati realized_price (event yang sama dipakai di
Insight 7). Ini konsisten dengan aturan anti-lookahead: definisi "bottom" harus bisa
dikonfirmasi TANPA tahu masa depan, dan STH RP cross RP adalah confirming signal yang
tersedia secara real-time (bukan dipilih ex-post dari harga rendah).

Event definition:
  - Episode = 4 tanggal Z1->Z2 unlock historis (identik dgn Insight 7):
    2012-04-19, 2015-11-03, 2019-05-07, 2023-03-05
  - t50 = hari kalender sampai btc_price pertama kali >= 1.5x harga di tanggal unlock
  - t100 = hari kalender sampai btc_price pertama kali >= 2.0x harga di tanggal unlock
  - pct_gain_100d = % perubahan harga persis 100 hari kalender setelah tanggal unlock
    (dibandingkan langsung ke klaim "~100 hari" video)
"""

import pandas as pd

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUT_DIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-07-02_bitcoin-bottom-signal-less-than-2-weeks-away"

df = pd.read_csv(CSV, parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 1].reset_index(drop=True)

EVENTS = ["2012-04-19", "2015-11-03", "2019-05-07", "2023-03-05"]

print("=" * 90)
print("INSIGHT 12 - RALLY SPEED PASCA-BOTTOM (Z1->Z2 UNLOCK OBJEKTIF, n=4)")
print("=" * 90)
print(f"\n>>> n = {len(EVENTS)} episode Z1->Z2 unlock historis (satu per bear market cycle -- independen antar cycle,")
print("    tapi tetap catatan: masing2 cuma 1 titik data per cycle, n=4 kecil.")

rows = []
for d in EVENTS:
    ev_date = pd.Timestamp(d)
    ev_row = df[df["date"] == ev_date].iloc[0]
    p0 = ev_row["btc_price"]

    fut = df[df["date"] > ev_date]
    d50 = fut[fut["btc_price"] >= p0 * 1.5]
    d100 = fut[fut["btc_price"] >= p0 * 2.0]
    t50 = (d50["date"].iloc[0] - ev_date).days if not d50.empty else None
    t100 = (d100["date"].iloc[0] - ev_date).days if not d100.empty else None

    target_100d = ev_date + pd.Timedelta(days=100)
    row_100d = df[df["date"] >= target_100d]
    if not row_100d.empty:
        p_100d = row_100d.iloc[0]["btc_price"]
        pct_100d = (p_100d / p0 - 1) * 100
    else:
        p_100d, pct_100d = None, None

    print(f"\nEpisode {d}: p0=${p0:,.2f}")
    print(f"  Hari sampai +50%  : {t50}")
    print(f"  Hari sampai +100% : {t100}")
    print(f"  Harga tepat +100 hari kalender: ${p_100d:,.2f}  (pct_gain = {pct_100d:+.1f}%)")

    rows.append({
        "z1z2_unlock_date": d,
        "price_at_unlock": round(p0, 2),
        "days_to_plus50pct": t50,
        "days_to_plus100pct": t100,
        "price_at_plus100d": round(p_100d, 2) if p_100d is not None else None,
        "pct_gain_at_100d": round(pct_100d, 1) if pct_100d is not None else None,
    })

t50_list = [r["days_to_plus50pct"] for r in rows]
t100_list = [r["days_to_plus100pct"] for r in rows]
pct_list = [r["pct_gain_at_100d"] for r in rows]

print(f"\n{'='*90}")
print("RINGKASAN")
print(f"{'='*90}")
print(f"t50  (hari sampai +50%)  per cycle: {t50_list}  -> min={min(t50_list)}, max={max(t50_list)}")
print(f"t100 (hari sampai +100%) per cycle: {t100_list}  -> min={min(t100_list)}, max={max(t100_list)}")
print(f"pct gain PERSIS di hari ke-100 per cycle: {pct_list}")
print("\n>>> Sebaran sangat lebar (t50: 19-233 hari, t100: 50-414 hari). TIDAK konsisten ~100 hari.")
print(">>> Salah satu cycle (2015-11-03) bahkan MASIH NEGATIF di hari ke-100 (belum naik sama sekali).")

pd.DataFrame(rows).to_csv(f"{OUT_DIR}\\events_post_bottom_rally_speed.csv", index=False)
print("\nCSV disimpan: events_post_bottom_rally_speed.csv")
