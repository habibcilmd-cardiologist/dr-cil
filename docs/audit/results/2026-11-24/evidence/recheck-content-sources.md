# İçerik ve taşıma bağımsız kontrolü — 24 Kasım 2026

Bu dosya önceki `content-evidence.json` ve `content-notes.md` kayıtlarını
silmeden yapılan yeniden incelemenin yöntemini ve resmî kaynaklarını kaydeder.
Kaynak içerik ve uygulama değiştirilmedi; mesaj/form gönderilmedi.

Yeniden üretim: depo kökünde
`python3 docs/audit/results/2026-11-24/evidence/recheck-content-check.py --build-root /tmp/dr-cil-audit-2026-11-24/public`.
Bu komut yalnız yeni `recheck-content-evidence.json` yardımcı kanıtını yazar.
`recheck-content-keyword-verification.json` içindeki sekiz hedef için
`build_file` dosyası okunup `<link rel=canonical>` değeri CSV'deki
`mevcut_canonical_url` ile karşılaştırılmıştır: **8/8 aynı**.
Hizmet hub'ında `id="girisimsel-kardiyoloji"` bulundu.

## Kaynak/çıktı tekrar kontrolü

- `content/{tr/hakkimda,en/about,ar/about}/index.md:16,21`: her üçünde
  1973 giriş yılı ve 1976 doğum tarihi aynı sayfada. CT-01 doğrulandı;
  hangi yılın doğru olduğu doğrulanamadı.
- `layouts/partials/home/hero.html:60,64,68`: 25+/20K+/100+ doğrudan
  sabitler. 75 numaralı yayın kaydı ve 14 DOI belirteci önceki sayımla
  yeniden karşılaştırılır. 75 kayıt, 100+ iddiasını çürütmez; liste :198'de
  tam CV'nin istenebileceğini söylüyor. CT-03 dayanak halen doğrulanamadı.
- `content/tr/hizmetler/_index.md:13`: `girisimsel-kardiyoloji` gerçek
  anchor tanımı. `content/tr/_index.md:35` aynı anchor'a bağlantı veriyor.
  CSV'deki öneri var olmayan anchor üretmiyor.
- `content/tr/iletisim/index.md:56` ve EN/AR karşılıkları Netlify POST
  formu. TR action eski `/tr/` yolunda. Yeni sunucuda backend/301 ile POST
  davranışı denenmedi; HOST-01 kanıtı kaynak bağımlılığıdır.
- `static/_redirects:5,8–11` ve `netlify.toml:20–23,68–118`: Netlify
  kuralları/başlıkları. Hedef sunucu bilinmediği için gerçek HTTP davranışı
  doğrulanmadı; hazırlık gereksinimleri bunların taşınmasıdır.
- `layouts/partials/extend-head-uncached.html:9–24`: üretimde Google tag
  ekleniyor. Development ölçümü bu üretim yükünü kapsamaz.
- `content/tr/kvkk/index.md:30–55` ve EN/AR privacy karşılıkları veri
  toplama metni içerir; gizlilik sayfası yok denmedi. Metinde üretim Google
  Analytics/Netlify altyapısının açıklaması ve saklama süresi bulunmadı.
  Uygulanacak hukuki yükümlülük veya ihlal kararı verilmedi.

## Bu turda açılan birincil kaynaklar

| Kaynak | Erişim | Bulguyu desteklediği sınır |
| --- | --- | --- |
| https://developers.google.com/search/docs/fundamentals/creating-helpful-content | 2026-11-24 | Yazar/kaynak/güven bilgisi ve olgusal doğruluk incelemesi; siteye özel sıralama sonucu değildir |
| https://support.google.com/business/answer/7091?hl=en | 2026-11-24 | Yerel bilgi doğruluğu ve alaka/mesafe/bilinirlik; bu sitede GBP/konum ölçümü yapılmadı |
| https://docs.netlify.com/manage/forms/setup/ | 2026-11-24 | `data-netlify` build algılama/teslim hizmeti ve `action` özel başarı sayfası; form teslim testi değildir |
| https://docs.netlify.com/manage/routing/redirects/overview/ | 2026-11-24 | `_redirects`/`netlify.toml` Netlify kural tanımları ve sıra davranışı |
| https://docs.netlify.com/manage/routing/headers/ | 2026-11-24 | `[[headers]]` yol kalıpları; yerel/yeni sunucuda uygulanma kanıtı değildir |

Web kaynak referansları (denetim oturumundaki alınan sonuç kimlikleri):
`turn451325074view0–4`, ilgili pasajlar `turn493786795view0–4`.
Bu kimlikler dış URL yerine geçmez; yeniden üretim yukarıdaki URL'leri açıp
ilgili `Who`, `relevance`, `data-netlify`, `_redirects`, `netlify.toml`
bölümlerini kontrol etmektir.

## Test sınırları

- GSC/GBP yetkili hesap bağlantısı mevcut araçlarda bulunmadı; GSC, profil
  doğrulaması, kategori, gerçek yorumlar, gösterim/tıklama, CTR ve konum
  raporları **NOT_RUN**. Herhangi bir ceza veya sıralama kaybı nedeni yoktur
  şeklinde de hüküm verilmedi.
- Canlı SERP/arama konumu ve hacim ölçümü **NOT_RUN**. Niyet eşlemesi,
  mevcut içerik amaçlarına dayanan editoryal plandır; hacim/sıra verisi değildir.
- Mesleki kimlik, unvan, toplam işlem sayısı, tüm yayınların yazarlığı ve
  saat/adres bilgisi için bağımsız yetkili kayıt doğrulaması **NOT_RUN**.
- Form mesajı, randevu veya WhatsApp iletisi gönderimi **NOT_RUN**.
- DNS/TLS/HTTP ölçümünü root denetimi yönetir; bu alt inceleme önceki
  `browser-public-dns.json` kaydını yeni alınmış DNS yanıtı olarak sunmaz.
