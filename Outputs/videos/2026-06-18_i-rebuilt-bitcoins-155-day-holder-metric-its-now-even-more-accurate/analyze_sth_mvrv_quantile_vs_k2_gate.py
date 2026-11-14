"""
V3 -- STH-MVRV trailing-Z quantile vs GATE VALUASI K2 (band absolut 0,80-0,97).

KLAIM YANG DIUJI (Matt Crosby, 2026-06-18, [10:07]-[10:31] + frame Figure 10):
  STH-MVRV yang dinormalisasi jadi trailing-Z lalu dibaca sebagai historical
  quantile "looking a lot more accurate", menandai turning point besar.
  -> pertanyaan framework: apakah versi quantile LEBIH BAIK dari gate valuasi
     K2 yang absolut (band 0,80-0,97)?

CATATAN PENTING: gate K2 adalah BAND DUA SISI, bukan threshold satu sisi.
  Batas bawah 0,80 fungsinya memisahkan bull dip dari bear dalam -- jadi
  perbandingannya harus band-vs-band, bukan threshold-vs-threshold.

BATASAN BESAR: data kita = vendor base "std" + boundary STH STATIS 155 hari.
  Tidak ada raw UTXO -> tidak bisa mereplikasi base "flt" / boundary 114d Matt.
  Yang diuji = METODOLOGI-nya di atas data kita, bukan replikasi angkanya.

ANTI-LOOKAHEAD: z = (x - mean_1460d) / std_1460d dengan window BERAKHIR t-1;
  percentile = expanding terhadap z-history sampai t-1 saja.
"""

import bisect
import warnings

import numpy as np
import pandas as pd

warnings.simplefilter("ignore")

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

Z_WIN      = 1460
MIN_Z_HIST = 365
GATE_LO    = 0.80
GATE_HI    = 0.97

df = pd.read_csv(MASTER, parse_dates=["date"])
df = df[df["btc_price"].notna()].sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["sth_mvrv", "mvrv_ratio", "sth_sopr", "asopr"]).reset_index(drop=True)

print("=" * 104)
print("V3  STH-MVRV TRAILING-Z QUANTILE  vs  GATE VALUASI K2 (band 0,80-0,97)")
print("=" * 104)
print(f"Data: {df['date'].min().date()} s/d {df['date'].max().date()} (n={len(df)})")
print("Basis: vendor std + boundary STH STATIS 155d. BUKAN base flt / 114d Matt.")

# ---------------------------------------------------------------- trailing-Z + expanding percentile
roll = df["sth_mvrv"].shift(1).rolling(Z_WIN, min_periods=Z_WIN)
df["z"] = (df["sth_mvrv"] - roll.mean()) / roll.std()

q = np.full(len(df), np.nan)
hist = []
for i, zi in enumerate(df["z"].values):
    if np.isnan(zi):
        continue
    if len(hist) >= MIN_Z_HIST:
        lo = bisect.bisect_left(hist, zi); hi = bisect.bisect_right(hist, zi)
        q[i] = (lo + 0.5 * (hi - lo)) / len(hist)
    bisect.insort(hist, zi)
df["q"] = q
qv = df[df["q"].notna()].reset_index(drop=True)
print(f"Quantile valid pertama: {qv['date'].min().date()} (warm-up {Z_WIN}d + {MIN_Z_HIST}d)")
print("-> cycle 2011 dan 2015 TIDAK bisa diuji (warm-up). Uji lintas-cycle TIDAK penuh.")

CYCLES = [("2015-16", "2015-07-16", "2016-12-31"),
          ("2017-18", "2017-01-01", "2018-12-31"),
          ("2019-21", "2019-01-01", "2021-12-31"),
          ("2022-24", "2022-01-01", "2024-12-31"),
          ("2025-26", "2025-01-01", "2026-12-31")]

# ---------------------------------------------------------------- (a) percentile di sth_mvrv 0,80 & 0,97
print("\n" + "-" * 104)
print("(a) PERSENTIL YANG BERKORESPONDENSI DENGAN sth_mvrv = 0,80 dan = 0,97, PER CYCLE")
print("    (hari dengan sth_mvrv dalam +-1,5% dari nilai target)")
print("-" * 104)
print(f"{'Cycle':<9} {'n hari':>7} | {'q @0,80 (med)':>14} {'IQR':>16} {'n':>5} | "
      f"{'q @0,97 (med)':>14} {'IQR':>16} {'n':>5}")
rows_a = []
for nm, s, e in CYCLES:
    sub = qv[(qv["date"] >= s) & (qv["date"] <= e)]
    if sub.empty:
        continue
    out = [nm, len(sub)]
    for tgt in (GATE_LO, GATE_HI):
        near = sub[(sub["sth_mvrv"] >= tgt * 0.985) & (sub["sth_mvrv"] <= tgt * 1.015)]
        if len(near) >= 5:
            med = near["q"].median()
            iqr = (near["q"].quantile(.25), near["q"].quantile(.75))
            out += [f"{med:.3f}", f"[{iqr[0]:.3f}-{iqr[1]:.3f}]", len(near)]
        else:
            out += ["-", "-", len(near)]
    print(f"{out[0]:<9} {out[1]:>7} | {out[2]:>14} {out[3]:>16} {out[4]:>5} | "
          f"{out[5]:>14} {out[6]:>16} {out[7]:>5}")
    rows_a.append(out)

# pooled
pool = {}
for tgt, key in ((GATE_LO, "lo"), (GATE_HI, "hi")):
    near = qv[(qv["sth_mvrv"] >= tgt * 0.985) & (qv["sth_mvrv"] <= tgt * 1.015)]
    pool[key] = near["q"].median()
    print(f"  POOLED q @ sth_mvrv={tgt:.2f} : median {near['q'].median():.3f} "
          f"(n={len(near)}, p10={near['q'].quantile(.10):.3f}, p90={near['q'].quantile(.90):.3f})")

spread_lo = [float(r[2]) for r in rows_a if r[2] != "-"]
spread_hi = [float(r[5]) for r in rows_a if r[5] != "-"]
if spread_lo:
    print(f"  Sebaran median q@0,80 antar cycle: {min(spread_lo):.3f} .. {max(spread_lo):.3f} "
          f"(rentang {max(spread_lo)-min(spread_lo):.3f})")
if spread_hi:
    print(f"  Sebaran median q@0,97 antar cycle: {min(spread_hi):.3f} .. {max(spread_hi):.3f} "
          f"(rentang {max(spread_hi)-min(spread_hi):.3f})")

sl2 = [float(r[2]) for r in rows_a if r[2] != "-" and r[0] != "2015-16"]
sh2 = [float(r[5]) for r in rows_a if r[5] != "-" and r[0] != "2015-16"]
print(f"  Tanpa cycle 2015-16 (z-history baru 365 hari, tidak stabil): "
      f"q@0,80 {min(sl2):.3f}..{max(sl2):.3f} (rentang {max(sl2)-min(sl2):.3f}), "
      f"q@0,97 {min(sh2):.3f}..{max(sh2):.3f} (rentang {max(sh2)-min(sh2):.3f})")

# ---------------------------------------------------------------- alarm bear CEPAT (Framework v2 sec 0)
d = df.copy()
d["aviv_upper"] = d["price_at_aviv_mean"] + 0.5 * (d["price_at_aviv_plus_1_sigma"] - d["price_at_aviv_mean"])
d["in_z5"] = (d["btc_price"] >= d["aviv_upper"]).fillna(False)

st, c = [], 0
for v in d["in_z5"]:
    c = c + 1 if v else 0
    st.append(c)
d["z5_streak"] = st

# sinyal 1: turun dari Z5 setelah >=7 hari di Z5
sig1 = np.zeros(len(d), bool)
for i in range(1, len(d)):
    if (not d["in_z5"].iloc[i]) and st[i - 1] >= 7:
        sig1[i] = True

# sinyal 2: gap MA90-MA60 STH-SOPR memuncak lalu turun >=14 hari
ma90 = d["sth_sopr"].rolling(90, min_periods=90).mean()
gap  = ma90 - ma90.rolling(60, min_periods=60).mean()
gv   = gap.values
sig2 = np.zeros(len(d), bool)
for i in range(1, len(d) - 14):
    if np.isnan(gv[i]) or gv[i] <= 0 or gv[i] <= gv[i - 1]:
        continue
    fut = gv[i + 1:i + 15]
    if len(fut) == 14 and np.all(fut < gv[i]):
        sig2[i + 14] = True

# sinyal 3: SMA30(MVRV) cross ke bawah SMA30-of-SMA30, bertahan >=7 hari
sma30 = d["mvrv_ratio"].rolling(30, min_periods=30).mean()
sma30b = sma30.rolling(30, min_periods=30).mean()
below3 = (sma30 < sma30b).fillna(False).values
sig3 = np.zeros(len(d), bool)
run = 0
for i in range(len(d)):
    run = run + 1 if below3[i] else 0
    if run == 7:
        sig3[i] = True

# sinyal 4: MVRV < SMA180 >=7 hari DAN kunjungan Z5 terakhir <=120 hari
sma180 = d["mvrv_ratio"].rolling(180, min_periods=180).mean()
below4 = (d["mvrv_ratio"] < sma180).fillna(False).values
last_z5 = np.full(len(d), 10 ** 6)
last = -10 ** 6
for i in range(len(d)):
    if d["in_z5"].iloc[i]:
        last = i
    last_z5[i] = i - last
sig4 = np.zeros(len(d), bool)
run = 0
for i in range(len(d)):
    run = run + 1 if below4[i] else 0
    if run >= 7 and last_z5[i] <= 120:
        sig4[i] = True

d["sig1"], d["sig2"], d["sig3"], d["sig4"] = sig1, sig2, sig3, sig4

# alarm ON: 2 dari 4 sinyal nyala dalam window pairing 90 hari.
# OFF (unlock): STH RP cross naik melewati RP.
above_rp = (d["sth_cost_basis"] > d["realized_price"]).astype(bool)
prev_rp  = above_rp.shift(1).fillna(False).astype(bool)
d["cross_up"] = above_rp & (~prev_rp)

alarm = np.zeros(len(d), bool)
on = False
recent = []   # (idx, sig_name)
for i in range(len(d)):
    fired = [s for s in ("sig1", "sig2", "sig3", "sig4") if d[s].iloc[i]]
    for f in fired:
        recent.append((i, f))
    recent = [(j, f) for j, f in recent if i - j <= 90]
    if not on and len({f for _, f in recent}) >= 2:
        on = True
    if on and d["cross_up"].iloc[i]:
        on = False
        recent = []
    alarm[i] = on
d["alarm_bear"] = alarm
print(f"\n  Alarm bear CEPAT (unlock LITERAL = STH RP cross naik RP): {int(alarm.sum())} hari dari {len(d)} ({alarm.mean()*100:.1f}%)")
print(f"    cross-up STH RP>RP hanya terjadi {int(d['cross_up'].sum())} kali sepanjang sejarah -> "
      f"sekali alarm nyala, dia nyaris tidak pernah mati. Ini keterbatasan implementasi literal,")
print("    dan sekaligus konsisten dengan catatan Framework v2 bahwa aturan unlock masih PENDING validasi.")

# versi TERBATAS: alarm hanya hidup <=365 hari sejak pairing terakhir (proxy episodik)
alarm2 = np.zeros(len(d), bool)
on2, last_pair, recent2 = False, -10**6, []
for i in range(len(d)):
    for s_ in ("sig1", "sig2", "sig3", "sig4"):
        if d[s_].iloc[i]:
            recent2.append((i, s_))
    recent2 = [(j, f) for j, f in recent2 if i - j <= 90]
    if len({f for _, f in recent2}) >= 2:
        on2, last_pair = True, i
    if on2 and (d["cross_up"].iloc[i] or i - last_pair > 365):
        on2, recent2 = False, []
    alarm2[i] = on2
d["alarm_bear_365"] = alarm2
print(f"  Alarm bear CEPAT versi TERBATAS (mati juga kalau >365 hari tanpa pairing baru): "
      f"{int(alarm2.sum())} hari ({alarm2.mean()*100:.1f}%)")

d = d.merge(qv[["date", "q"]], on="date", how="left", suffixes=("", "_dup"))
d["q"] = d["q_dup"] if "q_dup" in d.columns else d["q"]
d = d.drop(columns=[c for c in d.columns if c.endswith("_dup")])

# ---------------------------------------------------------------- (b) gate absolut vs gate percentile
v = d[d["q"].notna()].reset_index(drop=True)
v["gate_abs"] = (v["sth_mvrv"] >= GATE_LO) & (v["sth_mvrv"] <= GATE_HI)
Q_LO, Q_HI = round(pool["lo"], 2), round(pool["hi"], 2)
v["gate_q"] = (v["q"] >= Q_LO) & (v["q"] <= Q_HI)

print("\n" + "-" * 104)
print(f"(b) GATE VALUASI: absolut [{GATE_LO}-{GATE_HI}] vs percentile [{Q_LO}-{Q_HI}] "
      f"(kalibrasi POOLED dari (a), satu kali, tanpa grid search)")
print("-" * 104)
print(f"{'Cycle':<9} {'n hari':>7} {'abs':>6} {'q':>6} {'kedua':>6} {'hanya abs':>10} {'hanya q':>8} | "
      f"{'hanya q & alarm ON':>19} {'hanya q & alarm OFF':>20}")
tot = dict(abs=0, q=0, both=0, oa=0, oq=0, oq_alarm=0, oq_noalarm=0)
for nm, s, e in CYCLES:
    sub = v[(v["date"] >= s) & (v["date"] <= e)]
    if sub.empty:
        continue
    a, b = sub["gate_abs"], sub["gate_q"]
    both = int((a & b).sum()); oa = int((a & ~b).sum()); oq = int((~a & b).sum())
    oqa = int((~a & b & sub["alarm_bear_365"]).sum()); oqn = oq - oqa
    print(f"{nm:<9} {len(sub):>7} {int(a.sum()):>6} {int(b.sum()):>6} {both:>6} {oa:>10} {oq:>8} | "
          f"{oqa:>19} {oqn:>20}")
    tot["abs"] += int(a.sum()); tot["q"] += int(b.sum()); tot["both"] += both
    tot["oa"] += oa; tot["oq"] += oq; tot["oq_alarm"] += oqa; tot["oq_noalarm"] += oqn
print(f"{'TOTAL':<9} {len(v):>7} {tot['abs']:>6} {tot['q']:>6} {tot['both']:>6} {tot['oa']:>10} "
      f"{tot['oq']:>8} | {tot['oq_alarm']:>19} {tot['oq_noalarm']:>20}")

if tot["oq"]:
    print(f"\n  Dari {tot['oq']} hari tambahan yang HANYA dibuka gate percentile, "
          f"{tot['oq_alarm']} ({tot['oq_alarm']/tot['oq']*100:.1f}%) jatuh saat alarm bear CEPAT sudah bunyi "
          f"= FALSE OPEN.")
print(f"  Sebagai pembanding: dari {tot['abs']} hari gate absolut, "
      f"{int((v['gate_abs'] & v['alarm_bear_365']).sum())} "
      f"({int((v['gate_abs'] & v['alarm_bear_365']).sum())/max(tot['abs'],1)*100:.1f}%) jatuh saat alarm bear ON.")

# proxy hasil (karena alarm bear literal nyala 90% hari -> tidak diskriminatif):
# nilai hari-hari tambahan diukur lewat forward return 90 hari & max drawdown 90 hari
v["fwd90_"] = v["btc_price"].shift(-90) / v["btc_price"] - 1
fwd_min = v["btc_price"][::-1].rolling(90, min_periods=1).min()[::-1]
v["dd90"] = fwd_min.shift(-1) / v["btc_price"] - 1
print("\n  Karena alarm bear literal nyala 90,5% hari (tidak diskriminatif), nilai hari-hari")
print("  tambahan diukur pakai proxy HASIL: forward return 90 hari & max drawdown 90 hari.")
print(f"  {'Kelompok hari':<26} {'n':>5} {'med fwd90':>10} {'mean fwd90':>11} {'med maxDD90':>12} {'% fwd90<0':>10}")
grp = [("kedua gate nyala", v["gate_abs"] & v["gate_q"]),
       ("hanya gate absolut", v["gate_abs"] & ~v["gate_q"]),
       ("hanya gate percentile", ~v["gate_abs"] & v["gate_q"]),
       ("tidak ada gate", ~v["gate_abs"] & ~v["gate_q"])]
for nm_, m in grp:
    ss = v[m & v["fwd90_"].notna()]
    if len(ss) == 0:
        continue
    print(f"  {nm_:<26} {len(ss):>5} {ss['fwd90_'].median()*100:>9.1f}% {ss['fwd90_'].mean()*100:>10.1f}% "
          f"{ss['dd90'].median()*100:>11.1f}% {(ss['fwd90_']<0).mean()*100:>9.1f}%")
print("  (hari-hari overlapping -> sangat berkorelasi; angka indikatif, BUKAN uji signifikansi)")


# ---------------------------------------------------------------- (c) independensi
print("\n" + "-" * 104)
print("(c) INDEPENDENSI (Governance butir 1)")
print("-" * 104)
a = v["gate_abs"].astype(int); b = v["gate_q"].astype(int)
phi = np.corrcoef(a, b)[0, 1]
print(f"  |phi| (gate absolut vs gate percentile) = {abs(phi):.3f}")
print(f"  -> {'REPARAMETRISASI (bukan sinyal baru), |phi|>0,8' if abs(phi) > 0.8 else 'lolos ambang independensi |phi|<0,8 -- artinya dia sinyal LAIN, bukan versi lebih baik dari gate yang sama'}")
inter = int((a & b).sum()); union = int((a | b).sum())
print(f"  Jaccard overlap = {inter}/{union} = {inter/max(union,1)*100:.1f}%")

# uji inkremental sederhana: setelah gate absolut nyala, apakah gate percentile
# masih memisahkan forward return 90 hari?
v["fwd90"] = v["btc_price"].shift(-90) / v["btc_price"] - 1
g = v[v["gate_abs"] & v["fwd90"].notna()]
if len(g) > 30:
    g1 = g[g["gate_q"]]["fwd90"]; g0 = g[~g["gate_q"]]["fwd90"]
    print(f"\n  Uji inkremental (forward return 90 hari, HANYA di hari gate absolut nyala):")
    print(f"    gate_q juga nyala   : n={len(g1):>4}  median {g1.median()*100:>7.1f}%  "
          f"mean {g1.mean()*100:>7.1f}%")
    print(f"    gate_q TIDAK nyala  : n={len(g0):>4}  median {g0.median()*100:>7.1f}%  "
          f"mean {g0.mean()*100:>7.1f}%")
    print("    (hari-hari ini SANGAT berkorelasi -- overlapping window; angka = indikatif, bukan uji formal)")

print("\nSELESAI V3")
