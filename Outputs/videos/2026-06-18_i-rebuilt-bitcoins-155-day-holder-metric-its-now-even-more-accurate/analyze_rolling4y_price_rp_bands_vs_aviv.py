"""
V4 -- Quantile band rolling-4-tahun dari rasio Price/Realized Price,
sebagai analog fungsional AVIV Mean/Upper + batas bawah RP/CVDD.

KLAIM YANG DIUJI (Matt Crosby, 2026-06-18, [10:53]-[11:38], Figure 11):
  Band q05/q10/q20/q80/q90/q95 di sekitar filtered realized price;
  "these aren't repainting historically"; "right now we're in the bottom
  20th percentile ... at around $65,000"; batas atas "just around $130,000".

PRESEDEN YANG SUDAH CLOSED (window 1 tahun, basis sigma):
  Outputs/videos/2025-01-22_bitcoin-ath-what-next/findings_mvrv_rolling1y_vs_aviv.md
  -> "ballpark align tapi skala sigma tidak setara (~2:1), divergensi = artefak
      reaktivitas formula, tidak ada K-node baru". Di sini bedanya: window 4
      tahun dan basis QUANTILE (bukan sigma).

BATASAN: data kita = base "std" + realized price standar. Matt pakai filtered
  realized price (flt). Angka absolut TIDAK comparable; yang diuji metodologinya.

ANTI-LOOKAHEAD: quantile dihitung dari window rolling 1460 hari yang BERAKHIR
  di t-1 (shift(1) sebelum rolling), jadi band di hari t tidak memakai data t.
"""

import warnings

import numpy as np
import pandas as pd

warnings.simplefilter("ignore")

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
WIN    = 1460
QS     = [0.05, 0.10, 0.20, 0.80, 0.90, 0.95]

df = pd.read_csv(MASTER, parse_dates=["date"])
df = df[df["btc_price"].notna()].sort_values("date").reset_index(drop=True)

df["ratio"] = df["btc_price"] / df["realized_price"]
r_shift = df["ratio"].shift(1)
for q in QS:
    df[f"q{int(q*100):02d}"] = r_shift.rolling(WIN, min_periods=WIN).quantile(q) * df["realized_price"]

# persentil aktual harga hari itu terhadap window rolling 4 tahun (berakhir t-1)
pct = np.full(len(df), np.nan)
rv = df["ratio"].values
for i in range(WIN, len(df)):
    w = rv[i - WIN:i]
    pct[i] = (w < rv[i]).mean()
df["price_pct_4y"] = pct

# AVIV framework
df["aviv_mean_usd"]  = df["price_at_aviv_mean"]
df["aviv_upper_usd"] = df["price_at_aviv_mean"] + 0.5 * (df["price_at_aviv_plus_1_sigma"] - df["price_at_aviv_mean"])
df["aviv_1sig_usd"]  = df["price_at_aviv_plus_1_sigma"]

print("=" * 104)
print("V4  QUANTILE BAND ROLLING-4Y (Price/RP)  vs  AVIV MEAN/UPPER, RP, CVDD")
print("=" * 104)
print(f"Data {df['date'].min().date()} s/d {df['date'].max().date()}; band valid pertama "
      f"{df.loc[df['q90'].notna(), 'date'].min().date()} (warm-up {WIN} hari)")
print("Basis: realized price STANDAR (std). Matt pakai filtered RP -> angka absolut TIDAK comparable.")

# ---------------------------------------------------------------- (a) puncak
PEAKS = [("ATH 2017", "2017-12-17"), ("ATH Apr 2021", "2021-04-14"),
         ("ATH Nov 2021", "2021-11-08"), ("Peak Jul-Ags 2025", "2025-08-13"),
         ("Peak Okt 2025", "2025-10-06")]
print("\n" + "-" * 104)
print("(a) DI PUNCAK SIKLUS: harga vs band q90/q95 vs AVIV Upper (+0,5SD) vs AVIV +1SD")
print("-" * 104)
print(f"{'Event':<19} {'Tgl':>11} {'Price':>10} {'q90':>10} {'q95':>10} {'AVIVup':>10} {'AVIV+1sd':>10} | "
      f"{'q90/AVIVup':>10} {'q95/AVIV1sd':>11} {'pct harga':>9}")
for nm, dt in PEAKS:
    r = df[df["date"] <= dt].iloc[-1]
    if pd.isna(r["q90"]):
        print(f"{nm:<19} {str(r['date'].date()):>11} {r['btc_price']:>10,.0f}  band belum valid (warm-up)")
        continue
    print(f"{nm:<19} {str(r['date'].date()):>11} {r['btc_price']:>10,.0f} {r['q90']:>10,.0f} {r['q95']:>10,.0f} "
          f"{r['aviv_upper_usd']:>10,.0f} {r['aviv_1sig_usd']:>10,.0f} | "
          f"{r['q90']/r['aviv_upper_usd']:>10.2f} {r['q95']/r['aviv_1sig_usd']:>11.2f} "
          f"{r['price_pct_4y']:>9.3f}")

# ---------------------------------------------------------------- (b) bottom
BOTTOMS = [("Bottom 2018-12", "2018-12-14"), ("COVID 2020-03", "2020-03-12"),
           ("Bottom 2022-11", "2022-11-21"), ("Bottom-so-far 2026-06", "2026-06-30")]
print("\n" + "-" * 104)
print("(b) DI BEAR BOTTOM: harga vs band q05/q10/q20 vs Realized Price vs CVDD")
print("-" * 104)
print(f"{'Event':<22} {'Tgl':>11} {'Price':>10} {'q05':>10} {'q10':>10} {'q20':>10} {'RP':>10} {'CVDD':>9} | "
      f"{'P/RP':>6} {'P/CVDD':>7} {'pct':>6}")
for nm, dt in BOTTOMS:
    r = df[df["date"] <= dt].iloc[-1]
    print(f"{nm:<22} {str(r['date'].date()):>11} {r['btc_price']:>10,.0f} {r['q05']:>10,.0f} {r['q10']:>10,.0f} "
          f"{r['q20']:>10,.0f} {r['realized_price']:>10,.0f} {r['cvdd']:>9,.0f} | "
          f"{r['btc_price']/r['realized_price']:>6.2f} {r['btc_price']/r['cvdd']:>7.2f} "
          f"{r['price_pct_4y']:>6.3f}")

# ---------------------------------------------------------------- (c) 2026-06-16
print("\n" + "-" * 104)
print("(c) KLAIM VIDEO: 'harga ~$65k = persentil ~20' -- cek di data kita, 2026-06-16")
print("-" * 104)
r = df[df["date"] <= "2026-06-16"].iloc[-1]
print(f"  Tanggal {r['date'].date()}  harga ${r['btc_price']:,.0f}")
print(f"  Persentil rolling-4y aktual (Price/RP)  = {r['price_pct_4y']:.3f}  "
      f"({r['price_pct_4y']*100:.1f}th percentile)")
print(f"  Band: q05 ${r['q05']:,.0f} | q10 ${r['q10']:,.0f} | q20 ${r['q20']:,.0f} | "
      f"q80 ${r['q80']:,.0f} | q90 ${r['q90']:,.0f} | q95 ${r['q95']:,.0f}")
print(f"  Level framework: RP ${r['realized_price']:,.0f} | STH RP ${r['sth_cost_basis']:,.0f} | "
      f"LTH RP ${r['lth_cost_basis']:,.0f} | AVIV Mean ${r['aviv_mean_usd']:,.0f} | "
      f"AVIV Upper ${r['aviv_upper_usd']:,.0f} | CVDD ${r['cvdd']:,.0f}")

# label zona framework v2
def zone_row(r):
    sth, rp, lth, p = r["sth_cost_basis"], r["realized_price"], r["lth_cost_basis"], r["btc_price"]
    am, au = r["aviv_mean_usd"], r["aviv_upper_usd"]
    conv = (abs(sth - rp) / rp < 0.02) and (abs(rp - lth) / rp < 0.02)
    struct = "C" if conv else ("N" if sth > rp else "T")
    if struct == "C":
        if p < am:
            return struct, "Z2 (Konvergensi)"
        return struct, "Z4"
    if struct == "T":
        if p < sth:
            return struct, "Z1 (Bear bottom)"
        if p < rp:
            return struct, "Z1b"
        return struct, "Z2-transisi"
    if p >= au:
        return struct, "Z5"
    if p >= am:
        return struct, "Z4"
    if p >= sth:
        return struct, "Z3"
    if p >= rp:
        return struct, "ZD (Dip dalam)"
    return struct, "ZC (Capitulation)"


st_, zn_ = zone_row(r)
print(f"  Label zona framework hari itu: struktur {st_} -> {zn_}")
print(f"  -> Klaim video 'bottom 20th percentile' vs data kita: "
      f"{'KONSISTEN arah' if r['price_pct_4y'] <= 0.30 else 'TIDAK konsisten'} "
      f"(perlu diingat: basis RP berbeda std vs flt)")

# ---------------------------------------------------------------- (d) phi vs Price/CVDD < 1,10
print("\n" + "-" * 104)
print("(d) INDEPENDENSI: band bawah (P < q10) vs K4 kondisi 4 (Price/CVDD < 1,10)")
print("-" * 104)
v = df[df["q10"].notna()].copy()
v["below_q10"] = v["btc_price"] < v["q10"]
v["below_q05"] = v["btc_price"] < v["q05"]
v["below_q20"] = v["btc_price"] < v["q20"]
v["cvdd_cond"] = (v["btc_price"] / v["cvdd"]) < 1.10
print(f"  Periode {v['date'].min().date()} s/d {v['date'].max().date()} (n={len(v)})")
for c, nm in [("below_q05", "P < q05"), ("below_q10", "P < q10"), ("below_q20", "P < q20")]:
    a = v[c].astype(int); b = v["cvdd_cond"].astype(int)
    ph = np.corrcoef(a, b)[0, 1] if a.std() > 0 and b.std() > 0 else np.nan
    inter = int((a & b).sum()); union = int((a | b).sum())
    print(f"  {nm:<9}: {int(a.sum()):>4} hari | P/CVDD<1,10: {int(b.sum()):>4} hari | "
          f"irisan {inter:>4} | |phi| = {abs(ph):.3f} | Jaccard {inter/max(union,1)*100:.1f}%")
print("  Catatan: Price/CVDD<1,10 dan band bawah dua-duanya jarang nyala; "
      "|phi| kecil di sini lebih menandakan KEDUANYA jarang, bukan bahwa keduanya membawa info berbeda.")

# apa yang ditambahkan band bawah yang belum diberi P/CVDD?
extra = v[v["below_q10"] & ~v["cvdd_cond"]]
miss  = v[~v["below_q10"] & v["cvdd_cond"]]
print(f"\n  Hari P<q10 TAPI P/CVDD>=1,10 : {len(extra)}")
if len(extra):
    print(f"    rentang: {extra['date'].min().date()} .. {extra['date'].max().date()}; "
          f"sebaran tahun: {dict(extra['date'].dt.year.value_counts().sort_index())}")
print(f"  Hari P/CVDD<1,10 TAPI P>=q10 : {len(miss)}")
if len(miss):
    print(f"    rentang: {miss['date'].min().date()} .. {miss['date'].max().date()}; "
          f"sebaran tahun: {dict(miss['date'].dt.year.value_counts().sort_index())}")

# ---------------------------------------------------------------- ringkas akurasi band atas
print("\n" + "-" * 104)
print("EKSTRA: seberapa sering harga menembus band atas / bawah? (kalibrasi band)")
print("-" * 104)
for c, nm, side in [("q95", "P > q95", "up"), ("q90", "P > q90", "up"),
                    ("q10", "P < q10", "dn"), ("q05", "P < q05", "dn")]:
    m = (v["btc_price"] > v[c]) if side == "up" else (v["btc_price"] < v[c])
    print(f"  {nm:<9}: {int(m.sum()):>4} hari ({m.mean()*100:5.1f}%)  "
          f"[ekspektasi nominal {'5' if '95' in c or '05' in c else '10'}%]")

# ---------------------------------------------------------------- redundansi vs AVIV
print("\n" + "-" * 104)
print("EKSTRA 2: seberapa redundan band atas dengan AVIV? (rasio sepanjang sejarah)")
print("-" * 104)
w = v[v["aviv_upper_usd"].notna()].copy()
w["r_q90_avivup"] = w["q90"] / w["aviv_upper_usd"]
w["r_q95_aviv1"]  = w["q95"] / w["aviv_1sig_usd"]
for c, nm in [("r_q90_avivup", "q90 / AVIV Upper"), ("r_q95_aviv1", "q95 / AVIV +1SD")]:
    ss = w[c]
    print(f"  {nm:<18} median {ss.median():.2f}  p10 {ss.quantile(.10):.2f}  p90 {ss.quantile(.90):.2f}  "
          f"min {ss.min():.2f}  max {ss.max():.2f}")
print(f"  korelasi level harian q90 vs AVIV Upper (log) = "
      f"{np.corrcoef(np.log(w['q90']), np.log(w['aviv_upper_usd']))[0,1]:.4f}")

# ---------------------------------------------------------------- invariansi terhadap base RP
print("\n" + "-" * 104)
print("EKSTRA 3: apakah band SENSITIF terhadap pilihan base realized price (std vs flt)?")
print("-" * 104)
K = 1.094  # contoh: RP filtered ~9,4% lebih tinggi dari RP standar
alt_rp = df["realized_price"] * K
alt_ratio = df["btc_price"] / alt_rp
alt_q90 = alt_ratio.shift(1).rolling(WIN, min_periods=WIN).quantile(0.90) * alt_rp
cmp = (alt_q90 / df["q90"]).dropna()
print(f"  Kalau realized price diskalakan x{K} (konstan), band q90 berubah: "
      f"median rasio {cmp.median():.6f}, max deviasi {abs(cmp-1).max()*100:.4f}%")
print("  -> Band = quantile(P/RP) x RP. Kalau base RP hanya berbeda FAKTOR SKALA, band IDENTIK.")
print("     Konsekuensi: kerja 'filtered realized price' Matt hampir tidak mengubah output band ini.")

print("\nSELESAI V4")
