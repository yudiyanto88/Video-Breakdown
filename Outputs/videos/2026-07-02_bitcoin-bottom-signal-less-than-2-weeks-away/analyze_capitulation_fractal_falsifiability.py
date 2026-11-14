"""
Insight 1 - Time-based capitulation fractal falsifiability check
Video: "Bitcoin Bottom Signal (Less Than 2 Weeks Away)" - Bitcoin Magazine Pro, 2026-07-02

Klaim: proyeksi bottom sekitar 12 Juli 2026 (156 hari dari "initial shock" awal 2026,
mereplikasi jarak 156 hari dari fractal 2022 dan ~126 hari dari fractal 2018-19).

Event definition (eksplisit, sebelum lihat hasil):
  - "Local low dalam window prediksi" = harga terendah (btc_price) pada rentang
    tanggal 2026-07-05 s/d 2026-07-19 (window +/-1 minggu dari prediksi 12 Juli 2026).
  - "Lower-low baru" = harga di window prediksi LEBIH RENDAH dari harga terendah
    30 hari kalender sebelum window dimulai (2026-06-05 s/d 2026-07-04).
  - Anti-lookahead: kita hanya pakai data yang TERSEDIA (sampai tanggal terakhir di
    file CSV), bukan data masa depan yang belum ada. Kalau data terpotong sebelum
    window prediksi selesai, itu WAJIB dilaporkan sebagai keterbatasan, bukan
    dianggap window sudah selesai diuji.

Data cutoff: dicek otomatis dari max(date) di file.
"""

import pandas as pd

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

df = pd.read_csv(CSV, parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 1].reset_index(drop=True)

LAST_DATE = df["date"].max()

WINDOW_START = pd.Timestamp("2026-07-05")
WINDOW_END   = pd.Timestamp("2026-07-19")
PRED_DATE    = pd.Timestamp("2026-07-12")

PREWINDOW_START = pd.Timestamp("2026-06-05")
PREWINDOW_END   = pd.Timestamp("2026-07-04")

ATH_START = pd.Timestamp("2025-08-01")

print("=" * 90)
print("INSIGHT 1 - CAPITULATION FRACTAL FALSIFIABILITY CHECK")
print("=" * 90)
print(f"Data terakhir tersedia: {LAST_DATE.date()}")
print(f"Window prediksi        : {WINDOW_START.date()} s/d {WINDOW_END.date()} (prediksi bottom: {PRED_DATE.date()})")

if LAST_DATE < WINDOW_END:
    print(f"!! PERINGATAN: data terpotong {(WINDOW_END - LAST_DATE).days} hari SEBELUM window prediksi selesai.")
    print("   Window belum bisa diuji penuh -- verdict di bawah ini bersifat SEMENTARA (partial window).")

# ATH context
ath_ctx = df[(df["date"] >= ATH_START) & (df["date"] <= LAST_DATE)]
ath_row = ath_ctx.loc[ath_ctx["btc_price"].idxmax()]
print(f"\nATH siklus ini: {ath_row['date'].date()} @ ${ath_row['btc_price']:,.0f}")

# window observed so far (truncated at LAST_DATE if needed)
win_end_actual = min(WINDOW_END, LAST_DATE)
window = df[(df["date"] >= WINDOW_START) & (df["date"] <= win_end_actual)]
if window.empty:
    print("\nTidak ada data di window prediksi sama sekali (data berhenti sebelum window mulai).")
else:
    win_low_row = window.loc[window["btc_price"].idxmin()]
    print(f"\nData tersedia di window: {WINDOW_START.date()} s/d {win_end_actual.date()} ({len(window)} hari)")
    print(f"Local low DI DALAM window (sejauh data tersedia): {win_low_row['date'].date()} @ ${win_low_row['btc_price']:,.2f}")

    prewindow = df[(df["date"] >= PREWINDOW_START) & (df["date"] <= PREWINDOW_END)]
    prewin_low_row = prewindow.loc[prewindow["btc_price"].idxmin()]
    print(f"Local low 30 hari SEBELUM window (proxy 'lower-low baru'): {prewin_low_row['date'].date()} @ ${prewin_low_row['btc_price']:,.2f}")

    made_lower_low = win_low_row["btc_price"] < prewin_low_row["btc_price"]
    print(f"\n>>> Window low < pre-window low (lower-low baru terbentuk)? {made_lower_low}")

    last_row = df.iloc[-1]
    print(f"\nHarga di hari terakhir data ({last_row['date'].date()}): ${last_row['btc_price']:,.2f}")
    net_up_from_window_low = last_row["btc_price"] > win_low_row["btc_price"]
    print(f"Net naik dari window-low sampai hari terakhir data? {net_up_from_window_low}")

# full recent series for CSV export
export = df[(df["date"] >= PREWINDOW_START) & (df["date"] <= LAST_DATE)][["date", "btc_price"]].copy()
export["in_prediction_window"] = (export["date"] >= WINDOW_START) & (export["date"] <= WINDOW_END)
export.to_csv(
    r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-07-02_bitcoin-bottom-signal-less-than-2-weeks-away\events_capitulation_fractal_falsifiability.csv",
    index=False
)
print("\nCSV disimpan: events_capitulation_fractal_falsifiability.csv")
