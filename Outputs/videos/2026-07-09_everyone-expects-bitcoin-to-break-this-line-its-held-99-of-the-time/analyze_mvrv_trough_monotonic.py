"""
Topik 2: Klaim video -- lembah (trough) MVRV raw ratio per cycle makin tinggi secara
monoton tiap cycle berturut-turut (2011 < 2015 < 2018 < 2022 < now).

Definisi event: TROUGH per cycle = titik MVRV RAW RATIO terendah dalam window bear-market
cycle tsb (window sama seperti Topik 1, sudah dicek historically match tanggal cycle bottom
publik yang dikenal). n = 4 cycle SELESAI (2011, 2015, 2018, 2022) -- cycle sekarang belum
py trough (masih berjalan), jadi TIDAK dihitung sebagai titik ke-5 untuk klaim monotonic ini
(baru bisa dinilai kalau/ketika cycle ini benar2 dip).
"""
import pandas as pd
import numpy as np

df = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv", parse_dates=["date"])
df = df[["date", "btc_price", "mvrv_ratio", "realized_price"]].dropna().reset_index(drop=True)
df = df.sort_values("date").reset_index(drop=True)

trough_windows = [
    ("2011", "2011-08-01", "2012-06-01"),
    ("2015", "2014-06-01", "2015-12-31"),
    ("2018", "2018-06-01", "2019-03-01"),
    ("2022", "2022-01-01", "2022-12-31"),
]

rows = []
for name, s, e in trough_windows:
    sub = df[(df["date"] >= s) & (df["date"] <= e)]
    row = sub.loc[sub["mvrv_ratio"].idxmin()]
    rows.append({"cycle": name, "date": row["date"].date(), "mvrv_trough": row["mvrv_ratio"],
                 "btc_price": row["btc_price"]})

troughs = pd.DataFrame(rows)
print("=== Trough MVRV per cycle (n = %d) ===" % len(troughs))
print(troughs.to_string(index=False))

vals = troughs["mvrv_trough"].values
diffs = np.diff(vals)
is_monotonic = all(d > 0 for d in diffs)

print("\nSelisih berurutan (cycle[i+1] - cycle[i]):", [round(d, 4) for d in diffs])
print(f"Monoton naik (setiap langkah > 0)? {is_monotonic}")

print("\n=== Verdict ===")
if is_monotonic:
    print(f"SUPPORTED secara deskriptif untuk n={len(troughs)} cycle yang tersedia (2011->2015->2018->2022).")
    print("CATATAN WAJIB: n hanya 4 titik/cycle -- sample sangat kecil untuk klaim 'selalu monoton'.")
    print("Cycle saat ini (2024-2026) BELUM py trough -- klaim TIDAK BISA diverifikasi untuk cycle")
    print("berjalan sampai bear market berikutnya benar2 terjadi & terkonfirmasi titik terendahnya.")
else:
    print("NOT SUPPORTED -- ada pelanggaran urutan monotonic.")

# Extra robustness check: apakah kalau window trough sedikit digeser, urutan tetap monoton?
print("\n=== Robustness check: window trough diperlebar +/- beberapa bulan ===")
alt_windows = [
    ("2011", "2011-07-01", "2012-12-31"),
    ("2015", "2014-01-01", "2016-06-30"),
    ("2018", "2018-01-01", "2019-06-30"),
    ("2022", "2021-06-01", "2023-06-30"),
]
rows2 = []
for name, s, e in alt_windows:
    sub = df[(df["date"] >= s) & (df["date"] <= e)]
    row = sub.loc[sub["mvrv_ratio"].idxmin()]
    rows2.append({"cycle": name, "date": row["date"].date(), "mvrv_trough": row["mvrv_ratio"]})
troughs2 = pd.DataFrame(rows2)
print(troughs2.to_string(index=False))
vals2 = troughs2["mvrv_trough"].values
print("Monoton naik dgn window lebar?", all(np.diff(vals2) > 0))
