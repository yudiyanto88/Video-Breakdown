# -*- coding: utf-8 -*-
"""
V1 — Reachability threshold K4 lintas cycle (rising troughs?)

KLAIM YANG DIUJI (video BM Pro 2026-08-05, insight #4):
  "each trough higher" - trough MVRV tiap cycle makin tinggi. Basis video: n=3 bear low,
  kualitatif, tanpa angka.

KENAPA PENTING: K4 di Decision_Framework v2 memakai 4 kondisi threshold ABSOLUT:
  (1) LTH-MVRV < 1.0
  (2) aSOPR < 0.93 selama >=7 hari BERTURUT DAN LTH-SOPR < 0.50
  (3) Supply in Profit < 50% DAN STH profit < 10%
  (4) Price/CVDD < 1.10   (flag ekstrem <= 1.0)
Kalau trough naik struktural, K4 bisa gagal arm bukan karena pasar belum murah,
tapi karena penggarisnya usang.

--- DEFINISI EVENT (STANDAR VALIDASI poin 1) ---
Cycle bottom = konvensi bottom-to-bottom yang SUDAH established di project Onchain-Dashboard
  (research/framework_review_2026-07/backtest_k5nz/run_backtest.py):
      S1 2013-01-01 -> 2015-01-14
      S2 2015-01-15 -> 2018-12-15
      S3 2018-12-16 -> 2022-11-21
      S4 2022-11-22 -> 2026-07-15 (BELUM SELESAI)
"BEAR" = window dari CYCLE PEAK (harga tertinggi dalam window cycle itu) s/d CYCLE BOTTOM
  (tanggal batas akhir cycle di atas). Untuk bear berjalan (2025-26): peak s/d baris data
  terakhir 2026-07-15 -> BELUM SELESAI, minimum-nya masih bisa turun.
  B1 = peak 2013 -> 2015-01-14
  B2 = peak 2017 -> 2018-12-15
  B3 = peak 2021 -> 2022-11-21
  B4 = peak 2025 -> 2026-07-15 (ongoing)
SUPLEMEN (di luar konvensi established, dilaporkan terpisah, TIDAK masuk klaim utama):
  B0 = bear 2011 (peak 2011 -> low 2011), data mulai 2010-07-17.

Tidak ada merge/cooldown yang relevan: tiap bear = 1 window kontinu, 1 observasi per metrik
(minimum dalam window). n observasi = jumlah bear, bukan jumlah hari.

--- ANTI LOOKAHEAD (poin 3) ---
Ini uji DESKRIPTIF (apakah minimum historis naik), bukan sinyal keputusan. Tidak ada
keputusan yang diambil di dalam window, jadi tidak ada gate yang bisa bocor. Yang perlu
diingat: batas window (cycle bottom) memang ditentukan ex-post — itu memang sifat pertanyaan
"seberapa dalam bear ini", dan disebut eksplisit di findings.

--- CATATAN DATA ---
Semua kolom yang dipakai (mvrv_ratio, lth_mvrv, percent_btc_in_profit, pct_sth_in_profit,
asopr, lth_sopr, cvdd, btc_price) tersedia penuh sejak 2010-07-17 -> uji lintas-cycle penuh
mungkin untuk 4 bear. Data terakhir 2026-07-15, video 2026-08-05 -> selisih ~3 minggu.
"""

import pandas as pd
import numpy as np

DATA = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUT = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-05_the-free-simple-strategy-that-beats-bitcoin-it-just-flashed-again"

pd.set_option("display.width", 200)

df = pd.read_csv(DATA, parse_dates=["date"])
df = df.dropna(subset=["btc_price", "mvrv_ratio", "lth_mvrv", "asopr", "lth_sopr",
                       "percent_btc_in_profit", "pct_sth_in_profit", "cvdd",
                       "realized_price", "sth_cost_basis"]).copy()
df = df[df["btc_price"] > 0].sort_values("date").reset_index(drop=True)
LAST = df["date"].max()
print(f"Data: {df['date'].min().date()} s/d {LAST.date()}  (n={len(df)} hari)")
print("CATATAN: data berhenti 2026-07-15, video tanggal 2026-08-05 -> selisih ~3 minggu.")
print("         Semua pembacaan 'saat ini' di bawah = per 2026-07-15, bukan tanggal video.\n")

# --- kondisi K4 (disalin dari btlib.build_all, jangan hitung ulang formula sendiri) ---
df["p_cvdd"] = df["btc_price"] / df["cvdd"]
c1 = df["lth_mvrv"] < 1.0
b93 = df["asopr"] < 0.93
streak93 = (b93.groupby((~b93).cumsum()).cumcount() + 1).where(b93, 0)
c2 = (streak93 >= 7) & (df["lth_sopr"] < 0.50)
c3 = (df["percent_btc_in_profit"] < 50) & (df["pct_sth_in_profit"] < 10)
c4 = df["p_cvdd"] < 1.10
df["k4_c1"] = c1.fillna(False)
df["k4_c2"] = c2.fillna(False)
df["k4_c3"] = c3.fillna(False)
df["k4_c4"] = c4.fillna(False)
df["k4_count"] = df[["k4_c1", "k4_c2", "k4_c3", "k4_c4"]].sum(axis=1)
df["k4_extreme"] = df["p_cvdd"] <= 1.0

# MA7 untuk SOPR (SOPR harian sangat noisy; minimum harian mentah juga dilaporkan)
df["asopr_ma7"] = df["asopr"].rolling(7, min_periods=7).mean()
df["lth_sopr_ma7"] = df["lth_sopr"].rolling(7, min_periods=7).mean()

# --- window cycle (established) ---
CYCLES = [
    ("S1 2013-2015", "2013-01-01", "2015-01-14"),
    ("S2 2015-2018", "2015-01-15", "2018-12-15"),
    ("S3 2018-2022", "2018-12-16", "2022-11-21"),
    ("S4 2022-now",  "2022-11-22", str(LAST.date())),
]
BEAR_LABEL = {"S1 2013-2015": "B1 bear 2014-15",
              "S2 2015-2018": "B2 bear 2018",
              "S3 2018-2022": "B3 bear 2022",
              "S4 2022-now":  "B4 bear 2025-26 (ONGOING)"}

bears = []
for cn, lo, hi in CYCLES:
    w = df[(df["date"] >= lo) & (df["date"] <= hi)]
    pk = w.loc[w["btc_price"].idxmax()]
    bw = df[(df["date"] >= pk["date"]) & (df["date"] <= pd.Timestamp(hi))]
    lo_row = bw.loc[bw["btc_price"].idxmin()]
    bears.append(dict(label=BEAR_LABEL[cn], cycle=cn,
                      peak_date=pk["date"], peak_price=pk["btc_price"],
                      end_date=pd.Timestamp(hi),
                      low_date=lo_row["date"], low_price=lo_row["btc_price"],
                      win=bw, ongoing=(cn == "S4 2022-now")))

# SUPLEMEN: bear 2011 (di luar konvensi established)
w11 = df[(df["date"] >= "2010-07-17") & (df["date"] <= "2012-12-31")]
pk11 = w11.loc[w11["btc_price"].idxmax()]
tail11 = df[(df["date"] >= pk11["date"]) & (df["date"] <= "2012-01-31")]
lo11 = tail11.loc[tail11["btc_price"].idxmin()]
bw11 = df[(df["date"] >= pk11["date"]) & (df["date"] <= lo11["date"])]
bear11 = dict(label="B0 bear 2011 (SUPLEMEN)", cycle="pre-S1",
              peak_date=pk11["date"], peak_price=pk11["btc_price"],
              end_date=lo11["date"], low_date=lo11["date"], low_price=lo11["btc_price"],
              win=bw11, ongoing=False)

print("=" * 118)
print("WINDOW BEAR (peak cycle -> cycle bottom, konvensi bottom-to-bottom established)")
print("=" * 118)
for b in [bear11] + bears:
    print(f"  {b['label']:<28} peak {b['peak_date'].date()} ${b['peak_price']:>10,.0f}  ->  "
          f"low {b['low_date'].date()} ${b['low_price']:>10,.2f}   "
          f"({len(b['win'])} hari, drawdown {b['low_price']/b['peak_price']-1:+.1%})")

# =====================================================================
# (a) MINIMUM tiap metrik per bear
# =====================================================================
METRICS = [
    ("mvrv_ratio",            "MVRV Ratio",        None),
    ("lth_mvrv",              "LTH-MVRV",          1.00),
    ("percent_btc_in_profit", "Supply in Profit %", 50.0),
    ("pct_sth_in_profit",     "STH in Profit %",   10.0),
    ("asopr_ma7",             "aSOPR (MA7)",       0.93),
    ("lth_sopr_ma7",          "LTH-SOPR (MA7)",    0.50),
    ("p_cvdd",                "Price/CVDD",        1.10),
]

print("\n" + "=" * 118)
print("(a) MINIMUM TIAP METRIK PER BEAR  [tanggal minimum dalam kurung]")
print("    Kolom 'thr' = threshold K4 terkait. Tanda * = threshold TERSENTUH (min < thr).")
print("=" * 118)
hdr = f"{'metrik':<20}{'thr':>7}"
for b in [bear11] + bears:
    hdr += f"{b['label'].split()[0]:>26}"
print(hdr)
print("-" * 118)

min_table = {}
for col, name, thr in METRICS:
    line = f"{name:<20}{('-' if thr is None else f'{thr:g}'):>7}"
    for b in [bear11] + bears:
        s = b["win"][["date", col]].dropna()
        if s.empty:
            line += f"{'n/a':>26}"
            continue
        i = s[col].idxmin()
        v = s.loc[i, col]
        d = s.loc[i, "date"].date()
        hit = "*" if (thr is not None and v < thr) else " "
        line += f"{v:>10.3f}{hit} {str(d):>14}"
        min_table[(b["label"], name)] = (v, d, hit == "*")
    print(line)

# minimum aSOPR & LTH-SOPR harian mentah (pembanding, tanpa MA)
print("\n  Pembanding tanpa smoothing (minimum harian mentah):")
for col, name in [("asopr", "aSOPR harian"), ("lth_sopr", "LTH-SOPR harian")]:
    line = f"  {name:<20}"
    for b in [bear11] + bears:
        s = b["win"][["date", col]].dropna()
        i = s[col].idxmin()
        line += f"{s.loc[i, col]:>10.3f} {str(s.loc[i,'date'].date()):>13}"
    print(line)

# =====================================================================
# (b) & (c) hari kondisi K4 terpenuhi per bear
# =====================================================================
print("\n" + "=" * 118)
print("(b) JUMLAH HARI TIAP KONDISI K4 TERPENUHI PER BEAR (dan % dari panjang bear)")
print("(c) JUMLAH HARI count >=2 / >=3 / =4")
print("=" * 118)
print(f"{'bear':<28}{'hari':>6}{'C1':>13}{'C2':>13}{'C3':>13}{'C4':>13}{'>=2':>11}{'>=3':>11}{'=4':>11}{'P/CVDD<=1':>11}")
print("-" * 118)
rows_csv = []
for b in [bear11] + bears:
    w = b["win"]
    n = len(w)
    def fmt(mask):
        k = int(mask.sum())
        return f"{k:>5}({k/n*100:>4.1f}%)"
    r = dict(bear=b["label"], cycle=b["cycle"],
             peak_date=b["peak_date"].date(), peak_price=round(b["peak_price"], 2),
             low_date=b["low_date"].date(), low_price=round(b["low_price"], 2),
             bear_days=n, ongoing=b["ongoing"],
             days_c1=int(w["k4_c1"].sum()), days_c2=int(w["k4_c2"].sum()),
             days_c3=int(w["k4_c3"].sum()), days_c4=int(w["k4_c4"].sum()),
             days_cnt_ge2=int((w["k4_count"] >= 2).sum()),
             days_cnt_ge3=int((w["k4_count"] >= 3).sum()),
             days_cnt_eq4=int((w["k4_count"] == 4).sum()),
             days_extreme=int(w["k4_extreme"].sum()))
    for col, name, thr in METRICS:
        s = w[["date", col]].dropna()
        if s.empty:
            r[f"min_{col}"] = None
            r[f"min_{col}_date"] = None
            continue
        i = s[col].idxmin()
        r[f"min_{col}"] = round(float(s.loc[i, col]), 4)
        r[f"min_{col}_date"] = s.loc[i, "date"].date()
    rows_csv.append(r)
    print(f"{b['label']:<28}{n:>6}"
          f"{fmt(w['k4_c1'])}{fmt(w['k4_c2'])}{fmt(w['k4_c3'])}{fmt(w['k4_c4'])}"
          f"{int((w['k4_count']>=2).sum()):>11}{int((w['k4_count']>=3).sum()):>11}"
          f"{int((w['k4_count']==4).sum()):>11}{int(w['k4_extreme'].sum()):>11}")

# =====================================================================
# MONOTONISITAS
# =====================================================================
print("\n" + "=" * 118)
print("UJI MONOTONISITAS MINIMUM LINTAS 3 BEAR SELESAI (B1 -> B2 -> B3)")
print("  n=3 bear SELESAI + 1 bear BERJALAN (B4, belum selesai - minimumnya masih bisa turun)")
print("=" * 118)
done = [b["label"] for b in bears[:3]]
for col, name, thr in METRICS:
    vals = []
    for lab in done:
        vals.append(min_table.get((lab, name), (np.nan, None, False))[0])
    v4 = min_table.get((bears[3]["label"], name), (np.nan, None, False))[0]
    mono_up = all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))
    mono_dn = all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
    verdict = "NAIK monoton" if mono_up else ("TURUN monoton" if mono_dn else "TIDAK monoton")
    print(f"  {name:<20} B1={vals[0]:>8.3f}  B2={vals[1]:>8.3f}  B3={vals[2]:>8.3f}  "
          f"-> {verdict:<14} | B4(ongoing)={v4:>8.3f}")

print("\n  Threshold K4 yang TIDAK PERNAH tersentuh, per bear:")
for b in [bear11] + bears:
    never = []
    for col, name, thr in METRICS:
        if thr is None:
            continue
        v = min_table.get((b["label"], name), (np.nan, None, False))
        if not v[2]:
            never.append(name)
    # kondisi K4 level (bukan metrik tunggal)
    w = b["win"]
    never_cond = [f"C{i+1}" for i, c in enumerate(["k4_c1", "k4_c2", "k4_c3", "k4_c4"])
                  if int(w[c].sum()) == 0]
    print(f"    {b['label']:<28} metrik tak tersentuh: {', '.join(never) if never else '(semua tersentuh)'}")
    print(f"    {'':<28} kondisi K4 0 hari    : {', '.join(never_cond) if never_cond else '(semua pernah nyala)'}")

# =====================================================================
# STATUS TERAKHIR (per 2026-07-15)
# =====================================================================
last = df.iloc[-1]
print("\n" + "=" * 118)
print(f"STATUS PER {LAST.date()} (BUKAN tanggal video 2026-08-05 - selisih ~3 minggu)")
print("=" * 118)
print(f"  price=${last['btc_price']:,.0f}  STH RP=${last['sth_cost_basis']:,.0f}  "
      f"RP=${last['realized_price']:,.0f}  LTH RP=${last['lth_cost_basis']:,.0f}  CVDD=${last['cvdd']:,.0f}")
print(f"  MVRV={last['mvrv_ratio']:.3f}  LTH-MVRV={last['lth_mvrv']:.3f}  "
      f"SupplyProfit={last['percent_btc_in_profit']:.1f}%  STHProfit={last['pct_sth_in_profit']:.1f}%")
print(f"  aSOPR={last['asopr']:.3f} (MA7={last['asopr_ma7']:.3f})  "
      f"LTH-SOPR={last['lth_sopr']:.3f} (MA7={last['lth_sopr_ma7']:.3f})  P/CVDD={last['p_cvdd']:.3f}")
print(f"  K4: C1={bool(last['k4_c1'])} C2={bool(last['k4_c2'])} C3={bool(last['k4_c3'])} "
      f"C4={bool(last['k4_c4'])} -> count={int(last['k4_count'])}")

# =====================================================================
# CSV
# =====================================================================
outdf = pd.DataFrame(rows_csv)
path = OUT + r"\events_k4_threshold_reachability.csv"
outdf.to_csv(path, index=False)
print(f"\nCSV per-bear disimpan: {path}")
