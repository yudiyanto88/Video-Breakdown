# Findings — Apakah shock membalik trend atau memperpanjangnya?

**Insight asal:** B-1 — "Shock di BTC cenderung memperpanjang trend, bukan membalikkannya" (video: 36% flip setelah shock vs 46% hari acak)
**Sumber:** Look Into Bitcoin, "Bitcoin News Doesn't Actually Move The Price" (2026-08-15), `[06:38]`–`[07:14]`
**Script:** [`analyze_shock_trend_continuation.py`](analyze_shock_trend_continuation.py) (+ helper [`shock_zone_lib.py`](shock_zone_lib.py))
**Event table:** [`events_shock_trend_flip.csv`](events_shock_trend_flip.csv)
**Tanggal validasi:** 2026-08-20

---

## Definisi event

- Shock: definisi yang sama dengan validasi lain (PRIMARY `|log ret| >= 3 × vol30 at-gate`; VARIAN `|log ret| >= 8%`).
- **Trend at-gate** = tanda log return 30 hari yang berakhir di **t−1** — hari shock **dikeluarkan** dari perhitungan trend. Ini koreksi terhadap titik lemah utama versi presenter: kalau hari shock ikut masuk window trend, satu candle −15% otomatis melabeli trend jadi bearish dan hasilnya bias mekanis ke "continuation".
- **Flip** = tanda log return forward t→t+30 berbeda dari tanda trend at-gate.
- Verdict ditentukan oleh selisih terhadap **baseline (b) matched**: hari non-shock yang tanda trend at-gate-nya SAMA — bukan terhadap rata-rata semua hari.

---

## Q1/Q2 — Flip rate 30 hari

| Scope | Definisi | n shock | flip setelah shock | base (a) semua hari | base (b) matched | selisih vs (b) |
|---|---|---:|---:|---:|---:|---:|
| Full 2010-2026 | PRIMARY | 170 | 35,9% [29-43] | 46,5% | 46,5% | **−10,6pp** |
| ≥2013 | PRIMARY | 139 | **36,0%** [28-44] | 47,2% | 47,5% | **−11,6pp** |
| Full 2010-2026 | VARIAN 8% | 397 | 43,8% [39-49] | 46,5% | 46,0% | −2,2pp |
| ≥2013 | VARIAN 8% | 269 | 46,5% [41-52] | 47,2% | 47,0% | **−0,5pp** |

**Angka video tereplikasi hampir persis** di definisi PRIMARY: 36,0% vs 47,2% (video: 36% vs 46%).

**Efek koreksi at-gate ternyata kecil** — inilah pengujian terpenting dari validasi ini:

| Definisi | flip pasca-shock at-gate | flip pasca-shock naif | semua hari at-gate | semua hari naif |
|---|---:|---:|---:|---:|
| PRIMARY | 36,0% | 35,3% | 47,2% | 46,8% |
| VARIAN 8% | 46,5% | 46,5% | 47,2% | 46,8% |

Selisih at-gate vs naif hanya 0,7pp. **Jadi efek continuation BUKAN artefak dari hari shock yang ikut masuk window trend** — kecurigaan metodologis utama terhadap klaim presenter tidak terbukti.

**TAPI efeknya runtuh di definisi shock yang kedua.** Dengan ambang fixed 8%, selisihnya tinggal −0,5pp (≥2013) — praktis nol. Sesuai aturan anti-overfit di CLAUDE.md: **dua varian dites, hanya satu yang menghasilkan efek. Ini wajib dilaporkan sebagai peringatan, bukan sebagai konfirmasi.** Efeknya melekat pada definisi shock relatif-terhadap-volatility, bukan pada "pergerakan besar" secara umum.

## Q3a — Stratifikasi arah shock (≥2013, PRIMARY)

| Sel | n | flip% | CI | base (b) | selisih |
|---|---:|---:|---|---:|---:|
| DOWN-shock | 66 | 43,9% | [33-56] | 49,3% | **−5,3pp** |
| UP-shock | 73 | 28,8% | [20-40] | 46,0% | **−17,2pp** |

**Ini temuan terpenting yang video tidak sebut: efeknya hampir seluruhnya datang dari UP-shock, bukan DOWN-shock.**

## Q3b — Arah shock × tanda trend at-gate

| Sel | n | flip% | base% | selisih |
|---|---:|---:|---:|---:|
| DOWN + trend NAIK | 27 | 40,7% | 42,5% | −1,8pp |
| DOWN + trend TURUN | 39 | 46,2% | 53,9% | −7,8pp |
| UP + trend NAIK | 51 | 25,5% | 42,5% | **−17,1pp** |
| UP + trend TURUN | 22 | 36,4% | 53,9% | −17,6pp |

Sel terkuat (UP + trend NAIK, n=51): hanya 25,5% flip vs 42,5% baseline. Terjemahan praktisnya: **hari lonjakan besar di tengah uptrend cenderung diikuti uptrend yang berlanjut 30 hari berikutnya.** Sel DOWN + trend NAIK (n=27) — yang paling relevan untuk pertanyaan "apakah shock ke bawah membatalkan bull" — selisihnya **−1,8pp, praktis nol.**

## Q3c — Per cycle (PRIMARY, semua arah shock)

| Cycle | n | flip% | CI | base (b) | selisih | % dari total |
|---|---:|---:|---|---:|---:|---:|
| C1 2010-2015 | 61 | 32,8% | [22-45] | 38,7% | −5,9pp | 36% |
| C2 2015-2018 | 43 | 48,8% | [35-63] | 48,3% | **+0,5pp** | 25% |
| C3 2018-2022 | 32 | 25,0% | [13-42] | 47,9% | −22,9pp | 19% |
| C4 2022-2026 | 34 | 35,3% | [21-52] | 52,0% | −16,7pp | 20% |

**Efek muncul di 3 dari 4 cycle, hilang total di C2 (+0,5pp).** Tidak ada cycle yang menyumbang >50% event (maks C1 = 36%), jadi hasilnya tidak didominasi satu era — tapi juga tidak konsisten.

## Robustness — event-merged (cooldown 5 hari)

n event = **106** | flip = 34,0% [26-43] | matched baseline = 47,5% | selisih = **−13,5pp**
- DOWN n=51 → flip 43,1%, base 49,2%, selisih −6,1pp
- UP n=55 → flip 25,5%, base 45,9%, selisih **−20,4pp**

Setelah shock berdekatan digabung jadi satu event, efeknya bertahan dan bahkan sedikit menguat. Pemisahan DOWN vs UP juga bertahan.

**Catatan independensi yang wajib dibaca:** window forward 30 hari saling tumpang tindih antar hari shock, jadi CI Wilson di semua tabel di atas **terlalu sempit**. Baca sebagai indikasi arah, bukan uji signifikansi formal.

---

## Kesimpulan

**B-1 cenderung DIDUKUNG di angkanya (36,0% vs 47,5%, selisih −11,6pp, n=139 ≥2013), dan bertahan terhadap dua uji yang paling mungkin membunuhnya** — koreksi at-gate (selisih vs versi naif cuma 0,7pp) dan event-merging (n=106, selisih justru menguat ke −13,5pp). Sebaran per cycle: 61/43/32/34, tidak ada dominasi era, tapi efeknya hilang di C2 (+0,5pp).

**Dua keberatan besar yang harus ikut kemanapun angka ini dipakai:**

1. **Efeknya runtuh di definisi shock kedua.** Ambang fixed 8% memberi selisih −0,5pp. Dua varian dites, satu berhasil — per standar validasi CLAUDE.md itu tanda overfit terhadap definisi, bukan konfirmasi.
2. **Efeknya hampir seluruhnya dari UP-shock (−17,2pp), bukan DOWN-shock (−5,3pp).** Sel yang paling relevan untuk keputusan nyata — shock ke bawah saat trend masih naik (n=27) — selisihnya **−1,8pp, praktis nol.**

**Implikasi praktisnya jadi jauh lebih sempit dari yang disiratkan video.** Bacaan "satu hari merah besar bukan bukti trend berbalik" **tidak** didukung sebagai temuan kuantitatif — sel itu justru yang paling datar. Yang didukung adalah kebalikannya: **satu hari hijau besar di tengah uptrend cenderung bukan puncak** (n=51, 25,5% vs 42,5%) — relevan sebagai peringatan agar tidak menganggap green candle besar sebagai sinyal exit, tapi framework memang tidak pernah memakai candle tunggal sebagai trigger K1, jadi nilai tambahnya rendah.

**Verdict: menarik, tereplikasi, tapi tidak layak jadi input keputusan** — gagal robustness definisi dan efek nyata hanya di sisi yang tidak actionable.
