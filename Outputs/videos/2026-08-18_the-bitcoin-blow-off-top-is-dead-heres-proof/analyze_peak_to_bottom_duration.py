"""
V3 -- Durasi peak->bottom untuk K4 lantai waktu
Video: On-Chain Mind "The Bitcoin Blow-Off Top Is Dead (Here's Proof)" (2026-08-18)

Insight #5 video (bottom->peak ~35 bulan) DIBALIK arahnya: bottom->peak TIDAK actionable
karena bottom baru diketahui ex-post. Yang actionable = durasi PEAK->BOTTOM, karena
peak-nya sudah lewat (2025-10-06) dan gate K4 "lantai waktu" memakai
"(>=9 bulan sejak cycle peak) DAN (close < RP)".

DEFINISI EVENT (dikunci di muka):
  - PEAK  = close tertinggi dalam cycle, dikonfirmasi TIDAK terlampaui selama >=365 hari
            berikutnya (jadi peak yang dipakai adalah peak terkonfirmasi, bukan local high)
  - BOTTOM= close terendah antara peak dan hari harga menembus ATH lama lagi
  - Durasi peak->bottom dihitung dalam hari & bulan (30.44 hari)
  - Gate lantai waktu: hari pertama (t - peak >= 9 bulan) DAN (close < RP). Nilai RP
    tersedia hari itu juga -> tidak ada lookahead
  - Sensitivitas: peak C2 diganti local high Apr 2021 (bukan Nov 2021)

n = 3 cycle tertutup + 1 berjalan (peak Okt 2025). Tambahan: peak Jun 2011 dilaporkan
terpisah sebagai observasi ke-4 tertutup (era data sangat awal -- flag kualitas).
"""

import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-18_the-bitcoin-blow-off-top-is-dead-heres-proof"

df = pd.read_csv(MASTER, parse_dates=["date"])[
    ["date", "btc_price", "realized_price", "sth_cost_basis"]]
df = df.dropna(subset=["btc_price"]).sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 0].reset_index(drop=True)
LAST = df["date"].max()

print("=" * 100)
print("V3 -- DURASI PEAK->BOTTOM & GATE K4 LANTAI WAKTU")
print("=" * 100)
print(f"Data: {df['date'].min().date()} s/d {LAST.date()}")
print("CATATAN: data master terakhir 2026-07-15 -- bear pasca-peak Okt 2025 MASIH BERJALAN.")

# --- Deteksi peak terkonfirmasi (tidak terlampaui >=365 hari) ----------------
def confirmed_peaks():
    p = df["btc_price"].values
    d = df["date"].values
    out = []
    for i in range(len(df)):
        if p[i] < p[:i + 1].max():          # bukan ATH
            continue
        fut = df[(df["date"] > d[i]) & (df["date"] <= d[i] + np.timedelta64(365, "D"))]
        if len(fut) == 0:                    # belum cukup 365 hari data
            out.append((df.loc[i, "date"], p[i], "BELUM TERKONFIRMASI"))
            continue
        if fut["btc_price"].max() < p[i]:
            out.append((df.loc[i, "date"], p[i], "terkonfirmasi"))
    return out

raw = confirmed_peaks()
# ambil satu peak per cycle: peak dgn harga tertinggi dalam tiap klaster
peaks = []
for dt, pr, st in raw:
    if peaks and (dt - peaks[-1][0]).days < 365:
        if pr > peaks[-1][1]:
            peaks[-1] = (dt, pr, st)
    else:
        peaks.append((dt, pr, st))

print("\nPEAK TERKONFIRMASI (close tertinggi, tidak terlampaui >=365 hari)")
print(f"{'#':<3}{'Peak':<13}{'Harga':>14}  Status")
print("-" * 55)
for k, (dt, pr, st) in enumerate(peaks):
    print(f"{k:<3}{str(dt.date()):<13}{pr:>14,.2f}  {st}")

# --- Bottom = close terendah antara peak dan hari menembus ATH lama ----------
def bottom_after(peak_date, peak_price):
    fut = df[df["date"] > peak_date]
    rec = fut[fut["btc_price"] >= peak_price]
    end = rec["date"].iloc[0] if len(rec) else LAST
    w = df[(df["date"] > peak_date) & (df["date"] <= end)]
    i = w["btc_price"].idxmin()
    ongoing = len(rec) == 0
    return df.loc[i, "date"], df.loc[i, "btc_price"], ongoing

rows = []
print("\n" + "=" * 100)
print("DURASI PEAK -> BOTTOM")
print("=" * 100)
print(f"{'Peak':<13}{'P_peak':>13}  {'Bottom':<13}{'P_bottom':>13}"
      f"{'  Drawdown':>11}{'  Hari':>8}{'  Bulan':>8}  Status")
print("-" * 100)
for dt, pr, st in peaks:
    bd, bp, ongoing = bottom_after(dt, pr)
    days = (bd - dt).days
    rows.append(dict(peak=dt.date(), p_peak=round(pr, 2), bottom=bd.date(),
                     p_bottom=round(bp, 2), drawdown_pct=round((bp / pr - 1) * 100, 1),
                     days=days, months=round(days / 30.44, 1),
                     status=("BERJALAN" if ongoing else "tertutup")))
    print(f"{str(dt.date()):<13}{pr:>13,.2f}  {str(bd.date()):<13}{bp:>13,.2f}"
          f"{(bp/pr-1)*100:>10.1f}%{days:>8}{days/30.44:>8.1f}  "
          f"{'BERJALAN (bottom sementara)' if ongoing else 'tertutup'}")

res = pd.DataFrame(rows)
closed = res[res["status"] == "tertutup"]
main = closed[closed["peak"].astype(str) >= "2013"]   # 3 cycle utama (2013, 2017, 2021)
early = closed[closed["peak"].astype(str) < "2013"]

print(f"\nn TERTUTUP TOTAL = {len(closed)}  (utama 2013/2017/2021: n={len(main)}"
      f" | era awal <2013: n={len(early)})   n BERJALAN = {len(res)-len(closed)}")
print(f"3 cycle utama -> mean {main['months'].mean():.1f} bln | "
      f"min {main['months'].min():.1f} | max {main['months'].max():.1f} | "
      f"spread {main['months'].max()-main['months'].min():.1f} bln")
if len(early):
    print(f"Era awal (peak {early['peak'].iloc[0]}) = {early['months'].iloc[0]:.1f} bln -- "
          f"OUTLIER, flag kualitas data & likuiditas 2011")
print(f"Semua tertutup (n={len(closed)}) -> mean {closed['months'].mean():.1f} bln | "
      f"min {closed['months'].min():.1f} | max {closed['months'].max():.1f}")

# --- Gate K4 lantai waktu ---------------------------------------------------
print("\n" + "=" * 100)
print("UJI GATE K4 LANTAI WAKTU: (>=9 bulan sejak peak) DAN (close < RP)")
print("=" * 100)
print("Ditanyakan: bulan ke berapa harga PERTAMA KALI close < RP sejak peak, berapa lama")
print("bertahan, dan gate lantai waktu nyala berapa bulan SEBELUM/SESUDAH bottom aktual.")
gate_rows = []
print(f"\n{'Peak':<13}{'1st P<RP':<13}{'bln ke':>7}{'  streak<RP':>12}"
      f"{'  total hr <RP':>14}{'  gate nyala':<14}{'bln ke':>7}"
      f"{'  bottom':<13}{'  gate vs bottom':>17}")
print("-" * 118)
for dt, pr, st in peaks:
    bd, bp, ongoing = bottom_after(dt, pr)
    w = df[(df["date"] > dt) & (df["date"] <= (bd if not ongoing else LAST) + pd.Timedelta(days=200))]
    w = w.dropna(subset=["realized_price"])
    below = w[w["btc_price"] < w["realized_price"]]
    if len(below) == 0:
        print(f"{str(dt.date()):<13}{'TIDAK PERNAH < RP':<40}")
        gate_rows.append(dict(peak=dt.date(), first_below_rp=None, month_first_below=None,
                              longest_streak_days=0, total_days_below=0,
                              gate_date=None, gate_month=None, bottom=bd.date(),
                              gate_minus_bottom_days=None))
        continue
    fb = below["date"].iloc[0]
    m_fb = (fb - dt).days / 30.44
    # streak terpanjang di bawah RP
    flag = (w["btc_price"] < w["realized_price"]).values
    best = cur = 0
    for v in flag:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    total_below = int(flag.sum())
    # gate lantai waktu
    g = w[(w["date"] >= dt + pd.DateOffset(months=9)) & (w["btc_price"] < w["realized_price"])]
    if len(g):
        gd = g["date"].iloc[0]
        m_g = (gd - dt).days / 30.44
        rel = (gd - bd).days
        rel_s = f"{'+' if rel>0 else ''}{rel}d ({rel/30.44:+.1f}b)"
    else:
        gd, m_g, rel, rel_s = None, np.nan, None, "TIDAK NYALA"
    print(f"{str(dt.date()):<13}{str(fb.date()):<13}{m_fb:>7.1f}{best:>11}d"
          f"{total_below:>13}d  {str(gd.date()) if gd is not None else 'NONE':<14}"
          f"{m_g:>7.1f}{'  '+str(bd.date()):<13}{rel_s:>17}")
    gate_rows.append(dict(peak=dt.date(), first_below_rp=fb.date(),
                          month_first_below=round(m_fb, 1), longest_streak_days=best,
                          total_days_below=total_below,
                          gate_date=(gd.date() if gd is not None else None),
                          gate_month=(round(m_g, 1) if gd is not None else None),
                          bottom=bd.date(), gate_minus_bottom_days=rel))

pd.concat([res.set_index("peak"), pd.DataFrame(gate_rows).set_index("peak")], axis=1)\
  .reset_index().to_csv(rf"{OUTDIR}\events_peak_to_bottom_duration.csv", index=False)

print("\nBaca 'gate vs bottom': negatif = gate nyala SEBELUM bottom (beli masih kena")
print("penurunan lanjutan); positif = gate nyala SESUDAH bottom (telat, sebagian rally hilang).")

# --- SENSITIVITAS: peak C2 = Apr 2021 --------------------------------------
print("\n" + "=" * 100)
print("SENSITIVITAS -- kalau peak siklus 2021 dipilih local high APR 2021 (bukan Nov 2021)")
print("=" * 100)
w = df[(df["date"] >= "2021-03-01") & (df["date"] <= "2021-05-31")]
apr_d = w.loc[w["btc_price"].idxmax(), "date"]
apr_p = w.loc[w["btc_price"].idxmax(), "btc_price"]
bd = pd.Timestamp("2022-11-21")
bp = df.loc[df["date"] == bd, "btc_price"].iloc[0]
days_apr = (bd - apr_d).days
print(f"Peak Apr 2021 = {apr_d.date()}  ${apr_p:,.2f}  ->  bottom {bd.date()} ${bp:,.2f}")
print(f"Durasi = {days_apr} hari = {days_apr/30.44:.1f} bulan "
      f"(vs {(bd-pd.Timestamp('2021-11-08')).days/30.44:.1f} bulan pakai peak Nov 2021)")
lo, hi = main["months"].min(), main["months"].max()
inside = lo <= days_apr / 30.44 <= hi
print(f"Rentang 3 cycle utama = {lo:.1f}-{hi:.1f} bulan  ->  "
      f"varian Apr 2021 {'MASIH DI DALAM' if inside else 'DI LUAR'} rentang")
g2 = df[(df["date"] >= apr_d + pd.DateOffset(months=9)) & (df["date"] <= bd)]
g2 = g2[g2["btc_price"] < g2["realized_price"]]
if len(g2):
    print(f"Gate lantai waktu varian Apr-2021 nyala {g2['date'].iloc[0].date()} "
          f"= {(g2['date'].iloc[0]-bd).days}d relatif bottom "
          f"(vs pakai peak Nov 2021 lihat tabel di atas)")

# --- POSISI SEKARANG --------------------------------------------------------
print("\n" + "=" * 100)
print("POSISI SEKARANG (per tanggal data terakhir)")
print("=" * 100)
cur_peak = pd.Timestamp("2025-10-06")
last = df.iloc[-1]
months_since = (LAST - cur_peak).days / 30.44
print(f"Peak siklus: {cur_peak.date()}  ${df.loc[df['date']==cur_peak,'btc_price'].iloc[0]:,.0f}")
print(f"Data terakhir {LAST.date()}: harga ${last['btc_price']:,.0f} | RP ${last['realized_price']:,.0f}"
      f" | STH RP ${last['sth_cost_basis']:,.0f}")
print(f"Bulan sejak peak = {months_since:.1f}  (gate lantai waktu butuh >=9.0)")
print(f"Syarat close < RP saat ini: {'TERPENUHI' if last['btc_price']<last['realized_price'] else 'BELUM'}")
print(f"Proyeksi jendela bottom dari 3 cycle utama ({lo:.1f}-{hi:.1f} bln sejak peak): "
      f"{(cur_peak+pd.Timedelta(days=lo*30.44)).date()} s/d {(cur_peak+pd.Timedelta(days=hi*30.44)).date()}")
print(f"  (kalau observasi 2011 {early['months'].iloc[0]:.1f} bln ikut dihitung, batas bawah "
      f"jadi {(cur_peak+pd.Timedelta(days=early['months'].iloc[0]*30.44)).date()})"
      if len(early) else "")

print("\nSelesai. CSV: events_peak_to_bottom_duration.csv")
