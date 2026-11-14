"""
Insight 7 - 200-day/200-week MA reclaim vs Z1->Z2 unlock (STH RP cross RP)
Video: "Bitcoin Bottom Signal (Less Than 2 Weeks Away)" - Bitcoin Magazine Pro, 2026-07-02

Framework decision (Decision_Framework v2.md, baris 31): status bear berakhir (unlock)
didefinisikan sebagai STH RP (sth_cost_basis) cross NAIK melewati RP (realized_price),
masuk Z2 -- BUKAN saat harga reclaim MA teknikal apapun.

Event definitions (eksplisit):
  - Z1->Z2 unlock event = hari pertama sth_cost_basis > realized_price setelah
    sebelumnya <=. Merge/cooldown: kalau ada whipsaw (cross balik dalam <14 hari),
    dipakai tanggal cross-up TERAKHIR sebelum status "above" bertahan >14 hari
    berturut-turut (menghindari sinyal palsu dari noise beberapa hari).
  - "200_dma reclaim" / "200_wma reclaim" = hari pertama btc_price > MA tsb setelah
    sebelumnya <=, DAN bertahan di atas MA itu >=30 hari kalender berturut-turut
    (sustained reclaim, bukan whipsaw).
  - Untuk tiap episode Z1->Z2, dicari event reclaim MA (200dma / 200wma) TERDEKAT
    secara absolut waktu (bisa sebelum atau sesudah). Kalau tidak ada event reclaim
    dalam jarak wajar (>200 hari), dilaporkan sebagai "tidak ada reklaim bersih di
    sekitar periode itu" -- bukan dipaksakan pasangkan ke event yang jauh.

Anti-lookahead: semua tanggal event dihitung dari data historis aktual (bukan
window masa depan), pembandingan lead/lag murni deskriptif retrospektif.
"""

import pandas as pd

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUT_DIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-07-02_bitcoin-bottom-signal-less-than-2-weeks-away"

df = pd.read_csv(CSV, parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 1].reset_index(drop=True)

# ─── Z1->Z2 unlock events (sth_cost_basis cross up realized_price) ─────────
z = df.dropna(subset=["sth_cost_basis", "realized_price"]).reset_index(drop=True)
z["above"] = z["sth_cost_basis"] > z["realized_price"]
trans = z["above"].astype(int).diff().fillna(0)
raw_cross_up = [z["date"].iloc[i] for i in z.index[trans == 1]]

# merge whipsaws: keep last cross-up where the "above" state then holds >14 days
COOLDOWN = 14
confirmed = []
for cu in raw_cross_up:
    idx = z.index[z["date"] == cu][0]
    # check if stays above for >= COOLDOWN days from here
    fut = z["above"].iloc[idx: idx + COOLDOWN]
    if len(fut) < COOLDOWN or not fut.all():
        continue  # this cross-up reverted within cooldown -> whipsaw, skip as "confirmed"
    confirmed.append(cu)

print("=" * 90)
print("INSIGHT 7 - MA RECLAIM (200dma/200wma) vs Z1->Z2 UNLOCK (STH RP cross RP)")
print("=" * 90)
print(f"\nSemua raw cross-up sth_cost_basis > realized_price: {[d.date() for d in raw_cross_up]}")
print(f"Setelah merge whipsaw (cooldown {COOLDOWN}d, harus bertahan): {[d.date() for d in confirmed]}")
print(f"\n>>> n = {len(confirmed)} episode Z1->Z2 unlock historis (independen, satu per cycle bear market).")

# ─── Sustained MA reclaim events ────────────────────────────────────────────
def sustained_reclaims(df, ma_col, persist_days=30):
    sub = df.dropna(subset=[ma_col]).reset_index(drop=True)
    above = (sub["btc_price"] > sub[ma_col]).values
    dates = sub["date"].values
    ev = []
    for i in range(1, len(sub) - persist_days):
        if above[i] and not above[i - 1]:
            if all(above[i:i + persist_days]):
                ev.append(pd.Timestamp(dates[i]))
    return ev

ev_dma = sustained_reclaims(df, "200_dma", 30)
ev_wma = sustained_reclaims(df, "200_wma", 30)

print(f"\n200_dma sustained reclaim events (>=30d bertahan): {[d.date() for d in ev_dma]}")
print(f"200_wma sustained reclaim events (>=30d bertahan): {[d.date() for d in ev_wma]}")

def nearest_event(target_date, event_list, max_days=200):
    if not event_list:
        return None, None
    diffs = [(e - target_date).days for e in event_list]
    best_i = min(range(len(diffs)), key=lambda i: abs(diffs[i]))
    if abs(diffs[best_i]) > max_days:
        return None, None
    return event_list[best_i], diffs[best_i]

rows = []
print(f"\n{'Episode Z1->Z2':<16} {'200dma reclaim':<16} {'lag(d)':>8} {'200wma reclaim':<16} {'lag(d)':>8}")
print("-" * 78)
for cu in confirmed:
    dma_ev, dma_lag = nearest_event(cu, ev_dma, max_days=200)
    wma_ev, wma_lag = nearest_event(cu, ev_wma, max_days=200)
    dma_str = f"{dma_ev.date()}" if dma_ev is not None else "N/A (tdk ada di sekitar)"
    wma_str = f"{wma_ev.date()}" if wma_ev is not None else "N/A (tdk ada di sekitar)"
    dma_lag_str = f"{dma_lag:+d}" if dma_lag is not None else "-"
    wma_lag_str = f"{wma_lag:+d}" if wma_lag is not None else "-"
    print(f"{cu.date()!s:<16} {dma_str:<16} {dma_lag_str:>8} {wma_str:<16} {wma_lag_str:>8}")
    rows.append({
        "z1z2_unlock_date": cu.date(),
        "200dma_reclaim_date": dma_ev.date() if dma_ev is not None else None,
        "200dma_lag_days": dma_lag,
        "200wma_reclaim_date": wma_ev.date() if wma_ev is not None else None,
        "200wma_lag_days": wma_lag,
    })

print("\nCatatan lag: negatif = reclaim MA terjadi SEBELUM Z1->Z2 unlock (MA duluan).")
print("             positif = reclaim MA terjadi SESUDAH Z1->Z2 unlock (Z1->Z2 duluan).")

dma_lags = [r["200dma_lag_days"] for r in rows if r["200dma_lag_days"] is not None]
wma_lags = [r["200wma_lag_days"] for r in rows if r["200wma_lag_days"] is not None]
print(f"\n200dma lag -- n={len(dma_lags)}, values={dma_lags}")
print(f"200wma lag -- n={len(wma_lags)}, values={wma_lags} (n valid < total episode karena ada yg N/A)")

pd.DataFrame(rows).to_csv(f"{OUT_DIR}\\events_ma_reclaim_vs_z1z2_unlock.csv", index=False)
print("\nCSV disimpan: events_ma_reclaim_vs_z1z2_unlock.csv")
