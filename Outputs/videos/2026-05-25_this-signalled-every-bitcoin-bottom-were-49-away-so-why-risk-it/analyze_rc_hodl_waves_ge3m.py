"""
VALIDASI 1 — Realized Cap HODL Waves, agregat band umur >= 3 bulan (rc_ge3m)

Klaim video (B1): rc_ge3m ~84% sekarang; setiap kali level ini tercapai historically
                  bertepatan dengan bear market low ("practically every single time").
Klaim turunan (B2): kebalikannya (band <3m spiking) = bull market peak.
                  Seri yang SAMA dibaca dua arah: rc_lt3m = 100 - rc_ge3m.
Byproduct  (B3): nilai puncak rc_ge3m per bear -> cek klaim "4.9% away".

JEBAKAN: kolom realized_cap_1w & realized_cap_1_2y adalah input RHODL, nilainya
DUPLIKAT dari realized_cap_1d-1w & realized_cap_1y-2y. TIDAK dipakai di sini.

House rigor:
- Definisi event eksplisit (lihat konstanta di bawah)
- n dilaporkan total + per cycle
- Anti lookahead: percentile rolling dihitung trailing-only (window berakhir di hari itu)
- Independensi sample: sebaran per cycle dilaporkan
- Data mulai belakangan: seri harga baru mulai 2010-07-17 -> bear 2011 tercakup, bear
  pra-2011 tidak ada
- Tidak ada grid search threshold: 84 diambil dari video, alternatif relatif p95/4y
  ditetapkan a priori (hanya 2 varian dibandingkan)

Output: findings_rc_hodl_waves_ge3m.md (ditulis manual), events_rc_hodl_waves_ge3m.csv
"""

import pandas as pd
import numpy as np
import os

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = os.path.dirname(os.path.abspath(__file__))

# ---- DEFINISI EVENT (ditetapkan di depan) ----------------------------------
THRESH_ABS   = 84.0     # threshold absolut dari video
PCTL_WIN     = 1461     # 4 tahun kalender (rolling, trailing-only)
PCTL_LEVEL   = 95.0     # aturan relatif a priori
WINDOW_DAYS  = 60       # +-60 hari dari bear low = "bertepatan"
FP_WINDOW    = 90       # untuk pengelompokan episode
EPISODE_GAP  = 30       # gap > 30 hari antar hari-trigger = episode baru

BEAR_LOWS = [
    ("Bear 2011",    "2011-11-18"),
    ("Bear 2015",    "2015-01-14"),
    ("Bear 2018",    "2018-12-14"),
    ("Bear 2022",    "2022-11-21"),
]
BEAR_LOW_UNCONFIRMED = ("Bear 2025-26 (BELUM KONFIRMASI)", "2026-06-30")

CYCLE_PEAKS = [
    ("Peak 2011", "2011-06-08"),
    ("Peak 2013", "2013-11-30"),
    ("Peak 2017", "2017-12-16"),
    ("Peak 2021", "2021-11-08"),
    ("Peak 2025", "2025-10-06"),
]

# bear era = [cycle peak, bear low + 180d]  -> untuk max rc_ge3m per bear
BEAR_ERAS = [
    ("Bear 2011", "2011-06-08", "2011-11-18"),
    ("Bear 2015", "2013-11-30", "2015-01-14"),
    ("Bear 2018", "2017-12-16", "2018-12-14"),
    ("Bear 2022", "2021-11-08", "2022-11-21"),
    ("Bear 2025-26", "2025-10-06", None),   # ongoing
]

BANDS_LT3M = ["realized_cap_0-1d", "realized_cap_1d-1w",
              "realized_cap_1w-1m", "realized_cap_1m-3m"]

# ---- Load ------------------------------------------------------------------
df = pd.read_csv(MASTER, parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)

first_nonnull = df.loc[df[BANDS_LT3M].notna().all(axis=1), "date"].min()
first_price   = df.loc[df["btc_price"].notna() & (df["btc_price"] > 0), "date"].min()

df["rc_lt3m"] = df[BANDS_LT3M].sum(axis=1)
df["rc_ge3m"] = 100.0 - df["rc_lt3m"]

# sanity: semua band harus jumlah 100
ALL_BANDS = [c for c in df.columns if c.startswith("realized_cap_")
             and c not in ("realized_cap_1w", "realized_cap_1_2y", "realized_cap_usd",
                           "lth_realized_cap_usd", "sth_realized_cap_usd")]
rowsum = df[ALL_BANDS].sum(axis=1)

print("=" * 100)
print("VALIDASI 1 - RC HODL WAVES >=3M")
print("=" * 100)
print(f"Rows total            : {len(df)}  ({df.date.min().date()} s/d {df.date.max().date()})")
print(f"Band rc pertama non-null : {first_nonnull.date()}")
print(f"Harga BTC pertama > 0    : {first_price.date()}")
print(f"Band dipakai (12)        : {len(ALL_BANDS)} kolom, sum-per-baris min={rowsum.min():.4f} max={rowsum.max():.4f}")
print(f"  (realized_cap_1w & realized_cap_1_2y SENGAJA dikeluarkan - duplikat input RHODL)")

# Analisis dibatasi ke era harga tersedia
an = df[df["date"] >= first_price].copy().reset_index(drop=True)
print(f"Rentang analisis         : {an.date.min().date()} s/d {an.date.max().date()}  (n={len(an)} hari)")

# ---- Sanity check ke angka anchor ------------------------------------------
print("\n-- SANITY CHECK ANCHOR --")
for d, expect in [("2026-05-25", 83.63), ("2026-06-21", 84.22)]:
    v = an.loc[an.date == d, "rc_ge3m"].iloc[0]
    ok = "OK" if abs(v - expect) < 0.05 else "MISMATCH"
    print(f"  {d}: rc_ge3m = {v:.3f}%   (anchor {expect})  [{ok}]")
last = an.iloc[-1]
print(f"  Hari terakhir data {last.date.date()}: rc_ge3m = {last.rc_ge3m:.3f}%, price=${last.btc_price:,.0f}")

# ---- Rolling percentile (trailing-only, anti lookahead) ---------------------
an["pctl_4y"] = an["rc_ge3m"].rolling(PCTL_WIN, min_periods=365).apply(
    lambda w: (w <= w[-1]).mean() * 100.0, raw=True)

# ---- Helper ----------------------------------------------------------------
lows_all = BEAR_LOWS + [BEAR_LOW_UNCONFIRMED]
low_dates_conf = [pd.Timestamp(d) for _, d in BEAR_LOWS]
low_dates_all  = [pd.Timestamp(d) for _, d in lows_all]

def near_any(ts, dates, win):
    return any(abs((ts - d).days) <= win for d in dates)

def cycle_of(ts):
    y = ts.year
    if y <= 2012: return "cycle-2011"
    if y <= 2016: return "cycle-2015"
    if y <= 2020: return "cycle-2018"
    if y <= 2024: return "cycle-2022"
    return "cycle-2026"

an["cycle"] = an["date"].apply(cycle_of)

# =============================================================================
# 2. PRECISION
# =============================================================================
print("\n" + "=" * 100)
print("2. PRECISION - dari semua hari rc_ge3m >= 84, berapa % dalam +-60 hari bear low?")
print("=" * 100)

def precision_report(mask, label):
    hits = an[mask].copy()
    n = len(hits)
    if n == 0:
        print(f"{label}: n=0 hari trigger")
        return None
    hits["near_conf"] = hits["date"].apply(lambda t: near_any(t, low_dates_conf, WINDOW_DAYS))
    hits["near_all"]  = hits["date"].apply(lambda t: near_any(t, low_dates_all, WINDOW_DAYS))
    p_conf = hits["near_conf"].mean() * 100
    p_all  = hits["near_all"].mean() * 100
    print(f"\n{label}")
    print(f"  Total hari trigger n = {n}  ({n/len(an)*100:.1f}% dari {len(an)} hari)")
    print(f"  Precision (4 bear low terkonfirmasi)              : {p_conf:.1f}%  ({hits['near_conf'].sum()}/{n})")
    print(f"  Precision (+ low sementara 2026-06-30, unconfirmed): {p_all:.1f}%  ({hits['near_all'].sum()}/{n})")
    print("  Sebaran hari trigger per cycle:")
    for c, g in hits.groupby("cycle"):
        print(f"    {c:<12} n={len(g):>5}  ({g.date.min().date()} .. {g.date.max().date()})  "
              f"dalam +-60d bear low: {g['near_conf'].sum()}")
    return hits

hits_abs = precision_report(an["rc_ge3m"] >= THRESH_ABS, f"[A] Threshold ABSOLUT rc_ge3m >= {THRESH_ABS}")
hits_rel = precision_report(an["pctl_4y"] >= PCTL_LEVEL, f"[B] Aturan RELATIF percentile 4y (trailing) >= {PCTL_LEVEL}")

# episode grouping untuk threshold absolut
def to_episodes(hits):
    if hits is None or hits.empty:
        return pd.DataFrame()
    d = hits["date"].reset_index(drop=True)
    grp = (d.diff().dt.days.fillna(999) > EPISODE_GAP).cumsum()
    rows = []
    for g, idx in d.groupby(grp).groups.items():
        sub = hits.iloc[[hits.index.get_loc(i) for i in hits.index[idx]]] if False else hits.loc[hits["date"].isin(d[idx])]
        rows.append({
            "start": sub["date"].min(), "end": sub["date"].max(),
            "days": len(sub),
            "max_rc_ge3m": sub["rc_ge3m"].max(),
            "price_start": sub["btc_price"].iloc[0],
        })
    return pd.DataFrame(rows)

ep_abs = to_episodes(hits_abs)
print("\n-- EPISODE (gap >30 hari = episode baru), threshold absolut 84 --")
if not ep_abs.empty:
    for _, r in ep_abs.iterrows():
        nearest = min(((abs((r["start"] - d).days), nm) for nm, d in
                       [(n, pd.Timestamp(x)) for n, x in lows_all]))
        print(f"  {r['start'].date()} .. {r['end'].date()}  ({int(r['days']):>4}d)  "
              f"max={r['max_rc_ge3m']:.2f}%  bear-low terdekat dari AWAL episode: {nearest[1]} ({nearest[0]}d)")

# =============================================================================
# 3. RECALL
# =============================================================================
print("\n" + "=" * 100)
print("3. RECALL - nilai rc_ge3m di tiap bear low + persentilnya")
print("=" * 100)
recall_rows = []
for name, dstr in lows_all:
    ts = pd.Timestamp(dstr)
    row = an[an.date == ts]
    if row.empty:
        print(f"  {name}: TIDAK ADA DATA")
        continue
    row = row.iloc[0]
    v = row["rc_ge3m"]
    pct_full = (an["rc_ge3m"] <= v).mean() * 100                   # full history (ada lookahead - dilabeli)
    hist = an[an.date <= ts]
    pct_atgate = (hist["rc_ge3m"] <= v).mean() * 100               # at-gate, no lookahead
    w = an[(an.date >= ts - pd.Timedelta(days=WINDOW_DAYS)) & (an.date <= ts + pd.Timedelta(days=WINDOW_DAYS))]
    recall_rows.append({
        "bear": name, "low_date": dstr, "price_at_low": row["btc_price"],
        "rc_ge3m_at_low": v, "pctl_full_history": pct_full, "pctl_at_gate": pct_atgate,
        "rc_ge3m_max_pm60d": w["rc_ge3m"].max(),
        "hit_thresh84_at_low": v >= THRESH_ABS,
        "hit_thresh84_in_pm60d": (w["rc_ge3m"] >= THRESH_ABS).any(),
        "pctl_4y_at_low": row["pctl_4y"],
    })
    print(f"  {name:<34} low={dstr}  price=${row['btc_price']:>10,.0f}  rc_ge3m={v:6.2f}%  "
          f"pctl(full)={pct_full:5.1f}  pctl(at-gate)={pct_atgate:5.1f}  "
          f"max+-60d={w['rc_ge3m'].max():6.2f}%  >=84 di hari low? {'YA' if v>=THRESH_ABS else 'TIDAK'}")
rec = pd.DataFrame(recall_rows)

# =============================================================================
# 4. DRIFT STRUKTURAL
# =============================================================================
print("\n" + "=" * 100)
print("4. DRIFT STRUKTURAL - puncak rc_ge3m per bear era [cycle peak .. bear low]")
print("=" * 100)
drift_rows = []
for name, s, e in BEAR_ERAS:
    s = pd.Timestamp(s)
    e = pd.Timestamp(e) if e else an["date"].max()
    w = an[(an.date >= s) & (an.date <= e)]
    if w.empty:
        print(f"  {name}: tidak ada data (mulai {an.date.min().date()})")
        drift_rows.append({"bear": name, "era_start": s.date(), "era_end": e.date(),
                           "peak_rc_ge3m": np.nan, "peak_date": None, "n_days": 0})
        continue
    i = w["rc_ge3m"].idxmax()
    drift_rows.append({"bear": name, "era_start": s.date(), "era_end": e.date(),
                       "peak_rc_ge3m": w.loc[i, "rc_ge3m"], "peak_date": w.loc[i, "date"].date(),
                       "n_days": len(w)})
    print(f"  {name:<14} era {s.date()} .. {e.date()} (n={len(w)}d)  "
          f"PUNCAK rc_ge3m = {w.loc[i,'rc_ge3m']:.2f}%  pada {w.loc[i,'date'].date()}")
dr = pd.DataFrame(drift_rows)
vals = dr.dropna(subset=["peak_rc_ge3m"])["peak_rc_ge3m"].tolist()
mono = all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))
print(f"\n  Urutan puncak: {[round(v,2) for v in vals]}")
print(f"  Naik monoton antar cycle? {'YA -> threshold absolut drift, gugur' if mono else 'TIDAK'}")

# =============================================================================
# 5. LEAD/LAG
# =============================================================================
print("\n" + "=" * 100)
print("5. LEAD/LAG - hari pertama rc_ge3m >= 84 dalam bear era vs bear low aktual")
print("=" * 100)
lead_rows = []
for (name, s, e), (lname, ldate) in zip(BEAR_ERAS, lows_all):
    s = pd.Timestamp(s)
    low = pd.Timestamp(ldate)
    e_end = an["date"].max() if e is None else pd.Timestamp(e)
    # cari hari pertama trigger sejak cycle peak (at-gate: tidak melihat masa depan)
    w = an[(an.date >= s) & (an.date <= min(e_end, an["date"].max()))]
    trig_abs = w[w["rc_ge3m"] >= THRESH_ABS]
    trig_rel = w[w["pctl_4y"] >= PCTL_LEVEL]
    fa = trig_abs["date"].min() if not trig_abs.empty else pd.NaT
    fr = trig_rel["date"].min() if not trig_rel.empty else pd.NaT
    la = (low - fa).days if pd.notna(fa) else None
    lr = (low - fr).days if pd.notna(fr) else None
    lead_rows.append({"bear": name, "low_date": ldate,
                      "first_trigger_abs84": fa.date() if pd.notna(fa) else None,
                      "lead_days_abs84": la,
                      "first_trigger_pctl95_4y": fr.date() if pd.notna(fr) else None,
                      "lead_days_pctl95_4y": lr})
    print(f"  {name:<14} low={ldate}  | abs84 pertama: {str(fa.date()) if pd.notna(fa) else 'TIDAK PERNAH':<12} "
          f"lead={str(la)+'d' if la is not None else '-':>7}  | p95/4y pertama: "
          f"{str(fr.date()) if pd.notna(fr) else 'TIDAK PERNAH':<12} lead={str(lr)+'d' if lr is not None else '-':>7}")
ld = pd.DataFrame(lead_rows)
print("\n  (lead positif = sinyal muncul SEBELUM low; negatif = setelah low)")

# =============================================================================
# 6. B2 - sisi bull peak: rc_lt3m puncak lokal vs cycle peak
# =============================================================================
print("\n" + "=" * 100)
print("6. B2 - puncak lokal rc_lt3m (=100-rc_ge3m) vs cycle peak; banding AVIV Upper streak-end")
print("=" * 100)
AVIV_STREAK_END = {"Peak 2017": "2018-01-16", "Peak 2021": "2021-11-26", "Peak 2025": "2025-10-15"}
b2_rows = []
for name, pstr in CYCLE_PEAKS:
    p = pd.Timestamp(pstr)
    w = an[(an.date >= p - pd.Timedelta(days=180)) & (an.date <= p + pd.Timedelta(days=180))]
    if w.empty:
        print(f"  {name}: tidak ada data")
        continue
    i = w["rc_lt3m"].idxmax()
    pk_date = w.loc[i, "date"]
    lag = (pk_date - p).days
    aviv = AVIV_STREAK_END.get(name)
    aviv_lag = (pd.Timestamp(aviv) - p).days if aviv else None
    b2_rows.append({"peak": name, "peak_date": pstr, "rc_lt3m_localmax": w.loc[i, "rc_lt3m"],
                    "rc_lt3m_localmax_date": pk_date.date(), "lag_days_vs_peak": lag,
                    "aviv_upper_streak_end": aviv, "aviv_lag_days_vs_peak": aviv_lag})
    print(f"  {name:<10} peak={pstr}  puncak lokal rc_lt3m={w.loc[i,'rc_lt3m']:5.2f}% pada {pk_date.date()} "
          f"(lag {lag:+d}d)   | AVIV Upper streak-end {aviv} (lag {aviv_lag:+d}d)"
          if aviv else
          f"  {name:<10} peak={pstr}  puncak lokal rc_lt3m={w.loc[i,'rc_lt3m']:5.2f}% pada {pk_date.date()} (lag {lag:+d}d)")
b2 = pd.DataFrame(b2_rows)
print("\n  CATATAN: puncak lokal ini hanya bisa diketahui SETELAH fakta (butuh window +-180d)")
print("  -> tidak tradable at-gate. Nilai timing = 0 kecuali ada aturan konfirmasi terpisah.")

# =============================================================================
# 7. B3 - klaim '4.9% away'
# =============================================================================
print("\n" + "=" * 100)
print("7. B3 - klaim judul video '4.9% away' dari puncak bear sebelumnya")
print("=" * 100)
cur = an.loc[an.date == "2026-05-25", "rc_ge3m"].iloc[0]
print(f"  rc_ge3m 2026-05-25 = {cur:.2f}%")
print(f"  Implikasi klaim (relatif +4.9%)  : {cur*1.049:.2f}%")
print(f"  Implikasi klaim (+4.9 poin abs)  : {cur+4.9:.2f}%")
for _, r in dr.dropna(subset=["peak_rc_ge3m"]).iterrows():
    if r["bear"] == "Bear 2025-26":
        continue
    gap_pp = r["peak_rc_ge3m"] - cur
    gap_rel = (r["peak_rc_ge3m"] / cur - 1) * 100
    print(f"  Puncak {r['bear']:<12} = {r['peak_rc_ge3m']:.2f}%  -> jarak dari sekarang: "
          f"{gap_pp:+.2f} poin ({gap_rel:+.2f}% relatif)")

# =============================================================================
# SIMPAN CSV
# =============================================================================
rec2 = rec.merge(ld[["bear", "first_trigger_abs84", "lead_days_abs84",
                     "first_trigger_pctl95_4y", "lead_days_pctl95_4y"]], on="bear", how="left")
rec2 = rec2.merge(dr[["bear", "peak_rc_ge3m", "peak_date", "era_start", "era_end"]], on="bear", how="left")
out = os.path.join(OUTDIR, "events_rc_hodl_waves_ge3m.csv")
rec2.to_csv(out, index=False)
print(f"\nCSV event disimpan: {out}")

out2 = os.path.join(OUTDIR, "events_rc_hodl_waves_ge3m_peaks_b2.csv")
b2.to_csv(out2, index=False)
print(f"CSV B2 disimpan   : {out2}")
print("\nSELESAI.")
