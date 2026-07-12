"""
INSIGHT B — SMA30D F&G vs raw F&G untuk trigger K5 staging (deploy saat pullback >=5% + F&G < 50)

Rekonstruksi window K5 (sesuai Decision Framework v1):
- K5 mulai : STH RP (sth_cost_basis) cross NAIK melewati RP (realized_price)  [= masuk Z2]
- K5 tutup : harga close di atas AVIV Upper 3 hari berturut-turut
             AVIV Upper = price_at_aviv_mean + 0.5*(price_at_aviv_plus_1_sigma - price_at_aviv_mean)
             (formula sesuai data_dictionary.md / pola research/analyze_k3_stage_comparison.py)
- Setelah tutup, K5 baru bisa aktif lagi setelah reset bear (STH RP turun ke bawah RP dulu).
- State awal (2018-02, F&G mulai) = 'done' (pasca top 2017) supaya tidak salah aktif.

Definisi event pullback:
- Local high = running max harga sejak K5 window mulai.
- Event mulai: hari pertama drawdown dari local high <= -5%.
- Event selesai: harga bikin running high baru, atau window K5 tutup.
- Merge: event yang mulai <14 hari setelah event sebelumnya selesai digabung.

Trigger dibandingkan (anti-lookahead, nilai di tanggal t hanya pakai data <= t):
- RAW   : hari pertama dalam event dengan raw F&G < 50
- SMA30 : hari pertama dalam event dengan SMA30(F&G) < 50
Untuk tiap trigger dicatat tanggal, harga (harga "deploy"), lead/lag.
"""
import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Video-Breakdown\Outputs\2025-02-23_fear-greed-index"

cols = ["date", "btc_price", "Fear & Greed", "sth_cost_basis", "realized_price",
        "price_at_aviv_mean", "price_at_aviv_plus_1_sigma"]
df = pd.read_csv(MASTER, usecols=cols, parse_dates=["date"]).rename(columns={"Fear & Greed": "fg"})
df = df.sort_values("date").reset_index(drop=True)
df = df[df["date"] >= "2018-02-01"].reset_index(drop=True)
df["fg"] = df["fg"].ffill()
df["fg_sma30"] = df["fg"].rolling(30, min_periods=30).mean()
df["aviv_upper"] = df["price_at_aviv_mean"] + 0.5 * (df["price_at_aviv_plus_1_sigma"] - df["price_at_aviv_mean"])

# ── State machine window K5 ──────────────────────────────────────────────────
state = "done"   # 2018-02 = pasca top 2017
streak_above_upper = 0
windows = []
w_start = None
for i in range(1, len(df)):
    sth, rp = df.at[i, "sth_cost_basis"], df.at[i, "realized_price"]
    sth_prev, rp_prev = df.at[i - 1, "sth_cost_basis"], df.at[i - 1, "realized_price"]
    price, upper = df.at[i, "btc_price"], df.at[i, "aviv_upper"]
    streak_above_upper = streak_above_upper + 1 if price > upper else 0
    if state == "done" and sth <= rp:
        state = "off"
    elif state == "off" and sth_prev <= rp_prev and sth > rp:
        state = "k5"
        w_start = i
    elif state == "k5":
        if streak_above_upper >= 3:
            windows.append((w_start, i))
            state = "done"
        elif sth < rp * 0.97:   # gagal, balik bear dalam (buffer 3% anti flip-flop)
            windows.append((w_start, i))
            state = "off"
if state == "k5":
    windows.append((w_start, len(df) - 1))

print("WINDOW K5 TEREKONSTRUKSI:")
for a, b in windows:
    print(f"  {df.at[a,'date'].date()} -> {df.at[b,'date'].date()}  "
          f"(${df.at[a,'btc_price']:,.0f} -> ${df.at[b,'btc_price']:,.0f}, {b-a} hari)")

# ── Pullback events dalam window ─────────────────────────────────────────────
events = []
for a, b in windows:
    sub = df.iloc[a:b + 1].reset_index(drop=True)
    runmax = sub["btc_price"].cummax()
    dd = sub["btc_price"] / runmax - 1
    in_event = False
    ev = None
    for j in range(len(sub)):
        if not in_event and dd[j] <= -0.05:
            in_event = True
            ev = {"start_j": j, "days": []}
        if in_event:
            ev["days"].append(j)
            new_high = sub["btc_price"].iloc[j] >= runmax.iloc[max(j - 1, 0)] and j > 0 and dd[j] >= 0
            if new_high or j == len(sub) - 1:
                ev["end_j"] = j
                ev["sub"] = sub
                ev["win"] = (df.at[a, "date"].date(), df.at[b, "date"].date())
                events.append(ev)
                in_event = False

# merge event yang mulai <14 hari setelah event sebelumnya selesai (dalam window sama)
merged = []
for ev in events:
    if merged and merged[-1]["win"] == ev["win"]:
        prev = merged[-1]
        gap = (ev["sub"]["date"].iloc[ev["start_j"]] - prev["sub"]["date"].iloc[prev["end_j"]]).days
        if gap < 14:
            prev["end_j"] = ev["end_j"]
            prev["days"] = list(range(prev["start_j"], prev["end_j"] + 1))
            continue
    merged.append(ev)
events = merged

print(f"\nTOTAL PULLBACK EVENT >=5%: n={len(events)}")
print("=" * 118)
print(f"{'Event start':>12} {'Local high':>11} {'Max DD':>7} | {'RAW<50 date':>12} {'harga':>9} | "
      f"{'SMA30<50 date':>13} {'harga':>9} | {'lag SMA':>8} {'d-harga':>8}")
print("-" * 118)

rows = []
for ev in events:
    sub = ev["sub"]
    s, e = ev["start_j"], ev["end_j"]
    seg = sub.iloc[s:e + 1]
    start_date = seg["date"].iloc[0]
    lochigh = sub["btc_price"].iloc[:s + 1].max()
    maxdd = (seg["btc_price"] / lochigh - 1).min()
    raw_hit = seg[seg["fg"] < 50]
    sma_hit = seg[seg["fg_sma30"] < 50]
    r_date = raw_hit["date"].iloc[0] if not raw_hit.empty else None
    r_price = raw_hit["btc_price"].iloc[0] if not raw_hit.empty else None
    s_date = sma_hit["date"].iloc[0] if not sma_hit.empty else None
    s_price = sma_hit["btc_price"].iloc[0] if not sma_hit.empty else None
    lag = (s_date - r_date).days if (r_date is not None and s_date is not None) else None
    dprice = (s_price / r_price - 1) * 100 if (r_price and s_price) else None
    fmt = lambda d: d.strftime("%Y-%m-%d") if d is not None else "MISS"
    fp = lambda p: f"${p:,.0f}" if p is not None else "-"
    print(f"{start_date.strftime('%Y-%m-%d'):>12} {'$'+format(lochigh,',.0f'):>11} {maxdd*100:>6.1f}% | "
          f"{fmt(r_date):>12} {fp(r_price):>9} | {fmt(s_date):>13} {fp(s_price):>9} | "
          f"{str(lag)+'d' if lag is not None else '-':>8} "
          f"{format(dprice,'+.1f')+'%' if dprice is not None else '-':>8}")
    rows.append({"window": str(ev["win"][0]) + ".." + str(ev["win"][1]),
                 "event_start": start_date.date(), "local_high": round(lochigh),
                 "max_dd_pct": round(maxdd * 100, 1),
                 "raw_trigger": r_date.date() if r_date is not None else None,
                 "raw_price": round(r_price) if r_price else None,
                 "sma30_trigger": s_date.date() if s_date is not None else None,
                 "sma30_price": round(s_price) if s_price else None,
                 "sma_lag_days": lag, "sma_price_diff_pct": round(dprice, 1) if dprice is not None else None})

rdf = pd.DataFrame(rows)
rdf.to_csv(OUTDIR + r"\events_k5_pullback_fg_triggers.csv", index=False)

n_raw = rdf["raw_trigger"].notna().sum()
n_sma = rdf["sma30_trigger"].notna().sum()
both = rdf.dropna(subset=["sma_lag_days"])
print("-" * 118)
print(f"\nRINGKASAN: n event={len(rdf)} | RAW trigger={n_raw} | SMA30 trigger={n_sma}")
if len(both):
    print(f"Event dgn dua-duanya trigger: n={len(both)} | lag SMA median={both['sma_lag_days'].median():.0f}d "
          f"(range {both['sma_lag_days'].min():.0f}..{both['sma_lag_days'].max():.0f}d)")
    print(f"Selisih harga deploy SMA vs RAW: median {both['sma_price_diff_pct'].median():+.1f}% "
          f"(range {both['sma_price_diff_pct'].min():+.1f}%..{both['sma_price_diff_pct'].max():+.1f}%)")
print(f"RAW trigger tapi SMA MISS: {int(n_raw - len(both))} | SMA trigger tapi RAW MISS: {int(n_sma - len(both))}")
print("\nSaved: events_k5_pullback_fg_triggers.csv")
