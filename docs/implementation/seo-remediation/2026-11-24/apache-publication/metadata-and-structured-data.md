# Metadata, sosyal paylaşım, Google etiketleri ve FAQ

24 Kasım 2026. Son çıktı:
`output/releases/apache-publication-20261124-01/public`.

## Yapılan düzeltmeler

- `layouts/partials/seo/social-image.html`: sayfa için gerçek raster
  featured/cover/thumbnail görseli seçilir; yalnız SVG içerik diyagramı varsa
  mevcut site paylaşım görseli kullanılır. İçerikteki SVG veya makale schema
  görseli kaldırılmadı; yeni görsel üretilmedi.
- `layouts/partials/seo/social.html`: OG görselinin gerçek MIME türü, genişliği,
  yüksekliği ve açıklaması; Twitter görsel açıklaması eklendi. Kare görsele
  `summary`, yeterli yatay orana `summary_large_image` uygulanır. Başlık,
  açıklama ve OG URL mevcut canonical ile eşleşmeye devam eder.
- `layouts/partials/extend-head-uncached.html`: mevcut GA4 kimliği
  **G-TDC4PMVEMK** korundu. Üretim çıktısında kod bulunur; loader yalnız
  yapılandırılmış canlı alan adının HTTPS sürümünde çalışır. Aynı üretim
  çıktısını localhost/staging üzerinde açmak gerçek Analytics isteği üretmez.
- `layouts/partials/schema-faq.html`: yorum güncel Google FAQ rich result
  kaldırma tarihini kaydeder. FAQ JSON-LD üretme mantığı değiştirilmedi;
  görünür, gerçek soru/cevap eşleşmesi korunur.

## Çalıştırılan kontroller ve sonuç

`scripts/validate_metadata_output.py` gerçek derlenmiş **967 HTML** dosyasını
okudu. **294 alias** ayrıldı; kalan **673 sayfanın tamamında 0 hata**:

- OG/Twitter zorunlu kontrol alanları tekil ve dolu; OG URL canonical ile aynı.
- Üretim URL'leri HTTPS canlı domaini kullanıyor; localhost URL sızıntısı yok.
- Mevcut GSC doğrulama token'ı her sayfanın head bölümünde doğru ve tekil.
- GA4 kodu tek kez üretiliyor ve mevcut kimlik korunuyor.
- OG/Twitter görsel URL'leri aynı; gerçek dosyanın magic-byte MIME ve piksel
  boyutları bildirilen değerlerle eşleşiyor.
- Üç sitemap geçerli XML; bütün loc adresleri üretim origin'inde. robots.txt
  üç XML'i de bildiriyor: TR **258**, EN **196**, AR **198**; toplam **652**.

Görsel sonuçları:

| Kaynak | Gerçek biçim/boyut | Kart |
| --- | --- | --- |
| `/img/og-image.webp` | WebP, 1024 × 1024 | summary |
| `/hakkimda/featured.webp` | WebP, 640 × 640 | summary |
| `/en/about/featured.webp` | WebP, 640 × 640 | summary |

Bu kare görseller geçerli fallback'tir; yatay 1200 × 630 özel paylaşım tasarımı
yapılmış gibi raporlanmaz. Kaynakta bulunan kullanılmayan `og-image.png`
dosyasının gerçek biçimi JPEG'dir; bu PNG yolu yeni çıktıda OG/Twitter görseli
olarak yayımlanmıyor. Varsayılan gerçek WebP korunmuştur.

Örnek önce/sonra kanıtı `evidence/metadata-before-after.json` içindedir. Önceki
makale kartı SVG'yi işaret ediyordu; yeni kart mevcut raster fallback kullanır.

Gerçek derlenmiş Analytics inline kodu ayrıca Node VM ve sahte `document`
ile çalıştırıldı: **10/10 senaryo geçti**. Localhost, 127.0.0.1, IPv6,
`.localhost`, staging ve sahte domain son eki loader başlatmadı; gerçek
HTTPS apex/www senaryoları birer loader ve tek config çağrısı üretti.
Bu test **ağ isteği veya gerçek Analytics olayı göndermedi**.

Kanıtlar:

- `evidence/metadata-output.json`
- `evidence/metadata-before-after.json`
- `evidence/analytics-guard.json`

Tekrar komutları:

```sh
python3 scripts/validate_metadata_output.py output/releases/apache-publication-20261124-01/public --json docs/implementation/seo-remediation/2026-11-24/apache-publication/evidence/metadata-output.json
node scripts/tests/analytics-guard.test.mjs output/releases/apache-publication-20261124-01/public/index.html
```

## Schema geçerliliği, FAQ ve Google desteği ayrı konulardır

Google FAQ rich result özelliğini **7 Mayıs 2026** itibarıyla kaldırdı; ilgili
belge **15 Haziran 2026** tarihinde kaldırıldı. Eski “yetkili sağlık/kamu
sitelerine gösterilir” kuralı bugünkü destek durumu değildir. FAQPage hâlâ
Schema.org sözlüğünde geçerli bir türdür; doğru görünür soru/cevapları
tanımlamak için kalabilir. Google FAQ zengin sonucu veya sıralama kazanımı
vaat edilmez.

Önceki resmî Schema.org kabulü yalnız ana sayfa ile örnek makaleyi kapsıyordu;
iki örneğin sonucu bütün şablonların resmî kabulü değildir. Bu turdaki tüm
çıktı schema/breadcrumb kontrollerinin ayrı sonuçlarına da bakılmalıdır.
OG/Twitter etiketleri, Article/Breadcrumb/FAQ JSON-LD ve Google'ın gerçekten
gösterdiği arama sonucu birbirinin yerine geçen kontroller değildir.

## Bu raporun kanıtlamadığı işler

- Search Console hesabında güncel doğrulanmış sahiplik veya sitemap gönderimi.
  HTML meta etiketi URL-prefix mülkü içindir; Domain property DNS doğrulaması
  gerektirir. Etiketin varlığı hesap kabulü demek değildir.
- Doğru GA4 hesabında canlı olay teslimi, Realtime/DebugView veya rapor verisi.
- Canlı sosyal platform crawler'larının görsel HTTP/MIME erişimi ve gerçek
  Facebook/LinkedIn/X/WhatsApp paylaşım önizlemeleri.
- Yeni tam site örnekleriyle resmî Schema.org/RRT ve canlı URL inspection.
- Hukuki uygunluk onayı, klinik bilgi/kimlik doğrulaması, ilk sıra veya trafik
  artışı. Hiçbir hesap ayarı veya gerçek form/mesaj gönderimi yapılmadı.

Birincil kaynaklar (24 Kasım 2026'da okundu):

- https://developers.google.com/search/updates — 8 Mayıs / 15 Haziran 2026 FAQ kayıtları.
- https://schema.org/FAQPage
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- https://support.google.com/webmasters/answer/9008080
- https://ogp.me/
