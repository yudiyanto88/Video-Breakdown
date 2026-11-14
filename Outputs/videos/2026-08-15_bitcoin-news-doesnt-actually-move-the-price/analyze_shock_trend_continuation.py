"""
VALIDASI 4 - "Shock memperpanjang trend, bukan membalikkannya" (insight B-1).
Klaim video: BTC flip rate 36% setelah shock vs 46% di hari acak.

Q1 Trend AT-GATE = tanda log return 30 hari yang berakhir di t-1 (hari shock
   DIKELUARKAN - ini titik lemah utama versi presenter, karena shock day sendiri
   ikut membentuk "trend sebelum shock" kalau tidak dikeluarkan).
   Flip = tanda forward log return t -> t+30 berbeda dari trend at-gate.
Q2 Flip rate pasca-shock vs (a) semua hari, dan (b) MATCHED baseline: hari
   non-shock dengan tanda trend at-gate SAMA (reweight ke komposisi shock).
   Verdict ditentukan oleh selisih terhadap (b).
Q3 Stratifikasi: arah shock (down vs up) dan per cycle. n per sel dilaporkan.

Definisi shock: shock_zone_lib.py (identik dengan validasi 1-3).
"""
import numpy as np
import pandas as pd
import shock_zone_lib as L

OUT_CSV = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-15_bitcoin-news-doesnt-actually-move-the-price\events_shock_trend_flip.csv"

df = L.load_base().reset_index(drop=True)
lp = np.log(df["btc_price"].values)
n = len(df)

# trend at-gate: log return 30 hari yang BERAKHIR di t-1 (t dikecualikan)
trend = np.full(n, np.nan)
for i in range(31, n):
    trend[i] = lp[i - 1] - lp[i - 31]
# versi presenter (naif): trend 30 hari berakhir di t (shock day ikut)
trend_naive = np.full(n, np.nan)
for i in range(30, n):
    trend_naive[i] = lp[i] - lp[i - 30]
# forward 30 hari
fwd = np.full(n, np.nan)
for i in range(n - 30):
    fwd[i] = lp[i + 30] - lp[i]

df["trend_atgate"] = trend
df["trend_naive"] = trend_naive
df["fwd30"] = fwd
df["flip"] = np.where(np.isnan(trend) | np.isnan(fwd), np.nan,
                      (np.sign(trend) != np.sign(fwd)).astype(float))
df["flip_naive"] = np.where(np.isnan(trend_naive) | np.isnan(fwd), np.nan,
                            (np.sign(trend_naive) != np.sign(fwd)).astype(float))
df["trend_sign"] = np.sign(df["trend_atgate"])
df["shock_dir"] = np.sign(df["logret"])
df["shock_event"] = L.event_flags(df, "shock_primary")


def line(c="="):
    print(c * 100)


def rate(mask, col="flip"):
    v = df.loc[mask, col].dropna()
    if len(v) == 0:
        return 0, np.nan, (np.nan, np.nan)
    k = int(v.sum())
    lo, hi = L.wilson(k, len(v))
    return len(v), v.mean(), (lo, hi)


def matched_baseline(shock_mask, pool_mask, col="flip"):
    """Baseline (b): hari non-shock, flip rate per tanda trend at-gate,
    di-reweight ke komposisi tanda trend pada hari shock."""
    sh = df.loc[shock_mask].dropna(subset=[col, "trend_sign"])
    if len(sh) == 0:
        return np.nan, 0
    w = sh["trend_sign"].value_counts(normalize=True)
    pool = df.loc[pool_mask].dropna(subset=[col, "trend_sign"])
    tot, npool = 0.0, 0
    for s, wt in w.items():
        p = pool.loc[pool["trend_sign"] == s, col]
        if len(p) == 0:
            continue
        tot += wt * p.mean()
        npool += len(p)
    return tot, npool


BASE13 = df["date"] >= "2013-01-01"
NONSHOCK = ~df["shock_primary"]

line()
print("Q1/Q2 FLIP RATE 30 HARI  (klaim video: 36% setelah shock vs 46% hari acak)")
print("flip = tanda return 30 hari ke depan BEDA dari tanda trend 30 hari at-gate (berakhir t-1)")
for scope, m0 in [("FULL 2010-2026", pd.Series(True, index=df.index)), (">=2013", BASE13)]:
    for col, cl in [("shock_primary", "PRIMARY 3x vol30"), ("shock_fixed", "VARIAN 8%")]:
        sm = m0 & df[col]
        nn, r, ci = rate(sm)
        na, ra, _ = rate(m0)
        mb, npool = matched_baseline(sm, m0 & ~df[col])
        print(f"\n[{scope} | {cl}]  n shock (dgn fwd30 valid) = {nn}")
        print(f"  flip setelah shock            : {r*100:5.1f}%  [CI {ci[0]*100:.0f}-{ci[1]*100:.0f}]")
        print(f"  (a) baseline semua hari       : {ra*100:5.1f}%   (n={na})   selisih = {(r-ra)*100:+5.1f}pp")
        print(f"  (b) baseline MATCHED non-shock: {mb*100:5.1f}%   (n pool={npool}) selisih = {(r-mb)*100:+5.1f}pp")

line()
print("Efek definisi trend: versi AT-GATE (t-1) vs versi NAIF (trend termasuk hari shock)")
for col, cl in [("shock_primary", "PRIMARY"), ("shock_fixed", "VARIAN 8%")]:
    sm = BASE13 & df[col]
    _, r1, _ = rate(sm, "flip")
    _, r2, _ = rate(sm, "flip_naive")
    _, b1, _ = rate(BASE13, "flip")
    _, b2, _ = rate(BASE13, "flip_naive")
    print(f"  {cl:<10} shock: at-gate={r1*100:5.1f}%  naif={r2*100:5.1f}%   |  "
          f"semua hari: at-gate={b1*100:5.1f}%  naif={b2*100:5.1f}%")

line()
print("Q3a STRATIFIKASI ARAH SHOCK (>=2013, PRIMARY)")
print(f"{'sel':<28}{'n':>5}{'flip%':>8}{'CI':>14}{'base(b)%':>10}{'selisih':>9}")
for dsign, dnm in [(-1.0, "DOWN-shock"), (1.0, "UP-shock")]:
    sm = BASE13 & df["shock_primary"] & (df["shock_dir"] == dsign)
    nn, r, ci = rate(sm)
    mb, _ = matched_baseline(sm, BASE13 & NONSHOCK)
    print(f"{dnm:<28}{nn:>5}{r*100:>8.1f}{f'[{ci[0]*100:.0f}-{ci[1]*100:.0f}]':>14}"
          f"{mb*100:>10.1f}{(r-mb)*100:>+9.1f}")

print("")
print("Q3b STRATIFIKASI ARAH SHOCK x TANDA TREND AT-GATE (>=2013, PRIMARY)")
print(f"{'sel':<28}{'n':>5}{'flip%':>8}{'n_base':>8}{'base%':>8}{'selisih':>9}")
for dsign, dnm in [(-1.0, "DOWN"), (1.0, "UP")]:
    for tsign, tnm in [(1.0, "trend NAIK"), (-1.0, "trend TURUN")]:
        sm = BASE13 & df["shock_primary"] & (df["shock_dir"] == dsign) & (df["trend_sign"] == tsign)
        nn, r, ci = rate(sm)
        pool = df.loc[BASE13 & NONSHOCK & (df["trend_sign"] == tsign), "flip"].dropna()
        print(f"{dnm+' + '+tnm:<28}{nn:>5}{r*100:>8.1f}{len(pool):>8}{pool.mean()*100:>8.1f}"
              f"{(r-pool.mean())*100:>+9.1f}")

print("")
print("Q3c PER CYCLE (PRIMARY, semua arah shock)")
print(f"{'cycle':<16}{'n':>5}{'flip%':>8}{'CI':>14}{'base(b)%':>10}{'selisih':>9}{'%dari total':>12}")
tot = int((df["shock_primary"] & df["flip"].notna()).sum())
for cname, s, e in L.CYCLES:
    cm = (df["date"] >= s) & (df["date"] <= e)
    sm = cm & df["shock_primary"]
    nn, r, ci = rate(sm)
    mb, _ = matched_baseline(sm, cm & NONSHOCK)
    print(f"{cname:<16}{nn:>5}{r*100:>8.1f}{f'[{ci[0]*100:.0f}-{ci[1]*100:.0f}]':>14}"
          f"{mb*100:>10.1f}{(r-mb)*100:>+9.1f}{100.0*nn/tot:>11.0f}%")

print("")
print("Q3d PER CYCLE x ARAH (n per sel)")
piv = (df[df["shock_primary"] & df["flip"].notna()]
       .assign(dir=lambda x: np.where(x["shock_dir"] < 0, "down", "up"))
       .pivot_table(index="cycle", columns="dir", values="flip", aggfunc=["count", "mean"]))
print(piv.round(3).to_string())

line()
print("ROBUSTNESS: event-merged (cooldown 5 hari) - mengurangi ketergantungan antar sample")
sm = BASE13 & df["shock_event"]
nn, r, ci = rate(sm)
mb, _ = matched_baseline(sm, BASE13 & NONSHOCK)
print(f"  n event = {nn} | flip = {r*100:.1f}% [CI {ci[0]*100:.0f}-{ci[1]*100:.0f}] | "
      f"matched baseline = {mb*100:.1f}% | selisih = {(r-mb)*100:+.1f}pp")
for dsign, dnm in [(-1.0, "DOWN"), (1.0, "UP")]:
    sm2 = sm & (df["shock_dir"] == dsign)
    nn2, r2, ci2 = rate(sm2)
    mb2, _ = matched_baseline(sm2, BASE13 & NONSHOCK)
    print(f"    {dnm:<6} n={nn2:<4} flip={r2*100:5.1f}% base={mb2*100:5.1f}% "
          f"selisih={(r2-mb2)*100:+5.1f}pp")

print("")
print("CATATAN INDEPENDENSI: window forward 30 hari saling tumpang tindih antar hari shock,")
print("jadi CI Wilson di atas TERLALU sempit. Baca sebagai indikasi arah, bukan uji formal.")

ev = df[df["shock_primary"]][["date", "cycle", "zone", "btc_price", "logret", "vol30_atgate",
                              "trend_atgate", "trend_naive", "fwd30", "flip", "flip_naive",
                              "shock_dir", "shock_event"]].copy()
ev["ret_pct"] = (np.exp(ev["logret"]) - 1) * 100
ev.to_csv(OUT_CSV, index=False)
print("")
print(f"[saved] {OUT_CSV} ({len(ev)} baris)")
