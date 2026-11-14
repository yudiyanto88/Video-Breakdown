"""
Insight #4 -- "Bitcoin Volatility Channel" cross Price vs Fair Value as regime-change marker.

Vendor's own "Fair Value" formula is undisclosed (see Insight #3 script/findings for the
band-shape reconstruction attempt). For THIS insight we sidestep guessing the vendor's exact
centerline and instead use two established proxies already in our dataset, per task instruction:
  - PRIMARY:   true_market_mean_price  (Cointime "true market mean" -- an economic/valuation-based
               central price, conceptually closer to a "fair value" anchor than a pure technical MA)
  - SECONDARY: 200_wma  (200-week moving average -- widely used long-term trend/"fair value" line,
               used here purely as a sensitivity/robustness check on the SAME cross-event logic)

STANDAR VALIDASI (CLAUDE.md) applied:
1. Event def explicit below (raw sign-change cross, then whipsaw vs regime-change classification
   by how long the new side of the proxy is held before the NEXT cross)
2. n + per-cycle spread always reported
3. Anti-lookahead: whipsaw/regime classification looks FORWARD from the cross date to the NEXT
   cross -- that's the definition of the outcome being measured, not a decision input. The
   comparison against K-node triggers uses only same-day-or-later established trigger logic
   (reproduced from research/analyze_k3_stage_comparison.py, no re-derivation).
4. Independence: crosses grouped by macro-cycle, cycle-domination flagged
5. Full history: all columns used here (btc_price, true_market_mean_price, 200_wma, aviv_ratio,
   sth_sopr, sth_cost_basis, realized_price) are available since 2010-07-17/18 -- no late-start
   truncation issue for this particular insight.
6. No overfitting: whipsaw/regime-change cutoffs (<=30d / >90d) are the values the task specified
   a priori, not grid-searched. Both proxies (true_market_mean_price, 200_wma) reported side by
   side, not cherry-picked to the one that looks better.
"""

import pandas as pd
import numpy as np

pd.set_option("display.width", 140)

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUT_EVENTS = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\posts\2026-07-29_bitcoin-volatility-channel\events_volatility_channel_fair_value_cross.csv"

WHIPSAW_DAYS = 30      # cross reverses within this many days -> whipsaw (task-specified)
REGIME_DAYS = 90       # new side held at least this long before next cross -> genuine regime change (task-specified)
K_MATCH_WINDOW = 30    # +/- days to call a Fair-Value cross "redundant" with an established K-node trigger

# ─── Load ────────────────────────────────────────────────────────────────────
df = pd.read_csv(CSV, parse_dates=["date"])
cols = ["date", "btc_price", "true_market_mean_price", "200_wma",
        "aviv_ratio", "sth_sopr", "sth_cost_basis", "realized_price"]
df = df[cols].dropna(subset=["date", "btc_price"]).sort_values("date").reset_index(drop=True)


def cycle_label(d):
    if d < pd.Timestamp("2016-01-01"):
        return "2013-15"
    elif d < pd.Timestamp("2020-01-01"):
        return "2018-19"
    elif d < pd.Timestamp("2021-06-01"):
        return "2020 (covid)"
    elif d < pd.Timestamp("2023-06-01"):
        return "2022"
    else:
        return "2025-26"


# =============================================================================
# STEP 1: Raw crosses of price vs proxy (Fair Value candidate)
# =============================================================================
def find_crosses(d, proxy_col):
    d = d.dropna(subset=[proxy_col]).reset_index(drop=True)
    above = (d["btc_price"] > d[proxy_col]).values
    dates = d["date"].values
    prices = d["btc_price"].values
    proxy_vals = d[proxy_col].values

    crosses = []  # (index, date, direction) direction: "down" = above->below, "up" = below->above
    for i in range(1, len(d)):
        if above[i-1] and not above[i]:
            crosses.append((i, dates[i], "down"))
        elif not above[i-1] and above[i]:
            crosses.append((i, dates[i], "up"))

    rows = []
    for j, (i, dt, direction) in enumerate(crosses):
        dt = pd.Timestamp(dt)
        # next cross of ANY direction marks how long this regime lasted
        if j + 1 < len(crosses):
            next_dt = pd.Timestamp(crosses[j+1][1])
            hold_days = (next_dt - dt).days
            censored = False
        else:
            next_dt = pd.Timestamp(dates[-1])
            hold_days = (next_dt - dt).days
            censored = True  # this is the last cross in history -- regime hasn't necessarily ended

        if hold_days <= WHIPSAW_DAYS:
            classification = "whipsaw"
        elif hold_days > REGIME_DAYS:
            classification = "regime_change"
        else:
            classification = "ambiguous"
        if censored and classification != "whipsaw":
            classification += "_censored_ongoing"

        rows.append({
            "proxy": proxy_col,
            "cross_date": dt.date(),
            "direction": direction,
            "price": round(prices[i], 2),
            "proxy_level": round(proxy_vals[i], 2),
            "cycle": cycle_label(dt),
            "hold_days_to_next_cross": hold_days,
            "classification": classification,
        })
    return pd.DataFrame(rows)


print("=" * 100)
print("STEP 1 -- Raw Price vs Fair-Value-proxy crosses, full history")
print("=" * 100)

proxy_results = {}
for proxy_col in ["true_market_mean_price", "200_wma"]:
    ev = find_crosses(df, proxy_col)
    proxy_results[proxy_col] = ev
    n = len(ev)
    n_down = (ev["direction"] == "down").sum()
    n_up = (ev["direction"] == "up").sum()
    print(f"\n--- Proxy: {proxy_col} ---")
    print(f"n total crosses = {n}  (cross-down={n_down}, cross-up={n_up})")
    print("Per-cycle count:")
    print(ev["cycle"].value_counts().sort_index().to_string())
    print("\nClassification breakdown:")
    print(ev["classification"].value_counts().to_string())
    n_whip = ev["classification"].eq("whipsaw").sum()
    n_regime = ev["classification"].str.startswith("regime_change").sum()
    n_ambig = ev["classification"].eq("ambiguous").sum()
    print(f"\n% whipsaw (reversed <= {WHIPSAW_DAYS}d)      : {n_whip/n*100:.1f}% (n={n_whip}/{n})")
    print(f"% regime change (held > {REGIME_DAYS}d)     : {n_regime/n*100:.1f}% (n={n_regime}/{n})")
    print(f"% ambiguous ({WHIPSAW_DAYS+1}-{REGIME_DAYS}d)          : {n_ambig/n*100:.1f}% (n={n_ambig}/{n})")

# =============================================================================
# STEP 2: Established K-node triggers (reproduced from analyze_k3_stage_comparison.py
#          and data_dictionary.md -- NOT re-derived, same formula)
# =============================================================================
print("\n" + "=" * 100)
print("STEP 2 -- Established K-node triggers (reproduced from research/analyze_k3_stage_comparison.py)")
print("=" * 100)

dk = df.dropna(subset=["aviv_ratio", "btc_price"]).reset_index(drop=True)
HIST_MEAN = dk["aviv_ratio"].mean()
HIST_STD = dk["aviv_ratio"].std()
dk["true_mkt_mean"] = dk["btc_price"] / dk["aviv_ratio"]
dk["aviv_05sig"] = (HIST_MEAN + 0.5 * HIST_STD) * dk["true_mkt_mean"]  # AVIV Upper (framework def, +0.5sd)

MIN_STREAK_DAYS = 7  # K1/K3 trigger definition: sustained streak above AVIV Upper before cross-down counts
dk["above_05sig"] = dk["btc_price"] > dk["aviv_05sig"]
streak = []
cur = 0
for v in dk["above_05sig"]:
    cur = cur + 1 if v else 0
    streak.append(cur)
dk["streak_above"] = streak
dk["aviv_cross_down"] = False
above = dk["above_05sig"].values
strk = dk["streak_above"].values
for i in range(1, len(dk)):
    if not above[i] and strk[i-1] >= MIN_STREAK_DAYS:
        dk.at[i, "aviv_cross_down"] = True

k1_triggers = dk[dk["aviv_cross_down"]][["date"]].copy()
k1_triggers["trigger"] = "K1/K3 signal 1: AVIV Upper (+0.5sig) cross-down (Z5->Z4), streak>=7d"

# STH RP cross up RP -- Z1 -> Z2 transition ("status bear berakhir / unlock")
dz = df.dropna(subset=["sth_cost_basis", "realized_price"]).reset_index(drop=True)
above_z2 = (dz["sth_cost_basis"] > dz["realized_price"]).values
z2_dates = dz["date"].values
z2_triggers = []
for i in range(1, len(dz)):
    if not above_z2[i-1] and above_z2[i]:
        z2_triggers.append(pd.Timestamp(z2_dates[i]))
z2_triggers_df = pd.DataFrame({"date": z2_triggers})
z2_triggers_df["trigger"] = "STH RP cross up RP (Z1->Z2 transition / bear-status unlock)"

all_triggers = pd.concat([k1_triggers, z2_triggers_df], ignore_index=True).sort_values("date").reset_index(drop=True)
print(f"\nK1/K3 AVIV Upper cross-down triggers: n={len(k1_triggers)}")
print(f"STH RP cross-up RP (Z1->Z2) triggers : n={len(z2_triggers_df)}")

# =============================================================================
# STEP 3: For each REGIME-CHANGE-classified Fair-Value cross, is there an established
#          K-node trigger within +/- K_MATCH_WINDOW days? (redundant vs new information)
# =============================================================================
print("\n" + "=" * 100)
print(f"STEP 3 -- Regime-change Fair-Value crosses vs established K-node triggers (+/-{K_MATCH_WINDOW}d match window)")
print("=" * 100)

all_out_rows = []
for proxy_col, ev in proxy_results.items():
    regime_ev = ev[ev["classification"].str.startswith("regime_change")].copy()
    print(f"\n--- Proxy: {proxy_col}  (n regime-change crosses = {len(regime_ev)}) ---")
    matched = 0
    for _, row in regime_ev.iterrows():
        ev_date = pd.Timestamp(row["cross_date"])
        diffs = (all_triggers["date"] - ev_date).dt.days
        if len(diffs) > 0:
            idx_min = diffs.abs().idxmin()
            lead = diffs.loc[idx_min]  # negative = trigger before cross, positive = trigger after
            nearest_trigger = all_triggers.loc[idx_min, "trigger"]
            nearest_date = all_triggers.loc[idx_min, "date"]
        else:
            lead, nearest_trigger, nearest_date = None, None, None

        is_redundant = lead is not None and abs(lead) <= K_MATCH_WINDOW
        if is_redundant:
            matched += 1
        print(f"  {row['cross_date']} ({row['direction']:4s}, cycle {row['cycle']:>12s}, held {row['hold_days_to_next_cross']:>5d}d) "
              f"-> nearest K-trigger: {str(nearest_date)[:10] if nearest_date is not None else '-'} "
              f"(lead={lead}d, {'REDUNDANT' if is_redundant else 'no close match'}) [{nearest_trigger if is_redundant else ''}]")

        all_out_rows.append({
            "proxy": proxy_col,
            "cross_date": row["cross_date"],
            "direction": row["direction"],
            "cycle": row["cycle"],
            "hold_days_to_next_cross": row["hold_days_to_next_cross"],
            "nearest_k_trigger_date": nearest_date,
            "lead_days_vs_k_trigger": lead,
            "redundant_within_30d": is_redundant,
        })
    n_regime = len(regime_ev)
    if n_regime > 0:
        print(f"  => {matched}/{n_regime} ({matched/n_regime*100:.1f}%) regime-change FV crosses fall within +/-{K_MATCH_WINDOW}d of an established K-node trigger")

out_df = pd.DataFrame(all_out_rows)
out_df.to_csv(OUT_EVENTS, index=False)
print(f"\nSaved events CSV -> {OUT_EVENTS}")
