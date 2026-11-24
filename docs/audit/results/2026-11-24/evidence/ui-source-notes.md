# UI, erişilebilirlik ve güvenilirlik — kaynak/çıktı incelemesi

İnceleme tarihi: 24 Kasım 2026. Kaynak kodu değiştirilmedi. Bu dosyada
**statik olarak doğrulanan** bilgiler ile **tarayıcıda doğrulanması gereken**
etkiler ayrıdır. Gerçek viewport, computed layout, klavye ve ekran okuyucu
testleri bu alt incelemede çalıştırılmadı; ana denetimin tarayıcı kanıtlarıyla
birlikte okunmalıdır. Üretim örnekleri `/tmp/dr-cil-audit-2026-11-24/public/`
altındaki izole çıktıdır. Kontrol öznitelikleri `ui-static-extract.json` içindedir.

## UI-01 — Masaüstü başlık/menü yerleşimi: P1, güçlü kök neden adayı

**URL:** `/`, `/en/`, `/ar/`; ortak header diğer sayfaları da etkiler.

- `layouts/partials/header/basic.html:25`: masaüstü menüsü `hidden md:flex`,
  `gap-x-5`, `md:ml-12` ile açılıyor. `:212–220` uzun marka başlığını ve bu
  menüyü aynı `flex flex-1 items-center justify-between` satırında topluyor.
  **Gerçek `md` eşiği 853px:** `themes/blowfish/tailwind.config.js:14` ve
  derlenmiş `assets/css/compiled/main.css:2707–2714` bunu doğruluyor; standart
  Tailwind varsayımıyla 768px olarak raporlanmamalı.
- `layouts/partials/header/fixed.html:6`: dış sarmalayıcı `max-w-7xl`,
  `md:px-24 lg:px-32` kullanıyor. Geniş ekranın tamamı menü alanı değildir.
- `assets/css/custom.css:20–23` içindeki `white-space: nowrap !important`
  seçicisi marka başlığı nav'ını hedefliyor; gerçek menü linklerine uygulanmıyor.
  Gerçek etiketler `themes/blowfish/layouts/partials/header/header-option-simple.html:13`
  içindeki `<p class="text-base font-medium">` düğümleridir.
- Tema bütün `<a>` öğelerine `word-break: break-word` ve
  `overflow-wrap: break-word` veriyor (`themes/blowfish/assets/css/main.css:146–150`;
  derlenmiş karşılığı `assets/css/compiled/main.css:3680–3683`). Bu kural,
  daraltılan etiketlerde `white-space: normal` ile birlikte sözcük içi
  bölünmeye izin verir.
- `assets/css/custom.css:55–57` menü etiketlerine 14px ve ek yatay padding
  uyguluyor. `:83–84` gövdenin yatay taşmasını gizliyor; bu gerçek yerleşim
  düzelmesini kanıtlamaz.
- `config/_default/params.toml:70–78` içinde `disableTextInHeader=true`
  **header tablosunun içinde**. Şablon `basic.html:214` bunu kök
  `.Site.Params.disableTextInHeader` üzerinden arıyor. `hugo config --format json`
  çıktısından doğrulanan değerler: kök değer `null`,
  `params.header.disabletextinheader=true`.
- Aynı koşuldaki `not ... | default true` ifadesi, yanlış değer/default
  davranışı açısından ayrıca düzeltilmelidir; yalnız TOML anahtarını taşımak
  yeterli kabul edilmemeli. Başlık çıktıda görünür durumdadır.

**Etki:** Kullanıcının sağladığı ekran görüntüsündeki harf bölünmesiyle uyumlu
yerleşim sorunu. Hangi breakpoint'te hangi label'ın kaç piksele daraldığı ve
kelimeyi bölen son computed özellik ana tarayıcı testinde ölçülmelidir.

**En küçük çözüm yönü:** Marka başlığı için tek doğru parametre/koşul;
gerçek kullanılabilir genişliğe uyan masaüstü breakpoint'i ve küçülme
kuralları; menü etiketlerinde uygun nowrap/min-content davranışı. Başlığı
gizleyerek veya fontu aşırı küçülterek ürün kararını varsayma.

**Kabul:** 320–1920 CSS px test matrisi ve %200 gerçek zoom'da tüm etiketler
okunabilir; sığmadığı yerde erişilebilir mobil menüye geçer; clip/overflow
maskesiyle kaybolan kontrol bulunmaz. Her başarısız genişlik için computed
box/white-space/flex/min-width ve ekran görüntüsü kaydedilir.

## UI-02 — Uzmanlık kartı yanlış metin: P1, statik çıktı doğrulandı

**URL:** `https://docdrhabibcil.com/`.

`i18n/tr.yaml:25–26` doğrudan `Uzmanlık` / `Damar Açma` tanımlıyor.
`layouts/partials/home/hero.html:149–150` bu değerleri gösteriyor; ikinci
değerin fallback'i `hero_expertise_3`, o da `i18n/tr.yaml:12` satırında
`Damar Açma`. İzole üretim çıktısındaki iki kart değeri sırasıyla
`Damar Açma` ve `Akademik Yetkinlik`.

EN ilk kart değeri `Vascular Interventions`; AR ilk kart değeri
`فتح الأوعية الدموية`. Üç dilde de istenen uzmanlık ifadesiyle anlam eşleşmesi
ayrıca ele alınmalı. Bütün sitedeki “damar açma” terimleri silinmemeli.

**En küçük çözüm:** Türkçe kartın doğrudan/fallback metnini “Girişimsel
Kardiyoloji” olarak birleştirmek; EN/AR karşılıklarını doğrulamak.
**Kabul:** Ana sayfalarda istenen anlam görünür, 320/390px'de kart taşmaz;
fallback senaryosu aynı anlamı korur.

## UI-03 — Mobil menü klavye/semantik eksikleri: P1, statik doğrulandı

`header/basic.html:94–107` açıcıyı `div`, kapatıcıyı `li > span` olarak
üretiyor; button rolü, tabindex, erişilebilir ad, aria-expanded ve
aria-controls yok. İzole üretimde `#menu-button` gerçekten `div`,
`#menu-close-button` gerçekten `li`. Tema `assets/js/mobilemenu.js:32–33`
yalnız click dinleyicisi ekliyor; dosyada Enter/Space/Escape veya odak
yönetimi yok. Bu, klavyeyle erişilebilir kontrol uygulamasının eksik
olduğunu doğrudan gösterir; belirli tarayıcıda Tab dizisi henüz ölçülmedi.

**Kabul:** 390px'de klavyeyle açıcıya ulaşılır; Enter/Space açar; Escape
kapatır; açık durum doğru duyurulur; kapanınca odak açıcıya döner. Başka
modal ile odak/scroll çakışması oluşmaz.

## UI-04 — Modal odağı ve arama semantiği: P1/P2, güçlü davranış adayı

Randevu modalinin iyi tarafları: `extend-footer.html:47–52` içinde dialog,
aria-modal ve başlık ilişkisi var. `:568–591` ilk odağı kapatıcıya taşıyor
ve kapanışta önceki odağa dönüyor; `:605–608` Escape'i ele alıyor.

Eksik kalan kaynak davranışı: `:553–632` içinde Tab/Shift+Tab döngüsü veya
arka plan için inert yok. Bu nedenle görsel olarak modal olsa da odağın
arkadaki kontrollere kaçması güçlü adaydır; tarayıcıda doğrulanmalıdır.

Arama: `layouts/partials/search.html:1–23` dialog/aria-modal/başlık ilişkisi
ve input için gerçek label/aria-label sunmuyor; placeholder tek başına
etiket olarak kabul edilmemeli. `assets/js/search.js:94–114` input'a odak
veriyor ancak önceki odağı saklamadan `blur()` ile kapatıyor; Tab trap yok.
`search.js:76–85` yalnız sonuç varsa Enter'ı durduruyor; `search.html:9`
action'sız formunda sonuç yokken Enter'ın gezinme/yenileme davranışı
tarayıcıda ayrıca kontrol edilmelidir.

**Kabul:** Arama/randevuda Tab ve Shift+Tab odağı modal içinde tutar;
Escape kapatır; odak doğru açıcıya döner; ekran okuyucu modal/input adını
duyurur. Arama yükleme/hata/boş sonuç durumlarında Enter beklenmedik
yenileme yapmaz. Bu denetim sırasında randevu sağlayıcısına gerçek işlem
ve iletişim formu gönderimi yapılmamalı.

## UI-05 — Yerelleştirme ve reduced-motion: P2, statik doğrulandı

- `header/basic.html:38,46,71,78` arama/tema kontrollerinin erişilebilir
  adları bütün dillerde İngilizce; `:39,72` i18n anahtarında başlangıç
  boşluğu var (`" search.open_button_title"`), bu nedenle title çevirisi
  kontrol edilmeli.
- `extend-footer.html:4–12` Arapça sayfaya İngilizce medical disclaimer
  veriyor; `:21` Arapça WhatsApp erişilebilir adı da İngilizce fallback.
- `assets/js/search.js:154–161` yükleme/hata metinleri İngilizce.
- RTL kök yönü doğru üretiliyor: AR `html lang=ar dir=rtl`, TR/EN ltr.
  `themes/blowfish/layouts/_default/baseof.html:3–4` kaynağı bunu sağlıyor.
  Ancak header'da `ml-*`, hero/ikonlarda `margin-right` ve modalda fiziksel
  left/right kullanılıyor; görsel aynalama hatası tarayıcıda doğrulanmalı.
- `assets/css/custom.css:1881–1888` ve `:2426` devamındaki hero animasyonları
  sürekli. Bu dosyada `prefers-reduced-motion` bloğu yok. Footer'ın
  `extend-footer.html:533–541` reduced-motion kuralı yalnız randevu
  bileşenlerini kapsıyor; hero hareketini kapsamıyor.

**Kabul:** Kontrol adları/metinleri sayfa diliyle uyumlu; RTL'de okuma sırası
ve kontroller doğru; reduced-motion tercihinde gereksiz hero hareketi durur.
3B modelin ayrı hareket/maliyet incelemesi `04-performance.md` kapsamındadır.

## UI-06 — JS kapalıyken temel eylemler: P2, kaynak adayı

`hero.html:88–100` randevu çağrısı button + inline JS; alternatif href yok.
Mobil menü de JS'ye bağlı. WhatsApp ve hizmet CTA'ları gerçek anchor
oldukları için JS olmadan daha dayanıklı. İletişim ve hizmet içerikleri
statik HTML'de mevcut; JS-off tarayıcı testi bu alt incelemede yapılmadı.

**Kabul:** JS kapalı/CDN başarısızken içerik okunur ve en az bir görünür
randevu/iletişim/hizmet gezinme yolu kullanılabilir. Salt JS kontrolün
işlevsiz görünmesi yerine uygun fallback sağlanır.

## Güvenlik ve olumlu kontroller

- `assets/js/search.js:118–123` mesajları `textContent` ile oluşturuyor;
  kullanıcının boş sonuç sorgusu HTML'e doğrudan eklenmiyor. Önceki
  düzeltmeyi yeni açık gibi raporlamıyoruz. Sonuç verileri yine HTML
  şablonuyla üretiliyor; bu denetimde mevcut editör kontrollü indeks için
  bağımsız bir saldırı yolu gösterilmedi.
- Aynı dosyada HTTP/JSON/network/timeout hata yolları ve 15sn timeout var;
  aramayı kapatıp açarak yeniden deneme uygulanmış. Gerçek ağ hata testi
  henüz yapılmadı.
- Bu alt incelemenin izole üretim ağacında incelenen isim filtrelerinde
  `.bak`, debug veya `.toml` yayın dosyası bulunmadı. Bu, secret scan veya
  tüm güvenlik denetimi geçti iddiası değildir.
- Netlify kaynak ayarında frame denial, nosniff ve Referrer-Policy var;
  yeni sunucunun gerçek yanıtları ayrıca test edilmelidir. Eksik CSP'yi tek
  başına kanıtlanmış açık/SEO sorunu olarak sınıflandırmıyoruz.

## Ana denetim için öncelikli tarayıcı kontrolleri

1. 1280/1440/1920 ve 852/853/854/1023/1024px çevresinde nav box ölçümleri;
   header alanı ile brand/menü toplamının karşılaştırılması.
2. 390px'de Tab ile mobil menüyü aç/kapat; Enter/Space/Escape ve geri odak.
3. Randevu modalinde son linkten Tab, ilk kapatıcıdan Shift+Tab; arkaya
   kaçış var mı? Testte dış sağlayıcıya gitme.
4. Aramada başarısız/boş sorgu + Enter; Escape sonrası odak; modal dışına Tab.
5. AR ana sayfa menü/hero/arama; tema değişimi; 200% zoom ve reduced-motion.

## Birincil kaynaklar

24 Kasım 2026'da erişildi:

- [W3C APG — Button Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/button/)
- [W3C APG — Modal Dialog Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)

APG uygulama örüntüsü ile tam WCAG uygunluk iddiası birbirinden ayrıdır.
