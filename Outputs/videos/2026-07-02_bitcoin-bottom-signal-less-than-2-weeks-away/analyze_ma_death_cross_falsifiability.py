"""
Insight 6 - 50w/100w MA death cross falsifiability check
Video: "Bitcoin Bottom Signal (Less Than 2 Weeks Away)" - Bitcoin Magazine Pro, 2026-07-02

Klaim asli video: death cross 50-week/100-week MA diproyeksikan 10 Juli 2026,
dipakai sebagai penanda area bear low (dibandingkan dgn 2015, 2018-19, 2022).

KETERBATASAN DATA: kolom 100_wma TIDAK ada di data kita (lihat data_dictionary.md).
Proxy terdekat yang tersedia: 50_wma vs 200_wma. Ini BUKAN uji klaim asli video
(50w/100w), melainkan proxy dengan pasangan MA yang lebih lambat (200w) -- disebutkan
eksplisit di semua output supaya tidak disalahartikan sebagai konfirmasi/penolakan
langsung klaim video.

Event definition:
  - "Death cross" = hari pertama 50_wma < 200_wma setelah sebelumnya 50_wma >= 200_wma
  - "Golden cross" = kebalikannya
  - Proyeksi crossing masa depan = ekstrapolasi linear gap (50_wma - 200_wma) dari
    slope 90 hari terakhir data tersedia -- INI PROYEKSI, bukan fakta, wajib dilabel
    sebagai estimasi kasar (gap bisa berubah kalau harga bergerak tajam)
"""

import pandas as pd
import numpy as np

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUT_DIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-07-02_bitcoin-bottom-signal-less-than-2-weeks-away"

df = pd.read_csv(CSV, parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 1].reset_index(drop=True)
df = df.dropna(subset=["50_wma", "200_wma"]).reset_index(drop=True)
df["gap"] = df["50_wma"] - df["200_wma"]
df["above"] = df["50_wma"] > df["200_wma"]

LAST_DATE = df["date"].max()

print("=" * 90)
print("INSIGHT 6 - 50wma/200wma DEATH CROSS FALSIFIABILITY CHECK (proxy, BUKAN klaim asli 50w/100w)")
print("=" * 90)
print(f"Data terakhir tersedia: {LAST_DATE.date()}")

# ─── All historical crossovers of 50wma vs 200wma ───────────────────────────
trans = df["above"].astype(int).diff().fillna(0)
idxs = df.index[trans != 0]

events = []
for i in idxs:
    kind = "GOLDEN(50>200)" if df["above"].iloc[i] else "DEATH(50<200)"
    events.append({"date": df["date"].iloc[i], "type": kind})

print(f"\nSEMUA cross 50wma/200wma sepanjang histori data ({len(events)} event):")
for e in events:
    print(f"  {e['date'].date()}  {e['type']}")

n_death = sum(1 for e in events if "DEATH" in e["type"])
print(f"\n>>> n = {n_death} death cross historis (50wma/200wma) sejak data 200wma tersedia.")
print("    Sample sangat kecil -- WAJIB dianggap low-confidence, bukan pola berulang yang solid.")

# ─── Context: nearest local price low around the one historical death cross ─
death_events = [e for e in events if "DEATH" in e["type"]]
for e in death_events:
    ev_date = e["date"]
    window = df[(df["date"] >= ev_date - pd.Timedelta(days=200)) & (df["date"] <= ev_date + pd.Timedelta(days=200))]
    low_row = window.loc[window["btc_price"].idxmin()]
    lag = (low_row["date"] - ev_date).days
    print(f"\nDeath cross {ev_date.date()}: harga terendah lokal +/-200 hari ada di {low_row['date'].date()} "
          f"(${low_row['btc_price']:,.0f}), jarak = {lag:+d} hari (negatif = low terjadi SEBELUM death cross, positif = SESUDAH)")

# ─── Current cycle: is a new death cross imminent, per video's July 10 2026 claim? ──
print(f"\n{'-'*90}")
print("SIKLUS SEKARANG (2026):")
current = df.iloc[-1]
print(f"  {current['date'].date()}: 50wma=${current['50_wma']:,.0f}  200wma=${current['200_wma']:,.0f}  "
      f"gap=${current['gap']:,.0f} (50wma masih {current['gap']/current['200_wma']*100:.1f}% di atas 200wma)")

recent = df[df["date"] >= LAST_DATE - pd.Timedelta(days=90)]
x = (recent["date"] - recent["date"].min()).dt.days.values.astype(float)
y = recent["gap"].values
slope, intercept = np.polyfit(x, y, 1)
last_gap = recent["gap"].iloc[-1]
print(f"  Slope gap (90 hari terakhir): {slope:.2f} USD/hari")
if slope < 0:
    days_to_zero = -last_gap / slope
    proj_date = LAST_DATE + pd.Timedelta(days=days_to_zero)
    print(f"  Proyeksi linear (kasar): gap mencapai 0 dalam ~{days_to_zero:.0f} hari -> sekitar {proj_date.date()}")
    print(f"  Klaim video: death cross 10 Juli 2026. Proyeksi linear data kita: ~{proj_date.date()}")
else:
    print("  Gap sedang MELEBAR (tidak konvergen) -- tidak ada proyeksi cross.")

recent[["date", "btc_price", "50_wma", "200_wma", "gap"]].to_csv(
    f"{OUT_DIR}\\events_ma_death_cross_recent_gap.csv", index=False
)
pd.DataFrame(events).to_csv(f"{OUT_DIR}\\events_ma_death_cross_falsifiability.csv", index=False)
print("\nCSV disimpan: events_ma_death_cross_falsifiability.csv, events_ma_death_cross_recent_gap.csv")
