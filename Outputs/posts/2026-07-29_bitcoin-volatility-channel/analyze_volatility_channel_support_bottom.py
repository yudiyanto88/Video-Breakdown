"""
Insight #3 -- "Bitcoin Volatility Channel" (vendor: INVESTE MAIS) support-band touch = bottom signal.

Vendor formula is NOT published. We reconstruct a working proxy from btc_price only,
per vendor's own text description:
  - "central price average" (Fair Value / centerline)
  - band width driven by "annualized realized volatility, 365-day window"

Band model (log-space, symmetric multiplicative -- matches vendor snapshot ratios,
see calibration section below):
    sigma_t   = std(daily log-return, 365d window) * sqrt(365)      [ANNUALIZED REALIZED VOL]
    center_t  = exp( rolling_mean( log(price), window=W ) )         [FAIR VALUE proxy]
    support_t = center_t * exp(-k * sigma_t)
    resist_t  = center_t * exp(+k * sigma_t)

W and k are NOT known -- vendor formula undisclosed. We calibrate post-hoc against
ONE single snapshot read off the chart (mid-2026, low-confidence OCR):
    Fair Value ~ $66,690.52 | Support ~ $53,678.08 | Resistance ~ $82,860.50
This is curve-fitting to a single point, NOT an independently validated reproduction
of the vendor's actual formula. Treat every downstream number in this script as an
APPROXIMATE reconstruction, not ground truth.

STANDAR VALIDASI (CLAUDE.md) applied:
1. Event def explicit (below) incl. 30-day merge/cooldown + rationale
2. n + per-cycle spread always reported
3. Anti-lookahead: band computed with trailing-only rolling stats (band value AT the
   event date never uses future data). Forward reversal check is the OUTCOME we are
   measuring, not the trigger -- and right-censored (too-recent) events are flagged and
   excluded from the resolved-rate denominator instead of silently counted as failures.
4. Independence: events grouped by macro-cycle, cycle-domination flagged
5. Data-start: btc_price usable from 2010-07-17 in this file. Chart claims 2013-2026;
   pre-2014 BTC market depth/liquidity was thin -- flagged as a caveat on those events.
6. No overfitting to OUTCOME: k is calibrated to reproduce the band SHAPE (one snapshot),
   not searched to make the reversal-rate look good. Centerline window sensitivity
   (365d / 730d / empirically closest ~1095d) is reported side-by-side, not cherry-picked.
"""

import pandas as pd
import numpy as np

pd.set_option("display.width", 140)

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUT_EVENTS = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\posts\2026-07-29_bitcoin-volatility-channel\events_volatility_channel_support_bottom.csv"

# ─── Load ────────────────────────────────────────────────────────────────────
df = pd.read_csv(CSV, parse_dates=["date"])
df = df[["date", "btc_price"]].dropna()
df = df[df["btc_price"] > 0].sort_values("date").reset_index(drop=True)

df["log_price"] = np.log(df["btc_price"])
df["log_ret"] = df["log_price"].diff()
df["sigma365"] = df["log_ret"].rolling(365, min_periods=365).std() * np.sqrt(365)

# ─── Calibration: try centerline windows against the ONE chart snapshot ─────
TARGET_FV = 66690.52
TARGET_SUP = 53678.08
TARGET_RES = 82860.50

print("=" * 100)
print("CALIBRATION -- reconstructed band vs ONE chart snapshot (~2026-07-15, low-confidence OCR)")
print("=" * 100)

candidate_windows = [365, 730, 1095]  # 365d & 730d = task-specified; 1095d (~3y) added as empirical best-fit check
last = df.iloc[-1]
print(f"Last data date: {last['date'].date()}  btc_price=${last['btc_price']:,.0f}  sigma365={last['sigma365']:.4f}")
print(f"{'Window(d)':>10} {'k':>5} {'Center($)':>12} {'Support($)':>12} {'Resist($)':>12} {'Center err%':>12}")

for W in candidate_windows:
    center_log = df["log_price"].rolling(W, min_periods=W).mean().iloc[-1]
    center = np.exp(center_log)
    k = 0.5  # only print k=0.5 (best band-shape fit, see note below) to keep output readable
    sup = center * np.exp(-k * last["sigma365"])
    res = center * np.exp(k * last["sigma365"])
    center_err = (center - TARGET_FV) / TARGET_FV * 100
    print(f"{W:>10} {k:>5.1f} {center:>12,.0f} {sup:>12,.0f} {res:>12,.0f} {center_err:>11.1f}%")

print("")
print("Note: k=0.5 reproduces the SUPPORT/RESISTANCE-to-CENTER ratio almost exactly at the")
print("snapshot date (ln(82860/FV) = -ln(53678/FV) = 0.217 = k*sigma with k=0.5, sigma=0.434).")
print("But the CENTERLINE itself (365d & 730d rolling mean of log price) overshoots the vendor's")
print("stated Fair Value by ~28-30% -- neither of the two task-specified windows reproduces the")
print("snapshot centerline. A much longer window (~1095d/3y) fits far closer. This is a material")
print("reconstruction gap: the 'shape' (relative band width) replicates well, the 'level' (absolute")
print("Fair Value anchor) does not, using either specified window. All numbers below are therefore")
print("an approximate reconstruction, calibrated post-hoc to ONE point, not the vendor's real formula.")

# ─── Primary + sensitivity configs for the event study ──────────────────────
CONFIGS = {
    "W365_k0.5": (365, 0.5),     # task-specified
    "W730_k0.5": (730, 0.5),     # task-specified alternate
    "W1095_k0.5": (1095, 0.5),   # empirical best centerline fit (robustness check, not cherry-picked outcome)
}

COOLDOWN_DAYS = 30    # merge/cooldown: a support-touch "episode" commonly spans weeks of chop;
                      # 30d prevents counting daily re-touches within the same drawdown as separate
                      # events, while still catching genuinely separate dips (e.g. 2018 vs 2020) as distinct.
REVERSAL_WINDOW = 180  # days forward to check for reversal back above Fair Value (centerline)


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


def run_config(W, k, label):
    d = df.copy()
    d["center"] = np.exp(d["log_price"].rolling(W, min_periods=W).mean())
    d["support"] = d["center"] * np.exp(-k * d["sigma365"])
    d["resist"] = d["center"] * np.exp(k * d["sigma365"])
    d = d.dropna(subset=["center", "support", "sigma365"]).reset_index(drop=True)

    d["below_support"] = d["btc_price"] < d["support"]

    events = []
    last_event_date = None
    for i, row in d.iterrows():
        if row["below_support"]:
            if last_event_date is None or (row["date"] - last_event_date).days >= COOLDOWN_DAYS:
                events.append(i)
                last_event_date = row["date"]

    last_data_date = d["date"].max()
    rows = []
    for i in events:
        ev = d.loc[i]
        ev_date = ev["date"]
        ev_price = ev["btc_price"]
        window_end = ev_date + pd.Timedelta(days=REVERSAL_WINDOW)
        fwd = d[(d["date"] > ev_date) & (d["date"] <= window_end)]
        is_censored = window_end > last_data_date  # not enough forward data yet -- anti-lookahead guard

        reversal_date = None
        deeper_first = False
        min_price_before_reversal = ev_price
        for _, frow in fwd.iterrows():
            if frow["btc_price"] < min_price_before_reversal:
                min_price_before_reversal = frow["btc_price"]
            if frow["btc_price"] > frow["center"]:
                reversal_date = frow["date"]
                break
        if reversal_date is not None and min_price_before_reversal < ev_price:
            deeper_first = True

        if reversal_date is not None:
            days_to_rev = (reversal_date - ev_date).days
            outcome = "false_start_then_reversal" if deeper_first else "clean_reversal"
        elif is_censored:
            days_to_rev = None
            outcome = "censored_insufficient_data"  # event too recent, 180d window hasn't fully elapsed yet
        else:
            days_to_rev = None
            outcome = "no_reversal_in_window"

        rows.append({
            "config": label,
            "event_date": ev_date.date(),
            "price": round(ev_price, 2),
            "support_level": round(ev["support"], 2),
            "fair_value_level": round(ev["center"], 2),
            "cycle": cycle_label(ev_date),
            "reversal_date": reversal_date.date() if reversal_date is not None else None,
            "days_to_reversal": days_to_rev,
            "outcome": outcome,
        })
    return pd.DataFrame(rows)


all_events = []
print("")
print("=" * 100)
print(f"EVENT STUDY -- 'price closes below Support band' (cooldown={COOLDOWN_DAYS}d, reversal window={REVERSAL_WINDOW}d)")
print("=" * 100)

for label, (W, k) in CONFIGS.items():
    ev_df = run_config(W, k, label)
    all_events.append(ev_df)
    n = len(ev_df)
    print("")
    print(f"--- Config {label} ---")
    print(f"n total events = {n}")
    if n > 0:
        print("Per-cycle count:")
        print(ev_df["cycle"].value_counts().sort_index().to_string())
        print("")
        print("Outcome breakdown (raw, incl. censored):")
        print(ev_df["outcome"].value_counts().to_string())
        clean = (ev_df["outcome"] == "clean_reversal").sum()
        falsestart = (ev_df["outcome"] == "false_start_then_reversal").sum()
        noreversal = (ev_df["outcome"] == "no_reversal_in_window").sum()
        censored = (ev_df["outcome"] == "censored_insufficient_data").sum()
        n_resolved = n - censored
        print("")
        print(f"n resolved (full {REVERSAL_WINDOW}d forward window available) = {n_resolved}  |  n censored (too recent) = {censored}")
        if n_resolved > 0:
            print(f"% clean reversal within {REVERSAL_WINDOW}d       : {clean/n_resolved*100:.1f}% (n={clean}/{n_resolved})")
            print(f"% false-start-then-reversal (deeper first) : {falsestart/n_resolved*100:.1f}% (n={falsestart}/{n_resolved})")
            print(f"% no reversal within window           : {noreversal/n_resolved*100:.1f}% (n={noreversal}/{n_resolved})")
        else:
            print("All events censored -- cannot compute reversal rate for this config.")

events_all_df = pd.concat(all_events, ignore_index=True) if all_events else pd.DataFrame()
events_all_df.to_csv(OUT_EVENTS, index=False)
print("")
print(f"Saved events CSV -> {OUT_EVENTS}")

print("")
print("=" * 100)
print("VENDOR CHART CLAIM CHECK: vendor annotated only ~4 arrows (hand-picked) across full history.")
print("Reconstructed event count above (per config) shows the TRUE total frequency of the same")
print("pattern under a mechanical, consistent rule -- compare n against vendor's implicit '4'.")
print("=" * 100)
