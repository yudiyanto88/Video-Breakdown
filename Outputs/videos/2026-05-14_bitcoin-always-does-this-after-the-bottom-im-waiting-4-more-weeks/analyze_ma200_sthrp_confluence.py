"""
V2 - Confluence 200 DMA + STH RP sebagai resistance saat bear (PRIORITAS TERTINGGI)

Menjawab Flag Prioritas #1 yang masih terbuka dari analisis 2026-08-04:
Signal D (harga > STH RP >=3 hari) hit rate ~12% -> usulan dipasangkan dengan
reclaim 200D MA. Pertanyaan operasionalnya: apakah filter 200 DMA menyingkirkan
sebagian dari 7 event palsu TANPA membuang 1 event asli (2023-01-11)?

DEFINISI (dikunci sebelum menghitung):
  - Zona harian = Zone Structure v2 (Decision_Framework v2.md sec.1).
  - Fase bear (PRIMARY, sesuai instruksi) = hari berlabel ZC / Z1 / Z1b.
  - Event reclaim 200DMA: btc_price[t-1] < 200_dma[t-1] DAN btc_price[t] >= 200_dma[t],
    dengan hari t berlabel bear. Merge event dalam 30 hari jadi satu (ambil yang pertama).
  - Outcome window 30 hari (t+1..t+30):
      DITOLAK      = ada minimal satu close < 200_dma
      BREAK-TAHAN  = semua 30 hari close >= 200_dma
    (event yang window 30 harinya belum tertutup ditandai CENSORED, tidak dihitung
     ke hit rate)
  - Forward return 30/90 hari (dari close di tanggal event). Return yang windownya
    belum tertutup = NaN.
  - Confluence AT-GATE (tidak ada lookahead): pada tanggal event hitung
    gap = abs(200_dma - sth_cost_basis) / btc_price. Subset <=5% vs >5%.
  - Uji silang: 8 event BREAK Signal D dari events_sth_rp_resistance_bear.csv
    (analisis 2026-08-04) -> di 'break_date' (hari ke-3 streak di atas STH RP),
    apakah btc_price >= 200_dma?

Sensitivitas (dilaporkan terpisah, BUKAN untuk memilih hasil terbaik):
  - Fase bear ALT = ZC / ZD / Z1 / Z1b (karena bear 2025-26 berlabel ZD, bukan Z1).

Output print ASCII saja.
"""

import numpy as np
import os
import pandas as pd

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = (r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos"
          r"\2026-05-14_bitcoin-always-does-this-after-the-bottom-im-waiting-4-more-weeks")
PRECEDENT = (r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos"
             r"\2026-08-04_bitcoins-top-buyers-are-finally-capitulating"
             r"\events_sth_rp_resistance_bear.csv")

MERGE_DAYS = 30
OUT_WINDOW = 30
GAP_THRESHOLD = 0.05

# ---------------------------------------------------------------- load
df = pd.read_csv(MASTER, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "sth_cost_basis", "realized_price",
                       "lth_cost_basis", "200_dma"]).copy()
df = df[df["btc_price"] > 0].reset_index(drop=True)
LAST = df["date"].max()

aviv_mean = df["price_at_aviv_mean"].values
aviv_up = (df["price_at_aviv_mean"] + 0.5 *
           (df["price_at_aviv_plus_1_sigma"] - df["price_at_aviv_mean"])).values

price = df["btc_price"].values
sth = df["sth_cost_basis"].values
rp = df["realized_price"].values
lth = df["lth_cost_basis"].values
ma200 = df["200_dma"].values
dates = df["date"].values


def zone_label(p, s, r, l, am, au):
    if any(pd.isna(x) for x in [p, s, r, l]):
        return "NA"
    d1 = abs(s - r) / r
    d2 = abs(r - l) / r
    struct = "C" if (d1 < 0.02 and d2 < 0.02) else ("N" if s > r else "T")
    if not pd.isna(au) and p >= au:
        return "Z5"
    if struct == "N":
        if p < r:
            return "ZC"
        if p < s:
            return "ZD"
        if pd.isna(am) or p < am:
            return "Z3"
        return "Z4"
    if struct == "T":
        if p < s:
            return "Z1"
        if p < r:
            return "Z1b"
        return "Z2-transisi"
    if pd.isna(am) or p < am:
        return "Z2"
    return "Z4"


zones = np.array([zone_label(price[i], sth[i], rp[i], lth[i], aviv_mean[i], aviv_up[i])
                  for i in range(len(df))])
df["zone"] = zones

CYCLE_BOUNDS = [("2011", "2010-07-17", "2012-12-31"),
                ("2013-15", "2013-01-01", "2016-12-31"),
                ("2017-19", "2017-01-01", "2020-12-31"),
                ("2021-23", "2021-01-01", "2024-12-31"),
                ("2025-26", "2025-01-01", "2030-12-31")]


def cycle_of(d):
    for c, a, b in CYCLE_BOUNDS:
        if pd.Timestamp(a) <= d <= pd.Timestamp(b):
            return c
    return "?"


print("=" * 108)
print("V2 - CONFLUENCE 200 DMA + STH RP SEBAGAI RESISTANCE SAAT BEAR")
print("=" * 108)
print("Data: %s s/d %s (n=%d hari). TANGGAL DATA TERAKHIR = %s"
      % (df["date"].min().date(), LAST.date(), len(df), LAST.date()))
print("\nDistribusi label zona seluruh histori:")
for z, c in pd.Series(zones).value_counts().items():
    print("   %-12s %5d hari" % (z, c))


def run_events(bear_set, tag):
    is_bear = np.isin(zones, list(bear_set))
    print("\n" + "=" * 108)
    print("DEFINISI BEAR %s -> %s  (%d hari bear)" % (tag, "/".join(sorted(bear_set)), is_bear.sum()))
    print("=" * 108)

    raw = []
    for i in range(1, len(df)):
        if price[i - 1] < ma200[i - 1] and price[i] >= ma200[i] and is_bear[i]:
            raw.append(i)
    # merge dalam 30 hari
    merged = []
    for i in raw:
        if merged and (pd.Timestamp(dates[i]) - pd.Timestamp(dates[merged[-1]])).days <= MERGE_DAYS:
            continue
        merged.append(i)
    print("Raw cross-up di hari bear = %d  ->  setelah merge %dd = %d event"
          % (len(raw), MERGE_DAYS, len(merged)))

    rows = []
    for i in merged:
        d0 = pd.Timestamp(dates[i])
        fut = slice(i + 1, min(i + 1 + OUT_WINDOW, len(df)))
        pf, mf = price[fut], ma200[fut]
        closed = (len(pf) == OUT_WINDOW)
        if not closed:
            outcome = "CENSORED"
        else:
            outcome = "DITOLAK" if (pf < mf).any() else "BREAK-TAHAN"
        # hari pertama balik di bawah 200dma
        below = np.where(pf < mf)[0]
        days_to_fail = int(below[0] + 1) if len(below) else np.nan

        def fwd(h):
            j = i + h
            return round((price[j] / price[i] - 1) * 100, 1) if j < len(df) else np.nan

        gap = abs(ma200[i] - sth[i]) / price[i]
        rows.append(dict(
            cycle=cycle_of(d0), event_date=d0.date(), zone=zones[i],
            price=round(price[i], 2), ma200=round(ma200[i], 2), sth_rp=round(sth[i], 2),
            gap_at_gate_pct=round(gap * 100, 2),
            confluence=("KETAT <=5%" if gap <= GAP_THRESHOLD else "LEBAR >5%"),
            outcome=outcome, hari_ke_gagal=days_to_fail,
            ret_30d_pct=fwd(30), ret_90d_pct=fwd(90),
            price_vs_sth_pct=round(price[i] / sth[i] * 100, 1)))
    ev = pd.DataFrame(rows)
    return ev


pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)

# =====================================================================
# PRIMARY
# =====================================================================
ev = run_events({"ZC", "Z1", "Z1b"}, "PRIMARY")
if len(ev):
    print("\n" + ev[["cycle", "event_date", "zone", "price", "ma200", "sth_rp",
                     "gap_at_gate_pct", "confluence", "outcome", "hari_ke_gagal",
                     "ret_30d_pct", "ret_90d_pct"]].to_string(index=False))
    print("\n--- n TOTAL & SEBARAN PER CYCLE ---")
    print("n total event = %d" % len(ev))
    print(ev.groupby("cycle")["outcome"].value_counts().unstack(fill_value=0).to_string())
    dec = ev[ev["outcome"] != "CENSORED"]
    if len(dec):
        nrej = (dec["outcome"] == "DITOLAK").sum()
        print("\nDari %d event yang windownya TERTUTUP: DITOLAK %d (%.0f%%) | "
              "BREAK-TAHAN %d (%.0f%%)"
              % (len(dec), nrej, 100 * nrej / len(dec), len(dec) - nrej,
                 100 * (len(dec) - nrej) / len(dec)))
        for grp in ["DITOLAK", "BREAK-TAHAN"]:
            g = dec[dec["outcome"] == grp]
            if len(g):
                print("  %-12s n=%d | ret30d median %+.1f%% | ret90d median %+.1f%%"
                      % (grp, len(g), g["ret_30d_pct"].median(),
                         g["ret_90d_pct"].median() if g["ret_90d_pct"].notna().any() else float('nan')))
        print("\n--- CONFLUENCE at-gate (gap = |200DMA - STH RP| / harga) ---")
        for lab in ["KETAT <=5%", "LEBAR >5%"]:
            g = dec[dec["confluence"] == lab]
            if len(g):
                r = (g["outcome"] == "DITOLAK").sum()
                print("  %-11s n=%d | rejection rate %.0f%% (%d/%d) | ret30d median %+.1f%%"
                      % (lab, len(g), 100 * r / len(g), r, len(g), g["ret_30d_pct"].median()))
            else:
                print("  %-11s n=0" % lab)
    ev.to_csv(os.path.join(OUTDIR, "events_ma200_sthrp_confluence.csv"), index=False)
    print("\nCSV -> events_ma200_sthrp_confluence.csv")

# =====================================================================
# SENSITIVITAS (bear ALT termasuk ZD)
# =====================================================================
ev_alt = run_events({"ZC", "ZD", "Z1", "Z1b"}, "SENSITIVITAS")
if len(ev_alt):
    print("\n" + ev_alt[["cycle", "event_date", "zone", "price", "ma200", "sth_rp",
                         "gap_at_gate_pct", "confluence", "outcome", "hari_ke_gagal",
                         "ret_30d_pct", "ret_90d_pct"]].to_string(index=False))
    print("\nn total = %d" % len(ev_alt))
    print(ev_alt.groupby("cycle")["outcome"].value_counts().unstack(fill_value=0).to_string())
    dec = ev_alt[ev_alt["outcome"] != "CENSORED"]
    nrej = (dec["outcome"] == "DITOLAK").sum()
    print("Tertutup: DITOLAK %d/%d (%.0f%%)" % (nrej, len(dec), 100 * nrej / len(dec)))
    for lab in ["KETAT <=5%", "LEBAR >5%"]:
        g = dec[dec["confluence"] == lab]
        if len(g):
            r = (g["outcome"] == "DITOLAK").sum()
            print("  %-11s n=%d | rejection rate %.0f%% | ret30d median %+.1f%%"
                  % (lab, len(g), 100 * r / len(g), g["ret_30d_pct"].median()))
    ev_alt.to_csv(os.path.join(OUTDIR, "events_ma200_sthrp_confluence_alt.csv"), index=False)
    print("CSV -> events_ma200_sthrp_confluence_alt.csv")

# =====================================================================
# KORELASI 200DMA vs STH RP selama bear
# =====================================================================
print("\n" + "=" * 108)
print("KORELASI 200_dma vs sth_cost_basis SELAMA HARI BEAR")
print("=" * 108)
for tag, bs in [("PRIMARY ZC/Z1/Z1b", {"ZC", "Z1", "Z1b"}),
                ("ALT ZC/ZD/Z1/Z1b", {"ZC", "ZD", "Z1", "Z1b"}),
                ("SEMUA HARI", set(pd.unique(zones)))]:
    m = np.isin(zones, list(bs))
    a, b = ma200[m], sth[m]
    r_lvl = np.corrcoef(np.log(a), np.log(b))[0, 1]
    da, db = np.diff(np.log(a)), np.diff(np.log(b))
    r_chg = np.corrcoef(da, db)[0, 1]
    print("  %-20s n=%5d | r(log level) = %+.3f | r(perubahan harian log) = %+.3f"
          % (tag, m.sum(), r_lvl, r_chg))
print("\n  CATATAN: kalau r(log level) sangat tinggi, 'confluence 200DMA + STH RP'")
print("  BUKAN dua bukti independen melainkan pengukuran ganda dari hal yang sama")
print("  (dua-duanya rata-rata bergerak dari harga yang sama, beda cara bobot).")
print("  Gap |200DMA - STH RP|/harga selama bear PRIMARY:")
m = np.isin(zones, ["ZC", "Z1", "Z1b"])
g = np.abs(ma200[m] - sth[m]) / price[m]
print("    median %.1f%% | p25 %.1f%% | p75 %.1f%% | share hari gap<=5%% = %.0f%%"
      % (np.median(g) * 100, np.percentile(g, 25) * 100,
         np.percentile(g, 75) * 100, 100 * (g <= GAP_THRESHOLD).mean()))

# =====================================================================
# UJI SILANG ke 8 event BREAK Signal D (analisis 2026-08-04)
# =====================================================================
print("\n" + "=" * 108)
print("UJI SILANG: FILTER 200DMA DIPASANG DI 8 EVENT BREAK SIGNAL D (findings 2026-08-04)")
print("=" * 108)
prec = pd.read_csv(PRECEDENT)
brk = prec[prec["outcome"] == "BREAK"].copy()
brk["break_date"] = pd.to_datetime(brk["break_date"])
dmap = df.set_index("date")

rows = []
for _, r in brk.iterrows():
    bd = r["break_date"]
    if bd not in dmap.index:
        continue
    x = dmap.loc[bd]
    asli = (str(r["unlock_dlm_90d"]) != "TIDAK")
    rows.append(dict(
        cycle=r["cycle"], event_date=r["event_date"], break_date=bd.date(),
        price=round(x["btc_price"], 2), ma200=round(x["200_dma"], 2),
        sth_rp=round(x["sth_cost_basis"], 2),
        price_vs_ma200_pct=round(x["btc_price"] / x["200_dma"] * 100, 1),
        di_atas_200dma=bool(x["btc_price"] >= x["200_dma"]),
        gap_ma200_sth_pct=round(abs(x["200_dma"] - x["sth_cost_basis"]) / x["btc_price"] * 100, 2),
        zone=x["zone"],
        break_asli=asli,
        balik_bawah_sthrp_90d=r["balik_bawah_sthrp_dlm_90d"]))
xs = pd.DataFrame(rows)
print(xs.to_string(index=False))

tot = len(xs)
above = xs["di_atas_200dma"].sum()
asli = xs[xs["break_asli"]]
palsu = xs[~xs["break_asli"]]
print("\n  n break Signal D historis = %d" % tot)
print("  Di atas 200DMA pada hari ke-3 break : %d dari %d" % (above, tot))
print("  Break ASLI (diikuti unlock <=90d)   : n=%d -> di atas 200DMA: %d"
      % (len(asli), asli["di_atas_200dma"].sum()))
print("  Break PALSU                         : n=%d -> di atas 200DMA: %d (tersaring keluar: %d)"
      % (len(palsu), palsu["di_atas_200dma"].sum(),
         len(palsu) - palsu["di_atas_200dma"].sum()))
if len(asli):
    keep_real = asli["di_atas_200dma"].all()
    print("\n  => Filter 200DMA membuang event ASLI? %s" % ("YA" if not keep_real else "TIDAK"))
    lolos = xs[xs["di_atas_200dma"]]
    if len(lolos):
        print("  => Setelah filter: %d event lolos, %d di antaranya asli -> hit rate %.0f%% "
              "(sebelumnya %d/%d = %.0f%%)"
              % (len(lolos), lolos["break_asli"].sum(),
                 100 * lolos["break_asli"].sum() / len(lolos),
                 len(asli), tot, 100 * len(asli) / tot))
xs.to_csv(os.path.join(OUTDIR, "events_ma200_sthrp_crosscheck_signalD.csv"), index=False)
print("\nCSV -> events_ma200_sthrp_crosscheck_signalD.csv")
