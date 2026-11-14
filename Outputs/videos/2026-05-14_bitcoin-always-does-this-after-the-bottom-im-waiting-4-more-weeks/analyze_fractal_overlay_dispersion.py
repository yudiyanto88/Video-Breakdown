"""
V3 - Falsifikasi metode bar-pattern fractal overlay (post-low)

Video meng-overlay price action setelah lowest closing price bear sebelumnya
(2015 / 2018-19 / 2022) ke low 2026, lalu membaca proyeksi tanggal dari situ.

Yang diuji di sini adalah METODE-nya, bukan salah satu fractal:
kalau jalur post-low antar cycle sangat berbeda satu sama lain, overlay
manapun tidak punya isi prediktif -- terlepas dari fractal mana yang dipilih.

Definisi event eksplisit:
  - ATH cycle = running max close yang jadi puncak sebelum bear
  - cycle low = min close antara ATH dan ATH berikutnya
  - jalur post-low = P(t)/P(low) untuk t = 0..180 hari kalender sejak cycle low
Anti-lookahead: tidak relevan untuk deskripsi jalur (ini memang studi ex-post
tentang dispersi), TAPI dicatat eksplisit bahwa metode overlay ITU SENDIRI
butuh tahu di mana low-nya -- yang baru diketahui setelah fakta. Ini diuji
di bagian (5).

Output print ASCII-only (Windows console).
"""

import pandas as pd
import numpy as np

CSV = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"
OUTDIR = r"D:\Claude Code\Projects\Content-Breakdown\Outputs\videos\2026-05-14_bitcoin-always-does-this-after-the-bottom-im-waiting-4-more-weeks"

VIDEO_DATE = pd.Timestamp("2026-05-14")

df = pd.read_csv(CSV, parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df[df["btc_price"] > 0].reset_index(drop=True)
s = df.set_index("date")["btc_price"]
LAST = s.index.max()

print("=" * 108)
print("V3 - FALSIFIKASI METODE BAR-PATTERN FRACTAL OVERLAY (post-low)")
print("=" * 108)
print(f"Data: {s.index.min().date()} s/d {LAST.date()} (n={len(s)} hari). TANGGAL DATA TERAKHIR = {LAST.date()}")

# ---------------------------------------------------------------------------
# (1) Cycle ATH & cycle low objektif
# ---------------------------------------------------------------------------
# Window pencarian ATH per cycle ditetapkan a priori dari sejarah halving/cycle
# yang sudah umum dipakai (bukan hasil tuning): puncak 2011, 2013, 2017, 2021, 2025.
CYCLE_WINDOWS = [
    ("2011",    "2011-01-01", "2012-12-31"),
    ("2013-15", "2013-01-01", "2015-12-31"),
    ("2017-19", "2017-01-01", "2019-06-30"),
    ("2021-23", "2021-01-01", "2023-06-30"),
    ("2025-26", "2025-01-01", None),          # ongoing / censored
]

rows = []
for name, a, b in CYCLE_WINDOWS:
    seg = s.loc[a:] if b is None else s.loc[a:b]
    ath_date = seg.idxmax()
    ath = seg.loc[ath_date]
    post = seg.loc[ath_date:]
    low_date = post.idxmin()
    low = post.loc[low_date]
    ongoing = b is None
    rows.append(dict(
        cycle=name, ath_date=ath_date, ath=ath,
        low_date=low_date, low=low,
        days_ath_to_low=(low_date - ath_date).days,
        max_dd_pct=(low / ath - 1) * 100,
        ongoing=ongoing,
    ))
cyc = pd.DataFrame(rows)

print("\n" + "-" * 108)
print("(1) CYCLE ATH -> CYCLE LOW (objektif dari btc_price)")
print("-" * 108)
show = cyc.copy()
show["ath_date"] = show["ath_date"].dt.date
show["low_date"] = show["low_date"].dt.date
print(show.to_string(index=False,
      formatters={"ath": "{:,.0f}".format, "low": "{:,.0f}".format,
                  "max_dd_pct": "{:+.1f}".format}))
print("\n  CATATAN: cycle 2025-26 masih BERJALAN (censored) -- 'low' di atas adalah")
print("  low SEJAUH INI, bukan cycle low final. Tidak boleh dipakai setara 4 cycle selesai.")

# ---------------------------------------------------------------------------
# (2) Jalur post-low ternormalisasi P(t)/P(low)
# ---------------------------------------------------------------------------
HORIZONS = [30, 60, 90, 120, 180]
MAXT = 180

paths = {}
for r in cyc.itertuples():
    idx = pd.date_range(r.low_date, r.low_date + pd.Timedelta(days=MAXT), freq="D")
    seg = s.reindex(idx).ffill()
    paths[r.cycle] = seg / r.low

closed = [c for c in paths if not bool(cyc.set_index("cycle").loc[c, "ongoing"])]

print("\n" + "-" * 108)
print("(2) JALUR POST-LOW TERNORMALISASI  P(t)/P(low)  -- n=4 bear SELESAI")
print("-" * 108)
tab = []
for h in HORIZONS:
    vals = {}
    for c in closed:
        p = paths[c]
        d = p.index[0] + pd.Timedelta(days=h)
        vals[c] = p.loc[d] if d in p.index and not pd.isna(p.loc[d]) else np.nan
    v = np.array([x for x in vals.values() if not pd.isna(x)])
    row = {"t": f"t+{h}"}
    row.update({c: vals[c] for c in closed})
    row["min"] = v.min()
    row["max"] = v.max()
    row["max/min"] = v.max() / v.min()
    tab.append(row)
tab = pd.DataFrame(tab)
print(tab.to_string(index=False, float_format=lambda x: f"{x:.2f}"))

print("\n  Baca: angka 1.50 = harga 50% di atas cycle low. Kolom max/min = seberapa")
print("  lebar rentang antar-cycle di horizon itu. max/min besar = jalur tidak seragam.")

# ---------------------------------------------------------------------------
# (3) Korelasi pairwise log-return harian antar jalur post-low
# ---------------------------------------------------------------------------
print("\n" + "-" * 108)
print("(3) KORELASI PAIRWISE (Pearson pada log-return harian, t=0..180) ANTAR JALUR POST-LOW")
print("-" * 108)
lr = {}
for c in closed:
    lr[c] = np.log(paths[c]).diff().dropna().reset_index(drop=True)
L = pd.DataFrame(lr)
cm = L.corr()
print(cm.to_string(float_format=lambda x: f"{x:+.3f}"))
off = cm.values[np.triu_indices_from(cm.values, k=1)]
print(f"\n  Korelasi pairwise: n_pasang={len(off)} | median {np.median(off):+.3f} | "
      f"min {off.min():+.3f} | max {off.max():+.3f}")

# ---------------------------------------------------------------------------
# (4) Verdict dispersi
# ---------------------------------------------------------------------------
r90 = tab.loc[tab["t"] == "t+90"].iloc[0]
print("\n" + "-" * 108)
print("(4) VERDICT DISPERSI")
print("-" * 108)
print(f"  Di t+90: rentang {r90['min']:.2f}x - {r90['max']:.2f}x dari cycle low "
      f"(max/min = {r90['max/min']:.2f}x)")
print(f"  Korelasi log-return harian antar jalur: median {np.median(off):+.3f}")
if r90["max/min"] >= 1.5 and abs(np.median(off)) < 0.3:
    print("  => Jalur post-low TIDAK seragam dan pergerakan hariannya praktis tidak")
    print("     berkorelasi. Overlay fractal dari satu cycle ke cycle lain CENDERUNG")
    print("     tidak punya isi prediktif. HASIL NEGATIF = HASIL VALID.")
else:
    print("  => Dispersi/korelasi tidak memenuhi ambang falsifikasi yang ditetapkan;")
    print("     baca angka per horizon di atas sebelum menyimpulkan.")

# ---------------------------------------------------------------------------
# (5) Ex-post: anchor video vs kenyataan
# ---------------------------------------------------------------------------
print("\n" + "-" * 108)
print("(5) EX-POST -- APAKAH ANCHOR VIDEO MASIH VALID?")
print("-" * 108)
feb = s.loc["2026-01-01":"2026-03-31"]
feb_low_date, feb_low = feb.idxmin(), feb.min()
after = s.loc[VIDEO_DATE:]
post_low_date, post_low = after.idxmin(), after.min()
print(f"  Anchor yang dipakai video   : low Feb 2026 = ${feb_low:,.0f} @ {feb_low_date.date()}")
print(f"  Low TERENDAH setelah video  : ${post_low:,.0f} @ {post_low_date.date()}")
if post_low < feb_low:
    print(f"  => Anchor video SUDAH TERTEMBUS ({post_low/feb_low-1:+.1%}). Seluruh proyeksi")
    print("     fractal di video dipasang dari titik yang ternyata BUKAN low -- jadi")
    print("     salah bukan karena fractal-nya, tapi karena anchor-nya baru bisa")
    print("     diketahui setelah fakta. Ini cacat struktural metode, bukan nasib buruk.")
else:
    print("  => Anchor video masih bertahan sampai akhir data.")

# jalur aktual 2026 dari anchor video vs 3 fractal
print("\n  Jalur aktual dari anchor video vs jalur ketiga fractal (normalisasi ke anchor):")
idx = pd.date_range(feb_low_date, min(feb_low_date + pd.Timedelta(days=MAXT), LAST), freq="D")
actual = (s.reindex(idx).ffill() / feb_low)
rowsx = []
for h in HORIZONS:
    d = feb_low_date + pd.Timedelta(days=h)
    if d > LAST:
        rowsx.append({"t": f"t+{h}", "aktual_2026": np.nan, **{c: paths[c].iloc[min(h, MAXT)] for c in closed}})
        continue
    rowsx.append({"t": f"t+{h}", "aktual_2026": actual.loc[d],
                  **{c: paths[c].loc[paths[c].index[0] + pd.Timedelta(days=h)] for c in closed}})
X = pd.DataFrame(rowsx)
print(X.to_string(index=False, float_format=lambda x: f"{x:.2f}", na_rep="  (di luar data)"))

covered = X.dropna(subset=["aktual_2026"])
if len(covered):
    last_row = covered.iloc[-1]
    diffs = {c: abs(last_row[c] - last_row["aktual_2026"]) for c in closed}
    best = min(diffs, key=diffs.get)
    print(f"\n  Horizon terjauh yang tertutup data: {last_row['t']} "
          f"(aktual {last_row['aktual_2026']:.2f}x)")
    print(f"  Fractal terdekat di titik itu: {best} ({last_row[best]:.2f}x, selisih {diffs[best]:.2f})")
    print("  CATATAN: 'terdekat' di SATU titik bukan bukti prediktif -- dengan 3 fractal")
    print("  yang saling bertentangan, selalu ada satu yang kebetulan paling dekat.")

# CSV
out = []
for c in closed + [x for x in paths if x not in closed]:
    p = paths[c]
    for i, (d, v) in enumerate(p.items()):
        out.append(dict(cycle=c, t_days=i, date=d.date(), norm_vs_low=v))
for i, (d, v) in enumerate(actual.items()):
    out.append(dict(cycle="2026_anchor_video", t_days=i, date=d.date(), norm_vs_low=v))
O = pd.DataFrame(out)
O.to_csv(rf"{OUTDIR}\events_fractal_overlay_dispersion.csv", index=False)
print(f"\nCSV -> events_fractal_overlay_dispersion.csv  ({len(O)} baris)")
