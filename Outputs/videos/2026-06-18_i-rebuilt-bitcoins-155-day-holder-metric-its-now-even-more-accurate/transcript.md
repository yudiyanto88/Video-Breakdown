# I Rebuilt Bitcoin's 155-Day Holder Metric: It's Now Even More Accurate

**Channel:** Bitcoin Magazine Pro (host: Matt Crosby)
**URL:** https://www.youtube.com/watch?v=4QYJCJyoAyQ
**Tanggal video:** 2026-06-18
**Durasi:** 16:24
**Sumber transcript:** native captions (yt-dlp auto-caption, dedup + digabung per ~20 detik)

**Chapter dari deskripsi video:**
- 0:00 – LTH Threshold
- 1:56 – Research Paper
- 3:05 – Filtered Realized
- 4:25 – Dynamic Boundary
- 7:08 – SOPR Quantiles
- 10:54 – Quantile Bands
- 13:21 – Rookies vs Veterans
- 14:11 – Open Source

**Deskripsi video (ringkas):** "For years the industry defined Bitcoin long-term holders with a fixed 155-day threshold. My new research rebuilds it as a dynamic 114-day boundary that's more reactive — and fully open-source." Paper + interactive chart di mattcrosby.pro.

---

## Transcript

**[00:00]** Bitcoin long term holders. It's probably one of the most important thresholds within on chain analysis. If we look to long term holders is defined as an address that has held their Bitcoin for 155 days or more. Now you're going to want to stick around for this one because I did spend too much time to admit working on this.

**[00:22]** But that 155 day threshold, as I said, is incredibly important. But it's based on initial research from 2020. Now this was groundbreaking at the time, so props to Glassnode and their analysts for putting this together. But a lot of people ask me, "What actually is a long term holder?" And it's essentially when the probability of spending a UTXO or transferring that within the next 14 days as outlined in

**[00:46]** this Glassnode document, essentially declines at an exponential rate and and flattens out on this on this graph. But I wondered, Bitcoin's changed a lot in 6 years. I mean, if we look at the active addresses, we can see fewer and fewer people are actually using Bitcoin as a peer-to-peer electronic cash system. We can see through the ETFs and treasury

**[01:08]** companies, more and more people are holding Bitcoin indefinitely as a store of value asset. Now, granted, a few years later Glassnode did actually come back and revisit this in 2024 and fitted this log log almost power law dynamic to spending probability, which is very interesting. We can see it decays at a a very linear rate on this

**[01:32]** log log scale. We can see for every 10x fold in us 10x decrease in spend probability, it likely takes 10 times longer for that to occur. Which again, is very very interesting. But again, I I was thinking a static valuation for the long term holder boundary, at least in my mind, just just didn't really make a lot of sense.

**[01:56]** So I did a lot of research and I've written my first research paper exploring this exact topic. Now, first and foremost, before I delve any deeper, I wanted to replicate the findings from Glassnode. And I'll admit, I was a couple days off based on their initial publication. They have a lot of entity adjustment going on and some peculiarities, let's say, in their methodology, which wasn't made

**[02:20]** entirely publicly available. And along with that, I was able to replicate the power law dynamic and and come to this ultra long-term holder threshold, which is where the spend probability reduces from, at least in my calculations, 3% down to around 0.3%, which takes somewhere around 4 plus years. Now, what is interesting as well is

**[02:43]** during this analysis, as I said, there's some entity adjustment going on, essentially meaning that Glassnode are taking into account a lot of movement between exchanges and certain, you know, all the things that again wasn't made publicly available. But, during this research, it wasn't just long-term holder classification that I was trying to look deeper into and delve into and

**[03:06]** ensure it's the most accurate and actionable we can find. So, if we just look at the standard realized price. Now, this is the cost basis or average accumulation price for all BTC on the network, but not all BTC on the network is really proper transactions, at least in my view. So, we have a few different filters I think we need to apply to this. So, first and foremost, the block coin base,

**[03:30]** which is the block reward that miners receive upon minting a new block, the new inflationary, the new circulating BTC. That's not really a transaction in my eyes. As well as that, we have Bitcoin dust. We can just go to the the Bitcoin GitHub, the underlying core code that we see here. And dust is essentially a UTXO, which would really cost more to send than the transaction

**[03:55]** would actually be worth. It's essentially unspendable. And we also have transactions that are literally unspendable without the ROP return. And there's also inscriptions which have come about in 2023 which really exploded the amount of real nominal amount of transactions. You know, we were inscribing satoshis via ordinals, etc. And again, these kind of non-fungible

**[04:19]** satoshis in my mind aren't really transactions. So, when I filtered all of this out, recreated the original boundary. And again, rather than looking at accumulative all-time, the the thing I really wanted to emphasize and focus on was making metrics derived from this new classification of long-term and short-term holders more

**[04:43]** actionable. So, the way I did that was create the MVRV, the spent output profit ratio, the net unrealized profit and loss, the NUPL. And I wanted the the highs and lows to be in a much closer cluster, a much tighter range with this. So, the way I actually formulated in the end was to work on essentially a 4-year rolling basis, which is this green line, which is what

**[05:05]** I would more strongly consider to be the long-term holder boundary going forward. And and this is recalibrated on a daily basis based on the entire history of all Bitcoin transactions. Now, you might be hearing this and think 114 days. The classification of long-term holder has decreased. Like, I know people that have been holding for years and, you know, they wouldn't even consider

**[05:27]** themselves long-term holders at this point. You have to keep in mind this is at the the point in time in which spending probability exponentially decreases. And because people are holding Bitcoin as a store value asset more than ever, you don't have to hold it as long before your likelihood of spending it again drops off significantly. And what we can in this red line here, which isn't

**[05:49]** classified on a rolling window, this is the spend probability for the 0.9 quantile, the 90th percentile of transactions. So, essentially, at what point in time have 90% of transactions that will ever happen will occur. Because a lot of the Bitcoin that is in these long-term holder addresses might never actually be spent ever again.

**[06:13]** So, if we take a different kind of approach to separate long-term holders and long-term spenders, then again, we can see this almost inverse correlation where when the threshold for long-term holder spending increases, or long-term holding, I should say, this green line, the likelihood of spending that 90th percentile of spending decreases. People are using Bitcoin more. But recently, as this long-term

**[06:37]** holder boundary has dropped to 114 from my research, the likelihood of spending has diminished. So, the 90th percentile of Bitcoin output isn't happening for 213 days, an all-time high. So, at least to me, this is very interesting research. But as I said, as much as I can look into this and and formulate new

**[07:01]** definitions of what a long-term holder is, unless it's more actionable, more accurate, more reactive, and more true to what we're actually seeing, it's not really There's no point in having it. But we can see, if we look at the percentage of long-term holders. So, we can see the long-term holder supply in just raw numbers, currently about 16.57 million Bitcoin. But again, we can look at in percentage terms, and we can see

**[07:24]** this dotted gray line is that static 155-day classification, whereas this green line is this new methodology of dormant supply. And we can see, during the peak of 2021, for example, this dropped significantly, indicating that there was a hell of a lot more Bitcoin being moved from these long-term holders because the definition or the boundary of what a long-term

**[07:46]** holder is increased because their spend probability also increased. Meaning the Q point nine actually decreased. If you read through the paper, I'm not going to say it's light reading, but for on-chain data analysts, you'll probably find it pretty interesting. But right now we can see it's about 85% of Bitcoin is in this long-term holder supply higher than that static boundary. And the spend velocity is also decreased

**[08:09]** substantially. And along with that, because we're not just filtering or defining long-term holders based on spend probability, we're also getting rid of dust, we're getting rid of the unspendable transactions. The realized price on its own has actually been slightly changed. We can see here this solid black realized price line is actually slightly lower than this almost

**[08:32]** filtered true realized price line. Because as I said, if if we're counting the average accumulation price of Bitcoin UTXOs that are literally guaranteed to never be spent again, that's not really giving us a true representation of cost basis. Similarly for for minor rewards, that's coming every 10 minutes. Are they immediately spending it? No, but then are we double counting it

**[08:54]** when they do move it? To me that again just didn't make sense to include. So we can see here I did all of the spend output profit ratio analysis, MVRV, everything. But we can see it's more actionable. So what this is is the long-term holder spent output profit ratio. So on Bitcoin Magazine Pro, we have the standard spend output profit ratio. But again, we can look at this on a dynamic threshold or boundary for

**[09:18]** long-term or short-term holders. Change that into a trailing Z-score and look at the historic quantile. So essentially the percentile. At what point in time has say 10 the top 10% the top 5% of spending days occurred on a rolling basis? And we can see this is absolutely not nailed

**[09:41]** the Bitcoin tops and bottoms pretty much to perfection. I mean that double peak cycle maybe not. And in the most recent cycle wasn't the October peak, but that July peak again at $120,000. But every single bear market bottom even the COVID dip dropped into this lower quantiles absolutely to perfection. And where we are right now is on par with that $60,000 reading. Practically the lowest levels ever.

**[10:07]** Not only is it more interesting and variable, it's more actionable. And as I said, if we're redefining what a long-term holder is, we're also redefining what a short-term holder is. So with a similar bit of analysis, I looked into the short-term holder MVRV and applied the same methodology. And again, it's just looking it's it's looking a lot more accurate. Again, it's not nailing the exact peaks because we see big capitulations at

**[10:31]** different times throughout Bitcoin's history, but we can see these big major spikes to the upside are occurring when we're getting these big upside moves in Bitcoin's price action. And these big downside capitulations again also occurring at major market loads, major turning points for Bitcoin. So clearly, there's a little bit to this. And what we can do is is take it one

**[10:53]** step further, which you know we like to do. And almost take that kind of quantile methodology, but apply it to this new filtered realized price. The kind of gauge based on the ratio between the underlying cost basis for filtered Bitcoin transactions and the price. These kind of quantile bands and upper and a lower threshold of where we'd anticipate Bitcoin to be moving to.

**[11:15]** And again, these aren't repainting historically. This is based on real on-chain fundamental Bitcoin data. And right now we're in the bottom 20th percentile looking at this kind of quantile band methodology as I film this at around $65,000. It's giving an upwards Q5, so the absolute kind of upper threshold.

**[11:38]** But again, these are thresholds that we reached in this cycle. Everyone talks about on-chain data not being able to pick the cycle peaks, but again, if we look at it in a more reactive basis, on a variable length threshold, it's very very actionable. And right now, this is sitting at just around $130,000. Now, of course, this is going to increase as the realized price,

**[12:01]** this new filtered realized price increases. But to me, looking at something like this, which is adapting to the changes in data, and of course, there's limitations. Of course, there's areas where this can be improved upon. This is my first bit of work. It might do terrible. If you don't like it, fair enough. But again, I've I've I wanted to make public all of the formulas that I used, all of the filters, everything, so it can be replicated by anyone in a true

**[12:25]** open-source nature. So, if you do want to read through this paper, if you go to Mack Crosby.pro, which is almost going to be the test site we have for for Bitcoin Magazine Pro and my own certain tweaks and and data analysis, not only can you download the paper, read through it, tell me your thoughts, but you can also actually go and look at these interactive charts, so you can see how these have changed historically.

**[12:48]** Every single one of the metrics included within this paper. So, you can go, test it out, see, "Hmm, how's it looking with this new filtered realized price? What about this new long-term holder realized price? Look at how that's moving. Look at the short-term holder metrics, etc." I think the bear markets are for building, without a doubt. And I'm really taking the opportunity

**[13:11]** throughout this Bitcoin bear market to do as much interesting and insightful and useful for the community work that we can possibly do. And we're not stopping here, because not all long-term holders are created equally. I'm not going to take credit for coming up with this initial idea. There's Johan from the Bitcoin layer and Nim from the Bitcoin research cave already been doing fantastic work on actually separating

**[13:34]** long-term holders into rookies and veterans because you might be a long-term holder if you buy the exact bull market peak and hold until the next cycle. But you're not really an experienced good market timer if you do that. You just held for a long period of time. So, if we can then isolate long-term holders between those buying the tops and buying the bottoms, and maybe follow the genuine smart money, then we're just going to keep improving these metrics further and

**[13:58]** further. But again, I hope you at least found this partly interesting. And I'm hoping, as I said, people can take this and build upon it to continue to make Bitcoin on-chain data analysis better than it ever has been before. The industry has used a static 155-day threshold to define long-term holders for many, many years since March 2020. And as I said, Glassnode did revisit

**[14:22]** that in 2024 and pretty much replicate those findings, but their exact methodology is hidden, so I couldn't do that. And using that 2020 piece almost as my anchoring point and working backwards from there with genuinely true publicly available formulations and data, we were able to replicate those findings, but then adjust it so it's a little bit more actionable. And again, if you read through that paper, actually compares the accuracy of these all-time

**[14:47]** cumulative metrics, these rolling four-year. And I tested this across many, many different data sets. So, again, this was the truest findings that that I could come up with, but this is an open project. If any of you guys can come up with bet- better methodology, man, do I truly welcome it because I I don't want to personally benefit from this. Anyone can use this research paper. Anyone can update their own metrics to

**[15:10]** use this new variable long-term holder boundary to create even better data because then the entire space improves. But ultimately, what we can see is this new methodology is coming up with a threshold of 114 days, which is 27% lower than that static standard. And what we can see is, like I said, metrics built on this boundary seem to become more accurate, more reactive, and a

**[15:32]** little bit more actionable. And they're all pointing towards us being clearly in deep value territory. But as I said, this is my first ever publicly published research piece, so be nice. Don't be too horrible and mean with it. But I want this improved further, and I'm hoping over the next few weeks, next few months, during this bear market, we can set the standard

**[15:55]** for what on-chain data can be, and we can improve the space in general. And as always, thank you all very much for watching. Leave your comments below and social media. Leave your comments down below and on social media. Sorry, it's been a long day trying to get this together. What else? England are going to win the World Cup. Thank you all very much for watching, and I'll see you in the next one.

**[16:21]** &gt;&gt; [music]

---

## Lampiran — Catatan visual dari frame video

Frame diekstrak 60 buah @ 768px. Angka yang dibaca dari frame **low confidence dari resolusi frame** — jangan dipakai sebagai anchor kesimpulan (aturan CLAUDE.md). Angka yang muncul sebagai teks tercetak di paper (bukan tooltip chart) relatif lebih terbaca, tetap ditandai.

### [00:41] Glassnode 2020 — Figure 2 paper asli
Chart "probability of a UTXO to be spent within the next 14 days" vs coin age (0–1750 hari). Peluruhan eksponensial tajam, mendatar setelah ~100–200 hari. Teks paper Glassnode terbaca: UTXO yang melewati ambang lifespan tertentu = **Long Term Holders**, di bawahnya = **Short Term Holders**.

### [01:13] ETF Cumulative Flows (BTC) — Bitcoin Magazine Pro
Stacked area cumulative ETF flows ~2024 s/d Jul 2026, puncak ~1.2M+ BTC sekitar Okt 2025, lalu flat/turun. Overlay harga BTC: puncak ~$120k+ (Okt 2025), drop tajam ~Jan 2026 ke ~$70k, saat frame ini harga ~$65k.

### [01:30] Glassnode 2024 revisit — power law log-log
Dua chart "Average Spending Rate Per Age" (linear + log-log). Di log-log peluruhan hampir garis lurus = power law.

### [02:03] Paper Matt Crosby § 4. Methodology
Terbaca (teks paper): hazard estimation & forward spend probability; `h(a; D, W) = Σ events(a) / Σ at-risk(a)` pooled over W ending at D; 14-day forward spend probability lewat hazard chain. § 4.2 "The dormancy boundary: Long-Term Holders" — boundary = umur pertama di mana smoothed forward spend probability turun di bawah threshold q* dan tetap di bawahnya **14 hari berturut-turut**. Teks menyebut q* = **3.0% per 14 hari**, dikalibrasi supaya konstruksi mereproduksi tanggal kalibrasi Glassnode Maret 2020 (menghasilkan **157 hari** pada tanggal itu). Disebut juga: production lookback 1.460 hari (rolling 4 tahun), smoothing, Weibull/Cox alternatif dibahas di Section 7.

### [02:35] Figure 1 — 14-day forward spend probability by coin age
Dua panel: kiri "LTH threshold (1460-day window)", kanan "ULTH threshold (all-time window)". Dua kurva: **3 Mar 2020** (biru gelap) vs **16 Jun 2026** (merah). Marker terbaca: kiri **114d** (2026) vs **157d** (2020); kanan **1480d** (2020) vs **1686d** (2026). Caption: kurva 2020 berbelok dekat 155 hari; pada 2026 propensity level yang sama teridentifikasi di umur lebih muda karena seluruh kurva turun. Heading di bawahnya: "…re-derivation does not uniquely pin the number" — paper sendiri mengakui angka 114 tidak unik.

### [03:08]–[03:25] Bitcoin: Realized Price (Bitcoin Magazine Pro)
Chart standar realized price (garis oranye/kuning) vs harga BTC, 2013–2026 log scale, lalu di-zoom 2019–2026.

### [03:41] Blockchain.com — Mempool Transaction Count
Dipakai untuk argumen "tidak semua transaksi itu transaksi beneran".

### [04:14] Paper § 6. Results — 6.1 "The boundary is not constant: The distribution has formed a barbell"
Teks terbaca (teks paper, bukan chart): boundary menempati band stabil **~105–120 hari** melintasi dua cycle pertama (2012–2017 dan 2015–16), tidak pernah mendekati 155, termasuk selama cycle 2013 dan 2015-16. Band 150–231 hari terbentuk pada 2018–2022, **puncak 231 hari Desember 2021**, lalu kembali ke **114 hari pada 2026**. Tiga poin penting yang ditulis penulis sendiri: (1) window 1.460 hari tidak bisa terisi penuh untuk ~4 tahun pertama sejak genesis, jadi nilai 2012–2013 jalan di window yang lebih pendek dan diflag window-truncated; band baru established di **window terisi penuh dari 2014 ke depan**; (2) "155-day constant" itu **fitur dari episode 2018–2022 spesifik, bukan level run-on** (p ≤ 0.04, Section 8 item 3); (3) 114 hari sekarang = **kembali ke band pre-episode**, bukan fenomena yang diciptakan ETF. Disebut juga: ultra-dormancy boundary naik **1.480 → 1.686** (arah berlawanan dengan LTH boundary) — bukan artefak estimation window. Expanding spending boundary naik ke **213 hari**, rolling-window spending boundary ke **329 hari**.

### [05:19]–[06:25] Figure 2 — The dormancy boundary across the full history, 2013–2026
Dua garis: **dormancy boundary (fixed-1460d)** hijau, **Q(0.90) spending boundary (expanding)** merah putus-putus, plus garis referensi 155 hari. Anotasi terbaca: "peaked at 231 days (Dec 2021)", "Q(0.90): 213d today", "114d today", marker vertikal "155 day research" (2020) dan "Spot ETFs launch" (2024). Terlihat jelas: boundary hijau ~105–125 hari sepanjang 2013–2018, lompat ke atas 155 pada 2018, puncak ~231 (2021–22), turun tajam sejak 2024 ke 114. Merah bergerak berlawanan arah — turun saat hijau naik, naik tajam sejak 2024.

### [07:14]–[07:47] Figure 3 — Dormant supply share, 2013–2026
Hijau = dormant supply (iso 1460d), abu putus-putus = static 155d reference. Teks paper di atas chart terbaca: dynamic base **85.0661%** vs static-155 **82.7%**. Penulis sendiri menulis: gap itu **sebagian efek definisi + sebagian supply ageing** — "boundary yang lebih rendah secara mekanis mereklasifikasi lebih banyak koin jadi dormant", dan share saat ini pada definisi static-155 "roughly tied with 2024 rather than a clear record". Dia menyimpulkan sendiri: **membaca 114-day boundary sebagai propensity diagnostic dan mempertahankan static-155 split sebagai supply classifier yang konservatif**. Teks lanjutan: LTH velocity turun ke **0.0788% per hari** pada filtered (dynamic) base, deep di lower tail; tapi **liveliness justru naik sejak pertengahan 2024** — velocity didominasi rare ancient movements, liveliness age-weighted.

### [08:03] Bitcoin core `core.h` di GitHub
Dipakai untuk definisi dust.

### [08:53]–[09:09] Figure 5 — Realized price across boundary families, 2013–2026
Lima seri: BTC/USD, Realized price (std), Realized price (flt), LTH-RP (iso 1460d), LTH-RP (static 155). Caption terbaca: **dynamic LTH cost basis $56.290** duduk **13,9% di atas** static-155 cost basis **$49.434** (standard base); filtered base membuang coinbase, dust, unspendable outputs yang terkonsentrasi di supply paling tua.

### [09:25]–[09:58] Figure 7 — LTH-SOPR Trailing-Z quantile, 2013–2026
Sumbu Y 0–1 (quantile of history). Zona hijau di atas ~0.8, zona merah di bawah ~0.1. Caption: **current reading 0.6th percentile, "among the most oversold on record"**. Teks di atas chart (penting): "…gauge steps down — the 2017, 2021, and 2024-25 euphoria prints decline in raw Z — but **I flag this as suggestive only: the trailing-1,460-day normalisation base drifts (Section 7), so the direction is informative while the precise magnitudes are not stationary-comparable**." Anotasi hijau yang digambar Matt di layar menandai: spike atas ~2018 & ~2021, dan spike bawah ~2019, ~2020 (COVID), ~2022, ~2026.

### [10:15]–[10:47] Figure 10 — STH-MVRV Trailing-Z quantile, 2014–2026
Panel atas harga, panel bawah quantile 0–1. Caption: **current reading 29.8th percentile, on the filtered base**. Anotasi hijau Matt menandai banyak titik balik (2019, 2020, 2021, 2022, 2024, 2025, 2026) — lebih banyak sinyal, tapi juga jelas lebih "noisy" (seri bolak-balik antara 0 dan 1 berkali-kali per tahun).

### [11:04]–[11:53] Figure 11 — Price, filtered realized price, rolling 4-yr flt-MVRV quantile bands, 2018–2026
Band q05–q95 / q10–q90 / q20–q80 di sekitar filtered realized price. Legend box angka terbaca (low confidence, resolusi kecil): q95 $131.523 · q90 $124.582 · q80 $118.473 · q20 $65.631 · q10 $50.764 · q05 $47.280 · RP (flt) $58.468 · price $65.610. Caption: "Price sits near the 20th percentile of the trailing four-year regime." Anotasi hijau Matt menandai dua kali harga menyentuh band atas (~awal 2025 dan ~pertengahan 2025). Heading di bawah chart: "**7. Weighting, Lookback, and Out-of-Sample Robustness**" — teks terbaca menyebut sendiri: "the n=3 caveat stated in Section 1 governs throughout: with **three bear lows and three bull tops, a range of 0.036 versus … has limited power to declare a general winner** as these are suggestive single-asset patterns…"

### [12:26] Table 1 — Exclusion tiers
Tiga tier: **Tier 0 (always excluded)** = zero-value outputs & OP_RETURN, provably unspendable, dibuang dari std maupun flt → tidak dipakai di mana pun. **std** = semua spendable UTXO (Tier 0 sudah dibuang), coinbase & dust dipertahankan → dipakai untuk supply, realized price/cap, angka yang comparable secara eksternal. **flt** = std minus coinbase, minus dust by output type (≤546 sats pubkeyhash/pubkey/other; ≤540 scripthash; ≤294 witness_v0_keyhash; ≤330 witness_v0_scripthash & taproot) → dipakai untuk SOPR, spending thresholds, valuation bands, behavioural boundary. Teks di atas tabel menyebut implementasi mereka mereproduksi realized price / cohort supply / realized cap referensi publik **dalam 0.2% lintas tiga market era**.
