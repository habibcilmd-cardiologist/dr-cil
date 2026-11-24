# Breadcrumb düzeltmesi ve sekiz sorgunun SEO durumu

Tarih: 24 Kasım 2026. Önceki kabul kayıtları değiştirilmedi.

## Doğrulanmış hata ve düzeltme

Kullanıcının bildirdiği gezinme hatası üretim çıktısında doğrulandı.
`layouts/partials/breadcrumbs.html:11–13`, görünür link için ortak schema
öğesindeki mutlak URL'yi kullanıyordu. Dizaltı hizmet sayfasındaki Hizmetler
linki `https://docdrhabibcil.com/hizmetler/` idi.

Görünür link artık `urls.Parse` ve `RequestURI` ile `/hizmetler/` üretiyor.
Tarayıcı açık olduğu protokol/alan adı/port üzerinde kalır. Dil, kodlanmış yol
ve varsa base path korunur. Canonical ve JSON-LD mutlak üretim adreslerini korur.

| Açık sayfanın sunucusu | Hizmetler bağlantısının çözüldüğü adres |
| --- | --- |
| `http://localhost:1314` | `http://localhost:1314/hizmetler/` |
| `http://127.0.0.1:1314` | `http://127.0.0.1:1314/hizmetler/` |
| `https://docdrhabibcil.com` | `https://docdrhabibcil.com/hizmetler/` |

`scripts/validate_schema_output.py:42` ve `:162` artık görünür breadcrumb
linklerinin aynı sunucuda kalmasını ve schema öğeleriyle aynı sıradaki yolları
göstermesini denetler. Eski çıktı yeni regresyon kontrolünde beklenen şekilde
başarısız oldu: 704 mutlak link ve bunların bulunduğu 367 yol listesi.
1071 tanı kaydı bu iki kontrolün toplamıdır; 1071 ayrı bozuk link değildir.

## Çalıştırılan kontroller

| Kontrol | Sonuç | Kanıt |
| --- | --- | --- |
| İzole minify production build | Exit 0; 967 HTML | `evidence/build.log`, `build-manifest.json` |
| Yeni kontrol, eski çıktı | Beklenen başarısızlık; 704 origin + 367 eşleşme tanısı | `evidence/schema-before.json` |
| Yeni çıktı / hedefli schema ve breadcrumb regresyonu | 967 HTML, 673 JSON-LD, 367 görünür breadcrumb; 0 hata | `evidence/schema-after.json` |
| Statik release kabulü | 32/32; sekiz sorgu hedefi ve eski canonical'lar korundu | `evidence/release-check.json` |
| URL çözümleme | 704 link × 3 sunucu = 2112 çözümleme; 0 sunucu kaçışı | `evidence/origin-check.json` |
| Eski/yeni JSON-LD ve canonical karşılaştırması | Tüm HTML dosyalarında birebir aynı | `evidence/origin-check.json` |
| Çıktı farkı | Yalnız 367 HTML değişti; asset değişmedi | `evidence/origin-check.json` |
| Kaynak whitespace kontrolü | `git diff --check` geçti | `evidence/source-changes.patch` |

Bağımsız incelemede 967 HTML içinde canlı domaine giden görünür `<a href>`
bulunmadı. Menü, kart, dil geçişi, önceki/sonraki ve arama zaten göreli yollar
kullanıyor. Tema/Hugo uyumluluk ve eski ayar uyarıları devam ediyor.

Tekrar komutları:

```sh
python3 scripts/build-production.py --output /tmp/dr-cil-breadcrumb-fix-20261124-01
python3 scripts/validate_schema_output.py /tmp/dr-cil-breadcrumb-fix-20261124-01/public --json /tmp/dr-cil-breadcrumb-after-schema-20261124.json
python3 scripts/validate_seo_release.py --before /var/folders/t5/l46_wxcd1sjfl_jrlc8lqhj00000gq/T/dr-cil-production-9uvcvyei/public --after /tmp/dr-cil-breadcrumb-fix-20261124-01/public --output /tmp/dr-cil-breadcrumb-release-20261124.json
```

Builder tekrarında hedefin yeni/boş olması gerekir; mevcut hedefi temizleme.

## Çalışan sunucu ve yeni çıktı

1314'teki kullanıcı Python süreci (PID 76204) durdurulmadı, yeniden başlatılmadı
ve belge kökü değiştirilmedi. Önceki kabulde kaydedilen sunucu çıktısı:

`/var/folders/t5/l46_wxcd1sjfl_jrlc8lqhj00000gq/T/dr-cil-production-9uvcvyei/public`

Bu düzeltmenin yeni çıktısı:

`/tmp/dr-cil-breadcrumb-fix-20261124-01/public`

Ana sayfa değişmediği için SHA-256 hâlâ
`4a79c1dad0267299b166a0e932005d98a10aff97f393529267a2dcdc3d9ba4ef`.
Bu hash tek başına breadcrumb düzeltmesinin sunulduğunu kanıtlamaz.
`/hizmetler/dizalti-damar-tikanikligi/` ham çıktı SHA-256 değerleri:

- Önce: `c6240ad75cc9feb64d5f0e12529ee83ce59eecded6aa58e2681c4bb80a55c8fe`
- Sonra: `08bcaf233e93e7719cbc96dd774af0f2903594f907b1d36b9ea77c5ecb21e54d`

Yeni çıktıyı mevcut 1314 sürecini koruyarak kendi terminalinizde sunma örneği:

```sh
python3 -m http.server 1315 --bind 127.0.0.1 --directory /tmp/dr-cil-breadcrumb-fix-20261124-01/public
```

Bu sunucu komutu bu turda çalıştırılmadı; 1315 çalışıyor iddiası yok.
Python önizlemesi hosting/TLS/Netlify header ve yönlendirme kabulü değildir.

## Bu değişiklik için çalıştırılmayanlar

- Gerçek HTTP gövdesi: `curl` localhost 1314'e bağlanamadı (exit 7);
  sunulan yeni çıktı kimliği doğrulanamadı.
- Gerçek tarayıcı tıklaması: Chrome test sekmesi açma girişimi zaman aşımına
  uğradı; yeniden bağlantı kontrolü kullanılabilir tarayıcı döndürmedi.
  Statik URL çözümlemesi gerçek tarayıcı kabulü olarak sayılmadı.
- Resmî Schema.org/RRT tekrarları: JSON-LD birebir değişmedi; yeniden
  çalıştırılmadı. Önceki iki örnek tüm şablonların resmî kabulü değildir.
- Üretim performansı, Lighthouse/CrUX, TLS/cache/header/gerçek 301–404,
  GSC/GBP ve canlı sıralama testleri çalıştırılmadı.
- DNS/hesap değişikliği, gerçek form/mesaj/randevu, commit/push/deploy yapılmadı.

## Sekiz hedef sorgu için yapılan çalışma

Önceki uygulamada ana sayfa ve hizmet hub'ının başlık/açıklama/içerik girişleri
değiştirildi; rehber–hizmet–hekim bağlantıları kuruldu. Somut kaynaklar:
`content/tr/_index.md:3–4,25–30`, `content/tr/hizmetler/_index.md:3–24`,
`../02-keyword-content-map.csv`.

| Sorgu | Birincil mevcut hedef |
| --- | --- |
| istanbul kardiyolog | `/` |
| Kardiyoloji Uzmanı | `/` |
| Diyabetik Ayak | `/blog/diyabetik-ayak/` |
| Girişimsel Tedaviler | `/hizmetler/` |
| Girişimsel Kardiyoloji | `/hizmetler/` ve ilgili bölüm |
| Diz altı damar açma | `/hizmetler/dizalti-damar-tikanikligi/` |
| Girişimsel damar açma | `/hizmetler/`; koroner/periferik alt hizmetler |
| Diyabetik ayak tedavisi | `/blog/diyabetik-ayak/`; uygun vasküler hizmet desteği |

Benzer yeni anahtar kelime sayfaları üretilmedi. Önceki statik ölçümde ham eksik
link 98→0, eksik fragment 4→0, canonical sorunu 24→0, hreflang sorunu 72→0 oldu.
Bu sayılar Google sıralaması veya indeks sayısı değildir. Bu düzeltmenin
32/32 release kabulü mevcut sekiz hedefi tekrar doğruladı.

## Zirve hedefi için açık kalan işler

1. Canlı erişim ve yayın sonrası gerçek HTTP/TLS/301/404/cache kabulü.
2. Hekim onaylı kimlik/klinik bilgisi ve kaynaklandırma: `../medical-review/`
   kayıtlarındaki 8 kimlik kararı, 12 iddia taslağı ve 47 yüzde satırı.
3. Gerçek üretim mobil/masaüstü performans ölçümleri ve saha CWV verisi.
4. Yetkili GSC/GBP verileri; sekiz küme için sorgu/sayfa/cihaz/ülke ve dönem
   bazında gösterim/tıklama/CTR/konum; Google canonical/indeks durumu.
5. İki belirsiz taxonomy, kalan genel metadata ve 53 statik orphan adayının
   veriye dayalı değerlendirilmesi. Bu aday sayısı 53 indeks hatası değildir.

Teknik hazırlık yapıldı; canlı ilk sıra veya sıra artışı kanıtı yoktur.
Sağlık içeriğinin güvenilirliği ve özgün uzmanlık dayanağı ayrıca tamamlanmalı.
Sıralama garantisi verilmez.

Birincil kaynaklar (24 Kasım 2026'da açıldı):

- https://gohugo.io/functions/urls/parse/
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
