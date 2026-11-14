"""
Validasi: Konsistensi internal strategi DCA presenter

Presenter (video sama, 2026-06-08) bilang dia akumulasi karena base-case downside cuma
"5-6-7% lower low" dari level saat itu -- tapi model drawdown proyeksi presenter SENDIRI
(insight #1) memproyeksikan central case $55,311 dan worst case $43,830 dari ATH $126,219.03.

Cek murni konsistensi angka: berapa % gap dari harga BTC 2026-06-08 ke $55,311 (central) &
$43,830 (worst case)? Apakah "5-7% lower low" konsisten dengan model presenter sendiri?
"""

import pandas as pd

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

df = pd.read_csv(CSV, parse_dates=["date"])
df = df[["date", "btc_price"]].dropna().sort_values("date").reset_index(drop=True)

video_date = pd.Timestamp("2026-06-08")
row = df[df["date"] == video_date]
if row.empty:
    row = df[df["date"] <= video_date].iloc[[-1]]
price_on_date = row.iloc[0]["btc_price"]
actual_date = row.iloc[0]["date"]

print(f"Harga BTC pada/dekat tanggal video (2026-06-08): {actual_date.date()}  ${price_on_date:,.2f}")

# Presenter juga bilang "we whipped down to within about a hundred dollars" of $58,922 (bull case level)
# beberapa hari sebelum rekaman -- itu level terendah lokal yg disebut presenter. Kita pakai
# harga pada tanggal video sebagai basis "current" utk cek klaim "5-7% lower low DARI SINI".

central = 55311
worst = 43830

gap_central = (central / price_on_date - 1) * 100
gap_worst = (worst / price_on_date - 1) * 100

print(f"\nModel presenter sendiri (dari analyze_bear_drawdown_model.py / findings_bear_drawdown_model.md):")
print(f"  Central case  : ${central:,}  -> gap dari harga saat itu = {gap_central:+.1f}%")
print(f"  Worst case    : ${worst:,}  -> gap dari harga saat itu   = {gap_worst:+.1f}%")

print(f"\nKlaim presenter di menit [11:53]: \"5, 6, maybe 7% lower low\" dari level saat itu.")
implied_5pct = price_on_date * 0.95
implied_7pct = price_on_date * 0.93
print(f"  5% lower  = ${implied_5pct:,.0f}")
print(f"  7% lower  = ${implied_7pct:,.0f}")

print(f"\n--- CEK KONSISTENSI ---")
print(f"  Central case model sendiri ({gap_central:+.1f}%) vs klaim verbal (-5% s/d -7%): "
      f"{'KONSISTEN' if -7 <= gap_central <= -5 else 'TIDAK KONSISTEN -- selisih besar'}")
print(f"  Worst case model sendiri ({gap_worst:+.1f}%) vs klaim verbal (-5% s/d -7%): "
      f"{'KONSISTEN' if -7 <= gap_worst <= -5 else 'TIDAK KONSISTEN -- selisih besar'}")

multiple_central = abs(gap_central) / 6  # vs midpoint 6% of "5-6-7%"
multiple_worst = abs(gap_worst) / 6
print(f"\n  Central case downside ({abs(gap_central):.1f}%) adalah {multiple_central:.1f}x lebih besar dari klaim verbal (~6%)")
print(f"  Worst case downside ({abs(gap_worst):.1f}%) adalah {multiple_worst:.1f}x lebih besar dari klaim verbal (~6%)")

import pandas as pd
pd.DataFrame([
    {"scenario": "Price 2026-06-08", "price": price_on_date, "gap_pct": 0},
    {"scenario": "Verbal claim -5%", "price": implied_5pct, "gap_pct": -5},
    {"scenario": "Verbal claim -7%", "price": implied_7pct, "gap_pct": -7},
    {"scenario": "Model central case ($55,311)", "price": central, "gap_pct": round(gap_central,1)},
    {"scenario": "Model worst case ($43,830)", "price": worst, "gap_pct": round(gap_worst,1)},
]).to_csv("events_dca_strategy_internal_consistency.csv", index=False)
print("\n[Saved events_dca_strategy_internal_consistency.csv]")
