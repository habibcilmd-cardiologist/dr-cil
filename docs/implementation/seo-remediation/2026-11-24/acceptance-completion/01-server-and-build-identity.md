# Sunucu ve build kimliği

## Taze üretim çıktısı

Komut: `npm run build`

- Sonuç: başarılı (`exit 0`)
- Hugo: `v0.167.0+extended+withdeploy`
- Çıktı: `/var/folders/t5/l46_wxcd1sjfl_jrlc8lqhj00000gq/T/dr-cil-production-9uvcvyei/public`
- Manifest commit'i: `0721bf293e6842d065965c0c8a146954559b4540`
- Manifest zamanı: `2026-11-24T03:56:00.711183+00:00`
- Üretilen HTML: `967`; toplam dosya: `1436`

Build, tema sürümü ile ilgili Hugo uyumluluk uyarısı verdi; derleme başarısız olmadı. Ayrıntılı uyarı ve komut kanıtı [evidence/build-and-server.md](evidence/build-and-server.md) içindedir.

## 1314 doğrulaması

Python önizlemesi yalnız bu taze dizini sunacak şekilde `127.0.0.1:1314` üzerinde çalıştırıldı. Doğrulama ham HTTP gövdesi ile yapıldı; DOM'dan yeniden üretilmiş bir hash kullanılmadı.

| Kontrol | Sonuç |
| --- | --- |
| `GET /` | `200 OK`, `110410` bayt |
| Ana sayfa SHA-256 | `4a79c1dad0267299b166a0e932005d98a10aff97f393529267a2dcdc3d9ba4ef` |
| Taze output ile karşılaştırma | Birebir eşleşti |
| CSS asset | Sunulan bayt hash'i: `d1632653c72e31aec843d68181753251c7bea19cacfc4fff982f764c7848c2ae` |
| 3B JS asset | Sunulan bayt hash'i: `fa0263c732554a8fc0a39cbb8084e110f59f1dc62384b2382771375c1d9873c4` |
| Dinleyici | Python PID `76204`, `127.0.0.1:1314` |
| 1313 / 1315 | Dinleyen işlem yok |

Bu nedenle denetimde kullanılan port **1314** ve taze üretim derlemesi budur.

## Bu sunucunun yapmadıkları

`python -m http.server` Netlify değildir: `_redirects`, `netlify.toml` header/cache kuralları, gerçek 301/404 statüleri, TLS ve CDN davranışı burada kanıtlanamaz. Bunlar canlı origin doğrulamasına bırakılmıştır.
