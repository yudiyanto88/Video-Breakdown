"""
INSIGHT A — F&G peak mendahului price peak? (On-Chain Mind, video 2025-02-23)

Definisi event:
- Cycle A = 2018-02-01 s/d 2022-11-21 (bear bottom Nov 2022). F&G data mulai 2018-02-01.
- Cycle B = 2022-11-22 s/d data terakhir.
- "Price peak lokal (top)" = hari yang merupakan maksimum harga dalam window +/-45 hari
  DAN merupakan cycle-high baru (>= 99% dari running max cycle saat itu) DAN harga minimal
  drop 15% sesudahnya sebelum high baru (supaya Apr 2021 & Nov 2021 kepisah, noise kefilter).
- "ATH cluster" untuk cek diminishing (b): hari-hari yang set new cycle high, di-merge
  kalau jarak antar new-high < 30 hari -> satu cluster; wakil cluster = hari harga tertinggi.
- Extreme greed (c) = raw F&G >= 75 (bucket standar alternate.me: 75-100 = extreme greed).
Anti-lookahead: nilai F&G / SMA30 yang dibaca di tanggal T hanya pakai data <= T.
"""
import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Video-Breakdown\Outputs\2025-02-23_fear-greed-index"

df = pd.read_csv(MASTER, usecols=["date", "btc_price", "Fear & Greed"], parse_dates=["date"])
df = df.rename(columns={"Fear & Greed": "fg"}).sort_values("date").reset_index(drop=True)
df = df[df["date"] >= "2018-02-01"].reset_index(drop=True)
df["fg"] = df["fg"].ffill()  # 4 hari bolong -> ffill
df["fg_sma30"] = df["fg"].rolling(30, min_periods=30).mean()

CYCLES = {
    "Cycle A (2018-2022)": ("2018-02-01", "2022-11-21"),
    "Cycle B (2022-skrg)": ("2022-11-22", str(df["date"].max().date())),
}

def local_tops(sub):
    """Price top lokal: max window +/-45d, new cycle-high (>=99% running max), drop >=15% after."""
    p = sub["btc_price"].values
    dates = sub["date"].values
    runmax = np.maximum.accumulate(p)
    tops = []
    n = len(sub)
    for i in range(n):
        lo, hi = max(0, i - 45), min(n, i + 46)
        if p[i] < p[lo:hi].max():
            continue
        if p[i] < 0.99 * runmax[i]:
            continue
        # drop >=15% sesudahnya sebelum ada high baru
        j = i + 1
        min_after = p[i]
        broke = False
        while j < n:
            min_after = min(min_after, p[j])
            if p[j] > p[i]:
                break
            j += 1
        if min_after <= 0.85 * p[i] or j >= n:
            broke = True
        if broke:
            tops.append(i)
    # merge tops < 30 hari
    merged = []
    for i in tops:
        if merged and (dates[i] - dates[merged[-1]]).astype("timedelta64[D]").astype(int) < 30:
            if p[i] >= p[merged[-1]]:
                merged[-1] = i
        else:
            merged.append(i)
    return merged

def ath_clusters(sub):
    """Cluster hari-hari new cycle high (gap <30d = satu cluster), wakil = harga tertinggi."""
    p = sub["btc_price"].values
    runmax = np.maximum.accumulate(p)
    newhigh_idx = [i for i in range(len(p)) if p[i] >= runmax[i] and (i == 0 or p[i] > runmax[i - 1])]
    clusters = []
    cur = []
    for i in newhigh_idx:
        if cur and (sub["date"].iloc[i] - sub["date"].iloc[cur[-1]]).days >= 30:
            clusters.append(cur)
            cur = []
        cur.append(i)
    if cur:
        clusters.append(cur)
    reps = [max(c, key=lambda i: p[i]) for c in clusters]
    return reps

rows_a = []
print("=" * 100)
print("(a) F&G MAX CYCLE vs PRICE PEAK")
print("=" * 100)
for cname, (d0, d1) in CYCLES.items():
    sub = df[(df["date"] >= d0) & (df["date"] <= d1)].reset_index(drop=True)
    fgmax_i = sub["fg"].idxmax()
    fgmax_date, fgmax_val = sub.loc[fgmax_i, "date"], sub.loc[fgmax_i, "fg"]
    fgmax_price = sub.loc[fgmax_i, "btc_price"]
    # SMA30 max juga (lebih stabil)
    sma_i = sub["fg_sma30"].idxmax()
    sma_date, sma_val = sub.loc[sma_i, "date"], sub.loc[sma_i, "fg_sma30"]

    pmax_i = sub["btc_price"].idxmax()
    pmax_date, pmax_val = sub.loc[pmax_i, "date"], sub.loc[pmax_i, "btc_price"]
    fg_at_peak = sub.loc[pmax_i, "fg"]
    sma_at_peak = sub.loc[pmax_i, "fg_sma30"]
    lead = (pmax_date - fgmax_date).days
    print(f"\n{cname}")
    print(f"  F&G raw max     : {fgmax_val:.0f} pada {fgmax_date.date()} (price ${fgmax_price:,.0f})")
    print(f"  F&G SMA30 max   : {sma_val:.1f} pada {sma_date.date()}")
    print(f"  Price peak cycle: ${pmax_val:,.0f} pada {pmax_date.date()}")
    print(f"  F&G peak mendahului price peak: {lead} hari")
    print(f"  F&G saat price peak: raw={fg_at_peak:.0f}, SMA30={sma_at_peak:.1f}")

    # tops lokal dalam cycle
    tops = local_tops(sub)
    print(f"  Top lokal terdeteksi ({len(tops)}):")
    for i in tops:
        print(f"    {sub['date'].iloc[i].date()}  ${sub['btc_price'].iloc[i]:,.0f}  "
              f"raw F&G={sub['fg'].iloc[i]:.0f}  SMA30={sub['fg_sma30'].iloc[i]:.1f}")
        rows_a.append({"cycle": cname, "type": "local_top", "date": sub["date"].iloc[i].date(),
                       "price": round(sub["btc_price"].iloc[i]), "fg_raw": sub["fg"].iloc[i],
                       "fg_sma30": round(sub["fg_sma30"].iloc[i], 1)})

print("\n" + "=" * 100)
print("(b) DIMINISHING F&G DI SETIAP ATH CLUSTER BARU (SMA30)")
print("=" * 100)
rows_b = []
for cname, (d0, d1) in CYCLES.items():
    sub = df[(df["date"] >= d0) & (df["date"] <= d1)].reset_index(drop=True)
    reps = ath_clusters(sub)
    # buang cluster awal cycle yang bukan ATH bermakna (harga masih di bawah high cycle sebelumnya utk Cycle B tidak berlaku krn runmax intra-cycle)
    print(f"\n{cname} — ATH clusters (new cycle-high, merge <30d): n={len(reps)}")
    prev = None
    for i in reps:
        d, p, s = sub["date"].iloc[i], sub["btc_price"].iloc[i], sub["fg_sma30"].iloc[i]
        r = sub["fg"].iloc[i]
        dim = "" if prev is None else ("LOWER (diminishing)" if s < prev else "HIGHER (tidak diminishing)")
        print(f"  {d.date()}  ${p:,.0f}  raw={r:.0f}  SMA30={s:.1f}  {dim}")
        rows_b.append({"cycle": cname, "type": "ath_cluster", "date": d.date(), "price": round(p),
                       "fg_raw": r, "fg_sma30": round(s, 1), "vs_prev": dim or "first"})
        prev = s

print("\n" + "=" * 100)
print("(c) EXTREME GREED PERTAMA (raw F&G >= 75) PER CYCLE -> UPSIDE KE PRICE PEAK")
print("=" * 100)
for cname, (d0, d1) in CYCLES.items():
    sub = df[(df["date"] >= d0) & (df["date"] <= d1)].reset_index(drop=True)
    eg = sub[sub["fg"] >= 75]
    pmax_i = sub["btc_price"].idxmax()
    pmax_val, pmax_date = sub.loc[pmax_i, "btc_price"], sub.loc[pmax_i, "date"]
    if eg.empty:
        print(f"\n{cname}: tidak pernah >= 75")
        continue
    first = eg.iloc[0]
    upside = pmax_val / first["btc_price"] - 1
    days = (pmax_date - first["date"]).days
    print(f"\n{cname}")
    print(f"  Extreme greed pertama: {first['date'].date()}  F&G={first['fg']:.0f}  price=${first['btc_price']:,.0f}")
    print(f"  Price peak cycle     : {pmax_date.date()}  ${pmax_val:,.0f}")
    print(f"  Upside dari titik itu ke peak: {upside*100:.0f}%  ({days} hari)")
    # catatan Cycle A: F&G start 2018-02, extreme greed pertama mungkin sisa top 2017/awal data
    # tampilkan juga extreme greed pertama SETELAH bear bottom (proxy: setelah 2019-01-01 / 2023-01-01)
    cutoff = "2019-01-01" if "A" in cname else "2023-01-01"
    eg2 = sub[(sub["fg"] >= 75) & (sub["date"] >= cutoff)]
    if not eg2.empty:
        f2 = eg2.iloc[0]
        up2 = pmax_val / f2["btc_price"] - 1
        dd2 = (pmax_date - f2["date"]).days
        print(f"  (Setelah {cutoff}) pertama: {f2['date'].date()}  F&G={f2['fg']:.0f}  "
              f"price=${f2['btc_price']:,.0f}  upside ke peak {up2*100:.0f}%  ({dd2} hari)")

pd.DataFrame(rows_a + rows_b).to_csv(OUTDIR + r"\events_fg_tops_ath.csv", index=False)
print("\nSaved: events_fg_tops_ath.csv")
