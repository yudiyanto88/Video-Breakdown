"""
Validasi 3: 200-day MA / yearly (365-day) MA sebagai resistance ladder.
Sekadar cek akurasi angka yang disebut video, bukan structural insight.

Klaim video (2026-08-11): harga di bawah 200-day MA (~$70,000) dan
yearly/365-day MA (~$85,000).

CATATAN DATA: data terakhir tersedia 2026-07-15 (gap ~27 hari ke tanggal
video) -- dipakai sebagai proxy + ekstrapolasi tren singkat.
"""

import pandas as pd

df = pd.read_csv(
    r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv",
    parse_dates=["date"],
)
df = df.sort_values("date").reset_index(drop=True)

# 365-day rolling MA computed manually (tidak ada kolom siap pakai untuk 365d,
# yang ada 200_dma dan 200_wma/50_wma)
df["ma365"] = df["btc_price"].rolling(365, min_periods=365).mean()

last = df.iloc[-1]
VIDEO_DATE = pd.Timestamp("2026-08-11")
print(f"Data terakhir: {last['date'].date()}  |  Video: {VIDEO_DATE.date()}  |  gap = {(VIDEO_DATE-last['date']).days} hari\n")

print(f"btc_price @ {last['date'].date()} = ${last['btc_price']:,.0f}")
print(f"200_dma    @ {last['date'].date()} = ${last['200_dma']:,.0f}   (klaim video ~$70,000, selisih {(last['200_dma']-70000)/70000*100:+.1f}%)")
print(f"ma365      @ {last['date'].date()} = ${last['ma365']:,.0f}   (klaim video ~$85,000, selisih {(last['ma365']-85000)/85000*100:+.1f}%)")

print(f"\nHarga vs MA di data terakhir:")
print(f"  price < 200dma? {last['btc_price'] < last['200_dma']}  ({last['btc_price']:,.0f} vs {last['200_dma']:,.0f})")
print(f"  price < ma365?  {last['btc_price'] < last['ma365']}  ({last['btc_price']:,.0f} vs {last['ma365']:,.0f})")

# extrapolate both MAs to video date using recent 60d daily growth rate (MA declining as old high days roll off)
recent = df.tail(60)
g_dma = (recent["200_dma"].iloc[-1] / recent["200_dma"].iloc[0]) ** (1/59) - 1
g_365 = (recent["ma365"].iloc[-1] / recent["ma365"].iloc[0]) ** (1/59) - 1
days_ext = (VIDEO_DATE - last["date"]).days
ext_dma = last["200_dma"] * (1+g_dma) ** days_ext
ext_365 = last["ma365"] * (1+g_365) ** days_ext
print(f"\nEkstrapolasi ke {VIDEO_DATE.date()} (pakai trend 60hr terakhir):")
print(f"  200dma ~ ${ext_dma:,.0f}  (klaim ~$70,000)")
print(f"  ma365  ~ ${ext_365:,.0f}  (klaim ~$85,000)")

print("\nKonteks 10 hari terakhir:")
print(df[["date","btc_price","200_dma","ma365"]].tail(10).to_string(index=False))
