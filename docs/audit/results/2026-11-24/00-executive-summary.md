# Yönetici özeti — 24 Kasım 2026

**Karar:** Kaynakta düzeltme yapılmadan teşhis ve uygulama listesi hazırlandı.
Mevcut en ciddi yayın bulgusu DNS adres çözümlemesidir; görünür ilk düzeltme
menü ve uzmanlık kartıdır. Üretim masaüstü/mobil performansı henüz ölçülmedi;
bu rapor hız veya sıralama başarısı ilan etmez.

Başlangıç commit `2fad17e0b2e07e38dceadaccc7c877732ee10d19`, Blowfish `7ce8be1`
(v2.93.0), Hugo Extended 0.167.0. Aynı denetimde toplanan
kanıtlar ve ek çevrimdışı tekrar kontrolleri birlikte korundu. Kaynak hashlerinin tamamı önceki manifestle eşleşti;
bu turdaki schema, varlık ve içerik tekrar taramaları ayrı `recheck-*`
dosyalarındadır. Kullanıcının başlattığı ayrı 1314 production sayfası da açıldı; sonraki
ölçüm çağrısı kesildiği için üretim hız koşusu tamamlanmadı. Son karşılaştırmada
başlangıçtaki 593 dosya hash'i aynı, tema temiz; HEAD dışarıdan değişti
(`evidence/final-preservation.json`). Çalışma sırasında HEAD dışarıdan `b2944ac5` oldu; kaynak byte'ları değişmedi. Kod/içerik, DNS,
çalışan Hugo, hesaplar ve yayın değiştirilmedi; commit/push/deploy yapılmadı.

## Kullanıcının sorularına doğrudan yanıt

1. **Menü:** Kaydedilmiş gerçek tarayıcı ölçümünde 1024/1280/1440/1920 CSS px'de
   altı etiketin tamamı iki satır ve 48px yüksek. Uzun marka aynı flex
   satırında alan tüketiyor; linkler `flex-shrink:1`, `white-space:normal`,
   `word-break:break-word`. Menü `md=853px`'de açılıyor. `nowrap` yalnız
   marka seçicisinde; `disableTextInHeader` parametresi şablonun aradığı
   seviyede değil. Kaynak: `header/basic.html:25,212–220`,
   `custom.css:20–23,55–57`, tema `main.css:146–150` (**UI-01**).
2. **Uzmanlık kartı:** `i18n/tr.yaml:26` doğrudan “Damar Açma”; fallback
   `hero_expertise_3` de `:12` aynı değer. `home/hero.html:149–150` bunları
   gösteriyor. EN/AR da damar müdahalesi anlamında. Hedef üç dilde
   Girişimsel Kardiyoloji olmalı (**UI-02**).
3. **Performans:** Üretim Lighthouse, soğuk/sıcak ziyaret, saha CWV ve
   CPU/GPU karşılaştırması **çalıştırılmadı**. Development 3+3 tanılama
   üretim ölçümü değildir. Mobilde yalnız dar viewport kullanılmış;
   fiziksel telefon/CPU/ağ profili yok. Ayrıntı [04-performance.md](04-performance.md).
4. **3B:** Gerçek yol `home/profile.html:6` →
   `interventional-cardiology-diagram.html:16` → **partial** `three-heart.html`.
   Aktif GLB **1.511.228 bayt**, 12 HTML'de çağrılıyor. Observer 100px yaklaşım
   payı ve idle timeout 2000ms kullanıyor. Desktop 3/3 koşuda scroll
   olmadan model başladı; mobilde scroll sonrası. Kod sekme gizliyken duruyor,
   viewport dışına çıkınca durmuyor. Kaynak davranışı doğrulandı; toplam
   CPU/GPU maliyeti ve puana etkisi ölçülmedi (**PERF-01/02**).
5. **Schema:** 679 scriptin tamamı JSON olarak ayrışıyor. Buna rağmen 628
   route'ta breadcrumb sıra sorunu, 165 hizmette çelişen breadcrumb kimliği,
   495 uygunsuz `performer` ve 132 enum dışı `procedureType` var.
   `Cardiovascular`, `MedicalScholarlyArticle`, `EventScheduled` güncel
   sözlükte geçerli; sonuncusunun sayfaya uygun anlamı ayrı meseledir.
   Saatler ve otomatik review/otorite iddiaları gerçek bilgiyle teyit ister.
   FAQ rich-result gösterimi 7 Mayıs 2026'da kaldırılmıştır; yararlı SSS
   içeriğini silme gerekçesi değildir. Resmî validator testi yalnız tek DEV kod
   örneğidir; bütün production için resmî geçiş yok
   ([dört ayrı sonuç](03-schema-audit.md)).
6. **DNS/SEO/yerel görünürlük:** Denetimde alınan kamu DNS yanıtında apex
   A/AAAA NODATA, www NXDOMAIN, kontrol alan adı başarılı (**NET-01, P0**).
   Bu turdaki web sorguları alan adına yanıt getirmedi; güncel DNS sonucu
   üretmedi. İkinci resolver, TLS/origin, kesinti süresi ve registrar nedeni
   bilinmiyor. 976 HTML = 297 alias + 3 hata + 676 diğer route;
   ayrı canonical sayısı 652, Google indeks sayısı değil. Redirectler
   hesaba katılınca 66 çözülemeyen bağlantı kullanımı, 24 pagination canonical
   sorunu var. GSC/GBP/SERP verisi alınmadı; sıralama kaybının nedeni bilinmiyor.

## İlk on iş ve ölçülebilir kabul

| Sıra / iş | Kabul |
| --- | --- |
| 1. NET-01: yetkili zone ve yayın hedefini doğrula | İki resolver + authoritative kayıt; apex/www politikası, geçerli TLS ve HTTP 200 |
| 2. UI-01/02: menü ve uzmanlık | 320–1920, 852/853/854 ve gerçek %200 zoom; bölünme/kırpma yok, üç dil doğru |
| 3. UI-03/04: mobil menü ve modal odağı | Tab/Enter/Space/Escape, odak döngüsü/dönüşü ve scroll kilidi geçer |
| 4. STATIC-01/04: CTA/link/anchor | 66 çözülemeyen kullanım ve dört yanlış fragment sıfır; doğru dilde HTTP hedef |
| 5. HOST-01/02: taşıma ve form | Gerçek lokalize 404, tek 301; staging'de sentetik formun teslim/teşekkür/hata akışı |
| 6. SCH-01–05/07: schema üretimi | Sıra/@id/domain/enum hataları ve eksik görsel sıfır; semantik tür matrisi + resmî örnek test |
| 7. CT-01/03/04, SCH-06/08: bilgi dayanakları | Doğum yılı/saatler tutarlı; sayı, klinik oran ve review iddiaları belgeli |
| 8. STATIC-02/03: canonical/sitemap | Her gerekli pagination doğru canonical; üç dil tek açık sitemap keşif politikası |
| 9. PERF-01–05: üretim ve 3B ölçümü | En az 3+3 aynı koşullu cold koşu, sıcak ziyaret ayrı; izler ve A/B; medyan/aralık |
| 10. CT-05/06/08, STATIC-05–07: içerik ve ölçüm | Sekiz sorgu/amaç onayı; doğru iç bağlantılar; GSC/GBP baseline veya eksik veri kaydı |

Her işin eforu, bağımlılığı, riski ve geri dönüşü
[06-remediation-backlog.md](06-remediation-backlog.md) içindedir. Bütün
bulgular ve kanıtlar [01-findings.md](01-findings.md), URL/şablon ve
çalıştırılmayan testler [08-coverage-and-limitations.md](08-coverage-and-limitations.md) içindedir.

**Açık kalan tek çalışma koşulu:** Tarayıcı bağlantısı ve ayrı üretim test
sunucusuna izin verilen bir ortamda belirtilen runtime/performance paketini
çalıştırmak. DNS/GSC/GBP ve klinik bilgi için ilgili yetkili kayıt/export'lar
ayrı veri bağımlılığıdır. Bu eksikler başarı sonucuna çevrilmedi.
