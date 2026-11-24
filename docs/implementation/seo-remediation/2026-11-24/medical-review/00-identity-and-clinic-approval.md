# Hekim ve klinik bilgileri — onay kaydı taslağı

Tarih: 24 Kasım 2026. İlgili kayıtlar: **CT-01, CT-03, SCH-06, SCH-08**.
Durum: **Bloke — yetkili olgusal onay bekliyor**. Bu dosya görünür site
içeriği değildir; `content/` veya schema'ya otomatik aktarılmamalıdır.
Doğum yılı, saat, işlem/yayın sayısı veya kurum ilişkisi seçilmedi.

Kaynak satırları bu taslak hazırlanırken okunan kaynaklara ve önceki audit
JSON-LD snapshot'ına aittir. Devam eden teknik düzenlemeler satırları
kaydırabilir; alıntı ve dosya birlikte kontrol edilmelidir. Eski audit
kanıtları değiştirilmemiştir.

| Onay ID / bulgu | Önceki olgu ve kaynak | Gereken gerçek kayıt / karar | Onay sonrası en küçük değişiklik | Durum |
| --- | --- | --- | --- | --- |
| MR-I01 / CT-01 | TR `content/tr/hakkimda/index.md:16` 1973; `:21` 3 Nisan1976. EN/AR about dosyalarında da `:16,21` aynı çelişki | Hekimin doğru doğum yılı ve yayında doğum bilgisini tutma tercihi; kamuya açık onaylı CV yeterli, kimlik belgesi kopyası istenmiyor | Üç dilde onaylı tek bilgi veya hekimin onayıyla gereksiz doğum bilgisini çıkarmak; rastgele yıl seçmemek | Bekliyor |
| MR-I02 / SCH-06 | TR/EN/AR contact `index.md:27`: Pzt–Cmt08:00–18:00; audit `evidence/schema-iletisim-index.json`: Pzt–Cum09:00–18:00, Cmt09:00–14:00 | Saatler hekimin muayene saati mi hastanenin genel saati mi? Randevu usulü, geçerli hafta günleri, tatil istisnaları; klinik sorumlusu teyidi | Görünür üç dil ve varsa onaylı LocalBusiness saatlerini aynı kaynaktan üretmek. Yalnız eski schema ile görünür saatten birini seçmemek | Bekliyor; teknik schema omit/gate düzeltmesi bu gerçeklik onayı sayılmaz |
| MR-I03 / CT-03 | `layouts/partials/home/hero.html:60`:25+; `i18n/tr.yaml` hero açıklamasında 25 yılı aşkın klinik deneyim | Deneyim başlangıç tarihi; hekimlik/kardiyoloji uzmanlığı/girişimsel deneyim ayrımı; ölçüm tarihi | Onaylı kapsam ve tarih; gerekli ise kesin olmayan sayıyı onaylı nötr mesleki açıklamayla değiştirmek | Bekliyor |
| MR-I04 / CT-03 | Hero `:64`:20K+ invaziv girişim | İşlem tanımı, sayım dönemi, kişisel operatör/ekip katılımı ayrımı ve doğrulanmış toplu kayıt; hasta/kurum ham kayıtları siteye veya bu rapora kopyalanmamalı | Yalnız onaylı toplu sayı ve tanımı. Sayıyı büyütme, tahminle düşürme veya yayın listesiyle doğrulama yapma | Bekliyor |
| MR-I05 / CT-03 | Hero `:68`:100+ yayın; `content/tr/yayinlar/_index.md:27–193`:75 numaralı bibliyografik girdi; `:197–198` tam CV talep edilebilir. Biyografi `:87` 25+ uluslararası makale | “Yayın” tanımı: makale/bildiri/kitap bölümü; benzersiz çalışma sayısı, güncellik tarihi, onaylı tam bibliyografi ve yazarlık | Liste eksik olabilir;75 sayımı100+ iddiasını çürütmez. Tek onaylı kapsamla üç dilde sayı/başlık uyumu | Bekliyor |
| MR-I06 / SCH-08 | Audit procedure snapshot'ında `recognizingAuthority.name=Türk Kardiyoloji Derneği`; eski partial `.Lastmod`→`lastReviewed`, otomatik `reviewedBy` | Gerçek inceleyici adı/rolü/tarihi ve incelenen sayfa/sürüm; kurum için özel tanıma/onay belgesi veya hangi standartla ilişki kurulduğunun açık dayanağı | Kılavuz atfı, dernek üyeliği ve kurum onayı ayrı iddialardır. Dayanak yoksa bu property'leri üretmemek; onay varsa dar kapsamlı gerçek metadata | Bekliyor; bu teknik hata kapansa bile gerçek kurum/review onayı alınmış olmaz |
| MR-I07 / SCH-08 | Audit clinic JSON-LD:41.0082,28.9784; `priceRange=$$$`; klinik adı “Doç. Dr. Habib ÇİL - Kardiyoloji Kliniği” | Gerçek işletme/ofis varlığı, hekim–hastane ilişkisi, doğru yer koordinatı/adres, telefon/uzantı ve fiyat bilgisinin yayımlanma gerekçesi; yetkili GBP/klinik teyidi | Klinik varlığını ve hekimi ayrı modellemek; doğrulanmamış geo/fiyat/özel klinik adı üretmemek. Site metnindeki hastane adı bağımsız özel klinik varlığını kanıtlamaz | Bekliyor |
| MR-I08 / kimlik tutarlılığı | `content/tr/iletisim/index.md:45` DoktorSitesi URL'si `prof-dr-...`; diğer yerde `doc-dr-...`; görünen unvan Doç.Dr. | Güncel gerçek unvan, profilin gerçekten aynı hekime ait olması ve tercih edilen gerçek profil adresi; yetkili CV/kurumsal kayıt | Sadece doğrulanmış profile link/sameAs; URL'deki unvandan yeni akademik unvan türetmemek | Bekliyor |

## Doldurulacak onay alanı

| Alan | Yetkili yanıt |
| --- | --- |
| Onaylayan / rol | Bekliyor |
| Onay tarihi | Bekliyor — otomatik bugünün tarihi review tarihi değildir |
| Kaynak CV/kurumsal kayıt adı ve sürümü | Bekliyor |
| MR-I01–08 için ayrı karar | Bekliyor |
| Kamuya açılabilecek bilgi kapsamı | Bekliyor |
| Üç dil karşılıklarının kontrolü | Bekliyor |

Bağımsız menü, bağlantı, şablon ve schema domain/enum düzeltmeleri bu
onayları beklemek zorunda değildir. Doğrulanmamış alanların graph'tan
çıkarılması/gate edilmesi, kalan görünür içerikteki iddiaların tıbbi veya
olgusal olarak onaylandığı anlamına gelmez.
