"""
Validasi: Bitcoin Bear Market Drawdown Model (presenter: Bitcoin Magazine Pro, video 2026-06-08)

Klaim: rasio (bear log-drawdown / bull log-return) untuk 2013->2015, 2017->2018, 2021->2022
adalah 0.312 / 0.384 / 0.483. Rata-rata 0.393 (1SD range 0.363-0.504) diterapkan ke bull run
current (log-return 2.099 dari return 715.47%, ATH $126,219.03) -> central $55,311,
worst-case (ratio tertinggi, mean+1SD) $43,830, optimistic (ratio 2013) $65,528.

(a) Reproduksi rasio dari btc_price aktual untuk 3 cycle historis.
(b) Bandingkan proyeksi mean+-1SD (3 titik) vs regresi linear 3 titik (extrapolasi tren monoton).
(c) Bandingkan level $43,830 & $55,311 terhadap Realized Price & LTH Realized Price SAAT INI (data terbaru).

n=3 cycle historis untuk fitting -- LOW-CONFIDENCE SAMPLE SIZE, wajib di-flag tebal.
"""

import pandas as pd
import numpy as np

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

df = pd.read_csv(CSV, parse_dates=["date"])
df = df[["date", "btc_price", "realized_price", "lth_cost_basis"]].dropna(subset=["btc_price"])
df = df[df["btc_price"] > 0].sort_values("date").reset_index(drop=True)

def window_extreme(d0, d1, kind="max"):
    w = df[(df["date"] >= d0) & (df["date"] <= d1)]
    if w.empty:
        return None, None
    if kind == "max":
        row = w.loc[w["btc_price"].idxmax()]
    else:
        row = w.loc[w["btc_price"].idxmin()]
    return row["date"], row["btc_price"]

print("=" * 100)
print("(a) REPRODUKSI RASIO BEAR-LOG-DRAWDOWN / BULL-LOG-RETURN DARI DATA AKTUAL (btc_price)")
print("=" * 100)

# Cycle definitions -- peak/trough via local extrema windows (bukan titik tunggal dipilih manual)
cycles_def = [
    ("2013->2015", "2011-10-01", "2012-06-30", "2012-07-01", "2013-12-31", "2013-12-01", "2015-06-30"),
    ("2017->2018", "2015-01-01", "2015-06-30", "2015-07-01", "2018-01-01", "2018-01-01", "2019-06-30"),
    ("2021->2022", "2018-06-01", "2019-06-30", "2019-07-01", "2021-12-31", "2021-11-01", "2023-06-30"),
]

reproduced = []
for name, low_lo, low_hi, peak_lo, peak_hi, bear_lo, bear_hi in cycles_def:
    low_date, low_price   = window_extreme(low_lo, low_hi, "min")
    peak_date, peak_price = window_extreme(peak_lo, peak_hi, "max")
    bear_date, bear_price = window_extreme(peak_date, bear_hi, "min")  # search from actual peak date onward

    bull_log_return = np.log(peak_price / low_price)
    bear_log_dd     = np.log(peak_price / bear_price)
    ratio = bear_log_dd / bull_log_return

    reproduced.append({
        "cycle": name, "low_date": low_date, "low_price": low_price,
        "peak_date": peak_date, "peak_price": peak_price,
        "bear_date": bear_date, "bear_price": bear_price,
        "bull_log_return": bull_log_return, "bear_log_dd": bear_log_dd, "ratio": ratio,
    })

    print(f"\n{name}")
    print(f"  Bull low : {low_date.date()}  price=${low_price:,.2f}")
    print(f"  Peak     : {peak_date.date()}  price=${peak_price:,.2f}")
    print(f"  Bear low : {bear_date.date()}  price=${bear_price:,.2f}")
    print(f"  Bull log-return = {bull_log_return:.3f} | Bear log-drawdown = {bear_log_dd:.3f} | RATIO = {ratio:.3f}")

presenter_ratios = {"2013->2015": 0.312, "2017->2018": 0.384, "2021->2022": 0.483}
print("\n--- Perbandingan vs klaim presenter ---")
for r in reproduced:
    claimed = presenter_ratios[r["cycle"]]
    print(f"  {r['cycle']:<12} reproduksi={r['ratio']:.3f}  klaim presenter={claimed:.3f}  selisih={r['ratio']-claimed:+.3f}")

ratios = [r["ratio"] for r in reproduced]
mean_ratio = np.mean(ratios)
std_ratio  = np.std(ratios, ddof=1)
print(f"\nMean ratio (reproduksi n=3) = {mean_ratio:.3f}  |  SD = {std_ratio:.3f}  |  1SD range = [{mean_ratio-std_ratio:.3f}, {mean_ratio+std_ratio:.3f}]")
print(f"(Klaim presenter: mean=0.393, range 0.363-0.504)")

print("\n" + "=" * 100)
print("(b) PROYEKSI: mean+-1SD (3 titik) vs REGRESI LINEAR (extrapolasi tren monoton ke titik ke-4)")
print("=" * 100)

# Current cycle bull log return -- reproduksi dari data aktual: low 2022-11 -> ATH terkini
cur_low_date, cur_low_price = window_extreme("2022-06-01", "2023-06-30", "min")
cur_peak_date, cur_peak_price = window_extreme("2023-07-01", "2026-07-15", "max")
cur_bull_log_return = np.log(cur_peak_price / cur_low_price)
print(f"\nCurrent cycle (reproduksi data aktual): low={cur_low_date.date()} (${cur_low_price:,.2f}) -> "
      f"peak={cur_peak_date.date()} (${cur_peak_price:,.2f})")
print(f"Current bull log-return (reproduksi) = {cur_bull_log_return:.3f}  (klaim presenter: 2.099 dari ATH $126,219.03)")

# Pakai basis presenter (log-return 2.099, ATH 126219.03) supaya apple-to-apple dgn video,
# TAPI juga tampilkan versi full-reproduksi untuk cross-check.
PRESENTER_ATH = 126219.03
PRESENTER_LOG_RETURN = 2.099

def price_from_ratio(ratio, ath, log_return):
    bear_log_dd = ratio * log_return
    return ath / np.exp(bear_log_dd)

# --- Metode 1: mean +- 1SD dari 3 titik (metode presenter) ---
print("\n--- Metode 1: mean +- 1SD (cara presenter) ---")
for label, ratio_val in [("mean-1SD", mean_ratio - std_ratio), ("mean", mean_ratio), ("mean+1SD", mean_ratio + std_ratio)]:
    p = price_from_ratio(ratio_val, PRESENTER_ATH, PRESENTER_LOG_RETURN)
    print(f"  {label:<10} ratio={ratio_val:.3f}  -> proyeksi harga = ${p:,.0f}")

# --- Metode 2: regresi linear 3 titik (ratio vs urutan cycle), extrapolate ke titik ke-4 ---
print("\n--- Metode 2: regresi linear 3 titik (treat sbg tren monoton naik), extrapolate ke cycle ke-4 ---")
x = np.array([1, 2, 3])
y = np.array(ratios)
slope, intercept = np.polyfit(x, y, 1)
ratio_cycle4 = slope * 4 + intercept
print(f"  Slope={slope:.4f}, intercept={intercept:.4f}")
print(f"  Ratio cycles: {dict(zip([r['cycle'] for r in reproduced], [round(rr,3) for rr in ratios]))}")
print(f"  Extrapolasi ratio cycle ke-4 (linear) = {ratio_cycle4:.3f}")
p_linear = price_from_ratio(ratio_cycle4, PRESENTER_ATH, PRESENTER_LOG_RETURN)
print(f"  Proyeksi harga (linear-trend method) = ${p_linear:,.0f}")

p_central_presenter = price_from_ratio(mean_ratio, PRESENTER_ATH, PRESENTER_LOG_RETURN)
print(f"\nSelisih proyeksi: linear-trend (${p_linear:,.0f}) vs mean-based central (${p_central_presenter:,.0f}) "
      f"= ${p_central_presenter - p_linear:,.0f} ({(p_central_presenter/p_linear - 1)*100:+.1f}%)")

print("\n" + "=" * 100)
print("(c) BANDINGKAN $43,830 (worst-case) & $55,311 (central) vs REALIZED PRICE & LTH REALIZED PRICE SAAT INI")
print("=" * 100)

latest = df.iloc[-1]
print(f"\nData terbaru: {latest['date'].date()}")
print(f"  btc_price          = ${latest['btc_price']:,.2f}")
print(f"  realized_price (RP)= ${latest['realized_price']:,.2f}")
print(f"  lth_cost_basis (LTH RP) = ${latest['lth_cost_basis']:,.2f}")

for label, price in [("Worst-case $43,830", 43830), ("Central $55,311", 55311)]:
    vs_rp  = (price / latest["realized_price"] - 1) * 100
    vs_lth = (price / latest["lth_cost_basis"] - 1) * 100
    print(f"\n  {label}:")
    print(f"    vs RP terkini      : {vs_rp:+.1f}%  ({'DI ATAS RP' if vs_rp>0 else 'DI BAWAH RP'})")
    print(f"    vs LTH RP terkini  : {vs_lth:+.1f}%  ({'DI ATAS LTH RP' if vs_lth>0 else 'DI BAWAH LTH RP'})")

print("\n--- Historical check: berapa kali harga BTC pernah jauh di bawah LTH RP secara persisten? ---")
df["below_lth_rp"] = df["btc_price"] < df["lth_cost_basis"]
# episode grouping
below = df["below_lth_rp"].values
episodes = []
i = 0
while i < len(below):
    if below[i]:
        j = i
        while j < len(below) and below[j]:
            j += 1
        episodes.append((df["date"].iloc[i], df["date"].iloc[j-1], j - i))
        i = j
    else:
        i += 1
print(f"Total episode price < LTH RP sepanjang sejarah data: {len(episodes)}")
for s, e, n in episodes:
    if n >= 5:  # skip noise 1-4 hari
        min_price_in_ep = df[(df["date"]>=s)&(df["date"]<=e)]["btc_price"].min()
        min_lth_in_ep = df[(df["date"]>=s)&(df["date"]<=e)]["lth_cost_basis"].min()
        depth_pct = (min_price_in_ep/min_lth_in_ep - 1)*100
        print(f"  {s.date()} - {e.date()}  ({n}d)  max depth vs LTH RP = {depth_pct:.1f}%")

print("\nNOTE PENTING: n=3 cycle historis (2013,2017,2021) dipakai untuk fitting rasio -- SAMPLE SIZE KECIL,")
print("hasil (b) dan proyeksi manapun dari model ini WAJIB dibaca sebagai low-confidence directional, bukan presisi.")

# --- Export event table ---
out_rows = []
for r in reproduced:
    claimed = presenter_ratios[r["cycle"]]
    out_rows.append({
        "cycle": r["cycle"],
        "bull_low_date": r["low_date"].date(), "bull_low_price": round(r["low_price"], 2),
        "peak_date": r["peak_date"].date(), "peak_price": round(r["peak_price"], 2),
        "bear_low_date": r["bear_date"].date(), "bear_low_price": round(r["bear_price"], 2),
        "bull_log_return": round(r["bull_log_return"], 3),
        "bear_log_drawdown": round(r["bear_log_dd"], 3),
        "ratio_reproduced": round(r["ratio"], 3),
        "ratio_claimed_by_presenter": claimed,
    })
out_rows.append({
    "cycle": "current (2022-11 low -> ATH, reproduced)",
    "bull_low_date": cur_low_date.date(), "bull_low_price": round(cur_low_price, 2),
    "peak_date": cur_peak_date.date(), "peak_price": round(cur_peak_price, 2),
    "bear_low_date": "TBD (bear belum selesai)", "bear_low_price": "",
    "bull_log_return": round(cur_bull_log_return, 3),
    "bear_log_drawdown": "", "ratio_reproduced": "", "ratio_claimed_by_presenter": "",
})
pd.DataFrame(out_rows).to_csv("events_bear_drawdown_model.csv", index=False)
print("\n[Saved events_bear_drawdown_model.csv]")
