"""
VALIDASI 3 - sth_rp_resistance_bear
Klaim On-Chain Mind [01:17]-[01:44]:
  Di bear market, STH RP sering jadi RESISTANCE bukan support -- pembeli baru
  underwater, jadi saat harga rally balik ke level yang mereka bayar banyak yang
  keluar di break-even. Rally ke level ini harus diperlakukan hati-hati.

Kenapa penting: mengkalibrasi Signal D framework (harga > STH RP >=3 hari =
syarat wrap-up K4 -> Z1b).
Konteks: Price_Level_KB v1.4 sec.6.3 -- STH RP = level paling sering kasih
false signal (60 episode breach terpisah dalam 10 tahun).

DEFINISI (dikunci sebelum menghitung):
  - Bear window per cycle: cycle peak -> tanggal unlock struktural
    (sth_cost_basis cross NAIK realized_price setelah >=30 hari inversi).
    Cycle 2025-26 = BERJALAN (censored, unlock belum terjadi).
  - Event "sentuhan dari bawah": hari pertama btc_price >= 98% * sth_cost_basis
    setelah >=30 hari berturut-turut btc_price < 98% * sth_cost_basis.
    Cooldown 30 hari antar event.
  - Outcome (window 30 hari sesudah event): "BREAK" kalau ada >=3 hari berturut
    btc_price close > sth_cost_basis (persis Signal D). Selain itu "DITOLAK".
  - Sub-uji: dari event BREAK, berapa yang diikuti unlock struktural dalam 90 hari.
  - Tambahan: dari event BREAK, berapa yang harganya balik ke bawah STH RP dalam
    90 hari (break palsu) -- relevan langsung ke kalibrasi Signal D.

Output print ASCII saja.
"""

import numpy as np
import os
import pandas as pd

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = (r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos"
          r"\2026-08-04_bitcoins-top-buyers-are-finally-capitulating")

TOUCH_FRAC   = 0.98
PRE_DAYS     = 30
COOLDOWN     = 30
OUT_WINDOW   = 30
BREAK_PERSIST = 3
UNLOCK_PRE   = 30
SUB_WINDOW   = 90

CYCLE_WINDOWS = [("2011", "2010-07-17", "2011-12-31"),
                 ("2013", "2012-01-01", "2014-06-30"),
                 ("2017", "2015-01-01", "2018-06-30"),
                 ("2021", "2019-01-01", "2022-06-30"),
                 ("2025", "2023-01-01", "2026-12-31")]

df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "sth_cost_basis", "realized_price"]).copy()
df = df[df["btc_price"] > 0].reset_index(drop=True)

price = df["btc_price"].values
sth   = df["sth_cost_basis"].values
rp    = df["realized_price"].values
dates = df["date"].values

print("=" * 104)
print("VALIDASI 3 - STH RP SEBAGAI RESISTANCE DI BEAR MARKET")
print("=" * 104)
print("Rentang data : %s s/d %s (n=%d hari)"
      % (df["date"].min().date(), df["date"].max().date(), len(df)))

# ---------------------------------------------------------------- unlock
inv = (sth < rp)
st = np.zeros(len(df), dtype=int)
c = 0
for k, v in enumerate(inv):
    c = c + 1 if v else 0
    st[k] = c
unlocks = [k for k in range(1, len(df)) if (not inv[k]) and st[k - 1] >= UNLOCK_PRE]
unlock_dates = [pd.Timestamp(dates[k]) for k in unlocks]
print("Unlock struktural (n=%d): %s" % (len(unlock_dates), [str(u.date()) for u in unlock_dates]))

# ---------------------------------------------------------------- bear windows
bears = []
for cyc, a, b in CYCLE_WINDOWS:
    sub = df[(df["date"] >= a) & (df["date"] <= b)]
    if len(sub) == 0:
        continue
    pi = sub["btc_price"].idxmax()
    pdte = pd.Timestamp(dates[pi])
    ud = next((u for u in unlock_dates if u > pdte), None)
    end = ud if ud is not None else df["date"].max()
    bears.append(dict(cycle=cyc, peak_idx=pi, peak_date=pdte, peak_price=price[pi],
                      end_date=end, censored=(ud is None)))
print("\n--- BEAR WINDOW (peak -> unlock) ---")
for b in bears:
    print("    %s : %s -> %s  (%d hari)%s"
          % (b["cycle"], b["peak_date"].date(), b["end_date"].date(),
             (b["end_date"] - b["peak_date"]).days,
             "  [BERJALAN / CENSORED]" if b["censored"] else ""))

# ---------------------------------------------------------------- events
thr = TOUCH_FRAC * sth
under = price < thr
st_u = np.zeros(len(df), dtype=int)
c = 0
for k, v in enumerate(under):
    c = c + 1 if v else 0
    st_u[k] = c

rows = []
for b in bears:
    lo, hi = b["peak_idx"], int(df.index[df["date"] <= b["end_date"]][-1])
    k = lo + 1
    last_ev = -10 ** 9
    while k <= hi:
        if (not under[k]) and st_u[k - 1] >= PRE_DAYS and (k - last_ev) > COOLDOWN:
            ed = pd.Timestamp(dates[k])
            w = slice(k, min(k + OUT_WINDOW + 1, len(df)))
            pw, sw = price[w], sth[w]
            ab = pw > sw
            # cek >=BREAK_PERSIST hari berturut di atas STH RP
            run, mx, brk_i = 0, 0, None
            for t in range(len(ab)):
                run = run + 1 if ab[t] else 0
                if run > mx:
                    mx = run
                if run == BREAK_PERSIST and brk_i is None:
                    brk_i = k + t
            is_break = mx >= BREAK_PERSIST
            trough30 = float(np.min(pw)) if len(pw) else np.nan
            dd30 = trough30 / price[k] - 1.0
            r30 = (price[min(k + OUT_WINDOW, len(df) - 1)] / price[k] - 1.0)

            unl90 = ""
            back_below90 = ""
            d2u = np.nan
            if is_break:
                bd = pd.Timestamp(dates[brk_i])
                nu = [x for x in unlock_dates if x >= bd]
                d2u = (nu[0] - bd).days if nu else np.nan
                u = [x for x in unlock_dates if bd <= x <= bd + pd.Timedelta(days=SUB_WINDOW)]
                unl90 = str(u[0].date()) if u else "TIDAK"
                fw = df[(df["date"] > bd) & (df["date"] <= bd + pd.Timedelta(days=SUB_WINDOW))]
                back_below90 = bool(len(fw) and (fw["btc_price"] < fw["sth_cost_basis"]).any())

            rows.append(dict(
                cycle=b["cycle"], event_date=ed.date(), event_price=round(price[k], 2),
                sth_rp=round(sth[k], 2), pct_of_sthrp=round(100 * price[k] / sth[k], 1),
                hari_di_bawah_sebelumnya=int(st_u[k - 1]),
                outcome=("BREAK" if is_break else "DITOLAK"),
                max_hari_berturut_di_atas=int(mx),
                break_date=(str(pd.Timestamp(dates[brk_i]).date()) if brk_i is not None else ""),
                dd_30d_pct=round(dd30 * 100, 1), ret_30d_pct=round(r30 * 100, 1),
                unlock_dlm_90d=unl90, hari_break_ke_unlock=d2u,
                balik_bawah_sthrp_dlm_90d=back_below90,
                censored_cycle=b["censored"]))
            last_ev = k
            k += COOLDOWN
        else:
            k += 1

ev = pd.DataFrame(rows)
pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
print("\n" + "=" * 104)
print("EVENT 'SENTUHAN DARI BAWAH' (harga naik tembus %.0f%% STH RP setelah >=%dd di bawah)"
      % (TOUCH_FRAC * 100, PRE_DAYS))
print("=" * 104)
print(ev[["cycle", "event_date", "event_price", "sth_rp", "pct_of_sthrp",
          "hari_di_bawah_sebelumnya", "outcome", "max_hari_berturut_di_atas",
          "dd_30d_pct", "ret_30d_pct"]].to_string(index=False))

n = len(ev)
nb = int((ev["outcome"] == "BREAK").sum())
print("\n--- HIT RATE ---")
print("  n total event = %d | BREAK = %d (%.0f%%) | DITOLAK = %d (%.0f%%)"
      % (n, nb, 100 * nb / n, n - nb, 100 * (n - nb) / n))
print("\n  Sebaran per cycle:")
tab = ev.groupby("cycle")["outcome"].value_counts().unstack(fill_value=0)
print(tab.to_string())
print("\n  CATATAN independensi: event dalam satu cycle berkorelasi (bear yang sama).")
print("  n cycle = %d, jadi jumlah 'bear independen' = %d bukan %d."
      % (ev["cycle"].nunique(), ev["cycle"].nunique(), n))

rej = ev[ev["outcome"] == "DITOLAK"]
if len(rej):
    print("\n--- BIAYA SALAH BACA (event DITOLAK) ---")
    print("  n=%d | drawdown 30d MEDIAN = %.1f%% | min=%.1f%% max=%.1f%%"
          % (len(rej), rej["dd_30d_pct"].median(), rej["dd_30d_pct"].min(),
             rej["dd_30d_pct"].max()))
    print("  return 30d median = %+.1f%%" % rej["ret_30d_pct"].median())
brk = ev[ev["outcome"] == "BREAK"]
if len(brk):
    print("\n--- EVENT BREAK: drawdown 30d median = %.1f%% | return 30d median = %+.1f%% ---"
          % (brk["dd_30d_pct"].median(), brk["ret_30d_pct"].median()))

print("\n--- SUB-PERTANYAAN: dari event BREAK, berapa diikuti UNLOCK struktural dalam %dd? ---"
      % SUB_WINDOW)
if len(brk):
    print(brk[["cycle", "event_date", "break_date", "unlock_dlm_90d",
               "hari_break_ke_unlock", "balik_bawah_sthrp_dlm_90d"]].to_string(index=False))
    ok = (brk["unlock_dlm_90d"] != "TIDAK").sum()
    print("\n  BREAK diikuti unlock <=%dd : %d dari %d (%.0f%%)"
          % (SUB_WINDOW, ok, len(brk), 100 * ok / len(brk)))
    fb = brk["balik_bawah_sthrp_dlm_90d"].sum()
    print("  BREAK yang harganya BALIK ke bawah STH RP dalam %dd : %d dari %d (%.0f%%)"
          % (SUB_WINDOW, fb, len(brk), 100 * fb / len(brk)))
    print("  -> ini yang membedakan reversal asli dari resistance-rally.")
    dd = brk["hari_break_ke_unlock"].dropna()
    if len(dd):
        print("  Jarak break -> unlock BERIKUTNYA (hari, tanpa batas window): %s"
              % [int(x) for x in dd.values])

ev.to_csv(os.path.join(OUTDIR, "events_sth_rp_resistance_bear.csv"), index=False)
print("\nCSV -> events_sth_rp_resistance_bear.csv")
