"""
Uji: jual put hanya di "fase turun" yang ditentukan zona, DCA spot di luar itu.

Zona framework asli butuh STH RP dan AVIV (tidak ada di data Coin Metrics
community). Yang bisa dihitung persis hanya Realized Price:
RP = PriceUSD / CapMVRVCur. Jadi ini uji PROXY.

Aturan mode put (dicek tiap awal siklus 30 hari):
  A  "di atas RP"            : harga >= RP
  B  "di atas RP & turun"    : harga >= RP dan harga <= 80% dari high 365 hari
  C  "di atas RP & turun 30" : harga >= RP dan harga <= 70% dari high 365 hari
Di luar mode put -> semua kas dibelikan spot (DCA).
Mekanik put sama dengan analyze_btc_cash_secured_put.py.

Pakai: python3 -I analyze_btc_put_zone_proxy.py <path btc.csv>
"""
import math, sys
import numpy as np, pandas as pd

STEP, CONTRIB, HAIRCUT = 30, 1000.0, 0.10
T = STEP / 365
d = pd.read_csv(sys.argv[1], usecols=["time", "PriceUSD", "CapMVRVCur"], parse_dates=["time"])
d = d.dropna().sort_values("time").reset_index(drop=True)
d["rp"] = d.PriceUSD / d.CapMVRVCur
d["rv30"] = np.log(d.PriceUSD).diff().rolling(30).std() * math.sqrt(365)
d["hi365"] = d.PriceUSD.rolling(365, min_periods=1).max()
d["A"] = d.PriceUSD >= d.rp
d["B"] = d.A & (d.PriceUSD <= 0.8 * d.hi365)
d["C"] = d.A & (d.PriceUSD <= 0.7 * d.hi365)
d["none"] = False
d["all"] = True

ncdf = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
def bs_put(S, K, s):
    d1 = (math.log(S / K) + 0.5 * s * s * T) / (s * math.sqrt(T)); d2 = d1 - s * math.sqrt(T)
    return K * ncdf(-d2) - S * ncdf(-d1)

def run(df, col, otm, iv_mult=1.0):
    btc = cash = inv = 0.0; n_put = fills = 0
    idx = range(0, len(df) - STEP, STEP)
    for i in idx:
        r, e = df.iloc[i], df.iloc[i + STEP]
        cash += CONTRIB; inv += CONTRIB
        if not r[col]:
            btc += cash / r.PriceUSD; cash = 0.0; continue
        n_put += 1
        K = r.PriceUSD * (1 - otm)
        n = cash / K
        prem = n * bs_put(r.PriceUSD, K, r.rv30 * iv_mult) * (1 - HAIRCUT)
        if e.PriceUSD < K:
            btc += n; cash = prem; fills += 1
        else:
            cash += prem
    end = df.iloc[list(idx)[-1] + STEP].PriceUSD
    return (btc * end + cash) / end, n_put / len(idx), (fills / n_put if n_put else float("nan"))

PERIODS = {"2016-2026": ("2016-01-01", "2026-05-23"), "2016-2018": ("2016-01-01", "2018-12-31"),
           "2019-2022": ("2019-01-01", "2022-12-31"), "2023-2026": ("2023-01-01", "2026-05-23")}
for otm in (0.0, 0.05):
    print(f"\n### Strike {int(otm*100)}% di bawah harga")
    for name, (a, b) in PERIODS.items():
        df = d[(d.time >= a) & (d.time <= b)].reset_index(drop=True)
        base = run(df, "none", otm)[0]
        out = []
        for col, lbl in [("all", "Put terus"), ("A", "A >=RP"), ("B", "B >=RP & -20%"), ("C", "C >=RP & -30%")]:
            v, share, fr = run(df, col, otm)
            out.append(f"{lbl}: {(v/base-1)*100:+.1f}% (put {share*100:.0f}% siklus)")
        print(f"{name}: " + " | ".join(out))
print("\n### Sensitivitas IV, aturan B, strike 0%, 2016-2026")
df = d[d.time >= "2016-01-01"].reset_index(drop=True); base = run(df, "none", 0)[0]
print(" | ".join(f"IV x{m}: {(run(df,'B',0.0,m)[0]/base-1)*100:+.1f}%" for m in (0.8, 1.0, 1.2, 1.4)))
