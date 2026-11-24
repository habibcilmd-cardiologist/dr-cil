# Apache/PHP hosting — yayın kuralları ve yerel kabul

Tarih: 24 Kasım 2026. Apache 2.4.67 üzerinde gerçek yerel HTTP fixture kabulü:
**56 kontrol geçti, 0 başarısız**. Canlı sunucuya deploy yapılmadı.

## Kullanılacak dosya

- Kaynak depo kökü: `.htaccess`
- Hugo'nun çıktıya taşıdığı kaynak: `static/.htaccess`
- Yayın kökü: derlenmiş `public/.htaccess`

Kök ve static dosyası birebir aynı tutulmalıdır. Bu incelemedeki SHA-256:
`85b1db30d8c1ccb496917d8c8e1d9467bd215846e738a2e200febcabfc5ff965`.
Root ajanın oluşturduğu
`output/releases/apache-publication-20261124-01/public/.htaccess` de bu hash'le
eşleşti. Sunucuya **derlenmiş public klasörünün içeriği** yüklenir; depo, docs,
tema ve kaynak dosyaları web köküne yüklenmez. ZIP hazırlanmadı.

## Uygulanan davranış

| Kaynak satırı (`static/.htaccess`) | Davranış |
| --- | --- |
| 7 | Dizin listeleme ve MultiViews kapalı; index.html, normal klasör/slash ve UTF-8 |
| 14 | TR/EN/AR için yerel ErrorDocument; doğru dil ve gerçek HTTP 404 |
| 25 | Gizli ve yapılandırma/yedek kaynak dosyalarına erişim engeli; ACME yolu açık |
| 32 | Üretim domaininde nihai HTTPS/apex hedefi; localhost/staging kendi hostunda |
| 37 | `static/_redirects` içindeki 17 kesin emekli route; genel /tr kuralından önce |
| 44 | /tr ve /tr/* göçü; encoded Türkçe/Arapça yol ve query korunur |
| 49 | www → HTTPS/apex canonical; localhost canlı domaine yönlenmez |
| 64 | CSS/JS/JSON/XML/SVG/WebP/AVIF/WOFF2/GLB MIME türleri |
| 76 | nosniff, DENY, referrer; hatalar no-store |
| 83 | HTML/JSON/XML/txt tekrar doğrulama; değişebilir asset 1 gün |
| 91 | Yalnız adında 32–128 hex content hash bulunan CSS/JS immutable |
| 96 | Modüller varsa metin türlerine gzip; GLB ve sıkıştırılmış görsellere uygulanmaz |

Eksik her URL'yi ana sayfaya veya index.php'ye döndüren SPA rewrite yoktur.
PHP genel olarak yasaklanmadı; PHP çalıştırma desteği hostun sorumluluğundadır.
Körlemesine CSP/COEP/CORP veya HSTS preload eklenmedi.

## Gerçekten çalıştırılan kabul

Komut:

```sh
python3 scripts/tests/apache-publication.test.py --output docs/implementation/seo-remediation/2026-11-24/apache-publication/apache-fixture-test.json --port 1316
```

Script, sistem Apache'sini yalnız loopback 1316'da ayrı konfigürasyonla
çalıştırır; kullanıcı 1314 sürecine dokunmaz, iş bitince kendi sürecini kapatır.
Dinleyici kullanılamıyorsa açık başarısız kontrol ve nonzero exit üretir;
HTTP `NOT_RUN` olan bir koşu başarılı kabul edilmez.
Apache'nin kapanışta süreç grubuna sinyal gönderebilmesi nedeniyle fixture
`start_new_session=True` ile yalıtılmıştır. Apache testinin ilk çalıştırmasında
bu yalıtım eksikliği runner'ın exit 143 almasına yol açtı; runner düzeltildi,
son kabul ayrı fixture ile eksiksiz tekrarlandı.

- `.htaccess` gerçek `<Directory>` bağlamında include edilerek syntax: `Syntax OK`.
  Yalnız `httpd -t` çalıştırıp henüz okunmamış .htaccess'i geçmiş sayma hatası yoktur.
- TR/EN/AR ve hizmet klasöründe index.html: 200.
- 17 eski kesin URL: 301, localhost korunur, query aynıdır.
- /tr kökü, genel hizmet, encoded Türkçe/Arapça ve `%23`: doğru Location.
- Üretim www Host başlığıyla eski URL/hizmet: tek son HTTPS/apex 301 hedefi.
  Bunlar yerel Host-header testleridir; dış domaine istek takip edilmedi.
- Üç dilde olmayan URL: doğru dil gövdesi + gerçek 404 + `Cache-Control: no-store`.
- Üç sitemap, robots ve arama JSON'u: tekrar doğrulama.
- JSON/XML/GLB MIME; mutable CSS 1 gün; hashli CSS 1 yıl immutable.
- Olmayan hashli CSS: 404, immutable uygulanmaz.
- Gerçek gzip + Vary ve açılmış doğru gövde.
- ETag ile koşullu istek: 304; güvenlik başlıkları.
- Gizli/yapılandırma dosyası: 403; `.well-known/acme-challenge` fixture: 200.

Ham kayıt: [apache-fixture-test.json](apache-fixture-test.json).
Kayıttaki `work` klasöründe gerçek konfigürasyon ve Apache logları bulunur;
kalıcı JSON içinde startup/error logları da korunmuştur.

## Hedef hostta tamamlanması gerekenler

PHP barındırma tek başına `.htaccess` desteği demek değildir. Hedef Apache veya
uyumlu LiteSpeed olmalı; Nginx ve PHP'nin kendi geliştirme sunucusu bu dosyayı
uygulamaz. Modüller ve izin verilen `.htaccess` override direktifleri hostta
doğrulanmalıdır. Bu fixture `AllowOverride All` kullanır; üretimde host yöneticisi
gerekli direktifleri kendi yapılandırmasında açıkça izinli tutmalıdır.

Derlenmiş çıktı depo altında sunuluyorsa üst dizinlerdeki kaynak `.htaccess`
dosyalarının mirası ayrıca sınırlandırılmalıdır. Vhostta genel sınırı kapatıp
yalnız gerçek DocumentRoot için override açma örneği:

```apache
<Directory />
    AllowOverride None
    Require all denied
</Directory>
<Directory "/absolute/path/to/compiled/public">
    Options FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>
```

Bu vhost yapılandırması `.htaccess` dosyasına konmaz. Yalnız public kökündeki
yayın dosyasının uygulanmasını sağlar; kaynak depo kökündeki kopya yayın
konfigürasyonunun ikinci kez uygulanmasına yol açmamalıdır.

**HTTPS/topoloji kapısı açık:** Apex HTTP→HTTPS zorlaması kaynaktaki 53–59.
satırlarda açıklamalı ve devre dışıdır. Sertifika ve host/CDN HTTPS zorlaması
yayından önce doğrulanmalıdır. TLS doğrudan Apache'de sonlanıyorsa açıklamalı
blok etkinleştirilebilir. TLS reverse proxy/CDN'de sonlanıyorsa zorlama orada
yapılmalı veya güvenilir proxy eşlemesi sunucu düzeyinde yapılandırılmalıdır.
Rastgele X-Forwarded-Proto'ya güvenilmez; aksi takdirde HTTPS döngüsü oluşabilir.
Mevcut www ve eski üretim URL kuralları nihai HTTPS adresini hedefler, fakat
bu tek başına apex HTTP zorlaması veya TLS sertifikası kabulü değildir.

**Çalıştırılmadı:** gerçek yayın hostu/TLS/proxy/CDN kabulü, Brotli, HTTP/2–3,
uzak DNS, gerçek PHP backend/form teslimi. JSON sonucu bu alanlarda başarı
iddiası değildir. Dosya sentaksı ve yerel HTTP kabulü tüm sağlayıcılarda
kusursuz çalışma garantisi vermez.

Birincil belgeler (24 Kasım 2026'da okundu):

- https://httpd.apache.org/docs/2.4/howto/htaccess.html
- https://httpd.apache.org/docs/2.4/custom-error.html
- https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html
- https://httpd.apache.org/docs/2.4/rewrite/flags.html
- https://httpd.apache.org/docs/2.4/mod/mod_headers.html
- https://httpd.apache.org/docs/2.4/mod/mod_deflate.html
