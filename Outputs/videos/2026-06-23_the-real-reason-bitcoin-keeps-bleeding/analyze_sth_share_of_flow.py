"""
VALIDASI B-2 — Dekomposisi realized cap flow per cohort:
"STH mendominasi 78% negative flow = pasar tanpa structural guidance"
Video: "The Real Reason Bitcoin Keeps Bleeding" (On-Chain Mind, 2026-06-23)

Definisi (eksplisit, ditetapkan SEBELUM lihat hasil):
- f30 per cohort = RC[t] - RC[t-30] (perubahan realized cap 30 hari; setara jumlah
  flow harian 30 hari). Dipakai karena angka video sendiri berbasis "sebulan terakhir".
- Hari outflow: tot_f30 < 0.
- STH share of negative flow: neg_sth = min(sth_f30, 0); neg_lth = min(lth_f30, 0);
  share = neg_sth / (neg_sth + neg_lth), hanya di hari denominator < 0.
  (Kalau lth_f30 positif, seluruh negative flow berasal dari STH -> share = 100%.)
- CATATAN MEKANIS (dilaporkan, bukan hasil): delta RC per cohort tercemar maturation
  flow — coin usia 155 hari pindah STH->LTH di cost basis lama (STH RC turun, LTH RC
  naik TANPA transaksi pasar); LTH yang jual: LTH RC turun di cost basis lama, coin
  masuk STH RC di harga baru. Jadi "LTH outflow" = spend LTH - maturation inflow (net).
- H2 event (max 2 varian, anti overfit): dalam bear window (top -> bottom+90d),
  first date LTH share >= 40% (varian: >= 50%), syarat tot_f30 < 0 & denominator < 0,
  pakai smoothing MA7 pada share supaya tidak kena spike 1 hari.
  Dibandingkan vs: (a) tanggal cycle bottom, (b) first date lth_sopr < 0.50
  (raw harian; varian MA7) di window yang sama. Semua at-gate (tidak ada nilai masa depan).
- Bear windows (top -> bottom, +90d buffer sesudah bottom):
  C1: 2013-11-30 -> 2015-01-14 (bottom) -> 2015-04-14
  C2: 2017-12-17 -> 2018-12-15 -> 2019-03-15
  C3: 2021-11-10 -> 2022-11-21 -> 2023-02-19
  C4 (berjalan): 2025-10-06 -> sekarang (bottom belum dikonfirmasi)
- H3: angka video — sth_f30 & lth_f30 per 2026-06-23 vs klaim -$12.5B / -$4.5B (~3x).
"""
import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-06-23_the-real-reason-bitcoin-keeps-bleeding"

df = pd.read_csv(MASTER, usecols=['date','btc_price','realized_cap_usd',
                                  'sth_realized_cap_usd','lth_realized_cap_usd','lth_sopr'],
                 parse_dates=['date']).sort_values('date').reset_index(drop=True)
df = df.dropna(subset=['realized_cap_usd']).reset_index(drop=True)

for c, name in [('realized_cap_usd','tot'), ('sth_realized_cap_usd','sth'), ('lth_realized_cap_usd','lth')]:
    df[name+'_f30'] = df[c] - df[c].shift(30)

neg_sth = df['sth_f30'].clip(upper=0)
neg_lth = df['lth_f30'].clip(upper=0)
den = neg_sth + neg_lth
df['sth_share'] = np.where(den < 0, neg_sth / den, np.nan)
df['lth_share'] = 1 - df['sth_share']
df['lth_share_ma7'] = df['lth_share'].rolling(7).mean()
df['outflow_day'] = df['tot_f30'] < 0

CYCLES = [
    ('C1 2013-15', '2013-11-30', '2015-01-14'),
    ('C2 2017-19', '2017-12-17', '2018-12-15'),
    ('C3 2021-23', '2021-11-10', '2022-11-21'),
    ('C4 2025-26', '2025-10-06', None),
]
VIDEO_DATE = pd.Timestamp('2026-06-23')

print("="*100)
print("H1 — APAKAH STH SHARE ~78% ANOMALI ATAU NORMAL? (hari outflow: tot_f30 < 0, share terdefinisi)")
print("="*100)
mask = df['outflow_day'] & df['sth_share'].notna()
pool = df[mask]
print(f"n hari outflow (full history 2010-08+): {len(pool)}")
q = pool['sth_share'].quantile([0.05,0.10,0.25,0.50,0.75,0.90,0.95])
print("Distribusi STH share (semua hari outflow):")
for p, v in q.items():
    print(f"  p{int(p*100):02d}: {100*v:6.1f}%")
row_v = df[df['date'] == VIDEO_DATE]
if not row_v.empty and not np.isnan(row_v['sth_share'].iloc[0]):
    sv = row_v['sth_share'].iloc[0]
    pct = (pool['sth_share'] < sv).mean() * 100
    print(f"\nReading 2026-06-23: STH share = {100*sv:.1f}%  -> persentil {pct:.0f} dari semua hari outflow historis")
else:
    print("\n2026-06-23: share tidak terdefinisi (cek tanda flow)")
    print(row_v[['date','tot_f30','sth_f30','lth_f30']].to_string(index=False))

print("\nPer cycle (hanya hari outflow di dalam bear window):")
for name, top, bot in CYCLES:
    lo = pd.Timestamp(top)
    hi = (pd.Timestamp(bot) + pd.Timedelta(days=90)) if bot else df['date'].max()
    sub = df[(df['date'] >= lo) & (df['date'] <= hi) & mask]
    if sub.empty:
        print(f"  {name}: (tidak ada hari outflow)"); continue
    print(f"  {name}: n={len(sub):4d} | STH share median={100*sub['sth_share'].median():5.1f}%  "
          f"p10={100*sub['sth_share'].quantile(0.10):5.1f}%  p90={100*sub['sth_share'].quantile(0.90):5.1f}%")

print()
print("="*100)
print("H2 — APAKAH KENAIKAN LTH SHARE MENDAHULUI CYCLE BOTTOM? TIMING vs LTH-SOPR < 0.50 (K4)")
print("="*100)
for name, top, bot in CYCLES:
    lo = pd.Timestamp(top)
    hi = (pd.Timestamp(bot) + pd.Timedelta(days=90)) if bot else df['date'].max()
    w = df[(df['date'] >= lo) & (df['date'] <= hi)].copy()
    print(f"\n--- {name} (window {top} -> {str(hi)[:10]}; bottom: {bot if bot else 'belum'}) ---")
    for thr in (0.40, 0.50):
        hit = w[(w['lth_share_ma7'] >= thr) & w['outflow_day']]
        if hit.empty:
            print(f"  LTH share MA7 >= {int(thr*100)}%: TIDAK PERNAH")
        else:
            d0 = hit['date'].iloc[0]
            lead = (pd.Timestamp(bot) - d0).days if bot else None
            print(f"  LTH share MA7 >= {int(thr*100)}%: first {str(d0)[:10]}"
                  + (f"  ({lead:+d} hari sebelum bottom)" if lead is not None else "")
                  + f"  | n hari >= thr: {len(hit)}")
    mx = w.dropna(subset=['lth_share_ma7'])
    mx = mx[mx['outflow_day']]
    if not mx.empty:
        imax = mx['lth_share_ma7'].idxmax()
        dmax = df['date'].loc[imax]
        leadm = (pd.Timestamp(bot) - dmax).days if bot else None
        print(f"  Max LTH share MA7: {100*df['lth_share_ma7'].loc[imax]:.1f}% di {str(dmax)[:10]}"
              + (f"  ({leadm:+d} hari sebelum bottom)" if leadm is not None else ""))
    # LTH-SOPR < 0.50
    w['lth_sopr_ma7'] = df['lth_sopr'].rolling(7).mean().loc[w.index]
    for lbl, col in [('raw', 'lth_sopr'), ('MA7', 'lth_sopr_ma7')]:
        h = w[w[col] < 0.50]
        if h.empty:
            print(f"  LTH-SOPR {lbl} < 0.50: TIDAK PERNAH (min {w[col].min():.3f} di {str(w['date'].loc[w[col].idxmin()])[:10]})")
        else:
            d0 = h['date'].iloc[0]
            lead = (pd.Timestamp(bot) - d0).days if bot else None
            print(f"  LTH-SOPR {lbl} < 0.50: first {str(d0)[:10]}"
                  + (f"  ({lead:+d} hari sebelum bottom)" if lead is not None else "")
                  + f"  | n hari: {len(h)}")

print()
print("="*100)
print("H3 — VERIFIKASI ANGKA VIDEO per 2026-06-23 (klaim: STH -$12.5B vs LTH -$4.5B, ~3x; share ~78%)")
print("="*100)
for dt in [VIDEO_DATE, df['date'].max()]:
    r = df[df['date'] == dt]
    if r.empty: continue
    s, l, t = r['sth_f30'].iloc[0]/1e9, r['lth_f30'].iloc[0]/1e9, r['tot_f30'].iloc[0]/1e9
    print(f"{str(dt)[:10]}: 30d flow  STH {s:+.2f}B | LTH {l:+.2f}B | total {t:+.2f}B"
          + (f" | rasio STH/LTH outflow: {s/l:.2f}x" if l < 0 and s < 0 else "")
          + (f" | STH share neg flow: {100*r['sth_share'].iloc[0]:.1f}%" if not np.isnan(r['sth_share'].iloc[0]) else ""))
# konteks sebulan sekitar tanggal video
w = df[(df['date'] >= '2026-05-15') & (df['date'] <= '2026-07-12')]
print("\nRentang Mei-Jul 2026 (MA konteks): STH share min-max: "
      f"{100*w['sth_share'].min():.1f}% - {100*w['sth_share'].max():.1f}%")

# simpan tabel pendukung: share harian di 4 bear window
rows = []
for name, top, bot in CYCLES:
    lo = pd.Timestamp(top)
    hi = (pd.Timestamp(bot) + pd.Timedelta(days=90)) if bot else df['date'].max()
    sub = df[(df['date'] >= lo) & (df['date'] <= hi) & mask][['date','btc_price','tot_f30','sth_f30','lth_f30','sth_share','lth_share_ma7','lth_sopr']].copy()
    sub.insert(0, 'cycle', name)
    rows.append(sub)
pd.concat(rows).to_csv(f"{OUTDIR}\\_sth_share_bear_windows.csv", index=False)
print(f"\nSaved: _sth_share_bear_windows.csv")
