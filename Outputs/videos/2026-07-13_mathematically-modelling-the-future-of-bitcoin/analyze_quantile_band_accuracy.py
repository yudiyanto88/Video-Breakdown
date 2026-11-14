"""
INSIGHT 2: Quantile bands (5th/95th percentile of MVRV Ratio) klaim akurat "practically
to perfection" sepanjang sejarah BTC, termasuk out-of-sample (training dibatasi ke 2015/2019/2023).

Proxy dipakai (BUKAN re-implementasi fungsi decay eksponensial pembicara): band persentil
5/95 dari MVRV Ratio, dihitung HANYA dari data sampai TRAIN_CUTOFF (expanding window yang
BERHENTI di cutoff, tidak diupdate lagi sesudahnya -- ini genuine out-of-sample test, sama
semangat dengan yang diklaim pembicara). Breach = mvrv_ratio(t) forward < band_low ATAU
> band_high.

STANDAR VALIDASI:
1. Definisi event: breach = 1 hari kalender di mana mvrv_ratio ada di luar band [P5,P95]
   yang di-fit HANYA dari data <= cutoff. Tidak ada merge/cooldown -- breach dihitung per hari
   mentah karena klaimnya soal "akurasi band", bukan soal sinyal diskrit.
2. n dilaporkan: total hari forward-period, total hari breach, breakdown per cycle (era
   antar-halving) dan breakdown khusus sekitar bear low Nov 2022 & window 2025-2026 (current).
3. Anti-lookahead: band dihitung SEKALI dari data <= cutoff, TIDAK diupdate/expanding sesudah
   cutoff. ini exact requirement rule 3 (data untuk 'keputusan' harus tersedia di tanggal keputusan).
4. Independensi: breach hari-hari berdekatan (mis. selama satu bear-low episode) sangat
   berkorelasi -- dihitung juga jumlah EPISODE breach (breach yang delimited oleh gap >=14 hari
   non-breach) supaya tidak overcount satu episode capitulation sebagai puluhan "kejadian".
5. Data mvrv_ratio full history sejak 2010-07-17 -- tidak ada isu start-date terlambat.
6. Varian yang diuji cuma 3 (cutoff 2015/2019/2023, sesuai yang disebut pembicara sendiri di
   video) + 1 in-sample full-history sbg baseline pembanding -- bukan puluhan cutoff untuk
   cherry-pick yang "berhasil".
"""

import pandas as pd
import numpy as np

df = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_mvrv.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["mvrv_ratio"]).reset_index(drop=True)

CUTOFFS = ["2015-01-01", "2019-01-01", "2023-01-01"]
EPISODE_GAP_DAYS = 14  # gap non-breach minimal untuk memisahkan episode breach

HALVINGS = [
    ("Cycle 2010-2012", "2009-01-03", "2012-11-28"),
    ("Cycle 2012-2016", "2012-11-28", "2016-07-09"),
    ("Cycle 2016-2020", "2016-07-09", "2020-05-11"),
    ("Cycle 2020-2024", "2020-05-11", "2024-04-20"),
    ("Cycle 2024-now",  "2024-04-20", "2100-01-01"),
]

def cycle_label(date):
    for name, start, end in HALVINGS:
        if pd.Timestamp(start) <= date < pd.Timestamp(end):
            return name
    return "?"

def episodes_from_breach(sub):
    """sub: dataframe with date, breach(bool) sorted by date. Return list of (start,end,n_days)."""
    eps = []
    cur_start = None
    last_breach_date = None
    for _, row in sub.iterrows():
        if row["breach"]:
            if cur_start is None:
                cur_start = row["date"]
            last_breach_date = row["date"]
        else:
            if cur_start is not None and (row["date"] - last_breach_date).days > EPISODE_GAP_DAYS:
                eps.append((cur_start, last_breach_date))
                cur_start = None
    if cur_start is not None:
        eps.append((cur_start, last_breach_date))
    return eps

print("=" * 100)
print("INSIGHT 2: Quantile band (P5/P95 MVRV Ratio) out-of-sample breach test")
print("=" * 100)

all_events_rows = []

for cutoff_str in CUTOFFS:
    cutoff = pd.Timestamp(cutoff_str)
    train = df[df["date"] <= cutoff]
    band_low  = train["mvrv_ratio"].quantile(0.05)
    band_high = train["mvrv_ratio"].quantile(0.95)

    forward = df[df["date"] > cutoff].copy()
    forward["breach"] = (forward["mvrv_ratio"] < band_low) | (forward["mvrv_ratio"] > band_high)
    forward["breach_low"]  = forward["mvrv_ratio"] < band_low
    forward["breach_high"] = forward["mvrv_ratio"] > band_high
    forward["cycle"] = forward["date"].apply(cycle_label)

    n_total  = len(forward)
    n_breach = int(forward["breach"].sum())
    pct = 100 * n_breach / n_total if n_total else float("nan")

    print(f"\n--- Train cutoff: {cutoff_str} (n_train={len(train)} hari, band P5={band_low:.3f}, P95={band_high:.3f}) ---")
    print(f"Forward period: {forward['date'].min().date()} s/d {forward['date'].max().date()}  (n_total={n_total} hari)")
    print(f"Breach hari (raw)     : {n_breach} / {n_total}  ({pct:.2f}%)")
    print(f"  breach LOW (< P5)   : {int(forward['breach_low'].sum())} hari")
    print(f"  breach HIGH (> P95) : {int(forward['breach_high'].sum())} hari")

    # per cycle breakdown
    print("  Breakdown per cycle (hari forward yang termasuk cycle itu, breach count):")
    for name, start, end in HALVINGS:
        seg = forward[forward["cycle"] == name]
        if len(seg) == 0:
            continue
        print(f"    {name:<18}: n={len(seg):>5}  breach={int(seg['breach'].sum()):>4}  ({100*seg['breach'].mean():.1f}%)")

    # episodes (independence check)
    eps = episodes_from_breach(forward[["date", "breach"]])
    print(f"  n episode breach (gap>{EPISODE_GAP_DAYS}d) = {len(eps)}")
    for s, e in eps:
        dur = (e - s).days + 1
        print(f"    {s.date()} -> {e.date()}  ({dur}d)")
        all_events_rows.append({"cutoff": cutoff_str, "episode_start": s.date(), "episode_end": e.date(), "duration_days": dur})

    # Specific windows of interest
    bear_low_2022 = forward[(forward["date"] >= "2022-10-01") & (forward["date"] <= "2022-12-31")]
    if len(bear_low_2022) > 0:
        print(f"  [Fokus] Okt-Des 2022 (sekitar bear low): n={len(bear_low_2022)}, breach={int(bear_low_2022['breach'].sum())} "
              f"({100*bear_low_2022['breach'].mean():.1f}%), min mvrv_ratio={bear_low_2022['mvrv_ratio'].min():.3f} vs band_low={band_low:.3f}")

    window_2025_26 = forward[(forward["date"] >= "2025-01-01")]
    if len(window_2025_26) > 0:
        print(f"  [Fokus] 2025-2026 (s/d data terakhir): n={len(window_2025_26)}, breach={int(window_2025_26['breach'].sum())} "
              f"({100*window_2025_26['breach'].mean():.1f}%), min mvrv_ratio={window_2025_26['mvrv_ratio'].min():.3f}, "
              f"max mvrv_ratio={window_2025_26['mvrv_ratio'].max():.3f} vs band=[{band_low:.3f},{band_high:.3f}]")

# ─── In-sample (full history) baseline -- reference only, NOT a valid out-of-sample test ───
band_low_full  = df["mvrv_ratio"].quantile(0.05)
band_high_full = df["mvrv_ratio"].quantile(0.95)
print(f"\n--- Baseline in-sample (full history, TIDAK valid sbg test -- band dihitung dari SEMUA data termasuk masa depan) ---")
print(f"Band P5={band_low_full:.3f}, P95={band_high_full:.3f}")
last_row = df.iloc[-1]
print(f"Data terakhir ({last_row['date'].date()}): mvrv_ratio={last_row['mvrv_ratio']:.3f}")
print(f"  Apakah di bawah P5 in-sample? {'YA' if last_row['mvrv_ratio'] < band_low_full else 'TIDAK'}")

pd.DataFrame(all_events_rows).to_csv(
    r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-07-13_mathematically-modelling-the-future-of-bitcoin\events_quantile_band_breach.csv",
    index=False
)
print("\nSaved events_quantile_band_breach.csv")
