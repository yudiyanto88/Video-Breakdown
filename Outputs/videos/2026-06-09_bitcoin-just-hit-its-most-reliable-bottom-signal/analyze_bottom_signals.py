"""
Validasi 5 insight video On-Chain Mind "Bitcoin Just Hit Its Most Reliable Bottom Signal"
Data: D:\\Claude Code\\Projects\\Onchain-Dashboard\\data_master_all_metrics.csv
Semua output print pakai ASCII (Windows console).

Cycle lows (dari price minima, dikonfirmasi):
  2011-11-18 ($2.05), 2015-01-14 ($178.5), 2018-12-14 ($3281), 2022-11-21 ($15774)
"""
import pandas as pd
import numpy as np

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUT = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-06-09_bitcoin-just-hit-its-most-reliable-bottom-signal"

df = pd.read_csv(CSV, parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 0].reset_index(drop=True)

LOWS = {
    "2011": pd.Timestamp("2011-11-18"),
    "2015": pd.Timestamp("2015-01-14"),
    "2018": pd.Timestamp("2018-12-14"),
    "2022": pd.Timestamp("2022-11-21"),
}

def cycle_of(date):
    """Assign a date to a cycle bottom bucket for per-cycle reporting."""
    if date < pd.Timestamp("2013-01-01"): return "2011"
    if date < pd.Timestamp("2016-06-01"): return "2015"
    if date < pd.Timestamp("2020-06-01"): return "2018"
    return "2022+"

print("="*90)
print("DATA: rows", len(df), "range", df.date.min().date(), "->", df.date.max().date())
sl = df.dropna(subset=["pct_lth_in_loss"])
print("supply/loss cols first non-null:", sl.date.min().date())
print("="*90)

# =====================================================================
# VALIDASI 1 - LTH supply-in-loss MAX di window +-60d tiap cycle low
# =====================================================================
print("\n\n### VALIDASI 1 - LTH-supply-in-loss MAX per cycle (window +-60d) ###")
v1_rows = []
for cyc, low in LOWS.items():
    w = df[(df.date >= low - pd.Timedelta(days=60)) & (df.date <= low + pd.Timedelta(days=60))]
    w = w.dropna(subset=["pct_lth_in_loss"])
    if w.empty:
        print(f"  {cyc}: NO DATA")
        continue
    mx = w.loc[w.pct_lth_in_loss.idxmax()]
    v1_rows.append({"cycle":cyc,"low_date":low.date(),"n_days":len(w),
                    "max_pct_lth_in_loss":round(mx.pct_lth_in_loss,2),
                    "date_of_max":mx.date.date(),
                    "lth_loss_at_low":round(w.set_index('date').reindex([low]).pct_lth_in_loss.iloc[0],2) if low in set(w.date) else None})
    print(f"  {cyc}: low {low.date()} | MAX pct_lth_in_loss = {mx.pct_lth_in_loss:.2f}% on {mx.date.date()} | n={len(w)}d")
pd.DataFrame(v1_rows).to_csv(OUT + r"\events_v1_lth_loss_by_cycle.csv", index=False)
print("  -> ordering check (want 2015 > 2018 > 2022):")
print("     ", " > ".join(f"{r['cycle']}:{r['max_pct_lth_in_loss']}" for r in v1_rows))

# =====================================================================
# VALIDASI 2 - 50/50 supply in profit
# =====================================================================
print("\n\n### VALIDASI 2a - percent_btc_in_profit MIN di window +-30d tiap cycle low ###")
v2a = []
for cyc, low in LOWS.items():
    w = df[(df.date >= low - pd.Timedelta(days=30)) & (df.date <= low + pd.Timedelta(days=30))]
    w = w.dropna(subset=["percent_btc_in_profit"])
    if w.empty:
        print(f"  {cyc}: NO DATA"); continue
    mn = w.loc[w.percent_btc_in_profit.idxmin()]
    v2a.append({"cycle":cyc,"low_date":low.date(),"min_pct_in_profit":round(mn.percent_btc_in_profit,2),"date_of_min":mn.date.date(),"n_days":len(w)})
    print(f"  {cyc}: MIN percent_btc_in_profit = {mn.percent_btc_in_profit:.2f}% on {mn.date.date()} | n={len(w)}d")
pd.DataFrame(v2a).to_csv(OUT + r"\events_v2_profit_min_by_cycle.csv", index=False)

print("\n### VALIDASI 2b - standalone: cross DOWN below 50%, TP/FP vs cycle low +-90d ###")
# Event: percent_btc_in_profit crosses from >=50 to <50. Merge/cooldown: 180d between crossings.
d2 = df.dropna(subset=["percent_btc_in_profit"]).reset_index(drop=True)
p = d2.percent_btc_in_profit.values
dates = d2.date.values
raw_cross = []
for i in range(1, len(d2)):
    if p[i-1] >= 50 and p[i] < 50:
        raw_cross.append(i)
# cooldown merge 180d - keep first of a cluster
COOLDOWN = 180
merged = []
last = None
for i in raw_cross:
    dt = pd.Timestamp(dates[i])
    if last is None or (dt - last).days > COOLDOWN:
        merged.append(i); last = dt
low_list = list(LOWS.values())
def near_low(dt, win=90):
    return any(abs((dt - l).days) <= win for l in low_list)
v2b = []
for i in merged:
    dt = pd.Timestamp(dates[i])
    tp = near_low(dt, 90)
    v2b.append({"cross_date":dt.date(),"price":round(d2.btc_price.values[i],2),"cycle":cycle_of(dt),"within_90d_of_low":tp})
    print(f"  cross-down {dt.date()} price=${d2.btc_price.values[i]:,.0f} cycle={cycle_of(dt)} near_low(90d)={tp}")
pd.DataFrame(v2b).to_csv(OUT + r"\events_v2_crossings.csv", index=False)
tp = sum(r["within_90d_of_low"] for r in v2b); tot = len(v2b)
print(f"  TOTAL crossings (merged {COOLDOWN}d) n={tot}, TP(near low)={tp}, FP={tot-tp}, precision={tp/tot:.0%}" if tot else "  none")

# =====================================================================
# VALIDASI 3 - rolling 30d realized profit collapse
# =====================================================================
print("\n\n### VALIDASI 3 - rolling-30d realized profit collapse ###")
print("  PROKSI: daily_realized_profit_btc * btc_price (USD notional). BUKAN Glassnode gross realized profit persis.")
d3 = df.dropna(subset=["daily_realized_profit_btc","btc_price"]).reset_index(drop=True)
d3["rp_usd"] = d3.daily_realized_profit_btc * d3.btc_price
d3["rp_30d"] = d3.rp_usd.rolling(30, min_periods=30).mean()
# per cycle: peak of rp_30d in the run-up (from prior low/cycle start to next low), and trough near the low
print("  cycle | peak rp_30d (date) | trough rp_30d near low +-90d (date) | ratio trough/peak | lead(low - trough) days")
v3 = []
cyc_bounds = [("2011","2010-07-17","2012-06-01"),("2015","2012-06-01","2015-08-01"),
              ("2018","2015-08-01","2019-06-01"),("2022","2019-06-01","2023-06-01")]
for cyc, a, b in cyc_bounds:
    low = LOWS[cyc]
    seg = d3[(d3.date>=a)&(d3.date<=b)].dropna(subset=["rp_30d"])
    if seg.empty:
        print(f"  {cyc}: NO DATA"); continue
    pk = seg.loc[seg.rp_30d.idxmax()]
    tw = d3[(d3.date>=low-pd.Timedelta(days=90))&(d3.date<=low+pd.Timedelta(days=90))].dropna(subset=["rp_30d"])
    tr = tw.loc[tw.rp_30d.idxmin()]
    ratio = tr.rp_30d/pk.rp_30d if pk.rp_30d>0 else np.nan
    lead = (low - tr.date).days
    v3.append({"cycle":cyc,"peak_date":pk.date.date(),"peak_rp30d":round(pk.rp_30d,0),
               "trough_date":tr.date.date(),"trough_rp30d":round(tr.rp_30d,0),
               "trough_over_peak":round(ratio,3),"low_minus_trough_days":lead})
    print(f"  {cyc}: peak={pk.rp_30d:,.0f}({pk.date.date()}) trough={tr.rp_30d:,.0f}({tr.date.date()}) ratio={ratio:.3f} lead(low-trough)={lead}d")
pd.DataFrame(v3).to_csv(OUT + r"\events_v3_rp30d_by_cycle.csv", index=False)

# False positives: how often does rp_30d drop to <=10% of trailing 1y peak WITHOUT being near a cycle low?
print("\n  FALSE POSITIVE scan: rp_30d <= 10% of trailing-365d rolling max, NOT within +-90d of any cycle low")
d3["rp_30d_max365"] = d3.rp_30d.rolling(365, min_periods=90).max()
d3["collapse10x"] = (d3.rp_30d <= 0.10 * d3.rp_30d_max365) & d3.rp_30d_max365.notna() & (d3.rp_30d_max365>0)
# reduce to episodes (merge consecutive/near days, 90d cooldown)
coll = d3[d3.collapse10x].reset_index(drop=True)
episodes = []
last=None
for _,r in coll.iterrows():
    if last is None or (r.date-last).days>90:
        episodes.append(r); last=r.date
    else:
        last=r.date
tp3=fp3=0; v3fp=[]
for r in episodes:
    nl = near_low(r.date,90)
    tp3 += nl; fp3 += (not nl)
    v3fp.append({"episode_date":r.date.date(),"price":round(r.btc_price,2),"cycle":cycle_of(r.date),"near_low_90d":nl})
    print(f"    episode {r.date.date()} price=${r.btc_price:,.0f} cycle={cycle_of(r.date)} near_low={nl}")
pd.DataFrame(v3fp).to_csv(OUT + r"\events_v3_collapse_episodes.csv", index=False)
print(f"    episodes n={len(episodes)}, near-low(TP)={tp3}, FP={fp3}")

# =====================================================================
# VALIDASI 4 - velocity supply-in-loss ROC 30d
# =====================================================================
print("\n\n### VALIDASI 4 - ROC30 percent_btc_in_loss (+15 pts) forward drawdown & near-low ###")
d4 = df.dropna(subset=["percent_btc_in_loss","btc_price"]).reset_index(drop=True)
d4["roc30_loss"] = d4.percent_btc_in_loss - d4.percent_btc_in_loss.shift(30)
# forward min price over next N days -> drawdown from price at signal
price = d4.btc_price.values
def fwd_dd(i, n):
    j = min(i+n, len(d4)-1)
    if i+1 > len(d4)-1: return np.nan
    fut = price[i+1:j+1]
    if len(fut)==0: return np.nan
    return (fut.min()/price[i]-1)*100
# signal days
sig = d4[d4.roc30_loss >= 15].reset_index(drop=True).copy()
# merge into episodes 30d cooldown
episodes4=[]; last=None
for _,r in sig.iterrows():
    if last is None or (r.date-last).days>30:
        episodes4.append(r); last=r.date
    else: last=r.date
print(f"  raw signal-days (ROC30>=+15): {len(sig)} ; merged episodes (30d cooldown): {len(episodes4)}")
v4=[]
for r in episodes4:
    i = d4.index[d4.date==r.date][0]
    dd30=fwd_dd(i,30); dd60=fwd_dd(i,60); dd90=fwd_dd(i,90)
    nl=near_low(r.date,60)
    v4.append({"signal_date":r.date.date(),"price":round(r.btc_price,2),"cycle":cycle_of(r.date),
               "roc30_loss":round(r.roc30_loss,1),"fwd_dd_30d_pct":round(dd30,1) if not np.isnan(dd30) else None,
               "fwd_dd_60d_pct":round(dd60,1) if not np.isnan(dd60) else None,
               "fwd_dd_90d_pct":round(dd90,1) if not np.isnan(dd90) else None,"near_low_60d":nl})
    print(f"  {r.date.date()} px=${r.btc_price:,.0f} cyc={cycle_of(r.date)} ROC30=+{r.roc30_loss:.1f} dd30={dd30:.1f}% dd60={dd60:.1f}% dd90={dd90:.1f}% near_low60={nl}")
pd.DataFrame(v4).to_csv(OUT + r"\events_v4_roc_loss_episodes.csv", index=False)
tp4=sum(x["near_low_60d"] for x in v4); tot4=len(v4)
print(f"  episodes n={tot4}, near-low(60d)={tp4}, not-near={tot4-tp4}")
# median forward dd
import statistics as st
for k in ["fwd_dd_30d_pct","fwd_dd_60d_pct","fwd_dd_90d_pct"]:
    vals=[x[k] for x in v4 if x[k] is not None]
    if vals: print(f"    median {k} = {st.median(vals):.1f}% (min {min(vals):.1f}, max {max(vals):.1f})")

# =====================================================================
# VALIDASI 5 - historical MAX percent_btc_in_loss
# =====================================================================
print("\n\n### VALIDASI 5 - historical MAX percent_btc_in_loss ###")
d5 = df.dropna(subset=["percent_btc_in_loss"])
mx5 = d5.loc[d5.percent_btc_in_loss.idxmax()]
print(f"  ALL-TIME MAX percent_btc_in_loss = {mx5.percent_btc_in_loss:.2f}% on {mx5.date.date()} price=${mx5.btc_price:,.0f}")
print(f"  Ever >= 70%? {(d5.percent_btc_in_loss>=70).any()} ; days>=60%: {(d5.percent_btc_in_loss>=60).sum()} ; days>=50%: {(d5.percent_btc_in_loss>=50).sum()}")
# top 5 highest days
top5 = d5.sort_values("percent_btc_in_loss",ascending=False).head(8)[["date","percent_btc_in_loss","btc_price"]]
print("  Top days:")
for _,r in top5.iterrows():
    print(f"    {r.date.date()} {r.percent_btc_in_loss:.2f}% ${r.btc_price:,.0f}")
print("\nDONE.")
