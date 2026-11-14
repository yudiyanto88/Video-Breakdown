"""
V3 - Biaya lag window 200/365 hari

Pertanyaan: apakah metrik ber-window 200-365 hari layak jadi PRIMARY signal,
atau maksimal CONFIRMING?

SIFAT UJI: ini PENGUKURAN DESKRIPTIF LAG, bukan backtest sinyal. Titik referensi
(bottom siklus, hari pertama Z1, hari unlock Z2) sebagian bersifat post-hoc -
memang disengaja, karena yang diukur adalah SEBERAPA TERLAMBAT cross 200/365
dibanding penanda-penanda itu. Angka di sini TIDAK boleh dibaca sebagai edge.

DEFINISI EVENT (1 kejadian):
  hari t di mana SMA200(x) memotong SMA365(x) DARI ATAS KE BAWAH
  merge/cooldown: event dalam 365 hari sejak event sebelumnya dibuang
DUA VARIAN x SAJA (anti-overfit): mvrv_ratio, btc_price

YANG DIUKUR dari tiap t:
  (a) jarak hari ke cycle bottom aktual (nearest, bertanda; + = t sesudah bottom)
      dan ke bottom BERIKUTNYA setelah t
  (b) jarak hari ke hari pertama Z1 terbentuk setelah t
      Z1 = struktur T (sth_cost_basis < realized_price) DAN btc_price < sth_cost_basis
  (c) jarak hari ke hari unlock Z2 versi framework setelah t
      unlock = STH RP cross NAIK melewati RP (sth>rp hari t, sth<=rp hari t-1)
  (d) konteks biaya: jarak hari dari cycle peak terakhir ke t, dan drawdown
      yang SUDAH terjadi dari peak itu sampai t

Cycle peak/bottom memakai definisi yang sama dengan V1:
  peak = hari ATH yang diikuti >= 180 hari tanpa ATH baru DAN drawdown <= -30%

Output ASCII saja.
"""

import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUT_DIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\posts\2026-09-10_exchange-whale-ratio-binance-distribution-not-finished"

FAST, SLOW = 200, 365
COOLDOWN = 365

df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
cols = ["date", "btc_price", "mvrv_ratio", "sth_cost_basis", "realized_price", "price_at_aviv_mean"]
d = df[cols].dropna(subset=["btc_price", "sth_cost_basis", "realized_price", "mvrv_ratio"]).copy()
d = d[d["btc_price"] > 0].reset_index(drop=True)

print("=" * 100)
print("V3 - BIAYA LAG WINDOW 200/365 (pengukuran deskriptif, BUKAN backtest sinyal)")
print("=" * 100)
print(f"Data: {d.date.min().date()} s/d {d.date.max().date()} (n hari = {len(d)}) | 4 siklus penuh + 1 berjalan")

# --- Penanda siklus (definisi V1) -------------------------------------------
d["rmax"] = d["btc_price"].cummax()
ath_idx = d.index[d["btc_price"] >= d["rmax"] * 0.999999].tolist()
peaks, bottoms = [], []
for k in range(len(ath_idx) - 1):
    i, j = ath_idx[k], ath_idx[k + 1]
    if (d.date[j] - d.date[i]).days < 180:
        continue
    seg = d.loc[i:j]
    if seg.btc_price.min() / d.btc_price[i] - 1 > -0.30:
        continue
    peaks.append(d.date[i])
    bottoms.append(d.date[seg.btc_price.idxmin()])
i_last = ath_idx[-1]
if ((d.date.iloc[-1] - d.date[i_last]).days >= 180
        and d.loc[i_last:].btc_price.min() / d.btc_price[i_last] - 1 <= -0.30):
    peaks.append(d.date[i_last])
    bottoms.append(d.date[d.loc[i_last:].btc_price.idxmin()])

print("Cycle peak  :", ", ".join(str(p.date()) for p in peaks))
print("Cycle bottom:", ", ".join(str(b.date()) for b in bottoms) + "   (bottom 2026 = bottom SEMENTARA, siklus berjalan)")

# --- Penanda Z1 & unlock ----------------------------------------------------
d["struct_T"] = d["sth_cost_basis"] < d["realized_price"]
d["is_Z1"] = d["struct_T"] & (d["btc_price"] < d["sth_cost_basis"])
d["unlock"] = (~d["struct_T"]) & (d["struct_T"].shift(1).fillna(False))

z1_dates = list(d.date[d["is_Z1"]])
unlock_dates = list(d.date[d["unlock"]])
print(f"Hari Z1 total: {len(z1_dates)} | hari unlock (cross naik STH RP > RP): {len(unlock_dates)}")


def cycle_label(dt):
    y = dt.year
    return "2011" if y <= 2012 else "2013" if y <= 2015 else "2017" if y <= 2019 else \
           "2021" if y <= 2023 else "2025"


def next_after(dates_list, t):
    nxt = [x for x in dates_list if x > t]
    return nxt[0] if nxt else None


def detect(series):
    fast = series.rolling(FAST, min_periods=FAST).mean()
    slow = series.rolling(SLOW, min_periods=SLOW).mean()
    above = fast > slow
    cross_down = (above.shift(1).fillna(False) & (~above)).fillna(False)
    raw = d.index[cross_down].tolist()
    kept, last_dt = [], None
    for i in raw:
        t = d.date[i]
        if last_dt is not None and (t - last_dt).days < COOLDOWN:
            continue
        kept.append(i)
        last_dt = t
    return kept, int(cross_down.sum())


variants = {"mvrv_ratio": d["mvrv_ratio"], "btc_price": d["btc_price"]}
all_rows = []

for name, series in variants.items():
    kept, n_raw = detect(series)
    print("")
    print("-" * 100)
    print(f"VARIAN x = {name}   (SMA{FAST} cross ke bawah SMA{SLOW}, cooldown {COOLDOWN}d)")
    print("-" * 100)
    print(f"  cross-down mentah = {n_raw} | setelah cooldown = {len(kept)}")
    rows = []
    for i in kept:
        t = d.date[i]
        px = d.btc_price[i]
        # (a) bottom
        diffs = [(t - b).days for b in bottoms]
        k = int(np.argmin([abs(x) for x in diffs]))
        near_b, near_d = bottoms[k], diffs[k]
        nb = next_after(bottoms, t)
        # (b) Z1
        z1_now = bool(d.is_Z1[i])
        z1_next = next_after(z1_dates, t)
        # (c) unlock
        u_next = next_after(unlock_dates, t)
        # (d) peak terakhir sebelum t
        prev_peaks = [p for p in peaks if p <= t]
        if prev_peaks:
            pk = prev_peaks[-1]
            pk_px = d.btc_price[d.index[d.date == pk][0]]
            dd_done = (px / pk_px - 1) * 100
            days_from_peak = (t - pk).days
        else:
            pk, dd_done, days_from_peak = None, np.nan, np.nan
        rows.append(dict(
            varian=name, event_date=t.date(), cycle=cycle_label(t), btc_price=round(px, 2),
            peak_ref=(pk.date() if pk is not None else "-"),
            days_after_peak=days_from_peak,
            drawdown_sudah_terjadi_pct=round(dd_done, 1) if pd.notna(dd_done) else np.nan,
            bottom_nearest=near_b.date(), days_vs_nearest_bottom=near_d,
            bottom_next=(nb.date() if nb is not None else "-"),
            days_to_next_bottom=((nb - t).days if nb is not None else np.nan),
            Z1_aktif_di_t=z1_now,
            Z1_next=(z1_next.date() if z1_next is not None else "-"),
            days_to_next_Z1=((z1_next - t).days if z1_next is not None else np.nan),
            unlock_next=(u_next.date() if u_next is not None else "-"),
            days_to_next_unlock=((u_next - t).days if u_next is not None else np.nan),
        ))
    ev = pd.DataFrame(rows)
    all_rows.append(ev)
    print(f"  n = {len(ev)} | sebaran per cycle: {dict(ev.cycle.value_counts().sort_index())}")
    print("")
    print(f"  {'event':>12} {'cycle':>6} {'peak ref':>12} {'d.peak':>7} {'DD sudah':>9} "
          f"{'bottom near':>12} {'d.bot':>7} {'Z1 aktif':>9} {'d.Z1':>6} {'d.unlock':>9}")
    for _, r in ev.iterrows():
        g = lambda v, w=6: (f"{v:>{w}.0f}" if pd.notna(v) else " " * (w - 1) + "-")
        print(f"  {str(r.event_date):>12} {r.cycle:>6} {str(r.peak_ref):>12} "
              f"{g(r.days_after_peak,7)} {r.drawdown_sudah_terjadi_pct:>8.1f}% "
              f"{str(r.bottom_nearest):>12} {r.days_vs_nearest_bottom:>+7d} "
              f"{str(r.Z1_aktif_di_t):>9} {g(r.days_to_next_Z1)} {g(r.days_to_next_unlock,9)}")

    print("")
    print("  RINGKASAN LAG (median, hari):")
    print(f"    dari cycle peak ke cross            : {ev.days_after_peak.median():.0f} hari "
          f"(drawdown yang SUDAH terjadi: median {ev.drawdown_sudah_terjadi_pct.median():.1f}%)")
    print(f"    cross vs bottom terdekat (bertanda) : {ev.days_vs_nearest_bottom.median():+.0f} hari "
          f"({(ev.days_vs_nearest_bottom < 0).sum()} sebelum / {(ev.days_vs_nearest_bottom > 0).sum()} sesudah)")
    v = ev.days_to_next_bottom.dropna()
    print(f"    cross -> bottom BERIKUTNYA          : median {v.median():.0f} hari (n={len(v)})")
    v = ev.days_to_next_Z1.dropna()
    print(f"    cross -> hari pertama Z1 berikutnya : median {v.median():.0f} hari (n={len(v)}), "
          f"Z1 sudah aktif di hari cross: {int(ev.Z1_aktif_di_t.sum())}/{len(ev)}")
    v = ev.days_to_next_unlock.dropna()
    print(f"    cross -> unlock Z2 berikutnya       : median {v.median():.0f} hari (n={len(v)})")
    print("")
    print("  Sebaran per cycle (hari dari peak ke cross):")
    for c, grp in ev.groupby("cycle"):
        print(f"    {c}: n={len(grp)} | " + ", ".join(
            f"{r.event_date} (+{r.days_after_peak:.0f}d, DD {r.drawdown_sudah_terjadi_pct:+.0f}%)"
            for _, r in grp.iterrows()))

out = pd.concat(all_rows, ignore_index=True)
out.to_csv(OUT_DIR + r"\events_biaya_lag_window_200_365.csv", index=False)
print("")
print("CSV -> events_biaya_lag_window_200_365.csv")
print("")
print("CATATAN: bottom/Z1/unlock adalah penanda POST-HOC. Tujuan uji ini mengukur LAG,")
print("bukan membangun sinyal - jangan dibaca sebagai bukti edge.")
