# Yapılandırılmış veri uygulaması — 24 Kasım 2026

Kaynak düzeltmeleri uygulandı. Birleşik kaynakların **ara smoke build**'i
başarılıdır; nihai birleşik build/kabulü root raporundadır. Bu dosya resmî
Schema.org/Google geçiş sertifikası veya klinik doğrulama değildir.

## Dört bağımsız sonuç

| Katman | Gerçek sonuç ve sınır |
| --- | --- |
| JSON/graph/yerel regresyon | Ara minify çıktıda 982 HTML / 685 JSON-LD; bütün scriptler ayrıştı. Tek WebPage/canonical kimliği, breadcrumb sırası/hedefi, çelişen @id, uygunsuz performer, yanlış enum, görsel hedefi, boş ItemList, FAQ metin varlığı ve article şablon testleri: hedefli ihlal0. |
| Schema.org sözlüğü | MedicalWebPage, Person, Service, MedicalTest, DiagnosticProcedure, TherapeuticProcedure ve kullanılan ilişkiler güncel birincil sözlükle hedefli incelendi. Tam sözlük/reasoner/SHACL ve yeni resmî Validator testi **NOT_RUN**. Kaynak sınıflandırması hekim review değildir. |
| Google destek/uygunluk | Article/Breadcrumb/ProfilePage adaylıkları sayfa tiplerine göre ayrıldı; görünüm garantisi yok. FAQ gösterimi7Mayıs2026'da kaldırılmıştır; yararlı görünür SSS ve geçerli semantik ayrı tutuldu. Yeni production Rich Results Test kod/URL testi **NOT_RUN**. |
| Görünür içerik/gerçek bilgi | FAQ yalnız gerçekten content içinde bulunan Q/A'dan; hizmet listesi home content'inde linkli mevcut sayfalardan. Bilinmeyen klinik saat/koordinat/fiyat/kurum onayı/gerçek review ve sameAs iddiaları üretilmiyor. Gerçek klinik kaydı/saatler ve tüm hizmetlerin hekimce doğrulanmış ayrıntılı entity eşlemesi **Bloke**. |

## Yapılan değişiklikler

- `layouts/partials/schema.html`: tek `@graph`; kişi `Person` ve stable
  `#physician`; WebSite/page/article ayrı. Varsayımsal MedicalBusiness/
  Physician ofisi, fiyat, koordinat, çelişen saat ve doğrulanmamış sameAs
  yerine bu ek iddialar üretilmez. Görünür contact bilgisi bu ajan tarafından
  değiştirilmedi. Gerçek ofis verisi onaylandığında ayrı varlık eklenebilir.
- Kişi görseli assets'teki gerçek resource'tan yayımlanır; var olmayan
  `/img/...webp` string'i kullanılmaz. Dosya hedef testi geçti; canlı HTTP/MIME
  testi bu raporda **NOT_RUN**.
- `schema-breadcrumb-items.html` ve `breadcrumbs.html`: görünür breadcrumb ile
  graph aynı öğe kaynağını kullanır,1..N sırası. Dil kökü ve gerçek canonical
  URL kullanılır; ikinci procedure breadcrumb'ı kaldırılmıştır.
- `seo/current-page-url.html` SEO ajanıyla paylaşılan helper'dır; sayfalama
  WebPage/graph kimliğiyle canonical aynı gerçek URL'yi kullanır.
- `schema-procedure.html` ve `data/schema_content_types.yaml`:165 hizmet
  kaynağında tek MedicalProcedure varsayımı yok.37 paylaşılan translationKey,
  mevcut açık test/işlem başlığına dayanır. Ara çıktıda60 TherapeuticProcedure,
 36 MedicalTest,15 DiagnosticProcedure,51 geniş kapsamlı Service.3 boş
  kaynakta hizmet entity'si üretilmez. Klinik sonlanım/anatomi/işlem enum'u/
  planlı status/hazırlık/takip veya kurum otoritesi varsayılmaz.
- `schema-faq.html`: normal JSON string escaping; yalnız render edilen
  soru/cevaplar; sayfa başına tek FAQPage. Ara çıktıda267 FAQPage/1550 Q/A.
  Metin eşlemesi görsel/ekran okuyucu veya tıbbi doğrulama değildir.
- `schema-scholarly.html`: yayın listesi Article yapılmaz. Gelecekte gerçek
  yayın detayı için açık `scholarly.verified`, DOI,journal,authors metadata'sı
  gerekir. Bugünkü yayın listesi tek bilimsel yayın entity'si değildir.
- Gerçek blog detayları BlogPosting; liste/taxonomy CollectionPage;
  biyografi ProfilePage; iletişim ContactPage; hata/boş sayfa WebPage.
  Makale yayın/değişiklik tarihleri gerçek içerik metadata'sıdır, tıbbi review
  tarihi olarak yeniden kullanılmaz.

## Audit kapanışları

| ID | Uygulama / kabul durumu |
| --- | --- |
| SCH-01 | Uygulandı; tüm ara çıktıda artan sıra, hedef dosyaları ve ortak breadcrumb kaynağı doğrulandı. Resmî kod testi bekliyor. |
| SCH-02 | Uygulandı; aynı id için çelişen graph property0; dil hedefleri doğru canonical ile üretildi. HTTP/Google testi ayrı. |
| SCH-03 | Uygulandı; uygunsuz performer0; Service.provider yalnız Person ilişkisi; yeni yanlış MedicalWebPage provider alanı eklenmedi. |
| SCH-04 | Uygulandı; sınıf adları uygun @type olarak ayrıldı. Doğrulanmış işlem enum bilgisi olmadığı için procedureType emit edilmez; yanlış enum0. |
| SCH-05 | Uygulandı; yayımlanan gerçek görsel dosyası mevcut; canlı HTTP200/MIME doğrulaması bekliyor. |
| SCH-06 | Çelişen schema saatleri üretimi kaldırıldı. Gerçek saatin görünür üç dil/GBP/klinik kaydıyla tek kaynaktan eşlenmesi hekim/klinik verisi bekliyor; tam kabul kapatılmadı. |
| SCH-07 | Tek tür/anatomi/disease varsayımları giderildi; açık başlıklarla dar sınıflandırma ve broad Service fallback uygulandı. Tüm kaynakların hekimce onaylı ayrıntılı tıbbi sınıflandırması bekliyor. |
| SCH-08 | Otomatik review/Lastmod ve dernek otoritesi üretimi kaldırıldı. Gerçek review kaydı, kurum dayanağı ve gerçek ofis bilgisi doğrulanmış değildir. |
| SCH-09 | Uygulandı; gerçek blog detayları dışında otomatik Article/BlogPosting yok; ara output target testi geçti. |
| SCH-10 | Uygulandı;3 dolu ve doğru dilde home ItemList, kişi/ofis model ayrımı. Doğrulanmış gerçek ofis entity'sinin yayınlanması ayrı veri bekliyor. |

## Kanıt ve yeniden üretim

- `evidence/schema-before.json` / `.log`: başlangıç976HTML/679script;
  hedefli kabul kurallarında4210 ihlal. Bu sayı Google hata sayısı veya
  4210 ayrı audit bulgusu değildir; aynı route/property çoklu sayılabilir.
  Örneğin eski birleşik Person/Physician sözlükte otomatik geçersiz sayılmaz;
  burada seçilen ayrık kişi/ofis modelinin kabul kuralıdır. Eski132 enum dışı
  sınıfa ek33 çıplak enum string'i de strict tamIRI kuralında sayılmıştır.
- `evidence/schema-smoke-build.json` / `.log`: tam komut/env/geçici çıktı,
  exit0; ara source snapshot. Hugo53830ms; kullanıcı performansı değildir.
- `evidence/schema-smoke-after.json` / `.log`:982HTML,685script,679breadcrumb,
 267FAQ,1550Q/A,hedefli ihlal0; exit0.
- `evidence/schema-content-classification.csv`:165 mevcut kaynak, dil,
  translationKey,başlık,üretilecek sınıf ve sınırlılık; klinik review NOT_VERIFIED.
- `evidence/schema-primary-sources.json`:24Kasım2026 açılmış birincil kaynaklar.

```sh
python3 scripts/validate_schema_output.py BUILD_ROOT --json REPORT.json
```

Bu komut yerel dosyaları okur; HTTP/form isteği göndermez. `BUILD_ROOT` yerine
`schema-smoke-build.json` içindeki geçici root kullanılabilir. Kaybolursa
root raporundaki güvenli ayrı minify build komutunu yeniden çalıştırın.
`public/`/izlenen resources temizleme, --gc, kullanıcı server restart, DNS,
hesap, commit/push veya deploy yapılmadı.

## Çalıştırılmadı / dış veri

Yeni resmî Schema.org Validator ve Google RRT, Google public fetch/index,
HTTP görsel MIME/erişim, bağımsız mesleki/klinik kayıtları ve tüm klinik
metinlerin uzman fact-check'i çalıştırılmadı/doğrulanamadı. Root daha sonra
bu testlerden birini gerçekten tamamladıysa ham kanıtla ayrı kaydetmelidir.

## Nihai birleşik release doğrulaması

Root'un `/tmp/dr-cil-implementation-after-20261124-release/public` çıktısı: **967 HTML / 673 script**, hedefli yerel hata **0**. Önceki ara smoke685script kaydı farklı render snapshot'ıdır; nihai sayım673'tür. Resmî Validator/RRT, klinik gerçeklik ve gerçek image HTTP kabulü yeni çalıştırılmadı. Kanıt: `evidence/schema-after-final.json` ve `final-build-manifest.json`.
