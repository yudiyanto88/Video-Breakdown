"""
V1 - Kalibrasi ex-post call Matt Crosby (video 2026-05-14)

Menguji satu per satu klaim bertanggal di video terhadap data aktual.
CATATAN: data master berakhir 2026-07-15 -> window prediksi 4-8 minggu HANYA
sebagian tertutup. Semua bagian yang belum tertutup ditandai PARTIAL.

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

LAST = df["date"].max()

# --- 365D MA: tidak tersedia siap pakai, hitung rolling(365) dari btc_price ---
df["365_dma"] = df["btc_price"].rolling(365, min_periods=365).mean()

# --- AVIV bands (ikut pola data_dictionary / analyze_k3_stage_comparison) ---
df["aviv_mean_usd"] = df["price_at_aviv_mean"]
df["aviv_upper_usd"] = df["price_at_aviv_mean"] + 0.5 * (
    df["price_at_aviv_plus_1_sigma"] - df["price_at_aviv_mean"]
)


def zone_label(p, sth, rp, lth, av_mean, av_up):
    """Zone Structure v2 (Decision_Framework v2.md section 1)."""
    if any(pd.isna(x) for x in [p, sth, rp, lth]):
        return "NA"
    d1 = abs(sth - rp) / rp
    d2 = abs(rp - lth) / rp
    if d1 < 0.02 and d2 < 0.02:
        struct = "C"
    elif sth > rp:
        struct = "N"
    else:
        struct = "T"

    if not pd.isna(av_up) and p >= av_up:
        return "Z5"
    if struct == "N":
        if p < rp:
            return "ZC"
        if p < sth:
            return "ZD"
        if pd.isna(av_mean) or p < av_mean:
            return "Z3"
        return "Z4"
    if struct == "T":
        if p < sth:
            return "Z1"
        if p < rp:
            return "Z1b"
        return "Z2-transisi"
    # struct == "C"
    if pd.isna(av_mean) or p < av_mean:
        return "Z2"
    return "Z4"


df["zone"] = [
    zone_label(r.btc_price, r.sth_cost_basis, r.realized_price, r.lth_cost_basis,
               r.aviv_mean_usd, r.aviv_upper_usd)
    for r in df.itertuples()
]

print("=" * 100)
print("V1 - KALIBRASI EX-POST CALL MATT CROSBY (video 2026-05-14)")
print("=" * 100)
print(f"Data master: {df['date'].min().date()} s/d {LAST.date()}  (n={len(df)} hari)")
print(f"Hari sejak tanggal video sampai akhir data: {(LAST - VIDEO_DATE).days} hari")
print("PERINGATAN: window 8 minggu (56 hari) TERTUTUP; window 60 hari fwd-return "
      "dari sentuhan yang terjadi setelah ~2026-05-16 BELUM tertutup -> PARTIAL")

# =====================================================================
# (a) Verifikasi angka yang disebut di video per 2026-05-14
# =====================================================================
print("\n" + "-" * 100)
print("(a) VERIFIKASI ANGKA PER 2026-05-14")
print("-" * 100)
row = df[df["date"] == VIDEO_DATE].iloc[0]
claims = [
    ("btc_price (video: sekitar $78.700-$81.900 di layar)", row.btc_price),
    ("sth_cost_basis / STH-RP (video bilang ~$79.000)", row.sth_cost_basis),
    ("200_dma (video: titik rejection)", row["200_dma"]),
    ("365D MA rolling(365) dari btc_price (video: '1-year MA' = deciding point)", row["365_dma"]),
    ("200_wma (video baca ~$57k, low confidence dari frame)", row["200_wma"]),
    ("realized_price", row.realized_price),
    ("aviv_mean_usd", row.aviv_mean_usd),
    ("aviv_upper_usd", row.aviv_upper_usd),
]
for name, val in claims:
    print(f"  {name:<70} = ${val:,.0f}")
print(f"  Zona framework 2026-05-14                                              = {row.zone}")
print(f"  Harga vs STH RP : {row.btc_price/row.sth_cost_basis*100:6.1f}% "
      f"| vs 200DMA : {row.btc_price/row['200_dma']*100:6.1f}% "
      f"| vs 365DMA : {row.btc_price/row['365_dma']*100:6.1f}%")

# rentang harga minggu video
wk = df[(df["date"] >= VIDEO_DATE - pd.Timedelta(days=7)) & (df["date"] <= VIDEO_DATE)]
print(f"  Rentang close 7 hari s/d 2026-05-14: ${wk.btc_price.min():,.0f} - ${wk.btc_price.max():,.0f}")

# =====================================================================
# (b) Call "top mid-Mei lalu beberapa minggu turun"
# =====================================================================
print("\n" + "-" * 100)
print("(b) CALL: TOP MID-MEI LALU BEBERAPA MINGGU TURUN")
print("-" * 100)
post = df[df["date"] > VIDEO_DATE].copy()
imax = post["btc_price"].idxmax()
print(f"  Close tertinggi SETELAH 2026-05-14 : ${post.loc[imax,'btc_price']:,.0f} "
      f"pada {post.loc[imax,'date'].date()}")
print(f"  Close 2026-05-14                    : ${row.btc_price:,.0f}")
print(f"  -> harga setelah video {'TIDAK PERNAH' if post.loc[imax,'btc_price'] < row.btc_price else 'SEMPAT'} "
      f"melampaui close hari video")

# apakah 2026-05-10 highest close di window sekitar
for w in (30, 45, 60, 90):
    win = df[(df["date"] >= pd.Timestamp("2026-05-10") - pd.Timedelta(days=w)) &
             (df["date"] <= pd.Timestamp("2026-05-10") + pd.Timedelta(days=w))]
    top = win.loc[win["btc_price"].idxmax()]
    print(f"  Window +/-{w:>2}d sekitar 2026-05-10 -> highest close ${top.btc_price:,.0f} "
          f"pada {top.date.date()}  {'(= 10 Mei)' if top.date == pd.Timestamp('2026-05-10') else '(BUKAN 10 Mei)'}")

# trajectory 4-8 minggu (dan seterusnya sampai akhir data)
print("\n  Trajectory dari close 2026-05-14 (${:,.0f}):".format(row.btc_price))
traj_rows = []
for wk_n in [2, 4, 6, 8, 9]:
    tgt = VIDEO_DATE + pd.Timedelta(days=7 * wk_n)
    if tgt > LAST:
        print(f"    +{wk_n:>2} minggu ({tgt.date()}): DI LUAR DATA (PARTIAL)")
        continue
    r2 = df[df["date"] <= tgt].iloc[-1]
    ret = r2.btc_price / row.btc_price - 1
    print(f"    +{wk_n:>2} minggu ({r2.date.date()}): ${r2.btc_price:,.0f}  ({ret*100:+.1f}%)  zona={r2.zone}")
    traj_rows.append({"minggu": wk_n, "tanggal": r2.date.date(), "close": round(r2.btc_price, 0),
                      "ret_vs_video": round(ret * 100, 1), "zona": r2.zone})

mn = post.loc[post["btc_price"].idxmin()]
print(f"  Max drawdown dari close hari video sampai akhir data: "
      f"{(mn.btc_price/row.btc_price - 1)*100:.1f}% (low ${mn.btc_price:,.0f} @ {mn.date.date()})")

# =====================================================================
# (c) Base case "$60.000 adalah low"
# =====================================================================
print("\n" + "-" * 100)
print("(c) BASE CASE '$60.000 = LOW, >50% CHANCE' (dan skenario mid-$50k 20-25%)")
print("-" * 100)
print(f"  Minimum close setelah 2026-05-14 : ${mn.btc_price:,.0f} pada {mn.date.date()}")
below60 = post[post["btc_price"] < 60000]
mid50 = post[(post["btc_price"] >= 55000) & (post["btc_price"] < 60000)]
below55 = post[post["btc_price"] < 55000]
print(f"  Hari close < $60.000              : {len(below60)}"
      + (f"  (pertama {below60['date'].min().date()}, terakhir {below60['date'].max().date()})" if len(below60) else ""))
print(f"  Hari close di mid-$50k ($55k-$60k): {len(mid50)}"
      + (f"  (pertama {mid50['date'].min().date()})" if len(mid50) else ""))
print(f"  Hari close < $55.000              : {len(below55)}")
# low Feb 2026 sebagai anchor "60k"
feb = df[(df["date"] >= "2026-01-01") & (df["date"] <= "2026-03-31")]
febmin = feb.loc[feb["btc_price"].idxmin()]
print(f"  Anchor video 'low Feb ~$60k'      : min close Jan-Mar 2026 = ${febmin.btc_price:,.0f} "
      f"@ {febmin.date.date()}")
print(f"  -> low Feb TERTEMBUS setelah video? {'YA' if mn.btc_price < febmin.btc_price else 'TIDAK'}"
      f" (selisih {(mn.btc_price/febmin.btc_price-1)*100:+.1f}%)")

# =====================================================================
# (d) "DCA agresif di ~$70.000"
# =====================================================================
print("\n" + "-" * 100)
print("(d) DCA AGRESIF DI ~$70.000")
print("-" * 100)
touch70 = post[post["btc_price"] <= 70000]
if len(touch70) == 0:
    print("  $70.000 TIDAK pernah tersentuh setelah 2026-05-14")
else:
    t0 = touch70.iloc[0]
    print(f"  Sentuhan pertama close <= $70.000 : {t0.date.date()} @ ${t0.btc_price:,.0f}")
    print(f"  Total hari close <= $70.000       : {len(touch70)} (terakhir {touch70['date'].max().date()})")
    for h in (30, 60):
        tgt = t0.date + pd.Timedelta(days=h)
        if tgt > LAST:
            avail = (LAST - t0.date).days
            r3 = df[df["date"] <= LAST].iloc[-1]
            print(f"  Fwd return {h}d dari {t0.date.date()}: BELUM TERTUTUP (PARTIAL, baru {avail} hari). "
                  f"Return sejauh ini {(r3.btc_price/t0.btc_price-1)*100:+.1f}% (per {LAST.date()})")
        else:
            r3 = df[df["date"] <= tgt].iloc[-1]
            print(f"  Fwd return {h}d dari {t0.date.date()}: {(r3.btc_price/t0.btc_price-1)*100:+.1f}% "
                  f"(${r3.btc_price:,.0f} @ {r3.date.date()})")

# =====================================================================
# (e) Zona resistance $81.000-$85.000
# =====================================================================
print("\n" + "-" * 100)
print("(e) ZONA RESISTANCE $81.000-$85.000")
print("-" * 100)
band = post[(post["btc_price"] >= 81000) & (post["btc_price"] <= 85000)]
print(f"  Hari close di band $81k-$85k setelah 2026-05-14 : {len(band)}")
if len(band):
    print(f"    tanggal: {', '.join(str(d.date()) for d in band['date'])}")
# episode masuk band (merge hari berurutan)
inband = ((post["btc_price"] >= 81000) & (post["btc_price"] <= 85000)).values
episodes = 0
prev = False
for v in inband:
    if v and not prev:
        episodes += 1
    prev = v
print(f"  Jumlah episode terpisah masuk band              : {episodes}")
above85 = post[post["btc_price"] > 85000]
print(f"  Hari close > $85.000                            : {len(above85)}")
# streak >=3 hari di atas 85k
streak, best = 0, 0
for v in (post["btc_price"] > 85000).values:
    streak = streak + 1 if v else 0
    best = max(best, streak)
print(f"  Streak terpanjang close > $85.000               : {best} hari "
      f"-> break bertahan >=3 hari? {'YA' if best >= 3 else 'TIDAK'}")

# =====================================================================
# (f) Posisi per tanggal data terakhir
# =====================================================================
print("\n" + "-" * 100)
print(f"(f) POSISI PER TANGGAL DATA TERAKHIR ({LAST.date()})")
print("-" * 100)
last = df.iloc[-1]
for name, val in [("btc_price", last.btc_price), ("sth_cost_basis (STH RP)", last.sth_cost_basis),
                  ("realized_price (RP)", last.realized_price), ("lth_cost_basis (LTH RP)", last.lth_cost_basis),
                  ("200_dma", last["200_dma"]), ("365D MA (rolling 365)", last["365_dma"]),
                  ("200_wma", last["200_wma"]), ("cvdd", last.cvdd),
                  ("AVIV Mean (USD)", last.aviv_mean_usd), ("AVIV Upper (+0.5SD, USD)", last.aviv_upper_usd)]:
    print(f"  {name:<28} = ${val:,.0f}")
print(f"  Harga / STH RP  = {last.btc_price/last.sth_cost_basis:.3f}  "
      f"({'DI BAWAH' if last.btc_price < last.sth_cost_basis else 'DI ATAS'} STH RP)")
print(f"  Harga / RP      = {last.btc_price/last.realized_price:.3f}")
print(f"  Harga / 200DMA  = {last.btc_price/last['200_dma']:.3f}")
print(f"  Harga / 365DMA  = {last.btc_price/last['365_dma']:.3f}")
print(f"  Harga / CVDD    = {last.btc_price/last.cvdd:.3f}")
print(f"  ZONA FRAMEWORK  = {last.zone}")

# distribusi zona sejak tanggal video
print("\n  Distribusi zona harian 2026-05-15 s/d akhir data:")
for z, c in post["zone"].value_counts().items():
    print(f"    {z:<12} {c:>4} hari")

# =====================================================================
# CSV event ringkas
# =====================================================================
ev = df[df["date"] >= VIDEO_DATE][["date", "btc_price", "sth_cost_basis", "realized_price",
                                   "200_dma", "365_dma", "200_wma", "zone"]].copy()
ev["pct_vs_video_close"] = (ev["btc_price"] / row.btc_price - 1) * 100
out = OUTDIR + r"\events_expost_calibration.csv"
ev.to_csv(out, index=False)
print(f"\n[saved] {out}  ({len(ev)} baris)")
