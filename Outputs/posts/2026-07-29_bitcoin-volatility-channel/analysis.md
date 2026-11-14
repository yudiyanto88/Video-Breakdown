# Bitcoin Volatility Channel
**Sumber/Akun:** Tidak diketahui (chart berwatermark "INVESTE MAIS")
**Tanggal post:** Tidak diketahui — dipakai tanggal analisis 2026-07-29
**Tanggal analisis:** 2026-07-29
**URL:** -

> **Catatan arsip:** Kedua gambar sumber dilampirkan sebagai konten inline di chat, bukan file di disk — tidak ditemukan file fisiknya di sistem untuk disalin sebagai `gambar_1.png`/`gambar_2.png`. Folder ini karena itu tidak sepenuhnya self-contained secara visual; deskripsi gambar lengkap ada di `source.md`. Kalau Yudi punya file gambar asli, taruh manual di folder ini sebagai `gambar_1.png`/`gambar_2.png` untuk melengkapi arsip.

---

## Ringkasan

Post ini memperkenalkan "Bitcoin Volatility Channel" — model band pricing 4-garis (Bitcoin Price, Fair Value, Support, Resistance) dari vendor "INVESTE MAIS". Fair Value diklaim sebagai rata-rata harga pusat (trend indicator), dihitung dari annualized realized volatility (window 365 hari); Support/Resistance adalah band di sekitarnya yang lebarnya mengikuti volatilitas harga itu sendiri, bukan angka dolar tetap. Klaim utama: bottom BTC terbentuk ketika harga trading di dalam band Support (kadang deviasi ke bawah), yang dianggap periode akumulasi yang sangat baik. Dua gambar chart menunjukkan histori penuh 2013-2026 (dengan 4 titik yang di-highlight sebagai contoh) dan zoom 2021-2026 yang menambahkan sinyal cross Price-vs-Fair-Value sebagai penanda perubahan rezim.

Ini adalah indikator murni price-technical — tidak memakai data on-chain sama sekali (bukan realized cap, UTXO age, atau supply distribution), jadi secara struktural berbeda total dari semua level Realized Price family di framework kita. Setelah divalidasi lawan data historis (`data_master_all_metrics.csv`), ketiga klaim yang diuji — bottom signal dari touch Support, regime-change dari cross Fair Value, dan kesesuaian posisi harga saat ini dengan narasi "excellent accumulation" — **semuanya menunjukkan hasil negatif**: base rate reliability rendah, dan posisi harga saat ini justru sedang di zona ZD dengan Veto 1 K2 aktif (bukan sinyal akumulasi resmi).

---

## Insight Inventory

### [INDIKATOR CUSTOM] Bitcoin Volatility Channel (Fair Value / Support / Resistance band)
- **Insight:** Model band pricing 4-garis di mana Fair Value = rata-rata harga pusat (trend), dihitung dari annualized realized volatility (window 365 hari); Support/Resistance = band di atas/bawah Fair Value yang lebarnya mengikuti volatilitas harga sendiri, bukan angka absolut. Komponen dasarnya murni price-derived — mirip filosofi Bollinger/Keltner Channel (centerline = moving average harga, lebar band = fungsi realized volatility) — TIDAK memakai input on-chain apapun.
- **Indikator terkait:** Tidak ada padanan langsung di framework. Secara struktural (band di sekitar centerline) mirip AVIV Mean/Upper yang juga dipakai sebagai band Z4/Z5, tapi basis perhitungan sama sekali berbeda (volatility-of-price vs realized-cap-ratio).
- **Relevan ke:** general
- **Test klaim:** Basis price-only vs on-chain sudah jelas dari deskripsi kualitatif, tidak perlu diuji lawan data. Reproduksi formula eksak Fair Value/Support/Resistance tidak mungkin karena vendor tidak publikasikan matematikanya — apapun rekonstruksi berisiko overfitting ke satu titik data snapshot.
- **Perlu validasi Claude Code:** Tidak — perbedaan basis metodologi sudah jelas tanpa perlu cek data historis.

### [INDIKATOR CUSTOM] Band melebar mengikuti level harga (skala log, bukan lebar absolut)
- **Insight:** Sepanjang histori 2013-2026, lebar band Support-Resistance proporsional terhadap level harga — konsisten dengan band berbasis persentase/volatilitas, bukan lebar dolar tetap.
- **Indikator terkait:** Realized volatility (365-day annualized), diterapkan sebagai band relatif
- **Relevan ke:** general — selaras dengan prinsip framework "threshold absolut tidak reliable antar cycle, pakai pola relatif", meski konstruksinya beda total dan domainnya price-technical bukan on-chain
- **Test klaim:** Ini nyaris tautologi — kalau band memang dihitung dari realized volatility (dalam %/return), maka proporsionalitas terhadap harga otomatis terjadi secara matematis di skala log, bukan temuan empiris independen. Falsifiability rendah: hanya salah kalau ternyata band pakai offset dolar tetap, yang tidak terlihat dari chart.
- **Perlu validasi Claude Code:** Tidak — konsekuensi matematis dari metodologi yang sudah dideskripsikan.

### [STRATEGI] Harga di dalam/di bawah band Support = periode akumulasi bagus (bottom signal)
- **Insight:** Klaim eksplisit teks post: bottom BTC terbentuk ketika harga trading di dalam band Support, kadang deviasi ke bawah, dianggap periode akumulasi excellent. Didukung visual 4 titik historis di Gambar 1 (awal 2014, akhir 2018/awal 2019, ~2019-2020, area 2021-2022 & 2025-2026) yang diikuti pemulihan harga jangka panjang.
- **Indikator terkait:** Bitcoin Volatility Channel (Support band)
- **Relevan ke:** Konseptual bersinggungan dengan tujuan K4 (akumulasi di bear bottom Z1) di framework — tujuan serupa (identifikasi fase akumulasi terbaik), mekanisme total berbeda (price-volatility band vs LTH-MVRV/aSOPR/Supply-in-Profit/Price-CVDD)
- **Test klaim:** Basis cuma 4 titik visual — efektif ~3-4 bottom cycle genuinely terpisah (di bawah ambang 3 cycle, flagged low-confidence). Lebih penting: 4 titik ini dipilih hindsight oleh pembuat chart, chart hanya menampilkan touch Support yang berhasil diikuti pemulihan — pola classic selection bias.
- **Perlu validasi Claude Code:** Ya — direkonstruksi band-nya, dihitung total kejadian sepanjang histori penuh (bukan cuma 4 yang dipilih vendor) dan berapa % benar-benar diikuti reversal.

**[VALIDASI — 2026-07-29, CLOSED]** Rekonstruksi band (kalibrasi post-hoc ke satu snapshot chart) gagal mereproduksi level Fair Value vendor dengan window 365/730 hari (overshoot 28-30%), dan pada config manapun **hanya 0-9,5% kejadian "harga di bawah Support" (n=0-2 dari 2-21 event resolved, didominasi siklus 2022 ~35-50% dari total) diikuti reversal bersih dalam 180 hari** — mayoritas false-start atau belum reversal. Klaim "excellent accumulation" tidak didukung sebagai sinyal bottom reliable pada horizon 180 hari; 4 titik yang di-highlight vendor tampak hindsight-picked dari 18-26 kejadian mekanis yang jauh lebih banyak.
Detail: [`findings_volatility_channel_support_bottom.md`](findings_volatility_channel_support_bottom.md)

### [STRATEGI] / [INDIKATOR CUSTOM] Cross Price vs Fair Value sebagai penanda perubahan rezim
- **Insight:** Pola cross Price menembus Fair Value dipakai sebagai sinyal regime-change: cross-down muncul di leg turun bear 2022 dan penurunan 2025-2026; cross-up muncul di awal pemulihan 2023 dan sekali lagi di titik paling kanan chart (2026, terkini) — dibaca pembuat chart sebagai sinyal pemulihan sedang terbentuk.
- **Indikator terkait:** Bitcoin Volatility Channel (garis Fair Value, cross event)
- **Relevan ke:** Konseptual mirip fungsi cross-signal yang sudah ada di framework (STH RP cross RP untuk Z1→Z2, MVRV Momentum bearish/bullish cross K2/K3) — pola "cross level trend sebagai regime marker" sudah dipakai, tapi levelnya (Fair Value volatility-based) berbeda dari level on-chain manapun
- **Test klaim:** Basis cuma 2 contoh cross-down dan 2 cross-up (n sangat kecil, flagged low-confidence). Cross-up di titik paling kanan chart (2026, saat ini) rawan bias — observasi real-time tanpa horizon konfirmasi.
- **Perlu validasi Claude Code:** Ya — dihitung total cross sepanjang histori penuh pakai proxy centerline yang sudah ada (true_market_mean_price/200_wma), berapa % whipsaw vs genuine regime change, dan dibandingkan dengan trigger K-node established.

**[VALIDASI — 2026-07-29, CLOSED]** Cross Price vs proxy Fair Value (true_market_mean_price/200_wma) mayoritas whipsaw (72-81% dari n=104/69 cross sepanjang histori penuh, reversed ≤30 hari) — bukan penanda regime-change yang reliable. Hanya 10-11% (n=11/104, n=7/69) bertahan >90 hari sebagai genuine regime change, dan dari situ cuma 0-18% (n=2/11, n=0/7) berdekatan ±30 hari dengan trigger K-node established — jadi tidak largely redundant, tapi base rate whipsaw tinggi membuat sinyal ini sulit diandalkan real-time. Sebaran didominasi siklus 2013-15 (39-45% dari total n) — independensi sample lemah.
Detail: [`findings_volatility_channel_fair_value_cross.md`](findings_volatility_channel_fair_value_cross.md)

### [KONFIRMASI] Posisi harga terkini (dekat/dalam band Support) dibaca sebagai sinyal potensi bottom sedang terbentuk
- **Insight:** Snapshot terkini (2025-2026) menunjukkan Price ($64.491-64.625, low confidence dari resolusi gambar) berada dekat/di dalam band Support ($53.678), dengan panah hijau-naik terbaru di ujung kanan Gambar 2 — pembuat chart membacanya sebagai indikasi pemulihan sedang terbentuk.
- **Indikator terkait:** Bitcoin Volatility Channel
- **Relevan ke:** general — arah kesimpulan ("area harga sekarang dekat level akumulasi") searah dengan pembacaan zona bear/dip di framework, meski via mekanisme berbeda; belum tentu align posisi presisinya dengan Z1/ZC/ZD framework
- **Test klaim:** Perlu dibandingkan langsung dengan zona resmi framework di tanggal yang sama, dan status veto/gate K-node aktif saat ini.
- **Perlu validasi Claude Code:** Ya — bandingkan posisi harga terkini dengan zona resmi & status veto K-node framework.

**[VALIDASI — 2026-07-29, CLOSED]** Per data terbaru (2026-07-15, btc_price≈$65.098, cocok dengan OCR chart vendor ±0,7-0,9%), zona resmi framework adalah **ZD (Dip Dalam)** — bukan ZC/Z1 capitulation seperti tersirat narasi vendor "excellent accumulation". Best-effort reconstruction alarm bear cepat menunjukkan pool 2/4 sinyal aktif (BUNYI, flagged low-confidence), sehingga aksi resmi zona ZD adalah TUNGGU; terlepas dari itu, **K2 Veto 1 resmi (Supply in Profit 56,88% ≤60%) TRIGGERED**, yang secara eksplisit melarang entry K2 apapun kata gate lain. Klaim vendor "bottom forming, excellent accumulation" tidak align dengan bacaan framework resmi saat ini.
Detail: [`findings_current_position_vs_zone.md`](findings_current_position_vs_zone.md)

---

## Flag Prioritas

1. **Klaim "posisi harga saat ini = excellent accumulation" bertentangan dengan bacaan zona resmi framework (ZD, bukan capitulation) dan Veto 1 K2 yang sedang aktif** — ini yang paling penting didiskusikan karena langsung menyentuh keputusan aksi saat ini. Kalau ada yang mengikuti narasi vendor untuk mulai akumulasi sekarang, itu bertentangan dengan hard gate resmi (Supply in Profit 56,88% ≤60%).
2. **Base rate reliability band Support sebagai bottom signal sangat rendah (0-9,5% clean reversal)** — worth dicatat sebagai contoh nyata selection bias/hindsight di chart vendor pihak ketiga, relevan untuk kalibrasi seberapa skeptis terhadap klaim visual serupa dari sumber lain ke depannya.
3. **Cross Fair Value tidak redundant dengan K-node existing (overlap 0-18%)** — meski base rate whipsaw tinggi bikin sinyal ini kurang actionable sendirian, konsep "price cross centerline volatility-based" mungkin worth dieksplorasi lebih jauh sebagai confirming filter tambahan non-on-chain, kalau ada waktu riset lanjutan (bukan prioritas mendesak).

---

## Yang Langsung Diabaikan

- Reproduksi formula eksak "Fair Value"/annualized realized volatility 365-day vendor — tidak dipublikasikan, dan rekonstruksi post-hoc terbukti tidak match level snapshot chart pada window yang sesuai deskripsi (overshoot 28-30%). Tidak ada nilai tambah untuk terus mengejar replikasi eksak formula pihak ketiga yang tertutup.
- Watermark/branding "INVESTE MAIS" — tidak relevan secara analitis, sekadar identitas vendor chart.
