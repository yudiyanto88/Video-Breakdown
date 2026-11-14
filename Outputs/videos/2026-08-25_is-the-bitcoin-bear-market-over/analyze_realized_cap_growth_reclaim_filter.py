"""
VALIDASI P3 - realized_cap_growth_reclaim_filter

Klaim video: rally yang bertahan diikuti masuknya MODAL RIIL; rally squeeze
murni tidak. Proxy modal riil = realized_cap_usd.

Sample: 13 event "sentuhan STH RP dari bawah di bear" hasil validasi
2026-08-04 (events_sth_rp_resistance_bear.csv) - definisi event TIDAK diubah.

Yang dihitung per event:
  A. AT-GATE MURNI (bisa dipakai sebagai filter di hari event):
       d_rc_pre14  = %perubahan realized_cap_usd dari (t-14) ke t
       d_rc_pre30  = %perubahan realized_cap_usd dari (t-30) ke t
  B. KONFIRMASI (baru tersedia 14/30 hari setelah event - BUKAN gate hari-H,
     jadi hanya dipakai sebagai filter konfirmasi):
       d_rc_post14 = %perubahan realized_cap_usd dari t ke (t+14)
       d_rc_post30 = %perubahan realized_cap_usd dari t ke (t+30)

Label outcome (dari file event lama, tidak diubah):
  - "BERTAHAN"  = outcome BREAK DAN balik_bawah_sthrp_dlm_90d == False
  - "GAGAL"     = sisanya (DITOLAK, atau BREAK tapi balik ke bawah <=90 hari)
Event 2025-26 bertanda censored (window 90 hari belum penuh) diberi tanda.
"""

import pandas as pd
import numpy as np

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
BASE = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos"
EVSRC = BASE + r"\2026-08-04_bitcoins-top-buyers-are-finally-capitulating\events_sth_rp_resistance_bear.csv"
OUTDIR = BASE + r"\2026-08-25_is-the-bitcoin-bear-market-over"

df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "realized_cap_usd", "sth_cost_basis"]).reset_index(drop=True)
LAST = df["date"].max()
print("Data master:", df["date"].min().date(), "s/d", LAST.date())
print("realized_cap_usd tersedia sejak:", df["date"].min().date(), "(full history - tidak ada masalah data mulai belakangan)")

ev = pd.read_csv(EVSRC, parse_dates=["event_date"])
print(f"\nSample event dari validasi 2026-08-04: n={len(ev)}")


def rc_at(d):
    sub = df[df["date"] <= d]
    if len(sub) == 0:
        return np.nan
    if (d - sub.iloc[-1]["date"]).days > 5:
        return np.nan
    return float(sub.iloc[-1]["realized_cap_usd"])


rows = []
for _, r in ev.iterrows():
    d = r["event_date"]
    rc0 = rc_at(d)

    def pct(a, b):
        if np.isnan(a) or np.isnan(b) or a == 0:
            return np.nan
        return round((b / a - 1) * 100, 2)

    pre14 = pct(rc_at(d - pd.Timedelta(days=14)), rc0)
    pre30 = pct(rc_at(d - pd.Timedelta(days=30)), rc0)
    post14 = pct(rc0, rc_at(d + pd.Timedelta(days=14))) if d + pd.Timedelta(days=14) <= LAST else np.nan
    post30 = pct(rc0, rc_at(d + pd.Timedelta(days=30))) if d + pd.Timedelta(days=30) <= LAST else np.nan

    balik = r["balik_bawah_sthrp_dlm_90d"]
    balik_bool = (str(balik).strip().lower() == "true")
    bertahan = (r["outcome"] == "BREAK") and (not balik_bool) and (str(balik) != "nan")
    label = "BERTAHAN" if bertahan else "GAGAL"
    rows.append({
        "cycle": r["cycle"], "event_date": d.strftime("%Y-%m-%d"),
        "outcome_lama": r["outcome"], "balik_bawah_90d": balik,
        "label": label, "censored": bool(r["censored_cycle"]),
        "d_rc_pre14_pct": pre14, "d_rc_pre30_pct": pre30,
        "d_rc_post14_pct": post14, "d_rc_post30_pct": post30,
        "ret_30d_pct": r["ret_30d_pct"],
    })

out = pd.DataFrame(rows)
out.to_csv(OUTDIR + r"\events_realized_cap_growth_reclaim_filter.csv", index=False)

print("\n" + "=" * 118)
print("DELTA REALIZED CAP DI SEKITAR 13 EVENT SENTUHAN STH RP (BEAR)")
print("=" * 118)
print(f"{'cyc':<6}{'event':<12}{'outcome':<10}{'label':<10}{'pre14%':>9}{'pre30%':>9}{'post14%':>10}{'post30%':>10}{'ret30d%':>10}  cat")
print("-" * 118)


def s(x):
    return "     n/a" if (isinstance(x, float) and np.isnan(x)) else f"{x:>8.2f}"


for _, r in out.iterrows():
    print(f"{str(r['cycle']):<6}{r['event_date']:<12}{r['outcome_lama']:<10}{r['label']:<10}"
          f"{s(r['d_rc_pre14_pct']):>9}{s(r['d_rc_pre30_pct']):>9}{s(r['d_rc_post14_pct']):>10}"
          f"{s(r['d_rc_post30_pct']):>10}{r['ret_30d_pct']:>10.1f}"
          + ("  [censored]" if r["censored"] else ""))

print("\nSEBARAN PER CYCLE:")
for c, g in out.groupby("cycle"):
    print(f"   cycle {c}: n={len(g)} | BERTAHAN={int((g['label']=='BERTAHAN').sum())} "
          f"GAGAL={int((g['label']=='GAGAL').sum())}")

print("\n" + "=" * 118)
print("PEMISAHAN: BERTAHAN vs GAGAL")
print("=" * 118)
for lab, g in out.groupby("label"):
    print(f"\n{lab}  (n={len(g)}): {list(g['event_date'])}")
    for col in ["d_rc_pre14_pct", "d_rc_pre30_pct", "d_rc_post14_pct", "d_rc_post30_pct"]:
        v = g[col].dropna()
        if len(v):
            print(f"   {col:<18} median={v.median():>7.2f}%  min={v.min():>7.2f}%  max={v.max():>7.2f}%  (n={len(v)})")

# overlap check
print("\n" + "-" * 118)
print("CEK OVERLAP (apakah nilai kelompok BERTAHAN di luar rentang kelompok GAGAL?)")
print("-" * 118)
b = out[out["label"] == "BERTAHAN"]
g_ = out[out["label"] == "GAGAL"]
for col in ["d_rc_pre14_pct", "d_rc_pre30_pct", "d_rc_post14_pct", "d_rc_post30_pct"]:
    bv = b[col].dropna()
    gv = g_[col].dropna()
    if len(bv) == 0 or len(gv) == 0:
        print(f"  {col:<18} tidak bisa dibandingkan (kelompok kosong)")
        continue
    n_gagal_lebih_tinggi = int((gv >= bv.min()).sum())
    print(f"  {col:<18} BERTAHAN min={bv.min():>7.2f}% | GAGAL: {n_gagal_lebih_tinggi} dari {len(gv)} "
          f"event punya nilai >= min BERTAHAN -> {'TIDAK memisahkan' if n_gagal_lebih_tinggi > 0 else 'memisahkan'}")

# kandidat 2026
print("\n" + "-" * 118)
print("EVENT 2025-26 (kandidat berjalan / censored)")
print("-" * 118)
for _, r in out[out["cycle"] == 2025].iterrows():
    print(f"  {r['event_date']}  outcome={r['outcome_lama']}  label={r['label']}  "
          f"pre14={r['d_rc_pre14_pct']}%  pre30={r['d_rc_pre30_pct']}%  "
          f"post14={r['d_rc_post14_pct']}%  post30={r['d_rc_post30_pct']}%")

# baseline: laju realized cap harian di bear vs bull (konteks)
print("\n" + "-" * 118)
print("KONTEKS - laju perubahan realized_cap 30 hari, distribusi seluruh sejarah")
print("-" * 118)
df["rc_chg30"] = df["realized_cap_usd"].pct_change(30) * 100
q = df["rc_chg30"].dropna().quantile([0.1, 0.25, 0.5, 0.75, 0.9])
for k, v in q.items():
    print(f"   persentil {int(k*100):>2}%: {v:>7.2f}%")
print(f"   nilai 30 hari terakhir ({LAST.date()}): {float(df.iloc[-1]['rc_chg30']):.2f}%")
print(f"\nCSV -> {OUTDIR}\\events_realized_cap_growth_reclaim_filter.csv")
