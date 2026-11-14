"""
Validasi 2 insight dari video "This Strategy Beat Bitcoin DCA by 20x" (On-Chain Mind, 2026-07-28)

INSIGHT #1: Presenter klaim DCA $10,000 ke BTC sejak "2014" tumbuh ke ~$446,000
            (total return ~4,000%, CAGR ~36%, max drawdown ~83%).
            Cadence (mingguan/bulanan) TIDAK disebutkan presenter -> kita coba 2 varian.

INSIGHT #2: Calmar Ratio (CAGR / |MaxDD|) BTC buy-and-hold per cycle penuh.
            Presenter klaim DCA Calmar = 0.44 (dari window tunggal ~2014-2026).
            Kita cek apakah 0.44 itu representatif lintas cycle, atau cuma
            angka yang sensitif ke window 12-tahun yang mereka pilih.

Definisi event (STANDAR VALIDASI poin 1):
  - DCA event = kontribusi periodik tetap (mingguan=setiap 7 hari kalender,
    bulanan=tanggal 1 tiap bulan / hari trading terdekat) dari start_date s/d
    tanggal data terakhir yang tersedia (2026-07-15, dekat tanggal video 2026-07-28).
  - Portfolio value dihitung MARK-TO-MARKET HARIAN (bukan cuma di tanggal kontribusi)
    supaya max drawdown menangkap crash intra-periode.
  - Max drawdown dihitung dari peak NILAI PORTOFOLIO kumulatif (bukan dari harga BTC
    mentah) -> method ini "melunakkan" drawdown dibanding buy-and-hold murni karena
    kontribusi baru terus menambah basis, sesuai cara kerja kalkulator DCA pada umumnya.
  - CAGR DCA dihitung dengan metode sederhana ala kalkulator retail:
    CAGR = (final_value / total_contributed) ^ (1/years) - 1
    (BUKAN XIRR uang-tertimbang yang lebih akurat secara teknis -- tapi ini yang
    tampaknya dipakai presenter, karena angka 4,000% & 36% CAGR yang mereka sebut
    hanya konsisten kalau dihitung dengan cara ini. XIRR dilaporkan sbg pembanding).
  - Cycle boundary Insight #2 memakai konvensi bottom-to-bottom yang SUDAH established
    di project Onchain-Dashboard (research/framework_review_2026-07/backtest_k5nz/run_backtest.py):
      S1 2013-01-01 -> 2015-01-14
      S2 2015-01-15 -> 2018-12-15
      S3 2018-12-16 -> 2022-11-21
      S4 2022-11-22 -> 2026-07-15 (BELUM SELESAI -- cycle terbuka)
    (bukan 2011-2015/2015-2018/2018-2022/2022-2026 seperti draft awal, supaya konsisten
    dgn definisi yang sudah dipakai backtest lain di project -- lihat STANDAR VALIDASI
    soal "jangan bikin definisi baru kalau sudah ada acuan").

Anti-lookahead (poin 3): semua keputusan (beli DCA, hitung drawdown) memakai harga
  di hari itu saja, tidak ada data masa depan yang dipakai untuk keputusan apapun
  (ini backtest pasif, tidak ada sinyal trading, jadi risiko lookahead minim,
  tapi tetap dicatat sesuai checklist).

Independensi sample (poin 4): Insight #2 n=4 cycle, S4 BELUM SELESAI -- flag eksplisit.
"""

import pandas as pd
import numpy as np

pd.set_option("display.width", 140)

# ─── Load data ───────────────────────────────────────────────────────────────
DATA_PATH = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
df = pd.read_csv(DATA_PATH, parse_dates=["date"])
df = df[["date", "btc_price"]].dropna().sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 0].reset_index(drop=True)

LAST_DATE = df["date"].max()
print(f"Data BTC price: {df['date'].min().date()} s/d {LAST_DATE.date()}  (n={len(df)} hari)")

price_map = df.set_index("date")["btc_price"]


def get_price_on_or_after(d, price_series, max_lookahead=10):
    """Ambil harga persis di tanggal d, atau tanggal trading terdekat SETELAHNYA
    (menangani kalau tanggal kontribusi jatuh di luar range data)."""
    for offset in range(max_lookahead):
        dd = d + pd.Timedelta(days=offset)
        if dd in price_series.index:
            return dd, price_series.loc[dd]
    return None, None


# =============================================================================
# INSIGHT #1: DCA backtest simulation (weekly & monthly), start 2014-01-01
# =============================================================================
def dca_backtest(start_date, end_date, cadence, contribution=100.0):
    """
    cadence: 'W' (setiap 7 hari kalender dari start_date) atau 'MS' (tanggal 1 tiap bulan)
    contribution: nominal per periode (nilai absolut tidak penting -- total return,
                  CAGR, dan max drawdown adalah rasio yang invariant terhadap skala
                  kontribusi, karena DCA linear. contribution=100 dipakai sbg unit,
                  hasil akhir nanti di-scale ke basis $10,000 total utk pembanding
                  dgn angka dollar presenter)
    """
    if cadence == "W":
        contrib_dates = pd.date_range(start_date, end_date, freq="7D")
    elif cadence == "MS":
        contrib_dates = pd.date_range(start_date, end_date, freq="MS")
    else:
        raise ValueError(cadence)

    btc_held = 0.0
    total_contributed = 0.0
    contrib_log = []
    for cd in contrib_dates:
        actual_date, price = get_price_on_or_after(cd, price_map)
        if actual_date is None:
            continue
        btc_bought = contribution / price
        btc_held += btc_bought
        total_contributed += contribution
        contrib_log.append((actual_date, price, btc_bought, btc_held, total_contributed))

    # Mark-to-market HARIAN dari start_date s/d end_date, pakai btc_held kumulatif
    # per tanggal (btc_held konstan di antara dua tanggal kontribusi)
    contrib_df = pd.DataFrame(contrib_log, columns=["date", "price", "btc_bought", "btc_held_cum", "contributed_cum"])
    daily = df[(df["date"] >= start_date) & (df["date"] <= end_date)].copy().reset_index(drop=True)
    # forward-fill btc_held & contributed dari jadwal kontribusi
    holdings_series = contrib_df.set_index("date")["btc_held_cum"].reindex(daily["date"]).ffill().fillna(0.0)
    contributed_series = contrib_df.set_index("date")["contributed_cum"].reindex(daily["date"]).ffill().fillna(0.0)
    daily["btc_held_cum"] = holdings_series.values
    daily["contributed_cum"] = contributed_series.values
    daily["portfolio_value"] = daily["btc_held_cum"] * daily["btc_price"]

    # Max drawdown dari peak NILAI PORTOFOLIO (bukan harga BTC mentah)
    daily["running_max"] = daily["portfolio_value"].cummax()
    daily["drawdown"] = np.where(
        daily["running_max"] > 0,
        (daily["portfolio_value"] - daily["running_max"]) / daily["running_max"],
        0.0,
    )
    max_dd = daily["drawdown"].min()
    max_dd_date = daily.loc[daily["drawdown"].idxmin(), "date"]

    final_value = daily["portfolio_value"].iloc[-1]
    final_contributed = daily["contributed_cum"].iloc[-1]
    total_return = final_value / final_contributed - 1
    years = (end_date - start_date).days / 365.25

    # CAGR ala kalkulator retail (final/contributed)^(1/years)-1 -- ini yang
    # tampaknya dipakai presenter (lihat cross-check di komentar file header)
    cagr_simple = (final_value / final_contributed) ** (1 / years) - 1

    # XIRR (money-weighted, lebih akurat scr teknis) sbg pembanding tambahan
    try:
        from scipy.optimize import brentq

        cashflows = [(-contribution, cd) for cd in contrib_df["date"]]
        cashflows.append((final_value, end_date))

        def npv(rate):
            return sum(cf / (1 + rate) ** ((d - start_date).days / 365.25) for cf, d in cashflows)

        xirr = brentq(npv, -0.99, 10.0)
    except Exception:
        xirr = np.nan

    n_contributions = len(contrib_df)
    scale = 10000.0 / final_contributed  # scale ke basis "$10,000 total invested" ala presenter
    final_value_scaled = final_value * scale
    total_contributed_scaled = final_contributed * scale

    return {
        "cadence": cadence,
        "n_contributions": n_contributions,
        "start_date": start_date,
        "end_date": end_date,
        "years": years,
        "final_value_raw": final_value,
        "total_contributed_raw": final_contributed,
        "final_value_scaled_10k": final_value_scaled,
        "total_contributed_scaled_10k": total_contributed_scaled,
        "total_return_pct": total_return * 100,
        "cagr_simple_pct": cagr_simple * 100,
        "xirr_pct": xirr * 100 if not np.isnan(xirr) else np.nan,
        "max_dd_pct": max_dd * 100,
        "max_dd_date": max_dd_date,
        "daily_df": daily,
    }


print("\n" + "=" * 100)
print("INSIGHT #1 -- DCA backtest simulation vs klaim video ($10k -> $446k, CAGR ~36%, MaxDD ~83%)")
print("=" * 100)

START = pd.Timestamp("2014-01-01")
END = LAST_DATE  # 2026-07-15, data terakhir tersedia (dekat tanggal video 2026-07-28)

results = {}
for cadence, label in [("W", "Mingguan (setiap 7 hari)"), ("MS", "Bulanan (tanggal 1)")]:
    r = dca_backtest(START, END, cadence)
    results[cadence] = r
    print(f"\n--- Varian: {label} ---")
    print(f"  Periode        : {r['start_date'].date()} s/d {r['end_date'].date()}  ({r['years']:.2f} tahun)")
    print(f"  n kontribusi   : {r['n_contributions']}")
    print(f"  Total kontribusi (scaled ke basis $10k): ${r['total_contributed_scaled_10k']:,.0f}")
    print(f"  Final value    (scaled ke basis $10k)  : ${r['final_value_scaled_10k']:,.0f}")
    print(f"  Total return   : {r['total_return_pct']:,.0f}%   (klaim video: ~4,000%)")
    print(f"  CAGR (simple, final/contributed)       : {r['cagr_simple_pct']:.1f}%   (klaim video: ~36%)")
    print(f"  XIRR (money-weighted, pembanding)       : {r['xirr_pct']:.1f}%")
    print(f"  Max Drawdown (dari peak nilai portfolio): {r['max_dd_pct']:.1f}%   (klaim video: ~83%)")
    print(f"  Tanggal Max DD : {r['max_dd_date'].date()}")

# ─── Sensitivity check: geser start date beberapa bulan ─────────────────────
print("\n--- Sensitivity check: start date digeser +/- beberapa bulan (BUKAN cari yg cocok, cuma cek stabilitas) ---")
for alt_start_str in ["2014-04-01", "2013-10-01"]:
    alt_start = pd.Timestamp(alt_start_str)
    r_alt = dca_backtest(alt_start, END, "MS")
    print(
        f"  start={alt_start.date()} (bulanan): total_return={r_alt['total_return_pct']:,.0f}%  "
        f"CAGR={r_alt['cagr_simple_pct']:.1f}%  MaxDD={r_alt['max_dd_pct']:.1f}%"
    )

# ─── Toleransi check ──────────────────────────────────────────────────────
print("\n--- Cek toleransi (+/-15%) terhadap klaim video ---")
CLAIM = {"total_return_pct": 4000.0, "cagr_pct": 36.0, "max_dd_pct": 83.0}
for cadence, label in [("W", "Mingguan"), ("MS", "Bulanan")]:
    r = results[cadence]
    tr_diff = (r["total_return_pct"] - CLAIM["total_return_pct"]) / CLAIM["total_return_pct"] * 100
    cagr_diff = (r["cagr_simple_pct"] - CLAIM["cagr_pct"]) / CLAIM["cagr_pct"] * 100
    dd_diff = (abs(r["max_dd_pct"]) - CLAIM["max_dd_pct"]) / CLAIM["max_dd_pct"] * 100
    print(
        f"  {label}: total_return diff={tr_diff:+.1f}% | CAGR diff={cagr_diff:+.1f}% | MaxDD diff={dd_diff:+.1f}%  "
        f"-> {'MATCH (dlm 15%)' if abs(tr_diff)<=15 and abs(cagr_diff)<=15 and abs(dd_diff)<=15 else 'TIDAK MATCH'}"
    )

# =============================================================================
# INSIGHT #2: Calmar Ratio BTC buy-and-hold per cycle (bottom-to-bottom, established)
# =============================================================================
print("\n" + "=" * 100)
print("INSIGHT #2 -- Calmar Ratio (CAGR / |MaxDD|) BTC buy-and-hold per cycle")
print("Metode: LUMP-SUM buy-and-hold (bukan DCA equity curve) -- alasan: Calmar per")
print("cycle paling standar dihitung dari harga awal->akhir cycle + max drawdown harga")
print("mentah dalam window itu. Equity curve DCA insight #1 tercampur kontribusi lintas")
print("cycle sehingga tidak clean utk dipecah per-cycle.")
print("Cycle boundary = konvensi bottom-to-bottom established project (run_backtest.py)")
print("=" * 100)

CYCLES = [
    ("S1 2013-2015", "2013-01-01", "2015-01-14"),
    ("S2 2015-2018", "2015-01-15", "2018-12-15"),
    ("S3 2018-2022", "2018-12-16", "2022-11-21"),
    ("S4 2022-now (BELUM SELESAI)", "2022-11-22", str(LAST_DATE.date())),
]

calmar_rows = []
for name, lo, hi in CYCLES:
    lo_d, hi_d = pd.Timestamp(lo), pd.Timestamp(hi)
    window = df[(df["date"] >= lo_d) & (df["date"] <= hi_d)].reset_index(drop=True)
    if window.empty:
        continue
    start_price = window["btc_price"].iloc[0]
    end_price = window["btc_price"].iloc[-1]
    years = (hi_d - lo_d).days / 365.25
    cagr = (end_price / start_price) ** (1 / years) - 1

    running_max = window["btc_price"].cummax()
    dd = (window["btc_price"] - running_max) / running_max
    max_dd = dd.min()

    calmar = cagr / abs(max_dd) if max_dd != 0 else np.nan

    calmar_rows.append(
        {
            "cycle": name,
            "start": lo,
            "end": hi,
            "years": round(years, 2),
            "start_price": round(start_price, 2),
            "end_price": round(end_price, 2),
            "cagr_pct": round(cagr * 100, 1),
            "max_dd_pct": round(max_dd * 100, 1),
            "calmar": round(calmar, 3),
        }
    )
    print(
        f"\n{name}  ({lo} -> {hi}, {years:.2f}y)\n"
        f"  Price: ${start_price:,.2f} -> ${end_price:,.2f}\n"
        f"  CAGR: {cagr*100:.1f}%   MaxDD: {max_dd*100:.1f}%   Calmar: {calmar:.3f}"
    )

calmar_df = pd.DataFrame(calmar_rows)
print("\n--- Ringkasan Calmar per cycle ---")
print(calmar_df.to_string(index=False))
print(f"\nCalmar stats (n={len(calmar_df)} cycle): mean={calmar_df['calmar'].mean():.3f}, "
      f"min={calmar_df['calmar'].min():.3f}, max={calmar_df['calmar'].max():.3f}, "
      f"std={calmar_df['calmar'].std():.3f}")
print("PERINGATAN: n=4 cycle, S4 BELUM SELESAI (cycle terbuka) -- sample sangat kecil,")
print("MaxDD & CAGR S4 bisa berubah signifikan sebelum cycle ini selesai.")

# Bandingkan dgn window 12-tahun ala video (2014-2026, DCA vs lump-sum)
print("\n--- Untuk konteks: window ~2014-2026 (window yg dipakai video) sbg lump-sum single-window ---")
w = df[(df["date"] >= START) & (df["date"] <= END)].reset_index(drop=True)
sp, ep = w["btc_price"].iloc[0], w["btc_price"].iloc[-1]
yrs = (END - START).days / 365.25
cagr_full = (ep / sp) ** (1 / yrs) - 1
rmax = w["btc_price"].cummax()
dd_full = ((w["btc_price"] - rmax) / rmax).min()
calmar_full = cagr_full / abs(dd_full)
print(f"  Lump-sum 2014-2026: CAGR={cagr_full*100:.1f}%  MaxDD={dd_full*100:.1f}%  Calmar={calmar_full:.3f}")
print(f"  (Klaim video utk DCA window sama: CAGR~36%, MaxDD~83%, Calmar~0.44)")

# ─── Save events CSV ─────────────────────────────────────────────────────────
out_dir = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-07-28_this-strategy-beat-bitcoin-dca-by-20x"

# CSV 1: ringkasan DCA backtest variants
dca_summary_rows = []
for cadence, label in [("W", "Mingguan"), ("MS", "Bulanan")]:
    r = results[cadence]
    dca_summary_rows.append(
        {
            "variant": label,
            "start_date": r["start_date"].date(),
            "end_date": r["end_date"].date(),
            "years": round(r["years"], 2),
            "n_contributions": r["n_contributions"],
            "total_contributed_scaled_10k": round(r["total_contributed_scaled_10k"], 0),
            "final_value_scaled_10k": round(r["final_value_scaled_10k"], 0),
            "total_return_pct": round(r["total_return_pct"], 1),
            "cagr_simple_pct": round(r["cagr_simple_pct"], 1),
            "xirr_pct": round(r["xirr_pct"], 1) if not np.isnan(r["xirr_pct"]) else None,
            "max_dd_pct": round(r["max_dd_pct"], 1),
            "max_dd_date": r["max_dd_date"].date(),
            "claim_total_return_pct": 4000,
            "claim_cagr_pct": 36,
            "claim_max_dd_pct": 83,
        }
    )
dca_summary_df = pd.DataFrame(dca_summary_rows)

# CSV 2: calmar per cycle
calmar_df_out = calmar_df.copy()

combined_path = out_dir + r"\events_dca_backtest_calmar.csv"
with open(combined_path, "w", encoding="utf-8") as f:
    f.write("=== DCA Backtest Variants (Insight #1) ===\n")
    dca_summary_df.to_csv(f, index=False)
    f.write("\n=== Calmar Ratio per Cycle (Insight #2) ===\n")
    calmar_df_out.to_csv(f, index=False)

print(f"\nCSV pendukung disimpan: {combined_path}")
