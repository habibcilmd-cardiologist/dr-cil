# Kendi sunucusuna geçiş hazırlığı

Tarih: 24 Kasım 2026. İnceleme statik kaynak ve izole üretim çıktısına
dayanır. Sunucu, DNS, Netlify veya hesap ayarı değiştirilmedi. Mevcut
çalışan Hugo süreci durdurulmadı. Hedef işletim sistemi/sunucu ürünü,
sunucu adresi, ters proxy ve sertifika yöntemi henüz doğrulanmış değil.
Önceki aynı tarihli denetim kaydında tarayıcı üzerinden Google Public DNS
JSON yanıtları alınmıştır (`browser-public-dns.json`):
apex A/AAAA NODATA, www A/CNAME NXDOMAIN; kontrol `google.com` A yanıtı
başarılıdır. Bu, mevcut web çözümlemesinde **NET-01 P0** durumunu gösterir.
İkinci resolver, registrar kök nedeni, TLS/origin ve gerçek HTTP yanıtları
henüz doğrulanmadı; bu dosyadaki “bekliyor” kayıtları başarı kabulü değildir.
Bu turdaki kaynak/çıktı tekrar incelemesi
`evidence/recheck-content-evidence.json` (15 çıktı sayfası),
`evidence/recheck-content-keyword-verification.json` (sekiz sorgu hedefi)
ve `evidence/recheck-content-sources.md` içindedir. Önceki DNS kaydı yeni
DNS ölçümü olarak sayılmadı; DNS'nin son durumu birleşik rapordadır.

## Sonuç

Site statik olarak taşınabilir; ancak yalnız `public/` kopyalamak bütün
mevcut davranışları taşımaz. **Form işleme, eski URL yönlendirmeleri,
yerelleştirilmiş 404 ve başlıklar yeni sunucuda ayrıca karşılanmalıdır.**
Hugo geliştirme sunucusunun açılması üretim barındırmasının hazır
olduğunu göstermez.

İlk yayın engeli dosya taşıma değil, mevcut apex/www DNS çözümlemesidir.
Amaçlanan hedef ve yetkili zone doğrulanıp kayıtlar uygun platform hedeflerine
göre düzenlenmeden yayın hazır sayılmaz. Denetim kayıtları değiştirmedi.

## Doğrulanan mimari ve yapılandırma

| Konu | Doğrulanan kaynak/çıktı | Durum |
| --- | --- | --- |
| Üretim alan adı | `hugo.toml:1`: `https://docdrhabibcil.com/`; kamu DNS sorguları | Apex A/AAAA NODATA, www A/CNAME NXDOMAIN; tek kamu resolver hizmetinde doğrulandı |
| Üretim çıktı kökü | `netlify.toml:27`: `public`; izole audit build aynı statik yapıyı üretir | Statik doğrulandı |
| Yerel araç | `package.json:7` Hugo development server; `:9` üretim build kısayolu | npm uygulama sunucusu yok |
| Dil yolu | `hugo.toml:5–6`: varsayılan TR kökte, EN `/en/`, AR `/ar/` | Üretilen HTML ile doğrulandı |
| Eski URL geçişi | `static/_redirects:5` `/tr/* /:splat 301!`; ayrıca `netlify.toml:20–23` | Netlify'ya özgü kaynak kuralı |
| Lokalize hata | `static/_redirects:8–11`: EN, AR ve varsayılan 404 | Hedef HTML dosyaları mevcut; yeni HTTP eşleme bekliyor |
| Güvenlik/önbellek | `netlify.toml:68–118` | Kaynak doğrulandı; hedef sunucu yanıtı bekliyor |
| Form backend'i | Üç contact formu `data-netlify=true`, POST | Netlify bağımlılığı doğrulandı; taşınacak backend yok |
| Üçüncü taraflar | 3B modül Skypack, üretim Analytics Google, randevu dış sağlayıcılar | Tamamen bağımsız/offline yayın değil |

## HOST-01 — Form işleme taşınmıyor: P1, statik doğrulandı

Üç dilde üretilmiş iletişim formlarının method/action bilgileri:

| Form sayfası | Form adı | POST hedefi | Kaynak |
| --- | --- | --- | --- |
| `/iletisim/` | `contact-tr` | `/tr/iletisim/tesekkurler/` | `content/tr/iletisim/index.md:56–58` |
| `/en/contact/` | `contact-en` | `/en/contact/thank-you/` | `content/en/contact/index.md:56–58` |
| `/ar/contact/` | `contact-ar` | `/ar/contact/shukran/` | `content/ar/contact/index.md:56–58` |

`evidence/ui-static-extract.json` gerçek üretilen `<form>` özniteliklerini
kaydeder. Depoda yeni sunucu için bir form endpoint'i doğrulanmadı.
Netlify Forms, Netlify'nin build algılama ve teslim işleme hizmetidir;
normal bir statik dosya sunucusu `data-netlify` niteliğini çalıştırmaz.
Canlı Netlify formunun teslim durumunu bu bulgudan çıkarmıyoruz ve form
gönderimi yapmadık.

TR action eski `/tr/` yolunu kullanıyor. Yeni sunucunun 301 kuralı ile POST
davranışı birlikte tasarlanmalı; payload'un kaybolmadığı kontrollü test
yapılmadan “çalışır” denmemeli. Teşekkür sayfasının açılması mesajın
gerçekten alındığının kanıtı değildir.

**Öneri:** Yayına geçmeden endpoint/servis seçimi ve iletim/saklama akışı
belirlensin veya formun sunulan işlevi açıkça yeniden tasarlansın. İletişim
verileri ve serbest metin için veri minimizasyonu, erişim ve saklama
kararları da bu akışla ele alınmalı; bu rapor hukuki uygunluk kararı vermez.

**Kabul:** Staging'de kişisel/sağlık verisi içermeyen tek kontrollü test;
POST başarı/hata durumları, spam/honeypot, doğrulama, teslim ve doğru dilde
teşekkür/hata yolu uçtan uca kanıtlanır. Gerçek alıcıya test iletimi için
yetki ve açık hedef ayrıca bulunmalıdır.

## HOST-02 — Redirect ve 404 davranışı: P1 geçiş kapısı

`_redirects` ve `netlify.toml` dosyaları Netlify kurallarıdır. Nginx, Caddy
veya Apache için kendi yapılandırmasına aktarım gerekir. Yeni sunucu
ürünü bilinmediğinden çalıştırılmamış yapılandırma örneği teslim etmiyoruz.

**Gerekli davranışlar:**

- `/tr/` → `/`, `/tr/hakkimda/` → `/hakkimda/`: tek 301 adımı,
  query string korunur; hedef URL 200 ve doğru canonical verir.
- Geçerli mevcut dosya/klasör, catch-all hata kuralından önce sunulur.
- `/en/olmayan-audit-yolu/` EN 404 gövdesi ve **404** durumuyla;
  `/ar/olmayan-audit-yolu/` AR 404 gövdesi ve **404** durumuyla;
  diğer olmayan adresler TR 404 gövdesi ve **404** durumuyla döner.
- Her hatalı URL'yi ana sayfaya 200 ile döndüren SPA fallback kullanılmaz.
- UTF-8/percent-encoding, slash ve eski alias geçişleri döngü oluşturmaz.

**Kabul:** HEAD ve GET durum/Location/gövde/canonical testleri gerçek hedef
sunucuda kaydedilir. Statik HTML dosyasının varlığı HTTP testinin yerine geçmez.

## HOST-03 — Cache ve güvenlik başlıkları: P1/P2 geçiş kapısı

Mevcut kaynak artık genel HTML adreslerine bir yıllık immutable önbellek
uygulamıyor: `netlify.toml:71,82` yeniden doğrulama ister. Statik asset
kuralları `:88–118` bir gün + must-revalidate kullanıyor. Önceki hata yeni
denetimde varmış gibi raporlanmamalıdır; canlı yayında bu dosyanın hangi
sürümünün uygulanmış olduğu henüz doğrulanmadı.

Yeni sunucuda gereken doğrulamalar:

- `/`, klasör adresli hizmet/blog, `/en/`, `/ar/`, sitemap XML ve arama JSON
  için politika açık olsun; `/*.html` tek başına pretty URL'leri kapsamayabilir.
- Hash'li dosyalar için uzun cache mümkün, aynı URL'de değişen dosyalara
  yanlış immutable vermeyin. İçerik yayını sonrası eski dosya referanslarının
  ve yeni HTML'in birlikte çalışması kontrol edilir.
- Brotli/gzip, Content-Type, ETag veya Last-Modified ve 304 davranışı gerçek
  yanıtla test edilir. Sıkıştırma/HTTP2 etkinliği kaynak dosyadan çıkarılamaz.
- Kaynaktaki X-Frame-Options, nosniff, Referrer-Policy ve Permissions-Policy
  davranışlarının yeni sunucuda uygun karşılıkları değerlendirilir.
  CSP/HSTS birer ayrı politika kararıdır; doğrulanmadan katı değer yayınlama
  veya yalnız eksikliklerini SEO cezası/açık olarak sunma.

**Kabul:** Üretim benzeri hedefte HTML/CSS/JS/JSON/XML/model/görsel için
header örnekleri ve tekrar ziyaret davranışı kaydedilir; `.toml` dosyasının
varlığı yeterli sayılmaz.

## HOST-04 — Build tekrar üretilebilirliği ve yayın yöntemi: P2

Netlify `HUGO_VERSION=0.151.0` kullanıyor (`netlify.toml:30`); yerel kurulum
farklı bir sürümle derleniyor ve tema uyumluluk uyarısı veriyor. Kaynakları
güncellemeden aynı çıktının hangi sürümde üretileceği sabitlenmeli; tema
güncellemesi bu denetimin dışında kalır.

`netlify.toml:26` build komutu tema örnek klasörünü ve mevcut public'i silip
`--gc` çalıştırır. Yeni sunucuda bunu kontrolsüz canlı dizinde kullanmayın.
Yeni klonda tema submodule'ünün pinned commit'i alınmalı; root build,
staging doğrulaması ve atomik yayın/geri alma adımları ayrılmalı.

**Kabul:** Belirlenmiş Hugo Extended sürümü ve tema commit'iyle ayrı build
alınır; manifest/hash ve tarama testleri saklanır; eski çalışan sürüme
dönüş yolu doğrulanır. Üretimde Hugo watcher/dev server çalıştırmak gerekmez.

## HOST-05 — Dış bağımlılıklar ve ölçüm kapsamı: P2

- 3B: `layouts/partials/three-heart.html:67–69` Skypack modüllerini
  dinamik import eder; `layouts/shortcodes/three-heart.html:46–48`
  doğrudan import eder. Gerçek homepage yolu ve maliyet performans
  raporunda ele alınmalıdır; dosyaları taşımak CDN bağımsızlığı sağlamaz.
- Analytics: `layouts/partials/extend-head-uncached.html:9–24` yalnız
  production + Hugo server olmayan çıktıya eklenir. Kullanıcının
  `hugo serve` testi bu isteğin üretim maliyetini içermez.
- Randevu/WhatsApp hedefleri dış hizmetlerdir; yerelde modalın açılması
  dış sağlayıcının rezervasyon veya ileti akışını doğrulamaz.

**Kabul:** CDN hata/fallback ve CSP kararları, font/JS/görsel kaynakları,
3B davranışı ve üretim Analytics yükü ölçülür; gerçek mesaj/randevu işlemi
otomatik denetimin kapsamına sokulmaz.

## CT-09 — Veri akışı ile görünür gizlilik bilgisinin eşlenmesi: P2, güçlü aday

Üç dilde gizlilik sayfası mevcut: `/kvkk/`, `/en/privacy/`, `/ar/privacy/`.
`content/tr/kvkk/index.md:30–55` iletişim formu/WhatsApp ve sağlık bilgisi
toplama olasılığını açıklıyor. Form `content/tr/iletisim/index.md:63–80`
ad, telefon, isteğe bağlı e-posta ve serbest metin istiyor; üretim head'i
`layouts/partials/extend-head-uncached.html:9–24` Google tag ekliyor.
İncelenen gizlilik metinlerinde Google Analytics/Netlify hizmet adı ve
saklama süresi yok. Gerçek veri işleme/saklama düzeni, çerez/ağ davranışı
ve onay tercihlerinin yürürlükteki gereklilikleri karşılayıp karşılamadığı
bu denetimde doğrulanmadı. Bu kayıt hukuki ihlal veya her ziyaret için
zorunlu onay gerektiği hükmü değildir.

**En küçük sonraki adım:** Yeni form/analitik sistemi seçilirken gerçek veri
akışını ve sağlayıcıları işletme sorumlusu ile eşlemek; sağlık verisi
istenmesini sınırlandırmak ve görünür metni gerçek işlemlerle uyumlu hale
getirmek. Gereken hukuki değerlendirme uzman tarafından yapılmalıdır.

**Kabul:** Kontrol sahibi onaylı veri akışı (alan/amaç/alıcı/saklama süresi),
üç dilde bu akışla uyumlu bilgilendirme ve üretimde gerçek çerez/ağ/tercih
testleri; mesaj teslimi testiyle aynı yetkili staging kapsamı. Şimdiki
durum: kaynak bulguları doğrulandı, hukuki sonuç ve runtime tercihler
**Doğrulanamadı / NOT_RUN**.

## Henüz tamamlanmayan sunucu kabulü

| Kontrol | Bu alt incelemedeki durum | Tamamlama yolu |
| --- | --- | --- |
| DNS A/AAAA/CNAME/NS | Google Public DNS JSON: apex A/AAAA Status 0 Answer yok; www A/CNAME Status 3; NS dört p08.nsone.net; kontrol google.com başarılı | NET-01 P0; ikinci bağımsız resolver ve yetkili zone/amaçlanan yayın hedefiyle doğrulama gerekli |
| www/apex HTTP→HTTPS, TLS/sertifika | Doğrulanamadı | Hedef sunucu/alan adı üzerinden GET/HEAD ve sertifika testi |
| Yeni sunucu ürünü ve yapılandırması | Bilinmiyor | Gerçek hedef/platform bilgisi ve read-only yapılandırma incelemesi |
| Lokalize 404/301 ve eski URL'ler | Kaynak kuralları var; hedef HTTP testi yok | Staging yanıt matrisi |
| Form teslimi | Gönderilmedi; Netlify bağımlılığı statik doğrulandı | Yetkili kontrollü staging teslim testi |
| Üretim sıkıştırma/cache/HTTP sürümü | Doğrulanamadı | Gerçek header ve cold/warm ziyaret ölçümü |
| İzleme, log, rollback | Depoda hedef platform çözümü doğrulanmadı | Yayın ve geri alma planı + güvenli erişim/log kapsamı |

## Birincil kaynaklar

24 Kasım 2026'da bu turda yeniden açılarak erişildi; bölüm bazında kontrol
notları `evidence/recheck-content-sources.md` içindedir:

- [Netlify — Redirects and rewrites](https://docs.netlify.com/manage/routing/redirects/overview/)
- [Netlify — Custom headers](https://docs.netlify.com/manage/routing/headers/)
- [Netlify — Forms setup](https://docs.netlify.com/manage/forms/setup/)
- [Google Public DNS — JSON API](https://developers.google.com/speed/public-dns/docs/doh/json)

DNS ham kanıtı: `evidence/browser-public-dns.json`. Önceki shell denemesinde
kontrol alan adları da çözülemediğinden yalnız shell sonucuyla site arızası
çıkarılmamıştır. Kamu DNS sonucu ayrı, başarılı kontrol içeren yüzeydir.
Tek resolver yanıtından kesinti süresi, domain süresi dolması veya sorumlu
kişi çıkarılamaz. SOA primary adındaki p01 ile NS kümesindeki p08 farkı da
tek başına yanlış yapılandırma kanıtı değildir.

Bu kaynaklar Netlify davranışlarını açıklar; henüz seçilmemiş yeni sunucunun
aynı davranışları uyguladığının kanıtı değildir.
