"""
VALIDASI P2 - unlock_reachability_struktur_n

Gap yang diuji: DF v2 sec.0 mendefinisikan "status bear berakhir (unlock)" =
STH RP cross NAIK melewati RP. Cross itu hanya mungkin secara mekanis kalau
sebelumnya STH RP ADA DI BAWAH RP (struktur T). Kalau sepanjang bear struktur
tetap N (STH RP > RP), unlock formal TIDAK PERNAH bisa terjadi -> K5 tidak
bisa start.

(a) Berapa bear yang struktur N-nya tidak pernah putus (tidak pernah T)?
(b) Kapan bear "sebenarnya" berakhir (cycle low + reclaim permanen), dan berapa
    jauh dari sinyal unlock formal?
(c) Uji 3 kandidat unlock pengganti (at-gate, TIDAK ADA grid search):
      (i)   close > sth_cost_basis >=21 hari berturut
      (ii)  close > sth_cost_basis >=3 hari DAN slope 30-hari sth_cost_basis > 0
      (iii) (i) DAN close > 200_dma di hari sinyal

Definisi ground truth (dikunci sebelum menghitung):
  - Cycle peak: dari daftar peak siklus (rolling-max terverifikasi di bawah)
  - Cycle low  : harga close terendah antara peak dan peak berikutnya
  - "Bear sebenarnya berakhir" = RECLAIM PERMANEN = hari pertama SETELAH cycle
    low di mana close > sth_cost_basis DAN price bertahan di atas sth_cost_basis
    90 hari berturut sesudahnya. (forward-looking - dipakai HANYA sebagai label
    kebenaran, bukan sebagai gate)
  - Sinyal kandidat: at-gate murni (semua input tersedia di hari sinyal),
    cooldown 180 hari
  - Sinyal dinilai di dalam bear window (peak -> reclaim permanen + 60 hari)
      HIT  = sinyal muncul >= (reclaim_permanen - 30 hari) DAN dalam 90 hari
             sesudahnya harga tidak turun >=20% dari harga sinyal
      MISS = selain itu (kepagian / diikuti drawdown >=20%)
"""

import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-25_is-the-bitcoin-bear-market-over"

COOLDOWN = 180
DD_FAIL = -20.0
EARLY_TOL = 30   # hari toleransi "tidak kepagian"

df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "sth_cost_basis", "realized_price", "200_dma"]).reset_index(drop=True)
df = df[df["btc_price"] > 0].reset_index(drop=True)
LAST = df["date"].max()
print("Data:", df["date"].min().date(), "s/d", LAST.date(), "| n hari =", len(df))

df["struct_T"] = df["sth_cost_basis"] < df["realized_price"]
df["ratio_sthrp_rp"] = df["sth_cost_basis"] / df["realized_price"]

PEAKS = ["2011-06-08", "2013-11-29", "2017-12-16", "2021-11-08", "2025-10-06"]
PEAKS = [pd.Timestamp(p) for p in PEAKS]
CYCLE_NAME = ["2011", "2013", "2017", "2021", "2025"]

# ---------- verifikasi peak = rolling max lokal ----------
print("\nVerifikasi cycle peak (harga close di tanggal peak vs max 180 hari sekitarnya):")
for nm, p in zip(CYCLE_NAME, PEAKS):
    w = df[(df["date"] >= p - pd.Timedelta(days=180)) & (df["date"] <= p + pd.Timedelta(days=180))]
    row = df[df["date"] == p]
    if len(row) and len(w):
        print(f"  {nm}: {p.date()} close=${float(row.iloc[0]['btc_price']):,.0f} | "
              f"max +-180d=${float(w['btc_price'].max()):,.0f} ({'OK' if abs(float(row.iloc[0]['btc_price'])-float(w['btc_price'].max()))<1e-6 else 'CEK'})")

# ---------- cycle low & reclaim permanen ----------
bears = []
for i, (nm, p) in enumerate(zip(CYCLE_NAME, PEAKS)):
    end_search = PEAKS[i + 1] if i + 1 < len(PEAKS) else LAST
    seg = df[(df["date"] > p) & (df["date"] <= end_search)]
    if len(seg) == 0:
        continue
    low_idx = seg["btc_price"].idxmin()
    low_date = df.at[low_idx, "date"]
    low_price = float(df.at[low_idx, "btc_price"])

    # reclaim permanen: close > sth_cost_basis, lalu 90 hari berturut tetap di atas
    reclaim = None
    post = df[df["date"] > low_date].reset_index(drop=True)
    above = (post["btc_price"] > post["sth_cost_basis"]).values
    for j in range(len(post) - 90):
        if above[j] and above[j:j + 90].all():
            reclaim = post.at[j, "date"]
            break
    censored = reclaim is None

    win = df[(df["date"] >= p) & (df["date"] <= (reclaim if reclaim is not None else LAST))]
    n_T = int(win["struct_T"].sum())
    T_dates = win[win["struct_T"]]["date"]
    bears.append({
        "cycle": nm, "peak": p, "low_date": low_date, "low_price": low_price,
        "reclaim": reclaim, "censored": censored,
        "bear_days": len(win), "n_struct_T": n_T,
        "T_first": T_dates.min() if n_T else None,
        "T_last": T_dates.max() if n_T else None,
        "min_ratio": float(win["ratio_sthrp_rp"].min()),
        "min_ratio_date": win.loc[win["ratio_sthrp_rp"].idxmin(), "date"],
    })

print("\n" + "=" * 118)
print("(a) APAKAH STRUKTUR PERNAH TERBALIK (T) DI SETIAP BEAR?")
print("=" * 118)
print(f"{'cyc':<6}{'peak':<12}{'cycle low':<12}{'reclaim permanen':<18}{'hari bear':>10}{'hari T':>8}{'%T':>7}"
      f"{'min STHRP/RP':>14}  (tgl min)")
print("-" * 118)
for b in bears:
    rc = b["reclaim"].strftime("%Y-%m-%d") if b["reclaim"] is not None else "BELUM (censored)"
    pct = 100.0 * b["n_struct_T"] / b["bear_days"]
    print(f"{b['cycle']:<6}{b['peak'].strftime('%Y-%m-%d'):<12}{b['low_date'].strftime('%Y-%m-%d'):<12}"
          f"{rc:<18}{b['bear_days']:>10}{b['n_struct_T']:>8}{pct:>6.1f}%{b['min_ratio']:>14.3f}"
          f"  {b['min_ratio_date'].strftime('%Y-%m-%d')}")

never_T = [b for b in bears if b["n_struct_T"] == 0]
print(f"\n>> Bear yang struktur N-nya TIDAK PERNAH putus (0 hari T): n={len(never_T)} dari {len(bears)}"
      f"  -> {[b['cycle'] for b in never_T]}")
for b in bears:
    if b["n_struct_T"] > 0:
        print(f"   cycle {b['cycle']}: periode T {b['T_first'].date()} s/d {b['T_last'].date()}")

# ---------- (b) jarak sinyal unlock formal vs bear end ----------
df["struct_N"] = ~df["struct_T"]
unlock_formal = []
for i in range(1, len(df)):
    if df.at[i, "struct_N"] and df.at[i - 1, "struct_T"]:
        back = df.loc[max(0, i - 30):i - 1, "struct_T"]
        if len(back) == 30 and back.all():
            unlock_formal.append(df.at[i, "date"])

print("\n" + "=" * 118)
print("(b) SINYAL UNLOCK FORMAL (DF v2) vs BEAR END SEBENARNYA")
print("=" * 118)
print(f"Unlock formal terdeteksi: {[d.strftime('%Y-%m-%d') for d in unlock_formal]}")
print(f"\n{'cyc':<6}{'cycle low':<12}{'reclaim permanen':<18}{'unlock formal':<16}{'lag unlock-reclaim':>20}")
print("-" * 118)
for b in bears:
    u = [x for x in unlock_formal if b["peak"] <= x <= (b["reclaim"] + pd.Timedelta(days=200) if b["reclaim"] is not None else LAST)]
    us = u[0].strftime("%Y-%m-%d") if u else "TIDAK ADA"
    if u and b["reclaim"] is not None:
        lag = (u[0] - b["reclaim"]).days
        lags = f"{lag:+d} hari"
    else:
        lags = "n/a"
    rc = b["reclaim"].strftime("%Y-%m-%d") if b["reclaim"] is not None else "BELUM"
    print(f"{b['cycle']:<6}{b['low_date'].strftime('%Y-%m-%d'):<12}{rc:<18}{us:<16}{lags:>20}")

# ---------- (c) 3 kandidat unlock pengganti ----------
close = df["btc_price"].values
sthrp = df["sth_cost_basis"].values
dma200 = df["200_dma"].values
above_sth = close > sthrp

streak = np.zeros(len(df), dtype=int)
for i in range(len(df)):
    streak[i] = streak[i - 1] + 1 if (i > 0 and above_sth[i]) else (1 if above_sth[i] else 0)
df["streak_above_sth"] = streak

# slope 30 hari sth_cost_basis, at-gate (pakai data s/d hari ini saja)
df["sth_slope30"] = df["sth_cost_basis"] - df["sth_cost_basis"].shift(30)

cand = {
    "(i)   close>STH RP >=21 hari": (streak == 21),
    "(ii)  close>STH RP >=3 hari & slope30 STH RP > 0": (streak == 3) & (df["sth_slope30"].values > 0),
    "(iii) (i) DAN close > 200DMA": (streak == 21) & (close > dma200),
}


def apply_cooldown(mask):
    out = []
    last = None
    for i in np.where(mask)[0]:
        d = df.at[i, "date"]
        if last is not None and (d - last).days < COOLDOWN:
            continue
        out.append(i)
        last = d
    return out


def cycle_of(d):
    if d < pd.Timestamp("2012-01-01"):
        return "2011"
    if d < pd.Timestamp("2016-01-01"):
        return "2013"
    if d < pd.Timestamp("2020-01-01"):
        return "2017"
    if d < pd.Timestamp("2024-01-01"):
        return "2021"
    return "2025"


rows = []
print("\n" + "=" * 118)
print("(c) 3 KANDIDAT UNLOCK PENGGANTI - hanya sinyal DI DALAM bear window yang dinilai")
print("=" * 118)
for name, mask in cand.items():
    idxs = apply_cooldown(mask)
    print(f"\n--- {name} ---")
    print(f"    total sinyal seluruh sejarah (cooldown {COOLDOWN}d) = {len(idxs)}")
    hits = miss = 0
    detail = []
    for i in idxs:
        d = df.at[i, "date"]
        p0 = float(close[i])
        # apakah di dalam bear window?
        bw = None
        for b in bears:
            end = (b["reclaim"] + pd.Timedelta(days=60)) if b["reclaim"] is not None else LAST
            if b["peak"] <= d <= end:
                bw = b
                break
        if bw is None:
            continue
        w90 = df[(df["date"] > d) & (df["date"] <= d + pd.Timedelta(days=90))]
        dd = round((float(w90["btc_price"].min()) / p0 - 1) * 100, 1) if len(w90) else np.nan
        cens = (d + pd.Timedelta(days=90)) > LAST
        if bw["reclaim"] is not None:
            not_early = d >= bw["reclaim"] - pd.Timedelta(days=EARLY_TOL)
            lead = (d - bw["reclaim"]).days
        else:
            not_early = None
            lead = None
        ok = (not_early is True) and (not np.isnan(dd)) and (dd > DD_FAIL)
        if bw["censored"]:
            verdict = "CENSORED"
        elif ok:
            verdict = "HIT"
            hits += 1
        else:
            verdict = "MISS"
            miss += 1
        r90 = np.nan
        if d + pd.Timedelta(days=90) <= LAST:
            r90 = round((float(df[df["date"] <= d + pd.Timedelta(days=90)].iloc[-1]["btc_price"]) / p0 - 1) * 100, 1)
        detail.append((bw["cycle"], d.strftime("%Y-%m-%d"), p0, lead, dd, r90, verdict, cens))
        rows.append({"kandidat": name, "cycle": bw["cycle"], "signal_date": d.strftime("%Y-%m-%d"),
                     "price": round(p0, 2), "lag_vs_reclaim_hari": lead, "maxdd_90d": dd,
                     "ret_90d": r90, "verdict": verdict, "censored_90d": cens})
    print(f"    {'cyc':<6}{'sinyal':<12}{'harga':>12}{'lag vs reclaim':>16}{'dd90':>8}{'ret90':>8}  verdict")
    for c_, d_, p_, l_, dd_, r_, v_, cn_ in detail:
        ls = f"{l_:+d}d" if l_ is not None else "n/a"
        print(f"    {c_:<6}{d_:<12}{p_:>12,.0f}{ls:>16}{dd_:>8.1f}{(r_ if not np.isnan(r_) else float('nan')):>8.1f}  {v_}"
              + ("  [90d censored]" if cn_ else ""))
    per_cycle = {}
    for c_, *_ in detail:
        per_cycle[c_] = per_cycle.get(c_, 0) + 1
    tot = hits + miss
    hr = f"{100.0*hits/tot:.0f}%" if tot else "n/a"
    print(f"    >> di bear window: n={len(detail)} (dinilai {tot}, censored {len(detail)-tot}) | "
          f"HIT={hits} MISS={miss} | hit rate={hr}")
    print(f"    >> sebaran per cycle: {per_cycle}")

pd.DataFrame(rows).to_csv(OUTDIR + r"\events_unlock_reachability_struktur_n.csv", index=False)

# ---------- state 2025-26 ----------
b25 = [b for b in bears if b["cycle"] == "2025"][0]
w = df[df["date"] >= b25["peak"]]
print("\n" + "=" * 118)
print("STATE BEAR 2025-26 (s/d hari terakhir data)")
print("=" * 118)
print(f"  peak {b25['peak'].date()} -> {LAST.date()} = {len(w)} hari")
print(f"  hari struktur T = {int(w['struct_T'].sum())}")
print(f"  min STH RP / RP = {float(w['ratio_sthrp_rp'].min()):.3f} pada {w.loc[w['ratio_sthrp_rp'].idxmin(),'date'].date()}")
print(f"  STH RP / RP hari terakhir = {float(w.iloc[-1]['ratio_sthrp_rp']):.3f}")
print(f"  streak close>STH RP hari terakhir = {int(df.iloc[-1]['streak_above_sth'])} hari")
print(f"  slope30 STH RP hari terakhir = {float(df.iloc[-1]['sth_slope30']):,.0f} USD")
print(f"  close vs 200DMA = {float(df.iloc[-1]['btc_price']):,.0f} vs {float(df.iloc[-1]['200_dma']):,.0f}")
print(f"\nCSV -> {OUTDIR}\\events_unlock_reachability_struktur_n.csv")

# ================= SUPLEMEN 1: window mid-cycle 2019-2020 =================
# Bukan bear siklus penuh (peak 2019-06-26 ~$13k -> crash Mar 2020), tapi
# ditanyakan eksplisit apakah struktur N-nya juga tidak pernah putus.
print()
print("=" * 118)
print("SUPLEMEN 1 - WINDOW MID-CYCLE 2019-06-26 s/d 2020-05-01 (bukan bear siklus penuh)")
print("=" * 118)
w19 = df[(df["date"] >= pd.Timestamp("2019-06-26")) & (df["date"] <= pd.Timestamp("2020-05-01"))]
print(f"  n hari = {len(w19)} | hari struktur T = {int(w19['struct_T'].sum())}")
print(f"  min STH RP / RP = {float(w19['ratio_sthrp_rp'].min()):.3f} pada "
      f"{w19.loc[w19['ratio_sthrp_rp'].idxmin(),'date'].date()}")
print(f"  harga terendah = {float(w19['btc_price'].min()):,.0f} pada "
      f"{w19.loc[w19['btc_price'].idxmin(),'date'].date()}")
print("  -> unlock formal (STH RP cross naik RP) di window ini: "
      f"{[d.strftime('%Y-%m-%d') for d in unlock_formal if pd.Timestamp('2019-06-26') <= d <= pd.Timestamp('2020-05-01')] or 'TIDAK ADA'}")

# ================= SUPLEMEN 2: kandidat (i) vs unlock formal per cycle =================
print()
print("=" * 118)
print("SUPLEMEN 2 - KANDIDAT (i) [close>STH RP >=21 hari] vs UNLOCK FORMAL, sinyal TERAKHIR di tiap bear")
print("=" * 118)
idx_i = apply_cooldown(cand["(i)   close>STH RP >=21 hari"])
print(f"  {'cyc':<6}{'sinyal (i) terakhir':<22}{'unlock formal':<16}{'selisih (i) - formal':>22}")
for b in bears:
    end = (b["reclaim"] + pd.Timedelta(days=60)) if b["reclaim"] is not None else LAST
    sigs = [df.at[i, "date"] for i in idx_i if b["peak"] <= df.at[i, "date"] <= end]
    u = [x for x in unlock_formal if b["peak"] <= x <= (end + pd.Timedelta(days=200))]
    s_last = sigs[-1].strftime("%Y-%m-%d") if sigs else "TIDAK ADA"
    u_s = u[0].strftime("%Y-%m-%d") if u else "TIDAK ADA"
    dlt = f"{(sigs[-1]-u[0]).days:+d} hari" if (sigs and u) else "n/a"
    print(f"  {b['cycle']:<6}{s_last:<22}{u_s:<16}{dlt:>22}")
