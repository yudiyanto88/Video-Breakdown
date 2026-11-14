"""
Topik 3: Klaim video -- magnitude/severity dip harga BTC di bawah realized price (dalam %,
bukan USD) mengecil tiap cycle secara monoton (makin banyak lost/locked supply di harga
tinggi -> severity dip berkurang tiap cycle).

Definisi event (eksplisit):
- Satu "dip event" = periode BTC price cross-under realized_price sampai cross-back-over
  realized_price berikutnya (kontinu, tidak ada merge/cooldown -- satu window kontinu = satu
  event, ini natural karena cross-under/cross-over sudah mendefinisikan boundary event dgn
  jelas)
- Severity = (realized_price_at_min - btc_price_min) / realized_price_at_min, dihitung
  MENGGUNAKAN realized_price PADA TANGGAL btc_price minimum tsb (at-gate, bukan realized_price
  di awal atau akhir window -- anti-lookahead: severity dihitung dari data yg tersedia PADA
  hari btc_price terendah, bukan proyeksi title masa depan)
- n = jumlah dip event kontinu yang muncul di data (bisa >1 per cycle kalau ada beberapa
  cross-under/over dalam 1 bear market -- akan di-merge secara eksplisit kalau jaraknya < 30
  hari cooldown, supaya tidak overcount noise micro-crossing sebagai event terpisah)
"""
import pandas as pd
import numpy as np

df = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv", parse_dates=["date"])
df = df[["date", "btc_price", "realized_price"]].dropna().reset_index(drop=True)
df = df.sort_values("date").reset_index(drop=True)

df["below"] = df["btc_price"] < df["realized_price"]

# Identify contiguous below-RP segments
segments = []
in_seg = False
start_idx = None
for i in range(len(df)):
    if df["below"].iloc[i] and not in_seg:
        in_seg = True
        start_idx = i
    elif not df["below"].iloc[i] and in_seg:
        in_seg = False
        segments.append((start_idx, i - 1))
if in_seg:
    segments.append((start_idx, len(df) - 1))

print(f"Raw contiguous below-RP segments (sebelum merge): {len(segments)}")

# Merge segments separated by < COOLDOWN_DAYS (noise micro cross-over)
COOLDOWN_DAYS = 30
merged = []
for seg in segments:
    if merged:
        prev_start, prev_end = merged[-1]
        gap_days = (df["date"].iloc[seg[0]] - df["date"].iloc[prev_end]).days
        if gap_days < COOLDOWN_DAYS:
            merged[-1] = (prev_start, seg[1])
            continue
    merged.append(seg)

print(f"Segments setelah merge (cooldown {COOLDOWN_DAYS}d antar segmen berdekatan): {len(merged)}")

rows = []
for s, e in merged:
    seg_df = df.iloc[s:e+1]
    min_idx_local = seg_df["btc_price"].idxmin()
    min_row = df.loc[min_idx_local]
    rp_at_min = min_row["realized_price"]
    price_at_min = min_row["btc_price"]
    severity = (rp_at_min - price_at_min) / rp_at_min
    rows.append({
        "start": df["date"].iloc[s].date(),
        "end": df["date"].iloc[e].date(),
        "date_min_price": min_row["date"].date(),
        "btc_price_min": price_at_min,
        "realized_price_at_min": rp_at_min,
        "severity_pct": severity * 100,
        "duration_days": (df["date"].iloc[e] - df["date"].iloc[s]).days,
    })

events = pd.DataFrame(rows)
print(f"\n=== Dip-below-RP events (n = {len(events)}) ===")
print(events.to_string(index=False))

# Assign cycle label based on approximate year for clarity
def label_cycle(d):
    y = d.year
    if y <= 2012: return "2011-12 (post-2011 peak)"
    if y <= 2016: return "2014-16 (post-2013 peak)"
    if y <= 2019: return "2018-19 (post-2017 peak)"
    if y <= 2020: return "2020 (COVID crash)"
    if y <= 2023: return "2022-23 (post-2021 peak)"
    return "2024+ (current)"

events["cycle_label"] = events["date_min_price"].apply(label_cycle)
print("\n=== Dengan label cycle ===")
print(events[["cycle_label", "date_min_price", "severity_pct", "duration_days"]].to_string(index=False))

sev = events["severity_pct"].values
diffs = np.diff(sev)
print("\nSelisih severity berurutan (event[i+1] - event[i]):", [round(d, 2) for d in diffs])
print("Monoton MENGECIL (setiap langkah < 0)?", all(d < 0 for d in diffs))

print(f"\nn total event = {len(events)}")
print("Sebaran per cycle:")
print(events["cycle_label"].value_counts())

# ─── Per-cycle MAX severity (the "defining" cycle trough, satu per cycle bull-bear penuh) ──
# COVID 2020 di-flag terpisah: bukan cycle top->bottom penuh, tapi exogenous crash MID-cycle
# (recovery cepat, bukan bear market terminal) -- tidak dihitung sbg "cycle trough" tersendiri.
print("\n" + "=" * 70)
print("=== VIEW UTAMA: severity MAKSIMUM per cycle bull-bear PENUH (n=4) ===")
print("=" * 70)
full_cycles = {
    "2011-12": ("2011-08-01", "2012-06-01"),
    "2014-16": ("2014-06-01", "2015-12-31"),
    "2018-19": ("2018-06-01", "2019-03-01"),
    "2022-23": ("2022-01-01", "2022-12-31"),
}
cyc_rows = []
for name, (s, e) in full_cycles.items():
    sub = df[(df["date"] >= s) & (df["date"] <= e)]
    sub_below = sub[sub["btc_price"] < sub["realized_price"]]
    if sub_below.empty:
        continue
    row = sub_below.loc[sub_below["btc_price"].idxmin()]
    sev = (row["realized_price"] - row["btc_price"]) / row["realized_price"] * 100
    cyc_rows.append({"cycle": name, "date_min": row["date"].date(), "severity_pct": sev})

cyc_df = pd.DataFrame(cyc_rows)
print(cyc_df.to_string(index=False))
sev_vals = cyc_df["severity_pct"].values
print("\nSelisih berurutan:", [round(d, 2) for d in np.diff(sev_vals)])
print("Monoton MENGECIL di 4 cycle penuh ini?", all(d < 0 for d in np.diff(sev_vals)))
print("\nCATATAN: severity = (RP - price)/RP = 1 - MVRV_ratio pada titik trough. Ini SECARA")
print("MATEMATIS sama dengan klaim Topik 2 (trough MVRV naik monoton) -- BUKAN bukti independen")
print("baru, hanya reframing unit yang sama (1 - MVRV = severity %).")
print("\nCOVID 2020-03 (severity 15.10%, 6 hari) dikeluarkan dari view utama krn bukan cycle")
print("top->bottom penuh (exogenous shock, recovery <1 bulan, bukan bear market terminal).")
print("Kalau COVID dimasukkan sbg titik tersendiri di antara 2018-19 dan 2022-23, urutannya")
print("jadi 29.75 -> 15.10 -> 22.34 -- BUKAN monoton (naik lagi di 2022-23).")
