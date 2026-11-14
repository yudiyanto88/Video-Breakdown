"""
INSIGHT A -- Frekuensi/durasi visit Z5 (price >= AVIV Upper) menurun menjelang cycle top?
Proxy untuk klaim Alphractal SMB: "harga makin jarang mengunjungi zona resistance struktural".

DEFINISI EVENT (eksplisit):
- AVIV Upper = +0.5 SD, formula established (pola research/analyze_k3_stage_comparison.py):
    HIST_MEAN/HIST_STD dari aviv_ratio full-history, true_mkt_mean = price/aviv_ratio,
    aviv_upper = (HIST_MEAN + 0.5*HIST_STD) * true_mkt_mean
  CATATAN LOOKAHEAD: mean/std pakai full history (termasuk masa depan) -- sama dengan
  cara framework/ChartInspect menampilkan band. Dicatat sebagai caveat.
- Episode Z5 = run hari berturut-turut close >= AVIV Upper.
  MERGE RULE: dua run yang dipisah <= 7 hari di bawah band digabung jadi satu episode.
- Episode dianggap "selesai" (at-gate) 7 hari setelah hari terakhir di Z5 (konfirmasi merge window).

K1 SYARAT AWAL (pembanding timing):
- ATH day = close > running max sebelumnya. Cluster ATH = ATH days dipisah <= 30 hari.
- Per cluster: peak day (harga max), MVRV di peak day, aSOPR MA7 di peak day.
- Syarat awal aktif (per cycle): cluster ke-k punya MVRV peak < MVRV peak cluster k-1
  DAN aSOPR-MA7 peak < cluster k-1. Detection date at-gate = ATH day PERTAMA di cluster k
  di mana MVRV hari itu < max MVRV cluster k-1 dan aSOPR-MA7 hari itu < max cluster k-1.
"""
import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-07-08_this-new-bitcoin-chart-shows-market-exhaustion"

MERGE_GAP_DAYS  = 7
ATH_CLUSTER_GAP = 30

df = pd.read_csv(MASTER, parse_dates=["date"],
                 usecols=["date", "btc_price", "aviv_ratio", "mvrv_ratio", "asopr"])
df = df.sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "aviv_ratio"])
df = df[df["btc_price"] > 1].reset_index(drop=True)

# --- AVIV Upper (formula established, ikuti analyze_k3_stage_comparison.py) ---
HIST_MEAN = df["aviv_ratio"].mean()
HIST_STD  = df["aviv_ratio"].std()
df["true_mkt_mean"] = df["btc_price"] / df["aviv_ratio"]
df["aviv_upper"]    = (HIST_MEAN + 0.5 * HIST_STD) * df["true_mkt_mean"]
df["in_z5"]         = df["btc_price"] >= df["aviv_upper"]
print(f"Data: {df['date'].min().date()} s/d {df['date'].max().date()}  (n={len(df)})")
print(f"HIST_MEAN={HIST_MEAN:.4f}  HIST_STD={HIST_STD:.4f}")

# --- Runs Z5 ---
runs = []
start = None
for i in range(len(df)):
    if df.at[i, "in_z5"] and start is None:
        start = i
    elif not df.at[i, "in_z5"] and start is not None:
        runs.append((start, i - 1))
        start = None
if start is not None:
    runs.append((start, len(df) - 1))

# --- Merge runs dgn gap <= MERGE_GAP_DAYS ---
episodes = []
for r in runs:
    if episodes:
        prev = episodes[-1]
        gap = (df.at[r[0], "date"] - df.at[prev[1], "date"]).days - 1
        if gap <= MERGE_GAP_DAYS:
            episodes[-1] = (prev[0], r[1])
            continue
    episodes.append(r)

ep_rows = []
for k, (a, b) in enumerate(episodes):
    d0, d1 = df.at[a, "date"], df.at[b, "date"]
    seg = df.iloc[a:b + 1]
    maxp_i = seg["btc_price"].idxmax()
    ep_rows.append({
        "ep_start": d0.date(), "ep_end": d1.date(),
        "duration_d": (d1 - d0).days + 1,
        "days_in_z5": int(seg["in_z5"].sum()),
        "max_price": seg["btc_price"].max(),
        "max_price_date": df.at[maxp_i, "date"].date(),
    })
ep = pd.DataFrame(ep_rows)

# --- Assign ke bull cycle ---
cycles = [
    ("2012-13 (context)", "2012-01-01", "2014-06-01"),
    ("2016-17",           "2015-06-01", "2018-06-01"),
    ("2019 mini (context)","2019-01-01", "2019-12-31"),
    ("2020-21",           "2020-01-01", "2022-06-01"),
    ("2023-25",           "2023-01-01", "2026-12-31"),
]
def cyc(d):
    for name, a, b in cycles:
        if pd.Timestamp(a) <= pd.Timestamp(d) <= pd.Timestamp(b):
            return name
    return "other"
ep["cycle"] = ep["ep_start"].apply(cyc)

# gap ke episode sebelumnya dalam cycle yang sama
ep["gap_prev_d"] = np.nan
for c in ep["cycle"].unique():
    idxs = ep.index[ep["cycle"] == c].tolist()
    for j in range(1, len(idxs)):
        ep.at[idxs[j], "gap_prev_d"] = (pd.Timestamp(ep.at[idxs[j], "ep_start"]) -
                                        pd.Timestamp(ep.at[idxs[j - 1], "ep_end"])).days

ep.to_csv(f"{OUTDIR}\\_z5_episodes.csv", index=False)

print("\n" + "=" * 100)
print("EPISODE Z5 (price >= AVIV Upper), merge gap <= 7d")
print("=" * 100)
for c in [x[0] for x in cycles] + ["other"]:
    sub = ep[ep["cycle"] == c]
    if sub.empty:
        continue
    # cycle top = max price di window cycle
    a, b = None, None
    for name, x, y in cycles:
        if name == c:
            a, b = pd.Timestamp(x), pd.Timestamp(y)
    if a is not None:
        w = df[(df["date"] >= a) & (df["date"] <= min(b, df["date"].max()))]
        top_i = w["btc_price"].idxmax()
        top_d, top_p = df.at[top_i, "date"], df.at[top_i, "btc_price"]
    print(f"\n--- CYCLE {c}  (top: {top_d.date()} @ ${top_p:,.0f})  n_episode={len(sub)} ---")
    print(f"{'#':>2} {'start':>12} {'end':>12} {'dur(d)':>7} {'gap_prev(d)':>12} {'max_price':>12} {'max_date':>12}")
    for j, (_, r) in enumerate(sub.iterrows(), 1):
        gp = f"{r['gap_prev_d']:.0f}" if pd.notna(r['gap_prev_d']) else "-"
        print(f"{j:>2} {str(r['ep_start']):>12} {str(r['ep_end']):>12} {r['duration_d']:>7} "
              f"{gp:>12} {r['max_price']:>12,.0f} {str(r['max_price_date']):>12}")
    durs = sub["duration_d"].tolist()
    mono = all(durs[i] > durs[i + 1] for i in range(len(durs) - 1)) if len(durs) > 1 else None
    # episode yang memuat cycle top
    top_ep = None
    for j, (_, r) in enumerate(sub.iterrows(), 1):
        if pd.Timestamp(r["ep_start"]) <= top_d <= pd.Timestamp(r["ep_end"]) + pd.Timedelta(days=MERGE_GAP_DAYS):
            top_ep = j
    print(f"    durasi monotonic menurun? {mono} | urutan durasi: {durs}")
    print(f"    cycle top jatuh di episode ke: {top_ep} dari {len(sub)}")
    # deteksi at-gate: episode pertama yang durasinya < episode sebelumnya
    det = None
    for j in range(1, len(durs)):
        if durs[j] < durs[j - 1]:
            det_end = pd.Timestamp(sub.iloc[j]["ep_end"])
            det = (j + 1, det_end + pd.Timedelta(days=MERGE_GAP_DAYS))
            break
    if det:
        lead = (top_d - det[1]).days
        print(f"    deteksi 'durasi menurun' (at-gate, end ep#{det[0]} +7d konfirmasi): "
              f"{det[1].date()}  -> lead ke top: {lead}d")

# =============================================================
# K1 SYARAT AWAL: MVRV & aSOPR diminishing per ATH cluster
# =============================================================
df["asopr_ma7"] = df["asopr"].rolling(7, min_periods=7).mean()
df["run_max"]   = df["btc_price"].cummax()
df["new_ath"]   = df["btc_price"] > df["run_max"].shift(1)

ath_days = df.index[df["new_ath"]].tolist()
clusters = []
cur = [ath_days[0]] if ath_days else []
for i in ath_days[1:]:
    if (df.at[i, "date"] - df.at[cur[-1], "date"]).days <= ATH_CLUSTER_GAP:
        cur.append(i)
    else:
        clusters.append(cur)
        cur = [i]
if cur:
    clusters.append(cur)

cl_rows = []
for cl in clusters:
    seg = df.loc[cl]
    pk = seg["btc_price"].idxmax()
    cl_rows.append({
        "start": df.at[cl[0], "date"], "end": df.at[cl[-1], "date"],
        "peak_date": df.at[pk, "date"], "peak_price": df.at[pk, "btc_price"],
        "mvrv_max": seg["mvrv_ratio"].max(), "asopr7_max": seg["asopr_ma7"].max(),
        "idxs": cl,
    })

print("\n" + "=" * 100)
print("K1 SYARAT AWAL -- ATH clusters (gap<=30d) dan deteksi diminishing MVRV & aSOPR-MA7")
print("=" * 100)
for name, a, b in cycles:
    a, b = pd.Timestamp(a), pd.Timestamp(b)
    cyc_cl = [c for c in cl_rows if a <= c["peak_date"] <= b]
    if len(cyc_cl) < 2:
        continue
    print(f"\n--- CYCLE {name} ---")
    print(f"{'#':>2} {'peak_date':>12} {'peak_price':>12} {'MVRV_max':>9} {'aSOPR7_max':>11}")
    for j, c in enumerate(cyc_cl, 1):
        print(f"{j:>2} {str(c['peak_date'].date()):>12} {c['peak_price']:>12,.0f} "
              f"{c['mvrv_max']:>9.3f} {c['asopr7_max']:>11.4f}")
    det_date = None
    for j in range(1, len(cyc_cl)):
        prev = cyc_cl[j - 1]
        for i in cyc_cl[j]["idxs"]:
            if (df.at[i, "mvrv_ratio"] < prev["mvrv_max"] and
                    pd.notna(df.at[i, "asopr_ma7"]) and df.at[i, "asopr_ma7"] < prev["asopr7_max"]):
                det_date = df.at[i, "date"]
                break
        if det_date is not None:
            # cek apakah bertahan sampai peak cluster
            hold = (cyc_cl[j]["mvrv_max"] < prev["mvrv_max"] and
                    cyc_cl[j]["asopr7_max"] < prev["asopr7_max"])
            print(f"    DETEKSI syarat awal K1 (at-gate): {det_date.date()} "
                  f"(cluster #{j+1}; bertahan sampai peak cluster? {hold})")
            break
