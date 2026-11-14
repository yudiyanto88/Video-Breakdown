"""
shock_zone_lib.py — definisi bersama untuk 4 validasi video
"Bitcoin News Doesn't Actually Move The Price" (Look Into Bitcoin, 2026-08-15).

SATU definisi shock + SATU definisi zona v2 dipakai keempat script,
supaya hasilnya bisa saling dibaca. Tidak ada perhitungan formula ulang:
zona/AVIV mengikuti pola research/analyze_k3_stage_comparison.py + data_dictionary.md.

DEFINISI SHOCK (dikunci di muka, tidak diubah setelah lihat hasil):
  r_t   = ln(P_t / P_{t-1})
  vol_t = std(r, 30 hari yang berakhir di t-1)   <-- AT-GATE, hari shock DIKELUARKAN
  PRIMARY  : shock jika |r_t| >= 3 * vol_t
  VARIANT  : shock jika |r_t| >= 0.08   (fixed 8%)
  Hanya 2 varian. Tidak ada varian ketiga.

MERGE/COOLDOWN:
  - "shock day"   = flag harian mentah (dipakai untuk rate per zona & clustering,
                    karena pertanyaannya memang tentang kepadatan hari)
  - "shock event" = hari shock pertama dalam satu klaster; shock day berikutnya
                    dalam COOLDOWN=5 hari kalender diserap ke event yang sama
                    (dipakai untuk analisis event-level: trend flip, step-aside trigger)

ZONA v2 (Decision Framework v2 sec.1):
  struktur: N = STH RP > RP ; T = STH RP < RP ;
            C = |STH RP - RP|/RP < 2% DAN |RP - LTH RP|/RP < 2%  (C menang atas N/T)
  AVIV Mean  = kolom price_at_aviv_mean
  AVIV Upper = price_at_aviv_mean + 0.5*(price_at_aviv_plus_1_sigma - price_at_aviv_mean)
"""

import numpy as np
import pandas as pd

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

VOL_WINDOW   = 30
SHOCK_K      = 3.0
SHOCK_FIXED  = 0.08
COOLDOWN     = 5      # hari kalender untuk merge shock day -> shock event

# Siklus (bottom-to-bottom, dipakai untuk sebaran n per cycle)
CYCLES = [
    ("C1 2010-2015", "2010-07-17", "2015-01-13"),
    ("C2 2015-2018", "2015-01-14", "2018-12-14"),
    ("C3 2018-2022", "2018-12-15", "2022-11-21"),
    ("C4 2022-2026", "2022-11-22", "2026-12-31"),
]

ZONE_ORDER = ["ZC", "ZD", "Z1", "Z1b", "Z2", "Z2t", "Z3", "Z4", "Z5"]


def load_base():
    df = pd.read_csv(MASTER, parse_dates=["date"])
    cols = ["date", "btc_price", "sth_cost_basis", "realized_price", "lth_cost_basis",
            "price_at_aviv_mean", "price_at_aviv_plus_1_sigma",
            "mvrv_ratio", "sth_sopr"]
    df = df[cols].copy()
    df = df[df["btc_price"].notna() & (df["btc_price"] > 0)]
    df = df.sort_values("date").reset_index(drop=True)

    # --- AVIV bands (pola data_dictionary + analyze_k3_stage_comparison) ---
    df["aviv_mean_price"]  = df["price_at_aviv_mean"]
    df["aviv_upper_price"] = df["price_at_aviv_mean"] + 0.5 * (
        df["price_at_aviv_plus_1_sigma"] - df["price_at_aviv_mean"])

    # --- struktur ---
    rp   = df["realized_price"]
    sth  = df["sth_cost_basis"]
    lth  = df["lth_cost_basis"]
    conv = ((sth - rp).abs() / rp < 0.02) & ((rp - lth).abs() / rp < 0.02)
    struct = np.where(conv, "C", np.where(sth > rp, "N", "T"))
    df["struct"] = struct

    # --- zona ---
    p  = df["btc_price"]
    am = df["aviv_mean_price"]
    au = df["aviv_upper_price"]
    z = pd.Series(index=df.index, dtype=object)
    ok = df[["sth_cost_basis", "realized_price", "lth_cost_basis",
             "aviv_mean_price", "aviv_upper_price"]].notna().all(axis=1)

    z[ok & (p >= au)] = "Z5"
    rest = ok & (p < au)
    isC = rest & (df["struct"] == "C")
    z[isC & (p < am)]                = "Z2"
    z[isC & (p >= am)]               = "Z4"
    isN = rest & (df["struct"] == "N")
    z[isN & (p < rp)]                = "ZC"
    z[isN & (p >= rp) & (p < sth)]   = "ZD"
    z[isN & (p >= sth) & (p < am)]   = "Z3"
    z[isN & (p >= am)]               = "Z4"
    isT = rest & (df["struct"] == "T")
    z[isT & (p < sth)]               = "Z1"
    z[isT & (p >= sth) & (p < rp)]   = "Z1b"
    z[isT & (p >= rp)]               = "Z2t"
    df["zone"] = z

    # --- return & vol at-gate ---
    df["logret"] = np.log(df["btc_price"]).diff()
    df["vol30_atgate"]   = df["logret"].rolling(VOL_WINDOW).std().shift(1)
    df["absmean90_atgate"] = df["logret"].abs().rolling(90).mean().shift(1)

    # --- shock flags ---
    df["shock_primary"] = (df["logret"].abs() >= SHOCK_K * df["vol30_atgate"]) & \
                          df["vol30_atgate"].notna() & (df["vol30_atgate"] > 0)
    df["shock_fixed"]   = df["logret"].abs() >= SHOCK_FIXED
    df["shock_primary"] = df["shock_primary"].fillna(False)
    df["shock_fixed"]   = df["shock_fixed"].fillna(False)

    df["cycle"] = "-"
    for name, s, e in CYCLES:
        m = (df["date"] >= pd.Timestamp(s)) & (df["date"] <= pd.Timestamp(e))
        df.loc[m, "cycle"] = name
    return df


def event_flags(df, shock_col, cooldown=COOLDOWN):
    """Merge shock day berdekatan -> shock event (hari pertama klaster)."""
    flags = df[shock_col].values
    dates = df["date"].values
    out = np.zeros(len(df), dtype=bool)
    last = None
    for i in range(len(df)):
        if not flags[i]:
            continue
        if last is None or (dates[i] - dates[last]) / np.timedelta64(1, "D") > cooldown:
            out[i] = True
            last = i
    return out


def fwd_worst_drawdown(price, horizon):
    """Drawdown kumulatif terburuk dari harga hari t dalam t+1..t+horizon (negatif)."""
    p = price.values
    n = len(p)
    out = np.full(n, np.nan)
    for k in range(1, horizon + 1):
        shifted = np.concatenate([p[k:], np.full(k, np.nan)])
        cand = shifted / p - 1.0
        out = np.where(np.isnan(out), cand, np.fmin(out, cand))
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return (np.nan, np.nan)
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * np.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)
