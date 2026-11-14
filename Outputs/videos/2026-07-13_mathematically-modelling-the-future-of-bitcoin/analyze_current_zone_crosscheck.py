"""
INSIGHT 4: Cross-check independen -- apakah BTC saat ini (data terakhir tersedia) genuinely
masuk "extreme discount territory" / persentil ke-5 terbawah historis, seperti diklaim
pembicara (berdasarkan MODEL DIA, decaying MVRV trend line quantile bands)?

Pendekatan: JANGAN validasi model pembicara (sudah dicoba proxy-nya di INSIGHT 2). Di sini
kita cross-check pakai level & zone Decision Framework v2 KITA SENDIRI di titik data terakhir:
  - Zone structure v2 (dimensi STRUKTUR: STH RP vs RP vs LTH RP; dimensi POSISI HARGA)
  - mvrv_ratio, lth_mvrv, cvdd, percent_btc_in_profit, pct_sth_in_profit
  - Berapa banyak kondisi K4 (4 kondisi bear-bottom accumulation) yang aktif

STANDAR VALIDASI:
1. Definisi event: bukan uji statistik lintas waktu -- ini SATU snapshot point-in-time
   (data terakhir tersedia) dibandingkan terhadap definisi zone/K4 yang SUDAH ADA
   (dari Decision_Framework v2.md), tidak ada threshold baru yang di-fit.
2. n = 1 titik data (snapshot terakhir) -- WAJIB ditekankan ini bukan uji lintas-cycle,
   cuma satu titik waktu. Untuk konteks, ditambahkan histori 90 hari terakhir supaya
   terlihat trennya (bukan cuma satu hari terisolasi).
3. Anti-lookahead: semua level yang dipakai adalah level PADA HARI ITU (tidak ada nilai
   dari masa depan).
4. Independensi sample: n/a (satu snapshot).
5. Tidak ada data yang mulai belakangan dipakai di sini (semua kolom full-history).
6. Tidak ada threshold yang di-tweak -- pakai persis definisi zone/K4 dari Decision Framework v2.
"""

import pandas as pd
import numpy as np

df = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)

cols_needed = ["date", "btc_price", "mvrv_ratio", "lth_mvrv", "sth_mvrv", "cvdd",
               "percent_btc_in_profit", "pct_sth_in_profit", "pct_lth_in_profit",
               "sth_cost_basis", "lth_cost_basis", "realized_price",
               "price_at_aviv_mean", "price_at_aviv_plus_1_sigma", "aviv_ratio",
               "lth_sopr", "asopr"]
sub = df[cols_needed].dropna(subset=["btc_price", "mvrv_ratio", "realized_price", "sth_cost_basis"]).reset_index(drop=True)

last = sub.iloc[-1]
print("=" * 100)
print(f"INSIGHT 4: Cross-check zone independen -- snapshot terakhir {last['date'].date()}")
print("=" * 100)

price     = last["btc_price"]
sth_rp    = last["sth_cost_basis"]
rp        = last["realized_price"]
lth_rp    = last["lth_cost_basis"]
aviv_mean = last["price_at_aviv_mean"]
aviv_upper = aviv_mean + 0.5 * (last["price_at_aviv_plus_1_sigma"] - aviv_mean)  # framework formula (+0.5 SD)

print(f"\nLevel harga:")
print(f"  Price          = {price:,.0f}")
print(f"  STH RP (155d)  = {sth_rp:,.0f}")
print(f"  RP (full)      = {rp:,.0f}")
print(f"  LTH RP         = {lth_rp:,.0f}")
print(f"  AVIV Mean      = {aviv_mean:,.0f}")
print(f"  AVIV Upper(+0.5sd) = {aviv_upper:,.0f}")
print(f"  CVDD           = {last['cvdd']:,.0f}")

# ─── Dimensi 1: STRUKTUR (ordering) ──────────────────────────────────────────
gap_sth_rp = abs(sth_rp - rp) / rp
gap_rp_lth = abs(rp - lth_rp) / rp
if sth_rp > rp and gap_sth_rp >= 0.02:
    struktur = "N (Normal): STH RP > RP"
elif sth_rp < rp:
    struktur = "T (Terbalik): STH RP < RP"
else:
    struktur = "cek manual (dekat batas)"
if gap_sth_rp < 0.02 and gap_rp_lth < 0.02:
    struktur = "C (Konvergen): jarak STH RP-RP dan RP-LTH RP < 2%"

print(f"\nDimensi STRUKTUR: {struktur}")
print(f"  gap |STH RP - RP| / RP = {gap_sth_rp*100:.2f}%")
print(f"  gap |RP - LTH RP| / RP = {gap_rp_lth*100:.2f}%")

# ─── Dimensi 2: POSISI HARGA + Zone lookup (asumsi struktur N, paling umum) ──
if "N (Normal)" in struktur:
    if price < rp:
        zone = "ZC - Capitulation"
    elif rp <= price < sth_rp:
        zone = "ZD - Dip dalam"
    elif sth_rp <= price < aviv_mean:
        zone = "Z3"
    elif aviv_mean <= price < aviv_upper:
        zone = "Z4"
    else:
        zone = "Z5"
elif "T (Terbalik)" in struktur:
    if price < sth_rp:
        zone = "Z1 - Bear bottom"
    elif sth_rp <= price < rp:
        zone = "Z1b"
    else:
        zone = "Z2-transisi"
else:  # C
    if price < aviv_mean:
        zone = "Z2 - Konvergensi"
    else:
        zone = "Z4"

print(f"\n>>> ZONE SAAT INI (menurut Decision Framework v2): {zone}")

# ─── MVRV & related metrics ──────────────────────────────────────────────────
print(f"\nMetrik pendukung:")
print(f"  mvrv_ratio            = {last['mvrv_ratio']:.3f}")
print(f"  lth_mvrv               = {last['lth_mvrv']:.3f}")
print(f"  sth_mvrv               = {last['sth_mvrv']:.3f}")
print(f"  percent_btc_in_profit  = {last['percent_btc_in_profit']:.1f}%")
print(f"  pct_sth_in_profit      = {last['pct_sth_in_profit']:.1f}%")
print(f"  pct_lth_in_profit      = {last['pct_lth_in_profit']:.1f}%")
print(f"  Price / CVDD           = {price/last['cvdd']:.3f}")
print(f"  lth_sopr               = {last['lth_sopr']:.3f}")
print(f"  asopr                  = {last['asopr']:.3f}")

# ─── K4 condition count (jalur utama K4 -- hanya relevan kalau di Z1, tapi
#     dihitung tetap utk informasi/K4-tanpa-Z1 check) ────────────────────────
cond1 = last["lth_mvrv"] < 1.0
# cond2 perlu aSOPR<0.93 sustained >=7hari -- cek 7 hari terakhir
last7 = sub.tail(7)
cond2_asopr = (last7["asopr"] < 0.93).all()
cond2_lthsopr = last["lth_sopr"] < 0.50
cond2 = bool(cond2_asopr and cond2_lthsopr)
cond3 = (last["percent_btc_in_profit"] < 50) and (last["pct_sth_in_profit"] < 10)
cond4 = (price / last["cvdd"]) < 1.10

count = sum([cond1, cond2, cond3, cond4])
print(f"\nK4 4-kondisi check (jalur utama, hanya berlaku penuh kalau Zone=Z1):")
print(f"  (1) LTH-MVRV < 1.0                        : {cond1}  (nilai={last['lth_mvrv']:.3f})")
print(f"  (2) aSOPR<0.93 (7hr terakhir) & LTH-SOPR<0.50 : {cond2}  (aSOPR 7hr semua<0.93={cond2_asopr}, LTH-SOPR={last['lth_sopr']:.3f})")
print(f"  (3) Supply-in-profit<50% & STH-profit<10% : {cond3}  (profit total={last['percent_btc_in_profit']:.1f}%, STH profit={last['pct_sth_in_profit']:.1f}%)")
print(f"  (4) Price/CVDD < 1.10                     : {cond4}  (nilai={price/last['cvdd']:.3f})")
print(f"  >>> Count kondisi aktif = {count}/4")
print(f"  (Catatan: K4 jalur utama butuh Zone=Z1 dulu. Zone saat ini = {zone}, JADI JALUR UTAMA {'AKTIF' if zone=='Z1 - Bear bottom' else 'TIDAK AKTIF'}.")
print(f"   K4-tanpa-Z1 butuh count>=3 DAN alarm bear cepat sudah bunyi -- count saat ini {count}, {'CUKUP' if count>=3 else 'TIDAK CUKUP'} utk syarat count.)")

# ─── Konteks historis 90 hari terakhir (bukan cuma 1 titik terisolasi) ───────
print(f"\n--- Konteks 90 hari terakhir (bukan cuma 1 hari terisolasi) ---")
recent = sub.tail(90).copy()
recent["struktur_N"] = recent["sth_cost_basis"] > recent["realized_price"]
print(f"  n=90 hari, price range: {recent['btc_price'].min():,.0f} - {recent['btc_price'].max():,.0f}")
print(f"  mvrv_ratio range: {recent['mvrv_ratio'].min():.3f} - {recent['mvrv_ratio'].max():.3f}")
print(f"  Semua 90 hari struktur N (STH RP > RP)? {recent['struktur_N'].all()}")
print(f"  % hari price < STH RP (90 hari terakhir): {100*(recent['btc_price'] < recent['sth_cost_basis']).mean():.1f}%")
print(f"  % hari price < RP (90 hari terakhir): {100*(recent['btc_price'] < recent['realized_price']).mean():.1f}%")

# ─── Full-history percentile context untuk mvrv_ratio & price/cvdd (independen dari model pembicara) ───
mvrv_hist = df["mvrv_ratio"].dropna()
pct_rank_mvrv = (mvrv_hist < last["mvrv_ratio"]).mean() * 100
cvdd_hist = df.dropna(subset=["cvdd", "btc_price"])
pcvdd_series = cvdd_hist["btc_price"] / cvdd_hist["cvdd"]
pct_rank_pcvdd = (pcvdd_series < (price/last["cvdd"])).mean() * 100
print(f"\nPercentile rank full-history (independen dari model pembicara):")
print(f"  mvrv_ratio saat ini ({last['mvrv_ratio']:.3f}) ada di percentile ke-{pct_rank_mvrv:.1f} dari seluruh histori")
print(f"  Price/CVDD saat ini ({price/last['cvdd']:.3f}) ada di percentile ke-{pct_rank_pcvdd:.1f} dari seluruh histori")
