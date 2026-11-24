# Resmi schema doğrulaması

Kontroller, canlı URL taratmak yerine taze üretim çıktısından çıkarılan gerçek JSON-LD veya tam HTML kodu ile yapıldı. Böylece localhost'un dışarıdan taranamaması sonucu etkilemedi.

## Schema.org Markup Validator

Araç: [Schema.org Markup Validator](https://validator.schema.org/). Araç, doğrudan verilen markup'ı doğrulayabildiğini ve JSON-LD sözdizimi/graph hatalarını gösterdiğini belirtir.

| Kod girdisi | Sonuç |
| --- | --- |
| TR ana sayfa `index.html` içindeki JSON-LD | `0 HATA`, `0 UYARI`, 2 öğe: `WebPage`, `ItemList` |
| TR `blog/diyabetik-ayak/` içindeki JSON-LD | `0 HATA`, `0 UYARI`, 4 öğe: `BreadcrumbList`, `WebSite`, `BlogPosting`, `FAQPage` |

Bu iki doğrulama; ana sayfa/organizasyon bağlamını ve bir içerik sayfasındaki breadcrumb, yayın ve FAQ graph'ını kapsar. Tüm sayfalar/diller ve temsilî hizmet sayfası bu resmi araçta tek tek çalıştırılmadı.

## Google Rich Results Test

Araç: [Google Rich Results Test](https://search.google.com/test/rich-results). Taze TR ana sayfanın **tam HTML'i** “kod” sekmesinden, varsayılan smartphone denetim aracıyla çalıştırıldı.

Sonuç: **“Hiçbir öğe algılanmadı / Bu URL'de zengin sonuç algılanmadı.”** Test sonuç sayfası: [çalıştırma kaydı](https://search.google.com/test/rich-results/result?id=U9hlidd0SOLy7DE2FIiNcw).

Bu sonuç schema hatası olarak yorumlanmadı: Schema.org doğrulayıcısı aynı release'te 0 hata/uyarı verdi; Rich Results Test ise yalnız Google'ın desteklediği zengin sonuç türleri için uygunluk bildirir. Kapsamdaki ana sayfa `WebPage` ve `ItemList` graph'ı için bir zengin sonuç vaat edilmemektedir. Canlı URL/indeks/crawl durumu bu testten çıkarılamaz.

## Dış bağımlılık ve sınırlamalar

- Doğrulayıcıların erişilebilirliği, arayüzü ve Google uygunluk politikaları dış bağımlılıktır.
- Rich Results Test, Schema.org'un tüm geçerli türlerini “zengin sonuç” olarak raporlamaz.
- Canlı production URL taraması, deploy ve Search Console mülkiyet doğrulaması yapılmadı.
