"""
VALIDASI P4 - pullback_catcher_level_early_bull

Klaim video (segmen 2): level untuk add exposure saat dip di awal bull =
STH RP dan "true market mean". Framework kita pakai AVIV Mean (K5: tunggu
pullback >=5% dari high lokal).

Pertanyaan: di jendela EARLY BULL, saat terjadi pullback >=5% dari high lokal,
level mana yang paling sering "menangkap" dip -> low pullback berhenti dalam
+-3% dari level?

Definisi (dikunci sebelum menghitung):
  - Jendela early-bull = tanggal UNLOCK STRUKTURAL (STH RP cross naik melewati
    RP, DF v2 sec.0) s/d hari ke-3 dari streak pertama close > AVIV Upper
    (>=3 hari berturut) -> persis definisi "K5 selesai" di DF v2.
  - AVIV Upper = price_at_aviv_mean + 0.5*(price_at_aviv_plus_1_sigma -
    price_at_aviv_mean)  [formula resmi framework, tidak dihitung ulang]
  - Pullback = episode. Running high = max close sejak awal jendela.
    Episode DIBUKA saat close <= 0.95 * running_high.
    Trough = close terendah selama episode.
    Episode DITUTUP saat close kembali > running_high saat episode dibuka
    (atau jendela habis). Satu episode = satu event (ini sekaligus aturan
    merge/cooldown: tidak ada dua episode tumpang tindih).
  - "Tertangkap level X" = |trough_close / X(hari trough) - 1| <= 3%.
    Nilai level diambil di HARI TROUGH (at-gate untuk level, tidak ada nilai
    dari masa depan).
  - Overshoot ke bawah = (trough_close / X - 1) * 100 ketika trough < X.
"""

import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-25_is-the-bitcoin-bear-market-over"

PB_TH = 0.95      # pullback >=5%
TOL = 3.0         # +-3% dianggap "tertangkap"
AVIV_STREAK = 3   # hari di atas AVIV Upper untuk menutup jendela

df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
need = ["btc_price", "sth_cost_basis", "realized_price", "true_market_mean_price",
        "price_at_aviv_mean", "price_at_aviv_plus_1_sigma"]
df = df.dropna(subset=need).reset_index(drop=True)
df = df[df["btc_price"] > 0].reset_index(drop=True)
LAST = df["date"].max()
print("Data:", df["date"].min().date(), "s/d", LAST.date(), "| n hari =", len(df))

df["aviv_upper"] = df["price_at_aviv_mean"] + 0.5 * (df["price_at_aviv_plus_1_sigma"] - df["price_at_aviv_mean"])
df["struct_N"] = df["sth_cost_basis"] > df["realized_price"]

# ---------- unlock struktural ----------
unlocks = []
for i in range(1, len(df)):
    if df.at[i, "struct_N"] and not df.at[i - 1, "struct_N"]:
        back = df.loc[max(0, i - 30):i - 1, "struct_N"]
        if len(back) == 30 and (~back).all():
            unlocks.append(i)
print("\nUnlock struktural:", [df.at[i, "date"].strftime("%Y-%m-%d") for i in unlocks])

# ---------- akhir jendela: 3 hari berturut close > AVIV Upper ----------
above_up = (df["btc_price"] > df["aviv_upper"]).values
windows = []
for k, u in enumerate(unlocks):
    end = None
    for j in range(u, len(df) - AVIV_STREAK + 1):
        if above_up[j:j + AVIV_STREAK].all():
            end = j + AVIV_STREAK - 1
            break
    if end is None:
        end = len(df) - 1
    windows.append((u, end))

print("\n" + "=" * 118)
print("JENDELA EARLY-BULL (unlock -> cross AVIV Upper >=3 hari)")
print("=" * 118)
for (u, e) in windows:
    print(f"  {df.at[u,'date'].date()} -> {df.at[e,'date'].date()}  ({(df.at[e,'date']-df.at[u,'date']).days} hari) "
          f"| harga {df.at[u,'btc_price']:,.0f} -> {df.at[e,'btc_price']:,.0f}")


def cycle_of(d):
    if d < pd.Timestamp("2013-01-01"):
        return "2011->2012"
    if d < pd.Timestamp("2017-01-01"):
        return "2013->2015"
    if d < pd.Timestamp("2021-01-01"):
        return "2017->2019"
    return "2021->2023"


LEVELS = {"STH RP": "sth_cost_basis",
          "True Market Mean": "true_market_mean_price",
          "AVIV Mean": "price_at_aviv_mean"}

rows = []
for (u, e) in windows:
    seg = df.loc[u:e].reset_index(drop=True)
    close = seg["btc_price"].values
    run_high = close[0]
    i = 0
    while i < len(seg):
        if close[i] <= PB_TH * run_high:
            start_i = i
            peak_val = run_high
            # cari trough sampai close > peak_val (recovery) atau habis
            j = i
            trough_i = i
            while j < len(seg) and close[j] <= peak_val:
                if close[j] < close[trough_i]:
                    trough_i = j
                j += 1
            end_i = min(j, len(seg) - 1)
            tr = seg.iloc[trough_i]
            rec = {
                "cycle": cycle_of(seg.at[0, "date"]),
                "window_start": seg.at[0, "date"].strftime("%Y-%m-%d"),
                "pb_start": seg.at[start_i, "date"].strftime("%Y-%m-%d"),
                "trough_date": tr["date"].strftime("%Y-%m-%d"),
                "local_high": round(float(peak_val), 2),
                "trough_price": round(float(tr["btc_price"]), 2),
                "depth_pct": round((float(tr["btc_price"]) / float(peak_val) - 1) * 100, 1),
                "recovered": bool(j < len(seg)),
            }
            for lbl, col in LEVELS.items():
                lv = float(tr[col])
                dev = (float(tr["btc_price"]) / lv - 1) * 100
                rec[f"dev_{lbl}"] = round(dev, 2)
                rec[f"catch_{lbl}"] = bool(abs(dev) <= TOL)
            rows.append(rec)
            # lanjut setelah recovery; running high di-reset ke peak lama
            i = j
            run_high = peak_val
        else:
            if close[i] > run_high:
                run_high = close[i]
            i += 1

pb = pd.DataFrame(rows)
pb.to_csv(OUTDIR + r"\events_pullback_catcher_level_early_bull.csv", index=False)

print("\n" + "=" * 118)
print(f"PULLBACK >=5% DI JENDELA EARLY-BULL  |  n total = {len(pb)}")
print("=" * 118)
print(f"{'cycle':<12}{'pb start':<12}{'trough':<12}{'depth%':>8}"
      f"{'dev STHRP':>11}{'dev TMM':>10}{'dev AVIVm':>11}   catch (S/T/A)")
print("-" * 118)
for _, r in pb.iterrows():
    cs = "".join(["S" if r["catch_STH RP"] else "-",
                  "T" if r["catch_True Market Mean"] else "-",
                  "A" if r["catch_AVIV Mean"] else "-"])
    print(f"{r['cycle']:<12}{r['pb_start']:<12}{r['trough_date']:<12}{r['depth_pct']:>8.1f}"
          f"{r['dev_STH RP']:>11.1f}{r['dev_True Market Mean']:>10.1f}{r['dev_AVIV Mean']:>11.1f}   {cs}")

print("\nSEBARAN PULLBACK PER CYCLE:")
for c, g in pb.groupby("cycle"):
    print(f"   {c}: n={len(g)}  median depth={g['depth_pct'].median():.1f}%")

print("\n" + "=" * 118)
print(f"LEVEL MANA PALING SERING MENANGKAP DIP (trough dalam +-{TOL:.0f}% dari level)")
print("=" * 118)
print(f"{'level':<20}{'catch':>8}{'dari n':>8}{'hit%':>8}{'median dev':>13}{'median overshoot bawah':>25}{'n overshoot':>13}")
print("-" * 118)
for lbl in LEVELS:
    c = int(pb[f"catch_{lbl}"].sum())
    devs = pb[f"dev_{lbl}"]
    under = devs[devs < 0]
    ov = f"{under.median():.1f}%" if len(under) else "n/a"
    print(f"{lbl:<20}{c:>8}{len(pb):>8}{100.0*c/len(pb):>7.0f}%{devs.median():>12.1f}%{ov:>25}{len(under):>13}")

print("\nPER CYCLE (hit count per level):")
print(f"{'cycle':<14}" + "".join([f"{l:>20}" for l in LEVELS]))
for c, g in pb.groupby("cycle"):
    print(f"{c:<14}" + "".join([f"{int(g[f'catch_{l}'].sum()):>10}/{len(g):<9}" for l in LEVELS]))

print("\nCATATAN: satu pullback bisa tertangkap >1 level kalau level-levelnya berdekatan.")
overlap = pb[[f"catch_{l}" for l in LEVELS]].sum(axis=1)
print(f"  pullback tertangkap 0 level: {int((overlap==0).sum())} | 1 level: {int((overlap==1).sum())} "
      f"| >=2 level: {int((overlap>=2).sum())}")

print(f"\nCSV -> {OUTDIR}\\events_pullback_catcher_level_early_bull.csv")

# ---------- SENSITIVITAS TOLERANSI (3 varian, semua dilaporkan) ----------
print()
print("=" * 118)
print("SENSITIVITAS TOLERANSI +-3% / +-5% / +-7% (semua dilaporkan, bukan cherry-pick)")
print("=" * 118)
print(f"{'level':<20}{'+-3%':>10}{'+-5%':>10}{'+-7%':>10}   (dari n={len(pb)} pullback)")
for lbl in LEVELS:
    devs = pb[f"dev_{lbl}"].abs()
    print(f"{lbl:<20}{int((devs<=3).sum()):>10}{int((devs<=5).sum()):>10}{int((devs<=7).sum()):>10}")

# ---------- posisi level relatif harga sepanjang jendela early bull ----------
print()
print("-" * 118)
print("KONTEKS: posisi tiap level relatif HARGA rata-rata sepanjang jendela early-bull")
print("-" * 118)
for (u, e) in windows:
    seg = df.loc[u:e]
    s1 = ((seg["btc_price"] / seg["sth_cost_basis"] - 1) * 100).median()
    s2 = ((seg["btc_price"] / seg["true_market_mean_price"] - 1) * 100).median()
    s3 = ((seg["btc_price"] / seg["price_at_aviv_mean"] - 1) * 100).median()
    print(f"  {df.at[u,'date'].date()} -> {df.at[e,'date'].date()}: median harga vs STH RP {s1:+.1f}% | "
          f"vs TMM {s2:+.1f}% | vs AVIV Mean {s3:+.1f}%")
