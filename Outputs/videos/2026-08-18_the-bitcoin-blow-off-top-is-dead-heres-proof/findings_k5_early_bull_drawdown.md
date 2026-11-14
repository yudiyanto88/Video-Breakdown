# Findings — Drawdown Early-Bull vs Cap LTV 45% di K5

**Video:** On-Chain Mind — "The Bitcoin Blow-Off Top Is Dead (Here's Proof)" (2026-08-18)
**Tanggal validasi:** 2026-08-19
**Script:** `analyze_k5_early_bull_drawdown.py`
**Data pendukung:** `events_k5_early_bull_drawdown.csv`, `events_k5_video_episodes_zone.csv`
**Sumber data:** `data_master_all_metrics.csv` (2010-07-17 s/d **2026-07-15**)

---

## Ringkasan sederhana

Video bilang drawdown 20-45% rutin di 12 bulan pertama bull, dan teks K5 framework menulis
"koreksi 15-30% yang RUTIN". Dua-duanya benar bahwa drawdown besar itu ADA. Tapi pertanyaan
yang menyangkut uang bukan itu — melainkan: drawdown itu terjadi saat loan K5 sedang aktif
atau tidak?

Jawabannya cenderung **tidak**. Dari 51 entry K5 di 4 cycle, hanya **1 (2,0%)** yang
drawdown-nya sampai -25% (angka yang menaikkan LTV dari 45% ke 60%). Dua dari tiga episode
yang disebut video jatuh di luar wilayah deploy loan K5: episode 2015 di Z1b (K4 wrap-up,
spot only), episode 2019 di Z5 (framework justru menyuruh melunasi loan di situ). Hanya
episode 2023 yang murni K5, dan besarnya persis -20,0% — menyentuh cut-loss sadar, tidak
menyentuh cap 45%.

---

## Definisi event (dikunci di muka)

- **AVIV Upper** = `price_at_aviv_mean + 0.5*(price_at_aviv_plus_1_sigma - price_at_aviv_mean)`
  (+0,5 SD, mengikuti pola `research/analyze_k3_stage_comparison.py` — formula tidak dihitung ulang)
- **Jendela K5**: START = hari pertama STH RP close di atas RP setelah cycle bottom.
  END = hari ke-3 dari 3 hari berturut `btc_price >= AVIV Upper`
- **Entry K5** = hari pertama `btc_price <= 95% x trailing high 30 hari`; trailing high memakai
  rolling max **hanya data s/d hari itu** (anti-lookahead)
- **Merge:** entry berjarak <14 hari dari entry sebelumnya digabung
- **Outcome:** max drawdown dari harga entry ke (a) akhir jendela K5, (b) entry +180 hari
- Klasifikasi zona memakai Zone Structure v2 (Decision Framework v2 §1) apa adanya

## Jendela K5 per cycle (hasil, bukan asumsi)

| Cycle | Bottom | K5 start | K5 end | Durasi | Harga start -> end |
|---|---|---|---|---|---|
| C0 | 2011-11-18 | 2012-04-19 | 2013-04-09 | 355 hari | $5,14 -> $230,87 |
| C1 | 2015-01-14 | 2015-11-03 | 2017-05-03 | 547 hari | $404,61 -> $1.531,44 |
| C2 | 2018-12-14 | 2019-05-07 | 2019-07-10 | **64 hari** | $5.778,25 -> $12.125,03 |
| C3 | 2022-11-21 | 2023-03-01 | 2024-02-29 | 365 hari | $23.649,48 -> $61.192,56 |

Jendela K5 **tidak sama dengan "12 bulan pertama sejak bottom"**. Di C1, K5 baru mulai ~9,6
bulan setelah bottom. Di C2, K5 hanya hidup 64 hari. Video mengukur "12 bulan sejak bottom" —
potongan waktu yang sebagian besar milik K4/ZC, bukan K5.

---

## Hipotesis & verdict

### H1 — "Drawdown 20-45% rutin di 12 bulan pertama bull" (klaim video)
**Verdict: SEBAGIAN BENAR, tapi salah alamat.** Drawdown terdalam (peak-to-trough) 12 bulan
sejak bottom: C0 -41,6%, C1 -32,4%, C2 -45,0%, C3 -20,0% — jadi 4/4 cycle memang mengalaminya.
Tapi zona di titik trough: ZD (2012-08-19), **Z1** (2015-08-24), ZD (2019-11-24), ZD
(2023-09-11). Tidak satupun trough terjadi di Z3/Z2 — wilayah inti K5.

### H2 — Drawdown >=30% terjadi DI DALAM jendela K5
**Verdict: JARANG, dan hanya di cycle lama.** Peak-to-trough di dalam jendela K5: C0 -41,6%,
C1 -32,5%, C2 -17,9%, C3 -20,0%. Dua dari empat cycle memang >30% di dalam jendela, tapi ini
angka peak-to-trough jendela, bukan drawdown yang dialami posisi K5 — aturan K5 menyuruh masuk
SETELAH pullback >=5%, yang otomatis memotong bagian awal penurunan.

### H3 — Cap LTV 45% cukup menahan drawdown early-bull
**Verdict: YA, cenderung cukup — 1 dari 51 entry (2,0%) menembusnya.**

**Koreksi aritmetika:** LTV baru = cap / (1 - drawdown). LTV 60% tercapai di cap 52% -> -13,3%;
cap 48% -> -20,0%; cap 45% -> -25,0%. (Ambang -33% yang sempat dipakai di brief validasi keliru;
teks framework di K2 sendiri sudah benar: "-20% untuk cap 48%, -13% untuk cap 52%".)

**n = 51 entry. Sebaran: C0 = 11, C1 = 22, C2 = 3, C3 = 15.**

| Ambang drawdown | Arti | Horizon akhir jendela K5 | Horizon +180 hari |
|---|---|---|---|
| >=13,3% | LTV-60 dari cap 52% (lama) | **14/51 = 27,5%** | 16/51 = 31,4% |
| >=20% | cut-loss sadar (= LTV-60 dari cap 48%) | 3/51 = 5,9% | 4/51 = 7,8% |
| >=25% | **LTV-60 dari cap 45%** | **1/51 = 2,0%** | 2/51 = 3,9% |
| >=33% | ambang ekstra | 0/51 = 0,0% | 1/51 = 2,0% |

Sebaran per cycle (horizon akhir jendela K5): C0 1 entry >=20% (terburuk -32,4%), C1 2 entry
>=20% (terburuk -22,8%), C2 0 (terburuk -6,1%), C3 0 (terburuk -15,8%).

**Ini mereplikasi klaim framework sendiri secara independen.** Framework (findings Temuan 2 +
Addendum A) menyebut cap 52% kena wajib-jual LTV-60 di 23% deployment, cap 45% di 1,4%. Hasil
kami dengan definisi event berbeda: **27,5% vs 2,0%** — arah & besaran sama, cap 45%
menurunkan risiko wajib-jual sekitar 13-16x.

Disaring lagi ke zona inti K5 saja (Z2/Z3/ZD, membuang 6 entry di Z4): **n = 45, hanya 1
(2,2%) yang >=25%**, terburuk -32,4% (C0, 2012-08-17). Sebaran C0=10, C1=18, C2=2, C3=15.

### H4 — Klasifikasi kunci: tiga episode video jatuh di zona mana?
**Verdict: 2 dari 3 di luar wilayah deploy loan K5.**

| Episode video | Tgl awal | Harga | Zona | K aktif | Di dalam jendela K5? | Drawdown aktual |
|---|---|---|---|---|---|---|
| 2015 (video -34%) | 2015-03-11 | $296,79 | **Z1b** | K4 wrap-up (**spot only**) | **TIDAK** | -25,4% ke 2015-08-18 |
| 2019 (video -45%) | 2019-06-26 | $12.830,41 | **Z5** | K1 (**lunasi loan -> 0**) | Ya (C2), hari ke-50 dari 64 | -42,0% ke 2019-12-31 |
| 2023 (video -20%) | 2023-07-13 | $31.481,41 | **Z3** | **K5** | Ya (C3) | -20,0% ke 2023-09-11 |

- **2015**: struktur masih terbalik (STH RP < RP), K5 belum lahir (baru 2015-11-03). Lantai K4
  = spot only, tidak pernah menyentuh LTV. -34% versi video tidak bisa melukai loan.
- **2019**: dimulai saat harga sudah **Z5** — zona di mana K1 memerintahkan pelunasan loan.
  Jendela K5 masih nominal terbuka (syarat tutup butuh 3 hari berturut >= AVIV Upper), tapi
  zona hariannya sudah Z5/Z4.
- **2023**: satu-satunya K5 murni, besarnya persis -20,0% — menyentuh cut-loss sadar, TIDAK
  menyentuh LTV-60 dari cap 45% (butuh -25%).

---

## Detail penting & catatan rigor

1. **n & sebaran:** 51 entry; C2 hanya menyumbang 3 (jendela K5-nya 64 hari), C1 menyumbang 22
   (43%). Ketiga kejadian >=20% berasal dari C0+C1 saja — hasil **didominasi cycle lama**.
2. **Anti-lookahead:** trailing high 30 hari hanya data s/d hari entry; drawdown adalah outcome,
   bukan input keputusan.
3. **Independensi:** entry dalam satu cycle berkorelasi; merge 14 hari mengurangi tapi tidak
   menghapusnya. Baca 2,0% sebagai "jarang", bukan probabilitas presisi.
4. **Lubang definisi K5 (temuan sampingan):** syarat tutup "3 hari berturut >= AVIV Upper" bisa
   membuat K5 tetap terbuka saat zona harian sudah Z4/Z5. 6 dari 51 entry terjadi di Z4 — salah
   satunya 2019-06-27, satu-satunya entry dengan drawdown -38,7% di horizon 180 hari. Kalau
   jendela K5 juga ditutup begitu harga masuk Z4, entry itu hilang dan ambang >=33% jadi 0/50
   di kedua horizon.
5. **Teks "koreksi 15-30% yang RUTIN":** dengan C0 ikut dihitung, peak-to-trough di dalam
   jendela K5 mencapai -41,6% (C0) dan -32,5% (C1) — di atas band yang tertulis. Band cenderung
   perlu diperlebar ke ~15-40%, TANPA mengubah kesimpulan cap 45%.
6. **Data lag:** master terakhir 2026-07-15; tidak mempengaruhi hasil historis (jendela K5
   terakhir tutup 2024-02-29).

## Verdict akhir

**Klaim video benar sebagai deskripsi pengalaman early bull, tapi tidak menyentuh cap LTV 45%.**
Dari **n = 51 entry K5** (C0=11, C1=22, C2=3, C3=15), hanya **1 (2,0%)** yang drawdown-nya
>=25%. Dua dari tiga episode video (2015, 2019) terjadi di luar wilayah deploy loan K5 (Z1b
dan Z5); yang ketiga (2023) berhenti persis di -20,0%. Cap 45% cenderung tahan; mengembalikan
cap ke 52% akan menaikkan frekuensi wajib-jual dari 2,0% ke 27,5% (~13x lebih sering).

**Usulan (bukan penerapan):** (a) perlebar teks rasional K5 dari "koreksi 15-30%" jadi
"~15-40%, yang terdalam cenderung jatuh di luar jendela K5"; (b) pertimbangkan menutup jendela
K5 juga saat zona harian masuk Z4, bukan hanya lewat konfirmasi 3 hari AVIV Upper.
