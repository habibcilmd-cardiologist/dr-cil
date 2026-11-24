# Dr. Habib Çil web sitesi

Hugo ve Blowfish ile oluşturulan, Türkçe, İngilizce ve Arapça statik site.
Çalışma anında veritabanı veya Node.js uygulama sunucusu gerektirmez.

## Yerelde çalıştırma

Gereksinim: **Hugo Extended**. Node.js/npm yalnızca aşağıdaki kısayol
komutları için kullanılır; `npm install` gerekli değildir.

```sh
cd /Users/yavuz/prg/dr-cil
npm run dev
```

Adresler:

| Dil | Adres |
| --- | --- |
| Türkçe | http://localhost:1313/ |
| İngilizce | http://localhost:1313/en/ |
| Arapça | http://localhost:1313/ar/ |

Sunucuyu durdurmak için `Ctrl+C`. `npm start` aynı sunucuyu açar.
Başka port gerekirse `npm run dev -- --port 1314 --baseURL http://localhost:1314/`.
Geliştirme sunucusu bellekte çalışır; üretim için oluşturulan `public/`
klasörünü yerel adreslerle değiştirmez. Yerel önizlemede Analytics yüklenmez.

npm kullanmadan aynı komut:

```sh
hugo server --environment development --bind 127.0.0.1 --port 1313 --baseURL http://localhost:1313/ --disableFastRender --renderToMemory
```

Yeni bir klonda tema eksikse önce:

```sh
git submodule update --init --recursive
```

`hugo: command not found` hatasında Hugo Extended kurun; macOS/Homebrew için
`brew install hugo` kullanılabilir. `bind: operation not permitted` hatası
çalıştırma ortamının port açmayı kısıtladığını gösterir; komutu kendi macOS
Terminal uygulamanızda çalıştırın. `address already in use` ise port kullanımda
demektir; farklı bir port seçin veya önceki sunucuyu durdurun.

## Üretim çıktısı

```sh
npm run build
```

Her çağrı yeni bir geçici release klasörü üretir. Komutun son JSON satırındaki
`public` alanı gerçek çıktı yoludur; `build.log` ve SHA-256 içeren
`build-manifest.json` aynı release klasöründedir. Mevcut `public/` ve izlenen
görsel önbelleği değiştirilmez; `--gc` veya kaynak klasöründe temizlik yapılmaz.

Belirli bir **yeni veya boş** release klasörüne üretmek için:

```sh
npm run build -- --output /tmp/dr-cil-release-review
```

Önceden dosya bulunan bir hedef reddedilir. Manifestteki Hugo sürümü ve tema
commit'iyle kabul kontrollerini tamamladıktan sonra yalnız üretilen `public`
içeriği yayın paketidir. Geçici klasörler kalıcı arşiv değildir; yayın öncesi
onaylı release ve manifest ayrıca korunmalıdır.

Üretim alan adı `hugo.toml` içindeki `baseURL` değeridir. Aynı alan adıyla
sunucu değiştirilirken bu değeri değiştirmeniz gerekmez. Farklı alan adına
çıktı üretmek için:

```sh
npm run build -- --baseURL https://yeni-alan-adi.example/
```

## Netlify'dan kendi sunucusuna taşıma

`public/` içeriği Nginx, Caddy veya Apache ile sunulabilir. Üretim sunucusunda
Hugo veya npm çalıştırmak zorunlu değildir. Hugo geliştirme sunucusunu canlı
yayın sunucusu olarak kullanmayın.

Taşırken sunucuya ayrıca aktarılması gereken davranışlar:

- Eski `/tr/` ve `/tr/*` adreslerini sırasıyla `/` ve `/*` adreslerine 301 ile
  yönlendirin. Bu kurallar `static/_redirects` içindedir; Netlify dışındaki
  sunucular bu dosyayı kendiliğinden uygulamaz.
- `/en/` için `/en/404.html`, `/ar/` için `/ar/404.html`, diğer adresler için
  `/404.html` gösterin; HTTP durumu **404** olmalıdır.
- Klasör adreslerini ilgili `index.html` dosyasıyla sunun. Bulunamayan her
  adresi ana sayfaya döndüren SPA ayarı kullanmayın.
- HTML, XML ve arama indeksi JSON yanıtlarında yeniden doğrulama kullanın.
  `netlify.toml` güvenlik/önbellek başlıklarını yeni sunucuya ayrıca aktarın.
- HTTPS sertifikası ve DNS kayıtları sunucuda ayrıca yapılandırılmalıdır.
  Sunucuyu taşımak alan adının DNS sorununu tek başına çözmez.

## 24 Kasım 2026 incelemesi

Yerel derleme ve yeni release aracı Hugo Extended **0.167.0** ile doğrulandı.
`hugo-version.txt` ile yerel Netlify build tanımı **0.167.0** sürümüne
eşitlendi; canlı Netlify ayarı veya yayın değiştirilmedi. Blowfish v2.93.0'ın bildirdiği destek aralığı ise
**0.141.0–0.152.2**. Yeni sürümde derleme geçse de tema ve eski dil/görsel
ayarları için uyumluluk ve kullanım dışı bırakma uyarıları vardır. Tema
güncellemesini ayrı bir değişiklik olarak, üç dilin görünümünü kontrol ederek
yapmak gerekir.

Giderilen başlangıç sorunları:

- Arapça çevirilerde altı yinelenen anahtar ve yeni Hugo'nun ayırdığı
  `description` anahtarıyla çakışan çeviri yapısı.
- Eksik `dev`, `start`, `build` komutları.
- Arama sorgusunun HTML olarak eklenmesi ve indeks yükleme hatalarında sonsuz
  yüklenme durumu; aramayı kapatıp açarak yeniden denenebilir.
- Yerel önizlemede Analytics yüklenmesi.
- Netlify'da klasör adresli HTML sayfalarının bir yıl değişmez olarak
  önbelleğe alınması.

Sonraki iyileştirmeler:

- Sitemap sahipliği üç açık dil XML'i ve robots bildirimiyle düzenlendi.
  Canonical/hreflang/URL kabulünün gerçek sunucu HTTP testleri yayın öncesi tamamlanmalı.
- 3B kalp görünümü Three.js dosyalarını Skypack CDN'den alıyor. Tamamen
  bağımsız barındırma için bu dosyalar da yerelleştirilmeli.
- Yeni sunucunun türü netleşince yönlendirmeler, yerelleştirilmiş 404'ler,
  güvenlik başlıkları ve HTTPS yapılandırması gerçek HTTP yanıtlarıyla
  doğrulanmalı.

Bu incelemede DNS, Netlify yayını ve canlı sunucu değiştirilmedi.

## İletişim formu sağlayıcısı

Kendi sunucusuna geçiş için doğrulanmış bir form hizmeti henüz seçilmedi.
Varsayılan `params.contactForm.provider="disabled"` durumunda üç dilde
telefon/WhatsApp seçenekleri gösterilir; işlevsiz form veya sahte teslim
bildirimi üretilmez. Netlify veya başka bir serviste gerçek teslim kabulü
tamamlanmadan formu etkinleştirmeyin.

- Netlify Forms kullanılacaksa `[contactForm] provider="netlify"` seçilir;
  formun adı, honeypot ve aynı dilde gerçek teşekkür route'u üretilir.
- Başka bir doğrulanmış backend için `provider="endpoint"` ve HTTPS veya
  aynı origin altındaki gerçek `endpoint` adresi verilir. Endpoint, POST'u
  işlemeden bir 301 teşekkür yoluna yönlendirmemelidir. Teslim sonrası GET
  yönlendirmesi backend'in sorumluluğundadır.
- Teşekkür route'ları `/iletisim/tesekkurler/`, `/en/contact/thank-you/` ve
  `/ar/contact/shukran/` olarak korunur; bağımsız sayfalardır, noindex'tir,
  sitemap'e girmez ve yalnız açılmaları teslim kanıtı sayılmaz.

Hedef sunucuda lokalize gerçek 404, eski URL 301'leri, başlıklar ve HTTPS
ayrıca uygulanır. Kaynak kurallarının bulunması gerçek HTTP kabulü değildir.
