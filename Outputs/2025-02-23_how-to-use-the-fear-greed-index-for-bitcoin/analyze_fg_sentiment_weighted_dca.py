"""
INSIGHT C — Backtest sentiment-weighted DCA vs uniform DCA (klaim video: "historically performed well")

Definisi:
- Beli mingguan (setiap Senin), 2018-02-05 s/d data terakhir.
- Uniform : $100 tiap minggu.
- Weighted: bobot dari raw F&G pada HARI BELI (anti-lookahead — nilai tersedia di tanggal keputusan):
    F&G < 25   -> 2.0x
    25 <= F&G < 50 -> 1.5x
    50 <= F&G < 75 -> 1.0x
    F&G >= 75  -> 0.5x
- Normalisasi budget: hasil weighted di-scale supaya total spend = total spend uniform
  (dilaporkan sebagai BTC per $ dan avg cost basis — avg cost basis scale-invariant,
  jadi tidak terpengaruh normalisasi ex-post).
- Split per cycle: Cycle A = 2018-02-05..2022-11-21, Cycle B = 2022-11-22..akhir data.
- Sensitivity: varian bobot lebih agresif (3x/2x/1x/0.25x) sebagai satu cek robustness
  (bukan hunting threshold — dilaporkan apa adanya).
"""
import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

df = pd.read_csv(MASTER, usecols=["date", "btc_price", "Fear & Greed"], parse_dates=["date"])
df = df.rename(columns={"Fear & Greed": "fg"}).sort_values("date").reset_index(drop=True)
df = df[df["date"] >= "2018-02-01"].reset_index(drop=True)
df["fg"] = df["fg"].ffill()

buys = df[df["date"].dt.dayofweek == 0].copy()  # Senin

def weight(fg, scheme):
    if scheme == "base":
        return 2.0 if fg < 25 else 1.5 if fg < 50 else 1.0 if fg < 75 else 0.5
    else:  # aggressive
        return 3.0 if fg < 25 else 2.0 if fg < 50 else 1.0 if fg < 75 else 0.25

def run(sub, scheme):
    base_amt = 100.0
    w = sub["fg"].apply(lambda x: weight(x, scheme))
    spend_u = base_amt * len(sub)
    btc_u = (base_amt / sub["btc_price"]).sum()
    raw_spend_w = (base_amt * w).sum()
    raw_btc_w = (base_amt * w / sub["btc_price"]).sum()
    scale = spend_u / raw_spend_w            # normalisasi total budget sama
    btc_w = raw_btc_w * scale
    return {
        "n_buys": len(sub), "spend": spend_u,
        "btc_uniform": btc_u, "btc_weighted": btc_w,
        "cost_uniform": spend_u / btc_u, "cost_weighted": spend_u / btc_w,
        "btc_adv_pct": (btc_w / btc_u - 1) * 100,
        "w_mean": w.mean(),
        "pct_weeks_fear": (sub["fg"] < 50).mean() * 100,
    }

CYCLES = {
    "Full 2018-02..now": ("2018-02-01", str(df["date"].max().date())),
    "Cycle A 2018-2022": ("2018-02-01", "2022-11-21"),
    "Cycle B 2022-now ": ("2022-11-22", str(df["date"].max().date())),
}

for scheme, label in [("base", "BOBOT BASE (2.0/1.5/1.0/0.5)"), ("agg", "BOBOT AGRESIF (3.0/2.0/1.0/0.25)")]:
    print("=" * 95)
    print(label)
    print("=" * 95)
    print(f"{'Periode':<20}{'n beli':>7}{'%mgg F&G<50':>12}{'BTC unif':>10}{'BTC wtd':>10}"
          f"{'cost unif':>11}{'cost wtd':>11}{'BTC adv':>9}")
    for cname, (d0, d1) in CYCLES.items():
        sub = buys[(buys["date"] >= d0) & (buys["date"] <= d1)]
        r = run(sub, scheme)
        print(f"{cname:<20}{r['n_buys']:>7}{r['pct_weeks_fear']:>11.0f}%{r['btc_uniform']:>10.4f}"
              f"{r['btc_weighted']:>10.4f}{'$'+format(r['cost_uniform'],',.0f'):>11}"
              f"{'$'+format(r['cost_weighted'],',.0f'):>11}{r['btc_adv_pct']:>+8.1f}%")
    print()

# Distribusi bucket F&G per cycle (konteks kenapa hasil begitu)
print("=" * 95)
print("DISTRIBUSI MINGGU PER BUCKET F&G (hari beli)")
print("=" * 95)
for cname, (d0, d1) in CYCLES.items():
    sub = buys[(buys["date"] >= d0) & (buys["date"] <= d1)]
    b = pd.cut(sub["fg"], [0, 25, 50, 75, 101], right=False, labels=["<25", "25-50", "50-75", ">=75"])
    dist = b.value_counts(normalize=True).sort_index() * 100
    print(f"{cname}: " + "  ".join(f"{k}={v:.0f}%" for k, v in dist.items()))

# Rata-rata harga beli per bucket (mekanisme: apakah minggu fear memang harga 'murah' relatif?)
print("\nMedian F&G vs harga: korelasi mingguan F&G dgn forward return 52w (konteks, bukan klaim)")
buys2 = buys.reset_index(drop=True)
buys2["fwd52"] = buys2["btc_price"].shift(-52) / buys2["btc_price"] - 1
c = buys2[["fg", "fwd52"]].dropna().corr().iloc[0, 1]
print(f"Korelasi F&G (hari beli) vs return 52 minggu ke depan: {c:.2f}  (n={buys2['fwd52'].notna().sum()})")
