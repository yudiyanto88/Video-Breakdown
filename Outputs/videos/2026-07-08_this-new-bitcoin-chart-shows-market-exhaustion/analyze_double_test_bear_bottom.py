"""
INSIGHT B -- Pola "double test" lower support band per bear market (Alphractal SMB proxy).

DEFINISI EVENT (eksplisit):
- PROXY UTAMA "test" = episode Z1: btc_price < sth_cost_basis DAN sth_cost_basis < realized_price
  (ordering terbalik, definisi Z1 framework). Dua run Z1 dianggap episode TERPISAH hanya kalau
  dipisah >= 30 hari berturut-turut di luar Z1; gap < 30 hari digabung.
- VARIAN ALTERNATIF "lower band dalam" = episode btc_price/cvdd < 1.15, merge rule sama (30d).
- Bear windows (eksplisit, top s/d recovery):
    2011-12 (context, data awal noisy), 2014-15, 2018-19, Covid-2020, 2022, 2025-26 (berjalan).
- Final bottom = low absolut close di dalam bear window.

SIMULASI K4 (actionable):
- Pool 100 USD, 4 tranche x 25 (proxy confidence 3-dari-4 = 25%/bulan tabel K4).
- Strategi A (framework): tranche pertama di HARI PERTAMA episode Z1 #1, tranche berikutnya
  tiap >= 30 hari setelahnya, dieksekusi di hari Z1 pertama yang tersedia (kalau harga lagi
  keluar Z1, tunggu balik Z1). Sisa pool yang belum masuk saat bear selesai -> deploy di
  Signal D (3 hari berturut close > STH RP setelah episode Z1 terakhir).
- Strategi B (tunggu "test kedua"): pool utuh, mulai DCA skema sama di hari pertama episode #2.
  Kalau episode #2 TIDAK PERNAH datang -> seluruh pool masuk di Signal D setelah episode #1
  (penalti realistis: yang nunggu akhirnya beli saat harga sudah reclaim STH RP).
- Semua nilai at-gate: zona dihitung dari close hari itu, tidak ada info masa depan.
"""
import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-07-08_this-new-bitcoin-chart-shows-market-exhaustion"

SEP_DAYS = 30  # minimal hari di luar zona untuk memisah dua episode

df = pd.read_csv(MASTER, parse_dates=["date"],
                 usecols=["date", "btc_price", "sth_cost_basis", "realized_price", "cvdd"])
df = df.sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "sth_cost_basis", "realized_price"])
df = df[df["btc_price"] > 0.01].reset_index(drop=True)

df["in_z1"]   = (df["btc_price"] < df["sth_cost_basis"]) & (df["sth_cost_basis"] < df["realized_price"])
df["cvdd_ok"] = df["cvdd"].notna() & (df["cvdd"] > 0)
df["in_cvdd"] = df["cvdd_ok"] & (df["btc_price"] / df["cvdd"] < 1.15)

print(f"Data: {df['date'].min().date()} s/d {df['date'].max().date()}  (n={len(df)})")

bears = [
    ("2011-12 (context)", "2011-06-09", "2012-07-01"),
    ("2014-15",           "2013-11-30", "2015-12-31"),
    ("2018-19",           "2017-12-17", "2019-05-01"),
    ("Covid-2020",        "2020-02-13", "2020-08-01"),
    ("2022",              "2021-11-09", "2023-06-01"),
    ("2025-26 (berjalan)","2025-10-07", "2026-07-13"),
]

def find_episodes(sub, col):
    """Runs of col==True; gabung kalau gap luar-zona < SEP_DAYS."""
    idx = sub.index.tolist()
    runs, start = [], None
    for i in idx:
        if sub.at[i, col] and start is None:
            start = i
        elif not sub.at[i, col] and start is not None:
            runs.append((start, prev))
            start = None
        prev = i
    if start is not None:
        runs.append((start, idx[-1]))
    eps = []
    for r in runs:
        if eps:
            gap = (sub.at[r[0], "date"] - sub.at[eps[-1][1], "date"]).days - 1
            if gap < SEP_DAYS:
                eps[-1] = (eps[-1][0], r[1])
                continue
        eps.append(r)
    return eps

all_rows = []
for name, a, b in bears:
    a, b = pd.Timestamp(a), pd.Timestamp(b)
    sub = df[(df["date"] >= a) & (df["date"] <= b)]
    if sub.empty:
        continue
    low_i = sub["btc_price"].idxmin()
    low_d, low_p = df.at[low_i, "date"], df.at[low_i, "btc_price"]
    print("\n" + "=" * 100)
    print(f"BEAR {name}  window {a.date()} s/d {b.date()}  | low absolut: {low_d.date()} @ ${low_p:,.0f}")
    for col, label in [("in_z1", "Z1 (P<STH RP, STH RP<RP)"), ("in_cvdd", "P/CVDD < 1.15")]:
        eps = find_episodes(sub, col)
        print(f"  --- Proxy: {label}  ->  n_episode = {len(eps)}")
        prev_low = None
        for j, (s, e) in enumerate(eps, 1):
            seg = df.loc[s:e]
            seg_in = seg[seg[col]]
            mn_i = seg_in["btc_price"].idxmin()
            mn_d, mn_p = df.at[mn_i, "date"], df.at[mn_i, "btc_price"]
            days_in = int(seg[col].sum())
            has_low = s <= low_i <= e
            rel = ""
            if prev_low is not None:
                chg = (mn_p / prev_low[1] - 1) * 100
                dt  = (mn_d - prev_low[0]).days
                rel = f"| vs ep sebelumnya: {'LOWER' if chg < 0 else 'HIGHER'} low {chg:+.1f}%, jarak {dt}d"
            print(f"      ep{j}: {df.at[s,'date'].date()} s/d {df.at[e,'date'].date()} "
                  f"({days_in}d in-zone) | low ep: {mn_d.date()} @ ${mn_p:,.0f} "
                  f"{'<< FINAL BOTTOM' if has_low else ''} {rel}")
            prev_low = (mn_d, mn_p)
            all_rows.append({"bear": name, "proxy": label, "ep": j,
                             "start": df.at[s, "date"].date(), "end": df.at[e, "date"].date(),
                             "days_in_zone": days_in, "ep_low_date": mn_d.date(),
                             "ep_low": mn_p, "is_final_bottom": has_low})

pd.DataFrame(all_rows).to_csv(f"{OUTDIR}\\_bear_test_episodes.csv", index=False)

# =====================================================================
# SIMULASI K4: DCA sejak episode Z1 #1 vs tunggu episode #2
# =====================================================================
print("\n" + "=" * 100)
print("SIMULASI K4  |  pool=100, 4 tranche x 25, jarak antar tranche >= 30d, eksekusi di hari Z1")
print("=" * 100)

def signal_d(after_idx):
    """3 hari berturut close > STH RP, mulai cari setelah index tsb."""
    cnt = 0
    for i in range(after_idx + 1, len(df)):
        if df.at[i, "btc_price"] > df.at[i, "sth_cost_basis"]:
            cnt += 1
            if cnt >= 3:
                return i
        else:
            cnt = 0
    return None

def dca_from(start_idx, end_bound_idx, pool, n_tranche, last_z1_end):
    """DCA tranche di hari-hari Z1; sisa masuk di Signal D setelah episode Z1 terakhir."""
    tranche = pool / n_tranche
    spent_usd, got_btc, deployed = 0.0, 0.0, 0
    next_ok = df.at[start_idx, "date"]
    fills = []
    for i in range(start_idx, end_bound_idx + 1):
        if deployed >= n_tranche:
            break
        if df.at[i, "in_z1"] and df.at[i, "date"] >= next_ok:
            p = df.at[i, "btc_price"]
            spent_usd += tranche
            got_btc   += tranche / p
            deployed  += 1
            fills.append((df.at[i, "date"].date(), p))
            next_ok = df.at[i, "date"] + pd.Timedelta(days=30)
    leftover = pool - spent_usd
    if leftover > 1e-9:
        sd = signal_d(last_z1_end)
        if sd is not None:
            p = df.at[sd, "btc_price"]
            spent_usd += leftover
            got_btc   += leftover / p
            fills.append((df.at[sd, "date"].date(), p))
    avg = spent_usd / got_btc if got_btc > 0 else np.nan
    return avg, got_btc, fills, leftover

for name, a, b in bears:
    a, b = pd.Timestamp(a), pd.Timestamp(b)
    sub = df[(df["date"] >= a) & (df["date"] <= b)]
    if sub.empty:
        continue
    eps = find_episodes(sub, "in_z1")
    if not eps:
        print(f"\nBEAR {name}: tidak ada episode Z1 -- skip")
        continue
    end_bound = sub.index[-1]
    last_z1_end = eps[-1][1]
    ongoing = (name.find("berjalan") >= 0)

    avgA, btcA, fillsA, leftA = dca_from(eps[0][0], end_bound, 100.0, 4, last_z1_end)
    print(f"\nBEAR {name}")
    print(f"  A (DCA sejak ep1, {df.at[eps[0][0],'date'].date()}): avg entry ${avgA:,.0f}"
          f"  | fills: {[(str(d), round(p)) for d, p in fillsA]}"
          + (f"  | SISA belum masuk: {leftA:.0f}" if ongoing and leftA > 1e-9 else ""))
    if len(eps) >= 2:
        avgB, btcB, fillsB, leftB = dca_from(eps[1][0], end_bound, 100.0, 4, last_z1_end)
        dpct = (avgB / avgA - 1) * 100
        print(f"  B (tunggu ep2, mulai {df.at[eps[1][0],'date'].date()}): avg entry ${avgB:,.0f}"
              f"  | fills: {[(str(d), round(p)) for d, p in fillsB]}")
        print(f"  >>> avg entry B vs A: {dpct:+.1f}%  ({'B lebih murah' if dpct < 0 else 'A lebih murah/setara'})")
    else:
        sd = signal_d(last_z1_end)
        if ongoing:
            print("  B: episode ke-2 BELUM datang (bear berjalan) -- pool masih 100% cash, unresolved")
        elif sd is not None:
            p = df.at[sd, "btc_price"]
            dpct = (p / avgA - 1) * 100
            print(f"  B: episode ke-2 TIDAK PERNAH datang -> seluruh pool masuk di Signal D "
                  f"{df.at[sd,'date'].date()} @ ${p:,.0f}  | vs avg A: {dpct:+.1f}%")
