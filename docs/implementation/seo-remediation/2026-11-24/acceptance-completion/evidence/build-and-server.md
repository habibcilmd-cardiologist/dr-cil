# Build ve sunucu komut kanıtı

## Derleme

```text
$ npm run build
exit: 0
release: /var/folders/t5/l46_wxcd1sjfl_jrlc8lqhj00000gq/T/dr-cil-production-9uvcvyei
public:  /var/folders/t5/l46_wxcd1sjfl_jrlc8lqhj00000gq/T/dr-cil-production-9uvcvyei/public
```

Hugo, tema modülü sürümü için uyumluluk uyarısı verdi; sonuç üretildi ve hash doğrulaması başarılıydı.

## Çıktı kimliği

```text
HTML dosyası sayısı: 967
Toplam dosya sayısı: 1436
GET http://127.0.0.1:1314/: 200 OK
Ana sayfa SHA-256: 4a79c1dad0267299b166a0e932005d98a10aff97f393529267a2dcdc3d9ba4ef
1314 dinleyicisi: Python 76204 127.0.0.1:1314
1313 ve 1315 dinleyicisi: yok
```

## Tarayıcı artefaktları

- `output/playwright/home-tr-320.png`: mobil ana sayfa
- `output/playwright/home-tr-1280.png`: masaüstü ana sayfa
- `output/playwright/home-tr-heart-offline.png`: kontrollü çevrimdışı 3B hata geri kazanımı

Bu görseller denetim sırasında oluşturulmuştur; uygulama kaynağı değildir.
