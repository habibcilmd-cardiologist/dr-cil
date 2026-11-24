# Statik çıktı ve teknik SEO alt denetimi — 24 Kasım 2026

Bu alt denetim `/tmp/dr-cil-audit-2026-11-24/public` üretim çıktısını okur.
HTTP durumları, Google indeks durumu veya canlı DNS hakkında sonuç üretmez.
Kaynak kodunda değişiklik yapılmadı. Yardımcı kod yalnız bu evidence klasöründe.

## Tekrar üretim

```sh
cd /Users/yavuz/prg/dr-cil
hugo list all --noBuildLock > docs/audit/results/2026-11-24/evidence/static-source-content.csv
python3 docs/audit/results/2026-11-24/evidence/static-audit.py /tmp/dr-cil-audit-2026-11-24/public docs/audit/results/2026-11-24/evidence
```

Üretim çıktısını ana denetçi izole kaynak/cache ve ayrı hedefle oluşturdu;
bu komutlar mevcut kullanıcı sunucusunu yeniden başlatmaz. Dış URL'ler yalnız
`docdrhabibcil.com`/`www.docdrhabibcil.com` için yerel dosya haritasına alınır.
Sorgu ve fragment dosya varlığından ayrılır; percent-encoding bir kez çözülür;
dosya yolu büyük/küçük harf duyarlılığı korunur. `/tr/*` yönlendirmesi yalnız
ilan edilmiş Netlify kuralı olarak modellenir, gerçek HTTP sonucu sayılmaz.

## Kapsam ve sayılar

| Ölçüm | Sonuç |
| --- | ---: |
| Kaynak Markdown | 364: TR 160, EN 102, AR 102 |
| `hugo list all` satırı | 361: TR 159, EN 101, AR 101 |
| Kaynak liste kind | 346 page, 12 section, 3 home |
| Üretilmiş HTML | 976 |
| Meta-refresh alias HTML | 297 |
| Dil bazlı özel 404 HTML | 3 |
| Pagination HTML | 24 |
| Alias/404 hariç çıktı | 676: TR 266, EN 204, AR 206 |
| Ayrı canonical | 652: TR 258, EN 196, AR 198 |
| Taxonomy URL ailesi (pagination hariç) | 346 |
| Eksik title/description/tek-H1 kontrolü | 0 / 0 / 0 sorun |
| HTML'de referans verilen eksik yerel asset | 0 |
| İlan edilmiş yönlendirmeyi uygulamadan eksik iç link | 98 kullanım, 65 hedef, 45 kaynak sayfa |
| `/tr/*` kuralıyla hedefi mevcut olan eski link | 32 kullanım, 23 eski hedef |
| İlan edilmiş `/tr/*` kuralından sonra da çözülemeyen | 66 kullanım, 42 hedef, 40 kaynak sayfa |
| Eksik statik fragment | 4 kullanım, tek yanlış anchor |
| Başka sayfadan HTML a bağlantısı bulunmayan aday | 62: 53 taxonomy URL'si, 9 ana sayfa pagination |

Kaynak sayısı farkındaki üç dosya `content/{en,ar}/contact/{thank-you,shukran}.md`
ve `content/tr/iletisim/tesekkurler.md` dosyalarıdır. Parent `index.md` nedeniyle
leaf bundle kaynaklarıdır; bağımsız sayfa olarak listelenmez. Dosyalarda
`_build render: never` bulunduğu iddia edilmez. Bu yardımcı dosyaların bir
form sonrası sayfa olarak kullanılabilirliği ayrıca işlev denetimi gerektirir.

Envanter: `../02-url-and-template-inventory.csv`. CSV'deki HTTP sütunu bilinçli
olarak `not_measured`; statik indexability sütunu Google indeks sonucu değildir.
Kaynak içeriği exact Hugo permalink eşlemesiyle eklenir. Otomatik oluşturulan
archive/pagination template ailesi adları bir lookup trace değil sınıflamadır.

## STATIC-01 — Bozuk/yanlış iç bağlantılar

- **Öncelik:** P1. **Durum:** Statik çıktı ve kaynakta doğrulandı; canlı HTTP
  404 testi çalıştırılmadı.
- **Ölçüm:** 66 çözülemeyen kullanım, 42 hedef, 40 kaynak sayfa. Alt gruplar:
  11 literal `false/`, 16 yanlış kök `/contact/`, 15 dil prefixesiz
  `/services/`, 10 Arapça eksik hizmet, 7 `/tr/` kaldırıldıktan sonra da
  eksik, 7 diğer bağlantı.
- **Somut URL/çıktı:** `/en/services/myocardial-infarction/` çıktısında
  `<a href=false/>Coronary Artery Disease</a>`. Göreli hedef
  `/en/services/myocardial-infarction/false/`; dosya ve özel yönlendirme yok.
- **Kaynak:** `content/en/services/myocardial-infarction/index.md:191`;
  diğer 10 dosya `static-broken-links.json` içinde. `/en/blog/aortic-aneurysm-symptoms-diagnosis-and-modern-treatment-methods/`
  randevu CTA'sı için `content/en/blog/aortic-aneurysm/index.md:505`:
  `{{< button href="/contact/" target="_self" >}}`; gerçek iletişim hedefi
  `/en/contact/` iken `/contact/` dosyası yok.
- **Etki/kök neden:** Bağlam içi okuma ve randevu yolculuğu kesilir. Yanlış
  literal yol ve dil prefixesiz eski yollar içerikte kalmış. Netlify'daki
  genel 404 kuralı bu adresleri hizmet sayfasına dönüştürmez.
- **En küçük öneri:** Linkleri mevcut canonical sayfalarla eşleştir; uygun
  mevcut hedef yoksa uydurma hizmet sayfası açmak yerine ilgili gerçek blog
  veya hizmete bağla. Eski `/tr/` linklerini de doğrudan yeni canonical'a taşı.
- **Kabul:** Tam çıktı taramasında çözülemeyen link sıfır; randevu CTA'ları
  doğru dilde iletişime gider; gerçek HTTP kontrolü ayrı kaydedilir.
- **Kanıt:** `static-link-triage.json`, `static-broken-links.json`.

## STATIC-02 — Pagination canonical ve hreflang hedefleri ilk sayfada kalıyor

- **Öncelik:** P2 (teknik SEO; indeks kaybı veya ceza kanıtı yok).
- **Durum:** 24 pagination çıktısında doğrulandı: 15 liste/arşiv pagination,
  9 başka sayfadan linklenmeyen ana sayfa pagination kopyası. Bunlara bağlı 72 hreflang
  self/return işareti; bağımsız 72 farklı kök neden değildir.
- **Örnek:** `/blog/page/2/` canonical `/blog/`; `/en/blog/page/2/` canonical
  `/en/blog/`. Alternate adresleri de listelerin ilk sayfalarına gidiyor.
- **Kaynak:** `themes/blowfish/layouts/partials/head.html:32` `.Permalink`;
  `themes/blowfish/layouts/_default/list.html:70` ve diğer `.Paginate`
  çağrıları; `layouts/partials/extend-head-uncached.html:26-33` alternate
  üretimini `.AllTranslations`/ilk sayfa `.Permalink` üzerinden yapıyor.
- **Etki:** Dizinin farklı sayfaları birinci sayfayı canonical öneriyor;
  pagination diller arası eşleme de gerçek sayfa konumunu temsil etmiyor.
  Google'ın neyi indekslediği bu statik kontrolden bilinemez.
- **Öneri/kabul:** Liste politikası açıkça belirlenip gerçek liste pagination'ının kendi
  canonical'ı üretilecek; gereksiz 9 ana sayfa kopyası için üretimin kaldırılması
  da değerlendirilecek (her kopyayı indekslenebilir yapmak zorunlu değildir).
  Eşdeğer pagination alternatifi varsa doğru sayfaya
  bağlanacak. Değişiklikten sonra 24 canonical ve 72 hreflang kontrolü yeniden
  çalışacak. Normal, pagination dışı sayfalarda self/return/target hatası
  saptanmadı; bunları topluca yeniden kurmak gerekmez.
- **Resmî kural:** https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading
  — Google her pagination sayfasına kendi canonical adresini önerir.
- **Kanıt:** `static-canonical-issues.json`, `static-hreflang-issues.json`.

## STATIC-03 — Sitemap sahipliği ve dil keşfi parçalı

- **Öncelik:** P2. **Durum:** Üretilmiş XML ve kaynakta doğrulandı.
- **Gerçek çıktı:** Kök `sitemap.xml` bir sitemap index değil 258 TR URL'li
  `urlset`. `en/sitemap.xml` 196, `ar/sitemap.xml` 198 URL içeriyor.
  `tr/sitemap.xml` ve `hizmetler/sitemap.xml`, kök XML ile byte-eş.
- **Kaynak:** `static/robots.txt:10` yalnız kökü bildiriyor;
  `static/sitemap.xml:2-10` kaynakta dil index'i tarif ediyor ancak nihai
  kök dosya bunu taşımıyor. `layouts/_default/sitemap.xml:4-10` bütün sayfaları
  dil filtresiyle üretiyor. `hugo.toml:81-84`, diğer dillerin benzer outputs
  tabloları; `layouts/_default/home.globalindex.xml:5` ise farklı bir
  `tr_sitemap.xml` tasarımı içeriyor (bu dosya çıktıda yok).
- **Sınır:** Mevcut üretim kök dosyası sitemap index olmadığı için
  “kök → /tr/sitemap.xml → kök” canlı sitemap döngüsü doğrulanmış değildir.
  Böyle bir döngüyü olmuş gibi raporlama. Dil sayfaları hreflang ve bağlantılarla
  keşfedilebilir; sadece kök sitemap'te olmamak indekslenemezlik demek değildir.
- **Olumlu:** Beş XML geçerli biçimde ayrıştırıldı; tüm loc hedef dosyaları
  mevcut. Toplam 652 unique canonical, dillerin sitemap birleşiminde yer alıyor.
  Pagination dışı canonical için hiçbir sitemap'te bulunmama saptanmadı.
- **Öneri/kabul:** Tek sahipli kök dil index'i veya açıkça bildirilen üç
  sitemap politikası; 652 canonical için doğru dilde kapsama, geçerli XML,
  nihai 200 ve yönlendirme döngüsü olmaması gerçek HTTP ile doğrulanmalı.
- **Kanıt:** `static-sitemaps.json`, `static-not-in-any-sitemap.json`.

## STATIC-04 — İngilizce ana sayfadaki hizmet kartı yanlış anchor kullanıyor

- **Öncelik:** P2. **Durum:** Kaynak ve emitted ID farkıyla doğrulandı;
  scroll davranışını tarayıcıda ayrıca kontrol etmek gerekir.
- **URL:** `/en/` kartı `/en/services/#pacemaker-and-electrophysiology`
  hedefine bağlanıyor. Gerçek bölüm ID'si `pacemaker-electrophysiology`.
- **Kaynak:** `content/en/_index.md:39` ile
  `content/en/services/_index.md:67` çelişiyor. Ana sayfa ve üç ana sayfa
  pagination çıktısında aynı yanlış link var (4 kullanım).
- **Öneri/kabul:** Kart hedefi gerçek sabit bölüm ID'siyle aynı olacak;
  tıklama ilgili bölüme götürecek, sabit header başlığı örtmeyecek.
- **Kanıt:** `static-broken-fragments.json`.

## STATIC-05 — Front matter'dan ibaret 55 ayrı taxonomy benzeri sayfa

- **Öncelik:** P2. **Durum:** Kaynak/body ve üretilmiş URL varlığı doğrulandı;
  organik sıralama etkisi veya Google cezası doğrulanmadı.
- **Ölçüm:** `hugo list all` içinde tags altında 49, categories altında 6
  `kind=page` var. Hepsinin front matter sonrası içerik gövdesi boş.
  Bunların 53'üne başka bir sayfadan HTML `<a>` bağlantısı bulunmuyor;
  sitemap veya search JSON üzerinden keşif yine mümkün olabilir.
  Tüm sitede taxonomy URL ailesi 346/652 canonical; bu oran tek başına hata
  veya noindex kararı değildir.
- **Örnek:** `content/tr/tags/girisimsel-kardiyoloji.md:2-3`,
  `/tags/girisimsel-kardiyoloji/` başlığı “Girişimsel-Kardiyoloji”. Aynı
  konu için `/tags/girişimsel-kardiyoloji/` gerçek terim arşivi de var.
- **Öneri/kabul:** Gerçek ihtiyaç ve içeriğe göre normal sayfa/gerçek term
  arşivi ayrımını netleştir; boş paralel sayfaları körlemesine indexable
  tutma. Birleştirme gerekiyorsa URL ve 301 haritası hazırlanacak; yararlı
  arşivler korunacak. Toplu noindex/URL silme bu denetimde uygulanmadı.
- **Kanıt:** `static-empty-manual-taxonomy-pages.json`,
  `static-duplicate-titles.json`, URL envanteri.

## STATIC-06 — Arama indeksleri dil fallback'lerini açık etiket olmadan içeriyor

- **Öncelik:** P2 / ürün kararı. **Durum:** Veri ve kaynakta doğrulandı;
  arayüzde gerçekten gösterilen örnekler ayrıca doğrulanmalı.
- **Ölçüm:** Her indeks 423 kayıt. TR indeks: TR258+EN81+AR84; EN:
  TR143+EN196+AR84; AR: TR145+EN80+AR198. Üç JSON dosyasının hash'i farklıdır;
  “hepsi aynı indeks” demek yanlıştır.
- **Kaynak:** `themes/blowfish/layouts/_default/index.json:2-5` bilinçli
  `lang.Merge` fallback uyguluyor. Bu yüzden başka dilde sonuç bulunması
  tek başına beklenmeyen yazılım hatası sayılmaz.
- **Etki/öneri:** Kullanıcı sadece seçili dilde arama bekliyorsa yabancı
  terim arşivleri sonuçları kalabalıklaştırabilir. Politika seçili dil veya
  görünür dil etiketi/filtresi olarak açıkça belirlenmeli; eksik çeviriye
  erişim yararı da korunmalı.
- **Kabul:** Seçili dildeki mevcut eşdeğer varken başka dil hedefi tercih
  edilmez; fallback varsa dili açık; dil değiştirme ve sonuç linki test edilir.
- **Kanıt:** `static-search-indexes.json`.

## Ek gözlemler ve sınırlar

- 16 duplicate-title grubu 48 URL'yi; 9 duplicate-description grubu 379
  URL'yi içeriyor. Önemli bölümü pagination/taxonomy veya aynı site
  description fallback'i. Bunları 379 bağımsız kritik hata ya da sıralama
  kaybı kanıtı olarak sunma. Kaynak head metadata fallback'i
  `themes/blowfish/layouts/partials/head.html:20-21`.
- `x-default` tüm çevrili detaylarda kök anasayfaya ayarlanıyor
  (`extend-head-uncached.html:29-33`). Google x-default için fallback sayfa
  seçimine izin verir; bu statik olgu tek başına kesin invalidity değildir.
  Kullanıcının hangi fallback'e gitmesini istediğiyle tutarlılığı değerlendir.
- HTML `<a>` ve asset taraması, CSS içindeki url() veya schema image
  alanlarının eksiksiz denetimi değildir. Bunları schema/performance alt
  denetimleri ayrıca ele alır.
- Robots meta `index, follow` olması Google'da indekslendiğini göstermez.
  404 HTTP başlıkları görülmediği için 404 şablonunun robots etiketinden
  indeksleme sorunu çıkarılmadı.
- İç linkten yoksun aday sayımı aynı sayfanın kendisine/başlığına bağlantılarını
  inbound saymaz. 62 adayın 53'ü taxonomy URL ailesi, 9'u ana sayfa pagination'dır.
  Sitemap, JSON indeks veya dış bağlantılar bu HTML navigasyon grafiğine dahil
  değildir; “Google keşfedemez” sonucu çıkarılamaz.
- Resmî hreflang kuralları:
  https://developers.google.com/search/docs/specialty/international/localized-versions
  (denetim tarihinde kontrol edildi).
