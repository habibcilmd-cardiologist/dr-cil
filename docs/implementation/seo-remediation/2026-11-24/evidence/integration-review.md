# Salt okunur entegrasyon incelemesi

Tarih: 24 Kasım 2026. Kapsam: uygulanmakta olan UI/schema/SEO/3B kaynakları.
Bu incelemede kaynak dosyaları değiştirilmedi; yeni Hugo build'i, sunucu,
tarayıcı veya üretim performans koşusu başlatılmadı. Diğer ajanların
eşzamanlı yazdığı çalışma ağacı incelendi; nihai build kabulü değildir.

## Bulgular ve çözülme durumu

1. **INT-01 — `simple` liste şablonuna istemeden pagination eklenmesi:**
   İlk incelenen `seo/list-paginator.html` section/term türlerinin tamamında
   `.Paginate` başlatıyordu. TR/EN/AR hizmetler `_index.md:5` dosyaları
   `layout: simple` kullanır; tema `layouts/_default/simple.html:1–18`
   `.Paginate` çağırmaz. Head'deki yeni çağrı hayalet hizmet pagination
   çıktıları oluşturabilirdi. SEO ajanına ve root'a bildirildi. Son kaynak
   okumada `layouts/partials/seo/list-paginator.html:5` artık
   `(ne .Layout "simple")` korumasını içeriyor. **Kaynak düzeltmesi görüldü;
   final çıktı tekrar kontrolü bekliyor.**
2. **INT-02 — Çapraz dil paginator başlangıcı riski:** İlk `alternates.html`
   başka çevirilerin `.Paginate` sonucunu aynı render içinden başlatıyordu.
   Bu, tek başına timeout veya deadlock kanıtı değildir. Son kaynak okumada
   `layouts/partials/seo/alternates.html:4–16` yalnız ilk sayfa için gerçek
   çevirileri çıkarıyor; başka dil paginator'ını başlatmıyor. **Kaynakta
   risk azaltıldı; deadlock kök nedeni saptanmış sayılmadı.**
3. **INT-03 — Diff biçim kontrolü:** `git diff --check` inceleme anında
   yalnız `layouts/partials/extend-footer.html:48` trailing whitespace
   bildirdi. UI ajanına iletildi; bu runtime kritik hatası değildir.
   Sonrasında UI ajanı satırı temizlediğini ve kendi dosyaları için
   `git diff --check` çıkışının 0 olduğunu bildirdi.

## Timeout / rekürsiyon ayrımı

- Tema `baseof.html` → yerel `head.html:186` → `schema.html` ve yerel
  `head.html:1` → `seo/current-page-url.html` → `seo/list-paginator.html`
  yolları kaynak üzerinden takip edildi. Bunların içinde tekrar `head`,
  `baseof` veya `schema` render eden doğrudan template döngüsü bulunmadı.
- `schema.html:89` home içeriğini, `schema-faq.html:6` yalnız gerçek FAQ'lı
  sayfalarda içeriği; `schema.html:40,64,91` ve `schema-procedure.html:6`
  word count'u kullanır. Bu çağrıların varlığı deadlock kanıtı değildir.
- `evidence/ui-build.json` 180 saniyelik timeout kaydeder, tamamlanmış
  üretim/HTML kabulü değildir. `evidence/schema-smoke-build.json` başka bir
  ara snapshot için exit 0 kaydeder. Schema ajanı kendi build logundaki Hugo
  toplamını 53.830 ms olarak bildirdi; bu süre tarayıcı performansı değildir.
- Salt-okunur süreç envanteri `ps` ortam tarafından `operation not permitted`
  ile engellendi. Süreç/thread stack'i alınamadı; kısıt aşılmadı.

## Ek kaynak kontrolleri ve kalan kabul

- Ortak dialog JS'sinin `window.drcilDialog` tanımı, arama açıcıları, mobil
  menü ID'leri ve randevu DOMContentLoaded başlangıcı kaynakta eşleşiyor.
  İncelemede somut kritik bağlama hatası bulunmadı; gerçek klavye/focus ve
  computed layout kabulü çalıştırılmadı.
- `three-heart` shortcode'u `.Page` ile ortak partial'a gidiyor; module
  başlangıcı her `[data-heart-model]` kökünde `heartBound` koruması kullanıyor.
  Kaynakta iki ayrı aktif uygulama görülmedi. Gerçek GPU/CPU/ağ sonucu yok.
- Kaynaklar durulduktan sonra root'un tek final izole üretim build'i ve
  tüm HTML sözleşme/schema/link taraması esas alınmalı. Hayalet
  `/hizmetler/page/N/`, `/en/services/page/N/`, `/ar/services/page/N/`
  kopyalarının kalmadığı, normal blog pagination canonical'larının doğru
  olduğu ve duplicate ID/schema üretimi olmadığı nihai çıktıda kontrol
  edilmelidir. Başarılı derleme runtime performans başarısı sayılmamalıdır.
