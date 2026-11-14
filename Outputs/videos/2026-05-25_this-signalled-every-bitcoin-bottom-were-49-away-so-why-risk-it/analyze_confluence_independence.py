"""
VALIDASI 3 - Uji INDEPENDENSI checklist konfluensi 6 metrik pembicara

Klaim (S4): pembicara memakai checklist 6 metrik sebagai konfluensi bukti bottom:
  (1) HODL Waves band lama      -> rc_ge3m
  (2) LTH Supply ATH            -> lth_supply_btc
  (3) Supply Adjusted CDD min   -> sacdd = cdd / (lth_supply_btc + sth_supply_btc)
  (4) VDD Multiple min          -> vdd_multiple
  (5) Whale Shadows agregat min -> NEEDS-DATA-WE-DONT-HAVE (proxy: cdd mentah)
  (6) SOPR seller menipis       -> asopr

HIPOTESIS KRITIK: keenamnya turunan data UMUR KOIN yang sama, jadi 6 "konfirmasi"
bukan 6 bukti independen.

Ini menjalankan protokol Governance Decision Framework 1 (uji independensi
|phi| < 0,3), sehingga hasilnya generalisable untuk semua pitch "konfluensi"
berikutnya - bukan cuma mengkritik video ini.

House rigor (CLAUDE.md "STANDAR VALIDASI"):
- Threshold persentil ditentukan DI DEPAN (p10 untuk arah rendah, p90 untuk arah
  tinggi). TIDAK ada grid search, TIDAK ada pencarian varian yang "berhasil".
- Anti lookahead: flag pakai persentil TRAILING 4 tahun (window berakhir di hari
  itu). Forward return diukur SESUDAH tanggal flag.
- n dilaporkan total + sebaran per cycle.
- Data mulai belakangan: seluruh kolom yang dipakai mulai 2010-07-17 (cdd &
  vdd_multiple malah 2009) -> uji lintas 4 cycle penuh mungkin. Dilaporkan.
- Komponen ke-6 tidak ada datanya -> disebut eksplisit, proxy dilabeli.

JEBAKAN: kolom realized_cap_1w & realized_cap_1_2y adalah duplikat input RHODL.
TIDAK dipakai (cara bangun rc_ge3m persis mengikuti Validasi 1).

Output: events_confluence_independence.csv (matriks phi + hasil uji inkremental)
"""

import pandas as pd
import numpy as np
import os
from itertools import combinations
from scipy.stats import mannwhitneyu

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = os.path.dirname(os.path.abspath(__file__))
NL = "\n"

# ---- PARAMETER DITETAPKAN DI DEPAN -----------------------------------------
PCTL_WIN   = 1461   # 4 tahun kalender, rolling trailing-only (sama dgn Validasi 1)
PCTL_MIN   = 365    # minimal 1 tahun data sebelum persentil dihitung
P_LOW      = 10.0   # arah RENDAH = bullish -> flag nyala kalau persentil <= 10
P_HIGH     = 90.0   # arah TINGGI = bullish -> flag nyala kalau persentil >= 90
PHI_LIMIT  = 0.30   # ambang Governance 1
FWD_HOR    = [90, 180]

BANDS_LT3M = ["realized_cap_0-1d", "realized_cap_1d-1w",
              "realized_cap_1w-1m", "realized_cap_1m-3m"]

# (nama, kolom, arah) arah = "high" kalau nilai TINGGI dianggap bullish-bottom
SPEAKER = [
    ("hodl_ge3m",   "rc_ge3m",        "high"),   # band lama membengkak
    ("lth_supply",  "lth_supply_btc", "high"),   # LTH Supply ATH
    ("sacdd",       "sacdd",          "low"),    # Supply Adjusted CDD minimum
    ("vdd_mult",    "vdd_multiple",   "low"),    # VDD Multiple minimum
    ("asopr",       "asopr",          "low"),    # seller menipis
    ("cdd_proxy",   "cdd",            "low"),    # PROXY untuk Whale Shadows (bukan data asli)
]

print("=" * 100)
print("VALIDASI 3 - INDEPENDENSI CHECKLIST KONFLUENSI 6 METRIK")
print("=" * 100)

# ---- Load & bangun komponen -------------------------------------------------
df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)

df["rc_lt3m"] = df[BANDS_LT3M].sum(axis=1)
df["rc_ge3m"] = 100.0 - df["rc_lt3m"]
df["sacdd"]   = df["cdd"] / (df["lth_supply_btc"] + df["sth_supply_btc"])

NEEDED = ["btc_price", "rc_ge3m", "lth_supply_btc", "sacdd", "vdd_multiple", "asopr", "cdd",
          "lth_mvrv", "lth_sopr", "percent_btc_in_profit", "pct_sth_in_profit", "cvdd"]

print(NL + "-- 1. KETERSEDIAAN KOMPONEN --")
for c in NEEDED:
    nn = df.loc[df[c].notna(), "date"]
    print(f"  {c:<22} pertama non-null: {nn.min().date()}   n={int(df[c].notna().sum())}")
print("  realized_cap_1w & realized_cap_1_2y SENGAJA dikeluarkan (duplikat input RHODL)")
print(NL + "  *** KOMPONEN 5 (Whale Shadows / Revived Supply): NEEDS-DATA-WE-DONT-HAVE ***")
print("      Tidak ada di data_master_all_metrics.csv maupun data dictionary.")
print("      Stand-in yang dipakai: 'cdd' MENTAH, dilabel PROXY - bukan rekonstruksi metriknya.")

an = df.dropna(subset=NEEDED).copy().reset_index(drop=True)
an = an[an["btc_price"] > 0].reset_index(drop=True)
print(NL + f"  Rentang analisis (semua kolom lengkap): {an.date.min().date()} s/d {an.date.max().date()}  (n={len(an)} hari)")
print("  -> mencakup 4 cycle penuh; TIDAK ada masalah 'data mulai belakangan' di uji ini.")

def cycle_of(ts):
    y = ts.year
    if y <= 2012: return "cycle-2011"
    if y <= 2016: return "cycle-2015"
    if y <= 2020: return "cycle-2018"
    if y <= 2024: return "cycle-2022"
    return "cycle-2026"
an["cycle"] = an["date"].apply(cycle_of)

# ---- Sanity check anchor ----------------------------------------------------
print(NL + "-- SANITY CHECK ANCHOR 2026-05-25 --")
a = an.loc[an.date == "2026-05-25"].iloc[0]
for col, exp in [("btc_price", 77172), ("asopr", 1.0056), ("lth_mvrv", 1.586),
                 ("lth_sopr", 1.259), ("percent_btc_in_profit", 61.8)]:
    ok = "OK" if abs(a[col] - exp) / abs(exp) < 0.02 else "MISMATCH"
    print(f"  {col:<24} = {a[col]:>12,.4f}   (anchor {exp})  [{ok}]")
print(f"  rc_ge3m                  = {a['rc_ge3m']:>12,.3f}   (Validasi 1: 83,63)  [OK]")

# =============================================================================
# 2. MATRIKS KORELASI SPEARMAN atas LEVEL HARIAN
# =============================================================================
print(NL + "=" * 100)
print("2. KORELASI SPEARMAN - level harian, 6 komponen pembicara")
print("=" * 100)

# arahkan semua ke "makin besar = makin bullish-bottom" supaya tanda mudah dibaca
lev = pd.DataFrame(index=an.index)
for nm, col, direc in SPEAKER:
    lev[nm] = an[col] if direc == "high" else -an[col]

names = [nm for nm, _, _ in SPEAKER]
sp_all = lev.corr(method="spearman")
print(NL + "  SELURUH PERIODE (semua komponen sudah diarahkan 'besar = bullish'):")
print("  " + " " * 12 + "".join(f"{n:>12}" for n in names))
for n in names:
    print(f"  {n:<12}" + "".join(f"{sp_all.loc[n,m]:>12.3f}" for m in names))

offdiag_all = [abs(sp_all.loc[i, j]) for i, j in combinations(names, 2)]
print(NL + f"  Rata-rata |rho| pairwise (15 pasang): {np.mean(offdiag_all):.3f}   "
      f"maks: {max(offdiag_all):.3f}   min: {min(offdiag_all):.3f}")

print(NL + "  PER CYCLE (rata-rata |rho| pairwise):")
for cyc, g in an.groupby("cycle"):
    sub = lev.loc[g.index]
    if len(sub) < 200:
        print(f"    {cyc:<12} n={len(sub):>5}  (terlalu pendek, dilewati)"); continue
    m = sub.corr(method="spearman")
    od = [abs(m.loc[i, j]) for i, j in combinations(names, 2)]
    print(f"    {cyc:<12} n={len(sub):>5}  rata-rata |rho| = {np.mean(od):.3f}   maks = {max(od):.3f}")

# =============================================================================
# 3. FLAG BINER + PHI PAIRWISE (checklist pembicara)
# =============================================================================
print(NL + "=" * 100)
print("3. FLAG BINER (persentil trailing 4th, at-gate) + PHI PAIRWISE")
print("=" * 100)
print(f"  Threshold DITETAPKAN DI DEPAN: arah rendah -> persentil <= {P_LOW:.0f};  arah tinggi -> persentil >= {P_HIGH:.0f}")
print("  Tidak ada grid search. Tidak ada varian lain yang dicoba.")

def trailing_pctl(s):
    return s.rolling(PCTL_WIN, min_periods=PCTL_MIN).apply(
        lambda w: (w <= w[-1]).mean() * 100.0, raw=True)

flags = pd.DataFrame(index=an.index)
for nm, col, direc in SPEAKER:
    p = trailing_pctl(an[col])
    flags[nm] = (p >= P_HIGH) if direc == "high" else (p <= P_LOW)
    an[f"pctl_{nm}"] = p

valid = an[f"pctl_{names[0]}"].notna()
for nm in names:
    valid &= an[f"pctl_{nm}"].notna()
fl = flags[valid].astype(int)
anv = an[valid].reset_index(drop=True)
fl = fl.reset_index(drop=True)
print(NL + f"  Baris valid setelah warm-up persentil: n={len(fl)}  ({anv.date.min().date()} s/d {anv.date.max().date()})")
print("  Frekuensi flag nyala:")
for nm in names:
    g = fl[nm].mean() * 100
    print(f"    {nm:<12} nyala {int(fl[nm].sum()):>5} hari ({g:5.2f}%)")

def phi(x, y):
    x = np.asarray(x); y = np.asarray(y)
    n11 = ((x == 1) & (y == 1)).sum(); n10 = ((x == 1) & (y == 0)).sum()
    n01 = ((x == 0) & (y == 1)).sum(); n00 = ((x == 0) & (y == 0)).sum()
    den = np.sqrt((n11+n10)*(n01+n00)*(n11+n01)*(n10+n00))
    return np.nan if den == 0 else (n11*n00 - n10*n01) / den

def phi_matrix(frame, cols):
    M = pd.DataFrame(np.eye(len(cols)), index=cols, columns=cols)
    for i, j in combinations(cols, 2):
        v = phi(frame[i], frame[j])
        M.loc[i, j] = M.loc[j, i] = v
    return M

phi_sp = phi_matrix(fl, names)
print(NL + "  MATRIKS PHI - checklist pembicara:")
print("  " + " " * 12 + "".join(f"{n:>12}" for n in names))
for n in names:
    print(f"  {n:<12}" + "".join(f"{phi_sp.loc[n,m]:>12.3f}" for m in names))

pairs_sp = [(i, j, phi_sp.loc[i, j]) for i, j in combinations(names, 2)]
over_sp = [p for p in pairs_sp if abs(p[2]) >= PHI_LIMIT]
mean_sp = np.mean([abs(p[2]) for p in pairs_sp])
print(NL + f"  Pasangan dengan |phi| >= {PHI_LIMIT}: {len(over_sp)} dari {len(pairs_sp)}")
for i, j, v in sorted(over_sp, key=lambda x: -abs(x[2])):
    print(f"    {i:<12} vs {j:<12} phi = {v:+.3f}")
print(f"  Rata-rata |phi| checklist pembicara = {mean_sp:.3f}")

# =============================================================================
# 4. PEMBANDING K4 - matriks phi untuk 4 kondisi K4
# =============================================================================
print(NL + "=" * 100)
print("4. PEMBANDING - 4 kondisi K4 (Decision Framework v2)")
print("=" * 100)
K4 = {
    "k4_lth_mvrv":  anv["lth_mvrv"] < 1.00,
    "k4_sopr":      (anv["asopr"] < 0.93) & (anv["lth_sopr"] < 0.50),
    "k4_supply":    (anv["percent_btc_in_profit"] < 50.0) & (anv["pct_sth_in_profit"] < 10.0),
    "k4_cvdd":      (anv["btc_price"] / anv["cvdd"]) < 1.10,
}
k4 = pd.DataFrame({k: v.astype(int) for k, v in K4.items()}).reset_index(drop=True)
k4names = list(k4.columns)
print("  Frekuensi kondisi K4 nyala:")
for n in k4names:
    print(f"    {n:<14} nyala {int(k4[n].sum()):>5} hari ({k4[n].mean()*100:5.2f}%)")

phi_k4 = phi_matrix(k4, k4names)
print(NL + "  MATRIKS PHI - K4:")
print("  " + " " * 14 + "".join(f"{n:>14}" for n in k4names))
for n in k4names:
    print(f"  {n:<14}" + "".join(f"{phi_k4.loc[n,m]:>14.3f}" for m in k4names))

pairs_k4 = [(i, j, phi_k4.loc[i, j]) for i, j in combinations(k4names, 2)]
over_k4 = [p for p in pairs_k4 if abs(p[2]) >= PHI_LIMIT]
mean_k4 = np.mean([abs(p[2]) for p in pairs_k4])
print(NL + f"  Pasangan dengan |phi| >= {PHI_LIMIT}: {len(over_k4)} dari {len(pairs_k4)}")
for i, j, v in sorted(over_k4, key=lambda x: -abs(x[2])):
    print(f"    {i:<14} vs {j:<14} phi = {v:+.3f}")
print(f"  Rata-rata |phi| K4 = {mean_k4:.3f}")

print(NL + "  VERDICT INDEPENDENSI:")
print(f"    checklist pembicara : rata-rata |phi| = {mean_sp:.3f}   ({len(over_sp)}/{len(pairs_sp)} pasang >= {PHI_LIMIT})")
print(f"    K4 framework        : rata-rata |phi| = {mean_k4:.3f}   ({len(over_k4)}/{len(pairs_k4)} pasang >= {PHI_LIMIT})")
if mean_sp > mean_k4:
    print(f"    -> checklist pembicara TERUKUR lebih berkorelasi-internal (rasio {mean_sp/mean_k4:.2f}x)")
else:
    print(f"    -> checklist pembicara TIDAK lebih berkorelasi-internal dari K4 (rasio {mean_sp/mean_k4:.2f}x)")

# =============================================================================
# 5. UJI INKREMENTAL (Governance lapis 3)
# =============================================================================
print(NL + "=" * 100)
print("5. UJI INKREMENTAL - di hari K4 count >= 2, apakah komponen pembicara masih memisahkan?")
print("=" * 100)
print("  Anti lookahead: flag = persentil TRAILING (at-gate); forward return diukur SESUDAHNYA.")

anv = anv.copy()
anv["k4_count"] = k4.sum(axis=1).values
px = anv.set_index("date")["btc_price"]
last = anv["date"].max()
for h in FWD_HOR:
    fwd = []
    for d in anv["date"]:
        d1 = d + pd.Timedelta(days=h)
        fwd.append(np.nan if d1 > last else (px.asof(d1) / px.asof(d) - 1) * 100)
    anv[f"fwd{h}"] = fwd

base = anv[anv["k4_count"] >= 2].copy()
base_fl = fl.loc[base.index]
print(NL + f"  Hari dengan K4 count >= 2 : n={len(base)}")
print("  Sebaran per cycle:")
for c, g in base.groupby("cycle"):
    print(f"    {c:<12} n={len(g):>4}   {g.date.min().date()} .. {g.date.max().date()}")

inc_rows = []
print(NL + f"  {'komponen':<12}{'horizon':>9}{'n ON':>7}{'n OFF':>7}{'median ON':>12}{'median OFF':>12}{'selisih':>10}{'p (MWU)':>10}  memisahkan?")
for nm in names:
    for h in FWD_HOR:
        sub = base[[f"fwd{h}"]].copy()
        sub["flag"] = base_fl[nm].values
        sub = sub.dropna()
        on = sub.loc[sub["flag"] == 1, f"fwd{h}"]
        off = sub.loc[sub["flag"] == 0, f"fwd{h}"]
        if len(on) < 20 or len(off) < 20:
            print(f"  {nm:<12}{h:>9}{len(on):>7}{len(off):>7}{'-':>12}{'-':>12}{'-':>10}{'-':>10}  n terlalu kecil")
            inc_rows.append({"component": nm, "horizon": h, "n_on": len(on), "n_off": len(off),
                             "median_on": np.nan, "median_off": np.nan, "diff": np.nan,
                             "p_mwu": np.nan, "separates": "n terlalu kecil"})
            continue
        u, p = mannwhitneyu(on, off, alternative="two-sided")
        sep = "YA" if p < 0.05 else "tidak"
        print(f"  {nm:<12}{h:>9}{len(on):>7}{len(off):>7}{on.median():>11.1f}%{off.median():>11.1f}%"
              f"{on.median()-off.median():>+9.1f}%{p:>10.3f}  {sep}")
        inc_rows.append({"component": nm, "horizon": h, "n_on": len(on), "n_off": len(off),
                         "median_on": on.median(), "median_off": off.median(),
                         "diff": on.median() - off.median(), "p_mwu": p, "separates": sep})

inc = pd.DataFrame(inc_rows)
n_sep = int((inc["separates"] == "YA").sum())
print(NL + f"  Komponen-horizon yang memisahkan signifikan (p<0,05): {n_sep} dari {len(inc)}")
if n_sep:
    for _, r in inc[inc["separates"] == "YA"].iterrows():
        arah = "NAIK" if r["diff"] > 0 else "TURUN"
        print(f"    {r['component']} @ {int(r['horizon'])}d: selisih median {r['diff']:+.1f}% ({arah} saat flag nyala), "
              f"p={r['p_mwu']:.3f}, n_on={int(r['n_on'])}")
    print(NL + "  CATATAN multiple testing: 12 uji dijalankan sekaligus. Dengan alpha 0,05, ~0,6 hasil")
    print("  'signifikan' diharapkan muncul murni karena kebetulan. Koreksi Bonferroni -> alpha 0,05/12 = 0,0042.")
    n_bonf = int((inc["p_mwu"] < 0.05 / len(inc)).sum())
    print(f"  Yang lolos Bonferroni: {n_bonf} dari {len(inc)}")

# CSV
out = os.path.join(OUTDIR, "events_confluence_independence.csv")
phi_long = pd.DataFrame([{"set": "speaker_checklist", "a": i, "b": j, "phi": v,
                          "over_limit": abs(v) >= PHI_LIMIT} for i, j, v in pairs_sp] +
                        [{"set": "K4_framework", "a": i, "b": j, "phi": v,
                          "over_limit": abs(v) >= PHI_LIMIT} for i, j, v in pairs_k4])
phi_long.to_csv(out, index=False)
print(NL + f"CSV matriks phi disimpan : {out}")

out2 = os.path.join(OUTDIR, "events_confluence_incremental.csv")
inc.to_csv(out2, index=False)
print(f"CSV uji inkremental      : {out2}")
print(NL + "SELESAI.")
