"""
V2 -- Sensitivitas LTH Realized Price terhadap geseran boundary umur kohort,
dan dampaknya ke label struktur Zone Dimensi 1 + tanggal trigger Z2.

KLAIM YANG DIUJI (Matt Crosby, 2026-06-18, frame [08:53]-[09:09] Figure 5):
  "dynamic LTH cost basis $56.290 duduk 13,9% di atas static-155 cost basis
   $49.434 (standard base)"
  -> pertanyaan framework kita: kalau boundary LTH digeser, seberapa besar
     dampaknya ke Zone Structure v2 dan tanggal trigger Z2?

BATASAN BESAR (wajib disebut di findings):
  1. Data kita = vendor base "std" + boundary LTH STATIS 155 hari. Tidak ada
     raw UTXO -> TIDAK bisa mereplikasi boundary 114 hari maupun base "flt".
  2. HODL waves kita punya band '3m-6m' -- 114 hari DAN 155 hari dua-duanya
     jatuh DI DALAM band itu. Jadi LTH_RP(>=3m) vs LTH_RP(>=6m) adalah
     BRACKET / UPPER BOUND geseran boundary, BUKAN replikasi 114 hari.
     Efek boundary 155 -> 114 hari yang sebenarnya jauh LEBIH KECIL dari
     bracket ini. Jangan overclaim.

REKONSTRUKSI COST BASIS KOHORT:
  Kolom supply_<band> dan realized_cap_<band> di master CSV adalah SHARE
  (persen; sum semua band = 100 untuk supply, = 100 untuk realized cap).
  Maka:  cost_basis(kohort) = (sum rc_share / sum sup_share) * realized_price
  Diverifikasi: rekonstruksi seluruh band menghasilkan tepat realized_price,
  dan lth_cost_basis vendor selalu terletak di antara versi >=6m dan >=3m
  (sesuai ekspektasi karena 91d < 155d < 182d).
"""

import warnings

import numpy as np
import pandas as pd

warnings.simplefilter("ignore")

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = (r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos"
          r"\2026-06-18_i-rebuilt-bitcoins-155-day-holder-metric-its-now-even-more-accurate")

CONV_TOL = 0.02      # ambang 2% untuk struktur C (Konvergen)
START    = "2013-01-01"   # HODL waves di 2010-2012 masih tipis/ekstrem -> mulai 2013

BANDS_3M = ["3m-6m", "6m-12m", "1y-2y", "2y-3y", "3y-5y", "5y-7y", "7y-10y", "10y+"]
BANDS_6M = BANDS_3M[1:]
BANDS_1Y = BANDS_3M[2:]

df = pd.read_csv(MASTER, parse_dates=["date"])
df = df[df["btc_price"].notna()].sort_values("date").reset_index(drop=True)


def cohort_cb(bands):
    sup = sum(df["supply_" + b] for b in bands)
    rc  = sum(df["realized_cap_" + b] for b in bands)
    return (rc / sup) * df["realized_price"], sup


new = {}
new["lth_rp_3m"], new["share_3m"] = cohort_cb(BANDS_3M)
new["lth_rp_6m"], new["share_6m"] = cohort_cb(BANDS_6M)
new["lth_rp_1y"], new["share_1y"] = cohort_cb(BANDS_1Y)
df = pd.concat([df, pd.DataFrame(new)], axis=1)

print("=" * 104)
print("V2  SENSITIVITAS LTH REALIZED PRICE TERHADAP GESERAN BOUNDARY KOHORT")
print("=" * 104)
print("Basis: vendor std + boundary STATIS 155d. BRACKET >=3m / >=6m, BUKAN replikasi 114d Matt.")

# --- sanity: rekonstruksi seluruh band harus = realized_price
allb = ["0-1d", "1d-1w", "1w-1m", "1m-3m"] + BANDS_3M
sup_all = sum(df["supply_" + b] for b in allb)
rc_all  = sum(df["realized_cap_" + b] for b in allb)
chk = (rc_all / sup_all)
print(f"\nSanity check rekonstruksi (harus ~1.000): mean={chk.mean():.6f} min={chk.min():.6f} max={chk.max():.6f}")

d = df[df["date"] >= START].reset_index(drop=True)
print(f"Periode analisis: {d['date'].min().date()} s/d {d['date'].max().date()} (n={len(d)} hari)")

# ---------------------------------------------------------------- (a) selisih
d["dev_3m"] = d["lth_rp_3m"] / d["lth_cost_basis"] - 1
d["dev_6m"] = d["lth_rp_6m"] / d["lth_cost_basis"] - 1
d["dev_1y"] = d["lth_rp_1y"] / d["lth_cost_basis"] - 1
d["spread_3m_6m"] = d["lth_rp_3m"] / d["lth_rp_6m"] - 1

print("\n" + "-" * 104)
print("(a) SELISIH LTH_RP(>=3m) / LTH_RP(>=6m) / LTH_RP(>=1y) TERHADAP lth_cost_basis VENDOR (155d)")
print("-" * 104)
print(f"{'Seri':<18} {'mean':>9} {'median':>9} {'p10':>9} {'p90':>9} {'min':>9} {'max':>9}")
for col, nm in [("dev_3m", ">=3m vs vendor"), ("dev_6m", ">=6m vs vendor"),
                ("dev_1y", ">=1y vs vendor"), ("spread_3m_6m", ">=3m vs >=6m")]:
    s = d[col] * 100
    print(f"{nm:<18} {s.mean():>8.1f}% {s.median():>8.1f}% {s.quantile(.10):>8.1f}% "
          f"{s.quantile(.90):>8.1f}% {s.min():>8.1f}% {s.max():>8.1f}%")

CYCLES = [("2013-15", "2013-01-01", "2015-12-31"),
          ("2016-18", "2016-01-01", "2018-12-31"),
          ("2019-21", "2019-01-01", "2021-12-31"),
          ("2022-24", "2022-01-01", "2024-12-31"),
          ("2025-26", "2025-01-01", "2026-12-31")]

print(f"\n  Sebaran per cycle (median % deviasi terhadap vendor 155d):")
print(f"  {'Cycle':<9} {'n hari':>7} {'>=3m':>9} {'>=6m':>9} {'>=1y':>9} {'spread 3m-6m':>14}")
for nm, s, e in CYCLES:
    sub = d[(d["date"] >= s) & (d["date"] <= e)]
    if sub.empty:
        continue
    print(f"  {nm:<9} {len(sub):>7} {sub['dev_3m'].median()*100:>8.1f}% {sub['dev_6m'].median()*100:>8.1f}% "
          f"{sub['dev_1y'].median()*100:>8.1f}% {sub['spread_3m_6m'].median()*100:>13.1f}%")

print("\n  Fase pasar -- deviasi paling besar saat apa? (bucket berdasarkan MVRV Ratio)")
d["mvrv_bucket"] = pd.cut(d["mvrv_ratio"], [0, 1, 1.5, 2.5, 99],
                          labels=["<1 (bear)", "1-1.5", "1.5-2.5", ">2.5 (euforia)"])
g = d.groupby("mvrv_bucket", observed=True)[["dev_3m", "dev_6m", "spread_3m_6m"]].median() * 100
for idx, r in g.iterrows():
    cnt = int((d["mvrv_bucket"] == idx).sum())
    print(f"    {str(idx):<16} n={cnt:>5}  >=3m {r['dev_3m']:>7.1f}%  >=6m {r['dev_6m']:>7.1f}%  "
          f"spread {r['spread_3m_6m']:>7.1f}%")

# Konteks angka Matt
ref = d[d["date"] == "2026-06-16"]
if ref.empty:
    ref = d[d["date"] <= "2026-06-16"].tail(1)
r0 = ref.iloc[0]
print(f"\n  Snapshot {r0['date'].date()} (untuk konteks angka Matt $56.290 vs $49.434 = +13,9%):")
print(f"    vendor lth_cost_basis (155d) = ${r0['lth_cost_basis']:,.0f}")
print(f"    LTH_RP(>=3m, ~91d)           = ${r0['lth_rp_3m']:,.0f}  ({r0['dev_3m']*100:+.1f}%)")
print(f"    LTH_RP(>=6m, ~182d)          = ${r0['lth_rp_6m']:,.0f}  ({r0['dev_6m']*100:+.1f}%)")
print(f"    -> geseran boundary ke arah LEBIH MUDA menaikkan cost basis; bracket penuh 91d..182d "
      f"= {r0['spread_3m_6m']*100:.1f}%")

# ---------------------------------------------------------------- (b) label struktur Dimensi 1
def struct_label(sth, rp, lth):
    g1 = (sth - rp).abs() / rp
    g2 = (rp - lth).abs() / rp
    lab = np.where((g1 < CONV_TOL) & (g2 < CONV_TOL), "C", np.where(sth > rp, "N", "T"))
    return pd.Series(lab, index=sth.index)


d["lab_vendor"] = struct_label(d["sth_cost_basis"], d["realized_price"], d["lth_cost_basis"])
d["lab_3m"]     = struct_label(d["sth_cost_basis"], d["realized_price"], d["lth_rp_3m"])
d["lab_6m"]     = struct_label(d["sth_cost_basis"], d["realized_price"], d["lth_rp_6m"])

print("\n" + "-" * 104)
print("(b) LABEL STRUKTUR ZONE DIMENSI 1 (N / C / T) -- vendor vs rekonstruksi")
print("-" * 104)
for col, nm in [("lab_vendor", "vendor 155d"), ("lab_3m", ">=3m (91d)"), ("lab_6m", ">=6m (182d)")]:
    vc = d[col].value_counts().to_dict()
    print(f"  {nm:<14} N={vc.get('N',0):>5}  C={vc.get('C',0):>4}  T={vc.get('T',0):>5}")

for col, nm in [("lab_3m", ">=3m"), ("lab_6m", ">=6m")]:
    chg = (d[col] != d["lab_vendor"])
    print(f"\n  Label berubah vendor -> {nm}: {int(chg.sum())} hari dari {len(d)} "
          f"({chg.mean()*100:.2f}%)")
    if chg.any():
        tab = d[chg].groupby(["lab_vendor", col], observed=True).size().sort_values(ascending=False)
        for (a, b), n_ in tab.items():
            print(f"     {a} -> {b} : {n_} hari")
        print("     sebaran per cycle:")
        for cn, s, e in CYCLES:
            sub = d[(d["date"] >= s) & (d["date"] <= e)]
            if sub.empty:
                continue
            c_ = int((sub[col] != sub["lab_vendor"]).sum())
            print(f"       {cn:<9} {c_:>5} hari dari {len(sub)} ({c_/len(sub)*100:.1f}%)")

print("\n  Fokus struktur C (Konvergen) -- syarat: gap STH RP-RP DAN gap RP-LTH RP dua-duanya < 2%")
for col, nm in [("lab_vendor", "vendor 155d"), ("lab_3m", ">=3m"), ("lab_6m", ">=6m")]:
    cdays = d[d[col] == "C"]
    print(f"    {nm:<14} : {len(cdays)} hari C")
    if len(cdays):
        blocks, prev, start = [], None, None
        for dt in cdays["date"]:
            if prev is None or (dt - prev).days > 30:
                if prev is not None:
                    blocks.append((start, prev))
                start = dt
            prev = dt
        blocks.append((start, prev))
        for s_, e_ in blocks:
            print(f"        {s_.date()} .. {e_.date()} ({(e_-s_).days+1}d)")

# ---------------------------------------------------------------- (c) trigger Z2
# Z2 (Decision Framework v2): struktur C DAN P < AVIV Mean.
# Unlock bear framework juga pakai "STH RP cross naik melewati RP" -> catat dua-duanya.
d["aviv_mean_usd"] = d["price_at_aviv_mean"]
d["z2_vendor"] = (d["lab_vendor"] == "C") & (d["btc_price"] < d["aviv_mean_usd"])
d["z2_3m"]     = (d["lab_3m"] == "C") & (d["btc_price"] < d["aviv_mean_usd"])
d["z2_6m"]     = (d["lab_6m"] == "C") & (d["btc_price"] < d["aviv_mean_usd"])

# cross-up STH RP melewati RP (tidak tergantung LTH RP -> harus identik, dipakai sbg kontrol)
above = (d["sth_cost_basis"] > d["realized_price"]).astype(bool)
prev  = above.shift(1).fillna(False).astype(bool)
d["cross_up"] = above & (~prev)

print("\n" + "-" * 104)
print("(c) TANGGAL TRIGGER Z2 -- pergeseran akibat definisi LTH RP")
print("-" * 104)


def first_blocks(col):
    on = d[d[col]]
    if on.empty:
        return []
    out, prev, start = [], None, None
    for dt in on["date"]:
        if prev is None or (dt - prev).days > 90:
            if prev is not None:
                out.append((start, prev))
            start = dt
        prev = dt
    out.append((start, prev))
    return out


for col, nm in [("z2_vendor", "vendor 155d"), ("z2_3m", ">=3m"), ("z2_6m", ">=6m")]:
    bl = first_blocks(col)
    print(f"  Z2 ({nm}): {len(bl)} episode, total {int(d[col].sum())} hari")
    for s_, e_ in bl:
        print(f"      {s_.date()} .. {e_.date()} ({(e_-s_).days+1}d)")

print("\n  Kontrol -- cross-up STH RP melewati RP (tidak tergantung LTH RP, harus sama di semua versi):")
print("   ", ", ".join(str(x.date()) for x in d[d["cross_up"]]["date"]))

# geseran tanggal per episode (pasangkan episode terdekat)
print("\n  Geseran tanggal MULAI episode Z2 (vendor -> alternatif), pasangan dalam 365 hari:")
bl_v = first_blocks("z2_vendor")
for col, nm in [("z2_3m", ">=3m"), ("z2_6m", ">=6m")]:
    bl_a = first_blocks(col)
    for sv, ev in bl_v:
        cands = [(abs((sa - sv).days), sa) for sa, ea in bl_a if abs((sa - sv).days) <= 365]
        if cands:
            dd, sa = min(cands)
            print(f"    {nm:<6} {sv.date()} -> {sa.date()}  geser {(sa - sv).days:+d} hari")
        else:
            print(f"    {nm:<6} {sv.date()} -> TIDAK ADA episode padanan dalam 365 hari")

# ---------------------------------------------------------------- CSV
rows = []
chg_any = d[(d["lab_3m"] != d["lab_vendor"]) | (d["lab_6m"] != d["lab_vendor"])]
for _, r in chg_any.iterrows():
    rows.append(dict(date=r["date"].date(), btc_price=round(r["btc_price"], 2),
                     sth_rp=round(r["sth_cost_basis"], 2), rp=round(r["realized_price"], 2),
                     lth_rp_vendor155=round(r["lth_cost_basis"], 2),
                     lth_rp_3m=round(r["lth_rp_3m"], 2), lth_rp_6m=round(r["lth_rp_6m"], 2),
                     label_vendor=r["lab_vendor"], label_3m=r["lab_3m"], label_6m=r["lab_6m"]))
out = pd.DataFrame(rows)
out.to_csv(rf"{OUTDIR}\events_zone_label_changes.csv", index=False)
print(f"\nCSV disimpan: events_zone_label_changes.csv ({len(out)} baris hari yang labelnya berubah)")
print("SELESAI V2")
