"""
Validasi 2: Velocity RSI <15% "generational bottom" -- cross-check on-chain state.

Klaim video (On-Chain Mind, 2026-08-11): Weekly velocity RSI (indikator
proprietary channel, TIDAK ada di data kita -- NEEDS-DATA-WE-DONT-HAVE untuk
replikasi langsung) ~14%, diklaim historically menandai "generational bottom"
tiap kali <15%.

Yang BISA kita lakukan: cross-check independen -- apakah tanggal video
(2026-08-11, atau proxy tanggal data terakhir tersedia) menunjukkan kondisi
capitulation/bottom menurut sinyal ON-CHAIN framework kita sendiri (K4, 4
kondisi bear bottom, per Decision Framework v2 Section "K4").

CATATAN DATA: data terakhir tersedia 2026-07-15 (gap ~27 hari ke tanggal
video). Semua angka "current" di bawah pakai tanggal itu sbg proxy, dicatat
eksplisit.

K4 4 kondisi (Decision Framework v2):
  1. LTH-MVRV < 1.0
  2. aSOPR < 0.93 selama >= 7 hari berturut DAN LTH-SOPR < 0.50
  3. Supply in Profit < 50% DAN STH profit < 10%
  4. Price/CVDD < 1.10  (flag ekstrem: <=1.0)

Zone classification: identik dengan analyze_200wma_cyclical_floor.py
(replikasi Decision Framework v2 Section 1).
"""

import pandas as pd
import numpy as np

df = pd.read_csv(
    r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv",
    parse_dates=["date"],
)
df = df.sort_values("date").reset_index(drop=True)

LATEST_DATE = df["date"].max()
VIDEO_DATE = pd.Timestamp("2026-08-11")
print(f"Data terakhir tersedia: {LATEST_DATE.date()}  |  Tanggal video: {VIDEO_DATE.date()}  |  gap = {(VIDEO_DATE-LATEST_DATE).days} hari")
print("=> Semua angka 'current' di bawah pakai proxy tanggal data terakhir, BUKAN tanggal video persis.\n")

df["aviv_upper"] = df["price_at_aviv_mean"] + 0.5 * (
    df["price_at_aviv_plus_1_sigma"] - df["price_at_aviv_mean"]
)

def classify_zone(row):
    p   = row["btc_price"]
    sth = row["sth_cost_basis"]
    rp  = row["realized_price"]
    lth = row["lth_cost_basis"]
    avm = row["price_at_aviv_mean"]
    avu = row["aviv_upper"]
    if any(pd.isna(x) for x in [p, sth, rp, lth, avm, avu]):
        return "NA"
    dist_sth_rp = abs(sth - rp) / rp if rp != 0 else np.nan
    dist_rp_lth = abs(rp - lth) / lth if lth != 0 else np.nan
    if sth > rp:
        struct = "N"
    elif dist_sth_rp < 0.02 and dist_rp_lth < 0.02:
        struct = "C"
    else:
        struct = "T"
    if p >= avu:
        return "Z5"
    if struct == "N":
        if p < rp:
            return "ZC"
        elif p < sth:
            return "ZD"
        elif p < avm:
            return "Z3"
        else:
            return "Z4"
    elif struct == "T":
        if p < sth:
            return "Z1"
        elif p < rp:
            return "Z1b"
        else:
            return "Z2-transisi"
    else:
        if p < avm:
            return "Z2"
        else:
            return "Z4"

df["zone"] = df.apply(classify_zone, axis=1)
df["price_cvdd"] = df["btc_price"] / df["cvdd"]

# aSOPR < 0.93 streak
df["asopr_below_093"] = df["asopr"] < 0.93
streak = []
cur = 0
for v in df["asopr_below_093"]:
    cur = cur + 1 if v else 0
    streak.append(cur)
df["asopr_below_093_streak"] = streak

last = df.iloc[-1]

print("="*100)
print(f"(a) Nilai metrik on-chain @ {last['date'].date()} (proxy)")
print("="*100)
print(f"btc_price            = ${last['btc_price']:,.0f}")
print(f"mvrv_ratio            = {last['mvrv_ratio']:.3f}")
print(f"lth_mvrv              = {last['lth_mvrv']:.3f}")
print(f"asopr                 = {last['asopr']:.4f}   (streak <0.93 berturut = {int(last['asopr_below_093_streak'])} hari)")
print(f"lth_sopr              = {last['lth_sopr']:.4f}")
print(f"percent_btc_in_profit = {last['percent_btc_in_profit']:.1f}%")
print(f"pct_sth_in_profit     = {last['pct_sth_in_profit']:.1f}%")
print(f"cvdd                  = ${last['cvdd']:,.0f}")
print(f"price/cvdd            = {last['price_cvdd']:.3f}")
print(f"zone                  = {last['zone']}")

# also show last 10 days for context (data may lag / noisy last row)
print("\nKonteks 15 hari terakhir data tersedia:")
cols = ["date","btc_price","mvrv_ratio","lth_mvrv","asopr","lth_sopr",
        "percent_btc_in_profit","pct_sth_in_profit","price_cvdd","zone"]
print(df[cols].tail(15).to_string(index=False))

print("\n" + "="*100)
print("(b) K4 -- 4 kondisi bear bottom, evaluasi @ tanggal data terakhir")
print("="*100)
c1 = last["lth_mvrv"] < 1.0
c2 = (last["asopr_below_093_streak"] >= 7) and (last["lth_sopr"] < 0.50)
c3 = (last["percent_btc_in_profit"] < 50) and (last["pct_sth_in_profit"] < 10)
c4 = last["price_cvdd"] < 1.10
c4_extreme = last["price_cvdd"] <= 1.0

count_on = sum([c1, c2, c3, c4])
print(f"[1] LTH-MVRV < 1.0                                   : {last['lth_mvrv']:.3f} < 1.0        -> {'ON' if c1 else 'off'}")
print(f"[2] aSOPR<0.93 >=7d ({int(last['asopr_below_093_streak'])}d) DAN LTH-SOPR<0.50 ({last['lth_sopr']:.3f}) -> {'ON' if c2 else 'off'}")
print(f"[3] Supply Profit<50% ({last['percent_btc_in_profit']:.1f}%) DAN STH profit<10% ({last['pct_sth_in_profit']:.1f}%) -> {'ON' if c3 else 'off'}")
print(f"[4] Price/CVDD < 1.10 ({last['price_cvdd']:.3f})   (ekstrem <=1.0: {'YA' if c4_extreme else 'tidak'}) -> {'ON' if c4 else 'off'}")
print(f"\n>>> Count K4 conditions ON = {count_on}/4")

print("\n" + "="*100)
print(f"(c) Zone @ {last['date'].date()}: {last['zone']}")
print("="*100)

# ─── Historical context: past K4 count>=2 episodes for comparison scale ──
df["k4_c1"] = df["lth_mvrv"] < 1.0
df["k4_c2"] = (df["asopr_below_093_streak"] >= 7) & (df["lth_sopr"] < 0.50)
df["k4_c3"] = (df["percent_btc_in_profit"] < 50) & (df["pct_sth_in_profit"] < 10)
df["k4_c4"] = df["price_cvdd"] < 1.10
df["k4_count"] = df[["k4_c1","k4_c2","k4_c3","k4_c4"]].sum(axis=1)

print("\n" + "="*100)
print("Konteks historis: distribusi K4 count harian sepanjang data (n hari per count)")
print("="*100)
print(df["k4_count"].value_counts().sort_index())

# last time count>=2
hi_count_days = df[df["k4_count"] >= 2]
print(f"\nTotal hari sepanjang sejarah dgn K4 count>=2: {len(hi_count_days)}")
if not hi_count_days.empty:
    print(f"Episode count>=2 terakhir sebelum data terakhir: {hi_count_days['date'].max().date()}")
    print(f"Jarak dari data terakhir: {(last['date'] - hi_count_days['date'].max()).days} hari")

print("\nSelesai. Cross-check independen -- catatan: velocity RSI channel TIDAK bisa direplikasi (indikator proprietary, komponen tidak dipublikasikan).")
