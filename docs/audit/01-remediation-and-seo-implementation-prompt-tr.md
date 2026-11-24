# dr-cil — Denetim Bulgularını Düzeltme ve Organik Görünürlük Uygulama Promptu

Bu dosya bir uygulama ajanına doğrudan verilecek görevdir. Yalnız öneri veya
yeni bir denetim raporuyla bitirme: aşağıdaki sınırlar içinde gerçek kaynak
düzeltmelerini yap, doğrula ve kalan dış bağımlılıkları kanıtla.

## 1. Görev ve başarı tanımı

Depo: `/Users/yavuz/prg/dr-cil`.

Hugo/Blowfish geliştiricisi, performans mühendisi, erişilebilirlik uzmanı,
teknik SEO ve tıbbi içerik editörü olarak çalış. Türkçe/İngilizce/Arapça hekim
sitesini; sağlam gezinme, doğru semantik veri, hızlı üretim çıktısı,
doğrulanabilir hekim bilgileri ve anlaşılır hizmet mimarisiyle geliştir.

Öncelikli amaç, İstanbul hekim/hizmet aramalarında ve ilgili Türkiye geneli
bilgi aramalarında organik görünürlüğe uygun güçlü bir site oluşturmak.
Başarıyı kelime tekrarı, sayfa sayısı veya yalnız araç puanıyla ölçme.
Ölçülebilir teknik kabul, kullanıcı yolculuğu ve elde edilebilen gerçek arama
verileriyle değerlendir. Sıralama, trafik veya rich result garantisi verme.

**Bu görev yerel kaynak kodu ve doğrulanmış editoryal düzenlemeleri uygulama
yetkisi verir.** Rutin ve geri alınabilir işler için tekrar izin isteme.
Hekimin gerçekliği bilinmeyen bilgilerini seçme; klinik iddiaları onaysız
yayımlanabilir içerik haline getirme. DNS/Netlify/GSC/GBP hesap değişikliği,
gerçek form/mesaj/randevu gönderimi, commit/push/deploy bu görevle otomatik
yetkilendirilmiş değildir. Bu dış işlemler için önce somut değişiklik paketi
ve kabul planını hazırla. Eksik dış yetki, bağımsız yerel işleri durdurmasın.

## 2. Önce mevcut durumu oku

İlgili AGENTS.md kuralları, Git durumu, HEAD, tema alt modülü, Hugo sürümü,
yapılandırma, mevcut sunucu/portlar ve varsa daha yeni uygulama kayıtlarını
incele. Kullanıcının değişikliklerini koru. Kullanıcının çalışan sunucusunu
durdurma/yeniden başlatma; yeni bir sunucuyu boş portta ve ayrı build ile aç.
Port/ağ kısıtını aşma. Gerçekte erişilebilen adresi doğrula.

Şu belgeleri ve referans verdikleri kanıtları oku:

- `docs/audit/00-master-audit-prompt-tr.md`
- `docs/audit/results/2026-11-24/00-executive-summary.md`
- `docs/audit/results/2026-11-24/01-findings.md`
- `docs/audit/results/2026-11-24/02-url-and-template-inventory.csv`
- `docs/audit/results/2026-11-24/03-schema-audit.md`
- `docs/audit/results/2026-11-24/schema-inventory.csv`
- `docs/audit/results/2026-11-24/04-performance.md`
- `docs/audit/results/2026-11-24/05-keyword-url-map.csv`
- `docs/audit/results/2026-11-24/06-remediation-backlog.md`
- `docs/audit/results/2026-11-24/07-self-hosting-readiness.md`
- `docs/audit/results/2026-11-24/08-test-coverage.md` ve varsa diğer kapsam belgesi
- `docs/audit/results/2026-11-24/09-findings-matrix.csv`
- `docs/audit/results/2026-11-24/evidence/README-reproduction.md`

Ana denetim promptunun eski “kaynak değiştirme” sınırı denetim aşamasına
aitti; bu yeni görev kaynak düzeltmesini açıkça yetkilendirir. Kanıt disiplini
ve canlı sistem sınırları devam eder.

42 kayıt ve eski sayımlar başlangıç referansıdır. Zaten giderilmiş işi tekrar
açma; güncel kod/çıktıyla doğrula. Eski rapor/kanıtları değiştirmeden yeni
before/after kayıtları oluştur. İstenen şeye ulaşmak için yalnız gerekli
değişiklikleri yap; ilgisiz tema/framework yenilemesiyle kapsamı büyütme.
Tema alt modülünü gelişigüzel düzenlemek yerine yerel override kullan.

## 3. Sekiz sorgu ve mevcut sayfa mimarisi

Önce bu eşlemeyi mevcut gerçek permalink'lerle doğrula; dosya adından URL
tahmin etme. Aşağıdaki eşleme başlangıç yaklaşımıdır, sıralama verisi değildir.

| Sorgu | Başlangıç ana hedefi | Kullanıcı ihtiyacı / destek |
| --- | --- | --- |
| istanbul kardiyolog | `/` | İstanbul'da hekim seçimi; biyografi, klinik ve iletişim kanıtı |
| Kardiyoloji Uzmanı | `/` | Uzman seçimi; `/hakkimda/` mesleki kanıt |
| Diyabetik Ayak | `/blog/diyabetik-ayak/` | Bilgilendirme; uygun bağlamda vasküler değerlendirme/hizmet |
| Girişimsel Tedaviler | `/hizmetler/` | İşlem alanlarını ayıran hizmet hub'ı |
| Girişimsel Kardiyoloji | `/hizmetler/` içindeki mevcut ilgili bölüm | Uzmanlık/kapsam; biyografi ve ilgili koroner/yapısal hizmetler |
| Diz altı damar açma | `/hizmetler/dizalti-damar-tikanikligi/` | Spesifik hizmet, uygunluk, seçenekler ve sınırlar |
| Girişimsel damar açma | `/hizmetler/` | Anatomik ihtiyacı ayır; gerçek koroner/periferik alt hizmete yönlendir |
| Diyabetik ayak tedavisi | Mevcut diyabetik ayak rehberi + ilgili gerçek vasküler hizmetler | Tedavi seçenekleri ve ekip yaklaşımı; ayrı hizmet sayfası gerçek kapsam gerektirir |

Anchor bir canonical sayfa değildir; canonical'a `#fragment` ekleme.
Her eşanlamlı sorgu için ayrı, birbirine benzeyen sayfa üretme. Mevcut yararlı
URL'leri koru. Yeni bir uzmanlık veya diyabetik ayak hizmet sayfası ancak
farklı kullanıcı ihtiyacı, gerçek hizmet kapsamı ve özgün içerik dayanağı
varsa değerlendirilsin. Klinik kapsam doğrulanmıyorsa bunu inceleme taslağı
olarak tut. Diyabetik ayağı yalnız damar açmaya indirgeme.

## 4. Uygulama yönetimi

İlk kısa durum kontrolünden sonra B01–B15 paketlerini bağımlılık sırasıyla
uygula. Bağımsız UI, schema, link/SEO ve performans incelemelerini paralel
yürütebilirsin; aynı dosyada çakışmayı önle, sonuçları birleştir.

Her bulgu için başlangıçta şu izleme satırını aç:

`ID | güncel teşhis | değişiklik/dosya | önceki kanıt | kabul testi |
sonraki kanıt | durum | dış bağımlılık`

Durumlar: `Uygulanacak`, `Uygulanıyor`, `Uygulandı–Doğrulama Bekliyor`,
`Doğrulandı`, `Bloke`, `Uygulanamaz`.
`Uygulanamaz` gerekçe ister. Kod yazılması veya build geçmesi runtime
kabulünün yerine geçmez. Başarısız/çalıştırılamayan testi başarılı gösterme.
Bir hesap/klinik bilgi eksikse bir kez somut ihtiyacı kaydet, bağımsız işleri
tamamlamaya devam et. Yalnız plan sunup sonraki turu bekleme.

## 5. Dalga 1 — Görünür ve işlevsel düzeltmeler

### 5.1 Header, uzmanlık, üç dil ve erişilebilirlik

- UI-01/02: marka/menü alan hesabını, `disableTextInHeader` anahtarının
  konumunu ve şablon koşulunu birlikte düzelt. Linklerde harf bölünmesini
  gider; sığmayan masaüstü menüsünü uygun breakpoint'te mobil düzene geçir.
  `overflow-x:hidden`, kırpma veya aşırı font küçültme çözüm sayılmasın.
- Uzmanlık kartı doğrudan ve fallback değerleri: TR “Girişimsel Kardiyoloji”,
  EN “Interventional Cardiology”, AR uygun “طب القلب التداخلي” karşılığı.
  Anlam eşleşmesini kontrol et; sitenin başka yerlerindeki “damar açma”
  ifadelerini topluca silme.
- UI-03/04: mobil menü için semantik düğme, erişilebilir ad, expanded/controls;
  Enter/Space/Escape, odak ve scroll yönetimi. Arama/randevu modalinde ad,
  Tab/Shift+Tab döngüsü, arka plan etkileşimsizliği ve doğru açıcıya dönüş.
- UI-05/06: durum/boş/hata metinlerini üç dile taşı; RTL akışını düzelt.
  JS kapalı/CDN başarısızken ana içerik ve iletişim/hizmet yolları kullanılabilir
  olsun. Telefon, WhatsApp, dil/tema/arama, diagram ve footer kontrollerini test et.
- UI-07: Arapça 404'ün İngilizce else dalını ve `/en/` çıkışlarını düzelt.
  Her dilin mesajı ve ana sayfa/iletişim hedefi doğru olsun.

Kabul: TR/EN/AR; 320/360/390/430/768/852/853/854/1024/1280/1440/1920 CSS px,
DPR/viewport kaydı, %100 ve gerçek native %200 zoom. Etiketler bölünmez,
kontrol kaybolmaz; sabit header anchor başlığını örtmez. Klavye, odak,
kontrast/touch target ve reduced-motion kontrollerini otomatik puana ekle.
Tam WCAG uygunluğu iddiasını yalnız otomatik teste dayandırma.

### 5.2 Linkler, formlar ve yayın hazırlığı

- STATIC-01/04: gerçek canonical hedefler ve dil yollarıyla bozuk CTA,
  literal `false/`, yanlış prefix ve fragment'leri düzelt. İlan edilmiş
  `/tr/*` redirect'iyle çözülebilen linkleri ayrıca sınıflandır.
- HOST-01/02: teşekkür sayfaları gerçek bağımsız route olsun. Form POST'u
  eski 301 yoluna girmeden gerçek endpoint'e gitsin. Endpoint yoksa çalışıyor
  görünümü veya sahte başarı üretme; mevcut iletişim alternatiflerini koru,
  backend seçimini somut bir dış bağımlılık olarak belgele.
- Hedef platform belli ise yerel yapılandırmasını hazırla; belli değilse
  Nginx/Caddy/Apache'den birini gerçek platform gibi varsayma. Netlify
  `_redirects`/header/form işleme davranışının kendiliğinden taşınmadığını
  hesaba kat. Dizin index'i, tek adımlı eski URL geçişi ve gerçek lokalize
  HTTP404 gerekli; bulunmayan her şeyi home200 yapan fallback kullanma.
- NET-01'i güncel authoritative ve iki bağımsız resolver ile yeniden ölç;
  kontrol alan adı kullan. DNS aracı hatasını siteye ait DNS cevabı sayma.
  Kayıtları değiştirmeden hedef/zone/TLS/redirect planını hazırla.

Kabul: tam link taraması temiz; gerçek hedef HTTP testleri ayrı kaydedilir.
Yetkili staging varsa kişisel/sağlık verisi içermeyen testle teslim ve
teşekkür GET akışı ayrı kanıtlanır. Harici alıcıya izinsiz test mesajı gönderme.

## 6. Dalga 2 — Teknik SEO, schema ve ölçülmüş performans

### 6.1 Canonical, hreflang, sitemap, indeksleme

- STATIC-02/03: gerçekten gerekli pagination için kendi canonical'ı ve doğru
  eşdeğer dil hedefi; gereksiz home pagination'ı için gerekçeli karar.
  Gerçekte eşdeğer çeviri yoksa uydurma hreflang bağlantısı üretme.
- Tek sahipli sitemap yaklaşımı kur: kök dil index'i veya açık üç sitemap
  bildirimi. Static ve Hugo çıktısı aynı dosyaya yarışmasın; robots bildirimi
  gerçek XML ile uyuşsun. Sitemap/canonical/redirect/noindex kararları tutarlı olsun.
- Mevcut URL'leri SEO uğruna gelişigüzel değiştirme. Birleştirme gerekirse
  eski→yeni→gerekçe→301→iç link→sitemap haritasını önce oluştur. Kaynak veya
  indeks verisi olmadan toplu silme/noindex uygulama.
- Üretime localhost/staging canonical, yanlış baseURL veya dev noindex sızmasın.
  TR/EN/AR dil/locale tercihlerini gerçek hedefle ve güncel belgelerle incele;
  ülke kodunu varsayımla değiştirme.
- STATIC-05–07: boş manuel taxonomy sayfası ile gerçek term arşivini ayır;
  yararlı arşivi koru. Arama indeksindeki dil fallback'ini anlaşılır hale getir.
  Önemli sayfalarda doğal, amaca özgü title/H1/description ve doğru OG görselleri.
  Keyfi karakter sayısı, kelime yoğunluğu veya meta-keywords hedefi koyma.

### 6.2 Schema'yı gerçek içerik ve varlık modeline bağla

SCH-01–10'un tamamını ele al. Hekim, gerçek klinik/işletme, site, sayfa,
hizmet, hastalık, test, işlem ve yayın rollerini ayır. Stable @id ve
doğrulanmış veri kaynağı kullan. Kişi/işletme tiplerini körlemesine yığma.

- Breadcrumb tek veri kaynağı; benzersiz artan 1..N; doğru dil canonical'ları;
  aynı @id için çelişen tanım yok.
- Uygunsuz `performer` ve sınıf adlarını enum gibi kullanan `procedureType`
  düzeltmeleri; güncel domain/range ve gerçek sayfa anlamıyla doğrula.
- Bütün hizmetlere otomatik Heart/Percutaneous/MedicalCondition/planlı işlem
  atama. Sayfa bazında gerçek konu sınıflandırması oluştur.
- Liste, taxonomy, iletişim ve 404'ü otomatik makale yapma. Yayın listesi tek
  bilimsel makale değildir. Boş ItemList ve görünür içerikte olmayan FAQ üretme.
- Görselin kaynak klasöründe olması yeterli değil; yayımlanmış gerçek URL'sini
  graph'ta kullan ve erişilebilirliğini kontrol et.
- Görünür bilgilerle schema saat/adres/telefon/unvan eşleşsin. `.Lastmod`
  gerçek tıbbi inceleme tarihi değildir. Dernek onayı/üyelik, reviewer,
  koordinat, fiyat veya sameAs dayanağını uydurma.
- JSON parse, Schema.org sözlüğü, Google özellik desteği ve görünür/gerçek
  bilgi uyumunu dört ayrı sonuç olarak raporla. Geçerli tıbbi semantiği
  yalnız Google özel rich-result özelliği yok diye kaldırma. FAQ için
  denetim gününün güncel Google desteğini doğrula; eski sağlık-site tavsiyesine dayanma.

Kabul: bütün HTML'deki bütün JSON-LD scriptleri taranmış; hedefli hatalar
kapanmış. Temsilî TR/EN/AR production kodları Schema.org Validator ve Google
RRT'de ayrı test edilmiş; localhost'u public crawler'ın görebildiği varsayılmamış.
Çalıştırılmayan resmî testleri açıkça belirt.

### 6.3 Performans ve 3B kalp

**Değişiklikten önce production baseline al.** Hugo serve ölçümünü üretim
performansı sayma. Ayrı minify build ve izinli ayrı sunucu/port; gerçek
production Analytics/üçüncü taraf yükünü kapsa.

Ana sayfa desktop/mobile için aynı koşullu en az üç, tercihen beş cold-cache
koşu; sıcak ziyaret ayrı. Kritik hizmet/blog şablonları ve diğer dil ana
sayfalarını kapsa. Chrome/Lighthouse/Hugo sürümü, cache, CPU/ağ, viewport/DPR,
sunucu ve zamanı kaydet. Medyan/aralık ve ham JSON/HTML/izleri sakla.

LCP öğesi/alt süreleri, CLS kaynakları, long task/TBT, FCP/TTFB/Speed Index,
transfer/istek, JS/DOM/render maliyetini ölç. Hero responsive kaynak/boyut/
önceliğini ve vendor zincirini ölçülen nedenle düzelt; bütün scriptlere
körlemesine defer veya hero'ya lazy ekleme. İlk arama indeksinin maliyetini
ilk sayfa yükünden ayrı ölç.

Etkin **partial** ve eski shortcode'u ayır. Aktif modelde ilk viewport,
scroll, viewport dışı, sekme gizli, tekrar giriş; tek init/tek render loop;
DPR, gölge, autoRotate; reduced-motion, Save-Data, WebGL/CDN hata/fallback.
Model açık/istekleri engelli kontrollü karşılaştırmayı aynı koşullarda yap.
Offscreen render'ı durdur; tekrar görünürken güvenle devam et. Poster+
kullanıcı isteğiyle yükleme, yerel bağımlılık ve sıkıştırmayı ölçüme göre seç.
Kalbi sırf puan için silme; “sıfır maliyet” iddiasında bulunma. Eski shortcode
syntax borcunu aktif yolu bozmadan düzelt/konsolide et.

Saha hedeflerini güncel resmî kaynaktan doğrula: LCP≤2.5s, INP≤200ms,
CLS≤0.1, cihaz grubu p75. Lab TBT'yi INP, lab medyanını saha p75 sayma.
Saha verisi alınamadıysa geçti/kaldı sonucu üretme. Araç engelinde boş raporu
doldurmak için skor uydurma; uygulanabilen kaynak düzeltmelerini ayrı doğrula.

## 7. Dalga 3 — İçerik, hekim güveni ve İstanbul görünürlüğü

### 7.1 Öncelikli sayfaları gerçekten güçlendir

Sekiz sorgu için güncel URL/niyet/içerik farkı tablosu çıkar. Önce mevcut
ana sayfa, hizmet hub'ı, dizaltı/periferik hizmetler ve diyabetik ayak rehberini
geliştir. Her sayfanın yanıtladığı hasta sorusu ve farklı amacı açık olsun.

Başlık/alt başlık ve kısa girişten konu anlaşılsın. Uygun yerlerde kimler
için değerlendirilir, alternatifler, sınırlılıklar, riskler, süreç/takip ve
ne zaman değerlendirme gerektiği açıklansın. Bu alanları her sayfaya aynı
metinle doldurma. Kelime sayısı kotası koyma. Mevcut yararlı klinik ayrıntı,
görsel/diagram, kaynak ve bağlantıları sebepsiz kısaltma/silme.

Bilgilendirici rehber→klinik olarak ilgili hizmet→hekim/klinik→iletişim
yolunu doğal bağlamla kur; hizmetten ilgili rehbere geri bağlantı ver.
Yazar kutusunu doğru dilde biyografiye; biyografiyi gerçek yayın ve uzmanlık
kanıtlarına bağla. Footer'a bütün anahtar kelimeleri doldurma.

### 7.2 Tıbbi ve kişisel bilgiyi kanıt olmadan seçme

1973/1976, çalışma saatleri, 25+/20K+/100+ ve benzeri iddiaları kullanıcı/CV/
klinik kaydı olmadan doğru kabul edip eşitleme. Sadece başka web sayfasında
aynısının yazılması yeterli kanıt değildir. Dayanağı bulunmayan iddiayı
çoğaltma; önerilen kaldırma/yumuşatma veya doğru veri seçimini onaya ayır.

Tıbbi oran/tedavi iddialarını güncel birincil çalışma/kılavuz, hasta grubu,
takip ve sonlanımla eşle. Teknik başarı, damar açıklığı, yara iyileşmesi ve
ekstremite kurtarmayı aynı ölçüt yapma. Klinik öneri, başarı oranı, uygunluk
ve risk anlamını değiştiren metinleri `medical-review/` taslaklarında
önce/sonra/kaynak/gerekçe ile hazırla; hekim incelemesi olmadan yayımlanabilir
content'e veya schema'ya geçirme. Teknik/dil düzenlemelerini bu eksiklik
yüzünden durdurma. Gerçekleşmemiş review için tarih/kişi ekleme.

### 7.3 Yerel görünürlük ve dönüşüm

Gerçek ad/unvan/adres/telefon/saatleri site ve erişilebilen yetkili GBP
kaydıyla karşılaştır. Doğrulanmış klinik konumu/hizmet kapsamını anlaşılır
anlat; harita sonucu ile ülke geneli organik sonucu ayır. GBP değişikliklerini
hesap yetkisi olmadan yapma; hazır alan önerilerini dayanaklarıyla teslim et.
Gerçek mesleki atıfları ve yayın bağlantılarını değerlendir; sahte yorum,
ödül/puan, ücretli link, ilçe/şehir kopyaları ve doorway sayfaları üretme.

Telefon/WhatsApp/randevu/form yollarını kullanılabilir ve erişilebilir tut.
Tıklama; teslim edilmiş form, gerçek hasta veya gerçekleşmiş randevu değildir.
Varsa analitik olaylarını bu ayrımla ve veri minimizasyonuyla tasarla;
isim, telefon, e-posta, sağlık bilgisi veya serbest form içeriğini event'e koyma.
Gerçek üretim analitik/çerez/form akışı ile üç dil gizlilik metnini eşle;
hukuki uygunluk sonucunu uzman incelemesi olmadan ilan etme.

GSC/GBP/CrUX bağlantılarını mevcut yetkili araçlarda ara. Yoksa bir kez gereken
export listesini yaz. GSC query/page/device/country; brand/non-brand ve sekiz
konu kümesi; tıklama/gösterim/CTR/ortalama konum; indexing/sitemap/inspection/
manual-action/security; cihaz bazlı CWV. Uygun eşlenebilir dönemler ve veri
boşlukları belirtilsin; kesinti süresi/tarih/hacim uydurulmasın. SERP varsa
tarih/dil/cihaz/İstanbul konumu/yöntemi kaydet; tek ekranı ulusal sıra sayma.

## 8. Derleme, regresyon ve kendi sunucusuna hazırlık

Kaynak/hedef/cache/resource klasörlerini ayır; izlenen public/resources
üzerinde temizleme veya `--gc` yapma. Hugo/tema sürümünü uyum testiyle
belirle; mevcut Netlify sürümüyle yerelin aynı olduğunu varsayma.

Her anlamlı paket sonrası uygun build ve hedefli regresyon kontrolleri;
sonda tüm çıktı link/asset/fragment/canonical/hreflang/sitemap/JSON-LD taraması.
Kritik ortak üretim kuralları için kalıcı, anlamlı regresyon testleri ekle;
salt uygulamayı tekrar eden veya düşük etkili metin değişikliğini donduran
gereksiz testlerle işi şişirme.

Yeni sayfa sayısını eski sayıya eşitlemek zorunda değilsin; eklenen/kaldırılan/
birleşen route'ları ve nedenlerini raporla. İndekslenebilir canonical,
kaynak Markdown, üretilen HTML, alias ve 404 sayılarını ayrı tut.

Hedef sunucuda veya yetkili staging'de GET/HEAD ile index/MIME, lokalize404,
301/zincir, HTTPS/TLS, cache/revalidation, ETag/Last-Modified, sıkıştırma ve
güvenlik başlıklarını doğrula. Konfigürasyon dosyası varlığını gerçek yanıt
sayma. Atomik release ve geri dönüş paketini hazırla; bu prompt deploy değildir.

## 9. Zorunlu teslim ve bitiş ölçütü

`docs/implementation/seo-remediation/YYYY-MM-DD/` altında oluştur:

1. `00-progress.md`: bütün audit ID'leri ve B01–B15 için durum/kanıt/engel.
2. `01-changes-and-validation.md`: gerçek değişiklikler, dosya/satır, testler,
   before/after ve sınırlamalar; eski audit üzerinde oynamadan.
3. `02-keyword-content-map.csv`: sekiz sorgu, gerçek canonical, niyet,
   ana/destek rolü, yapılan değişiklik, iç bağlantılar ve ölçüm.
4. `03-redirect-and-indexing-map.csv`: URL değişiklikleri ve gerekçeleri;
   değişiklik yoksa bunu belirt. Canonical/hreflang/sitemap kararlarını ekle.
5. `04-schema-validation.md`: dört bağımsız schema sonucu ve örnekler.
6. `05-performance-before-after.md`: koşullar, ham koşular, medyan/aralık,
   3B stratejisi, lab/saha farkı; NOT_RUN'lar.
7. `06-launch-readiness.md`: DNS/hosting/form/GSC/GBP için somut paket,
   yetki/veri bekleyenler ve release/rollback kabul listesi.
8. `medical-review/`: yalnız gerekli klinik/kişisel bilgi onay taslakları.
9. `evidence/`: güvenli ham test çıktıları, JSON/HTML/izler, ekran görüntüleri,
   yeniden üretim komutları ve build/çalışma ağacı manifesti.

Her başlangıç bulgusu bir sonuca bağlı olsun. Gerçekten giderilmiş,
uygulanmış ama test bekleyen ve dış bağımlılıkla bloke olan işleri açıkça
ayır. Teknik yerel işler bittiğinde yalnız dış erişim nedeniyle tüm projeyi
tamamlanmış veya tamamen yapılamamış ilan etme.

Son yanıtta: ne düzeldi, hangi testler gerçekten geçti, önce/sonra ölçüm,
sekiz sorgunun artık hangi sayfalarla karşılandığı, kalan klinik/hesap/onay
gereksinimi ve deploy öncesi durum. Kanıt dosyalarına bağlantı ver.

## 10. Güncel birincil kaynaklarla çalış

Uygulama gününde ihtiyaç duyulan sayfaları yeniden aç; tarih ve URL kaydet:

- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://developers.google.com/search/docs/essentials/spam-policies
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- https://developers.google.com/search/updates
- https://developers.google.com/search/docs/specialty/international/localized-versions
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
- https://support.google.com/business/answer/7091
- https://schema.org/ ; https://validator.schema.org/
- https://search.google.com/test/rich-results
- https://web.dev/articles/vitals
- https://gohugo.io/documentation/
- Gerektiği ölçüde W3C/WAI ve gerçekten seçilen sunucu/platform belgeleri.

**Şimdi güncel durumu kısa doğrula, izleme matrisini oluştur ve bağımsız
yerel düzeltmeleri uygulamaya başla. Yalnız yeni bir planla veya genel SEO
tavsiyeleriyle bitirme.**
