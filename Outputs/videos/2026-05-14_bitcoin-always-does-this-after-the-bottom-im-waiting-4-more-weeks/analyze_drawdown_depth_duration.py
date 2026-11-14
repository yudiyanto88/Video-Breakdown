"""
V4 - Drawdown depth & durasi ATH -> cycle low

Video memakai chart "Bitcoin Drawdowns from ATH to Cycle Low" untuk berargumen
bahwa bear ini "masih punya waktu panjang": cycle berjalan dibaca di ~-35%
pada hari ke-200-an, sementara cycle lama memanjang 600-800 hari & -75/-85%.

Yang diuji:
 (1) angka objektif per cycle dari btc_price
 (2) VERIFIKASI angka video: per 2026-05-14, berapa hari sejak ATH Okt 2025 dan
     berapa max drawdown? Video baca ~-35% pada low $62.200 -- benar atau ~-50%?
 (3) hubungan DESKRIPTIF kedalaman vs durasi (n=4 -> deskriptif saja, tidak
     diinferensikan)
 (4) status lantai waktu K4 per tanggal data terakhir

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
rp = df.set_index("date")["realized_price"]
LAST = s.index.max()

print("=" * 108)
print("V4 - DRAWDOWN DEPTH & DURASI ATH -> CYCLE LOW")
print("=" * 108)
print(f"Data: {s.index.min().date()} s/d {LAST.date()} (n={len(s)} hari). TANGGAL DATA TERAKHIR = {LAST.date()}")

CYCLE_WINDOWS = [
    ("2011",    "2011-01-01", "2012-12-31"),
    ("2013-15", "2013-01-01", "2015-12-31"),
    ("2017-19", "2017-01-01", "2019-06-30"),
    ("2021-23", "2021-01-01", "2023-06-30"),
    ("2025-26", "2025-01-01", None),
]

rows = []
for name, a, b in CYCLE_WINDOWS:
    seg = s.loc[a:] if b is None else s.loc[a:b]
    ath_date = seg.idxmax(); ath = seg.loc[ath_date]
    post = seg.loc[ath_date:]
    low_date = post.idxmin(); low = post.loc[low_date]
    rows.append(dict(cycle=name, ath_date=ath_date, ath=ath, low_date=low_date, low=low,
                     days=(low_date - ath_date).days, dd_pct=(low / ath - 1) * 100,
                     ongoing=(b is None)))
cyc = pd.DataFrame(rows)

print("\n" + "-" * 108)
print("(1) ANGKA OBJEKTIF PER CYCLE")
print("-" * 108)
sh = cyc.copy(); sh["ath_date"] = sh["ath_date"].dt.date; sh["low_date"] = sh["low_date"].dt.date
print(sh.to_string(index=False, formatters={"ath": "{:,.0f}".format, "low": "{:,.0f}".format,
                                            "dd_pct": "{:+.1f}".format}))
print("\n  n = 4 bear SELESAI + 1 BERJALAN (2025-26, censored -- low & durasi belum final).")

# ---------------------------------------------------------------------------
# (2) Verifikasi angka video
# ---------------------------------------------------------------------------
print("\n" + "-" * 108)
print("(2) VERIFIKASI ANGKA VIDEO (per 2026-05-14)")
print("-" * 108)
cur = cyc[cyc["cycle"] == "2025-26"].iloc[0]
ath_d, ath_v = cur["ath_date"], cur["ath"]
upto = s.loc[ath_d:VIDEO_DATE]
low_v, low_d = upto.min(), upto.idxmin()
print(f"  ATH cycle berjalan                    : ${ath_v:,.0f} @ {ath_d.date()}")
print(f"  Hari sejak ATH per {VIDEO_DATE.date()}      : {(VIDEO_DATE - ath_d).days} hari")
print(f"  Low terendah ATH -> {VIDEO_DATE.date()}      : ${low_v:,.0f} @ {low_d.date()}")
print(f"  Max drawdown sampai tanggal video     : {(low_v/ath_v-1)*100:+.1f}%")
print()
print(f"  Video menyebut low ~$62.200 -> drawdown terhadap ATH ${ath_v:,.0f} = "
      f"{(62200/ath_v-1)*100:+.1f}%")
print(f"  Video MEMBACA chart di ~-35%. Selisih dengan hitungan langsung: "
      f"{abs(-35 - (62200/ath_v-1)*100):.0f} poin persentase.")
print("  => Angka -35% di chart video CENDERUNG TIDAK cocok dengan drawdown terhadap")
print("     ATH spot. Kemungkinan chart-nya memakai basis lain (mis. ATH weekly/monthly")
print("     close, atau sumbu dibaca keliru dari frame). Angka dari frame = LOW CONFIDENCE;")
print("     yang dipakai untuk kesimpulan adalah hitungan langsung dari btc_price.")
print()
print(f"  Drawdown maksimum cycle berjalan SAMPAI AKHIR DATA ({LAST.date()}): "
      f"{cur['dd_pct']:+.1f}% (low ${cur['low']:,.0f} @ {cur['low_date'].date()}, "
      f"hari ke-{cur['days']})")

# ---------------------------------------------------------------------------
# (3) Kedalaman vs durasi -- DESKRIPTIF
# ---------------------------------------------------------------------------
print("\n" + "-" * 108)
print("(3) KEDALAMAN vs DURASI -- DESKRIPTIF SAJA (n=4, JANGAN diinferensikan)")
print("-" * 108)
done = cyc[~cyc["ongoing"]]
print(f"  Durasi ATH->low (hari) : min {done['days'].min()} | median {done['days'].median():.0f} | "
      f"max {done['days'].max()}")
print(f"  Max drawdown (%)       : min {done['dd_pct'].min():+.1f} | median {done['dd_pct'].median():+.1f} | "
      f"max {done['dd_pct'].max():+.1f}")
print(f"  Durasi 3 bear MODERN (2013-15/2017-19/2021-23): "
      f"{sorted(done[done['cycle']!='2011']['days'].tolist())} hari -> rentang sempit 363-411")
print(f"  Cycle berjalan per akhir data: {cur['days']} hari sejak ATH "
      f"({cur['days']/365*12:.1f} bulan) ke low sementara")
r = np.corrcoef(done["days"], done["dd_pct"])[0, 1]
print(f"  Korelasi durasi vs kedalaman (n=4): r = {r:+.3f}")
print("  => n=4 TERLALU KECIL untuk inferensi apapun; angka r di atas DESKRIPTIF saja.")
print("     Catatan independensi: 4 bear ini berasal dari 4 cycle berbeda tapi satu aset")
print("     yang sama, jadi tidak sepenuhnya independen secara struktur pasar.")

# ---------------------------------------------------------------------------
# (4) Status lantai waktu K4
# ---------------------------------------------------------------------------
print("\n" + "-" * 108)
print("(4) STATUS LANTAI WAKTU K4 (>=9 bulan sejak cycle peak DAN close < RP)")
print("-" * 108)
months_video = (VIDEO_DATE - ath_d).days / 365.25 * 12
months_last = (LAST - ath_d).days / 365.25 * 12
p_last, rp_last = s.loc[LAST], rp.loc[LAST]
p_vid, rp_vid = s.loc[VIDEO_DATE], rp.loc[VIDEO_DATE]

def status(m, p, r_):
    c1 = m >= 9
    c2 = p < r_
    return c1, c2, (c1 and c2)

for label, d, m, p, r_ in [("Tanggal video 2026-05-14", VIDEO_DATE, months_video, p_vid, rp_vid),
                           (f"Akhir data {LAST.date()}", LAST, months_last, p_last, rp_last)]:
    c1, c2, ok = status(m, p, r_)
    print(f"  {label}:")
    print(f"    bulan sejak peak {ath_d.date()} = {m:.1f}  -> syarat >=9 bulan: {'YA' if c1 else 'BELUM'}")
    print(f"    close ${p:,.0f} vs RP ${r_:,.0f}        -> syarat close < RP : {'YA' if c2 else 'TIDAK'}")
    print(f"    LANTAI WAKTU K4 = {'AKTIF' if ok else 'BELUM AKTIF'}")

first9 = ath_d + pd.DateOffset(months=9)
print(f"\n  Tanggal syarat '>=9 bulan' terpenuhi : {first9.date()}")
sub = s.loc[first9:]
sub_rp = rp.loc[first9:]
below = sub[sub < sub_rp.reindex(sub.index)]
if len(below):
    print(f"  Hari pertama (>=9 bulan DAN close < RP): {below.index[0].date()} "
          f"(close ${below.iloc[0]:,.0f} vs RP ${sub_rp.loc[below.index[0]]:,.0f})")
    print(f"  Jumlah hari kedua syarat terpenuhi s/d akhir data: {len(below)}")
else:
    print("  Belum pernah kedua syarat terpenuhi bersamaan sampai akhir data.")
    print(f"  Sejak {first9.date()}: close selalu >= RP. Jarak close/RP terakhir = "
          f"{p_last/rp_last:.2f}x -- harga harus turun {(1-rp_last/p_last)*100:.0f}% lagi")
    print("  untuk memicu jalur lantai waktu.")

cyc.assign(ath_date=cyc["ath_date"].dt.date, low_date=cyc["low_date"].dt.date) \
   .to_csv(rf"{OUTDIR}\events_drawdown_depth_duration.csv", index=False)
print(f"\nCSV -> events_drawdown_depth_duration.csv ({len(cyc)} baris)")
