"""
Validasi 1: 200-week MA sebagai cyclical floor / multi-year accumulation zone.

Klaim video (On-Chain Mind, 2026-08-11):
  - 200-week MA saat ini ~$63,800
  - 200-week MA compounding ~30%/tahun konsisten 4 tahun terakhir
  - "Setiap episode historis harga <=200-week MA selalu jadi multi-year
    accumulation zone" (floor yang bertahan)

CATATAN DATA: data_master_all_metrics.csv terakhir update 2026-07-15 (semua
file data_*.csv di Onchain-Dashboard mentok di tanggal yang sama). Video
tanggal 2026-08-11 -- ada gap ~27 hari yang TIDAK bisa diisi. Semua angka
"current" di validasi ini memakai 2026-07-15 sebagai proxy tanggal terakhir
yang tersedia, bukan tanggal video persis. Ini dicatat eksplisit di findings.

Definisi event (house rigor - wajib eksplisit sebelum hitung):
  1. Kolom `200_wma` di master = rolling(1400 hari kalender, min_periods=1)
     dari btc_price -- verified by reconstruction. Ini BUKAN true 200-week MA
     sebelum 1400 hari data terkumpul (early data = expanding mean, bukan
     rolling mature). Makanya analisis dibatasi mulai tanggal data price
     matang: 2010-07-17 (mulai price data) + 1400 hari kalender.
  2. Event "price below 200wma": raw run = hari-hari berturut-turut close
     btc_price < 200_wma.
  3. Raw run dengan panjang < MIN_RUN_DAYS (5 hari) dibuang sebagai noise
     (whipsaw satu-dua hari, bukan episode).
  4. Dua raw run (masing2 >=5 hari) digabung jadi SATU episode kalau gap
     (hari2 di antaranya di atas 200wma) < MERGE_GAP_DAYS (14 hari).
  5. Episode final: start = hari pertama run pertama dlm grup gabungan,
     end = hari terakhir run terakhir dlm grup gabungan.
  6. "Floor holds" test (H b): dalam 180 hari SETELAH episode berakhir,
     apakah harga pernah breach > 10% di bawah titik terendah episode?
     Kalau data forward < 180 hari (episode terlalu dekat ke ujung data),
     ditandai INCOMPLETE -- tidak dihitung pass/fail (anti lookahead-bias
     sekaligus anti cherry-pick data belum lengkap).

Zone classification: replikasi persis Decision Framework v2 Section 1
(N/C/T struktur x posisi harga -> ZC/ZD/Z3/Z4/Z5/Z1/Z1b/Z2-transisi/Z2/Z4).
AVIV Upper = price_at_aviv_mean + 0.5*(price_at_aviv_plus_1_sigma - price_at_aviv_mean)
per catatan data_dictionary.md / pola analyze_k3_stage_comparison.py.
"""

import pandas as pd
import numpy as np

MIN_RUN_DAYS    = 5    # raw run minimum length to count as candidate episode
MERGE_GAP_DAYS  = 14   # merge two raw runs if gap between them < this
FLOOR_WINDOW    = 180  # forward days to test "floor holds"
BREACH_PCT      = 0.10 # >10% below episode low = floor breached

pd.set_option("display.width", 140)

# ─── Load ────────────────────────────────────────────────────────────────
df = pd.read_csv(
    r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv",
    parse_dates=["date"],
)
df = df.sort_values("date").reset_index(drop=True)

LATEST_DATE = df["date"].max()
print(f"Data terakhir tersedia: {LATEST_DATE.date()}  (video: 2026-08-11, gap ~{(pd.Timestamp('2026-08-11')-LATEST_DATE).days} hari)")

price_start = df["date"].min()
mature_start = price_start + pd.Timedelta(days=1400)
print(f"Price data mulai: {price_start.date()}  |  200_wma matang (rolling 1400d penuh) mulai: {mature_start.date()}")

dfm = df[df["date"] >= mature_start].reset_index(drop=True)
dfm = dfm.dropna(subset=["btc_price", "200_wma"]).reset_index(drop=True)
print(f"n hari dianalisis (200_wma matang): {len(dfm)}  ({dfm['date'].min().date()} s/d {dfm['date'].max().date()})")

# ─── AVIV Upper (formula framework) ─────────────────────────────────────
dfm["aviv_upper"] = dfm["price_at_aviv_mean"] + 0.5 * (
    dfm["price_at_aviv_plus_1_sigma"] - dfm["price_at_aviv_mean"]
)

def classify_zone(row):
    p   = row["btc_price"]
    sth = row["sth_cost_basis"]
    rp  = row["realized_price"]
    lth = row["lth_cost_basis"]
    avm = row["price_at_aviv_mean"]
    avu = row["aviv_upper"]
    if any(pd.isna(x) for x in [p, sth, rp, lth, avm, avu]):
        return "NA"

    dist_sth_rp = abs(sth - rp) / rp if rp != 0 else np.nan
    dist_rp_lth = abs(rp - lth) / lth if lth != 0 else np.nan

    if sth > rp:
        struct = "N"
    elif dist_sth_rp < 0.02 and dist_rp_lth < 0.02:
        struct = "C"
    else:
        struct = "T"

    if p >= avu:
        return "Z5"

    if struct == "N":
        if p < rp:
            return "ZC"
        elif p < sth:
            return "ZD"
        elif p < avm:
            return "Z3"
        else:
            return "Z4"
    elif struct == "T":
        if p < sth:
            return "Z1"
        elif p < rp:
            return "Z1b"
        else:
            return "Z2-transisi"
    else:  # C
        if p < avm:
            return "Z2"
        else:
            return "Z4"

dfm["zone"] = dfm.apply(classify_zone, axis=1)

# ─── Event detection: price < 200wma ────────────────────────────────────
dfm["below"] = dfm["btc_price"] < dfm["200_wma"]

# raw runs
raw_runs = []
in_run = False
for i, v in enumerate(dfm["below"].values):
    if v and not in_run:
        run_start = i
        in_run = True
    if not v and in_run:
        raw_runs.append((run_start, i - 1))
        in_run = False
if in_run:
    raw_runs.append((run_start, len(dfm) - 1))

raw_runs = [(s, e) for s, e in raw_runs if (e - s + 1) >= MIN_RUN_DAYS]
print(f"\nRaw runs (>= {MIN_RUN_DAYS}d berturut-turut di bawah 200wma), sebelum merge: {len(raw_runs)}")

# merge raw runs with gap < MERGE_GAP_DAYS
episodes = []
if raw_runs:
    cur_s, cur_e = raw_runs[0]
    for s, e in raw_runs[1:]:
        gap_days = (dfm.at[s, "date"] - dfm.at[cur_e, "date"]).days - 1
        if gap_days < MERGE_GAP_DAYS:
            cur_e = e  # merge
        else:
            episodes.append((cur_s, cur_e))
            cur_s, cur_e = s, e
    episodes.append((cur_s, cur_e))

print(f"Episodes final setelah merge (gap < {MERGE_GAP_DAYS}d digabung): {len(episodes)}")

# ─── Per-episode analysis ────────────────────────────────────────────────
rows = []
for s, e in episodes:
    start_date = dfm.at[s, "date"]
    end_date   = dfm.at[e, "date"]
    span = dfm.iloc[s:e+1]
    low_idx   = span["btc_price"].idxmin()
    low_price = dfm.at[low_idx, "btc_price"]
    low_date  = dfm.at[low_idx, "date"]

    zone_start = dfm.at[s, "zone"]
    zone_low   = dfm.at[low_idx, "zone"]

    fwd_end = end_date + pd.Timedelta(days=FLOOR_WINDOW)
    fwd = dfm[(dfm["date"] > end_date) & (dfm["date"] <= fwd_end)]

    if dfm["date"].max() < fwd_end:
        status = "INCOMPLETE (data forward < 180d)"
        breach = None
    else:
        min_fwd = fwd["btc_price"].min()
        breach_pct_actual = (low_price - min_fwd) / low_price
        breach = breach_pct_actual > BREACH_PCT
        status = "BREACH" if breach else "HOLDS"

    rows.append({
        "episode_start": start_date.date(),
        "episode_end": end_date.date(),
        "duration_days": (end_date - start_date).days + 1,
        "low_price": round(low_price, 2),
        "low_date": low_date.date(),
        "zone_at_start": zone_start,
        "zone_at_low": zone_low,
        "floor_status": status,
    })

ev_df = pd.DataFrame(rows)
print("\n" + "="*120)
print("EPISODES: price < 200-week MA (matang, merge gap<14d, min run 5d)")
print("="*120)
print(ev_df.to_string(index=False))

n_total = len(ev_df)
n_holds = (ev_df["floor_status"] == "HOLDS").sum()
n_breach = (ev_df["floor_status"] == "BREACH").sum()
n_incomplete = (ev_df["floor_status"].str.startswith("INCOMPLETE")).sum()

print(f"\nn episode total = {n_total}")
print(f"  HOLDS (floor bertahan, no breach >10% dlm 180d)  = {n_holds}")
print(f"  BREACH (breach >10% dlm 180d)                     = {n_breach}")
print(f"  INCOMPLETE (data forward blm cukup, tdk dihitung) = {n_incomplete}")
n_eval = n_holds + n_breach
if n_eval > 0:
    print(f"  Hit rate (HOLDS / evaluable) = {n_holds}/{n_eval} = {100*n_holds/n_eval:.0f}%")

# zone overlap check
print("\nZone overlap (zone_at_start value_counts):")
print(ev_df["zone_at_start"].value_counts())
print("\nZone overlap (zone_at_low value_counts):")
print(ev_df["zone_at_low"].value_counts())

ev_df.to_csv(
    r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-11_bitcoins-trend-is-bearish-heres-where-it-flips\events_200wma_cyclical_floor.csv",
    index=False,
)

# ─── (d) CAGR 200wma last 4 years ────────────────────────────────────────
print("\n" + "="*120)
print("CAGR 200-week MA, 4 tahun terakhir (dari data terakhir tersedia)")
print("="*120)
end_row_date = dfm["date"].max()
start_target = end_row_date - pd.Timedelta(days=4*365)
start_row = dfm[dfm["date"] <= start_target].iloc[-1]
end_row   = dfm[dfm["date"] == end_row_date].iloc[0]
cagr = (end_row["200_wma"] / start_row["200_wma"]) ** (365.0 / (end_row["date"]-start_row["date"]).days) - 1
print(f"200wma @ {start_row['date'].date()} = ${start_row['200_wma']:,.0f}")
print(f"200wma @ {end_row['date'].date()}   = ${end_row['200_wma']:,.0f}")
print(f"CAGR (4y) = {cagr*100:.1f}%/tahun")

# also 1-year-by-1-year breakdown for the last 4 years to check consistency
print("\nBreakdown per tahun (yoy 200wma growth), 4 titik terakhir:")
for yrs_back in [4, 3, 2, 1, 0]:
    target = end_row_date - pd.Timedelta(days=yrs_back*365)
    row = dfm[dfm["date"] <= target].iloc[-1]
    print(f"  {row['date'].date()}: 200wma = ${row['200_wma']:,.0f}")

# yoy growth
print("\nYoY growth 200wma per tahun (dari titik2 di atas):")
pts = []
for yrs_back in [4, 3, 2, 1, 0]:
    target = end_row_date - pd.Timedelta(days=yrs_back*365)
    row = dfm[dfm["date"] <= target].iloc[-1]
    pts.append((row["date"], row["200_wma"]))
for i in range(1, len(pts)):
    d0, v0 = pts[i-1]
    d1, v1 = pts[i]
    yoy = (v1/v0 - 1) * 100
    print(f"  {d0.date()} -> {d1.date()}: {yoy:+.1f}%")

# ─── (e) current 200wma vs claim ─────────────────────────────────────────
print("\n" + "="*120)
print("(e) 200wma di data terakhir vs klaim video ~$63,800")
print("="*120)
last_row = dfm.iloc[-1]
print(f"Tanggal data terakhir: {last_row['date'].date()}")
print(f"btc_price  = ${last_row['btc_price']:,.0f}")
print(f"200_wma    = ${last_row['200_wma']:,.0f}")
print(f"Klaim video (2026-08-11): 200wma ~$63,800, harga persis di level itu")
print(f"Selisih 200wma vs klaim: {last_row['200_wma'] - 63800:+,.0f} ({(last_row['200_wma']/63800-1)*100:+.1f}%)")

# extrapolate trend to 2026-08-11 using recent daily growth rate of 200wma
recent = dfm.tail(60)
daily_growth = (recent["200_wma"].iloc[-1] / recent["200_wma"].iloc[0]) ** (1/59) - 1
days_to_extrapolate = (pd.Timestamp("2026-08-11") - last_row["date"]).days
extrap_200wma = last_row["200_wma"] * (1 + daily_growth) ** days_to_extrapolate
print(f"\nEkstrapolasi 200wma ke 2026-08-11 pakai daily growth rate 60hr terakhir ({daily_growth*100:.4f}%/hari):")
print(f"  Extrapolated 200wma @ 2026-08-11 ~ ${extrap_200wma:,.0f}")
