# Birleştirilmiş bulgular — 24 Kasım 2026

Bu rapor mevcut çalışma ağacından ayrı hedefe üretilen **production çıktısını**,
kaynak incelemelerini ve çalışan **development** sunucusundaki gerçek tarayıcı
gözlemlerini birleştirir. Kaynak kodu, içerik, çalışan sunucu, DNS, Netlify veya
hesap ayarları değiştirilmedi. İzole production çıktısının canlı Netlify
sürümüyle byte eşitliği doğrulanmadı.

## Kanıtın nasıl okunacağı

**Doğrulandı** belirtilen kaynak/çıktı veya gerçek tarayıcı olgusunu ifade eder;
statik tarama canlı HTTP veya Google indeks sonucu değildir. **Güçlü aday**
için kullanıcıya sayısal etki veya dış olgu eksiktir. **Doğrulanamadı / NOT_RUN**
gerekli verinin/testin olmadığını bildirir. P0 kritik yayın/erişim engeli;
P1 önemli işlev/doğruluk; P2 iyileştirme/ölçüm/tasarım kararı; P3 bakım.
**NET-01 kapsamında mevcut web adreslerinin DNS çözümlemesini engelleyen P0
durumu doğrulandı.** Kesintinin geçmiş süresi, kayıtları kimin değiştirdiği,
registrar kök nedeni veya Google cezası hakkında doğrulanmış sonuç yoktur.

Aynı konu iki sorun sayılmadı: **CT-02 → SCH-06** (saatler),
**CT-07 → HOST-01** (formlar), UI-05’in hareket kısmı **PERF-02** içinde;
HOST-05’in CDN bilgisi **PERF-01/03** ile ilişkilidir. Başlık sayısı kritik
hata sayısı değildir; adaylar ve taşıma kapıları da yer alır.

Ayrıntılar: [schema](03-schema-audit.md), [performans](04-performance.md),
[içerik kanıtı](evidence/content-notes.md), [statik SEO](evidence/static-findings.md),
[UI kaynak incelemesi](evidence/ui-source-notes.md),
[sunucuya geçiş](07-self-hosting-readiness.md).
Aşağıdaki kaynak yolları depo köküne, kanıt adları `evidence/` klasörüne göredir.

## Kapsam özeti

| Kanıt tabanı | Gerçek kapsam |
| --- | --- |
| Kaynak içerik | 364 Markdown: TR 160 / EN 102 / AR 102; Hugo bağımsız kaynak listesi 361; üç teşekkür dosyası leaf-bundle kaynağı |
| Üretilmiş HTML | 976 dosya: 297 alias, 3 özel 404, 24 pagination; alias/404 hariç 676 route |
| Ayrı canonical | 652: TR 258 / EN 196 / AR 198; Google’da 652 sayfa indeksli demek değildir |
| HTML varlık taraması | Eksik yerel HTML asset referansı 0; schema görselleri ayrı kontrol |
| JSON-LD | 679 route, 679 script, 3.322 top-level node; JSON parse hatası 0 |
| Gerçek tarayıcı görünümü | Localhost development; 320/360/390/430/768/1024/1280/1440/1920 CSS px; DPR 1 |
| Development tanı koşuları | Desktop 1280×900 ve mobil viewport 390×844; üçer tekrar; production/saha/Lighthouse benchmark değil |
| Resmî doğrulayıcı | Bir development hizmet JSON-LD örneği kod girişiyle Schema.org ve Google Rich Results Test’te çalıştırıldı; canlı URL crawl değil |
| Bağımsız ağ yüzeyi | Tarayıcıdan Google Public DNS JSON; apex A/AAAA NODATA, www A/CNAME NXDOMAIN; kontrol alan adı başarıyla çözüldü; ikinci resolver testi yok |

Tam URL tablosu: [02-url-and-template-inventory.csv](02-url-and-template-inventory.csv).
Farklı sayım birimleri birbirine eklenmemelidir.

## DNS ve mevcut yayına erişim

### NET-01 — Web adreslerinin DNS çözümlemesi yok

**P0 · Doğrulandı — tek kamu resolver hizmetinden gerçek DNS yanıtları**

- **URL/kapsam:** `https://docdrhabibcil.com/` ve `https://www.docdrhabibcil.com/`; Google Public DNS JSON API'de A/AAAA/NS ve www A/CNAME sorguları.
- **Kaynak:** Üretim alan adı `hugo.toml:1`; dış kanıt kaynağı `https://dns.google/resolve?name=docdrhabibcil.com&type=A` ve `browser-public-dns.json` içindeki diğer tam sorgu URL'leri.
- **Olgu / kök neden:** Apex A ve AAAA yanıtları Status 0, Answer yok, SOA Authority var: NODATA. Apex NS sorgusu dört `dns*.p08.nsone.net` kaydını döndürüyor. www A/CNAME Status 3: NXDOMAIN. Aynı hizmetten `google.com` A yanıtı başarılı; bu kanıt shell ortamının genel DNS kısıtından bağımsızdır. Web hostname'lerinin adres çözümlemesi mevcut yanıtlarda yok; registrar/zone değişikliğinin nedeni ve origin'in durumu bilinmiyor. SOA primary adındaki p01 ile NS kümesindeki p08 farkı tek başına misconfiguration kanıtı sayılmadı.
- **Öneri:** Mevcut yetkili zone ve amaçlanan yayın hedefi doğrulansın; Netlify geri dönüşü veya kendi sunucusu için doğru apex/www hedefleri, seçilen platformun gerçek gereksinimleriyle tanımlansın. Bu denetimde DNS değiştirilmedi; sunucu dosyalarını taşımak tek başına bu çözümleme sorununu gidermez.
- **Kabul:** Yetkili kaynaktan ve en az iki bağımsız resolver'dan doğru apex/www cevapları; seçilen adres politikasında çalışan HTTP→HTTPS ve www/apex yönlendirmesi; geçerli TLS; ana sayfa, robots ve sitemap için gerçek başarılı HTTP sonuçları. DNS dışındaki origin/TLS kabulü ayrı kanıt ister.
- **Kanıt:** [browser-public-dns.json](evidence/browser-public-dns.json); önceki [network-probes.json](evidence/network-probes.json) shell denemeleri ayrı sınırlı kanıt. Güncel JSON yanıt yorumları [Google Public DNS API](https://developers.google.com/speed/public-dns/docs/doh/json) tanımıyla ele alınır.

## Arayüz, gezinme ve erişilebilirlik

### UI-01 — Masaüstü menü sözcükleri bölünüyor

**P1 · Doğrulandı — gerçek tarayıcı + kaynak**

- **URL/kapsam:** http://localhost:1313/; 1024/1280/1440/1920 CSS px
- **Kaynak:** layouts/partials/header/basic.html:25,212–220; layouts/partials/header/fixed.html:6; assets/css/custom.css:20–23; themes/blowfish/assets/css/main.css:146–150; config/_default/params.toml:70–78
- **Olgu / kök neden:** Altı menü etiketinin tamamı dört genişlikte iki satır; anchor yüksekliği 48 px. Computed white-space normal, word-break break-word, flex-shrink 1. Uzun marka başlığı ve menü daralan aynı satırda; nowrap yalnız marka nav’ını kapsıyor. disableTextInHeader header altında tanımlıyken şablon kökte arıyor. Gerçek md eşiği 853 px (tema config:14; compiled CSS:2707–2714).
- **Öneri:** Başlık parametresi/koşulu, kullanılabilir genişlik, flex ve masaüstü breakpoint’i birlikte düzeltilmeli; tema link bölme kuralı menü etiketlerine uygulanmamalı.
- **Kabul:** 852/853/854 sınırı, 320–1920 px matrisi ve gerçek %200 zoom’da kırılan, kırpılan veya kaybolan etiket yok; sığmadığı yerde erişilebilir mobil menü. Aşırı font küçültme/overflow gizleme yeterli değil.
- **Kanıt:** browser-layout-observations.json; ui-static-extract.json; browser-menu-1280-crop.jpg

### UI-02 — Uzmanlık kartı yanlış değeri gösteriyor

**P1 · Doğrulandı — gerçek tarayıcı + production çıktı**

- **URL/kapsam:** /, /en/, /ar/
- **Kaynak:** i18n/tr.yaml:12,25–26; layouts/partials/home/hero.html:149–150
- **Olgu / kök neden:** Türkçe kart “Uzmanlık → Damar Açma”. Doğrudan değer ve fallback aynı yanlış alanı gösteriyor. EN “Vascular Interventions”, AR “فتح الأوعية الدموية”.
- **Öneri:** Kartın hedefini “Girişimsel Kardiyoloji” yapmak; doğrudan/fallback ve EN/AR anlam karşılıklarını birlikte düzenlemek. Sitenin diğer yerlerindeki damar açma terimlerini silmek gerekmiyor.
- **Kabul:** Üç dilde istenen uzmanlık anlamı görünür; fallback aynı anlamı korur; dar ekran ve zoom’da kart taşmaz.
- **Kanıt:** browser-layout-observations.json; ui-static-extract.json

### UI-03 — Mobil menünün klavye semantiği ve Escape davranışı eksik

**P1 · Doğrulandı — belirli runtime senaryosu + kaynak**

- **URL/kapsam:** http://localhost:1313/hizmetler/dizalti-damar-tikanikligi/; 390×844, DPR 1
- **Kaynak:** layouts/partials/header/basic.html:94–107; themes/blowfish/assets/js/mobilemenu.js:7–33
- **Olgu / kök neden:** Açıcı DIV, role yok, tabIndex -1; kapatıcı LI/SPAN. Click menüyü açıyor; Escape sonrası wrapper visible/opacity 1 ve body overflowY hidden kalıyor. Kod yalnız click dinliyor. Tam ardışık Tab kapsamı/ekran okuyucu çalıştırılmadı.
- **Öneri:** Semantik düğme, erişilebilir ad/expanded/controls, klavye ve odak yönetimi sağlamak.
- **Kabul:** Tab ile açıcıya ulaşılır; Enter/Space açar; Escape kapatır; odak açıcıya döner; açık durumda beklenmedik arka plan etkileşimi ve scroll kilidi kalmaz.
- **Kanıt:** browser-keyboard-observations.json; ui-static-extract.json

### UI-04 — Modal odağı kaçıyor; arama kapanınca açıcıya dönmüyor

**P1 · Doğrulandı — belirli runtime senaryoları**

- **URL/kapsam:** http://localhost:1313/hizmetler/dizalti-damar-tikanikligi/; 390×844
- **Kaynak:** layouts/partials/extend-footer.html:568–608; layouts/partials/search.html:1–23; assets/js/search.js:94–114
- **Olgu / kök neden:** Randevu açılınca close button odaklanıyor; oradan Shift+Tab arka plandaki appointment-button’a kaçıyor. Escape kapatıp odağı geri veriyor (olumlu). Aramada modal role ve input aria-label yok; Escape sonrası odak BODY oluyor. Tab trap/inert kaynakta yok. Sonuç yokken Enter’ın form yenileme riski henüz denenmedi.
- **Öneri:** Modal içi odak döngüsü, arka plan etkileşimsizliği, dialog/input adı ve doğru açıcıya odak dönüşü; boş sonuç Enter davranışını ayrıca test etmek.
- **Kabul:** Her iki modalde Tab/Shift+Tab odağı içeride tutar; Escape kapatır ve açıcıya döner; ekran okuyucu adlandırması ve boş/hata/yükleme arama durumları doğrulanır.
- **Kanıt:** browser-keyboard-observations.json; ui-source-notes.md

### UI-05 — Ortak kontrollerde dil karşılıkları eksik

**P2 · Doğrulandı — kaynak; boş arama mesajı runtime**

- **URL/kapsam:** /, /en/, /ar/ ve ortak kontroller
- **Kaynak:** layouts/partials/header/basic.html:38–79; layouts/partials/extend-footer.html:4–12,21; assets/js/search.js:154–161
- **Olgu / kök neden:** Arama/tema accessible adları İngilizce; AR disclaimer ve WhatsApp adı İngilizce fallback. Gerçek Türkçe sayfada sonuçsuz sorgu “No results found…” gösterdi. Header title i18n anahtarındaki başlangıç boşluğu ayrıca kontrol gerektiriyor. AR kök dir=rtl doğru; bütün RTL görünümü geçti denmiyor.
- **Öneri:** Görünen ve duyurulan metinleri i18n üzerinden üç dile taşımak; AR fiziksel left/right ve ikon sırasını görsel olarak denetlemek.
- **Kabul:** Kontrollerin metin/adları sayfa diliyle uyumlu; AR okuma sırası ve yerleşim testli. Hareket tercihi ayrı PERF-02’de.
- **Kanıt:** browser-keyboard-observations.json; ui-source-notes.md

### UI-06 — JS olmayan ortamda bazı temel eylemler için fallback yok

**P2 · Güçlü aday — kaynak doğrulandı, JS-off NOT_RUN**

- **URL/kapsam:** Ana sayfalar ve mobil gezinme
- **Kaynak:** layouts/partials/home/hero.html:88–100; layouts/partials/header/basic.html:94–107
- **Olgu / kök neden:** Hero randevu çağrısı yalnız inline JS ile diğer button’a tıklıyor; mobil menü de JS’ye bağlı. WhatsApp ve hizmet CTA’ları gerçek anchor olduğundan daha dayanıklı. JS-off tarayıcı testi yapılmadı.
- **Öneri:** JS/CDN başarısızlığında açık, gerçek bağlantılı iletişim/randevu ve gezinme yolu sağlamak.
- **Kabul:** JS kapalıyken içerik okunur; en az bir görünür iletişim/hizmet yolu çalışır; işlevsiz görünen temel kontrol bırakılmaz.
- **Kanıt:** ui-source-notes.md

## Yapılandırılmış veri

### SCH-01 — Breadcrumb sıraları tekrarlanıyor

**P1 · Doğrulandı — bütün üretim çıktısı**

- **URL/kapsam:** /hizmetler/hipertansiyon/ dahil 628 route
- **Kaynak:** layouts/partials/schema.html:82–87
- **Olgu / kök neden:** İlk breadcrumb dizilerinin position değerleri 1,3,3. Home atlanırken ancestor indeksi korunuyor; son öğe liste uzunluğuyla yeniden 3 oluyor. Google’ın temsilci kod testini geçmesi bu yapısal belirsizliği ortadan kaldırmıyor.
- **Öneri:** Sıraları yalnız gerçekten eklenen öğelerden üretmek.
- **Kabul:** Bütün BreadcrumbList’lerde benzersiz artan 1..N sırası; tüm route’ların kontrolü ve temsilci resmî kod testi.
- **Kanıt:** schema-summary.json; schema-hizmetler-hipertansiyon-index.json

### SCH-02 — Aynı breadcrumb kimliğinin çelişen tanımları var

**P1 · Doğrulandı**

- **URL/kapsam:** 165 hizmet route’u; TR/EN/AR hipertansiyon/echocardiography örnekleri
- **Kaynak:** layouts/partials/schema.html:78–95; layouts/partials/schema-procedure.html:30–32,68–79
- **Olgu / kök neden:** Aynı #breadcrumb için iki farklı itemListElement veriliyor. İkinci dizi TR /tr/hizmetler/, EN/AR /services/ ve dil kökü yerine / kullanıyor. TR migration redirect’i bulunduğundan eski yol otomatik canlı 404 sayılmadı.
- **Öneri:** Görünür breadcrumb ile aynı veriden tek tanım üretmek; meşru farklı yollar varsa kimliklerini ayırmak.
- **Kabul:** Aynı @id için çelişen dizi kalmaz; her dilde hedefler doğru canonical 200 adreslerine gider.
- **Kanıt:** schema-pages.json/conflicting_ids; hizmet örnek JSON’ları

### SCH-03 — performer yanlış domain’lerde kullanılıyor

**P1 · Doğrulandı — çıktı/sözlük; temsilci validator uyarıları**

- **URL/kapsam:** 165 hizmette 495 düğüm: MedicalProcedure, MedicalWebPage, BreadcrumbList
- **Kaynak:** layouts/partials/schema.html:146–150
- **Olgu / kök neden:** Partial’ın döndürdüğü üç nesnenin tamamına performer merge ediliyor. Güncel sözlükte performer Event property’si. Temsilci Schema.org kod testi MedicalProcedure ve MedicalWebPage için performer uyarılarını gösterdi; üçüncü uyarının ayrıntısı açılmadı.
- **Öneri:** Uygunsuz alanı kaldırmak; gerçek hekim–hizmet ilişkisini ancak doğrulanmış domain/range ve entity modeliyle kurmak.
- **Kabul:** Event olmayan bu düğümlerde uygunsuz performer yok; seçilen ilişki sözlük ve gerçek içerikle uyumlu; resmî testte ilgili uyarılar kapanmış.
- **Kanıt:** schema-inventory.csv; schema-jsonld-all.jsonl; browser-validator-results.json

### SCH-04 — İşlem sınıfları procedureType enum değeri gibi yazılıyor

**P1 · Doğrulandı — çıktı/sözlük; temsilci validator hatası**

- **URL/kapsam:** /en/services/echocardiography/ ve /hizmetler/dizalti-damar-tikanikligi/; 132/165 değer
- **Kaynak:** layouts/partials/schema-procedure.html:41; ilgili içerik front matter’ı:9
- **Olgu / kök neden:** TherapeuticProcedure/DiagnosticProcedure/SurgicalProcedure gibi sınıf adları MedicalProcedureType üyeleri yerine kullanılıyor. Temsilci Schema.org testinde TherapeuticProcedure geçersiz procedureType hatası çıktı. 33 PercutaneousProcedure değeri otomatik yanlış sayılmadı; IRI biçimi ayrıca doğrulanmalı.
- **Öneri:** Ana entity sınıfı ile işlem enum’unu ayırıp her hizmetin gerçek tıbbi anlamıyla eşlemek.
- **Kabul:** 132 uyuşmazlık giderilir; kalan enum’lar güncel gerçek üye/değer biçimindedir; görünür konu ve resmî test uyumlu.
- **Kanıt:** schema-summary.json; schema-inventory.csv; browser-validator-results.json

### SCH-05 — Schema hekim görseli yayımlanan dosyaya gitmiyor

**P1 · Doğrulandı — statik production hedefi**

- **URL/kapsam:** 679 graph; /img/istanbul-kardiyoloji-uzmani-doc-dr-habib-cil.webp
- **Kaynak:** layouts/partials/schema.html:38; layouts/partials/home/hero.html:129–138
- **Olgu / kök neden:** Hardcoded JSON-LD görsel yolu izole production’da yok; görünür hero farklı işlenmiş resource URL’sinde var. Temsilci RRT’nin localhost image uyarısı tek başına production 404 kanıtı değildir; eksik production dosyası ayrı statik kanıttır.
- **Öneri:** Graph içinde de yayımlanmış resource’un gerçek permalink’ini kullanmak.
- **Kabul:** Production hedef dosyası var; gerçek GET 200, doğru MIME ve taranabilirlik ayrıca kanıtlı.
- **Kanıt:** schema-index.json; schema-summary.json/SCHEMA_IMAGE_MISSING_IN_BUILD

### SCH-06 — Görünür çalışma saatleriyle schema çelişiyor

**P1 · Doğrulandı; CT-02 aynı bulgunun alias’ı**

- **URL/kapsam:** /iletisim/, /en/contact/, /ar/contact/; klinik graph’ı 15 route’ta
- **Kaynak:** content/tr/iletisim/index.md:27; EN/AR contact/index.md:27; layouts/partials/schema.html:70–72
- **Olgu / kök neden:** Görünür bilgi Pzt–Cmt 08:00–18:00; schema Pzt–Cum 09:00–18:00 ve Cmt 09:00–14:00. Bağımsız sabit bilgiler çelişiyor. Gerçek saat ve GBP kaydı görülmedi.
- **Öneri:** Gerçek saati kullanıcı/klinik kaynağıyla doğrulayıp tek veri kaynağına bağlamak.
- **Kabul:** Üç dilde görünür bilgi, bütün graph’lar ve erişilebilen yetkili işletme kaydı uyuşur.
- **Kanıt:** schema-iletisim-index.json; content-evidence.json

### SCH-07 — Hastalık/test/işlem tek semantik şablona zorlanıyor

**P1 · Örneklerde doğrulandı; kapsamın tamamı tıbbi inceleme gerektiriyor**

- **URL/kapsam:** /en/services/echocardiography/; /hizmetler/alt-ekstremite-arter-hastaligi/
- **Kaynak:** layouts/partials/schema-procedure.html:9,34–47,64; content/tr/hizmetler/alt-ekstremite-arter-hastaligi/index.md:1–4
- **Olgu / kök neden:** Echocardiography test adı MedicalCondition oluyor. Alt ekstremite başlıklı boş kaynağa Heart/Percutaneous varsayımları atanıyor. 165 hizmette aynı yaklaşım; 111 Heart değerinin hepsinin yanlış olduğu iddia edilmiyor. EventScheduled sözlükte geçerli, bilgilendirme sayfasındaki anlamı ayrıca gerekçelenmeli.
- **Öneri:** Ana entity, anatomi ve işlem tipini sayfa konusu/hekim incelemesiyle eşlemek; sessiz genel varsayımları kaldırmak.
- **Kabul:** Her sayfanın ana entity’si ve tıbbi alanları gerçek içerikle uyumlu; hastalık, test, işlem ve hizmet rolleri ayrı.
- **Kanıt:** İlgili schema örnek JSON’ları; 03-schema-audit.md

### SCH-08 — Review ve otorite iddialarının dayanağı doğrulanamıyor

**P1 · Güçlü aday — otomatik atama doğrulandı**

- **URL/kapsam:** 165 hizmet sayfası
- **Kaynak:** layouts/partials/schema-procedure.html:29,47,61–62
- **Olgu / kök neden:** Lastmod gerçek inceleme kaydı yerine lastReviewed oluyor; meslek derneği genel recognizingAuthority olarak ekleniyor. İnceleme/kurum dayanağı alınmadı; bunlara kesin sahte denmedi. Koordinat ve priceRange için de bağımsız teyit gerekli.
- **Öneri:** Gerçek inceleme tarihi/kaydı ve gerektiğinde otorite kaynağıyla doğrulamak; dayanak yoksa iddiayı üretmemek.
- **Kabul:** İnceleme sahibi/tarihi gerçek kayıtla eşleşir; otorite, koordinat, fiyat gibi dış olgular teyitli; otomatik tarih klinik review kanıtı sayılmaz.
- **Kanıt:** schema-inventory.csv; 03-schema-audit.md

### SCH-09 — Liste/iletişim/hata sayfaları makale oluyor

**P2 · Doğrulandı**

- **URL/kapsam:** /tags/, /404.html, /iletisim/, /blog/, /blog/page/2/
- **Kaynak:** layouts/partials/schema.html:98–120
- **Olgu / kök neden:** İlk üç örnek Article, blog listeleri BlogPosting+MedicalWebPage alıyor. 367 Article’ın 355’inde wordCount 0. Gerçek sayfa türü yerine path ve home/service değil koşulu belirleyici.
- **Öneri:** Yalnız gerçek makaleyi Article/BlogPosting yapmak; liste/profil/iletişim/hata sayfalarını gerçek amaçlarına göre modellemek.
- **Kabul:** Şablon–schema matrisi her route’ta doğru; ilgili Google Article koşulları ayrı kontrol edilmiş.
- **Kanıt:** schema-tags-index.json; schema-blog-index.json; schema-404.json; schema-inventory.csv

### SCH-10 — Boş hizmet ItemList’i ve entity sınırı

**P2 · Boş liste doğrulandı; entity modeli güçlü aday**

- **URL/kapsam:** 12 home/pagination çıktısı; hekim node’u ortak
- **Kaynak:** layouts/partials/schema.html:29–42,124–131
- **Olgu / kök neden:** ItemList’te itemListElement yok; AR listesi İngilizce ad/açıklama alıyor. Person+Physician birleşimi sözlükte otomatik geçersiz değil; ayrı MedicalBusiness adresinin bu node’a kendiliğinden aktarılacağı varsayılamaz. Temsilci RRT LocalBusiness’i geçerli bulup adres/fiyat/görsel için kritik olmayan uyarı verdi.
- **Öneri:** Listeyi gerçek görünür hizmetlere bağlamak; hekim/ofis kimlik ve adres ilişkisini gerçek model/Google koşullarıyla netleştirmek.
- **Kabul:** Liste dolu ve doğru dilde; kişi/ofis entity sınırı ve adres ilişkileri doğrulanmış; isteğe bağlı uyarılar kritik hata diye sunulmaz.
- **Kanıt:** schema-index.json; schema-ar-index.json; browser-validator-results.json

## İç bağlantı, dil ve tarama mimarisi

### STATIC-01 — Çözülemeyen iç bağlantılar var

**P1 · Statik doğrulandı; canlı HTTP 404 testi ayrı**

- **URL/kapsam:** 40 kaynak route; /en/services/myocardial-infarction/ ve İngilizce blog CTA örnekleri
- **Kaynak:** content/en/services/myocardial-infarction/index.md:191; content/en/blog/aortic-aneurysm/index.md:505
- **Olgu / kök neden:** İlan edilmiş TR redirect’i sonrası 66 kullanım, 42 hedef çözülemiyor. Literal false/, yanlış /contact/, prefixesiz /services/ ve eksik AR hedefler var. Redirect ile zaten çözülen 32 eski kullanım bu sayıya tekrar eklenmedi.
- **Öneri:** Linkleri gerçek canonical hedeflerle eşlemek; CTA’larda doğru dilde iletişim yolunu kullanmak.
- **Kabul:** Tam çıktı taramasında çözülemeyen link 0; randevu yolu doğru dilde; gerçek HTTP durumları ayrıca kaydedilmiş.
- **Kanıt:** static-link-triage.json; static-broken-links.json

### STATIC-02 — Pagination canonical/alternate’ları ilk sayfaya dönüyor

**P2 · Doğrulandı**

- **URL/kapsam:** /blog/page/2/, /en/blog/page/2/ ve toplam 24 pagination
- **Kaynak:** themes/blowfish/layouts/partials/head.html:32; themes/blowfish/layouts/_default/list.html:70; layouts/partials/extend-head-uncached.html:26–33
- **Olgu / kök neden:** Canonical liste ilk sayfasına; alternate da ilk sayfa translation permalink’lerine gidiyor. 72 hreflang işareti aynı kök nedene ait. 15 gerçek liste pagination’ı ve 9 gereksiz home kopyası ayrılmalı; Google’ın neyi indekslediği bilinmiyor.
- **Öneri:** Gerçek pagination’a kendi canonical’ını ve varsa eşdeğer pagination alternate’ını üretmek; home kopyalarının gerekliliğini değerlendirmek.
- **Kabul:** 24 canonical ve 72 self/return kontrolü doğru; normal sayfaların zaten geçen dil eşlemeleri bozulmamış.
- **Kanıt:** static-canonical-issues.json; static-hreflang-issues.json

### STATIC-03 — Sitemap sahipliği ve dil keşfi parçalı

**P2 · Doğrulandı**

- **URL/kapsam:** /sitemap.xml, /en/sitemap.xml, /ar/sitemap.xml, /tr/sitemap.xml, /hizmetler/sitemap.xml
- **Kaynak:** static/sitemap.xml:2–10; static/robots.txt:10; layouts/_default/sitemap.xml:4–10; layouts/_default/home.globalindex.xml:5; hugo.toml:81–84
- **Olgu / kök neden:** Kök XML dil index’i değil 258 TR urlset; EN196/AR198. TR ve hizmetler sitemap’i kökle byte-eş. Üç dilin birleşiminde 652 canonical’ın hepsi mevcut; kanıtlanmış sitemap döngüsü veya tüm dilin indekslenemezliği yok.
- **Öneri:** Tek sahipli kök dil index’i veya açık üç sitemap bildirimi politikası kurmak.
- **Kabul:** Geçerli XML, doğru dil kapsaması, 652 canonical, gerçek HTTP 200 ve redirect döngüsü yok.
- **Kanıt:** static-sitemaps.json; static-not-in-any-sitemap.json

### STATIC-04 — İngilizce hizmet kartının anchor’ı yanlış

**P2 · Statik doğrulandı; scroll uçtan uca NOT_RUN**

- **URL/kapsam:** /en/ → /en/services/#pacemaker-and-electrophysiology; 4 home/pagination kullanımı
- **Kaynak:** content/en/_index.md:39; content/en/services/_index.md:67
- **Olgu / kök neden:** Gerçek bölüm ID’si pacemaker-electrophysiology; kart farklı anchor kullanıyor.
- **Öneri:** Kartı gerçek sabit bölüm ID’sine bağlamak.
- **Kabul:** Tıklama doğru bölüme kayar; sabit header başlığı örtmez; aynı kartın pagination kopyaları da doğru.
- **Kanıt:** static-broken-fragments.json

### STATIC-05 — Boş paralel taxonomy benzeri sayfalar var

**P2 · Doğrulandı; organik etkisi ölçülmedi**

- **URL/kapsam:** /tags/girisimsel-kardiyoloji/ ve ayrı /tags/girişimsel-kardiyoloji/ örneği
- **Kaynak:** content/tr/tags/girisimsel-kardiyoloji.md:2–3; kaynak CSV’deki diğer normal tag/category page’ler
- **Olgu / kök neden:** 49 tag+6 category normal page yalnız front matter; 53’üne başka HTML sayfadan anchor yok. 346 taxonomy ailesinin 652 canonical içindeki oranı tek başına hata değil; sitemap/search keşfi yine mümkün.
- **Öneri:** Normal page/gerçek term ayrımını ve boş paralel URL’leri içerik ihtiyacına göre düzenlemek; yararlı arşivleri korumak.
- **Kabul:** Gerekli birleştirmelerde URL/301 haritası ve iç linkler doğru; toplu noindex/silme kararı gerekçesiz uygulanmamış.
- **Kanıt:** static-empty-manual-taxonomy-pages.json; static-orphan-candidates.json

### STATIC-06 — Dil fallback sonuçları açık politika/etiket gerektiriyor

**P2 · Veri doğrulandı; ürün kararı**

- **URL/kapsam:** /index.json, /en/index.json, /ar/index.json
- **Kaynak:** themes/blowfish/layouts/_default/index.json:2–5
- **Olgu / kök neden:** Her indeks 423 kayıt. TR:258TR+81EN+84AR; EN:143TR+196EN+84AR; AR:145TR+80EN+198AR. Bu bilinçli lang.Merge fallback’i; dosyaların hash’leri farklı, hepsi aynı indeks değil. Gerçek arama sonucu örneklemesi tamamlanmadı.
- **Öneri:** Seçili dil ve çeviri fallback politikasını belirlemek; gerekirse dil etiketi/filtre sağlamak.
- **Kabul:** Mevcut dil eşdeğeri varken başka dil hedefi tercih edilmez; fallback dili açıktır; dil değiştirme ve sonuç linki testlidir.
- **Kanıt:** static-search-indexes.json

### STATIC-07 — Metadata tekrarları sayfa amaçlarını ayırmıyor

**P2 · Doğrulandı — havuz bulgusu**

- **URL/kapsam:** 16 duplicate-title grubu/48 URL; 9 description grubu/379 URL
- **Kaynak:** themes/blowfish/layouts/partials/head.html:20–21; ilgili URL’lerin içerik metadata’sı
- **Olgu / kök neden:** Önemli bölüm pagination/taxonomy ve site description fallback’i. Bunlar 379 ayrı kritik hata veya ceza kanıtı değil. Eksik title/description/tek-H1 kontrolünde sorun 0 olumlu sonuçtur.
- **Öneri:** Önce önemli hizmet/blog amaçlarını ayıran metadata üretmek; pagination ve boş sayfa köklerini STATIC-02/05 ile çözmek.
- **Kabul:** Kalıcı önemli sayfalarda amaçla uyumlu metadata; kalan tekrarlar gerekçeli ve raporlanmış; yapay karakter sayısı eşiğine göre kritik hata üretilmemiş.
- **Kanıt:** static-duplicate-titles.json; static-duplicate-descriptions.json

## Performans ve yükleme stratejisi

### PERF-01 — 3B görünürlük stratejisi masaüstünde ilk isteği engellemiyor

**P2 · İlk istek runtime doğrulandı; offscreen maliyet kaynak adayı**

- **URL/kapsam:** /; desktop 1280×900 ve mobil viewport 390×844 development
- **Kaynak:** layouts/partials/home/profile.html:6; layouts/partials/interventional-cardiology-diagram.html:16; layouts/partials/three-heart.html:35–55,164–183
- **Olgu / kök neden:** Gerçek yol lazy partial. Desktop 3/3 yenilemede scroll olmadan GLB isteği 894.8–1589.3 ms’de başladı; her koşuda yaklaşık 1.51 MB transfer. Mobilde ilk örneklemede 3/3 istek/canvas yok, scroll sonrası açılıyor. İlk observer disconnect sonrası offscreen render durdurma yok; sekme gizlenince duruyor. CPU/GPU etkisi/A-B ölçülmedi.
- **Öneri:** Yükleme ve render görünürlük stratejisini açıkça seçip ölçmek; viewport dışında render durdurmak; gerekirse poster/istek üzerine yüklemeyi karşılaştırmak.
- **Kabul:** İlk viewport/scroll/offscreen/tekrar girişte istek ve tek render loop davranışı kanıtlı; production ve mobil profilinde maliyet ölçülmüş. Lazy veya idle sıfır maliyet demek değildir.
- **Kanıt:** browser-model-observations.json; browser-dev-diagnostics.json; performance-asset-inventory.json

### PERF-02 — Hareket/veri tercihleri bütünüyle ele alınmıyor

**P2 · Statik doğrulandı; OS/Save-Data/WebGL senaryoları NOT_RUN**

- **URL/kapsam:** Üç dil ana sayfa ve aktif 3B
- **Kaynak:** layouts/partials/three-heart.html:26–27,91–117; assets/css/custom.css:1877–1888; layouts/partials/extend-footer.html:533–541
- **Olgu / kök neden:** Reduced-motion yorumu gerçek kontrolle karşılanmıyor; autoRotate/gölgeler açık. Hero hareketleri sonsuz; footer reduced-motion kuralı yalnız randevu bileşenlerini kapsıyor. DPR’yi 2’ye sınırlama ve yüksek DPR’de antialias kapatma mevcut olumlu önlemlerdir.
- **Öneri:** Reduced-motion’da gereksiz hareketi kapatmak; Save-Data/WebGL/CDN hatalarında hafif, anlamlı fallback sağlamak.
- **Kabul:** Gerçek tercihler ve hata senaryolarında gereksiz istek/hareket yok; içerik ve bağlantılar kullanılabilir; pil/ısı/FPS etkisi ölçüme dayanıyor.
- **Kanıt:** 04-performance.md; ui-source-notes.md

### PERF-03 — Head’de senkron vendor zinciri var

**P2 · Öznitelikler doğrulandı; darboğaz etkisi aday**

- **URL/kapsam:** Ortak sayfalar; yerel dış JS 118553 bayt, jQuery slim 70264 bayt
- **Kaynak:** themes/blowfish/layouts/partials/head.html:118–140; themes/blowfish/layouts/partials/vendor.html:1–3; layouts/partials/header/basic.html:251–254
- **Olgu / kök neden:** Appearance/zoom/jQuery senkron üretiliyor; küçük görünüm scriptinin flash önleme amacı olabilir. Menüde jQuery bağımlılığı var. Bunların LCP/TBT’nin ana nedeni olduğu henüz ölçülmedi.
- **Öneri:** Bağımlılık sırasını koruyarak gerekli sayfa/ertelenmiş yükleme ve küçük kullanımın sadeleştirilmesini ölçmek; körlemesine bütün scriptlere defer eklememek.
- **Kabul:** Üretimde tekrarlı önce/sonra izleri; tema flash’ı, menü aktifliği, arama, mobil menü ve zoom regresyonu yok.
- **Kanıt:** performance-asset-inventory.json/.csv; 04-performance.md

### PERF-04 — Hero kaynak seçimi ve önceliği iyileştirme adayı

**P2 · Çıktı öznitelikleri doğrulandı; LCP/CLS production etkisi bilinmiyor**

- **URL/kapsam:** /, /en/, /ar/; 35410 bayt ortak işlenmiş WebP
- **Kaynak:** layouts/partials/home/hero.html:131–138; assets/css/custom.css:2349–2367
- **Olgu / kök neden:** Görsel eager; width/height/srcset/sizes/fetchpriority yok. CSS alan ayırıyor, bu yüzden kesin CLS kötü denemez. Development desktop LCP IMG, mobil viewport LCP P; üretim ölçümü değildir.
- **Öneri:** Gerçek production LCP öğesi/alt sürelerine göre intrinsic boyut, responsive kaynak ve gerekçeli fetchpriority seçmek.
- **Kabul:** Doğru cihaz kaynağı yüklenir; görüntü kalitesi ve ayrılan alan korunur; CLS ve LCP tekrar ölçülür. İlk görünüm görseli körlemesine lazy yapılmaz.
- **Kanıt:** performance-asset-inventory.json; browser-dev-diagnostics.json

### PERF-05 — İlk arama büyük JSON ve senkron Fuse kurulumu getiriyor

**P2 · Dosya boyutu/kod doğrulandı; süre etkisi ölçülmedi**

- **URL/kapsam:** /index.json 1.067 MB; /en/index.json 1.043 MB; /ar/index.json 1.445 MB ham
- **Kaynak:** assets/js/search.js:148–180; themes/blowfish/layouts/_default/index.json:2–5
- **Olgu / kök neden:** İndeks arama açılınca alınır; ilk sayfa yükleme bütçesine yazılmamalı. Parse/Fuse kurulumu ve query maliyeti mobil CPU’da ölçülmedi. Dil fallback kapsamı STATIC-06 ile ilişkilidir.
- **Öneri:** İlk arama/açılış/sonuç ve long task ölçümünden sonra alan azaltımı, indeks kapsamı veya worker seçmek.
- **Kabul:** Yavaş mobil profilinde ilk sonuç süreleri/uzun görevler kayıtlı; hata/yeniden deneme ve dil politikası çalışır; TBT/JSON baytı INP diye sunulmaz.
- **Kanıt:** performance-asset-inventory.json; static-search-indexes.json

### PERF-06 — Kullanılmayan eski 3B shortcode’da sözdizimi hatası

**P3 · Doğrulandı — Node check; mevcut HTML etkisi yok**

- **URL/kapsam:** Mevcut production HTML’de kullanılmayan shortcode
- **Kaynak:** layouts/shortcodes/three-heart.html:133–146
- **Olgu / kök neden:** Çıkarılan module node --check ile çıkış 1 veriyor; kapanış/callback yapısı ayrışmıyor. Bu dosya mevcut ana sayfanın eager yolunu çalıştırdığına veya ana sayfanın çöktüğüne kanıt değil.
- **Öneri:** Yeniden kullanımdan önce onarmak veya tek aktif uygulamaya birleştirmek.
- **Kabul:** Sözdizimi kontrolü 0; kullanılacaksa gerçek render/error testleri; aktif lazy yolun davranışı korunmuş.
- **Kanıt:** performance-unused-shortcode-syntax.mjs; performance-unused-shortcode-syntax.log

## İçerik, güven ve sorgu eşlemesi

### CT-01 — Biyografide aynı sayfada iki doğum yılı var

**P1 · Doğrulandı**

- **URL/kapsam:** /hakkimda/, /en/about/, /ar/about/
- **Kaynak:** content/tr/hakkimda/index.md:16,21; EN/AR about/index.md:16,21
- **Olgu / kök neden:** Giriş paragrafı 1973, özgeçmiş paragrafı 1976 diyor. Denetim doğru yılı seçmiyor; kullanıcıya dönük aynı kişi bilgisinde çelişki var.
- **Öneri:** Kullanıcı/CV kaynağıyla doğru bilgiyi belirleyip tek kaynağa bağlamak.
- **Kabul:** Üç dilde biyografi ve gerekli diğer entity/profil bilgisi aynı doğrulanmış olguyu gösterir.
- **Kanıt:** content-evidence.json; content-notes.md

### CT-03 — Hero sayısal iddiaları veri dayanağına bağlanmamış

**P1 · Sabit iddia doğrulandı; gerçek dayanak Doğrulanamadı**

- **URL/kapsam:** Üç dil ana sayfa: 25+ yıl, 20K+ girişim, 100+ yayın
- **Kaynak:** layouts/partials/home/hero.html:60–69; content/tr/yayinlar/_index.md:27–193,197–198
- **Olgu / kök neden:** Hero sayıları hardcoded. Yayın listesinde 75 numaralı girdi var ama tam CV talep edilebildiği belirtiliyor; liste eksik olabilir, bu sayım 100+ iddiasını yanlış kanıtlamaz. Girişim sayısı/deneyim kapsamının dayanağı alınmadı.
- **Öneri:** Her iddianın tanımı, tarih aralığı, güncelliği ve gerçek dayanağını onaylamak; gizli kayıtları rapora/yayına kopyalamamak.
- **Kabul:** Üç dil/CV/yayın kapsamı tutarlı; her sayı için sahibi ve doğrulanmış tanım/dayanak var.
- **Kanıt:** content-evidence.json; content-notes.md

### CT-04 — Hedef sağlık oranlarının okuyucu kaynakları yok

**P1 · Kaynak boşluğu doğrulandı; klinik doğruluk Doğrulanamadı**

- **URL/kapsam:** /blog/diyabetik-ayak/, /blog/periferik-arter-hastaligi/, /hizmetler/dizalti-damar-tikanikligi/, /hizmetler/periferik-damar/
- **Kaynak:** content/tr/blog/diyabetik-ayak/index.md:344–393,463–487; content/tr/hizmetler/dizalti-damar-tikanikligi/index.md:25,75–86
- **Olgu / kök neden:** Dört dosyada sırasıyla 23/4/19/1 yüzde içeren satır; HTTP kaynak bağlantısı veya kaynakça başlığı yok. Her satır araştırma sonucu değil. Oranların yanlışlığı değil; hasta grubu, takip ve sonlanım bağlamının okuyucu tarafından doğrulanamaması saptandı.
- **Öneri:** Hekimin her klinik iddiayı uygun güncel kılavuz/birincil çalışma, hasta grubu, takip süresi ve sonlanımla eşlemesi.
- **Kabul:** Erişilebilir kaynak/tarih/bağlam ve gerçek review sorumlusu var; teknik başarı, açıklık, yara iyileşmesi ve ekstremite kurtarma karıştırılmaz; tıbbi değişiklik hekim onaylıdır.
- **Kanıt:** content-evidence.json; content-notes.md

### CT-05 — Vasküler rehberlerden ilgili hizmetlere doğrudan geçiş yok

**P2 · Doğrulandı**

- **URL/kapsam:** Diyabetik ayak ve periferik arter blogları → dizaltı/periferik hizmetler
- **Kaynak:** İki blogun içerik/üretilmiş anchor grafiği; content/tr/hizmetler/periferik-damar/index.md:220–225; dizalti-damar-tikanikligi/index.md:402–406
- **Olgu / kök neden:** İki rehberde söz konusu hizmetlere doğrudan anchor yok; hizmetler kendi aralarında bağlanıyor. Bu zayıf hasta yolculuğudur, ölçülmüş sıralama kaybı değildir.
- **Öneri:** Klinik olarak uygun bağlamda mevcut rehber/hizmetleri doğru canonical ile bağlamak; diyabetik ayağı yalnız damar açmaya indirgememek.
- **Kabul:** Anlamlı ve doğru dilde rehber–hizmet yolu; bağlantı taraması ve gerçek kullanıcı yolculuğu kontrolü.
- **Kanıt:** content-evidence.json; content-notes.md/CT-05

### CT-06 — Yazar kutusundan biyografiye bağlantı yok

**P2 · Doğrulandı**

- **URL/kapsam:** /blog/diyabetik-ayak/ temsilci
- **Kaynak:** themes/blowfish/layouts/partials/author.html:43–55; layouts/_default/single.html:135–137
- **Olgu / kök neden:** Yazar adı kutuda metin, biyografiye link değil. Hakkımda genel menüden erişiliyor; hekim kimliği bütünüyle yok değil, yazıdan mesleki kanıta doğrudan geçiş eksik.
- **Öneri:** Yazar kutusunu doğru dilde doğrulanmış biyografiye bağlamak; gerçek inceleyici/editör ile yazarı ayrı tutmak.
- **Kabul:** Yazıdan ilgili hekim biyografisine ulaşılır; gösterilen unvan ve varsa inceleme rolü gerçek bilgiyle uyumlu.
- **Kanıt:** content-evidence.json; content-notes.md

### CT-08 — Bilgi/hekim/hizmet sorgu rolleri netleştirilmeli

**P2 · Güçlü aday — niyet/URL eşlemesi; sıralama verisi yok**

- **URL/kapsam:** Sekiz hedef sorgu; mevcut ana sayfa, blog ve vasküler hizmetler
- **Kaynak:** content/tr/_index.md:2–20; content/tr/hizmetler/_index.md:12–43
- **Olgu / kök neden:** Ana sayfa yerel kardiyolog niyetini zaten içeriyor; katalogda girişimsel/periferik alt konular var. Diyabetik ayak adını taşıyan ayrı hizmet detayı saptanmadı; blog ve mevcut damar hizmetleri tüm diyabetik ayak bakımına eşit değil. GSC olmadan cannibalization, hacim ve rank nedeni kesinleşmez.
- **Öneri:** Önce sekiz sorgunun mevcut canonical/amaç eşlemesini hekimle onaylamak; yeni sayfayı yalnız gerçek hizmet kapsamı/niyet gerektiriyorsa açmak.
- **Kabul:** Her sayfanın farklı kullanıcı ihtiyacı açık; GSC baseline/izleme planı var; şehir sayfası/anahtar kelime çoğaltması ve sıralama garantisi yok.
- **Kanıt:** 05-keyword-url-map.csv; content-evidence.json

## Kendi sunucusuna geçiş kapıları

### HOST-01 — Form backend’i ve teşekkür akışı taşınmıyor

**P1 · Statik doğrulandı; CT-07 aynı bulgunun alias’ı**

- **URL/kapsam:** /iletisim/, /en/contact/, /ar/contact/
- **Kaynak:** Her contact/iletisim index.md:56–58; teşekkür .md dosyaları parent index.md leaf bundle altında
- **Olgu / kök neden:** Üç form POST/data-netlify kullanıyor; TR action eski /tr/iletisim/tesekkurler/. Üç teşekkür dosyası bağımsız Hugo sayfası olarak listelenmiyor. Statik dosya sunucusuna kopyalamak Netlify form backend’i yaratmaz. Canlı formun çalışmadığı iddia edilmiyor; gerçek gönderim yapılmadı.
- **Öneri:** Yeni backend/servis kararını, doğru dilde teşekkür/error URL’sini ve veri minimizasyonu/teslim akışını belirlemek.
- **Kabul:** Yetkili, sentetik verili staging testinde POST başarı/hata/spam/teslim ve teşekkür yolu çalışır; yalnız başarı sayfası mesaj teslimi sayılmaz.
- **Kanıt:** ui-static-extract.json; static-source-content.csv; 07-self-hosting-readiness.md

### HOST-02 — Redirect/404 kuralları yeni sunucuda uygulanmayı bekliyor

**P1 geçiş kapısı · Kaynak kuralları doğrulandı; hedef HTTP NOT_RUN**

- **URL/kapsam:** /tr/* ve üç dilde olmayan URL örnekleri
- **Kaynak:** static/_redirects:5–11; netlify.toml:20–23
- **Olgu / kök neden:** Netlify kuralları sıradan Nginx/Caddy/Apache tarafından kendiliğinden uygulanmaz. Hedef sunucu ürünü/yapılandırması henüz doğrulanmış değil.
- **Öneri:** Ürün belirlendiğinde gerçek index/redirect/lokalize 404 kurallarını açıkça aktarmak; varsayımsal konfigürasyonu çalışmış saymamak.
- **Kabul:** Tek 301, query/slash/UTF-8 korunması; mevcut sayfa 200; doğru dilde gövdeyle gerçek 404; SPA ana sayfa 200 fallback yok.
- **Kanıt:** 07-self-hosting-readiness.md; ilgili kaynak dosyalar

### HOST-03 — Üretim başlıkları ve sıkıştırma doğrulanmayı bekliyor

**P2 geçiş kapısı · Kaynak politikası doğrulandı; hedef yanıt NOT_RUN**

- **URL/kapsam:** /, pretty hizmet/blog URL’leri, JSON/XML/CSS/JS/model/görsel
- **Kaynak:** netlify.toml:68–118
- **Olgu / kök neden:** Mevcut kaynak HTML’de revalidation, varlıklarda bir gün kullanıyor; önceki bir yıllık HTML hatası artık bu çalışma ağacında yok. Hedef sunucuda bunlar, güvenlik başlıkları ve HTTP sıkıştırması ayrıca uygulanmalı.
- **Öneri:** Gerçek hedef yanıtlarında Content-Type, cache, ETag/Last-Modified/304, gzip/Brotli ve uygun güvenlik başlıklarını doğrulamak.
- **Kabul:** Temsilci dosya türlerinin GET/HEAD başlıkları ve cold/warm davranışı saklanır; çevrimdışı gzip tahmini HTTP sıkıştırması kanıtı sayılmaz.
- **Kanıt:** 07-self-hosting-readiness.md; network-probes.json

### HOST-04 — Build sürümü ve güvenli yayın yöntemi sabitlenmemiş

**P2 · Doğrulandı — yapılandırma/sürüm uyarıları**

- **URL/kapsam:** Bütün site build’i
- **Kaynak:** netlify.toml:26,30; themes/blowfish/config.toml:3–5; package.json:7–9
- **Olgu / kök neden:** Netlify Hugo 0.151.0, yerel 0.167.0; tema bildirimi 0.141.0–0.152.2. Netlify build’i public/tema örneğini silip --gc çalıştırır. Mevcut derleme geçiyor; bu gelecekteki uyum veya güvenli yayın akışını kanıtlamaz.
- **Öneri:** Sürüm/tema commit’ini sabitlemek; ayrı build, staging, atomik yayın ve rollback tasarlamak; canlı dizinde kontrolsüz temizlik yapmamak.
- **Kabul:** Tekrarlanabilir build manifest/hash, tam tarama sonucu ve test edilmiş geri dönüş yolu; üretimde Hugo watcher çalıştırma gereği yok.
- **Kanıt:** production-build.log; initial-worktree-state.json; 07-self-hosting-readiness.md

## Resmî doğrulayıcı sonuçları ve sınırı

[Gerçek araç sonucu](evidence/browser-validator-results.json), bir hizmet
sayfasından alınan **development** JSON-LD’nin kod girişiyle testidir:
`http://localhost:1313/hizmetler/dizalti-damar-tikanikligi/`.
Localhost kimlikleri korundu; production URL crawl, bütün site uygunluğu ve
bütün görünür sayfa içeriğinin doğrulaması değildir.

- **Schema.org Validator:** 4 öğe, **1 hata + 3 uyarı**. TherapeuticProcedure
  procedureType hatası ve iki performer domain uyarısının metni kaydedildi;
  breadcrumb uyarısının sayısı görüldü, ayrıntısı açılmadı.
- **Google Rich Results Test:** **3 geçerli öğe**: breadcrumb, local business,
  organization. LocalBusiness’te adres, priceRange ve görsel URL’si için
  kritik olmayan uyarılar var. Test girdisi localhost görsel kullandığından,
  görsel uyarısı tek başına production fetch hatası kanıtı değildir.
- Bir aracın öğeyi geçerli sayması SCH-01/02 gibi yapısal/semantik bulguları
  yok etmez. Diğer aracın bir hata göstermesi de bütün schema’ların geçersiz
  olduğu veya Google cezası bulunduğu anlamına gelmez.

## Olumlu sonuçlar ve yanlış çıkarılmaması gerekenler

- HTML taramasında eksik title/description/tek-H1 kontrol sorunu ve HTML asset
  hedefi eksikliği 0. Schema hekim görseli SCH-05 ayrı bulgusudur.
- 679 JSON-LD scripti JSON olarak ayrışıyor. FAQ duplikasyonu, ilave Microdata
  veya RDFa saptanmadı. Bu klinik doğruluk veya Google uygunluk garantisi değil.
- MedicalScholarlyArticle, MedicalWebPage ve Cardiovascular sözlükte vardır;
  EventScheduled güncel MedicalProcedure.status range’inde geçerlidir.
  Google’ın özel rich-result galerisinde olmamak “olmayan/zararlı schema” demek değildir.
- Mevcut production çıktısında MedicalScholarlyArticle 0. Yayın listesini tek
  bilimsel makale entity’si yapmak doğru çözüm değil. FAQ rich-result gösterimi
  7 Mayıs 2026’da kaldırılmıştır; yararlı görünür SSS içeriği ayrı konudur.
- Sayısal/kimlik iddiaları için dayanak gerekliliği tüm CV/yayınların sahte
  olduğu anlamına gelmez; sitede 75 numaralı bibliyografik girdi ve DOI metinleri var.
- Arama mesajında kullanıcı sorgusu artık textContent ile ekleniyor;
  HTTP/JSON/network/timeout/yeniden deneme altyapısı mevcut. Önceki sorunlar
  bu denetimde yeni açık gibi sayılmadı; tam güvenlik testi yapıldı iddiası yok.

## Kapsam / NOT_RUN eki

| İş | Durum/kanıt | Sınır veya tamamlanma yolu |
| --- | --- | --- |
| İzole production build ve bütün HTML tarama | Çalıştırıldı; build log + static/schema JSON/CSV | Canlı Netlify byte eşitliği yok |
| TR menü görünümü 320–1920 | Gerçek viewport; browser-layout-observations.json | 852/853/854 sınır testi henüz bekliyor |
| Menü ekran görüntüsü | browser-menu-1280-crop.jpg; CUA ile yakalanıp dosya doğrulandı | Tek viewport, bütün responsive matrisin yerine geçmez |
| Gerçek %200 zoom | NOT_RUN | Viewport emülasyonu zoom değildir |
| Temsilci mobil menü / modal odağı / arama | Çalıştırıldı; browser-keyboard-observations.json | Tam ardışık Tab, ekran okuyucu, kontrast ve bütün şablonlar değil |
| EN/AR runtime, JS-off ve kontrollü hata senaryoları | NOT_RUN / kapsam kısmi | Statik dil yönü/gövde varlığı görsel geçiş sayılmaz |
| ≥3 production cold-cache Lighthouse desktop+mobile | NOT_RUN | Development tanı koşuları bunun yerine geçmez |
| Development 3+3 Resource/Navigation Timing | browser-dev-diagnostics.json | CPU/ağ throttling, gerçek telefon veya saha p75 değil; OS/DNS/TLS cache tamamen sıfırlanmadı |
| 3B ilk sayfa ve mobil scroll | browser-model-observations.json | Desktop 3/3 ilk isteği, mobil scroll init’i gözlendi; CPU/GPU A-B ve offscreen FPS yok |
| Model engelli A-B, Save-Data, WebGL/CDN failure | NOT_RUN | 3B’nin ölçülmüş hız puanı kaybı veya sıfır etki iddiası yok |
| Schema.org / Google RRT kod testi | Bir temsilci development örneğinde çalıştırıldı | Bütün production URL’leri için resmî geçiş verilmedi |
| CrUX/RUM/GSC/GBP | Doğrulanamadı | Saha CWV p75, rank/CTR, manual action ve profil durumu çıkarılamaz |
| Kamu DNS sorguları | browser-public-dns.json; Google DNS API'den apex NODATA, www NXDOMAIN ve başarılı kontrol | Tek kamu resolver; ikinci resolver, doğrudan authoritative sorgu ve registrar kök neden incelemesi yapılmadı |
| Shell DNS/HTTP | network-probes.json; kontrol alan adları da çözülemedi | Bu shell sonuçları tek başına siteye özgü arıza kanıtı değil; ayrı kamu DNS sorgusu NET-01'i doğruladı; tarayıcı localhost’a ulaştı |
| Hedef production TLS/cache/compression/redirect/404 | NOT_RUN | Yeni sunucu ve gerçek yanıt matrisi gerekli |
| Klinik oranların tam uzman fact-check’i | NOT_RUN | Kaynak boşluğu var; oranların yanlışlığı kanıtlanmadı |
| Form teslimi/randevu işlemi | Gönderilmedi / NOT_RUN | Gerçek mesaj, rezervasyon veya hesap işlemi yapılmadı |

İlk uygulama sırası ve ölçülebilir kabul planı
[06-remediation-backlog.md](06-remediation-backlog.md) içindedir. Eksik testler
başarıya çevrilmedi; erişim/ölçüm sınırları ilgili alt raporlarda açıktır.
