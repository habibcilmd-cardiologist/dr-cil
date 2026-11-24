# dr-cil — Kalan Kabul ve Doğrulama İşlerini Tamamlama Promptu

Depo: `/Users/yavuz/prg/dr-cil`.

Önceki yerel uygulamayı baştan yapma. Güncel kodu ve mevcut kanıtları okuyup
yalnız kalan kabul kontrollerini tamamla. Test somut hata gösterirse en küçük
yerel düzeltmeyi uygula ve ilgili kontrolleri tekrar çalıştır. Yalnız plan veya
yeniden denetim üretmekle bitirme. Bağımsız yapılabilen işler ilerlesin.

## 1. Başlangıç durumu ve portlar

24 Kasım 2026'daki bu prompt hazırlığında:

- `lsof` çıktısında Python PID 35254, **127.0.0.1:1314 LISTEN** olarak görüldü.
- 1313 ve 1315 için dinleyen işlem görünmedi.
- Python işleminin CWD'si depo köküydü; **CWD document root kanıtı değildir**.
  İşlem argümanları izin nedeniyle okunamadı.
- Bu yürütme ortamında curl, 1314 dahil bu portlara bağlanamadı. TCP dinleme
  kanıtıyla HTTP/uygulama kabulünü birbirine karıştırma.
- Önceki 1314 HTTP gövdesi eski baseline ile eşleşmişti. 1314'te yeni düzeltmeleri
  görüyormuş gibi test yapma; şimdi hangi çıktının sunulduğunu yeniden doğrula.
- Kaynak dosyaları son doğrulanmış kaynak manifestiyle eşleşti; Git HEAD'in
  değişmesi tek başına kaynak byte'larının değiştiği anlamına gelmez.

Güncel release adayı:

`/tmp/dr-cil-implementation-after-20261124-release/public`

Yanındaki `build-manifest.json` ile önceki test kanıtlarını kontrol et.
Bu prompt yazılırken güncel `index.html` 110410 bayt ve SHA-256:

`4a79c1dad0267299b166a0e932005d98a10aff97f393529267a2dcdc3d9ba4ef`

Eski baseline ana sayfası 101605 bayt ve SHA-256:

`5443e2b1e1d457569a8dac8ab4b21df104705dbd1bfe8f3484aee8387539b5a8`

Bunlar başlangıç snapshot'larıdır. Kaynak değişirse yeni boş hedefe build al,
yeni manifesti kaydet; eski hash'i sağlamak için çıktıyı elle değiştirme.

**İlk iş:** port + gerçek GET yanıtı + ham HTTP gövdesi hash'i + seçilmiş
JS/CSS hash'lerini güncel release ile karşılaştır. DOM outerHTML hash'i kullanma.
Sıkıştırılmış yanıtı karşılaştırırken açılmış temsil byte'larını esas al.
Document root okunamıyorsa bilinmiyor yaz; HTTP byte eşliği kurulabiliyorsa
diğer kontrolleri gereksiz yere durdurma.

1314 gerçekten güncel release'i sunuyorsa kullanabilirsin. Eski baseline ise
koru; izinli boş 1315'te güncel release'i ayrı sun. Çalışan kullanıcı sürecini
durdurma veya yeniden başlatma. `PermissionError: Operation not permitted`
alınırsa başka API/terminal/port yoluyla kısıtı dolanma. Gereken tek ortam
adımını bildir, bağımsız kontrollerle devam et. Sadece adres kullanımda ise
başka izinli boş port seç ve gerçek adresi kaydet.

İzinli kullanıcı terminalinde güncel çıktı için örnek:

```sh
python3 -m http.server 1315 --bind 127.0.0.1 --directory /tmp/dr-cil-implementation-after-20261124-release/public
```

Bu Python sunucusu UI/performans önizlemesidir; Netlify 301/404/header/form
kurallarını uygulamaz. Gerçek hosting kabulünü bununla geçti sayma.

## 2. Okunacak kayıtlar ve korunacak işler

- `docs/audit/01-remediation-and-seo-implementation-prompt-tr.md`
- `docs/implementation/seo-remediation/2026-11-24/00-progress.md`
- `01-changes-and-validation.md`, `02-keyword-content-map.csv`
- `03-redirect-and-indexing-map.csv`, `04-schema-validation.md`
- `05-performance-before-after.md`, `06-launch-readiness.md`
- Aynı dizindeki `medical-review/` ve ilgili `evidence/` dosyaları.
- İlgili AGENTS.md, güncel Git durumu, tema/sürüm ve daha yeni kayıtlar.

Son kayıt: 42 bulgu/B01–B15; 3 yerel doğrulanmış, 30 uygulanmış-kabul bekleyen,
9 bloke. Bunları güncel duruma göre ele al; bitmiş işi tekrar açma. 967 HTML,
673 JSON-LD, 32 release kontrolü, 9 Node 3B testi ve 8 × 3 dil contact fixture kabulü
önceki kaynak snapshot'ında geçti. Kaynak/çıktı aynıysa bunları gerekçesiz
tekrarlama; yeni hata/düzeltme olduğunda ilgili regresyonu çalıştır.

Önceki kanıtları değiştirme. Bu tur için
`docs/implementation/seo-remediation/2026-11-24/acceptance-completion/`
altında yeni kayıt oluştur. Kullanıcının değişikliklerini koru.

## 3. Gerçek tarayıcı, görünüm ve erişilebilirlik

Güncel release kimliği doğrulandıktan sonra TR/EN/AR ana sayfa ve temel
şablonları test et: biyografi, iletişim, klinik/yayın listesi, hizmet hub'ı,
dizaltı/periferik hizmetler, iki blog, FAQ, taxonomy, pagination ve üç 404.
EN/AR birer hizmet/blog detayı dahil gerçek URL envanterini kullan.

- CSS genişlikleri: 320, 360, 390, 430, 768, 852, 853, 854, 1023, 1024, 1025, 1280, 1440, 1920.
  Güncel header breakpoint'i 1024; eski 853 sınırını yeni breakpoint sanma.
- %100 ve **gerçek native %200 zoom**; browser/viewport/DPR/zoom birlikte kaydedilsin.
  Viewport emülasyonu veya ekran görüntüsünü büyütme native zoom değildir.
- Menü etiketleri, logo/kart ve kontrollerde bölünme/kırpma/taşma; computed
  layout ve ekran görüntüsü. Overflow gizlemeyi çözüm sayma.
- Menü/modal: Tab, Shift+Tab, Enter, Space, Escape; odak döngüsü/dönüşü, inert ve
  scroll kilidi. Dil/arama/tema/footer ve sabit header/anchor davranışı.
- Arama: yükleme/boş/hata/yeniden deneme/Enter; mevcut dil ve açık fallback
  etiketi; doğru sonuç URL'si. En az bir gerçek TR/EN/AR sorgu senaryosu.
- AR RTL, ekran okuyucu adları, kontrast/touch alanı, reduced-motion, JS-off,
  CDN başarısızlığı; ana içerik ve gerçek iletişim bağlantıları kullanılabilir.
- AR 404 metni ve /ar/ çıkışları doğru; HTTP 404 durumu hosting testinde ayrı.

Yeni görsel/işlevsel hata varsa dosya/satır+URL+koşul+önceki kanıtı kaydet,
minimum düzeltme ve tekrar testi yap. Tam WCAG 2.2 AA sonucu otomatik puana dayanmasın.

## 4. Üretim performansı ve gerçek 3B davranışı

Minify production ve gerçek üretim üçüncü taraf yükleriyle çalış; development
sunucusunu production benchmark sayma. Lighthouse erişilebilir ise çalıştır;
başka lab yöntemi kullanılıyorsa adını ve kapsamını açıkça belirt, Lighthouse
puanı üretme. Kısıtları aşma.

- En az 3 masaüstü + 3 mobil aynı koşullu cold-cache koşu, tercihen 5; warm ayrı.
  CPU/ağ/cache/viewport/DPR/sürüm/sunucu/zaman ve sabit gözlem penceresi kaydı.
- Ham JSON/HTML/izler, medyan/aralık; iyi koşuyu seçme. Kritik hizmet/blog ve
  diğer dil ana sayfalarını da kapsa. Yerel ağın canlıya genelleme sınırını yaz.
- LCP öğe/alt süreleri, CLS kaynakları, TBT/long task, FCP/TTFB/Speed Index,
  transfer/istek, JS/DOM/render. Lab TBT ≠ INP; lab sonucu saha p75 değildir.
- Güncel kalp artık poster+kullanıcı isteği modelidir. İlk viewport'ta
  kendiliğinden CDN/GLB isteği olmaması, Load/Retry/Pause, tek init/loop,
  scroll/offscreen/hidden/re-entry, keyboard, reduced-motion/Save-Data,
  WebGL/CDN/model hata/fallback senaryolarını gerçek tarayıcıda doğrula.
- Model tam/istekleri engelli kontrollü karşılaştırma; mümkünse CPU/GPU izi.
  Kaynakta lazy/ondemand olması sıfır maliyet veya hız puanı kazanımı değildir.
- PERF03 vendor ve PERF05 ilk aramayı ölç; ancak nedensel darboğaz bulunursa
  hedefli düzelt. Görünür özellik/model kalitesini sırf puan için kaldırma.

Ölçüm araçlarının test sekmesine uyguladığı CPU/ağ/cache/viewport/zoom ve
instrumentation ayarlarını sonunda önceki haline getir. Kullanıcı pencerelerini
koru; test penceresi aç. Gerçek ölçülmeyen değer için NOT_RUN yaz.

## 5. Yeni resmî schema doğrulaması

TR/EN/AR home, gerçek blog, hizmet/test/işlem, liste/iletişim örneklerinin
**güncel production JSON-LD** kodunu Schema.org Validator ve Google RRT'de
ayrı test et. Localhost'a Google'ın erişebildiğini varsayma; kod girişini
kullan. Eski tek DEV testini bu sürümün kabulü sayma.

JSON/graph, güncel sözlük/domain/range, Google özellik desteği ve görünür/
gerçek bilgi uyumunu ayrı sütunlarda ver. Gerçek hata/uyarı metni, test girdi
hash'i, tarih ve sonuç sakla. Desteklenmeyen rich result, geçersiz schema veya
ceza demek değildir. Sadece uyarıyı kapatmak için adres/fiyat/review/otorite
uydurma; güncel FAQ desteğini birincil belgeden kontrol et.

## 6. Gerçek hosting ve dış hesap kontrolleri

Sunucu/platform bilgisi varsa salt okunur doğrula; bilinmiyorsa çalışmış
Nginx/Caddy/Apache ayarı icat etme. Yapılabilen HTTP testlerini çalıştır:

- Authoritative + iki resolver ve kontrol alan adı; NS/A/AAAA/CNAME; apex/www;
  IPv6 varsa; TLS/sertifika/HTTP→HTTPS ve yönlendirme zinciri.
- Eski /tr/*, emekli home/page yolları ve XML girişleri: tek 301, query/UTF-8
  korunur; hedef 200. Üç dilde olmayan URL doğru dil gövdesiyle gerçek 404.
- Robots/sitemap gerçek XML 200, canonical/noindex uyumu; MIME, HTTP sürümü,
  HTML/JSON/XML cache/revalidation, ETag/Last-Modified, Brotli/gzip ve başlıklar.

GSC/GBP/CrUX için mevcut yetkili salt okunur araçları ara. Veri varsa sekiz
sorgu/konu kümesi, brand/non-brand, page/device/country, CTR/gösterim/tıklama/konum;
indexing/sitemap/Google canonical/manual-action/security ve CWV dönem/kapsamı.
GBP gerçek ad/adres/telefon/saat/kategoriyle karşılaştır. Veri yoksa gereken
export listesini bir defa yaz; bağımsız teknik işleri sürdür.

İki belirsiz taxonomy, kalan metadata ve statik orphan adaylarını gerçek
kaynak/indeks/ihtiyaç verisiyle karara bağla; otomatik toplu noindex/silme veya
anahtar kelime sayfası çoğaltması yapma. Sekiz sorgunun mevcut URL eşlemesini koru.

## 7. Form ve hekim onayı sınırları

Form varsayılan disabled/fallback kalsın; gerçek servis seçmeden etkinleştirme.
Yerel mock/fixture ile doğrulama/hata/teşekkür davranışını test edebilirsin.
**Sentetik dahil dış alıcıya mesaj, form veya randevu gönderme.** Gerçek teslim
kabulü için hedefi ve kapsamı belirli ayrı yetki gerekir. Butona tıklamayı
teslim/gerçek randevu sayma. Analitiğe sağlık/kimlik/iletişim/form metni taşıma.

medical-review'daki 8 kimlik kararı, 12 klinik taslak ve 47 yüzde satırı için
gerçek hekim/kayıt sahibi onayı gerekir. 1973/1976, saat, 25+/20K+/100+ veya oranları
tahminle seçme. Onay gelirse görünür metin ve schema'yı birlikte güncelle;
lastmod'u tıbbi review tarihi yapma. Eksik kararları somut tek onay listesi
olarak sun; bu eksikler diğer kabul kontrollerini durdurmasın.

## 8. Yetki ve teslim

Rutin geri alınabilir yerel test/düzeltmeler yetkilidir. DNS/hesap değişikliği,
gerçek mesaj/randevu, commit/push/deploy yapma. Güvenlik/ağ/port kısıtını aşma.
Yeni build gerekirse güvenli builder ve ayrı yeni/boş hedef kullan;
public/resources temizliği veya --gc yok. Geçen testleri eşikleri gevşeterek kapatma.

Yeni acceptance-completion dizininde:

1. `00-status.md`: 42 ID/B01–B15, önceki durum → gerçek yeni kabul, kanıt/engel.
2. `01-server-and-build-identity.md`: gerçek port/listener/GET/hash/manifest/asset eşliği.
3. `02-browser-accessibility.md`: URL/viewport/DPR/native zoom ve kalıcı görsel/klavye kanıtı.
4. `03-performance.md`: ham koşular/medyan/aralık, 3B ve before/after, lab/saha ayrımı.
5. `04-schema-official.md`: iki resmî araç ve dört ayrı doğrulama katmanı.
6. `05-hosting-and-external.md`: HTTP/DNS/hesap/form/klinik kapıları, eksik veri/izin.
7. `evidence/`: güvenli ham sonuçlar, ekran görüntüleri, izler ve tekrar komutları.

Önceki kayıtları üzerine yazma. Kaynak düzeltmesi olursa etkilenen regresyon
testlerini ve güncel release kimliğini yenile. Son yanıtta **hangi portta hangi
build çalışıyor**, gerçekten geçen kontroller ve yalnız dış bağımlılıkla kalan
işleri açıkça belirt. Çalıştırılmayan testi başarılı sayma; sıralama artışı vaat etme.

Şimdi güncel port/build kimliğini doğrula ve kalan bağımsız kabul işlerine başla.
