"""
Uji: saat kondisi K4 (akumulasi di dasar bear), lebih baik DCA spot atau jual put?

K4 asli: harga di Z1 (harga < STH RP < RP) + hitungan 4 kondisi (LTH-MVRV<1,
aSOPR/LTH-SOPR, Supply in Profit, Price/CVDD). Data itu tidak ada di Coin Metrics
community data. PROXY yang dipakai: MVRV < 1 (harga di bawah Realized Price).

Episode = rangkaian hari MVRV<1, digabung kalau jeda < 30 hari, minimal 30 hari.
Di dalam episode, tiap 30 hari masuk $1000:
  - DCA: beli spot
  - Put d%: jual put 30 hari di strike harga x (1-d), semua kas jadi jaminan
Akhir episode: sisa kas dibelikan spot di harga akhir episode.
Ukuran: jumlah BTC akhir vs DCA.
Pakai: python3 -I analyze_btc_put_k4_proxy.py <path btc.csv>
"""
import math, sys
import numpy as np, pandas as pd

STEP, CONTRIB, HAIRCUT = 30, 1000.0, 0.10
T = STEP / 365
d = pd.read_csv(sys.argv[1], usecols=["time", "PriceUSD", "CapMVRVCur"], parse_dates=["time"])
d = d.dropna().sort_values("time").reset_index(drop=True)
d["rv30"] = np.log(d.PriceUSD).diff().rolling(30).std() * math.sqrt(365)
d = d[d.time >= "2011-06-01"].reset_index(drop=True)

ncdf = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
def bs_put(S, K, s):
    d1 = (math.log(S / K) + 0.5 * s * s * T) / (s * math.sqrt(T)); d2 = d1 - s * math.sqrt(T)
    return K * ncdf(-d2) - S * ncdf(-d1)

# episode MVRV<1
below = d.CapMVRVCur < 1
eps, start, last = [], None, None
for i, b in enumerate(below):
    if b:
        if start is None: start = i
        elif i - last > 30: eps.append((start, last)); start = i
        last = i
if start is not None: eps.append((start, last))
eps = [(a, b) for a, b in eps if b - a >= 30]

def run(seg, otm, iv_mult=1.0):
    btc = cash = 0.0; fills = n = 0; prem_sum = 0.0
    for i in range(0, len(seg) - STEP, STEP):
        r, e = seg.iloc[i], seg.iloc[i + STEP]
        cash += CONTRIB
        if otm is None:
            btc += cash / r.PriceUSD; cash = 0.0; continue
        K = r.PriceUSD * (1 - otm); q = cash / K
        p = bs_put(r.PriceUSD, K, r.rv30 * iv_mult) * (1 - HAIRCUT)
        prem_sum += p / K; n += 1
        if e.PriceUSD < K: btc += q; cash = q * p; fills += 1
        else: cash += q * p
    end = seg.iloc[-1].PriceUSD
    return btc + cash / end, (fills / n if n else np.nan), (prem_sum / n if n else np.nan)

rows = []
for a, b in eps:
    seg = d.iloc[a:b + 1].reset_index(drop=True)
    if len(seg) < STEP + 1: continue
    base = run(seg, None)[0]
    row = {"episode": f"{seg.time.iloc[0]:%Y-%m-%d} s/d {seg.time.iloc[-1]:%Y-%m-%d}",
           "hari": len(seg),
           "harga": f"{seg.PriceUSD.iloc[0]:,.0f} -> {seg.PriceUSD.iloc[-1]:,.0f} (min {seg.PriceUSD.min():,.0f})",
           "IV_median": round(seg.rv30.median(), 2)}
    for otm in (0.0, 0.05, 0.10):
        v, fr, pm = run(seg, otm)
        row[f"put{int(otm*100)}%"] = f"{(v/base-1)*100:+.1f}% (isi {fr*100:.0f}%, premi {pm*100:.1f}%/bln)"
    rows.append(row)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
print(pd.DataFrame(rows).to_string(index=False))

print("\nSensitivitas IV, put ATM, per episode:")
for a, b in eps:
    seg = d.iloc[a:b + 1].reset_index(drop=True)
    if len(seg) < STEP + 1: continue
    base = run(seg, None)[0]
    print(f"  {seg.time.iloc[0]:%Y-%m}: " + " | ".join(f"x{m}: {(run(seg,0.0,m)[0]/base-1)*100:+.1f}%" for m in (0.8, 1.0, 1.2, 1.4)))
