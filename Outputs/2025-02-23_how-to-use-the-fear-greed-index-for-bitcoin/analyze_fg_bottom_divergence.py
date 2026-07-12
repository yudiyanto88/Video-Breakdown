import pandas as pd

df = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv", parse_dates=["date"])
df = df.sort_values("date").set_index("date")
fg = df["Fear & Greed"].ffill()
px = df["btc_price"]
sma30 = fg.rolling(30).mean()

def major_lows(series, order):
    s = series.dropna(); lows=[]
    for i in range(order, len(s)-order):
        w = s.iloc[i-order:i+order+1]
        if s.iloc[i] == w.min():
            lows.append((s.index[i], s.iloc[i]))
    merged=[]
    for d,v in lows:
        if merged and (d-merged[-1][0]).days <= order:
            if v < merged[-1][1]: merged[-1]=(d,v)
        else: merged.append((d,v))
    return merged

windows = {
    "Bear 2018": ("2018-05-01","2019-04-01"),
    "Bear 2022": ("2022-04-01","2023-01-31"),
    "Bear 2025-26 (ongoing)": ("2025-10-06", str(px.index.max().date())),
}
for name,(a,b) in windows.items():
    print("="*70); print(name)
    p = px.loc[a:b]
    for order in (45,60):
        lows = major_lows(p, order)
        print(f" order={order}d major lows:")
        for d,v in lows:
            print(f"   {d.date()} ${v:,.0f}  SMA30={sma30.loc[d]:.1f}  rawFG={fg.loc[d]:.0f}")
        for (d1,v1),(d2,v2) in zip(lows,lows[1:]):
            pdir = "LL" if v2<v1 else "HL"
            sdir = "HIGHER" if sma30.loc[d2]>sma30.loc[d1] else "LOWER"
            verdict = "REGULAR BULL DIV" if (v2<v1 and sma30.loc[d2]>sma30.loc[d1]) else ("HIDDEN BULL DIV" if (v2>v1 and sma30.loc[d2]<sma30.loc[d1]) else "no div")
            print(f"   {d1.date()} -> {d2.date()}: price {pdir}, SMA30 {sdir} ({sma30.loc[d1]:.1f}->{sma30.loc[d2]:.1f}) => {verdict}")
