# İçerik, hedef sorgular, tıbbi güven ve yerel görünürlük

Tarih: 24 Kasım 2026. Kapsam: mevcut kaynaklar ve
`/tmp/dr-cil-audit-2026-11-24/public` üretim çıktısı. Kaynak kodu değiştirilmedi.
Tamamlayıcı kanıt: `content-evidence.json`; sorgu eşlemesi:
`../05-keyword-url-map.csv`. Canlı Google sıralaması, GSC, GBP yetkili hesap
durumu, gerçek dönüşümler ve klinik iddiaların doğruluğu bu alt incelemede
ölçülmedi. Aşağıdaki içerik sorunları bir Google cezasının veya sıralama kaybının
kanıtı değildir.

## Doğrulanan bulgular ve kabul ölçütleri

### CT-01 — Biyografide üç dilde çelişen doğum yılı — P1, Doğrulandı

- URL'ler: `https://docdrhabibcil.com/hakkimda/`, `/en/about/`, `/ar/about/`.
- Kaynak: `content/tr/hakkimda/index.md:16` ve `:21`; EN ve AR
  `about/index.md` dosyalarında da aynı satırlar.
- Giriş paragrafı 1973, özgeçmiş paragrafı 1976 yılını bildiriyor. İki ifade
  aynı sayfada ve üretilen çıktıda birlikte bulunuyor.
- Etki: hekimin kimlik bilgisi hakkında doğrudan kullanıcı güveni sorunu.
- Öneri: doğru yılı kullanıcı/özgeçmiş kaynağı ile belirleyip tek gerçek veri
  kaynağına bağlamak. Bu denetim hangi yılın doğru olduğuna karar vermiyor.
- Kabul: TR/EN/AR biyografi ve varsa structured data aynı doğrulanmış bilgiyi
  göstermeli; otomatik arama ve görünür içerik kontrolüyle tekrar doğrulanmalı.

### CT-02 — Görünen çalışma saatleri ile schema saatleri farklı — P1, Doğrulandı

- URL: `https://docdrhabibcil.com/iletisim/`, EN ve AR iletişim karşılıkları;
  schema ana sayfalarda da kullanılıyor.
- Kaynak: `content/tr/iletisim/index.md:27`,
  `content/en/contact/index.md:27`, `content/ar/contact/index.md:27`;
  `layouts/partials/schema.html:71-72`.
- Görünür bilgi Pazartesi–Cumartesi 08:00–18:00. JSON-LD
  Pazartesi–Cuma 09:00–18:00 ve Cumartesi 09:00–14:00 bildiriyor.
- Etki: hastanın ziyaret/randevu kararında çelişki; yapılandırılmış verinin
  görünür içerik ve işletme bilgileriyle tutarlılığı bozuluyor.
- Öneri: gerçek hekim/klinik saatlerini doğrulayıp içerik, schema ve yetkili
  GBP kaydıyla eşlemek. GBP'nin şu anki saati görülmedi.
- Kabul: bütün dillerde görünen ve işaretlenen saatler aynı; özel/tatil
  saatleri yalnız doğrulanmışsa eklenmiş olmalı.

### CT-03 — Hero sayısal iddiaları veri kaynağından kopuk — P1, Doğrulandı / dayanak Doğrulanamadı

- URL: üç dilin ana sayfaları.
- Kaynak: `layouts/partials/home/hero.html:60-69` doğrudan `25+`, `20K+`,
  `100+` sabitlerini yazıyor. `i18n/tr.yaml:6` ayrıca 25 yılı aşkın deneyim
  iddiasını içeriyor.
- Kaynak kodda 20K+ girişim için kayıt/atıf görülmedi. Yayın sayfasında
  `content/tr/yayinlar/_index.md:27-193` toplam 75 numaralı kayıt var:
  25 uluslararası makale, 9 uluslararası bildiri, 2 kitap bölümü,
  18 ulusal makale, 21 ulusal bildiri. Bunlar 75 ayrı numaralı girdidir;
  yayın türleri arası olası aynı çalışma eşleşmeleri ayıklanmadı.
- Bu sayım 100+ iddiasının yanlışlığını kanıtlamaz: liste eksik olabilir ve
  sayfa zaten tam CV'nin talep edilebileceğini söylüyor (`:197-198`). Ancak
  100+'ın tanımı ve dayanağı bu site çıktısıyla doğrulanamıyor.
- Öneri: deneyim başlangıcı, toplam girişim ve yayın tanımı/kapsamını gerçek
  mesleki kayıtlarla onaylayıp görünür dayanak ve güncellik bilgisi oluşturmak.
  İddiaları otomatik olarak daha büyük sayılarla değiştirmemek.
- Kabul: her sayı için sahibi, tarih aralığı, tanımı ve doğrulanmış dayanak;
  üç dil ve biyografi/yayın sayfalarında tutarlılık. Kişisel/kurumsal gizli
  kayıtlar herkese açık yayımlanmak zorunda değildir; iddia yine doğrulanmalı.

### CT-04 — Hedef sağlık içeriğinde oranların kaynakları gösterilmiyor — P1, Doğrulandı / klinik doğruluk Doğrulanamadı

- URL: `/blog/diyabetik-ayak/`, `/blog/periferik-arter-hastaligi/`,
  `/hizmetler/dizalti-damar-tikanikligi/`, `/hizmetler/periferik-damar/`.
- Dört kaynak dosyada sırasıyla 23, 4, 19 ve 1 adet yüzde içeren satır var;
  bunların tümü araştırma sonucu değildir (ör. tedavi hedefi de olabilir).
  Dört dosyanın hiçbirinde HTTP kaynak bağlantısı veya Kaynak/Referans
  başlıklı kaynakça bölümü yok.
- Somut örnek: `content/tr/blog/diyabetik-ayak/index.md:344-393` teknik başarı,
  bacak kurtarma, açıklık ve yara iyileşmesi oranları veriyor; `:463-487`
  zaman ufuklu başka sonuçlar veriyor. `content/tr/hizmetler/dizalti-damar-tikanikligi/index.md:25`
  ekstremite kurtarma oranı, `:75-86` prognoz ve yaygınlık oranları içeriyor.
- Kaynak yokluğu bu oranların yanlış olduğu anlamına gelmez. Denetim,
  çalışmaların hasta grubu, işlem türü, takip süresi ve sonlanım tanımının
  okuyucu tarafından doğrulanamadığını saptıyor.
- Öneri: hekim editoryal incelemesinde her klinik iddiayı güncel birincil
  kılavuz veya uygun çalışmayla eşlemek; teknik başarı, ekstremite kurtarma,
  yara iyileşmesi ve damar açıklığını ayrı sonlanımlar olarak korumak.
- Kabul: ilgili iddiaların yanında erişilebilir kaynak/tarih/bağlam;
  gerçek inceleme tarihi ve sorumlusu; desteklenmeyen iddialar için hekimin
  onayladığı düzeltme. Bu turda tıbbi metin değiştirilmedi.

Klinik inceleme için doğrulanmış başlangıç kaynakları:

- [IWGDF 2023 güncelleme merkezi](https://iwgdfguidelines.org/guidelines-2023/):
  diyabetik ayak, PAD, yara bakımı ve offloading için ayrı kılavuzlar mevcut;
  merkez bazı güncellemelerin 2027'de yapılacağını belirtiyor.
- [AHA 2024 PAD kılavuzu özeti](https://professional.heart.org/en/science-news/2024-guideline-for-the-management-of-lower-extremity-peripheral-artery-disease/top-things-to-know):
  farklı klinik PAD grupları ve çok disiplinli bakım ayrımı var. Bu kaynağı
  okumak sitedeki bütün oranları doğrulamak yerine geçmez.

### CT-05 — İki ana rehberden ilgili vasküler hizmetlere doğrudan bağlantı yok — P2, Doğrulandı

- URL: `/blog/diyabetik-ayak/`, `/blog/periferik-arter-hastaligi/`.
- Kaynak: bu iki blog dosyasında `relref` veya `/hizmetler/` içerik bağlantısı
  bulunmadı. Üretim HTML'sindeki bütün anchor'lar tarandığında da
  `/hizmetler/dizalti-damar-tikanikligi/` ve `/hizmetler/periferik-damar/`
  hedeflerine doğrudan bağlantı bulunmadı; bu kontrol sorgu dizelerinde yer
  alan sosyal paylaşım URL'lerini iç bağlantı saymıyor.
- Hizmetlerin kendi aralarında bağlantı var:
  `content/tr/hizmetler/periferik-damar/index.md:220-225`,
  `content/tr/hizmetler/dizalti-damar-tikanikligi/index.md:402-406`.
- Etki: ilgili hasta bilgilendirmesinden değerlendirme/hizmet kapsamına geçiş
  zayıf. Bu bir sıralama etkisi ölçümü değildir.
- Öneri: klinik olarak uygun bağlamlarda mevcut rehber ve hizmet sayfalarını
  birbirine bağlamak; diyabetik ayağı yalnız damar açma işlemiyle eşitlememek.
- Kabul: belirlenen rehber/hizmet çiftlerinde anlamlı, erişilebilir, doğru
  canonical hedefli çift yönlü bağlantılar; şablon linkleri ve kullanıcı yolu
  tarayıcıda kontrol edilmiş olmalı.

### CT-06 — Varsayılan yazar kutusunda biyografi bağlantısı yok — P2, Doğrulandı

- Örnek URL: `/blog/diyabetik-ayak/`.
- Kaynak: `themes/blowfish/layouts/partials/author.html:43-55` yazar adını
  metin olarak, bio'yu kısa açıklama olarak gösteriyor; isim biyografiye link
  değil. `layouts/_default/single.html:135-137` varsayılan yazar partial'ını çağırıyor.
- Hakkımda sayfası genel menüden erişilebilir; yazar bilgisi bütünüyle yok
  değildir. Sorun yazı bağlamından mesleki kanıta doğrudan geçiş eksikliğidir.
- Öneri/kabul: yazar kutusundan doğru dilde doğrulanmış biyografiye erişim;
  varsa gerçek editör/inceleyici ile yazarı ayıran doğru bilgi.

### CT-07 — İletişim formları Netlify backend'ine bağımlı — P1 taşıma hazırlığı, Doğrulandı

- URL: `/iletisim/`, `/en/contact/`, `/ar/contact/`.
- Kaynak: her dilin iletişim `index.md:56` satırı `data-netlify=true` ile
  POST formu üretiyor. TR action eski `/tr/iletisim/tesekkurler/`; EN
  `/en/contact/thank-you/`; AR `/ar/contact/shukran/`.
- Düz statik dosya sunucusunun bu formu işleyeceğini varsaymak geçersizdir.
  Form işleme backend'i veya yetkili bir servis ayrıca tasarlanmalı/test edilmeli.
  Eski TR action'ın 301 üzerinden geçmesi POST yönlendirme davranışı açısından
  ayrıca test edilmeli; gerçek ortamda hangi yanıtın alındığı ölçülmedi.
- Hiçbir gerçek form/hasta mesajı gönderilmedi. Mevcut Netlify form işlemesinin
  çalışıp çalışmadığına dair sonuç yok.
- Kabul: seçilen yeni sunucuda sentetik veriyle yetkili entegrasyon testi;
  başarı/başarısızlık durumu, spam ve gizlilik yaklaşımı, doğru dilde teşekkür
  URL'si ve alıcıya teslim; kullanıcıya yalnız başarı sayfası göstermek yeterli değil.

### CT-08 — Bilgilendirici/hekim/hizmet rollerinin eşleştirilmesi gerekiyor — P2, Güçlü aday

- Mevcut ana sayfa title ve description yerel kardiyolog niyetini zaten
  içeriyor (`content/tr/_index.md:2-20`). Hizmet kataloğunda girişimsel
  kardiyoloji ve periferik alt dallar var (`content/tr/hizmetler/_index.md:12-43`).
- Buildde `diyabetik` adını taşıyan sayfalar blog ve etiket arşivi; ayrı
  diyabetik ayak hizmet sayfası bulunmadı. Vasküler alt sorunları açıklayan
  mevcut dizaltı/periferik hizmetler, diyabetik ayağın bütün bakım kapsamıyla
  aynı şey değildir.
- Öneri: önce CSV'deki rollerle mevcut sayfaları netleştirmek. Yeni hizmet
  sayfası yalnız gerçek hizmet kapsamı/ekip bilgisi ve arama niyeti gerektiriyorsa
  hazırlanmalı; her sorgu için aynı içerikli yeni sayfa açılmamalı.
- GSC olmadan query cannibalization, arama hacmi, anahtar kelime konumu veya
  dönüşüm kaybı doğrulanamadı. Birden fazla sayfanın aynı konudan söz etmesi
  tek başına sorun değildir.
- Kabul: sekiz sorgunun URL/amaç eşlemesi uzman tarafından onaylı; her sayfa
  farklı kullanıcı ihtiyacını karşılıyor; GSC baseline ve izleme planı var.

## Pozitif unsurlar ve kapsam sınırı

Hakkımda sayfaları ayrıntılı eğitim/mesleki deneyim ve uzmanlık bölümleri
sunuyor. Yayın listesi boş değil; 14 DOI metni ve 75 numaralı bibliyografik
kayıt içeriyor. Bir örnek DOI (10.1111/joic.12225) PubMed aramasında gerçek
makale kaydıyla eşleşti, ancak açılan PubMed sayfası bu oturumda yazar listesini
döndürmedi; bu nedenle tüm yazarlık/kurum/unvan bilgileri dış kaynaklarla
doğrulanmış sayılmadı. Yayın listesinin tamamına sahte/uydurma denemez.

Hedef diyabetik ayak ve dizaltı içeriğinde çok disiplinli bakım, riskler ve
acil yardım uyarıları da var. Bunlar korunmalı; sorun yalnız metni daha fazla
anahtar kelimeyle doldurarak çözülmemeli.

## Yerel görünürlük için doğrulanamayanlar ve gerekli baseline

Yetkili GBP kaydı, kategorileri, doğrulama durumu, yorumlar ve profil
performansı bu alt incelemede okunmadı. GSC sorgu/sayfa raporuna erişilmedi;
canlı sıralama ve arama hacmi ölçülmedi. Gerekenler:

1. GSC son 16 ay sorgu/sayfa/cihaz/ülke dışa aktarımı; kesinti öncesi/sonrası
   eşlenebilir dönem ve son 28/90 gün karşılaştırması. Ortalama konum tek bir
   sabit ülke sıralaması olarak yorumlanmamalı.
2. GBP'nin kullanıcıya ait doğrulanmış kaydı ve mevcut isim/adres/saat/
   kategori/website ekranı; gerçek işletme bilgileriyle eşleme.
3. İletişim/randevu bağlantı tıklamalarının kişisel sağlık verisi içermeyen
   toplu ölçümü ve doğru üretim Analytics yapılandırmasının teyidi.
4. Doğrulanmış mesleki profiller ve gerçek kurumsal ilişki/mesleki atıflar.
   Bağlantı/yorum satın alma veya yapay ilçe sayfaları önerilmez.

## Resmî kaynaklar — 24 Kasım 2026 tarihinde okundu

- [Google yerel sıralama rehberi](https://support.google.com/business/answer/7091?hl=en):
  işletme bilgilerinin doğruluğunu ve alaka/mesafe/bilinirlik boyutlarını
  açıklıyor; harita sonuçları için yapılan bu açıklama ulusal organik sıra
  garantisi değildir.
- [Google people-first içerik rehberi](https://developers.google.com/search/docs/fundamentals/creating-helpful-content):
  kaynakların, yazar bilgisinin ve doğruluğun değerlendirilmesini öneriyor;
  E-E-A-T bağımsız bir mekanik puan veya tek sıralama faktörü olarak sunulmuyor.

İçerik için önerilen hiçbir değişiklik bu turda uygulanmadı.
