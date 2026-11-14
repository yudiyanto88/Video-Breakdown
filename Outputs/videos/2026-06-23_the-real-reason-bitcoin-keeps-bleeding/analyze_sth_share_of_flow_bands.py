"""
VALIDASI B-2 (bagian 2) — replikasi metode video via HODL wave age bands.
Video kemungkinan pakai dekomposisi flow per age band (bukan net cohort delta),
karena net cohort delta memberi LTH f30 POSITIF (maturation inflow) yang tidak
cocok dengan klaim "LTH -$4.5B".

Definisi (ditetapkan sebelum lihat hasil):
- band_f30 = realized_cap_<band>[t] - [t-30] per band.
- neg_total = jumlah min(band_f30, 0) semua band.
- STH share (band) = jumlah min(band_f30,0) band muda / neg_total.
  Dua proxy batas STH (155d jatuh di tengah band 3m-6m):
    narrow = 0-1d, 1d-1w, 1w-1m, 1m-3m  (<90d)
    wide   = narrow + 3m-6m             (<180d)
- Distribusi historis dihitung di hari outflow total (tot_f30 < 0).
- Flow harian per band di tanggal video = band_f30 / 30 ($M/hari) untuk cek
  klaim "band 1-3 bulan terbesar ~$64M/hari".
"""
import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
BANDS = ['0-1d','1d-1w','1w-1m','1m-3m','3m-6m','6m-12m','1y-2y','2y-3y','3y-5y','5y-7y','7y-10y','10y+']
NARROW = ['0-1d','1d-1w','1w-1m','1m-3m']
WIDE = NARROW + ['3m-6m']

cols = ['date','realized_cap_usd'] + [f'realized_cap_{b}' for b in BANDS]
df = pd.read_csv(MASTER, usecols=cols, parse_dates=['date']).sort_values('date').reset_index(drop=True)
df = df.dropna(subset=['realized_cap_usd']).reset_index(drop=True)

# KOLOM BAND = PERSEN dari realized cap (sum band = 100) -> konversi ke USD dulu
sm = df[[f'realized_cap_{b}' for b in BANDS]].sum(axis=1)
print(f"Cek: sum persen band mean={sm.mean():.4f} (harus ~100)")
for b in BANDS:
    df[f'rcusd_{b}'] = df[f'realized_cap_{b}'] / 100.0 * df['realized_cap_usd']

df['tot_f30'] = df['realized_cap_usd'] - df['realized_cap_usd'].shift(30)
for b in BANDS:
    df[f'f30_{b}'] = df[f'rcusd_{b}'] - df[f'rcusd_{b}'].shift(30)

negs = pd.DataFrame({b: df[f'f30_{b}'].clip(upper=0) for b in BANDS})
neg_total = negs.sum(axis=1)
df['sth_share_narrow'] = np.where(neg_total < 0, negs[NARROW].sum(axis=1) / neg_total, np.nan)
df['sth_share_wide'] = np.where(neg_total < 0, negs[WIDE].sum(axis=1) / neg_total, np.nan)
df['neg_total'] = neg_total

mask = (df['tot_f30'] < 0) & df['sth_share_wide'].notna()
pool = df[mask]
VIDEO_DATE = pd.Timestamp('2026-06-23')

print("\n" + "="*100)
print("H1 (band-level) — distribusi STH share dari total negative band flow, hari outflow")
print("="*100)
print(f"n hari outflow: {len(pool)}")
for label, col in [('narrow (<3m)','sth_share_narrow'), ('wide (<6m, paling dekat STH 155d)','sth_share_wide')]:
    q = pool[col].quantile([0.10,0.25,0.50,0.75,0.90])
    qs = "  ".join(f"p{int(p*100)}={100*v:.1f}%" for p,v in q.items())
    print(f"  {label}: {qs}")
r = df[df['date'] == VIDEO_DATE]
if not r.empty:
    for label, col in [('narrow','sth_share_narrow'), ('wide','sth_share_wide')]:
        v = r[col].iloc[0]
        pctl = (pool[col] < v).mean()*100
        print(f"  2026-06-23 {label}: {100*v:.1f}% -> persentil {pctl:.0f}")

print("\nPer cycle bear window (median share wide):")
CYCLES = [('C1 2013-15','2013-11-30','2015-04-14'), ('C2 2017-19','2017-12-17','2019-03-15'),
          ('C3 2021-23','2021-11-10','2023-02-19'), ('C4 2025-26','2025-10-06', None)]
for name, lo, hi in CYCLES:
    sub = df[(df['date'] >= lo) & (df['date'] <= (hi or str(df['date'].max()))) & mask]
    if sub.empty: continue
    print(f"  {name}: n={len(sub):4d} | wide median={100*sub['sth_share_wide'].median():5.1f}% "
          f"p10={100*sub['sth_share_wide'].quantile(0.10):5.1f}% p90={100*sub['sth_share_wide'].quantile(0.90):5.1f}% | "
          f"narrow median={100*sub['sth_share_narrow'].median():5.1f}%")

print("\n" + "="*100)
print("H3 (band-level) — flow 30d per band per 2026-06-23 ($B) dan $M/hari")
print("="*100)
if not r.empty:
    for b in BANDS:
        f = r[f'f30_{b}'].iloc[0]
        print(f"  {b:>7s}: {f/1e9:+7.2f}B  ({f/30/1e6:+8.1f} M/hari)")
    sth_n = sum(r[f'f30_{b}'].iloc[0] for b in NARROW)
    sth_w = sum(r[f'f30_{b}'].iloc[0] for b in WIDE)
    lth_w = sum(r[f'f30_{b}'].iloc[0] for b in BANDS if b not in WIDE)
    neg_sth_w = sum(min(r[f'f30_{b}'].iloc[0],0) for b in WIDE)
    neg_lth_w = sum(min(r[f'f30_{b}'].iloc[0],0) for b in BANDS if b not in WIDE)
    print(f"\n  Net <6m: {sth_w/1e9:+.2f}B | net >=6m: {lth_w/1e9:+.2f}B | total: {r['tot_f30'].iloc[0]/1e9:+.2f}B")
    print(f"  NEGATIVE flow saja: <6m {neg_sth_w/1e9:+.2f}B | >=6m {neg_lth_w/1e9:+.2f}B"
          f" | rasio {neg_sth_w/neg_lth_w:.2f}x | share <6m: {100*neg_sth_w/(neg_sth_w+neg_lth_w):.1f}%")
