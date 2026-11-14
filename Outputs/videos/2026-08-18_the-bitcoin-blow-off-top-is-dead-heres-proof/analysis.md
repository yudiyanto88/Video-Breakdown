# The Bitcoin Blow-Off Top Is Dead (Here's Proof)
**Channel:** On-Chain Mind
**Tanggal video:** 2026-08-18
**Tanggal analisis:** 2026-08-19
**Link:** https://www.youtube.com/watch?v=8nx1juRXRWE

> **Catatan keterbatasan sumber:** stream video gagal di-download (HTTP 403 — YouTube n-challenge / DRM),
> jadi **frame chart tidak tersedia** untuk analisis ini. Seluruh ekstraksi bersumber dari transcript
> caption verbatim. Angka yang hanya muncul di layar (tooltip, sumbu, label chart) tidak tertangkap —
> tapi video ini narasinya menyebut semua angka kuncinya, jadi dampaknya kecil.

**Tidak ada flag STOP.** Tidak satupun insight menyentuh hard constraint LTV sebagai override, dan
video tidak mengusulkan sistem eksekusi pengganti zone-based + K-node (tidak ada trigger, sizing,
maupun exit rule di dalamnya).

---

## Ringkasan

Video 6 menit tanpa satupun indikator on-chain — ini yang pertama untuk On-Chain Mind di index ini.
Seluruh isinya price-multiple diukur dari cycle bottom, dipotong per horizon waktu. Tesisnya: bagian
depan cycle stabil, bagian belakangnya sekarat. Dia menunjukkan multiple 12 bulan pertama nyaris
identik tiga cycle berturut (2.36x / 2.23x / 2.27x), multiple 24 bulan justru naik (4.55x → 6.11x →
6.25x), tapi multiple bottom-ke-peak runtuh order-of-magnitude dua kali (107x → 21x → di bawah 8x).
Konsekuensinya, leg terakhir cycle — window dari bulan ke-24 sampai peak, yang menurutnya konsisten
~11 bulan — kolaps dari 23.7x ke 3.47x ke 1.27x. "Blow-off top klasik sekarang pada dasarnya sudah
hilang untuk selamanya."

Paruh kedua video lebih berguna daripada paruh pertama: dia membongkar angka 2.3x-nya sendiri dan
menunjukkan jalan ke sana sama sekali tidak mulus. 2019 sempat 4x di bulan ke-6 lalu jatuh 45% dan
menutup tahun di 2.2x. 2015 setelah 7 bulan cuma 7% di atas low. 2023 turun 20% dari $31k ke $25k.
Kesimpulan praktisnya: fase berikutnya akan terasa choppy, dan akan ada momen yang terasa seperti
sudah berakhir padahal belum.

Pembicara sendiri menurunkan bobot analisisnya di akhir — dia menempatkannya "in the same camp as the
four-year cycle astrology" `[05:42]`, yang bertegangan dengan judul "Here's Proof".

**Hasil validasi mengubah gambaran ini secara material.** Aritmetika video reproduce bersih (selisih
<5% dari data kami), tapi video **membuang cycle 2011-13 tanpa alasan**, dan cycle itu membunuh tiga
dari empat polanya sekaligus: 12-bulan bukan 2.3x melainkan **5.68x**, 24-bulan bukan ~6x melainkan
**336x**, dan window "11 bulan" hanya **0.4 bulan**. Lebih parah lagi, menggeser tanggal bottom ±45
hari menggoyang multiple 12-bulan sebesar 33-59% — jadi "flat 2.3x" tidak robust bahkan tanpa cycle
2011-13. Yang bertahan dan justru menguat cuma satu: runtuhnya peak multiple, monoton di 4/4 cycle.

---

## Insight Inventory

### [BARU] Front-end cycle multiple stabil ~2.3x di 12 bulan pertama
- **Insight:** Multiple 12 bulan pertama bull market hampir identik tiga cycle: C1 = **2.36x**,
  C2 = **2.23x**, C3 = **2.27x** — "basically the same number of about 2.3x". Pembicara eksplisit
  bilang ini di luar ekspektasinya: di pasar yang katanya maturing, dia mengharap multiple awal ikut
  menyusut. `[00:53]`–`[01:31]`
- **Indikator terkait:** tidak ada indikator on-chain — price multiple dari cycle bottom, anchor 12 bulan
- **Relevan ke:** K5 (kecepatan deploy di awal bull), K6; general
- **Test klaim:** Angkanya replikasi bersih, tapi "remarkably flat" adalah artefak dua hal. Pertama,
  cycle 2011-13 memberi 5.68x — kalau dimasukkan ceritanya jadi "runtuh sekali lalu datar", yaitu
  maturasi biasa, bukan temuan mengejutkan. Kedua, sebaran 2.24–2.41 cuma ~7% sementara tanggal bottom
  adalah parameter bebas yang tidak pernah didefinisikan pembicara — ketatnya angka kemungkinan besar
  hasil derajat kebebasan. **Salah kalau** menggeser tanggal bottom ±45 hari membuat ketiga multiple
  menyebar >±20%, atau cycle ke-4 memberi angka di luar 1.8–2.8x. n = 3 cycle (klaim video).
- **Perlu validasi Claude Code:** Ya — diuji bersama insight multiple lain dalam satu script

**[VALIDASI — 2026-08-19, CLOSED]** GAGAL di dua arah sekaligus. Cycle 2011-13 yang dibuang video
memberi **5.68x** di 12 bulan — 2.5x lipat dari "flat 2.3x", jadi klaimnya "3 dari 4 cycle, dan yang
keempat sangat jauh" (**n = 4**: C0 5.68x, C1 2.41x, C2 2.17x, C3 2.27x). Yang lebih merusak: menggeser
tanggal bottom ±45 hari menggoyang multiple 12-bulan sebesar **55.1% / 58.8% / 33.1% / 36.9%** — keempatnya
di atas ambang robust ±20% yang dipatok di muka. Rentang penuh 0.99x–5.68x (n=20 kombinasi); bahkan kalau
C0 dibuang seperti video, rentangnya 0.99x–2.67x — "flat 2.3x" bisa jadi "tidak naik sama sekali" hanya
dengan menggeser bottom C1 45 hari lebih awal.
Detail: [`findings_cycle_multiple_grid.md`](findings_cycle_multiple_grid.md)

### [BARU] Multiple 24 bulan justru NAIK antar cycle
- **Insight:** Multiple 2 tahun pertama meningkat, bukan menurun: C1 = **4.55x**, C2 = **6.11x**,
  C3 = **6.25x**. "The early part of the cycle is actually holding steady and then the 2-year mark is
  actually getting a touch stronger." `[01:31]`–`[01:55]`
- **Indikator terkait:** price multiple dari cycle bottom, anchor 24 bulan
- **Relevan ke:** K5, K6, K2; general
- **Test klaim:** "Steadily rising" terlalu kuat untuk datanya. C1→C2 lompatan nyata, tapi C2→C3 hanya
  **+5.6%** — di dalam noise tanggal-bottom, bukan tren. Jadi efektif 1 kenaikan + 1 flat, dari sampel
  yang membuang cycle bernilai 336x. Ada juga masalah fase: bulan-24 kebetulan jatuh di Des 2020 (tengah
  melt-up) untuk C2 dan Nov 2024 (spike pasca-pemilu AS) untuk C3 — keselarasan kebetulan, bukan struktur.
  **Salah kalau** sensitivitas ±45 hari menghasilkan urutan C2 > C3. n = 3 cycle.
- **Perlu validasi Claude Code:** Ya — diuji bersama insight multiple lain

**[VALIDASI — 2026-08-19, CLOSED]** GAGAL. Cycle 2011-13 memberi **335.99x** di bulan ke-24 — pola
"naik pelan 4.5 → 6.25x" hanya muncul kalau cycle terbesar dibuang. Sensitivitas tanggal bottom ±45
hari menggoyang multiple 24-bulan sebesar **92.7% / 56.7% / 63.4% / 48.9%** (n = 4 cycle) — semua jauh
di atas ambang ±20%. Rentang C2 sendiri 2.15x–9.53x tergantung pilihan tanggal bottom, yang menelan
seluruh selisih C2-vs-C3 yang jadi dasar klaim.
Detail: [`findings_cycle_multiple_grid.md`](findings_cycle_multiple_grid.md)

### [KONFIRMASI] Peak multiple runtuh order-of-magnitude dua kali berturut
- **Insight:** Multiple bottom→peak: C1 = **107x**, C2 = **21x**, C3 = **just under 8x**. "That's not
  a gentle decline. That's an order of magnitude collapse twice in a row." `[01:55]`–`[02:09]`
- **Indikator terkait:** price multiple bottom→peak
- **Relevan ke:** K1 & K3 (syarat awal "MVRV & aSOPR diminishing di setiap ATH baru"); tema diminishing
  di framework. Sudah ada versi on-chain-nya di `source_index.md` — "Diminishing MVRV peaks tiap cycle
  (n=5)", video On-Chain Mind 2025-01-22
- **Test klaim:** Ini bagian paling kokoh di video — order-of-magnitude, tidak bisa dijelaskan noise
  tanggal bottom. Tapi nilai informasinya rendah karena hampir tautologis: market cap naik ~1000x antar
  cycle, return persentase memang wajib mengecil. Satu falsifier yang masih hidup: angka 7.9x
  mengasumsikan 2025-10-06 adalah peak final cycle ini — kalau kelak ada ATH baru di cycle yang sama,
  8x jadi lantai, bukan hasil akhir. n = 3 (klaim video), n = 4 (validasi kami).
- **Perlu validasi Claude Code:** Tidak sebagai klaim mandiri — sudah established dan versi on-chain-nya
  sudah jadi gate aktif. Tapi ikut terhitung di grid multiple 4-cycle

**[VALIDASI — 2026-08-19, CLOSED]** BENAR, dan **satu-satunya klaim video yang justru menguat** ketika
sampel dilengkapi: **563.9x → 109.5x → 20.6x → 7.9x**, monoton turun di **4/4 cycle** (rasio antar cycle
5.1x / 5.3x / 2.6x). Tidak ada perubahan framework yang diusulkan — versi on-chain-nya sudah terpasang
sebagai syarat awal K1 & K3.
Detail: [`findings_cycle_multiple_grid.md`](findings_cycle_multiple_grid.md)

### [BARU] "Year 3 is where the returns go to die" — leg terakhir kolaps
- **Insight:** Kalau window 24 bulan → peak diisolasi, return leg terakhir: C1 = **23.7x**, C2 = **3.47x**,
  C3 = **1.27x** (total **+27%**). Kesimpulan: "the classic blow-off top is now basically gone for good."
  `[02:34]`–`[03:23]`
- **Indikator terkait:** price multiple segmen 24 bulan → peak
- **Relevan ke:** K1 (nilai menahan posisi sampai puncak vs jual di trigger), K3 (payoff short di leg
  akhir), Z5
- **Test klaim:** Ini **turunan aritmetika murni** dari dua insight sebelumnya (Peak ÷ multiple-24bln:
  107/4.55 = 23.5, 21/6.11 = 3.44, 8/6.25 = 1.28), bukan observasi independen. Menyajikannya sebagai
  temuan ketiga menggandakan kesan bukti padahal n tetap 3 dan observasinya sama persis. Nuansanya:
  karena harga bottom saling coret di rasio Peak/P24, metrik ini justru lebih tahan terhadap kesalahan
  harga bottom. Yang tidak bisa dipertahankan adalah lompatan "gone for good" — itu ekstrapolasi kurva
  peluruhan dari 3 titik. **Salah kalau** cycle berikutnya memberi final leg >2x, atau kalau peak
  2025-10-06 ternyata bukan peak final.
- **Perlu validasi Claude Code:** Ya — diuji bersama insight multiple lain

**[VALIDASI — 2026-08-19, CLOSED]** Return leg akhir memang turun di tiga cycle yang dipakai video
(23.87x → 3.51x → 1.27x, replikasi bersih), tapi **"decay monoton" gagal dengan n = 4**: cycle 2011-13
justru cuma **1.68x** — nilai kedua terendah ada di cycle tertua, jadi kurvanya bukan peluruhan searah.
Premis strukturalnya juga rontok (lihat insight window ~11 bulan di bawah): di C0, jendela 24bln→peak
hanya **0.4 bulan**, jadi "year 3" bahkan tidak ada. Kesimpulan "blow-off gone for good" tidak didukung
sebagai ekstrapolasi; yang didukung hanya diminishing amplitudo.
Detail: [`findings_cycle_multiple_grid.md`](findings_cycle_multiple_grid.md)

### [BARU] Window 24 bulan → cycle peak konsisten ~11 bulan
- **Insight:** Jarak dari titik 24 bulan sampai cycle peak "happens to be roughly 11 months long" di
  ketiga cycle — implikasinya peak jatuh sekitar bulan ke-35 dari bottom. Ini klaim **timing**, terpisah
  dari klaim magnitudo. `[02:34]`–`[02:46]`
- **Indikator terkait:** tidak ada — struktur waktu murni (bulan sejak cycle bottom)
- **Relevan ke:** K1 (kapan Z5/puncak diperkirakan), K4 lantai waktu; general
- **Test klaim:** Sirkular begitu dibongkar: bulan-24 didefinisikan dari bottom, jadi "11 bulan dari
  bulan-24 ke peak" identik dengan "bottom→peak = 35 bulan" — yaitu persis four-year/halving cycle yang
  ditolak pembicara di `[00:27]`. Tegangan internal itu **terkonfirmasi**: ini murni struktur kalender
  dengan titik nol digeser dari halving ke bottom. Datanya ketat (35.1 / 35.0 / 34.5 bulan) tapi cycle
  2011-13 memberi ~24.5 bulan. Tambahan: peak C2 ambigu (Apr 2021 $64.8k vs Nov 2021 $69k) — memilih
  Apr 2021 memberi 28 bulan, pilihan yang tidak dijustifikasi pembicara. n = 3.
- **Perlu validasi Claude Code:** Ya — tapi **dibalik arahnya**. bottom→peak tidak actionable karena
  bottom hanya diketahui ex-post; yang actionable adalah durasi peak→bottom, yang cocok dengan posisi
  pasar sekarang (peak 2025-10-06) dan langsung menyentuh K4 lantai waktu

**[VALIDASI — 2026-08-19, CLOSED]** Klaim asli GAGAL: window 24bln→peak = **0.4 bulan** di cycle
2011-13 (vs 11.1 / 10.8 / 10.5 di tiga cycle lain) — "selalu ~11 bulan" adalah artefak dari tiga cycle
yang kebetulan berdurasi ~35 bulan. Tapi arah sebaliknya berguna: durasi **peak→bottom = 13.5 / 11.9 /
12.4 bulan** (n = 3 cycle utama tertutup, mean 12.6, spread hanya 1.6 bulan), plus outlier era awal 2011
(5.4 bulan) dan cycle berjalan 8.8 bulan per data 2026-07-15. Gate K4 lantai waktu (≥9 bulan sejak peak
DAN close < RP) nyala **0.8–3.4 bulan sebelum bottom aktual di 3/3 cycle utama** — konsisten cepat,
tidak pernah telat, sesuai desain DCA 5%/bulan. Per data terakhir syarat waktu sudah terpenuhi (9.3
bulan) tapi **close < RP belum** ($65.098 vs RP $52.740) — lantai waktu belum aktif.
Detail: [`findings_peak_to_bottom_duration.md`](findings_peak_to_bottom_duration.md)

### [BARU] Gains ter-kompresi ke depan — front end stabil, back end mati
- **Insight:** Sintesis pembicara atas angka-angka di atas: "the gains that used to show right at the
  very end of the cycle in that classic explosive blow-off top are actually compressing forward into the
  earlier part of the cycle instead." Klaimnya bukan sekadar "return mengecil" — melainkan distribusi
  return **bergeser posisi** di dalam cycle. `[02:09]`–`[02:34]`
- **Indikator terkait:** price multiple, distribusi return dalam cycle
- **Relevan ke:** K5 (agresivitas deploy), K6, K1 (bobot exit di puncak); menyentuh asumsi dasar urutan
  siklus penuh
- **Test klaim:** Ini payung naratif atas insight-insight di atas, dan secara aritmetika **terpaksa
  benar** kalau peak multiple runtuh sementara multiple-24bln datar — jadi bukan bukti independen. Uji
  yang benar-benar memisahkan "front-loading nyata" dari "sekadar diminishing" adalah share log-return
  yang dinormalisasi ke panjang cycle masing-masing, dan itu tidak dilakukan video. **Salah kalau**
  waktu-mencapai-50%-log-return tidak mengecil sebagai fraksi panjang cycle. n = 3.
- **Perlu validasi Claude Code:** Ya — prioritas tinggi, ini yang paling berpotensi mengubah perilaku
  (pacing K5/K6)

**[VALIDASI — 2026-08-19, CLOSED]** TIDAK ADA BUKTI front-loading yang konsisten. Share log-return
ternormalisasi (t50 / durasi cycle) urut waktu = **0.66 / 0.83 / 0.66 / 0.43** — **tidak monoton**
(n = 4 cycle). Cycle 2015-17 justru yang paling *back-loaded* (0.83) padahal video memasukkannya ke
kelompok "front-end stabil", dan cycle 2011-13 sama dengan 2019-21 di 0.66. Cycle terakhir memang paling
front-loaded (0.43) tapi itu 1 observasi dari 4. Kesimpulan: yang berubah lintas cycle terutama
**amplitudo** (peak multiple runtuh 4/4), bukan bentuk kurvanya.
Detail: [`findings_cycle_multiple_grid.md`](findings_cycle_multiple_grid.md)

### [KONFIRMASI] Drawdown brutal 20–45% rutin di 12 bulan pertama bull market
- **Insight:** Angka headline 12-bulan yang mulus menyembunyikan drawdown besar. Tiga contoh:
  **2019** — per 26 Juni harga sudah 4x off the bottom, lalu **jatuh 45%** dan menutup tahun di 2.2x;
  **2015** — per 18 Agustus harga $194, cuma **7% di atas low**, sebelumnya sempat $296 di Maret lalu
  memberi balik **34%**; **2023** — puncak ~$31,000 di Juli lalu **drawdown 20%** ke $25,000 per 11
  September. `[03:23]`–`[04:53]`
- **Indikator terkait:** price drawdown, price multiple
- **Relevan ke:** K5 (cap LTV 45%, rasional "koreksi 15–30% yang RUTIN di setiap early bull"), K2
  (staged cut & cut-loss −20%), HARD LIMITS LTV
- **Test klaim:** **Insight dengan dampak framework tertinggi di video ini** — dua dari tiga contoh
  (−34% dan −45%) berada di atas rentang "15–30%" yang tertulis di rasional K5. Tapi ada celah besar
  sebelum ini boleh dipakai menekan cap LTV: drawdown yang dikutip diukur dari high lokal apapun,
  sedangkan K5 (a) baru masuk setelah pullback ≥5% dari high lokal, dan (b) berakhir saat harga cross
  AVIV Upper ≥3 hari. Sangat mungkin spike Jun 2019 sudah di atas AVIV Upper — artinya keruntuhan −45%
  terjadi di wilayah K1/K2, bukan K5, sehingga tidak menguji cap 45% sama sekali. **Menekan framework
  kalau** drawdown ≥30% memang terjadi *di dalam* jendela K5 di ≥2 dari 3 cycle. n = 3 episode.
- **Perlu validasi Claude Code:** Ya — prioritas tertinggi

**[VALIDASI — 2026-08-19, CLOSED]** Klaim benar sebagai deskripsi pengalaman early bull (drawdown
20–45% muncul di 4/4 cycle) tapi **salah alamat — tidak menyentuh cap LTV 45%**. Dari **n = 51 entry K5**
(C0 = 11, C1 = 22, C2 = 3, C3 = 15) hanya **1 (2.0%)** yang drawdown-nya ≥25%, yaitu ambang yang mendorong
LTV dari cap 45% ke 60%. Dua dari tiga episode video jatuh di luar wilayah deploy loan K5: 2015-03-11 di
**Z1b** (K4 wrap-up, spot only — tidak pernah menyentuh LTV) dan 2019-06-26 di **Z5** (zona di mana K1
justru memerintahkan pelunasan loan); yang benar-benar K5 murni (2023-07-13, Z3) berhenti persis di
**−20.0%** — menyentuh cut-loss sadar, bukan LTV-60. Mengembalikan cap ke 52% akan menaikkan frekuensi
wajib-jual dari 2.0% ke **27.5%** (~13x lebih sering), mereplikasi temuan framework sendiri secara
independen. Catatan: hasil didominasi cycle lama — ketiga kejadian ≥20% semuanya dari C0+C1.
Detail: [`findings_k5_early_bull_drawdown.md`](findings_k5_early_bull_drawdown.md)

### [BARU] Angka 6 bulan bisa lebih tinggi dari angka 12 bulan
- **Insight:** Di 2019, multiple bulan ke-6 (4x) **lebih tinggi** dari bulan ke-12 (2.2x). "If you've
  been looking at that 6 month mark thinking that we're in some kind of steady uptrend, then you got
  absolutely hammered on the way down." `[03:35]`–`[03:59]`
- **Indikator terkait:** price multiple, anchor waktu
- **Relevan ke:** K5, K2; general — kritik metodologis terhadap multiple sebagai alat baca posisi cycle
- **Test klaim:** Ironisnya ini **kritik paling tajam di video terhadap video itu sendiri** — kalau
  multiple bergantung pada bulan mana kebetulan kamu mengukur, maka "2.36 / 2.23 / 2.27 remarkably flat"
  di bulan-12 kehilangan makna khusus; bulan-12 tidak istimewa, dia cuma satu titik dari kurva yang
  bergelombang. Praktis tidak bisa salah secara aritmetika, jadi nilainya metodologis, bukan prediktif.
  n = 1 contoh (2019).
- **Perlu validasi Claude Code:** Tidak mandiri — kurva multiple bulanan di validasi grid otomatis
  menampilkan ini

**[VALIDASI — 2026-08-19, CLOSED]** BENAR tapi jarang — **1 dari 4 cycle** pada grid bulanan (C2:
2.65x di bulan 6 vs 2.17x di bulan 12). Catatan penting: angka "4x di bulan ke-6" yang disebut video
adalah **high intramonth** (2019-06-26, $12.830 / $3.281 = 3.91x), bukan titik grid bulan-6 — memakai
high intramonth untuk satu sisi dan close bulanan untuk sisi lain melebih-lebihkan efeknya.
Detail: [`findings_cycle_multiple_grid.md`](findings_cycle_multiple_grid.md)

### [KONFIRMASI] Fase berikutnya akan terasa seperti sudah berakhir padahal belum
- **Insight:** Proyeksi karakter fase berikutnya: "not going to feel like a textbook bull market at all.
  It's going to feel choppy and uncertain, and there will be moments where it genuinely looks like it's
  over, well before it actually is." Ditambah observasi bahwa drawdown seperti itu "would have shaken
  plenty of people out well before the top was actually in." `[04:53]`–`[05:18]`, `[05:36]`
- **Indikator terkait:** tidak ada — karakterisasi kualitatif regime
- **Relevan ke:** alarm bear CEPAT (risiko salah bunyi tipe Mei 2021), K3, K2
- **Test klaim:** Sebagai klaim, tidak falsifiable dalam bentuk yang diucapkan — "akan terasa seperti
  sudah berakhir" tidak punya kondisi yang bisa membuatnya salah. Tapi terjemahan operasionalnya sudah
  dikunci di framework: risiko false positive alarm bear CEPAT tipe Mei 2021, yang di K3 ditulis sebagai
  "risiko yang diterima secara sadar" dengan pengaman syarat awal + K1-selesai + sizing 30%. Framework
  juga sudah memisahkan alarm CEPAT (sengaja sigap, biaya salah bunyi = pause) dari PRESISI (sengaja
  lambat, untuk short). Tidak ada tambahan informasi.
- **Perlu validasi Claude Code:** Tidak — sudah established sebagai trade-off eksplisit

### [STRATEGI] Ambil return di depan cycle, jangan tunggu blow-off
- **Insight:** Implikasi praktis yang dia tarik: "If we can make a 2 to 6x return in the first year or
  two of every bull market, then that's still pretty impressive." Artinya sumber return utama sudah
  pindah ke tahun 1–2, dan menahan posisi menunggu leg terakhir semakin tidak berbayar. `[05:42]`–`[06:07]`
- **Indikator terkait:** price multiple 12 & 24 bulan
- **Relevan ke:** K5 (kecepatan deploy), K6, K1 (kapan mengurangi posisi)
- **Test klaim:** Satu-satunya bagian yang benar-benar actionable, dan juga yang paling berbahaya karena
  asimetri kerugiannya. Kalau kamu de-risk di bulan-24 dan pola peluruhan ternyata tidak berlanjut, kamu
  menyerahkan mayoritas return cycle — di C1 keputusan itu membuang **23.6x**. Kamu bertaruh pada
  ekstrapolasi 3 titik (yang jadi 4 titik non-monoton kalau 2011-13 dimasukkan) dengan payoff kalah jauh
  lebih besar dari payoff menang. Perlu dicatat: framework **sudah** punya front-loading dalam bentuk
  lebih aman — K5 "agresivitas = kecepatan deploy, bukan tinggi LTV", dan K6 mengurangi loan di tiap
  local high selama Z2/Z3 — keduanya mengambil manfaat di depan cycle **tanpa menjual BTC**. Versi
  berbahaya (jual spot di bulan 12–24) tidak didukung; versi amannya sudah terpasang. n = 3.
- **Perlu validasi Claude Code:** Ya — **belum diuji, backlog**. Pertanyaan kalau kelak dijalankan:
  bandingkan tiga kebijakan per cycle atas basis BTC yang sama — (a) hold sampai trigger K1, (b) jual 25%
  di bulan-24 sejak bottom lalu sisanya di trigger K1, (c) jual 25% saat harga pertama mencapai 5x dari
  bottom. Metrik: BTC-equivalent akhir + USDT hasil, diukur di tanggal bottom cycle berikutnya. Catatan
  wajib: (b) dan (c) sama-sama butuh tanggal bottom yang hanya diketahui ex-post → hasilnya batas atas,
  bukan performa yang bisa direalisasikan

### [STRATEGI] Penolakan four-year cycle + self-caveat "astrology camp"
- **Insight:** Dua pernyataan posisi metodologis. Di awal: "this isn't about the four-year cycle theory
  because... I'm not really a fan of leaning on the calendar as some sort of gospel. But what I am
  interested in is patterns in the data and actually measurable behavior across cycles" `[00:27]`. Di
  akhir, dia justru menempatkan analisisnya sendiri: "this type of analysis goes both in the same camp
  as the four-year cycle astrology, but also in another camp that gives me hope that there are some
  serious gains definitely still on the cards here" `[05:42]`.
- **Indikator terkait:** —
- **Relevan ke:** general (bobot epistemik seluruh video)
- **Test klaim:** Pembicara menurunkan bobot analisisnya sendiri, dan itu harus diterima apa adanya —
  bukan sebagai kerendahan hati retoris tapi sebagai batas kepercayaan yang dia tetapkan sendiri.
  Konsekuensinya, kesimpulan terkuat di video ("blow-off top gone for good", `[03:16]`) tidak boleh
  dibaca dengan bobot lebih tinggi daripada yang penulisnya berikan. Inkonsistensi yang perlu dicatat
  tegas: menolak kalender di `[00:27]` lalu membangun seluruh analisis di atas "bulan ke-N sejak bottom"
  dan "peak di bulan ~35" adalah kalender, hanya dengan titik nol digeser dari halving ke bottom. Tidak
  ada yang bisa membuat insight ini "salah" — dia bukan klaim empiris.
- **Perlu validasi Claude Code:** Tidak — meta-komentar epistemik, tidak testable

### [KONFLIK] Cycle diindeks dari bottom pakai hitungan bulan + multiple lintas-cycle
- **Insight:** Seluruh kerangka video mengukur posisi cycle lewat dua hal: (a) jumlah bulan sejak cycle
  bottom (12 / 24 / ~35 bulan), dan (b) multiple harga yang dibandingkan langsung antar cycle (2.3x,
  6.25x, 107x, 21x, 8x). `[00:53]`–`[03:10]`
- **Konflik dengan:** Prinsip utama framework — "threshold absolut tidak reliable antar cycle, framework
  pakai pola relatif" — dan Zone Structure v2 yang memposisikan cycle lewat ordering level (STH RP / RP /
  LTH RP / AVIV) plus posisi harga, bukan lewat kalender atau multiple.
- **Alasan konflik:** Konfliknya perlu **dipertajam, bukan diambil apa adanya**. Ini bukan soal "absolut
  vs relatif" — multiple-dari-bottom sudah dinormalisasi ke bottom, jadi secara teknis relatif, tidak
  sekelas "MVRV > 3.5 = jual". Konflik yang sebenarnya adalah **observabilitas anchor**: level STH RP /
  RP / LTH RP / AVIV bisa dibaca hari ini juga, sedangkan "bulan ke-N sejak bottom" butuh mengetahui
  bottom yang hanya terkonfirmasi berbulan-bulan kemudian. Itu pelanggaran anti-lookahead di level
  **desain**, bukan implementasi — dan itulah kenapa kerangka ini secara permanen tidak bisa naik kelas
  jadi gate, berapa pun bagus hasil backtest-nya. Penyeimbang: framework sendiri sudah punya elemen
  time-anchored yang sah (K4 lantai waktu ≥9 bulan sejak peak, tervalidasi 3/3), jadi "waktu sebagai
  anchor" bukan pelanggaran doktrin per se — yang bermasalah adalah anchor yang tidak observable
  real-time.
- **Rekomendasi:** Diskusikan lebih lanjut dengan Yudi. **Bukan kandidat STOP** — tidak menyentuh hard
  constraint LTV, dan video tidak punya trigger/sizing/exit rule sehingga tidak memenuhi syarat
  "framework fundamental berbeda". Turunkan statusnya jadi **kalibrasi ekspektasi, bukan sinyal**.

---

## Flag Prioritas

1. **Drawdown early-bull vs cap LTV 45%** — satu-satunya insight yang menyentuh hard constraint aktif,
   dan hasilnya bersih: cap 45% cenderung tahan (1 dari 51 entry K5 menembus ambang −25%), dan dua dari
   tiga episode yang dipakai video terjadi di luar wilayah deploy loan. Tapi ada satu konsekuensi teks:
   rasional K5 menulis "koreksi 15–30% yang RUTIN" sementara peak-to-trough di dalam jendela K5 mencapai
   −41.6% (C0) dan −32.5% (C1). Perlu diputuskan apakah kalimat itu diperlebar ke ~15–40%. Penerapannya
   di project Onchain-Dashboard, bukan di sini.

2. **Lubang definisi jendela K5** (temuan sampingan validasi, bukan dari video) — syarat tutup K5 "3 hari
   berturut ≥ AVIV Upper" membuat jendela K5 bisa tetap nominal terbuka saat zona harian sudah Z4/Z5.
   6 dari 51 entry terjadi di Z4, termasuk satu-satunya entry dengan drawdown −38.7% di horizon 180 hari
   (2019-06-27). Kalau jendela K5 juga ditutup begitu harga masuk Z4, entry itu hilang. Worth didiskusikan.

3. **Durasi peak→bottom & posisi sekarang** — hasil validasi paling actionable dari sesi ini, dan bukan
   dari video (arah insight dibalik). Per data 2026-07-15: 9.3 bulan sejak peak, syarat waktu K4 sudah
   terpenuhi tapi close < RP belum ($65.098 vs $52.740). Proyeksi jendela bottom dari 3 cycle utama:
   ~Okt–Nov 2026. **Data master terakhir 2026-07-15 — satu bulan lebih tua dari hari ini; status close
   < RP perlu dicek ulang setelah data di-update.**

4. **Metodologi video: seleksi sampel** — membuang cycle 2011-13 mengubah 3 dari 5 klaim dari "gagal"
   jadi "berhasil", tanpa alasan yang diberikan pembicara. Ini worth diingat sebagai pola untuk sumber
   yang sama ke depan, bukan cuma untuk video ini.

5. **Ambil return di depan cycle (backlog validasi)** — satu-satunya bagian actionable dari video, tapi
   asimetri kerugiannya besar dan versi amannya sudah terpasang di K5/K6. Kalau mau diuji, definisi
   backtest-nya sudah disiapkan di insight terkait.

---

## Yang Langsung Diabaikan

- **Komentar kondisi pasar Agustus 2026** (`[05:54]`–`[06:07]`, "relentless sideways chop") — tanpa
  mekanik on-chain atau angka; cuma konteks tanggal video.
- **Intro/framing** (`[00:14]`–`[00:27]`, "something that's been sat on my charts for a while") — tidak
  ada klaim.
- **Judul "Here's Proof"** — klaim retoris yang dikontradiksi self-caveat pembicara sendiri di `[05:42]`,
  dan tidak bertahan di validasi.
