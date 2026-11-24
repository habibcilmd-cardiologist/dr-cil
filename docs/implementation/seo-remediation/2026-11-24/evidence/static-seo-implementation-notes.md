# Statik SEO uygulama notları — 24 Kasım 2026

Bu dilim kaynak uygulamasıdır. DNS/hesap/deploy/mesaj işlemi veya tema alt
modülünde değişiklik yapılmadı. Son entegre production build ve tam tarama
root tarafından çalıştırılır; bu dosyada yapılmamış runtime/HTTP sonucu yoktur.

## Değişiklikler ve bulgu eşlemesi

| Bulgu | Uygulama | Kanıt / kabul sınırı |
| --- | --- | --- |
| STATIC-01 | 45 content dosyasında98 link hedefi düzeltildi:66 çözülemeyen kullanım ve32 eski `/tr/` iç linki. Link metni, klinik ifade, front matter/permalink değiştirilmedi. | `static-link-replacements.json`; uygulama scripti bütün hedeflerin envanterde gerçek route olduğunu assert etti. Final bütün çıktı taraması ve gerçek HTTP root kabulündedir. |
| STATIC-02 | Yerel `head.html` ve `seo/current-page-url.html` aynı Pager URL'sini canonical olarak kullanır. Sayfa2+ title'da yerelleştirilmiş sayfa numarası; OG URL/title aynı kaynaktan. | `seo/list-paginator.html` section/term için tema ile aynı koleksiyonu başlatır; simple hizmet hub'ını ve normal sayfaları paginate etmez. Başka dilin paginator'ını render thread'inden başlatmaz. |
| STATIC-02, hreflang | Sayfa2+ üzerinde gerçek yazı kümesi eşdeğerliği kanıtlanmadığından alternate üretilmez; sayfa1/normal çevirilerde self+gerçek translation ve varsa aynı konunun TR x-default'ı. Detaydan home'a yanlış genel x-default kaldırıldı. | Bu bir çeviri hedefini uydurmama tercihidir; sayfa2'yi diğer dilin sayfa1'ine bağlamaz. Normal sayfaların karşılıklı hreflang kabulü final taramadadır. |
| STATIC-02, home kopyaları | Üç recent-articles preview partial'ında `.Paginate` kaldırıldı, aynı first-N ve görünüm korundu. Asıl blog/kategori arşivi pagination'ı korunur. |12 eski home pager route'u (dil başına page1 aliası + page2–4 kopyaları) exact301 planında. `static-seo-redirect-rules.txt` root HOST sahibine iletildi; gerçek HTTP henüz NOT_RUN. |
| STATIC-03 | Native sitemap generation ve section Sitemap output'ları kapatıldı. Tek sahibi `home.sitemappages.xml` olan üç dil urlset'i: root, `/en/sitemap.xml`, `/ar/sitemap.xml`. Robots üçünü açık bildirir. | Yeni outputformat `SiteMapPages`; eski static sitemap ve üç çakışan/işlevsiz XML template kaldırıldı. `/tr/` altında harita ilan edilmez. Thank-you noindex/sitemap.disable dahil filtrelenir. Final XML/HTTP kabulü ayrıca. |
| STATIC-04 | EN home bozuk fragment `#pacemaker-and-electrophysiology`→`#pacemaker-electrophysiology` düzeltmesi root sahibine bırakıldı. | Root-owned `content/en/_index.md`; bu ajan o dosyaya yazmadı. |
| STATIC-05 |55 boş manuel taxonomy normal page'in53'ü tek bir gerçek aynı-dil term ile kesin normalize title eşleşti. `single.html` hook'u mevcut term.Pages içeriklerini ve gerçek arşiv linkini gösterir. | `static-taxonomy-exact-matches.json`; yalnız case/hyphen/underscore/space normalizasyonu, diakritikler korunur, fuzzy/transliterasyon yok. URL/canonical/robots/sitemap üyeliği değiştirilmedi. Final53 emitted HTML hook sayımı root'ta. |
| STATIC-05, kalan | `/tags/istanbul-kardiyolog/` ve `/tags/kardiyak-izleme/` için tek gerçek exact term eşleşmesi bulunmadı. | İlgisiz yazı/metin veya redirect/noindex kararı uydurulmadı. Bu iki kaynak ve normal/term URL konsolidasyonu GSC/URL politika incelemesine açık; bütün STATIC-05 kapandı denemez. |
| STATIC-06 | Mevcut `lang.Merge` çeviri fallback'i korunur; JSON entry'de language/languageName var; summary plain text. UI ajanı farklı dil sonuç etiketini ve link lang/dir'ini uygular. | Aynı TranslationKey için seçilen dilin önceliği korunur. Final üç JSON ve browser dil/sorgu testi gerekli; tamamı aynı indeks veya current-language-only değil. |
| STATIC-07 | Front matter home title kullanılır; archive pager başlığı ayrışır. Tek canonical/OG/twitter metadata kaynağı; blog Article social tipi, diğerleri website. Öncelikli hedef sayfa metadata'sı root content kapsamındadır. | Genel site-description fallback'i bütün arşivlerde kaldırılmış değildir; duplicate sayısını sıfıra indirme iddiası yok. Düşük değerli mekanik kelime/karakter hedefi uygulanmadı. |

## Link düzeltme kararları

- EN `false/` hedeflerinin9'u gerçek Coronary Artery Disease rehberine,
  ikisi gerçek Abdominal Aortic Aneurysm rehberine bağlandı. Hastalık adını
  iletişim sayfasına bağlama gibi yanıltıcı bir çözüm uygulanmadı.
- Olmayan generic valve/CABG hizmet endpoint'leri için mevcut aynı-dil
  bilgilendirici rehber kullanıldı; yeni bir CABG veya başka hizmet vaadi eklenmedi.
- Klinik sayfalarındaki eski angiography/angioplasty eşanlamlı yolları gerçek
  mevcut hizmete; lower-extremity linki mevcut peripheral-vascular hizmetine.
- EN bloglarının prefixesiz service/contact ve slug değişmiş blog hedefleri,
  CSV'deki gerçek emitted permalink'lere eşlendi. Turkish-character ve Arapça
  encoding içeren geçerli URL'ler topluca değiştirilmedi.

## Başlangıç ve son kontrol komutları

Gerçekten çalıştırılanlar:

- Audit URL envanteri + broken-link triage JSON toplandı ve tüm98 önerilen
  yeni hedefin gerçek envanter üyeliği assertion ile doğrulandı; exit0.
-55 manual taxonomy kaynağının aynı taxonomy/same-language gerçek term
  title eşleşmesi sayıldı;53 tek eşleşme,2 eşleşme yok; exit0.
- Native/custom sitemap outputs `hugo config --format json` ile incelendi;
  güncel primary Hugo sitemap belgeleriyle karşılaştırıldı.

Kaynaklar tamamlandıktan sonra bu ajan ayrı build başlatmadı; root'un
entegre derlemesini bölmemek için aşağıdaki kabuller merkezî çalıştırılır:

1. Production build exit0; bütün iç link/asset/fragment hedefleri.
2. Gerçek archive pagination canonical self, OG url aynı, title numarası.
3. Üç XML geçerli urlset; doğru dil ve loc; thank-you yok; robots haritaları
   dosyada var; `/tr/sitemap.xml` veya section sitemap ilanı/çakışması yok.
4.53 normal taxonomy çıktı sayfasında gerçek arşiv+ilgili içerik linki;2
   eşleşmeyende boş bir related-section üretilmiyor.
5. Üç arama JSON'unda dil alanları; mevcut eşdeğerde seçilen dil önceliği;
   fallback etiketinin browser kontrolü.
6.12 home kopyası ve eski duplicate sitemap için hedef platformda exact
   GET301→GET200; config varlığı HTTP geçişi değildir.

Tarayıcı, Google indeks/URL Inspection, rank/CTR ve gerçek HTTP sonuçları
bu dilimde **NOT_RUN**; Google'ın hangi canonical'ı seçtiği bilinmiyor.

## Güncel primary kaynaklar

24 Kasım 2026'da açıldı:

- https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading — her gerçek pager için ayrı canonical.
- https://developers.google.com/search/docs/specialty/international/localized-versions — gerçek eşdeğer ve karşılıklı dil bağlantıları.
- https://gohugo.io/templates/pagination/ — tek ilk initialization/collection ve caching davranışı.
- https://gohugo.io/templates/sitemap/ — native multilingual output ve generation disable/override.
- https://gohugo.io/configuration/sitemap/ — page inclusion disable/filename.

Google kaynaklarına atfedilen açıklamalar teknik ilke özetidir; sitenin
gerçek indeks/sıralama sonucunun kanıtı değildir.
