"""
V2 (PROXY) - MA200/365 cross di metrik exchange-flow AGREGAT

PENTING - INI PROXY, BUKAN UJI KLAIM ASLINYA.
Exchange Whale Ratio (EWR) = rasio 10 inflow terbesar terhadap total inflow di
SATU exchange (Binance). Dataset kita TIDAK punya data per-exchange maupun
konsentrasi per-transaksi - yang ada cuma magnitude agregat seluruh exchange.
Hasil apapun di sini TIDAK memvonis klaim EWR pembuat post. Yang dijawab cuma:
"apakah cross MA panjang (200/365) di metrik exchange-flow agregat punya nilai
prediktif sama sekali?"

DEFINISI EVENT (1 kejadian):
  hari t di mana SMA200(x) memotong SMA365(x) DARI ATAS KE BAWAH
  + syarat at-gate PRA-REGISTRASI: SMA200(t) berada di 5% teratas dari nilai
    SMA200 pada jendela TRAILING 365 hari (t-365..t)  <- trailing, bukan centered
  merge/cooldown: event dalam 365 hari sejak event sebelumnya dibuang

  Mode kedua (fallback, DIUMUMKAN): tanpa gate level sama sekali. Dipakai karena
  gate pra-registrasi ternyata degenerate secara struktural (0 event) - lihat
  penjelasan yang dicetak script.

DUA VARIAN x SAJA (anti-overfit):
  A. x = inflow
  B. x = inflow / total_balance

GROUND TRUTH: forward return btc_price di +90 / +180 / +365 hari dari t,
dibandingkan baseline unconditional (median forward return SEMUA hari di
rentang data yang sama).

AMBANG A PRIORI (ditetapkan sebelum melihat hasil):
  sinyal dianggap punya nilai kalau median forward-180d >= baseline + 15pp.
  n < 4 -> laporkan sebagai anekdotal, jangan klaim.

TAMBAHAN: jarak hari dari t ke cycle bottom aktual terdekat
  (negatif = t sebelum bottom, positif = t sesudah bottom)

Output ASCII saja.
"""

import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
EXCH = r"D:\Claude Code\Projects\Onchain-Dashboard\data_exchange.csv"
OUT_DIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\posts\2026-09-10_exchange-whale-ratio-binance-distribution-not-finished"

FAST, SLOW = 200, 365
TOP_PCT = 0.05        # SMA200 harus di 5% teratas trailing 365 hari
COOLDOWN = 365
HORIZONS = [90, 180, 365]
THRESHOLD_PP = 15.0   # ambang a priori untuk fwd-180 di atas baseline
MIN_N = 4

# --- Load & cek ketersediaan ------------------------------------------------
df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
d = df[["date", "btc_price", "inflow", "outflow", "net_flow", "total_balance"]].copy()
d = d[d["btc_price"].notna() & (d["btc_price"] > 0)].reset_index(drop=True)

print("=" * 100)
print("V2 (PROXY) - MA200/365 CROSS DI EXCHANGE FLOW AGREGAT")
print("PROXY: dataset TIDAK punya Exchange Whale Ratio / data per-exchange.")
print("=" * 100)
for c in ["inflow", "outflow", "net_flow", "total_balance"]:
    nn = d[c].notna()
    print(f"  {c:15s}: non-NA {nn.sum():5d} hari | {d.date[nn].min().date()} s/d {d.date[nn].max().date()}")
print(f"  btc_price      : non-NA {d.btc_price.notna().sum():5d} hari | "
      f"{d.date.min().date()} s/d {d.date.max().date()}")

try:
    ex = pd.read_csv(EXCH, parse_dates=["date"])
    print(f"  [fallback file] data_exchange.csv : {ex.date.min().date()} s/d {ex.date.max().date()}")
except Exception as e:
    print(f"  [fallback file] data_exchange.csv tidak terbaca: {e}")

LAST_FLOW = d.date[d["inflow"].notna()].max()
print("")
print(f"CATATAN DATA (STANDAR VALIDASI butir 5): kolom exchange flow BERHENTI di "
      f"{LAST_FLOW.date()} - {(d.date.max() - LAST_FLOW).days} hari terakhir (s/d "
      f"{d.date.max().date()}) KOSONG. Kondisi terkini TIDAK bisa dinilai dengan metrik ini.")

# --- Cycle bottom (definisi sama dengan V1) ---------------------------------
d["rmax"] = d["btc_price"].cummax()
ath_idx = d.index[d["btc_price"] >= d["rmax"] * 0.999999].tolist()
bottoms = []
for k in range(len(ath_idx) - 1):
    i, j = ath_idx[k], ath_idx[k + 1]
    if (d.date[j] - d.date[i]).days < 180:
        continue
    seg = d.loc[i:j]
    if seg.btc_price.min() / d.btc_price[i] - 1 > -0.30:
        continue
    bottoms.append(d.date[seg.btc_price.idxmin()])
i_last = ath_idx[-1]
if ((d.date.iloc[-1] - d.date[i_last]).days >= 180
        and d.loc[i_last:].btc_price.min() / d.btc_price[i_last] - 1 <= -0.30):
    bottoms.append(d.date[d.loc[i_last:].btc_price.idxmin()])
print("")
print("Cycle bottom referensi (definisi sama dengan V1): "
      + ", ".join(str(b.date()) for b in bottoms))


def nearest_bottom(t):
    diffs = [(t - b).days for b in bottoms]
    k = int(np.argmin([abs(x) for x in diffs]))
    return bottoms[k], diffs[k]


# --- Forward return ---------------------------------------------------------
for h in HORIZONS:
    d[f"fwd{h}"] = d["btc_price"].shift(-h) / d["btc_price"] - 1

baseline, base2015 = {}, {}
for h in HORIZONS:
    baseline[h] = d[d["date"] <= LAST_FLOW][f"fwd{h}"].dropna().median() * 100
    base2015[h] = d[(d["date"] >= "2015-01-01") & (d["date"] <= LAST_FLOW)][f"fwd{h}"].dropna().median() * 100

print("")
print("BASELINE unconditional (median forward return semua hari):")
print(f"  rentang penuh {d.date.min().date()}..{LAST_FLOW.date()} : "
      + "  ".join(f"+{h}d={baseline[h]:+.1f}%" for h in HORIZONS))
print("  rentang 2015+                        : "
      + "  ".join(f"+{h}d={base2015[h]:+.1f}%" for h in HORIZONS))


def detect(series, use_gate):
    """use_gate=True  -> gate PRA-REGISTRASI: SMA200(t) di TOP_PCT teratas trailing SLOW hari
       use_gate=False -> tanpa gate level (fallback yang diumumkan)"""
    s = series.copy()
    fast = s.rolling(FAST, min_periods=FAST).mean()
    slow = s.rolling(SLOW, min_periods=SLOW).mean()
    above = fast > slow
    cross_down = above.shift(1).fillna(False) & (~above)
    cross_down = cross_down.fillna(False)
    q = fast.rolling(SLOW, min_periods=SLOW).quantile(1 - TOP_PCT)
    gate = (fast >= q).fillna(False)
    sel = (cross_down & gate) if use_gate else cross_down
    raw = d.index[sel].tolist()
    kept, last_dt = [], None
    for i in raw:
        t = d.date[i]
        if last_dt is not None and (t - last_dt).days < COOLDOWN:
            continue
        kept.append(i)
        last_dt = t
    return kept, int(cross_down.sum()), len(raw)


def cycle_label(dt):
    y = dt.year
    return "2011" if y <= 2012 else "2013" if y <= 2015 else "2017" if y <= 2019 else \
           "2021" if y <= 2023 else "2025"


variants = {
    "A_inflow": d["inflow"],
    "B_inflow_per_balance": d["inflow"] / d["total_balance"],
}

all_rows = []
for name, series in variants.items():
    for use_gate in (True, False):
        mode = ("GATE PRA-REGISTRASI (SMA200 top 5% trailing 365d)" if use_gate
                else "TANPA GATE LEVEL (fallback, diumumkan)")
        kept, n_raw, n_sel = detect(series, use_gate)
        print("")
        print("-" * 100)
        print(f"VARIAN {name}  |  {mode}")
        print("-" * 100)
        print(f"  cross-down mentah = {n_raw} | lolos seleksi = {n_sel} | "
              f"setelah cooldown {COOLDOWN}d = {len(kept)}")
        if use_gate and n_sel == 0:
            print("  0 event. Sebabnya STRUKTURAL, bukan hasil: di hari cross-down, SMA200 baru saja")
            print("  jatuh DI BAWAH SMA365 (= rata-rata 365 hari dari data yang sama), jadi hampir")
            print("  mustahil nilai SMA200 hari itu ada di 5% TERATAS trailing 365 hari.")
            print("  Gate pra-registrasi ini degenerate -> dipakai mode fallback tanpa gate.")
        if not kept:
            print("  TIDAK ADA EVENT di mode ini.")
            continue

        rows = []
        for i in kept:
            t = d.date[i]
            b, dd = nearest_bottom(t)
            r = dict(varian=name, mode=("gated" if use_gate else "nogate"),
                     event_date=t.date(), cycle=cycle_label(t),
                     btc_price=round(d.btc_price[i], 2),
                     bottom_ref=b.date(), days_vs_bottom=dd,
                     posisi=("SEBELUM bottom" if dd < 0 else
                             "SESUDAH bottom" if dd > 0 else "TEPAT di bottom"))
            for h in HORIZONS:
                v = d[f"fwd{h}"][i]
                r[f"fwd{h}_pct"] = round(v * 100, 1) if pd.notna(v) else np.nan
            rows.append(r)
        ev = pd.DataFrame(rows)
        all_rows.append(ev)

        print(f"  n = {len(ev)} | sebaran per cycle: {dict(ev.cycle.value_counts().sort_index())}")
        print("")
        print(f"  {'event':>12} {'cycle':>6} {'price':>11} {'bottom ref':>12} {'jarak':>7} "
              f"{'posisi':>16} {'fwd90':>8} {'fwd180':>8} {'fwd365':>8}")
        for _, r in ev.iterrows():
            fm = lambda v: (f"{v:>7.1f}%" if pd.notna(v) else "       -")
            print(f"  {str(r.event_date):>12} {r.cycle:>6} {r.btc_price:>11,.0f} "
                  f"{str(r.bottom_ref):>12} {r.days_vs_bottom:>+7d} {r.posisi:>16} "
                  f"{fm(r.fwd90_pct)} {fm(r.fwd180_pct)} {fm(r.fwd365_pct)}")

        print("")
        print("  HASIL vs BASELINE:")
        for h in HORIZONS:
            vals = ev[f"fwd{h}_pct"].dropna()
            if len(vals) == 0:
                print(f"    +{h}d : tidak ada data forward")
                continue
            med = vals.median()
            print(f"    +{h}d : median event = {med:+.1f}% (n={len(vals)}) | baseline penuh "
                  f"{baseline[h]:+.1f}% -> {med - baseline[h]:+.1f}pp | baseline 2015+ "
                  f"{base2015[h]:+.1f}% -> {med - base2015[h]:+.1f}pp")
        v180 = ev["fwd180_pct"].dropna()
        if len(v180):
            edge = v180.median() - baseline[180]
            print("")
            print(f"  AMBANG A PRIORI (median fwd180 >= baseline + {THRESHOLD_PP:.0f}pp): "
                  f"selisih {edge:+.1f}pp -> {'LULUS' if edge >= THRESHOLD_PP else 'TIDAK LULUS'}")
            if len(ev) < MIN_N:
                print(f"  n = {len(ev)} < {MIN_N} -> ANEKDOTAL, tidak boleh diklaim sebagai edge.")
        # posisi vs bottom
        before = (ev.days_vs_bottom < 0).sum()
        after = (ev.days_vs_bottom > 0).sum()
        print(f"  Posisi vs cycle bottom: {before} event sebelum bottom, {after} sesudah bottom | "
              f"median |jarak| = {ev.days_vs_bottom.abs().median():.0f} hari")

if all_rows:
    out = pd.concat(all_rows, ignore_index=True)
    out.to_csv(OUT_DIR + r"\events_ma200_365_cross_exchange_flow.csv", index=False)
    print("")
    print("CSV -> events_ma200_365_cross_exchange_flow.csv")
else:
    print("")
    print("Tidak ada event sama sekali - CSV tidak ditulis.")

print("")
print("PENGINGAT: hasil di atas TIDAK memvonis klaim Exchange Whale Ratio pembuat post.")
print("EWR = konsentrasi inflow per-exchange (Binance); yang diuji di sini = magnitude agregat.")
