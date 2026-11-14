"""
Validasi: cross-under MVRV Ratio vs SMA180 -- klasifikasi recency Z5.

Pertanyaan inti: apakah event 2019, 2024, 2026 "jinak" (versi chart sumber)
atau "lanjut -19% s/d -48%" (versi KB MVRV v1.4 6C.2)?

DEFINISI EVENT (STRICT, aturan 6C.1/6C.2 KB MVRV v1.4):
  - Regime = mvrv_ratio >= SMA180(mvrv_ratio) -> "above"; < -> "below"
  - Cross-under = hari pertama regime pindah above -> below, dengan:
      (a) below bertahan >= 7 hari berturut-turut (persistensi), DAN
      (b) run "above" tepat sebelumnya berdurasi >= 7 hari (regime positif >= 7 hari)
  - ATURAN MERGE ANTAR-EPISODE: tidak ada cooldown waktu tambahan.
    Merge terjadi secara struktural: kalau dua below-run dipisah above-run
    < 7 hari, cross kedua TIDAK memenuhi syarat (b) sehingga otomatis
    tergabung ke episode koreksi yang sama. Dua event terpisah hanya
    mungkin kalau di antaranya ada pemulihan above >= 7 hari penuh.

DEFINISI LONGGAR (untuk rekonsiliasi count 11 vs 16, Governance v2 4c):
  - L0: SEMUA hari cross above->below, tanpa syarat apapun (raw cross)
  - L1: cross dengan persistensi below >= 7 hari saja (tanpa syarat regime
        positif sebelumnya >= 7 hari)

PER EVENT (semua at-gate, anti-lookahead kecuali forward window yang memang
ground-truth):
  - tanggal cross, harga close saat cross
  - hari sejak terakhir btc_price >= AVIV Upper (hanya data <= tanggal event)
    AVIV Upper = price_at_aviv_mean + 0.5*(price_at_aviv_plus_1_sigma
                 - price_at_aviv_mean)   [pola analyze_k3_stage_comparison.py
                 versi kolom master; data_dictionary.md]
  - max forward drawdown 120 hari dari close tanggal event (ground-truth
    window; event yang windownya belum penuh diberi flag)

Catatan lookahead yang diterima framework: band AVIV (price_at_aviv_*) dari
provider dihitung dengan mean/SD full-history -- sama dengan pola script
established. SMA180 sendiri murni backward-looking.
"""

import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\posts\2026-07-19_mvrv-vs-sma180-deviation-cross-under"

PERSIST = 7   # hari minimal below untuk sah
PRIOR   = 7   # hari minimal regime above sebelum cross
FWD     = 120 # window ground-truth drawdown
DD_TH   = -0.15  # threshold drawdown >=15% (metrik KB)

df = pd.read_csv(MASTER, parse_dates=["date"])
df = df[["date", "btc_price", "mvrv_ratio",
         "price_at_aviv_mean", "price_at_aviv_plus_1_sigma"]].copy()
df = df.sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "mvrv_ratio"]).reset_index(drop=True)

print("Rentang data           : %s s/d %s (n=%d hari)" % (
    df["date"].iloc[0].date(), df["date"].iloc[-1].date(), len(df)))

# SMA180 murni backward-looking
df["sma180"] = df["mvrv_ratio"].rolling(180, min_periods=180).mean()

# AVIV Upper (formula established, kolom master)
df["aviv_upper"] = df["price_at_aviv_mean"] + 0.5 * (
    df["price_at_aviv_plus_1_sigma"] - df["price_at_aviv_mean"])
aviv_start = df.loc[df["aviv_upper"].notna(), "date"].min()
print("Kolom AVIV tersedia mulai: %s" % aviv_start.date())

# Regime & run-length
d = df.dropna(subset=["sma180"]).reset_index(drop=True)
print("SMA180 tersedia mulai  : %s" % d["date"].iloc[0].date())
above = (d["mvrv_ratio"] >= d["sma180"]).values

run_above = np.zeros(len(d), dtype=int)
run_below = np.zeros(len(d), dtype=int)
for i in range(len(d)):
    if above[i]:
        run_above[i] = run_above[i-1] + 1 if i > 0 else 1
    else:
        run_below[i] = run_below[i-1] + 1 if i > 0 else 1

dates  = d["date"].values
prices = d["btc_price"].values
aviv_u = d["aviv_upper"].values

# hitung streak below TOTAL untuk tiap below-run (lihat ke depan hanya untuk
# memutuskan validitas event -- ini bagian dari DEFINISI event (butuh konfirmasi
# 7 hari), bukan lookahead pada nilai keputusan; tanggal event tetap tanggal
# cross, dan pemakaian real-time berarti sinyal baru "sah" di hari ke-7)
def below_run_length_from(i):
    n = 0
    j = i
    while j < len(d) and not above[j]:
        n += 1
        j += 1
    return n

events_L0, events_L1, events_strict = [], [], []
for i in range(1, len(d)):
    if above[i] or not above[i-1]:
        continue  # bukan hari cross above->below
    prior_run = run_above[i-1]
    blen = below_run_length_from(i)
    events_L0.append(i)
    if blen >= PERSIST:
        events_L1.append(i)
        if prior_run >= PRIOR:
            events_strict.append(i)

print()
print("COUNT PER DEFINISI:")
print("  L0 raw cross (tanpa syarat)                 : n=%d" % len(events_L0))
print("  L1 persistensi below>=7d saja               : n=%d" % len(events_L1))
print("  STRICT (persistensi + regime above>=7d)     : n=%d" % len(events_strict))

# daftar L1 yang gugur di strict (buat rekonsiliasi)
gugur = [i for i in events_L1 if i not in events_strict]
if gugur:
    print("  L1 yang gugur karena regime above < 7 hari  :")
    for i in gugur:
        print("    %s (above-run sebelumnya = %d hari)" % (
            pd.Timestamp(dates[i]).date(), run_above[i-1]))

# fungsi cycle
def cycle_of(ts):
    ts = pd.Timestamp(ts)
    if ts < pd.Timestamp("2015-01-14"): return "C1 (2011-2015)"
    if ts < pd.Timestamp("2018-12-15"): return "C2 (2015-2018)"
    if ts < pd.Timestamp("2022-11-21"): return "C3 (2019-2022)"
    return "C4 (2023-...)"

rows = []
for i in events_strict:
    t = pd.Timestamp(dates[i])
    px = prices[i]
    # hari sejak terakhir price >= AVIV Upper, HANYA data s/d hari event
    mask = (~np.isnan(aviv_u[:i+1])) & (prices[:i+1] >= aviv_u[:i+1])
    idxs = np.where(mask)[0]
    if len(idxs) > 0:
        last_z5 = pd.Timestamp(dates[idxs[-1]])
        days_since_z5 = (t - last_z5).days
        z5_str = str(days_since_z5)
    else:
        last_z5 = None
        days_since_z5 = None
        z5_str = "belum pernah (dlm data AVIV)"
    # forward drawdown 120 hari dari close event
    fwd = prices[i+1: i+1+FWD]
    full = len(fwd) == FWD
    if len(fwd) > 0:
        maxdd = fwd.min() / px - 1.0
    else:
        maxdd = np.nan
    rows.append({
        "cross_date": t.date(),
        "cycle": cycle_of(t),
        "price_at_cross": round(px, 2),
        "prior_above_run_d": int(run_above[i-1]),
        "below_run_d": below_run_length_from(i),
        "last_z5_date": last_z5.date() if last_z5 is not None else None,
        "days_since_z5": days_since_z5,
        "max_fwd_dd_120d_pct": round(maxdd * 100, 1) if not np.isnan(maxdd) else None,
        "dd_ge_15pct": (maxdd <= DD_TH) if not np.isnan(maxdd) else None,
        "fwd_window_full": full,
    })

ev = pd.DataFrame(rows)
ev.to_csv(OUTDIR + r"\events_z5_recency_classification.csv", index=False)

print()
print("=" * 118)
print("TABEL EVENT STRICT (n=%d)" % len(ev))
print("=" * 118)
print("%-12s %-16s %12s %8s %8s %-14s %-22s %10s %8s %6s" % (
    "cross_date", "cycle", "price", "aboveRun", "belowRun",
    "last_Z5", "days_since_Z5", "maxDD120d", "dd>=15%", "full?"))
for _, r in ev.iterrows():
    print("%-12s %-16s %12.2f %8d %8d %-14s %-22s %9s%% %8s %6s" % (
        r["cross_date"], r["cycle"], r["price_at_cross"],
        r["prior_above_run_d"], r["below_run_d"],
        r["last_z5_date"] if r["last_z5_date"] else "-",
        r["days_since_z5"] if r["days_since_z5"] is not None else "belum pernah",
        r["max_fwd_dd_120d_pct"], r["dd_ge_15pct"], r["fwd_window_full"]))

# sebaran per cycle
print()
print("SEBARAN PER CYCLE:")
print(ev.groupby("cycle").size().to_string())

# klasifikasi recency
print()
print("=" * 118)
print("KLASIFIKASI RECENCY Z5 (grup KB 6C.2: <=75 hari vs >600 hari)")
print("=" * 118)
def grp(x):
    if x is None or (isinstance(x, float) and np.isnan(x)): return "belum pernah Z5 (data AVIV mulai 2010)"
    if x <= 75:   return "<=75 hari"
    if x > 600:   return ">600 hari"
    return "75-600 hari (gap)"
ev["grp"] = [grp(x) for x in ev["days_since_z5"]]
ev.to_csv(OUTDIR + r"\events_z5_recency_classification.csv", index=False)
for g in ["<=75 hari", "75-600 hari (gap)", ">600 hari", "belum pernah Z5 (data AVIV mulai 2010)"]:
    sub = ev[ev["grp"] == g]
    if len(sub) == 0:
        continue
    dds = sub["max_fwd_dd_120d_pct"].dropna()
    print("\nGrup %s : n=%d" % (g, len(sub)))
    for _, r in sub.iterrows():
        print("  %s  dd120=%s%%  (dd>=15%%: %s%s)" % (
            r["cross_date"], r["max_fwd_dd_120d_pct"], r["dd_ge_15pct"],
            "" if r["fwd_window_full"] else ", WINDOW BELUM PENUH"))
    if len(dds) > 0:
        print("  median dd grup: %.1f%% | hit dd>=15%%: %d/%d" % (
            dds.median(), (dds <= -15).sum(), len(dds)))

# fokus pertanyaan inti: event 2019, 2024, 2026
print()
print("=" * 118)
print("PERTANYAAN INTI -- event 2019, 2024, 2026: jinak (chart) atau ganas (KB)?")
print("=" * 118)
for yr in [2019, 2024, 2025, 2026]:
    sub = ev[[pd.Timestamp(x).year == yr for x in ev["cross_date"]]]
    for _, r in sub.iterrows():
        verdict = "GANAS (dd >= 15%)" if r["dd_ge_15pct"] else "JINAK (dd < 15%)"
        if not r["fwd_window_full"]:
            verdict += " -- window 120d BELUM PENUH, provisional"
        print("  %s | days_since_Z5=%s | maxDD120d=%s%% -> %s" % (
            r["cross_date"], r["days_since_z5"], r["max_fwd_dd_120d_pct"], verdict))

# base rate untuk konteks lift
all_dd = []
for i in range(len(d) - FWD):
    fwd = prices[i+1:i+1+FWD]
    all_dd.append(fwd.min() / prices[i] - 1.0)
all_dd = np.array(all_dd)
print()
print("Base rate (hari acak, dd>=15%% dalam 120 hari): %.2f" % (all_dd <= DD_TH).mean())
