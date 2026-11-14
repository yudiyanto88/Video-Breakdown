"""
INSIGHT 3: CAGR Realized Price -- klaim pembicara: rata-rata historis ~38%, saat ini
(2026-07) turun ke sekitar 0-8%, karena harga setahun lalu mirip harga sekarang.

Definisi dipakai: rolling 1-year (365 hari kalender) growth rate Realized Price =
  CAGR_365(t) = RP(t) / RP(t-365d) - 1
(periode window = 1 tahun persis, jadi CAGR == growth rate tahunan sederhana, tidak perlu
pemangkatan tambahan.)

STANDAR VALIDASI:
1. Definisi event: bukan event diskrit, ini deret waktu kontinu (rolling growth rate).
   Dilaporkan sbg rata-rata & sebaran per cycle, bukan "kejadian" tunggal.
2. n = jumlah hari valid rolling value per cycle, dilaporkan eksplisit.
3. Anti-lookahead: CAGR_365(t) hanya pakai RP(t) dan RP(t-365d), keduanya <= tanggal t. Valid
   dipakai "at-gate" pada hari t sendiri (bukan intip masa depan).
4. Independensi: rolling 365d window overlap = otokorelasi tinggi antar hari berdekatan;
   nilai per cycle dirata-ratakan dulu (bukan dihitung n hari mentah sbg n independen).
5. Data realized_price full history 2010-07-17 -- tidak ada isu start-date terlambat.
6. Tidak ada threshold yang di-fit/dioverfit di sini -- murni deskriptif.
"""

import pandas as pd
import numpy as np

df = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_price_level.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["realized_price"]).reset_index(drop=True)

df = df.set_index("date")
rp = df["realized_price"]

# rolling 365-day growth rate: nilai RP 365 hari kalender sebelumnya (bukan index-shift n-rows,
# supaya benar meski ada gap tanggal)
rp_reindexed = rp.reindex(pd.date_range(rp.index.min(), rp.index.max(), freq="D")).interpolate(limit=3)
cagr = rp_reindexed / rp_reindexed.shift(365) - 1
cagr = cagr.dropna()

HALVINGS = [
    ("Cycle 2010-2012", "2009-01-03", "2012-11-28"),
    ("Cycle 2012-2016", "2012-11-28", "2016-07-09"),
    ("Cycle 2016-2020", "2016-07-09", "2020-05-11"),
    ("Cycle 2020-2024", "2020-05-11", "2024-04-20"),
    ("Cycle 2024-now",  "2024-04-20", "2100-01-01"),
]

print("=" * 100)
print("INSIGHT 3: Rolling 1-year CAGR Realized Price -- klaim rata-rata historis ~38%, current 0-8%")
print("=" * 100)

full_mean   = cagr.mean()
full_median = cagr.median()
n_total     = len(cagr)
print(f"\nSeluruh histori (n={n_total} hari valid, {cagr.index.min().date()} s/d {cagr.index.max().date()}):")
print(f"  Mean CAGR   = {full_mean*100:.1f}%")
print(f"  Median CAGR = {full_median*100:.1f}%")
print(f"  Std CAGR    = {cagr.std()*100:.1f}%")
print(f"  Min / Max   = {cagr.min()*100:.1f}% / {cagr.max()*100:.1f}%")

print("\nBreakdown rata-rata per cycle (bukan cuma satu angka gabungan):")
for name, start, end in HALVINGS:
    seg = cagr[(cagr.index >= start) & (cagr.index < end)]
    if len(seg) == 0:
        continue
    print(f"  {name:<18}: n={len(seg):>5}d  mean={seg.mean()*100:>7.1f}%  median={seg.median()*100:>7.1f}%  "
          f"min={seg.min()*100:>7.1f}%  max={seg.max()*100:>7.1f}%")

# Current value = last available data point
last_date = cagr.index.max()
last_val = cagr.iloc[-1]
print(f"\nNilai CAGR pada data terakhir tersedia ({last_date.date()}): {last_val*100:.2f}%")

# Last 90 days trend (to show "trending down" claim)
recent = cagr.tail(90)
print(f"\n90 hari terakhir: mean={recent.mean()*100:.1f}%, min={recent.min()*100:.1f}%, max={recent.max()*100:.1f}%")
print(f"Nilai 365 hari lalu (untuk verifikasi klaim 'harga setahun lalu mirip sekarang'):")
rp_today = rp_reindexed.iloc[-1]
rp_1y_ago = rp_reindexed.iloc[-1-365]
print(f"  RP({last_date.date()}) = {rp_today:,.0f}")
print(f"  RP({(last_date - pd.Timedelta(days=365)).date()}) = {rp_1y_ago:,.0f}")
print(f"  Growth = {(rp_today/rp_1y_ago - 1)*100:.2f}%")

# Also show btc_price comparison for context (not RP) since speaker said "price a year ago similar to today"
price = df["btc_price"].reindex(pd.date_range(df.index.min(), df.index.max(), freq="D")).interpolate(limit=3)
price_today = price.iloc[-1]
price_1y_ago = price.iloc[-1-365]
print(f"\n[Konteks tambahan -- btc_price, bukan RP]")
print(f"  Price({last_date.date()}) = {price_today:,.0f}")
print(f"  Price({(last_date - pd.Timedelta(days=365)).date()}) = {price_1y_ago:,.0f}")
print(f"  Growth = {(price_today/price_1y_ago - 1)*100:.2f}%")

# Save time series for record
out = pd.DataFrame({"date": cagr.index, "rp_cagr_365d": cagr.values})
out.to_csv(
    r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-07-13_mathematically-modelling-the-future-of-bitcoin\events_rp_cagr_365d.csv",
    index=False
)
print("\nSaved events_rp_cagr_365d.csv (n=%d rows)" % len(out))
