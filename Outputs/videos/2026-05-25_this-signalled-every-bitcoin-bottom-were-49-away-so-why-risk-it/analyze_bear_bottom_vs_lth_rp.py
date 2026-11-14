"""
VALIDASI 2 - Bear bottom selalu terjadi DI BAWAH LTH Realized Price?

Klaim video (B8), [07:30]-[07:48]: "every single Bitcoin bear market has had its
bottom out occurring beneath this level, and we haven't done that yet"
-> level = LTH Realized Price (lth_cost_basis), ~$48.600 pada 2026-05-25.

CATATAN: pembicara mengangkat klaim ini justru untuk MENOLAK bobotnya. Jadi klaim
ini berdiri melawan bias sumbernya sendiri -> kalau lolos, nilainya tinggi.

House rigor (CLAUDE.md "STANDAR VALIDASI"):
- Definisi event eksplisit (konstanta di bawah, ditetapkan di depan)
- n dilaporkan total + sebaran per cycle
- Anti lookahead: trigger dievaluasi at-gate (nilai hari itu); forward return
  diukur SESUDAH tanggal keputusan. Bagian lead/lag memang memakai tanggal low
  (hindsight) - itu deskriptif, dilabeli eksplisit.
- Independensi sample: hanya 4 bear low terkonfirmasi -> disebut eksplisit
- Data mulai belakangan: lth_cost_basis mulai 2010-07-17 (dilaporkan di output)
- Tidak ada grid search: threshold (a)=1.0, (b)=1.0, (c)=1.05 semuanya diambil
  dari sumber (video / Price Level KB) - tidak dicari-cari

Output: events_bear_bottom_vs_lth_rp.csv, events_bear_bottom_vs_lth_rp_episodes.csv
"""

import pandas as pd
import numpy as np
import os

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = os.path.dirname(os.path.abspath(__file__))

# ---- DEFINISI EVENT (ditetapkan di depan) ----------------------------------
WINDOW_DAYS  = 60    # +-60 hari dari bear low = "bertepatan"
FP_WINDOW    = 90    # +-90 hari: batas untuk menyebut episode "dekat bear low"
EPISODE_GAP  = 30    # gap > 30 hari antar hari trigger = episode baru
TAIL_DAYS    = 180   # perpanjangan era untuk head-to-head versi adil (lihat 4b)

THR_A = 1.00   # (a) Price / LTH RP < 1.0             <- klaim video
THR_B = 1.00   # (b) STH RP / LTH RP < 1.0            <- Price Level KB 4.1
THR_C = 1.05   # (c) Price / CVDD   < 1.05            <- Price Level KB 4.2

BEAR_LOWS = [
    ("Bear 2011", "2011-11-18"),
    ("Bear 2015", "2015-01-14"),
    ("Bear 2018", "2018-12-14"),
    ("Bear 2022", "2022-11-21"),
]
BEAR_LOW_UNCONFIRMED = ("Bear 2025-26 (BELUM KONFIRMASI)", "2026-06-30")

# bear era = [cycle peak .. bear low] -> untuk cari trigger PERTAMA per bear
BEAR_ERAS = [
    ("Bear 2011", "2011-06-08", "2011-11-18"),
    ("Bear 2015", "2013-11-30", "2015-01-14"),
    ("Bear 2018", "2017-12-16", "2018-12-14"),
    ("Bear 2022", "2021-11-08", "2022-11-21"),
    ("Bear 2025-26 (BELUM KONFIRMASI)", "2025-10-06", None),  # ongoing
]

ANCHOR_DATE = "2026-05-25"
NL = "\n"

# ---- Load ------------------------------------------------------------------
df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)

COLS = ["btc_price", "lth_cost_basis", "sth_cost_basis", "cvdd", "realized_price"]
first_dates = {c: df.loc[df[c].notna() & (df[c] > 0), "date"].min() for c in COLS}

print("=" * 100)
print("VALIDASI 2 - BEAR BOTTOM vs LTH REALIZED PRICE")
print("=" * 100)
print(f"Rows total : {len(df)}  ({df.date.min().date()} s/d {df.date.max().date()})")
print(NL + "-- 1. KETERSEDIAAN DATA (menentukan berapa bear yang bisa diuji) --")
for c in COLS:
    print(f"  {c:<18} pertama non-null & >0 : {first_dates[c].date()}   n={int((df[c].notna()&(df[c]>0)).sum())}")

start = max(first_dates.values())
an = df[df["date"] >= start].copy().reset_index(drop=True)
an["ratio_a"] = an["btc_price"] / an["lth_cost_basis"]       # Price / LTH RP
an["ratio_b"] = an["sth_cost_basis"] / an["lth_cost_basis"]  # STH RP / LTH RP
an["ratio_c"] = an["btc_price"] / an["cvdd"]                 # Price / CVDD
print(NL + f"  Rentang analisis : {an.date.min().date()} s/d {an.date.max().date()}  (n={len(an)} hari)")
print("  -> keempat bear low terkonfirmasi (2011/2015/2018/2022) TERCAKUP. Bear pra-2010 tidak ada datanya.")

# ---- Sanity check anchor ----------------------------------------------------
print(NL + "-- SANITY CHECK ANCHOR 2026-05-25 --")
a = an.loc[an.date == ANCHOR_DATE].iloc[0]
for col, exp in [("btc_price", 77172), ("lth_cost_basis", 48650), ("cvdd", 48644),
                 ("sth_cost_basis", 77910), ("realized_price", 54172)]:
    ok = "OK" if abs(a[col] - exp) / exp < 0.01 else "MISMATCH"
    print(f"  {col:<18} = {a[col]:>12,.0f}   (anchor {exp:,})  [{ok}]")

def cycle_of(ts):
    y = ts.year
    if y <= 2012: return "cycle-2011"
    if y <= 2016: return "cycle-2015"
    if y <= 2020: return "cycle-2018"
    if y <= 2024: return "cycle-2022"
    return "cycle-2026"

an["cycle"] = an["date"].apply(cycle_of)

lows_all = BEAR_LOWS + [BEAR_LOW_UNCONFIRMED]
low_conf = [pd.Timestamp(d) for _, d in BEAR_LOWS]
low_all  = [pd.Timestamp(d) for _, d in lows_all]

def near_any(ts, dates, win):
    return any(abs((ts - d).days) <= win for d in dates)

# =============================================================================
# 2. RECALL - rasio Price/LTH RP di tiap bear low
# =============================================================================
print(NL + "=" * 100)
print("2. RECALL - Price / LTH RP di hari bear low + MINIMUM dalam +-60 hari")
print("=" * 100)
rows = []
for name, dstr in lows_all:
    ts = pd.Timestamp(dstr)
    r = an[an.date == ts]
    if r.empty:
        print(f"  {name}: TIDAK ADA DATA"); continue
    r = r.iloc[0]
    w = an[(an.date >= ts - pd.Timedelta(days=WINDOW_DAYS)) &
           (an.date <= ts + pd.Timedelta(days=WINDOW_DAYS))]
    imin = w["ratio_a"].idxmin()
    rows.append({
        "bear": name, "low_date": dstr, "price_at_low": r["btc_price"],
        "lth_rp_at_low": r["lth_cost_basis"],
        "ratio_price_lthrp_at_low": r["ratio_a"],
        "below_lthrp_at_low": bool(r["ratio_a"] < THR_A),
        "min_ratio_pm60d": w["ratio_a"].min(),
        "min_ratio_pm60d_date": an.loc[imin, "date"].date(),
        "below_lthrp_in_pm60d": bool((w["ratio_a"] < THR_A).any()),
        "ratio_sthrp_lthrp_at_low": r["ratio_b"],
        "ratio_price_cvdd_at_low": r["ratio_c"],
    })
    print(f"  {name:<34} low={dstr} price=${r['btc_price']:>10,.0f} LTH_RP=${r['lth_cost_basis']:>10,.0f}"
          f"  ratio={r['ratio_a']:5.3f}  {'DI BAWAH' if r['ratio_a']<THR_A else 'DI ATAS  '}"
          f"  | min+-60d={w['ratio_a'].min():5.3f} @ {an.loc[imin,'date'].date()}"
          f"  {'(pernah di bawah)' if (w['ratio_a']<THR_A).any() else '(TIDAK pernah di bawah)'}")

rec = pd.DataFrame(rows)
n_conf = rec[~rec.bear.str.contains("BELUM")]
print(NL + f"  RECALL di hari low       : {int(n_conf['below_lthrp_at_low'].sum())}/{len(n_conf)} bear low terkonfirmasi")
print(f"  RECALL dalam +-60 hari   : {int(n_conf['below_lthrp_in_pm60d'].sum())}/{len(n_conf)} bear low terkonfirmasi")

# =============================================================================
# 3. FALSE POSITIVE - semua hari Price < LTH RP, dikelompokkan jadi episode
# =============================================================================
print(NL + "=" * 100)
print("3. FALSE POSITIVE - total hari Price < LTH RP, dikelompokkan jadi episode (gap >30d)")
print("=" * 100)

trig = an[an["ratio_a"] < THR_A].copy().reset_index(drop=True)
print(f"  Total hari Price < LTH RP : n={len(trig)}  ({len(trig)/len(an)*100:.2f}% dari {len(an)} hari)")
print("  Sebaran per cycle:")
for c, g in trig.groupby("cycle"):
    print(f"    {c:<12} n={len(g):>4}   {g.date.min().date()} .. {g.date.max().date()}")

grp = (trig["date"].diff().dt.days.fillna(999) > EPISODE_GAP).cumsum()
ep_rows = []
for g, sub in trig.groupby(grp):
    s, e = sub["date"].min(), sub["date"].max()
    imin = sub["ratio_a"].idxmin()
    # jarak episode ke bear low terdekat: jarak MINIMUM antara rentang episode dan
    # tanggal low (0 kalau low jatuh di dalam rentang episode)
    def dist(d, s=s, e=e):
        if s <= d <= e: return 0
        return min(abs((s - d).days), abs((e - d).days))
    dc = min((dist(d), nm) for nm, d in [(n, pd.Timestamp(x)) for n, x in BEAR_LOWS])
    da = min((dist(d), nm) for nm, d in [(n, pd.Timestamp(x)) for n, x in lows_all])
    ep_rows.append({
        "ep_start": s.date(), "ep_end": e.date(), "days": len(sub),
        "min_ratio": sub["ratio_a"].min(), "min_ratio_date": sub.loc[imin, "date"].date(),
        "price_min": sub["btc_price"].min(),
        "nearest_conf_low": dc[1], "dist_days_conf": dc[0],
        "near90_conf": dc[0] <= FP_WINDOW,
        "nearest_any_low": da[1], "dist_days_any": da[0],
        "near90_any": da[0] <= FP_WINDOW,
    })
ep = pd.DataFrame(ep_rows)
print(NL + f"  Jumlah episode: {len(ep)}")
print(f"  {'Episode':<26}{'hari':>6}{'min ratio':>11}   {'bear low terdekat (terkonfirmasi)':<38}{'jarak':>8}  dalam +-90d?")
for _, r in ep.iterrows():
    print(f"  {str(r['ep_start'])+' .. '+str(r['ep_end']):<26}{int(r['days']):>6}{r['min_ratio']:>11.3f}   "
          f"{r['nearest_conf_low']:<38}{int(r['dist_days_conf']):>6}d  {'YA' if r['near90_conf'] else 'TIDAK <-- FALSE POSITIVE'}")

fp_conf = int((~ep["near90_conf"]).sum())
print(NL + f"  Episode yang TIDAK dalam +-90 hari bear low terkonfirmasi : {fp_conf} dari {len(ep)}")
print(f"  Episode yang TIDAK dalam +-90 hari bear low manapun (+2026): {int((~ep['near90_any']).sum())} dari {len(ep)}")
tr_near = trig["date"].apply(lambda t: near_any(t, low_conf, WINDOW_DAYS))
print(f"  Precision level-hari (4 bear terkonfirmasi, +-{WINDOW_DAYS}d): {tr_near.mean()*100:.1f}%  ({int(tr_near.sum())}/{len(trig)})")

# --- Biaya praktis false positive: forward return dari AWAL tiap episode -----
# (anti lookahead: keputusan diambil di ep_start, return diukur SESUDAHNYA)
print(NL + "  -- Biaya praktis: forward return dari HARI PERTAMA tiap episode (at-gate) --")
px = an.set_index("date")["btc_price"]
for h in (90, 180, 365):
    vals = []
    for _, r in ep.iterrows():
        d0 = pd.Timestamp(r["ep_start"]); d1 = d0 + pd.Timedelta(days=h)
        if d1 > an["date"].max():
            vals.append(np.nan); continue
        vals.append((px.asof(d1) / px.asof(d0) - 1) * 100)
    ep[f"fwd_{h}d_pct"] = vals
print(f"  {'Episode mulai':<16}{'fwd90d':>10}{'fwd180d':>10}{'fwd365d':>10}   status")
fmt = lambda x: f"{x:+.1f}%" if pd.notna(x) else "n/a"
for _, r in ep.iterrows():
    st = "dekat bear low" if r["near90_conf"] else "FALSE POSITIVE (jarak >90d)"
    print(f"  {str(r['ep_start']):<16}{fmt(r['fwd_90d_pct']):>10}{fmt(r['fwd_180d_pct']):>10}{fmt(r['fwd_365d_pct']):>10}   {st}")

# =============================================================================
# 4. HEAD-TO-HEAD dengan rule established framework
# =============================================================================
print(NL + "=" * 100)
print("4. HEAD-TO-HEAD - trigger PERTAMA per bear era (at-gate, sejak cycle peak)")
print("=" * 100)
print("  (a) Price / LTH RP  < 1.00   [klaim video]")
print("  (b) STH RP / LTH RP < 1.00   [Price Level KB 4.1 - nol false positive 10 thn]")
print("  (c) Price / CVDD    < 1.05   [Price Level KB 4.2 - 6/6]" + NL)

RULES = [("a_price_lt_lthrp", "ratio_a", THR_A),
         ("b_sthrp_lt_lthrp", "ratio_b", THR_B),
         ("c_price_cvdd_lt105", "ratio_c", THR_C)]

def first_triggers(w):
    out = {}
    for rname, col, thr in RULES:
        t = w[w[col] < thr]["date"]
        out[rname] = t.min() if not t.empty else pd.NaT
    return out

h2h_rows = []
for (bname, s, e), (lname, ldate) in zip(BEAR_ERAS, lows_all):
    s = pd.Timestamp(s)
    low = pd.Timestamp(ldate)
    e_end = an["date"].max() if e is None else pd.Timestamp(e)
    w = an[(an.date >= s) & (an.date <= min(e_end, an["date"].max()))]
    firsts = first_triggers(w)
    rec_r = {"bear": bname, "era_start": s.date(), "low_date": ldate}
    for rname, _, _ in RULES:
        f = firsts[rname]
        rec_r[f"first_{rname}"] = f.date() if pd.notna(f) else None
        rec_r[f"lead_days_{rname}"] = (low - f).days if pd.notna(f) else None
    got = sorted([(k, v) for k, v in firsts.items() if pd.notna(v)], key=lambda x: x[1])
    rec_r["order"] = " -> ".join(k.split("_")[0] for k, _ in got) if got else "(tidak ada trigger)"
    for other in ["b_sthrp_lt_lthrp", "c_price_cvdd_lt105"]:
        key = f"a_minus_{other.split('_')[0]}_days"
        if pd.notna(firsts["a_price_lt_lthrp"]) and pd.notna(firsts[other]):
            rec_r[key] = (firsts[other] - firsts["a_price_lt_lthrp"]).days
        else:
            rec_r[key] = None

    # --- 4b: versi ADIL untuk pesaing - era diperpanjang ke low + 180 hari ---
    # Alasan: Price Level KB mencatat STH/LTH<1.0 terjadi Jan-Mei 2019 (SETELAH
    # low 2018). Kalau era dipotong tepat di low, rule (b) otomatis "tidak pernah
    # trigger" - itu tidak adil ke pesaing. Versi ini melaporkan keduanya.
    e_ext = min(low + pd.Timedelta(days=TAIL_DAYS), an["date"].max())
    w2 = an[(an.date >= s) & (an.date <= e_ext)]
    f2 = first_triggers(w2)
    for rname, _, _ in RULES:
        f = f2[rname]
        rec_r[f"ext_first_{rname}"] = f.date() if pd.notna(f) else None
        rec_r[f"ext_lead_days_{rname}"] = (low - f).days if pd.notna(f) else None
    h2h_rows.append(rec_r)

    print(f"  {bname}  (era {s.date()} .. {low.date()};  era diperpanjang s/d {e_ext.date()})")
    for rname, _, _ in RULES:
        f, fe = firsts[rname], f2[rname]
        ld = (low - f).days if pd.notna(f) else None
        lde = (low - fe).days if pd.notna(fe) else None
        print(f"     {rname:<20} era ketat : {str(f.date()) if pd.notna(f) else 'TIDAK PERNAH':<12} lead {str(ld)+'d' if ld is not None else '-':>7}"
              f"   | era +180d: {str(fe.date()) if pd.notna(fe) else 'TIDAK PERNAH':<12} lead {str(lde)+'d' if lde is not None else '-':>7}")
    print(f"     URUTAN (era ketat): {rec_r['order']}")
    da, dc_ = rec_r["a_minus_b_days"], rec_r["a_minus_c_days"]
    def desc(d):
        if d is None: return "tidak bisa dibanding"
        if d > 0: return f"a duluan {d}d"
        if d == 0: return "sama hari"
        return f"a telat {-d}d"
    print(f"     a vs b: {desc(da)}   | a vs c: {desc(dc_)}" + NL)

h2h = pd.DataFrame(h2h_rows)

print("  RINGKAS (hanya 4 bear terkonfirmasi):")
h4 = h2h[~h2h.bear.str.contains("BELUM")]
for lbl, pre in [("era ketat [peak..low]", "first_"), (f"era +{TAIL_DAYS}d [peak..low+{TAIL_DAYS}d]", "ext_first_")]:
    na = h4[pre + "a_price_lt_lthrp"].notna().sum()
    nb = h4[pre + "b_sthrp_lt_lthrp"].notna().sum()
    nc = h4[pre + "c_price_cvdd_lt105"].notna().sum()
    print(f"    {lbl:<34} -> (a) trigger di {na}/4 bear   (b) {nb}/4   (c) {nc}/4")

print(NL + f"  URUTAN dengan era diperpanjang +{TAIL_DAYS}d (versi paling adil untuk pesaing):")
cnt_a_first = 0
for _, r in h4.iterrows():
    tri = [(k.replace("ext_first_", "").split("_")[0], r[k])
           for k in ["ext_first_a_price_lt_lthrp", "ext_first_b_sthrp_lt_lthrp", "ext_first_c_price_cvdd_lt105"]
           if r[k] is not None]
    tri.sort(key=lambda x: x[1])
    if tri and tri[0][0] == "a":
        cnt_a_first += 1
    print(f"    {r['bear']:<12} {' -> '.join(f'{n}({d})' for n, d in tri)}")
print(NL + f"    (a) Price<LTH RP jadi trigger PERTAMA di {cnt_a_first}/4 bear era")

# =============================================================================
# 4c. INDEPENDENSI BASIS - apakah (a) benar-benar basis ketiga yang berbeda?
# =============================================================================
print(NL + "=" * 100)
print("4c. INDEPENDENSI BASIS - overlap & korelasi antar rule (a), (b), (c)")
print("=" * 100)
ma = an["ratio_a"] < THR_A
mb = an["ratio_b"] < THR_B
mc = an["ratio_c"] < THR_C
print(f"  Hari trigger: (a) n={int(ma.sum())}   (b) n={int(mb.sum())}   (c) n={int(mc.sum())}   dari {len(an)} hari")
print(f"  Spearman level harian: rho(a,b) = {an['ratio_a'].corr(an['ratio_b'], method='spearman'):.3f}"
      f"   rho(a,c) = {an['ratio_a'].corr(an['ratio_c'], method='spearman'):.3f}")
print(f"  Overlap (c) di dalam (a) : {int((ma&mc).sum())}/{int(mc.sum())} hari = {(ma&mc).sum()/max(mc.sum(),1)*100:.1f}%"
      f"   -> {'(c) SUBSET PENUH dari (a)' if (ma&mc).sum()==mc.sum() else 'sebagian'}")
print(f"  Overlap (b) di dalam (a) : {int((ma&mb).sum())}/{int(mb.sum())} hari = {(ma&mb).sum()/max(mb.sum(),1)*100:.1f}%")
lr = an["lth_cost_basis"] / an["cvdd"]
print(f"  LTH RP / CVDD sepanjang sejarah: median {lr.median():.2f}  (hari terakhir {lr.iloc[-1]:.3f})")
print("  -> (a) & (b) berbagi penyebut LTH RP; (c) seluruhnya termuat di dalam (a).")
print("     Artinya (a) bukan basis ke-3 independen, melainkan SELUBUNG KASAR yang lebih luas & lebih dini.")

# =============================================================================
# 5. KONDISI SEKARANG
# =============================================================================
print(NL + "=" * 100)
print("5. KONDISI SEKARANG")
print("=" * 100)
for dstr in [ANCHOR_DATE, str(an["date"].max().date())]:
    r = an[an.date == dstr].iloc[0]
    print(f"  {dstr}:  price=${r['btc_price']:>10,.0f}  LTH_RP=${r['lth_cost_basis']:>10,.0f}"
          f"  Price/LTH_RP={r['ratio_a']:5.3f}   STH/LTH={r['ratio_b']:5.3f}   Price/CVDD={r['ratio_c']:5.3f}")
    need = r["lth_cost_basis"] / r["btc_price"] - 1
    print(f"     -> agar Price < LTH RP butuh harga turun {abs(need)*100:.1f}% (ke ${r['lth_cost_basis']:,.0f})")
b26 = an[an.date >= "2025-10-06"]
i = b26["ratio_a"].idxmin()
print(f"  Minimum Price/LTH RP sepanjang bear 2025-26 sejauh ini: {b26['ratio_a'].min():.3f} @ {an.loc[i,'date'].date()}"
      f"  (price ${an.loc[i,'btc_price']:,.0f})")

# =============================================================================
# SIMPAN CSV
# =============================================================================
out = os.path.join(OUTDIR, "events_bear_bottom_vs_lth_rp.csv")
rec.merge(h2h, on=["bear"], how="outer").to_csv(out, index=False)
print(NL + f"CSV event disimpan  : {out}")

out2 = os.path.join(OUTDIR, "events_bear_bottom_vs_lth_rp_episodes.csv")
ep.to_csv(out2, index=False)
print(f"CSV episode disimpan: {out2}")
print(NL + "SELESAI.")
