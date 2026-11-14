# -*- coding: utf-8 -*-
"""
V1 - Bullish MVRV Momentum cross (+ harga > STH RP) saat status bear, BUKAN Z1,
     sebagai penanda akhir bear.

Klaim video (On-Chain Mind 2026-09-15, [08:10]-[08:50] & [13:18]):
  "crossovers in this momentum view have tended to lead those big trend changes";
  MVRV Momentum "right on the edge" hijau pertama >1 tahun -> "might confirm bull is back".
Gap yang diuji: KB MVRV 6C.1 hanya menguji bullish cross di Z1 (n=4) & di koreksi bull
(n=10). Bullish cross selama bear terkonfirmasi TAPI di luar Z1 (kasus 2025-26: struktur N,
tidak pernah Z1) belum pernah diuji.

DEFINISI (dikunci sebelum menghitung, dipakai ulang persis):
  MVRV Momentum (KB 6C.1): fast = SMA30(mvrv_ratio); slow = SMA30(fast); gap = fast - slow.
    Bullish cross valid: gap[i] >= 0, gap[i-1] < 0, regime negatif sebelumnya >= 7 hari
    berturut, dan gap[i..i+6] semua >= 0 (bertahan >= 7 hari)  -> verbatim
    research/analyze_mvrv_momentum_bullcross.py.
    ANTI-LOOKAHEAD: validitas baru diketahui di hari ke-7 (i+6) -> TANGGAL KEPUTUSAN = i+6.
    Semua label at-gate (zona, Signal D, bear window) & outcome dihitung dari i+6.
  Bear window, cycle low, reclaim permanen, aturan HIT/MISS: verbatim
    findings_unlock_reachability_struktur_n.md (2026-08-25):
      peak list 2011-06-08, 2013-11-29, 2017-12-16, 2021-11-08, 2025-10-06
      cycle low = close terendah peak -> peak berikutnya
      reclaim permanen = hari pertama setelah low: close > sth_cost_basis & bertahan 90 hari
      bear window = peak -> reclaim permanen + 60 hari (censored -> hari terakhir data)
      HIT = tanggal keputusan >= reclaim - 30 hari DAN maxDD 90 hari > -20%; selain itu MISS
  Zona DF v2 sec.1 (2 dimensi, AVIV Upper = mean + 0.5*(+1sig - mean)) at-gate.
  Event = bullish cross valid dgn tanggal keputusan di bear window, zona at-gate != Z1,
    cooldown 30 hari antar event.
  Sub-kelompok: Signal D aktif at-gate (close > sth_cost_basis >= 3 hari berturut) vs tidak.
  Window mid-cycle 2019-06-26 s/d 2020-05-01 (analog struktur N) dilaporkan TERPISAH.
  Tidak ada varian parameter tambahan.
Output print ASCII saja.
"""
import numpy as np
import pandas as pd

MASTER = "D:/Claude Code/Projects/Onchain-Dashboard/data_master_all_metrics.csv"
OUTDIR = ("D:/Claude Code/Projects/Content-Breakdown/Outputs/videos/"
          "2026-09-15_bitcoin-mvrv-explained-almost-nobody-reads-it-properly")

HOLD = 7
COOLDOWN = 30
DD_FAIL = -20.0
EARLY_TOL = 30
FWD = 90
SIGD = 3

df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "sth_cost_basis", "realized_price", "200_dma"]).reset_index(drop=True)
df = df[df["btc_price"] > 0].reset_index(drop=True).copy()
LAST = df["date"].max()
N = len(df)
print("Data:", df["date"].min().date(), "s/d", LAST.date(), "| n hari =", N)

price = df["btc_price"].values
sth = df["sth_cost_basis"].values
rp = df["realized_price"].values
dates = df["date"]

# ---------------- zona DF v2 ----------------
aviv_mean = df["price_at_aviv_mean"].values
aviv_up = (df["price_at_aviv_mean"] + 0.5 * (df["price_at_aviv_plus_1_sigma"] - df["price_at_aviv_mean"])).values
lth = df["lth_cost_basis"].values


def zone_of(i):
    p, s, r, l, m, u = price[i], sth[i], rp[i], lth[i], aviv_mean[i], aviv_up[i]
    if np.isnan(m) or np.isnan(u):
        return "NA"
    conv = (abs(s - r) / r < 0.02) and (abs(r - l) / r < 0.02)
    if p >= u:
        return "Z5"
    if conv:
        return "Z2" if p < m else "Z4"
    if s > r:  # N
        if p < r:
            return "ZC"
        if p < s:
            return "ZD"
        if p < m:
            return "Z3"
        return "Z4"
    # T
    if p < s:
        return "Z1"
    if p < r:
        return "Z1b"
    return "Z2t"


df["zone"] = [zone_of(i) for i in range(N)]

# ---------------- streak close > STH RP ----------------
above = price > sth
streak = np.zeros(N, dtype=int)
for i in range(N):
    streak[i] = (streak[i - 1] + 1 if i > 0 else 1) if above[i] else 0
df["streak_above_sth"] = streak

# ---------------- bear windows (verbatim 08-25) ----------------
PEAKS = [pd.Timestamp(p) for p in ["2011-06-08", "2013-11-29", "2017-12-16", "2021-11-08", "2025-10-06"]]
CYC = ["2011", "2013", "2017", "2021", "2025"]


def reclaim_after(low_date):
    post = df[df["date"] > low_date].reset_index(drop=True)
    ab = (post["btc_price"] > post["sth_cost_basis"]).values
    for j in range(len(post) - 90):
        if ab[j] and ab[j:j + 90].all():
            return post.at[j, "date"]
    return None


bears = []
for k, (nm, p) in enumerate(zip(CYC, PEAKS)):
    end_search = PEAKS[k + 1] if k + 1 < len(PEAKS) else LAST
    seg = df[(df["date"] > p) & (df["date"] <= end_search)]
    li = seg["btc_price"].idxmin()
    low_date = df.at[li, "date"]
    rc = reclaim_after(low_date)
    bears.append(dict(cycle=nm, peak=p, low_date=low_date, low_price=float(df.at[li, "btc_price"]),
                      reclaim=rc, censored=rc is None,
                      end=(rc + pd.Timedelta(days=60)) if rc is not None else LAST))

print("\nBear window (definisi 08-25):")
for b in bears:
    print("  %s peak %s | low %s | reclaim permanen %s | window s/d %s%s" % (
        b["cycle"], b["peak"].date(), b["low_date"].date(),
        b["reclaim"].date() if b["reclaim"] is not None else "BELUM",
        b["end"].date(), "  [CENSORED]" if b["censored"] else ""))


def bear_of(d):
    for b in bears:
        if b["peak"] <= d <= b["end"]:
            return b
    return None


# ---------------- MVRV Momentum bullish cross (verbatim KB 6C.1 script) ----------------
fast = df["mvrv_ratio"].rolling(30).mean()
slow = fast.rolling(30).mean()
gap = (fast - slow).values
g = pd.Series(gap)
crosses, pending = [], []
run_neg = 0
for i in range(1, N):
    if np.isnan(gap[i]) or np.isnan(gap[i - 1]):
        run_neg = 0
        continue
    if gap[i] < 0:
        run_neg += 1
    else:
        if gap[i - 1] < 0 and run_neg >= HOLD:
            nxt = g.iloc[i:i + HOLD]
            if len(nxt) == HOLD and (nxt >= 0).all():
                crosses.append(i)
            elif len(nxt) < HOLD and (nxt >= 0).all():
                pending.append(i)
        run_neg = 0
print("\nTotal bullish cross valid seluruh sejarah: %d | pending (<7 hari data sesudah): %s" % (
    len(crosses), [str(dates.iloc[i].date()) for i in pending]))


def fwd_stats(j):
    d = dates.iloc[j]
    p0 = price[j]
    w = df[(df["date"] > d) & (df["date"] <= d + pd.Timedelta(days=FWD))]
    cens = (d + pd.Timedelta(days=FWD)) > LAST
    dd = round((float(w["btc_price"].min()) / p0 - 1) * 100, 1) if len(w) else np.nan
    r = np.nan
    if not cens:
        r = round((float(df[df["date"] <= d + pd.Timedelta(days=FWD)].iloc[-1]["btc_price"]) / p0 - 1) * 100, 1)
    return dd, r, cens


rows = []
for i in crosses:
    j = i + HOLD - 1  # tanggal keputusan
    d = dates.iloc[j]
    b = bear_of(d)
    in_mid = pd.Timestamp("2019-06-26") <= d <= pd.Timestamp("2020-05-01")
    if b is None and not in_mid:
        continue
    dd, r90, cens90 = fwd_stats(j)
    rows.append(dict(
        cross_date=str(dates.iloc[i].date()), decision_date=str(d.date()),
        window=("bear_" + b["cycle"]) if b is not None else "midcycle_2019_20",
        cycle=b["cycle"] if b is not None else "mid2019",
        price=round(price[j], 2), sth_rp=round(sth[j], 2), rp=round(rp[j], 2),
        zone_at_gate=df.at[j, "zone"], price_gt_sthrp=bool(above[j]),
        streak_above_sth=int(streak[j]), signalD_active=bool(streak[j] >= SIGD),
        _j=j, maxdd_90d=dd, ret_90d=r90, censored_90d=cens90))
ev = pd.DataFrame(rows)

# ---------------- penilaian di bear window ----------------
def judge(row, bear_rec, bear_cens):
    d = pd.Timestamp(row["decision_date"])
    if bear_cens:
        return "CENSORED", None
    lag = (d - bear_rec).days
    ok = (d >= bear_rec - pd.Timedelta(days=EARLY_TOL)) and (not np.isnan(row["maxdd_90d"])) and (row["maxdd_90d"] > DD_FAIL)
    return ("HIT" if ok else "MISS"), lag


verdicts, lags, excl, cool_flags = [], [], [], []
last_kept = None
for _, r in ev.iterrows():
    if r["window"].startswith("bear_"):
        b = [x for x in bears if x["cycle"] == r["cycle"]][0]
        v, lag = judge(r, b["reclaim"], b["censored"])
        if r["zone_at_gate"] == "Z1":
            e = "Z1 (dikecualikan)"
        else:
            d = pd.Timestamp(r["decision_date"])
            if last_kept is not None and (d - last_kept).days < COOLDOWN:
                e = "cooldown (dikecualikan)"
            else:
                e = "EVENT"
                last_kept = d
    else:
        v, lag, e = None, None, "midcycle (terpisah)"
    verdicts.append(v)
    lags.append(lag)
    excl.append(e)
ev["verdict"] = verdicts
ev["lag_vs_reclaim_hari"] = lags
ev["status"] = excl

# lag vs cycle low
lag_low = []
for _, r in ev.iterrows():
    if r["window"].startswith("bear_"):
        b = [x for x in bears if x["cycle"] == r["cycle"]][0]
        lag_low.append((pd.Timestamp(r["decision_date"]) - b["low_date"]).days)
    else:
        lag_low.append(None)
ev["lag_vs_cycle_low_hari"] = lag_low

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
show = ["cycle", "cross_date", "decision_date", "price", "zone_at_gate", "streak_above_sth",
        "signalD_active", "lag_vs_cycle_low_hari", "lag_vs_reclaim_hari", "maxdd_90d", "ret_90d", "verdict", "status"]

print("\n" + "=" * 130)
print("SEMUA BULLISH CROSS VALID DI BEAR WINDOW (termasuk Z1 yang dikecualikan)")
print("=" * 130)
print(ev[ev["window"].str.startswith("bear_")][show].to_string(index=False))

E = ev[ev["status"] == "EVENT"].copy()
judged = E[E["verdict"].isin(["HIT", "MISS"])]
nh = int((judged["verdict"] == "HIT").sum())
print("\n" + "=" * 130)
print("HASIL UTAMA - event = bullish cross di bear window, zona at-gate != Z1, cooldown 30 hari")
print("=" * 130)
print("  n event = %d (dinilai %d, censored %d)" % (len(E), len(judged), len(E) - len(judged)))
if len(judged):
    print("  HIT = %d | MISS = %d | hit rate = %.0f%%" % (nh, len(judged) - nh, 100.0 * nh / len(judged)))
print("  sebaran per cycle:", E.groupby("cycle").size().to_dict())
print("  verdict per cycle:")
print(E.groupby(["cycle", "verdict"]).size().unstack(fill_value=0).to_string())
print("  zona at-gate:", E["zone_at_gate"].value_counts().to_dict())
if len(judged):
    print("  median ret90 = %+.1f%% | median maxDD90 = %.1f%%" % (judged["ret_90d"].median(), judged["maxdd_90d"].median()))

print("\n  SUB-KELOMPOK Signal D at-gate:")
for flag, lab in [(True, "Signal D AKTIF (close>STH RP >=3 hari)"), (False, "Signal D TIDAK aktif")]:
    s = E[E["signalD_active"] == flag]
    sj = s[s["verdict"].isin(["HIT", "MISS"])]
    h = int((sj["verdict"] == "HIT").sum())
    hr = ("%.0f%%" % (100.0 * h / len(sj))) if len(sj) else "n/a"
    med = ("ret90 med %+.1f%%, maxDD90 med %.1f%%" % (sj["ret_90d"].median(), sj["maxdd_90d"].median())) if len(sj) else ""
    print("   - %-40s n=%d (dinilai %d) HIT=%d MISS=%d hit rate=%s | per cycle %s | %s" % (
        lab, len(s), len(sj), h, len(sj) - h, hr, s.groupby("cycle").size().to_dict(), med))

# ---------------- Z1 crosses (referensi konsistensi KB 6C.1) ----------------
Z = ev[ev["status"] == "Z1 (dikecualikan)"]
print("\n  Referensi: bullish cross di bear window dgn zona at-gate Z1 (dikecualikan): n=%d -> %s" % (
    len(Z), list(Z["decision_date"])))
print("  (KB 6C.1 mencatat Z1 n=4: Mei 2015, Okt 2015, Feb 2019, Des 2022 - dengan tanggal cross, bukan tanggal keputusan)")

# ---------------- baseline pembanding ----------------
print("\n" + "=" * 130)
print("BASELINE PEMBANDING")
print("=" * 130)
print("  (dari findings 08-25) kandidat (i) close>STH RP >=21 hari: n=7, HIT 2, hit rate 29%")
print("  (dari findings 08-04) Signal D BREAK -> unlock formal <=90 hari: 1/8 = 12% (KRITERIA BERBEDA)")

# like-for-like: 8 tanggal BREAK Signal D (findings 08-04) dinilai dgn aturan HIT/MISS 08-25
SIGD_BREAKS = ["2012-01-02", "2014-06-01", "2015-03-12", "2015-06-18", "2018-07-29",
               "2022-03-29", "2023-01-13", "2026-05-06"]
hh = mm = 0
out = []
for s in SIGD_BREAKS:
    d = pd.Timestamp(s)
    j = int(df.index[df["date"] == d][0])
    b = bear_of(d)
    dd, r90, c90 = fwd_stats(j)
    if b is None:
        out.append((s, "di luar bear window", dd, r90))
        continue
    if b["censored"]:
        out.append((s, "CENSORED", dd, r90))
        continue
    ok = d >= b["reclaim"] - pd.Timedelta(days=EARLY_TOL) and dd > DD_FAIL
    hh += ok
    mm += (not ok)
    out.append((s, "HIT" if ok else "MISS", dd, r90))
print("  Suplemen like-for-like: 8 tanggal BREAK Signal D (08-04) dinilai dgn aturan HIT/MISS 08-25:")
for s, v, dd, r in out:
    print("     %s  %-22s maxDD90 %6.1f%%  ret90 %s" % (s, v, dd, ("%+.1f%%" % r) if not np.isnan(r) else "n/a"))
print("     -> HIT %d / dinilai %d = %.0f%%" % (hh, hh + mm, 100.0 * hh / max(hh + mm, 1)))

# daily base rate: hari acak di bear window non-censored, zona != Z1
brows = []
for b in bears:
    if b["censored"]:
        continue
    idx = df.index[(df["date"] >= b["peak"]) & (df["date"] <= b["end"])]
    for j in idx:
        if df.at[j, "zone"] == "Z1":
            continue
        d = dates.iloc[j]
        dd, r90, c90 = fwd_stats(j)
        ok = (d >= b["reclaim"] - pd.Timedelta(days=EARLY_TOL)) and (dd > DD_FAIL)
        brows.append((b["cycle"], bool(streak[j] >= SIGD), ok, bool(gap[j] > 0), bool(d >= b["reclaim"])))
bdf = pd.DataFrame(brows, columns=["cycle", "sigD", "hit", "gap_pos", "post_reclaim"])
print("  Base rate HARIAN (setiap hari di bear window selesai, zona != Z1, aturan HIT/MISS yang sama):")
print("     semua hari: n=%d hari, hit %.0f%%" % (len(bdf), 100 * bdf["hit"].mean()))
print("     hari Signal D aktif: n=%d, hit %.0f%% | tidak aktif: n=%d, hit %.0f%%" % (
    int(bdf["sigD"].sum()), 100 * bdf[bdf["sigD"]]["hit"].mean(),
    int((~bdf["sigD"]).sum()), 100 * bdf[~bdf["sigD"]]["hit"].mean()))
print("     per cycle (hit %):", (bdf.groupby("cycle")["hit"].mean() * 100).round(0).to_dict())
st = bdf[bdf["sigD"] & bdf["gap_pos"]]
print("     DESKRIPTIF (bukan uji sinyal) hari dgn state gap momentum > 0 DAN Signal D aktif: n=%d hari, hit %.0f%% | per cycle %s" % (
    len(st), 100 * st["hit"].mean(), (st.groupby("cycle")["hit"].mean() * 100).round(0).to_dict()))
stp = st[~st["post_reclaim"]]
print("       dari n=%d hari itu, %d hari jatuh SETELAH reclaim permanen (trivially HIT). Sebelum reclaim saja: n=%d, hit %.0f%% | per cycle %s" % (
    len(st), int(st["post_reclaim"].sum()), len(stp), 100 * stp["hit"].mean(), (stp.groupby("cycle")["hit"].mean() * 100).round(0).to_dict()))
print("     CATATAN: hari-hari sangat berautokorelasi -> base rate ini deskriptif, bukan n independen.")

# ---------------- mid-cycle 2019-06 s/d 2020-05 ----------------
print("\n" + "=" * 130)
print("WINDOW MID-CYCLE 2019-06-26 s/d 2020-05-01 (analog struktur N, dilaporkan terpisah)")
print("=" * 130)
wm = df[(df["date"] >= "2019-06-26") & (df["date"] <= "2020-05-01")]
mlow = wm.loc[wm["btc_price"].idxmin(), "date"]
mrec = reclaim_after(mlow)
print("  low window = %s ($%s) | reclaim permanen ANALOG (definisi sama) = %s" % (
    mlow.date(), format(float(wm["btc_price"].min()), ",.0f"), mrec.date() if mrec is not None else "n/a"))
M = ev[ev["window"] == "midcycle_2019_20"].copy()
mv = []
for _, r in M.iterrows():
    v, lag = judge(r, mrec, mrec is None)
    mv.append((v, lag))
M["verdict"] = [x[0] for x in mv]
M["lag_vs_reclaim_hari"] = [x[1] for x in mv]
ev.loc[M.index, "verdict"] = M["verdict"]
ev.loc[M.index, "lag_vs_reclaim_hari"] = M["lag_vs_reclaim_hari"]
print(M[["cross_date", "decision_date", "price", "zone_at_gate", "streak_above_sth", "signalD_active",
         "lag_vs_reclaim_hari", "maxdd_90d", "ret_90d", "verdict"]].to_string(index=False))
print("  n=%d | struktur N sepanjang window (0 hari T, findings 08-25)" % len(M))

# ---------------- status sekarang ----------------
print("\n" + "=" * 130)
print("STATUS PER %s" % LAST.date())
print("=" * 130)
print("  gap momentum = %+.5f | zona = %s | streak close>STH RP = %d" % (gap[-1], df.iloc[-1]["zone"], streak[-1]))
cur = ev[ev["cycle"] == "2025"]
print("  bullish cross valid di bear 2025-26:", list(cur["decision_date"]) if len(cur) else "TIDAK ADA",
      "| status:", list(cur["status"]) if len(cur) else "")

out_cols = ["window", "cycle", "cross_date", "decision_date", "price", "sth_rp", "rp", "zone_at_gate",
            "price_gt_sthrp", "streak_above_sth", "signalD_active", "lag_vs_cycle_low_hari",
            "lag_vs_reclaim_hari", "maxdd_90d", "ret_90d", "censored_90d", "verdict", "status"]
ev[out_cols].to_csv(OUTDIR + "/events_bullcross_bear_nonz1.csv", index=False)
print("\nCSV -> events_bullcross_bear_nonz1.csv")
