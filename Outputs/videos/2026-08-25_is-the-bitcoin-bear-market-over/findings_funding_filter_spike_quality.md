# Findings - Funding rendah saat spike = rally berkualitas?

**Tanggal validasi:** 26 Agustus 2026
**Script:** `analyze_funding_filter_spike_quality.py`
**Event table:** `events_funding_filter_spike_quality.csv`
**Data:** `data_master_all_metrics.csv`; `funding_rate` mulai **2020-03-31**, `total_oi` mulai **2020-02-28**, keduanya s/d 2026-07-08

> **FLAG PERMANEN LOW-CONFIDENCE:** funding rate & open interest **baru ada sejak 2020** = sekitar **1,5 siklus**. Uji lintas-cycle penuh **tidak mungkin** dilakukan untuk metrik ini. Semua angka di bawah harus dibaca sebagai indikasi awal, bukan bukti.

---

## Ringkasan sederhana

**Klaim video TIDAK terkonfirmasi - arah datanya justru berlawanan.** Dari **n=39** spike harian >=+7% sejak 2020, kelompok dengan funding **tertinggi** (Q4) justru punya median return 30 hari **+15,2%** dan drawdown paling dangkal (-4,3%), sementara kelompok funding Q2 (rendah-menengah) punya median return 30 hari **-8,6%** dan drawdown -12,4%. Hubungannya juga **tidak monoton** (Q1 bagus, Q2 jelek, Q3 bagus, Q4 bagus) - pola yang biasanya menandakan tidak ada sinyal, cuma noise.

Kombinasi yang persis dihipotesiskan video - **funding rendah + OI rendah = "rally spot berkualitas"** (n=13) - malah **paling buruk**: median return 30 hari **-7,6%**, drawdown 30 hari **-12,5%**. Kelompok "leverage" (funding tinggi + OI tinggi, n=12) justru +11,1% / -3,9%.

**TAPI ini hampir pasti efek regime, bukan bukti bahwa leverage itu bagus:** kelompok funding Q4 berisi **8 dari 10 event dari bull 2020-21** (Nov 2020 - Mar 2021, fase paling eksplosif dalam data). Funding tinggi di sana adalah **gejala** bull yang sedang berjalan, bukan penyebab. Sebaliknya, kelompok funding rendah penuh dengan spike-spike bear rally 2022 dan Mei-Sep 2021.

---

## Definisi event (dikunci sebelum menghitung)

- **Event** = return 1 hari `btc_price` >= **+7%**
- **Cooldown 14 hari** (spike dalam 14 hari setelah event sebelumnya dibuang)
- Periode: **2020-03-31** (hari pertama funding tersedia) s/d 2026-07-15
- **Split at-gate:** `funding_rate` di hari event (kuartil), dan delta `total_oi` 3 hari = `total_oi(t)/total_oi(t-3) - 1` (kuartil). Keduanya tersedia di hari event - tidak ada nilai dari masa depan
- **Outcome (ground truth):** return 30/90 hari + max drawdown 30/90 hari dari close hari event

---

## n & sebaran per fase

**n total = 39 event spike >=+7%**

| Fase | n | Catatan |
|------|---|---------|
| Bull 2020-21 | **20** | **51% dari seluruh sample** |
| Bear 2022 | 9 | |
| Bull 2023-25 | 9 | |
| Bear 2025-26 | **1** | cuma 2026-02-06 |

**Independensi - ini masalah terbesarnya:** lebih dari separuh event berasal dari **satu fase saja** (bull 2020-21). Bear 2025-26 cuma menyumbang 1 event. Jadi apapun hasil split-nya, dia lebih menggambarkan "seperti apa bull 2020-21" daripada "seperti apa spike secara umum".

---

## Split A - kuartil funding rate di hari event (at-gate)

| Kuartil | n | Rentang funding | med ret 30d | med dd 30d | med ret 90d | med dd 90d | Sebaran fase |
|---------|---|-----------------|-------------|------------|-------------|------------|--------------|
| Q1 (terendah) | 10 | -0,3368 .. 0,0073 | +10,4% | -7,8% | +20,0% | -8,9% | 6 bull20-21, 2 bear22, 1 bull23-25, 1 bear25-26 |
| Q2 | 10 | 0,0155 .. 0,0689 | **-8,6%** | -12,4% | **-10,2%** | -18,9% | 4 bear22, 3 bull20-21, 3 bull23-25 |
| Q3 | 9 | 0,0714 .. 0,1045 | +10,3% | -4,6% | +24,6% | -11,5% | 3 bull20-21, 3 bear22, 3 bull23-25 |
| Q4 (tertinggi) | 10 | 0,1144 .. 1,1807 | **+15,2%** | **-4,3%** | +22,1% | **-8,0%** | **8 bull20-21**, 2 bull23-25 |

**Tidak monoton.** Kalau klaim video benar, harusnya Q1 paling bagus dan Q4 paling jelek - yang terjadi justru Q4 paling bagus dan Q2 paling jelek.

## Split B - kuartil delta open interest 3 hari (at-gate)

| Kuartil | n | Rentang dOI 3d | med ret 30d | med dd 30d | med ret 90d | med dd 90d |
|---------|---|----------------|-------------|------------|-------------|------------|
| Q1 (terendah) | 10 | -30,44% .. -5,51% | -4,7% | -9,8% | +12,8% | -9,8% |
| Q2 | 10 | -4,42% .. -0,60% | -6,8% | -11,2% | +12,9% | -14,0% |
| Q3 | 9 | +0,13% .. +2,52% | +7,0% | -4,8% | +18,1% | -14,8% |
| Q4 (tertinggi) | 10 | +4,68% .. +16,73% | **+12,6%** | **-2,5%** | **+26,0%** | **-4,3%** |

Di sini polanya **monoton, tapi ARAHNYA berlawanan dengan klaim video**: makin cepat OI naik saat spike, makin bagus return dan makin dangkal drawdown-nya. Sekali lagi, Q4 didominasi bull 2020-21 (7 dari 10).

## Split C - kombinasi persis hipotesis video

| Kelompok | n | med ret 30d | med dd 30d | med ret 90d | med dd 90d |
|----------|---|-------------|------------|-------------|------------|
| funding RENDAH + OI RENDAH ("berkualitas") | 13 | **-7,6%** | **-12,5%** | +12,3% | -12,5% |
| funding TINGGI + OI TINGGI ("leverage") | 12 | +11,1% | -3,9% | +25,2% | -8,2% |
| campuran | 14 | +13,7% | -4,2% | +19,5% | -9,7% |

Kelompok yang menurut video paling "berkualitas" adalah kelompok dengan **hasil terburuk** di semua horizon pendek. Sebaran fasenya: kelompok "berkualitas" = 5 bull20-21, 4 bear22, 3 bull23-25, 1 bear25-26 (jadi relatif menyebar); kelompok "leverage" = 7 bull20-21, 3 bear22, 2 bull23-25.

## Korelasi rank (Spearman, n=39)

| Outcome | vs funding at-gate | vs delta OI 3d |
|---------|--------------------|----------------|
| ret 30d | +0,20 | +0,28 |
| maxdd 30d | +0,29 | **+0,46** |
| ret 90d | +0,12 | +0,24 |
| maxdd 90d | +0,14 | +0,28 |

Semua korelasi **positif** (funding/OI lebih tinggi -> return lebih baik & drawdown lebih dangkal) dan **lemah sampai sedang**. Tidak ada satupun yang mendukung arah klaim video.

---

## Cek Standar Validasi

1. **Definisi event** - eksplisit (+7% 1 hari), cooldown 14 hari, dikunci sebelum menghitung. OK
2. **n dilaporkan** - n=39, sebaran fase 20/9/9/1. OK
3. **Anti-lookahead** - funding & delta OI diambil di hari event; return/drawdown hanya ground truth. OK
4. **Independensi** - **51% event dari bull 2020-21 saja**; kuartil funding tertinggi 8/10 dari fase itu. Hasil didominasi satu fase - disebut tebal. OK
5. **Data mulai belakangan** - **funding/OI mulai 2020 = ~1,5 siklus. Uji lintas-cycle penuh TIDAK MUNGKIN. Flag permanen low-confidence.** OK
6. **Overfit** - tidak ada threshold yang dicari; pakai kuartil (pembagian netral), dan semua kelompok dilaporkan termasuk yang berlawanan arah. OK

---

## Verdict

**TIDAK TERKONFIRMASI - arah data justru berlawanan, tapi hasilnya tidak bisa dipercaya sebagai bukti balik.** Dari **n=39** spike harian >=+7% (2020-03-31 s/d 2026-07-15; sebaran fase: 20 bull20-21, 9 bear22, 9 bull23-25, 1 bear25-26), kombinasi "funding rendah + OI rendah" yang video sebut rally berkualitas malah punya median return 30 hari **-7,6%** dan drawdown **-12,5%**, sementara kombinasi "leverage" punya +11,1% / -3,9%. Korelasi rank funding vs outcome semuanya **positif lemah** (+0,12 s/d +0,29). Namun **51% sample berasal dari bull 2020-21 saja**, dan kuartil funding tertinggi 8/10-nya dari fase itu - jadi yang terukur kemungkinan besar adalah **efek regime** (funding tinggi = gejala bull sedang jalan), bukan hubungan sebab-akibat. Rekomendasi: **jangan pakai funding sebagai filter kualitas rally** dalam bentuk yang video usulkan. Ini konsisten dengan posisi DF v2 yang sudah ada - funding cuma **pengubah ukuran tranche** di K2, bukan pembuka pintu. **Data 2020+ = ~1,5 siklus - low confidence permanen.**
