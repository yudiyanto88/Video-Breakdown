"""
VALIDASI #2 — Deselerasi outflow Realized Cap -> precondition local floor?
Video: "The Real Reason Bitcoin Keeps Bleeding" (On-Chain Mind, 2026-06-23)
Klaim: "exhaustion of selling is almost always the precondition for at least a local floor"

Definisi event (eksplisit, ditetapkan SEBELUM lihat hasil):
- flow(t) = delta harian realized_cap_usd; MA30 = SMA(flow, 30)
- ma30_pct = MA30 / realized_cap * 100  (%/hari, supaya comparable lintas era)
- REZIM OUTFLOW: rangkaian hari MA30 < 0, gabung kalau dipisah <= 7 hari MA30 >= 0.
  Filter signifikansi: peak outflow rezim (paling negatif) <= -0.02%/hari
  (~ -0.6%/bulan). Rezim di bawah ambang ini = noise, dibuang (dilaporkan).
- DECELERATION EVENT (at-gate): hari pertama dalam rezim di mana MA30 masih < 0
  tapi |ma30_pct| <= (1 - X) * |running peak|, X = 50% (robustness: 30%, 70%).
  Re-arm: setelah event, event baru hanya boleh kalau MA30 bikin low rezim BARU
  (lebih dalam dari peak sebelumnya) dulu.
- LOCAL FLOOR: low30 = harga terendah dalam 30 hari SETELAH event (t_e+1..t_e+30).
  Floor valid kalau harga tidak pernah close di bawah low30 selama 60 hari
  (varian: 90 hari) setelah tanggal low30. Hit = floor terbentuk <= 30 hari dari event.
- FALSE POSITIVE: floor 60d gagal DAN dalam 180 hari setelah event harga close
  > 15% di bawah low30 (leg-down baru).
- Tautologi/lead-lag: bandingkan tanggal event vs tanggal aSOPR MA7 kembali >= 0.99
  terdekat (recovery ke ~1). Kalau selalu koinsiden (+-14 hari) -> tidak ada info baru.
"""
import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Video-Breakdown\Outputs\2026-06-23_the-real-reason-bitcoin-keeps-bleeding"

df = pd.read_csv(MASTER, usecols=['date','btc_price','realized_cap_usd','asopr'],
                 parse_dates=['date']).sort_values('date').reset_index(drop=True)
df = df.dropna(subset=['realized_cap_usd','btc_price']).reset_index(drop=True)
df = df[df['btc_price'] > 0.01].reset_index(drop=True)
df['flow'] = df['realized_cap_usd'].diff()
df['ma30'] = df['flow'].rolling(30).mean()
df['ma30_pct'] = df['ma30'] / df['realized_cap_usd'] * 100.0
df['asopr_ma7'] = df['asopr'].rolling(7).mean()
df = df.dropna(subset=['ma30_pct']).reset_index(drop=True)

MIN_PEAK = -0.02  # %/hari

# --- identifikasi rezim outflow (merge gap <=7) ---
negm = (df['ma30_pct'] < 0).values
regimes = []
i, n = 0, len(df)
while i < n:
    if negm[i]:
        start = i; j = i; last = i
        while j < n:
            if negm[j]:
                last = j; j += 1
            else:
                k = j
                while k < n and not negm[k]:
                    k += 1
                if k < n and (k - j) <= 7:
                    j = k
                else:
                    break
        regimes.append((start, last))
        i = last + 1
    else:
        i += 1

price = df['btc_price'].values
dates = df['date'].values
ma30p = df['ma30_pct'].values

def asopr_recovery_near(idx):
    """tanggal terdekat (sebelum/sesudah) aSOPR MA7 cross ke >= 0.99 dari bawah; return lag hari (event - recovery)."""
    v = df['asopr_ma7'].values
    crosses = [k for k in range(1, n) if v[k] >= 0.99 and v[k-1] < 0.99]
    if not crosses: return None, None
    best = min(crosses, key=lambda k: abs(k - idx))
    lag = idx - best
    return df['date'].iloc[best], lag

def eval_events(X, verbose=False):
    rows = []
    excluded = 0
    for (s, e) in regimes:
        seg = ma30p[s:e+1]
        if seg.min() > MIN_PEAK:
            excluded += 1
            continue
        run_peak = 0.0
        armed = True
        peak_at_last_event = None
        for k in range(s, e+1):
            v = ma30p[k]
            if v < run_peak:
                if peak_at_last_event is not None and v < peak_at_last_event:
                    armed = True  # low rezim baru lebih dalam dari peak saat event terakhir
                run_peak = v
            if (armed and run_peak <= MIN_PEAK and v < 0
                    and abs(v) <= (1 - X) * abs(run_peak)):
                # event
                t_e = k
                lo_win = price[t_e+1:t_e+31]
                if len(lo_win) < 30: break
                low30 = lo_win.min()
                low30_idx = t_e + 1 + int(np.argmin(lo_win))
                def hold(days):
                    fut = price[low30_idx+1:low30_idx+1+days]
                    if len(fut) < days: return None
                    return bool((fut >= low30).all())
                h60, h90 = hold(60), hold(90)
                fut180 = price[t_e+1:t_e+181]
                fp = (h60 is False) and len(fut180) == 180 and (fut180.min() < low30 * 0.85)
                # drawdown tambahan setelah event sampai low terendah 180 hari ke depan
                add_dd = (fut180.min()/price[t_e] - 1)*100 if len(fut180) == 180 else np.nan
                rec_dt, lag = asopr_recovery_near(t_e)
                rows.append({
                    'event_date': str(dates[t_e])[:10], 'price': price[t_e],
                    'peak_ma30_pct': run_peak, 'ma30_pct_at_event': v,
                    'low30': low30, 'low30_date': str(dates[low30_idx])[:10],
                    'floor60': h60, 'floor90': h90, 'false_pos_15pct': fp,
                    'add_dd_180d_%': add_dd,
                    'asopr_ma7_at_event': df['asopr_ma7'].iloc[t_e],
                    'asopr_rec_date': str(rec_dt)[:10] if rec_dt is not None else '-',
                    'lag_vs_asopr_rec_d': lag,
                })
                armed = False
                peak_at_last_event = run_peak
        # (satu rezim bisa >1 event lewat re-arm)
    return pd.DataFrame(rows), excluded

for X in (0.5, 0.3, 0.7):
    ev, excl = eval_events(X)
    print("="*110)
    print(f"DECELERATION EVENTS — shrink >= {int(X*100)}% dari peak outflow (rezim peak <= {MIN_PEAK}%/hari; {excl} rezim noise dibuang)")
    print("="*110)
    if ev.empty:
        print("(tidak ada event)"); continue
    print(ev.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    n_ev = len(ev)
    ok60 = ev['floor60'].dropna()
    ok90 = ev['floor90'].dropna()
    print(f"\nn={n_ev} event | Hit rate local floor <=30d, hold 60d: {ok60.sum()}/{len(ok60)} ({100*ok60.mean():.0f}%)"
          f" | hold 90d: {ok90.sum()}/{len(ok90)} ({100*ok90.mean():.0f}%)")
    print(f"False positive (floor gagal + leg-down >15% dlm 180d): {ev['false_pos_15pct'].sum()}/{n_ev}")
    print(f"Median drawdown tambahan 180d setelah event: {ev['add_dd_180d_%'].median():.1f}%")
    lags = ev['lag_vs_asopr_rec_d'].dropna()
    print(f"Lag vs aSOPR recovery (+ = event SETELAH aSOPR balik >=0.99): median={lags.median():.0f}d, "
          f"dalam +-14d: {(lags.abs()<=14).sum()}/{len(lags)}, dalam +-30d: {(lags.abs()<=30).sum()}/{len(lags)}")
    print(f"aSOPR MA7 saat event: median={ev['asopr_ma7_at_event'].median():.4f}, "
          f">=0.99 saat event: {(ev['asopr_ma7_at_event']>=0.99).sum()}/{n_ev}")
    if X == 0.5:
        ev.to_csv(f"{OUTDIR}\\_decel_events_50pct.csv", index=False)

# --- BASE RATE pembanding: seberapa sering "local floor <=30d" terbentuk dari HARI ACAK dalam rezim outflow ---
print("\n" + "="*110)
print("BASE RATE — hari acak DALAM rezim outflow signifikan (tanpa syarat deselerasi): local floor <=30d?")
print("="*110)
rng = np.random.default_rng(42)
pool = []
for (s, e) in regimes:
    if ma30p[s:e+1].min() <= MIN_PEAK:
        pool.extend(range(s, e+1))
pool = [k for k in pool if k + 31 < n]
sample = rng.choice(pool, size=min(500, len(pool)), replace=False)
hits60 = []
for t_e in sample:
    lo_win = price[t_e+1:t_e+31]
    low30 = lo_win.min(); low30_idx = t_e + 1 + int(np.argmin(lo_win))
    fut = price[low30_idx+1:low30_idx+61]
    if len(fut) < 60: continue
    hits60.append(bool((fut >= low30).all()))
print(f"Base rate floor60 dari {len(hits60)} hari acak dalam rezim outflow: {100*np.mean(hits60):.0f}%")

# --- status sekarang ---
print("\n" + "="*110)
print("STATUS SEKARANG (rezim 2025-26)")
print("="*110)
cur = df[df['date'] >= '2025-10-01']
peak_idx = cur['ma30_pct'].idxmin()
print(f"Peak outflow rezim ini: {df['ma30_pct'].loc[peak_idx]:.4f}%/hari (${df['ma30'].loc[peak_idx]/1e6:,.0f}M/hari) di {str(df['date'].loc[peak_idx])[:10]}")
print(f"MA30 sekarang ({str(df['date'].iloc[-1])[:10]}): {df['ma30_pct'].iloc[-1]:.4f}%/hari (${df['ma30'].iloc[-1]/1e6:,.0f}M/hari)")
print(f"Shrink dari peak: {100*(1 - abs(df['ma30_pct'].iloc[-1])/abs(df['ma30_pct'].loc[peak_idx])):.0f}%")
print(f"MA30 di tanggal video 2026-06-23: ${df.loc[df['date']=='2026-06-23','ma30'].values[0]/1e6:,.0f}M/hari")
