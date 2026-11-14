# Bitcoin MVRV Explained (Almost Nobody Reads It Properly)
**Channel:** On-Chain Mind
**URL:** https://www.youtube.com/watch?v=NOqtqNy5GkE
**Tanggal video:** 2026-09-15
**Durasi:** 15:02
**Sumber transkrip:** YouTube auto-captions (en), di-dedupe dari rolling captions. Typo auto-caption (mis. "MVV", "NVRB", "bare market") dibiarkan apa adanya. Timestamp paragraf = perkiraan (resolusi ~detik awal paragraf).

---

[00:00] The MVRV ratio is probably the single most quoted onchain metric in Bitcoin. You'll see it in tweets at the top of every cycle and you'll see it rolled out at every capitulation load for proof that the bottom is in. And yet, for something so widely quoted, I think this is one of the most misunderstood metrics.

[00:26] So, in this video, I want to give you a proper overview of this classic metric using the five different ways that I like to look at it through my own dashboard and flagging the myths as we go, including the one about the Zcore that almost everybody gets wrong. So, let's get into it. Now, let's start at the beginning. MVRV stands for market value to realize value, and it's been around since about 2018, and the concept is actually beautifully simple. You take Bitcoin's market cap, which is just the current price multiplied by the circulating supply of Bitcoin, and then you divide it by the realized cap, and that's basically the whole metric.

[00:51] And every derivative of it is built off this bond concept. And the value that it spits out essentially tells you how much the market is paying for Bitcoin relative to what the market actually paid for their Bitcoin. But the second number, the realized cap, is the part that I really need you to understand because if you get that, then everything else in this video just falls into place. Now, the market cap, as we said, prices every single coin in existence at today's price.

[01:16] So, it doesn't care whether a coin last moved in 2011 or last moved this morning. Whatever the spot price is today, for instance, it's 77,000 at the time of recording. It values every single Bitcoin at that 77,000, which is useful, but as we'll see, the vast majority of coins didn't actually exchange hands at 77,000 or anywhere near it. Now, the realized cap does something much more clever.

[01:42] It takes every individual UTXO, which is essentially every unspent chunk of Bitcoin that's sitting on the chain, and it values that coin at the price that it last moved on chain. And then it just adds all of those up. So a coin that last transacted at $300 is counted at $300. And a coin that last moved today at $77,000 is again counted at $77,000. And what you end up with is an aggregate cost basis for the entire network.

[02:09] Or how I like to view it, it's the total amount of capital that's actually committed to Bitcoin. So it's essentially the onchain equivalent of asking what the market is actually paid in real dollars for the coins that they're currently holding. And right now it's currently stood at just over $1 trillion. So while the market cap is a great vanity metric for seeing how big Bitcoin could potentially become, the realized cap is the actual true amount of capital that has been entrusted to this network.

[02:34] And $1 trillion is a hell of a lot when you think about it. Now anyway, back to the MV. We said that this metric essentially compares the market cap to the realized cap. So when the MV is at one, then the average holder is exactly at break even. So here the market is valuing the network at precisely what the network paid for it. And when MVRV is at three, the average unit of Bitcoin is worth three times what it last moved for.

[03:00] And when it drops below one, the average holder is actually underwater. So really MV isn't a price metric. It's a measure of the aggregate unrealized profit and loss of the network. Now, why does that matter for market behavior? Well, because unrealized profit is the fuel for investors selling. Nobody sells a coin because they're deeply underwater unless they're capitulating. But when the average holder is up 200, 300, or even 400%.

[03:27] Then the temptation to realize those gains becomes more and more overwhelming. So really, when MV is high, the incentive to sell is high as well, and the market has to absorb it because remember, everyone has a price. You might think that you'd never sell, but if I put a few thousand% gains in front of you, you'd definitely be tempted to, right? All right, so now that we've grasped the concept, let's get into the different ways that we can actually look at the MVRV because there's some views that are way more powerful than others. And the first here is the raw MVRV.

[03:53] And this is the classic that you've probably seen. It's the plain ratio that everybody quotes. And historically, readings above three or four on this metric have coincided with the euphoric market tops. And readings below one have marked those deep value zones near cycle lows. And that genuinely did work for many cycles.

[04:18] But there's a problem with the raw view that is getting missed, and it's the reason that I lean much more heavily on one of the later views that I'm about to show you. Bitcoin's raw MV peaks are getting lower and lower every single cycle. In 2011, you had readings that were absolutely absurd, off the top of the chart. And in 2013 and 2014, the peaks were enormous, too. 2017 was lower, but still pretty parabolic. And in 2021, we were still euphoric, but lower once again. So, if you're sitting there waiting for the old numbers to print, then you're likely going to be waiting forever.

[04:44] What you're looking at are structurally diminishing returns in the metric itself because Bitcoin is larger and it's more liquid and it's more institutionally held than it ever was. And it simply doesn't get as absurdly overextended relative to its own cost basis as it once did. And we actually saw this play out this cycle once again. Our peak readings barely got over 2.5, which compared to previous cycles are pretty subdued readings.

[05:10] But even more interesting than that, we actually never even dip below one during our most recent bear. And this is the first time this has ever happened. And it means that even with price drawing down as far as it did, it still didn't drop below the average cost basis of the average holder. And for me, this feels like a trend that is just going to keep continuing into the future. So what do we do about all of this? Well, for me, we have to stop looking at the absolute number and start looking at where the number sits relative to its own history.

[05:35] Which brings me on to the second view, which is equally as popular. And that's the zcore. And I want to clear up just a little bit of misunderstanding about this metric that gets pushed around all over the place. The MVRV zcore isn't a zcore of the MVRV ratio. It might sound like a small thing, but it actually matters. Most people assume that you take the MVRV numbers over time and work out the average and how much they typically swing, then standardize from there. But that's actually not it. What actually happens is simpler.

[06:02] You just take the market cap, subtract the realized cap, and what you're left over is the raw dollar gap between the two, and then you divide that gap by how much the market cap normally swings around. And it was built to try and smooth out those huge distortions that you get in Bitcoin's early life. So, it behaves far more consistently as the asset matures. But actually, when you look at it, it's a very similar pattern to the raw metric itself.

[06:28] And we're not seeing anywhere near the violent swings that we did in the past. So, this is one of the most quoted metrics online, yet it hasn't been particularly useful. Now, the third view here is the one I'd argue is the most underused by far and honestly the most powerful, which is the percentile view. So, instead of asking what the raw MVRV or even the Zcore is, the percentile view asks a different question. What percentage of Bitcoin's history has MV been lower than it is right now?

[06:54] So a reading that is in the 95th percentile means that MVRV has only ever been higher than this 5% of the time ever. And a reading in the fifth percentile means that it's almost never been cheaper than this on this basis. And you see why that's so much more useful because a percentile is dimensionless. So it doesn't care what the raw MV tops out or even if that keeps coming lower every cycle.

[07:19] It doesn't care about those diminishing returns. So it automatically rescales itself to the asset's own evolving history, which means you can compare 2013 to 2017 and 2021 to today on a genuinely like forlike footing. A 90th percentile reading in 2013 and a 90th percentile reading today mean the same thing, which is that the market is as stretch as it basically ever gets relative to itself. The raw number can't give you that, but the percentile can.

[07:47] And if you want to see every chart that I use, including the ones I'm using today, then go check them all out at onchainmind.io, where you'll also find our weekly newsletter. Now, the fourth view takes a completely different lens on it, and that's the momentum. Now, the levels tell you where we are, but they don't tell you which way we're traveling or how quickly. And the momentum solves that.

[08:12] And what we're doing here is looking at the rate of change of the MVRV by comparing the short-term movement against the longerterm baseline. And what that gives you is a read on whether profitability across the network is either expanding or contracting, which is quite a useful metric in itself. And think about this distinction for a second. The MVRV can be sitting at a perfectly healthy two, which sounds neutral and comfortable. But if the momentum has just rolled over and turned negative, you're in a market where the average profitability is deteriorating even though the headline number looks fine.

[08:38] And equally, when the raw number crosses back above one from below and the momentum is accelerating upwards, that has historically been one of the cleanest signals that the bare market is genuinely over rather than just bouncing. So crossovers in this momentum view have tended to lead those big trend changes. And that's the whole point of it.

[09:04] And we can see that right now that we're right on the edge of transitioning back into the green again for the first time in over a year, which tells us that if we can keep up this momentum for a little while longer, then we might be able to confirm that the bull market is indeed back. Now, the fifth and final view here is the distribution. And this is my favorite for pure early warning. Rather than plotting the MVV against time, we can look at how MVV readings are distributed. So, how much time the metric is spent at each level and where the current reading sits within that distribution.

[09:29] And when price is pushing into the thin right hand tail where there's very little history that's lived there, you're being told something quite specific. You're being told that the market is in a territory where holders have historically found it almost impossible not to sell. And that's an advanced warning of sellside distribution and it usually arrives prior to the price rolling over rather than after.

[09:54] Now, let's quickly talk about cohorts because everything up to this point has been about the total MVRV. But there's even more power that we can gather from this metric. For instance, you can calculate the MVRV for any subset of the supply. And the one that matters more than any others in my opinion is the short-term holders. Now, firstly, short-term holders are coins that have moved within the last 155 days, so about 5 months. And long-term holders are coins that haven't moved in longer than that. And that 155day threshold isn't arbitrary.

[10:19] It's the point beyond which coins statistically become far less likely to be spent. And actually when you look at it, these two groups behave in completely opposite ways and the aggregate metric blends them into mush. So the short-term holder MV is the most tactical view here and this is the one where you can genuinely use it in practice. Even on the raw view, this one has remained remarkably consistent for many cycles now. And the reason is simple. Short-term holders are the recent buyers.

[10:45] So the reactive money and the speculators, their cost basis is by default close to the spot price. So their MVRV oscillates fast and violently around one. And in a bull market, short-term holder MV falling back to one has repeatedly marked the local bottom of a correction because that's where the level where recent buyers are collectively at break even and price is sitting right on their cost basis.

[11:10] And it becomes kind of a support zone where they're happy to step back in and buy at their cost basis again. Buying dips at that level and trimming when it stretches well above one has been one of the most reliable rhythm trades in onchain analysis. And you can see this most clearly in the 2017 bull run. Every time price pulled back hard, short-term holder MVRV dropped back towards one. And every time that's where the correction found its flaw as the perfect buy the dip moment.

[11:35] Recent buyers hit break even. They stepped back in and then the uptrend resumed again. And it happened repeatedly throughout the entire run, right up until the euphoria pushed the MVRV so far above one that there was just no cohort left underneath to defend it. And in a bare market, this actually works in reverse.

[12:01] Short-term holder MV rallying back up towards one has repeatedly marked the local top of a relief bounce because that's where the level of recent buyers are collectively back to break even again and the price is sitting right on their cost basis. So it kind of becomes a resistance zone where they're just relieved to get out and sell back at the cost basis. And selling the rallies into this level rather than chasing them has been the mirror image version of the same rhythm trade. And the 2018 bare market that followed is a textbook case. Once the top was in, short-term holder NVRB couldn't hold above one anymore.

[12:26] Every rally that dragged it back up to that level got sold straight into for the entire bare market. And that rejection at one was basically the signature of the whole year right up until 2019 when price finally broke back above it which marked the start of the next bull market. And 2022 is almost a carbon copy.

[12:52] We saw the same rejections, the same grinding bear and the rally stalling out at the recent buyers cost basis month after month until the structure finally shifted going into 2023 and the bull market came back. And right now in 2026, we've watched the exact same pattern play out again. Since the top in last October, every attempt to reclaim that one level was sold straight into, and the short-term holder MVRV spent nearly all of this year pinned below it. Month after month of rallies just failing at the same ceiling.

[13:18] And it's the same mechanics of human psychology playing out all over again. But for the first time since October, we've actually convincingly broke back above one. And in every other historical case, that reclaim has marked the start of the next bull. So only time will tell if that's the exact same story playing out again. So to quickly wrap all of this up, is the MVRV the best timing tool that we have? Well, in my opinion, no, not on its own.

[13:43] The raw value can stay in the overheated zone for many months whilst price keeps climbing and it can sit under one for a long grinding time before anything changes. It gives you a rough idea about the risk and reward and the incentive of investors over a cycle, but not about what the next week or month are going to do. But as you've seen, I've been relying less and less on the raw version itself and even the Zcore, too. The diminishing peaks are a feature and not a bug.

[14:09] But they also make it harder to judge where we really sit in the cycle as time evolves. And personally, that's why I like using the percentile view because it doesn't care what the raw number is, only where today ranks against the other days in Bitcoin's history. But the one trusty raw view that I can't see changing anytime soon is the short-term holder MVRV. And this is because the cohort itself resets every 5 months.

[14:34] There's always a fresh wave of recent buyers with a fresh cost basis and with a fresh set of irrational behaviors that we can take advantage of. So anyway, I hope you'll find this useful and if you like these metric deep dives then let me know down in the comments section and I'll keep doing some more. But anyway, thanks again for watching and as always, I'll catch you in the next one. [music] >> [music]

---

## Catatan visual dari frame (low confidence dari resolusi frame, 512px)

Semua chart dari dashboard On-Chain Mind ("Profit & Loss Dashboard", onchainmind.io). Timestamp frame perkiraan (~11 detik per frame).

- **[00:00-01:00] MVRV raw (2010-2026):** garis putus-putus di 1.0. Puncak ~8 (2011), ~6 (2013), ~5 (2017), ~4 (2021), ~2.7 (2024/25). Nilai terakhir ~1.4-1.5.
- **[01:50-02:30] Realised Cap (log scale):** anotasi "$1T" di ujung kanan (2026).
- **[04:20-05:00] MVRV raw + garis tren turun** ditarik dari puncak 2011 melewati puncak 2013, 2017, 2021, ke 2024/25 = ilustrasi "diminishing peaks". Tulisan "WHAT DO WE DO ABOUT THIS?".
- **[05:40-06:10] MVRV Z-Score:** rumus di layar = (Market Cap − Realized Cap) / Standard Deviation (Market Cap). Puncak ~10 (2013/2017), ~7-8 (2021), ~3-4 (2024). Nilai terakhir dekat ~0.5.
- **[06:40-07:10] MVRV Percentile ("Historical Percentile", 0-100%):** zona merah di atas ~90%, zona hijau di bawah ~10-15%, garis putus-putus di 50%. Siklus 2024 sempat mencapai zona atas (~90%+). Nilai terakhir (Sep 2026) sekitar ~35-40th percentile, setelah low sekitar ~15-20% di 2026.
- **[07:50-08:00] B-roll:** montase dashboard berbagai chart.
- **[08:10-08:50] MVRV Momentum (2015-2026):** osilator hijau/merah di sekitar 0. Anotasi panah di: crossover naik ~2015/16, crossover naik ~2019, crossover naik ~2023. Periode merah panjang ~2025-2026; nilai terakhir di sekitar 0, "right on the edge" berubah hijau. Metode persis tidak dijelaskan selain "short-term movement vs longer-term baseline".
- **[09:10-09:40] MVRV Distribution (histogram frekuensi harian):** mode sekitar ~1.2-1.4. Panel "Current Status": **MVRV 1.43**, bucket range 1.40-1.60, days in range 605, % days below 36.6%.
- **[10:00-10:30] STH MVRV (2017-2026):** garis putus-putus di 1.0, puncak ~2.1 (akhir 2017). Nilai terakhir di atas 1 (~1.1).
- **[11:20-12:00] STH MVRV zoom Jan 2016 - Apr 2019:** panah di 7 titik (2016-2017) saat STH-MVRV turun ke ~1.0 lalu memantul = "buy the dip". Setelah top Des 2017, STH-MVRV di bawah 1 sepanjang 2018, reclaim awal 2019.
- **[13:00-13:30] STH MVRV zoom Okt 2025 - Sep 2026:** STH-MVRV ~1.1 di Okt 2025, turun di bawah 1 dari ~Nov 2025, low ~0.68-0.7 sekitar Feb 2026, rally ke ~0.97 sekitar Mei 2026 lalu gagal, turun lagi, lalu reclaim tajam ke ~1.15 sekitar Agustus 2026, sekarang ~1.08-1.1. Harga (sumbu kanan) naik dari ~$62-65k ke ~$80k lalu ~$77k.
- **[14:00-14:40] Outro:** kolase MVRV raw, percentile, STH MVRV.

Harga BTC saat rekaman disebut $77,000 [00:59]; realized cap "just over $1 trillion" [02:04].
