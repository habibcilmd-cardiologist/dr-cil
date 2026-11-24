# Yayın hazırlığı — 24 Kasım 2026

**Deploy yapılmadı; yayın kabulü tamamlanmış değildir.** Yerel kaynak ve çıktı
kabulü geçti; klinik veri/gerçek browser/origin kapıları aşağıda bekliyor.

## Somut release paketi

- Üretilen kök: `/tmp/dr-cil-implementation-after-20261124-release/public`.
- Build log ve SHA-256 manifest: evidence/final-build.log ve final-build-manifest.json.
- Kaynak farkı/yeni dosyalar: evidence/source-changes.patch ve final-preservation.json.
- Builder: `npm run build -- --output /tmp/dr-cil-yeni-bos-release`.
  Hedef yeni veya boş olmalıdır; eski release'e yazma reddedilir.
- Pin Hugo Extended0.167.0, tema7ce8be1/v2.93.0; tema bildirilen aralık üstü
  uyarısı vardır. Yerel derleme/çıktı testleri bu uyarıyı yok sayarak resmi
  tema uyumluluk veya tam tarayıcı garantisi vermez. Canlı Netlify ayarı değişmedi.

Üretim build'i geçici klasördedir; kalıcı release arşivi yerine geçmez.
Kod/rapor/manifest depoda; aynı komutla ayrı yeni build üretilebilir. Kamuya
sunulacak dosyalar yalnız public altıdır; cache/resources/manifest/raporları
web köküne kopyalamayın. Netlify'nin yeni yerel build tanımı artık --gc veya
tema/public silme komutu çalıştırmaz.

## Dış kapılar ve yapılacak tek somut adım

| Kapı | Şu anki kanıt | Tamamlama |
| --- | --- | --- |
| Browser/performans | Baseline1314hash eş; yeni port bind yasak; native Chrome1313ERR_CONNECTION_REFUSED | Port izni ve erişilebilir güncel test sunucusu olan ortamda bu release'i ayrı sun; 3+3cold/warm/native200 paketini çalıştır |
| DNS | Yeni DoH sorgularında site cevabı yok; kontrol başarılı; kayıt değişmedi | Yetkili zone+amaçlanan origin;authoritative/iki resolver ile A/AAAA/CNAME/NS |
| TLS ve yönlenme | Kaynak `_redirects` kuralları; gerçek yanıt yok | Apex/www/HTTP→HTTPS/sertifika ve IPv6 varsa ölç |
| HTTP404/301 | Dil şablonları ve explicit rules yerel kabulden geçti | Gerçek sunucuda doğru dilde404; tek301/query/UTF-8; SPA home200 yok |
| Form | Varsayılan disabled, gerçek telefon/WhatsApp;8statik senaryo geçti | Gerçek backend/teslim adresi seç;yetkili staging sentetik teslim+error/spam+teşekkür |
| Header/cache | Netlify kaynak politikası korunur; yeni sunucu bilinmiyor | Seçilen sunucuya açık aktarım;HTML/JSON/XML revalidation, MIME/ETag/Brotli/gzip/TLS |
| Google/schema | Tüm script yerel parse/kurallar0; resmî test yeni değil | Temsilci TR/EN/ARproduction koduyla Validator+RRT;GSCURLInspection ayrı |
| Klinik gerçeklik | 8kimlik onayı,12klinik taslak,47% satırı korunur | Kayıt sahibi/hekim;doğru yıl/saat/sayı/kaynak/review |
| GSC/GBP/CrUX | Yetkili araç/veri bulunmadı; hesap değişmedi | Performancequery/page/device/country;indexing/sitemap/canonical/security/manualaction;GBPbilgileri;CWVdönemi |
| İndeks politikası | 53kesin arşiv dolduruldu,2unknown;eski canonical'lar korunur | Gerçek ihtiyaç/URLverisiyle kalan taxonomy/metadata kararı;otomatiknoindex/silme yok |

Tek ortam adımı için örnek **yerel önizleme** komutu (bu ortamda bind
reddedildi; kullanıcı sunucusunu durdurmadan izinli bir boş port gerekir):

```sh
python3 -m http.server 1315 --bind 127.0.0.1 --directory /tmp/dr-cil-implementation-after-20261124-release/public
```

Bu Python önizlemesi Netlify redirect/header/form veya dil bazlı404 kurallarını
uygulamaz; yalnız UI/performans önizlemesidir, üretim hosting seçimi değildir.
Sunucu türü bilinmediği için çalışmış Nginx/Caddy/Apache ayarı icat edilmedi.

## Yayın ve geri dönüş sırası

1. Yetkili platform/hedef ve gerçek kayıtlar belirlenir; bekleyen klinik bilgi
   kararları kaynaklara aktarılıp yeni ayrı build/test paketi alınır.
2. Eski çalışan release, DNS/TTL ve platform kural snapshot'ları korunur.
3. Staging'de bütün kritik kabul ve form teslim yetkisi tamamlanır. Telefon/
   WhatsApp linkine tıklama mesaj/gerçek randevu veya teslim sayılmaz.
4. Yayın yetkisi ayrı verildiğinde doğrulanmış public release atomik aktive
   edilir; DNS/hesaplarda izinsiz işlem yapılmaz. --gc/canlı klasör temizliği yok.
5. Health/HTTP/telemetry kabulü başarısızsa önceki doğrulanmış release'e atomik
   geri dönüş; eski sistem teslim teyidi olmadan kapatılmaz. Bu tatbikat yapılmadı.

GSC baseline: 8konu kümesi+brand/non-brand, sayfa/cihaz/ülke; eşlenebilir dönem
ve kesinti boşlukları. Organik sonuç, harita görünürlüğü ve gerçek iletişim
ayrı ölçülür. Hasta adı/iletişim/sağlık metni analytics event'e aktarılmaz.
Sıralama/CTR/traffic artışı veya ceza nedeni bu veriler olmadan ilan edilmez.
