# Apache yayın dosyası, ana sayfa ve metadata kabulü

24 Kasım 2026. Yerel Mac deposuna erişim yeniden kuruldu; önceki ZIP taslağı
yerine gerçek güncel kaynaklar üzerinde çalışıldı. Deploy/DNS/hesap değişikliği
ve gerçek form/mesaj/randevu gönderimi yapılmadı.

## Teslim edilen yalın dosya

- Depo kökü: `/Users/yavuz/prg/dr-cil/.htaccess`.
- Hugo kaynağı: `/Users/yavuz/prg/dr-cil/static/.htaccess`.
- Yeni üretim çıktısı:
  `/Users/yavuz/prg/dr-cil/output/releases/apache-publication-20261124-01/public/.htaccess`.
- Üç dosya byte-eş; SHA-256
  `85b1db30d8c1ccb496917d8c8e1d9467bd215846e738a2e200febcabfc5ff965`.
- Mevcut eski `public/` klasörü temizlenmedi veya üzerine toplu build alınmadı.
  Yayın için yukarıdaki **yeni üretim çıktısının** public içeriği kullanılmalı.

Dosya, gerçek `static/_redirects` haritasındaki kesin eski yolları genel /tr
kuralından önce uygular; query/encoded yol korunur. Üç dilde gerçek 404,
MIME/cache/ETag/gzip ve kaynak dosyası korumaları vardır. Detay ve gerçek
Apache kabulü: `01-apache-rules-and-validation.md`, `apache-fixture-test.json`.

HTTP→HTTPS zorlaması hedef host/CDN'nin güvenilir TLS topolojisiyle kurulmalı.
Doğrudan Apache TLS bloğu bu bilgi olmadan etkinleştirilmedi. PHP desteği tek
başına .htaccess desteği değildir; Apache/uyumlu sunucu ve override izinleri
gereklidir. Hedef yayın sunucusunda TLS/proxy kabulü henüz yapılmadı.

## İstenen metin

`content/tr/_index.md:25` artık şu ifadeyle başlıyor:

> İstanbul'da çalışan Girişimsel Kardiyolog Doç. Dr. Habib ÇİL’in

Mesleki geçmiş, yayın, hizmet ve iletişim linkleri korundu; yerel alan adı
hardcode edilmedi. Derlenmiş gerçek HTML metni de doğrulandı. Bu sınırlı metin
değişikliği sitenin tamamına hukuki uygunluk onayı anlamına gelmez.

## Gerçekten geçen kontroller

| Alan | Sonuç | Kanıt |
| --- | --- | --- |
| Yeni production build | Exit 0; 967 HTML, 673 JSON-LD | Release `build.log`, `build-manifest.json` |
| Apache kuralları, izole gerçek sunucu | Bütün kontroller geçti | `apache-fixture-test.json` |
| Gerçek yeni çıktı / yerel Apache HTTP | 17/17 | `evidence/real-output-http.json` |
| Yerel schema/breadcrumb regresyonu | 0 hata; 267 FAQPage, 367 görünür breadcrumb | `evidence/schema-output.json` |
| Statik release kabulü | 32/32; sekiz hedef ve eski canonical'lar korundu | `evidence/release-checks.json` |
| Metadata çıktı taraması | 967 HTML / 673 nonalias; 0 hata | `evidence/metadata-output.json` |
| Analytics guard | 10/10; VM/mock, gerçek istek yok | `evidence/analytics-guard.json` |
| Sitemap | TR 258 + EN 196 + AR 198 = 652; üç XML gerçek yerel HTTP 200 | Metadata ve HTTP JSON'ları |

GSC doğrulama token'ı ve mevcut GA4 `G-TDC4PMVEMK` korundu. Üretim kodu
localhost/staging üzerinde ölçüm başlatmıyor; HTTPS üretim hostunda etkin.
OG/Twitter gerçek raster görsel, MIME, boyut ve alt metinle eşlendi; SVG
diyagramlar sosyal paylaşım görseli olarak kullanılmıyor. Kare mevcut görseller
için summary kartı seçildi; yeni yatay görsel veya yeni görsel iddiası yok.
Detay: `metadata-and-structured-data.md`.

## Çalışan port ve durdurma sınırı

- Güncel derleme **Apache 2.4.67 ile http://127.0.0.1:1313/** üzerinde çalışıyor.
- Ana sayfa GET 200; 110860 bayt ve SHA-256
  `1f430d052ef64ba0cbe7d156156bfed129dd5bd09d375ca6e546692b4e270184`;
  yerel release dosyasıyla ham HTTP gövdesi birebir eşleşiyor.
- Yeni Apache ana PID: 98490. Prefork worker PID'leri aynı sunucunun
  çocuklarıdır; ayrı site sunucuları değildir.
- Kullanıcının önceki **Python PID 76204 / 1314** sürecini durdurma yetkisi
  kullanıcı tarafından verildi. Ancak `os.kill(76204, SIGTERM)` yürütme
  kısıtı nedeniyle `PermissionError: [Errno 1] Operation not permitted` verdi.
  Başka API/terminal yoluyla aynı engellenen sinyal denenmedi.
- Bu nedenle **bütün eski sunucular kapatıldı** veya **1314 yeniden başlatıldı**
  sonucu verilmez. Eski 1314 hâlâ eski derlemeyi sunuyor. Kullanıcı kendi
  terminalinde bu mevcut eski süreci kapatabilir: `kill 76204`.
- 1315 ve geçici Apache test portu 1316 kapalıdır.

İlk gerçek public ön kontrolünde minimal Apache config, depo kökündeki
.htaccess'i nested public üstünden miras alarak 500 verdi; eski 1314 o sırada
korundu. Önizleme virtual-host sınırı `<Directory /> AllowOverride None`
ve yalnız derlenmiş public için `AllowOverride All` olacak şekilde düzeltildi.
Sonraki gerçek çıktı kabulü 17/17 geçti. Bu, .htaccess kısıtını aşmak değil,
yalnız yayın kökünde kuralları okuyacak yerel sunucu yapılandırmasıdır.

Yeni server/config/GET kanıtı: `evidence/server-start.json`.

## Çalıştırılmayanlar / dış bağımlılıklar

- Gerçek yayın hostunun TLS, CDN/proxy, DNS ve PHP handler davranışı.
- Search Console hesabında sahiplik/indeks veya Analytics hesabında olay teslimi.
- Sosyal platformların canlı paylaşım önizlemeleri.
- Yeni resmî Schema.org/RRT koşuları; bu tur schema JSON-LD mantığı değişmedi.
- Gerçek tarayıcı etkileşimi ve 3+3 üretim performans/CWV ölçümleri.
- Eski dış Python sürecini kapatma/aynı portu yeniden başlatma, yukarıdaki
  yürütme kısıtı nedeniyle tamamlanamadı.

Google FAQ rich result desteğinin 7 Mayıs 2026'da kaldırılması güncel resmî
kayıttan doğrulandı. Görünür FAQ semantiği korunur; Google FAQ görünümü veya
sıralama artışı kabul sonucu üretilmez. Önceki kabul/denetim kanıtları korundu.
Commit/push yapılmadı. Kullanıcının `library.html` dosyasına dokunulmadı.
