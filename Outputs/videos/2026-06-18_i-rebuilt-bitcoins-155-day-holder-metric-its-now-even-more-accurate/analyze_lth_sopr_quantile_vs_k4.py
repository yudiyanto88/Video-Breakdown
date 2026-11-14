"""
V1 -- LTH-SOPR trailing-Z -> historical quantile, sebagai kandidat pengganti
threshold absolut lth_sopr < 0.50 di K4 kondisi 2.

KLAIM YANG DIUJI (Matt Crosby, video 2026-06-18, [09:25]-[09:58]):
  "LTH-SOPR diubah jadi trailing Z-score lalu dilihat historic quantile-nya
   -- menandai setiap bear market bottom, termasuk COVID dip, absolutely to
   perfection."

BATASAN BESAR (wajib disebut di findings):
  Dataset kita = base "std" + boundary LTH STATIS 155 hari (vendor ChartInspect
  /Glassnode). Kita TIDAK punya raw UTXO, jadi TIDAK bisa mereplikasi base "flt"
  (filtered) atau boundary dinamis 114 hari milik Matt. Yang diuji di sini =
  METODOLOGI-nya (trailing-Z -> expanding percentile) di atas data kita sendiri,
  BUKAN replikasi angka Matt.

ANTI-LOOKAHEAD (STANDAR VALIDASI butir 3):
  z(t)   = (lth_sopr(t) - mean_1460d(t)) / std_1460d(t), window trailing
           BERAKHIR di t-1 (shift(1) sebelum rolling)
  q(t)   = persentil z(t) terhadap z-history sampai t-1 SAJA (expanding),
           bukan full-history percentile (yang repainting)
  Versi full-history percentile TETAP dihitung, hanya untuk mengukur seberapa
  besar bias lookahead-nya (pertanyaan (e)).

OUTPUT: print ASCII saja (console Windows), + events_lth_sopr_quantile.csv
"""

import bisect
import warnings

import numpy as np
import pandas as pd

warnings.simplefilter("ignore")
pd.options.mode.chained_assignment = None

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = (r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos"
          r"\2026-06-18_i-rebuilt-bitcoins-155-day-holder-metric-its-now-even-more-accurate")

Z_WIN        = 1460   # trailing window Z-score (4 tahun) -- sama dgn paper Matt
MIN_Z_HIST   = 365    # minimal jumlah z-value sebelum percentile dianggap valid
BOTTOM_HALF  = 180    # window +-180 hari untuk definisi bear bottom
MERGE_DAYS   = 365    # merge kandidat bottom yang berjarak < 365 hari
MIN_DD       = 0.45   # drawdown minimal dari ATH berjalan supaya disebut bear bottom
Q_LOW        = 0.10
Q_HIGH       = 0.90
LTH_SOPR_ABS = 0.50
ASOPR_ABS    = 0.93
ASOPR_STREAK = 7
SEARCH_WIN   = 365    # window +-365d untuk cari trigger pertama di sekitar bottom
COOLDOWN     = 90     # cooldown antar episode sinyal (untuk hitung false alarm)


# ---------------------------------------------------------------- load
df = pd.read_csv(MASTER, parse_dates=["date"])
df = df[df["btc_price"].notna()].sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["lth_sopr", "asopr"]).reset_index(drop=True)

print("=" * 100)
print("V1  LTH-SOPR TRAILING-Z QUANTILE  vs  K4 KONDISI 2 (lth_sopr < 0.50)")
print("=" * 100)
print(f"Data: {df['date'].min().date()} s/d {df['date'].max().date()}  (n hari = {len(df)})")
print("Basis data: vendor std + boundary LTH STATIS 155 hari. BUKAN base flt / boundary 114d Matt.")


# ---------------------------------------------------------------- trailing Z
roll = df["lth_sopr"].shift(1).rolling(Z_WIN, min_periods=Z_WIN)
df["z_mean"] = roll.mean()
df["z_std"]  = roll.std()
df["z"]      = (df["lth_sopr"] - df["z_mean"]) / df["z_std"]

z_first = df.loc[df["z"].notna(), "date"].min()
print(f"\nZ-score valid pertama : {z_first.date()}  (butuh {Z_WIN} hari trailing penuh)")


# ---------------------------------------------------------------- expanding percentile (anti-lookahead)
z_vals = df["z"].values
q_exp  = np.full(len(df), np.nan)
hist   = []
for i in range(len(df)):
    zi = z_vals[i]
    if np.isnan(zi):
        continue
    if len(hist) >= MIN_Z_HIST:
        lo = bisect.bisect_left(hist, zi)
        hi = bisect.bisect_right(hist, zi)
        q_exp[i] = (lo + 0.5 * (hi - lo)) / len(hist)   # mid-rank
    bisect.insort(hist, zi)
df["q_exp"] = q_exp

# full-history percentile (REPAINTING -- hanya untuk uji bias lookahead)
mask = df["z"].notna()
zz   = np.sort(df.loc[mask, "z"].values)
df["q_full"] = np.nan
df.loc[mask, "q_full"] = [
    (bisect.bisect_left(zz.tolist(), v) + 0.5 * (bisect.bisect_right(zz.tolist(), v)
                                                 - bisect.bisect_left(zz.tolist(), v))) / len(zz)
    for v in df.loc[mask, "z"].values
]

q_first = df.loc[df["q_exp"].notna(), "date"].min()
print(f"Quantile expanding valid pertama : {q_first.date()}  "
      f"(warm-up {Z_WIN}d + {MIN_Z_HIST}d z-history)")


# ---------------------------------------------------------------- definisi bear bottom
# DEFINISI EVENT (eksplisit):
#   kandidat = hari yang close-nya = minimum close dalam window +-180 hari
#   merge    = kandidat berjarak < 365 hari digabung, ambil yang close-nya paling rendah
#   filter   = drawdown dari ATH berjalan (running max close) >= 45%
#   catatan  = bottom < 180 hari dari ujung data = "bottom-so-far", TIDAK FINAL
price = df["btc_price"].values
dates = df["date"].values
n     = len(df)

cand = []
for i in range(n):
    lo = max(0, i - BOTTOM_HALF)
    hi = min(n, i + BOTTOM_HALF + 1)
    if price[i] == price[lo:hi].min():
        cand.append(i)

merged = []
for i in cand:
    if merged and (df["date"].iloc[i] - df["date"].iloc[merged[-1]]).days < MERGE_DAYS:
        if price[i] < price[merged[-1]]:
            merged[-1] = i
    else:
        merged.append(i)

run_ath = df["btc_price"].cummax().values
bottoms = []
for i in merged:
    dd = 1 - price[i] / run_ath[i]
    if dd >= MIN_DD:
        bottoms.append((i, dd))

print("\n" + "-" * 100)
print("EVENT: BEAR BOTTOM (close terendah dalam +-180 hari, merge 365d, drawdown >= 45% dari ATH berjalan)")
print("-" * 100)
print(f"{'Tgl bottom':>12} {'Close':>12} {'DD dari ATH':>12}  {'Status':>18}  Q-expanding tersedia?")
btm_rows = []
last_date = df["date"].iloc[-1]
for i, dd in bottoms:
    d = df["date"].iloc[i]
    prov = "BOTTOM-SO-FAR" if (last_date - d).days < BOTTOM_HALF else "final"
    avail = "YA" if pd.notna(df["q_exp"].iloc[i]) else "TIDAK (warm-up)"
    print(f"{str(d.date()):>12} {price[i]:>12,.0f} {dd*100:>11.1f}%  {prov:>18}  {avail}")
    btm_rows.append(dict(idx=i, date=d, price=price[i], dd=dd, prov=prov, avail=avail))

testable = [b for b in btm_rows if b["avail"] == "YA"]
print(f"\nn bear bottom terdeteksi total = {len(btm_rows)}")
print(f"n bear bottom TESTABLE (quantile tersedia) = {len(testable)}  "
      f"-> {', '.join(str(b['date'].date()) for b in testable)}")


# ---------------------------------------------------------------- (a) timing per bottom
def first_trigger(cond, center_idx, win=SEARCH_WIN):
    """Hari pertama cond=True di dalam window +-win hari dari center. Return (idx, offset) atau (None, None)."""
    c   = df["date"].iloc[center_idx]
    sel = df[(df["date"] >= c - pd.Timedelta(days=win)) & (df["date"] <= c + pd.Timedelta(days=win))]
    hit = sel[cond.loc[sel.index]]
    if hit.empty:
        return None, None
    j = hit.index[0]
    return j, (df["date"].iloc[j] - c).days


cond_q     = df["q_exp"] < Q_LOW
cond_qfull = df["q_full"] < Q_LOW
cond_abs   = df["lth_sopr"] < LTH_SOPR_ABS

print("\n" + "-" * 100)
print("(a) TIMING SINYAL DI SEKITAR TIAP BEAR BOTTOM (window pencarian +-365 hari)")
print("    offset negatif = sinyal DULUAN sebelum bottom; positif = terlambat")
print("-" * 100)
print(f"{'Bottom':>12} | {'Q_exp<0.10 tgl':>14} {'off':>6} | {'lth_sopr<0.50 tgl':>17} {'off':>6} | "
      f"{'Q_full<0.10 tgl':>15} {'off':>6} | {'min Q +-180d':>12}")

ev_rows = []
for b in btm_rows:
    i = b["idx"]
    jq,  oq  = first_trigger(cond_q,     i)
    ja,  oa  = first_trigger(cond_abs,   i)
    jf,  of_ = first_trigger(cond_qfull, i)
    lo = max(0, i - BOTTOM_HALF); hi = min(n, i + BOTTOM_HALF + 1)
    minq = df["q_exp"].iloc[lo:hi].min()
    fmt = lambda j, o: (str(df['date'].iloc[j].date()), f"{o:+d}") if j is not None else ("-", "-")
    a1, a2 = fmt(jq, oq); b1, b2 = fmt(ja, oa); c1, c2 = fmt(jf, of_)
    print(f"{str(b['date'].date()):>12} | {a1:>14} {a2:>6} | {b1:>17} {b2:>6} | {c1:>15} {c2:>6} | "
          f"{(f'{minq:.3f}' if pd.notna(minq) else '-'):>12}")
    ev_rows.append(dict(
        bottom_date=b["date"].date(), bottom_price=round(b["price"], 2),
        drawdown_pct=round(b["dd"] * 100, 1), status=b["prov"],
        q_exp_first_date=a1, q_exp_offset_days=a2,
        lth_sopr_abs_first_date=b1, lth_sopr_abs_offset_days=b2,
        q_full_first_date=c1, q_full_offset_days=c2,
        min_q_exp_pm180=(round(minq, 4) if pd.notna(minq) else None),
    ))


# ---------------------------------------------------------------- (b) selektivitas
valid = df[df["q_exp"].notna()].copy()   # periode adil untuk kedua sinyal
print("\n" + "-" * 100)
print(f"(b) SELEKTIVITAS -- periode adil {valid['date'].min().date()} s/d {valid['date'].max().date()} "
      f"(n={len(valid)} hari)")
print("-" * 100)


def episodes(sub, colcond):
    """Blok kontigu sinyal, digabung kalau jeda antar blok <= COOLDOWN hari."""
    on = sub[colcond].copy()
    if on.empty:
        return []
    eps, start, prev = [], on["date"].iloc[0], on["date"].iloc[0]
    for d in on["date"].iloc[1:]:
        if (d - prev).days > COOLDOWN:
            eps.append((start, prev)); start = d
        prev = d
    eps.append((start, prev))
    return eps


for name, cond in [("Q_exp < 0.10", valid["q_exp"] < Q_LOW),
                   ("lth_sopr < 0.50", valid["lth_sopr"] < LTH_SOPR_ABS),
                   ("Q_full < 0.10 (repainting)", valid["q_full"] < Q_LOW)]:
    days = int(cond.sum())
    eps  = episodes(valid, cond)
    hit  = 0
    for b in testable:
        c = b["date"]
        near = valid[(valid["date"] >= c - pd.Timedelta(days=BOTTOM_HALF)) &
                     (valid["date"] <= c + pd.Timedelta(days=BOTTOM_HALF))]
        if cond.loc[near.index].any():
            hit += 1
    fa = 0
    for s, e in eps:
        if not any(abs((s - b["date"]).days) <= SEARCH_WIN or abs((e - b["date"]).days) <= SEARCH_WIN
                   for b in testable):
            fa += 1
    print(f"  {name:<28} : {days:>4} hari ({days/len(valid)*100:4.1f}%) | "
          f"{len(eps):>2} episode | hit {hit}/{len(testable)} bottom | "
          f"episode di luar +-365d bottom = {fa}")
    for s, e in eps:
        tag = "" if any(abs((s - b['date']).days) <= SEARCH_WIN or abs((e - b['date']).days) <= SEARCH_WIN
                        for b in testable) else "  <-- FALSE ALARM"
        print(f"       episode {s.date()} .. {e.date()} ({(e-s).days+1}d){tag}")


print("\nCATATAN definisi event: 2021-07-20 lolos filter drawdown 45% tapi itu CRASH MID-CYCLE")
print("  (Mei-Jul 2021), bukan bear bottom siklus. Angka hit-rate di atas dilaporkan APA ADANYA;")
print("  tanpa event mid-cycle itu: Q_exp<0.10 = 4/4 bottom, lth_sopr<0.50 = 2/4 bottom.")


# ---------------------------------------------------------------- (c) dampak ke K4
# Zona Z1 (Decision Framework v2, Dimensi 1 + 2): struktur T (sth RP < RP) DAN P < STH RP
df["struct_T"] = df["sth_cost_basis"] < df["realized_price"]
df["Z1"]       = df["struct_T"] & (df["btc_price"] < df["sth_cost_basis"])

# aSOPR < 0.93 selama >= 7 hari berturut
below = (df["asopr"] < ASOPR_ABS).values
st, cur = [], 0
for v in below:
    cur = cur + 1 if v else 0
    st.append(cur)
df["asopr_streak"] = st
df["asopr_cond"]   = df["asopr_streak"] >= ASOPR_STREAK

df["k4_c1"] = df["lth_mvrv"] < 1.0
df["k4_c2_abs"] = df["asopr_cond"] & (df["lth_sopr"] < LTH_SOPR_ABS)
df["k4_c2_q"]   = df["asopr_cond"] & (df["q_exp"] < Q_LOW)
df["k4_c3"] = (df["percent_btc_in_profit"] < 50) & (df["pct_sth_in_profit"] < 10)
df["k4_c4"] = (df["btc_price"] / df["cvdd"]) < 1.10

df["k4_abs"] = df[["k4_c1", "k4_c2_abs", "k4_c3", "k4_c4"]].sum(axis=1)
df["k4_q"]   = df[["k4_c1", "k4_c2_q",   "k4_c3", "k4_c4"]].sum(axis=1)

BEARS = [("Bear 2018-19", "2018-01-01", "2019-06-30"),
         ("COVID 2020",   "2020-01-01", "2020-06-30"),
         ("Bear 2022-23", "2022-01-01", "2023-06-30"),
         ("Bear 2025-26", "2025-11-01", "2026-07-15")]

print("\n" + "-" * 100)
print("(c) DAMPAK KE K4 KONDISI 2 : aSOPR<0.93 >=7d DAN [lth_sopr<0.50]  vs  [Q_exp<0.10]")
print("    (count K4 hanya dihitung di hari Z1 aktif -- jalur utama K4)")
print("-" * 100)
print(f"{'Bear':<14} {'hari Z1':>8} {'c2 abs':>7} {'c2 q':>6} | {'DCA-hari abs (>=2)':>19} {'DCA-hari q':>11} | "
      f"{'max count abs':>13} {'max count q':>11}")
k4_rows = []
for name, s, e in BEARS:
    sub = df[(df["date"] >= s) & (df["date"] <= e)]
    z1  = sub[sub["Z1"]]
    if z1.empty:
        print(f"{name:<14} {0:>8} {'-':>7} {'-':>6} | {'-':>19} {'-':>11} | {'-':>13} {'-':>11}   (Z1 tidak pernah terbentuk)")
        k4_rows.append(dict(bear=name, z1_days=0))
        continue
    c2a, c2q = int(z1["k4_c2_abs"].sum()), int(z1["k4_c2_q"].sum())
    da, dq   = int((z1["k4_abs"] >= 2).sum()), int((z1["k4_q"] >= 2).sum())
    print(f"{name:<14} {len(z1):>8} {c2a:>7} {c2q:>6} | {da:>19} {dq:>11} | "
          f"{int(z1['k4_abs'].max()):>13} {int(z1['k4_q'].max()):>11}")
    k4_rows.append(dict(bear=name, z1_days=len(z1), c2_abs_days=c2a, c2_q_days=c2q,
                        dca_days_abs=da, dca_days_q=dq,
                        max_count_abs=int(z1["k4_abs"].max()), max_count_q=int(z1["k4_q"].max())))

print("\n  Distribusi tier count K4 di hari Z1 (abs -> q), per bear:")
for name, s, e in BEARS:
    z1 = df[(df["date"] >= s) & (df["date"] <= e) & df["Z1"]]
    if z1.empty:
        continue
    ta = z1["k4_abs"].value_counts().sort_index().to_dict()
    tq = z1["k4_q"].value_counts().sort_index().to_dict()
    print(f"   {name:<14} abs={ta}   q={tq}")


# ---- (c-diag) kenapa kondisi 2 nyaris tidak pernah nyala? bedah komponennya
print("\nDiagnostik kondisi 2 -- per window bear PENUH (bukan cuma hari Z1):")
print(f"  {'Bear':<14} {'hari':>5} {'aSOPR<0.93 >=7d':>16} {'lth_sopr<0.50':>14} {'Q_exp<0.10':>11} "
      f"{'c2 abs':>7} {'c2 q':>6}")
for name, s_, e_ in BEARS:
    sub = df[(df["date"] >= s_) & (df["date"] <= e_)]
    print(f"  {name:<14} {len(sub):>5} {int(sub['asopr_cond'].sum()):>16} "
          f"{int((sub['lth_sopr'] < LTH_SOPR_ABS).sum()):>14} {int((sub['q_exp'] < Q_LOW).sum()):>11} "
          f"{int(sub['k4_c2_abs'].sum()):>7} {int(sub['k4_c2_q'].sum()):>6}")

print("\n  TEMUAN SAMPINGAN -- syarat aSOPR<0.93 selama >=7 hari berturut:")
print(f"    streak aSOPR<0.93 TERPANJANG sepanjang sejarah = {int(df['asopr_streak'].max())} hari "
      f"(tgl {df.loc[df['asopr_streak'].idxmax(), 'date'].date()})")
print(f"    total hari asopr<0.93 = {int((df['asopr'] < ASOPR_ABS).sum())}; "
      f"total hari streak>=7 = {int(df['asopr_cond'].sum())}")
print("    -> kondisi 2 K4 (leg aSOPR) TIDAK PERNAH nyala di data kita, apapun leg LTH-SOPR-nya.")


# ---- (c-jalur2) K4-tanpa-Z1: count >= 3 (tanpa syarat Z1), abs vs quantile
print("\nJalur K4-tanpa-Z1 (count >= 3 tanpa syarat Z1) -- window bear penuh:")
print(f"  {'Bear':<14} {'count>=3 abs':>13} {'count>=3 q':>11} {'count>=2 abs':>13} {'count>=2 q':>11}")
for name, s_, e_ in BEARS:
    sub = df[(df["date"] >= s_) & (df["date"] <= e_)]
    print(f"  {name:<14} {int((sub['k4_abs'] >= 3).sum()):>13} {int((sub['k4_q'] >= 3).sum()):>11} "
          f"{int((sub['k4_abs'] >= 2).sum()):>13} {int((sub['k4_q'] >= 2).sum()):>11}")


# ---------------------------------------------------------------- (d) klaim #18 -- quantile > 0.90 di 2025
print("\n" + "-" * 100)
print("(d) KLAIM #18 : Q_exp > 0.90 di 2025 -- dekat peak Jul 2025 atau peak Okt 2025?")
print("-" * 100)
y25 = df[(df["date"] >= "2025-01-01") & (df["date"] <= "2025-12-31")]
hi  = y25[y25["q_exp"] > Q_HIGH]
if hi.empty:
    print("  TIDAK ADA hari dengan Q_exp > 0.90 sepanjang 2025.")
else:
    print(f"  Hari Q_exp>0.90 di 2025: n={len(hi)}, pertama {hi['date'].iloc[0].date()}, "
          f"terakhir {hi['date'].iloc[-1].date()}")
    for s, e in episodes(y25, y25["q_exp"] > Q_HIGH):
        print(f"    episode {s.date()} .. {e.date()} ({(e-s).days+1}d)")

print("\nSemua episode Q_exp > 0.90 sepanjang sejarah (cooldown 90d):")
for s_, e_ in episodes(df[df["q_exp"].notna()], df.loc[df["q_exp"].notna(), "q_exp"] > Q_HIGH):
    seg = df[(df["date"] >= s_) & (df["date"] <= e_)]
    print(f"    {s_.date()} .. {e_.date()} ({(e_-s_).days+1}d)  harga {seg['btc_price'].iloc[0]:,.0f} -> "
          f"{seg['btc_price'].iloc[-1]:,.0f}  (max harga di episode {seg['btc_price'].max():,.0f})")

peak_jul = y25[(y25["date"] >= "2025-06-01") & (y25["date"] <= "2025-08-31")].nlargest(1, "btc_price")
peak_oct = y25[(y25["date"] >= "2025-09-15") & (y25["date"] <= "2025-11-15")].nlargest(1, "btc_price")
print(f"  Peak lokal Jul-Aug 2025 : {peak_jul['date'].iloc[0].date()}  ${peak_jul['btc_price'].iloc[0]:,.0f}")
print(f"  Peak lokal Okt 2025     : {peak_oct['date'].iloc[0].date()}  ${peak_oct['btc_price'].iloc[0]:,.0f}")
print(f"  Q_exp max Jun-Aug 2025  : {y25[(y25['date']>='2025-06-01')&(y25['date']<='2025-08-31')]['q_exp'].max():.3f}")
print(f"  Q_exp max Sep-Nov 2025  : {y25[(y25['date']>='2025-09-01')&(y25['date']<='2025-11-30')]['q_exp'].max():.3f}")

# K1 trigger aktual di data kita: cross-down AVIV Upper (+0.5SD) setelah >=14 hari di Z5
df["aviv_upper"] = df["price_at_aviv_mean"] + 0.5 * (df["price_at_aviv_plus_1_sigma"] - df["price_at_aviv_mean"])
df["in_z5"] = df["btc_price"] >= df["aviv_upper"]
st, cur = [], 0
for v in df["in_z5"].fillna(False):
    cur = cur + 1 if v else 0
    st.append(cur)
df["z5_streak"] = st
k1_trig = []
for i in range(1, len(df)):
    if (not df["in_z5"].iloc[i]) and df["z5_streak"].iloc[i-1] >= 14:
        k1_trig.append(df["date"].iloc[i])
k1_2025 = [d for d in k1_trig if pd.Timestamp("2025-01-01") <= d <= pd.Timestamp("2026-03-31")]
print(f"  K1 trigger (turun Z5->Z4 setelah >=14d di Z5) di 2025-Q1'26: "
      f"{[str(d.date()) for d in k1_2025] if k1_2025 else 'tidak ada'}")
if not hi.empty and k1_2025:
    print(f"  Jarak Q_exp>0.90 pertama ({hi['date'].iloc[0].date()}) ke K1 trigger pertama "
          f"({k1_2025[0].date()}) = {(k1_2025[0]-hi['date'].iloc[0]).days:+d} hari")


# ---------------------------------------------------------------- (e) besar bias lookahead
print("\n" + "-" * 100)
print("(e) UJI LOOKAHEAD BIAS : expanding percentile vs full-history percentile")
print("-" * 100)
v = df[df["q_exp"].notna()]
diff = (v["q_full"] - v["q_exp"]).abs()
print(f"  n hari dibandingkan       : {len(v)}")
print(f"  |q_full - q_exp| mean     : {diff.mean():.4f}   median: {diff.median():.4f}   max: {diff.max():.4f}")
print(f"  korelasi Spearman         : {v['q_exp'].corr(v['q_full'], method='spearman'):.4f}")
both_lo = ((v["q_exp"] < Q_LOW) & (v["q_full"] < Q_LOW)).sum()
only_e  = ((v["q_exp"] < Q_LOW) & ~(v["q_full"] < Q_LOW)).sum()
only_f  = (~(v["q_exp"] < Q_LOW) & (v["q_full"] < Q_LOW)).sum()
print(f"  hari <0.10 : dua-duanya={both_lo}, hanya expanding={only_e}, hanya full-history={only_f}")
if (both_lo + only_e + only_f) > 0:
    print(f"  disagreement rate di zona <0.10 = "
          f"{(only_e+only_f)/(both_lo+only_e+only_f)*100:.1f}% dari hari yang salah satu nyala")

# phi antara sinyal absolut dan sinyal quantile (Governance butir 1)
a = (v["lth_sopr"] < LTH_SOPR_ABS).astype(int)
q = (v["q_exp"] < Q_LOW).astype(int)
phi = np.corrcoef(a, q)[0, 1]
print(f"\n  |phi| (lth_sopr<0.50  vs  Q_exp<0.10) = {abs(phi):.3f}  "
      f"-> {'reparametrisasi (bukan sinyal baru)' if abs(phi) > 0.8 else 'independen secukupnya (sinyal berbeda)'}")


# ---- (f) stabilitas seri quantile (whipsaw)
print("\n" + "-" * 100)
print("(f) STABILITAS SERI QUANTILE -- seberapa sering seri bolak-balik ekstrem?")
print("-" * 100)
vv = df[df["q_exp"].notna()].reset_index(drop=True)
a_lo = (vv["q_exp"] < Q_LOW).values
a_hi = (vv["q_exp"] > Q_HIGH).values
both = sum(1 for i in range(len(vv) - 30) if a_lo[i:i+30].any() and a_hi[i:i+30].any())
print(f"  jendela 30 hari yang memuat q<0.10 DAN q>0.90 sekaligus: {both} dari {len(vv)-30} "
      f"({both/(len(vv)-30)*100:.1f}%)")
print("  min/max/mean q_exp per bulan, 2026:")
m26 = vv[vv["date"] >= "2026-01-01"].set_index("date")["q_exp"].resample("ME").agg(["min", "max", "mean"]).round(3)
for idx, r in m26.iterrows():
    print(f"    {idx.date()}  min={r['min']:.3f}  max={r['max']:.3f}  mean={r['mean']:.3f}")


# ---------------------------------------------------------------- simpan CSV
ev = pd.DataFrame(ev_rows)
ev.to_csv(rf"{OUTDIR}\events_lth_sopr_quantile.csv", index=False)
print(f"\nCSV event disimpan: events_lth_sopr_quantile.csv  ({len(ev)} baris)")
print("SELESAI V1")
