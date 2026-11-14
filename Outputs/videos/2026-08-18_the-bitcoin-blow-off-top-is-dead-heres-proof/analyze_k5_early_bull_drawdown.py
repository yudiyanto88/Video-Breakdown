"""
V1 -- Drawdown early-bull vs cap LTV 45% di K5
Video: On-Chain Mind "The Bitcoin Blow-Off Top Is Dead (Here's Proof)" (2026-08-18)

KLAIM VIDEO: drawdown 20-45% RUTIN di 12 bulan pertama bull
  - 2019: -45% (dari 4x di 26 Jun 2019)
  - 2015: -34% (dari $296 Mar 2015 ke $194 Agu 2015)
  - 2023: -20% (dari ~$31k Jul 2023 ke ~$25k 11 Sep 2023)
Teks K5 framework: "koreksi 15-30% yang RUTIN di setiap early bull".

PERTANYAAN INTI: drawdown >=30% itu terjadi DI DALAM jendela K5 atau di luarnya?

DEFINISI EVENT (dikunci di muka, tidak diubah setelah lihat hasil):
  - Jendela K5 per cycle:
      START = hari pertama sth_cost_basis (STH RP) close di ATAS realized_price (RP)
              setelah cycle bottom  [= framework: "STH RP cross ke atas RP"]
      END   = hari ke-3 dari 3 hari berturut-turut btc_price >= AVIV Upper
              [= framework: "harga cross AVIV Upper >=3 hari"]
  - AVIV Upper = price_at_aviv_mean + 0.5*(price_at_aviv_plus_1_sigma - price_at_aviv_mean)
    (pola dari research/analyze_k3_stage_comparison.py -- +0.5 SD, tidak dihitung ulang)
  - Entry K5 = hari pertama btc_price <= 95% dari trailing high 30 hari (rolling max
    HANYA data masa lalu s/d hari itu -- anti lookahead), di dalam jendela K5
  - Merge: entry berjarak < 14 hari dari entry sebelumnya digabung (ambil yang pertama)
  - Outcome: max drawdown dari harga entry sampai
      (a) akhir jendela K5, dan (b) entry + 180 hari  -- DUA horizon terpisah
  - Ambang: >=20% (cut-loss), >=25% (LTV-60 dari cap 45%), >=33% (LTV-60 dari cap 52% lama)

Output: print ASCII saja (Windows console), CSV event, tabel klasifikasi zona.
"""

import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-18_the-bitcoin-blow-off-top-is-dead-heres-proof"

PULLBACK_PCT   = 0.95   # <= 95% trailing high 30d
TRAIL_DAYS     = 30
MERGE_DAYS     = 14
HORIZON_DAYS   = 180
AVIV_UPPER_SD  = 0.5
CONFIRM_DAYS   = 3      # hari berturut >= AVIV Upper untuk tutup K5

# --- Load -------------------------------------------------------------------
df = pd.read_csv(MASTER, parse_dates=["date"])
cols = ["date", "btc_price", "sth_cost_basis", "realized_price", "lth_cost_basis",
        "price_at_aviv_mean", "price_at_aviv_plus_1_sigma"]
df = df[cols].sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "sth_cost_basis", "realized_price"])
df = df[df["btc_price"] > 0].reset_index(drop=True)

df["aviv_upper"] = df["price_at_aviv_mean"] + AVIV_UPPER_SD * (
    df["price_at_aviv_plus_1_sigma"] - df["price_at_aviv_mean"])

print("=" * 100)
print("V1 -- DRAWDOWN EARLY-BULL DI DALAM JENDELA K5")
print("=" * 100)
print(f"Data: {df['date'].min().date()} s/d {df['date'].max().date()}  (n hari = {len(df)})")
print("CATATAN: data master terakhir update 2026-07-15 -- cycle C3 pasca-peak masih berjalan.")

# --- Cycle bottoms & peaks (deteksi sendiri, tidak asal terima referensi) ----
BOTTOM_SEARCH = [("C0", "2011-06-15", "2012-03-01"),
                 ("C1", "2014-06-01", "2015-12-31"),
                 ("C2", "2018-06-01", "2019-06-30"),
                 ("C3", "2022-06-01", "2023-06-30")]
PEAK_SEARCH   = [("C0", "2013-01-01", "2014-06-01"),
                 ("C1", "2017-06-01", "2018-06-01"),
                 ("C2", "2021-01-01", "2022-06-01"),
                 ("C3", "2025-01-01", "2026-07-15")]

def extreme(a, b, how):
    w = df[(df["date"] >= a) & (df["date"] <= b)]
    i = w["btc_price"].idxmin() if how == "min" else w["btc_price"].idxmax()
    return df.loc[i, "date"], df.loc[i, "btc_price"]

cycles = {}
print("\nVERIFIKASI TANGGAL SIKLUS (dari btc_price, deteksi sendiri):")
print(f"{'Cyc':<5}{'Bottom':<13}{'P_bottom':>12}   {'Peak':<13}{'P_peak':>13}   {'Multiple':>9}")
print("-" * 76)
for (c, ba, bb), (_, pa, pb) in zip(BOTTOM_SEARCH, PEAK_SEARCH):
    bd, bp = extreme(ba, bb, "min")
    pd_, pp = extreme(pa, pb, "max")
    cycles[c] = dict(bottom=bd, p_bottom=bp, peak=pd_, p_peak=pp)
    print(f"{c:<5}{bd.date().isoformat():<13}{bp:>12,.2f}   "
          f"{pd_.date().isoformat():<13}{pp:>13,.2f}   {pp/bp:>8.1f}x")

# --- Jendela K5 per cycle ---------------------------------------------------
def k5_window(bottom_date, peak_date):
    """START: STH RP cross ke atas RP setelah bottom. END: 3 hari berturut P >= AVIV Upper."""
    w = df[df["date"] >= bottom_date].reset_index(drop=True)
    above = (w["sth_cost_basis"] > w["realized_price"]).values
    start_i = None
    for i in range(1, len(w)):
        if above[i] and not above[i - 1]:
            start_i = i
            break
    if start_i is None:
        return None, None, None
    start_date = w.loc[start_i, "date"]
    # END: cari 3 hari berturut close >= AVIV Upper, setelah start
    sub = w.iloc[start_i:].reset_index(drop=True)
    ge = (sub["btc_price"] >= sub["aviv_upper"]).values
    run = 0
    end_date = None
    for i in range(len(sub)):
        run = run + 1 if ge[i] else 0
        if run >= CONFIRM_DAYS:
            end_date = sub.loc[i, "date"]
            break
    # semua cross STH RP > RP setelah bottom (untuk cek whipsaw)
    n_cross = int(((~pd.Series(above).shift(1).fillna(False).astype(bool)) & pd.Series(above)).sum())
    return start_date, end_date, n_cross

print("\nJENDELA K5 PER CYCLE")
print(f"{'Cyc':<5}{'K5 start':<13}{'K5 end':<13}{'Durasi':>8}{'  P@start':>12}{'  P@end':>13}"
      f"{'  end vs peak':>14}")
print("-" * 90)
for c in cycles:
    s, e, ncr = k5_window(cycles[c]["bottom"], cycles[c]["peak"])
    cycles[c]["k5_start"], cycles[c]["k5_end"] = s, e
    ps = df.loc[df["date"] == s, "btc_price"].iloc[0] if s is not None else np.nan
    pe = df.loc[df["date"] == e, "btc_price"].iloc[0] if e is not None else np.nan
    dur = (e - s).days if (s is not None and e is not None) else None
    dvp = (cycles[c]["peak"] - e).days if e is not None else None
    print(f"{c:<5}{str(s.date()) if s is not None else 'NONE':<13}"
          f"{str(e.date()) if e is not None else 'NONE':<13}"
          f"{(str(dur)+'d') if dur else '-':>8}{ps:>12,.2f}{pe:>13,.2f}"
          f"{('peak -'+str(dvp)+'d') if dvp else '-':>14}")

# --- Entry events di dalam jendela K5 ---------------------------------------
df["trail_high30"] = df["btc_price"].rolling(TRAIL_DAYS, min_periods=TRAIL_DAYS).max()  # inklusif hari ini, masa lalu saja
df["is_pullback"]  = df["btc_price"] <= PULLBACK_PCT * df["trail_high30"]

rows = []
for c in cycles:
    s, e = cycles[c]["k5_start"], cycles[c]["k5_end"]
    if s is None or e is None:
        continue
    w = df[(df["date"] >= s) & (df["date"] <= e)].reset_index(drop=True)
    last_entry = None
    for i in range(len(w)):
        if not bool(w.loc[i, "is_pullback"]):
            continue
        d = w.loc[i, "date"]
        if last_entry is not None and (d - last_entry).days < MERGE_DAYS:
            continue
        last_entry = d
        p_entry = w.loc[i, "btc_price"]
        # (a) sampai akhir jendela K5
        fw_k5 = w[(w["date"] >= d)]
        mdd_k5 = (fw_k5["btc_price"].min() / p_entry - 1) * 100
        dt_k5  = fw_k5.loc[fw_k5["btc_price"].idxmin(), "date"]
        # (b) sampai +180 hari (boleh melewati akhir jendela K5)
        fw_180 = df[(df["date"] >= d) & (df["date"] <= d + pd.Timedelta(days=HORIZON_DAYS))]
        mdd_180 = (fw_180["btc_price"].min() / p_entry - 1) * 100
        dt_180  = fw_180.loc[fw_180["btc_price"].idxmin(), "date"]
        rows.append(dict(cycle=c, entry_date=d.date(), entry_price=round(p_entry, 2),
                         pct_off_high=round((p_entry / w.loc[i, "trail_high30"] - 1) * 100, 2),
                         mdd_to_k5_end_pct=round(mdd_k5, 2), mdd_k5_trough_date=dt_k5.date(),
                         mdd_180d_pct=round(mdd_180, 2), mdd_180d_trough_date=dt_180.date(),
                         k5_start=s.date(), k5_end=e.date()))

ev = pd.DataFrame(rows)
ev.to_csv(rf"{OUTDIR}\events_k5_early_bull_drawdown.csv", index=False)

print(f"\nEVENT ENTRY K5 (pullback <= -5% dari trailing high 30d, merge <{MERGE_DAYS}d)")
print(f"n TOTAL = {len(ev)}")
print("Sebaran per cycle: " + ", ".join(f"{c}={int((ev['cycle']==c).sum())}" for c in cycles))

print(f"\n{'Cyc':<5}{'Entry':<13}{'P entry':>12}{'  off high':>10}"
      f"{'  MDD->K5end':>13}{'  MDD 180d':>11}")
print("-" * 68)
for _, r in ev.iterrows():
    print(f"{r['cycle']:<5}{str(r['entry_date']):<13}{r['entry_price']:>12,.2f}"
          f"{r['pct_off_high']:>10.1f}%{r['mdd_to_k5_end_pct']:>12.1f}%{r['mdd_180d_pct']:>10.1f}%")

# --- Jawaban ambang ---------------------------------------------------------
def share(col, thr):
    hit = (ev[col] <= -thr)
    return hit.sum(), len(ev), hit.sum() / len(ev) * 100

print("\n" + "=" * 100)
print("JAWABAN AMBANG (fraksi entry yang drawdown-nya menembus batas)")
print("=" * 100)
print("KOREKSI ARITMETIKA: LTV baru = cap / (1 - drawdown). LTV 60% tercapai saat")
print("  cap 52% -> drawdown -13.3% | cap 48% -> -20.0% | cap 45% -> -25.0%")
print("  (jadi -33% BUKAN ambang cap 52%; -33% tetap dilaporkan sbg ambang ekstra)\n")
for label, thr in [("(0) >=13.3% -> memicu LTV-60 dari cap 52% (lama)", 13.3),
                   ("(1) >=20% -> memicu cut-loss sadar (= LTV-60 dari cap 48%)", 20),
                   ("(2) >=25% -> memicu wajib-jual LTV-60 dari cap 45%", 25),
                   ("(3) >=33% -> ambang ekstra (drawdown sangat dalam)", 33)]:
    a1, n1, p1 = share("mdd_to_k5_end_pct", thr)
    a2, n2, p2 = share("mdd_180d_pct", thr)
    print(f"{label}")
    print(f"    horizon akhir-jendela-K5 : {a1}/{n1} = {p1:.1f}%")
    print(f"    horizon +180 hari        : {a2}/{n2} = {p2:.1f}%")

print("\nSebaran per cycle untuk tiap ambang (horizon akhir jendela K5):")
print(f"{'Cyc':<6}{'n':>4}{'  >=20%':>9}{'  >=25%':>9}{'  >=33%':>9}{'  MDD terburuk':>16}")
print("-" * 56)
for c in cycles:
    sub = ev[ev["cycle"] == c]
    if len(sub) == 0:
        print(f"{c:<6}{0:>4}{'-':>9}{'-':>9}{'-':>9}{'-':>16}")
        continue
    print(f"{c:<6}{len(sub):>4}{(sub['mdd_to_k5_end_pct']<=-20).sum():>9}"
          f"{(sub['mdd_to_k5_end_pct']<=-25).sum():>9}{(sub['mdd_to_k5_end_pct']<=-33).sum():>9}"
          f"{sub['mdd_to_k5_end_pct'].min():>15.1f}%")

print("\nSebaran per cycle (horizon +180 hari, boleh keluar jendela K5):")
print(f"{'Cyc':<6}{'n':>4}{'  >=20%':>9}{'  >=25%':>9}{'  >=33%':>9}{'  MDD terburuk':>16}")
print("-" * 56)
for c in cycles:
    sub = ev[ev["cycle"] == c]
    if len(sub) == 0:
        continue
    print(f"{c:<6}{len(sub):>4}{(sub['mdd_180d_pct']<=-20).sum():>9}"
          f"{(sub['mdd_180d_pct']<=-25).sum():>9}{(sub['mdd_180d_pct']<=-33).sum():>9}"
          f"{sub['mdd_180d_pct'].min():>15.1f}%")

# --- KLASIFIKASI ZONA: tiga episode video -----------------------------------
def zone_label(row):
    """Zone Structure v2 (Decision Framework v2 section 1)."""
    p, sth, rp, lth = row["btc_price"], row["sth_cost_basis"], row["realized_price"], row["lth_cost_basis"]
    am, au = row["price_at_aviv_mean"], row["aviv_upper"]
    d1 = abs(sth - rp) / rp
    d2 = abs(rp - lth) / rp
    if d1 < 0.02 and d2 < 0.02:
        struct = "C"
    elif sth > rp:
        struct = "N"
    else:
        struct = "T"
    if struct == "N":
        if p >= au:  return "Z5", struct
        if p < rp:   return "ZC", struct
        if p < sth:  return "ZD", struct
        if p < am:   return "Z3", struct
        return "Z4", struct
    if struct == "T":
        if p >= au:  return "Z5", struct
        if p < sth:  return "Z1", struct
        if p < rp:   return "Z1b", struct
        return "Z2-transisi", struct
    # struct == C
    if p >= au:  return "Z5", struct
    if p < am:   return "Z2", struct
    return "Z4", struct

K_ACTIVE = {"ZC": "K3 pegang / K4-tanpa-Z1 / lantai waktu -- TIDAK ADA DEPLOY LOAN",
            "ZD": "K2 (kalau bull) / tunggu",
            "Z3": "K5 (naik dari bawah) / K2 (dip dari atas)",
            "Z4": "K6 / K2 / K1",
            "Z5": "K1 / K2 ke Z4",
            "Z1": "K4", "Z1b": "K4 wrap-up",
            "Z2-transisi": "K5 bersiap", "Z2": "K5 mulai"}

EPISODES = [
    ("2015 (video: -34%)", "2015-03-11", "2015-08-18"),
    ("2019 (video: -45%)", "2019-06-26", "2019-12-31"),
    ("2023 (video: -20%)", "2023-07-13", "2023-09-11"),
]

print("\n" + "=" * 100)
print("KLASIFIKASI KUNCI -- tiga episode drawdown yang disebut video, zona pada HARI AWAL drawdown")
print("=" * 100)
print(f"{'Episode':<22}{'Tgl awal':<12}{'Harga':>11}{'  Zona':>7}{'  Struct':>8}"
      f"{'  Di dlm K5?':>12}  K aktif")
print("-" * 118)
epi_rows = []
for name, d0, d1 in EPISODES:
    d0 = pd.Timestamp(d0); d1 = pd.Timestamp(d1)
    r = df[df["date"] <= d0].iloc[-1]
    z, st = zone_label(r)
    r1 = df[df["date"] <= d1].iloc[-1]
    z1, st1 = zone_label(r1)
    dd = (r1["btc_price"] / r["btc_price"] - 1) * 100
    # apakah tanggal awal ada di dalam jendela K5 cycle manapun?
    inside = "TIDAK"
    for c in cycles:
        s, e = cycles[c]["k5_start"], cycles[c]["k5_end"]
        if s is not None and e is not None and s <= d0 <= e:
            inside = f"YA ({c})"
    print(f"{name:<22}{str(d0.date()):<12}{r['btc_price']:>11,.2f}{z:>7}{st:>8}{inside:>12}  {K_ACTIVE[z]}")
    print(f"{'  -> akhir drawdown':<22}{str(d1.date()):<12}{r1['btc_price']:>11,.2f}{z1:>7}{st1:>8}"
          f"{'':>12}  drawdown aktual = {dd:.1f}%")
    epi_rows.append(dict(episode=name, start=d0.date(), zone_start=z, struct_start=st,
                         inside_k5=inside, end=d1.date(), zone_end=z1,
                         drawdown_pct=round(dd, 2)))

pd.DataFrame(epi_rows).to_csv(rf"{OUTDIR}\events_k5_video_episodes_zone.csv", index=False)

# --- Drawdown TERBESAR di dalam vs di luar jendela K5, 12 bulan pertama ------
print("\n" + "=" * 100)
print("PEMBANDING: drawdown terdalam (peak-to-trough) di DALAM jendela K5 vs")
print("            di 12 bulan pertama sejak cycle bottom (wilayah K4/ZC/Z1 + K5)")
print("=" * 100)
print(f"{'Cyc':<5}{'MDD dlm jendela K5':>22}{'MDD 12bln sejak bottom':>26}{'  Zona saat MDD 12bln':>24}")
print("-" * 80)
for c in cycles:
    s, e = cycles[c]["k5_start"], cycles[c]["k5_end"]
    w = df[(df["date"] >= s) & (df["date"] <= e)].reset_index(drop=True)
    dd_k5 = ((w["btc_price"] / w["btc_price"].cummax()) - 1).min() * 100
    b = cycles[c]["bottom"]
    w12 = df[(df["date"] >= b) & (df["date"] <= b + pd.Timedelta(days=365))].reset_index(drop=True)
    ser = (w12["btc_price"] / w12["btc_price"].cummax()) - 1
    dd12 = ser.min() * 100
    itr = ser.idxmin()
    ztr, _ = zone_label(w12.loc[itr])
    print(f"{c:<5}{dd_k5:>21.1f}%{dd12:>25.1f}%{('  '+ztr+' @ '+str(w12.loc[itr,'date'].date())):>24}")

print("\nSelesai. CSV: events_k5_early_bull_drawdown.csv, events_k5_video_episodes_zone.csv")
