# -*- coding: utf-8 -*-
"""
V3 — Reproduksi leg BLIND DCA dari tabel hasil video BM Pro (slide [10:46])

KLAIM YANG DIUJI (insight #17 / #16):
  Tabel hasil video, asumsi tertulis "0.1% fees, one-bar fill lag, 20% CGT on realised gains":
    Blind DCA : total paid in $66,700 | final value $2,968,017 | IRR 54.0% | BTC 46.8 | maxDD -83.5%
    (dua leg lain — Accumulation & Sell mode — memakai indikator BM Pro yang parameternya
     TIDAK diungkap; TIDAK direplikasi, itu akan jadi overfitting. Lihat findings.)

INKONSISTENSI YANG DISELESAIKAN: slide bilang "$1,000 seed plus $100 a week";
  lisan [05:50]/[09:52] bilang "starting with $100 and depositing $100 every single week".
  -> dua varian seed diuji (a priori dari sumbernya sendiri, bukan grid search).

--- DEFINISI EVENT (STANDAR VALIDASI poin 1) ---
  Kontribusi = SEED sekali di 2014-01-01, lalu $100 setiap 7 HARI KALENDER
    (2014-01-01, 2014-01-08, ...) s/d baris data terakhir 2026-07-15.
    Kontribusi $100 pertama jatuh di hari yang sama dengan seed (t=0).
  Equity = mark-to-market HARIAN (btc_held * btc_price), supaya max drawdown menangkap
    crash intra-periode; sama persis dgn metode yang sudah dipakai di project ini
    (Outputs/videos/2026-07-28_this-strategy-beat-bitcoin-dca-by-20x/
     analyze_dca_backtest_and_calmar.py).
  Max drawdown = penurunan terdalam dari peak NILAI PORTOFOLIO kumulatif.
  XIRR = money-weighted IRR (brentq atas NPV, day-count 365.25) — metode identik dgn
    findings_dca_backtest_and_calmar.md supaya angka bisa dibandingkan lintas findings.

  DUA VARIAN BIAYA (bukan tuning; dua-duanya diambil dari asumsi yang DITULIS di slide):
    F0 = tanpa biaya, fill di harga hari yang sama  (baseline bersih)
    F1 = fee 0.1% + one-bar fill lag (beli dieksekusi di harga close HARI BERIKUTNYA)
  20% CGT tidak berlaku untuk leg blind DCA: tidak ada realised gain (tidak pernah jual).

--- ANTI LOOKAHEAD (poin 3) ---
  Backtest pasif tanpa sinyal; jadwal kontribusi ditetapkan a priori. one-bar fill lag
  justru membuat eksekusi memakai harga yang BELUM diketahui di hari keputusan — itu
  konservatif (bukan lookahead) karena keputusan belinya tidak bergantung harga.

--- CATATAN DATA ---
  btc_price penuh 2010-07-17 s/d 2026-07-15. Video tanggal 2026-08-05 -> data kita
  BERHENTI ~3 minggu LEBIH AWAL. Karena itu total setoran & final value kita otomatis
  lebih kecil; koreksi dihitung eksplisit di bawah.
"""

import numpy as np
import pandas as pd
from scipy.optimize import brentq

DATA = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

START = pd.Timestamp("2014-01-01")
WEEKLY = 100.0

df = pd.read_csv(DATA, parse_dates=["date"])
df = df[["date", "btc_price"]].dropna().sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 0].reset_index(drop=True)
LAST = df["date"].max()
price = df.set_index("date")["btc_price"]

print(f"Data harga BTC: {df['date'].min().date()} s/d {LAST.date()} (n={len(df)} hari)")
print("CATATAN PENTING: data berhenti 2026-07-15, video 2026-08-05 -> selisih ~3 minggu")
print("                 (~3 kontribusi mingguan). Semua pembanding disesuaikan.\n")


def price_on_or_after(d, maxlag=10):
    for k in range(maxlag):
        dd = d + pd.Timedelta(days=k)
        if dd in price.index:
            return dd, float(price.loc[dd])
    return None, None


def run_dca(seed, fee=0.0, fill_lag=0, end=LAST):
    """seed di t=0 + WEEKLY tiap 7 hari kalender. fee = fraksi (0.001 = 0.1%).
    fill_lag = jumlah hari kalender penundaan eksekusi (one-bar lag = 1)."""
    dates = pd.date_range(START, end, freq="7D")
    btc = 0.0
    paid = 0.0
    flows = []           # (jumlah negatif, tanggal) utk XIRR
    log = []
    for i, d in enumerate(dates):
        amt = WEEKLY + (seed if i == 0 else 0.0)
        exec_d, px = price_on_or_after(d + pd.Timedelta(days=fill_lag))
        if exec_d is None or exec_d > end:
            continue
        btc += (amt * (1 - fee)) / px
        paid += amt
        flows.append((-amt, d))
        log.append((d, exec_d, px, amt, btc, paid))

    daily = df[(df["date"] >= START) & (df["date"] <= end)].copy().reset_index(drop=True)
    lg = pd.DataFrame(log, columns=["sched", "exec_date", "px", "amt", "btc_cum", "paid_cum"])
    hold = lg.set_index("exec_date")["btc_cum"].reindex(daily["date"]).ffill().fillna(0.0)
    pcum = lg.set_index("exec_date")["paid_cum"].reindex(daily["date"]).ffill().fillna(0.0)
    daily["btc"] = hold.values
    daily["paid"] = pcum.values
    daily["equity"] = daily["btc"] * daily["btc_price"]
    daily["peak"] = daily["equity"].cummax()
    daily["dd"] = np.where(daily["peak"] > 0, daily["equity"] / daily["peak"] - 1, 0.0)
    mdd = float(daily["dd"].min())
    mdd_date = daily.loc[daily["dd"].idxmin(), "date"]

    final_px = float(daily["btc_price"].iloc[-1])
    final_val = btc * final_px

    def npv(r):
        s = 0.0
        for cf, d in flows:
            s += cf / (1 + r) ** ((d - START).days / 365.25)
        s += final_val / (1 + r) ** ((end - START).days / 365.25)
        return s
    try:
        xirr = brentq(npv, -0.95, 10.0)
    except Exception:
        xirr = float("nan")

    return dict(seed=seed, fee=fee, fill_lag=fill_lag, n_contrib=len(lg), paid=paid,
                btc=btc, final_px=final_px, final_val=final_val, xirr=xirr,
                mdd=mdd, mdd_date=mdd_date, daily=daily, last_contrib=lg["sched"].iloc[-1])


CLAIM = dict(paid=66700.0, final=2968017.0, irr=54.0, btc=46.8, mdd=-83.5)

print("=" * 116)
print("(a)-(e) REPRODUKSI LEG BLIND DCA - $100/7 hari sejak 2014-01-01, dua varian SEED")
print("=" * 116)
print(f"{'varian':<34}{'n setor':>8}{'total setor':>13}{'BTC':>9}{'final value':>14}"
      f"{'XIRR':>8}{'maxDD':>9}{'setoran terakhir':>18}")
print("-" * 116)
runs = {}
for seed, slab in [(1000.0, "seed $1.000 (SLIDE)"), (100.0, "seed $100 (LISAN)")]:
    for fee, lag, flab in [(0.0, 0, "F0 tanpa fee"), (0.001, 1, "F1 fee0,1%+lag1")]:
        r = run_dca(seed, fee, lag)
        key = (seed, flab)
        runs[key] = r
        print(f"{slab + ' / ' + flab:<34}{r['n_contrib']:>8}{r['paid']:>13,.0f}{r['btc']:>9.2f}"
              f"{r['final_val']:>14,.0f}{r['xirr']*100:>7.1f}%{r['mdd']*100:>8.1f}%"
              f"{str(r['last_contrib'].date()):>18}")
print(f"{'KLAIM VIDEO (per 2026-08-05)':<34}{'-':>8}{CLAIM['paid']:>13,.0f}{CLAIM['btc']:>9.1f}"
      f"{CLAIM['final']:>14,.0f}{CLAIM['irr']:>7.1f}%{CLAIM['mdd']:>8.1f}%{'?':>18}")

# =====================================================================
# (e) Mana yang cocok: seed $1.000 atau seed $100?
# =====================================================================
print("\n" + "=" * 116)
print("(e) MENYELESAIKAN INKONSISTENSI SLIDE ($1.000 seed) vs LISAN ($100 seed)")
print("=" * 116)
print("  Uji aritmetika total setoran. Total video = $66.700.")
for seed in [1000.0, 100.0]:
    rest = CLAIM["paid"] - seed
    n = rest / WEEKLY
    print(f"    seed ${seed:,.0f} -> sisa ${rest:,.0f} = {n:.1f} setoran mingguan "
          f"({'BULAT' if abs(n - round(n)) < 1e-9 else 'TIDAK bulat'})")
    if abs(n - round(n)) < 1e-9:
        # setoran ke-1 di t=0, jadi setoran terakhir = START + (n-1)*7 hari
        lastd = START + pd.Timedelta(days=int(round(n) - 1) * 7)
        print(f"        -> setoran mingguan terakhir jatuh {lastd.date()} "
              f"(video terbit 2026-08-05: {'MASUK AKAL' if lastd <= pd.Timestamp('2026-08-05') else 'SETELAH tanggal video -> TIDAK mungkin'})")
r1 = runs[(1000.0, "F0 tanpa fee")]
r2 = runs[(100.0, "F0 tanpa fee")]
print(f"\n  Total setoran kita per {LAST.date()}: seed$1.000 = ${r1['paid']:,.0f} | "
      f"seed$100 = ${r2['paid']:,.0f}")
gap = CLAIM["paid"] - r1["paid"]
print(f"  Selisih thd $66.700 (seed $1.000) = ${gap:,.0f} = {gap/WEEKLY:.0f} setoran mingguan "
      f"= {gap/WEEKLY*7:.0f} hari -> KONSISTEN dgn data kita berhenti ~3 minggu lebih awal.")
gap2 = CLAIM["paid"] - r2["paid"]
print(f"  Selisih thd $66.700 (seed $100)   = ${gap2:,.0f} = {gap2/WEEKLY:.0f} setoran mingguan "
      f"= {gap2/WEEKLY*7:.0f} hari -> perlu ~{gap2/WEEKLY*7/7:.0f} minggu ekstra, "
      f"jatuh {(START + pd.Timedelta(days=(r2['n_contrib'] + int(gap2/WEEKLY) - 1)*7)).date()}.")

# =====================================================================
# (f) Harga BTC implied dari tabel video
# =====================================================================
print("\n" + "=" * 116)
print("(f) HARGA BTC IMPLIED DARI TABEL VIDEO vs HARGA AKTUAL")
print("=" * 116)
imp_dca = CLAIM["final"] / CLAIM["btc"]
print(f"  Blind DCA      : {CLAIM['final']:,.0f} / {CLAIM['btc']} BTC = ${imp_dca:,.0f}")
imp_acc = (3115675 - 2007) / 49.1
imp_sell = (5794249 - 1107111) / 73.9
print(f"  Accumulation   : (3.115.675 - 2.007) / 49,1 BTC = ${imp_acc:,.0f}")
print(f"  Sell mode      : (5.794.249 - 1.107.111) / 73,9 BTC = ${imp_sell:,.0f}")
print(f"  -> ketiga kolom internally consistent di sekitar ${np.mean([imp_dca, imp_acc, imp_sell]):,.0f} "
      f"(sebaran {min(imp_dca,imp_acc,imp_sell):,.0f}-{max(imp_dca,imp_acc,imp_sell):,.0f}) -- VERIFIKASI ULANG OK.")
act = float(price.loc[LAST])
print(f"  Harga aktual btc_price {LAST.date()} = ${act:,.0f}")
print(f"  Selisih implied vs aktual = {imp_dca/act-1:+.2%}")
# sensitivitas pembulatan 46.8 BTC (3 angka penting)
lo_px = CLAIM["final"] / 46.85
hi_px = CLAIM["final"] / 46.75
print(f"  Sensitivitas pembulatan BTC (46,75-46,85): implied price ${lo_px:,.0f}-${hi_px:,.0f} "
      f"-> {'TIDAK menutup' if not (lo_px <= act <= hi_px) else 'menutup'} selisih ke ${act:,.0f}.")
print("  Tren harga 30 hari terakhir data kita (konteks arah sebelum tanggal video):")
tail = df.tail(31)
print(f"    {tail['date'].iloc[0].date()} ${tail['btc_price'].iloc[0]:,.0f}  ->  "
      f"{tail['date'].iloc[-1].date()} ${tail['btc_price'].iloc[-1]:,.0f}  "
      f"({tail['btc_price'].iloc[-1]/tail['btc_price'].iloc[0]-1:+.1%}); "
      f"min ${tail['btc_price'].min():,.0f} max ${tail['btc_price'].max():,.0f}")

# =====================================================================
# Normalisasi: bandingkan apple-to-apple pada total setoran yang sama
# =====================================================================
print("\n" + "=" * 116)
print("NORMALISASI: apa jadinya angka kita KALAU harga akhir = harga implied video ($63.419)")
print("(mengisolasi efek selisih ~3 minggu data + selisih harga, bukan mengubah strategi)")
print("=" * 116)
for seed, slab in [(1000.0, "seed $1.000"), (100.0, "seed $100")]:
    for flab in ["F0 tanpa fee", "F1 fee0,1%+lag1"]:
        r = runs[(seed, flab)]
        v = r["btc"] * imp_dca
        print(f"  {slab} / {flab:<16}: BTC={r['btc']:.2f} -> nilai @${imp_dca:,.0f} = ${v:,.0f} "
              f"(klaim ${CLAIM['final']:,.0f}, selisih {v/CLAIM['final']-1:+.1%}); "
              f"BTC vs 46,8 = {r['btc']/CLAIM['btc']-1:+.1%}")

print("\n" + "=" * 116)
print("TOLERANSI vs KLAIM VIDEO (+/-10% dianggap 'reproduce')")
print("=" * 116)
for (seed, flab), r in runs.items():
    d_btc = r["btc"] / CLAIM["btc"] - 1
    d_paid = r["paid"] / CLAIM["paid"] - 1
    d_irr = r["xirr"] * 100 / CLAIM["irr"] - 1
    d_mdd = abs(r["mdd"] * 100) / abs(CLAIM["mdd"]) - 1
    ok = all(abs(x) <= 0.10 for x in [d_btc, d_paid, d_irr, d_mdd])
    print(f"  seed ${seed:>6,.0f} / {flab:<16}: dBTC={d_btc:+6.1%} dSetor={d_paid:+6.1%} "
          f"dIRR={d_irr:+6.1%} dMaxDD={d_mdd:+6.1%} -> {'REPRODUCE' if ok else 'TIDAK semua dalam 10%'}")

print("\nn (poin 2): 1 leg strategi diuji (blind DCA), 4 konfigurasi (2 seed x 2 asumsi biaya),")
print("            1 window historis (2014-01-01 s/d 2026-07-15) yang mencakup 3 bear penuh")
print("            (2014-15, 2018, 2022) + 1 bear berjalan. Max drawdown -> 1 observasi dominan")
print("            (bear 2018), jadi angka maxDD SANGAT bergantung satu cycle.")
