# This Strategy Beat Bitcoin DCA by 20x

**Channel:** On-Chain Mind
**URL:** https://www.youtube.com/watch?v=e0NAIj7tpgY
**Tanggal video:** 2026-07-28
**Durasi:** 07:49

---

## Catatan visual (dari frame video, low confidence dari resolusi frame)

- Indikator utama yang dibahas: **"Z-Score Probability Waves"** — chart menunjukkan harga BTC (garis putih/hijau) dengan band hijau/merah (probability waves) mengelilingi, dari 2013-2026, style dashboard "On-Chain Mind" (onchainmind.io).
- Strategi bernama **"Trading Cross"**: equity curve chart membandingkan 4 garis dari $10,000 awal — Trading Cross (pink, tertinggi), DCA Bitcoin (putih), Gold (kuning), S&P 500 (biru) — periode ~2014-2026.
- Angka akhir on-screen: DCA = $446,000; Gold = $32,000; S&P 500 = $40,000; Trading Cross tidak ditulis eksplisit di frame tapi disebutkan verbal "over $8 million".
- Chart drawdown: dua garis (pink = Trading Cross, putih = DCA) menunjukkan drawdown % dari waktu ke waktu — pink jelas lebih dangkal dibanding putih di sebagian besar periode.
- Slide "Calmar Ratio (CAGR ÷ Max Drawdown)": Trading Cross = 1.68, DCA = 0.44.
- Slide "10,000 Simulations": grafik fan/cone hijau menunjukkan sebaran hasil Monte Carlo, median line naik ke kanan atas.

---

## Transkrip

```
[00:03] Since 2014, dollar cost averaging into Bitcoin produced a 4,000% return, but
[00:06] Bitcoin produced a 4,000% return, but the price of earning it, however, was
[00:08] the price of earning it, however, was sitting through multiple 80% drawdowns.
[00:11] sitting through multiple 80% drawdowns. So, in this video, I'll show you one of
[00:12] So, in this video, I'll show you one of our top strategies that delivered an
[00:14] our top strategies that delivered an 80,000% return, but with the maximum
[00:16] 80,000% return, but with the maximum drawdown of just 42% along the way. So,
[00:19] drawdown of just 42% along the way. So, let's get straight into it.
[00:24] Now, before we get into the data, let me address the most obvious question. This
[00:26] address the most obvious question. This isn't just a backtest that's been
[00:28] isn't just a backtest that's been optimized perfection. It's a rule-based
[00:30] optimized perfection. It's a rule-based strategy that my subscribers and I have
[00:32] strategy that my subscribers and I have been using in real time, tested inside
[00:34] been using in real time, tested inside the strategy lab, where the goal isn't
[00:36] the strategy lab, where the goal isn't to maximize returns, but to try and
[00:39] to maximize returns, but to try and break the strategy itself and just see
[00:41] break the strategy itself and just see if it survives. So, by the end of this
[00:43] if it survives. So, by the end of this video, you'll be able to recreate the
[00:44] video, you'll be able to recreate the numbers for yourself in the strategy lab
[00:46] numbers for yourself in the strategy lab and decide whether they stand up to the
[00:48] and decide whether they stand up to the scrutiny. Now, what we have on screen is
[00:50] scrutiny. Now, what we have on screen is one of my favorite statistical
[00:52] one of my favorite statistical indicators, which is the Z-score
[00:53] indicators, which is the Z-score probability waves. And this here is just
[00:56] probability waves. And this here is just an advanced mean reversion tool that
[00:58] an advanced mean reversion tool that adapts across cycles. And the standard
[01:00] adapts across cycles. And the standard deviation of that result helps answer a
[01:02] deviation of that result helps answer a very simple question. How unusual is
[01:05] very simple question. How unusual is today relative to how this asset has
[01:07] today relative to how this asset has actually been behaving? And a reading of
[01:09] actually been behaving? And a reading of plus two means that the price is two
[01:11] plus two means that the price is two standard deviations above its normal
[01:13] standard deviations above its normal baseline, and a reading of minus two
[01:15] baseline, and a reading of minus two means it's two standard deviations
[01:17] means it's two standard deviations below. And the reason this matters so
[01:19] below. And the reason this matters so much for Bitcoin specifically is that
[01:20] much for Bitcoin specifically is that the baseline moves. Bitcoin in 2015 and
[01:24] the baseline moves. Bitcoin in 2015 and Bitcoin in 2025 are not the same asset.
[01:27] Bitcoin in 2025 are not the same asset. The volatility is compressed and the
[01:29] The volatility is compressed and the market cap has grown by orders of
[01:30] market cap has grown by orders of magnitude. Now, looking at a signal and
[01:33] magnitude. Now, looking at a signal and trading a signal are two very different
[01:35] trading a signal are two very different things, and that gap is where most
[01:37] things, and that gap is where most people actually lose their money. So,
[01:39] people actually lose their money. So, what we're going to do today is look at
[01:40] what we're going to do today is look at a way to actually trade this. Now, the
[01:42] a way to actually trade this. Now, the strategy we're going to be using here is
[01:44] strategy we're going to be using here is something called the trading cross, and
[01:46] something called the trading cross, and it takes the probability waves on the
[01:48] it takes the probability waves on the shorter time frame and trades the cross
[01:50] shorter time frame and trades the cross up and the cross down. And it's very
[01:52] up and the cross down. And it's very simple in its methodology. It buys
[01:54] simple in its methodology. It buys whenever the cross is above one into the
[01:56] whenever the cross is above one into the positive and then sells when we cross
[01:58] positive and then sells when we cross back below zero. So, essentially it buys
[02:01] back below zero. So, essentially it buys momentum when it's confirmed to the
[02:03] momentum when it's confirmed to the upside, but then immediately exits as
[02:06] upside, but then immediately exits as soon as any negative downside has
[02:07] soon as any negative downside has occurred. And you'll notice how
[02:09] occurred. And you'll notice how deliberately simple but asymmetric that
[02:11] deliberately simple but asymmetric that is. The entry demands proof. You're not
[02:14] is. The entry demands proof. You're not buying into strength. You're buying into
[02:16] buying into strength. You're buying into strength that's already pushed a full
[02:18] strength that's already pushed a full standard deviation above its own
[02:19] standard deviation above its own baseline, which filters out those
[02:21] baseline, which filters out those enormous amounts of noise and chop that
[02:23] enormous amounts of noise and chop that you see. But the exit demands nothing
[02:25] you see. But the exit demands nothing else. The moment price slips back to
[02:27] else. The moment price slips back to merely average, you're flat and you're
[02:29] merely average, you're flat and you're not waiting for a confirmation of
[02:30] not waiting for a confirmation of weakness. You're not giving it any room.
[02:33] weakness. You're not giving it any room. And that asymmetry is what produces the
[02:34] And that asymmetry is what produces the drawdown profile that we're about to
[02:36] drawdown profile that we're about to look at. And it's literally the
[02:37] look at. And it's literally the mathematical opposite of how most retail
[02:39] mathematical opposite of how most retail traders behave, which is to enter early
[02:41] traders behave, which is to enter early on hope and then exit late on hope. Now,
[02:44] on hope and then exit late on hope. Now, here we can see the equity curve for
[02:46] here we can see the equity curve for each strategy. And the pink line is the
[02:48] each strategy. And the pink line is the trading cross and the white line is
[02:49] trading cross and the white line is simply dollar cost averaging into
[02:51] simply dollar cost averaging into Bitcoin. And then the yellow and blue
[02:53] Bitcoin. And then the yellow and blue lines are the equivalent strategies for
[02:55] lines are the equivalent strategies for gold and the S&P 500. All starting with
[02:58] gold and the S&P 500. All starting with that same $10,000. DCA into Bitcoin grew
[03:01] that same $10,000. DCA into Bitcoin grew to about $446,000,
[03:04] to about $446,000, gold to roughly $32,000,
[03:06] gold to roughly $32,000, and the S&P 500 to about $40,000.
[03:09] and the S&P 500 to about $40,000. The trading cross, however, finished at
[03:11] The trading cross, however, finished at over $8 million.
[03:13] over $8 million. And this lets you compare the strategy
[03:15] And this lets you compare the strategy not just against holding Bitcoin, but
[03:17] not just against holding Bitcoin, but against the two of the benchmarks that
[03:18] against the two of the benchmarks that most of the capital in the world is
[03:20] most of the capital in the world is actually measured against. Now, from a
[03:22] actually measured against. Now, from a simple raw returns perspective, you can
[03:24] simple raw returns perspective, you can see that it delivered an 80,000% return,
[03:26] see that it delivered an 80,000% return, which is a 72% compound annual growth
[03:29] which is a 72% compound annual growth rate versus dollar cost averaging's
[03:31] rate versus dollar cost averaging's 4,000% return or a 36% compound annual
[03:34] 4,000% return or a 36% compound annual growth rate. So, the strategy roughly
[03:37] growth rate. So, the strategy roughly doubles the annualized rate of
[03:38] doubles the annualized rate of compounding. And when you double a
[03:40] compounding. And when you double a compounding rate over a decade, the gap
[03:43] compounding rate over a decade, the gap becomes absurd. And that's the entire
[03:45] becomes absurd. And that's the entire lesson of compounding in one screenshot.
[03:47] lesson of compounding in one screenshot. It's not that the strategy made twice
[03:49] It's not that the strategy made twice the money, it made 20 times as much
[03:51] the money, it made 20 times as much money, but the advantage was applied
[03:53] money, but the advantage was applied again and again to a growing base.
[03:56] again and again to a growing base. And here we can see that you also do
[03:57] And here we can see that you also do that with much less of a drawdown
[03:59] that with much less of a drawdown profile, which is the part that actually
[04:01] profile, which is the part that actually makes it investable in real life. Again,
[04:03] makes it investable in real life. Again, the pink line here is the trading cross,
[04:05] the pink line here is the trading cross, which has a maximum drawdown of 42.9%
[04:09] which has a maximum drawdown of 42.9% while DCA drew down by 83% during that
[04:11] while DCA drew down by 83% during that time. And I want to be honest about what
[04:13] time. And I want to be honest about what an 80% drawdown actually feels like
[04:15] an 80% drawdown actually feels like because it's very easy to look at that
[04:17] because it's very easy to look at that chart in hindsight. An 83% drawdown
[04:20] chart in hindsight. An 83% drawdown means that for every $100,000 that you
[04:22] means that for every $100,000 that you had, you're looking at having $17,000 at
[04:24] had, you're looking at having $17,000 at the end of it. And then to simply return
[04:27] the end of it. And then to simply return to back where you started, you'd need a
[04:28] to back where you started, you'd need a 490% return. And that is the moment
[04:31] 490% return. And that is the moment where pretty much everybody sells and
[04:34] where pretty much everybody sells and it's why so few people actually capture
[04:36] it's why so few people actually capture those brilliant 4,000% returns that DCA
[04:39] those brilliant 4,000% returns that DCA has actually presented us with. And
[04:41] has actually presented us with. And nothing here explains this trade-off
[04:42] nothing here explains this trade-off better than something called the Calmar
[04:44] better than something called the Calmar ratio, which is essentially the compound
[04:46] ratio, which is essentially the compound annual growth rate divided by the
[04:48] annual growth rate divided by the maximum drawdown. So here, the higher
[04:50] maximum drawdown. So here, the higher numbers are better because it means that
[04:52] numbers are better because it means that you're getting a better return per unit
[04:54] you're getting a better return per unit of pain that you've actually endured.
[04:56] of pain that you've actually endured. And the trading cross strategy had a
[04:58] And the trading cross strategy had a Calmar ratio of 1.68 while DCA was 0.44.
[05:03] Calmar ratio of 1.68 while DCA was 0.44. Now, if we think about what those two
[05:04] Now, if we think about what those two numbers are saying, a Calmar of 0.44
[05:07] numbers are saying, a Calmar of 0.44 means that for every 1% of
[05:09] means that for every 1% of peak-to-trough pain that you had to
[05:11] peak-to-trough pain that you had to absorb, you were compensated with 0.44%
[05:15] absorb, you were compensated with 0.44% of annual growth. And a Calmar of 1.68
[05:18] of annual growth. And a Calmar of 1.68 means that 1% of pain bought you 1.68%
[05:22] means that 1% of pain bought you 1.68% of annual growth. So that's nearly four
[05:24] of annual growth. So that's nearly four times the compensation for the same unit
[05:26] times the compensation for the same unit of suffering. So even though Bitcoin is
[05:28] of suffering. So even though Bitcoin is one of the best risk-adjusted trades of
[05:30] one of the best risk-adjusted trades of all time, a Calmar ratio of 0.44 is
[05:33] all time, a Calmar ratio of 0.44 is actually pretty poor because the
[05:35] actually pretty poor because the drawdown is so extreme. And anything
[05:37] drawdown is so extreme. And anything above one is considered absolutely
[05:39] above one is considered absolutely excellent. So 1.68 is pretty outstanding
[05:42] excellent. So 1.68 is pretty outstanding here. But a single backtest here is just
[05:44] here. But a single backtest here is just one sequence of events. It's one path
[05:47] one sequence of events. It's one path through history. So, we ran a quick
[05:49] through history. So, we ran a quick Monte Carlo simulation of 10,000
[05:51] Monte Carlo simulation of 10,000 simulations. And this takes the
[05:53] simulations. And this takes the strategy's actual daily returns, and
[05:55] strategy's actual daily returns, and then randomly reshuffles their order
[05:57] then randomly reshuffles their order thousands of times, and then creates
[05:59] thousands of times, and then creates thousands of alternative histories. And
[06:01] thousands of alternative histories. And the question here is simple. Was the
[06:03] the question here is simple. Was the performance dependent on getting lucky
[06:05] performance dependent on getting lucky with the order of the returns, or was
[06:07] with the order of the returns, or was the edge genuinely robust? And the
[06:09] the edge genuinely robust? And the answer here is pretty clear. Only a tiny
[06:11] answer here is pretty clear. Only a tiny fraction of simulations underperformed
[06:14] fraction of simulations underperformed Bitcoin DCA.
[06:15] Bitcoin DCA. And even then, it was often by just a
[06:17] And even then, it was often by just a few thousand dollars.
[06:18] few thousand dollars. In fact, the fifth percentile outcome
[06:21] In fact, the fifth percentile outcome still finished at $463,000.
[06:24] still finished at $463,000. So, in other words, if you run the
[06:25] So, in other words, if you run the strategy 100 different times under
[06:28] strategy 100 different times under equally realistic market conditions,
[06:30] equally realistic market conditions, only around five runs would have
[06:32] only around five runs would have produced a lower return. And yet, the
[06:34] produced a lower return. And yet, the worst 5% outcome still actually beat
[06:37] worst 5% outcome still actually beat dollar cost averaging. The other 95 runs
[06:39] dollar cost averaging. The other 95 runs performed even better, and often by
[06:41] performed even better, and often by quite a significant margin.
[06:43] quite a significant margin. And the reason that's such a powerful
[06:44] And the reason that's such a powerful test is that it destroys the luck of
[06:46] test is that it destroys the luck of ordering. If your headline number only
[06:48] ordering. If your headline number only exists because three enormous winners
[06:50] exists because three enormous winners happened to land on a particular
[06:51] happened to land on a particular sequence, then resequencing them will
[06:54] sequence, then resequencing them will expose that immediately, and your median
[06:56] expose that immediately, and your median outcome will collapse far below your
[06:58] outcome will collapse far below your back-tested one.
[06:59] back-tested one. So, that here confirms that this final
[07:01] So, that here confirms that this final figure is actually very close to the
[07:02] figure is actually very close to the median outcome, which tells you the edge
[07:04] median outcome, which tells you the edge is from the distribution of returns
[07:06] is from the distribution of returns itself, and not just from a fortunate
[07:08] itself, and not just from a fortunate arrangement of them.
[07:10] arrangement of them. So, really here, this is just a quick
[07:11] So, really here, this is just a quick taster. This is the whole point of the
[07:13] taster. This is the whole point of the strategy lab for me. Not to give you a
[07:15] strategy lab for me. Not to give you a number to believe in, but to give you
[07:16] number to believe in, but to give you every tool that you need to actually
[07:18] every tool that you need to actually disbelieve it, and then show you what's
[07:20] disbelieve it, and then show you what's left standing afterwards. So, if you'd
[07:22] left standing afterwards. So, if you'd like to try it yourself, then go head
[07:24] like to try it yourself, then go head over to onchainmind.io, where you'll
[07:25] over to onchainmind.io, where you'll find two other strategies that are based
[07:27] find two other strategies that are based on completely different signals of mine.
[07:29] on completely different signals of mine. And there's many more being built into
[07:30] And there's many more being built into the lab very soon. So, anyway, I hope
[07:32] the lab very soon. So, anyway, I hope you all found this useful, and as
[07:34] you all found this useful, and as always, I'll catch you in the next one.
[07:37] always, I'll catch you in the next one.
[07:37] >> [music] >> Onchain Mind
[07:43] Onchain Mind >> [music]
[07:44] >> [music] >> Call it.
```
