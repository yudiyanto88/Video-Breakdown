"""
VALIDASI #3 — Flow Momentum (MA30 vs MA90 realized capital flow)
Video: "The Real Reason Bitcoin Keeps Bleeding" (On-Chain Mind, 2026-06-23)
Klaim: MA30 flow < MA90 flow = structural demand melemah = "opportunity to start scaling in"

(a) korelasi Flow Momentum vs Capital Bleeding (rc30) -> kalau >0.9, satu indikator
(b) first-cross MA30<MA90 di bear 2014/2018/2022(/2026): drawdown tambahan sampai cycle bottom
(c) korelasi MA30 flow vs MA30 net_realized_pl_usd -> redundansi vs metrik existing
"""
import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

df = pd.read_csv(MASTER, usecols=['date','btc_price','realized_cap_usd','net_realized_pl_usd'],
                 parse_dates=['date']).sort_values('date').reset_index(drop=True)
df = df.dropna(subset=['realized_cap_usd','btc_price']).reset_index(drop=True)
df = df[df['btc_price'] > 0.01].reset_index(drop=True)

df['flow'] = df['realized_cap_usd'].diff()
df['ma30'] = df['flow'].rolling(30).mean()
df['ma90'] = df['flow'].rolling(90).mean()
df['momentum'] = df['ma30'] - df['ma90']
df['momentum_pct'] = df['momentum'] / df['realized_cap_usd'] * 100.0   # %/hari, comparable lintas era
df['rc30'] = df['realized_cap_usd'].pct_change(30) * 100.0
df['nrpl_ma30'] = df['net_realized_pl_usd'].rolling(30).mean()
df['nrpl_ma30_pct'] = df['nrpl_ma30'] / df['realized_cap_usd'] * 100.0
df['ma30_pct'] = df['ma30'] / df['realized_cap_usd'] * 100.0

CYCLES = [('C1_2010-2011','2010-07-17','2011-11-18'),
          ('C2_2012-2015','2011-11-19','2015-01-14'),
          ('C3_2015-2018','2015-01-15','2018-12-15'),
          ('C4_2019-2022','2018-12-16','2022-11-21'),
          ('C5_2023-now','2022-11-22','2099-01-01')]

d = df.dropna(subset=['momentum_pct','rc30','nrpl_ma30_pct']).copy()

print("="*100)
print("(a) KORELASI Flow Momentum vs Capital Bleeding (rc30)")
print("="*100)
print(f"Full history : Pearson (momentum_pct vs rc30) = {d['momentum_pct'].corr(d['rc30']):.3f}")
print(f"               Spearman                        = {d['momentum_pct'].corr(d['rc30'], method='spearman'):.3f}")
agree = ((d['momentum_pct']<0) == (d['rc30']<0)).mean()
print(f"Kesepakatan tanda (momentum<0 vs rc30<0): {100*agree:.1f}% hari")
for name,a,b in CYCLES:
    m = (d['date']>=a)&(d['date']<=b)
    if m.sum()>100:
        print(f"  {name}: Pearson={d.loc[m,'momentum_pct'].corr(d.loc[m,'rc30']):.3f}  "
              f"sign-agree={100*((d.loc[m,'momentum_pct']<0)==(d.loc[m,'rc30']<0)).mean():.1f}%")

print("\n" + "="*100)
print("(b) FIRST CROSS MA30<MA90 SETELAH CYCLE TOP -> drawdown tambahan sampai cycle bottom")
print("="*100)
bears = [('Bear 2014-15','2013-11-30','2015-01-14'),
         ('Bear 2018-19','2017-12-17','2018-12-15'),
         ('Bear 2022','2021-11-10','2022-11-21'),
         ('Bear 2025-26','2025-10-06', None)]
dd_all = df.dropna(subset=['momentum']).reset_index(drop=True)
cross_dn = (dd_all['momentum'] < 0) & (dd_all['momentum'].shift(1) >= 0)
for name, top, bot in bears:
    top_dt = pd.Timestamp(top)
    # first cross setelah top
    m = cross_dn & (dd_all['date'] > top_dt)
    if bot: m = m & (dd_all['date'] <= pd.Timestamp(bot))
    idxs = dd_all.index[m]
    if len(idxs)==0:
        print(f"{name}: tidak ada cross"); continue
    fc = idxs[0]
    p_cross = dd_all['btc_price'].iloc[fc]; d_cross = dd_all['date'].iloc[fc]
    p_top = dd_all.loc[(dd_all['date']>=top_dt)&(dd_all['date']<=top_dt+pd.Timedelta(days=5)),'btc_price'].max()
    if bot:
        bot_dt = pd.Timestamp(bot)
        p_bot = dd_all.loc[dd_all['date']==bot_dt,'btc_price'].values[0]
        add_dd = 100*(p_bot/p_cross-1)
        days_to_bot = (bot_dt - d_cross).days
        n_crosses = int(m.sum())
        print(f"{name}: top {top} (${p_top:,.0f}) | first cross {str(d_cross)[:10]} @ ${p_cross:,.0f} "
              f"({100*(p_cross/p_top-1):.1f}% dari top)")
        print(f"    -> cycle bottom {bot} @ ${p_bot:,.0f}: drawdown TAMBAHAN setelah cross = {add_dd:.1f}%, {days_to_bot} hari | total cross-down dalam bear: {n_crosses}")
    else:
        low_so_far = dd_all.loc[dd_all['date']>=d_cross,'btc_price'].min()
        print(f"{name}: top {top} (${p_top:,.0f}) | first cross {str(d_cross)[:10]} @ ${p_cross:,.0f} "
              f"({100*(p_cross/p_top-1):.1f}% dari top) | low sejauh ini ${low_so_far:,.0f} ({100*(low_so_far/p_cross-1):.1f}% setelah cross) [bear belum tentu selesai]")

print("\n" + "="*100)
print("(c) REDUNDANSI vs net_realized_pl_usd (MA30)")
print("="*100)
print(f"Full history : Pearson (ma30 flow vs ma30 nrpl, raw USD)   = {d['ma30'].corr(d['nrpl_ma30']):.4f}")
print(f"               Pearson (normalized %RC)                     = {d['ma30_pct'].corr(d['nrpl_ma30_pct']):.4f}")
print(f"               Spearman (normalized)                        = {d['ma30_pct'].corr(d['nrpl_ma30_pct'], method='spearman'):.4f}")
for name,a,b in CYCLES:
    m = (d['date']>=a)&(d['date']<=b)
    if m.sum()>100:
        print(f"  {name}: Pearson raw={d.loc[m,'ma30'].corr(d.loc[m,'nrpl_ma30']):.4f}  norm={d.loc[m,'ma30_pct'].corr(d.loc[m,'nrpl_ma30_pct']):.4f}")
# momentum vs nrpl momentum
d['nrpl_mom'] = d['nrpl_ma30'] - d['net_realized_pl_usd'].rolling(90).mean()
print(f"\nMomentum (MA30-MA90) flow vs momentum net_realized_pl: Pearson = {d['momentum'].corr(d['nrpl_mom']):.4f}")

print("\nStatus sekarang: momentum = ${:,.0f}M/hari ({}), rc30 = {:.2f}%".format(
    df['momentum'].iloc[-1]/1e6, str(df['date'].iloc[-1])[:10], df['rc30'].iloc[-1]))
print("Momentum di tanggal video 2026-06-23: ${:,.0f}M/hari".format(
    df.loc[df['date']=='2026-06-23','momentum'].values[0]/1e6))
