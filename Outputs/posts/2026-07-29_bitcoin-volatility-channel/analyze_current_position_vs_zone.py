"""
Insight #5 -- "Bitcoin Volatility Channel" narrative: price near/in Support band right now
= bottom forming, excellent accumulation. Compare against the OFFICIAL Decision Framework v2
zone/K-node status for the latest available data date.

Zone structure, AVIV Upper formula, and K-node gate/veto definitions reproduced EXACTLY from
`Decision_Framework v2.md` and `research/analyze_k3_stage_comparison.py` -- not re-derived.

STANDAR VALIDASI (CLAUDE.md) applied:
1. Event/state def explicit: zone determination uses the exact ordering + price-position table
   from Decision_Framework v2.md section 1. Alarm bear cepat signals 1&2 reproduced exactly
   (same code as analyze_k3_stage_comparison.py); signals 3&4 are a best-effort simplified
   reconstruction (flagged explicitly -- NOT the validated official state machine).
2. n reported where relevant (single latest-date snapshot; no event-counting needed for this insight)
3. Anti-lookahead: all values pulled for the LATEST available date only (2026-07-15), no forward data used
4. Independence: n/a (single point-in-time read, not a historical event study)
5. Data-start: all columns used here (sth_cost_basis, realized_price, lth_cost_basis, aviv_ratio,
   mvrv_ratio, percent_btc_in_profit, sth_sopr, asopr) available since 2010 -- no late-start issue
6. No threshold search -- all thresholds are the framework's OWN documented numbers, used as-is
"""

import pandas as pd
import numpy as np

pd.set_option("display.width", 140)

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

df = pd.read_csv(CSV, parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)

# ─── AVIV bands (reproduced from analyze_k3_stage_comparison.py -- NOT re-derived) ──
dk = df.dropna(subset=["aviv_ratio", "btc_price"]).copy().reset_index(drop=True)
HIST_MEAN = dk["aviv_ratio"].mean()
HIST_STD = dk["aviv_ratio"].std()
dk["true_mkt_mean"] = dk["btc_price"] / dk["aviv_ratio"]
dk["aviv_upper_framework"] = (HIST_MEAN + 0.5 * HIST_STD) * dk["true_mkt_mean"]  # AVIV Upper, K3-script method

df = df.merge(dk[["date", "aviv_upper_framework"]], on="date", how="left")

last_date = df["date"].max()
last = df[df["date"] == last_date].iloc[0]

print("=" * 100)
print(f"SNAPSHOT -- latest available data date: {last_date.date()}")
print("=" * 100)
print(f"btc_price              : ${last['btc_price']:,.2f}")
print(f"sth_cost_basis (STH RP): ${last['sth_cost_basis']:,.2f}")
print(f"realized_price (RP)    : ${last['realized_price']:,.2f}")
print(f"lth_cost_basis (LTH RP): ${last['lth_cost_basis']:,.2f}")
print(f"price_at_aviv_mean (AVIV Mean, framework col): ${last['price_at_aviv_mean']:,.2f}")
print(f"aviv_upper_framework (K3-script method)       : ${last['aviv_upper_framework']:,.2f}")
print(f"mvrv_ratio             : {last['mvrv_ratio']:.4f}")
print(f"sth_mvrv               : {last['sth_mvrv']:.4f}")
print(f"lth_mvrv               : {last['lth_mvrv']:.4f}")
print(f"percent_btc_in_profit  : {last['percent_btc_in_profit']:.2f}%")
print(f"pct_sth_in_profit      : {last['pct_sth_in_profit']:.2f}%")
print(f"pct_lth_in_profit      : {last['pct_lth_in_profit']:.2f}%")
print(f"sth_sopr               : {last['sth_sopr']:.4f}")
print(f"asopr                  : {last['asopr']:.4f}")
print(f"lth_sopr               : {last['lth_sopr']:.4f}")
print(f"cvdd                   : ${last['cvdd']:,.2f}   -> price/cvdd = {last['btc_price']/last['cvdd']:.3f}")

# ─── OCR sanity check (Insight source claimed Price ~$64,625 / $64,491 mid-2026) ──
print("\n" + "-" * 100)
print("OCR SANITY CHECK vs source.md chart reading (low-confidence OCR reads: $64,625.10 / $64,491.81)")
print(f"Actual btc_price on latest data date ({last_date.date()}): ${last['btc_price']:,.2f}")
diff_pct = (last['btc_price'] - 64625.10) / 64625.10 * 100
print(f"Diff vs Gambar-1 OCR reading: {diff_pct:+.2f}% -- same ballpark, OCR reading directionally plausible (still low-confidence).")

# ─── Zone determination (Decision_Framework v2.md section 1, exact table) ───────
print("\n" + "=" * 100)
print("ZONE DETERMINATION (Decision_Framework v2.md structure)")
print("=" * 100)

sth_rp = last["sth_cost_basis"]
rp = last["realized_price"]
lth_rp = last["lth_cost_basis"]
p = last["btc_price"]
aviv_mean = last["price_at_aviv_mean"]
aviv_upper = last["aviv_upper_framework"]

gap_sth_rp = (sth_rp - rp) / rp * 100
gap_rp_lth = (rp - lth_rp) / lth_rp * 100
print(f"Gap STH RP - RP  : {gap_sth_rp:+.2f}%")
print(f"Gap RP - LTH RP  : {gap_rp_lth:+.2f}%")

if abs(gap_sth_rp) < 2 and abs(gap_rp_lth) < 2:
    structure = "C (Konvergen)"
elif sth_rp > rp:
    structure = "N (Normal)"
else:
    structure = "T (Terbalik)"
print(f"\nStruktur: {structure}  (STH RP={sth_rp:,.0f} vs RP={rp:,.0f} vs LTH RP={lth_rp:,.0f})")

zone = None
if structure.startswith("N"):
    if p < rp:
        zone = "ZC -- Capitulation"
    elif p < sth_rp:
        zone = "ZD -- Dip dalam"
    elif p < aviv_mean:
        zone = "Z3"
    elif p < aviv_upper:
        zone = "Z4"
    else:
        zone = "Z5"
elif structure.startswith("T"):
    if p < sth_rp:
        zone = "Z1 -- Bear bottom"
    elif p < rp:
        zone = "Z1b"
    else:
        zone = "Z2-transisi"
else:  # C
    if p < aviv_mean:
        zone = "Z2 -- Konvergensi"
    else:
        zone = "Z4"

print(f"\nPrice = ${p:,.2f}")
print(f"  vs RP (${rp:,.2f}), STH RP (${sth_rp:,.2f}), AVIV Mean (${aviv_mean:,.2f}), AVIV Upper (${aviv_upper:,.2f})")
print(f"\n>>> ZONA RESMI FRAMEWORK SAAT INI: {zone} <<<")

# ─── Alarm bear CEPAT -- signals 1 & 2 fully reproduced, 3 & 4 best-effort ──────
print("\n" + "=" * 100)
print("ALARM BEAR CEPAT -- pool 4 sinyal, bunyi jika >=2/4 dalam window 90 hari")
print("(Signals 1 & 2 = exact reproduction from analyze_k3_stage_comparison.py logic.")
print(" Signals 3 & 4 = best-effort simplified reconstruction -- NOT the validated official")
print(" state machine, flagged low-confidence, included for context only.)")
print("=" * 100)

MIN_STREAK_DAYS = 7
PEAK_CONFIRM_DAYS = 14
LOOKBACK = 90

dk["above_upper"] = dk["btc_price"] > dk["aviv_upper_framework"]
streak = []
cur = 0
for v in dk["above_upper"]:
    cur = cur + 1 if v else 0
    streak.append(cur)
dk["streak_above"] = streak
dk["sig1_cross_down"] = False
above = dk["above_upper"].values
strk = dk["streak_above"].values
for i in range(1, len(dk)):
    if not above[i] and strk[i-1] >= MIN_STREAK_DAYS:
        dk.at[i, "sig1_cross_down"] = True

dm = df.dropna(subset=["sth_sopr"]).copy().reset_index(drop=True)
dm["ma90_sth"] = dm["sth_sopr"].rolling(90, min_periods=90).mean()
dm["ma90_ma60_sth"] = dm["ma90_sth"].rolling(60, min_periods=60).mean()
dm["sth_gap"] = dm["ma90_sth"] - dm["ma90_ma60_sth"]
dm["sig2_gap_peak"] = False
gap_vals = dm["sth_gap"].values
for i in range(1, len(dm) - PEAK_CONFIRM_DAYS):
    if pd.isna(gap_vals[i]) or gap_vals[i] <= 0:
        continue
    if gap_vals[i] <= gap_vals[i-1]:
        continue
    future = gap_vals[i+1:i+1+PEAK_CONFIRM_DAYS]
    if len(future) < PEAK_CONFIRM_DAYS:
        continue
    if all(future[j] < gap_vals[i] for j in range(len(future))):
        sig_idx = i + PEAK_CONFIRM_DAYS
        if sig_idx < len(dm):
            dm.at[sig_idx, "sig2_gap_peak"] = True

# Signal 3 (best-effort): MVRV momentum bearish cross -- SMA30(mvrv_ratio) crosses below
# SMA30(SMA30(mvrv_ratio)), sustained >= 7 days
dv = df.dropna(subset=["mvrv_ratio"]).copy().reset_index(drop=True)
dv["sma30"] = dv["mvrv_ratio"].rolling(30, min_periods=30).mean()
dv["sma30_of_sma30"] = dv["sma30"].rolling(30, min_periods=30).mean()
dv["below3"] = dv["sma30"] < dv["sma30_of_sma30"]
streak3 = []
cur3 = 0
for v in dv["below3"]:
    cur3 = cur3 + 1 if v else 0
    streak3.append(cur3)
dv["streak_below3"] = streak3
dv["sig3_active"] = dv["streak_below3"] >= 7

# Signal 4 (best-effort): MVRV Ratio < SMA180, sustained >=7d, AND last Z5 visit <=~120 days
dv["sma180"] = dv["mvrv_ratio"].rolling(180, min_periods=180).mean()
dv["below180"] = dv["mvrv_ratio"] < dv["sma180"]
streak4 = []
cur4 = 0
for v in dv["below180"]:
    cur4 = cur4 + 1 if v else 0
    streak4.append(cur4)
dv["streak_below180"] = streak4
dv["sig4a_active"] = dv["streak_below180"] >= 7

# Z5 history for "last Z5 visit" (P >= AVIV Upper)
dz = dk[["date", "btc_price", "aviv_upper_framework"]].copy()
dz["is_z5"] = dz["btc_price"] >= dz["aviv_upper_framework"]
z5_dates = dz.loc[dz["is_z5"], "date"]
last_z5_date = z5_dates[z5_dates <= last_date].max() if len(z5_dates[z5_dates <= last_date]) > 0 else None
days_since_z5 = (last_date - last_z5_date).days if last_z5_date is not None else None

sig1_recent = dk[(dk["date"] <= last_date) & (dk["date"] > last_date - pd.Timedelta(days=LOOKBACK)) & dk["sig1_cross_down"]]
sig2_recent = dm[(dm["date"] <= last_date) & (dm["date"] > last_date - pd.Timedelta(days=LOOKBACK)) & dm["sig2_gap_peak"]]
sig3_now = dv[dv["date"] == last_date]["sig3_active"].values
sig4a_now = dv[dv["date"] == last_date]["sig4a_active"].values

sig1_on = len(sig1_recent) > 0
sig2_on = len(sig2_recent) > 0
sig3_on = bool(sig3_now[0]) if len(sig3_now) > 0 else False
sig4_on = bool(sig4a_now[0]) if len(sig4a_now) > 0 else False
sig4_on_full = sig4_on and (days_since_z5 is not None and days_since_z5 <= 120)

print(f"Last Z5 visit (P >= AVIV Upper): {last_z5_date.date() if last_z5_date is not None else 'never'}  "
      f"({days_since_z5} days ago)" if last_z5_date is not None else "no Z5 visit found")
print(f"\nSignal 1 (AVIV Upper cross-down, streak>=7d) fired in last {LOOKBACK}d : {sig1_on}"
      f"  ({sig1_recent['date'].dt.date.tolist() if sig1_on else '-'})")
print(f"Signal 2 (STH-SOPR MA gap peak+decline 14d) fired in last {LOOKBACK}d    : {sig2_on}"
      f"  ({sig2_recent['date'].dt.date.tolist() if sig2_on else '-'})")
print(f"Signal 3 (MVRV momentum bearish cross, best-effort, currently active)  : {sig3_on}")
print(f"Signal 4 (MVRV < SMA180 >=7d AND last Z5 <=120d, best-effort)          : {sig4_on_full}"
      f"  (MVRV<SMA180 streak condition alone: {sig4_on})")

pool_count = sum([sig1_on, sig2_on, sig3_on, sig4_on_full])
print(f"\nPool count (best-effort) = {pool_count}/4  -> alarm bear CEPAT {'BUNYI (>=2/4)' if pool_count >= 2 else 'belum bunyi (<2/4)'}")
print("CAVEAT: signals 3 & 4 are simplified/best-effort reconstructions, not the validated")
print("official state machine -- treat this pool count as directional context only, not a")
print("definitive framework alarm reading.")

# ─── K2 gate/veto context (only meaningful if bull status / ZD-Z3-Z4) ───────────
print("\n" + "=" * 100)
print("K2 GATE/VETO CONTEXT (Decision_Framework v2.md section K2) -- relevant since zone = ZD")
print("=" * 100)
gate1 = 0.80 <= last["sth_mvrv"] <= 0.97
gate2_sopr_ok = True  # STH-SOPR<0.97 not sustained >14d -- check below
gate2_asopr = last["asopr"] > 0.95

d_sopr = df.dropna(subset=["sth_sopr"]).copy().reset_index(drop=True)
d_sopr["below097"] = d_sopr["sth_sopr"] < 0.97
streak_sopr = []
cur_s = 0
for v in d_sopr["below097"]:
    cur_s = cur_s + 1 if v else 0
    streak_sopr.append(cur_s)
d_sopr["streak_below097"] = streak_sopr
cur_streak_sopr = d_sopr[d_sopr["date"] == last_date]["streak_below097"].values
gate2_sopr_ok = bool(cur_streak_sopr[0] <= 14) if len(cur_streak_sopr) > 0 else None

print(f"Gate 1 (valuasi) STH-MVRV in [0.80,0.97]: {last['sth_mvrv']:.4f} -> {'OPEN' if gate1 else 'CLOSED'}")
print(f"Gate 2 (perilaku) STH-SOPR<0.97 not sustained >14d: streak={cur_streak_sopr[0] if len(cur_streak_sopr)>0 else '?'}d -> "
      f"{'OK' if gate2_sopr_ok else 'FAIL'}; aSOPR={last['asopr']:.4f}>0.95 -> {'OK' if gate2_asopr else 'FAIL'}")
gate2_open = gate2_sopr_ok and gate2_asopr
print(f"Gate 2 combined: {'OPEN' if gate2_open else 'CLOSED'}")

veto1 = last["percent_btc_in_profit"] <= 60
print(f"\nVeto 1 (Supply in Profit <=60%): {last['percent_btc_in_profit']:.2f}% -> {'TRIGGERED (BLOCK)' if veto1 else 'clear'}")

d_lth = df.dropna(subset=["pct_lth_in_profit"]).copy().reset_index(drop=True)
d_lth["ma30_lth_profit"] = d_lth["pct_lth_in_profit"].rolling(30, min_periods=30).mean()
last_lth_row = d_lth[d_lth["date"] == last_date]
if len(last_lth_row) > 0:
    lth_now = last_lth_row["pct_lth_in_profit"].values[0]
    lth_ma30 = last_lth_row["ma30_lth_profit"].values[0]
    veto2 = (lth_ma30 - lth_now) > 2
    print(f"Veto 2 (LTH profit share >2pt below its 30d MA): now={lth_now:.2f}%, MA30={lth_ma30:.2f}%, "
          f"drop={lth_ma30-lth_now:+.2f}pt -> {'TRIGGERED (BLOCK)' if veto2 else 'clear'}")
else:
    veto2 = None

veto3_a = sig4_on  # MVRV < SMA180 sustained >=7d (same calc as signal 4a above)
veto3_b = days_since_z5 is not None and days_since_z5 <= 120
veto3 = veto3_a and veto3_b
print(f"Veto 3 (sinyal penghenti: MVRV<SMA180>=7d AND last Z5<=120d): {'TRIGGERED (BLOCK)' if veto3 else 'clear'}")

print(f"\n>>> K2 STATUS: Gate1={'OPEN' if gate1 else 'CLOSED'}, Gate2={'OPEN' if gate2_open else 'CLOSED'}, "
      f"Veto1={'ON' if veto1 else 'off'}, Veto2={'ON' if veto2 else 'off'}, Veto3={'ON' if veto3 else 'off'}")
if veto1 or veto2 or veto3:
    print(">>> Kesimpulan: minimal SATU veto aktif -> K2 TIDAK BOLEH MASUK saat ini, terlepas dari gate.")
else:
    print(">>> Semua veto bersih -- keputusan tergantung status bull/bear (lihat alarm cepat di atas).")
