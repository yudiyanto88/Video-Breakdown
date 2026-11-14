# -*- coding: utf-8 -*-
"""
V4 — Base rate hari per zona v2 + kapasitas sizing K4 / lantai waktu

PRINSIP YANG DIUJI (video BM Pro 2026-08-05, insight #21):
  "about 12% of Bitcoin's days are in this sell region. Over one in 10... it doesn't want
  to be a monumental amount" -> ukuran aksi per sinyal dikalibrasi ke BASE RATE sinyal.
  Framework kita menetapkan sizing K1 (20-30% sekali) dan K4 (15/25/35% cash pool per bulan)
  + lantai waktu (5%/bulan) TANPA referensi eksplisit ke base rate zona.

--- DEFINISI (STANDAR VALIDASI poin 1) ---
Zona v2 & kondisi K4: TIDAK dihitung ulang. Script ini meng-IMPORT `btlib.build_all()` dari
  D:\\Claude Code\\Projects\\Onchain-Dashboard\\research\\framework_review_2026-07\\backtest_k5nz\\
  (READ-ONLY; tidak ada file apapun yang ditulis ke project itu) supaya klasifikasi zona
  2-dimensi (struktur N/C/T x posisi harga) dan k4_count identik dengan backtest established.
Cycle = konvensi bottom-to-bottom established (run_backtest.py):
  S1 2013-01-01..2015-01-14 | S2 ..2018-12-15 | S3 ..2022-11-21 | S4 ..2026-07-15 (BELUM SELESAI)
  Baris sebelum 2013-01-01 dilaporkan sebagai "S0 pra-2013 (SUPLEMEN)". CATATAN: btlib
  membuang baris tanpa kolom AVIV -> sampel efektif mulai 2011-02-09 (bukan 2010-07-17).
Lantai waktu: definisi DISALIN dari research/framework_review_2026-07/opus_time_floor_validation.py
  - lag = 9 bulan * 30 hari = 270 hari setelah CYCLE PEAK (idxmax harga dalam window cycle)
  - kondisi = close < RP
  - start = hari pertama kondisi nyala; stop = Signal D (close > STH RP >=3 hari berturut) pertama
  - hari aktif = kondisi nyala antara start..stop-1
Bear window (untuk simulasi kapasitas) = cycle peak -> cycle bottom, identik V1/V2.

--- ANTI LOOKAHEAD (poin 3) ---
Base rate zona & k4_count = fungsi data hari itu saja (btlib) -> at-gate bersih.
Lantai waktu memakai "cycle peak" yang secara definisi baru pasti diketahui ex-post; ini
  bawaan definisi framework, bukan pilihan script ini — DISEBUT eksplisit di findings.
  Sebagai kontrol, dihitung juga versi CAUSAL: peak = running max harga sejak awal cycle.

--- CATATAN DATA ---
Semua kolom penuh sejak 2010-07-17 (tidak ada metrik yang mulai belakangan di uji ini).
Data terakhir 2026-07-15; video 2026-08-05 -> selisih ~3 minggu, cycle S4 BELUM SELESAI.
"""

import sys
import numpy as np
import pandas as pd

BTLIB_DIR = r"D:\Claude Code\Projects\Onchain-Dashboard\research\framework_review_2026-07\backtest_k5nz"
OUT = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-05_the-free-simple-strategy-that-beats-bitcoin-it-just-flashed-again"
sys.dont_write_bytecode = True   # WAJIB: cegah Python menulis __pycache__/*.pyc ke
                                 # folder Onchain-Dashboard (project itu READ-ONLY bagi kita)
sys.path.insert(0, BTLIB_DIR)
import btlib  # noqa: E402  (READ-ONLY import dari Onchain-Dashboard)

df = btlib.build_all().reset_index(drop=True)
LAST = df["date"].max()
print(f"Data (via btlib.build_all): {df['date'].min().date()} s/d {LAST.date()}  n={len(df)} hari")
print("CATATAN: data berhenti 2026-07-15, video 2026-08-05 -> selisih ~3 minggu; S4 belum selesai.\n")

CYCLES = [
    ("S0 pra-2013 (SUPLEMEN)", "2010-07-17", "2012-12-31"),
    ("S1 2013-2015", "2013-01-01", "2015-01-14"),
    ("S2 2015-2018", "2015-01-15", "2018-12-15"),
    ("S3 2018-2022", "2018-12-16", "2022-11-21"),
    ("S4 2022-now (BELUM SELESAI)", "2022-11-22", str(LAST.date())),
]
ZONES = ["ZC", "ZD", "Z1", "Z1b", "Z2", "Z2t", "Z3", "Z4", "Z5"]

# =====================================================================
# (a) BASE RATE HARI PER ZONA
# =====================================================================
print("=" * 124)
print("(a) BASE RATE: JUMLAH HARI PER ZONA v2, PER CYCLE DAN TOTAL")
print("    (klasifikasi zona = btlib/Decision_Framework v2 sec.1, tidak dihitung ulang)")
print("=" * 124)
print(f"{'cycle':<30}{'hari':>7}" + "".join(f"{z:>10}" for z in ZONES))
print("-" * 124)
rows = []
for cn, lo, hi in CYCLES:
    w = df[(df["date"] >= lo) & (df["date"] <= hi)]
    vc = w["zone"].value_counts()
    line = f"{cn:<30}{len(w):>7}"
    r = dict(scope=cn, days=len(w))
    for z in ZONES:
        c = int(vc.get(z, 0))
        r[f"days_{z}"] = c
        r[f"pct_{z}"] = round(c / len(w) * 100, 2) if len(w) else 0.0
        line += f"{c:>10}"
    rows.append(r)
    print(line)
vc_all = df["zone"].value_counts()
TOTLAB = f"TOTAL {df['date'].min().date()}..{LAST.date()}"
line = f"{TOTLAB:<30}{len(df):>7}" + "".join(f"{int(vc_all.get(z,0)):>10}" for z in ZONES)
print("-" * 124)
print(line)
line = f"{'% dari semua hari':<30}{'100%':>7}" + "".join(
    f"{int(vc_all.get(z,0))/len(df)*100:>9.1f}%" for z in ZONES)
print(line)
rtot = dict(scope=TOTLAB, days=len(df))
for z in ZONES:
    rtot[f"days_{z}"] = int(vc_all.get(z, 0))
    rtot[f"pct_{z}"] = round(int(vc_all.get(z, 0)) / len(df) * 100, 2)
rows.append(rtot)

print(f"\n  Cek silang klaim Decision_Framework v2 sec.1: 'seluruh 703 hari Z5' -> "
      f"hitungan kita {int(vc_all.get('Z5',0))} hari Z5"
      f" ({'COCOK' if abs(int(vc_all.get('Z5',0))-703)<=5 else 'SELISIH'}).")
print(f"  Base rate 'sell region' pembanding klaim video (~12% hari): Z5 = "
      f"{int(vc_all.get('Z5',0))/len(df)*100:.1f}% | Z4+Z5 = "
      f"{(int(vc_all.get('Z4',0))+int(vc_all.get('Z5',0)))/len(df)*100:.1f}% dari semua hari.")

# =====================================================================
# (b) HARI PER LEVEL K4 COUNT
# =====================================================================
print("\n" + "=" * 124)
print("(b) JUMLAH HARI PER LEVEL k4_count (0/1/2/3/4), PER CYCLE")
print("    + berapa di antaranya yang benar-benar MEMBUKA aksi K4")
print("      (jalur utama: zona Z1; jalur K4-tanpa-Z1: count>=3 DAN alarm bear cepat aktif)")
print("=" * 124)
print(f"{'cycle':<30}{'hari':>7}{'cnt0':>8}{'cnt1':>8}{'cnt2':>8}{'cnt3':>8}{'cnt4':>8}"
      f"{'Z1&cnt>=2':>11}{'noZ1&cnt>=3':>13}{'K4 aktif':>10}{'P/CVDD<=1':>11}")
print("-" * 124)
k4rows = []
for cn, lo, hi in CYCLES:
    w = df[(df["date"] >= lo) & (df["date"] <= hi)]
    main = (w["zone"] == "Z1") & (w["k4_count"] >= 2)
    noz1 = (w["zone"] != "Z1") & (w["k4_count"] >= 3) & (w["bear_active"])
    act = main | noz1
    ext = (w["pcvdd"] <= 1.0)
    cnts = [int((w["k4_count"] == k).sum()) for k in range(5)]
    print(f"{cn:<30}{len(w):>7}" + "".join(f"{c:>8}" for c in cnts)
          + f"{int(main.sum()):>11}{int(noz1.sum()):>13}{int(act.sum()):>10}{int(ext.sum()):>11}")
    k4rows.append(dict(scope=cn, days=len(w), **{f"days_k4count_{k}": cnts[k] for k in range(5)},
                       days_k4_main=int(main.sum()), days_k4_noz1=int(noz1.sum()),
                       days_k4_active=int(act.sum()), days_pcvdd_le1=int(ext.sum())))

# =====================================================================
# (c) LANTAI WAKTU
# =====================================================================
P = df["price"].values
R = df["rp"].values
S = df["sth_rp"].values
above_sth = (df["price"] > df["sth_rp"]).values
LAG = 9 * 30  # 270 hari, identik opus_time_floor_validation.py


def signal_d_after(start_idx, cutoff_idx):
    run = 0
    for i in range(start_idx, cutoff_idx + 1):
        run = run + 1 if above_sth[i] else 0
        if run >= 3:
            return i
    return None


print("\n" + "=" * 124)
print("(c) LANTAI WAKTU: hari aktif per cycle (>=9 bulan sejak cycle peak DAN close < RP)")
print("    definisi disalin dari opus_time_floor_validation.py; stop = Signal D (P>STH RP >=3 hari)")
print("=" * 124)
print(f"{'cycle':<30}{'peak (ex-post)':>16}{'start':>12}{'stop/SignalD':>14}{'hari aktif':>11}"
      f"{'|kontrol CAUSAL start':>22}{'hari aktif':>12}")
print("-" * 124)
floor_rows = []
floor_mask_global = np.zeros(len(df), bool)
for cn, lo, hi in CYCLES:
    w = df[(df["date"] >= lo) & (df["date"] <= hi)]
    if w.empty:
        continue
    i0, i1 = w.index[0], w.index[-1]

    def run_floor(pk_idx):
        cond = np.zeros(len(df), bool)
        for i in range(max(pk_idx + LAG, i0), i1 + 1):
            cond[i] = P[i] < R[i]
        idxs = np.where(cond)[0]
        if len(idxs) == 0:
            return None, None, None, np.zeros(len(df), bool)
        start = idxs[0]
        sd = signal_d_after(start, i1)
        stop = sd if sd is not None else i1
        m = cond.copy()
        m[stop:] = False
        m[:start] = False
        return start, stop, sd, m

    pk_ex = w["price"].idxmax()
    st1, sp1, sd1, m1 = run_floor(pk_ex)

    # kontrol CAUSAL: peak = running max sejak awal cycle; lantai boleh nyala kalau
    # sudah >=270 hari sejak running-max TERAKHIR dan close < RP
    cond_c = np.zeros(len(df), bool)
    runmax = -np.inf
    runmax_i = i0
    for i in range(i0, i1 + 1):
        if P[i] > runmax:
            runmax = P[i]
            runmax_i = i
        if (i - runmax_i) >= LAG and P[i] < R[i]:
            cond_c[i] = True
    idxs_c = np.where(cond_c)[0]
    if len(idxs_c):
        st2 = idxs_c[0]
        sd2 = signal_d_after(st2, i1)
        sp2 = sd2 if sd2 is not None else i1
        m2 = cond_c.copy()
        m2[sp2:] = False
        m2[:st2] = False
    else:
        st2, sp2, m2 = None, None, np.zeros(len(df), bool)

    floor_mask_global |= m1
    f = lambda i: (str(df["date"].iloc[i].date()) if i is not None else "-")
    print(f"{cn:<30}{f(pk_ex):>16}{f(st1):>12}{f(sp1):>14}{int(m1.sum()):>11}"
          f"{f(st2):>22}{int(m2.sum()):>12}")
    floor_rows.append(dict(scope=cn, peak_expost=f(pk_ex), floor_start=f(st1),
                           floor_stop=f(sp1), floor_days_expost=int(m1.sum()),
                           floor_start_causal=f(st2), floor_days_causal=int(m2.sum())))
df["floor_active"] = floor_mask_global

# =====================================================================
# (d) KAPASITAS SIZING — apakah cash pool habis sebelum cycle low?
# =====================================================================
print("\n" + "=" * 124)
print("(d) KAPASITAS SIZING: konversi 15/25/35%-per-bulan (K4) & 5%-per-bulan (lantai waktu)")
print("    ke %-cash-pool-per-hari, lalu akumulasi sepanjang bear.")
print("    Aturan: rate bulanan / 30,44 = rate harian. Prioritas: K4 (count 2/3/4 -> 15/25/35%)")
print("            > lantai waktu (5%) . Flag ekstrem P/CVDD<=1,0 -> tarik 50% SISA pool hari itu.")
print("    Mode A (operasional, dilaporkan utama): % dari pool AWAL -> pool bisa HABIS di 100%.")
print("    Mode B (kontrol): % dari SISA pool -> secara matematis tidak pernah habis.")
print("=" * 124)

DAYS_PER_MONTH = 30.44
rate_by_count = {2: 0.15, 3: 0.25, 4: 0.35}

# bear window = cycle peak -> cycle bottom (sama V1/V2)
bear_rows = []
for cn, lo, hi in CYCLES:
    if "SUPLEMEN" in cn:
        continue
    w = df[(df["date"] >= lo) & (df["date"] <= hi)]
    pk = w["price"].idxmax()
    bw = df.loc[pk:w.index[-1]]
    low_i = bw["price"].idxmin()
    ongoing = "BELUM SELESAI" in cn

    depA = 0.0   # kumulatif % pool awal
    remB = 1.0   # sisa pool mode B
    depA_at_low = None
    exhaust_date = None
    days_active = 0
    days_after_exhaust_before_low = 0
    detail = []
    for i in bw.index:
        r = df.loc[i]
        z1_main = (r["zone"] == "Z1") and (r["k4_count"] >= 2)
        noz1 = (r["zone"] != "Z1") and (r["k4_count"] >= 3) and bool(r["bear_active"])
        k4on = z1_main or noz1
        if k4on:
            monthly = rate_by_count[int(min(max(r["k4_count"], 2), 4))]
        elif bool(r["floor_active"]):
            monthly = 0.05
        else:
            monthly = 0.0
        daily = monthly / DAYS_PER_MONTH
        if daily > 0:
            days_active += 1
        add = min(daily, max(0.0, 1.0 - depA))
        depA += add
        remB *= (1 - daily)
        if r["pcvdd"] <= 1.0:
            addx = min(0.5 * (1.0 - depA), max(0.0, 1.0 - depA))
            depA += addx
            remB *= 0.5
            detail.append((str(r["date"].date()), "EKSTREM P/CVDD<=1", round(depA * 100, 1)))
        if depA >= 0.999 and exhaust_date is None:
            exhaust_date = r["date"]
        if i == low_i:
            depA_at_low = depA
        if exhaust_date is not None and i <= low_i and r["date"] > exhaust_date:
            days_after_exhaust_before_low += 1

    print(f"\n  {cn}  bear {df['date'].iloc[pk].date()} -> low {df['date'].loc[low_i].date()}"
          f"{'  (low SEMENTARA)' if ongoing else ''}  [{len(bw)} hari]")
    print(f"    hari dgn deploy aktif (K4 atau lantai) : {days_active}")
    print(f"    kapasitas terpakai di TITIK LOW (mode A): {depA_at_low*100:.1f}% dari cash pool")
    print(f"    kapasitas terpakai di AKHIR window     : {depA*100:.1f}%")
    print(f"    pool HABIS sebelum low?                : "
          f"{'YA, ' + str(exhaust_date.date()) if exhaust_date is not None and exhaust_date <= df['date'].loc[low_i] else 'TIDAK'}"
          + (f"  ({days_after_exhaust_before_low} hari sisa bear tanpa amunisi)" if days_after_exhaust_before_low else ""))
    print(f"    mode B (kontrol, % dari sisa)          : terpakai {(1-remB)*100:.1f}%, sisa {remB*100:.1f}%")
    if detail:
        print(f"    hari flag ekstrem P/CVDD<=1,0          : {len(detail)} -> {detail[:5]}")
    bear_rows.append(dict(scope=cn, bear_start=str(df["date"].iloc[pk].date()),
                          bear_low=str(df["date"].loc[low_i].date()), bear_days=len(bw),
                          deploy_days=days_active,
                          capacity_used_at_low_pct=round(depA_at_low * 100, 1),
                          capacity_used_end_pct=round(depA * 100, 1),
                          exhausted_before_low=bool(exhaust_date is not None
                                                    and exhaust_date <= df["date"].loc[low_i]),
                          exhaust_date=str(exhaust_date.date()) if exhaust_date is not None else None,
                          modeB_used_pct=round((1 - remB) * 100, 1), ongoing=ongoing))

print("\n  RINGKASAN (d): kapasitas terpakai per bear (mode A, % cash pool):")
for r in bear_rows:
    print(f"    {r['scope']:<30} di low: {r['capacity_used_at_low_pct']:>6.1f}%  "
          f"| habis sebelum low: {'YA' if r['exhausted_before_low'] else 'TIDAK'}  "
          f"| hari deploy: {r['deploy_days']}")

# --- diagnostik bear BERJALAN (kenapa framework masih diam per 2026-07-15) ---
print("\n" + "=" * 124)
print("DIAGNOSTIK BEAR BERJALAN (per data terakhir; ingat video 3 minggu lebih baru)")
print("=" * 124)
w4 = df[(df["date"] >= "2022-11-22")]
pk4 = w4["price"].idxmax()
pk4_date = df["date"].iloc[pk4]
clock = pk4_date + pd.Timedelta(days=LAG)
lastr = df.iloc[-1]
print(f"  cycle peak (ex-post) : {pk4_date.date()} @ ${df['price'].iloc[pk4]:,.0f}")
print(f"  jam 9 bulan (270 hari) habis : {clock.date()} "
      f"({'SUDAH lewat' if clock <= LAST else 'BELUM lewat'} per {LAST.date()})")
print(f"  syarat kedua lantai waktu (close < RP): price ${lastr['price']:,.0f} vs RP "
      f"${lastr['rp']:,.0f} -> {'TERPENUHI' if lastr['price'] < lastr['rp'] else 'BELUM terpenuhi'}")
print(f"  zona hari terakhir = {lastr['zone']} (struktur {lastr['struct']}), k4_count = "
      f"{int(lastr['k4_count'])}, alarm bear cepat aktif = {bool(lastr['bear_active'])}")
print("  -> per 2026-07-15 tidak ada satu pun jalur deploy K4/lantai waktu yang nyala di bear ini.")

# =====================================================================
# CSV
# =====================================================================
zdf = pd.DataFrame(rows)
kdf = pd.DataFrame(k4rows)
fdf = pd.DataFrame(floor_rows)
bdf = pd.DataFrame(bear_rows)
path = OUT + r"\events_zone_base_rate.csv"
with open(path, "w", encoding="utf-8", newline="") as f:
    f.write("=== (a) Hari per zona v2 per cycle ===\n")
    zdf.to_csv(f, index=False)
    f.write("\n=== (b) Hari per level k4_count per cycle ===\n")
    kdf.to_csv(f, index=False)
    f.write("\n=== (c) Lantai waktu per cycle ===\n")
    fdf.to_csv(f, index=False)
    f.write("\n=== (d) Kapasitas sizing per bear ===\n")
    bdf.to_csv(f, index=False)
print(f"\nCSV disimpan: {path}")

print("\n" + "=" * 124)
print("n (STANDAR VALIDASI poin 2 & 4)")
print("=" * 124)
print(f"  n hari total = {len(df)} ({df['date'].min().date()} s/d {LAST.date()}; btlib membuang baris tanpa kolom AVIV -> mulai 2011-02, bukan 2010-07)")
print("  n cycle = 4 established (S1-S4) + 1 suplemen pra-2013; S4 BELUM SELESAI")
print("  n bear utk simulasi kapasitas = 3 SELESAI + 1 BERJALAN")
print("  Independensi: hari dalam satu zona sangat berkorelasi (blok kontinu) -> base rate")
print("  harian bukan n independen; unit yang jujur = jumlah KUNJUNGAN zona per cycle.")
vis = {}
for cn, lo, hi in CYCLES:
    w = df[(df["date"] >= lo) & (df["date"] <= hi)]
    for z in ZONES:
        m = (w["zone"] == z).values
        n_vis = int(np.sum(m & ~np.concatenate(([False], m[:-1]))))
        vis.setdefault(z, []).append(n_vis)
print("\n  Jumlah KUNJUNGAN (blok kontinu) per zona per cycle "
      f"[{', '.join(c[0] for c in CYCLES)}]:")
for z in ZONES:
    print(f"    {z:<5} {vis[z]}  total={sum(vis[z])}")
