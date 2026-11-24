# Tarayıcı, responsive ve erişilebilirlik kabulü

Tarayıcı: Playwright ile gerçek Chromium. Test hedefi yalnız `http://127.0.0.1:1314` taze output'uydu. Yerel sayfa konsolu, kontrollü çevrimdışı 3B senaryosu dışında `0` hata verdi.

## Responsive ölçümü

Her değer için `document.documentElement.scrollWidth` gerçek viewport genişliğinden küçüktü; dolayısıyla yatay sayfa taşması gözlenmedi. `clientWidth` dikey scrollbar nedeniyle daha küçüktür.

| Viewport | clientWidth | scrollWidth |
| ---: | ---: | ---: |
| 320 | 312 | 316 |
| 360 | 352 | 356 |
| 390 | 382 | 386 |
| 430 | 422 | 426 |
| 768 | 760 | 764 |
| 852 | 844 | 848 |
| 853 | 845 | 849 |
| 854 | 846 | 850 |
| 1023 | 1015 | 1019 |
| 1024 | 1016 | 1020 |
| 1025 | 1017 | 1021 |
| 1280 | 1272 | 1276 |
| 1440 | 1432 | 1436 |
| 1920 | 1912 | 1916 |

Gözle incelenen örnekler: [320 px mobil](../../../../../output/playwright/home-tr-320.png) ve [1280 px masaüstü](../../../../../output/playwright/home-tr-1280.png).

## Etkileşim sonuçları

| Senaryo | Sonuç |
| --- | --- |
| TR mobil menü | Açıldı; `Esc` ile kapandı ve odak “Menüyü aç” düğmesine döndü. |
| Klavye | İlk `Tab` “Ana içeriğe geç” bağlantısına gitti. Menü içinde `Tab` sonraki bağlantıya, `Shift+Tab` kapat düğmesine döndü. |
| EN arama | `diabetic foot` sorgusu doğru blog sonucunu verdi. |
| AR arama | `القدم السكرية` sorgusu doğru blog sonucunu verdi. |
| TR sonuç-yok | `qxzvnomatch` için erişilebilir durum mesajı “sonuç bulunamadı” verdi. |
| AR statik 404 şablonu | Arapça metin, ana sayfa ve iletişim bağlantıları doğru çıktı. Python sunucusu bunu HTTP 200 ile verir; gerçek 404 statüsü test edilmedi. |
| Reduced motion | `prefers-reduced-motion: reduce` altında 3B model otomatik yüklenmedi; isteğe bağlı yükleme kontrolü kaldı. |
| Tüm Hizmetler | İlk ekranda lazy-load bekleme metni, bölüm viewport'a getirildiğinde hizmet listesiyle değişti. |
| 3B başarı | Düğmeye basılana kadar model isteği yoktu. Basınca `/models/3d-kalp-modeli-doc-dr-habib-cil-istanbul-kardiyoloji-uzmani.glb` `200` yüklendi; görsel ve döndürmeyi durdur kontrolü oluştu. |
| 3B hata geri kazanımı | Kontrollü çevrimdışı durumda anlaşılır hata ve “Tekrar dene” düğmesi çıktı. Sonrasında ağ yeniden çevrimiçi yapıldı. |

## Çalıştırılmayan erişilebilirlik kontrolleri

- Gerçek tarayıcıdaki native `%200` zoom (viewport emülasyonu bunun yerine geçmez).
- JavaScript kapalı tam akış.
- Gerçek ekran okuyucu ile sesli/semantik denetim.
- Tüm odak sırası için uçtan uca manuel klavye turu ve yüksek-kontrast işletim sistemi kombinasyonları.

Bu maddeler “geçti” sayılmamıştır; sadece yukarıdaki gerçek etkileşimler kanıtlanmıştır.
