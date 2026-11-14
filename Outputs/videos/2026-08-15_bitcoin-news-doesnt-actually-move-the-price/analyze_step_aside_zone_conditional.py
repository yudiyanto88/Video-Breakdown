"""
VALIDASI 3 - "Step aside" saat shock: mahal atau tidak? (insight K-3 + konflik X-1)

Q1 Replikasi step-aside REALISTIS tanpa hindsight top-15: setiap DOWN-shock
   (logret <= -3 x vol30 at-gate) -> keluar penuh ke cash N hari (N=5, 10),
   lalu masuk lagi. Bandingkan CAGR + max drawdown vs buy&hold, per cycle & full.
   Klaim video: step-aside 5 hari -> CAGR 33,2% vs buy&hold 66,8% (selisih 33,6 pp).
   Sebagai pembanding langsung klaim video, dua aturan tambahan juga diuji:
     - ANY-shock  : keluar setelah shock arah apapun (naik ATAU turun)
     - HINDSIGHT  : keluar setelah 15 hari |logret| terbesar (persis aturan video,
                    tapi ini MUSTAHIL dieksekusi real-time - hanya untuk cek angka)
Q2 Varian kondisional: step-aside HANYA aktif kalau
   (a) harga di Z5 / masih dalam window K1 (pernah Z5 dalam 90 hari terakhir)
   (b) alarm bear CEPAT (Decision Framework v2 sec.0) sedang bunyi
Q3 Jumlah trigger per cycle + sensitivitas tanggal mulai (2013 / 2015 / 2017)
   + sensitivitas biaya transaksi (0 / 20 bps per switch)

Semua sinyal AT-GATE: keputusan keluar diambil di close hari shock, return yang
dilewatkan adalah t+1..t+N. Tidak ada informasi masa depan (kecuali rule HINDSIGHT
yang memang sengaja dibuat sebagai replikasi klaim video).
"""
import numpy as np
import pandas as pd
import shock_zone_lib as L

OUT_CSV = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-08-15_bitcoin-news-doesnt-actually-move-the-price\events_step_aside_triggers.csv"
COST_BPS = 20.0   # biaya satu kali switch (keluar atau masuk), basis point

df = L.load_base().reset_index(drop=True)
n = len(df)


def line(c="="):
    print(c * 100)


# =============================================================================
# ALARM BEAR CEPAT (Decision Framework v2 sec.0) - 4 sinyal, bunyi kalau 2 nyala
# dalam window pairing 90 hari. Unlock: STH RP cross NAIK melewati RP.
# Sinyal 2 mengikuti pola research/analyze_k3_stage_comparison.py (peak + 14 hari
# konfirmasi, semua gap di 14 hari itu < gap puncak).
# =============================================================================
price = df["btc_price"].values
au = df["aviv_upper_price"].values
zone = df["zone"].values
sth = df["sth_cost_basis"].values
rp = df["realized_price"].values

above = price >= au
sig1 = np.zeros(n, dtype=bool)
streak = 0
for i in range(n):
    if i > 0 and (not above[i]) and streak >= 7:
        sig1[i] = True
    streak = streak + 1 if above[i] else 0

ma90 = df["sth_sopr"].rolling(90, min_periods=90).mean()
ma90_60 = ma90.rolling(60, min_periods=60).mean()
gap = (ma90 - ma90_60).values
sig2 = np.zeros(n, dtype=bool)
CONF = 14
for i in range(1, n - CONF):
    if not np.isfinite(gap[i]) or gap[i] <= 0 or gap[i] <= gap[i - 1]:
        continue
    fut = gap[i + 1:i + 1 + CONF]
    if len(fut) == CONF and np.all(fut < gap[i]) and i + CONF < n:
        sig2[i + CONF] = True

mv = df["mvrv_ratio"]
sma30 = mv.rolling(30, min_periods=30).mean()
sma30_30 = sma30.rolling(30, min_periods=30).mean()
bearx = (sma30 < sma30_30).values
sig3 = np.zeros(n, dtype=bool)
run = 0
for i in range(n):
    run = run + 1 if bearx[i] else 0
    if run == 7:
        sig3[i] = True

sma180 = mv.rolling(180, min_periods=180).mean()
below = (mv < sma180).values
days_since_z5 = np.full(n, 10 ** 6)
last = None
for i in range(n):
    if zone[i] == "Z5":
        last = i
    if last is not None:
        days_since_z5[i] = i - last
sig4 = np.zeros(n, dtype=bool)
run = 0
for i in range(n):
    run = run + 1 if below[i] else 0
    if run == 7 and days_since_z5[i] <= 120:
        sig4[i] = True

sigs = np.vstack([sig1, sig2, sig3, sig4])

# versi RAW: 2 dari 4 sinyal muncul dalam 90 hari terakhir (tanpa persistensi)
raw_alarm = np.zeros(n, dtype=bool)
for i in range(n):
    lo = max(0, i - 89)
    raw_alarm[i] = sum(1 for s in range(4) if sigs[s, lo:i + 1].any()) >= 2

# versi LITERAL: sekali ON, tetap ON sampai unlock (STH RP cross naik lewat RP)
lit_alarm = np.zeros(n, dtype=bool)
on = False
for i in range(n):
    if not on:
        on = raw_alarm[i]
    else:
        if i > 0 and sth[i - 1] <= rp[i - 1] and sth[i] > rp[i]:
            on = False
    lit_alarm[i] = on

df["bear_alarm_raw"] = raw_alarm
df["bear_alarm_literal"] = lit_alarm

line()
print("REPLIKASI ALARM BEAR CEPAT (v2 sec.0)")
for j, nm in enumerate(["s1 turun dari Z5 tembus AVIV Upper", "s2 gap STH-SOPR peak + 14d turun",
                        "s3 MVRV momentum bearish cross 7d", "s4 MVRV<SMA180 7d & Z5 <=120d"]):
    print(f"  {nm:<40} n hari sinyal = {int(sigs[j].sum())}")
print(f"  ALARM RAW (2 dari 4 dalam 90d)     ON = {int(raw_alarm.sum())}/{n} ({100.0*raw_alarm.mean():.1f}% hari)")
print(f"  ALARM LITERAL (+persistensi/unlock) ON = {int(lit_alarm.sum())}/{n} ({100.0*lit_alarm.mean():.1f}% hari)")
print("  CATATAN: dua-duanya nyala di mayoritas hari -> varian (b) hampir tidak")
print("  membedakan apa-apa dari aturan tanpa syarat. Ini keterbatasan replikasi, bukan hasil.")
print(df.groupby("cycle")[["bear_alarm_raw", "bear_alarm_literal"]].mean().mul(100).round(1).to_string())

# =============================================================================
# STEP-ASIDE BACKTEST
# =============================================================================
df["down_shock"] = df["shock_primary"] & (df["logret"] < 0)
df["any_shock"] = df["shock_primary"]
df["in_k1_window"] = (df["zone"] == "Z5") | (days_since_z5 <= 90)
df["trig_k1"] = df["down_shock"] & df["in_k1_window"]
df["trig_bear"] = df["down_shock"] & df["bear_alarm_raw"]


def backtest(d, trig, N, cost_bps=0.0):
    """Keluar penuh ke cash pada close hari trigger, kembali di close t+N.
    Trigger berulang saat masih di luar -> perpanjang (reset clock)."""
    r = np.nan_to_num(d["logret"].values)
    trig = np.asarray(trig, dtype=bool)
    m = len(d)
    invested = np.ones(m, dtype=bool)
    out_until = -1
    for i in range(m):
        if i <= out_until:
            invested[i] = False
        if trig[i]:
            out_until = max(out_until, i + N)
    step = np.exp(np.where(invested, r, 0.0))
    if cost_bps > 0:
        switches = np.zeros(m)
        for i in range(1, m):
            if invested[i] != invested[i - 1]:
                switches[i] = 1
        step = step * (1 - cost_bps / 10000.0) ** switches
    return np.cumprod(step), invested


def stats(eq, dates):
    yrs = (dates.iloc[-1] - dates.iloc[0]).days / 365.25
    cagr = eq[-1] ** (1 / yrs) - 1
    peak = np.maximum.accumulate(eq)
    return cagr, (eq / peak - 1).min(), eq[-1], yrs


def rules_for(d):
    """daftar (nama, boolean trigger array) untuk sub-sample d"""
    out = [("step-aside SEMUA down-shock", d["down_shock"].values),
           ("step-aside ANY-shock (naik+turun)", d["any_shock"].values),
           ("step-aside HANYA Z5/window K1", d["trig_k1"].values),
           ("step-aside HANYA alarm bear raw", d["trig_bear"].values)]
    # HINDSIGHT: 15 hari |logret| terbesar DI DALAM sub-sample (aturan video)
    hs = np.zeros(len(d), dtype=bool)
    idx = np.argsort(-np.nan_to_num(np.abs(d["logret"].values)))[:15]
    hs[idx] = True
    out.append(("HINDSIGHT top-15 |move| (video)", hs))
    return out


def run_block(start, label, Ns=(5, 10), cost=0.0):
    d = df[df["date"] >= start].reset_index(drop=True).copy()
    bh, _ = backtest(d, np.zeros(len(d), dtype=bool), 5, cost)
    c0, m0, f0, yrs = stats(bh, d["date"])
    print("")
    print(f"[{label}]  {d['date'].iloc[0].date()} s/d {d['date'].iloc[-1].date()}  "
          f"({yrs:.1f} tahun, biaya {cost:.0f}bps/switch)")
    print(f"  {'BUY & HOLD':<36} CAGR={c0*100:7.1f}%  MDD={m0*100:7.1f}%  x{f0:,.0f}")
    rows = []
    for tname, trig in rules_for(d):
        for N in Ns:
            eq, inv = backtest(d, trig, N, cost)
            c, mdd, f, _ = stats(eq, d["date"])
            print(f"  {tname+' N='+str(N):<36} CAGR={c*100:7.1f}%  MDD={mdd*100:7.1f}%  x{f:,.0f}"
                  f"  | trig={int(trig.sum()):<4} {100.0*(~inv).mean():4.1f}% di luar"
                  f"  | dCAGR={(c-c0)*100:+6.1f}pp")
            rows.append(dict(scope=label, cost=cost, rule=tname, N=N, cagr=c, mdd=mdd,
                             mult=f, n_trigger=int(trig.sum()), cagr_bh=c0, mdd_bh=m0))
    return rows


line()
print("Q1 + Q2 + Q3 STEP-ASIDE vs BUY & HOLD")
allrows = []
for start, label in [("2013-01-01", "FULL >=2013"), ("2015-01-01", "mulai 2015 (versi video)"),
                     ("2017-01-01", "mulai 2017")]:
    allrows += run_block(start, label)
allrows += run_block("2015-01-01", "mulai 2015 + biaya 20bps", cost=COST_BPS)

line()
print("PER CYCLE (>=2013) - uji independensi sample")
for cname, s, e in L.CYCLES:
    sub = df[(df["date"] >= max(pd.Timestamp(s), pd.Timestamp("2013-01-01"))) &
             (df["date"] <= pd.Timestamp(e))].reset_index(drop=True)
    if len(sub) < 200:
        continue
    bh, _ = backtest(sub, np.zeros(len(sub), dtype=bool), 5)
    c0, m0, f0, yrs = stats(bh, sub["date"])
    print("")
    print(f"[{cname}] {sub['date'].iloc[0].date()} s/d {sub['date'].iloc[-1].date()} ({yrs:.1f}th)")
    print(f"  {'BUY & HOLD':<36} CAGR={c0*100:8.1f}%  MDD={m0*100:7.1f}%")
    for tname, trig in rules_for(sub):
        for N in (5, 10):
            eq, inv = backtest(sub, trig, N)
            c, mdd, f, _ = stats(eq, sub["date"])
            print(f"  {tname+' N='+str(N):<36} CAGR={c*100:8.1f}%  MDD={mdd*100:7.1f}%"
                  f"  | trig={int(trig.sum()):<3} | {(c-c0)*100:+8.1f}pp")

line()
print("JUMLAH TRIGGER PER CYCLE")
print(df.groupby("cycle")[["down_shock", "any_shock", "trig_k1", "trig_bear"]].sum().to_string())

line()
print("RINGKASAN (selisih CAGR & MDD vs B&H)")
res = pd.DataFrame(allrows)
res["dCAGR_pp"] = (res["cagr"] - res["cagr_bh"]) * 100
res["dMDD_pp"] = (res["mdd"] - res["mdd_bh"]) * 100
print(res[["scope", "rule", "N", "n_trigger", "dCAGR_pp", "dMDD_pp"]]
      .to_string(index=False, float_format=lambda x: f"{x:8.1f}"))
print("")
for rule in res["rule"].unique():
    sub = res[res["rule"] == rule]
    print(f"  {rule:<36} menang CAGR di {int((sub['dCAGR_pp']>0).sum())}/{len(sub)} skenario; "
          f"median dCAGR = {sub['dCAGR_pp'].median():+6.1f}pp")

ev = df[df["any_shock"]][["date", "cycle", "zone", "btc_price", "logret", "vol30_atgate",
                          "bear_alarm_raw", "bear_alarm_literal", "in_k1_window",
                          "down_shock", "trig_k1", "trig_bear"]].copy()
ev["ret_pct"] = (np.exp(ev["logret"]) - 1) * 100
ev.to_csv(OUT_CSV, index=False)
print("")
print(f"[saved] {OUT_CSV} ({len(ev)} baris)")
