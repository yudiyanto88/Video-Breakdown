# Findings — Drawdown depth & durasi ATH → cycle low

**Tanggal validasi:** 5 Agustus 2026
**Script:** [`analyze_drawdown_depth_duration.py`](analyze_drawdown_depth_duration.py)
**Event CSV:** [`events_drawdown_depth_duration.csv`](events_drawdown_depth_duration.csv)
**Data:** `data_master_all_metrics.csv`, **berakhir 2026-07-15**

Video memakai chart "Bitcoin Drawdowns from ATH to Cycle Low" untuk berargumen bahwa bear ini
"masih punya waktu panjang" — cycle berjalan dibacanya di ~−35% pada hari ke-200-an, sementara
cycle lama memanjang 600–800 hari dan −75/−85%.

---

## 1. Angka objektif per cycle (dari `btc_price`)

| Cycle | ATH | Cycle low | Hari ATH→low | Max DD |
|---|---|---|---|---|
| 2011 | $30 @ 2011-06-08 | $2 @ 2011-11-18 | 163 | −93,1% |
| 2013-15 | $1.156 @ 2013-11-29 | $178 @ 2015-01-14 | 411 | −84,6% |
| 2017-19 | $19.538 @ 2017-12-16 | $3.281 @ 2018-12-14 | 363 | −83,2% |
| 2021-23 | $67.525 @ 2021-11-08 | $15.774 @ 2022-11-21 | 378 | −76,6% |
| **2025-26** *(berjalan)* | **$124.715 @ 2025-10-06** | **$58.460 @ 2026-06-30** | **267** | **−53,1%** |

**n = 4 bear selesai + 1 berjalan (censored).**

---

## 2. Verifikasi angka video — **dua angka video tidak cocok**

Per tanggal video **2026-05-14**:
- Hari sejak ATH (2025-10-06): **220 hari**
- Low terendah ATH → tanggal video: **$62.840 @ 2026-02-05**
- **Max drawdown sampai tanggal video: −49,6%**

Video membaca chart-nya di **~−35%** pada low ~$62.200. Dihitung langsung terhadap ATH spot $124.715,
low $62.200 = **−50,1%** — **selisih 15 poin persentase**.

Kemungkinan penyebab: chart komunitas itu memakai basis ATH yang berbeda (weekly/monthly close), atau
sumbu dibaca keliru dari frame. Apapun sebabnya, **angka −35% dari frame berlabel low confidence dan
tidak dipakai** — yang dipakai adalah hitungan langsung dari `btc_price`.

**Konsekuensi untuk argumen video:** kalau drawdown sebenarnya −50% (bukan −35%), jarak ke rata-rata
bear modern (−76,6% s/d −84,6%) jauh lebih kecil daripada yang dia gambarkan. Argumen "masih jauh dari
selesai" jadi **lebih lemah** dari yang dia sampaikan — walaupun arah kesimpulannya (belum sedalam
bear sebelumnya) tetap benar.

Per akhir data (2026-07-15), max drawdown cycle berjalan sudah **−53,1%** (low $58.460 @ 2026-06-30, hari ke-267).

### Klaim "600–800 hari" juga tidak cocok

Video menyebut cycle lama memanjang **600–800 hari**. Data: **163 / 411 / 363 / 378 hari** —
tidak ada satupun yang mendekati 600. Sumbu-x chart komunitas itu memang membentang sampai 800+ hari,
tapi itu **panjang sumbu**, bukan posisi cycle low. Ini contoh langsung kenapa angka yang dibaca dari
frame tidak boleh jadi anchor.

---

## 3. Kedalaman vs durasi — **deskriptif saja (n=4)**

- Durasi ATH→low: min **163** · median **370** · max **411** hari
- Max drawdown: min **−93,1%** · median **−83,9%** · max **−76,6%**
- Tiga bear **modern** (2013-15 / 2017-19 / 2021-23): **363, 378, 411 hari** — rentang sangat sempit
- Korelasi durasi vs kedalaman: **r = +0,812**

**r = +0,812 dari n=4 TIDAK boleh diinferensikan** — satu titik saja (2011: 163 hari, −93,1%) sudah
menentukan hampir seluruh korelasinya, dan 2011 adalah cycle paling awal dengan struktur pasar yang
sangat berbeda. Angka ini dilaporkan sebagai deskripsi, bukan hubungan.

Catatan independensi: keempat bear berasal dari 4 cycle berbeda tapi **satu aset yang sama** — tidak
sepenuhnya independen secara struktur pasar.

Yang **cenderung** bisa dipetik: kalau bear ini mengikuti pola tiga bear modern (363–411 hari),
cycle low-nya akan jatuh sekitar **Oktober–November 2026** — jadi klaim video "masih ada waktu"
punya dasar. Tapi cycle berjalan **jauh lebih dangkal** (−53,1% vs −76,6% terdangkal sebelumnya),
yang justru mendukung tesis "this time is different" yang dia sendiri setengah tolak.

---

## 4. Status lantai waktu K4 — **BELUM AKTIF** (koreksi penting)

Syarat: **≥9 bulan sejak cycle peak DAN close < RP**.

| Tanggal | Bulan sejak peak | ≥9 bulan? | Close vs RP | close < RP? | **Lantai waktu K4** |
|---|---|---|---|---|---|
| 2026-05-14 (video) | 7,2 | Belum | $81.060 vs $54.254 | Tidak | **BELUM AKTIF** |
| 2026-07-15 (akhir data) | 9,3 | **Ya** | $65.098 vs $52.740 | **Tidak** | **BELUM AKTIF** |

Syarat waktu (≥9 bulan) terpenuhi sejak **2026-07-06**. Tapi syarat kedua **tidak pernah** terpenuhi:
sejak tanggal itu close selalu ≥ RP. Rasio close/RP terakhir = **1,23×** — harga masih harus turun
**~19%** lagi (ke bawah ~$52.700) untuk memicu jalur lantai waktu.

> **Koreksi terhadap catatan Stage 2.** Claim-tester menyatakan lantai waktu K4 "sudah aktif sejak
> Juli 2026" (mengutip catatan analisis lain). Data tidak mendukung itu: hanya syarat waktunya yang
> terpenuhi, syarat `close < RP` belum. **Artinya konflik KF1/STOP-1 masih bersifat filosofis, belum
> operasional** — tidak ada DCA lantai waktu yang sedang berjalan untuk ditunda.

---

## Kesimpulan

**n=4 bear selesai + 1 berjalan.** Dua angka yang dibaca video dari chart komunitas tidak cocok dengan
data: drawdown per tanggal video sebenarnya **−49,6%**, bukan ~−35% (selisih 15 pp), dan durasi bear
sebelumnya **163–411 hari**, bukan 600–800. Arah argumennya ("bear ini belum sedalam/selama sebelumnya")
tetap benar, tapi **jaraknya jauh lebih kecil** dari yang dia gambarkan.

Tiga bear modern punya durasi ATH→low yang mengejutkan seragam (**363/378/411 hari**), sedangkan
kedalamannya bervariasi (−76,6% s/d −84,6%); cycle berjalan pada hari ke-267 dengan −53,1%
**cenderung** lebih dangkal dari semuanya. Hubungan kedalaman↔durasi **tidak diinferensikan** (n=4,
r=+0,812 didominasi satu titik 2011).

**Lantai waktu K4 BELUM AKTIF** per akhir data — syarat waktu terpenuhi sejak 2026-07-06, syarat
`close < RP` belum (butuh turun ~19% lagi).
