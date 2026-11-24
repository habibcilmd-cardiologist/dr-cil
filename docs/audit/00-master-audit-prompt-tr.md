# dr-cil — Kapsamlı Site Denetimi İçin Ana Prompt

Aşağıdaki görevi, kanıta dayalı bir teknik denetim olarak tamamla. Bu görevde
istenen çıktı teşhis, ölçüm, önceliklendirme ve uygulanabilir iş listesidir.
Kaynak kodunda veya canlı sistemde düzeltme uygulama.

## 1. Rol, proje ve hedef

Hugo/Blowfish konusunda deneyimli web geliştirici, performans mühendisi,
erişilebilirlik denetçisi, teknik SEO ve yapılandırılmış veri uzmanı gibi
çalış. Bağımsız incelemeleri paralelleştirebilirsin; sonuçları tek bir raporda
birleştir ve çelişen bulguları çöz.

- Depo: `/Users/yavuz/prg/dr-cil`
- Kullanıcı yerel siteyi `hugo serve` ile başlattı. İlk kontrol adresi:
  `http://localhost:1313/`. Gerçek dinleme adresini doğrula.
- Üretim için yapılandırılan alan adı: `https://docdrhabibcil.com/`.
  Mevcut dosyalardan doğrula; erişilebilir olduğunu varsayma.
- Site Hugo ile üretilen statik, Türkçe/İngilizce/Arapça bir hekim sitesidir.
- Kullanıcı Netlify yayınının DNS nedeniyle durduğunu bildirdi ve kendi
  sunucusuna geçmeyi planlıyor. Bildirilen nedeni bağımsız ölçümle doğrula.
- Amaç: hataları ve gerçek etkilerini bulmak, üç dilde sağlam kullanıcı
  deneyimi ve teknik temel oluşturmak, İstanbul ve Türkiye hedefli organik
  görünürlüğü geliştirmek için kanıtlı bir plan hazırlamak.
- Sıralama, trafik, rich result veya Google tarafından indeksleme garantisi
  verme. Rakip firmanın performans/schema iddiasını kanıtlanmış kabul etme.

Hedef sorguların tamamını kapsa:

1. istanbul kardiyolog
2. Kardiyoloji Uzmanı
3. Diyabetik Ayak
4. Girişimsel Tedaviler
5. Girişimsel Kardiyoloji
6. Diz altı damar açma
7. Girişimsel damar açma
8. Diyabetik ayak tedavisi

## 2. Çalışma sınırları ve kanıt disiplini

1. Önce ilgili `AGENTS.md`, mevcut git durumu, tema alt modülü, Hugo sürümü,
   yapılandırma ve önceki denetim belgelerini incele. Önceden yapılmış
   değişiklikleri sahiplenme, geri alma veya üzerine yazma.
2. Kaynak kodu, içerik, DNS, Netlify ayarı, canlı sunucu, Google Business
   Profile ve Search Console üzerinde değişiklik yapma. Commit/push/deploy
   yapma. Denetim için rapor ve yardımcı kontrol dosyaları oluşturabilirsin.
3. Kullanıcının çalışan Hugo sunucusunu durdurma veya yeniden başlatma.
   Üretim çıktısı için ayrı geçici hedef ve gerekirse ayrı port kullan;
   mevcut `public/` veya izlenen görsel önbelleğini temizleme. `--gc` çalıştırma.
4. Yalnız `hugo serve` çıktısını ölçüp üretim performansı diye sunma.
   Minify edilmiş üretim çıktısını ayrı doğrula; Analytics ve diğer üçüncü
   tarafların üretimde farklı yüklenebileceğini dikkate al.
5. Ağ, tarayıcı veya port yetkisi engelinde kısıtı aşmaya çalışma. Bağımsız
   incelemeye devam et, eksik kalan doğrulama için gereken tek somut adımı
   bildir. Kullanıcıya aynı bilgiyi/izni tekrar tekrar sorma.
6. Durumları açıkça ayır: **Doğrulandı / Güçlü aday / Doğrulanamadı /
   Uygulanamaz**. Kodda bir şey görmek ile tarayıcıda çalıştığını gözlemlemek
   aynı kanıt değildir. Yapılmayan test için başarı sonucu yazma.
7. Google, Schema.org, web.dev, Hugo ve ilgili sunucu belgelerinin denetim
   günündeki güncel, birincil kaynaklarını kullan. Tarih ve bağlantı ver.
   Eski raporları, bu prompttaki başlangıç bilgilerini ve mevcut scriptleri
   güncel kuralın yerine koyma.
8. Lighthouse puanı, ağ süresi, sıralama, arama hacmi veya doğrulayıcı sonucu
   uydurma. Erişilemeyen veriyi eksik olarak işaretle. Search Console
   erişimi yoksa ceza, indeksleme nedeni veya trafik kaybının kesin nedeni
   hakkında hüküm verme.

Her bulgu şu alanları taşısın:

`ID | Öncelik | Durum/güven | URL/şablon | Kaynak dosya:satır |
Gerçek çıktı/ölçüm | Yeniden üretim | Kullanıcı/arama etkisi |
Kök neden | En küçük çözüm önerisi | Kabul testi | Kanıt dosyası/resmî kaynak`

P0: erişilebilirlik/yayın/indeksleme gibi yayını durduran kritik engel;
P1: önemli işlev, doğruluk, görünüm veya ölçülmüş performans sorunu;
P2: belirgin iyileştirme; P3: bakım/temizlik. Kanıtlanmamış SEO cezasını P0 yapma.

## 3. Envanter ve test kapsamı

Kaynak içerik sayısı, üretilen sayfa sayısı, alias sayısı ve indekslenebilir
canonical URL sayısını birbirine karıştırma. Dil ve şablon bazında say.

Statik çıktının tamamında mümkün olan denetimleri otomatik yap:
HTTP/URL haritası, iç bağlantı hedefleri, canonical/hreflang, başlıklar,
görseller ve JSON-LD sözdizimi/tekrarları. Tarayıcı ve performans ölçümleri
için gerekçeli, bütün temel şablonları temsil eden bir örneklem seç.

Örneklem en az şunları içersin:

- TR, EN, AR ana sayfaları.
- Hakkımda, iletişim, klinik, yayınlar listesi ve varsa gerçek yayın detayı.
- Hizmet listesi; kardiyoloji/girişimsel kardiyoloji, diyabetik ayak,
  periferik damar ve diz altı damar konularındaki mevcut hizmet detayları.
- Blog listesi ve en az iki farklı blog detayı; FAQ bulunan bir sayfa.
- Etiket/kategori, sayfalama, eski `/tr/` URL'si ve üç dilde gerçek 404.
- İngilizce ve Arapçada birer hizmet ve blog detayı.

Mevcut gerçek URL'leri bul; dosya adından tahmin ederek var olmayan URL yazma.
Kapsanan ve kapsanmayan URL/şablonları ayrı tabloda göster.

## 4. Görünüm, menü ve kullanıcı deneyimi

Kullanıcının ekran görüntülerindeki somut sorunlar:

- Masaüstü menüsünde “Hakkımda”, “Hizmetler”, “Klinik”, “Yayınlar”, “Blog”,
  “İletişim” gibi sözcüklerin son harfleri alt satıra düşüyor.
- Hero fotoğrafının solundaki **Uzmanlık → Damar Açma** ifadesinin hedefi
  **Uzmanlık → Girişimsel Kardiyoloji** olmalı.

İlgili başlangıç noktaları:
`layouts/partials/header/{basic,fixed}.html`,
`layouts/partials/home/hero.html`, `assets/css/custom.css`, `i18n/*.yaml`.
Türkçe `hero_float_1_value` ve hero fallback değerlerini birlikte izle.

Denetle:

- Gerçek computed style, flex-shrink/min-width, başlık/logo genişliği,
  menü boşlukları, yazı boyutu, white-space, word-break ve breakpoint ilişkisi.
- Masaüstü menüsünün eldeki alana göre erken açılıp açılmadığı; uzun marka
  başlığı ile dil/arama/tema kontrollerinin aynı satıra etkisi.
- `overflow-x: hidden`, kırpma veya metni aşırı küçültmenin taşmayı gizleyip
  gizlemediği. Sorunu gizleyen öneriyi çözüm olarak kabul etme.
- 320, 360, 390, 430, 768, 1024, 1280, 1440 ve 1920 CSS piksel genişlikleri;
  hata veren breakpoint'in hemen altı/üstü; %100 ve gerçek tarayıcı %200 zoom.
  DPR, viewport ve zoom'u raporla. Görseli büyütmeyi zoom testi sayma.
- Uzmanlık kartının hedef metni, fallback'i, dar ekranda taşması ve EN/AR
  anlam karşılıkları. “Damar açma” terimini sitenin tamamından kaldırmayı önerme.
- Sabit header'ın içerik/anchor başlıklarını örtmesi; mobil menü, dil
  değişimi, arama, randevu modali, WhatsApp/telefon bağlantıları, hizmet
  diyagramları ve footer kontrolleri.
- Klavye odağı, Escape, modal odağı ve geri dönüşü, ekran okuyucu adları,
  başlık hiyerarşisi, kontrast, dokunma alanları, reduced-motion ve Arapça RTL.
- JS kapalı veya üçüncü taraf CDN çalışmıyorken ana içerik ve bağlantılar.

Her görsel hata için URL + viewport + ekran görüntüsü + CSS/kök neden ver.
WCAG 2.2 AA iddiasını yalnız otomatik erişilebilirlik puanına dayandırma.

## 5. Masaüstü ve mobil performans; 3B kalbin gerçek maliyeti

Önce test ortamını kaydet: commit/çalışma ağacı, Hugo/Chrome/Lighthouse
sürümleri, işletim sistemi, üretim build komutu, URL, cache, CPU/ağ profili,
viewport, sunucu, ölçüm zamanı. Yerel dosyaların ağ gecikmesini ortadan
kaldırmasının canlı performans tahmini için sınırını açıkla.

Üretim ana sayfasında masaüstü ve mobil için en az üç aynı koşullu soğuk
cache ölçümü yap; mümkünse beş. Medyanı ve aralığı raporla, en iyi koşuyu
seçme. Önemli hizmet ve blog şablonlarını da ölç. İlk ziyaret ve tekrar
ziyareti ayır; sonuç JSON/HTML ve gerekli ağ/performans izlerini sakla.

- LCP öğesi ve alt süreleri, CLS kaynakları, TBT/long tasks, FCP, Speed Index,
  TTFB, transfer boyutu/istek sayısı, JS yürütme, DOM ve render maliyeti.
- Hero görseli/video, responsive srcset/sizes, width/height veya aspect-ratio,
  eager/lazy ve fetchpriority; CSS/JS yükleme zinciri ve kullanılmayan kod.
- Sistem fontu iddiası ile gerçek font istekleri, render engelleyen kaynaklar,
  büyük inline CSS/SVG, blur/filter/animasyon ve üçüncü taraf scriptleri.
- Sunucu tarafında DNS/TLS/redirect süreleri, Brotli/gzip, cache-control,
  ETag/Last-Modified ve HTTP sürümü. Yerelde Netlify başlıkları uygulanıyor
  varsayma; gerçek HTTP yanıtını kontrol et.

Saha verisi varsa CrUX/PageSpeed Insights/Search Console üzerinden masaüstü
ve mobili ayrı incele. URL/origin kapsamını ve veri dönemini belirt.
Yeterli saha verisi yoksa “saha CWV sonucu yok” de. Laboratuvar TBT'yi INP
diye sunma; etkileşimli lab ölçümünü de saha p75 ile aynı kabul etme.
Güncel eşikleri doğrula: LCP ≤2.5 sn, INP ≤200 ms, CLS ≤0.1; saha sonucu
cihaz grubu başına p75 üzerinden değerlendirilir. Lighthouse puanını
tek başına sıralama veya tüm CWV'lerin geçtiğinin kanıtı yapma.

3B model için iki uygulamayı ve gerçek çağrı zincirini mutlaka incele:

- `layouts/partials/three-heart.html`
- `layouts/shortcodes/three-heart.html`
- Bunları çağıran ana sayfa/içerik, Three.js/GLTFLoader/OrbitControls ve modeller.

Yorumlardaki “lazy/non-blocking” ifadelerini kanıt sayma. Ağ zaman çizelgesi
ve ana iş parçacığı iziyle şunları göster:

1. İlk viewport'ta, kullanıcı scroll etmeden hangi JS/model istekleri var?
2. Scroll ile yaklaşınca IntersectionObserver/rootMargin ne zaman tetikliyor?
3. requestIdleCallback ve timeout ağır işi ilk yükleme/ilk etkileşimle
   çakıştırıyor mu? İsteklerin gecikmesi toplam CPU/GPU maliyetini yok ediyor mu?
4. Canvas ekrandan çıkınca veya sekme gizlenince render gerçekten duruyor mu?
5. Mobil DPR, gölgeler, antialias, texture/model boyutu, draw-call ve sürekli
   autoRotate maliyeti nedir? Birden fazla init/render loop oluşuyor mu?
6. reduced-motion, Save-Data, WebGL yokluğu, CDN/ağ hatası ve fallback davranışı.
7. Ekranda model görünmeden önce CLS için yeterli alan ayrılmış mı?

Kontrollü, kaynak kodunu değiştirmeyen bir karşılaştırma yapılabiliyorsa
model istekleri engelli/tam çalışan durumları aynı koşullarda karşılaştır.
Bu karşılaştırmanın kullanıcıya sunulan bir düzeltme olmadığını belirt.
“Performansa sıfır etki” vaadi verme. Poster + kullanıcı isteğiyle yükleme,
viewport dışı durdurma, sıkıştırma veya yerel bağımlılıklar gibi seçenekleri
ölçülen soruna göre önceliklendir. Modeli yalnız puan yükseltmek için silmeyi
otomatik çözüm kabul etme.

## 6. Yapılandırılmış veri: dört ayrı doğrulama

Her sayfadaki JSON-LD scriptlerinin **tamamını**, theme üretimini ve içerik
içine gömülü işaretlemeyi topla. Gerekirse Microdata/RDFa'yı da incele.
Yalnız template metnini veya tek scripti kontrol edip “schema geçti” deme.

Şu dört sonucu ayrı sütunlarla raporla:

1. JSON/JSON-LD sözdizimi ve graph/@id tutarlılığı.
2. Schema.org güncel sözlüğünde tür/property/enum ve beklenen değer tipleri.
3. Google'ın denetim gününde desteklediği rich result özelliği ve koşulları.
4. Görünür sayfa içeriğiyle ve gerçek kişi/klinik/hizmet bilgileriyle doğruluk.

Bir tür Google rich result galerisinde yok diye “Schema.org'da yok”,
“SEO'ya zararlı” veya “Google cezası sebebi” deme. Geçerli tıbbi semantik
türleri sadece bu gerekçeyle kaldırmayı önerme. Rich Results Test'te desteklenen
öğe bulunmaması da tek başına geçersizlik değildir.

Schema.org Validator ve Google Rich Results Test'i farklı amaçlarla kullan;
test tarihi, girdi URL/kod, gerçek hata/uyarı ve ekran/çıktıyı kaydet.
Özel localhost URL'sine Google'ın ulaşabildiğini varsayma; testin kod girişini
kullan veya çalıştırılmadığını yaz. Mevcut `scripts/check_schema.py` ve
diğer scriptlerin gerçekte neyi doğruladığını incele; kapsamı aşan sonuç çıkarma.

Başlıca dosyalar: `layouts/partials/schema.html`, `schema-procedure.html`,
`schema-faq.html`, `schema-scholarly.html`, breadcrumbs ve theme partial'ları.

İncelenecek mevcut kod adayları — bunları otomatik hata hükmü sayma:

- `Person`/`Physician`/`MedicalBusiness`/klinik/hekim kimliklerinin modellenmesi,
  stable @id'ler, author/publisher ve aynı varlığa verilen farklı bilgiler.
- `MedicalSpecialty` enum'u ve `Cardiovascular`; resmî sözlükten doğrula.
- `MedicalProcedure.status = EventScheduled`: hem güncel property/range
  geçerliliğini hem genel bilgilendirme sayfasındaki anlamını ayrı değerlendir.
- Hastalık, danışmanlık, test ve tedavi sayfalarının tamamına aynı
  `MedicalProcedure`, `PercutaneousProcedure`, `Heart` varsayımlarının uygulanması.
- Procedure partial'ının döndürdüğü WebPage/Breadcrumb dahil her düğüme
  `performer` eklenmesi; geçerli property domain/range ve anlam ilişkileri.
- Aynı `#breadcrumb` için birden fazla, çelişkili graph tanımı ve TR/EN/AR
  breadcrumb hedeflerinin gerçek canonical adresleriyle uyuşması.
- İşlem başlığının otomatik `MedicalCondition` olarak işaretlenmesi.
- Liste, taxonomy, iletişim ve diğer yardımcı sayfaların otomatik Article
  olarak işaretlenmesi; sayfanın gerçek ana konusu ve türü.
- `MedicalScholarlyArticle` gerçek bilimsel yayını mı, listeyi mi tanımlıyor?
  Türün varlığını, yayın bilgisini ve alanların doğruluğunu ayrı kontrol et.
- Boş ItemList, eksik görünür FAQ, tekrar eden FAQPage, kaçış/HTML sorunları.
- `reviewedBy`, `lastReviewed`, `recognizingAuthority`, adres/koordinat,
  çalışma saatleri, `priceRange`, unvanlar ve sameAs için gerçek kanıt.
  Bir meslek derneğinin onayını, tıbbi incelemeyi, üyeliği, fiyatı veya
  değerlendirme puanını uydurma; .Lastmod'u otomatik tıbbi inceleme kanıtı sayma.
- Görsel URL'leri gerçekten var mı ve taranabiliyor mu? assets/ kaynağından
  üretilen görselin static/img altında aynı adla bulunduğunu varsayma.

Güncellik başlangıç notu: Google'ın resmî 2026 değişiklik kaydına göre FAQ
rich results 7 Mayıs 2026'dan itibaren gösterilmiyor. Denetim gününde yeniden
doğrula; “sağlık sitesi olduğu için FAQ zengin sonuç alır” şeklindeki eski
tavsiyeyi tekrar etme. Bu durum görünür SSS içeriğini otomatik kaldırma gerekçesi
değildir.

## 7. Teknik SEO, DNS ve indekslenebilirlik

- DNS'in NS/A/AAAA/CNAME kayıtları ve resolver karşılaştırması; www/apex,
  IPv4/IPv6 farkları, HTTP/HTTPS, TLS sertifikası ve yönlendirme zinciri.
  Yerel çalışma ortamının tüm alan adlarını çözememesini sitenin DNS arızası
  sanma; kontrol alan adı ve mümkünse bağımsız resolver ile ayır.
- Kesinti süreleri, robots erişimi, 5xx/timeout ve crawl etkisi için erişilebilen
  log/gerçek ölçüm; geçmiş veri yoksa süresini veya kaybı tahmin diye etiketle.
- robots.txt, meta robots, X-Robots-Tag; staging/dev noindex'in üretime
  sızması; robots engeli ile noindex'in farklı etkileri.
- HTTP durumları, soft 404, redirect zinciri/döngüsü, yanlış SPA fallback,
  alias, slash, URL encoding, Türkçe karakter ve eski `/tr/` geçişi.
- Her indekslenebilir sayfanın canonical'ı, dil eşleşmesi, hreflang'ın
  karşılıklılığı, kendine referansları ve mevcutsa x-default doğruluğu.
- `static/sitemap.xml`, `layouts/_default/*sitemap*`, Hugo'nun kendi sitemap
  çıktısı ve robots içindeki bildirim arasındaki gerçek sahiplik/çakışma.
  Kök sitemap urlset mi index mi; üç dil nasıl keşfediliyor; her bildirilen
  sitemap 200 dönen doğru XML mi? Redirect ile kendisine dönüyor mu?
- Sitemap URL'lerinde canonical 200/indexlenebilirlik, lastmod gerçekliği,
  pagination, tag/category şişmesi, orphan ve bozuk iç bağlantılar.
- Title/H1/description, başlık tekrarı, Open Graph ve gerçek sayfa amacı.
  Keyfi karakter sayısı eşiğini tek başına kritik SEO hatası kabul etme.
- Arama indeksi JSON'unun üç dilde içeriği; diller arası yanlış sonuç/link,
  canonical sızıntısı, arama sonucunun yanlış dilde açılması.
- GSC mevcutsa performans, page indexing, sitemap, seçilen canonical,
  URL inspection, manual action/security ve saha CWV raporları. Önce mevcut
  yetkili bağlantıları ara; erişim yoksa gerekli rapor/export listesini ver.

## 8. Arama niyeti, tıbbi içerik güveni ve yerel görünürlük

Her hedef sorgu için şu eşlemeyi tabloyla üret:

`Sorgu | Yerel/ulusal niyet | Mevcut canonical URL | İçerik türü |
Birincil/ikincil hedef | Kapsam açığı | Rakip URL çakışması |
İç link önerisi | Gerekli kanıt | Ölçüm yöntemi`

Mevcut sayfayı güçlendirme ile yeni sayfa ihtiyacını ayır. Her anahtar kelime
için neredeyse aynı yeni sayfa üretme. Özellikle hizmet/blog sayfalarının
birbirini hedeflemesini, diyabetik ayak ile periferik damar hastalığı
bağlantısının hem anlaşılır hem tıbben doğru kurulmasını incele.

- Hekim biyografisi, doğrulanabilir uzmanlık/unvan, yayınlar ve kaynaklar,
  editoryal sorumluluk, gerçek tıbbi gözden geçirme bilgisi ve iletişim şeffaflığı.
- “25+ yıl”, “20K+ girişim”, “100+ yayın” gibi görünen iddiaların dayanağı.
  Sahte başarı oranı, hasta yorumu, inceleme, ödül veya yetki bilgisi ekleme.
- Hizmet kapsamı, kimler için uygun olduğu/sınırlılıkları, alternatifler ve
  hastanın kararına yardımcı özgün açıklamalar. Tıbbi içeriği bu turda yeniden
  yazma; doğrulanması gereken iddiaları uzman incelemesine ayır.
- YMYL/E-E-A-T'yi mekanik puan veya doldurulacak schema alanları gibi sunma.
- İstanbul aramalarında gerçek adres/telefon/unvan tutarlılığı, Google Business
  Profile kategori/website/klinik bilgileri, kanıtlı mesleki atıflar ve yerel
  görünürlük. Harita sonucu ile ülke çapındaki organik sonucu ayrı ele al.
- SERP incelemesi yapılabiliyorsa tarih, dil, cihaz, arama konumu ve yöntemi
  kaydet. Tek arama ekranını sabit ulusal sıralama veya hacim verisi sayma.
- Şehir/ilçe sayfalarını topluca çoğaltma, keyword stuffing, gizli metin,
  sahte yorum veya bağlantı satın alma gibi öneriler verme.
- GSC verisi varsa baseline: sorgu/sayfa/cihaz/ülke bazında gösterim, tıklama,
  CTR ve ortalama konum. Kesintiden önce/sonra karşılaştırma için eşlenebilir
  dönem öner. Sıralama artışı için kesin oran veya tarih vaat etme.

## 9. Güvenilirlik, güvenlik ve kendi sunucusuna geçiş

Statik site kapsamına uygun kontrol yap: bozuk/çift event handler, arama sorgusu
DOM güvenliği, dış linkler, bağımlılık/CDN hataları, console/network hataları,
yanlışlıkla yayınlanan yedek/debug dosyaları ve hassas bilgi sızıntısı.
Anahtar veya kişisel verinin kendisini rapora kopyalama.

Yeni sunucu için şu davranışları belgeleyip eksik olanı işaretle:
doğru index.html sunumu, `/tr/*` 301 geçişi, dil bazlı gerçek 404,
HTML/JSON/XML cache politikası, statik dosya sürümleme, sıkıştırma, HTTPS,
güvenlik başlıkları ve üçüncü taraf bağımlılıkları. Netlify `_redirects` ve
`netlify.toml` dosyalarının Nginx/Caddy/Apache'de kendiliğinden çalışmadığını
hesaba kat. Sunucu türü bilinmiyorsa gerçekmiş gibi yapılandırma icat etme.

Çerez/analitik/iletişim ve hekim tanıtımıyla ilgili görünen uygunluk risklerini
işaretle; hukuki kesin sonuç verme. Hukuki kural ileri sürmen gerekiyorsa
güncel resmî kaynağı doğrula ve gereken uzman incelemesini belirt.

## 10. Zorunlu teslimler ve bitiş ölçütü

Depo içinde `docs/audit/results/YYYY-MM-DD/` altında oluştur:

1. `00-executive-summary.md`: en fazla iki sayfa; gerçek engeller, ilk on
   öncelik, doğrulananlar ve bilinmeyenler, kullanıcının sorularına doğrudan yanıt.
2. `01-findings.md`: bütün kanıtlı bulgular ve adaylar, ortak ID sistemiyle.
3. `02-url-and-template-inventory.csv`: sayfa/dil/şablon/canonical/index durumu.
4. `03-schema-audit.md` ve `schema-inventory.csv`: tür/property/sayfa kapsamı,
   dört doğrulama sonucu, gerçek hata metni, görünür içerik ve resmî kaynaklar.
5. `04-performance.md`: masaüstü/mobil yöntem, ham koşular, medyan/aralık,
   lab/saha ayrımı, 3B başlangıç/scroll/etkileşim/offscreen analizi.
6. `05-keyword-url-map.csv`: sekiz hedef sorgunun mevcut URL ve iş planı eşlemesi.
7. `06-remediation-backlog.md`: kök nedene göre gruplanmış P0–P3 işler,
   kapsam/dosya, tahmini efor, bağımlılık, risk, kabul testi ve geri alma yolu.
8. `07-self-hosting-readiness.md`: doğrulananlar, taşınacak Netlify davranışları,
   DNS/TLS ve sunucu tarafında bekleyen kontroller.
9. `evidence/`: gerçek raporlar/ölçümler, ilgili güvenli ekran görüntüleri,
   JSON-LD örnekleri ve yeniden üretim komutları. Ortam izlerini/ham ölçümleri
   kullanıcı/hasta bilgisi ve kimlik bilgisi içermeyecek şekilde sakla.

Her dosyanın dolu olması için sonuç uydurma; erişim engeli varsa dosyada
`Doğrulanamadı`, nedeni ve tamamlamak için gerekli somut adımı yaz.

Backlog üç uygulama dalgası içersin:

- **Dalga 1:** Menü ve uzmanlık kartı dahil doğrulanmış görünür/işlevsel
  hatalar; varsa erişim/indekslemeyi gerçekten engelleyen sorunlar.
- **Dalga 2:** Schema semantik doğruluğu, canonical/hreflang/sitemap ve
  ölçülmüş performans darboğazları; 3B için kanıtlı yükleme/render stratejisi.
- **Dalga 3:** İçerik mimarisi, gerçek tıbbi güven unsurları, iç bağlantılar,
  yerel görünürlük ve sürdürülebilir ölçüm.

Son yanıtın şu sorulara açık yanıt versin:

1. Menü neden harf bölüyor; hangi genişlikte, hangi CSS/layout nedeniyle?
2. Uzmanlık kartının yanlış değeri tam olarak nereden geliyor?
3. Masaüstü ve mobil performans ne durumda; gerçekten ölçüldü mü?
4. Ana sayfadaki gerçek 3B yol hangisi; ne zaman hangi maliyeti yaratıyor?
5. Hangi schema hatalı, hangisi geçerli ancak Google rich result desteği yok,
   hangisi içerik/kanıt açısından sorunlu, hangisi doğrulanamadı?
6. DNS/yayın kesintisi, teknik SEO, içerik ve yerel görünürlük için hangi
   sonuçlar kanıtlı; sıralamanın nedenine dair neler henüz bilinmiyor?
7. İlk uygulanacak on iş ve her birinin ölçülebilir kabulü nedir?

Yalnız genel SEO tavsiyeleri veya araç skorlarıyla bitirme. İddiaların gerçek
URL, dosya, çıktı ve ölçüme dayansın. Bu turda düzeltme yapmadan denetimi ve
uygulamaya hazır backlog'u tamamla.

## Başlangıç için resmî kaynaklar

Bu listeyi denetim gününde yeniden doğrula; güncel kurala ulaşmak için kullan:

- https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- https://developers.google.com/search/updates
- https://schema.org/Physician
- https://schema.org/MedicalProcedure
- https://schema.org/MedicalScholarlyArticle
- https://schema.org/MedicalWebPage
- https://validator.schema.org/
- https://search.google.com/test/rich-results
- https://web.dev/articles/vitals
- https://developers.google.com/search/docs/appearance/page-experience
- https://support.google.com/business/answer/7091
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
