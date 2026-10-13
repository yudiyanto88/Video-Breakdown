"""
Simulasi akumulasi BTC: DCA spot vs jual cash-secured put bulanan.

Data: Coin Metrics community data (github.com/coinmetrics/data, csv/btc.csv),
kolom PriceUSD (harga penutupan harian) dan CapMVRVCur.

PENTING: premi option TIDAK berasal dari data historis asli (Deribit diblokir
dari sandbox). Premi dihitung dengan Black-Scholes memakai volatilitas
realisasi 30 hari x pengali (IV_MULT). Pengali 1.0 = anggap pasar memasang
harga volatilitas sama dengan yang baru saja terjadi. Hasil sensitif terhadap
anggapan ini, jadi dijalankan beberapa pengali.

Aturan:
- Setiap 30 hari masuk modal baru $1000.
- DCA: langsung beli BTC di harga penutupan.
- PUT_d: semua kas jadi jaminan, jual put 30 hari strike = harga x (1-d).
  Premi (dipotong HAIRCUT untuk biaya + spread) masuk kas di depan.
  Saat expiry: kalau harga < strike, seluruh kas dipakai beli BTC di strike.
- HYBRID_d: sama dengan PUT_d, tapi kalau 3 siklus berturut-turut tidak
  terisi, seluruh kas dibelikan spot.
- MVRV_SWITCH: kalau MVRV di bawah median 4 tahun terakhir -> DCA spot
  (semua kas dibelikan). Kalau di atas -> PUT 10% OTM.
- Kas tidak diberi bunga (berlaku sama untuk semua strategi).

Pakai: python3 -I analyze_btc_cash_secured_put.py <path ke btc.csv>
"""
import math
import sys

import numpy as np
import pandas as pd

CSV = sys.argv[1]
STEP = 30
T = STEP / 365
CONTRIB = 1000.0
HAIRCUT = 0.10

raw = pd.read_csv(CSV, usecols=["time", "PriceUSD", "CapMVRVCur"], parse_dates=["time"])
raw = raw.dropna(subset=["PriceUSD"]).sort_values("time").reset_index(drop=True)
raw["ret"] = np.log(raw["PriceUSD"]).diff()
raw["rv30"] = raw["ret"].rolling(30).std() * math.sqrt(365)
raw["mvrv_med4y"] = raw["CapMVRVCur"].rolling(1460, min_periods=730).median()


def ncdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def bs_put(S, K, sigma):
    if sigma <= 0:
        return max(K - S, 0.0)
    d1 = (math.log(S / K) + 0.5 * sigma**2 * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return K * ncdf(-d2) - S * ncdf(-d1)


def run(df, mode, otm=0.10, iv_mult=1.0, hybrid_wait=3):
    idx = list(range(0, len(df) - STEP, STEP))
    btc = cash = invested = 0.0
    fills = cycles = waits = 0
    prem_yields, ratio_series, cash_share = [], [], []
    for i in idx:
        row, end = df.iloc[i], df.iloc[i + STEP]
        S, ST = row.PriceUSD, end.PriceUSD
        cash += CONTRIB
        invested += CONTRIB

        use_put = mode in ("put", "hybrid")
        if mode == "dca":
            use_put = False
        if mode == "mvrv":
            use_put = pd.notna(row.mvrv_med4y) and row.CapMVRVCur > row.mvrv_med4y

        if not use_put:
            btc += cash / S
            cash = 0.0
        else:
            K = S * (1 - otm)
            p = bs_put(S, K, row.rv30 * iv_mult) * (1 - HAIRCUT)
            n = cash / K
            prem = n * p
            prem_yields.append(p / K)
            cycles += 1
            if ST < K:
                btc += n
                cash = prem
                fills += 1
                waits = 0
            else:
                cash += prem
                waits += 1
                if mode == "hybrid" and waits >= hybrid_wait:
                    btc += cash / ST
                    cash = 0.0
                    waits = 0
        val = btc * ST + cash
        ratio_series.append(val / invested)
        cash_share.append(cash / val if val else 0)

    S_end = df.iloc[idx[-1] + STEP].PriceUSD
    value = btc * S_end + cash
    r = np.array(ratio_series)
    dd = (r / np.maximum.accumulate(r) - 1).min()
    return {
        "invested": invested,
        "value": value,
        "multiple": value / invested,
        "btc_equiv": value / S_end,
        "fill_rate": fills / cycles if cycles else np.nan,
        "avg_prem_month": np.mean(prem_yields) if prem_yields else np.nan,
        "avg_cash_share": float(np.mean(cash_share)),
        "max_dd": dd,
    }


PERIODS = {
    "2016-01 s/d 2026-05 (penuh)": ("2016-01-01", "2026-05-23"),
    "2016-01 s/d 2018-12": ("2016-01-01", "2018-12-31"),
    "2019-01 s/d 2022-12": ("2019-01-01", "2022-12-31"),
    "2023-01 s/d 2026-05": ("2023-01-01", "2026-05-23"),
}

STRATS = [("DCA spot", "dca", 0, 1.0)]
for d in (0.0, 0.05, 0.10, 0.15):
    STRATS.append((f"Put {int(d*100)}% OTM", "put", d, 1.0))
for d in (0.05, 0.10):
    STRATS.append((f"Hybrid {int(d*100)}% (3 bln)", "hybrid", d, 1.0))
STRATS.append(("MVRV switch (put 10%)", "mvrv", 0.10, 1.0))

pd.set_option("display.width", 200)
for name, (a, b) in PERIODS.items():
    df = raw[(raw.time >= a) & (raw.time <= b)].reset_index(drop=True)
    rows = []
    for label, mode, otm, m in STRATS:
        r = run(df, mode, otm, m)
        r["strategi"] = label
        rows.append(r)
    out = pd.DataFrame(rows).set_index("strategi")
    base = out.loc["DCA spot", "btc_equiv"]
    out["vs_DCA_%"] = (out["btc_equiv"] / base - 1) * 100
    print(f"\n=== {name} ===")
    print(out[["invested", "multiple", "btc_equiv", "vs_DCA_%", "fill_rate",
               "avg_prem_month", "avg_cash_share", "max_dd"]].round(4).to_string())

print("\n=== Sensitivitas pengali IV (periode penuh) ===")
df = raw[(raw.time >= "2016-01-01")].reset_index(drop=True)
base = run(df, "dca")["btc_equiv"]
for m in (0.8, 1.0, 1.2, 1.4):
    line = []
    for label, mode, otm in [("Put 5%", "put", 0.05), ("Put 10%", "put", 0.10),
                             ("Hybrid 10%", "hybrid", 0.10), ("MVRV switch", "mvrv", 0.10)]:
        r = run(df, mode, otm, m)
        line.append(f"{label}: {(r['btc_equiv']/base-1)*100:+.1f}%")
    print(f"IV x{m}: " + " | ".join(line))
