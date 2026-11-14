# -*- coding: utf-8 -*-
"""
V3 - Apakah persentil MVRV "kebal" diminishing peaks?

Klaim video (On-Chain Mind 2026-09-15, [06:28]-[07:47]):
  percentile view "doesn't care about those diminishing returns"; "a 90th percentile
  reading in 2013 and a 90th percentile reading today mean the same thing".
  Frame [06:40-07:10]: 2024-25 sempat ~90%+, sekarang ~35-40, low 2026 ~15-20 (low confidence).
  Panel distribusi [09:10-09:40]: MVRV 1.43, % days below 36.6% (low confidence).

DEFINISI (dipakai ulang persis dari findings_mvrv_percentile_causal.md, 2026-08-05):
  P1 causal = percentile rank mvrv_ratio[t] di antara mvrv_ratio[0..t] (expanding, <=),
  burn-in 365 hari (valid sejak 2011-07-17). Full-sample hanya CERMIN (lookahead).
  Tanpa varian detrended.
  Cycle peak: 2011-06-08, 2013-11-29, 2017-12-16, 2021-11-08, 2025-10-06.
  Cycle low (close min peak->peak, definisi 08-25): 2011-11-18, 2015-01-14, 2018-12-14,
    2022-11-21, 2026-06-30 (sementara).
  Bull window = cycle low sebelumnya -> cycle peak (bull 2011: awal data -> 2011-06-08,
    seluruhnya di burn-in -> hanya cermin full-sample).
  Bear window = cycle peak -> cycle low (2025: peak -> hari terakhir data).

FALSIFIKASI (ditetapkan di muka oleh claim-tester):
  Klaim GAGAL kalau (1) bull 2021 ATAU bull 2024-25 tidak mencapai >= p90 causal, ATAU
  (2) persentil peak turun searah peak raw (turun monoton di tiap cycle berurutan, sama
  seperti raw).
Sanity C3: % hari mvrv_ratio < nilai 2026-09-15 (full history) vs 36.6% di video.
Output print ASCII saja.
"""
import numpy as np
import pandas as pd

DATA = "D:/Claude Code/Projects/Onchain-Dashboard/data_master_all_metrics.csv"
OUT = ("D:/Claude Code/Projects/Content-Breakdown/Outputs/videos/"
       "2026-09-15_bitcoin-mvrv-explained-almost-nobody-reads-it-properly")
BURN_IN = 365

df = pd.read_csv(DATA, parse_dates=["date"])
df = df.dropna(subset=["btc_price", "mvrv_ratio", "realized_price"]).copy()
df = df[(df["btc_price"] > 0) & (df["mvrv_ratio"] > 0)].sort_values("date").reset_index(drop=True)
LAST = df["date"].max()
n = len(df)
mv = df["mvrv_ratio"].values
print("Data: %s s/d %s (n=%d) | burn-in -> causal valid sejak %s" % (
    df["date"].min().date(), LAST.date(), n, df["date"].iloc[BURN_IN].date()))

p1c = np.full(n, np.nan)
for i in range(BURN_IN, n):
    p1c[i] = (mv[:i + 1] <= mv[i]).sum() / (i + 1) * 100.0
srt = np.sort(mv)
p1f = np.searchsorted(srt, mv, side="right") / n * 100.0
df["p1_causal"] = p1c
df["p1_full"] = p1f

PEAKS = ["2011-06-08", "2013-11-29", "2017-12-16", "2021-11-08", "2025-10-06"]
LOWS = ["2011-11-18", "2015-01-14", "2018-12-14", "2022-11-21", "2026-06-30"]
NAMES = ["2011", "2013", "2017", "2021", "2025"]


def row_at(d):
    r = df[df["date"] <= pd.Timestamp(d)].iloc[-1]
    return r


print("\n" + "=" * 110)
print("(1) PERSENTIL DI TANGGAL CYCLE PEAK")
print("=" * 110)
print("%-6s %-12s %8s %10s %9s" % ("cycle", "peak", "MVRV", "P1causal", "P1full"))
peak_rows = []
for nm, pk in zip(NAMES, PEAKS):
    r = row_at(pk)
    pc = r["p1_causal"]
    print("%-6s %-12s %8.3f %10s %9.1f" % (nm, pk, r["mvrv_ratio"], ("%.1f" % pc) if not np.isnan(pc) else "burn-in", r["p1_full"]))
    peak_rows.append(dict(cycle=nm, peak=pk, mvrv_at_peak=round(r["mvrv_ratio"], 4),
                          p1_causal_at_peak=None if np.isnan(pc) else round(pc, 2), p1_full_at_peak=round(r["p1_full"], 2)))

print("\n" + "=" * 110)
print("(2) PER BULL WINDOW (cycle low sebelumnya -> cycle peak): max MVRV raw, max persentil, hari >= p90")
print("=" * 110)
bull_rows = []
starts = [str(df["date"].min().date())] + LOWS[:-1]
print("%-6s %-12s %-12s %6s %9s %-12s %10s %-12s %8s %8s %8s %8s" % (
    "bull", "mulai", "peak", "hari", "maxMVRV", "tgl", "maxP1c", "tgl", "hr>=p90c", "%hari", "hr>=p95c", "maxP1f"))
for nm, a, pk in zip(NAMES, starts, PEAKS):
    w = df[(df["date"] >= a) & (df["date"] <= pk)]
    wc = w.dropna(subset=["p1_causal"])
    imx = w["mvrv_ratio"].idxmax()
    if len(wc):
        ipc = wc["p1_causal"].idxmax()
        maxpc, dpc = df.at[ipc, "p1_causal"], str(df.at[ipc, "date"].date())
        n90 = int((wc["p1_causal"] >= 90).sum())
        n95 = int((wc["p1_causal"] >= 95).sum())
        pct90 = 100.0 * n90 / len(w)
    else:
        maxpc, dpc, n90, n95, pct90 = np.nan, "burn-in", 0, 0, np.nan
    print("%-6s %-12s %-12s %6d %9.3f %-12s %10s %-12s %8d %7s %8d %8.1f" % (
        nm, a, pk, len(w), df.at[imx, "mvrv_ratio"], df.at[imx, "date"].date(),
        ("%.1f" % maxpc) if not np.isnan(maxpc) else "n/a", dpc, n90,
        ("%.1f%%" % pct90) if not np.isnan(pct90) else "n/a", n95, w["p1_full"].max()))
    bull_rows.append(dict(bull=nm, start=a, peak=pk, days=len(w), max_mvrv=round(df.at[imx, "mvrv_ratio"], 4),
                          max_mvrv_date=str(df.at[imx, "date"].date()),
                          max_p1_causal=None if np.isnan(maxpc) else round(maxpc, 2), max_p1_causal_date=dpc,
                          days_ge_p90_causal=n90, pct_days_ge_p90_causal=None if np.isnan(pct90) else round(pct90, 1),
                          days_ge_p95_causal=n95, max_p1_full=round(w["p1_full"].max(), 2)))

# threshold MVRV yang setara p90 causal di tanggal peak (menunjukkan "bar" yang harus dilewati)
print("\n  Nilai MVRV yang setara p90 causal (kuantil 90 dari data s/d tanggal) di tanggal peak:")
for nm, pk in zip(NAMES, PEAKS):
    hist = df[df["date"] <= pk]["mvrv_ratio"].values
    if len(hist) > BURN_IN:
        print("    %s %s: p90 = %.3f | p95 = %.3f" % (nm, pk, np.quantile(hist, 0.90), np.quantile(hist, 0.95)))
hist = mv
print("    per %s: p90 = %.3f | p95 = %.3f" % (LAST.date(), np.quantile(hist, 0.90), np.quantile(hist, 0.95)))

print("\n" + "=" * 110)
print("(3) BEAR LOW: persentil causal di cycle low vs min di bear berjalan")
print("=" * 110)
bear_rows = []
for nm, pk, lo in zip(NAMES, PEAKS, LOWS):
    end = lo if nm != "2025" else str(LAST.date())
    w = df[(df["date"] >= pk) & (df["date"] <= end)].dropna(subset=["p1_causal"])
    if not len(w):
        print("  %s: burn-in" % nm)
        continue
    im = w["p1_causal"].idxmin()
    r = row_at(lo)
    print("  %s: P1 causal @ low %s = %s | min P1 causal di bear = %.1f pada %s | min P1 full = %.1f%s" % (
        nm, lo, ("%.1f" % r["p1_causal"]) if not np.isnan(r["p1_causal"]) else "burn-in",
        df.at[im, "p1_causal"], df.at[im, "date"].date(), w["p1_full"].min(),
        "  [BERJALAN, low sementara]" if nm == "2025" else ""))
    bear_rows.append(dict(bear=nm, low=lo, p1_causal_at_low=None if np.isnan(r["p1_causal"]) else round(r["p1_causal"], 2),
                          min_p1_causal_in_bear=round(df.at[im, "p1_causal"], 2),
                          min_date=str(df.at[im, "date"].date()), min_p1_full_in_bear=round(w["p1_full"].min(), 2)))

print("\n" + "=" * 110)
print("(4) FALSIFIKASI")
print("=" * 110)
br = {r["bull"]: r for r in bull_rows}
f1 = []
for c in ["2021", "2025"]:
    ok = br[c]["max_p1_causal"] is not None and br[c]["max_p1_causal"] >= 90
    f1.append(ok)
    print("  bull %s mencapai >= p90 causal? %s (max %.1f)" % (c, "YA" if ok else "TIDAK", br[c]["max_p1_causal"]))
seq_raw_peak = [float(r["mvrv_at_peak"]) for r in peak_rows if r["p1_causal_at_peak"] is not None]
seq_pc_peak = [float(r["p1_causal_at_peak"]) for r in peak_rows if r["p1_causal_at_peak"] is not None]
seq_raw_bull = [float(br[c]["max_mvrv"]) for c in ["2013", "2017", "2021", "2025"]]
seq_pc_bull = [float(br[c]["max_p1_causal"]) for c in ["2013", "2017", "2021", "2025"]]


def mono_dec(s):
    return all(s[i] > s[i + 1] for i in range(len(s) - 1))


print("  di tanggal peak (2013,2017,2021,2025): raw %s -> %s | P1 causal %s -> %s" % (
    seq_raw_peak, "TURUN MONOTON" if mono_dec(seq_raw_peak) else "tidak monoton",
    seq_pc_peak, "TURUN MONOTON" if mono_dec(seq_pc_peak) else "tidak monoton"))
print("  max per bull (2013,2017,2021,2025): raw %s -> %s | P1 causal %s -> %s" % (
    seq_raw_bull, "TURUN MONOTON" if mono_dec(seq_raw_bull) else "tidak monoton",
    seq_pc_bull, "TURUN MONOTON" if mono_dec(seq_pc_bull) else "tidak monoton"))
fail = (not all(f1)) or mono_dec(seq_pc_peak) or mono_dec(seq_pc_bull)
print("  >> kriteria falsifikasi terpenuhi (klaim GAGAL)? %s" % ("YA" if fail else "TIDAK"))

print("\n" + "=" * 110)
print("(5) SANITY C3 & C1 per %s" % LAST.date())
print("=" * 110)
cur = mv[-1]
below = (mv < cur).mean() * 100
bucket = int(((mv >= 1.40) & (mv < 1.60)).sum())
print("  mvrv_ratio = %.4f | %% hari < nilai ini (full history %s..%s) = %.1f%% (video 36.6%%)" % (
    cur, df["date"].min().date(), LAST.date(), below))
print("  %% hari < 1.43 (angka layar video) = %.1f%%" % ((mv < 1.43).mean() * 100))
print("  hari di bucket 1.40-1.60 = %d (video 605)" % bucket)
print("  P1 causal per %s = %.1f (= full-sample di hari terakhir) | frame video ~35-40" % (LAST.date(), p1c[-1]))
w26 = df[(df["date"] >= "2026-01-01")].dropna(subset=["p1_causal"])
im = w26["p1_causal"].idxmin()
print("  min P1 causal 2026 = %.1f pada %s | frame video low 2026 ~15-20" % (df.at[im, "p1_causal"], df.at[im, "date"].date()))

ev = (pd.DataFrame(peak_rows)
      .merge(pd.DataFrame(bull_rows).rename(columns={"bull": "cycle", "peak": "peak_b"}), on="cycle", how="outer")
      .merge(pd.DataFrame(bear_rows).rename(columns={"bear": "cycle"}), on="cycle", how="outer")
      .drop(columns=["peak_b"]))
ev.to_csv(OUT + "/events_mvrv_percentile_diminishing_peaks.csv", index=False)
print("CSV -> events_mvrv_percentile_diminishing_peaks.csv")
