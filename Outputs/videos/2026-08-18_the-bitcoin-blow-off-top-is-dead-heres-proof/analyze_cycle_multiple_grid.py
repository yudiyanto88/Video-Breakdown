"""
V2 -- Grid multiple 4-cycle + share log-return + sensitivitas tanggal bottom
Video: On-Chain Mind "The Bitcoin Blow-Off Top Is Dead (Here's Proof)" (2026-08-18)

KLAIM VIDEO (hanya 3 cycle: 2015-17, 2019-21, 2023-25; cycle 2011-13 DIBUANG):
  a) 12-bulan multiple "remarkably flat" ~2.3x  (2.36x / 2.23x / 2.27x)
  b) 24-bulan multiple naik pelan (4.55x / 6.11x / 6.25x)
  c) Peak multiple runtuh order-of-magnitude (107x -> 21x -> 8x)
  d) "Final leg" 24-bulan -> peak selalu ~11 bulan, return-nya mati (23.7x -> 3.47x -> 1.27x)
  e) 6-bulan bisa > 12-bulan (2019: 4x di bulan 6, tutup tahun di 2.2x)

UJI: ulangi dengan SEMUA 4 cycle (C0 2011-13 disertakan justru karena video membuangnya),
plus dua uji ketat yang tidak dilakukan video:
  - share log-return: ln(P_t/P_bottom) / ln(P_peak/P_bottom) -> memisahkan "front-loading
    nyata" dari "sekadar diminishing return" (multiple absolut selalu mengecil kalau
    peak multiple mengecil; share menormalisasi itu)
  - t50 = bulan pertama share log-return >= 50%, dilaporkan ABSOLUT (bulan) dan
    sebagai FRAKSI panjang bottom->peak
  - sensitivitas tanggal bottom: geser -45, -15, +15, +45 hari (5 varian PRE-REGISTERED,
    bukan tuning). Kalau spread multiple 12-bulan > +/-20%, "flat 2.3x" dinyatakan rapuh.

Kolom: btc_price saja. n = 4 cycle (3 tertutup penuh + C3 yang peak-nya baru Okt 2025).
"""

import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-18_the-bitcoin-blow-off-top-is-dead-heres-proof"

df = pd.read_csv(MASTER, parse_dates=["date"])[["date", "btc_price"]]
df = df.dropna().sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 0].reset_index(drop=True)

print("=" * 104)
print("V2 -- GRID MULTIPLE 4 CYCLE, SHARE LOG-RETURN, SENSITIVITAS TANGGAL BOTTOM")
print("=" * 104)
print(f"Data btc_price: {df['date'].min().date()} s/d {df['date'].max().date()}  (n hari={len(df)})")
print("n CYCLE = 4  (C0 2011-13 SENGAJA disertakan -- video membuangnya)")

def px(d):
    """Close terakhir yang tersedia s/d tanggal d (tanpa lookahead)."""
    w = df[df["date"] <= d]
    return np.nan if w.empty else w["btc_price"].iloc[-1]

def extreme(a, b, how):
    w = df[(df["date"] >= a) & (df["date"] <= b)]
    i = w["btc_price"].idxmin() if how == "min" else w["btc_price"].idxmax()
    return df.loc[i, "date"], df.loc[i, "btc_price"]

SPEC = [("C0", "2011-06-15", "2012-03-01", "2013-01-01", "2014-06-01"),
        ("C1", "2014-06-01", "2015-12-31", "2017-06-01", "2018-06-01"),
        ("C2", "2018-06-01", "2019-06-30", "2021-01-01", "2022-06-01"),
        ("C3", "2022-06-01", "2023-06-30", "2025-01-01", "2026-07-15")]

cyc = {}
print("\nTANGGAL SIKLUS (deteksi sendiri dari btc_price)")
print(f"{'Cyc':<5}{'Bottom':<13}{'P_bottom':>12}  {'Peak':<13}{'P_peak':>13}"
      f"{'  Peak mult':>12}{'  bottom->peak':>15}")
print("-" * 90)
for c, ba, bb, pa, pb in SPEC:
    bd, bp = extreme(ba, bb, "min")
    pk, pp = extreme(pa, pb, "max")
    months = (pk - bd).days / 30.44
    cyc[c] = dict(bottom=bd, p_bottom=bp, peak=pk, p_peak=pp, months=months)
    print(f"{c:<5}{str(bd.date()):<13}{bp:>12,.2f}  {str(pk.date()):<13}{pp:>13,.2f}"
          f"{pp/bp:>11,.1f}x{months:>13.1f} bln")

# ============================================================================
# 1. KURVA MULTIPLE BULANAN (bulan 1-36)
# ============================================================================
grid_rows = []
for c in cyc:
    b, pb, pk = cyc[c]["bottom"], cyc[c]["p_bottom"], cyc[c]["peak"]
    for m in range(0, 37):
        d = b + pd.DateOffset(months=m)
        if d > df["date"].max():
            continue
        p = px(d)
        grid_rows.append(dict(cycle=c, month=m, date=d.date(), price=round(p, 2),
                              multiple=round(p / pb, 3),
                              post_peak=(d > pk)))
grid = pd.DataFrame(grid_rows)
grid.to_csv(rf"{OUTDIR}\events_cycle_multiple_grid.csv", index=False)

piv = grid.pivot(index="month", columns="cycle", values="multiple")
print("\nKURVA MULTIPLE BULANAN (x dari harga bottom). '*' = sudah lewat cycle peak")
print(f"{'Bln':>4}" + "".join(f"{c:>12}" for c in cyc))
print("-" * 52)
for m in range(0, 37):
    line = f"{m:>4}"
    for c in cyc:
        r = grid[(grid["cycle"] == c) & (grid["month"] == m)]
        if r.empty:
            line += f"{'-':>12}"
        else:
            star = "*" if bool(r["post_peak"].iloc[0]) else " "
            line += f"{r['multiple'].iloc[0]:>11,.2f}{star}"
    print(line)

print("\nSOROTAN vs KLAIM VIDEO")
print(f"{'Cyc':<5}{'6bln':>9}{'12bln':>9}{'18bln':>9}{'24bln':>9}{'Peak':>10}"
      f"{'  24bln->peak':>14}{'  return leg akhir':>19}")
print("-" * 84)
for c in cyc:
    g = lambda m: grid[(grid["cycle"] == c) & (grid["month"] == m)]["multiple"]
    m6, m12, m18, m24 = [g(m).iloc[0] if len(g(m)) else np.nan for m in (6, 12, 18, 24)]
    pkm = cyc[c]["p_peak"] / cyc[c]["p_bottom"]
    leg_months = cyc[c]["months"] - 24
    leg_ret = pkm / m24 if not np.isnan(m24) else np.nan
    print(f"{c:<5}{m6:>8,.2f}x{m12:>8,.2f}x{m18:>8,.2f}x{m24:>8,.2f}x{pkm:>9,.1f}x"
          f"{leg_months:>12.1f}b{leg_ret:>17,.2f}x")

print("\nKlaim video (3 cycle saja): 12bln 2.36/2.23/2.27x ~ 'flat 2.3x';")
print("24bln 4.55/6.11/6.25x; peak 107/21/8x; final leg ~11 bulan 23.7/3.47/1.27x")

# ============================================================================
# 2. SHARE LOG-RETURN
# ============================================================================
print("\n" + "=" * 104)
print("SHARE LOG-RETURN = ln(P_t/P_bottom) / ln(P_peak/P_bottom)")
print("  -> berapa PERSEN dari seluruh perjalanan bottom->peak (skala log) sudah selesai di bulan t")
print("=" * 104)
share_rows = []
print(f"{'Cyc':<5}{'6bln':>9}{'12bln':>9}{'18bln':>9}{'24bln':>9}"
      f"{'  t50 (bln)':>12}{'  t50/durasi':>13}{'  durasi b->p':>14}")
print("-" * 84)
for c in cyc:
    b, pb, pp = cyc[c]["bottom"], cyc[c]["p_bottom"], cyc[c]["p_peak"]
    tot = np.log(pp / pb)
    sh = {}
    for m in (6, 12, 18, 24):
        p = px(b + pd.DateOffset(months=m))
        sh[m] = np.log(p / pb) / tot * 100
    # t50: bulan pertama share >= 50%
    t50 = None
    for m in range(1, 60):
        d = b + pd.DateOffset(months=m)
        if d > cyc[c]["peak"]:
            break
        s = np.log(px(d) / pb) / tot * 100
        if s >= 50:
            t50 = m
            break
    frac = t50 / cyc[c]["months"] if t50 else np.nan
    print(f"{c:<5}{sh[6]:>8.1f}%{sh[12]:>8.1f}%{sh[18]:>8.1f}%{sh[24]:>8.1f}%"
          f"{(t50 if t50 else -1):>11}{frac:>13.2f}{cyc[c]['months']:>12.1f}b")
    share_rows.append(dict(cycle=c, share6=round(sh[6], 1), share12=round(sh[12], 1),
                           share18=round(sh[18], 1), share24=round(sh[24], 1),
                           t50_month=t50, t50_fraction=round(frac, 3),
                           duration_months=round(cyc[c]["months"], 1)))
pd.DataFrame(share_rows).to_csv(rf"{OUTDIR}\events_cycle_share_logreturn.csv", index=False)

print("\nBaca: kalau t50/durasi ROUGHLY SAMA lintas cycle -> bentuk kurva tidak berubah,")
print("      yang berubah cuma AMPLITUDO (diminishing return biasa), BUKAN 'front-loading'.")
print("      Kalau t50/durasi MENGECIL tajam -> gain benar-benar pindah ke depan.")

# ============================================================================
# 3. SENSITIVITAS TANGGAL BOTTOM (5 varian pre-registered)
# ============================================================================
print("\n" + "=" * 104)
print("SENSITIVITAS TANGGAL BOTTOM  (geser -45, -15, 0, +15, +45 hari)")
print("  P_bottom = close di tanggal geseran itu (BUKAN min lokal), semuanya dilaporkan")
print("=" * 104)
SHIFTS = [-45, -15, 0, 15, 45]
sens_rows = []
for horizon in (6, 12, 24):
    print(f"\n--- multiple {horizon} BULAN ---")
    print(f"{'Cyc':<5}" + "".join(f"{('d'+str(s)):>10}" for s in SHIFTS)
          + f"{'  min':>9}{'  max':>9}{'  spread vs d0':>15}")
    print("-" * 92)
    for c in cyc:
        vals = []
        for s in SHIFTS:
            b = cyc[c]["bottom"] + pd.Timedelta(days=s)
            pb = px(b)
            p = px(b + pd.DateOffset(months=horizon))
            vals.append(p / pb if (pb and not np.isnan(pb)) else np.nan)
        base = vals[SHIFTS.index(0)]
        lo, hi = np.nanmin(vals), np.nanmax(vals)
        spread = max(abs(hi / base - 1), abs(lo / base - 1)) * 100
        print(f"{c:<5}" + "".join(f"{v:>9,.2f}x" for v in vals)
              + f"{lo:>8,.2f}x{hi:>8,.2f}x{spread:>13.1f}%")
        sens_rows.append(dict(cycle=c, horizon_months=horizon,
                              **{f"shift_{s}": round(v, 3) for s, v in zip(SHIFTS, vals)},
                              min=round(lo, 3), max=round(hi, 3),
                              spread_vs_base_pct=round(spread, 1)))
pd.DataFrame(sens_rows).to_csv(rf"{OUTDIR}\events_cycle_multiple_sensitivity.csv", index=False)

# vonis robustness untuk klaim "flat 2.3x"
print("\nVONIS ROBUSTNESS klaim 'flat ~2.3x di 12 bulan':")
sens12 = pd.DataFrame(sens_rows)
sens12 = sens12[sens12["horizon_months"] == 12]
worst = sens12["spread_vs_base_pct"].max()
print(f"  spread maksimum multiple 12-bulan akibat geser tanggal bottom +/-45 hari = {worst:.1f}%")
print(f"  ambang pre-registered = 20%  ->  {'TIDAK ROBUST' if worst > 20 else 'robust'}")
# rentang 12-bulan lintas SEMUA cycle & SEMUA varian
allv = sens12[[f"shift_{s}" for s in SHIFTS]].values.flatten()
allv = allv[~np.isnan(allv)]
print(f"  rentang multiple 12-bulan lintas 4 cycle x 5 varian: "
      f"{allv.min():.2f}x s/d {allv.max():.2f}x  (n={len(allv)} kombinasi)")
v3 = sens12[sens12["cycle"] != "C0"][[f"shift_{s}" for s in SHIFTS]].values.flatten()
v3 = v3[~np.isnan(v3)]
print(f"  kalau C0 DIBUANG (seperti video): {v3.min():.2f}x s/d {v3.max():.2f}x")

print("\nCATATAN OVERFIT: hanya 5 varian tanggal bottom yang dicoba, ditetapkan DI MUKA,")
print("dan SEMUANYA dilaporkan. Tidak ada tanggal bottom yang dipilih karena hasilnya rapi.")
print("\nSelesai. CSV: events_cycle_multiple_grid.csv, events_cycle_share_logreturn.csv,")
print("            events_cycle_multiple_sensitivity.csv")
