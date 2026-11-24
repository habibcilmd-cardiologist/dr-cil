# URL, şablon ve test kapsamı — 24 Kasım 2026

Bu dosya mevcut turu ve önceki aynı tarihli kayıtları ayırır. Başlangıçta
bulunan `browser-*.json` gözlemleri yeni çalıştırma değildir. Bu tur iki
tarayıcı bağlantısı zaman aşımına uğradı; yeni runtime gözlemi **0**.
Başka bir eşzamanlı işlemin yazdığı `08-coverage-and-limitations.md` ve zip,
bu turda yapılmış testlerin kanıtı olarak kullanılmadı.

## Sayım birimleri ve otomatik kapsam

| Birim | Gerçek sayı / ayrım | Kanıt |
| --- | --- | --- |
| Kaynak Markdown | 364: TR160, EN102, AR102; Hugo bağımsız kaynak listesi361, üç teşekkür dosyası leaf-bundle kaynağı | static-source-content.csv, static-summary.json; kaynak/URL eşlemesi02 CSV |
| Üretilen HTML | 976: TR369, EN302, AR305; 297 alias, 3 özel404, 24 pagination | Yeni recheck-production-static/static-summary.json |
| Alias/404 dışı route | 676: TR266, EN204, AR206; pagination dahil | Aynı özet; canonical URL sayısıyla aynı birim değil |
| Ayrı canonical adayları | 652: TR258, EN196, AR198; statik noindex bulunmadı |02 CSV ve dil sitemap'leri; Google indeks/HTTP200 sayısı değildir |
| Kaynak/şablon | 976 CSV satırında dil, sınıf, template_family; kaynak eşlemesi Hugo listesiyle zenginleştirilmiş | 02-url-and-template-inventory.csv |
| HTML link/asset/anchor | Bütün976 dosya; ham98 eksik link kullanımı, ilan edilen /tr kuralıyla32 çözülebilir; kalan66/42 hedef;4 fragment;0 eksik HTML asset | recheck-production-static/; static-link-triage.json. Gerçek sunucu bu redirect'i uyguluyor kabul edilmedi |
| Canonical/hreflang | Bütün çıktı;24 pagination canonical,72 ilgili hreflang sorunu; normal dil eşlemelerinde yinelenen/conflicting gruplar0 | static-canonical-issues.json, static-hreflang-issues.json |
| Metadata/headings/images | Bütün HTML; eksik title/description/tek-H1 bulgusu0; tekrarlar ayrı listeli. Schema image hedefi ayrı eksik | static-heading-issues.json, static-duplicate-*.json; SCH-05 |
| JSON-LD |976 HTML içinden679 script,3322 top node,parse hatası0; Microdata/RDFa0; hedefli sözlük/graph testleri | recheck-schema-output.json; tam reasoner/SHACL/resmî test değildir |
| Yeni üretim tekrar derlemesi | exit0;976 HTML önceki ayrı build ile byte-eş,fark0; yeni tam statik tarama exit0 | recheck-production-build.json/.log; recheck-build-comparison.json |

676 route veya652 canonical, Google'ın gerçekten indekslediği sayfa sayısı
değildir.404 dosyası olması gerçek HTTP404 olduğunu göstermez; alias refresh
HTML'i de gerçek server301 değildir. XML dosyası GET200 gibi sunulmadı.

## Mevcut gerçek URL ve şablon örneklemi

Aşağıdakiler02 CSV'de bulunan gerçek çıktı URL'leridir. Amaç bütün ana
şablonları/dilleri kapsayan tarayıcı ve performans planıdır; çalıştırılmayan
test yapılmış gibi gösterilmez. Kısaltmalar: **S** bu tur statik kaynak/çıktı
doğrulaması; **Ö** önceki aynı gün browser kanıtı; **N** runtime NOT_RUN.

| URL / aile | Şablon veya kapsam | Statik | Runtime / performans |
| --- | --- | --- | --- |
| https://docdrhabibcil.com/ | Ana sayfa/profile/hero, header,3B | S | Ö:localhost TR viewport/DEV3+3; yeni browser N; production benchmark N |
| https://docdrhabibcil.com/en/ | EN ana sayfa | S | N:tam EN menü/arama/modal/görsel/performans |
| https://docdrhabibcil.com/ar/ | AR ana sayfa,RTL | S | N:tam AR gezinme/RTL/klavye/performans |
| https://docdrhabibcil.com/hakkimda/ ; https://docdrhabibcil.com/en/about/ ; https://docdrhabibcil.com/ar/about/ | single,biyografi/kimlik | S | N:tam görsel/ekran okuyucu; doğru doğum yılı dış teyit yok |
| https://docdrhabibcil.com/iletisim/ ; https://docdrhabibcil.com/en/contact/ ; https://docdrhabibcil.com/ar/contact/ | single,form/saatler | S | N:POST/teslim/teşekkür; gerçek veri gönderilmedi |
| https://docdrhabibcil.com/klinik/ | list,klinik | S | N:tam browser ve gerçek klinik bilgi teyidi |
| https://docdrhabibcil.com/yayinlar/ | list,75 bibliyografik girdi/14 DOI | S | N:yayınların tüm yazarlık teyidi; bağımsız yayın detay URL'si yok,Uygulanamaz |
| https://docdrhabibcil.com/hizmetler/ | list,gerçek #girisimsel-kardiyoloji hub bölümü | S | N:tam kart/anchor/diagrams ve perf |
| https://docdrhabibcil.com/hizmetler/anjiyoplasti/ | single,girişimsel hizmet | S | N:şablon production perf ve klinik fact-check |
| https://docdrhabibcil.com/hizmetler/dizalti-damar-tikanikligi/ | single,dizaltı;görünür FAQ | S | Ö:390×844 keyboard,JSON-LD kod alımı; yeni N; production perf N |
| https://docdrhabibcil.com/hizmetler/periferik-damar/ | single,periferik/diyabetik ayakla vasküler ilişki | S | N:browser/perf ve klinik oran incelemesi |
| https://docdrhabibcil.com/hizmetler/alt-ekstremite-arter-hastaligi/ | single,boş kaynak/schema konu örneği | S | N:tarayıcı; boş sayfa konu modeli ayrıca SCH-07 |
| https://docdrhabibcil.com/blog/ | list | S | N:tam gezinme/perf |
| https://docdrhabibcil.com/blog/diyabetik-ayak/ | single,uzun rehber;hizmetten farklı hasta niyeti | S | N:browser/perf/uzman iddia incelemesi |
| https://docdrhabibcil.com/blog/periferik-arter-hastaligi/ | single,ikinci blog detay/bağlantılar | S | N:browser/perf |
| https://docdrhabibcil.com/en/services/echocardiography/ ; https://docdrhabibcil.com/ar/services/echocardiography/ | EN/AR hizmet,JSON-LD semantik örneği | S | N:EN/AR browser/perf |
| https://docdrhabibcil.com/en/blog/aortic-aneurysm-symptoms-diagnosis-and-modern-treatment-methods/ ; https://docdrhabibcil.com/ar/blog/aortic-aneurysm/ | EN/AR blog detay | S | N:EN/AR browser/perf |
| https://docdrhabibcil.com/tags/diyabetik-ayak/ | Taxonomy/manuel normal page ayrımı CSV'de | S | N:browser/perf |
| https://docdrhabibcil.com/categories/damar-hastalıkları/ | Gerçek term arşivi;encoded karşılığı aynı hedef olarak kontrol edilir | S | N:browser/HTTP/perf |
| https://docdrhabibcil.com/blog/page/2/ ; https://docdrhabibcil.com/en/blog/page/2/ ; https://docdrhabibcil.com/ar/blog/page/2/ | Pagination | S | N:browser/HTTP/perf;canonical sorunu STATIC-02 |
| https://docdrhabibcil.com/404.html ; https://docdrhabibcil.com/en/404.html ; https://docdrhabibcil.com/ar/404.html | Gerçek özel404 dosyaları | S | N:HTTP404; AR İngilizce metin/çıkış statik doğrulandı:UI-07 |

Eski https://docdrhabibcil.com/tr/ ve `/tr/hakkimda/` için kanıt,
mevcut canonical sayfa dosyası değil `static/_redirects:5` / netlify.toml
geçiş kuralıdır. GET301/Location/zincir/son200 testi **NOT_RUN**. Üç dilde
gerçek olmayan URL'nin sunucudan diline uygun404 döndürmesi de **NOT_RUN**.
Örnek dosya varlığından runtime sonucu türetilmedi.

## Tarayıcı ve performans matrisi

| Test | Önceki kayıt / bu tur | Eksik kapsam ve tek somut tamamlanma adımı |
| --- | --- | --- |
| Menü320/360/390/430/768/1024/1280/1440/1920 | Ö:TR,/localhost,DPR1;bug dört desktop genişlikte. YeniN | Çalışan browser ile EN/AR dahil aynı matris; her hata için screenshot+computed box/style |
| Eşik852/853/854 | Kaynaktan853 doğrulandı;browserN | Aynı tarayıcıda üç CSS genişliğini test et |
| Native %200 zoom | N | Gerçek tarayıcı zoom'u; viewport/DPR/zoom birlikte kaydet; ekran büyütme/emülasyon sayılmaz |
| Kalıcı görsel kanıt | Ö:browser-menu-1280-crop.jpg | Hero/AR/diğer viewport ve zoom için yeni ekran görüntüsü yok; çalışan browserda kaydet |
| Mobil menü/arama/randevu | Ö:390×844 dizaltı sayfasında belirli Escape/Shift+Tab/odak senaryoları | Bütün Tab sırası, telefon/WhatsApp dış işlemsiz href kontrolü, theme/footer/anchor/diagram etkileşimi üç dildeN |
| Ekran okuyucu/kontrast/touch target | N | Manuel yardımcı teknoloji ve gerçek computed kontrast/hedef ölçümü; WCAG2.2AA sonucu yok |
| JS kapalı,CDN/WebGL hatası,reduced-motion,Save-Data | N | Kontrollü tarayıcı senaryosu;statik fallback kodu runtime geçişi değildir |
| Production home ≥3desktop+3mobile cold | N | Yeni izole minify çıktıyı izinli ayrı test sunucusunda sun; aynı ağ/CPU/cache/sampling ve ham JSON/HTML/iz |
| Hizmet/blog ve diğer iki dil perf | N | Yukarıdaki temel şablon örnekleminde production desktop/mobile koşuları |
| Sıcak ziyaret | N | Cold paketinden ayrı sıcak-cache profil;DEV reload'u warm diye sunma |
| DEV3+3 metrik | Ö:ham Resource/Navigation Timing ve gözlenen long task/kayma | Üretim benchmark/saha p75/TBT/INP değil;04 raporunda ayrı medyan/aralık |
| 3B ilk viewport ve mobil scroll | Ö:desktop3/3 GLB,390px başlangıçta0,scroll sonrasıcanvas | Production trace/model açık-engelli A/B,offscreen frame sayımı,gizli sekme,re-entry tek init/loop,DPR/gölge/drawcall ölçümüN |
| LCP alt süreleri/CLS kaynakları/CPU-GPU | N | Üretim ağ/ana iş parçacığı/GPU izini al;DEV long task'ını nedensel olarak modele atama |
| DNS | Ö:Google Public DNS apexA/AAAANODATA,wwwNXDOMAIN,kontrolbaşarılı | Bu tur site DNS cevabı alınamadı;ikinci resolver+authoritative ile yenile |
| TLS/HTTP/cache/Brotli/gzip/ETag/protokol | N | Gerçek origin/target netleşince GET/HEAD ve timing/header test matrisi |
| Schema.org Validator / Google RRT | Ö:tek DEV hizmet JSON-LD kodu; bu tur yeniN | Üç dil/temel production şablonlarının kod girişiyle yeni örnekleri;iki servis farklı amaçta |
| CrUX/PSI/GSC/GBP,SERP | Doğrulanamadı / N | Yetkili rapor/export ve veri dönemi/cihaz/konum;06 iş listesi istenen export'ları belirtir |
| Klinik gerçeklik/unvan/sayı/saat/otorite | Doğrulanamadı | Yetkili CV/klinik kaydı+hekim incelemesi;web metnini kendi kanıtı sayma |

Yerel dinleme adresi bu tur `lsof` ile doğrulanamadı (boş çıktı,exit1);
önceki tarayıcı kaydının URL'si `http://localhost:1313/` idi. Bu kısıt,
sunucunun kullanıcı bilgisayarında durduğu anlamına gelmez. Sunucu yeniden
başlatılmadı, port/ağ kısıtı aşılmadı. Runtime/performance paketinin önündeki
tek ortam adımı, erişilebilir ayrı üretim test sunucusu ve çalışan tarayıcı
bağlantısıdır; hesap/klinik kayıtları ayrı veri bağımlılığıdır.

Tam kanıt listesi ve tekrar komutları
[README-reproduction.md](evidence/README-reproduction.md) içindedir.
