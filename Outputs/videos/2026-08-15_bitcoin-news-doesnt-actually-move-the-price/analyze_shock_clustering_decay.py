"""
VALIDASI 2 - Clustering (B-5) + decay profile (B-6).

Q1 P(ada shock lain dalam 5 hari | hari ini shock) vs baseline. Horizon 10 juga.
   Klaim video: BTC 47% vs 29%.
Q2 Baseline dua cara: (a) unconditional rate, (b) shuffle per-tahun (jumlah shock
   per tahun dipertahankan) -> efek komposisi era tidak dihitung sebagai clustering.
Q3 Decay: mean |logret| di t+1..t+30 / mean|logret| trailing 90d AT-GATE.
   Hari ke berapa turun di bawah 1.2x? Klaim video: ~10-20 hari trading.
Q4 Beda horizon peluruhan ZC/Z1 vs Z4/Z5?
Q5 Kondisional 1 hari turun >=10%: drawdown kumulatif terburuk 5 & 10 hari (p50/80/95).

Definisi shock & zona: shock_zone_lib.py (dikunci di muka, tidak diubah setelah lihat hasil).
"""
import numpy as np
import pandas as pd
import shock_zone_lib as L

OUT_CSV = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-15_bitcoin-news-doesnt-actually-move-the-price\events_shock_clustering.csv"
RNG = np.random.default_rng(20260820)
NBOOT = 1000

df = L.load_base()
df["dd5"] = L.fwd_worst_drawdown(df["btc_price"], 5)
df["dd10"] = L.fwd_worst_drawdown(df["btc_price"], 10)
df13 = df[df["date"] >= "2013-01-01"].reset_index(drop=True)


def line(c="="):
    print(c * 100)


def any_shock_fwd(flags, h):
    """ada shock di t+1..t+h ? (NaN kalau window keluar sample)"""
    n = len(flags)
    out = np.zeros(n, dtype=float)
    for i in range(n):
        if i + h >= n:
            out[i] = np.nan
        else:
            out[i] = 1.0 if flags[i + 1:i + 1 + h].any() else 0.0
    return out


def cluster_stats(d, col, h):
    flags = d[col].values.astype(bool)
    fw = any_shock_fwd(flags, h)
    valid = ~np.isnan(fw)
    cond = fw[valid & flags]
    base = fw[valid]
    return dict(n_shock=int(len(cond)), p_cond=float(np.mean(cond)),
                n_all=int(len(base)), p_rand=float(np.mean(base)))


def shuffle_baseline(d, col, h, nboot=NBOOT):
    """Baseline (b): acak ulang posisi shock DI DALAM tiap tahun kalender,
    jumlah shock per tahun dipertahankan -> komposisi era netral."""
    years = d["date"].dt.year.values
    flags = d[col].values.astype(bool)
    idx_by_year = {y: np.where(years == y)[0] for y in np.unique(years)}
    cnt_by_year = {y: int(flags[ix].sum()) for y, ix in idx_by_year.items()}
    res_cond = []
    for _ in range(nboot):
        f = np.zeros(len(d), dtype=bool)
        for y, ix in idx_by_year.items():
            k = cnt_by_year[y]
            if k:
                f[RNG.choice(ix, size=k, replace=False)] = True
        fw = any_shock_fwd(f, h)
        valid = ~np.isnan(fw)
        res_cond.append(np.mean(fw[valid & f]))
    return float(np.mean(res_cond)), np.percentile(res_cond, [2.5, 97.5])


line()
print("Q1/Q2 CLUSTERING  (klaim video BTC: 47% vs 29% untuk horizon 5 hari)")
for scope, d in [("FULL 2010-2026", df), (">=2013", df13)]:
    for col, cl in [("shock_primary", "PRIMARY 3x vol30"), ("shock_fixed", "VARIAN 8%")]:
        for h in (5, 10):
            s = cluster_stats(d, col, h)
            mb, ci = shuffle_baseline(d, col, h)
            lo, hi = L.wilson(int(round(s["p_cond"] * s["n_shock"])), s["n_shock"])
            print(f"{scope:<15}{cl:<18}h={h:<3} n_shock={s['n_shock']:<4} "
                  f"P(cond)={s['p_cond']*100:5.1f}% [CI {lo*100:.0f}-{hi*100:.0f}]  "
                  f"base_a={s['p_rand']*100:5.1f}%  base_b(shuffle)={mb*100:5.1f}% "
                  f"[{ci[0]*100:.0f}-{ci[1]*100:.0f}]  lift_vs_b={(s['p_cond']-mb)*100:+5.1f}pp")

line("-")
print("Robustness: buang efek trivial 'shock kemarin - shock hari ini' dengan menghitung")
print("shock lain di window t+2..t+h (t+1 dikeluarkan), kondisi = shock day PRIMARY, >=2013.")


def cluster_gap(d, cond_col, target_col, h, skip=1):
    flags_t = d[target_col].values.astype(bool)
    flags_c = d[cond_col].values.astype(bool)
    n = len(d)
    fw = np.full(n, np.nan)
    for i in range(n):
        if i + h >= n:
            continue
        fw[i] = 1.0 if flags_t[i + 1 + skip:i + 1 + h].any() else 0.0
    valid = ~np.isnan(fw)
    return (int(np.sum(valid & flags_c)), float(np.mean(fw[valid & flags_c])),
            float(np.mean(fw[valid])))


for h in (5, 10):
    nc, pc, pr = cluster_gap(df13, "shock_primary", "shock_primary", h)
    print(f"  window t+2..t+{h:<3} n={nc:<4} P(cond)={pc*100:5.1f}%  base_a(hari acak)={pr*100:5.1f}%  "
          f"lift={(pc-pr)*100:+5.1f}pp")

print("")
print("Sebaran shock per cycle (PRIMARY, dipakai untuk cek dominasi era):")
print(df.groupby("cycle")["shock_primary"].sum().to_string())

# ---------------- Q3/Q4 decay ----------------
line()
print("Q3 DECAY - mean |logret| t+1..t+30 dinormalisasi ke mean|logret| trailing 90d AT-GATE")
print("(1.0 = 'hari normal'; ambang yang diminta = 1.2x)")


def decay_profile(d, mask, horizon=30):
    idx = np.where(mask)[0]
    lr = d["logret"].abs().values
    norm = d["absmean90_atgate"].values
    rows = []
    for k in range(0, horizon + 1):
        vals = []
        for i in idx:
            j = i + k
            if j < len(d) and np.isfinite(norm[i]) and norm[i] > 0 and np.isfinite(lr[j]):
                vals.append(lr[j] / norm[i])
        rows.append((k, len(vals), float(np.mean(vals)) if vals else np.nan,
                     float(np.median(vals)) if vals else np.nan))
    p = pd.DataFrame(rows, columns=["k", "n", "mean_x", "median_x"])
    p["smooth5"] = p["mean_x"].rolling(5, center=True, min_periods=3).mean()
    return p


def first_below(prof, thr=1.2, col="mean_x"):
    sub = prof[prof["k"] >= 1]
    hit = sub[sub[col] < thr]
    return int(hit["k"].iloc[0]) if len(hit) else None


KS = [0, 1, 2, 3, 4, 5, 7, 10, 14, 20, 30]
for scope, d in [("FULL", df), (">=2013", df13)]:
    m = d["shock_primary"].values.astype(bool)
    prof = decay_profile(d, m)
    print("")
    print(f"[{scope}] n shock = {int(m.sum())} | pertama mean < 1.2x : {first_below(prof)}"
          f" | pertama median < 1.2x : {first_below(prof, col='median_x')}"
          f" | pertama mean-smooth5 < 1.2x : {first_below(prof, col='smooth5')}")
    print("  k    :", " ".join(f"{k:>5}" for k in KS))
    print("  mean :", " ".join(f"{prof.loc[k,'mean_x']:5.2f}" for k in KS))
    print("  med  :", " ".join(f"{prof.loc[k,'median_x']:5.2f}" for k in KS))
    print("  smth5:", " ".join(f"{prof.loc[k,'smooth5']:5.2f}" for k in KS))

print("")
print("Q4 DECAY PER ZONA SHOCK (>=2013, PRIMARY)")
for zs, nm in [(["ZC", "Z1", "Z1b"], "ZC/Z1/Z1b (bawah)"), (["Z4", "Z5"], "Z4/Z5 (atas)"),
               (["ZD", "Z3"], "ZD/Z3 (tengah)")]:
    m = (df13["shock_primary"] & df13["zone"].isin(zs)).values
    prof = decay_profile(df13, m)
    print(f"  {nm:<20} n={int(m.sum()):<4} k1={prof.loc[1,'mean_x']:.2f} k3={prof.loc[3,'mean_x']:.2f} "
          f"k5={prof.loc[5,'mean_x']:.2f} k10={prof.loc[10,'mean_x']:.2f} k20={prof.loc[20,'mean_x']:.2f} "
          f"k30={prof.loc[30,'mean_x']:.2f} | pertama <1.2x mean={first_below(prof)} "
          f"smooth5={first_below(prof, col='smooth5')}")

print("")
print("Decay per arah shock (>=2013):")
for sgn, nm in [(-1, "DOWN-shock"), (1, "UP-shock")]:
    m = (df13["shock_primary"] & (np.sign(df13["logret"]) == sgn)).values
    prof = decay_profile(df13, m)
    print(f"  {nm:<12} n={int(m.sum()):<4} k1={prof.loc[1,'mean_x']:.2f} k5={prof.loc[5,'mean_x']:.2f} "
          f"k10={prof.loc[10,'mean_x']:.2f} k20={prof.loc[20,'mean_x']:.2f} | pertama <1.2x mean="
          f"{first_below(prof)} smooth5={first_below(prof, col='smooth5')}")

# ---------------- Q5 ----------------
line()
print("Q5 KONDISIONAL: satu hari turun >=10% (simple return <= -10%)")
big = df13[(np.exp(df13["logret"]) - 1) <= -0.10].reset_index(drop=True)
print(f"n hari (>=2013) = {len(big)} | sebaran cycle:")
print(big.groupby("cycle").size().to_string())
big["f"] = True
ev_mask = L.event_flags(big, "f", cooldown=5)
print(f"n EPISODE setelah merge cooldown 5 hari = {int(ev_mask.sum())}")
print(big[ev_mask].groupby("cycle").size().to_string())
for lab, sub in [("semua hari", big), ("episode (merge 5d)", big[ev_mask])]:
    for h, col in [(5, "dd5"), (10, "dd10")]:
        v = sub[col].dropna().values * 100
        print(f"  {lab:<20} DD terburuk {h:>2} hari ke depan: "
              f"p50={np.percentile(v,50):6.1f}%  p80={np.percentile(v,20):6.1f}%  "
              f"p95={np.percentile(v,5):6.1f}%  worst={v.min():6.1f}%  n={len(v)}")

print("")
print("Pembanding: hari acak >=2013 (bukan setelah -10%)")
for h, col in [(5, "dd5"), (10, "dd10")]:
    v = df13[col].dropna().values * 100
    print(f"  {'hari acak':<20} DD terburuk {h:>2} hari ke depan: "
          f"p50={np.percentile(v,50):6.1f}%  p80={np.percentile(v,20):6.1f}%  "
          f"p95={np.percentile(v,5):6.1f}%  worst={v.min():6.1f}%  n={len(v)}")

print("")
print("  Implikasi LTV, kondisional SETELAH sudah kena -10% sehari (drawdown 10 hari berikutnya):")
v = big["dd10"].dropna().values
for cap in (0.45, 0.48):
    for tgt in (0.58, 0.60, 0.65):
        need = 1 - cap / tgt
        print(f"    cap {cap*100:.0f}% -> LTV {tgt*100:.0f}%: butuh drop tambahan {need*100:5.1f}% ; "
              f"{100.0*np.mean(v <= -need):4.0f}% dari kejadian mencapainya dalam 10 hari")

flags = df["shock_primary"].values.astype(bool)
fw5 = any_shock_fwd(flags, 5)
fw10 = any_shock_fwd(flags, 10)
ev = df[flags][["date", "cycle", "zone", "btc_price", "logret",
                "vol30_atgate", "absmean90_atgate", "dd5", "dd10"]].copy()
ev["ret_pct"] = (np.exp(ev["logret"]) - 1) * 100
ev["next_shock_5d"] = fw5[flags]
ev["next_shock_10d"] = fw10[flags]
ev.to_csv(OUT_CSV, index=False)
print("")
print(f"[saved] {OUT_CSV} ({len(ev)} baris)")
