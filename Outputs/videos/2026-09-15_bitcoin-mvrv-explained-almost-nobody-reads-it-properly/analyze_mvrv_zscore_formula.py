# -*- coding: utf-8 -*-
"""
V4 - Rumus & kausalitas kolom mvrv_zscore.

Konflik dokumentasi:
  - Video (On-Chain Mind 2026-09-15, [05:40-06:10], rumus di layar):
      Z = (Market Cap - Realized Cap) / StDev(Market Cap)
  - KB MVRV v1.4 sec.1: Z = (MVRV - mean) / stdev (historical mean & stdev seluruh history)
  - data_dictionary.md: mvrv_zscore = "Z-score MVRV full-history"

DEFINISI (maks 4 varian, dikunci sebelum menghitung - TIDAK ditambah kalau tidak ada yang cocok):
  market_cap = mvrv_ratio * realized_cap_usd  (cross-check: btc_price * (lth_supply_btc + sth_supply_btc))
  A-exp : (MC - RC) / std_expanding(MC)          [std s/d hari t saja -> causal]
  A-full: (MC - RC) / std_fullsample(MC)         [std seluruh data s/d 2026-09-15 -> lookahead]
  B-exp : (MVRV - mean_exp(MVRV)) / std_exp(MVRV)
  B-full: (MVRV - mean_full) / std_full
  std = pandas default (ddof=1). Expanding min_periods = 2.
Ukuran kecocokan vs mvrv_zscore: korelasi Pearson, median |error|, median rasio (kolom/varian),
  di (i) seluruh data, (ii) pasca burn-in 365 hari (sejak 2011-07-17, sama dgn V3).
Nilai di 2017-12-16, 2021-11-08, 2022-11-21, 2025-10-06.
Aturan: "cocok" = korelasi >= 0.99 DAN median |error| <= 0.05 (ditetapkan di muka). Kalau tidak ada
  yang cocok -> TIDAK KONKLUSIF, berhenti.
Suplemen bukti revisi historis: nilai Z yang tercatat di KB MVRV v1.4 sec.2.1 (ditulis sebelum
  data s/d 2026-09-15) vs nilai kolom sekarang di rentang tanggal yang sama.
Output print ASCII saja.
"""
import numpy as np
import pandas as pd

DATA = "D:/Claude Code/Projects/Onchain-Dashboard/data_master_all_metrics.csv"
BURN_IN = 365
MATCH_CORR = 0.99
MATCH_MAE = 0.05

df = pd.read_csv(DATA, parse_dates=["date"])
df = df.dropna(subset=["btc_price", "mvrv_ratio", "realized_cap_usd", "mvrv_zscore"]).copy()
df = df[(df["btc_price"] > 0) & (df["mvrv_ratio"] > 0)].sort_values("date").reset_index(drop=True)
LAST = df["date"].max()
print("Data: %s s/d %s (n=%d)" % (df["date"].min().date(), LAST.date(), len(df)))

MC = df["mvrv_ratio"] * df["realized_cap_usd"]
RC = df["realized_cap_usd"]
df["mc"] = MC
sup = df["lth_supply_btc"] + df["sth_supply_btc"]
mc2 = df["btc_price"] * sup
ok = mc2.notna() & (mc2 > 0)
rel = (MC[ok] / mc2[ok] - 1).abs()
print("Cross-check market cap: MVRV*RC vs price*(LTH+STH supply): n=%d hari, median |selisih| = %.3f%%, p95 = %.3f%%" % (
    int(ok.sum()), rel.median() * 100, rel.quantile(0.95) * 100))

mv = df["mvrv_ratio"]
V = {
    "A-exp": (MC - RC) / MC.expanding(min_periods=2).std(),
    "A-full": (MC - RC) / MC.std(),
    "B-exp": (mv - mv.expanding(min_periods=2).mean()) / mv.expanding(min_periods=2).std(),
    "B-full": (mv - mv.mean()) / mv.std(),
}
z = df["mvrv_zscore"]

print("\n" + "=" * 110)
print("KECOCOKAN VARIAN vs kolom mvrv_zscore")
print("=" * 110)
print("%-8s | %-34s | %-34s" % ("varian", "seluruh data: corr / med|err| / med rasio", "pasca burn-in: corr / med|err| / med rasio"))
res = {}
for k, v in V.items():
    out = []
    for sub in [slice(None), slice(BURN_IN, None)]:
        a = z.iloc[sub]
        b = v.iloc[sub]
        m = a.notna() & b.notna() & np.isfinite(b)
        corr = np.corrcoef(a[m], b[m])[0, 1]
        mae = (a[m] - b[m]).abs().median()
        rb = b[m].abs() > 0.2
        ratio = (a[m][rb] / b[m][rb]).median()
        out.append((corr, mae, ratio))
    res[k] = out
    print("%-8s | corr %.4f  med|err| %8.4f  rasio %6.3f | corr %.4f  med|err| %8.4f  rasio %6.3f" % (
        k, out[0][0], out[0][1], out[0][2], out[1][0], out[1][1], out[1][2]))

match = [k for k, o in res.items() if o[1][0] >= MATCH_CORR and o[1][1] <= MATCH_MAE]
print("\n  Varian yang COCOK (corr >= %.2f & med|err| <= %.2f, pasca burn-in): %s" % (MATCH_CORR, MATCH_MAE, match or "TIDAK ADA -> TIDAK KONKLUSIF"))

print("\n" + "=" * 110)
print("NILAI DI TANGGAL KUNCI")
print("=" * 110)
print("%-12s %8s %10s %9s %9s %9s %9s" % ("tanggal", "MVRV", "mvrv_z", "A-exp", "A-full", "B-exp", "B-full"))
for d in ["2013-11-29", "2017-12-16", "2021-11-08", "2022-11-21", "2025-10-06", str(LAST.date())]:
    i = int(df.index[df["date"] <= d][-1])
    print("%-12s %8.3f %10.3f %9.3f %9.3f %9.3f %9.3f" % (
        df.at[i, "date"].date(), mv.iloc[i], z.iloc[i], V["A-exp"].iloc[i], V["A-full"].iloc[i], V["B-exp"].iloc[i], V["B-full"].iloc[i]))

# ---- kalau A cocok: cek sensitivitas historis terhadap panjang data (bukti lookahead) ----
print("\n" + "=" * 110)
print("SUPLEMEN - apakah nilai historis BERUBAH kalau data diperpanjang? (sifat full-sample)")
print("=" * 110)
for cut in ["2021-11-08", "2025-10-06"]:
    sub = df[df["date"] <= cut]
    mcs = sub["mvrv_ratio"] * sub["realized_cap_usd"]
    zA = (mcs - sub["realized_cap_usd"]) / mcs.std()
    mvs = sub["mvrv_ratio"]
    zB = (mvs - mvs.mean()) / mvs.std()
    i = sub.index[-1]
    print("  kalau data berhenti %s: A-full di %s = %.3f | B-full = %.3f   (vs dgn data s/d %s: A-full %.3f, B-full %.3f, kolom %.3f)" % (
        cut, cut, zA.iloc[-1], zB.iloc[-1], LAST.date(), V["A-full"].iloc[i], V["B-full"].iloc[i], z.iloc[i]))

print("\n  Nilai Z tercatat di KB MVRV v1.4 sec.2.1 vs kolom sekarang (rentang tanggal sama):")
KB = [("Cycle Peak 2017", "2017-12-08", "2017-12-19", "7.49-9.24"),
      ("Cycle Peak 2021", "2021-10-20", "2021-11-09", "2.96-3.66"),
      ("Cycle Peak 2025", "2025-10-05", "2025-10-07", "2.40-2.53")]
for nm, a, b, kbv in KB:
    w = df[(df["date"] >= a) & (df["date"] <= b)]
    print("    %-16s KB: %-10s | kolom sekarang: %.2f-%.2f | A-exp: %.2f-%.2f | A-full: %.2f-%.2f" % (
        nm, kbv, w["mvrv_zscore"].min(), w["mvrv_zscore"].max(),
        V["A-exp"].loc[w.index].min(), V["A-exp"].loc[w.index].max(),
        V["A-full"].loc[w.index].min(), V["A-full"].loc[w.index].max()))

print("\n  Threshold Z yang dipakai KB (B2 >1.0; B5 < -0.15; B6 > 0.05; 4B >1.0 / < -0.15):")
print("  hari terakhir kolom < -0.15 = %s | hari terakhir > 1.0 = %s" % (
    df[z < -0.15]["date"].max().date(), df[z > 1.0]["date"].max().date()))
for k in ["A-exp", "A-full"]:
    s = V[k]
    print("  %-7s: hari terakhir < -0.15 = %s | hari terakhir > 1.0 = %s" % (
        k, df[s < -0.15]["date"].max().date(), df[s > 1.0]["date"].max().date()))
# selisih label threshold antara kolom (apapun rumusnya) dan versi causal A-exp
for thr, sgn in [(1.0, ">"), (-0.15, "<"), (0.05, ">")]:
    a = (z > thr) if sgn == ">" else (z < thr)
    b = (V["A-exp"] > thr) if sgn == ">" else (V["A-exp"] < thr)
    m = V["A-exp"].notna()
    m.iloc[:BURN_IN] = False
    print("  Z %s %.2f: hari berbeda label kolom vs A-exp (pasca burn-in) = %d dari %d (%.1f%%)" % (
        sgn, thr, int((a[m] != b[m]).sum()), int(m.sum()), 100 * (a[m] != b[m]).mean()))
