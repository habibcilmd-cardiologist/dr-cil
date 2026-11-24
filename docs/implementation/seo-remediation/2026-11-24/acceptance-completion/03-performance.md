# Performans kabulü

Bu turda gerçek üretim origin, Netlify CDN cache/header davranışı veya Lighthouse/CrUX verisi kullanılmadı. Yerel Python sunucusunda elde edilecek süreler, canlı performans kabulü olarak anlamlı değildir.

## Çalıştırılmayan testler

- En az üç soğuk ve üç sıcak gerçek origin ölçümü.
- Mobil ve masaüstü Lighthouse / PageSpeed ölçümü.
- Gerçek cache-control, CDN hit/miss, transfer boyutu ve üçüncü taraf etki analizi.
- CrUX, Search Console veya Google Business Profile verisi.

## Yerel gözlem (performans puanı değildir)

3B GLB ilk viewport'ta veya sayfa açılışında istenmedi; yalnız kullanıcı “3B kalp modelini yükle” düğmesine bastıktan sonra `200` ile yüklendi. Bu, istek-zamanlaması davranışının yerel kanıtıdır; LCP/INP/TBT ya da gerçek ağ performansı sonucu değildir.

Canlı origin erişimine izin verildiğinde, aynı release hash'iyle 3+3 soğuk/sıcak ölçüm ve mobil/masaüstü Lighthouse çalıştırılmalıdır.
