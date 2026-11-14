# Transcript — EVERYONE Expects Bitcoin To Break This Line, It's Held 99% Of The Time

**Channel:** Bitcoin Magazine Pro
**URL:** https://youtu.be/UVFDWEXV5eM
**Tanggal video:** 2026-07-09
**Durasi:** 11:03
**Sumber transcript:** YouTube captions

---

## Catatan visual (dari frame video)

- Chart utama: **Bitcoin: Realized Price** (platform Bitcoin Magazine Pro, TradingView-style), garis hitam = harga BTC, garis oranye = Realized Price. Range historis 2011-2026 (multi-cycle), harga BTC saat rekaman terlihat di sekitar $105-110K (log/linear chart candlestick oranye di frame lain).
- Chart kedua: **candlestick MVRV (bukan Z-score)**, dengan dua garis anotasi manual (merah di atas menghubungkan puncak-puncak MVRV, hijau di bawah menghubungkan lembah-lembah MVRV) membentuk pola wedge/converging channel — highs makin rendah, lows makin tinggi tiap cycle. Lingkaran hijau menandai titik-titik puncak & lembah yang dipakai sebagai anchor line of best fit.
- Spreadsheet Excel: kolom fit `MVRV = EXP(a + b × date)`, dengan sel terbaca (low confidence, resolusi kecil):
  - Peak slope (b): 0.000, Peak intercept (a): 9.624
  - Trough slope (b): 0.000, Trough intercept (a): -7.431
  - Latest date: 7/7/26, Latest MVRV: 1.194
  - Implied peak: 2.569, Implied trough: 1.005
  - Peak Price: $136,273.33 (tertulis "136,273.33" di satu frame), Trough Price: $53,302.51 / $53,039.00 (dua frame beda menunjukkan angka sedikit berbeda — kemungkinan software live-update saat rekaman), Realized Price: $53,039.00 / $53,030.09
  - Days Below (trough line historis): 17 hari, Below %: 0.293% (dibulatkan pembicara jadi "0.29%")
  - Days Above (trough line historis, artinya hari² MVRV di atas garis trough): 9 hari, Below %: 0.155% (dibulatkan pembicara jadi "0.15%")
- Chart ketiga: **Bitcoin: Long Term Holder MVRV**, garis hitam = LTH MVRV, garis oranye = LTH Realized Price, band merah muda di bawah chart. Range default Apr 2025 - Jun 2026 (frame ini menampilkan window pendek, bukan multi-cycle).

---

## Transcript

[00:02] the Bitcoin realized price. All the cost basis, average accumulation price of all
[00:05] Bitcoin on the network. Clearly, just
[00:08] buy when price goes to or beneath this
[00:11] line, and you're going to nail every
[00:13] single Bitcoin bear market. I mean, if
[00:14] we take the Z-score of this, standardize
[00:17] the ratio between the underlying price
[00:19] and that realized price, again, just
[00:21] just buy in the green zone. It's it's
[00:23] simple. It's it's obvious.
[00:26] But, what if it wasn't? What if there's
[00:28] a chance, in fact, a fairly good chance
[00:30] we actually don't reach it this cycle?
[00:33] Cuz one thing I noticed, rather than
[00:34] just looking at the MVRV Z-score,
[00:38] just the MVRV, the raw ratio between
[00:40] this cost basis, its average
[00:42] accumulation price of Bitcoin,
[00:44] and the underlying price, you can notice
[00:46] that a pretty clear and obvious pattern.
[00:48] I'll just hide the price
[00:50] so we can just focus on the data.
[00:53] We can clearly see we're contracting
[00:56] both in upside moves, the deviation
[00:58] above this cost basis,
[01:01] and to the downside.
[01:03] We're almost forming this wedge pattern
[01:05] in which the highs aren't quite as high,
[01:07] but the lows aren't quite as low. So, I
[01:10] wondered if there was a way that we
[01:11] could kind of mathematically
[01:13] look at this rather than roughly draw
[01:15] drawing lines on the chart. So, first
[01:17] and foremost, I thought it'd be best to
[01:18] look at this on a logarithmic scale. So,
[01:20] if you if you do have a Bitcoin Magazine
[01:22] Pro site subscription, you gain access
[01:24] to loads of TradingView indicators,
[01:25] including the MVRV Z-score, which I've
[01:28] just removed the Z-score. This is just
[01:29] the MVRV.
[01:32] And again, if we just go to the weekly
[01:33] time frame, so it's a bit clearer. On a
[01:35] on a linear scale, again, you can kind
[01:38] of see this relationship, but it's not
[01:40] the clearest. If you go to a log scale,
[01:43] however, though,
[01:45] it seems to be that there's some
[01:47] undeniable
[01:49] trend in this data that seems to be
[01:53] somewhat consistent.
[01:55] So, what I did is took all of this data,
[01:57] the raw data again, CSV download from
[01:59] the site. If you got a site
[02:00] subscription, you can do this analysis
[02:02] yourself to replicate my finding. If we
[02:05] go over to Excel here,
[02:07] if we find statistically the line of
[02:09] best fit from all of the peaks and all
[02:12] of the troughs
[02:13] of all of Bitcoin's history, we can see
[02:17] it is pretty remarkably accurate. I
[02:19] mean, all the peaks, the double top in
[02:21] 2013 wasn't quite there. The most recent
[02:23] almost triple price section top didn't
[02:26] quite make it.
[02:27] But the other two peaks, including the
[02:29] initial 2011 team bull market, wow, was
[02:32] it it absolutely nailed it.
[02:35] Following that, the Bitcoin bear
[02:36] markets, again, the two middle ones,
[02:38] 2015, 2018, not quite there, but within
[02:41] about 10%.
[02:43] But the other two bear market lows,
[02:45] pretty much spot-on.
[02:46] But what is incredibly interesting
[02:49] is if we just zoom in to where we are,
[02:51] this green trend line, the statistical
[02:54] line of best fit through these Bitcoin
[02:56] NVRV troughs,
[02:59] it's actually just crossed above
[03:02] one.
[03:04] Now, what does this mean? Well, when
[03:05] they're at parity, when Bitcoin's price
[03:07] reaches
[03:08] the realized price or the realized cap,
[03:10] you'll be looking at the market cap in
[03:11] terms of this data,
[03:13] that would be parity, one to one.
[03:16] The fact that this is above one
[03:17] indicates that this trend line is
[03:19] pointing towards the fact Bitcoin is not
[03:21] going to reach parity. Therefore, it's
[03:22] not going to dip beneath that realized
[03:25] price. Now, what I can actually do is
[03:26] just move this to the side. Again, we
[03:28] have all of the data points, the anchors
[03:30] of the data, the underlying slopes,
[03:32] formulas, everything. So, you can
[03:34] replicate your findings yourself.
[03:36] But if we just zoom in,
[03:38] we can see the latest MVRV score, 1.194.
[03:43] Just this data point here.
[03:46] The implied bottom,
[03:48] currently with today's data, keeping in
[03:50] mind this trend line is trending to the
[03:52] upside is 1.005
[03:59] above one. And this is very recent. If we actually just scroll all the way to
[04:00] the bottom of the data, we can see it
[04:02] was only a few days ago this was
[04:03] actually
[04:05] beneath one indicating that Bitcoin,
[04:07] according to this line of best fit
[04:09] through the NVAV ratio troughs, was
[04:11] likely going to dip beneath it.
[04:14] But the longer we're chopping and
[04:15] consolidating, the more people are
[04:16] accumulating Bitcoin at these levels.
[04:20] We're seeing that realized price trend
[04:22] line indicate that we're not going to
[04:24] dip beneath that level.
[04:26] And what we can do is almost work
[04:27] backwards. So, we can see at parity, the
[04:29] realized price being 53,039
[04:32] as I film this, Bitcoin to reach a one
[04:35] on the NVAV ratio would reach exactly
[04:36] this level. But the fact that this is
[04:38] above one indicates that this trend line
[04:40] is at 53,300.
[04:43] Now, I know $300 isn't a a significant
[04:46] amount of discrepancy between these two
[04:48] valuations, but again, this is trending
[04:50] to the upside. Now, I know what you're
[04:52] thinking.
[04:54] Yeah, but in two previous cycles, if we
[04:57] look at the, you know, bear market way
[04:59] back here in 2011, and if we look even
[05:02] to the 2022, our most recent comparable
[05:04] bear market, we actually dipped beneath
[05:05] this trend line.
[05:07] And you are right, we could definitely
[05:08] dip beneath it again.
[05:10] But throughout Bitcoin's
[05:12] entire history,
[05:15] there's been 17 days beneath this trend
[05:18] line. That is a 0.29%
[05:21] chance
[05:23] that we dip beneath it.
[05:24] Days above, cuz again, we can just work
[05:26] backwards again.
[05:28] How many days have we spent above this
[05:29] trend line? Only nine days. 0.15%
[05:33] of all of Bitcoin's history. Now, if we
[05:35] were to reach that upper trend line
[05:36] currently, that's pointing towards
[05:38] 136,000
[05:41] dollars.
[05:42] One thing you have to take into
[05:43] consideration is the realized price is
[05:46] changing
[05:47] every single day. Even if it's pointing
[05:48] towards the fact we won't dip beneath it
[05:50] and we may just be a few percent above
[05:52] it. Currently, this trend line this this
[05:54] realized price is trending down. So,
[05:57] even if Bitcoin remains stagnant right
[05:59] now,
[06:01] the realized price is trending down. So,
[06:02] that MVRV's goal is actually shifting to
[06:04] the upside. So, there is a chance we're
[06:06] going to the mid $50,000 region,
[06:08] potentially even to just a few hundred
[06:09] dollars above this. There's a chance we
[06:11] even spend a couple days beneath this.
[06:14] But, looking at the trend line, looking
[06:17] at the data,
[06:19] man, it it
[06:20] I think waiting for a a a $30,000
[06:23] Bitcoin, a $40,000 Bitcoin is incredibly
[06:26] hopeful. Now, I know what you're
[06:27] thinking.
[06:29] We're going to go beneath that. We're
[06:30] going to go to the long-term holder
[06:32] realized price.
[06:34] Is this applicable to long-term holder
[06:36] realized price?
[06:37] The answer is
[06:40] maybe.
[06:41] We can also see if we zoom in looking at
[06:42] the realized price, this is just looking
[06:44] at the cost basis or average
[06:45] accumulation price of Bitcoins most
[06:47] long-term experienced holders. This is
[06:49] on track to cross $50,000 in just a week
[06:53] or two's time. So, maybe those colliding
[06:56] will provide some confluence if we were
[06:57] to have some downside price action. But
[06:59] again, if you look throughout all of
[07:01] Bitcoin's history, we can see we dipped
[07:02] beneath this long-term holder realized
[07:04] price. Are you telling me we're not
[07:05] going to get to that level?
[07:07] Well, even though it's not as clear and
[07:08] obvious, we can definitely still see a
[07:11] trend in this data.
[07:13] Now, granted, it's not quite as clean.
[07:16] If I connect the peaks on the long-term
[07:17] holder MVRV, it's very hard to find a
[07:20] way that they actually predict with a
[07:22] great deal of accuracy. We can see just
[07:24] looking at 2017, the previous bull
[07:25] market, it wasn't a million miles away,
[07:28] but it wasn't quite there.
[07:31] Now, you do have to take into
[07:32] consideration with the long-term holder
[07:34] RV, it's taking into account Bitcoin
[07:36] from well over a decade ago.
[07:38] Bitcoin that very well may be lost and
[07:41] and never
[07:42] So,
[07:43] there is a little bit of trend here,
[07:47] but not so much. But, it makes sense
[07:50] that Bitcoin every single cycle from
[07:52] here and indefinitely is going to cross
[07:55] beneath this realized price. Because
[07:57] once you take into consideration
[07:59] the millions of Bitcoin that is never
[08:01] going to move moved again. The millions
[08:03] of Bitcoin that is lost or that was
[08:05] accumulated at just a few dollars,
[08:08] it makes sense that every single dip
[08:10] beneath it is less severe.
[08:13] And it makes sense that an asset that
[08:15] has gone from a few pennies to well over
[08:17] a hundred thousand dollars
[08:20] is likely going to see contracting
[08:22] volatility.
[08:24] And those early adopters are going to be
[08:25] rewarded. So, do I think the Bitcoin
[08:27] price is going to dip beneath the
[08:29] realized price?
[08:31] Well, as I said, we we've done it
[08:33] before, but we're talking about a 99.7
[08:38] plus percent chance
[08:42] that we don't I mean, it's it's not
[08:43] exactly like that, but a 99.7% chance
[08:46] throughout any day within Bitcoin's
[08:48] history that we were above this trend
[08:50] line.
[08:52] To me, those those odds just tell me
[08:54] that
[08:56] waiting for a price significantly
[08:58] beneath $50,000 is risky to say the very
[09:02] least.
[09:04] But then again, if we look to an upside
[09:05] target looking at the realized price in
[09:07] the previous few cycles, we can see that
[09:09] this has gone from, say, $300 as Bitcoin
[09:12] started bull market to over $5,000. In
[09:16] the previous market from around 5 and
[09:19] 1/2 thousand to when we peaked at
[09:21] $23,000.
[09:23] If we look to the realized price in the
[09:24] most recent cycle, started $20,000 and
[09:26] now up to about $55,000.
[09:29] So, potentially a a 4x in the pre-
[09:32] previous cycle and a 3x. If we even saw
[09:34] a 2x from these current prices, so just
[09:36] say a $53,000
[09:39] $106,000, sorry. It's been a long few
[09:42] days. If we change the realized price to
[09:44] $106,000
[09:45] and this trend line holds true, then a
[09:47] peak Bitcoin price could happen in the
[09:49] next cycle of $272,000.
[09:54] Now, keep in mind that trend line is also coming to the downside. So, if we
[09:56] saw an implied peak of, say, 2.2, then
[09:59] this would move down to $233,000.
[10:01] But, nevertheless, I think it's an
[10:02] interesting date point and something to
[10:05] take into consideration that just
[10:06] because Bitcoin always goes beneath the
[10:09] realized price. Yes, but to a
[10:11] significantly lesser degree every single
[10:14] cycle as Bitcoin is maturing, as more
[10:16] people are accumulating at considerably
[10:18] higher prices for an asset that's gone
[10:20] from a few million dollars to multiple
[10:21] trillions of dollars in size. It It just
[10:24] makes sense that we're not going to
[10:26] continuously dip beneath this by 5, 10,
[10:28] 15, 20 plus percent.
[10:31] In fact,
[10:32] the data is pointing towards us
[10:34] potentially
[10:36] not even crossing beneath it at all this
[10:38] cycle. But, as always, I'm sure many of
[10:41] you will disagree with me. Tell me I'm
[10:43] wrong. Tell me that you're going to go
[10:44] all in at the exact bottom at $37,400
[10:48] on October the 6th. And sincerely, I
[10:50] hope you do. But, if you did like this
[10:51] content, let me know in the comments
[10:53] below and on social media. If you didn't
[10:54] like this content, then again, you can
[10:57] laugh at me in a few months time when
[10:58] you're inevitably right and the data is
[11:00] inevitably wrong. Thank you all very
[11:02] much for watching and I'll see you in
[11:03] the next one.
