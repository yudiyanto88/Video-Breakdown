# The FREE & SIMPLE Strategy That Beats Bitcoin (It Just Flashed Again)

**Channel:** Bitcoin Magazine Pro (pembicara: Matt Crosby, Director of Research & Analytics)
**URL:** https://youtu.be/2XLmK_TDOgc
**Tanggal video:** 5 Agustus 2026
**Durasi:** 12:08
**Sumber transkrip:** native captions YouTube (auto-generated), di-dedupe dari rolling caption
**Tanggal diambil:** 6 Agustus 2026

---

## Catatan visual penting (dibaca dari frame video)

Transkrip di bawah tidak memuat angka yang hanya tampil di layar. Berikut isi slide
kunci, dibaca dari frame resolusi tinggi (1600px) — akurasi baik, tapi tetap
perlakukan sebagai bacaan-dari-frame.

### [02:05] Chart MVRV Quantile Bands (bitcoinmagazinepro.com, gratis)
- Panel atas: BTC Price (hitam) + Realized Price (oranye) + band 5th-95th percentile
  (gradien hijau di bawah = murah, merah di atas = mahal)
- Panel bawah: "Percentile of cycle-adjusted MVRV (0 = cheapest day in history,
  100 = most expensive)"
- **Current Percentile: 8%** (per tanggal video, 5 Agt 2026)
- Tooltip contoh: Aug 2024 - BTC Price $59,060, MVRV ratio 1.88, Realized Price $31,414
- Tooltip contoh: Mar 2023 - BTC Price $23,470, MVRV ratio 1.18, Realized Price $19,860

### [04:10-07:40] Slide "Zone map - both sides ramp linearly with depth; the trim toggle is the only difference between modes"

Sumbu Y = MVRV band percentile. Boundary: 85 dan 90 di atas, 10 di bawah.

| Regime | % of days | Aksi |
|---|---|---|
| Pause + trim | 11.8% | deposit ke reserve, stack di-trim (persentil >90) |
| Pause | 4.9% | deposit masuk reserve cash (persentil 85-90) |
| Plain DCA | 66.9% | deposit beli BTC, reserve tidak disentuh (persentil 10-85) |
| Buy hard | 12.6% | deposit + penarikan reserve (persentil <10) |

Teks logika di slide (verbatim):
- "Both sides scale linearly with depth past the boundary."
- "Buying: zero at percentile 10, half at 5, and the full 10% of whatever cash sits
  in the reserve once the oscillator reaches 0."
- "Trimming: zero at percentile 90, half at 95, and the full 0.75% of the stack at 100.
  Trimming stops if BTC would fall below 50% of the book."
- "Accumulation mode is identical with the trim switched off."

Label pada grafik ramp: "peak 0.75% of the stack, per day" (sisi jual);
"peak 10% of the reserve, per day" (sisi beli).

### [09:36-10:00] Bar chart "Every start date, quarterly, 2014 to 2023 - sell mode positive on 100% of 39, accumulation on 74%"
- Sumbu Y: "IRR advantage over blind DCA (pp)"
- Dua seri: "Sell mode, after 20% [tax]" (biru) dan "Accumulation, no sell" (oranye)
- Biru: ~+9.5 s/d +11 pp untuk start date 2014-2020, turun ke ~+6 pp untuk start 2021-2022,
  naik lagi ke ~+8.5 pp untuk start 2023
- Oranye: NEGATIF (~-0.2 s/d -0.6 pp) untuk start date 2015-06 s/d 2016-12 (sekitar 6-7 bar),
  sisanya positif +1 s/d +6 pp
- n = 39 start date kuartalan

### [10:12] Slide heatmap "Taxed median edge over blind DCA (pp) - 39 start dates 2014-2023, 50% floor. Orange box marks the chosen cell"

Panel kiri "Sell side - boundary and trim rate" (Y = trim boundary percentile, X = peak daily trim rate at percentile 100):

| Trim boundary \ trim rate | 0.5% | 0.75% | 1.0% | 1.5% |
|---|---|---|---|---|
| 85 | +6.8 / +8.4 | +7.2 | +5.1 | +3.4 |
| 87 | +6.4 / +8.7 | +8.3 | +6.7 | +4.2 |
| **90** | +5.9 / +8.6 | **+10.1 (chosen)** | +9.0 | +6.9 |
| 93 | +4.9 / +7.6 | +9.3 | +10.1 | +9.0 |
| 95 | (blank) / +6.5 | +8.1 | +9.1 | +9.5 |

*(kolom pertama heatmap punya 5 kolom; label sumbu X yang terbaca: 0.5%, 0.75%, 1.0%, 1.5% -
kolom paling kiri labelnya tertutup. Dua angka per baris di kolom awal = kolom-1 dan kolom-2.)*

Panel kanan "Buy side - zone width and reserve rate" (Y = buy-hard zone percentile, X = peak daily reserve rate at percentile 0):

| Buy-hard zone \ reserve rate | 2% | 5% | 10% | 20% | 40% |
|---|---|---|---|---|---|
| 5 | +7.3 | +10.0 | +10.2 | +10.1 | +9.x |
| **10** | +9.0 | +10.2 | **+10.1 (chosen)** | +9.7 | +9.x |
| 15 | +9.2 | +9.7 | +9.4 | +8.7 | +7.x |
| 20 | +8.8 | +8.4 | +7.4 | +5.9 | +4.x |
| 25 | +8.2 | +7.0 | +5.4 | +4.3 | +3.x |

### [10:46] Tabel hasil final "$1,000 seed plus $100 a week from January 2014 - 0.1% fees, one-bar fill lag, 20% CGT on realised gains"

| Metrik | Blind DCA | Accumulation | Sell mode (taxed) |
|---|---|---|---|
| Total paid in | $66,700 | $66,700 | $66,700 |
| Final value | $2,968,017 | $3,115,675 | $5,794,249 |
| Multiple of blind | 1.00x | 1.05x | 1.95x |
| IRR | 54.0% | 54.7% | 64.0% |
| BTC held | 46.8 | 49.1 | 73.9 |
| BTC vs blind | - | +4.9% | +57.9% |
| Cash reserve left | $0 | $2,007 | $1,107,111 |
| Cash as % of book | 0.0% | 0.1% | 19.1% |
| Cash after yr 1 | 0.0% | 13.9% | 72.3% |
| Max drawdown | -83.5% | -83.2% | -70.4% |
| (jumlah trade jual) | 0 | 0 | 715 |
| (pajak dibayar) | $0 | $0 | $1,026,987 |

Panel "Cash reserve (% of book)" menunjukkan reserve membangun 4 kali: 2014 (dari seed),
2017-2018 (puncak ~50%), 2021-2022 (puncak ~72%), 2024-2026 (puncak ~62%, sedang
di-drawdown ke ~20% per Agt 2026).

### [11:41-11:50] Teks FAQ halaman chart (verbatim, dibaca dari frame)
- "What is a good MVRV Quantile reading to accumulate Bitcoin? Historically, readings
  below the 25th percentile have coincided with bear market accumulation ranges, and
  readings below the 10th percentile have appeared only near major cycle lows."
- "Why do the valuation bands tighten over time? As Bitcoin matures, its valuation
  extremes compress: each cycle's MVRV peak has been lower than the last, and each
  trough higher. The model fits this contraction directly."
- "Can Bitcoin's price move outside the bands? Yes, and that is by design. The shaded
  bands cover the 5th to 95th percentile of history. Breaks above the top band have
  marked the final phase of bull markets, and breaks below the bottom band have marked
  capitulation lows."
- "How is this different from the raw MVRV ratio? The raw ratio tells you market value
  relative to realized value today, but the same number can mean different things in
  different cycles. The quantile approach converts each reading into a percentile of
  all history, adjusted for cycle compression."

---

## Transkrip

[00:01] Hi everyone, I'm Matt from Bitcoinpro.com
[00:03] and today we are going to look into
[00:05] Bitcoin, but specifically this brand new
[00:09] amazing completely entirely free chart.
[00:12] We've added the MVRV quantile bands.
[00:15] Now, I know I've been talking about
[00:18] these quite a lot recently. A couple
[00:21] weeks ago, we released a video looking
[00:22] at exactly this approach, looking at
[00:25] these MV projection bands, applying an
[00:28] amplitude decay model, looking at the
[00:32] returns versus blind DCA versus buy and
[00:35] hold. I'll link it below so you can
[00:37] watch that if you haven't already. But
[00:40] the issue with this is this was just a
[00:43] small little niche bit of Pine Script
[00:46] I'd made for the purpose of this video.
[00:48] And as many of you pointed out, we do
[00:51] have to pay taxes unfortunately. So I
[00:53] went back and I altered the strategy. I
[00:56] looked at it through the point of view
[00:58] of an oscillator so we could actually
[01:00] measure it on a 0 to 100 scale. I went
[01:03] back to the guys at BM Pro and I
[01:05] thought, how can we make this? And we
[01:08] just made it. It wasn't too difficult.
[01:11] But now what we can do is see quickly,
[01:14] clearly, easily the valuation of Bitcoin
[01:17] in comparison to its historic value. So
[01:19] just as a quick refresher, what this is
[01:21] doing is looking at the MVRV score of
[01:24] Bitcoin, the market value to realize
[01:27] value, the average accumulation price,
[01:28] the cost basis of BTC, just this red
[01:32] line here. and it is fitting this
[01:34] amplitude decay model which is taking
[01:37] into account its fairly predictable
[01:41] rising bottoms and declining peaks. Now
[01:45] once we do all of that we can actually
[01:47] normalize Bitcoin and where it currently
[01:49] sits in relationship in in accordance to
[01:52] historical overvalued and undervalued
[01:55] levels. So we can scroll down here and
[01:56] you can see all of the underlying logic
[01:59] calculation methodology etc.
[02:03] But if we just look at where we are
[02:05] right now, current percentile 8%. Now,
[02:08] if I just zoom in over the past three
[02:10] cycles, what we can see, this is
[02:12] comparable to when Bitcoin is
[02:15] pretty much bottoming out in every
[02:17] single bare cycle. Can we go lower? Yes,
[02:20] of course we can. If we look to say
[02:22] 2022, we almost started hitting these
[02:24] bottom percentiles as Bitcoin first
[02:26] reached about $18,000.
[02:29] We then went down to about 15,000. So,
[02:31] we did go 20% lower. That's not out of
[02:33] the question. But one thing this model
[02:35] takes into consideration is the fact
[02:36] that if you look at the 2015 bare market
[02:39] low, we were very much beneath the
[02:41] realized price. 2019, a little bit less.
[02:44] 2022, a little bit less. We're reaching
[02:46] these levels before we've actually
[02:48] reached the realized price.
[02:52] A lot of people are looking at Bitcoin
[02:54] as
[02:55] a linear one or zero. Do I buy? Do I
[02:58] sell? If instead you take into
[03:00] consideration approach like this,
[03:02] working in percentiles, working in
[03:04] probabilities,
[03:06] then you can see returns like this where
[03:08] you're massively outperforming
[03:10] dollar cost averaging. But it'd be
[03:12] rubbish if we just provided this tool
[03:14] and didn't tell you exactly how to use
[03:16] it because I've done a lot of data
[03:19] analysis over the past few days. Now,
[03:22] this is by all accounts, and I I'll
[03:25] prove it with the numbers in a minute,
[03:29] the approach that if if you do not know
[03:31] what you're doing with your Bitcoin
[03:32] investing, this is probably not a bad
[03:35] place to start. And there's a few
[03:37] different ways you can really implement
[03:38] this. If you are of the mindset of never
[03:41] sell your Bitcoin,
[03:43] that's absolutely fine. You do you. you
[03:45] can still use this model and you will
[03:47] almost certainly still outperform blind
[03:50] dollar cost averaging into the market.
[03:51] Now, if we could lump some all the way
[03:53] back in 2014, yeah, that's a little bit
[03:56] different. But most of us don't have an
[03:59] infinite amount of cash sideline ready
[04:01] to deploy into the market. Most of us
[04:02] get paid from our jobs and from that we
[04:05] drip that into our investments. So, the
[04:08] way this works is, and I'm just going to
[04:10] hide myself because I might be a little
[04:11] bit in the way. When we are beneath
[04:14] the 10th percentile, we're in the bottom
[04:16] 10% of readings here, we are
[04:19] aggressively buying Bitcoin. Now, what
[04:23] we are buying with is this reserve. So,
[04:26] just quickly as well, standard if we're
[04:28] beneath the 85th percentile, which yes,
[04:30] it's very high. You should be dollar
[04:32] cost averaging into Bitcoin quite a lot.
[04:34] Essentially, if you look at the Bitcoin
[04:35] price action, even when we're starting
[04:37] to get a little bit overvalued, you
[04:39] know, we might be overvalued at a few
[04:41] thousand dollars before we rally 10x.
[04:43] So, yes, we are accumulating up until
[04:46] the 85th percentile. Now, if you are
[04:51] selling your Bitcoin, you do not have
[04:53] to, but this takes into consideration
[04:55] about a.1%
[04:57] fee for every sale and a 20% capital
[05:00] gains tax on every single profitable
[05:02] trade. This has all been taken into
[05:04] consideration.
[05:05] We are selling more aggressively as we
[05:08] start to get to the very overheated
[05:10] values and we're not selling a huge
[05:12] amount only at the very top 3/4 of a
[05:15] percentage point
[05:17] at the absolute peak of Bitcoin. Now
[05:20] again the reasoning for this is because
[05:21] we can be at new alltime highs looking
[05:24] very overvalued and still double. So, we
[05:27] want to take into consideration the fact
[05:29] that about 12% of Bitcoin's days are in
[05:33] this cell region. Over one in 10.
[05:36] There's quite a lot of time that you're
[05:37] going to be taking profit. So, it
[05:39] doesn't want to be a monumental amount.
[05:40] You don't want to start scaling out too
[05:42] early. If you don't want to sell, again,
[05:44] that is absolutely fine. But above 85%,
[05:49] you're pausing that dollar cost
[05:50] averaging in and the the baseline we use
[05:53] for this. And again, I'll get into the
[05:54] numbers. We did many many different
[05:55] methodologies of starting with a larger
[05:57] amount, depositing on monthly basis or a
[05:59] weekly basis. But for this, for
[06:01] simplicity's sake, I did starting with
[06:03] $100 and depositing $100 every single
[06:06] week. Now, this is just on the opening
[06:08] of the weekly candle. So, midnight
[06:09] Monday. Again, I tested this at the US
[06:12] open time. I tested this randomly
[06:15] seeding throughout the week. So, we buy
[06:16] randomly on Monday, Tuesday, Wednesday,
[06:17] Thursday, Friday. It didn't matter. They
[06:20] were fairly negligible differences in
[06:22] returns. But for simplicity sake, we are
[06:24] doing this at the weekly open with $100.
[06:28] Above 85% we're not selling below 85%
[06:32] standard DCA. But with this cash reserve
[06:34] that we've built up in this upper 80
[06:38] well this top 15% above the 85th
[06:40] percentile and especially if we've got
[06:42] an additional cash reserve because we've
[06:44] been very slowly scaling out. As we get
[06:45] into that top 10%, we build up a cash
[06:48] reserve. And this is where we're very
[06:50] aggressively scaling into Bitcoin. And
[06:52] again, this starts linearly. All the
[06:55] logic is here if you want to pause it
[06:57] and actually see exactly what we're
[06:58] doing. But at the lowest point of a
[07:01] Bitcoin bare market, when we are at the
[07:03] zero percentile, you're deploying 10% of
[07:06] your additional cash reserve to buy as
[07:08] much BTC as possible. And one thing we
[07:11] also figured out is
[07:14] it's not that you never want to sell
[07:15] your Bitcoin. Some people might change
[07:17] their views on that. The point is you
[07:19] never want to sell all of your Bitcoin
[07:21] as well from a monetary standpoint, from
[07:24] a performance standpoint, from a
[07:25] philosophical standpoint. I mean, why
[07:27] are we even here if all we're trying to
[07:28] do is maximize our fiat? No, I'm trying
[07:30] to maximize my Bitcoin. So, we're also
[07:33] putting a floor in of 50%. You can see
[07:36] here trimming stops if BTC would fall
[07:38] 50%. We always want half of our invested
[07:41] capital in BTC.
[07:44] Okay, that's the logic. Now, does it
[07:46] work?
[07:49] Again, I didn't want to overfit this.
[07:51] So, I didn't just want to test from
[07:52] 2014. And if you do go back and watch
[07:54] that YouTube video, we can see we did
[07:56] lots of out of sample testing. We tested
[07:59] if we limit the data to start in 2015,
[08:01] in 2018.
[08:03] We wanted to make sure that this is a
[08:05] viable strategy going forward. So, not
[08:07] only did we test this across multiple
[08:09] different start dates with multiple
[08:11] different data ranges, regardless on
[08:16] every single start date, 100% of start
[08:19] dates, you outperformed Bitcoin when
[08:22] taking into consideration 20% taxes and
[08:25] a.1%
[08:27] trade fee, which to be honest is quite
[08:29] high.
[08:30] This isn't taking into account any
[08:32] thresholds of capital gains allowance or
[08:33] setting your losses, etc. This is 20% on
[08:35] every single profitable sale you ever
[08:37] make. You beat buy and hold. You beat
[08:40] blind DCA 100% of the time.
[08:47] If you didn't want to sell your Bitcoin, which is a very valid strategy as well,
[08:49] you still bit beat Bitcoin about three
[08:52] quarters of the time. Now the only real
[08:55] phase of time and again I'm just going
[08:57] to hide myself where you didn't
[08:58] outperform Bitcoin is pretty much at the
[09:01] bottom of that 2014 1516 bare market
[09:05] because you haven't built up a cash
[09:06] reserve yet. So you're competing with
[09:10] blind DCA but then not having the cash
[09:12] reserve to actually deploy more at these
[09:14] cycle lows. However, any start date
[09:17] since then has outperformed.
[09:21] So, it's it's not looking bad. But
[09:23] again, we'll delve deeper because we
[09:25] didn't just check selling in the top
[09:28] 10%, pausing at the top 15% and and the
[09:32] deploy rates when we're in the bottom
[09:33] 10%. We tested every single combination
[09:36] possible.
[09:38] These are the optimal strategies. Now,
[09:40] we want to see numbers. How much did it
[09:42] actually outperform by?
[09:45] Outperformed by quite a lot. If we look
[09:47] at the blind DCA with this exact
[09:49] strategy,
[09:52] you started with $100, $100 a week. You
[09:56] finished on 46.8 Bitcoin.
[09:59] Not too bad with the accumulation
[10:03] strategy. Now, again, this was from
[10:04] 2014. So, if if we actually just go back
[10:07] here, this is just the the worst time to
[10:10] start. This is and my head's in the way.
[10:12] I'll hide it again. This is the very
[10:15] first bar here which we can see the
[10:17] outperformance by just accumulation
[10:18] without selling is minuscule. If we'd
[10:21] have done this from any other time this
[10:23] the the peak of the bare uh the bull
[10:25] market sorry then performance would have
[10:27] been considerably greater but I wanted
[10:29] as much back testing history as possible
[10:31] and it still outperformed blind DCA not
[10:34] by much granted but
[10:37] the sell strategy 73.9
[10:40] bitcoin
[10:42] after tax
[10:44] after fees and we can go and see all the
[10:47] raw numbers here we can see you
[10:49] practically doubled
[10:51] buy and hold blind DC ECA
[10:54] even if you paid a million dollars in
[10:56] taxes.
[10:59] This is a very simplistic strategy. Will
[11:02] it work forever? Maybe not. But what
[11:05] we're trying to do here is trying to
[11:08] create more actionable, more robust,
[11:12] more efficient, more accurate, more
[11:14] trusting. I mean, we're given everything
[11:17] that's happening right now. Again, you
[11:18] should verify, you shouldn't trust, but
[11:22] the MV quantile bands, if you don't know
[11:24] where to start, this is probably a good
[11:26] place to start. It will be free forever.
[11:30] So, you don't have to have any site
[11:32] subscription. Of course, I'm a little
[11:33] bit biased. I would say get a site
[11:34] subscription cuz then you can get
[11:36] indicator alerts, you get trading view
[11:38] scripts. You even have the chance
[11:41] to download this data via API, which is
[11:43] how I actually came up with all of these
[11:44] numbers because it's not the easiest
[11:46] just by eyeballing on the chat. So,
[11:48] there's lots of benefits as well. But,
[11:49] if this is the last Bitcoin Magazine Pro
[11:52] video you ever watch, it's probably not
[11:55] a bad one for it to be. But, as always,
[11:58] thank you all very much for watching.
