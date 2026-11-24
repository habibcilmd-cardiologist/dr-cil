# Kaynak değişiklikleri ve doğrulama — 24 Kasım 2026

Yerel uygulama tamamlandı; bütün başlangıç bulguları durum matrisine bağlandı.
Çalışmayan gerçek browser/production testleri ve klinik/dış veri bağımlılıkları
açık tutuldu. DNS, hesap, gerçek mesaj/randevu ve deploy yapılmadı; commit/push yok.

## Somut değişiklikler

- Menü alanı/breakpoint/nowrap ve mevcut başlık tercihi; gerçek düğmeler,
  ortak modal odak/inert/Escape, üç dil metinler, AR404, JS fallback.
- Mevcut URL'lerde hedef sayfa metadata ve rehber↔hizmet↔hekim bağlantıları.
  Sekiz sorgu CSV'de ayrı niyetle eşlenir; yeni benzer keyword sayfası yok.
- 45 kaynakta98 eski/bozuk link; EN home fragment;13 emekli home/sitemap
  kuralı +4 doğrudan /tr/page istisnası.12 home duplicate/alias route retire edilir;
  eski canonical içerikler korunur. Gerçek HTTP301 testi yapılmadı.
- Gerçek pagination self-canonical/title/OG; kanıtlanmış eşdeğerlik olmayan
  sayfa2+ hreflang omit; normal çevirilerin self/return bağlantıları korunur.
- Üç açık dil sitemap'i ve robots, tek sahiplik;53 kesin arşiv eşleşmesinde
  gerçek içerik bağlantıları;2 belirsiz manuel sayfaya tahmin uygulanmadı.
- Tek schema graph/breadcrumb, doğru amaç türleri, gerçek image; yanlış
  performer/enum/anatomi/status ve otomatik review/kurum/saat iddiaları kaldırıldı.
- 3B anatomik poster + kullanıcı isteği, tek frame zinciri, offscreen/hidden
  duruş, reduced-motion/Pause ve hata/Retry; eski shortcode konsolide edildi.
  Hero intrinsic boyut/srcset/sizes; gerçek iletişim href'i.
- Provider seçilene kadar iletişim formu render edilmez; telefon/WhatsApp
  bağlantıları vardır.8 sağlayıcı/URL senaryosu×3 dil Hugo fixture'ında geçti.
  Üç bağımsız teşekkür URL noindex/search/sitemap dışı; teslim iddiası üretmez.
- Güvenli build aracı boş/yeni hedef ister, kaynak public/resources'u temizlemez.
  Test edilen Hugo0.167.0 yerel/Netlify kaynak tanımında pinlendi; tema sürümü
  korunur. Theme destek aralığı/deprecation uyarıları devam eder.

## Önce / sonra — statik çıktı

| Ölçüm | Başlangıç | Nihai | Kanıt |
| --- | ---: | ---: | --- |
| Kaynak Markdown | 364 | 364 | source manifest |
| Alias HTML | 297 | 294 | static-before/after |
| Özel404 HTML | 3 | 3 | static-before/after |
| Pagination HTML | 24 | 15 | static-before/after |
| HTML dosyası | 976 | 967 | static-before/after |
| Alias/404 dışı route | 676 | 670 | static-before/after |
| Ayrı canonical | 652 | 670 | static-before/after |
| Statik noindex | 0 | 3 | static-before/after |
| Ham eksik link kullanımı | 98 | 0 | static-before/after |
| Eksik HTML asset | 0 | 0 | static-before/after |
| Eksik fragment | 4 | 0 | static-before/after |
| Canonical sorunu | 24 | 0 | static-before/after |
| Hreflang sorunu | 72 | 0 | static-before/after |
| Statik orphan adayı | 62 | 53 | static-before/after |

Başlangıç98 ham linkin32'si eski /tr kuralıyla çözülebiliyordu;66'sı çözülemiyordu.
Nihai0 ölçümü ham taramada da0'dır. HTML sayısındaki azalma yeni içerik silinmesi
değildir:9 gereksiz home pagination +3 home/page/1 alias kaldırıldı,3 gerçek
yardımcı teşekkür sayfası eklendi.670 canonical'ın3'ü noindex yardımcı sayfadır;
667 statik indekslenebilir aday Google indeks sayısı değildir. Sitemap union652
normal canonical;15 gerçek pagination HTML linkleriyle keşfedilir, sitemap'e
ayrıca eklenmedi.652 eski canonical içerik ve üç özel404 canonical korunur.

## Gerçekten geçenler

- Nihai minify production build exit0: `/tmp/dr-cil-implementation-after-20261124-release`; Hugo0.167.0.
- 967 HTML / 673 JSON-LD: yerel hedefli schema ihlali0. Resmî validator değildir.
- 673 nonalias HTML UI kontratı: hata0; gerçek görünüm/klavye değildir.
- 32 release kabul kontrolü; eski canonical koruma,8 hedef,search/sitemap/form/redirect kuralları.
- 9 Node lifecycle/DOM-stub testi; gerçek WebGL/CPU/GPU değildir.
- 8 contact shortcode senaryosu,24 Hugo dil render'ı; HTTP/teslim değildir.
- Mevcut release hedefini reddetme exit2 ve eski manifest hash'inin korunması.
- 47 yüzde satırı başlangıç Git sürümüyle birebir aynı; klinik sayılar değiştirilmedi.

Komutlar/sonuçlar: evidence/final-test-commands.json, schema-after-final.json,
ui-contract-final.json, seo-release-final.json, contact-form-tests.json,
heart-viewer-node-tests.json ve build-existing-output-guard.json.

## Test edilmeyenler ve kalan işler

Native%200 ve genişlik matrisi (yeni1023/1024/1025 dahil), gerçek Tab/ekran
okuyucu/kontrast/RTL/JS-off; üretim ≥3desktop+3mobile cold ve sıcak ölçüm,
Lighthouse/CPU-GPU/modelA-B ve hata senaryoları; resmî schema/RRT tekrarı;
originHTTP/TLS/headers/301/404; GSC/GBP/CrUX/SERP ve gerçek mesaj teslimi NOT_RUN.
İzinli mevcut1314 HTTP gövdesi baseline ile byte-eş doğrulandı; ölçüm kurulumu
kernel reset nedeniyle çalışmadı, sonraki bağlantı timeout oldu. Yeni1315
socket.bind Operation not permitted: kısıt aşılmadı, kullanıcı server'ı durmadı.

İki belirsiz taxonomy ve kalan genel metadata tekrarları karar bekler; statik
orphan53 bir aday sayımıdır,53 indeks/ceza hatası değildir. PERF03/05 için
ölçülmemiş CPU darboğazı veya INP hükmü kurulmadı. Klinik kimlik/saat/istatistik
ve review olguları medical-review altında onay bekler. 6 hedef sayfanın lastmod'u
gerçek editoryal değişiklik tarihiyle güncellendi; tıbbi review tarihi değildir.

## Koruma ve geri dönüş

Tema alt modülü ve önceki audit kanıtları korunur. Değişiklikler henüz commit
edilmedi. `evidence/source-changes.patch` yalnız uygulama kaynaklarını içerir;
yeni dosyalar dahil tam liste manifesttedir. Otomatik rollback çalıştırılmadı.
Başka değişiklikler geldiyse ters patch uygulamadan önce güncel diff incelenmeli.
Üretim release'i değiştirilmedi; yayın/atomik geri dönüş kabulü06dosyasındadır.

Sonuç dizinindeki [00-progress.md](00-progress.md), [02-keyword-content-map.csv](02-keyword-content-map.csv),
[04-schema-validation.md](04-schema-validation.md), [05-performance-before-after.md](05-performance-before-after.md)
ve [06-launch-readiness.md](06-launch-readiness.md) birlikte okunmalıdır.

## Güncel kaynak satırları

| Dosya | Satır | Amaç |
| --- | ---: | --- |
| [layouts/partials/header/basic.html](sandbox:/Users/yavuz/prg/dr-cil/layouts/partials/header/basic.html) | 6 | Header/menü |
| [assets/css/custom.css](sandbox:/Users/yavuz/prg/dr-cil/assets/css/custom.css) | 20 | Header breakpoint/layout |
| [assets/js/mobilemenu.js](sandbox:/Users/yavuz/prg/dr-cil/assets/js/mobilemenu.js) | 14 | Ortak odak/inert |
| [assets/js/search.js](sandbox:/Users/yavuz/prg/dr-cil/assets/js/search.js) | 27 | Arama/modal |
| [layouts/404.html](sandbox:/Users/yavuz/prg/dr-cil/layouts/404.html) | 1 | Üç dil404 |
| [layouts/partials/author.html](sandbox:/Users/yavuz/prg/dr-cil/layouts/partials/author.html) | 50 | Biyografi bağlantısı |
| [layouts/partials/head.html](sandbox:/Users/yavuz/prg/dr-cil/layouts/partials/head.html) | 1 | Canonical/title |
| [layouts/partials/seo/alternates.html](sandbox:/Users/yavuz/prg/dr-cil/layouts/partials/seo/alternates.html) | 1 | Hreflang |
| [layouts/home.sitemappages.xml](sandbox:/Users/yavuz/prg/dr-cil/layouts/home.sitemappages.xml) | 2 | Sitemap sahipliği |
| [layouts/partials/seo/manual-taxonomy-links.html](sandbox:/Users/yavuz/prg/dr-cil/layouts/partials/seo/manual-taxonomy-links.html) | 5 | 53 kesin arşiv |
| [layouts/partials/schema.html](sandbox:/Users/yavuz/prg/dr-cil/layouts/partials/schema.html) | 50 | Graph ve breadcrumb |
| [layouts/partials/schema-procedure.html](sandbox:/Users/yavuz/prg/dr-cil/layouts/partials/schema-procedure.html) | 7 | Konu sınıflandırması |
| [data/schema_content_types.yaml](sandbox:/Users/yavuz/prg/dr-cil/data/schema_content_types.yaml) | 4 | Dar kaynak haritası |
| [assets/js/heart-viewer.js](sandbox:/Users/yavuz/prg/dr-cil/assets/js/heart-viewer.js) | 15 | Render lifecycle |
| [layouts/partials/three-heart.html](sandbox:/Users/yavuz/prg/dr-cil/layouts/partials/three-heart.html) | 7 | Poster/istek |
| [layouts/partials/home/hero.html](sandbox:/Users/yavuz/prg/dr-cil/layouts/partials/home/hero.html) | 147 | Hero kaynakları |
| [layouts/shortcodes/contact-form.html](sandbox:/Users/yavuz/prg/dr-cil/layouts/shortcodes/contact-form.html) | 9 | Form sağlayıcı kapısı |
| [static/_redirects](sandbox:/Users/yavuz/prg/dr-cil/static/_redirects) | 7 | Doğrudan301 |
| [scripts/build-production.py](sandbox:/Users/yavuz/prg/dr-cil/scripts/build-production.py) | 30 | Güvenli/pinli build |
| [netlify.toml](sandbox:/Users/yavuz/prg/dr-cil/netlify.toml) | 30 | Yerel CI sürüm tanımı |

## Son yerel Chrome denemesi

Yerel Chrome ayrı test penceresinde `http://localhost:1313/` açıldı; **ERR_CONNECTION_REFUSED** gözlendi. Native%200/görsel kabul çalıştırılamadı. Test penceresi kapatıldı, kullanıcının önceki penceresi korundu; kullanıcı sunucusu başlatılmadı/yeniden başlatılmadı. Bu sonuç public DNS/origin teşhisi değildir. Kanıt: `evidence/browser-native-attempt.json`.
