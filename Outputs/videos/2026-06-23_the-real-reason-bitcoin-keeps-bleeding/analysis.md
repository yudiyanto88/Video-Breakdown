# The Real Reason Bitcoin Keeps Bleeding
**Channel:** On-Chain Mind
**Tanggal video:** 2026-06-23
**Tanggal analisis:** 2026-07-13
**Link:** https://www.youtube.com/watch?v=CH76_nDAXFU

---

## Ringkasan

Video ~12 menit yang membedah kenapa harga BTC terus turun meski Saylor/MSTR terus membeli. Seluruh analisis dibangun dari satu fondasi: Realized Cap (saat ini ~$1.07T) dan turunannya. Empat blok utama: (1) Realized Capital Flow — outflow harian turun dari ~$1B/hari ke ~$94M/hari (rata-rata 30 hari ~$500M/hari), dibaca sebagai deselerasi menuju selling exhaustion; (2) dua indikator custom — "Flow Momentum" (MA30 vs MA90 dari flow) dan "Capital Bleeding" (30-day % change realized cap) yang dipromosikan sebagai sinyal DCA "yang tidak akan pernah redundant"; (3) dekomposisi cohort — STH menyumbang ~78% negative flow (STH -$12.5B vs LTH -$4.5B sebulan terakhir), dibaca sebagai pasar tanpa "structural guidance"; (4) institutional flows — ~30% gross capital flow kini dari institusi, ETF outflow $3.75B menjelaskan ~¼ dari penurunan realized cap $14B sebulan → klaim "sell-off pertama yang institutionally-led". Kesimpulan pembicara: bukan bottom call, tapi kondisi sekarang ("second largest capital bleeding event of this bear", -1.3%/bulan) adalah environment terbaik untuk disciplined DCA.

Empat klaim actionable-nya sudah diuji lawan data historis dashboard — hasilnya jauh lebih dingin dari narasi video: Capital Bleeding PARTIAL (fenomenanya nyata, klaim "potent signal right now" tidak didukung), deselerasi outflow REJECT (lebih jelek dari base rate), Flow Momentum REJECT (redundan total dengan `net_realized_pl_usd` + early entry -70% historis), dan dominasi STH 78% REJECT (properti mekanis metrik, bukan anomali).

---

## Insight Inventory

### [KONFIRMASI] Realized Cap sebagai ukuran capital riil, lebih superior dari Market Cap
- **Insight:** Realized Cap menilai setiap coin di harga saat terakhir bergerak on-chain = total cost basis seluruh network (~$1.07T sekarang). Lebih powerful dari market cap (harga terakhir × supply). [00:46]
- **Indikator terkait:** Realized Cap — dasar seluruh Realized Price family (RP, STH RP, LTH RP) di framework
- **Relevan ke:** General — fondasi zone structure Z1–Z5
- **Test klaim:** Definisional, bukan empiris — sudah jadi fondasi framework. Satu catatan: "incorruptible metric" adalah overstatement; realized cap tetap punya distorsi (internal transfer exchange/custodian, reshuffling wallet ETF), meski kecil di level agregat.
- **Perlu validasi Claude Code:** Tidak — sudah established.

### [KONFIRMASI] On-chain cost basis > exchange volume untuk ukur demand riil
- **Insight:** Exchange volume terdistorsi HFT, wash trading, leverage; realized cap hanya menghitung coin yang benar-benar bergerak on-chain. [02:00]
- **Indikator terkait:** Realized Cap vs exchange volume
- **Relevan ke:** General — konsisten dengan pilihan framework yang full on-chain
- **Test klaim:** Argumen metodologis yang masuk akal tapi murni naratif — tidak ada aksi yang berubah karenanya.
- **Perlu validasi Claude Code:** Tidak — tidak actionable.

### [BARU] Deselerasi outflow realized cap sebagai sinyal selling exhaustion / precondition local floor
- **Insight:** Outflow harian turun dari ~$1B/hari ke ~$94M/hari (MA30 ~$500M/hari). Klaim kunci: "exhaustion of selling is almost always the precondition for at least a local floor". [02:31], [10:06]
- **Indikator terkait:** Realized Capital Flow (delta harian realized cap)
- **Relevan ke:** K4 (timing akumulasi) / Z1
- **Test klaim:** Risiko tautologi tinggi — outflow realized cap secara mekanis adalah realized losses, yang menyusut setiap kali harga berhenti turun; arah "necessary" hampir trivial, yang berguna adalah arah "sufficient" (deselerasi → floor). Sample ~4 bear cycle, cukup. Precedent buruk: sinyal deceleration serupa (Apparent Demand) sudah dua kali REJECT.
- **Perlu validasi Claude Code:** Ya — hit rate deceleration event → local floor di bear 2014-15/2018-19/2022, false positive pre-crash, dan overlap dengan aSOPR recovery.

**[VALIDASI — 2026-07-13, CLOSED]** Verdict: **REJECT**. Hit rate deceleration event → local floor (hold 60d) cuma 43–50% (n=21–25 event, robust di threshold 30/50/70%), LEBIH RENDAH dari base rate 60% hari acak di dalam rezim outflow yang sama; 8/21 false positive keras termasuk persis pre-November-crash 2018 dan pre-Juni 2022, median drawdown tambahan 180d setelah event -37.4%. Event juga koinsiden dengan aSOPR MA7 balik ≥0.99 (median lag 2 hari, 17/21 dalam ±14 hari) — tidak ada info baru vs yang sudah dipantau framework (K4 kondisi 2 family). Konsisten dengan precedent REJECT Apparent Demand deceleration. Catatan: angka "$94M/hari" di video kemungkinan snapshot delta harian (noisy), bukan MA30 — MA30 di tanggal video masih -$489M/hari. Detail: [`findings_outflow_deceleration_local_floor.md`](findings_outflow_deceleration_local_floor.md).

### [BARU] Dekomposisi realized cap flow per cohort: STH mendominasi 78% outflow
- **Insight:** STH menyumbang ~78% negative realized capital flow; band terbesar cohort 1–3 bulan (~$64M/hari). Sebulan terakhir STH -$12.5B vs LTH -$4.5B (~3x). Interpretasi: new entrants churning supply antar mereka sendiri, conviction holders dormant → pasar tanpa "structural guidance", tetap choppy sampai conviction capital kembali. [06:12]
- **Indikator terkait:** Realized cap flow per cohort (STH/LTH); bersinggungan dengan Supply in Profit/Loss STH/LTH
- **Relevan ke:** General / konteks K4
- **Test klaim:** Titik lemah utama: dominasi STH pada flow bisa mekanis, bukan informatif — coin yang baru bergerak otomatis jadi STH, jadi STH by construction selalu mendominasi realized flow. Angka 78% baru berarti kalau anomali vs baseline historis. Bagian "conviction dormant → belum bottom" sebagian sudah dicover K4 kondisi 2 (menunggu LTH capitulation via LTH-SOPR) dengan sinyal lebih spesifik. "Choppy sampai conviction kembali" tidak falsifiable sebagaimana dirumuskan.
- **Perlu validasi Claude Code:** Ya — apakah share STH 78% anomali atau nilai normal historis (persentil), dan apakah lonjakan share LTH flow mendahului bottom dengan timing berbeda dari LTH-SOPR < 0.50 yang sudah dipakai K4.

**[VALIDASI — 2026-07-13, CLOSED]** Verdict: **REJECT**. Kecurigaan mekanis terkonfirmasi: dominasi STH atas negative realized cap flow adalah kondisi default metrik — median historis 88.5% (band-level) s/d 100% (net cohort delta; LTH RC 30d biasanya justru POSITIF karena maturation inflow), reading tanggal video di persentil 37–52 alias normal, bukan anomali (n=1.589 hari outflow, 5 cycle). Kenaikan LTH share juga tidak informatif untuk bottom timing: first-hit ≥40% di 3 bear historis = +87/+23/+2 hari sebelum bottom (**n=3**, tidak konsisten), koinsiden dengan LTH-SOPR < 0.50 di 2 cycle dan premature -54% di cycle satunya — tidak ada info baru di atas K4. Yang terverifikasi cuma total flow: -$14.68B/30d per 2026-06-23 vs klaim "$14B"; split -12.5B/-4.5B dan "band 1-3m terbesar $64M/hari" tidak tereplikasi (data kita: band terbesar 3m-6m, -$812M/hari). Detail: [`findings_sth_share_of_flow.md`](findings_sth_share_of_flow.md).

### [BARU] Institutional flows ~30% dari gross capital flow — dinamika baru pertama kali
- **Insight:** ~30% gross capital flow saat ini dari institusi (spot ETF + MSTR) — belum pernah terjadi. Sub-klaim penting: sejak launch 2024, ETF flows secara historis TIDAK menutupi/mendistorsi on-chain data ("completely dwarfed by on-chain capital flows"); MSTR juga bukan driving force — itulah kenapa pembelian $1B Saylor tidak menggerakkan harga. [07:34]
- **Indikator terkait:** Realized Capital Flows + overlay Spot ETF flows & MSTR flows
- **Relevan ke:** General — framework tidak punya komponen institutional flow
- **Test klaim:** Fenomena satu cycle by construction (ETF baru ada sejak 2024) → **low-confidence otomatis**, tidak bisa diuji lintas cycle. Sub-klaim "ETF tidak mendistorsi on-chain data" relevan untuk kredibilitas seluruh Realized Cap family, tapi data ETF/MSTR flows tidak ada di dashboard. Narasi institutional demand juga sudah pernah muncul di video 2025-01-22 dan diputus tidak actionable.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia (ETF/MSTR flows tidak ada di dataset). Murni naratif untuk saat ini.

### [BARU] ETF outflows menjelaskan ¼ penurunan realized cap bulanan — "sell-off led by institutions"
- **Insight:** 30 hari terakhir: spot ETF offload ~$3.75B vs total realized cap turun ~$14B → ~25% sell-off "dijelaskan" ETF flows. MSTR +$232M, tidak cukup menahan bleeding. "The so-called diamond hands might be no more." [09:01], [10:32]
- **Indikator terkait:** Spot ETF flows vs 30-day realized cap change
- **Relevan ke:** General
- **Test klaim:** Dua masalah serius. (1) Aritmetika apples-to-oranges: ETF outflow adalah redemption pada harga pasar, penurunan realized cap adalah repricing coin ke cost basis lebih rendah — membagi $3.75B/$14B mencampur dua satuan akuntansi berbeda. (2) Kontradiksi internal dengan insight cohort: kalau STH menyumbang 78% negative flow, maka "sell-off led by institutions" dengan kontribusi ~25% adalah overstatement. Satu cycle → low-confidence.
- **Perlu validasi Claude Code:** Tidak — data tidak tersedia, dan metodologinya sendiri cacat sehingga tidak layak dikejar meski datanya ada.

### [INDIKATOR CUSTOM] Flow Momentum (MA30 vs MA90 realized capital flow)
- **Insight:** MA30 vs MA90 dari delta harian realized cap. Positif & accelerating = tren robust tapi locally overheated; negatif/merah = structural demand melemah → "opportunity to start scaling in". Reading saat video: "averagely weak". [03:05]
- **Komponen dasar:** Rate-of-change realized cap + struktur MA gap — analog gap MA90–MA60 STH-SOPR (K1/K3) tapi diterapkan di sisi bottom; delta realized cap ≈ net realized P/L + issuance
- **Indikator terkait:** Realized Cap, `net_realized_pl_usd`
- **Relevan ke:** Kandidat pembanding sinyal momentum K1/K3 atau timing entry
- **Test klaim:** Bukan threshold absolut (bagus), tapi "negatif = mulai scaling in" rawan early entry — momentum bisa negatif berbulan-bulan sebelum bottom; reading pembicara sendiri ("make of that what you will") menunjukkan sinyal tidak tegas. Perlu cek redundansi vs Capital Bleeding dan vs `net_realized_pl_usd`.
- **Perlu validasi Claude Code:** Ya — korelasi dengan Capital Bleeding & `net_realized_pl_usd`, dan drawdown setelah first-cross di 3 bear historis.

**[VALIDASI — 2026-07-13, CLOSED]** Verdict: **REJECT** (sebagai sinyal entry) + redundan. Flow Momentum praktis identik dengan MA30 `net_realized_pl_usd` yang sudah ada di data (Pearson 0.9996–0.9999 di semua cycle) — bukan metrik baru. Sebagai trigger "scaling in": first cross MA30<MA90 setelah top di 3 bear lengkap selalu disusul drawdown tambahan -70.7% s/d -76.9% selama 335–382 hari sampai bottom; bear sekarang sudah -47.2% setelah cross Okt 2025 ($110.810 → low $58.460). Korelasi dengan Capital Bleeding 0.805 — bukan duplikat persis, tapi satu keluarga. Detail: [`findings_flow_momentum.md`](findings_flow_momentum.md).

### [INDIKATOR CUSTOM] Capital Bleeding (30-day % change Realized Cap) sebagai sinyal DCA
- **Insight:** 30-day % change realized cap negatif = net capital keluar network. Makin panjang streak merah → makin discounted → sinyal menaikkan jumlah DCA saat downturn. Klaim durability: "will never become redundant" karena first-principles accounting dari settled dollars. Streak historis: 2014, 2015, 2018–19, 2022, sekarang. [03:46]
- **Komponen dasar:** Murni rate-of-change 30 hari Realized Cap — normalisasi persentase dari derivative yang sama dengan Flow Momentum
- **Indikator terkait:** Realized Cap
- **Relevan ke:** K4 / Z1 (kandidat sinyal tambahan scaling DCA)
- **Test klaim:** Sample ≥4 bear, lolos syarat 3 cycle; sign-based + relative, bukan threshold absolut. TAPI klaim "never become redundant" harus ditolak sebagai prinsip: akuntansinya first-principles, makna sinyalnya tidak kebal perubahan struktur pasar — ironisnya video ini sendiri membuktikannya (institusi kini 30% flow = struktur flow sudah berubah). Falsifiability yang benar: apakah DCA saat bleeding mengalahkan baseline DCA berbasis price drawdown — kalau cuma proxy "harga lagi turun", tidak menambah apa-apa.
- **Perlu validasi Claude Code:** Ya — prioritas #1: alpha vs baseline drawdown, monotonicity panjang streak, overlap dengan K4 confidence count.

**[VALIDASI — 2026-07-13, CLOSED]** Verdict: **PARTIAL**. Deskriptif benar (n=18 episode lintas 5 cycle; streak makin panjang → forward return makin baik, Spearman +0.39 di 180d; bucket run ≥100 hari: fwd365 100% positif tapi efektifnya cuma ~4 episode independen). Klaim actionable gagal: semua hari bleeding adalah subset dari drawdown ≥20% ATH dan median return-nya justru lebih rendah (fwd180 +28.5% vs +39.3% DD20 vs +42.7% DD20-tanpa-bleeding) — tidak ada alpha di atas filter drawdown sederhana. BLEED mengalahkan DCA uniform hanya di 2 cycle terakhir (di C2 kalah telak: -27.5% vs +91%) — hati-hati recency bias. Bukan redundan K4 (fire 7–9 bulan lebih awal, overlap K4≥2 cuma 11.8%; sebaliknya 98% hari K4≥2 juga bleeding) tapi terlalu kasar untuk timing — posisi yang bisa dipertahankan: konteks rezim bear-bottom multi-bulan, bukan sinyal. Detail: [`findings_capital_bleeding_dca.md`](findings_capital_bleeding_dca.md).

### [INDIKATOR CUSTOM] Reading Capital Bleeding saat ini: event terbesar kedua bear market ini
- **Insight:** Realized cap turun ~1.3%/bulan = capital bleeding event terbesar kedua bear market ini → "potent local DCA signal flashing right now". [05:53], [11:09]
- **Komponen dasar:** Sama dengan Capital Bleeding di atas — ini reading aktualnya
- **Indikator terkait:** Capital Bleeding
- **Relevan ke:** K4 / kondisi pasar Juni 2026
- **Test klaim:** Bentuk klaim sehat (relatif intra-cycle), tapi -1.3%/bulan perlu dikalibrasi lintas cycle — bleeding 2018/2022 kemungkinan jauh lebih dalam. Klaim salah kalau reading ini ternyata persentil biasa yang historis masih diikuti bleeding lebih dalam.
- **Perlu validasi Claude Code:** Ya — dilebur ke tes Capital Bleeding.

**[VALIDASI — 2026-07-13, CLOSED]** Verdict: **NOT-SUPPORTED**. Reading -1.35%/bulan ada di **persentil 48** dari semua hari negatif historis — persis median, bukan ekstrem. Di bear 2014/2018/2022, saat level ini pertama kali tercapai, cycle bottom masih **-50.4% / -57.0% / -55.1%** lebih rendah (103/311/303 hari kemudian), dan bleeding masih memburuk ke -4.3% / -6.3% / -5.7%. "Terbesar kedua bear ini" benar tapi trivial: bear 2025-26 baru punya 2 episode (min -2.60% di 2026-02-18; episode berjalan sejak 23 Mei 2026, min -1.62% di 2026-06-30) — dengan n=2 otomatis "terbesar kedua". Detail: [`findings_capital_bleeding_dca.md`](findings_capital_bleeding_dca.md).

### [STRATEGI] Disciplined DCA saat network di-markdown, tanpa bottom-calling
- **Insight:** Pembicara eksplisit tidak memanggil bottom ("nobody's actually defending the spot price"), tapi kondisi "no one wants to buy + network marked down in real dollar terms" = environment terbaik untuk disciplined DCA; capital bleeding streaks dipakai untuk menaikkan jumlah DCA, bukan timing entry sekali-jalan. [11:09]
- **Indikator terkait:** Capital Bleeding, Flow Momentum
- **Relevan ke:** Selaras filosofi K4 (akumulasi bertahap, agresivitas diatur kondisi terukur) — bukan framework fundamentally berbeda, flag STOP tidak terpicu
- **Test klaim:** Perbedaan operasional saja: K4 pakai 4 kondisi terukur (LTH-MVRV, aSOPR/LTH-SOPR, Supply in Profit, Price/CVDD), pembicara pakai bleeding streak. Pertanyaan "apakah bleeding layak jadi input K4" sudah terjawab di validasi Capital Bleeding: tidak, cukup sebagai konteks.
- **Perlu validasi Claude Code:** Tidak — komponen actionable-nya tercakup validasi Capital Bleeding.

---

## Flag Prioritas

1. **Capital Bleeding — verdict PARTIAL dengan temuan menarik soal posisi vs K4** — indikator ini fire 7–9 bulan LEBIH AWAL dari K4≥2 dan 98% hari K4≥2 berada di dalam bleeding streak. Artinya dia bisa berfungsi sebagai "pintu masuk rezim akumulasi" (context layer) sementara K4 tetap jadi filter presisi. Worth didiskusikan: apakah mau dicatat formal sebagai context note di K4, atau cukup diarsipkan di findings.
2. **Reading video "potent DCA signal right now" vs hasil uji** — video menyarankan menaikkan DCA sekarang; data bilang reading -1.35% itu median historis, dan di 3 bear sebelumnya level ini pertama tercapai saat bottom masih 50–57% lebih rendah. Relevan langsung untuk keputusan akumulasi Yudi di kondisi pasar saat ini.
3. **Deselerasi outflow REJECT — pola berulang "deceleration signal" gagal** — ini kali ketiga sinyal deselerasi flow gagal diuji (setelah 2x Apparent Demand). Worth dijadikan prinsip eksplisit di project: klaim "slowing = exhaustion = floor" dari channel manapun default-nya skeptis.
4. **Status kapitulasi LTH bear ini (temuan sampingan validasi B-2)** — LTH-SOPR belum pernah < 0.50 bear ini (min 0.623 per 2026-06-30), dan lensa LTH-share-of-flow konvergen ke kesimpulan sama: kapitulasi LTH gaya 2015/2018/2022 belum terjadi. Konsisten dengan status K4 saat ini — data point relevan untuk keputusan akumulasi.

---

## Yang Langsung Diabaikan

- **ETF ¼ sell-off & "diamond hands might be no more"** — aritmetika mencampur satuan akuntansi berbeda (redemption at market price vs repricing cost basis), kontradiktif dengan data cohort-nya sendiri (STH 78% vs institusi 25%), satu cycle, data tidak tersedia di dashboard.
- **Institutional flows 30% sebagai dinamika baru** — menarik sebagai narasi, tapi satu cycle by construction dan tidak ada data ETF/MSTR di dashboard; narasi serupa dari video 2025-01-22 juga sudah diputus tidak actionable.
- **Klaim durability "will never become redundant"** — ditolak sebagai prinsip; tidak ada indikator yang kebal perubahan struktur pasar, dan video ini sendiri mendokumentasikan perubahan struktur flow (institusi 30%).
- **Promosi onchainmind.io / 7-day free trial** — sponsor.
- **Hook Saylor di pembuka** — retorika; substansinya sudah tercakup di insight institutional flows.
