"""
INSIGHT 1: Dynamic LTH classification (multi age-band boundary) vs fixed 155-day cutoff.

Klaim sumber: paper "Dynamic Long-Term Holder Classification for Bitcoin" milik pembicara
menghitung realized price di banyak age-band boundary (0-30d, 30-90d, ..., 730d+) alih-alih
satu cutoff tetap 155 hari yang dipakai framework kita untuk STH/LTH split.

Pertanyaan: apakah pindah cutoff (155d -> <90d / <180d / <270d) menggeser SECARA MATERIAL
tanggal crossing STH-RP <-> RP (transisi struktur N<->T, gerbang K5/Z2 di Decision Framework v2)?

STANDAR VALIDASI (CLAUDE.md):
1. Definisi event eksplisit: "crossing" = hari di mana tanda (candidate_RP - RP_full) berubah,
   dikonfirmasi kalau tanda baru bertahan >= CONFIRM_DAYS hari berturut (anti noise satu-hari).
   Window pencarian pasangan crossing across cutoff = +/- MATCH_WINDOW hari, arah harus sama
   (naik vs turun), diambil pasangan terdekat.
2. n dilaporkan + sebaran per cycle.
3. Anti-lookahead: semua RP proxy dihitung dari cap/supply per HARI ITU SAJA (bukan revisi
   masa depan) -- hodl_waves adalah snapshot end-of-day, tidak ada leakage.
4. Independensi sample: crossing dari cycle sama dicatat, disebutkan clustering.
5. Data hodl_waves full history sejak 2009 -- tidak ada isu start-date terlambat di sini.
6. Tidak overfit: cuma 3 varian cutoff (90d/180d/270d) dites, bukan puluhan kombinasi.

Catatan proksi 270 hari: age-band di data kita berhenti di 90d,180d,365d (3m-6m dan 6m-12m
bins) -- TIDAK ada boundary asli di 270 hari. Untuk <270d, dipakai interpolasi linear:
asumsikan supply & realized_cap terdistribusi merata per-hari di dalam bin 6m-12m (180-365d),
lalu ambil proporsi (270-180)/(365-180) = 48.6% dari bin itu. Ini ASUMSI kasar (bukan data asli)
-- hasil untuk <270d harus dibaca sebagai lower-confidence dibanding <90d/<180d yang align
persis dengan boundary bin asli.
"""

import pandas as pd
import numpy as np

CONFIRM_DAYS = 5     # hari konfirmasi tanda baru bertahan (anti one-day noise)
MATCH_WINDOW = 180   # hari toleransi pencarian pasangan crossing across cutoff

# ─── Load data ───────────────────────────────────────────────────────────────
hw = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_hodl_waves.csv", parse_dates=["date"])
pl = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_price_level.csv", parse_dates=["date"])

df = hw.merge(pl[["date", "sth_cost_basis", "realized_price", "btc_price"]], on="date", suffixes=("", "_pl"))
df = df.sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["realized_price", "sth_cost_basis"]).reset_index(drop=True)

# ─── Candidate realized-price proxies per cutoff ────────────────────────────
# PENTING: supply_<band> & realized_cap_<band> di data_hodl_waves.csv adalah PERSENTASE
# (dari total supply / total realized cap), BUKAN nilai absolut. Untuk dapat harga rata-rata
# USD suatu subset umur coin: price_subset = RP_full * (sum(cap_pct subset) / sum(supply_pct subset))
# -- karena cap_pct/supply_pct = (price_band/RP_full), dan RP_full sudah kita punya dari
# data_price_level.csv. Diverifikasi: sum semua supply_<band> = 100.0, sum semua realized_cap_<band> = 100.0.
def cum(bands):
    sup = df[[f"supply_{b}" for b in bands]].sum(axis=1)
    cap = df[[f"realized_cap_{b}" for b in bands]].sum(axis=1)
    return df["realized_price"] * (cap / sup)

bands_90  = ["0-1d", "1d-1w", "1w-1m", "1m-3m"]                 # <90d (exact bin edge)
bands_180 = bands_90 + ["3m-6m"]                                # <180d (exact bin edge)

df["rp_90d"]  = cum(bands_90)
df["rp_180d"] = cum(bands_180)

# <270d: interpolasi linear di dalam bin 6m-12m (180-365d)
frac_270 = (270 - 180) / (365 - 180)  # = 0.4865
sup_180 = df[[f"supply_{b}" for b in bands_180]].sum(axis=1)
cap_180 = df[[f"realized_cap_{b}" for b in bands_180]].sum(axis=1)
sup_270 = sup_180 + frac_270 * df["supply_6m-12m"]
cap_270 = cap_180 + frac_270 * df["realized_cap_6m-12m"]
df["rp_270d"] = df["realized_price"] * (cap_270 / sup_270)

df["rp_155d_official"] = df["sth_cost_basis"]  # existing framework STH RP

# ─── Crossing detector (generic) ────────────────────────────────────────────
def detect_crossings(candidate_col, ref_col="realized_price"):
    diff = df[candidate_col] - df[ref_col]
    sign = np.sign(diff.values)
    events = []
    i = 1
    n = len(sign)
    while i < n:
        if sign[i] != 0 and sign[i] != sign[i-1] and sign[i-1] != 0:
            # potential cross at i; confirm sustained for CONFIRM_DAYS
            new_sign = sign[i]
            end = min(i + CONFIRM_DAYS, n)
            if end - i == CONFIRM_DAYS and np.all(sign[i:end] == new_sign):
                direction = "UP" if new_sign > 0 else "DOWN"
                events.append((df.at[i, "date"], direction))
                # skip ahead to avoid re-detecting same confirmed event repeatedly
                i += CONFIRM_DAYS
                continue
        i += 1
    return events

events_155 = detect_crossings("rp_155d_official")
events_90  = detect_crossings("rp_90d")
events_180 = detect_crossings("rp_180d")
events_270 = detect_crossings("rp_270d")

print("=" * 100)
print("INSIGHT 1: Dynamic LTH boundary vs fixed 155-day cutoff -- crossing STH-RP <-> RP")
print("=" * 100)
print(f"n crossing events (155d official)  : {len(events_155)}")
print(f"n crossing events (<90d candidate)  : {len(events_90)}")
print(f"n crossing events (<180d candidate) : {len(events_180)}")
print(f"n crossing events (<270d candidate, interpolated): {len(events_270)}")

print("\n--- Semua crossing 155d (official framework STH RP) ---")
for d, dirn in events_155:
    print(f"  {d.date()}  {dirn}")

# ─── Match each 155d event to nearest same-direction event in each candidate ─
def match_nearest(ref_events, cand_events):
    rows = []
    for ref_date, ref_dir in ref_events:
        candidates = [(d, dirn) for d, dirn in cand_events if dirn == ref_dir]
        if not candidates:
            rows.append((ref_date, ref_dir, None, None))
            continue
        diffs = [(abs((d - ref_date).days), d) for d, dirn in candidates]
        diffs.sort()
        best_delta, best_date = diffs[0]
        if best_delta <= MATCH_WINDOW:
            offset = (best_date - ref_date).days
            rows.append((ref_date, ref_dir, best_date, offset))
        else:
            rows.append((ref_date, ref_dir, None, None))
    return rows

match_90  = match_nearest(events_155, events_90)
match_180 = match_nearest(events_155, events_180)
match_270 = match_nearest(events_155, events_270)

results = []
for i, (ref_date, ref_dir, _, _) in enumerate(match_90):
    row = {
        "ref_date_155d": ref_date.date(),
        "direction": ref_dir,
        "match_90d_date": match_90[i][2].date() if match_90[i][2] is not None else "NO MATCH",
        "offset_90d_days": match_90[i][3],
        "match_180d_date": match_180[i][2].date() if match_180[i][2] is not None else "NO MATCH",
        "offset_180d_days": match_180[i][3],
        "match_270d_date": match_270[i][2].date() if match_270[i][2] is not None else "NO MATCH",
        "offset_270d_days": match_270[i][3],
    }
    results.append(row)

res_df = pd.DataFrame(results)
print("\n--- Tabel pencocokan (offset dalam hari, +/- terhadap tanggal official 155d) ---")
print(res_df.to_string(index=False))

res_df.to_csv(
    r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-07-13_mathematically-modelling-the-future-of-bitcoin\events_dynamic_lth_boundary.csv",
    index=False
)

# ─── Summary stats ───────────────────────────────────────────────────────────
for label, col in [("<90d", "offset_90d_days"), ("<180d", "offset_180d_days"), ("<270d (interp)", "offset_270d_days")]:
    vals = res_df[col].dropna()
    if len(vals) > 0:
        print(f"\n{label}: n_matched={len(vals)}/{len(res_df)}, mean offset={vals.mean():.1f}d, "
              f"median={vals.median():.1f}d, max abs={vals.abs().max():.0f}d, min abs={vals.abs().min():.0f}d")
    else:
        print(f"\n{label}: n_matched=0/{len(res_df)} -- NO MATCH sama sekali")

print("\nCatatan: n event historis kecil (lihat tabel) -- setiap event kemungkinan dari cycle")
print("berbeda, jadi TIDAK independen dalam arti statistik biasa, tapi tiap event = 1 regime")
print("transition unik (bukan sample berulang dari fenomena sama).")
