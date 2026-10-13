# Findings: akumulasi BTC lewat cash-secured put vs DCA spot

**Pertanyaan:** kalau akumulasi BTC dengan jual put bulanan (seperti metode Brian di BLP #43, tapi untuk BTC), apakah hasilnya lebih banyak BTC dibanding DCA biasa?
**Script:** `analyze_btc_cash_secured_put.py`
**Data:** harga penutupan harian BTC dan MVRV dari Coin Metrics community data (`coinmetrics/data`, `csv/btc.csv`), 2016-01-01 sampai 2026-05-23.

## Batasan yang harus dibaca dulu

- **Premi option bukan data asli.** Akses ke Deribit (sumber volatilitas tersirat BTC) diblokir dari sandbox. Premi dihitung dengan Black-Scholes memakai volatilitas 30 hari terakhir. Karena premi asli biasanya sedikit lebih mahal dari volatilitas yang terjadi (pengetahuan umum, belum kuverifikasi dengan data), aku menjalankan pengali 0,8 sampai 1,4.
- Premi dipotong 10% untuk biaya dan spread.
- Kas tidak diberi bunga, untuk semua strategi.
- Siklus 30 hari, settle di harga penutupan hari expiry.
- Sampel: sekitar 3 siklus BTC. Masuk kategori **low-confidence** menurut aturan CLAUDE.md.

## Aturan simulasi

Setiap 30 hari masuk modal $1.000.
- **DCA spot:** langsung beli BTC.
- **Put d% OTM:** semua kas jadi jaminan put 30 hari dengan strike = harga × (1 − d). Kalau terisi, semua kas dibelikan BTC di strike.
- **Hybrid:** sama dengan Put, tapi kalau 3 bulan berturut-turut tidak terisi, kasnya dibelikan spot.
- **MVRV switch:** kalau MVRV di bawah median 4 tahunnya, DCA spot. Kalau di atas, jual put 10% OTM.

## Hasil: jumlah BTC akhir dibanding DCA (pengali IV 1,0)

| Strategi | 2016–2026 | 2016–2018 | 2019–2022 | 2023–2026 |
|---|---|---|---|---|
| Put 0% OTM (ATM) | −10,7% | −10,9% | −15,3% | −4,9% |
| Put 5% OTM | −16,8% | −17,2% | −14,2% | −9,7% |
| Put 10% OTM | −16,1% | −16,2% | −23,7% | −26,3% |
| Put 15% OTM | −32,9% | −33,7% | −19,8% | −31,0% |
| Hybrid 10% | −10,9% | −11,4% | −7,7% | −9,0% |
| MVRV switch | **−7,2%** | −8,5% | −3,1% | −2,8% |

Detail lain (periode penuh): put 10% OTM terisi di 22% siklus, dengan premi rata-rata sekitar 3% per bulan. Drawdown terdalam hampir sama dengan DCA (sekitar −85%), jadi jual put tidak terbukti mengurangi drawdown.

**Sensitivitas pengali IV (periode penuh, Put 10%):** x0,8 −18,6%; x1,0 −16,1%; x1,2 −13,2%; x1,4 −9,9%. Bahkan dengan premi 40% lebih mahal, hasilnya tetap kalah dari DCA.

## Di mana put menang

Hanya di jendela bear murni (dari puncak sampai dasar):

| Jendela | Harga | Put 0% | Put 5% | Put 10% |
|---|---|---|---|---|
| Des 2017 → Des 2018 | 19.250 → 3.185 | +11,1% | +17,8% | +19,3% |
| Nov 2021 → Nov 2022 | 64.756 → 15.778 | +6,3% | +7,8% | +9,5% |
| Okt 2025 → Mei 2026 | 124.824 → 76.620 | +2,3% | +4,3% | +2,2% |
| Jun 2019 → Mar 2020 | 12.863 → 5.628 | +3,5% | −1,5% | −1,9% |

**Nilai premi itu sendiri:** dibanding limit order di strike yang sama (premi nol), premi menambah sekitar 7 sampai 10 poin persen. Klaim "lebih untung dari limit order" terbukti. Klaim "lebih untung dari DCA" tidak.

## Kenapa kalah

BTC naik sangat kuat dalam jangka panjang. Setiap bulan kas menunggu tidak terisi, kas itu kehilangan kenaikan tersebut, dan premi 2 sampai 6% per bulan tidak cukup menutupnya. Strike yang makin jauh membuat premi makin tipis dan kas makin lama menganggur. Kerugian dari loss opportunity jauh lebih besar dari tambahan premi.

## Apa yang bisa membuat temuan ini salah

- Premi asli jauh lebih mahal dari model, misalnya saat panik. Pengali 1,4 sudah diuji dan tetap kalah, tapi lonjakan premi di hari-hari panik tidak tertangkap model bulanan.
- Kas diberi bunga stablecoin 4 sampai 5% per tahun. Efeknya kecil karena porsi kas rata-rata hanya 2 sampai 10%.
- Siklus BTC ke depan jauh lebih datar (naik pelan, banyak bergerak menyamping). Di kondisi itu put bisa menang, sesuai pola di jendela bear di atas.

## Kesimpulan untuk dipakai

1. **Jangan menggantikan DCA dengan jual put.** Di semua periode multi-tahun, DCA menang 3 sampai 33%.
2. **Kalau mau pakai, pakai hanya di fase turun dari puncak.** Di situ put menang 2 sampai 19% atas DCA. Kesulitannya: kamu harus tahu sedang di fase itu. Framework zona bisa jadi penentunya, tapi itu belum diuji di sini.
3. **Di zona murah, beli spot langsung.** MVRV switch (spot saat MVRV rendah, put saat tinggi) adalah varian terbaik, tapi tetap kalah tipis (−3 sampai −9%). Artinya, menahan kas di zona mahal pun sudah mahal.
4. **Strike dekat (0 sampai 5% OTM) lebih baik dari strike jauh** untuk tujuan akumulasi. Strike jauh terasa aman, tapi hasilnya paling buruk karena kas jarang terisi.

---

## Lanjutan: put hanya di fase turun, ditentukan zona (uji PROXY)

**Script:** `analyze_btc_put_zone_proxy.py`

**Batasan:** zona framework asli butuh STH RP dan AVIV, dan dua data itu tidak ada di Coin Metrics community data. Yang bisa dihitung persis hanya Realized Price (RP = harga / MVRV). Jadi zona diganti proxy:
- **A:** harga ≥ RP (kira-kira Z3 ke atas)
- **B:** harga ≥ RP **dan** sudah turun ≥20% dari high 365 hari (fase turun dari puncak)
- **C:** sama dengan B, tapi turun ≥30%

Di luar kondisi itu, semua kas dibelikan spot. Mekanik put sama dengan uji pertama.

**Hasil, jumlah BTC dibanding DCA murni (strike 0% / 5% di bawah harga):**

| Aturan | 2016–2026 | 2016–2018 | 2019–2022 | 2023–2026 | Porsi siklus pakai put |
|---|---|---|---|---|---|
| Put terus | −10,7 / −16,8% | −10,9 / −17,2% | −15,3 / −14,2% | −4,9 / −9,7% | 100% |
| A (≥RP) | −10,1 / −15,5% | −10,9 / −17,2% | −6,0 / −4,9% | −2,8 / −7,7% | 92% |
| B (≥RP, turun 20%) | −2,5 / −2,8% | −2,7 / −2,9% | −2,7 / −2,8% | +0,3 / +0,6% | 42% |
| C (≥RP, turun 30%) | **+0,1 / +0,3%** | +0,4 / +0,7% | −1,9 / −2,6% | −0,2 / −0,7% | 28% |

Sensitivitas premi untuk aturan B (strike 0%, 2016–2026): x0,8 −3,0%; x1,0 −2,5%; x1,2 −1,9%; x1,4 −1,4%.

**Bacaan:**
- Filter zona level saja (A) hampir tidak membantu, karena harga ada di atas RP pada 92% waktu.
- Filter arah (B/C) menghapus hampir seluruh kerugian, tapi **tidak menghasilkan keunggulan**. Hasil terbaik sekitar 0%, sama dengan DCA.
- Kenapa tidak menang seperti di jendela bear murni (+2 sampai +19%)? Filter baru aktif setelah harga sudah turun 20 sampai 30%, jadi bagian awal penurunan terlewat. Filter juga ikut aktif di koreksi tengah bull (misalnya pertengahan 2021), dan di situ harga lalu naik lagi sehingga put kalah.

**Kesimpulan sementara:** dengan penentu fase berbasis RP dan penurunan dari puncak, jual put hanya menyamai DCA. Ia tidak lebih buruk, tapi juga tidak lebih baik, dan menambah kerumitan serta risiko platform. Uji dengan zona asli (STH RP, AVIV Mean/Upper) belum dilakukan dan butuh `data_master_all_metrics.csv` dari Onchain-Dashboard.

---

## Lanjutan: put saat kondisi K4 (uji PROXY)

**Script:** `analyze_btc_put_k4_proxy.py`

**Batasan:** K4 asli butuh Z1 (harga < STH RP < RP) dan empat kondisi (LTH-MVRV, aSOPR/LTH-SOPR, Supply in Profit, Price/CVDD). Data itu tidak ada di sini. Proxy yang dipakai: **MVRV < 1** (harga di bawah Realized Price). Satu episode = rangkaian hari MVRV<1, jeda di bawah 30 hari digabung, minimal 30 hari. Di akhir episode, sisa kas dibelikan spot.

**Hasil, jumlah BTC dibanding DCA di episode yang sama:**

| Episode | Harga (awal → akhir, min) | Put ATM | Put 5% | Put 10% |
|---|---|---|---|---|
| Des 2014 – Okt 2015 | 320 → 275 (min 176) | −2,2% | −1,5% | +3,9% |
| Nov 2018 – Apr 2019 | 4.792 → 4.138 (min 3.185) | +1,6% | −0,7% | −2,1% |
| Jun 2022 – Jan 2023 | 22.316 → 18.870 (min 15.758) | +3,6% | +3,8% | +4,6% |
| (2011–2014, pasar sangat kecil, belum ada options) | | +5 s/d +17% | | |

Premi model saat K4: sekitar 6 sampai 7% per bulan untuk put ATM, karena volatilitas di dasar bear tinggi. Sensitivitas premi (put ATM): 2022 +2,0% sampai +6,9%; 2018 −0,2% sampai +5,3%; 2015 −4,5% sampai +2,5% (pengali 0,8 sampai 1,4).

**Bacaan:**
- Ini satu-satunya kondisi di mana put **cenderung** lebih baik dari DCA, tapi selisihnya kecil (sekitar −2% sampai +5%) dan tidak konsisten antar episode. n = 3 episode yang relevan, jadi low-confidence.
- K4 cocok dengan put karena tiga hal bertemu: premi mahal, harga bergerak datar di dekat dasar, dan **terisi adalah hasil yang memang diinginkan**.
- Risiko terbesar justru di luar model: **risiko pihak ketiga di saat paling buruk.** FTX runtuh November 2022, tepat di tengah episode K4. Jaminan di bursa atau platform options menumpuk risiko pihak ketiga persis saat risiko itu paling tinggi.
- Saat data berakhir (2026-05-23), MVRV = 1,41, jadi proxy K4 belum aktif.

**Cara pakai yang paling masuk akal (ide, belum diuji dengan aturan tranche K4 asli):**
- Tranche spot K4 tetap dibeli spot seperti biasa.
- Tranche yang memang direncanakan menunggu harga lebih rendah diganti dengan put di level tranche itu. Kalau terisi, sama saja dengan rencana. Kalau tidak, dapat premi.
- Kalau keluar dari zona (harga kembali di atas RP/STH RP), sisa kas langsung dibelikan spot.
- Hanya jaminan penuh, tanpa margin, dan dana tersebar, tidak semuanya di satu platform.
