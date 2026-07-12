"""
Validasi Insight A — "Demand Momentum" (On-Chain Mind, video 2025-01-27)

Definisi video (footnote chart CryptoQuant):
  DM = (30-day change in Short-term Supply) - (30-day change in Long-term Supply)
Kita replikasi pakai cutoff 155-hari Glassnode (sth_supply_btc / lth_supply_btc).

Uji:
  [1] Hitung DM full history.
  [2] Dekomposisi: korelasi DM vs 2*delta30(STH supply). Kalau ~1 -> redundant.
  [3] Gate test di Z3-Z4: forward return 30/60/90d saat DM "collapsed"
      (turun >80% dari local peak 90d) vs saat DM "rebound".
      - collapsed(t): peak90(t) > 0 dan DM(t) < 0.20 * peak90(t)
        (peak90 = rolling max 90d, window BERAKHIR di t -> at-gate, no lookahead)
      - rebound(t): bukan collapsed DAN DM(t) > DM(t-14) (momentum naik)
      Event-level: hari PERTAMA masuk state collapsed, cooldown 90d antar event.
  [4] False negative klaim "tanpa rebound momentum harga sulit naik":
      episode rally >=20% dalam 90d ke depan yang DIMULAI saat DM flat/negatif
      (DM <= 0) ATAU saat DM collapsed. Merge: hari-hari kualifikasi berjarak
      <=30d dianggap satu episode.

Zona (ikut pola framework / data_dictionary):
  AVIV Upper = price_at_aviv_mean + 0.5*(price_at_aviv_plus_1_sigma - price_at_aviv_mean)
  Z3: RP <= price < AVIV Mean ; Z4: AVIV Mean <= price < AVIV Upper

Cycle split (untuk sebaran n):
  c2013: <=2015-01-14 | c2017: ..2018-12-15 | c2021: ..2022-11-21 | c2024: sesudahnya
"""
import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Video-Breakdown\Outputs\2025-01-27_bitcoin-whales-are-accumulating-right-now"

df = pd.read_csv(MASTER, parse_dates=["date"], usecols=[
    "date","btc_price","sth_supply_btc","lth_supply_btc","realized_price",
    "price_at_aviv_mean","price_at_aviv_plus_1_sigma"])
df = df.sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price","sth_supply_btc","lth_supply_btc"]).reset_index(drop=True)
df = df[df["btc_price"] > 0.1].reset_index(drop=True)

# ── [1] Demand Momentum ──────────────────────────────────────────────────────
df["d30_sth"] = df["sth_supply_btc"] - df["sth_supply_btc"].shift(30)
df["d30_lth"] = df["lth_supply_btc"] - df["lth_supply_btc"].shift(30)
df["dm"]      = df["d30_sth"] - df["d30_lth"]

# ── [2] Dekomposisi ──────────────────────────────────────────────────────────
v = df.dropna(subset=["dm"])
corr_2x  = np.corrcoef(v["dm"], 2*v["d30_sth"])[0,1]
corr_1x  = np.corrcoef(v["dm"], v["d30_sth"])[0,1]
# total supply STH+LTH dan issuance 30d implisit
df["tot_supply"] = df["sth_supply_btc"] + df["lth_supply_btc"]
df["d30_tot"]    = df["tot_supply"] - df["tot_supply"].shift(30)
v2 = df.dropna(subset=["dm","d30_tot"])
resid = v2["dm"] - (2*v2["d30_sth"] - v2["d30_tot"])
print("="*100)
print("[2] DEKOMPOSISI")
print(f"  corr(DM, 2*d30_STH)          = {corr_2x:.6f}")
print(f"  corr(DM,   d30_STH)          = {corr_1x:.6f}")
print(f"  identitas DM = 2*d30_STH - d30_total : max|resid| = {resid.abs().max():.6f} BTC")
print(f"  d30_total (issuance 30d) range: {v2['d30_tot'].min():,.0f} .. {v2['d30_tot'].max():,.0f} BTC")

# ── Zona ─────────────────────────────────────────────────────────────────────
df["aviv_upper"] = df["price_at_aviv_mean"] + 0.5*(df["price_at_aviv_plus_1_sigma"] - df["price_at_aviv_mean"])
df["z3"] = (df["btc_price"] >= df["realized_price"]) & (df["btc_price"] < df["price_at_aviv_mean"])
df["z4"] = (df["btc_price"] >= df["price_at_aviv_mean"]) & (df["btc_price"] < df["aviv_upper"])
df["z34"] = df["z3"] | df["z4"]

def cycle_of(d):
    if d <= pd.Timestamp("2015-01-14"): return "c2013"
    if d <= pd.Timestamp("2018-12-15"): return "c2017"
    if d <= pd.Timestamp("2022-11-21"): return "c2021"
    return "c2024"
df["cycle"] = df["date"].apply(cycle_of)

# ── Forward returns (untuk evaluasi, bukan untuk keputusan) ──────────────────
for h in (30, 60, 90):
    df[f"fwd{h}"] = df["btc_price"].shift(-h) / df["btc_price"] - 1
df["fwd90_max"] = df["btc_price"][::-1].rolling(90, min_periods=90).max()[::-1].shift(-1) / df["btc_price"] - 1
# fwd90_max = max return dalam 90 hari ke depan (t+1..t+90)

# ── [3] State collapsed vs rebound di Z3-Z4 ─────────────────────────────────
df["peak90"] = df["dm"].rolling(90, min_periods=90).max()   # window berakhir di t (at-gate)
df["collapsed"] = (df["peak90"] > 0) & (df["dm"] < 0.20*df["peak90"])
df["rebound"]   = (~df["collapsed"]) & (df["dm"] > df["dm"].shift(14))

print("\n" + "="*100)
print("[3] DAY-LEVEL: forward return di Z3-Z4, state DM collapsed vs rebound")
print("    (hari-hari berurutan TIDAK independen - lihat event-level di bawah)")
sub = df[df["z34"] & df["fwd90"].notna() & df["peak90"].notna()]
for state, mask in [("COLLAPSED", sub["collapsed"]), ("REBOUND", sub["rebound"])]:
    s = sub[mask]
    print(f"\n  state={state}  n_hari={len(s)}  sebaran cycle: {s['cycle'].value_counts().to_dict()}")
    for h in (30,60,90):
        r = s[f"fwd{h}"]
        print(f"    fwd{h}d: median={r.median()*100:+.1f}%  mean={r.mean()*100:+.1f}%  %positif={(r>0).mean()*100:.0f}%")

# Event-level: hari pertama masuk collapsed di Z3-Z4, cooldown 90d
events = []
last_ev = None
prev_col = False
for i, row in df.iterrows():
    c = bool(row["collapsed"]) if pd.notna(row["peak90"]) else False
    if c and not prev_col and row["z34"]:
        if last_ev is None or (row["date"] - last_ev).days > 90:
            events.append(i); last_ev = row["date"]
    prev_col = c
ev = df.loc[events, ["date","cycle","btc_price","dm","peak90","fwd30","fwd60","fwd90","fwd90_max"]].copy()
print("\n  EVENT-LEVEL: entry ke state collapsed saat di Z3-Z4 (cooldown 90d)")
print(f"  n_event={len(ev)}  sebaran: {ev['cycle'].value_counts().to_dict()}")
for _, r in ev.iterrows():
    print(f"    {r['date'].date()}  [{r['cycle']}] px=${r['btc_price']:>9,.0f}  DM={r['dm']:>10,.0f} (peak90={r['peak90']:>10,.0f})"
          f"  fwd30={r['fwd30']*100:+6.1f}%  fwd60={r['fwd60']*100:+6.1f}%  fwd90={r['fwd90']*100:+6.1f}%  max90={r['fwd90_max']*100:+6.1f}%")
print(f"  median fwd30/60/90: {ev['fwd30'].median()*100:+.1f}% / {ev['fwd60'].median()*100:+.1f}% / {ev['fwd90'].median()*100:+.1f}%")

# Baseline: SEMUA hari Z3-Z4
base = df[df["z34"] & df["fwd90"].notna()]
print(f"\n  BASELINE semua hari Z3-Z4 (n={len(base)}): "
      f"median fwd30={base['fwd30'].median()*100:+.1f}%  fwd60={base['fwd60'].median()*100:+.1f}%  fwd90={base['fwd90'].median()*100:+.1f}%")

# ── [4] False negative: rally >=20%/90d yang mulai saat DM flat/negatif ─────
print("\n" + "="*100)
print("[4] FALSE NEGATIVE TEST: rally >=20% (max dalam 90d ke depan) mulai saat DM <= 0")
def rally_episodes(mask_start, label):
    """mask_start: kondisi DM di hari t. Episode = hari dgn fwd90_max>=20% & kondisi,
       merge kalau jarak antar hari kualifikasi <=30d."""
    q = df[(df["fwd90_max"] >= 0.20) & mask_start & df["dm"].notna() & df["fwd90_max"].notna()]
    eps = []
    last = None
    for d in q["date"]:
        if last is None or (d - last).days > 30:
            eps.append(d)
        last = d
    print(f"\n  Kondisi start: {label}  ->  n_episode={len(eps)}")
    bycycle = {}
    for d in eps:
        bycycle.setdefault(cycle_of(d), []).append(d)
    for c, ds in bycycle.items():
        print(f"    {c} ({len(ds)}): " + ", ".join(x.strftime("%Y-%m-%d") for x in ds))
    return eps

eps_neg  = rally_episodes(df["dm"] <= 0, "DM <= 0 (flat/negatif)")
eps_col  = rally_episodes(df["collapsed"].fillna(False), "DM collapsed (>80% di bawah peak90)")
eps_neg34 = rally_episodes((df["dm"] <= 0) & df["z34"], "DM <= 0 DAN di Z3-Z4")

# pembanding: episode rally total (tanpa syarat DM)
eps_all = rally_episodes(pd.Series(True, index=df.index), "TANPA syarat DM (semua rally)")
print(f"\n  Rasio: {len(eps_neg)}/{len(eps_all)} episode rally dimulai saat DM<=0 "
      f"= {len(eps_neg)/max(len(eps_all),1)*100:.0f}%")

# simpan tabel event
ev.to_csv(rf"{OUTDIR}\events_demand_momentum_collapsed.csv", index=False)
print("\nSaved: events_demand_momentum_collapsed.csv")
