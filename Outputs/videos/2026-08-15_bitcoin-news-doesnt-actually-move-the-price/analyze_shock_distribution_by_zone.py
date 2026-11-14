"""
VALIDASI 1 - Distribusi shock day per zona v2 (insight B-7:
"shock terbesar terkonsentrasi saat harga sedang jatuh").

Q1 shock per 100 hari zona (bukan jumlah mentah)
Q2 down-shock vs up-shock per zona, rasio down:up
Q3 zona loan aktif (K2: ZD/Z3/Z4 ; K5: Z2/Z3) -> p95 drawdown 3 hari vs headroom LTV
Q4 full-history vs >=2013

Definisi shock & zona: lihat shock_zone_lib.py (dikunci di muka).
"""
import numpy as np
import pandas as pd
import shock_zone_lib as L

OUT_CSV = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-15_bitcoin-news-doesnt-actually-move-the-price\events_shock_by_zone.csv"

df = L.load_base()
df["dd3"]  = L.fwd_worst_drawdown(df["btc_price"], 3)
df["dd5"]  = L.fwd_worst_drawdown(df["btc_price"], 5)

def line(c="="): print(c * 100)

def zone_table(d, shock_col, label):
    line()
    print(f"[{label}]  n hari = {len(d)}  |  {d['date'].min().date()} s/d {d['date'].max().date()}")
    tot_shock = int(d[shock_col].sum())
    base_rate = 100.0 * tot_shock / len(d)
    print(f"Total shock = {tot_shock}  |  rate keseluruhan = {base_rate:.2f} per 100 hari")
    print(f"{'Zona':<6}{'hari':>7}{'shock':>7}{'per100d':>9}{'down':>7}{'up':>6}{'down:up':>9}"
          f"{'%down':>7}{'medDD3':>9}{'p95DD3':>9}")
    print("-" * 100)
    rows = []
    for z in L.ZONE_ORDER:
        sub = d[d["zone"] == z]
        if len(sub) == 0:
            continue
        s = sub[sub[shock_col]]
        dn = int((s["logret"] < 0).sum()); up = int((s["logret"] > 0).sum())
        per100 = 100.0 * len(s) / len(sub)
        ratio = (dn / up) if up > 0 else np.inf
        pdown = 100.0 * dn / len(s) if len(s) else np.nan
        med = np.nanmedian(sub["dd3"]) * 100
        p95 = np.nanpercentile(sub["dd3"], 5) * 100   # 5th pct = 95th pct drawdown magnitude
        print(f"{z:<6}{len(sub):>7}{len(s):>7}{per100:>9.2f}{dn:>7}{up:>6}"
              f"{(f'{ratio:.2f}' if np.isfinite(ratio) else 'inf'):>9}"
              f"{pdown:>7.0f}{med:>9.1f}{p95:>9.1f}")
        rows.append(dict(scope=label, zone=z, days=len(sub), shocks=len(s),
                         per100d=round(per100, 2), down=dn, up=up,
                         ratio_down_up=(round(ratio, 2) if np.isfinite(ratio) else None),
                         pct_down=round(pdown, 1) if len(s) else None,
                         med_dd3_pct=round(med, 2), p95_dd3_pct=round(p95, 2)))
    return pd.DataFrame(rows)

def zone_grouped(d, zones, gname, shock_col):
    sub = d[d["zone"].isin(zones)]
    s = sub[sub[shock_col]]
    dn = int((s["logret"] < 0).sum()); up = int((s["logret"] > 0).sum())
    return dict(group=gname, zones="+".join(zones), days=len(sub), shocks=len(s),
                per100d=round(100.0 * len(s) / len(sub), 2) if len(sub) else np.nan,
                down=dn, up=up)

def ltv_headroom(d, zones, gname):
    sub = d[d["zone"].isin(zones)].dropna(subset=["dd3"])
    dd = sub["dd3"].values
    print(f"\n{gname}  (zona {'+'.join(zones)})  n hari = {len(dd)}")
    for q, lab in [(50, "p50"), (80, "p80"), (95, "p95"), (99, "p99")]:
        print(f"  {lab} drawdown 3-hari : {np.percentile(dd, 100 - q) * 100:7.2f}%")
    print(f"  worst 3-hari           : {dd.min() * 100:7.2f}%  ({sub.loc[sub['dd3'].idxmin(),'date'].date()})")
    for cap in (0.45, 0.48):
        print(f"  -- dari cap LTV {cap*100:.0f}%:")
        for tgt, lab in [(0.58, "rung-1 58%"), (0.60, "wajib-jual 60%"),
                         (0.62, "rung-2 62%"), (0.65, "rung-3 65%")]:
            need = 1 - cap / tgt
            hit = 100.0 * np.mean(dd <= -need)
            print(f"     {lab:<16} butuh drop {need*100:5.1f}%  ->  {hit:5.2f}% hari "
                  f"({int(np.sum(dd <= -need))} hari) drawdown 3-hari sedalam itu")

all_rows = []
for scope, d in [("FULL 2010-2026", df), (">=2013", df[df["date"] >= "2013-01-01"])]:
    for col, cl in [("shock_primary", "PRIMARY 3x vol30"), ("shock_fixed", "VARIAN fixed 8%")]:
        all_rows.append(zone_table(d, col, f"{scope} | {cl}"))

line()
print("Q2 RINGKAS - grup zona (PRIMARY, >=2013)")
d13 = df[df["date"] >= "2013-01-01"]
grp = [(["ZC", "Z1", "Z1b"], "BEAR BAWAH (ZC/Z1/Z1b)"),
       (["ZD", "Z3"], "MID (ZD/Z3)"),
       (["Z4", "Z5"], "ATAS (Z4/Z5)"),
       (["ZD", "Z3", "Z4"], "K2 loan aktif"),
       (["Z2", "Z2t", "Z3"], "K5 loan aktif")]
print(f"{'grup':<26}{'hari':>7}{'shock':>7}{'per100d':>9}{'down':>7}{'up':>6}")
for zs, nm in grp:
    g = zone_grouped(d13, zs, nm, "shock_primary")
    print(f"{nm:<26}{g['days']:>7}{g['shocks']:>7}{g['per100d']:>9.2f}{g['down']:>7}{g['up']:>6}")

line()
print("Q3 HEADROOM LTV - drawdown 3-hari dari titik entry (>=2013, semua hari di zona itu)")
ltv_headroom(d13, ["ZD", "Z3", "Z4"], "K2 loan window")
ltv_headroom(d13, ["Z2", "Z2t", "Z3"], "K5 loan window")
ltv_headroom(d13, ["ZD"], "K2 - hanya ZD (dip terdalam yang diizinkan)")

line()
print("Q4 SEBARAN SHOCK PER CYCLE (PRIMARY)")
print(df.groupby("cycle")["shock_primary"].agg(["sum", "count"]).to_string())
print("\nPorsi shock full-history yang terjadi pra-2013:",
      f"{100.0*df[df['date']<'2013-01-01']['shock_primary'].sum()/df['shock_primary'].sum():.1f}%",
      f"({int(df[df['date']<'2013-01-01']['shock_primary'].sum())} dari {int(df['shock_primary'].sum())})")
print("Porsi HARI pra-2013:",
      f"{100.0*len(df[df['date']<'2013-01-01'])/len(df):.1f}%")

ev = df[df["shock_primary"] | df["shock_fixed"]][
    ["date", "cycle", "zone", "struct", "btc_price", "logret", "vol30_atgate",
     "shock_primary", "shock_fixed", "dd3", "dd5"]].copy()
ev["ret_pct"] = (np.exp(ev["logret"]) - 1) * 100
ev["sigma_mult"] = ev["logret"].abs() / ev["vol30_atgate"]
ev.to_csv(OUT_CSV, index=False)
print(f"\n[saved] {OUT_CSV}  ({len(ev)} baris)")

# ─── Q3b: conditional ladder-jump + daftar hari ekstrem ──────────────────────
line()
print("Q3b LADDER JUMP - kalau rung-1 (58%) tersentuh, seberapa sering langsung lewat 60/62/65%?")
for zs, nm in [(["ZD", "Z3", "Z4"], "K2 window"), (["Z2", "Z2t", "Z3"], "K5 window")]:
    sub = d13[d13["zone"].isin(zs)].dropna(subset=["dd3"])
    dd = sub["dd3"].values
    for cap in (0.45, 0.48):
        base = np.sum(dd <= -(1 - cap / 0.58))
        print(f"  {nm} cap {cap*100:.0f}%: n hari sentuh 58% = {int(base)}")
        for tgt in (0.60, 0.62, 0.65):
            k = np.sum(dd <= -(1 - cap / tgt))
            p = 100.0 * k / base if base else np.nan
            print(f"      -> juga lewat {tgt*100:.0f}%: {int(k)} ({p:.0f}% dari yang sentuh 58%)")

print("\nHari dengan drawdown 3-hari <= -22.4% (lompat 45%->58%) di zona K2 window:")
ext = d13[d13["zone"].isin(["ZD", "Z3", "Z4"]) & (d13["dd3"] <= -0.224)]
print(ext.groupby("cycle").size().to_string())
print(ext[["date", "zone", "btc_price", "dd3"]].assign(dd3=lambda x: (x["dd3"]*100).round(1)).to_string(index=False))

print("\nCross-check klaim framework '92 kejadian turun >=13% dalam <=3 hari' (semua zona, full history):")
allday = df.dropna(subset=["dd3"])
print("  n hari dengan dd3 <= -13%:", int((allday["dd3"] <= -0.13).sum()),
      "| >=2013:", int((allday[allday["date"] >= "2013-01-01"]["dd3"] <= -0.13).sum()))

# episode-merged (cooldown 5 hari) supaya sebanding dengan hitungan "kejadian"
tmp = df.dropna(subset=["dd3"]).copy()
tmp["flag13"] = tmp["dd3"] <= -0.13
tmp = tmp.reset_index(drop=True)
ep = L.event_flags(tmp, "flag13")
print("  setelah merge cooldown 5 hari -> n EPISODE:", int(ep.sum()),
      "| >=2013:", int(ep[(tmp['date'] >= '2013-01-01').values].sum()))
