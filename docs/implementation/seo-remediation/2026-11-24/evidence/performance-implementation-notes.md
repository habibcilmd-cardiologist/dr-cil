# Performans uygulaması — 24 Kasım 2026

Kaynak değişiklikleri yalnız `layouts/partials/three-heart.html`,
`layouts/shortcodes/three-heart.html`, `layouts/partials/home/hero.html`,
`assets/js/heart-viewer.js` ve anlamlı regresyon testi
`scripts/tests/heart-viewer.test.mjs` kapsamındadır. i18n/hero animasyon CSS'i
UI ajanıyla koordine edildi. DNS/hesap/mesaj/commit/deploy yapılmadı.

## Başlangıç ve karar

Root'un değişiklik öncesi minify production snapshot'ı
`baseline-build.json` içinde. `index.html` 101605 bayt,
SHA-256 `5443e2b1e1d457569a8dac8ab4b21df104705dbd1bfe8f3484aee8387539b5a8`.
Root'un 1314 üzerinden aldığı HTTP200 gövdesiyle aynı kimlik doğrulandı.
Bu, o andaki 1314 sayfasının baseline olduğunu gösterir; herhangi bir
performans koşusunun çalıştırıldığı anlamına gelmez.

Denetimde masaüstü3/3 ilk viewport model isteği ve1.511.228 bayt GLB
saptanmıştı. Yeni strateji kalp resmini koruyup aynı 3B modeli gerçek bir
Load düğmesiyle isteğe bağlı açar. Model silinmedi/sıkıştırılmadı, gölge ve
DPR kalite ayarları topluca düşürülmedi. Başlangıçta isteğe bağlı ağ/iş
oluşturulmaması amaçlandı; sayısal LCP/TBT/GPU kazancı henüz ölçülmedi.

## Yapılanlar ve kapsam

| Bulgu | Gerçek yerel değişiklik / durum |
| --- | --- |
| PERF-01 | İlk otomatik observer/idle import yerine poster+Load. Import/GLB ancak kullanıcı eyleminde. Tek cancellable RAF, viewport ve document.hidden kapısı; re-entry aynı chain'i kullanır. Kaynak+Node lifecycle doğrulandı; tarayıcı GPU/iz kabulü bekler. |
| PERF-02 | Reduced-motion'da initial autoRotate ve damping kapalı, tek kare/etkileşim çizimi. Kullanıcı Pause/Start düğmesi; veri bağlantısından bağımsız isteğe bağlı yükleme Save-Data'da da istemsiz model indirmez. API/WebGL/CDN/model hatası poster+Retry; asenkron generation guard ve kaynak temizliği. Gerçek OS/CDN/WebGL hata senaryoları browserda henüz doğrulanmadı. |
| PERF-03 | Vendor zincirinin performans darboğazı olduğu ölçülmedi. Tema head/vendor'a körlemesine defer eklenmedi. UI header jQuery ihtiyacını ve SEO head yüklemesini kendi kapsamlarında ele alır; bu kaydı sırf build geçiyor diye kapanmış sayma. |
| PERF-04 | Hero eager kalır, intrinsic width/height; kaynak genişlikleri320/480/700 ve CSS yüksekliklerinden türeyen sizes; ilk hero için fetchpriority high. Source/image boyut alanı gerçek resource Width/Height ile üretilir. Production LCP/CLS etkisi ölçülmeden iyileşme oranı ilan edilmez. |
| PERF-05 | İlk arama parse/Fuse maliyeti ölçülmedi. Veri daraltma/dil fallback'i SEO ajanında; worker/algoritma dönüşümü yapılmadı. Açılış ve ilk sonuç timing'i ayrıca bekler. |
| PERF-06 | Ayrı bozuk shortcode scripti kaldırılarak `.Page` ile aynı partial'a yönlendirildi. Model/observer/lifecycle tek uygulamada. Tekrarlı partial için instance ID ayrımı ve module bootstrap guard var; gerçek iki-instance render kabulü root build/browser testine bağlı. |

Hero'da ayrıca mevcut appointment linkine `data-appointment-trigger` ile
progressive enhancement, native contact href; RTL logical margin; uzmanlık
fallback'i `hero_expertise_1` yapıldı. Yeni klinik iddia veya sayı eklenmedi.

## Gerçek çalıştırılan kontroller

- `node --check assets/js/heart-viewer.js`: exit0.
- `node scripts/tests/heart-viewer.test.mjs`: **9 PASS**, çıktı
  `heart-viewer-node-tests.json`. Bunlar scheduler/DOM-stub testidir;
  gerçek Three.js/WebGL/browser veya performans benchmark değildir.
- Testler: başlangıç offscreen0RAF, repeated-sync tek chain, offscreen/hidden
  kapısı, re-entry, reduced-motion/pause tek kare, dispose sonrası restart
  yok, duplicate bootstrap ve istemsiz başlatma yok, WebGL yokken CDN'den
  önce fallback, retry recoverable.
- Kaynak kod incelemesi: yükleme bitişinde odak yalnız hâlâ Load üzerindeyse
  taşınır; native disabled yerine aria-disabled+state guard. Eski renderer'dan
  gecikmiş contextlost yeni retry'ı bozamaz (attempt/generation guard).
- `performance-implementation-collect.py` baseline dosya envanteri çalıştı;
  `performance-before-after-assets.json` içinde. After henüz verilmemişse
  null olması bilinçlidir; gerçek final build ile root yeniden çalıştırır.
- Root için hazırlanan observer init/read yardımcılarının Node syntaxcheck'i
  geçti. Dosyanın hazırlanması browser ölçümünün çalıştırılması değildir.

Lighthouse PATH'te bulunmadı; Chrome.app varlığı Lighthouse koşusu değildir.
Alt ajan araç kataloğunda CUA/Browser js expose edilmediği için browsera
alternatif shell/Playwright yoluyla erişim denenmedi. Root'ta çalışan CUA
üzerinden koşulmuş gerçek veriler varsa05 raporuna ayrıca bağlanmalıdır.

## Resmî kaynaklar

2026-11-24 tarihinde yeniden açıldı:

- https://web.dev/articles/vitals — lab/saha ve p75 ayrımı.
- https://web.dev/articles/browser-level-image-lazy-loading — ilk görünüm
  hero'sunu lazy yapmama, gerçek görüntü boyutu/öncelik kararı.
- https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
- https://threejs.org/docs/ — renderer ve controls API belgeleri; kullanılan
  proje sürümü sabit0.132.2, güncelAPI ile kör uyumsuz dönüşüm yapılmadı.

## Kalan doğrulamalar

Production final build/template rendering, gerçek model yüklenmesi,
keyboard/drag/zoom/Pause, offscreen/hidden frame sayımı, iki viewer örneği,
Save-Data/OS tercihi, gerçek CDN/WebGL hata/retry, CLS ekranı ve aynıkoşullu
cold/warm ölçümleri. Kaynak state machine veya Node testi bu browser
kontrollerinin başarı kanıtı sayılmaz.
