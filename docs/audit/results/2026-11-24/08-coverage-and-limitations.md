# Kapsam, yöntem ve tamamlanmayan kontroller

Tarih: 24 Kasım 2026. Durumlar: **EXECUTED** gerçek çalıştırma,
**PARTIAL** belirtilen kapsamda çalıştırma, **NOT_RUN** çalıştırılmadı,
**BLOCKED/INTERRUPTED** ortam veya bağlantı nedeniyle bitmedi.

## Ortam ve yeniden üretim

- Depo `/Users/yavuz/prg/dr-cil`; ilk çalışma ağacı ve commit bilgisi
  `evidence/initial-worktree-state.json`, son karşılaştırma
  `evidence/final-preservation.json`.
- Hugo `0.167.0+extended+withdeploy darwin/arm64`, Node `v26.11.0`,
  Python `3.9.6`; Blowfish `7ce8be1d2f7e0cfef792433f4a1b42c0b66090f4`
  (`v2.93.0`). Tema destek aralığı 0.141.0–0.152.2; Netlify0.151.0.
- CUA in-app browser UA Chrome158; yerel kurulu Chrome uygulaması157.
  Kurulu Chrome sürümünü ölçüm tarayıcısı sürümü yerine kullanma.
- Kullanıcının Hugo development sunucusu `127.0.0.1:1313`, başlangıçta
  lsof ile görüldü. Kaynak/çalışan sunucu yeniden başlatılmadı.
- Ayrı üretim build'i aşağıdaki komutla geçti. `public/` veya izlenen
  resources temizlenmedi; `--gc` kullanılmadı.

```sh
cd /Users/yavuz/prg/dr-cil
HUGO_RESOURCEDIR=/tmp/dr-cil-audit-2026-11-24/resources \
HUGO_CACHEDIR=/tmp/dr-cil-audit-2026-11-24/cache \
hugo --environment production --minify \
  --destination /tmp/dr-cil-audit-2026-11-24/public
```

Üretim build log'u `evidence/production-build.log`. Özel tarayıcı/CLI erişim
sınırını aşacak alternatif süreç/bağlantı kullanılmadı. Shell'in hem siteyi
hem google.com/github.com kontrol alanlarını çözememesi genel ortam
kısıtıdır; site DNS bulgusunun kanıtı bu değildir. Ayrı gerçek DNS sonucu
tarayıcıdan Google Public DNS JSON yanıtlarıyla alındı.

## Çalıştırma matrisi

| Kontrol | Durum | Gerçek kapsam / kanıt |
| --- | --- | --- |
| Üretim derlemesi | EXECUTED | Minify edilmiş ayrı çıktı; log ve hash envanteri |
| Tam HTML/URL taraması | EXECUTED | 976 HTML, alias/404/pagination ayrımı; 02 CSV ve static-* |
| İç link/asset/fragment | EXECUTED statik | Canonical alan adı → çıktı haritası; /tr kuralı modellemesi; canlı HTTP testi yerine geçmez |
| Canonical/hreflang/sitemap/metadata | EXECUTED statik | Bütün çıktı; kaynak ve percent-encoding kontrolleri; indeks/GSC kanıtı değil |
| Tam JSON-LD toplama | EXECUTED | 679 script, parse ve hedefli enum/property/graph taraması; tüm Schema.org sözlüğü reasoner'ı değil |
| Resmî Schema.org Validator | PARTIAL | Tek gerçek DEV hizmet kodu, 5691karakter; 1hata/3uyarı; bütün üretim URL'leri değil |
| Google Rich Results Test | PARTIAL | Aynı tek DEV kodu; 3geçerli öğe, LB3isteğe bağlı uyarı; URL crawl veya GSC testi değil |
| Public DNS | PARTIAL | Google resolver: apexA/AAAA/NS, wwwA/CNAME, kontrolgoogle.comA; ikinci bağımsız resolver yok |
| Üretim origin/TLS/redirect/header | NOT_RUN | Alan adında web adres çözümleme engeli; proxy502 gerçek origin durum kodu sayılmadı |
| Menü viewport matrisi | EXECUTED / sınırlı | 320/360/390/430/768/1024/1280/1440/1920; dört masaüstü genişlikte iki satır; kullanıcı ekran görüntüsüyle uyum |
| 852/853/854 sınır noktası | NOT_RUN | 853 gerçek eşik kaynak/derlenmiş CSS ile doğrulandı; tam sınır tarayıcı testi yapılmadı |
| Gerçek native%200 zoom | NOT_RUN | Viewport override gerçek zoom olarak sunulmadı |
| Modal/arama/mobil menü klavye | PARTIAL | 390×844, dizaltı hizmet sayfası; Shift+Tab/Escape/odak ve DOMsemantik gözlemleri |
| Ekran okuyucu, kontrast, dokunma hedefleri | NOT_RUN | Kaynak riskleri raporlandı; WCAG2.2AA geçişi verilmedi |
| Üç dil HTML/RTL | EXECUTED statik | Üç dil ve temsilî içerikler; kök RTL, çeviri/bağlantı/schema bilgileri |
| EN/AR tam görsel/klavye turu | NOT_RUN | Tüm etkileşimler üç dilde tarayıcıda tekrar edilmedi |
| JS-off/CDN-failure/WebGL-failure | NOT_RUN | Kaynak fallback'leri incelendi; kontrollü tarayıcı hatası yapılmadı |
| Altı development tanı koşusu | EXECUTED | 3desktop1280×900 +3dar390×844; cachebypass, throttlingyok, DPR1, örnekleme pencereleri farklı |
| Mobil model scroll tetikleme | EXECUTED | Başlangıç3/3modelyok; scroll sonrası Skypack+GLB+canvas; browser-model-observations.json |
| Desktop başlangıç model yükleme | EXECUTED | 1280×900 koşularında3/3scrollolmadan; kaynak kodun lazy olması ilk yüklemeyi her viewport'ta engellemiyor |
| CPU/GPU/longtask kaynak atfı | NOT_RUN | Gözlenen longtask'lar kaydedildi; modele nedensel olarak atanmadı |
| Model engelli/açık A/B | NOT_RUN | Kontrollü performans karşılaştırması yapılmadı |
| Offscreen/gizli sekme kaynak tasarımı | EXECUTED kaynak | Viewport dışı render durdurması yok; gerçek GPUtrace/karşılaştırma yapılmadı |
| Üretim önizlemesi açılışı | EXECUTED | Kullanıcı ayrı Python1314sunucusunu başlattığını bildirdi; http://127.0.0.1:1314/ gerçek tarayıcıda açıldı |
| ≥3desktop/mobile kontrollü üretim koşusu | INTERRUPTED | Ağ/CPU/önbellek kontrol çağrısında bağlantı kesildi; tamamlanmış sayısal üretim koşusu yok |
| Lighthouse JSON/HTML ve puan | NOT_RUN | Kullanılabilir CLI yok; tarayıcı tanı metrikleri Lighthouse puanı gibi sunulmadı |
| Sıcak tekrar ziyaret profili | NOT_RUN | Development cache-bypass tekrarları sıcak-cache benchmark diye etiketlenmedi |
| CrUX/sahaCWV/GSC/GBP | NOT_RUN | Yetkili bağlantı bulunmadı/veri alınmadı; “sahada veri yok” iddiası yapılmadı |
| SERP/sıralama/arama hacmi | NOT_RUN | Sekiz sorgu içerik/URL niyetiyle eşlendi; konum/hacim uydurulmadı |
| Tıbbi oranların klinik doğruluğu | NOT_RUN | Kaynak/bağlam eksikliği belirlendi; klinik inceleme hekim iş paketi |
| Gerçek form/randevu/mesaj | NOT_RUN | Hiçbir hasta mesajı, form veya randevu gönderilmedi |
| Yeni sunucu staging kabulü | NOT_RUN | Platform/IP bilinmiyor; kaynak taşıma gereksinimleri belgelendi |

## Temsilî URL kapsamı

Tam URL envanteri [02-url-and-template-inventory.csv](02-url-and-template-inventory.csv)
içindedir. Aşağıdaki örnekler hayali URL değildir; üretim çıktısında mevcutlar.

| Aile / örnek | Statik kaynak/çıktı | Gerçek tarayıcı |
| --- | --- | --- |
| `/`, `/en/`, `/ar/` | Tümü | TRana sayfa görünüm, 6devkoşu; productionTRaçılış; EN/AR etkileşim NOT_RUN |
| `/hakkimda/`, `/en/about/`, `/ar/about/` | Biyografi çelişkisi/kaynak+çıktı | NOT_RUN |
| `/iletisim/`, `/en/contact/`, `/ar/contact/` | Form/hours/schema | Gerçek gönderim NOT_RUN |
| `/klinik/`, `/yayinlar/` | Envanter, içerik ve schema | NOT_RUN |
| `/hizmetler/` | Tam çıktı/link/fragment | Sayfa akışının tamamı NOT_RUN |
| `/hizmetler/dizalti-damar-tikanikligi/` | İçerik/schema/payload | Sayfa açıldı; klavye ve JSON-LDcode alımı |
| `/hizmetler/periferik-damar/` | İçerik/schema/payload | NOT_RUN |
| `/en/services/echocardiography/`, `/ar/services/echocardiography/` | Schema ve dil ilişkileri | NOT_RUN |
| `/blog/diyabetik-ayak/`, `/blog/periferik-arter-hastaligi/` | Kaynak, link, iddia/payload | NOT_RUN |
| `/blog/page/2/` ve dil karşılıkları | Canonical/hreflang | Tarayıcı/HTTP NOT_RUN |
| Taxonomy normal sayfaları ve gerçek term arşivleri | 55normal boş sayfa +346URLailesi envanteri | NOT_RUN |
| Eski `/tr/*`, özel404 ve bulunmayan URL'ler | İlan edilmiş kurallar/dosya varlığı | Gerçek hedef sunucu yanıt testi NOT_RUN |

Yalnız bütün HTML'lerin dosya olarak taranmış olması, bütün sayfalarda manuel
UX/erişilebilirlik veya bütün HTTP yanıtlarının çalıştırıldığı anlamına gelmez.

## Eksik kontrolleri tamamlamak için somut adımlar

1. **Öncelikli erişim:** Yetkili DNS zone ve gerçek Netlify/yeni sunucu hedefi
   doğrulansın. İki resolver + TLS/HTTP kabulüyle NET-01 kapansın.
2. **Ölçüm:** Kullanıcının açtığı ayrı 1314 önizlemesi üzerinden bağlantısı
   kararlı bir ölçüm ortamında aynı ağ/CPU/cache profilli ≥3 üretim koşusu
   çalıştırılsın; ham raporlar saklansın. Bu server geliştirme/test içindir,
   canlı üretim sunucusu gereksinimlerini karşılamaz.
3. **Hesap verisi:** Yetkili GSC query/page/device/country ve indeks/sitemap/
   manual-action raporları, GBP'nin mevcut işletme bilgileri ve varsa CrUX
   dönem/kapsamı sağlansın; dış hesaplarda bu tur değişiklik yapılmadı.
4. **Manuel kabul:** %200 zoom, breakpoint852/853/854, üç dil/RTL, screenreader,
   JS-off, CDN/WebGL hatası, form/backend staging testleri tamamlanmalı.

Shell üretim server'ı başlatma girişimi `PermissionError: Operation not
permitted` ile bitti; kullanıcı komutu kendi terminalinde başlatarak önizleme
erişimini sağladı. Son tarayıcı kontrol isteği kullanıcı tarafından
kesildi/bağlantı kaldırıldı. Bu son kontrolün ağ/CPU ayarlarının başarıyla
uygulandığı veya geri sıfırlandığı gözlenmedi; üretim timing sonucu
türetilmedi. Söz konusu yüzey geçici denetim tarayıcısıdır; kullanıcı Chrome
profili, işletim sistemi ağı veya site kaynakları bu testle değiştirilmedi.

## Dosyaların tekrar üretimi ve korunması

Statik, schema, içerik ve performans yardımcıları `evidence/` içinde;
çalışma komutları ilgili raporlarda. Son karşılaştırma başlangıçtaki kaynak
dosya SHA-256 değerlerini yeniden hesaplar; HEAD/staged durumunun dışarıdan
değişmesiyle kaynak byte'larının değişmesi ayrı raporlanır. Bu denetim
uygulama kodu için commit/push/deploy yapmaz.
