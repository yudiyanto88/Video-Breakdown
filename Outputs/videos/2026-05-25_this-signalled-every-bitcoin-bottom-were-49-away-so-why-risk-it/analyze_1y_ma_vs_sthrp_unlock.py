"""
VALIDASI 5 - "1-year moving average" pembicara vs aturan unlock framework (STH RP cross RP)

Klaim B9 [11:01]-[11:11]: "until we break that kind of one-year moving average around
95 and a half thousand dollars ish... we can't concretely say that this bear market
is finished."

Nilai untuk kita: Decision Framework v2 sec.0 punya aturan unlock sendiri - STH RP
(sth_cost_basis) cross NAIK melewati RP (realized_price) - yang statusnya MASIH PENDING
VALIDASI. Head-to-head ini punya nilai terlepas dari kualitas argumen videonya.

Yang diuji:
1. ma365 = SMA365(btc_price) vs kolom siap pakai 50_wma (350 hari). Sama atau beda?
2. Per bear (2011, 2015, 2018-19, 2022-23): tanggal reclaim pertama price > MA yang
   BERTAHAN >=7 hari. Berapa hari sesudah bear low, berapa % harga sudah naik dari low.
3. Head-to-head: tanggal sth_cost_basis cross naik melewati realized_price (aturan
   framework), perlakuan konfirmasi 7 hari yang SAMA supaya adil.
4. Whipsaw count: berapa kali price cross naik MA lalu jatuh lagi ke bawah dalam <=30
   hari, sepanjang regime bear. Ini menentukan gate vs context.
5. Status sekarang.

House rigor (CLAUDE.md "STANDAR VALIDASI"):
1. Definisi event eksplisit (cross + konfirmasi 7 hari + regime bear didefinisikan di depan).
2. n dilaporkan total + per cycle. n di sini KECIL (4 bear) - disebut tebal di kesimpulan.
3. Anti lookahead: konfirmasi ">=7 hari" baru DIKETAHUI di hari ke-7. Dilaporkan DUA
   tanggal: tanggal cross (hindsight) dan tanggal actionable (cross + 6 hari), plus
   harga & upside di masing-masing.
4. Independensi: 4 bear = 4 observasi. Tidak ada klaim statistik.
5. Data mulai belakangan: btc_price, realized_price, sth_cost_basis semua 2010-07-17 ->
   SMA365 baru siap 2011-07-16, jadi bear low 2011-11-18 masih tercakup.
6. Tidak ada grid search: konfirmasi 7 hari & whipsaw 30 hari ditetapkan di depan, hanya
   satu varian masing-masing. Perbandingan 50_wma vs SMA365 = cek definisi, bukan tuning.

Output: events_1y_ma_vs_sthrp_unlock.csv
"""

import pandas as pd
import numpy as np
import os

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = os.path.dirname(os.path.abspath(__file__))
NL = "\n"

# ---- PARAMETER DITETAPKAN DI DEPAN -----------------------------------------
CONFIRM  = 7    # hari bertahan di atas garis supaya reclaim dianggap sah
WHIP_WIN = 30   # cross naik lalu balik ke bawah dalam <=30 hari = whipsaw

BEAR_LOWS = {"bear-2011": "2011-11-18", "bear-2015": "2015-01-14",
             "bear-2018": "2018-12-14", "bear-2022": "2022-11-21"}
BEAR_LOWS = {k: pd.Timestamp(v) for k, v in BEAR_LOWS.items()}
PEAKS = [pd.Timestamp(d) for d in
         ["2011-06-08", "2013-11-30", "2017-12-16", "2021-11-08", "2025-10-06"]]
NEXT_PEAK = {"bear-2011": pd.Timestamp("2013-11-30"), "bear-2015": pd.Timestamp("2017-12-16"),
             "bear-2018": pd.Timestamp("2021-11-08"), "bear-2022": pd.Timestamp("2025-10-06")}
LOW_UNCONF = pd.Timestamp("2026-06-30")   # BELUM terkonfirmasi

print("=" * 108)
print("VALIDASI 5 - 1Y MOVING AVERAGE (klaim B9) vs ATURAN UNLOCK FRAMEWORK (STH RP cross RP)")
print("=" * 108)

df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 0].reset_index(drop=True)
df["ma365"] = df["btc_price"].rolling(365).mean()

NEEDED = ["btc_price", "ma365", "50_wma", "realized_price", "sth_cost_basis", "lth_cost_basis"]
print(NL + "-- 0. KETERSEDIAAN DATA --")
for c in NEEDED:
    nn = df.loc[df[c].notna(), "date"]
    print(f"  {c:<16} {nn.min().date()} .. {nn.max().date()}   n={int(df[c].notna().sum())}")

an = df.dropna(subset=NEEDED).reset_index(drop=True)
print(NL + f"  Rentang analisis: {an.date.min().date()} .. {an.date.max().date()}  n={len(an)} hari")
print("  CATATAN data mulai belakangan: SMA365 butuh warm-up 365 hari dari 2010-07-17,")
print("  jadi seri baru siap 2011-07-16. Bear low 2011-11-18 MASIH tercakup -> 4 bear penuh.")

print(NL + "-- SANITY CHECK ANCHOR 2026-05-25 --")
a = an.loc[an.date == "2026-05-25"].iloc[0]
for col, exp in [("btc_price", 77172), ("realized_price", 54172), ("sth_cost_basis", 77910),
                 ("lth_cost_basis", 48650), ("50_wma", 94325)]:
    ok = "OK" if abs(a[col] - exp) / abs(exp) < 0.02 else "MISMATCH"
    print(f"  {col:<16} = {a[col]:>12,.2f}   (anchor {exp:,})  [{ok}]")
print(f"  ma365 (SMA365)   = {a['ma365']:>12,.2f}   <- pembicara bilang '95,5 ribu-an'")
print(f"  Selisih ma365 vs 50_wma di tanggal video: {(a['ma365']/a['50_wma']-1)*100:+.2f}%")

# =============================================================================
# 1. SMA365 vs 50_wma - definisi mana yang dipakai pembicara?
# =============================================================================
print(NL + "=" * 108)
print("1. SMA365 (365 hari) vs kolom 50_wma (350 hari) - apakah menghasilkan tanggal yang sama?")
print("=" * 108)
d = (an["ma365"] / an["50_wma"] - 1) * 100
print(f"  Selisih relatif ma365 vs 50_wma: median {d.median():+.2f}%  p5 {d.quantile(.05):+.2f}%  "
      f"p95 {d.quantile(.95):+.2f}%  maks abs {d.abs().max():.2f}%")
print(f"  Korelasi Spearman level: {an['ma365'].corr(an['50_wma'], method='spearman'):+.4f}")
above_a = (an["btc_price"] > an["ma365"])
above_b = (an["btc_price"] > an["50_wma"])
print(f"  Hari 'harga di atas garis': ma365 {int(above_a.sum())} hari, 50_wma {int(above_b.sum())} hari")
print(f"  Kesepakatan harian posisi di atas/bawah garis: {(above_a == above_b).mean()*100:.2f}% dari {len(an)} hari")

# =============================================================================
# HELPER
# =============================================================================
def sustained_cross_up(a_ser, b_ser, dates, start_idx, confirm=CONFIRM):
    """Cross NAIK pertama a>b sesudah start_idx yang bertahan >=confirm hari berturut.
    Return (idx_cross, idx_confirm) atau (None, None)."""
    a = a_ser.values; b = b_ser.values
    n = len(a)
    for i in range(max(start_idx, 1), n):
        if a[i] > b[i] and a[i-1] <= b[i-1]:
            j = i + confirm - 1
            if j >= n:
                return None, None
            if all(a[k] > b[k] for k in range(i, j + 1)):
                return i, j
    return None, None

def count_whipsaw(a_ser, b_ser, mask, win=WHIP_WIN):
    """Jumlah cross NAIK a>b yang balik ke bawah dalam <=win hari, dihitung hanya kalau
    HARI SEBELUM cross (i-1) ada di dalam mask (regime bear).

    PENTING: regime diuji di i-1, BUKAN di i. Kalau diuji di i, aturan framework
    (STH RP cross RP) otomatis nol-cross di regime-B ('STH RP < RP') secara definisi -
    artefak, bukan temuan. Menguji di i-1 = 'apakah pasar sedang di regime bear tepat
    sebelum cross terjadi' dan berlaku adil untuk ketiga aturan.
    Return (n_whipsaw, n_cross, list)."""
    a = a_ser.values; b = b_ser.values; m = mask.values
    n = len(a); ws = []; crosses = 0
    for i in range(1, n):
        if a[i] > b[i] and a[i-1] <= b[i-1] and m[i-1]:
            crosses += 1
            back = None
            for k in range(i + 1, min(i + win + 1, n)):
                if a[k] <= b[k]:
                    back = k; break
            if back is not None:
                ws.append((i, back, back - i))
    return len(ws), crosses, ws

px = an.set_index("date")["btc_price"]

# =============================================================================
# 2 & 3. RECLAIM 1Y-MA vs ATURAN UNLOCK FRAMEWORK, PER BEAR
# =============================================================================
print(NL + "=" * 108)
print("2+3. HEAD-TO-HEAD PER BEAR - reclaim 1Y-MA vs STH RP cross naik RP")
print("=" * 108)
print(f"  Definisi (ditetapkan di depan): cross NAIK pertama SESUDAH bear low yang bertahan")
print(f"  >=  {CONFIRM} hari berturut-turut. ANTI-LOOKAHEAD: tanggal cross baru bisa dikonfirmasi")
print(f"  di hari ke-{CONFIRM}, jadi kolom 'actionable' = tanggal cross + {CONFIRM-1} hari - itu yang")
print("  dipakai untuk menghitung upside yang hilang.")

RULES = [
    ("1Y_MA_sma365", an["btc_price"], an["ma365"], "price > SMA365 (klaim pembicara)"),
    ("1Y_MA_50wma",  an["btc_price"], an["50_wma"], "price > 50_wma (350 hari)"),
    ("FW_STHRP_x_RP", an["sth_cost_basis"], an["realized_price"], "STH RP > RP (aturan framework)"),
]

rows = []
for bear, low in BEAR_LOWS.items():
    idx_low = int(an.index[an.date == low][0]) if (an.date == low).any() else \
              int(an.index[an.date >= low][0])
    p_low = float(an["btc_price"].iloc[idx_low])
    peak = NEXT_PEAK[bear]
    p_peak = float(px.asof(peak))
    print(NL + f"  --- {bear}  low {low.date()} @ ${p_low:,.0f}  "
          f"(puncak cycle berikutnya {peak.date()} @ ${p_peak:,.0f}) ---")
    print(f"    {'aturan':<15}{'cross':<12}{'actionable':<12}{'hari dr low':>12}"
          f"{'harga act.':>12}{'naik dr low':>12}{'sisa ke peak':>14}")
    for name, A, B, desc in RULES:
        i, j = sustained_cross_up(A, B, an["date"], idx_low)
        if i is None:
            print(f"    {name:<15}{'TIDAK ADA cross yang bertahan sesudah low':<50}")
            rows.append(dict(bear=bear, rule=name, cross_date=None, actionable_date=None))
            continue
        d_cross = an["date"].iloc[i]; d_act = an["date"].iloc[j]
        p_act = float(an["btc_price"].iloc[j])
        up = (p_act / p_low - 1) * 100
        rem = (p_peak / p_act - 1) * 100
        print(f"    {name:<15}{str(d_cross.date()):<12}{str(d_act.date()):<12}"
              f"{(d_act-low).days:>12}{p_act:>12,.0f}{up:>11.1f}%{rem:>13.1f}%")
        rows.append(dict(bear=bear, rule=name, low_date=low.date(), low_price=round(p_low, 2),
                         cross_date=d_cross.date(), actionable_date=d_act.date(),
                         days_after_low=(d_act - low).days, price_actionable=round(p_act, 2),
                         upside_from_low_pct=round(up, 1),
                         remaining_to_peak_pct=round(rem, 1),
                         next_peak=peak.date(), next_peak_price=round(p_peak, 2)))

EV = pd.DataFrame(rows)

print(NL + "  RINGKASAN HEAD-TO-HEAD (mana yang lebih dulu, berapa hari, berapa % upside hilang):")
print(f"    {'bear':<12}{'1Y-MA act.':<13}{'FW act.':<13}{'selisih hari':>13}"
      f"{'naik dr low 1Y-MA':>19}{'naik dr low FW':>16}{'selisih upside':>16}")
comp = []
for bear in BEAR_LOWS:
    r1 = EV[(EV.bear == bear) & (EV.rule == "1Y_MA_sma365")]
    r2 = EV[(EV.bear == bear) & (EV.rule == "FW_STHRP_x_RP")]
    if len(r1) == 0 or len(r2) == 0 or r1.iloc[0].actionable_date is None or r2.iloc[0].actionable_date is None:
        print(f"    {bear:<12} (tidak lengkap)"); continue
    r1 = r1.iloc[0]; r2 = r2.iloc[0]
    dd = (pd.Timestamp(str(r1.actionable_date)) - pd.Timestamp(str(r2.actionable_date))).days
    who = "FW duluan" if dd > 0 else ("1Y-MA duluan" if dd < 0 else "sama hari")
    print(f"    {bear:<12}{str(r1.actionable_date):<13}{str(r2.actionable_date):<13}{dd:>13}"
          f"{r1.upside_from_low_pct:>18.1f}%{r2.upside_from_low_pct:>15.1f}%"
          f"{r1.upside_from_low_pct - r2.upside_from_low_pct:>15.1f}%   ({who})")
    comp.append(dict(bear=bear, days_1yma_minus_fw=dd,
                     up_1yma=r1.upside_from_low_pct, up_fw=r2.upside_from_low_pct,
                     upside_gap_pct=round(r1.upside_from_low_pct - r2.upside_from_low_pct, 1),
                     rem_1yma=r1.remaining_to_peak_pct, rem_fw=r2.remaining_to_peak_pct))
CMP = pd.DataFrame(comp)
if len(CMP):
    print(NL + f"    n = {len(CMP)} bear (SEMPAT SEMUA 4 kalau lengkap). "
          f"FW lebih dulu di {int((CMP.days_1yma_minus_fw>0).sum())}/{len(CMP)} bear.")
    print(f"    Median selisih hari (1Y-MA - FW) : {CMP.days_1yma_minus_fw.median():+.0f} hari")
    print(f"    Median upside dari low saat sinyal : 1Y-MA {CMP.up_1yma.median():.1f}%  vs  FW {CMP.up_fw.median():.1f}%")
    print(f"    Median sisa upside ke puncak cycle : 1Y-MA {CMP.rem_1yma.median():.1f}%  vs  FW {CMP.rem_fw.median():.1f}%")

# =============================================================================
# 4. WHIPSAW
# =============================================================================
print(NL + "=" * 108)
print("4. WHIPSAW - cross naik lalu balik ke bawah dalam <=30 hari, di dalam regime bear")
print("=" * 108)
regimes = {
    "regime-A (harga < RP)":       an["btc_price"] < an["realized_price"],
    "regime-B (STH RP < RP, 'struktur T')": an["sth_cost_basis"] < an["realized_price"],
    "regime-C (gabungan A atau B)": (an["btc_price"] < an["realized_price"]) |
                                    (an["sth_cost_basis"] < an["realized_price"]),
}
for rn, mask in regimes.items():
    print(NL + f"  {rn}: {int(mask.sum())} hari ({mask.mean()*100:.1f}% dari {len(an)})")
    for name, A, B, desc in RULES:
        nw, nc, ws = count_whipsaw(A, B, mask)
        rate = (nw / nc * 100) if nc else np.nan
        print(f"    {name:<15} cross naik di regime: {nc:>3}   whipsaw <=30d: {nw:>3}   "
              f"({rate:5.1f}%)" if nc else f"    {name:<15} tidak ada cross di regime ini")

print(NL + "  Detail whipsaw 1Y-MA (SMA365) di regime-C:")
nw, nc, ws = count_whipsaw(an["btc_price"], an["ma365"], regimes["regime-C (gabungan A atau B)"])
for i, k, gap in ws:
    print(f"    cross {an['date'].iloc[i].date()} @ ${an['btc_price'].iloc[i]:,.0f}  ->  "
          f"balik ke bawah {an['date'].iloc[k].date()} ({gap} hari)")
print(NL + "  Detail whipsaw aturan framework (STH RP x RP) di regime-C:")
nw2, nc2, ws2 = count_whipsaw(an["sth_cost_basis"], an["realized_price"],
                              regimes["regime-C (gabungan A atau B)"])
if not ws2:
    print("    (tidak ada)")
for i, k, gap in ws2:
    print(f"    cross {an['date'].iloc[i].date()}  ->  balik ke bawah {an['date'].iloc[k].date()} ({gap} hari)")

# whipsaw sepanjang SELURUH sejarah (konteks tambahan, bukan gate)
print(NL + "  SEMUA cross naik STH RP melewati RP sepanjang sejarah (aturan framework):")
A_ = an["sth_cost_basis"].values; B_ = an["realized_price"].values
for i in range(1, len(an)):
    if A_[i] > B_[i] and A_[i-1] <= B_[i-1]:
        back = None
        for k in range(i+1, len(an)):
            if A_[k] <= B_[k]:
                back = k; break
        dur = "masih bertahan sampai akhir data" if back is None else               f"balik ke bawah {an['date'].iloc[back].date()} ({(an['date'].iloc[back]-an['date'].iloc[i]).days} hari)"
        print(f"    cross {an['date'].iloc[i].date()}  harga ${an['btc_price'].iloc[i]:,.0f}  ->  {dur}")

print(NL + "  Konteks - whipsaw sepanjang SELURUH sejarah (tanpa filter regime):")
allmask = pd.Series(True, index=an.index)
for name, A, B, desc in RULES:
    nw, nc, ws = count_whipsaw(A, B, allmask)
    print(f"    {name:<15} cross naik: {nc:>3}   whipsaw <=30d: {nw:>3}   ({nw/nc*100 if nc else float('nan'):5.1f}%)")

# =============================================================================
# 5. STATUS SEKARANG
# =============================================================================
print(NL + "=" * 108)
print("5. STATUS DI HARI TERAKHIR DATA")
print("=" * 108)
last = an.iloc[-1]
print(f"  Tanggal        : {last.date.date()}")
print(f"  btc_price      : ${last.btc_price:,.0f}")
print(f"  SMA365 (ma365) : ${last.ma365:,.0f}   harga {'DI ATAS' if last.btc_price>last.ma365 else 'DI BAWAH'} "
      f"({(last.btc_price/last.ma365-1)*100:+.1f}%)")
print(f"  50_wma         : ${last['50_wma']:,.0f}   harga {'DI ATAS' if last.btc_price>last['50_wma'] else 'DI BAWAH'} "
      f"({(last.btc_price/last['50_wma']-1)*100:+.1f}%)")
print(f"  realized_price : ${last.realized_price:,.0f}")
print(f"  sth_cost_basis : ${last.sth_cost_basis:,.0f}   -> aturan unlock framework "
      f"(STH RP > RP) : {'NYALA' if last.sth_cost_basis>last.realized_price else 'BELUM nyala'} "
      f"(rasio {last.sth_cost_basis/last.realized_price:.3f})")
print(f"  lth_cost_basis : ${last.lth_cost_basis:,.0f}")
print(NL + "  *** DUA ATURAN SEDANG BERTENTANGAN DI HARI TERAKHIR DATA ***")
print(f"    Aturan pembicara (price > 1Y MA) : BELUM - harga ${last.btc_price:,.0f} vs "
      f"SMA365 ${last.ma365:,.0f}, butuh +{(last.ma365/last.btc_price-1)*100:.1f}%")
print(f"    Aturan framework (STH RP > RP)   : NYALA sejak cross terakhir (lihat daftar di section 4)")
# --- 5b. Apakah aturan unlock framework sempat RE-ARM di bear berjalan? ---
print(NL + "  -- 5b. APAKAH ATURAN FRAMEWORK SEMPAT 'RE-ARM' DI BEAR BERJALAN? --")
cur = an[an.date >= PEAKS[-1]]
ratio = cur["sth_cost_basis"] / cur["realized_price"]
imin = ratio.idxmin()
print(f"    Sejak cycle peak {PEAKS[-1].date()} (n={len(cur)} hari):")
print(f"      hari dengan STH RP < RP  : {int((cur['sth_cost_basis'] < cur['realized_price']).sum())}")
print(f"      hari dengan harga < RP   : {int((cur['btc_price'] < cur['realized_price']).sum())}")
print(f"      rasio STH RP / RP MINIMUM: {ratio.min():.3f} pada {an['date'].loc[imin].date()}")
print("    -> STH RP TIDAK PERNAH turun ke bawah RP di bear ini. Aturan unlock framework")
print("       masih 'ON' terus sejak cross 2023-03-05 dan BELUM PERNAH re-arm, jadi saat ini")
print("       ia tidak membawa informasi apapun tentang selesai/belumnya bear berjalan.")
print("    Sebaran hari STH RP < RP per tahun (seluruh sejarah):")
b = an[an["sth_cost_basis"] < an["realized_price"]]
print("      " + "  ".join(f"{y}:{n}" for y, n in b.groupby(b.date.dt.year).size().items()))

print(NL + f"  Low sementara 2026-06-30 @ ${px.asof(LOW_UNCONF):,.0f} - BELUM TERKONFIRMASI,")
print("  tidak dipakai sebagai bukti apapun di angka-angka di atas.")
print(f"  Kenaikan dari low sementara ke hari terakhir data: "
      f"{(last.btc_price/px.asof(LOW_UNCONF)-1)*100:+.1f}%")

# ---- CSV --------------------------------------------------------------------
out = os.path.join(OUTDIR, "events_1y_ma_vs_sthrp_unlock.csv")
EV.to_csv(out, index=False)
print(NL + f"CSV event disimpan : {out}   (n baris = {len(EV)})")
if len(CMP):
    out2 = os.path.join(OUTDIR, "events_1y_ma_vs_sthrp_headtohead.csv")
    CMP.to_csv(out2, index=False)
    print(f"CSV head-to-head   : {out2}")
print(NL + "SELESAI.")
