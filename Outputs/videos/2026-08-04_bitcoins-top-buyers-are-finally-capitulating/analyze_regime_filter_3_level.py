"""
VALIDASI 2 - regime_filter_3_level
Klaim On-Chain Mind [00:33]-[01:03], [10:33]-[10:49]:
  Tiga level regime = STH Realized Price, 200D MA, 365D MA.
  Harga di ATAS ketiganya = bull hidup; di BAWAH ketiganya = bear kembali.
  Bear terkonfirmasi ~$102.000 Nov 2025 saat cross ke bawah yearly MA.
  Urutan reclaim yang diklaim: STH RP dulu (~$66.000), baru 365D MA (~$85.000).

SUDAH DIVALIDASI SEBELUMNYA (tidak diulang): 200D MA reclaim sisi NAIK ->
CLOSED 2026-07-28, mendahului unlock STH RP/RP 23-51 hari (n=4).
Yang diuji di sini: sisi TURUN, 365D MA spesifik, dan kombinasi 3 level.

DEFINISI (dikunci sebelum menghitung):
  - ma200 & ma365 = rolling mean btc_price, min_periods penuh (BUKAN centered).
    ma365 baru tersedia mulai 2011-07-17 -> peak 2011 tidak bisa diuji penuh.
  - REGIME-OFF event: hari pertama dari streak >=5 hari berturut-turut
    btc_price < min(sth_cost_basis, ma200, ma365). Cooldown 90 hari antar event.
  - REGIME-ON (reclaim per level): close di atas level >=3 hari berturut.
  - Unlock struktural: hari pertama sth_cost_basis > realized_price setelah
    >=30 hari inversi (sama seperti validasi 1; at-gate).
  - False positive (pertanyaan B): setelah REGIME-OFF event, harga mencetak ATH
    BARU dalam 180 hari (ATH = running max harga s/d tanggal event).

Output print ASCII saja.
"""

import numpy as np
import os
import pandas as pd

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = (r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos"
          r"\2026-08-04_bitcoins-top-buyers-are-finally-capitulating")

OFF_PERSIST  = 5
ON_PERSIST   = 3
COOLDOWN     = 90
FP_WINDOW    = 180
UNLOCK_PRE   = 30

CYCLE_WINDOWS = [("2011", "2010-07-17", "2011-12-31"),
                 ("2013", "2012-01-01", "2014-06-30"),
                 ("2017", "2015-01-01", "2018-06-30"),
                 ("2021", "2019-01-01", "2022-06-30"),
                 ("2025", "2023-01-01", "2026-12-31")]

# ------------------------------------------------------------------ load
df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "sth_cost_basis", "realized_price"]).copy()
df = df[df["btc_price"] > 0].reset_index(drop=True)

df["ma200"] = df["btc_price"].rolling(200, min_periods=200).mean()
df["ma365"] = df["btc_price"].rolling(365, min_periods=365).mean()

print("=" * 104)
print("VALIDASI 2 - REGIME FILTER 3 LEVEL (STH RP + 200D MA + 365D MA)")
print("=" * 104)
print("Rentang data : %s s/d %s (n=%d hari)"
      % (df["date"].min().date(), df["date"].max().date(), len(df)))
print("ma200 mulai valid %s ; ma365 mulai valid %s (min_periods penuh, rolling bukan centered)"
      % (df.loc[df["ma200"].notna(), "date"].min().date(),
         df.loc[df["ma365"].notna(), "date"].min().date()))
# cross-check vs kolom 200_dma bawaan
cc = df.dropna(subset=["ma200", "200_dma"])
print("Cross-check ma200 hitung-sendiri vs kolom '200_dma': korelasi=%.5f, median abs diff=%.2f%%"
      % (cc["ma200"].corr(cc["200_dma"]),
         (100 * (cc["ma200"] / cc["200_dma"] - 1).abs()).median()))

price = df["btc_price"].values
dates = df["date"].values
lvl = df[["sth_cost_basis", "ma200", "ma365"]].values
have_all = ~np.isnan(lvl).any(axis=1)
below_all = have_all & (price < np.nanmin(lvl, axis=1))

# ------------------------------------------------------------------ cycle peaks
peaks = []
for cyc, a, b in CYCLE_WINDOWS:
    sub = df[(df["date"] >= a) & (df["date"] <= b)]
    if len(sub) == 0:
        continue
    i = sub["btc_price"].idxmax()
    peaks.append((cyc, i, pd.Timestamp(dates[i]), price[i]))
print("\n--- CYCLE PEAK (max harga di window tiap cycle) ---")
for cyc, i, d, p in peaks:
    print("    %s : %s  $%.2f" % (cyc, d.date(), p))

# ------------------------------------------------------------------ regime-off events
off_events = []
i = 0
while i < len(df) - OFF_PERSIST:
    if below_all[i] and below_all[i:i + OFF_PERSIST].all():
        off_events.append(i)
        j = i + OFF_PERSIST
        while j < len(df) and (pd.Timestamp(dates[j]) - pd.Timestamp(dates[i])).days < COOLDOWN:
            j += 1
        i = j
    else:
        i += 1
print("\n--- REGIME-OFF EVENTS (close < ketiga level, >=%dd, cooldown %dd) : n=%d ---"
      % (OFF_PERSIST, COOLDOWN, len(off_events)))

# ------------------------------------------------------------------ unlock
inv = (df["sth_cost_basis"] < df["realized_price"]).values
st = np.zeros(len(df), dtype=int)
c = 0
for k, v in enumerate(inv):
    c = c + 1 if v else 0
    st[k] = c
unlocks = [k for k in range(1, len(df)) if (not inv[k]) and st[k - 1] >= UNLOCK_PRE]
unlock_dates = [pd.Timestamp(dates[k]) for k in unlocks]
print("Unlock struktural (n=%d): %s" % (len(unlock_dates), [str(u.date()) for u in unlock_dates]))

# =================================================================== A
print("\n" + "=" * 104)
print("PERTANYAAN A - SISI TURUN: berapa lama setelah peak sinyal '3-level off' nyala?")
print("=" * 104)
rowsA = []
for cyc, pi, pd_, pp in peaks:
    cand = [e for e in off_events if e > pi]
    if not cand:
        rowsA.append(dict(cycle=cyc, peak_date=pd_.date(), peak_price=round(pp, 2),
                          off_date="TIDAK ADA", lag_days=np.nan, dd_pct=np.nan,
                          off_price=np.nan, note="belum ada"))
        continue
    e = cand[0]
    ed = pd.Timestamp(dates[e])
    lag = (ed - pd_).days
    dd = price[e] / pp - 1.0
    note = ""
    if cyc == "2011":
        note = "ma365 baru valid 2011-07-17 (+39d stlh peak) -> lag minimum artifisial"
    rowsA.append(dict(cycle=cyc, peak_date=pd_.date(), peak_price=round(pp, 2),
                      off_date=ed.date(), off_price=round(price[e], 2),
                      lag_days=lag, dd_pct=round(dd * 100, 1), note=note))
A = pd.DataFrame(rowsA)
pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
print(A.to_string(index=False))
val = A["lag_days"].dropna().values
print("\n  n cycle terukur = %d | lag: %s hari | median=%.0fd" %
      (len(val), [int(x) for x in val], np.median(val)))
print("  drawdown dari peak saat sinyal nyala: %s persen" % [float(x) for x in A["dd_pct"].dropna().values])
print("  PEMBANDING: alarm bear CEPAT framework di Okt 2025 = +4 hari setelah peak")
print("  (angka referensi dari Decision_Framework v2 sec.0; alarm cepat cycle LAIN")
print("   TIDAK dihitung ulang di sini -- perbandingan lintas cycle belum lengkap)")

# =================================================================== B
print("\n" + "=" * 104)
print("PERTANYAAN B - FALSE POSITIVE: regime-off tapi ATH baru dalam %d hari?" % FP_WINDOW)
print("=" * 104)
run_ath = df["btc_price"].cummax().values

def fwd(idx, h):
    tgt = pd.Timestamp(dates[idx]) + pd.Timedelta(days=h)
    sub = df[df["date"] >= tgt]
    return (sub.iloc[0]["btc_price"] / price[idx] - 1.0) if len(sub) else np.nan

# grouping "bear episode": event dalam 1 bear yang sama (gap < 365d) dianggap 1 klaster
groups, gid = [], 0
for n_, e in enumerate(off_events):
    if n_ > 0 and (pd.Timestamp(dates[e]) - pd.Timestamp(dates[off_events[n_ - 1]])).days > 365:
        gid += 1
    groups.append(gid)

rowsB = []
for e in off_events:
    ed = pd.Timestamp(dates[e])
    ath_at = run_ath[e]
    fut = df[(df["date"] > ed) & (df["date"] <= ed + pd.Timedelta(days=FP_WINDOW))]
    made_ath = bool(len(fut) and fut["btc_price"].max() > ath_at)
    # drawdown terdalam 180d setelah event
    dd180 = (fut["btc_price"].min() / price[e] - 1.0) if len(fut) else np.nan
    rowsB.append(dict(klaster=groups[off_events.index(e)],
                      off_date=ed.date(), off_price=round(price[e], 2),
                      ath_saat_event=round(ath_at, 2),
                      ath_baru_dlm_180d=made_ath,
                      klasifikasi=("FALSE POSITIVE" if made_ath else "bear beneran"),
                      min_price_180d=round(fut["btc_price"].min(), 2) if len(fut) else np.nan,
                      dd_180d_pct=round(dd180 * 100, 1) if len(fut) else np.nan,
                      fwd90=round(fwd(e, 90) * 100, 1), fwd180=round(fwd(e, 180) * 100, 1),
                      fwd365=round(fwd(e, 365) * 100, 1)))
B = pd.DataFrame(rowsB)
print(B.to_string(index=False))
nfp = int(B["ath_baru_dlm_180d"].sum())
print("\n  n regime-off event = %d | FALSE POSITIVE = %d (%.0f%%) | bear beneran = %d"
      % (len(B), nfp, 100 * nfp / len(B), len(B) - nfp))

print("  INDEPENDENSI: %d event itu mengelompok jadi %d klaster bear (gap >365d antar klaster)"
      % (len(B), B["klaster"].nunique()))
print("  -> uji false-positive efektif berbasis n=%d episode independen, BUKAN n=%d"
      % (B["klaster"].nunique(), len(B)))
print("\n  Forward return DARI tanggal regime-off (uji 'apa mahal keluar di sini?'):")
for h in ("fwd90", "fwd180", "fwd365"):
    v = B[h].dropna().values
    print("    %s : n=%d median=%+.1f%% | positif=%d/%d (kalau sering positif = sinyal telat/mahal)"
          % (h, len(v), np.median(v), int((v > 0).sum()), len(v)))

print("\n  CEK EKSPLISIT dua kasus yang sering bikin sinyal lain salah bunyi:")
for label, lo, hi in [("Mar 2020 (COVID)", "2020-02-15", "2020-04-30"),
                      ("Mei 2021", "2021-05-01", "2021-08-31")]:
    hit = B[(pd.to_datetime(B["off_date"]) >= lo) & (pd.to_datetime(B["off_date"]) <= hi)]
    if len(hit):
        print("    %s -> ADA event: %s" % (label, hit.to_dict("records")))
    else:
        # kenapa tidak nyala? tampilkan hari 'below_all' di window itu
        w = df[(df["date"] >= lo) & (df["date"] <= hi)].copy()
        wb = below_all[(df["date"] >= lo).values & (df["date"] <= hi).values]
        print("    %s -> TIDAK ada event. Hari 'close < ketiga level' di window: %d dari %d hari"
              % (label, int(wb.sum()), len(w)))
        if wb.sum():
            print("        tanggalnya: %s"
                  % [str(x.date()) for x in w.loc[wb, "date"]][:15])

# =================================================================== C
print("\n" + "=" * 104)
print("PERTANYAAN C - URUTAN RECLAIM (STH RP vs 200D MA vs 365D MA vs unlock)")
print("=" * 104)
print("Catatan: trough cycle ditentukan EX-POST (studi urutan deskriptif, bukan sinyal live).")

def first_reclaim(level_col, from_idx, to_idx):
    lv = df[level_col].values
    for k in range(from_idx, min(to_idx, len(df) - ON_PERSIST)):
        if np.isnan(lv[k]):
            continue
        w = price[k:k + ON_PERSIST] > lv[k:k + ON_PERSIST]
        if len(w) == ON_PERSIST and w.all():
            return k
    return None

rowsC = []
for idx, (cyc, pi, pdte, pp) in enumerate(peaks):
    nxt_peak = peaks[idx + 1][1] if idx + 1 < len(peaks) else len(df) - 1
    seg = df.iloc[pi:nxt_peak]
    ti = seg["btc_price"].idxmin()
    td = pd.Timestamp(dates[ti])
    ud = next((u for u in unlock_dates if u > pdte), None)
    row = dict(cycle=cyc, peak_date=pdte.date(), trough_date=td.date(),
               trough_price=round(price[ti], 2),
               unlock_date=(ud.date() if ud else "BELUM"))
    for col, nm in [("sth_cost_basis", "sthrp"), ("ma200", "ma200"), ("ma365", "ma365")]:
        k = first_reclaim(col, ti, nxt_peak)
        row[nm + "_reclaim"] = pd.Timestamp(dates[k]).date() if k is not None else "-"
        row[nm + "_price"] = round(price[k], 2) if k is not None else np.nan
        row[nm + "_vs_unlock_d"] = ((ud - pd.Timestamp(dates[k])).days
                                    if (k is not None and ud is not None) else np.nan)
    rowsC.append(row)
C = pd.DataFrame(rowsC)
print(C[["cycle", "peak_date", "trough_date", "trough_price", "sthrp_reclaim",
         "ma200_reclaim", "ma365_reclaim", "unlock_date"]].to_string(index=False))
print("\nHarga di tiap reclaim:")
print(C[["cycle", "sthrp_price", "ma200_price", "ma365_price"]].to_string(index=False))
print("\nJarak ke unlock (positif = reclaim MENDAHULUI unlock):")
print(C[["cycle", "sthrp_vs_unlock_d", "ma200_vs_unlock_d", "ma365_vs_unlock_d"]].to_string(index=False))

print("\nURUTAN reclaim per cycle:")
for _, r in C.iterrows():
    items = [(r["sthrp_reclaim"], "STH RP"), (r["ma200_reclaim"], "200D MA"),
             (r["ma365_reclaim"], "365D MA")]
    items = [(pd.Timestamp(str(a)), b) for a, b in items if a != "-"]
    items.sort()
    order = " -> ".join("%s (%s)" % (b, a.date()) for a, b in items)
    claim_ok = (len(items) == 3 and items[0][1] == "STH RP"
                and [b for a, b in items].index("365D MA") > [b for a, b in items].index("STH RP"))
    print("  %s : %s   | urutan klaim video (STH RP sebelum 365D MA)? %s"
          % (r["cycle"], order, "YA" if claim_ok else "TIDAK"))

A.to_csv(os.path.join(OUTDIR, "events_regime_filter_3_level_sisi_turun.csv"), index=False)
B.to_csv(os.path.join(OUTDIR, "events_regime_filter_3_level.csv"), index=False)
C.to_csv(os.path.join(OUTDIR, "events_regime_filter_3_level_reclaim.csv"), index=False)
print("\nCSV -> events_regime_filter_3_level*.csv")
