"""
VALIDASI #1 — Capital Bleeding (30d % change Realized Cap) sebagai sinyal DCA
Video: "The Real Reason Bitcoin Keeps Bleeding" (On-Chain Mind, 2026-06-23)

Definisi event (eksplisit, ditetapkan SEBELUM lihat hasil):
- rc30(t) = % change 30 hari realized_cap_usd
- Hari negatif: rc30 < 0
- SIGNAL AKTIF (at-gate, causal, dipakai backtest DCA):
    rc30 < 0 selama >= 14 hari berturut-turut sampai hari t (tanpa lookahead)
- EPISODE (untuk hitung n): rangkaian hari negatif, dua rangkaian digabung
    kalau dipisah <= 7 hari non-negatif; episode qualifying kalau total
    hari negatif >= 14
- Forward return: (price[t+h]/price[t] - 1), h = 90/180/365. Hari tanpa data
    forward h dibuang dari perbandingan horizon itu.
- Cycle bottoms untuk label: 2011-11-18, 2015-01-14, 2018-12-15, 2022-11-21
"""
import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Video-Breakdown\Outputs\2026-06-23_the-real-reason-bitcoin-keeps-bleeding"

cols = ['date','btc_price','realized_cap_usd','net_realized_pl_usd',
        'lth_mvrv','asopr','lth_sopr','percent_btc_in_profit','pct_sth_in_profit',
        'cvdd','sth_cost_basis','realized_price']
df = pd.read_csv(MASTER, usecols=cols, parse_dates=['date']).sort_values('date').reset_index(drop=True)
df = df.dropna(subset=['realized_cap_usd','btc_price']).reset_index(drop=True)
df = df[df['btc_price'] > 0.01].reset_index(drop=True)

df['rc30'] = df['realized_cap_usd'].pct_change(30) * 100.0
df = df.dropna(subset=['rc30']).reset_index(drop=True)

CYCLE_BOUNDS = [('C1_2010-2011', pd.Timestamp('2011-11-18')),
                ('C2_2012-2015', pd.Timestamp('2015-01-14')),
                ('C3_2015-2018', pd.Timestamp('2018-12-15')),
                ('C4_2019-2022', pd.Timestamp('2022-11-21')),
                ('C5_2023-now',  pd.Timestamp('2099-01-01'))]
def cycle_of(d):
    for name, end in CYCLE_BOUNDS:
        if d <= end: return name
    return 'C5_2023-now'
df['cycle'] = df['date'].apply(cycle_of)

# ---------- (a) Streak / episode identification ----------
neg = (df['rc30'] < 0).values
# causal run length (hari negatif berturut-turut, reset kalau non-negatif)
run = np.zeros(len(df), dtype=int)
for i in range(len(df)):
    run[i] = run[i-1] + 1 if neg[i] and i > 0 else (1 if neg[i] else 0)
df['neg_run'] = run
df['signal_active'] = df['neg_run'] >= 14   # at-gate DCA signal

# Episodes (merge gap <=7 hari non-negatif)
episodes = []
i = 0
n = len(df)
while i < n:
    if neg[i]:
        start = i; j = i; last_neg = i
        while j < n:
            if neg[j]:
                last_neg = j; j += 1
            else:
                # lihat gap
                k = j
                while k < n and not neg[k]:
                    k += 1
                if k < n and (k - j) <= 7:
                    j = k  # merge
                else:
                    break
        end = last_neg
        neg_days = int(neg[start:end+1].sum())
        episodes.append((start, end, neg_days))
        i = end + 1
    else:
        i += 1

ep_rows = []
for (s, e, nd) in episodes:
    if nd < 14: continue
    seg = df.iloc[s:e+1]
    ep_rows.append({
        'start': df['date'].iloc[s].date(), 'end': df['date'].iloc[e].date(),
        'neg_days': nd, 'span_days': (df['date'].iloc[e]-df['date'].iloc[s]).days+1,
        'min_rc30': seg['rc30'].min(),
        'min_rc30_date': seg.loc[seg['rc30'].idxmin(),'date'].date(),
        'cycle': df['cycle'].iloc[s],
        'price_start': df['btc_price'].iloc[s], 'price_end': df['btc_price'].iloc[e],
    })
ep = pd.DataFrame(ep_rows)
print("="*100)
print("(a) EPISODE CAPITAL BLEEDING (rc30<0, merge gap<=7d, total hari negatif >=14)")
print("="*100)
print(ep.to_string(index=False))
print(f"\nTotal episode qualifying: n={len(ep)}")
print("Sebaran per cycle:")
print(ep['cycle'].value_counts().sort_index().to_string())
ep.to_csv(f"{OUTDIR}\\_capital_bleeding_episodes.csv", index=False)

# ---------- forward returns ----------
price = df['btc_price'].values
for h in (90, 180, 365):
    fwd = np.full(len(df), np.nan)
    fwd[:-h] = price[h:] / price[:-h] - 1.0
    df[f'fwd{h}'] = fwd * 100.0

# running ATH drawdown (at-gate)
df['run_ath'] = df['btc_price'].cummax()
df['dd_from_ath'] = (df['btc_price']/df['run_ath'] - 1.0) * 100.0
df['dd20'] = df['dd_from_ath'] <= -20.0

# ---------- (b) DCA comparison ----------
print("\n" + "="*100)
print("(b) FORWARD RETURN PER STRATEGI BELI (setiap hari eligible = 1 pembelian)")
print("="*100)
strategies = {
    'BLEED (signal_active: rc30<0 run>=14d)': df['signal_active'],
    'UNIFORM (semua hari)': pd.Series(True, index=df.index),
    'DD20 (drawdown>=20% dari ATH)': df['dd20'],
    'DD20 & BLEED': df['dd20'] & df['signal_active'],
    'DD20 & bukan-BLEED': df['dd20'] & ~df['signal_active'],
    'BLEED & bukan-DD20': df['signal_active'] & ~df['dd20'],
}
rows = []
for name, mask in strategies.items():
    for h in (90, 180, 365):
        sub = df.loc[mask, f'fwd{h}'].dropna()
        rows.append({'strategi': name, 'h': h, 'n_hari': len(sub),
                     'median_%': sub.median(), 'mean_%': sub.mean(),
                     'pct_positif': (sub > 0).mean()*100 if len(sub) else np.nan})
res = pd.DataFrame(rows)
for h in (90, 180, 365):
    print(f"\n--- Horizon {h} hari ---")
    print(res[res['h']==h][['strategi','n_hari','median_%','mean_%','pct_positif']]
          .to_string(index=False, float_format=lambda x: f"{x:9.2f}"))

# per-cycle median utk BLEED vs UNIFORM (cek dominasi cycle)
print("\nPer-cycle median fwd180 (BLEED vs UNIFORM vs DD20):")
for cyc in df['cycle'].unique():
    m = df['cycle'] == cyc
    b = df.loc[m & df['signal_active'], 'fwd180'].dropna()
    u = df.loc[m, 'fwd180'].dropna()
    d20 = df.loc[m & df['dd20'], 'fwd180'].dropna()
    print(f"  {cyc}: BLEED n={len(b):4d} med={b.median():8.1f}% | UNIF n={len(u):4d} med={u.median():8.1f}% | DD20 n={len(d20):4d} med={d20.median():8.1f}%")

# ---------- (c) Monotonicity: streak makin panjang = makin discounted? ----------
print("\n" + "="*100)
print("(c) MONOTONICITY — forward return vs panjang run negatif saat beli (at-gate)")
print("="*100)
buckets = [(14,29),(30,59),(60,99),(100,10**6)]
for h in (90,180,365):
    print(f"\nHorizon {h}d:")
    for lo,hi in buckets:
        m = df['signal_active'] & df['neg_run'].between(lo,hi)
        sub = df.loc[m, f'fwd{h}'].dropna()
        lab = f"{lo}-{hi}" if hi<10**6 else f"{lo}+"
        print(f"  run {lab:>8}: n={len(sub):5d}  median={sub.median():8.2f}%  mean={sub.mean():8.2f}%  pct+={100*(sub>0).mean():5.1f}%")
    act = df[df['signal_active']].dropna(subset=[f'fwd{h}'])
    if len(act) > 10:
        from scipy.stats import spearmanr
        rho, p = spearmanr(act['neg_run'], act[f'fwd{h}'])
        print(f"  Spearman rho(run_len, fwd{h}) = {rho:+.3f} (p={p:.2e})")

# ---------- (d) Overlap dengan K4 confidence count ----------
print("\n" + "="*100)
print("(d) OVERLAP DENGAN K4 (Decision Framework)")
print("="*100)
c1 = df['lth_mvrv'] < 1.0
asopr_7d = df['asopr'].rolling(7).max() < 0.93   # 7 hari berturut2 < 0.93
c2 = asopr_7d & (df['lth_sopr'] < 0.50)
c3 = (df['percent_btc_in_profit'] < 50) & (df['pct_sth_in_profit'] < 10)
c4 = (df['btc_price'] / df['cvdd']) < 1.10
df['k4_count'] = c1.fillna(False).astype(int) + c2.fillna(False).astype(int) + \
                 c3.fillna(False).astype(int) + c4.fillna(False).astype(int)
df['z1'] = (df['btc_price'] < df['sth_cost_basis']) & (df['sth_cost_basis'] < df['realized_price'])

act = df[df['signal_active']]
print(f"Hari signal BLEED aktif: {len(act)}")
for th in (1,2):
    print(f"  ... dengan K4 count >= {th}: {100*(act['k4_count']>=th).mean():.1f}%")
print(f"  ... di Z1 (K4 berlaku): {100*act['z1'].mean():.1f}%")
k4d = df[df['k4_count']>=2]
print(f"Hari K4 count >= 2 total: {len(k4d)}; yang juga BLEED aktif: {100*k4d['signal_active'].mean():.1f}%")
# lead/lag per bear: tanggal pertama BLEED aktif vs pertama K4>=2 vs pertama Z1
print("\nLead/lag per bear (tanggal pertama):")
bears = [('Bear 2014-15','2014-01-01','2015-06-01'),
         ('Bear 2018-19','2018-01-01','2019-04-01'),
         ('Bear 2022','2021-11-09','2023-01-15'),
         ('Bear 2025-26','2025-10-07','2026-07-12')]
for name, a, b in bears:
    w = df[(df['date']>=a)&(df['date']<=b)]
    f_bleed = w.loc[w['signal_active'],'date'].min()
    f_k4    = w.loc[w['k4_count']>=2,'date'].min()
    f_z1    = w.loc[w['z1'],'date'].min()
    print(f"  {name}: BLEED aktif={str(f_bleed)[:10]} | K4>=2={str(f_k4)[:10]} | Z1={str(f_z1)[:10]}")

# ---------- (e) Persentil reading saat ini ----------
print("\n" + "="*100)
print("(e) READING SAAT INI (-1.35% di 2026-06-23) DALAM DISTRIBUSI HISTORIS")
print("="*100)
cur_video = df.loc[df['date']==pd.Timestamp('2026-06-23'),'rc30'].values[0]
cur_now   = df['rc30'].iloc[-1]
this_bear = df[df['date']>='2025-10-07']
trough_now = this_bear['rc30'].min(); trough_now_dt = this_bear.loc[this_bear['rc30'].idxmin(),'date']
print(f"rc30 di tanggal video (2026-06-23): {cur_video:.2f}%")
print(f"rc30 hari ini ({str(df['date'].iloc[-1])[:10]}): {cur_now:.2f}%")
print(f"rc30 terdalam bear ini: {trough_now:.2f}% ({str(trough_now_dt)[:10]})")
negs = df.loc[df['rc30']<0,'rc30']
print(f"\nDistribusi semua hari negatif full history (n={len(negs)}):")
for q in (5,10,25,50,75):
    print(f"  p{q:2d}: {np.percentile(negs,q):7.2f}%")
print(f"Persentil reading video (-1.35%) di antara hari negatif: p{100*(negs<cur_video).mean():.0f} "
      f"(artinya {100*(negs<cur_video).mean():.0f}% hari negatif historis LEBIH dalam)")
for name,a,b,bot in [('Bear 2014-15','2014-01-01','2015-06-01','2015-01-14'),
                     ('Bear 2018-19','2018-01-01','2019-04-01','2018-12-15'),
                     ('Bear 2022','2021-11-09','2023-01-15','2022-11-21')]:
    w = df[(df['date']>=a)&(df['date']<=b)]
    wn = w.loc[w['rc30']<0]
    print(f"\n{name}: min rc30={w['rc30'].min():.2f}% | hari negatif dgn rc30 <= -1.35%: {(wn['rc30']<=cur_video).sum()}/{len(wn)}")
    # kapan pertama kali rc30 <= -1.35, lalu berapa lama & dalam sampai bottom
    first = w.loc[w['rc30']<=cur_video,'date'].min()
    if pd.notna(first):
        p_first = w.loc[w['date']==first,'btc_price'].values[0]
        bot_dt = pd.Timestamp(bot)
        p_bot = df.loc[df['date']==bot_dt,'btc_price'].values[0]
        print(f"  Pertama kali rc30<=-1.35%: {str(first)[:10]} @ ${p_first:,.0f}")
        print(f"  Cycle bottom: {bot} @ ${p_bot:,.0f} -> {(bot_dt-first).days} hari kemudian, {100*(p_bot/p_first-1):.1f}% lebih rendah")
    # kedalaman bleeding lanjutan setelah level -1.35% tercapai
    after = w[w['date']>=first]
    print(f"  rc30 terdalam setelah itu: {after['rc30'].min():.2f}%")
print("\nCek klaim 'second largest bleeding event of this bear': episode bear 2025-26:")
print(ep[ep['start']>=pd.Timestamp('2025-10-07').date()].to_string(index=False))
