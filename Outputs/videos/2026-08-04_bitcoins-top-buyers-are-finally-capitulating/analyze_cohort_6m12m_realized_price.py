"""
VALIDASI 1 - cohort_6m12m_realized_price
Klaim On-Chain Mind [03:31]-[04:16], [11:40]-[11:57]:
  Kohort holder 6 bulan-1 tahun ("top buyers") underwater rata-rata ~13 bulan di
  tiga bear terakhir; momen flip (harga balik di atas cost basis kohort) menandai
  resumsi bull market. Episode terakhir mulai Nov 2025 di ~$95.000 -> proyeksi
  selesai ~Des 2026.

REKONSTRUKSI (PENTING: ini rekonstruksi dari HODL-wave band, BUKAN seri
realized-price kohort resmi Glassnode -- angka bisa beda dari yang ditayangkan):
  cohort_supply_btc = (supply_6m-12m / 100) * (lth_supply_btc + sth_supply_btc)
  cohort_rcap_usd   = (realized_cap_6m-12m / 100) * realized_cap_usd
  cohort_RP         = cohort_rcap_usd / cohort_supply_btc

DEFINISI EVENT (dikunci sebelum menghitung):
  - Underwater episode START: hari pertama btc_price < cohort_RP setelah >=90 hari
    berturut-turut btc_price >= cohort_RP.
  - Underwater episode END (FLIP): hari pertama btc_price > cohort_RP yang diikuti
    >=14 hari berturut-turut btc_price > cohort_RP (anti-whipsaw).
    ANTI-LOOKAHEAD: tanggal flip baru DIKETAHUI 13 hari kemudian
    (flip_confirmed = flip + 13d). Kedua tanggal dilaporkan; lead/lag dihitung
    untuk kedua versi.
  - Unlock struktural framework: hari pertama sth_cost_basis > realized_price
    setelah >=30 hari berturut-turut inversi (STH RP < RP). Aturan ini at-gate
    (tidak perlu data masa depan) dan mereproduksi persis n=4 unlock dari
    validasi 200D-MA yang sudah CLOSED (2012, 2015, 2019, 2023).
  - Matching episode->unlock: unlock pertama yang jatuh di window
    [start episode, flip + 365 hari]. Kalau tidak ada -> "TIDAK ADA".

Output print ASCII saja (Windows console).
"""

import numpy as np
import os
import pandas as pd

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = (r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos"
          r"\2026-08-04_bitcoins-top-buyers-are-finally-capitulating")

MIN_ABOVE_DAYS = 90   # syarat "sehat" sebelum episode underwater dimulai
FLIP_PERSIST   = 14   # persistensi konfirmasi flip
UNLOCK_PRE     = 30   # hari berturut inversi sebelum unlock dihitung sah
MATCH_WINDOW   = 365  # window matching episode -> unlock

CYCLE_PEAKS = {"2011": "2011-06-08", "2013": "2013-11-30", "2017": "2017-12-17",
               "2021": "2021-11-10", "2025": "2025-10-06"}

# ------------------------------------------------------------------ load
df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "realized_price", "sth_cost_basis",
                       "realized_cap_usd", "lth_supply_btc", "sth_supply_btc"]).copy()
df = df[df["btc_price"] > 0].reset_index(drop=True)

df["tot_supply"] = df["lth_supply_btc"] + df["sth_supply_btc"]
df["coh_supply"] = df["supply_6m-12m"] / 100.0 * df["tot_supply"]
df["coh_rcap"]   = df["realized_cap_6m-12m"] / 100.0 * df["realized_cap_usd"]
df["coh_rp"]     = df["coh_rcap"] / df["coh_supply"]
df = df.dropna(subset=["coh_rp"]).reset_index(drop=True)

price = df["btc_price"].values
crp   = df["coh_rp"].values
dates = df["date"].values
sth   = df["sth_cost_basis"].values
rp    = df["realized_price"].values

print("=" * 104)
print("VALIDASI 1 - COHORT 6m-12m REALIZED PRICE (rekonstruksi dari HODL-wave band)")
print("=" * 104)
print("Rentang data : %s s/d %s (n hari = %d)"
      % (df["date"].min().date(), df["date"].max().date(), len(df)))

# ------------------------------------------------------------------ SANITY GATE
print("\n--- SANITY GATE ---")
last = df.iloc[-1]
print("[1] Rasio coh_RP/RP per %s = %.3fx (target sanity claim-tester ~1.90x)"
      % (last["date"].date(), last["coh_rp"] / last["realized_price"]))
chk = df[df["date"] == "2026-07-01"]
if len(chk):
    r = chk.iloc[0]
    print("    Cek 2026-07-01 : coh_RP=$%.0f | RP=$%.0f | rasio=%.3fx"
          % (r["coh_rp"], r["realized_price"], r["coh_rp"] / r["realized_price"]))

print("\n[2] coh_RP > RP di titik 'top buyer sudah matang' (peak + 9 bulan).")
print("    CATATAN: band 6m-12m itu ROLLING -- pembeli puncak baru masuk band ini")
print("    6-12 bulan SETELAH peak, jadi cek harus di peak+9m, bukan di awal bear.")
gate_ok = True
for cyc, pk in CYCLE_PEAKS.items():
    tgt = pd.Timestamp(pk) + pd.Timedelta(days=274)
    sub = df[df["date"] <= tgt]
    if len(sub) == 0 or sub.iloc[-1]["date"] < tgt - pd.Timedelta(days=30):
        print("    peak %s + 9m (%s) : data belum ada (episode masih berjalan)" % (cyc, tgt.date()))
        continue
    r = sub.iloc[-1]
    ok = r["coh_rp"] > r["realized_price"]
    gate_ok = gate_ok and ok
    print("    peak %s + 9m (%s) : coh_RP=%12.2f  RP=%12.2f  rasio=%.2fx -> %s"
          % (cyc, r["date"].date(), r["coh_rp"], r["realized_price"],
             r["coh_rp"] / r["realized_price"], "OK" if ok else "GAGAL"))
print("    Gate coh_RP>RP : %s" % ("LULUS" if gate_ok else "GAGAL"))

# ------------------------------------------------------------------ episodes
above = (price >= crp)
streak_above = np.zeros(len(df), dtype=int)
c = 0
for i, v in enumerate(above):
    c = c + 1 if v else 0
    streak_above[i] = c

episodes = []
i = 1
while i < len(df):
    if (not above[i]) and streak_above[i - 1] >= MIN_ABOVE_DAYS:
        start = i
        flip = None
        j = start + 1
        while j < len(df):
            if price[j] > crp[j]:
                win = price[j:j + FLIP_PERSIST] > crp[j:j + FLIP_PERSIST]
                if len(win) == FLIP_PERSIST and win.all():
                    flip = j
                    break
            j += 1
        episodes.append((start, flip))
        if flip is None:
            break
        i = flip + FLIP_PERSIST
    else:
        i += 1

# ------------------------------------------------------------------ unlock struktural
inv = (sth < rp)
streak_inv = np.zeros(len(df), dtype=int)
c = 0
for i, v in enumerate(inv):
    c = c + 1 if v else 0
    streak_inv[i] = c
unlocks = [i for i in range(1, len(df)) if (not inv[i]) and streak_inv[i - 1] >= UNLOCK_PRE]
unlock_dates = [pd.Timestamp(dates[i]) for i in unlocks]

print("\n--- UNLOCK STRUKTURAL (STH RP cross naik RP, setelah inversi >=%dd) ---" % UNLOCK_PRE)
for i in unlocks:
    print("    %s  price=$%11.2f  panjang inversi sebelumnya=%dd"
          % (pd.Timestamp(dates[i]).date(), price[i], streak_inv[i - 1]))
print("    n unlock = %d  (cocok dgn validasi 200D-MA CLOSED 2026-07-28: 2012/2015/2019/2023)"
      % len(unlocks))

# ------------------------------------------------------------------ sanity gate [3]
print("\n[3] Episode underwater terakhir harus mulai ~Nov 2025 di ~$90-100k:")
last_ep = episodes[-1]
sd_last = pd.Timestamp(dates[last_ep[0]])
ok3 = (pd.Timestamp("2025-10-01") <= sd_last <= pd.Timestamp("2025-12-31")
       and 88000 <= price[last_ep[0]] <= 102000)
print("    aktual: mulai %s di harga $%.0f (coh_RP $%.0f) -> %s"
      % (sd_last.date(), price[last_ep[0]], crp[last_ep[0]],
         "OK (klaim video ~Nov 2025 @ ~$95.000)" if ok3 else "GAGAL"))

# ------------------------------------------------------------------ forward returns
def fwd_ret(idx, horizon):
    tgt = pd.Timestamp(dates[idx]) + pd.Timedelta(days=horizon)
    sub = df[df["date"] >= tgt]
    if len(sub) == 0:
        return np.nan
    return sub.iloc[0]["btc_price"] / price[idx] - 1.0

base = {}
for h in (90, 180, 365):
    vals = [fwd_ret(k, h) for k in range(len(df))]
    base[h] = np.array([v for v in vals if not np.isnan(v)])

# ------------------------------------------------------------------ tabel episode
CTX = {1: "2011 bear", 2: "2014-15 bear", 3: "2018-19 bear", 4: "2020 COVID crash",
       5: "2022-23 bear", 6: "2025-26 bear (berjalan)"}
rows = []
for n, (s, f) in enumerate(episodes, 1):
    sd, sp = pd.Timestamp(dates[s]), price[s]
    if f is not None:
        fd, fp = pd.Timestamp(dates[f]), price[f]
        dur = (fd - sd).days
        fd_conf = fd + pd.Timedelta(days=FLIP_PERSIST - 1)
        seg = slice(s, f + 1)
        censored = False
    else:
        fd = fp = fd_conf = None
        dur = (df["date"].max() - sd).days
        seg = slice(s, len(df))
        censored = True

    trough_i = s + int(np.argmin(price[seg]))
    max_gap = float(np.min(price[seg] / crp[seg]) - 1.0)

    hi = (fd + pd.Timedelta(days=MATCH_WINDOW)) if fd is not None else df["date"].max()
    cand = [u for u in unlock_dates if sd <= u <= hi]
    ud = cand[0] if cand else None

    rows.append(dict(
        episode=n, cycle_context=CTX.get(n, "?"),
        start_date=sd.date(), start_price=round(sp, 2), start_coh_rp=round(crp[s], 2),
        flip_date=(fd.date() if fd is not None else "ONGOING"),
        flip_price=(round(fp, 2) if fd is not None else np.nan),
        flip_confirmed_date=(fd_conf.date() if fd_conf is not None else ""),
        duration_days=dur, duration_months=round(dur / 30.44, 1),
        censored=censored,
        trough_date=pd.Timestamp(dates[trough_i]).date(),
        trough_price=round(price[trough_i], 2),
        max_pct_below_cohRP=round(max_gap * 100, 1),
        unlock_date=(ud.date() if ud is not None else "TIDAK ADA"),
        unlock_minus_flip_days=((ud - fd).days if (ud is not None and fd is not None) else np.nan),
        unlock_minus_flipconf_days=((ud - fd_conf).days if (ud is not None and fd_conf is not None) else np.nan),
        fwd90=(round(fwd_ret(f, 90) * 100, 1) if f is not None else np.nan),
        fwd180=(round(fwd_ret(f, 180) * 100, 1) if f is not None else np.nan),
        fwd365=(round(fwd_ret(f, 365) * 100, 1) if f is not None else np.nan),
    ))

ev = pd.DataFrame(rows)
pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)

print("\n" + "=" * 104)
print("EPISODE UNDERWATER (harga < cohort_RP)   n total = %d" % len(ev))
print("=" * 104)
print(ev[["episode", "cycle_context", "start_date", "start_price", "start_coh_rp",
          "flip_date", "flip_price", "duration_days", "duration_months",
          "censored", "max_pct_below_cohRP"]].to_string(index=False))

# ------------------------------------------------------------------ A: durasi
done = ev[~ev["censored"]]
print("\n--- PERTANYAAN A: DURASI ---")
print("n episode SELESAI = %d ; n episode BERJALAN (censored) = %d"
      % (len(done), int(ev["censored"].sum())))
d_all = done["duration_days"].values
print("  SEMUA episode selesai (n=%d): min=%dd median=%.0fd mean=%.0fd max=%dd"
      % (len(d_all), d_all.min(), np.median(d_all), d_all.mean(), d_all.max()))
print("     -> dalam bulan: min=%.1f median=%.1f mean=%.1f max=%.1f"
      % (d_all.min() / 30.44, np.median(d_all) / 30.44, d_all.mean() / 30.44, d_all.max() / 30.44))

bear3 = done[done["episode"].isin([2, 3, 5])]
d3 = bear3["duration_days"].values
print("  SUBSET '3 bear terakhir' spt klaim video (2014-15, 2018-19, 2022-23; n=%d):" % len(d3))
print("     durasi: %s hari = %s bulan"
      % ([int(x) for x in d3], [round(float(x) / 30.44, 1) for x in d3]))
print("     mean=%.0fd (%.1f bulan)  median=%.0fd (%.1f bulan)  spread=%dd (%.1f bulan)"
      % (d3.mean(), d3.mean() / 30.44, np.median(d3), np.median(d3) / 30.44,
         d3.max() - d3.min(), (d3.max() - d3.min()) / 30.44))
print("  CATATAN: episode 1 (2011) = era supply band tipis -> flag low-reliability.")
print("           episode 4 (2020 COVID) BUKAN cycle bear -- video tidak menghitungnya,")
print("           tapi mesin event menangkapnya (false positive kalau flip dipakai mentah).")

# ------------------------------------------------------------------ B: lead/lag
print("\n--- PERTANYAAN B (PALING PENTING): LEAD/LAG FLIP vs UNLOCK STRUKTURAL ---")
print("(positif = flip MENDAHULUI unlock = leading marker; negatif = flip TERLAMBAT)")
print(ev[["episode", "cycle_context", "flip_date", "flip_confirmed_date", "unlock_date",
          "unlock_minus_flip_days", "unlock_minus_flipconf_days"]].to_string(index=False))
ll = ev["unlock_minus_flip_days"].dropna().values
llc = ev["unlock_minus_flipconf_days"].dropna().values
if len(ll):
    print("\n  n pasangan flip<->unlock = %d" % len(ll))
    print("  lead/lag (flip mentah)     : %s | median=%+.0fd mean=%+.0fd positif=%d/%d"
          % (["%+d" % x for x in ll], np.median(ll), ll.mean(), (ll > 0).sum(), len(ll)))
    print("  lead/lag (flip TERKONFIRM) : %s | median=%+.0fd mean=%+.0fd positif=%d/%d"
          % (["%+d" % x for x in llc], np.median(llc), llc.mean(), (llc > 0).sum(), len(llc)))
print("  PEMBANDING: 200D MA reclaim mendahului unlock +23 s/d +51 hari (n=4, CLOSED 2026-07-28)")

# ------------------------------------------------------------------ C: forward return
print("\n--- PERTANYAAN C: FORWARD RETURN DARI TANGGAL FLIP (%) ---")
print(ev[["episode", "cycle_context", "flip_date", "fwd90", "fwd180", "fwd365"]].to_string(index=False))
print("\n  BASELINE TANPA SYARAT (semua hari %s - %s):"
      % (df["date"].min().date(), df["date"].max().date()))
for h in (90, 180, 365):
    a = base[h]
    print("    %3dd : n=%d  median=%+.1f%%  mean=%+.1f%%  P(positif)=%.0f%%"
          % (h, len(a), np.median(a) * 100, a.mean() * 100, (a > 0).mean() * 100))
print("\n  FLIP EVENTS vs baseline:")
for h, col in [(90, "fwd90"), (180, "fwd180"), (365, "fwd365")]:
    v = ev[col].dropna().values
    v2 = ev[ev["episode"] != 1][col].dropna().values   # buang 2012 (pre-2013 rapuh)
    print("    %3dd : n=%d median=%+.1f%% (baseline %+.1f%%) | tanpa ep1(2012): n=%d median=%+.1f%%"
          % (h, len(v), np.median(v), np.median(base[h]) * 100, len(v2), np.median(v2)))

# ------------------------------------------------------------------ proyeksi
cur = ev[ev["censored"]]
if len(cur):
    c0 = cur.iloc[0]
    sd = pd.Timestamp(c0["start_date"])
    print("\n--- PROYEKSI EPISODE BERJALAN (menjawab klaim 'Des 2026') ---")
    print("  mulai %s @ $%.0f (coh_RP $%.0f); per %s sudah %d hari (%.1f bulan)"
          % (sd.date(), c0["start_price"], c0["start_coh_rp"],
             df["date"].max().date(), c0["duration_days"], c0["duration_months"]))
    print("  implied flip pakai 3 bear terakhir (%dd - %dd): %s s/d %s"
          % (d3.min(), d3.max(), (sd + pd.Timedelta(days=int(d3.min()))).date(),
             (sd + pd.Timedelta(days=int(d3.max()))).date()))
    print("  implied flip pakai mean 3 bear (%.0fd) : %s"
          % (d3.mean(), (sd + pd.Timedelta(days=float(d3.mean()))).date()))
    print("  implied flip pakai SEMUA episode (%dd - %dd): %s s/d %s"
          % (d_all.min(), d_all.max(), (sd + pd.Timedelta(days=int(d_all.min()))).date(),
             (sd + pd.Timedelta(days=int(d_all.max()))).date()))

ev.to_csv(os.path.join(OUTDIR, "events_cohort_6m12m_realized_price.csv"), index=False)
print("\nCSV -> events_cohort_6m12m_realized_price.csv")
