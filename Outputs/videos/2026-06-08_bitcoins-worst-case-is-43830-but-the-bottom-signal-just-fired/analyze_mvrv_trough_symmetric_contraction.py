"""
Validasi: MVRV trough contraction & proyeksi "tidak dip di bawah RP" (MVRV=1)

Klaim presenter: peak & trough MVRV ratio contracting predictably tiap cycle (garis tren manual
melalui bear-low 2012, 2015, 2018-19, 2022-23). Proyeksi: cycle ini mungkin TIDAK dip di bawah
MVRV=1 sama sekali -- pertama kali dalam sejarah kalau benar.

Uji:
1. Ambil mvrv_ratio, cari trough (local min) di tiap window bear cycle 2012, 2015, 2018-19, 2022-23.
2. Fit regresi linear atas 4 titik trough, extrapolate ke cycle sekarang (titik ke-5). Apakah >1.0?
3. Sensitivitas: ganti anchor point jadi rata-rata window +-30 hari sekitar tanggal low.
4. Berapa kali sepanjang sejarah data MVRV TIDAK pernah dip <1.0 selama bear market (n, sebaran)?
"""

import pandas as pd
import numpy as np

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

df = pd.read_csv(CSV, parse_dates=["date"])
df = df[["date", "btc_price", "mvrv_ratio"]].dropna(subset=["mvrv_ratio", "btc_price"])
df = df[df["btc_price"] > 0].sort_values("date").reset_index(drop=True)

# Bear-market windows (post-peak consolidation/bottom periods), sesuai penyebutan presenter transcript:
# "the 2012, the 2015 bear market low, 2019 bear market low, 2022 into 2023 bear market low"
windows = [
    ("2012", "2011-10-01", "2012-12-31"),
    ("2015", "2014-06-01", "2015-12-31"),
    ("2018-19", "2018-06-01", "2019-06-30"),
    ("2022-23", "2022-06-01", "2023-06-30"),
]

print("=" * 100)
print("1. MVRV TROUGH PER BEAR CYCLE (single-point local minimum dalam window)")
print("=" * 100)

troughs = []
for label, d0, d1 in windows:
    w = df[(df["date"] >= d0) & (df["date"] <= d1)]
    row = w.loc[w["mvrv_ratio"].idxmin()]
    troughs.append({"cycle": label, "date": row["date"], "mvrv_trough": row["mvrv_ratio"]})
    print(f"  {label:<10} trough date={row['date'].date()}  MVRV={row['mvrv_ratio']:.4f}  price=${row['btc_price']:,.2f}")

print("\n" + "=" * 100)
print("2. REGRESI LINEAR ATAS 4 TITIK TROUGH, EXTRAPOLATE KE CYCLE KE-5 (SEKARANG)")
print("=" * 100)

x = np.array([1, 2, 3, 4])
y = np.array([t["mvrv_trough"] for t in troughs])
slope, intercept = np.polyfit(x, y, 1)
pred5 = slope * 5 + intercept
print(f"  Titik: {[round(v,4) for v in y]}")
print(f"  Slope={slope:.4f}  Intercept={intercept:.4f}")
print(f"  Extrapolasi trough cycle ke-5 (linear) = {pred5:.4f}")
print(f"  Prediksi trough > 1.0 (tidak dip)? {'YA' if pred5 > 1.0 else 'TIDAK'}")

print("\n" + "=" * 100)
print("3. SENSITIVITAS: window rata-rata +-30 hari sekitar tanggal low (bukan titik tunggal)")
print("=" * 100)

troughs_avg = []
for t in troughs:
    d = t["date"]
    w = df[(df["date"] >= d - pd.Timedelta(days=30)) & (df["date"] <= d + pd.Timedelta(days=30))]
    avg_val = w["mvrv_ratio"].mean()
    troughs_avg.append(avg_val)
    print(f"  {t['cycle']:<10} single-point={t['mvrv_trough']:.4f}  window+-30d avg={avg_val:.4f}")

y2 = np.array(troughs_avg)
slope2, intercept2 = np.polyfit(x, y2, 1)
pred5_avg = slope2 * 5 + intercept2
print(f"\n  Regresi linear pakai window-avg: slope={slope2:.4f}, intercept={intercept2:.4f}")
print(f"  Extrapolasi trough cycle ke-5 (window-avg based) = {pred5_avg:.4f}")
print(f"  Prediksi trough > 1.0? {'YA' if pred5_avg > 1.0 else 'TIDAK'}")
print(f"\n  Selisih hasil single-point vs window-avg method: {pred5:.4f} vs {pred5_avg:.4f} "
      f"(delta={pred5-pred5_avg:+.4f}) -- {'SENSITIF ke pilihan anchor' if abs(pred5-pred5_avg)>0.05 else 'relatif stabil'}")

# Extra sensitivity: drop earliest point (2012) -- often noisy/thin-data era -- refit on 2015,2018-19,2022-23 only
print("\n  --- Extra sensitivity: refit tanpa titik 2012 (data era awal, thin liquidity) ---")
x3 = np.array([2, 3, 4])
y3 = y[1:]
slope3, intercept3 = np.polyfit(x3, y3, 1)
pred5_no2012 = slope3 * 5 + intercept3
print(f"  Titik dipakai: {[round(v,4) for v in y3]}")
print(f"  Extrapolasi (3 titik, tanpa 2012) = {pred5_no2012:.4f}  -> >1.0? {'YA' if pred5_no2012>1.0 else 'TIDAK'}")

print("\n" + "=" * 100)
print("4. HISTORIS: berapa kali MVRV TIDAK dip di bawah 1.0 selama bear market? (n & sebaran)")
print("=" * 100)

for label, d0, d1 in windows:
    w = df[(df["date"] >= d0) & (df["date"] <= d1)]
    min_val = w["mvrv_ratio"].min()
    dipped = min_val < 1.0
    n_days_below = (w["mvrv_ratio"] < 1.0).sum()
    print(f"  {label:<10} min MVRV di window = {min_val:.4f}  | dip <1.0? {'YA' if dipped else 'TIDAK'} "
          f"| n hari <1.0 dlm window = {n_days_below}")

n_bear_cycles = len(windows)
n_no_dip = sum(1 for label, d0, d1 in windows
               if df[(df["date"]>=d0)&(df["date"]<=d1)]["mvrv_ratio"].min() >= 1.0)
print(f"\n  Dari n={n_bear_cycles} bear cycle yang diuji (2012, 2015, 2018-19, 2022-23): "
      f"{n_no_dip} yang TIDAK pernah dip <1.0.")
print(f"  (Artinya: seluruh {n_bear_cycles - n_no_dip}/{n_bear_cycles} bear cycle historis SELALU dip <1.0 -- "
      f"belum pernah ada preseden 'tidak dip'.)")

print("\nNOTE: n=4 titik untuk fit regresi -- SAMPLE SIZE SANGAT KECIL. Hasil extrapolasi sensitif")
print("terhadap pilihan anchor (single-point vs window-avg vs exclude-2012) -- lihat bagian 3.")

# --- Export event table ---
out_rows = []
for i, t in enumerate(troughs):
    out_rows.append({
        "cycle": t["cycle"], "trough_date": t["date"].date(),
        "mvrv_trough_single_point": round(t["mvrv_trough"], 4),
        "mvrv_trough_window30d_avg": round(troughs_avg[i], 4),
    })
out_rows.append({
    "cycle": "current (extrapolated)", "trough_date": "",
    "mvrv_trough_single_point": round(pred5, 4),
    "mvrv_trough_window30d_avg": round(pred5_avg, 4),
})
pd.DataFrame(out_rows).to_csv("events_mvrv_trough_symmetric_contraction.csv", index=False)
print("\n[Saved events_mvrv_trough_symmetric_contraction.csv]")
