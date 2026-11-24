# Önceliklendirilmiş uygulama listesi — 24 Kasım 2026

Bu dosya uygulanmış düzeltme kaydı değildir. Kaynak ve canlı sistem bu turda
değiştirilmedi. Eforlar mevcut yapıya dayalı mühendislik tahminidir; DNS
yayılımı, sağlayıcı/hesap erişimi ve klinik inceleme beklemesi dahil değildir.
Bir mühendislik günü yaklaşık 6 saat odaklı çalışmadır. Başarı, aşağıdaki
kabul kanıtıyla verilir; yalnız kod/build geçişiyle iş kapatılmaz.

## İlk on uygulama paketi

Yönetici özetindeki 1–10 sırası aşağıdaki B01–B10 ile aynıdır. P0 yalnız
gerçek kayıt zamanındaki DNS yayın engelidir; aday SEO etkileri P0 değildir.
Hesap/DNS/yayın değişiklikleri bu denetimin dışındadır; ileride uygulanacak
işler için gerçek hedef ve yetki ayrıca esas alınmalıdır.

| Paket / öncelik / dalga | Bulgular; en küçük kapsam ve dosyalar | Efor; bağımlılık; risk | Ölçülebilir kabul | Geri dönüş |
| --- | --- | --- | --- | --- |
| B01 / P0 / 1 | NET-01. Yetkili zone + seçilen platform/origin hedefini doğrula; kayıt planını hazırla. Kaynak alan adı `hugo.toml:1`; mevcut DNS'yi tahminle değiştirme. | 0.5–1 gün + dış bekleme; domain/platform kaydı; yanlış hedef veya MX etkisi | Authoritative ve iki bağımsız resolver'da beklenen A/AAAA/CNAME/NS; apex/www, IPv4/IPv6 (varsa), HTTP→HTTPS zinciri; geçerli TLS; home/robots/sitemap GET başarılı. İkinci resolver ile mevcut teşhisi önce yenile. | Kayıt değişimi yapılacaksa önce zone/TTL snapshot'ı; doğrulanmış eski hedefe kayıt dönüşü; çalışan siteyi kaldırmadan geçiş. |
| B02 / P1 / 1 | UI-01/02. `header/basic.html:25,212–220`, `header/fixed.html:6`, `custom.css:20–57`, `params.toml:70–78`, `home/hero.html:149–150`, `i18n/{tr,en,ar}.yaml`. Parametre/koşul ve alan hesabını birlikte düzelt; doğrudan/fallback uzmanlık anlamını eşitle. | 1–2 gün; çalışan browser; header/RTL regresyonu | TR/EN/AR 320,360,390,430,768,852,853,854,1024,1280,1440,1920 CSS px, DPR kaydı, %100 ve native %200. Menü etiketlerinde harf bölme/kırpma/kaybolma yok; sığmadığında erişilebilir menü; kart doğru ve taşmıyor. Overflow gizleme veya aşırı küçültme çözüm sayılmaz. | Header/CSS/i18n değişiklik setini birlikte geri al; eski build sakla. |
| B03 / P1 / 1 | UI-03/04. `header/basic.html:94–107`, tema mobilemenu.js, `extend-footer.html:553–632`, `search.html:1–23`, `search.js:76–114`. Semantik düğme, adlandırma, modal odak çevrimi ve geri dönüş. Tema alt modülünü doğrudan değiştirmek yerine uygun yerel override seç. | 1–2 gün; B02 ile koordinasyon; scroll/odak çakışması | Klavye ile aç/kapat; Enter/Space/Escape, aria state; Tab/Shift+Tab arka plana kaçmaz; kapanınca açıcı odakta; scroll kilidi çözülür. Arama boş/hata/yeniden deneme/Enter ve ekran okuyucu adları testli. | İlgili JS/template setini birlikte geri al; menü/aramanın önceki çalışan build'i. |
| B04 / P1 (anchor P2) / 1 | STATIC-01/04. `static-link-triage.json` tam hedef listesi, `content/en/services/myocardial-infarction/index.md:191`, EN blog CTA'ları; `content/en/_index.md:39`, `en/services/_index.md:67`. Mevcut doğru dil canonical'ını kullan; olmayan endpoint üretme. | 0.5–1 gün; URL sahiplik kararı; yanlış çeviri hedefi | Aynı tam çıktı taraması: çözülemeyen 66 kullanım/42 hedef ve 4 yanlış fragment sıfır; örnek CTA'larda GET ve yönlenme doğru; sabit header hedef başlığı örtmüyor. Mevcut /tr redirect'leri çift hata sayılmaz. | İçerik link diff'ini geri al; gerekli gerçek redirect'leri kaldırma. |
| B05 / P1 / 1 | HOST-01/02, UI-07. Üç contact formu `index.md:56–58`, teşekkür leaf-bundle dosyaları; `static/_redirects:5–11`, `netlify.toml:20–23`; `layouts/404.html:8–43` ve i18n. Backend + bağımsız teşekkür route'u + gerçek server 404/301 politikası; Arapça mesaj ve /ar/, /ar/contact/ çıkışları. | 1–3 gün; hedef server/servis ve teslim adresi belli olmalı; mesaj kaybı/yanlış başarı | Yetkili staging'de sentetik test: POST başarılı/başarısız, spam, teslim, teşekkür ve hata yolları; her dilde doğru metin/çıkışlarla gerçek 404; /tr GET tek 301 ve query/UTF-8 korunur. Form action gerçek POST endpoint'ine doğrudan bağlanır; payload teslimi ve başarı sonrası teşekkür GET akışı ayrı kanıtlanır, POST'un 301 boyunca korunmasına güvenilmez. | Eski platform ve backend çalışırken geri dönüş URL/DNS planı; teslim teyidi olmadan eski akışı kapatma. |
| B06 / P1 / 2 | SCH-01–05/07. `schema.html:38,78–95,146–150`, `schema-procedure.html:9,29–79`. Tek breadcrumb kaynağı; 1..N; doğru @id, property, enum, yayımlanan image; hastalık/test/işlem ayrımı. | 1–2 gün + hekim sınıflandırması; B04 URL'leri; ortak graph regresyonu | 679 route'un JSON-LD tamamı parse olur; 628 sıra/165 kimlik/495 performer/132 enum uyumsuzluğu ve eksik görsel sıfır. Her hizmetin gerçek türü belgeli; tek temsilci yerine TR/EN/AR ve ana şablonlarda Validator + RRT kod testi. Rich-result desteği ve içerik doğruluğu ayrı kaydedilir. | Schema override'larını tek paket geri al; eski ve yeni graph snapshot'ları sakla. |
| B07 / P1 / 1 (bilgi) + 2 (schema) | CT-01/03/04, SCH-06/08. TR/EN/AR about:16,21; hero:60–69; contact:27; schema:70–72; procedure:29,47,61–62; hedef klinik oranlar. Önce gerçek CV/saat/sayı/review/kaynak, sonra tek bilgi kaynağı. | 1–2 mühendislik günü + hekim/klinik beklemesi; gerçek kayda erişim; yanlış sağlık/otorite iddiası | Üç dil doğum yılı ve görünür/schema saatleri aynı gerçek kayıtla uyuşur. 25+/20K+/100+ tanımı/tarih/dayanak belli; tıbbi oranlar hasta grubu/sonlanım/takiple kaynaklı; lastmod tıbbi review sayılmaz; dayanaksız kurum onayı üretilmez. | Onaylı bilgi snapshot'ı; eski çelişkiyi yeniden yaymak yerine doğrulanmamış alanı askıya alma kararı kaydedilir; kaynak diff'i geri alınabilir. |
| B08 / P2 / 2 | STATIC-02/03. Tema head/list override'ı, `extend-head-uncached.html:26–33`, `static/sitemap.xml`, `robots.txt`, yerel sitemap şablonları ve hugo outputs. Tek XML sahipliği; gerçek pagination ve gereksiz home kopyalarını ayır. | 1–2 gün; B04 URL politikası; dil/pagination keşfini bozma | Gereken pagination kendi canonical'ına; 24/72 kök hata yeniden taramada kapanır veya gereksiz route bilinçli kaldırılır. Tek kök dil index'i ya da açık üç sitemap bildirimi; 652 mevcut canonical kayıpsız (bilinçli URL kararları ayrıca map'li), child XML GET200, self-redirect yok. | Eski XML/robots/override seti; URL kaldırılmışsa geçiş haritasını koru; GSC gönderimini aceleyle silme. |
| B09 / P2, ölçüm önce / 2 | PERF-01–05. Önce kaynak değiştirmeyen üretim benchmark; sonra `three-heart.html`, `home/hero.html`, vendor/head, `search.js` alanında ölçülen neden. Model silmek varsayılan çözüm değil. | Ölçüm 1 gün; hedefli değişiklik 1–3 gün; browser/izole test portu; görsel/interaction regresyonu | Minify production: desktop+mobile aynı koşullu ≥3 cold (tercihen5), sıcak ziyaret ayrı; medyan/aralık ve JSON/HTML/iz. Home+kritik service/blog. LCP öğe/alt süreleri, CLS kaynakları, long tasks, transfer, JS/DOM. Model tam/engelli kontrollü A/B; ilk viewport/scroll/offscreen/hidden/tekrar giriş; reduced-motion/Save-Data/CDN/WebGL fallback. Tek init/loop ve offscreen duruş ölçülür. TBT ≠ INP; saha hedefleri p75 LCP≤2.5s, INP≤200ms, CLS≤0.1; sonuç yoksa geçiş yok. | Benchmark öncesi build'i tut; her optimizasyonu bağımsız geri al; kalite/işlev kaybında poster/aktif model kararı yeniden değerlendir. |
| B10 / P2 / 3 | CT-05/06/08, STATIC-05–07. `05-keyword-url-map.csv`; TR blog/hizmet linkleri; author partial; manual taxonomy kaynakları; `index.json` lang.Merge ve metadata. Mevcut sayfa amaçlarını netleştir, kopya şehir/kelime sayfası üretme. | 2–4 gün + klinik/içerik onayı; B04/B07/B08; faydalı arşiv/çeviri kaybı | 8/8 sorgu mevcut canonical/niyet/hekim kapsamıyla onaylı; rehber↔ilgili hizmet ve yazar→biyografi yolu; boş 55 manuel sayfa için tek tek karar, 301 gerekirse kanıtlı; dil fallback görünür; duplicate metadata gerekçeli. GSC/GBP baseline ya alınır ya net eksik kaydı bırakılır. Sıralama garantisi verilmez. | URL/metadata/iç-link snapshot ve redirect map; yayınlanan yararlı URL'yi gerekçesiz silme; içerik değişikliği ayrı geri alınabilir. |

## Üç dalganın kalan işleri

| İş / dalga / öncelik | Kapsam, kök neden | Efor; bağımlılık; risk | Kabul ve geri dönüş |
| --- | --- | --- | --- |
| B11 / 1 / P2 | UI-05/06. TR/EN/AR kontrol adları, arama hata/boş metni, RTL; JS yokken randevu/iletişim ve gezinme fallback. `header/basic.html:38–79`, `extend-footer.html:4–21`, `search.js:154–161`, hero:88–100. | 1 gün; B02/B03; locale/fallback kırılması | Üç dilde visible/accessibility metni; JS/CDN kapalı ana içerik ve gerçek link; AR sıra/taşma, touch target/kontrast, anchor örtülmesi ve footer testleri. Eski i18n/template paketiyle geri al. Tam WCAG 2.2 AA iddiası için manuel inceleme ayrıca gerekir. |
| B12 / 2 / P2 | SCH-09/10. Liste/taxonomy/404/contact için Article varsayımı ve boş service ItemList; `schema.html:98–120` ve hizmet listesi dalı. | 0.5–1 gün; B06; entity türlerinin karışması | Her şablona gerçek amaç matrisi; yardımcı sayfa Article değil, boş ItemList yok; gerçek yayına ScholarlyArticle yalnız gerçek veriyle. 652 canonical + 404 taraması; schema paketini geri al. |
| B13 / 1–2 yayın kapısı / P2 | HOST-03/04. `netlify.toml:26–118`, tema sürüm bildirimi, `package.json:7–9`; headers, gzip/Brotli, ETag/Last-Modified, sabit sürüm/tema commit'i, atomik yayın ve geri dönüş. | 1–2 gün; server seçimi ve B01/B05; stale HTML/yanlış MIME/güvensiz release | Hedef HTTP yanıtlarında HTML/JSON/XML revalidation; hashli asset ile değişebilir dosya ayrımı; TLS/protokol/MIME/security; temiz ayrı build ve release manifest; önceki release'e geri dönüş tatbikatı. Üretim dizininde --gc/temizlik denemesi yok. |
| B14 / 3 / P2 aday | CT-09. `content/tr/kvkk/index.md:30–55`, EN/AR privacy ve `extend-head-uncached.html:9–24`; gerçek form/Analytics/üçüncü taraf akışını görünür metinle eşle. | 0.5–1 gün + uzman görüşü; seçilen backend, runtime veri akışı; hassas veri gereksiz toplama | Gerçek istek/çerez ve tercihler kaydı; sağlayıcı/amaç/saklama/veri minimizasyonu için yetkili karar; dil tutarlılığı. Hukuki ihlal hükmü çıkarma. Metin/ayarlar ayrı sürümlenir, yanlış veri açıklamasını geri alma planı. |
| B15 / 3 / P3 | PERF-06. Kullanılmayan `shortcodes/three-heart.html:133–146` syntax borcu; aktif partial ile iki uygulama. | 0.25–0.5 gün; B09 sonrası; yanlış eski yolu etkinleştirme | node --check exit0; konsolidasyon varsa aktif 12 sayfa davranışı/GLB yolu korunur. Önceki dosya geri yüklenebilir; yalnız puan için 3B silinmez. |

## Ölçüm, erişim ve yayın için kapanış kapıları

- **Dalga 1:** B01–B05, B07'nin bilgi tutarlılığı, B11; mevcut gerçek
  işlev/görünüm sorunları ve yayın engeli. DNS düzelmeden bütün kaynak işlerini
  bekletmek gerekmez; yerel teşhis ve UI düzeltmeleri bağımsız ilerleyebilir.
- **Dalga 2:** B06, B08, B09, B12, B13; schema/canonical/sitemap ve ölçümle
  seçilmiş performans düzeltmeleri. Önce baseline, sonra kontrollü karşılaştırma.
- **Dalga 3:** B10, B14, B15; içerik/iç link/yerel görünürlük ve bakım.

GSC erişimi yoksa gerekli tek export paketi: sorgu+sayfa+cihaz+ülke bazlı
performance (tıklama/gösterim/CTR/ortalama konum; karşılaştırılabilir dönemler),
page indexing ve sitemap sonuçları, örnek URL inspection/Google canonical,
manual action/security ve cihaz bazlı CWV. GBP için kategori, website,
adres/telefon/saatler ve doğrulanmış profil görünümü. Bu veriler olmadan
kesinti kaynaklı trafik kaybı, ceza veya cannibalization kesinleştirilemez.
İstanbul konumlu TR/EN mobil/masaüstü SERP örneklemi ayrı tarih/konum/yöntemle
kaydedilmeli; tek ekran hacim veya ulusal sabit sıralama sayılmamalı.

Çalıştırılmayan runtime/performance testlerini tamamlamak için tarayıcı
bağlantısının ve ayrı minify production test sunucusunun erişilebilir olduğu
bir ortam yeterlidir; kullanıcının 1313 süreci durdurulmaz. Form/randevu
gönderimi bu denetimde yapılmadı; ileride kontrollü test de teslim yetkisi
olan staging hedefinde sentetik veriyle sınırlandırılmalıdır.

Her bulgunun gerçek çıktı/kaynak/kabulü [01-findings.md](01-findings.md),
dört schema sonucu [03-schema-audit.md](03-schema-audit.md), kapsam ve
NOT_RUN listesi [08-coverage-and-limitations.md](08-coverage-and-limitations.md) ile birlikte okunur.
