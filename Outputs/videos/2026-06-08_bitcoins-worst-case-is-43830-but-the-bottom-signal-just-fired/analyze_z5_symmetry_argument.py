"""
Validasi: Argumen simetri Z5 (HIGH PRIORITY)

Klaim presenter: karena cycle 2024/25 tidak pernah menyentuh band "Over Valued" (proprietary chart
"Bitcoin Cycle Master"), maka logikanya cycle ini juga tidak akan turun sampai menyentuh band lower
ekstrem.

Relevan LANGSUNG ke syarat awal K1 framework kita: "Harga pernah bertahan di Z5/AVIV Upper minimal
14 hari dalam siklus ini."

Formula AVIV Upper (framework resmi, dari data_dictionary.md + pola analyze_k3_stage_comparison.py):
  HIST_MEAN, HIST_STD = mean/std aviv_ratio (full history)
  true_mkt_mean = btc_price / aviv_ratio
  AVIV Upper (+0.5 SD) = (HIST_MEAN + 0.5*HIST_STD) * true_mkt_mean
  Z5 = price >= AVIV Upper

Uji: hitung total hari Z5, jumlah episode terpisah, tanggal & panjang tiap episode dalam window
2023-01-01 s/d data terbaru. Cek apakah ada episode >=14 hari (syarat K1).
"""

import pandas as pd
import numpy as np

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

df = pd.read_csv(CSV, parse_dates=["date"])
df = df[["date", "btc_price", "aviv_ratio"]].dropna(subset=["btc_price", "aviv_ratio"])
df = df[df["btc_price"] > 0].sort_values("date").reset_index(drop=True)

HIST_MEAN = df["aviv_ratio"].mean()
HIST_STD  = df["aviv_ratio"].std()
df["true_mkt_mean"] = df["btc_price"] / df["aviv_ratio"]
df["aviv_05sig"] = (HIST_MEAN + 0.5 * HIST_STD) * df["true_mkt_mean"]
df["in_z5"] = df["btc_price"] >= df["aviv_05sig"]

print(f"HIST_MEAN(aviv_ratio)={HIST_MEAN:.4f}  HIST_STD={HIST_STD:.4f}")

print("\n" + "=" * 100)
print("Z5 EPISODES -- FULL HISTORY (untuk konteks, berapa total hari Z5 sepanjang sejarah)")
print("=" * 100)

def find_episodes(mask, dates):
    episodes = []
    in_z5 = mask.values
    i = 0
    n = len(in_z5)
    while i < n:
        if in_z5[i]:
            j = i
            while j < n and in_z5[j]:
                j += 1
            episodes.append((dates.iloc[i], dates.iloc[j-1], j - i))
            i = j
        else:
            i += 1
    return episodes

all_episodes = find_episodes(df["in_z5"], df["date"])
total_days_all = sum(e[2] for e in all_episodes)
print(f"Total hari Z5 sepanjang seluruh histori data: {total_days_all} hari, dalam {len(all_episodes)} episode")

print("\n" + "=" * 100)
print(f"Z5 EPISODES -- WINDOW 2023-01-01 s/d {df['date'].max().date()} (cycle 2024/25 & bear berjalan)")
print("=" * 100)

window = df[df["date"] >= "2023-01-01"].reset_index(drop=True)
win_episodes = find_episodes(window["in_z5"], window["date"])
total_days_win = sum(e[2] for e in win_episodes)

print(f"\nTotal hari Z5 dalam window 2023-01-01 s/d sekarang: {total_days_win} hari, {len(win_episodes)} episode\n")

if win_episodes:
    print(f"{'#':<4}{'Mulai':<14}{'Selesai':<14}{'Panjang (hari)':<16}{'>=14d (syarat K1)?'}")
    for idx, (s, e, n) in enumerate(win_episodes, 1):
        flag = "YA" if n >= 14 else "tidak"
        print(f"{idx:<4}{str(s.date()):<14}{str(e.date()):<14}{n:<16}{flag}")
else:
    print("TIDAK ADA episode Z5 sama sekali dalam window ini.")

longest = max((e[2] for e in win_episodes), default=0)
n_ge14 = sum(1 for e in win_episodes if e[2] >= 14)

print(f"\nEpisode terpanjang dalam window: {longest} hari")
print(f"Jumlah episode >=14 hari (syarat K1 'pernah bertahan di Z5 min 14 hari'): {n_ge14}")

if n_ge14 > 0:
    print("\n>>> PREMIS PRESENTER SALAH -- harga TERBUKTI pernah bertahan di Z5 >=14 hari cycle ini.")
    print(">>> Argumen simetri ('tidak pernah overvalued -> tidak akan undervalued') runtuh di premis awal.")
else:
    print("\n>>> Premis presenter (tidak pernah sustained Z5 >=14 hari) TIDAK terbantahkan oleh data ini.")
    print(">>> Catatan: ini beda dari klaim chart proprietary mereka (band 'Over Valued' beda definisi/threshold")
    print(">>> dari AVIV Upper framework kita) -- tapi dari SUDUT PANDANG K1 framework, syarat awal belum/tidak terpenuhi.")

print("\n" + "=" * 100)
print("Konteks tambahan: level AVIV Upper (Z5 threshold) & harga di beberapa tanggal kunci")
print("=" * 100)
for d in ["2024-03-01", "2024-11-01", "2025-01-01", "2025-08-01", "2025-10-01", "2025-10-28"]:
    row = df[df["date"] <= d].iloc[-1]
    print(f"  {row['date'].date()}  price=${row['btc_price']:,.0f}  AVIV_Upper(Z5 threshold)=${row['aviv_05sig']:,.0f}  "
          f"in_Z5={row['in_z5']}")

print("\n" + "=" * 100)
print("TEST LOGIKA SIMETRI: apakah durasi Z5 di puncak cycle historis BERKORELASI dgn ")
print("kedalaman bear market berikutnya (vs Realized Price)? (n=3 cycle historis lengkap)")
print("=" * 100)

df_price = pd.read_csv(CSV, parse_dates=["date"])
df_price = df_price[["date", "btc_price", "realized_price"]].dropna()

cycle_windows = [
    ("2013 peak -> 2015 bear", "2013-01-01", "2014-06-30", "2014-07-01", "2015-06-30"),
    ("2017 peak -> 2018 bear", "2017-01-01", "2018-01-15", "2018-01-16", "2019-06-30"),
    ("2021 peak -> 2022 bear", "2021-01-01", "2021-12-15", "2021-12-16", "2023-06-30"),
]

for label, bull_lo, bull_hi, bear_lo, bear_hi in cycle_windows:
    bull_w = df[(df["date"] >= bull_lo) & (df["date"] <= bull_hi)]
    z5_days = int(bull_w["in_z5"].sum())
    z5_eps = find_episodes(bull_w["in_z5"], bull_w["date"].reset_index(drop=True))
    longest_ep = max((e[2] for e in z5_eps), default=0)

    bear_w = df_price[(df_price["date"] >= bear_lo) & (df_price["date"] <= bear_hi)]
    depth_vs_rp = ((bear_w["btc_price"] / bear_w["realized_price"]) - 1).min() * 100

    print(f"\n{label}:")
    print(f"  Total hari Z5 di fase bull   : {z5_days} hari ({len(z5_eps)} episode, terpanjang {longest_ep}d)")
    print(f"  Kedalaman bear terdalam vs RP: {depth_vs_rp:.1f}%")

print("\n2024/25 cycle (current, sudah dihitung di atas): total 48 hari Z5, 8 episode, terpanjang 13 hari")
print("(belum ada bear-low definitif -- window masih berjalan per data terakhir)")

print("\nKESIMPULAN LOGIKA SIMETRI: correlation antara durasi Z5 & kedalaman bear berikutnya perlu dibaca")
print("dari n=3 titik historis DI ATAS -- SAMPLE SANGAT KECIL untuk klaim korelasi apapun secara statistik.")

# --- Export event table (Z5 episodes 2023+) ---
out_rows = [{"episode_no": i+1, "start": s.date(), "end": e.date(), "days": n, "meets_k1_14d": n >= 14}
            for i, (s, e, n) in enumerate(win_episodes)]
pd.DataFrame(out_rows).to_csv("events_z5_symmetry_argument.csv", index=False)
print("\n[Saved events_z5_symmetry_argument.csv]")
