"""
Validasi Insight B — Realized Profit Collapse = floor? (On-Chain Mind, 2025-01-27)

Klaim video: realized profit anjlok ($10B/hari Des -> $2-3B/hari Jan) berarti
heavy selling sudah lewat -> floor terbentuk.

Metrik: rrp (relative realized profit = realized profit / market cap) SMA7
        -> comparable antar cycle (USD absolut tidak).

Definisi event (ditetapkan SEBELUM lihat hasil):
  - rrp_sma7(t) <= 0.30 * peak60(t), dengan peak60 = rolling max 60d BERAKHIR di t
    (drop >=70% dari local peak 60 hari — at-gate, no lookahead)
  - konteks bull: btc_price(t) > realized_price(t)  (Z3+ proxy: harga di atas RP)
  - syarat peak bermakna: peak60 >= median full-history rrp_sma7 sampai t
    (expanding median, at-gate) — supaya bukan noise saat rrp memang selalu kecil
  - event = hari PERTAMA kondisi true; cooldown 60d antar event

Outcome (window ground-truth 90 hari):
  - max drawdown dari harga event dalam 90d (pakai low harian close)
  - forward return 60d dan 90d
  - "floor OK" = maxDD < 15% DAN fwd90 > 0
  - false positive keras = close di bawah RP dalam 90d setelah event

Uji inkremental vs K2 kondisi #2 (SOPR reset):
  K2 cond2 = STH-SOPR < 0.97 (belum bertahan >14d) DAN aSOPR > 0.95.
  Untuk tiap event: apakah K2 cond2 aktif dalam window [event-14d, event+14d]?
  Kalau hampir semua event tertangkap SOPR reset -> tidak ada nilai inkremental.
"""
import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Video-Breakdown\Outputs\2025-01-27_bitcoin-whales-are-accumulating-right-now"

df = pd.read_csv(MASTER, parse_dates=["date"], usecols=[
    "date","btc_price","realized_price","rrp","asopr","sth_sopr"])
df = df.sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 0.1].dropna(subset=["rrp","realized_price"]).reset_index(drop=True)

df["rrp7"]   = df["rrp"].rolling(7, min_periods=7).mean()
df["peak60"] = df["rrp7"].rolling(60, min_periods=60).max()
df["med_exp"]= df["rrp7"].expanding(min_periods=180).median()

df["cond"] = (df["rrp7"] <= 0.30*df["peak60"]) & \
             (df["btc_price"] > df["realized_price"]) & \
             (df["peak60"] >= df["med_exp"])

def cycle_of(d):
    if d <= pd.Timestamp("2015-01-14"): return "c2013"
    if d <= pd.Timestamp("2018-12-15"): return "c2017"
    if d <= pd.Timestamp("2022-11-21"): return "c2021"
    return "c2024"
df["cycle"] = df["date"].apply(cycle_of)

# K2 cond2 di tiap hari: sth_sopr<0.97 & belum >14 hari berturut & asopr>0.95
below = (df["sth_sopr"] < 0.97).values
streak = np.zeros(len(df), dtype=int)
for i in range(len(df)):
    streak[i] = streak[i-1]+1 if (below[i] and i>0) else (1 if below[i] else 0)
df["k2c2"] = below & (streak <= 14) & (df["asopr"] > 0.95).values

# Events
events = []
last = None
cond = df["cond"].values
for i in range(1, len(df)):
    if cond[i] and not cond[i-1]:
        if last is None or (df.at[i,"date"] - last).days > 60:
            events.append(i); last = df.at[i,"date"]

px = df["btc_price"].values
rp = df["realized_price"].values
rows = []
for i in events:
    d = df.at[i,"date"]
    w = df.iloc[i+1:i+91]
    if len(w) < 90:
        fwd60 = fwd90 = maxdd = below_rp = None
    else:
        fwd60 = px[i+60]/px[i]-1
        fwd90 = px[i+90]/px[i]-1
        maxdd = w["btc_price"].min()/px[i]-1
        below_rp = bool((w["btc_price"] < w["realized_price"]).any())
    # K2 cond2 dalam [-14,+14]
    lo, hi = max(0,i-14), min(len(df)-1, i+14)
    k2hit = bool(df["k2c2"].iloc[lo:hi+1].any())
    rows.append(dict(date=d, cycle=df.at[i,"cycle"], price=px[i],
                     rrp7=df.at[i,"rrp7"], peak60=df.at[i,"peak60"],
                     fwd60=fwd60, fwd90=fwd90, maxdd=maxdd,
                     below_rp_90d=below_rp, k2c2_pm14d=k2hit))
ev = pd.DataFrame(rows)

print("="*110)
print("EVENT: rrp SMA7 turun >=70% dari peak 60d, harga > RP, cooldown 60d")
print(f"n_event={len(ev)}  sebaran cycle: {ev['cycle'].value_counts().to_dict()}")
print("-"*110)
for _, r in ev.iterrows():
    if r["fwd90"] is None or pd.isna(r["fwd90"]):
        print(f"  {r['date'].date()} [{r['cycle']}] px=${r['price']:>10,.0f}  (window 90d belum lengkap)")
        continue
    ok = (r["maxdd"] > -0.15) and (r["fwd90"] > 0)
    print(f"  {r['date'].date()} [{r['cycle']}] px=${r['price']:>10,.0f}  "
          f"maxDD={r['maxdd']*100:+6.1f}%  fwd60={r['fwd60']*100:+7.1f}%  fwd90={r['fwd90']*100:+7.1f}%  "
          f"belowRP90d={'YA' if r['below_rp_90d'] else 'tdk'}  K2c2±14d={'YA' if r['k2c2_pm14d'] else 'TIDAK'}  "
          f"floorOK={'YA' if ok else 'TIDAK'}")

full = ev.dropna(subset=["fwd90"])
ok   = full[(full["maxdd"] > -0.15) & (full["fwd90"] > 0)]
fp   = full[full["below_rp_90d"] == True]
print("-"*110)
print(f"Dengan window lengkap: n={len(full)}")
print(f"  'floor OK' (maxDD<15% & fwd90>0): {len(ok)}/{len(full)} = {len(ok)/max(len(full),1)*100:.0f}%")
print(f"  false positive keras (close < RP dalam 90d): {len(fp)}/{len(full)} = {len(fp)/max(len(full),1)*100:.0f}%")
print(f"  median maxDD={full['maxdd'].median()*100:+.1f}%  fwd60={full['fwd60'].median()*100:+.1f}%  fwd90={full['fwd90'].median()*100:+.1f}%")
print(f"  per cycle 'floor OK':")
for c in ["c2013","c2017","c2021","c2024"]:
    s = full[full["cycle"]==c]
    o = s[(s["maxdd"]>-0.15)&(s["fwd90"]>0)]
    print(f"    {c}: {len(o)}/{len(s)}")

# Baseline: semua hari dengan harga > RP
df["fwd90"] = df["btc_price"].shift(-90)/df["btc_price"]-1
base = df[(df["btc_price"]>df["realized_price"]) & df["fwd90"].notna()]
# baseline maxDD 90d
roll_min = df["btc_price"][::-1].rolling(90,min_periods=90).min()[::-1].shift(-1)
df["maxdd90"] = roll_min/df["btc_price"]-1
baseh = df[(df["btc_price"]>df["realized_price"]) & df["maxdd90"].notna()]
b_ok = baseh[(baseh["maxdd90"]>-0.15)&(baseh["fwd90"]>0)]
print(f"\nBASELINE semua hari harga>RP (n={len(baseh)}, day-level, tidak independen):")
print(f"  'floor OK' rate: {len(b_ok)/len(baseh)*100:.0f}%   median fwd90={baseh['fwd90'].median()*100:+.1f}%  median maxDD={baseh['maxdd90'].median()*100:+.1f}%")

# Inkremental
n_k2 = int(full["k2c2_pm14d"].sum())
print(f"\nINKREMENTAL vs K2 kondisi #2:")
print(f"  event dgn K2c2 aktif dalam ±14d: {n_k2}/{len(full)}")
no_k2 = full[~full["k2c2_pm14d"]]
if len(no_k2):
    o = no_k2[(no_k2["maxdd"]>-0.15)&(no_k2["fwd90"]>0)]
    print(f"  event TANPA K2c2 (kandidat nilai inkremental): {len(no_k2)}, 'floor OK' di antaranya: {len(o)}/{len(no_k2)}")
    for _, r in no_k2.iterrows():
        print(f"    {r['date'].date()} [{r['cycle']}] maxDD={r['maxdd']*100:+.1f}% fwd90={r['fwd90']*100:+.1f}%")

ev.to_csv(rf"{OUTDIR}\events_realized_profit_collapse.csv", index=False)
print("\nSaved: events_realized_profit_collapse.csv")
