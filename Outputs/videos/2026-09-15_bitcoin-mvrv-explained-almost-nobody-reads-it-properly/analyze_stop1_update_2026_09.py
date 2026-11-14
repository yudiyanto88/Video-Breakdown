# -*- coding: utf-8 -*-
"""
V2 - Update fakta STOP-1 dengan data s/d 2026-09-15 (deskriptif, BUKAN uji sinyal baru).

Semua definisi dipakai ulang persis dari validasi CLOSED:
  - struktur T = sth_cost_basis < realized_price  (findings_unlock_reachability_struktur_n, 08-25)
  - kandidat (i)  : close > sth_cost_basis >=21 hari berturut (fire saat streak == 21), cooldown 180
  - kandidat (ii) : close > sth_cost_basis >=3 hari (streak == 3) DAN slope30 sth_cost_basis > 0, cooldown 180
  - MVRV Momentum : gap = SMA30(mvrv_ratio) - SMA30(SMA30); bullish cross valid = >=7 hari negatif
                    sebelumnya + >=7 hari >=0 sesudahnya (KB 6C.1); keputusan di hari ke-7
  - zona DF v2 sec.1; gate K2 = sth_mvrv di band [0.80, 0.97)  (btlib G1)
  - Signal D = close > sth_cost_basis >=3 hari berturut
  - event BREAK 2026-04-26 (findings_sth_rp_resistance_bear 08-04): 12 hari close > STH RP mulai 2026-05-06

Pertanyaan:
 (a) hari struktur T sejak peak 2025-10-06, min STH RP/RP
 (b) close pertama > STH RP episode sekarang, streak s/d 09-15, kandidat (i)/(ii), close vs 200_dma
 (c) gap MVRV Momentum: tanda, tanggal cross bullish, hari bertahan, valid?
 (d) max sth_mvrv & hari > 1.0 selama 2026-04-20..2026-05-31; + semua episode sth_mvrv > 1 sejak peak
 (e) min P/RP & min lth_mvrv sejak peak
 (f) zona DF v2 & status gate K2 per 2026-09-15
Output print ASCII saja.
"""
import numpy as np
import pandas as pd

MASTER = "D:/Claude Code/Projects/Onchain-Dashboard/data_master_all_metrics.csv"
PEAK = pd.Timestamp("2025-10-06")

df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "sth_cost_basis", "realized_price", "200_dma"]).reset_index(drop=True)
df = df[df["btc_price"] > 0].reset_index(drop=True).copy()
LAST = df["date"].max()
N = len(df)
print("Data s/d", LAST.date())

price = df["btc_price"].values
sth = df["sth_cost_basis"].values
rp = df["realized_price"].values
dates = df["date"]

df["struct_T"] = df["sth_cost_basis"] < df["realized_price"]
df["ratio_sthrp_rp"] = df["sth_cost_basis"] / df["realized_price"]
above = price > sth
streak = np.zeros(N, dtype=int)
for i in range(N):
    streak[i] = (streak[i - 1] + 1 if i > 0 else 1) if above[i] else 0
df["streak"] = streak
df["slope30"] = df["sth_cost_basis"] - df["sth_cost_basis"].shift(30)

W = df[df["date"] >= PEAK]

# (a)
print("\n(a) STRUKTUR sejak peak %s (%d hari)" % (PEAK.date(), len(W)))
im = W["ratio_sthrp_rp"].idxmin()
print("  hari struktur T = %d" % int(W["struct_T"].sum()))
print("  min STH RP/RP = %.3f pada %s | nilai 09-15 = %.3f" % (
    df.at[im, "ratio_sthrp_rp"], df.at[im, "date"].date(), df.iloc[-1]["ratio_sthrp_rp"]))

# (b)
print("\n(b) EPISODE CLOSE > STH RP SEKARANG")
k = N - 1
if streak[k] > 0:
    start = k - streak[k] + 1
    print("  close pertama > STH RP episode sekarang = %s | streak s/d %s = %d hari" % (
        dates.iloc[start].date(), LAST.date(), streak[k]))
else:
    start = None
    print("  harga di bawah STH RP per %s" % LAST.date())
# episode sebelumnya sejak peak
eps = []
i = 0
Wi = W.index
for j in Wi:
    if streak[j] == 1:
        e = j
        while e + 1 < N and streak[e + 1] > 0:
            e += 1
        eps.append((dates.iloc[j].date(), dates.iloc[e].date(), e - j + 1))
print("  semua episode close > STH RP sejak peak (mulai, selesai, hari):")
for e in eps:
    print("     ", e)


def cooldown(mask, cd=180):
    out, last = [], None
    for i in np.where(mask)[0]:
        d = dates.iloc[i]
        if last is not None and (d - last).days < cd:
            continue
        out.append(i)
        last = d
    return out


ci = cooldown(streak == 21)
cii = cooldown((streak == 3) & (df["slope30"].values > 0))
print("  kandidat (i)  fire (cooldown 180) sejak peak:", [str(dates.iloc[i].date()) for i in ci if dates.iloc[i] >= PEAK] or "TIDAK ADA")
print("  kandidat (ii) fire (cooldown 180) sejak peak:", [str(dates.iloc[i].date()) for i in cii if dates.iloc[i] >= PEAK] or "TIDAK ADA")
if start is not None:
    s3 = start + 2
    if s3 < N:
        print("  di hari streak==3 (%s): slope30 STH RP = %+.0f USD -> (ii) %s" % (
            dates.iloc[s3].date(), df.at[s3, "slope30"], "NYALA" if df.at[s3, "slope30"] > 0 else "TIDAK nyala (definisi persis: streak==3)"))
    ep = df.iloc[start:]
    pos = ep[ep["slope30"] > 0]
    print("  [info, bukan definisi (ii)] hari pertama di episode ini dgn streak>=3 & slope30>0: %s" % (
        pos[pos["streak"] >= 3]["date"].iloc[0].date() if len(pos[pos["streak"] >= 3]) else "belum ada"))
    print("  slope30 STH RP per %s = %+.0f USD" % (LAST.date(), df.iloc[-1]["slope30"]))
last = df.iloc[-1]
print("  close vs 200_dma per %s: %s vs %s (%s)" % (LAST.date(), format(last["btc_price"], ",.0f"),
      format(last["200_dma"], ",.0f"), "DI ATAS" if last["btc_price"] > last["200_dma"] else "DI BAWAH"))
a200 = (df["btc_price"] > df["200_dma"]).values
st2 = 0
for j in range(N - 1, -1, -1):
    if a200[j]:
        st2 += 1
    else:
        break
if st2:
    print("  close > 200_dma sejak %s (%d hari berturut)" % (dates.iloc[N - st2].date(), st2))
print("  STH RP per 09-15 = %s | RP = %s" % (format(last["sth_cost_basis"], ",.0f"), format(last["realized_price"], ",.0f")))

# (c)
print("\n(c) MVRV MOMENTUM (versi kita, KB 6C.1)")
fast = df["mvrv_ratio"].rolling(30).mean()
slow = fast.rolling(30).mean()
gap = (fast - slow).values
sign = np.sign(gap)
print("  gap per %s = %+.5f (%s)" % (LAST.date(), gap[-1], "POSITIF" if gap[-1] >= 0 else "NEGATIF"))
# cari cross terakhir (perubahan tanda)
j = N - 1
while j > 0 and (gap[j - 1] >= 0) == (gap[j] >= 0):
    j -= 1
prev_run = 0
t = j - 1
while t >= 0 and not np.isnan(gap[t]) and (gap[t] >= 0) == (gap[j - 1] >= 0):
    prev_run += 1
    t -= 1
held = N - j
print("  cross terakhir = %s (%s) | bertahan %d hari s/d %s | regime sebelumnya %d hari" % (
    dates.iloc[j].date(), "bullish" if gap[j] >= 0 else "bearish", held, LAST.date(), prev_run))
print("  valid (>=7 hari bertahan & regime sebelumnya >=7)? %s | tanggal keputusan (hari ke-7) = %s" % (
    "YA" if (held >= 7 and prev_run >= 7) else "TIDAK", dates.iloc[j + 6].date() if held >= 7 else "n/a"))
print("  gap maks sejak cross = %+.5f pada %s" % (np.nanmax(gap[j:]), dates.iloc[j + int(np.nanargmax(gap[j:]))].date()))
# riwayat cross sejak peak
chg = []
for i in range(1, N):
    if dates.iloc[i] < PEAK - pd.Timedelta(days=30) or np.isnan(gap[i]) or np.isnan(gap[i - 1]):
        continue
    if (gap[i] >= 0) != (gap[i - 1] >= 0):
        chg.append((str(dates.iloc[i].date()), "bull" if gap[i] >= 0 else "bear"))
print("  semua pergantian tanda gap sejak 2025-09-06:", chg)
# hari terakhir gap positif sebelum episode ini (untuk "hijau pertama >1 tahun")
lastpos = [i for i in range(j) if not np.isnan(gap[i]) and gap[i] >= 0]
print("  hari positif terakhir sebelum cross ini = %s" % (dates.iloc[lastpos[-1]].date() if lastpos else "n/a"))

# (d)
print("\n(d) STH-MVRV")
w = df[(df["date"] >= "2026-04-20") & (df["date"] <= "2026-05-31")]
im = w["sth_mvrv"].idxmax()
print("  2026-04-20..2026-05-31: max sth_mvrv = %.4f pada %s | hari > 1.0 = %d dari %d" % (
    df.at[im, "sth_mvrv"], df.at[im, "date"].date(), int((w["sth_mvrv"] > 1.0).sum()), len(w)))
gt = (df["sth_mvrv"] > 1.0).values
print("  episode sth_mvrv > 1.0 sejak peak (mulai, selesai, hari, max):")
i = int(df.index[df["date"] >= PEAK][0])
while i < N:
    if gt[i]:
        s0 = i
        while i + 1 < N and gt[i + 1]:
            i += 1
        seg = df.iloc[s0:i + 1]
        print("     %s  %s  %3d  max %.4f" % (dates.iloc[s0].date(), dates.iloc[i].date(), i - s0 + 1, seg["sth_mvrv"].max()))
    i += 1
print("  sth_mvrv per 09-15 = %.4f | max sejak 2026-07-01 = %.4f" % (
    df.iloc[-1]["sth_mvrv"], df[df["date"] >= "2026-07-01"]["sth_mvrv"].max()))
print("  cek konsistensi: sth_mvrv vs price/sth_cost_basis per 09-15 = %.4f vs %.4f" % (
    df.iloc[-1]["sth_mvrv"], price[-1] / sth[-1]))

# (e)
print("\n(e) SEJAK PEAK")
W = df[df["date"] >= PEAK].copy()
W["p_rp"] = W["btc_price"] / W["realized_price"]
a = W["p_rp"].idxmin()
b = W["lth_mvrv"].idxmin()
print("  min P/RP = %.3f pada %s | min lth_mvrv = %.3f pada %s" % (
    W.at[a, "p_rp"], W.at[a, "date"].date(), W.at[b, "lth_mvrv"], W.at[b, "date"].date()))
print("  P/RP per 09-15 = %.3f | lth_mvrv per 09-15 = %.3f | mvrv_ratio = %.4f" % (
    W.iloc[-1]["p_rp"], W.iloc[-1]["lth_mvrv"], W.iloc[-1]["mvrv_ratio"]))

# (f)
print("\n(f) ZONA DF v2 & GATE K2 per", LAST.date())
r = df.iloc[-1]
m = r["price_at_aviv_mean"]
u = m + 0.5 * (r["price_at_aviv_plus_1_sigma"] - m)
s, R, L, P = r["sth_cost_basis"], r["realized_price"], r["lth_cost_basis"], r["btc_price"]
conv = abs(s - R) / R < 0.02 and abs(R - L) / R < 0.02
struct = "C" if conv else ("N" if s > R else "T")
if P >= u:
    z = "Z5"
elif struct == "C":
    z = "Z2" if P < m else "Z4"
elif struct == "N":
    z = "ZC" if P < R else ("ZD" if P < s else ("Z3" if P < m else "Z4"))
else:
    z = "Z1" if P < s else ("Z1b" if P < R else "Z2t")
print("  harga %s | STH RP %s | RP %s | LTH RP %s | AVIV Mean %s | AVIV Upper %s" % tuple(
    format(x, ",.0f") for x in [P, s, R, L, m, u]))
print("  struktur = %s | zona = %s" % (struct, z))
g1 = 0.80 <= r["sth_mvrv"] < 0.97
print("  gate K2 (sth_mvrv di [0.80, 0.97)): sth_mvrv = %.4f -> %s" % (r["sth_mvrv"], "DALAM band" if g1 else "DI LUAR band (di atas 0.97)" if r["sth_mvrv"] >= 0.97 else "DI LUAR band (di bawah 0.80)"))
print("  status unlock DF v2 (STH RP cross naik RP): mekanis tidak mungkin selama struktur N tanpa pernah T")
