# -*- coding: utf-8 -*-
"""
V2 — Proxy percentile MVRV CAUSAL + uji kata "only near cycle lows"

KLAIM YANG DIUJI (video BM Pro 2026-08-05, insight #5/#1/#6/#8):
  - "MVRV Quantile Bands" = MVRV Ratio -> fit amplitude decay model -> percentile rank
    0-100 terhadap SELURUH SEJARAH. Reading saat video dibuat: percentile 8%.
  - Klaim: 8% ~ "bottoming out in every single bear cycle", tercapai SEBELUM harga
    menyentuh Realized Price.
  - FAQ BM Pro: "<25th percentile = bear market accumulation ranges"; "<10th percentile
    have appeared ONLY near major cycle lows".

TITIK LEMAH YANG DIUJI: kata "percentile of ALL history". Kalau rank dihitung full-sample,
setiap pembacaan historis memuat informasi masa depan -> LOOKAHEAD BIAS STRUKTURAL
(STANDAR VALIDASI poin 3). Uji: bangun versi CAUSAL (expanding window) dan ukur selisihnya.

--- DEFINISI EVENT (poin 1) ---
Proxy percentile (2 varian CAUSAL saja — lihat ATURAN BERHENTI di bawah):
  P1 "raw"        : percentile rank mvrv_ratio[t] di antara mvrv_ratio[0..t]  (expanding)
  P2 "detrended"  : OLS expanding log(mvrv_ratio) ~ t memakai data [0..t] SAJA;
                    residual dihitung utk [0..t] dgn fit itu; percentile rank residual[t]
                    di antara residual[0..t]. Ini proxy paling dekat dgn "amplitude decay
                    model" BM Pro yang parameternya TIDAK diungkap.
  Pembanding (BUKAN varian baru, hanya cermin dari 2 di atas): versi FULL-SAMPLE dari
  P1 & P2 -> untuk MENGUKUR besar lookahead bias, bukan untuk dipakai sbg sinyal.
  BURN-IN: 365 hari pertama (mulai 2010-07-17) dibuang -> proxy causal valid sejak 2011-07-17.

Episode reading di bawah threshold: hari-hari berurutan dgn reading < thr digabung jadi
  SATU episode kalau jeda antar hari < 30 hari (aturan merge/cooldown eksplisit).

Cycle low (ground truth ex-post, boleh ex-post karena ini GROUND TRUTH bukan gate):
  konvensi bottom-to-bottom established (backtest_k5nz/run_backtest.py):
    2015-01-14, 2018-12-15, 2022-11-21 + low 2011-11-18 (pra-konvensi, suplemen)
    Cycle berjalan: low sementara 2026-06-30 -> BELUM TERKONFIRMASI sbg cycle low,
    dilaporkan terpisah (dgn & tanpa).
Window "dekat cycle low" = +/-180 hari (a priori, tidak di-grid-search).

--- ATURAN BERHENTI EKSPLISIT ---
Kalau proxy causal tidak konvergen ke ballpark 8% per Agt-2026 -> laporkan INCONCLUSIVE
untuk reproduksi angka BM Pro dan BERHENTI. TIDAK menambah varian ke-3/ke-4 untuk mengejar
angka 8% (itu overfitting, poin 6). Bagian (b)-(e) tetap dijalankan tapi diberi label
"memakai proxy KAMI, bukan indikator BM Pro".

--- CATATAN DATA ---
mvrv_ratio, btc_price, realized_price penuh sejak 2010-07-17. Baris terakhir 2026-07-15,
video 2026-08-05 -> selisih ~3 minggu; semua pembacaan "saat ini" = per 2026-07-15.
"""

import pandas as pd
import numpy as np

DATA = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUT = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-05_the-free-simple-strategy-that-beats-bitcoin-it-just-flashed-again"

BURN_IN = 365
NEAR_WINDOW = 180
MERGE_GAP = 30

df = pd.read_csv(DATA, parse_dates=["date"])
df = df.dropna(subset=["btc_price", "mvrv_ratio", "realized_price"]).copy()
df = df[(df["btc_price"] > 0) & (df["mvrv_ratio"] > 0)].sort_values("date").reset_index(drop=True)
LAST = df["date"].max()
n = len(df)
print(f"Data: {df['date'].min().date()} s/d {LAST.date()}  (n={n} hari)")
print("CATATAN: data berhenti 2026-07-15; video 2026-08-05 -> selisih ~3 minggu.")
print(f"Burn-in proxy causal: {BURN_IN} hari -> valid sejak {df['date'].iloc[BURN_IN].date()}\n")

mv = df["mvrv_ratio"].values
logmv = np.log(mv)
t = np.arange(n, dtype=float)

# =====================================================================
# P1 causal: expanding percentile rank mentah
# =====================================================================
p1_causal = np.full(n, np.nan)
for i in range(BURN_IN, n):
    hist = mv[:i + 1]
    p1_causal[i] = (hist <= mv[i]).sum() / (i + 1) * 100.0

# P1 full-sample (pembanding lookahead)
order = np.argsort(mv)
p1_full = np.empty(n)
srt = np.sort(mv)
p1_full = np.searchsorted(srt, mv, side="right") / n * 100.0

# =====================================================================
# P2 causal: expanding OLS log(mvrv) ~ t, percentile rank residual
# =====================================================================
p2_causal = np.full(n, np.nan)
slope_hist = np.full(n, np.nan)
cs_t = np.cumsum(t)
cs_tt = np.cumsum(t * t)
cs_y = np.cumsum(logmv)
cs_ty = np.cumsum(t * logmv)
for i in range(BURN_IN, n):
    m = i + 1
    st, stt, sy, sty = cs_t[i], cs_tt[i], cs_y[i], cs_ty[i]
    den = m * stt - st * st
    if den <= 0:
        continue
    b = (m * sty - st * sy) / den
    a = (sy - b * st) / m
    res = logmv[:m] - (a + b * t[:m])
    slope_hist[i] = b
    p2_causal[i] = (res <= res[i]).sum() / m * 100.0

# P2 full-sample
b_full, a_full = np.polyfit(t, logmv, 1)
res_full = logmv - (a_full + b_full * t)
srt_r = np.sort(res_full)
p2_full = np.searchsorted(srt_r, res_full, side="right") / n * 100.0

df["p1_causal"] = p1_causal
df["p1_full"] = p1_full
df["p2_causal"] = p2_causal
df["p2_full"] = p2_full
df["p_rp"] = df["btc_price"] / df["realized_price"]

print("Trend log(MVRV) ~ t (full-sample): slope/hari = %.3e -> %.2f%% per tahun"
      % (b_full, (np.exp(b_full * 365) - 1) * 100))
print("Trend causal terakhir (fit s/d 2026-07-15): slope/hari = %.3e -> %.2f%% per tahun\n"
      % (slope_hist[-1], (np.exp(slope_hist[-1] * 365) - 1) * 100))

# =====================================================================
# (a) Selisih causal vs full-sample di 4 tanggal kunci
# =====================================================================
KEY = ["2015-01-14", "2018-12-15", "2022-11-21", "2026-07-15"]
print("=" * 112)
print("(a) SELISIH PEMBACAAN: CAUSAL (expanding) vs FULL-SAMPLE (lookahead) di 4 tanggal kunci")
print("=" * 112)
print(f"{'tanggal':<12}{'MVRV':>8}{'P1 causal':>11}{'P1 full':>9}{'d(P1)':>8}"
      f"{'P2 causal':>11}{'P2 full':>9}{'d(P2)':>8}{'P/RP':>8}")
print("-" * 112)
for k in KEY:
    r = df[df["date"] == k]
    if r.empty:
        r = df[df["date"] <= k].iloc[[-1]]
    r = r.iloc[0]
    print(f"{str(r['date'].date()):<12}{r['mvrv_ratio']:>8.3f}"
          f"{r['p1_causal']:>11.1f}{r['p1_full']:>9.1f}{r['p1_causal']-r['p1_full']:>+8.1f}"
          f"{r['p2_causal']:>11.1f}{r['p2_full']:>9.1f}{r['p2_causal']-r['p2_full']:>+8.1f}"
          f"{r['p_rp']:>8.3f}")

d_all = df.dropna(subset=["p1_causal"])
print(f"\n  Selisih |causal - full| di SELURUH sampel (n={len(d_all)} hari, sejak burn-in):")
for c in ["p1", "p2"]:
    dd = (d_all[f"{c}_causal"] - d_all[f"{c}_full"])
    print(f"    {c}: mean={dd.mean():+.1f}pp  median={dd.median():+.1f}pp  "
          f"min={dd.min():+.1f}pp  max={dd.max():+.1f}pp  mean|d|={dd.abs().mean():.1f}pp")

last = df.iloc[-1]
print(f"\n  >>> PEMBACAAN TERAKHIR ({LAST.date()}): MVRV={last['mvrv_ratio']:.3f} | "
      f"P1 causal={last['p1_causal']:.1f} | P2 causal={last['p2_causal']:.1f} | "
      f"P1 full={last['p1_full']:.1f} | P2 full={last['p2_full']:.1f}")
print(f"      Klaim BM Pro per 2026-08-05: percentile 8.")
conv = [abs(last['p1_causal'] - 8) <= 5, abs(last['p2_causal'] - 8) <= 5]
print(f"      Konvergen ke ballpark 8 (+/-5pp)? P1: {'YA' if conv[0] else 'TIDAK'} | "
      f"P2: {'YA' if conv[1] else 'TIDAK'}")
if not any(conv):
    print("      -> ATURAN BERHENTI AKTIF: reproduksi angka 8 = INCONCLUSIVE.")
    print("         TIDAK menambah varian ke-3/ke-4 (overfitting). Lanjut (b)-(e) dgn label")
    print("         'proxy KAMI, bukan indikator BM Pro'.")

# =====================================================================
# WINDOW BEAR (peak cycle -> cycle bottom) — definisi identik dgn V1
# =====================================================================
CYCLES = [
    ("S0 pra-2013 (SUPLEMEN)", "2010-07-17", "2011-11-18"),
    ("S1 2013-2015", "2013-01-01", "2015-01-14"),
    ("S2 2015-2018", "2015-01-15", "2018-12-15"),
    ("S3 2018-2022", "2018-12-16", "2022-11-21"),
    ("S4 2022-now (BELUM SELESAI)", "2022-11-22", str(LAST.date())),
]
BEARS = []
for cn, lo, hi in CYCLES:
    w = df[(df["date"] >= lo) & (df["date"] <= hi)]
    pk = w.loc[w["btc_price"].idxmax()]
    bw = df[(df["date"] >= pk["date"]) & (df["date"] <= pd.Timestamp(hi))]
    lw = bw.loc[bw["btc_price"].idxmin()]
    BEARS.append(dict(cycle=cn, peak_date=pk["date"], peak_price=pk["btc_price"],
                      low_date=lw["date"], low_price=lw["btc_price"],
                      p_rp_low=lw["p_rp"], win=bw, cyc=w,
                      ongoing=("BELUM SELESAI" in cn)))

print("\n" + "=" * 118)
print("(b) BEAR LOW: Price/RP di titik low + JUMLAH HARI harga di bawah RP")
print("    Bear window = peak cycle -> cycle bottom (sama dgn V1). Bear berjalan: low SEMENTARA")
print("    per 2026-07-15, masih bisa turun lagi.")
print("=" * 118)
print(f"{'bear (cycle)':<30}{'peak':>12}{'low date':>12}{'low price':>12}{'P/RP@low':>10}"
      f"{'hariP<RP(bear)':>15}{'hari bear':>10}{'hariP<RP(cycle)':>16}")
print("-" * 118)
brows = []
for b in BEARS:
    dbb = int((b["win"]["btc_price"] < b["win"]["realized_price"]).sum())
    dbc = int((b["cyc"]["btc_price"] < b["cyc"]["realized_price"]).sum())
    tag = "  <-- SEMENTARA" if b["ongoing"] else ""
    print(f"{b['cycle']:<30}{str(b['peak_date'].date()):>12}{str(b['low_date'].date()):>12}"
          f"{b['low_price']:>12,.2f}{b['p_rp_low']:>10.3f}{dbb:>15}{len(b['win']):>10}{dbc:>16}{tag}")
    brows.append(dict(cycle=b["cycle"], peak_date=str(b["peak_date"].date()),
                      low_date=str(b["low_date"].date()), low_price=round(b["low_price"], 2),
                      p_rp_at_low=round(b["p_rp_low"], 4), days_p_below_rp_bear=dbb,
                      bear_days=len(b["win"]), days_p_below_rp_cycle=dbc,
                      ongoing=b["ongoing"]))

done = [r for r in brows if not r["ongoing"] and "SUPLEMEN" not in r["cycle"]]
seq_prp = [float(r["p_rp_at_low"]) for r in done]
seq_days = [r["days_p_below_rp_bear"] for r in done]
print(f"\n  P/RP di bear low, 3 bear SELESAI (B1,B2,B3): {seq_prp} -> "
      f"{'NAIK monoton' if all(seq_prp[i]<seq_prp[i+1] for i in range(len(seq_prp)-1)) else 'TIDAK monoton'}")
print(f"  Hari P<RP DI DALAM bear, 3 bear SELESAI: {seq_days} -> "
      f"{'MENURUN monoton' if all(seq_days[i]>seq_days[i+1] for i in range(len(seq_days)-1)) else 'TIDAK menurun monoton'}")
ong = [r for r in brows if r["ongoing"]][0]
print(f"  Bear BERJALAN (2025-26): P/RP di low sementara = {ong['p_rp_at_low']:.3f}; "
      f"hari P<RP di dalam bear ini = {ong['days_p_below_rp_bear']} "
      f"(harga BELUM pernah menyentuh RP sejak peak {ong['peak_date']}).")
print(f"  Catatan: kolom hariP<RP(cycle) untuk S4 = {ong['days_p_below_rp_cycle']} hari, tapi itu EKOR")
print("  bear 2022 (Des-2022/Jan-2023) yang jatuh di dalam window cycle S4 - bukan bear berjalan.")

# =====================================================================
# (c) + (d) Pertama kali reading < 10 DI DALAM tiap bear
# =====================================================================
print("\n" + "=" * 118)
print("(c)+(d) PERTAMA KALI READING < 10 DI DALAM TIAP BEAR")
print("        (proxy causal KAMI, BUKAN indikator BM Pro - lihat aturan berhenti di atas)")
print("        + max drawdown lanjutan sampai bear low & hari ke bear low")
print("=" * 118)
fc_rows = []
for pname in ["p1_causal", "p2_causal"]:
    print(f"\n  --- {pname} ---")
    print(f"  {'bear (cycle)':<30}{'first<10':>12}{'MVRV':>8}{'P/RP':>8}{'P>RP?':>7}"
          f"{'price':>12}{'low date':>12}{'maxDD lanjut':>14}{'hari->low':>10}")
    for b in BEARS:
        w = b["win"].dropna(subset=[pname])
        if w.empty:
            print(f"  {b['cycle']:<30}{'(burn-in)':>12}")
            continue
        hit = w[w[pname] < 10]
        if hit.empty:
            print(f"  {b['cycle']:<30}{'TIDAK PERNAH':>12}"
                  f"   (min reading dalam bear = {w[pname].min():.1f})")
            fc_rows.append(dict(proxy=pname, cycle=b["cycle"], first_below10=None,
                                min_reading_in_bear=round(float(w[pname].min()), 2)))
            continue
        f = hit.iloc[0]
        fwd = df[(df["date"] >= f["date"]) & (df["date"] <= b["low_date"])]
        mdd = fwd["btc_price"].min() / f["btc_price"] - 1
        dts = (b["low_date"] - f["date"]).days
        print(f"  {b['cycle']:<30}{str(f['date'].date()):>12}{f['mvrv_ratio']:>8.3f}{f['p_rp']:>8.3f}"
              f"{('YA' if f['p_rp'] > 1 else 'tidak'):>7}{f['btc_price']:>12,.0f}"
              f"{str(b['low_date'].date()):>12}{mdd:>13.1%}{dts:>10}")
        fc_rows.append(dict(proxy=pname, cycle=b["cycle"], first_below10=str(f["date"].date()),
                            mvrv=round(f["mvrv_ratio"], 4), p_rp=round(f["p_rp"], 4),
                            price_above_rp=bool(f["p_rp"] > 1), price=round(f["btc_price"], 2),
                            bear_low_date=str(b["low_date"].date()),
                            further_maxdd_pct=round(mdd * 100, 1), days_to_low=dts,
                            min_reading_in_bear=round(float(w[pname].min()), 2)))

print("\n  Uji klaim 'reading rendah tercapai SEBELUM harga menyentuh RP':")
for pname in ["p1_causal", "p2_causal"]:
    d10 = df.dropna(subset=[pname])
    d10 = d10[d10[pname] < 10]
    above = d10[d10["p_rp"] > 1]
    pre26 = above[above["date"] < "2026-01-01"]
    print(f"    {pname}: hari reading<10 = {len(d10)}; di antaranya P>RP = {len(above)} "
          f"({len(above) / max(len(d10), 1) * 100:.1f}%); sebelum 2026 = {len(pre26)} hari"
          + (f" (rentang {pre26['date'].iloc[0].date()} .. {pre26['date'].iloc[-1].date()})"
             if len(pre26) else ""))

# =====================================================================
# (e) Uji kata "ONLY near cycle lows"
# =====================================================================
def episodes(sub_dates, gap=MERGE_GAP):
    eps, cur, prev = [], [], None
    for d in sub_dates:
        if prev is not None and (d - prev).days >= gap:
            eps.append(cur)
            cur = []
        cur.append(d)
        prev = d
    if cur:
        eps.append(cur)
    return eps

LOWS_CONF = [pd.Timestamp(x) for x in ["2011-11-18", "2015-01-14", "2018-12-15", "2022-11-21"]]
LOW_TMP = [b for b in BEARS if b["ongoing"]][0]["low_date"]

print("\n" + "=" * 118)
print('(e) UJI KATA "ONLY": episode reading < p10 dan < p25, jarak ke cycle low terdekat')
print(f"    merge episode kalau jeda >= {MERGE_GAP} hari | 'dekat' = +/-{NEAR_WINDOW} hari dari cycle low")
print(f"    cycle low TERKONFIRMASI (n=4): {[str(d.date()) for d in LOWS_CONF]}")
print(f"    low SEMENTARA bear berjalan (BELUM terkonfirmasi): {LOW_TMP.date()}")
print("=" * 118)
ep_rows = []
for pname in ["p1_causal", "p2_causal"]:
    for thr in [10, 25]:
        sub = df.dropna(subset=[pname])
        sub = sub[sub[pname] < thr]
        dts_l = list(sub["date"])
        eps = episodes(dts_l)

        def mind(d, lows):
            return min(abs((d - L).days) for L in lows)

        arr_conf = np.array([mind(d, LOWS_CONF) for d in dts_l])
        arr_tmp = np.array([mind(d, LOWS_CONF + [LOW_TMP]) for d in dts_l])
        pct_conf = (arr_conf <= NEAR_WINDOW).mean() * 100 if len(arr_conf) else float("nan")
        pct_tmp = (arr_tmp <= NEAR_WINDOW).mean() * 100 if len(arr_tmp) else float("nan")
        print(f"\n  --- {pname} < p{thr} ---  total hari={len(dts_l)} "
              f"({len(dts_l) / len(d_all) * 100:.1f}% dari hari pasca burn-in), jumlah episode={len(eps)}")
        print(f"      % hari dlm +/-{NEAR_WINDOW}h dari cycle low TERKONFIRMASI      : {pct_conf:.1f}%")
        print(f"      % hari kalau low SEMENTARA {LOW_TMP.date()} ikut dihitung : {pct_tmp:.1f}%")
        print(f"      {'ep':<4}{'mulai':>12}{'selesai':>12}{'hari':>6}{'min read':>10}"
              f"{'low konf terdekat':>19}{'jarak':>7}{'dekat(konf)':>12}{'dekat(+tmp)':>12}")
        fp_conf = fp_tmp = 0
        for k, e in enumerate(eps, 1):
            st, en = e[0], e[-1]
            dc = min(mind(d, LOWS_CONF) for d in e)
            dt_ = min(mind(d, LOWS_CONF + [LOW_TMP]) for d in e)
            Lbest = min(LOWS_CONF, key=lambda L: min(abs((d - L).days) for d in e))
            minread = sub[(sub["date"] >= st) & (sub["date"] <= en)][pname].min()
            nc, nt = dc <= NEAR_WINDOW, dt_ <= NEAR_WINDOW
            fp_conf += (not nc)
            fp_tmp += (not nt)
            print(f"      {k:<4}{str(st.date()):>12}{str(en.date()):>12}{len(e):>6}{minread:>10.1f}"
                  f"{str(Lbest.date()):>19}{dc:>7}{('YA' if nc else 'TIDAK'):>12}"
                  f"{('YA' if nt else 'TIDAK'):>12}")
            ep_rows.append(dict(proxy=pname, threshold=thr, episode=k, start=str(st.date()),
                                end=str(en.date()), days=len(e),
                                min_reading=round(float(minread), 2),
                                nearest_confirmed_low=str(Lbest.date()),
                                dist_days_confirmed=int(dc), dist_days_incl_temp_low=int(dt_),
                                near180_confirmed=bool(nc), near180_incl_temp=bool(nt)))
        print(f"      -> episode BUKAN dekat cycle low terkonfirmasi (false positive thd kata 'only'): "
              f"{fp_conf} dari {len(eps)}  |  kalau low sementara ikut dihitung: {fp_tmp} dari {len(eps)}")

pd.DataFrame(ep_rows).to_csv(OUT + "\\events_mvrv_percentile_episodes.csv", index=False)
pd.DataFrame(brows).to_csv(OUT + "\\events_mvrv_percentile_bearlows.csv", index=False)
pd.DataFrame(fc_rows).to_csv(OUT + "\\events_mvrv_percentile_first_below10.csv", index=False)
print("\nCSV disimpan: events_mvrv_percentile_episodes.csv, "
      "events_mvrv_percentile_bearlows.csv, events_mvrv_percentile_first_below10.csv")

print("\n" + "=" * 118)
print("RINGKASAN n (STANDAR VALIDASI poin 2 & 4)")
print("=" * 118)
print(f"  n hari total pasca burn-in = {len(d_all)} (2011-07-17 s/d 2026-07-15)")
print("  n bear SELESAI = 3 (2014-15, 2018, 2022) + 1 suplemen 2011 + 1 BERJALAN (2025-26)")
print("  n cycle low TERKONFIRMASI = 4 (2011-11-18 suplemen, 2015-01-14, 2018-12-15, 2022-11-21)")
print("  Independensi: hari dalam satu episode SANGAT berkorelasi (autokorelasi MVRV harian ~1)")
print("  -> unit analisis yang jujur = EPISODE (n=9-10), bukan hari (n=372-1160).")
