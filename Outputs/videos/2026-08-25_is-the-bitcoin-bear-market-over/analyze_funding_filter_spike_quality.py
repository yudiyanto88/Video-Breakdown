"""
VALIDASI P5 - funding_filter_spike_quality

Klaim video: kalau funding tetap RENDAH saat harga spike naik besar, rally itu
"berkualitas" (real spot demand), bukan leverage -> lebih tahan lama.

PERINGATAN PERMANEN: funding_rate & total_oi baru ada sejak 2020-02-28/2020-03-31.
Itu ~1,5 siklus. SAMPLE KECIL - hasil di sini permanen LOW-CONFIDENCE dan tidak
bisa diuji lintas semua siklus.

Definisi event (dikunci sebelum menghitung):
  - Event = return 1 hari btc_price >= +7%
  - Cooldown 14 hari (event dalam 14 hari setelah event sebelumnya dibuang)
  - Periode = sejak funding_rate tersedia s/d hari terakhir data
Split AT-GATE (nilai tersedia di hari event, tidak ada nilai masa depan):
  - funding_rate di hari event -> kuartil (Q1 = paling rendah)
  - delta total_oi 3 hari = total_oi(t)/total_oi(t-3) - 1 -> kuartil
Outcome (ground truth): return 30/90 hari ke depan + max drawdown 30/90 hari.
"""

import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-25_is-the-bitcoin-bear-market-over"

SPIKE = 7.0
COOLDOWN = 14

df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 0].reset_index(drop=True)
LAST = df["date"].max()

fr = df.dropna(subset=["funding_rate"])
oi = df.dropna(subset=["total_oi"])
print("Data master s/d:", LAST.date())
print(f"funding_rate : {fr['date'].min().date()} s/d {fr['date'].max().date()} (n={len(fr)})")
print(f"total_oi     : {oi['date'].min().date()} s/d {oi['date'].max().date()} (n={len(oi)})")
START = max(fr["date"].min(), oi["date"].min())
print(f">> periode uji mulai {START.date()} = SEKITAR 1,5 SIKLUS. SAMPLE KECIL - LOW CONFIDENCE PERMANEN.")

df["ret1d"] = df["btc_price"].pct_change() * 100
df["d_oi3"] = df["total_oi"].pct_change(3) * 100

sub = df[(df["date"] >= START)].reset_index(drop=True)

# ---------- deteksi event ----------
ev_idx = []
last = None
for i in range(len(sub)):
    if pd.isna(sub.at[i, "ret1d"]) or sub.at[i, "ret1d"] < SPIKE:
        continue
    d = sub.at[i, "date"]
    if last is not None and (d - last).days < COOLDOWN:
        continue
    if pd.isna(sub.at[i, "funding_rate"]):
        continue
    ev_idx.append(i)
    last = d

print(f"\nn EVENT spike 1 hari >= +{SPIKE:.0f}% (cooldown {COOLDOWN}d) = {len(ev_idx)}")


def cycle_of(d):
    if d < pd.Timestamp("2022-01-01"):
        return "2020-21 bull"
    if d < pd.Timestamp("2023-03-01"):
        return "2022 bear"
    if d < pd.Timestamp("2025-10-06"):
        return "2023-25 bull"
    return "2025-26 bear"


rows = []
for i in ev_idx:
    d = sub.at[i, "date"]
    p0 = float(sub.at[i, "btc_price"])

    def fwd(days):
        tgt = d + pd.Timedelta(days=days)
        if tgt > LAST:
            return np.nan, np.nan
        w = df[(df["date"] > d) & (df["date"] <= tgt)]
        r = round((float(w.iloc[-1]["btc_price"]) / p0 - 1) * 100, 1)
        dd = round((float(w["btc_price"].min()) / p0 - 1) * 100, 1)
        return r, dd

    r30, dd30 = fwd(30)
    r90, dd90 = fwd(90)
    rows.append({
        "cycle": cycle_of(d),
        "event_date": d.strftime("%Y-%m-%d"),
        "ret1d": round(float(sub.at[i, "ret1d"]), 1),
        "price": round(p0, 2),
        "funding_rate": round(float(sub.at[i, "funding_rate"]), 5),
        "d_oi3_pct": round(float(sub.at[i, "d_oi3"]), 2) if not pd.isna(sub.at[i, "d_oi3"]) else np.nan,
        "ret_30d": r30, "maxdd_30d": dd30, "ret_90d": r90, "maxdd_90d": dd90,
        "censored_90d": (d + pd.Timedelta(days=90)) > LAST,
    })

ev = pd.DataFrame(rows)
ev["fr_q"] = pd.qcut(ev["funding_rate"], 4, labels=["Q1 (terendah)", "Q2", "Q3", "Q4 (tertinggi)"])
ev["oi_q"] = pd.qcut(ev["d_oi3_pct"], 4, labels=["Q1 (terendah)", "Q2", "Q3", "Q4 (tertinggi)"])
ev.to_csv(OUTDIR + r"\events_funding_filter_spike_quality.csv", index=False)

print("\n" + "=" * 118)
print("TABEL EVENT SPIKE")
print("=" * 118)
print(f"{'cycle':<14}{'event':<12}{'ret1d':>7}{'funding':>10}{'dOI3d%':>9}{'ret30':>8}{'dd30':>8}{'ret90':>8}{'dd90':>8}"
      f"  {'fr kuartil':<15}")
print("-" * 118)


def s(x):
    return "   n/a" if (isinstance(x, float) and np.isnan(x)) else f"{x:>6.1f}"


for _, r in ev.iterrows():
    print(f"{r['cycle']:<14}{r['event_date']:<12}{r['ret1d']:>7.1f}{r['funding_rate']:>10.4f}"
          f"{(r['d_oi3_pct'] if not np.isnan(r['d_oi3_pct']) else float('nan')):>9.2f}"
          f"{s(r['ret_30d']):>8}{s(r['maxdd_30d']):>8}{s(r['ret_90d']):>8}{s(r['maxdd_90d']):>8}  {str(r['fr_q']):<15}"
          + ("[censored 90d]" if r["censored_90d"] else ""))

print("\nSEBARAN PER CYCLE/FASE:")
for c, g in ev.groupby("cycle"):
    print(f"   {c}: n={len(g)}")

print("\n" + "=" * 118)
print("SPLIT A - KUARTIL FUNDING RATE DI HARI EVENT (at-gate)")
print("=" * 118)
print(f"{'kuartil':<16}{'n':>4}{'rentang funding':>26}{'med ret30':>11}{'med dd30':>10}{'med ret90':>11}{'med dd90':>10}")
print("-" * 118)
for q, g in ev.groupby("fr_q", observed=True):
    print(f"{str(q):<16}{len(g):>4}{f'{g.funding_rate.min():.4f} .. {g.funding_rate.max():.4f}':>26}"
          f"{g['ret_30d'].median():>11.1f}{g['maxdd_30d'].median():>10.1f}"
          f"{g['ret_90d'].median():>11.1f}{g['maxdd_90d'].median():>10.1f}")
    print(f"                 tanggal: {list(g['event_date'])}")
    print(f"                 sebaran cycle: {dict(g['cycle'].value_counts())}")

print("\n" + "=" * 118)
print("SPLIT B - KUARTIL DELTA OPEN INTEREST 3 HARI (at-gate)")
print("=" * 118)
print(f"{'kuartil':<16}{'n':>4}{'rentang dOI3d%':>26}{'med ret30':>11}{'med dd30':>10}{'med ret90':>11}{'med dd90':>10}")
print("-" * 118)
for q, g in ev.groupby("oi_q", observed=True):
    print(f"{str(q):<16}{len(g):>4}{f'{g.d_oi3_pct.min():.2f} .. {g.d_oi3_pct.max():.2f}':>26}"
          f"{g['ret_30d'].median():>11.1f}{g['maxdd_30d'].median():>10.1f}"
          f"{g['ret_90d'].median():>11.1f}{g['maxdd_90d'].median():>10.1f}")
    print(f"                 sebaran cycle: {dict(g['cycle'].value_counts())}")

print("\n" + "=" * 118)
print("SPLIT C - KOMBINASI: funding rendah (Q1-Q2) & OI rendah (Q1-Q2) = 'rally spot' hipotesis video")
print("=" * 118)
low_fr = ev["fr_q"].isin(["Q1 (terendah)", "Q2"])
low_oi = ev["oi_q"].isin(["Q1 (terendah)", "Q2"])
groups = {
    "funding RENDAH + OI RENDAH (hipotesis 'berkualitas')": low_fr & low_oi,
    "funding TINGGI + OI TINGGI (hipotesis 'leverage')": (~low_fr) & (~low_oi),
    "campuran": ~((low_fr & low_oi) | ((~low_fr) & (~low_oi))),
}
for name, m in groups.items():
    g = ev[m]
    if len(g) == 0:
        print(f"{name:<52} n=0")
        continue
    print(f"{name:<52} n={len(g):<3} med ret30={g['ret_30d'].median():>6.1f}%  med dd30={g['maxdd_30d'].median():>6.1f}%  "
          f"med ret90={g['ret_90d'].median():>6.1f}%  med dd90={g['maxdd_90d'].median():>6.1f}%")
    print(f"    sebaran cycle: {dict(g['cycle'].value_counts())}")
    print(f"    tanggal: {list(g['event_date'])}")

# uji arah sederhana: korelasi rank
print("\n" + "-" * 118)
print("KORELASI RANK (Spearman) funding at-gate vs outcome")
print("-" * 118)
for col in ["ret_30d", "maxdd_30d", "ret_90d", "maxdd_90d"]:
    v = ev[["funding_rate", col]].dropna()
    v2 = ev[["d_oi3_pct", col]].dropna()
    print(f"  {col:<10} vs funding: rho={v['funding_rate'].corr(v[col], method='spearman'):+.2f} (n={len(v)})"
          f"   |  vs dOI3d: rho={v2['d_oi3_pct'].corr(v2[col], method='spearman'):+.2f} (n={len(v2)})")

print(f"\nCSV -> {OUTDIR}\\events_funding_filter_spike_quality.csv")
print("\n!! INGAT: funding/OI mulai 2020 -> ~1,5 siklus. Semua angka di atas LOW CONFIDENCE.")
