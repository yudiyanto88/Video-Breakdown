"""
V1 - Degenerasi aturan unlock status bear (Decision Framework v2 Sec 0)

Aturan yang diuji:
  "Status bear berakhir (unlock): STH RP cross naik melewati RP (masuk Z2)"
  (framework sendiri menandai aturan ini '⚠ pending validasi backtest final')

Hipotesis: cross naik STH RP > RP HANYA mungkin kalau sebelumnya pernah
terbentuk struktur T (sth_cost_basis < realized_price). Kalau di suatu bear
window struktur T tidak pernah terbentuk, trigger unlock TIDAK PERNAH punya
kesempatan firing -> status bear terkunci selamanya (degenerasi aturan).

DEFINISI EVENT (1 kejadian = 1 bear window):
  - cycle peak = hari ATH (running max) yang diikuti >= 180 hari tanpa ATH baru
    DAN drawdown minimum dalam window <= -30%
  - bear window = [peak_date .. tanggal ATH baru berikutnya]  (closed)
                  [peak_date .. tanggal data terakhir]        (ongoing)
  - tidak ada merge: tiap peak yang lolos kriteria = 1 window terpisah

TRIGGER YANG DIUKUR (semua at-gate, tanpa lookahead):
  U1  unlock >=1 hari : hari t di mana sth>rp dan sth(t-1)<=rp(t-1),
                        setelah minimal 1 hari T di window yang sama
  U7  unlock >=7 hari : hari t = hari ke-7 berturut sth>rp,
                        setelah minimal 1 hari T di window yang sama
  ALT trigger alternatif: harga close > price_at_aviv_mean 3 hari berturut
                        (signal = hari ke-3), dicari SETELAH harga pernah
                        close di bawah AVIV Mean di dalam window

CATATAN LOOKAHEAD:
  - bottom window dipakai HANYA sebagai titik referensi deskriptif untuk
    mengukur biaya keterlambatan; bottom tidak dipakai sebagai input keputusan.
  - AVIV Mean memakai kolom `price_at_aviv_mean` (per data_dictionary:
    "AVIV Mean dalam USD - batas Z3/Z4. Ini yang dipakai framework").
    Kolom ini memakai mean AVIV yang berjalan (time-varying), jadi lebih aman
    dari lookahead dibanding pola full-history mean/std di
    research/analyze_k3_stage_comparison.py (perbedaan dicatat di findings).

Output ASCII saja (Windows console cp1252).
"""

import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUT_DIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\posts\2026-09-10_exchange-whale-ratio-binance-distribution-not-finished"

MIN_GAP_DAYS = 180     # jarak minimum ke ATH berikutnya supaya disebut cycle peak
MIN_DRAWDOWN = -0.30   # drawdown minimum di dalam window
ALT_CONFIRM   = 3      # hari berturut close > AVIV Mean untuk trigger alternatif
CROSS_VARIANTS = [1, 7]  # dua varian saja (anti-overfit)

# --- Load -------------------------------------------------------------------
df = pd.read_csv(MASTER, parse_dates=["date"])
cols = ["date", "btc_price", "sth_cost_basis", "realized_price",
        "lth_cost_basis", "price_at_aviv_mean", "price_at_aviv_plus_1_sigma"]
d = df[cols].dropna(subset=["btc_price", "sth_cost_basis", "realized_price"]).copy()
d = d[d["btc_price"] > 0].sort_values("date").reset_index(drop=True)

# AVIV Upper framework = mean + 0.5 * (plus_1_sigma - mean)   (data_dictionary)
d["aviv_upper"] = d["price_at_aviv_mean"] + 0.5 * (
    d["price_at_aviv_plus_1_sigma"] - d["price_at_aviv_mean"])

d["struct_T"] = d["sth_cost_basis"] < d["realized_price"]

print("=" * 100)
print("V1 - DEGENERASI ATURAN UNLOCK STATUS BEAR (STH RP cross naik lewat RP)")
print("=" * 100)
print(f"Data: {d.date.min().date()} s/d {d.date.max().date()}  (n hari = {len(d)})")
print(f"Kolom AVIV: price_at_aviv_mean (non-NA {d.price_at_aviv_mean.notna().sum()} hari, "
      f"mulai {d.date[d.price_at_aviv_mean.notna()].min().date()})")

# --- Enumerasi bear window --------------------------------------------------
d["rmax"] = d["btc_price"].cummax()
d["is_ath"] = d["btc_price"] >= d["rmax"] * 0.999999
ath_idx = d.index[d["is_ath"]].tolist()

windows = []
for k in range(len(ath_idx) - 1):
    i, j = ath_idx[k], ath_idx[k + 1]
    gap = (d.date[j] - d.date[i]).days
    if gap < MIN_GAP_DAYS:
        continue
    seg = d.loc[i:j]
    dd = seg.btc_price.min() / d.btc_price[i] - 1
    if dd > MIN_DRAWDOWN:
        continue
    windows.append(dict(peak_i=i, end_i=j, ongoing=False))

# window ongoing (peak terakhir yang belum dilampaui)
last_ath_i = ath_idx[-1]
gap_now = (d.date.iloc[-1] - d.date[last_ath_i]).days
dd_now = d.loc[last_ath_i:].btc_price.min() / d.btc_price[last_ath_i] - 1
if gap_now >= MIN_GAP_DAYS and dd_now <= MIN_DRAWDOWN:
    windows.append(dict(peak_i=last_ath_i, end_i=len(d) - 1, ongoing=True))


def label_cycle(dt):
    y = dt.year
    if y <= 2012:
        return "2011"
    if y <= 2015:
        return "2013"
    if y <= 2019:
        return "2017"
    if y <= 2023:
        return "2021"
    return "2025"


def first_cross_up(seg, min_days):
    """Hari pertama sth>rp bertahan min_days berturut, HANYA setelah ada hari T.
    at-gate: signal dikeluarkan di hari ke-min_days."""
    T = seg["struct_T"].values
    if not T.any():
        return None, "T tidak pernah terbentuk"
    first_T = int(np.argmax(T))            # index relatif pertama T
    above = (~T)                            # sth > rp (atau sama -> ~T)
    run = 0
    for k in range(first_T, len(seg)):
        run = run + 1 if above[k] else 0
        if run >= min_days:
            return seg.index[k], "ok"
    return None, "T terbentuk tapi cross naik tidak pernah terkonfirmasi"


def alt_trigger(seg):
    """close > AVIV Mean ALT_CONFIRM hari berturut, setelah pernah close di bawah."""
    p = seg["btc_price"].values
    am = seg["price_at_aviv_mean"].values
    below = p < am
    if not np.any(below & ~np.isnan(am)):
        return None
    start = int(np.argmax(below))
    run = 0
    for k in range(start, len(seg)):
        if np.isnan(am[k]):
            run = 0
            continue
        run = run + 1 if p[k] > am[k] else 0
        if run >= ALT_CONFIRM:
            return seg.index[k]
    return None


def first_cross_up_unbounded(start_i, min_days):
    """Sama seperti first_cross_up tapi TIDAK dibatasi akhir window - dipakai untuk
    menjawab 'berapa lama status bear tergantung' kalau T tidak pernah terbentuk
    di dalam window (status bear terbawa ke periode berikutnya)."""
    seg = d.loc[start_i:]
    return first_cross_up(seg, min_days)


def alt_all_and_post(seg, bot_i):
    """Semua hari sinyal ALT di window + sinyal ALT pertama pada/setelah bottom.
    Yang kedua POST-HOC (bottom baru diketahui belakangan) - dipakai HANYA sebagai
    pembanding deskriptif biaya keterlambatan, bukan aturan yang bisa dijalankan."""
    p_ = seg["btc_price"].values
    am = seg["price_at_aviv_mean"].values
    sig = []
    below_seen = False
    run = 0
    for k in range(len(seg)):
        if np.isnan(am[k]):
            run = 0
            continue
        if p_[k] < am[k]:
            below_seen = True
            run = 0
            continue
        if below_seen:
            run += 1
            if run >= ALT_CONFIRM:
                sig.append(seg.index[k])
    post = next((x for x in sig if x >= bot_i), None)
    return sig, post


rows = []
for w in windows:
    i, j = w["peak_i"], w["end_i"]
    seg = d.loc[i:j]
    peak_dt, peak_px = d.date[i], d.btc_price[i]
    end_dt = d.date[j]
    bot_i = seg.btc_price.idxmin()
    bot_dt, bot_px = d.date[bot_i], d.btc_price[bot_i]

    nT = int(seg["struct_T"].sum())
    T_first = d.date[seg.index[seg["struct_T"].values][0]] if nT else None
    T_last = d.date[seg.index[seg["struct_T"].values][-1]] if nT else None

    row = dict(
        cycle=label_cycle(peak_dt),
        peak_date=peak_dt.date(), peak_price=round(peak_px, 2),
        end_date=end_dt.date(), ongoing=w["ongoing"],
        window_days=(end_dt - peak_dt).days,
        bottom_date=bot_dt.date(), bottom_price=round(bot_px, 2),
        drawdown_pct=round((bot_px / peak_px - 1) * 100, 1),
        T_days=nT,
        T_first=T_first.date() if T_first is not None else "-",
        T_last=T_last.date() if T_last is not None else "-",
    )

    for md in CROSS_VARIANTS:
        idx, note = first_cross_up(seg, md)
        if idx is not None:
            u_dt, u_px = d.date[idx], d.btc_price[idx]
            row[f"U{md}_date"] = u_dt.date()
            row[f"U{md}_days_from_peak"] = (u_dt - peak_dt).days
            row[f"U{md}_days_from_bottom"] = (u_dt - bot_dt).days
            row[f"U{md}_rise_from_bottom_pct"] = round((u_px / bot_px - 1) * 100, 1)
        else:
            row[f"U{md}_date"] = "NO SIGNAL"
            row[f"U{md}_days_from_peak"] = np.nan
            row[f"U{md}_days_from_bottom"] = np.nan
            row[f"U{md}_rise_from_bottom_pct"] = np.nan
        row[f"U{md}_note"] = note

    a_idx = alt_trigger(seg)
    if a_idx is not None:
        a_dt, a_px = d.date[a_idx], d.btc_price[a_idx]
        row["ALT_date"] = a_dt.date()
        row["ALT_days_from_peak"] = (a_dt - peak_dt).days
        row["ALT_days_from_bottom"] = (a_dt - bot_dt).days
        row["ALT_rise_from_bottom_pct"] = round((a_px / bot_px - 1) * 100, 1)
    else:
        row["ALT_date"] = "NO SIGNAL"
        row["ALT_days_from_peak"] = np.nan
        row["ALT_days_from_bottom"] = np.nan
        row["ALT_rise_from_bottom_pct"] = np.nan

    # -- status bear "tergantung": unlock dicari tanpa batas akhir window --
    for md in CROSS_VARIANTS:
        u_idx, _ = first_cross_up_unbounded(i, md)
        if u_idx is not None:
            row[f"U{md}_unbounded_date"] = d.date[u_idx].date()
            row[f"U{md}_hang_days"] = (d.date[u_idx] - peak_dt).days
        else:
            row[f"U{md}_unbounded_date"] = "BELUM (per {})".format(d.date.iloc[-1].date())
            row[f"U{md}_hang_days"] = (d.date.iloc[-1] - peak_dt).days

    sigs, post = alt_all_and_post(seg, bot_i)
    row["ALT_n_firing"] = len(sigs)
    row["ALT_first_before_bottom"] = (len(sigs) > 0 and sigs[0] < bot_i)
    if post is not None:
        row["ALTpost_date"] = d.date[post].date()
        row["ALTpost_days_from_bottom"] = (d.date[post] - bot_dt).days
        row["ALTpost_rise_from_bottom_pct"] = round((d.btc_price[post] / bot_px - 1) * 100, 1)
    else:
        row["ALTpost_date"] = "NO SIGNAL"
        row["ALTpost_days_from_bottom"] = np.nan
        row["ALTpost_rise_from_bottom_pct"] = np.nan

    # flag kualitas data AVIV di era awal (aviv_mean tercemar nilai ekstrem 2010)
    row["aviv_reliable"] = peak_dt >= pd.Timestamp("2013-06-01")

    rows.append(row)

ev = pd.DataFrame(rows)

# --- Print ------------------------------------------------------------------
print("\n" + "-" * 100)
print(f"BEAR WINDOW YANG LOLOS KRITERIA (gap ATH >= {MIN_GAP_DAYS}d, drawdown <= {MIN_DRAWDOWN:.0%})")
print("-" * 100)
print(f"n total = {len(ev)}  ({(~ev.ongoing).sum()} closed + {ev.ongoing.sum()} ongoing)")
print("Sebaran per cycle:", dict(ev.cycle.value_counts().sort_index()))

print("\nPERTANYAAN A - apakah struktur T (STH RP < RP) pernah terbentuk?")
print(f"{'cycle':>6} {'peak':>12} {'akhir window':>13} {'hari':>5} {'DD':>7} "
      f"{'T?':>4} {'hari T':>7} {'T pertama':>12} {'T terakhir':>12}")
for _, r in ev.iterrows():
    print(f"{r.cycle:>6} {str(r.peak_date):>12} {str(r.end_date):>13} {r.window_days:>5} "
          f"{r.drawdown_pct:>6.1f}% {('YA' if r.T_days > 0 else 'TIDAK'):>4} {r.T_days:>7} "
          f"{str(r.T_first):>12} {str(r.T_last):>12}"
          + ("   [ONGOING]" if r.ongoing else ""))

print("\nPERTANYAAN C - dua varian durasi cross (>=1 hari vs >=7 hari), keduanya apa adanya")
print(f"{'cycle':>6} {'peak':>12} | {'U1 date':>12} {'d.peak':>7} {'d.bot':>6} {'naik%':>7} "
      f"| {'U7 date':>12} {'d.peak':>7} {'d.bot':>6} {'naik%':>7}")
for _, r in ev.iterrows():
    def f(v, fmt="{:>7.0f}"):
        return fmt.format(v) if pd.notna(v) else "      -"
    print(f"{r.cycle:>6} {str(r.peak_date):>12} | {str(r.U1_date):>12} {f(r.U1_days_from_peak)} "
          f"{f(r.U1_days_from_bottom, '{:>6.0f}')} {f(r.U1_rise_from_bottom_pct)} "
          f"| {str(r.U7_date):>12} {f(r.U7_days_from_peak)} "
          f"{f(r.U7_days_from_bottom, '{:>6.0f}')} {f(r.U7_rise_from_bottom_pct)}")

print("\nPERTANYAAN B - biaya keterlambatan: trigger alternatif (close > AVIV Mean 3 hari berturut)")
print(f"{'cycle':>6} {'peak':>12} | {'ALT date':>12} {'d.peak':>7} {'d.bot':>6} {'naik dari bottom':>17} "
      f"| {'unlock U1 naik%':>16} | selisih")
for _, r in ev.iterrows():
    alt = r.ALT_rise_from_bottom_pct
    u1 = r.U1_rise_from_bottom_pct
    diff = (u1 - alt) if (pd.notna(alt) and pd.notna(u1)) else np.nan
    fa = f"{alt:>16.1f}%" if pd.notna(alt) else "               -"
    fu = f"{u1:>15.1f}%" if pd.notna(u1) else "  NO SIGNAL    "
    fd = f"{diff:+.1f}pp" if pd.notna(diff) else ("unlock tidak nyala" if pd.isna(u1) else "-")
    dp = f"{r.ALT_days_from_peak:>7.0f}" if pd.notna(r.ALT_days_from_peak) else "      -"
    db = f"{r.ALT_days_from_bottom:>6.0f}" if pd.notna(r.ALT_days_from_bottom) else "     -"
    print(f"{r.cycle:>6} {str(r.peak_date):>12} | {str(r.ALT_date):>12} {dp} {db} {fa} | {fu} | {fd}")

print("")
print("PERTANYAAN B (bagian 1) - berapa lama status bear TERGANTUNG tanpa trigger unlock")
print("   (unlock dicari maju tanpa batas akhir window; kalau T tak pernah terbentuk di window,")
print("    status bear terbawa melewati ATH baru berikutnya)")
print(f"{'cycle':>6} {'peak':>12} {'T di window':>12} {'U1 unbounded':>14} {'hari tergantung':>16} {'U7 unbounded':>14} {'hari':>6}")
for _, r in ev.iterrows():
    print(f"{r.cycle:>6} {str(r.peak_date):>12} {('YA' if r.T_days>0 else 'TIDAK'):>12} "
          f"{str(r.U1_unbounded_date):>14} {r.U1_hang_days:>16} {str(r.U7_unbounded_date):>14} {r.U7_hang_days:>6}")

print("")
print("PERTANYAAN B (bagian 2) - perilaku trigger alternatif AVIV Mean di dalam window")
print(f"{'cycle':>6} {'peak':>12} {'AVIV data ok?':>14} {'n firing':>9} {'firing 1 sblm bottom?':>22} "
      f"{'ALTpost date':>13} {'d.bot':>6} {'naik dari bottom':>17}")
for _, r in ev.iterrows():
    db = f"{r.ALTpost_days_from_bottom:>6.0f}" if pd.notna(r.ALTpost_days_from_bottom) else "     -"
    rb = f"{r.ALTpost_rise_from_bottom_pct:>16.1f}%" if pd.notna(r.ALTpost_rise_from_bottom_pct) else "               -"
    print(f"{r.cycle:>6} {str(r.peak_date):>12} {('ya' if r.aviv_reliable else 'TIDAK (artefak)'):>14} "
          f"{r.ALT_n_firing:>9} {str(r.ALT_first_before_bottom):>22} {str(r.ALTpost_date):>13} {db} {rb}")

# --- Ringkasan agregat ------------------------------------------------------
noT = ev[ev.T_days == 0]
print("\n" + "-" * 100)
print("RINGKASAN")
print("-" * 100)
print(f"Window dengan struktur T terbentuk : {(ev.T_days > 0).sum()} / {len(ev)}")
print(f"Window TANPA struktur T sama sekali: {len(noT)} / {len(ev)}"
      + (f"  -> {', '.join(str(x) for x in noT.peak_date)}" if len(noT) else ""))
for md in CROSS_VARIANTS:
    fired = ev[ev[f"U{md}_date"] != "NO SIGNAL"]
    print(f"U{md} (cross >= {md} hari) firing di {len(fired)}/{len(ev)} window; "
          f"median naik dari bottom = "
          + (f"{fired[f'U{md}_rise_from_bottom_pct'].median():.1f}%" if len(fired) else "n/a"))
altf = ev[ev.ALT_date != "NO SIGNAL"]
print(f"ALT (AVIV Mean 3d) firing di {len(altf)}/{len(ev)} window; median naik dari bottom = "
      f"{altf.ALT_rise_from_bottom_pct.median():.1f}%")

both = ev[(ev.U1_date != "NO SIGNAL") & (ev.ALT_date != "NO SIGNAL")]
if len(both):
    print(f"Window di mana keduanya nyala (n={len(both)}): median selisih U1-ALT = "
          f"{(both.U1_rise_from_bottom_pct - both.ALT_rise_from_bottom_pct).median():+.1f}pp "
          f"(positif = unlock framework lebih telat/mahal)")

# status window ongoing
og = ev[ev.ongoing]
if len(og):
    r = og.iloc[0]
    print(f"\nWINDOW ONGOING (peak {r.peak_date}): sudah {r.window_days} hari, "
          f"hari T = {r.T_days}, U1 = {r.U1_date}, ALT = {r.ALT_date}")
    last = d.iloc[-1]
    print(f"  Kondisi terakhir {last.date.date()}: price=${last.btc_price:,.0f} "
          f"STH RP=${last.sth_cost_basis:,.0f} RP=${last.realized_price:,.0f} "
          f"AVIV Mean=${last.price_at_aviv_mean:,.0f} | struktur = "
          f"{'T (terbalik)' if last.sth_cost_basis < last.realized_price else 'N (normal)'}")
    gap_pct = (last.sth_cost_basis / last.realized_price - 1) * 100
    print(f"  Jarak STH RP vs RP saat ini: {gap_pct:+.1f}% "
          f"(harus negatif dulu supaya trigger unlock punya kesempatan firing)")

sub = ev[ev.aviv_reliable]
b2 = sub[(sub.U1_date != "NO SIGNAL") & (sub.ALTpost_date != "NO SIGNAL")]
if len(b2):
    print("")
    print(f"Pembanding biaya keterlambatan (window dgn data AVIV wajar, n={len(b2)}):")
    print(f"  median naik dari bottom saat unlock U1  = {b2.U1_rise_from_bottom_pct.median():.1f}%")
    print(f"  median naik dari bottom saat ALTpost    = {b2.ALTpost_rise_from_bottom_pct.median():.1f}%")
    print(f"  median selisih (U1 - ALTpost)           = "
          f"{(b2.U1_rise_from_bottom_pct - b2.ALTpost_rise_from_bottom_pct).median():+.1f}pp "
          f"(positif = unlock framework lebih mahal)")
print("")
print(f"Catatan: window peak < 2013-06 ditandai aviv_reliable=False - kolom price_at_aviv_mean "
      f"di era 2010-2013 tercemar nilai aviv_ratio ekstrem 2010 (harga hampir tidak pernah di atas AVIV Mean).")

ev.to_csv(OUT_DIR + r"\events_unlock_bear_degenerasi.csv", index=False)
print("\nCSV -> events_unlock_bear_degenerasi.csv")
