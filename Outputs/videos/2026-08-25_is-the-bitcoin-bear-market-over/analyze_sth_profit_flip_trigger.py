"""
VALIDASI P1 - sth_profit_flip_trigger
Klaim video (On-Chain Mind, 2026-08-25): flip eksplosif % STH in profit dari
hampir 0 ke >80% adalah pola khas AWAL BULL MARKET.

Definisi event (DIKUNCI SEBELUM MENGHITUNG):
  - Event = hari pertama pct_sth_in_profit > 80, DENGAN syarat dalam 60 hari
    kalender sebelumnya (termasuk hari itu) pernah ada pct_sth_in_profit < 10.
  - Cooldown 180 hari: event berikutnya baru dihitung >=180 hari setelah event
    sebelumnya.
  - Periode: 2010-07-17 s/d hari terakhir data.
  - Semua nilai keputusan diambil AT-GATE (hari event), tidak ada nilai dari
    masa depan window.

Outcome yang diukur (ground truth, forward-looking - hanya untuk skor, bukan gate):
  - Return 90 / 180 / 365 hari ke depan dari close hari event
  - Unlock struktural dalam 180 hari (definisi DF v2 sec.0: STH RP cross NAIK
    melewati RP)
  - False positive: max drawdown (close terendah vs close event) <= -25% dalam
    90 hari

Kondisi tambahan yang diuji (signature KB Supply in Profit sec.1.8):
  - pct_sth_in_profit > pct_lth_in_profit di hari event

Output: events_sth_profit_flip_trigger.csv + print ASCII.
"""

import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-25_is-the-bitcoin-bear-market-over"

LOW_TH = 10.0     # ambang "hampir semua STH rugi"
HIGH_TH = 80.0    # ambang "hampir semua STH untung"
FLIP_WINDOW = 60  # hari maksimum dari <10% ke >80%
COOLDOWN = 180    # hari
DD_TH = -25.0     # false positive threshold

# ---------------- load ----------------
df = pd.read_csv(MASTER, parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 0].dropna(subset=["btc_price", "sth_cost_basis",
                                            "realized_price", "pct_sth_in_profit"]).reset_index(drop=True)
print("Data:", df["date"].min().date(), "s/d", df["date"].max().date(), "| n hari =", len(df))

LAST = df["date"].max()

# ---------------- unlock struktural (DF v2 sec.0) ----------------
# unlock = STH RP cross NAIK melewati RP (dari <= jadi >)
df["struct_N"] = df["sth_cost_basis"] > df["realized_price"]
unlock_dates = []
for i in range(1, len(df)):
    if df.at[i, "struct_N"] and not df.at[i - 1, "struct_N"]:
        unlock_dates.append(df.at[i, "date"])
# hanya unlock "bermakna": didahului >=30 hari berturut struktur T/non-N
unlock_major = []
for d in unlock_dates:
    i = df.index[df["date"] == d][0]
    back = df.loc[max(0, i - 30):i - 1, "struct_N"]
    if len(back) == 30 and (~back).all():
        unlock_major.append(d)
print("\nUNLOCK struktural (STH RP cross naik RP, didahului >=30 hari struktur T):")
for d in unlock_major:
    print("   ", d.date())

# ---------------- deteksi event flip ----------------
vals = df["pct_sth_in_profit"].values
dates = df["date"].values
events = []
last_ev = None
for i in range(len(df)):
    if vals[i] <= HIGH_TH:
        continue
    lo = max(0, i - FLIP_WINDOW)
    window_prev = vals[lo:i + 1]
    if window_prev.min() >= LOW_TH:
        continue
    ev_date = df.at[i, "date"]
    if last_ev is not None and (ev_date - last_ev).days < COOLDOWN:
        continue
    # hari terakhir <10% sebelum flip -> ukur kecepatan flip
    idx_low = lo + int(np.where(window_prev < LOW_TH)[0][-1])
    events.append({
        "idx": i,
        "event_date": ev_date,
        "low_date": df.at[idx_low, "date"],
        "flip_days": (ev_date - df.at[idx_low, "date"]).days,
        "low_pct_sth": round(float(vals[idx_low]), 2),
        "event_pct_sth": round(float(vals[i]), 2),
    })
    last_ev = ev_date

print(f"\nn EVENT FLIP (<{LOW_TH:.0f}% -> >{HIGH_TH:.0f}% dlm <={FLIP_WINDOW}d, cooldown {COOLDOWN}d) = {len(events)}")

# ---------------- cycle labeling ----------------
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

# ---------------- outcome per event ----------------
rows = []
for ev in events:
    i = ev["idx"]
    d = ev["event_date"]
    p0 = float(df.at[i, "btc_price"])

    def fwd_ret(days):
        tgt = d + pd.Timedelta(days=days)
        if tgt > LAST:
            return np.nan
        sub = df[df["date"] <= tgt]
        return round((float(sub.iloc[-1]["btc_price"]) / p0 - 1) * 100, 1)

    win90 = df[(df["date"] > d) & (df["date"] <= d + pd.Timedelta(days=90))]
    if len(win90) > 0:
        dd90 = round((float(win90["btc_price"].min()) / p0 - 1) * 100, 1)
    else:
        dd90 = np.nan
    censored90 = (d + pd.Timedelta(days=90)) > LAST

    # unlock dalam 180 hari sesudah event
    unl = [u for u in unlock_major if d < u <= d + pd.Timedelta(days=180)]
    unlock_180 = unl[0].strftime("%Y-%m-%d") if unl else "TIDAK"
    # apakah event terjadi SETELAH unlock (dalam 180 hari sebelumnya)?
    unl_before = [u for u in unlock_major if d - pd.Timedelta(days=180) <= u <= d]
    unlock_prev = unl_before[-1].strftime("%Y-%m-%d") if unl_before else "-"

    rows.append({
        "cycle": cycle_of(d),
        "event_date": d.strftime("%Y-%m-%d"),
        "low_date": ev["low_date"].strftime("%Y-%m-%d"),
        "flip_days": ev["flip_days"],
        "low_pct_sth": ev["low_pct_sth"],
        "event_pct_sth": ev["event_pct_sth"],
        "price": round(p0, 2),
        "pct_lth_in_profit": round(float(df.at[i, "pct_lth_in_profit"]), 2),
        "sth_gt_lth": bool(df.at[i, "pct_sth_in_profit"] > df.at[i, "pct_lth_in_profit"]),
        "sth_mvrv": round(float(df.at[i, "sth_mvrv"]), 3),
        "struct": "N" if bool(df.at[i, "struct_N"]) else "T",
        "ret_90d": fwd_ret(90),
        "ret_180d": fwd_ret(180),
        "ret_365d": fwd_ret(365),
        "maxdd_90d": dd90,
        "false_pos_dd25": (dd90 <= DD_TH) if not np.isnan(dd90) else np.nan,
        "unlock_dlm_180d": unlock_180,
        "unlock_180d_sebelum": unlock_prev,
        "censored_90d": censored90,
    })

ev_df = pd.DataFrame(rows)
out_csv = OUTDIR + r"\events_sth_profit_flip_trigger.csv"
ev_df.to_csv(out_csv, index=False)

print("\n" + "=" * 118)
print("TABEL EVENT FLIP STH-IN-PROFIT")
print("=" * 118)
hdr = f"{'cyc':<5}{'event':<12}{'low_dt':<12}{'d':>4}{'low%':>7}{'ev%':>7}{'LTH%':>7}{'S>L':>5}{'str':>4}{'r90':>8}{'r180':>8}{'r365':>8}{'dd90':>8}  unlock<=180d"
print(hdr)
print("-" * 118)
for _, r in ev_df.iterrows():
    def f(x):
        return "  n/a" if (isinstance(x, float) and np.isnan(x)) else f"{x:>7.1f}"
    print(f"{r['cycle']:<5}{r['event_date']:<12}{r['low_date']:<12}{r['flip_days']:>4}"
          f"{r['low_pct_sth']:>7.1f}{r['event_pct_sth']:>7.1f}{r['pct_lth_in_profit']:>7.1f}"
          f"{('Y' if r['sth_gt_lth'] else 'N'):>5}{r['struct']:>4}"
          f"{f(r['ret_90d']):>8}{f(r['ret_180d']):>8}{f(r['ret_365d']):>8}{f(r['maxdd_90d']):>8}  {r['unlock_dlm_180d']}")

print("\nSEBARAN PER CYCLE:")
for c, g in ev_df.groupby("cycle"):
    print(f"   cycle {c}: n={len(g)}  tanggal={list(g['event_date'])}")

# ---------------- ringkasan hit / false positive ----------------
val = ev_df[~ev_df["maxdd_90d"].isna()]
hit_unlock = ev_df[ev_df["unlock_dlm_180d"] != "TIDAK"]
fp = val[val["false_pos_dd25"] == True]
print("\n" + "=" * 118)
print("RINGKASAN")
print("=" * 118)
print(f"n total event             = {len(ev_df)}")
print(f"diikuti unlock <=180 hari = {len(hit_unlock)}  ({', '.join(hit_unlock['event_date']) if len(hit_unlock) else '-'})")
print(f"event terjadi SETELAH unlock (unlock <=180d sebelumnya) = "
      f"{int((ev_df['unlock_180d_sebelum'] != '-').sum())}")
print(f"false positive (dd90 <= {DD_TH}%) = {len(fp)} dari {len(val)} yang bisa dinilai"
      f"  ({', '.join(fp['event_date']) if len(fp) else '-'})")
for h in ["ret_90d", "ret_180d", "ret_365d", "maxdd_90d"]:
    s = ev_df[h].dropna()
    if len(s):
        print(f"  {h:<10} median={s.median():>7.1f}%  min={s.min():>7.1f}%  max={s.max():>7.1f}%  (n={len(s)})")

# ---------------- (d) split by sth>lth ----------------
print("\n" + "-" * 118)
print("SPLIT KONDISI TAMBAHAN: pct_sth_in_profit > pct_lth_in_profit (at-gate)")
print("-" * 118)
for flag, g in ev_df.groupby("sth_gt_lth"):
    lab = "STH>LTH (YA)" if flag else "STH<=LTH (TIDAK)"
    fpn = int((g["false_pos_dd25"] == True).sum())
    unl = int((g["unlock_dlm_180d"] != "TIDAK").sum())
    print(f"{lab:<18} n={len(g):<3} false_pos={fpn:<3} unlock<=180d={unl:<3} "
          f"median r90={g['ret_90d'].median():.1f}% median r365={g['ret_365d'].median():.1f}%")
    print(f"                   tanggal: {list(g['event_date'])}")


# ---------------- split by STRUKTUR at-gate (temuan tak terduga) ----------------
print()
print("-" * 118)
print("SPLIT STRUKTUR at-gate (N = STH RP > RP ; T = STH RP < RP)")
print("-" * 118)
for st, g in ev_df.groupby("struct"):
    fpn = int((g["false_pos_dd25"] == True).sum())
    unl = int((g["unlock_dlm_180d"] != "TIDAK").sum())
    print(f"  struktur {st}: n={len(g)}  unlock<=180d={unl}  false_pos={fpn}  "
          f"median r90={g['ret_90d'].median():.1f}%  median r365={g['ret_365d'].median():.1f}%")
    print(f"     tanggal: {list(g['event_date'])}")
    print(f"     r365 per event: {list(zip(g['event_date'], g['ret_365d']))}")

# ---------------- varian sensitivitas (dibatasi 3) ----------------
print("\n" + "-" * 118)
print("SENSITIVITAS (3 varian saja - bukan grid search, hanya cek kerapuhan definisi)")
print("-" * 118)


def count_events(low_th, high_th, win, cool=COOLDOWN):
    out = []
    last = None
    for i in range(len(df)):
        if vals[i] <= high_th:
            continue
        lo = max(0, i - win)
        if vals[lo:i + 1].min() >= low_th:
            continue
        dte = df.at[i, "date"]
        if last is not None and (dte - last).days < cool:
            continue
        out.append(dte)
        last = dte
    return out


for (lo_, hi_, w_) in [(5.0, 80.0, 60), (10.0, 80.0, 90), (10.0, 90.0, 60)]:
    ds = count_events(lo_, hi_, w_)
    print(f"  <{lo_:.0f}% -> >{hi_:.0f}% dlm <={w_}d : n={len(ds)} -> {[x.strftime('%Y-%m-%d') for x in ds]}")

# ---------------- STATE CHECK hari terakhir ----------------
last_row = df.iloc[-1]
print("\n" + "=" * 118)
print(f"STATE CHECK - hari terakhir data ({LAST.date()})")
print("=" * 118)
for c in ["btc_price", "sth_mvrv", "pct_sth_in_profit", "pct_lth_in_profit",
          "percent_btc_in_profit", "sth_cost_basis", "realized_price",
          "true_market_mean_price", "lth_cost_basis", "price_at_aviv_mean", "cvdd"]:
    if c in df.columns:
        print(f"  {c:<26} = {float(last_row[c]):,.4f}")
print(f"  struktur                   = {'N (STH RP > RP)' if bool(last_row['struct_N']) else 'T (STH RP < RP)'}")
print(f"  price vs STH RP            = {float(last_row['btc_price'])/float(last_row['sth_cost_basis'])*100:.1f}% dari STH RP")
# berapa lama pct_sth_in_profit terakhir < 10?
below10 = df[df["pct_sth_in_profit"] < LOW_TH]
print(f"  terakhir pct_sth_in_profit < {LOW_TH:.0f}%  = "
      f"{below10['date'].max().date() if len(below10) else 'never'}")
print(f"  min pct_sth_in_profit 180 hari terakhir = "
      f"{df[df['date'] > LAST - pd.Timedelta(days=180)]['pct_sth_in_profit'].min():.1f}%")
print(f"\nCSV -> {out_csv}")
