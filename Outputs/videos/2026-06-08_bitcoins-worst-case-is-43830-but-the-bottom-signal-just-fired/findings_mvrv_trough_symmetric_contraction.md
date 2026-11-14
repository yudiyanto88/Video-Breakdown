# Findings — MVRV Trough Symmetric Contraction

**Tanggal validasi:** 2026-07-30
**Script:** `analyze_mvrv_trough_symmetric_contraction.py`
**Event CSV:** `events_mvrv_trough_symmetric_contraction.csv`

## Klaim yang diuji

Presenter menarik garis tren manual melalui titik trough MVRV historis (2012, 2015,
2018-19, 2022-23), lalu berargumen tren contracting ini memproyeksikan cycle sekarang
mungkin **tidak akan dip di bawah MVRV=1 (Realized Price) sama sekali** — akan jadi
pertama kalinya dalam sejarah kalau benar.

**n = 4 titik trough** — sample sangat kecil untuk fitting regresi apapun.

## Trough MVRV per cycle (reproduksi)

| Cycle | Tanggal | MVRV trough |
|---|---|---|
| 2012 | 2011-10-19 | 0.4013 |
| 2015 | 2015-01-14 | 0.5677 |
| 2018-19 | 2018-12-14 | 0.7025 |
| 2022-23 | 2022-11-09 | 0.7604 |

Trend contraction memang nyata dan konsisten arah (0.40 → 0.57 → 0.70 → 0.76, makin dangkal tiap cycle).

## Regresi linear (n=4), ekstrapolasi ke cycle ke-5

| Metode anchor | Proyeksi trough cycle sekarang | >1.0? |
|---|---|---|
| Titik tunggal (nilai low harian) | 0.911 | Tidak |
| Window ±30 hari (rata-rata sekitar tanggal low) | 0.981 | Tidak (tapi sangat dekat) |
| Exclude 2012 (era thin-liquidity, n=3) | 0.870 | Tidak |

**Ketiga varian sensitivity konsisten menolak** klaim presenter bahwa ekstrapolasi tren memprediksi harga tidak akan dip di bawah RP sama sekali. Yang diprediksi regresi adalah dip yang **lebih dangkal** (sekitar 2-13% di bawah RP tergantung metode), bukan tanpa dip sama sekali.

## Preseden historis

Dari 4 bear cycle yang diuji: **4/4 (100%) pernah dip di bawah MVRV=1**, dengan durasi 132-311 hari berturut-turut di bawah threshold per cycle. Tidak ada satupun preseden "tidak dip" di data yang tersedia.

## Verdict

**[VALIDASI — 2026-07-30, CLOSED]** Regresi linear atas 4 titik trough MVRV historis (0.40→0.57→0.70→0.76) mengekstrapolasi ke cycle sekarang menghasilkan **0.87–0.98 tergantung metode anchor** — ketiganya TETAP di bawah 1.0, TIDAK memprediksi "tidak dip sama sekali" seperti diklaim presenter. Trend contraction-nya sendiri nyata dan konsisten (didukung n=4, low-confidence sample), tapi kesimpulan presenter (harga tidak akan menyentuh RP di cycle ini) **tidak didukung oleh ekstrapolasi matematis dari datanya sendiri** — yang paling mungkin terjadi menurut tren ini adalah dip tipis di bawah RP (2-13%), bukan zero-dip. Preseden historis 4/4 cycle selalu dip <1.0 memperkuat skeptisisme terhadap klaim "pertama kali dalam sejarah" ini.
