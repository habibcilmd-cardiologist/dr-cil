# Hosting ve dış bağımlılıklar

## Çalıştırılmayan canlı kontroller

Kullanıcı kısıtı gereği aşağıdakiler yapılmadı:

- DNS, domain, Netlify hesap veya deploy ayarı değiştirme.
- Canlı origin üzerinden HTTPS/TLS, canonical, redirect, 404 HTTP statüsü, `_redirects`, `netlify.toml` headers/cache kontrolü.
- Search Console, Google Business Profile veya Analytics hesabı değişikliği.
- Gerçek form, randevu ya da mesaj gönderimi.

## Önizleme sınırı

1314'teki `python -m http.server`, yalnız taze output'un sayfa/asset davranışını sunar. Netlify fonksiyonlarını ve host seviyesindeki yönlendirme/cache kurallarını taklit etmez. Bu nedenle yerel sonuçlardan canlı hosting için yeşil kabul sonucu çıkarılmamıştır.

## Dış istek notu

İlk üretim önizleme sayfası açılışında Google Analytics uç noktasına otomatik bir `page_view` POST'u görüldü. Bu telemetri olayından sonra tarayıcı denemelerinde Google Tag Manager ve Analytics istekleri mocklandı. Hiçbir kullanıcı mesajı, randevu talebi veya iletişim formu gönderilmedi.

## Sonraki güvenli adım

Deploy yetkisi verildiğinde, aynı commit ve release hash'i ile ayrı bir canlı-origin kontrolü yapılmalı; sonuçta gerçek 301/404/header/cache/TLS kanıtları ve performans tekrarları bu klasöre eklenmelidir.
