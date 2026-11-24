# Gerçek veri akışı ve gizlilik eşlemesi — CT-09

24 Kasım 2026. **İnceleme taslağı; hukuki uygunluk/ihlal kararı değildir.**
Yalnız mevcut metin/şablon ve önceki audit gözlemleri okundu. Form/hasta
mesajı, WhatsApp iletisi, randevu veya hesap değişikliği yapılmadı. Mevcut
gizlilik sayfaları bulunduğu için “gizlilik sayfası yok” sonucu verilmedi.

## Kaynak ve bilinmeyenler

| Kanal | Somut kaynak | Görülen veri/bağımlılık | Henüz bilinmeyen |
| --- | --- | --- | --- |
| İletişim formu | `content/tr/iletisim/index.md:56–80` ve EN/AR contact karşılıkları | Netlify POST; ad,telefon,e-posta,serbest metin; yeni uygulamadaki backend/gating son durumu root raporunda | Gerçek aktif endpoint/teslim alıcısı,saklama,erişim yetkileri,spam/servis logları,başarı/hata/iletim testi |
| Google tag | `layouts/partials/extend-head-uncached.html:9–24` okuma anında production+serverolmayan koşulla tag/config | Üretimde üçüncü taraf istek kodu var; development yüklememesi üretim davranışını kanıtlamaz | Gerçek istek/çerez/tercih davranışı,olay parametreleri,URL/query aktarımı,hesap ayarları,retention; browser ölçümü ayrı |
| WhatsApp | İletişim sayfası ve sabit bağlantılar; KVKK`:50–53` | Kullanıcının dış hizmete gitmesini sağlayan bağlantı; gerçek ileti gönderilmedi | İşletme/kişisel hesap,cihaz/erişim,saklama/aktarım düzeni; tıklama mesaj teslimi değildir |
| Dış randevu sağlayıcıları | `appointment-section` ve modal hedefleri | Dış profillere bağlantı | Hangi kuruluşun hangi veriyi aldığı ve kendi bilgilendirmesi; site içi tıklama randevu değildir |
| Gizlilik metinleri | TR `/kvkk/` kaynak`:18–55`,EN/AR `/privacy/` kaynak`:18–51` | Amaçlar,kimlik/iletişim/sağlık verisi ve aktarım kategorileri anılıyor | Gerçek altyapı/sağlayıcı/amaç/retention ile metin birebir eşlemesi; metindeki sağlık-hizmeti/insurance akışının bu web formuna uygulanıp uygulanmadığı |

## Yetkili sorumlu tarafından doldurulacak kontrol formu

| Alan | Kontrol / karar | Durum |
| --- | --- | --- |
| Veri sorumlusu ve iletişim | Gerçek kişi/kuruluş,sorumlu rolü,başvuru kanalı | Bekliyor |
| Formun işlevi | Genel iletişim mi randevu talebi mi? Web üzerinden sağlık belgesi/klinik ayrıntı alınacak mı? Gereksiz veri istememe kararı | Bekliyor |
| Her form alanı | Amaç,zorunluluk,alıcı,işleme/saklama süresi ve silme/erişim süreci | Bekliyor |
| Endpoint/sağlayıcı | Netlify veya seçilecek gerçek backend;alt işleyenler,bulunduğu ortam ve işletmeci | Bekliyor |
| Başarı ve hata | Mesaj teslimi ile teşekkür GET ayrı;hata halinde yanlış başarı gösterilmemesi;sentetik yetkili staging testi | NOT_RUN |
| Analitik olaylar | Tıklama/teslim/randevu ayrımı;ad/telefon/e-posta/sağlık/serbest metin veya bunları içeren URL/query gönderilmemesi | Yapılandırma ve browser kabulü bekliyor |
| Çerez/tercih | Gerçek ilk yükleme ve tercih değişikliğinden sonra istek/çerez testi;uygulanacak gereklilikleri uzman değerlendirecek | NOT_RUN |
| Metin ve diller | Seçilen gerçek akışın TR/EN/AR görünür metinlerle eşlenmesi;anlaşılır açıklama,gerçek sağlayıcı bilgileri | Bekliyor |
| Klinik akış sınırı | Web formu açıklamasını hastanenin bütün hasta kayıt/tedavi sistemini tanımlıyor gibi genişletmeme | Bekliyor |
| İnceleme kaydı | Yetkili sorumlu/uzman,tarih,karar ve yayımlanacak sürüm | Bekliyor |

## Öneri taslağı

Mevcut soyut hukuki metne varsayımla sağlayıcı,ülke,saklama süresi veya
izin mekanizması eklemeyin. Önce yukarıdaki gerçek akışı onaylayın; ardından
hangi açıklamanın hangi kanalı anlattığını ayırın. Formun sağlık bilgisi
istememesi tercih ediliyorsa serbest metnin yanında bu kapsamı anlaşılır
ifade etme önerisi yetkili sorumlu tarafından incelenmelidir. Yeni backend
hazır değilken çalışıyor gibi form sunulmaması teknik kabulüdür; bunun tek
başına hukuki uygunluk sağladığı iddia edilmemelidir.

Bu alt görevde `content/*/privacy`, `content/tr/kvkk`, analitik ayarı veya
form kodu değiştirilmedi. Kaynakta varlık incelemesi runtime çerez/ağ
kabulünün ve yetkili hukuki değerlendirmenin yerine geçmez.

## Yerel uygulama sonrası varsayılan

`params.contactForm.provider="disabled"`: etkin form alanı yok; telefon/WhatsApp bağlantıları gösterilir. Önceki form alanları yukarıda başlangıç veri akışı olarak incelenmiştir. Netlify veya endpoint modu açıkça seçilmeden yeni form verisi toplanmaz. Üretim Analytics kaynağı mevcut haliyle korunmuştur; gerçek çerez/tercih ve hukuki inceleme beklemektedir. Sentetik mesaj dahil gerçek dış alıcıya gönderim yapılmadı.
