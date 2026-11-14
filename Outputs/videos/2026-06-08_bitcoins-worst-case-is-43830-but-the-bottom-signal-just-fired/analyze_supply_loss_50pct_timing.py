"""
Validasi: Timing klaim ">50% Bitcoin supply in loss" (HIGH PRIORITY -- kemungkinan konflik faktual)

Presenter (video 2026-06-08) mengklaim ">50% Bitcoin supply in loss = capitulation signal"
dan bilang itu "just happened again" saat video direkam (mengutip Benjamin Cowen).

Uji: baca percent_btc_in_loss (== 100 - percent_btc_in_profit) pada 2026-06-08 dan window
sekitarnya (2026-05-25 s/d 2026-06-15). Apakah benar >50% pada/sebelum tanggal video?
"""

import pandas as pd

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

df = pd.read_csv(CSV, parse_dates=["date"])
df = df[["date", "btc_price", "percent_btc_in_profit", "percent_btc_in_loss",
         "pct_sth_in_profit", "pct_sth_in_loss"]].dropna(subset=["btc_price"])
df = df.sort_values("date").reset_index(drop=True)

window = df[(df["date"] >= "2026-05-25") & (df["date"] <= "2026-06-15")]

print("=" * 100)
print("SUPPLY IN LOSS -- WINDOW 2026-05-25 s/d 2026-06-15 (video direkam 2026-06-08)")
print("=" * 100)
print(f"\n{'Tanggal':<12}{'Price':>12}{'%Supply Profit':>16}{'%Supply Loss':>15}{'%STH Profit':>14}{'%STH Loss':>12}")
for _, row in window.iterrows():
    print(f"{str(row['date'].date()):<12}{row['btc_price']:>12,.0f}{row['percent_btc_in_profit']:>16.2f}"
          f"{row['percent_btc_in_loss']:>15.2f}{row['pct_sth_in_profit']:>14.2f}{row['pct_sth_in_loss']:>12.2f}")

video_date = pd.Timestamp("2026-06-08")
row_on_date = df[df["date"] == video_date]
if row_on_date.empty:
    row_on_date = df[df["date"] <= video_date].iloc[[-1]]
    print(f"\nNOTE: tidak ada data persis di 2026-06-08, pakai data terdekat sebelumnya: {row_on_date['date'].values[0]}")

r = row_on_date.iloc[0]
print(f"\n--- NILAI PERSIS PADA/DEKAT TANGGAL VIDEO (2026-06-08) ---")
print(f"  Tanggal              : {r['date'].date()}")
print(f"  Price                : ${r['btc_price']:,.2f}")
print(f"  %Supply in Profit    : {r['percent_btc_in_profit']:.2f}%")
print(f"  %Supply in Loss      : {r['percent_btc_in_loss']:.2f}%")
print(f"  Klaim presenter (>50% in loss)? {'BENAR' if r['percent_btc_in_loss'] > 50 else 'SALAH -- masih di bawah 50%'}")

# Cari kapan (jika pernah) supply in loss menembus 50% di sekitar window ini
print("\n--- Kapan (jika pernah) %Supply in Loss menembus 50% di window yang lebih luas (2026-01-01 s/d terbaru)? ---")
wide = df[df["date"] >= "2026-01-01"]
crossed = wide[wide["percent_btc_in_loss"] > 50]
if crossed.empty:
    print("  TIDAK PERNAH menembus 50% sepanjang 2026 (s/d data terbaru).")
    print(f"  Max %Supply in Loss di 2026: {wide['percent_btc_in_loss'].max():.2f}% "
          f"pada {wide.loc[wide['percent_btc_in_loss'].idxmax(),'date'].date()}")
else:
    print(f"  Pertama kali menembus 50%: {crossed['date'].min().date()}")
    print(crossed[["date","btc_price","percent_btc_in_loss"]].to_string(index=False))

print(f"\nData terbaru tersedia: {df['date'].max().date()}  |  %Supply in Loss saat itu = "
      f"{df.iloc[-1]['percent_btc_in_loss']:.2f}%")

window.to_csv("events_supply_loss_50pct_timing.csv", index=False)
print("\n[Saved events_supply_loss_50pct_timing.csv]")
