# Performans ve 3B kalp denetimi — 24 Kasım 2026

## Bu turdaki bağımsız tekrar kontrolünün kapsamı

Bu dosyada aşağıda korunan tarayıcı süreleri ve önceki üretim varlık ölçümleri,
denetim klasöründe bu çalışma başlamadan önce bulunan kanıtlara aittir. Bu
turda yeni bir Chrome/Lighthouse koşusu yapılmadı. Aktif ve eski 3B şablon,
çağıran partial'lar ve koşullu yükleme/render davranışı kaynak satırlarından
yeniden okundu; aşağıdaki `PERF-01`–`PERF-06` ayrımı korunmaktadır. Önceki
geliştirme gözlemleri yeni üretim ölçümü olarak sunulmamaktadır.

Yeni kanıt: `evidence/recheck-perf-evidence.json`. Mevcut izole üretim
çıktısındaki TR/EN/AR ana sayfaların SHA-256'ları önceki varlık envanteriyle
birebir eşleşti. 976 HTML yeniden tarandı: etkin partial model yolu 12
dosyada, eski shortcode model yolu 0 dosyada, video etiketi 0 dosyada.
Aktif GLB 1.511.228 bayt, tek mesh/primitive ve tek gömülü görseldir; eski GLB
3.255.284 bayt ve bu çıktıda kullanılmıyor. Primitive sayısı gerçek draw-call
ölçümü olarak sunulmamıştır. Yeni kanıtta Node v26.11.0, macOS 26.6.2 arm64
ve PATH'te Lighthouse bulunmaması da kaydedilmiştir.

24 Kasım 2026 tekrar kontrolünde web.dev'in Web Vitals, optimize-lcp ve
browser-level-image-lazy-loading sayfaları yeniden açıldı. LCP ≤2.5 saniye,
INP ≤200 ms ve CLS ≤0.1 hedeflerinin mobil/masaüstü ayrı p75 kapsamı;
etkileşimsiz Lighthouse'ta TBT ile INP'nin aynı ölçüm olmaması ve
laboratuvarın saha verisinin yerini tutmaması doğrulandı. Hero'ya körlemesine
lazy yükleme önerilmemesinin dayanağı aynı resmî görsel yükleme rehberidir.

Ek sınır: `isInitialized` bayrağı aynı partial örneğinde ikinci başlangıcı
engeller (`three-heart.html:32,38–40`); bu, çalışma anında her sayfada tek
render döngüsü olduğunun sayımla doğrulanması değildir. WebGL/CDN yükleme
hataları için catch/fallback kodu vardır (`:157–163,206–211`), ancak
IntersectionObserver oluşturulması try bloğunun dışındadır (`:36`, `:64`).
Eski tarayıcı/API yokluğu ve hata simülasyonları **Çalıştırılmadı**. GLTF
yükleme hatasında animasyonun sonlandırılması da kaynakta yoktur; bunun
CPU/GPU etkisi **Ölçülmedi**. Hiçbir koşul için “performansa sıfır etki” veya
“CWV geçti” sonucu çıkarılmamıştır.

## Sonuç ve ölçüm sınırı

**Masaüstü/mobil hız puanı veya Core Web Vitals geçiş sonucu bu denetimde
üretilmedi.** Üretim HTML ve varlıkları üzerinde gerçek bayt ölçümleri,
yükleme öznitelikleri ve 3B çağrı zinciri doğrulandı. Ardından mevcut yerel
**geliştirme** sunucusunda üç masaüstü viewport ve üç dar viewport tanılama
koşusu kaydedildi; aşağıdaki ayrı bölümde medyan/aralıkları verildi. Ağ/port
kısıtı ve PATH'te çalıştırılabilir Lighthouse bulunmaması nedeniyle tekrarlı
**üretim Lighthouse** koşuları çalıştırılmadı. Rakip firmanın “masaüstü yavaş” iddiası
bu bulgularla ne doğrulanmış ne de çürütülmüş olur.

| Denetim | Sonuç |
| --- | --- |
| Ayrı üretim derlemesi | Başarılı; `evidence/production-build.log` |
| Üretilmiş üç dil ana sayfa ve varlık ölçümleri | Doğrulandı; çevrimdışı bayt ölçümü |
| Tüm HTML'de gerçek 3B/video yolunun taranması | Doğrulandı; 12 sayfa lazy model, sıfır eski model, sıfır video etiketi |
| ≥3 soğuk-cache masaüstü ve mobil Lighthouse koşusu | Çalıştırılmadı; skor/medyan/aralık yok |
| Üretim LCP/FCP/CLS/TBT/Speed Index/TTFB | Ölçülmedi; ayrı yerel geliştirme tanılama süreleri var |
| Gerçek kullanıcı INP ve diğer saha CWV p75 | Doğrulanamadı; CrUX/GSC/RUM verisi alınmadı |
| HTTP gzip/Brotli, cache ve TLS/HTTP sürümü | Bu raporda doğrulanamadı; dosya sıkıştırma tahmini HTTP yanıtı değildir |
| Geliştirme sunucusunda Resource/Navigation Timing ve ilk viewport tetiklenmesi | CUA tarayıcıda kaydedildi; performans zaman çizelgesi/CPU-GPU izi alınmadı |
| Model açık/engelli A/B, mobil DPR/Save-Data/WebGL hata senaryoları | Çalıştırılmadı |

Kullanıcının çalışan Hugo sunucusu değiştirilmedi. Kod/deploy/DNS değişikliği
yapılmadı. Tarayıcı tanılaması, üretim benchmark veya fiziksel telefon testi
olarak sunulmadı; tek ekran görüntüsü performans zaman çizelgesini kanıtlamaz.

## Ortam ve yeniden üretilebilirlik

- İzole üretim çıktısı: `/tmp/dr-cil-audit-2026-11-24/public`.
- Hugo: `v0.167.0+extended+withdeploy darwin/arm64`.
- Başlangıç commit/çalışma ağacı: `evidence/initial-worktree-state.json`.
- Node: `v26.11.0`; kurulu yerel Chrome uygulama sürümü: `157.0.8103.80`.
  Tanılama yapılan CUA in-app tarayıcının UA'sı ise **Chrome/158.0.0.0**;
  bunlar aynı çalıştırılabilir dosya/profil olarak değerlendirilmedi.
- `command -v lighthouse`, `google-chrome`, `chromium`, `chromium-browser`
  sonuçları boş. Chrome.app'in varlığı, Lighthouse koşusu yapıldığı anlamına gelmez.
- Başka bir kurulu uygulamanın içinde bir Lighthouse bundle'ı bulundu;
  bu bundle CLI olarak çalıştırılmadı ve kısıtı aşmak için kullanılmadı.
- Çevrimdışı çıktı ölçümü tarayıcı profili kullanmaz. Ayrı tanılama serisi:
  24 Kasım 2026, mevcut `http://localhost:1313/` Hugo **development** sunucusu,
  1280×900 ve 390×844 CSS piksel, DPR override 1, CPU/ağ throttling yok,
  `Network.setCacheDisabled(true)` ile reload. Tam soğuk işletim sistemi/DNS/
  TLS/CDN cache'i garanti edilmedi; koşuların gözlem pencereleri farklı.

## Ayrı yerel geliştirme tanılaması — üretim benchmark değildir

Kanıtlar: `evidence/browser-dev-diagnostics.json`,
`browser-model-observations.json`; ham koşulardan hesaplanan istatistikler
`performance-dev-summary.json`. Navigation/Resource Timing ve buffered
PerformanceObserver kullanıldı. Aşağıdaki değerler **yerel geliştirme
sunucusundaki tanılama** değerleridir; Lighthouse puanı, mobil cihaz hızı,
üretim/saha CWV geçişi veya kontrollü önce/sonra testi değildir.

| Tanılama metriği | Masaüstü viewport 1280×900; n=3 medyan [min–max] | Dar viewport 390×844; n=3 medyan [min–max] |
| --- | ---: | ---: |
| TTFB (ms) | 20.6 [6.6–35.1] | 1.4 [1.0–5.8] |
| DOMContentLoaded (ms) | 374.3 [201.0–677.5] | 161.3 [65.7–214.3] |
| load olayı (ms) | 382.7 [205.6–689.8] | 164.2 [69.1–218.9] |
| FCP (ms) | 312 [184–536] | 148 [100–164] |
| Gözlem penceresindeki LCP (ms) | 312 [268–536] | 180 [100–232] |
| Gözlenen kayma toplamı; resmî CLS sertifikası değil | 0.0000116 [0–0.0001266] | 0.0000622 [0–0.0000622] |
| Gözlenen long-task süre toplamı (ms); TBT/INP değil | 95 [74–189] | 0 [0–0] |

Masaüstü gözlem pencereleri 7.05–14.16 saniye, dar viewport pencereleri
2.22–2.61 saniyedir. Pencerelerin ve cache geçmişinin farklılığı cihazlar
arasında hız üstünlüğü çıkarımını engeller. İlk profilin LCP öğesi `IMG`,
dar viewport'unki `P` idi. Gözlenen kayma toplamları, `hadRecentInput`
olmayan gözlem kayıtlarının toplamıdır; resmi CLS session-window hesabı
veya p75 saha sınıflaması olarak kullanılmadı. Long-task toplamından TBT
veya INP hesaplanmadı; kullanıcı etkileşimi/saha INP verisi yok.

**3B tetiklenme gözlemi:** Masaüstü 1280×900'de üç reload'un **üçünde de
scroll olmadan GLB istendi** ve canvas oluştu. Model isteği başlangıç medyanı
1355.5 ms [894.8–1589.3], istek süresi medyanı 229.6 ms [112.8–566.6];
Resource Timing `transferSize` her koşuda 1511528 bayttı. Dosyanın
1511228 baytlık boyutuyla 300 bayt fark, bu tarayıcı kaydındaki transfer
muhasebesidir; farklı sunuculara aynen genellenmez. Skypack ilk istekleri
286.3–785.5 ms arasında başladı. Bu kanıt, “masaüstünde kullanıcı model
bölümüne scroll etmeden hiç yüklenmez” iddiasını bu viewport için çürütür.

390×844'te üç ilk gözlem penceresinin **üçünde de Skypack/GLB isteği ve
canvas yoktu**. Sonraki scroll testinde scrollY=1702, model rect'i
top=-159.5/bottom=180.5 iken Skypack isteği yaklaşık 19.703 s, GLB isteği
20.155 s navigasyon zamanında başladı; GLB süresi 30.4 ms ve canvas oluşumu
kaydedildi. Bunlar scroll'a kadar geçen süreyi içerir; “20 saniyede yükleniyor”
gibi bir performans sonucu değildir. Scroll sonrası tek gözlem, genişlik,
yükseklik ve zaman penceresi dışındaki bütün mobil senaryoları kanıtlamaz.

Bu koşularda masaüstü model başlangıcı, gözlenen ilk LCP zamanından sonraydı.
Bu, modelin ilk LCP'yi kesin kötüleştirdiği iddiasını desteklemez; modelin
hiç maliyeti olmadığı veya sonrasındaki long task'ların kesin modelden
kaynaklandığı sonucu da çıkarılamaz. Kontrollü model-açık/engelli A/B,
offscreen frame sayımı ve CPU/GPU atfı yapılmadı. Canlı üretim Analytics'i
geliştirme sunucusunda yoktur; gerçek sunucu/ağ ve fiziksel telefon koşulları
bu sonuçlarla temsil edilmez.

Çevrimdışı envanteri yeniden üretmek için depo kökünde:

```sh
python3 docs/audit/results/2026-11-24/evidence/performance-collect.py
```

Bu yardımcı yalnız dosya okur ve denetim kanıtlarını günceller; HTTP isteği,
sunucu veya tarayıcı açmaz. `gzip9_estimate_bytes`, aynı dosyanın Python
gzip seviye 9 ile hesaplanan tahmini boyutudur. Sunucunun gerçekten gzip
uyguladığı, aynı oranı sağlayacağı veya istemcinin bu kadar veri aldığı
sonucu çıkarılamaz. SHA-256 değerleri JSON/CSV kanıtında bulunur.

## Gerçek varlık boyutları

| Kaynak | Ham bayt | Çevrimdışı gzip9 tahmini | Not |
| --- | ---: | ---: | --- |
| `/` HTML | 101605 | 23366 | TR üretim |
| `/en/` HTML | 99224 | 22872 | EN üretim |
| `/ar/` HTML | 124161 | 27405 | AR üretim |
| `/hizmetler/dizalti-damar-tikanikligi/` HTML | 96528 | 24216 | Gerçek hizmet URL'si |
| `/hizmetler/periferik-damar/` HTML | 79026 | 20089 | Gerçek hizmet URL'si |
| `/blog/diyabetik-ayak/` HTML | 128137 | 32684 | Gerçek blog URL'si |
| Ortak CSS bundle | 160183 | 26388 | Tek render engelleyici stylesheet |
| Hero WebP | 35410 | — | Üç ana sayfada aynı işlenmiş görsel |
| jQuery slim | 70264 | Kanıt CSV'sinde | Head'de `defer/async` yok |
| Appearance JS | 3615 | Kanıt CSV'sinde | Head'de senkron; tema flash önleme amacı olabilir |
| Zoom JS | 8828 | Kanıt CSV'sinde | Head'de senkron |
| Main JS bundle | 34017 | Kanıt CSV'sinde | `defer` var; Fuse dahil |
| Background blur JS | 826 | Kanıt CSV'sinde | Gövdede senkron |
| Process JS | 1003 | Kanıt CSV'sinde | Footer'da senkron |
| Yerel dış JS toplamı | 118553 | — | CDN'den Three.js/gtag buna dahil değil |
| TR arama JSON | 1067469 | 253535 | Arama açılınca alınır; ilk yükleme bütçesi değil |
| EN arama JSON | 1043274 | 246296 | Aynı ayrım |
| AR arama JSON | 1444730 | 270939 | Aynı ayrım |
| Aktif kalp GLB | 1511228 | 1252362 | Koşullu yüklenen model |
| Kullanılmayan alternatif GLB | 3255284 | 2945110 | Üretilen HTML'de referansı bulunmadı |

Her ana sayfanın içinde ayrıca 9093 bayt çalıştırılabilir inline JS ve 5713
bayt inline CSS vardır; bunlar HTML boyutunun zaten içindedir, toplama tekrar
eklenmemelidir. GTM/gtag scriptinin haricî dosya ve ikincil istek boyutları
ölçülmedi. Ana sayfada kullanılan statik dosyaların hepsini tarayıcının aynı
anda indirdiği varsayılmadı; özellikle model ve arama indeksi koşulludur.

Üretilmiş HTML'de video etiketi bulunmadı. `assets/videos/` içindeki 155341
bayt MP4'nin varlığı onun ana sayfada indirildiğini göstermez. Aynı şekilde
statik model klasöründeki OBJ/JPG/MTL ve kullanılmayan GLB, dağıtım boyutunu
etkileyebilir ama referans/istek olmadan ilk yükleme maliyeti sayılmaz.

## PERF-01 — Görünüm dışına çıkan 3B kalbin render'ı durdurulmuyor

**P2; kaynak ve üretilmiş JS ile doğrulandı; sayısal kullanıcı etkisi ölçülmedi.**

Gerçek çağrı zinciri:

`config/_default/params.toml` profile yerleşimi →
`layouts/partials/home/profile.html:3,6` →
`interventional-cardiology-diagram.html:16` → `three-heart.html` partial'ı.

Üretim HTML'de aktif model referansı `/`, `/en/`, `/ar/` ve bunların
`page/2/`, `page/3/`, `page/4/` sürümlerinde bulunur: toplam **12 sayfa**.
`layouts/shortcodes/three-heart.html` eager yolu hiçbir üretilmiş HTML'de
bulunmadı; dolayısıyla o eski yolu mevcut ana sayfanın yükleme nedeni
olarak göstermek yanlış olur.

Aktif partial `three-heart.html:35–55` bir IntersectionObserver kurar,
`rootMargin:100px`, `threshold:0.1` ile ilk kesişmede observer'ı kapatır ve
`requestIdleCallback(...,{timeout:2000})`, destek yoksa 100 ms timeout kullanır.
67–69'da Three.js, GLTFLoader ve OrbitControls CDN'den dinamik import edilir;
127'de 1.51 MB GLB istenir. Bu kod başlangıç isteğini koşula bağlar. Yukarıdaki
tarayıcı tanılamasında masaüstü 1280×900'de scroll olmadan tetiklenme,
390×844'te ise ilk pencerede erteleme ve sonraki scroll'da başlama gözlendi.
Idle timeout, ağır işi sıfırlamaz. Başka viewport ve üretim koşulları ayrıca
ölçülmelidir.

`three-heart.html:164–183` requestAnimationFrame döngüsünü yalnız sekme
gizlendiğinde durdurur. Canvas viewport'tan çıkınca durduran ikinci bir
observer yoktur; ilk observer zaten disconnect edilmiştir. Görünür sekmede
`controls.update()` ve `renderer.render()` çağrıları devam eder. Bu bir kod
davranışıdır; kaç ms CPU/GPU, kaç FPS veya kaç puan kaybı yarattığı ölçülmedi.

Öneri: modelin viewport görünürlüğünü yüklemeden sonra da izle; görünüm
dışında render'ı durdur; yeniden girişte tek döngü başlat. Kullanıcı isteğiyle
yüklenen poster seçeneğini ancak ölçümlü karşılaştırmadan sonra seç.

Kabul: ilk viewport'ta istenen stratejiye göre GLB/Three.js isteği yok;
scroll sonrasında yalnız bir init; viewport dışında frame/render çağrısı
duruyor; tekrar girişte tek döngü; masaüstü/mobil etkileşim izi ve uzun görev
karşılaştırması saklanmış. Sayısal bütçe baseline ölçümünden sonra belirlenmeli.

## PERF-02 — 3B ve hero hareketi kullanıcı tercihlerine bütünüyle uymuyor

**P2; kaynakta doğrulandı; OS/tarayıcı davranış testi yapılmadı.**

Partial 26'da reduced-motion hakkında yorum var, fakat 27'de yalnız
`typeof window` kontrol ediliyor. `prefers-reduced-motion`, Save-Data ve WebGL
yetenek kontrolü model başlatılmadan önce yok. `three-heart.html:91–117`
DPR'yi 2 ile sınırlar, yüksek DPR'de antialias'ı kapatır; bu iyi bir önlemdir.
Yine de `powerPreference:high-performance`, gölgeler ve autoRotate açıktır.
Genel catch/fallback kalp simgesi gösterir; boyut/başlatma maliyetini önlemez.

`assets/css/custom.css:1877–1888` hero float/drift/ECG animasyonlarını sonsuz
çalıştırır. Dosyada reduced-motion media kuralı bulunmadı; footer'daki
`extend-footer.html:533–541` kuralı yalnız randevu bileşenlerini kapsar.

Öneri: reduced-motion'da otomatik dönüş/hero dekorasyon hareketini durdur;
Save-Data veya desteklenmeyen WebGL için hafif ve anlamlı poster/fallback
sun. Tüm cihazlarda modeli kaldırma gerekliliği henüz kanıtlanmadı.

Kabul: gerçek reduced-motion ve Save-Data testleri; gereksiz model isteklerinin
yokluğu; WebGL/CDN hatasında içerik/bağlantılar kullanılabilir; konsolda
yakalanmamış hata yok. Pil/ısı ve FPS değerlendirmesi ölçüm gerektirir.

## PERF-03 — Head'de senkron vendor zinciri var

**P2; yükleme öznitelikleri doğrulandı; darboğaz büyüklüğü güçlü aday.**

`themes/blowfish/layouts/partials/head.html:118–140` appearance/zoom scriptlerini,
`vendor.html:1–3` jQuery'yi senkron üretir. Render edilmiş HTML de bunu doğrular.
Appearance küçük ve görünüm flash'ını önleme amacı taşıyabilir; bütün scriptleri
körlemesine defer yapmak önerilmez. `layouts/partials/header/basic.html:251–254`
jQuery kullanır; bağımlılığı kaldırmak bu kodu da ele almayı gerektirir.

İyileştirme adayı: menüdeki küçük jQuery kullanımını ölçerek sadeleştirmek,
zoom'u gerekli sayfaya ayırmak ve dependency sırasını koruyarak ertelemek.
Mevcut JS maliyetinin LCP veya TBT'nin asıl nedeni olduğu kanıtlanmadı.

Kabul: aynı üretim koşullarında tekrarlı önce/sonra Lighthouse ve ana iş
parçacığı izi; tema flash'ı, menü aktifliği, arama, zoom, mobil menü regresyonu yok.

## PERF-04 — Hero görselinin kaynak seçim/öncelik seçenekleri eksik

**P2; üretilmiş öznitelikler doğrulandı; CLS/LCP sorunu olarak doğrulanmadı.**

`home/hero.html:131–138` görseli 700×900 sınırında varsayılan q96 ile işler;
çıktı 35410 bayttır. Orijinal WebP 11186 bayt; daha büyük işlenmiş çıktı tek
başına kullanıcı etkisi kanıtı değildir. `img` eager'dır; width/height,
srcset/sizes ve fetchpriority yoktur. Eager kullanımını kaldırmak önerilmez:
bu görsel LCP adayı olabilir. `custom.css:2349–2367` media alanına sabit
yükseklik ayırır; bu, eksik img boyutlarından çıkarılabilecek CLS riskini
azaltır. Dolayısıyla “width/height yok, CLS kesin kötü” sonucu çıkarılmadı.

Öneri: önce gerçek LCP öğesini belirle, uygun intrinsic boyut/oran ve mobil
responsive kaynağı tanımla; high priority yalnız ölçümle gerekçelendirilirse.
CSS'teki blur/drop-shadow/backdrop-filter maliyeti GPU izinde araştırılmalı;
CSS kuralının varlığı tek başına yavaşlık bulgusu değildir.

Kabul: gerçek LCP öğesi/alt süreleri belgeli; uygun kaynak seçiliyor; görsel
yüklenirken layout shift yok; mobil ve masaüstünde görüntü kalitesi korunuyor.

## PERF-05 — İlk arama 1–1.44 MB JSON ve eşzamanlı Fuse kurulumu getiriyor

**P2; payload/kod doğrulandı; etkileşim süresi ölçülmedi.**

Arama ilk açıldığında `assets/js/search.js:148–180` dilin `index.json`
dosyasını indirip Fuse nesnesini kurar. Veri ilk sayfa yüklemesinin doğrudan
yükü değildir; arama etkileşimine aittir. Büyük indeksin parse/kurulum ve
query maliyetini mobil CPU'da ölçmeden INP bozuk denemez. Dil içeriği ve
indeks şişmesi teknik SEO envanteriyle birlikte değerlendirilmelidir.

Kabul: yavaş mobil profilinde ilk arama/açılış/ilk sonuç süreleri ve uzun
görevler belgeli; yükleme/başarısızlık/tekrar deneme anlaşılır; yanlış dil
sonucu yok. İndeks alan azaltımı veya worker ancak ölçüme göre seçilmeli.

## PERF-06 — Kullanılmayan eski shortcode'da JavaScript sözdizimi hatası

**P3; Node sözdizimi kontrolüyle doğrulandı; mevcut HTML'de etkisi yok.**

`layouts/shortcodes/three-heart.html:133–146` çevresindeki kapanış/callback
yapısı ayrıştırılamıyor. Script çıkarılıp `node --check` ile kontrol edildi;
çıkış kodu 1. Kanıt: `evidence/performance-unused-shortcode-syntax.mjs` ve
`.log`. Bu dosya halen kullanılmadığı için mevcut ana sayfanın bozuk
olduğuna veya eager modeli yüklediğine kanıt değildir. İleride yeniden
kullanılacaksa önce tek aktif uygulamaya konsolide edilmeli veya onarılmalı.

## Tamamlanacak ölçüm paketi

Yetkili ağ/port ve Lighthouse erişimi olan ortamda minify üretim çıktısını
ayrı yerel sunucuda sun; kullanıcının geliştirme sunucusunu değiştirme.
Üç ana sayfa + kritik hizmet/blog örneklerini kapsa. En az üç aynı koşullu
soğuk cache masaüstü/mobil koşusu, tercihen beş; medyan/aralık ve ham JSON/HTML
sakla. Aynı profilde sıcak tekrar ziyareti ayrı ölç.

Önce LCP öğesini, long task kaynağını ve CLS olaylarını bul. Ardından model
açık/istekleri engelli koşullarını, ilk viewport/scroll/ilk etkileşim/viewport
dışı/sekme gizli senaryolarını karşılaştır. Lighthouse TBT'yi INP olarak
etiketleme. Gerçek kullanıcı verisi edinilirse URL/origin ve cihaz kapsamını,
veri dönemini kaydet.

Güncel saha hedefleri: cihaz grubu başına p75 LCP ≤2.5 saniye, INP ≤200 ms,
CLS ≤0.1. Lighthouse tek koşu puanı saha CWV geçişi veya sıralama garantisi
değildir. Bu sitede saha verisinin bulunmadığı değil, **alınmadığı** söylendi.

## Birincil kaynaklar

24 Kasım 2026'da açılarak incelendi:

- https://web.dev/articles/vitals — mevcut CWV metrikleri/eşikleri, p75 ve
  cihaz grupları; etkileşimsiz Lighthouse'ta INP ölçülememesi.
- https://web.dev/articles/optimize-lcp — saha/lab ayrımı ve ölçümden önce
  LCP nedenini belirleme yaklaşımı.
- https://web.dev/articles/browser-level-image-lazy-loading — ilk görünüm
  görselini lazy yapmama, eager/fetchpriority ayrımı, boyut ayırma.

Ana kanıt: `evidence/performance-asset-inventory.json`, `.csv`,
`performance-glb-*.json`, `performance-tooling.json`,
`performance-rendered-inline-syntax.json`, `browser-dev-diagnostics.json`,
`browser-model-observations.json`, `performance-dev-summary.json`, üretim build log'u ve
başlangıç çalışma ağacı manifesti. Kaynak satırları mevcut denetim snapshot'ına
aittir; gelecekte değişirse yeniden doğrulanmalıdır.
