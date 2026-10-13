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
