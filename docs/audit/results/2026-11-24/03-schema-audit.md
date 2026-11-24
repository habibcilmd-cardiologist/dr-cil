# Yapılandırılmış veri denetimi — 24 Kasım 2026

Bu rapor, mevcut kaynaklardan ayrı hedefe üretilen **üretim HTML çıktısını**
inceler. Canlı Netlify sürümüyle byte eşitliği doğrulanmadı. Kaynak kodunda
düzeltme yapılmadı. Hiçbir bulgu Google cezası veya mevcut sıralama kaybının
kanıtı olarak sunulmaz.

## Kapsam, yöntem ve sınırlar

Derleme: `/tmp/dr-cil-audit-2026-11-24/public`.

```sh
python3 docs/audit/results/2026-11-24/evidence/schema-audit.py \
  /tmp/dr-cil-audit-2026-11-24/public \
  docs/audit/results/2026-11-24
```

HTMLParser ile bütün HTML dosyalarındaki JSON-LD scriptleri, Microdata ve
RDFa işaretleri toplandı; JSON ayrıştırıldı; top-level ve nested düğümler ayrı
sayıldı; çelişkili kimlikler, breadcrumb sıraları, dosya hedefleri ve seçilmiş
property/enum ilişkileri denetlendi. Özel kontrol scripti **resmî Schema.org
Validator değildir**. JSON-LD expansion/RDF reasoner veya bütün sözlüğe karşı
eksiksiz SHACL doğrulaması çalıştırılmadı.

Schema.org'un erişilen sayfaları V30.1 / 2026-09-16 sürüm bilgisini gösteriyor;
sayfalar ayrıca development-version uyarısı taşıyor. Hedefli sözlük kontrolü,
denetim tarihinde erişilen bu birincil tanımlara dayanıyor.

| Ölçüm | Sonuç |
| --- | ---: |
| Taranan HTML dosyası | 976 |
| JSON-LD içeren HTML route'u | 679 |
| JSON-LD scripti | 679 |
| JSON ayrıştırma hatası | **0** |
| Top-level graph düğümü / CSV satırı | 3.322 |
| JSON-LD içermeyen alias/refresh HTML dosyası | 297 |
| Microdata tespit edilen HTML | 0 |
| RDFa tespit edilen HTML | 0 |
| JSON-LD içeren route'lardaki farklı canonical değeri | 655 |

679 sayısı **route/dosya sayısıdır**; 679 farklı indekslenebilir canonical
sayfa anlamına gelmez. Sayfalama çıktıları da bu taramaya dahildir. 655 farklı
canonical değerinin hepsinin indekslenebilir olduğu bu schema diliminde
iddia edilmez; URL envanterine bakılmalıdır.

### Dört katman ayrı değerlendirilmiştir

| Katman | Gerçek sonuç |
| --- | --- |
| JSON/JSON-LD sözdizimi ve graph | 679 script JSON olarak ayrıştı; 165 sayfada aynı breadcrumb kimliğine çelişen tanımlar var. Tam JSON-LD expansion yapılmadı. |
| Schema.org sözlüğü/property/enum | Kullanılan ana türler mevcut; `performer` domain'i ve 132 `procedureType` değeri için hedefli sözlük uyuşmazlıkları doğrulandı. Bütün property ilişkilerine resmî-validator geçişi verilmedi. |
| Google özelliği/uygunluk | Güncel birincil belgeler kontrol edildi. Tek bir gerçek DEV kod örneği Google Rich Results Test'te 3 geçerli öğe verdi; LocalBusiness için 3 kritik olmayan uyarı var. Üretim URL taraması ve URL Inspection yapılmadı. |
| Görünür içerik/gerçek bilgi | Çalışma saati çelişkisi doğrudan kanıtlandı. İnceleme tarihi, dernek otoritesi, koordinat ve fiyat iddialarının gerçek dayanağı doğrulanamadı. |

### Gerçek resmî doğrulayıcı testleri — tek DEV örneği

Ana denetimde, tarayıcı üzerinden `http://localhost:1313/hizmetler/dizalti-damar-tikanikligi/`
sayfasının gerçek DOM'undan alınan **5.691 karakterlik JSON-LD**, bir
`script[type=application/ld+json]` içine sarılıp iki resmî servisin **kod**
modunda test edildi. Localhost @id/URL'leri korundu. Bu girdi DEV render'dır;
bu rapordaki ayrı üretim dosyalarıyla byte eş olduğu iddia edilmez. Test canlı
public URL taraması değildir; görünür bütün sayfa içeriği ve görsel/public
URL erişilebilirliği bu kod girdisiyle doğrulanmış sayılmaz.

| Resmî test | Gözlenen sonuç | Sınır |
| --- | --- | --- |
| Schema.org Validator | 4 öğe grubu; **1 hata, 3 uyarı**. MedicalWebPage grubu 1 hata/2 uyarı; BreadcrumbList 0 hata/1 uyarı; WebSite ve FAQPage 0/0. | Tek DEV hizmet kodu; bütün üretim çıktısına resmî test geçişi verilmedi. |
| Google Rich Results Test | **3 geçerli öğe:** Breadcrumb 1, LocalBusiness 1, Organization 1. LocalBusiness'te **3 kritik olmayan** uyarı. | Breadcrumb graph/sıra sorunlarına rağmen bu örnek Google'da geçerli kabul edildi; bunlar Google kritik hatası olarak sunulamaz. |
| Search Console URL Inspection | **NOT_RUN** | Yetkili GSC bağlantısı yok; Google'ın public URL'yi nasıl gördüğü doğrulanmadı. |

Schema.org Validator'ın gözlenen hatası: `TherapeuticProcedure`
`procedureType` değeri geçersiz; beklenen üyeler `NoninvasiveProcedure` ve
`PercutaneousProcedure`. Açılan uyarılar `performer` alanının MedicalProcedure
ve MedicalWebPage üzerinde tanınmadığını belirtiyor. Breadcrumb uyarısının
sayısı görüldü; ayrıntısı açılmadığı için metni/özelliği tahmin edilmiyor.

Google LocalBusiness kritik olmayan uyarıları: eksik `address`, eksik
`priceRange`, geçersiz `image` URL'si. Bu örneğin görsel adresi localhost
olduğundan, Google'ın bu uyarısı SCH-05'teki üretim dosyası eksikliğinin
doğrudan kanıtı değildir. SCH-05 bağımsız statik dosya karşılaştırmasıdır.

Kanıt: `evidence/browser-validator-results.json`;
[Google test sonucu](https://search.google.com/test/rich-results/result?id=qsf2f9kvkCtQm7CbrWhRBg).
`schema-inventory.csv` ve yeniden üretilebilir offline scriptteki
`official_validator=NOT_RUN` satırları **o üretim düğümüne tek tek resmî test
uygulanmadığını** gösterir; yukarıdaki tek DEV örneğinin çalıştırılmadığı
anlamına gelmez.

## Tür envanteri ve Google desteği

`schema-inventory.csv` her top-level düğüm için URL, script/düğüm konumu,
property listesi, JSON sonucu, hedefli sözlük kontrolü, özellik adayı ve içerik
durumu içerir. Nested tip/property sayımları `evidence/schema-summary.json`
içindedir. Birden fazla @type aynı düğümde bulunabildiği için tür toplamları
3.322 düğüm toplamından büyük olabilir.

| Top-level tür | Düğüm sayısı | Sözlük ve Google yorumu |
| --- | ---: | --- |
| WebSite | 679 | Mevcut tür. Sayfa kümesini tanımlar; her sayfaya bağımsız bir zengin sonuç garantisi vermez. |
| Person + Physician | 679 ortak düğüm | İki tür de mevcut. Güncel Physician tanımı bireysel hekimi veya ofisini MedicalOrganization olarak ele alır; birleşimi otomatik olarak “olmayan tür” saymak yanlıştır. Entity sınırları ve LocalBusiness adres gereksinimi ayrıca değerlendirilmeli. |
| BreadcrumbList | 832 | Google Breadcrumb özelliği mevcut; somut sıra ve graph sorunları var. |
| Article | 367 | Google Article özelliği mevcut; liste, iletişim ve hata sayfalarına uygulanması ayrıca içerik açısından yanlış/uygunsuz olabilir. |
| BlogPosting + MedicalWebPage | 129 ortak düğüm | Türler mevcut; blog liste/sayfalama sayfalarında da üretiliyor. MedicalWebPage için ayrı bir Google rich result özelliği tanımlı değil. |
| MedicalWebPage (hizmet düğümü) | 165 | Mevcut semantik tür; özel Google zengin sonuç desteği olmaması geçersizlik değildir. |
| FAQPage | 279 | Mevcut Schema.org türü. Google FAQ rich result özelliği 7 Mayıs 2026'dan beri gösterilmiyor. |
| MedicalProcedure | 165 | Mevcut tür; kendi adına özel Google rich result özelliği yok. Property, enum ve gerçek sayfa amacı kontrol edilmeli. |
| MedicalBusiness | 15 | Mevcut LocalBusiness alt türü; Google LocalBusiness adaylığı gerçek işletme bilgileri ve koşullara bağlı. |
| ItemList | 12 | Mevcut tür; bu listeler öğe içermiyor. Sırf ItemList eklemek Google carousel sağlamaz. |
| MedicalScholarlyArticle | **0** | Tür gerçekten mevcut; mevcut üretim çıktısında hiç üretilmiyor. Template'te bulunması canlı çıktıda kullanıldığı anlamına gelmez. |

Nested düğümlerde ayrıca ListItem (2.457), Question (1.632), Answer (1.632),
PostalAddress (15), GeoCoordinates (15), OpeningHoursSpecification (30),
Organization (165), MedicalCondition (165) bulunuyor. Nested referansların
type'ları dahil edilince WebSite ve Physician sayıları yükselir; bunlar yeni
top-level varlık sayısı değildir.

## Öncelikli bulgular

### SCH-01 — Breadcrumb sıraları 628 route'ta `1,3,3` — P1 / Doğrulandı

- **URL/çıktı:** `/hizmetler/hipertansiyon/` ve toplam 628 route.
  İlk BreadcrumbList'te `position` değerleri `[1,3,3]`.
- **Kaynak:** `layouts/partials/schema.html:82–87`. `.Ancestors.Reverse`
  indeksinde home atlanıyor ancak sıra hesabında atlanan indeks tutuluyor;
  son öğe daha sonra liste uzunluğuyla tekrar 3 oluyor.
- **Etki:** İki farklı breadcrumb öğesinin aynı sırayı taşıması navigasyon
  zincirini belirsizleştiriyor. Google Rich Results Test'in tek DEV örneğinde
  breadcrumb **geçerli** bulundu. Bu bulgu Google'ın kritik hatası veya kesin
  reddi şeklinde yorumlanamaz.
- **Çözüm:** Yalnız gerçekten eklenen öğeler üzerinden artan sıra üretmek.
- **Kabul:** Bütün üretilen BreadcrumbList'lerde benzersiz, artan `1..N` sıra;
  ilgili URL'lerde Schema.org ve Rich Results Test kod testi.
- **Kanıt:** `evidence/schema-summary.json`,
  `evidence/schema-hizmetler-hipertansiyon-index.json`.
- **Resmî dayanak:** [BreadcrumbList](https://schema.org/BreadcrumbList),
  [Google Breadcrumb](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb).

### SCH-02 — 165 hizmet sayfasında aynı breadcrumb @id'si çelişiyor — P1 / Doğrulandı

- **URL:** `/hizmetler/hipertansiyon/`, `/en/services/echocardiography/`,
  `/ar/services/echocardiography/` dahil 165 hizmet route'u (57 TR, 54 EN, 54 AR).
- **Gerçek çıktı:** Aynı `.../#breadcrumb` kimliğine iki farklı
  `itemListElement` dizisi veriliyor. Genel dizi doğru hizmet canonical'ını
  kullanırken ikinci dizi Türkçede `/tr/hizmetler/`, EN/AR için `/services/`
  kullanıyor. EN/AR ikinci dizinin home hedefi de dil kökü yerine `/`.
- **Kaynak:** `schema.html:78–95` ve `schema-procedure.html:30–32,68–79`.
- **Önemli ayrım:** TR `/tr/*` için Netlify migration redirect'i tanımlı;
  bu hedefi yalnız dosya yok diye kesin HTTP 404 saymıyoruz. `/services/`
  de üretim dosyalarında yok; gerçek sunucu yanıtı bu dilimde ölçülmedi.
- **Çözüm:** Görünür breadcrumb ile aynı veriden tek graph tanımı üretmek;
  farklı, meşru breadcrumb yolları gerekiyorsa farklı kimlikler kullanmak.
- **Kabul:** Aynı @id için çelişen özellik kalmaması; tüm dil hedeflerinin
  doğru canonical 200 adreslerine gitmesi; genel ve procedure dizisi çakışmaması.
- **Kanıt:** `evidence/schema-pages.json` içindeki `conflicting_ids`;
  hizmet örnek JSON dosyaları. Tam URL listesi `schema-summary.json` içinde.

### SCH-03 — `performer` 495 yanlış türdeki düğüme ekleniyor — P1 / Doğrulandı

- **Kapsam:** 165 MedicalProcedure + 165 MedicalWebPage + 165 BreadcrumbList.
- **Kaynak:** `layouts/partials/schema.html:146–150`; procedure partial'ının
  döndürdüğü üç nesnenin tamamı aynı `performer` alanıyla merge ediliyor.
- **Sözlük karşılaştırması:** [performer](https://schema.org/performer)
  Event üzerinde, etkinlikteki icracıyı tanımlayan property'dir. Bu üç sınıf
  Event alt türü değildir. Buradaki sorun property'sinin hiç var olmaması
  değil, yanlış domain'de kullanılmasıdır.
- **Resmî test:** Tek DEV örneğinde Schema.org Validator, MedicalProcedure
  ve MedicalWebPage için `performer` uyarılarını gösterdi. Bu, 495 örneğin
  tamamının resmî serviste ayrı ayrı test edildiği anlamına gelmez.
- **Çözüm:** Yanlış alanı kaldırmak; gerçek hekim–hizmet ilişkisi gerekiyorsa
  [Physician.availableService](https://schema.org/Physician) gibi uygun ilişkiyi
  gerçek entity modeline göre kurmak. Yeni bir alanı doğrulamadan ikame etmemek.
- **Kabul:** Event olmayan bu düğümlerde `performer` yok; seçilen yeni ilişkinin
  domain/range ve gerçek içerik karşılığı doğrulanmış.
- **Kanıt:** `schema-inventory.csv`, `evidence/schema-jsonld-all.jsonl`.

### SCH-04 — `procedureType` için sınıf adları enum gibi kullanılıyor — P1 / Doğrulandı

| Çıkan değer | Sayı | Hedefli sözlük sonucu |
| --- | ---: | --- |
| PercutaneousProcedure | 33 | Gerçek MedicalProcedureType üyesi; tam enum IRI'siyle ifade edilmesi ayrıca doğrulanmalı. |
| TherapeuticProcedure | 63 | Bir MedicalProcedure **sınıfı**; bu enum'un üyesi değil. |
| DiagnosticProcedure | 51 | Bir MedicalProcedure **sınıfı**; bu enum'un üyesi değil. |
| SurgicalProcedure | 15 | Bir MedicalProcedure **sınıfı**; bu enum'un üyesi değil. |
| PreventiveTherapy | 3 | MedicalProcedureType enum üyesi değil. |

- **Kaynak:** `schema-procedure.html:41`; örneğin
  `content/tr/hizmetler/hipertansiyon/index.md:9`,
  `content/en/services/echocardiography/index.md:9`.
- **Sonuç:** 132/165 değer yanlış kavramsal sınıflandırmada. Sınıf adlarını
  `@type` ile işlem sınıfı seçmek için kullanmak ile `procedureType` enum değeri
  yapmak farklıdır.
- **Resmî test:** Tek DEV örneğindeki `TherapeuticProcedure` değeri için
  Schema.org Validator'da gerçekten **1 hata** gözlendi; diğer üretim
  örneklerine ait 132 sayısı kendi tam taramamızdan gelir.
- **Dayanak:** [MedicalProcedureType](https://schema.org/MedicalProcedureType),
  [DiagnosticProcedure](https://schema.org/DiagnosticProcedure),
  [TherapeuticProcedure](https://schema.org/TherapeuticProcedure).
- **Kabul:** Her hizmetin ana entity tipi içerikle uyumlu; `procedureType`
  veriliyorsa güncel enum'un gerçek üyesi ve uygun IRI/değer biçimi kullanılıyor.

### SCH-05 — Bütün hekim görsel referansları üretilen dosyada yok — P1 / Doğrulandı (statik çıktı)

- **Kapsam:** 679 graph içindeki hekim düğümü.
- **Değer:** `https://docdrhabibcil.com/img/istanbul-kardiyoloji-uzmani-doc-dr-habib-cil.webp`.
  Bu yol ayrı üretim çıktısında dosyaya karşılık gelmiyor.
- **Kaynak:** `schema.html:38` hardcoded URL kuruyor. Gerçekte hero,
  `home/hero.html:129–138` ile Hugo resource'tan işlenmiş, farklı adlı görseli
  yayımlıyor. Görselin `assets/img/` altında bulunması, aynı dosyanın
  `public/img/` altında otomatik yayımlandığının kanıtı değildir.
- **Etki:** Görünür hero resmi çalışırken JSON-LD görseli bulunamayabilir.
  Bu rapor canlı domain'de ölçülmüş bir 404 iddiası değildir.
- **Resmî test sınırı:** Google kod testindeki geçersiz image uyarısı
  localhost adresli DEV girdisine aittir; public üretim görselinin durumuyla
  özdeşleştirilmez.
- **Çözüm:** Graph için de yayımlanan resource'un gerçek permalink'ini kullanmak.
- **Kabul:** JSON-LD görsel adresi production dosyasında mevcut; gerçek HTTP
  GET 200 ve doğru MIME ile taranabilir.
- **Kanıt:** `evidence/schema-index.json`, bütün eksik hedef URL'leri
  `schema-summary.json` içinde `SCHEMA_IMAGE_MISSING_IN_BUILD`.

### SCH-06 — Çalışma saatleri görünür içerikle çelişiyor — P1 / Doğrulandı

- **URL:** `/iletisim/`, `/en/contact/`, `/ar/contact/`; aynı klinik graph'ı
  ana sayfa/pagination dahil 15 route'ta üretiliyor.
- **Görünür içerik:** Pazartesi–Cumartesi **08:00–18:00**.
- **Schema:** Hafta içi **09:00–18:00**, Cumartesi **09:00–14:00**.
- **Kaynak:** TR `content/tr/iletisim/index.md:27`; EN/AR contact dosyaları:27;
  `schema.html:70–72`.
- **Çözüm/kabul:** Kullanıcıdan doğrulanan gerçek çalışma saatini tek veri
  kaynağı yapmak; görünür üç dil ve bütün graph'lar birebir uyuşmalı.
- **Kanıt:** `evidence/schema-iletisim-index.json` ve ilgili kaynak satırları.

### SCH-07 — Hizmet konusu, anatomi ve sayfa amacı tek şablona indirgenmiş — P1 / Doğrulandı (örnekler); tüm sayfalar için tıbbi inceleme gerekli

- **Örnek 1:** `/en/services/echocardiography/` sayfasında
  `about: {"@type":"MedicalCondition","name":"Echocardiography - Heart Ultrasound Imaging"}`.
  Tanısal işlem adını hastalık/condition adı gibi modelleyen sabit şablon var.
- **Örnek 2:** `/hizmetler/alt-ekstremite-arter-hastaligi/` yalnız title/slug
  içeren kaynak dosyadan `bodyLocation:"Heart"` ve
  `procedureType:"PercutaneousProcedure"` varsayımları alıyor; title alt
  ekstremiteye işaret ediyor. Bu aynı zamanda içerik açığıdır.
- **Kapsam:** 165 hizmette aynı MedicalProcedure ana entity yaklaşımı;
  111 `bodyLocation:"Heart"` değeri. **111'inin yanlış olduğu iddia edilmez.**
- **Kaynak:** `schema-procedure.html:9,34–47,64`;
  `content/tr/hizmetler/alt-ekstremite-arter-hastaligi/index.md:1–4`.
- **Çözüm:** Hastalık bilgilendirmesi, test, işlem ve hizmet sunumunu gerçek
  içerik türüne göre ayırmak; anatomi/işlem varsayımını sessizce doldurmamak.
- **Kabul:** İlgili hekim tarafından doğrulanan sayfa–ana entity eşlemesi,
  klinik anlamı doğru anatomi ve görünür içeriğe dayanan özellikler.

### SCH-08 — İnceleme ve otorite iddiaları otomatik atanıyor — P1 / Güçlü aday

- **Kapsam:** 165 MedicalWebPage için `reviewedBy` ve `lastReviewed`;
  165 MedicalProcedure için `recognizingAuthority`.
- **Kaynak:** `schema-procedure.html:29,47,61–62`. `lastReviewed`, özel bir
  tıbbi inceleme kaydı yerine `.Lastmod` değerinden türetiliyor; dernek adı
  TR/diğer dil koşuluyla her hizmete ekleniyor.
- **Kesin bilinen:** Bu otomatik atama kodda ve çıktıda var. **Bilinmeyen:**
  gerçek tıbbi incelemenin yapılıp yapılmadığı veya derneğin ilgili işlemi
  tanımasına dair kaynak. Bunları “kesin sahte” diye sınıflamıyoruz.
- **Dayanak:** [reviewedBy](https://schema.org/reviewedBy),
  [lastReviewed](https://schema.org/lastReviewed),
  [recognizingAuthority/MedicalProcedure](https://schema.org/MedicalProcedure).
- **Kabul:** İddialar için gerçek review tarihi/kaydı ve gerekiyorsa otorite
  kaynağı; kanıt yoksa iddia üretilmemesi. Klinik koordinatı ve `priceRange`
  için de bağımsız doğrulama gerekiyor; mevcut public adresin doğruluğunu
  koordinata otomatik taşımamak gerekir.

### SCH-09 — Liste ve yardımcı sayfalar Article/BlogPosting oluyor — P2 / Doğrulandı

- **Kapsam:** 367 Article; bunların 355'inde `wordCount:0`.
  Tag/category/pagination yol heuristiği 361 Article route'unu işaretliyor;
  bu heuristik tek başına hata hükmü değildir. Blog liste/sayfalamasındaki
  12 route da BlogPosting + MedicalWebPage alıyor.
- **Somut örnekler:** `/tags/` Article, `/404.html` Article,
  `/iletisim/` Article, `/blog/` ve `/blog/page/2/` BlogPosting.
- **Kaynak:** `schema.html:98–120`; `.Kind` veya gerçek makale türü yerine
  path içeriği ve “home/service değil” koşulları kullanılıyor.
- **Çözüm/kabul:** Makale yalnız gerçek makale sayfasına; liste, iletişim,
  profil ve hata sayfası için gerçek amacına uygun tür. Tüm route'larda
  doğrulanmış şablon–schema eşlemesi ve Google Article koşullarının kontrolü.
- **Dayanak:** [Google Article](https://developers.google.com/search/docs/appearance/structured-data/article),
  [genel içerik politikası](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).

### SCH-10 — Boş ItemList ve yerelleştirme/kimlik modelinin gözden geçirilmesi — P2

- **Doğrulandı:** 12 home/pagination çıktısındaki ItemList'te
  `itemListElement` yok (`schema.html:124–131`). Arapça home listesi İngilizce
  ad/açıklama alıyor. Görünür hizmet listesini tanımlayan öğe bağlantıları yok.
- **Güçlü aday:** Aynı `#physician` hem Person hem Physician. Güncel sözlükte
  bu otomatik geçersizlik değildir, ancak LocalBusiness adayı olan Physician
  düğümlerinde adres yok; ayrı MedicalBusiness node'undaki adres aynı entity'ye
  otomatik taşınmaz. Gerçek kişi/ofis ayrımı ve LocalBusiness koşulları
  incelenmeli. Tek DEV örneğindeki Google testi address, priceRange ve image
  için kritik olmayan uyarılar verdi; LocalBusiness öğesini **geçerli** saydı.
  Bu nedenle eksik alanlar burada kritik Google doğrulama hatası ilan edilmez.
- **Kabul:** Varsa ItemList gerçek görünür hizmetleri referanslıyor; Arapça
  etiketler Arapça; hekim/klinik entity sınırı ve address ilişkisi doğrulanmış.

## Hatalı sayılmaması gerekenler ve olumlu kontroller

1. **MedicalScholarlyArticle vardır.** Mevcut output'ta 0 olması,
   `schema-scholarly.html:5` koşulunun gerçek yayın listesinde çalışmamasıyla
   uyumlu. `content/tr/yayinlar/_index.md` bir liste/section'dır; gerçek
   yayın-detay sayfası bu çıktıda saptanmadı. Her bilimsel yayını ayrı gerçek
   entity olarak sunma ilerideki içerik tasarımıdır; listeyi bir bilimsel
   makale ilan etmek doğru çözüm değildir.
2. **MedicalProcedure.status = EventScheduled sözlükte yok değildir.**
   Güncel property beklenen tipleri arasında EventStatusType var. Bunun genel
   tedavi bilgilendirme sayfasında neden “planlanmış” olduğu semantik olarak
   açıklanmıyor; bu yüzden P2 anlam/gereklilik incelemesidir, doğrudan
   bilinmeyen-property veya bilinmeyen-enum hatası değildir.
3. **Cardiovascular enum'u vardır.** `http://schema.org/Cardiovascular`
   referansını otomatik “Cardiology yazılmalıydı” diye hata saymak yanlıştır.
   Tutarlı HTTPS IRI tercih edilebilir; tek başına sıralama sorunu kanıtı değildir.
4. **MedicalWebPage vardır.** Özel Google rich result desteği olmaması onu
   geçersiz yapmaz. Google'ın [galerisi](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)
   Schema.org'un bütün sözlüğü değildir.
5. **JSON sözdizimi geçiyor:** 679 scriptte sıfır ayrıştırma hatası.
   Theme'in `head.html:186` çağrısı proje partial'ına resolve oluyor; ayrıca
   ikinci theme JSON-LD scripti tespit edilmedi. İçerik içine gömülü ilave
   scriptler de bütün-HTML taramasına dahildir; toplam her şemalı HTML'de bir.
6. **FAQ tekrarı tespit edilmedi:** 279 FAQPage, her ilgili sayfada birer tane;
   1.632 Question ve 1.632 Answer. Bu, bütün cevapların tıbben doğrulandığı veya
   her görünür FAQ'nın birebir eşlendiği anlamına gelmez. Google'ın [2026
   değişiklik kaydı](https://developers.google.com/search/updates) FAQ rich
   result gösterimini 7 Mayıs 2026'dan itibaren kaldırdığını belirtiyor.
   Görünür SSS içeriğinin yararı devam edebilir; sırf bu değişiklik için
   kullanıcıya yararlı SSS'yi silmek önerilmez.

## Mevcut schema kontrol scriptinin sınırı

`scripts/check_schema.py:42–123`, JSON scriptlerini topluyor ve FAQ sayı/ID
çıktısı veriyor. Geçersiz JSON'da hata yazıp `continue` ediyor (:53–57);
vocabulary/domain/range, breadcrumb dizisi, graph çelişkisi veya gerçek bilgi
doğruluğu kontrolü yapmıyor. Bu scriptin başarılı process çıkışı bütün
schema'ların geçerli olduğunun kabul testi olamaz. Resmî doğrulayıcı çıktısı
yerine de kullanılamaz.

## Ham kanıt ve yeniden üretim

- `schema-inventory.csv`: 3.322 top-level düğüm ve dört katmana ait durum alanları.
- `evidence/schema-summary.json`: bütün sayımlar, type/property kapsamı ve
  her kontrol için tam URL listesi; otomatik semantic flags'in bir kısmı
  yalnız inceleme adayıdır.
- `evidence/schema-pages.json`: 976 HTML route'u, graph değerleri, script
  konumları ve çelişki detayları.
- `evidence/schema-jsonld-all.jsonl`: 679 scriptin orijinal metni, SHA-256,
  çıktı dosyası ve URL'si. Minify edilmiş HTML'deki kaynak konumu çoğunlukla
  satır 1 olduğundan property/JSON yolu ve dosya adı kullanılır.
- `evidence/schema-*-index.json`: ana sayfa, hizmet, iletişim, liste ve 404
  örneklerinin küçük bağımsız kanıtları.

İlk düzeltme sırası: SCH-01/02 breadcrumb üretimi → SCH-03/04 property/enum
modeli → SCH-05 yayımlanan görsel → SCH-06 gerçek saatler → SCH-07/08 tıbbi
semantik ve kanıt yönetimi. Bunlar aynı değişiklikte topluca uygulanmak
zorunda değildir; her biri kendi kabul testiyle kapatılmalıdır.

**Doğrulanamadı:** canlı Google rich result görünümü, Search Console schema
hataları/manual action, bütün FAQ metinlerinin görünür içerikle otomatik tam
eşlemesi, gerçek tıbbi review kayıtları, kurum onayı, koordinat/fiyat
dayanağı ve canlı URL'lerin HTTP/MIME sonuçları. Bu eksikler eldeki kaynak
ve statik-output bulgularını geçersiz kılmaz; sonuçlarının sınırını belirler.

## Tamamlama turundaki bağımsız kontrol

24 Kasım 2026 tamamlama turunda yukarıdaki önceki denetim kanıtları korunarak
`schema.html`, `schema-procedure.html`, `schema-faq.html`,
`schema-scholarly.html` ve mevcut kontrol scriptinin kapsamı yeniden okundu.
Ana semantik hükümleri değiştirecek bir çelişki saptanmadı. Yeni kontrol,
resmî doğrulayıcıların yeniden çalıştırılması olarak sunulmaz; yukarıdaki
validator sonuçları önceki aynı gün DEV kod testine aittir.

Google'ın [güncel değişiklik kaydı](https://developers.google.com/search/updates)
yeniden açıldı: 8 Mayıs 2026 kaydı, FAQ zengin sonucunun 7 Mayıs'tan itibaren
gösterilmeyeceğini; 15 Haziran kaydı ilgili belgenin kaldırıldığını bildiriyor.
Bu, geçerli `FAQPage` semantiğinin veya yararlı görünür SSS'nin kaldırılmasını
gerektirmez. [MedicalProcedure](https://schema.org/MedicalProcedure),
[MedicalProcedureType](https://schema.org/MedicalProcedureType),
[Physician](https://schema.org/Physician), [performer](https://schema.org/performer),
[Cardiovascular](https://schema.org/Cardiovascular) ve
[MedicalScholarlyArticle](https://schema.org/MedicalScholarlyArticle) tanımları
ayrıca yeniden açılarak hedefli olarak kontrol edildi.

Yeni kaynak kontrol kaydı: `evidence/recheck-schema-official-sources.json`.
Bağımsız tam çıktı taraması `evidence/recheck-schema.py` çalıştırıldı
(çıkış kodu 0); ham sonuç `evidence/recheck-schema-output.json` içindedir.
976 HTML, 679 script, 0 JSON parse hatası, 3.322 top-level düğüm,
628 sırası kesintili/tekrarlı breadcrumb route'u, 165 çelişen @id route'u,
495 `performer` düğümü ve 132 enum-üyesi-olmayan `procedureType` değeri
yeniden sayıldı; önceki sonuçlarla uyuştu. Microdata/RDFa ve aynı sayfada
FAQPage tekrarı bulunmadı. Bu taramanın JSON
ayrıştırması, düğüm sayısı ve hedefli graph kontrolleri için kanıt sağladığı;
tam JSON-LD expansion, klinik doğruluk, public HTTP veya Google indeks
doğrulaması olmadığı korunur.

## Yeni üretim derlemesiyle eşitlik

Bu tur root denetiminde ayrıca ayrı minify production build alındı (exit0).
`evidence/recheck-production-build.json` tam komut/env/hedefi kaydeder.
`evidence/recheck-build-comparison.json`: önceki/yeni **976 HTML byte-eş**,
fark0. Bu dosyanın mevcut çıktı sayımları yeni build için de geçerlidir;
Google/Schema.org resmî servislerinin yeni production testinin yapıldığı
anlamına gelmez. Canlı Netlify byte eşitliği hâlâ doğrulanmadı.
