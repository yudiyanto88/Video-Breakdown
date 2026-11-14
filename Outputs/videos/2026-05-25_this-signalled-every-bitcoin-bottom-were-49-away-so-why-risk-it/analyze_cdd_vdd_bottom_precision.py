"""
VALIDASI 4 - Presisi VDD Multiple & Supply-Adjusted CDD sebagai penanda bear low,
             + kuantifikasi failure mode, + uji confound HARGA.

Klaim B6 [02:54]-[03:11]: VDD Multiple di level bear-market-low = distribusi LTH/whale berhenti.
Klaim B7 [03:28]-[04:04]: Supply Adjusted CDD di level yang historically = "unbelievable
             accumulation opportunity" - TAPI pembicara sendiri mengakui failure mode:
             di 2018 sinyal ini muncul tepat SEBELUM downward spike besar.

HIPOTESIS KRITIK: VDD = coin-days x HARGA USD. Saat harga turun 48%, VDD ikut turun
tanpa perubahan perilaku holder sama sekali. "LTH berhenti distribusi" dan "harga rendah
sehingga coin-days yang sama bernilai lebih kecil dalam USD" menghasilkan pembacaan
IDENTIK. Uji: bandingkan varian value-weighted vs varian yang komponen harganya dilepas.

House rigor (CLAUDE.md "STANDAR VALIDASI"):
1. Definisi event eksplisit: hari PERTAMA di bawah threshold, cooldown 90 hari.
2. n dilaporkan total + sebaran per cycle.
3. Anti lookahead: threshold persentil DUA mode - (a) full-history (sesuai instruksi,
   tapi in-sample/lookahead - dilabel), (b) trailing 4 tahun at-gate (sama dgn Validasi 3).
   Drawdown & return diukur SESUDAH tanggal trigger.
4. Independensi sample: event dari cycle sama berkorelasi - sebaran per cycle dilaporkan.
5. Data mulai belakangan: cdd & vdd mulai 2009-01-03, btc_price 2010-07-17 -> 4 cycle penuh.
6. TIDAK ada grid search. Threshold = p5 & p10 saja, ditetapkan di depan. Semua seri
   diuji dan SEMUA hasilnya dilaporkan (tidak ada varian yang dibuang).

Output: events_cdd_vdd_bottom_precision.csv
"""

import pandas as pd
import numpy as np
import os

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = os.path.dirname(os.path.abspath(__file__))
NL = "\n"

# ---- PARAMETER DITETAPKAN DI DEPAN -----------------------------------------
PCTLS      = [5.0, 10.0]   # a priori. TIDAK ada grid search.
COOLDOWN   = 90            # hari antar event
WIN_LOW    = 60            # +-60 hari dari bear low = "tepat sasaran"
DD_HOR     = 90            # horizon drawdown maksimum sesudah trigger
DD_LIMIT   = -20.0         # ambang failure mode
PCTL_WIN   = 1461          # trailing 4 tahun (mode anti-lookahead)
PCTL_MIN   = 365

BEAR_LOWS = ["2011-11-18", "2015-01-14", "2018-12-14", "2022-11-21"]
BEAR_LOWS = [pd.Timestamp(d) for d in BEAR_LOWS]
LOW_UNCONF = pd.Timestamp("2026-06-30")   # BELUM terkonfirmasi - dilaporkan terpisah
PEAKS = [pd.Timestamp(d) for d in
         ["2011-06-08", "2013-11-30", "2017-12-16", "2021-11-08", "2025-10-06"]]
# Event SESUDAH cycle peak terakhir tidak bisa dinilai: bear low cycle ini BELUM
# terkonfirmasi. Dikeluarkan dari presisi/recall, dilaporkan terpisah di section 9.
SCORE_CUTOFF = pd.Timestamp("2025-10-06")

print("=" * 108)
print("VALIDASI 4 - PRESISI VDD MULTIPLE & SUPPLY-ADJUSTED CDD DI BEAR LOW + UJI CONFOUND HARGA")
print("=" * 108)

# ---- Load & bangun seri -----------------------------------------------------
df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)

supply = df["lth_supply_btc"] + df["sth_supply_btc"]
vdd_daily = df["cdd"] * df["btc_price"]           # identitas VDD = CDD x harga

new = pd.DataFrame({
    "vdd_daily":     vdd_daily,
    "sacdd":         df["cdd"] / supply,
    # (1) value-weighted, bentuk MA30/MA365 = bentuk chart BMPro
    "vdd_mult_ma":   vdd_daily.rolling(30).mean() / vdd_daily.rolling(365).mean(),
    # (2) price-stripped twin dari (1): struktur rasio persis sama, harga dilepas
    "cdd_mult_ma":   df["cdd"].rolling(30).mean() / df["cdd"].rolling(365).mean(),
    # (3) benchmark naif: MURNI harga, tanpa data umur koin sama sekali
    "price_ratio":   df["btc_price"].rolling(30).mean() / df["btc_price"].rolling(365).mean(),
})
new["sacdd_ma30"]  = new["sacdd"].rolling(30).mean()
new["sacdd_ma900"] = new["sacdd"].rolling(900).mean()
df = pd.concat([df, new], axis=1)

print(NL + "-- 0. KETERSEDIAAN DATA & IDENTITAS VDD --")
for c in ["btc_price", "cdd", "vdd_30d_ma", "vdd_365d_ma", "vdd_multiple",
          "lth_supply_btc", "sth_supply_btc"]:
    nn = df.loc[df[c].notna(), "date"]
    print(f"  {c:<18} {nn.min().date()} .. {nn.max().date()}   n={int(df[c].notna().sum())}")

chk = df.dropna(subset=["vdd_30d_ma", "vdd_daily"])
ratio = (chk["vdd_30d_ma"] / chk["vdd_daily"].rolling(30).mean().loc[chk.index]).dropna()
print(NL + f"  Identitas terverifikasi: vdd_30d_ma == MA30(cdd x btc_price)  "
      f"(rasio min={ratio.min():.6f} maks={ratio.max():.6f})")
print("  -> VDD memang VALUE-WEIGHTED. Komponen harga ada di dalamnya secara aljabar.")

print(NL + "-- 0b. DEFINISI KOLOM vdd_multiple DI DATA MASTER (PENTING) --")
sub = df.dropna(subset=["vdd_multiple", "vdd_365d_ma"])
d_ratio = sub["vdd_daily"] / sub["vdd_365d_ma"]
print(f"  vdd_multiple == VDD HARIAN / MA365(VDD)   (selisih maks {abs(d_ratio - sub['vdd_multiple']).max():.2e})")
print(f"  BUKAN MA30/MA365. Jadi kolom ini seri HARIAN yang sangat berisik.")
wk = df[(df.date >= "2026-05-20") & (df.date <= "2026-05-30")]
print("  Contoh keberisikan satu minggu di sekitar tanggal video:")
print("    " + "  ".join(f"{r.date.date()}:{r.vdd_multiple:.3f}" for _, r in wk.iterrows()))

print(NL + "-- SANITY CHECK ANCHOR 2026-05-25 --")
a = df.loc[df.date == "2026-05-25"].iloc[0]
for col, exp in [("btc_price", 77172), ("realized_price", 54172), ("sth_cost_basis", 77910),
                 ("lth_cost_basis", 48650), ("50_wma", 94325)]:
    ok = "OK" if abs(a[col] - exp) / abs(exp) < 0.02 else "MISMATCH"
    print(f"  {col:<18} = {a[col]:>12,.2f}   (anchor {exp:,})  [{ok}]")
print(f"  vdd_multiple       = {a['vdd_multiple']:>12,.4f}   (anchor 0,533)  [MISMATCH - lihat catatan]")
print(f"  vdd_mult_ma (MA30/MA365) = {a['vdd_mult_ma']:.4f}   <- versi yang dipakai di uji ini")
print("  CATATAN: anchor 0,533 tidak cocok karena kolom vdd_multiple = rasio HARIAN yang")
print("  berayun 0,18-0,69 dalam satu minggu yang sama. Tidak ada angka satu-hari yang")
print("  bermakna untuk seri ini -> primary series di uji ini = versi MA30/MA365.")

# ---- Window analisis --------------------------------------------------------
SERIES = [
    ("vdd_mult_ma",  "VALUE-weighted", "VDD Multiple MA30/MA365 (bentuk chart BMPro)"),
    ("vdd_multiple", "VALUE-weighted", "kolom master mentah = VDD harian / MA365"),
    ("sacdd_ma30",   "unit-weighted",  "Supply-Adjusted CDD, MA30"),
    ("sacdd_ma900",  "unit-weighted",  "Supply-Adjusted CDD, MA900 (BMPro pakai MA900 & MA30)"),
    ("cdd_mult_ma",  "unit-weighted",  "TWIN price-stripped dari VDD Multiple: MA30(cdd)/MA365(cdd)"),
    ("price_ratio",  "HARGA MURNI",    "benchmark naif: MA30(price)/MA365(price), tanpa umur koin"),
]

# Window inti TIDAK dibatasi oleh sacdd_ma900 (butuh 900 hari warm-up, akan membuang
# bear low 2011). sacdd_ma900 dibiarkan NaN di awal & event-nya di-skip per-seri.
CORE = ["btc_price", "vdd_mult_ma", "vdd_multiple", "sacdd_ma30", "cdd_mult_ma", "price_ratio"]
an = df.dropna(subset=CORE).reset_index(drop=True)
an = an[an["btc_price"] > 0].reset_index(drop=True)
print(NL + f"-- Rentang analisis inti: {an.date.min().date()} .. {an.date.max().date()}  n={len(an)} hari")
print("   Mencakup 4 bear low terkonfirmasi? " +
      str(all(an.date.min() <= d <= an.date.max() for d in BEAR_LOWS)))
for c, _, _ in SERIES:
    nn = an.loc[an[c].notna(), "date"]
    print(f"   {c:<15} tersedia {nn.min().date()} .. {nn.max().date()}  n={int(an[c].notna().sum())}")
print("   CATATAN 'data mulai belakangan': sacdd_ma900 butuh warm-up 900 hari -> baru mulai")
print("   2013-01-01, jadi seri itu TIDAK bisa melihat bear low 2011. Dilaporkan eksplisit.")

def cycle_of(ts):
    y = ts.year
    if y <= 2012: return "cycle-2011"
    if y <= 2016: return "cycle-2015"
    if y <= 2020: return "cycle-2018"
    if y <= 2024: return "cycle-2022"
    return "cycle-2026"
an["cycle"] = an["date"].apply(cycle_of)

# =============================================================================
# 1. DEKOMPOSISI CONFOUND - berapa besar VDD Multiple sebenarnya HARGA?
# =============================================================================
print(NL + "=" * 108)
print("1. DEKOMPOSISI CONFOUND HARGA - inti kritiknya")
print("=" * 108)
print("  VDD Multiple = MA30(CDD x P) / MA365(CDD x P).  Kalau CDD konstan, rasio ini")
print("  tetap turun saat harga turun, karena MA30(P) < MA365(P). Seberapa besar efeknya?")

lg = pd.DataFrame({
    "vdd": np.log(an["vdd_mult_ma"]),
    "cdd": np.log(an["cdd_mult_ma"]),
    "prc": np.log(an["price_ratio"]),
}).replace([np.inf, -np.inf], np.nan).dropna()

def r2_ols(y, X):
    n = len(np.asarray(X[0]))
    X = np.column_stack([np.ones(n)] + [np.asarray(c) for c in X])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ b
    return 1 - resid.var() / np.asarray(y).var()

y = lg["vdd"].values
print(NL + f"  n = {len(lg)} hari (log-space)")
print(f"  R2  log(VDD Mult) ~ log(price_ratio) SAJA          : {r2_ols(y, [lg['prc']]):.3f}")
print(f"  R2  log(VDD Mult) ~ log(cdd_mult) SAJA             : {r2_ols(y, [lg['cdd']]):.3f}")
print(f"  R2  log(VDD Mult) ~ keduanya                       : {r2_ols(y, [lg['prc'], lg['cdd']]):.3f}")
print(f"  Spearman  VDD Mult vs price_ratio : {an['vdd_mult_ma'].corr(an['price_ratio'], method='spearman'):+.3f}")
print(f"  Spearman  VDD Mult vs cdd_mult    : {an['vdd_mult_ma'].corr(an['cdd_mult_ma'], method='spearman'):+.3f}")
print(f"  Spearman  sacdd_ma30 vs price_ratio : {an['sacdd_ma30'].corr(an['price_ratio'], method='spearman'):+.3f}")

# =============================================================================
# 2. EVENT GENERATION
# =============================================================================
print(NL + "=" * 108)
print("2. DEFINISI EVENT (ditetapkan SEBELUM menghitung)")
print("=" * 108)
print(f"  Trigger  : hari PERTAMA seri turun ke <= threshold persentil (p5 / p10)")
print(f"  Cooldown : {COOLDOWN} hari - trigger berikutnya diabaikan sampai cooldown lewat")
print(f"  Tepat sasaran (hit) : |trigger - bear low terkonfirmasi| <= {WIN_LOW} hari")
print(f"  Failure mode        : drawdown MAKSIMUM {DD_HOR} hari sesudah trigger <= {DD_LIMIT:.0f}%")
print(f"  Mode threshold      : (A) full-history persentil [sesuai instruksi, IN-SAMPLE/lookahead]")
print(f"                        (B) trailing {PCTL_WIN} hari at-gate [anti-lookahead]")
print("  TIDAK ada grid search: hanya p5 & p10, dan SEMUA 6 seri dilaporkan apa adanya.")

px = an.set_index("date")["btc_price"]
dates = an["date"].values
prices = an["btc_price"].values
last_date = an["date"].max()

def fwd_stats(i):
    """drawdown maksimum & return pada horizon DD_HOR, dihitung SESUDAH hari i."""
    d0 = an["date"].iloc[i]
    d1 = d0 + pd.Timedelta(days=DD_HOR)
    trunc = d1 > last_date
    m = (an["date"] > d0) & (an["date"] <= d1)
    w = an.loc[m, "btc_price"]
    if len(w) == 0:
        return np.nan, np.nan, np.nan, trunc
    p0 = an["btc_price"].iloc[i]
    mdd = (w.min() / p0 - 1) * 100
    dd_date = an.loc[m, "date"].iloc[int(np.argmin(w.values))]
    ret = (w.iloc[-1] / p0 - 1) * 100
    return mdd, ret, dd_date, trunc

def trailing_pctl(s):
    return s.rolling(PCTL_WIN, min_periods=PCTL_MIN).apply(
        lambda w: (w <= w[-1]).mean() * 100.0, raw=True)

TRAIL = {c: trailing_pctl(an[c]) for c, _, _ in SERIES}

def make_events(col, p, mode):
    s = an[col]
    ok = s.notna().values
    if mode == "full":
        thr = np.nanpercentile(s, p)
        below = (s <= thr).values & ok
        thr_txt = f"{thr:.4g}"
    else:
        below = (TRAIL[col] <= p).values & ok
        thr_txt = f"trailing p{p:.0f}"
    ev, last_i = [], -10**9
    for i in range(len(an)):
        if below[i] and (i - last_i) > COOLDOWN:
            ev.append(i); last_i = i
    rows = []
    for i in ev:
        d0 = an["date"].iloc[i]
        mdd, ret, ddd, trunc = fwd_stats(i)
        gaps = [(d0 - L).days for L in BEAR_LOWS]
        k = int(np.argmin([abs(g) for g in gaps]))
        rows.append({
            "series": col, "weighting": dict((c, w) for c, w, _ in SERIES)[col],
            "pctl": p, "mode": mode, "threshold": thr_txt,
            "trigger_date": d0.date(), "cycle": an["cycle"].iloc[i],
            "price": round(float(an["btc_price"].iloc[i]), 2),
            "value": round(float(s.iloc[i]), 5),
            "nearest_low": BEAR_LOWS[k].date(), "days_to_low": gaps[k],
            "hit_60d": abs(gaps[k]) <= WIN_LOW,
            "max_dd_90d_pct": None if np.isnan(mdd) else round(mdd, 2),
            "dd_date": None if not isinstance(ddd, pd.Timestamp) else ddd.date(),
            "fail_dd20": (not np.isnan(mdd)) and mdd <= DD_LIMIT,
            "ret_90d_pct": None if np.isnan(ret) else round(ret, 2),
            "truncated": trunc,
            "scoreable": d0 <= SCORE_CUTOFF,
        })
    return pd.DataFrame(rows)

all_ev = []
for col, _, _ in SERIES:
    for p in PCTLS:
        for mode in ["full", "trailing"]:
            e = make_events(col, p, mode)
            if len(e):
                all_ev.append(e)
EV = pd.concat(all_ev, ignore_index=True)

# =============================================================================
# 3. TABEL PRESISI
# =============================================================================
print(NL + "=" * 108)
print("3. PRESISI PER SERI - MODE A (full-history persentil, IN-SAMPLE)")
print("=" * 108)
print(f"  Event dengan trigger > {SCORE_CUTOFF.date()} (sesudah cycle peak terakhir) DIKELUARKAN")
print("  dari presisi/recall: bear low cycle berjalan belum terkonfirmasi. Lihat section 9.")

def summary(mode):
    print(NL + f"  {'seri':<15}{'bobot':<16}{'p':>4}{'n ev':>6}{'hit +-60d':>11}{'presisi':>9}"
          f"{'recall 4 low':>14}{'fail DD>=20%':>14}{'med DD90':>10}")
    rows = []
    for col, w, _ in SERIES:
        for p in PCTLS:
            e = EV[(EV.series == col) & (EV.pctl == p) & (EV["mode"] == mode) & EV.scoreable]
            if len(e) == 0:
                print(f"  {col:<15}{w:<16}{p:>4.0f}{0:>6}   (tidak ada event)"); continue
            hits = int(e.hit_60d.sum())
            prec = hits / len(e) * 100
            lows_hit = e.loc[e.hit_60d, "nearest_low"].nunique()
            usable = e[e.max_dd_90d_pct.notna()]
            fails = int(usable.fail_dd20.sum())
            failp = fails / len(usable) * 100 if len(usable) else np.nan
            medd = usable.max_dd_90d_pct.median() if len(usable) else np.nan
            print(f"  {col:<15}{w:<16}{p:>4.0f}{len(e):>6}{hits:>11}{prec:>8.1f}%"
                  f"{lows_hit:>10}/4{fails:>8}/{len(usable):<5}{medd:>9.1f}%")
            rows.append(dict(series=col, weighting=w, pctl=p, mode=mode, n_events=len(e),
                             hits=hits, precision_pct=round(prec, 1), lows_recalled=lows_hit,
                             n_fail_dd20=fails, n_usable=len(usable),
                             fail_rate_pct=None if np.isnan(failp) else round(failp, 1),
                             median_dd90_pct=None if np.isnan(medd) else round(medd, 2)))
    return pd.DataFrame(rows)

sumA = summary("full")
print(NL + "=" * 108)
print("4. PRESISI PER SERI - MODE B (persentil TRAILING 4 tahun, AT-GATE / anti-lookahead)")
print("=" * 108)
sumB = summary("trailing")

# ---- sebaran per cycle ------------------------------------------------------
print(NL + "=" * 108)
print("5. SEBARAN EVENT PER CYCLE (mode A full-history, p10)")
print("=" * 108)
for col, _, _ in SERIES:
    e = EV[(EV.series == col) & (EV.pctl == 10.0) & (EV["mode"] == "full") & EV.scoreable]
    cyc = e.cycle.value_counts().reindex(
        ["cycle-2011", "cycle-2015", "cycle-2018", "cycle-2022", "cycle-2026"], fill_value=0)
    print(f"  {col:<15} n={len(e):>3}   " + "  ".join(f"{k.replace('cycle-',''):}={v}" for k, v in cyc.items()))

# =============================================================================
# 6. FAILURE MODE - daftar event lengkap seri utama
# =============================================================================
print(NL + "=" * 108)
print("6. FAILURE MODE - DAFTAR EVENT LENGKAP (mode A full-history, p10)")
print("=" * 108)
for col in ["vdd_mult_ma", "sacdd_ma30", "sacdd_ma900", "cdd_mult_ma", "price_ratio"]:
    e = EV[(EV.series == col) & (EV.pctl == 10.0) & (EV["mode"] == "full")]
    if len(e) == 0: continue
    print(NL + f"  --- {col} (n={len(e)}) ---")
    print(f"    {'trigger':<12}{'harga':>11}{'ke low':>9}{'hit':>6}{'maxDD90':>10}{'tgl DD':>12}{'ret90':>9}")
    for _, r in e.iterrows():
        dd = "n/a" if r.max_dd_90d_pct is None else f"{r.max_dd_90d_pct:.1f}%"
        rt = "n/a" if r.ret_90d_pct is None else f"{r.ret_90d_pct:.1f}%"
        flag = " <-- FAIL" if r.fail_dd20 else ""
        print(f"    {str(r.trigger_date):<12}{r.price:>11,.0f}{r.days_to_low:>9}"
              f"{('YA' if r.hit_60d else '-'):>6}{dd:>10}{str(r.dd_date):>12}{rt:>9}{flag}")

print(NL + "  Distribusi drawdown maksimum 90d (mode A, p10, seluruh event semua seri):")
u = EV[(EV.pctl == 10.0) & (EV["mode"] == "full") & EV.max_dd_90d_pct.notna() & EV.scoreable]
for col, _, _ in SERIES:
    s = u.loc[u.series == col, "max_dd_90d_pct"]
    if len(s) == 0: continue
    print(f"    {col:<15} n={len(s):>3}  min={s.min():>7.1f}%  p25={s.quantile(.25):>7.1f}%  "
          f"median={s.median():>7.1f}%  maks={s.max():>7.1f}%   >=20% turun: {int((s<=DD_LIMIT).sum())}")

# =============================================================================
# 7. KASUS 2018 - yang diakui pembicara sendiri
# =============================================================================
print(NL + "=" * 108)
print("7. REPRODUKSI KASUS 2018 (failure mode yang diakui pembicara)")
print("=" * 108)
p2018 = an[(an.date >= "2018-01-01") & (an.date <= "2019-06-30")]
pk = p2018.loc[p2018.btc_price.idxmax()]
tr = p2018.loc[p2018.btc_price.idxmin()]
print(f"  Konteks harga: puncak periode {pk.date.date()} ${pk.btc_price:,.0f} -> "
      f"bear low 2018-12-14 ${px.asof(pd.Timestamp('2018-12-14')):,.0f}")
nov = an[(an.date >= "2018-11-01") & (an.date <= "2018-12-20")]
print(f"  Downward spike Nov-Des 2018: 2018-11-01 ${px.asof(pd.Timestamp('2018-11-01')):,.0f} -> "
      f"2018-12-14 ${px.asof(pd.Timestamp('2018-12-14')):,.0f}  "
      f"({(px.asof(pd.Timestamp('2018-12-14'))/px.asof(pd.Timestamp('2018-11-01'))-1)*100:.1f}%)")

e18 = EV[(EV["mode"] == "full") &
         (EV.trigger_date.astype(str) >= "2018-01-01") &
         (EV.trigger_date.astype(str) <= "2019-03-31")]
if len(e18) == 0:
    print(NL + "  TIDAK ADA trigger sama sekali di jendela 2018-01-01 .. 2019-03-31 untuk seri manapun.")
else:
    print(NL + f"  {'seri':<15}{'p':>4}{'trigger':<14}{'harga':>11}{'ke low':>9}{'maxDD90':>10}{'ret90':>9}")
    for _, r in e18.sort_values("trigger_date").iterrows():
        dd = "n/a" if r.max_dd_90d_pct is None else f"{r.max_dd_90d_pct:.1f}%"
        rt = "n/a" if r.ret_90d_pct is None else f"{r.ret_90d_pct:.1f}%"
        print(f"  {r.series:<15}{r.pctl:>4.0f} {str(r.trigger_date):<13}{r.price:>11,.0f}"
              f"{r.days_to_low:>9}{dd:>10}{rt:>9}")

print(NL + "  Cek langsung 'sinyal muncul SEBELUM spike': ada trigger di Sep-Nov 2018?")
pre = e18[(e18.trigger_date.astype(str) >= "2018-09-01") & (e18.trigger_date.astype(str) <= "2018-11-14")]
print(f"    n = {len(pre)}" + ("" if len(pre) == 0 else
      "  -> " + ", ".join(f"{r.series} p{r.pctl:.0f} @{r.trigger_date} (DD90 {r.max_dd_90d_pct}%)"
                          for _, r in pre.iterrows())))

# nilai seri di sekitar puncak sebelum spike (tanpa event-gating)
print(NL + "  Level persentil TRAILING seri di 2018-11-01 (sebelum spike) vs 2018-12-14 (low):")
for col, _, _ in SERIES:
    i1 = an.index[an.date == "2018-11-01"]
    i2 = an.index[an.date == "2018-12-14"]
    if len(i1) and len(i2):
        print(f"    {col:<15} 2018-11-01 pctl={TRAIL[col].iloc[i1[0]]:>6.1f}   "
              f"2018-12-14 pctl={TRAIL[col].iloc[i2[0]]:>6.1f}")

# =============================================================================
# 8. HEAD-TO-HEAD CONFOUND: value-weighted vs unit-weighted vs harga murni
# =============================================================================
print(NL + "=" * 108)
print("8. HEAD-TO-HEAD - kalau komponen harga dilepas, presisinya runtuh atau tidak?")
print("=" * 108)
for mode in ["full", "trailing"]:
    print(NL + f"  MODE {'A (full-history)' if mode=='full' else 'B (trailing at-gate)'}, p10:")
    print(f"    {'seri':<15}{'bobot':<16}{'n':>4}{'presisi':>9}{'recall':>8}{'fail DD20':>11}")
    for col, w, _ in SERIES:
        e = EV[(EV.series == col) & (EV.pctl == 10.0) & (EV["mode"] == mode) & EV.scoreable]
        if len(e) == 0:
            print(f"    {col:<15}{w:<16}{0:>4}   (tidak ada event)"); continue
        us = e[e.max_dd_90d_pct.notna()]
        print(f"    {col:<15}{w:<16}{len(e):>4}{e.hit_60d.mean()*100:>8.1f}%"
              f"{e.loc[e.hit_60d,'nearest_low'].nunique():>6}/4"
              f"{int(us.fail_dd20.sum()):>7}/{len(us):<4}")

# overlap trigger VDD vs price_ratio
def trig_set(col, p, mode, tol=30):
    return set(pd.to_datetime(EV[(EV.series == col) & (EV.pctl == p) &
                                 (EV["mode"] == mode) & EV.scoreable].trigger_date))
A = trig_set("vdd_mult_ma", 10.0, "full")
B = trig_set("price_ratio", 10.0, "full")
C = trig_set("cdd_mult_ma", 10.0, "full")
def near(a, b, tol=45):
    return sum(1 for x in a if any(abs((x - y).days) <= tol for y in b))
print(NL + f"  Overlap trigger (+-45 hari), mode A p10:")
print(f"    VDD Mult ({len(A)} ev) yang punya pasangan di price_ratio ({len(B)} ev) : {near(A,B)}/{len(A)}")
print(f"    VDD Mult ({len(A)} ev) yang punya pasangan di cdd_mult   ({len(C)} ev) : {near(A,C)}/{len(A)}")

# =============================================================================
# 9. LOW 2026 YANG BELUM TERKONFIRMASI - dilaporkan TERPISAH
# =============================================================================
print(NL + "=" * 108)
print("9. LOW SEMENTARA 2026-06-30 (BELUM TERKONFIRMASI - tidak dihitung sebagai bukti)")
print("=" * 108)
print(f"  Harga 2026-06-30 = ${px.asof(LOW_UNCONF):,.0f};  hari terakhir data "
      f"{last_date.date()} = ${px.asof(last_date):,.0f}")
e26 = EV[(EV["mode"] == "full") & (EV.trigger_date.astype(str) >= "2026-01-01")]
if len(e26) == 0:
    print("  Tidak ada trigger di 2026 untuk seri manapun (mode A).")
else:
    for _, r in e26.sort_values("trigger_date").iterrows():
        print(f"    {r.series:<15} p{r.pctl:>2.0f}  {r.trigger_date}  harga ${r.price:,.0f}  "
              f"jarak ke 2026-06-30 = {(pd.Timestamp(str(r.trigger_date)) - LOW_UNCONF).days} hari  "
              f"maxDD90 {r.max_dd_90d_pct} (truncated={r.truncated})")
print(NL + f"  Event dengan trigger > {SCORE_CUTOFF.date()} memang DIKELUARKAN dari presisi/recall "
      f"(kolom scoreable=False di CSV): n={int((~EV.scoreable).sum())} baris dari {len(EV)}.")
print(f"  (Bear low yang dipakai hanya 4 yang terkonfirmasi: {[str(d.date()) for d in BEAR_LOWS]})")

# ---- CSV --------------------------------------------------------------------
out = os.path.join(OUTDIR, "events_cdd_vdd_bottom_precision.csv")
EV.to_csv(out, index=False)
print(NL + f"CSV event lengkap disimpan : {out}   (n baris = {len(EV)})")
out2 = os.path.join(OUTDIR, "events_cdd_vdd_precision_summary.csv")
pd.concat([sumA, sumB], ignore_index=True).to_csv(out2, index=False)
print(f"CSV ringkasan presisi      : {out2}")
print(NL + "SELESAI.")
