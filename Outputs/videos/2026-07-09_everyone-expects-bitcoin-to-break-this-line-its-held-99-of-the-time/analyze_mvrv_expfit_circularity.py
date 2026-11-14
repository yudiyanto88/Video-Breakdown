"""
Topik 1: Validasi klaim video "MVRV exponential peak/trough fit line" (Bitcoin Magazine Pro,
2026-07-09). Klaim: garis fit eksponensial trough MVRV historis baru saja crossing di atas
MVRV=1 -> Bitcoin kemungkinan besar TIDAK akan dip di bawah realized price cycle ini.
Basis "probabilitas": cuma 17 hari (0.29%) MVRV pernah di bawah garis trough-fit sepanjang
sejarah, dan 9 hari (0.15%) di atas garis peak-fit -> "99.7%+ chance".

Definisi event (eksplisit, sebelum hitung apapun):
- PEAK per cycle = titik MVRV RAW RATIO tertinggi dalam window bull-run cycle tsb
  (bukan titik harga ATH -- MVRV bisa peak sebelum harga ATH kalau realized price naik cepat)
- TROUGH per cycle = titik MVRV RAW RATIO terendah dalam window bear-market cycle tsb
- Window ditentukan dari tanggal2 cycle top/bottom yang sudah diketahui publik (dipakai juga
  video ybs: 2011, 2013, 2017/2018, 2021/2022, 2024-2025 -- cycle saat ini)
- n peak = 5 (2011, 2013, 2017, 2021, 2024-25-so-far). n trough = 4 (2011, 2015, 2018, 2022)
  -- cycle sekarang BELUM py ya trough (itu justru yang mau diprediksi), makanya tidak masuk
  fit trough.
- INI SAMPLE SANGAT KECIL (5 & 4 titik). Fit garis dari titik sekecil ini rawan overfitting /
  sangat sensitif ke tiap titik individual -- wajib di-test leave-one-out (bagian c).

Anti-lookahead: fit dilakukan dgn SEMUA data historis yg sudah terjadi (bukan proyeksi masa
depan) -- ini valid karena klaim video sendiri fully retrospective (garis dihitung dari
seluruh histori s/d skrg). Tidak ada isu at-gate di sini karena klaim bukan real-time trading
rule, tapi character-of-model check (apakah fit robust).
"""
import pandas as pd
import numpy as np

pd.set_option("display.width", 140)

df = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv", parse_dates=["date"])
df = df[["date", "btc_price", "mvrv_ratio", "realized_price"]].dropna().reset_index(drop=True)
df = df.sort_values("date").reset_index(drop=True)
df["ordinal"] = df["date"].map(pd.Timestamp.toordinal)

print("Data range:", df["date"].min().date(), "to", df["date"].max().date(), "| n_days =", len(df))

# ─── (a) Definisi peak & trough per cycle (window eksplisit) ────────────────────────────────
peak_windows = [
    ("2011 peak",    "2011-01-01", "2011-08-01"),
    ("2013 peak",    "2013-01-01", "2013-12-31"),
    ("2017 peak",    "2017-06-01", "2017-12-31"),
    ("2021 peak",    "2020-06-01", "2021-12-31"),
    ("2024-25 peak", "2023-06-01", "2026-07-15"),  # cycle berjalan, "peak so far"
]
trough_windows = [
    ("2011 trough", "2011-08-01", "2012-06-01"),
    ("2015 trough", "2014-06-01", "2015-12-31"),
    ("2018 trough", "2018-06-01", "2019-03-01"),
    ("2022 trough", "2022-01-01", "2022-12-31"),
]

def extract(windows, kind):
    rows = []
    for name, s, e in windows:
        sub = df[(df["date"] >= s) & (df["date"] <= e)]
        row = sub.loc[sub["mvrv_ratio"].idxmax()] if kind == "max" else sub.loc[sub["mvrv_ratio"].idxmin()]
        rows.append({"cycle": name, "date": row["date"], "mvrv_ratio": row["mvrv_ratio"],
                     "btc_price": row["btc_price"], "ordinal": row["ordinal"]})
    return pd.DataFrame(rows)

peaks = extract(peak_windows, "max")
troughs = extract(trough_windows, "min")

print("\n=== PEAK anchor points (n = %d) ===" % len(peaks))
print(peaks[["cycle", "date", "mvrv_ratio", "btc_price"]].to_string(index=False))
print("\n=== TROUGH anchor points (n = %d) ===" % len(troughs))
print(troughs[["cycle", "date", "mvrv_ratio", "btc_price"]].to_string(index=False))

# ─── Fit exponensial: ln(mvrv) = a + b*ordinal  (regresi linear di log-space) ───────────────
def fit_line(sub_df):
    x = sub_df["ordinal"].values.astype(float)
    y = np.log(sub_df["mvrv_ratio"].values.astype(float))
    b, a = np.polyfit(x, y, 1)
    return a, b

a_peak, b_peak = fit_line(peaks)
a_trough, b_trough = fit_line(troughs)

print(f"\nPEAK fit:   ln(MVRV) = {a_peak:.6f} + {b_peak:.8f} * ordinal")
print(f"TROUGH fit: ln(MVRV) = {a_trough:.6f} + {b_trough:.8f} * ordinal")

df["peak_line"] = np.exp(a_peak + b_peak * df["ordinal"])
df["trough_line"] = np.exp(a_trough + b_trough * df["ordinal"])

latest = df.iloc[-1]
print(f"\nLatest date: {latest['date'].date()}, MVRV aktual: {latest['mvrv_ratio']:.4f}")
print(f"Implied trough line (hari ini): {latest['trough_line']:.4f}")
print(f"Implied peak line (hari ini):   {latest['peak_line']:.4f}")

# ─── (b) Hitung ulang independen: % hari MVRV < trough_line, % hari MVRV > peak_line ────────
below_trough = df["mvrv_ratio"] < df["trough_line"]
above_peak = df["mvrv_ratio"] > df["peak_line"]
n_below = below_trough.sum()
n_above = above_peak.sum()
n_total = len(df)
print(f"\n=== (b) Replikasi independen ===")
print(f"n_total hari (dgn data mvrv+realized_price): {n_total}")
print(f"Hari MVRV < trough_line: {n_below}  ({100*n_below/n_total:.3f}%)  [klaim video: 17 hari, 0.29%]")
print(f"Hari MVRV > peak_line:   {n_above}  ({100*n_above/n_total:.3f}%)  [klaim video: 9 hari, 0.15%]")

if n_below > 0:
    print("\nTanggal2 di bawah trough_line:")
    print(df.loc[below_trough, ["date", "mvrv_ratio", "trough_line"]].to_string(index=False))
if n_above > 0:
    print("\nTanggal2 di atas peak_line:")
    print(df.loc[above_peak, ["date", "mvrv_ratio", "peak_line"]].to_string(index=False))

# ─── (c) Leave-one-out sensitivity test pada TROUGH fit ────────────────────────────────────
print("\n=== (c) Leave-one-out sensitivity test (TROUGH fit, n=4 -> n=3) ===")
today_ordinal = latest["ordinal"]
base_implied_today = np.exp(a_trough + b_trough * today_ordinal)
print(f"Baseline (semua 4 trough): implied trough level hari ini = {base_implied_today:.4f}  (>1 = 'won't dip below RP')")

loo_results = []
for i in range(len(troughs)):
    sub = troughs.drop(troughs.index[i])
    a_i, b_i = fit_line(sub)
    implied_today_i = np.exp(a_i + b_i * today_ordinal)
    dropped = troughs.iloc[i]["cycle"]
    loo_results.append((dropped, implied_today_i, implied_today_i > 1))
    print(f"  Drop [{dropped:<12}] -> implied trough hari ini = {implied_today_i:.4f}  | >1 (won't dip)? {implied_today_i > 1}")

n_flip = sum(1 for _, _, above1 in loo_results if not above1)
print(f"\nDari {len(loo_results)} leave-one-out runs, {n_flip} run(s) FLIP prediksi jadi <1 (WILL dip) saat 1 titik dibuang.")

# ─── Extra: fit tanpa titik EKSTRIM 2011 (paling tua, paling mempengaruhi slope krn 15th jauh) ─
print("\n=== Extra check: fit trough TANPA anchor 2011 (titik paling ekstrem/tertua) ===")
sub_no2011 = troughs[troughs["cycle"] != "2011 trough"]
a_no11, b_no11 = fit_line(sub_no2011)
implied_no11 = np.exp(a_no11 + b_no11 * today_ordinal)
print(f"n=3 (drop 2011): implied trough hari ini = {implied_no11:.4f}  | >1 (won't dip)? {implied_no11 > 1}")

# ─── (d) Ringkasan n ─────────────────────────────────────────────────────────────────────────
print("\n=== RINGKASAN n ===")
print(f"n peak anchor points  = {len(peaks)}  (per cycle: {list(peaks['cycle'])})")
print(f"n trough anchor points = {len(troughs)}  (per cycle: {list(troughs['cycle'])})")
print("PERINGATAN: n=4-5 titik untuk fit regresi lintas SELURUH sejarah BTC adalah sample")
print("sangat kecil. Setiap titik individual (terutama titik tertua/paling ekstrem, 2011)")
print("punya leverage besar terhadap slope garis -- lihat hasil leave-one-out di atas.")
