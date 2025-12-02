# 🗺️ Proje Yol Haritası – Dr. Habib ÇİL Tanıtım Sitesi

Mevcut dokümantasyonunuzu temel alarak projenin hayata geçirilmesi için izlenmesi gereken adımlar şunlardır:

## 1. Projenin Başlatılması (Temel Setup)

`2-Blowfish-Hugo.md` dosyasında anlatıldığı gibi Hugo projesini oluşturun, Blowfish temasını bir "Git submodule" olarak ekleyin ve temel klasör/dosya yapısını hazırlayın.

**Yapılacaklar:**

-   Hugo Extended sürümü yüklü mü kontrol edin
-   `hugo new site dr-cil` ile yeni proje oluşturun
-   Blowfish temasını submodule olarak ekleyin: `git submodule add https://github.com/nunocoracao/blowfish.git themes/blowfish`
-   `config/_default/` klasörünü oluşturup config dosyalarını yerleştirin

**Başarı Kriteri:** `hugo server` komutunda hatasız çalışma ve localhost:1313'te boş site görüntülenmesi

---

## 2. Versiyon Kontrolü (Git Setup)

Proje zaten bir Git deposu içinde. İlk adımı tamamladıktan sonra bir commit yaparak projenin başlangıç noktasını sabitleyin.

**Yapılacaklar:**

-   Temel yapı ve config dosyalarının commit'ini yapın
-   GitHub'daki (`portwebdesign/dr-cil`) remote'a push edin

---

## 3. İçeriklerin Eklenmesi (Content Structure)

Sitenin asıl içeriklerini (akademik yayınlar, klinik hizmetler, blog yazıları vb.) `1-Araştırma.md` ve `4-Çoklu-Dil.md`'de önerilen yapıya göre content klasörüne eklemeye başlayın.

**Yapılacaklar:**

-   **Çoklu Dil Desteği:** `config/_default/languages.toml` içinde TR ve EN dil ayarlarını yapın
-   Content klasörü altında `tr/` ve `en/` alt klasörleri oluşturun
-   **Sayfalar:** Ana sayfa (\_index.md), Hakkımda, Kliniğim, Yayınlar, Blog, İletişim sayfalarını oluşturun
-   **Akademik İçerik:** Yayınları, konferans bilgilerini, eğitim geçmişini ekleyin
-   **Klinik İçerik:** Uzmanlık alanları, tedavi yöntemleri, klini­ği hakkında bilgi, çalışma saatleri ekleyin

**Not:** `1-Araştırma.md`'de Blowfish'in akademik + hasta odaklı tasarımda dengeleri vurgulanmıştır. İçerik bu dengede olmalıdır.

---

## 4. Ekstra Özelliklerin Entegrasyonu (Critical Features)

`3-Extra-Olmalı.md` dosyasında belirtilen kritik eklemeleri yapın. **Bu adım SIRAYLA takip edilmelidir:**

### 4.1 Yasal Footer Uyarısı (Zorunlu)

-   Türkiye'de tıbbi siteler için yasal uyarı sorumludur
-   `layouts/` klasörü altında `_default/baseof.html` override edin
-   Footer'a şu metni ekleyin:
    ```
    "Bu sitedeki bilgiler sadece bilgilendirme amaçlıdır.
    Tanı ve tedavi için mutlaka sağlık profesyoneline başvurunuz.
    Bu site Tabipler Birliği Etik Kurallarına uygun hazırlanmıştır."
    ```

### 4.2 Hızlı İletişim: Sabit WhatsApp Butonu

-   Mobil dönüşüm oranını %100+ artırır
-   `baseof.html` içinde `</body>` etiketinden hemen önce WhatsApp floating button HTML/CSS'sini ekleyin
-   Telefon numarası: Doç. Dr.'ın güncel numarası ile güncellenmelidir
-   UX için önem: **Kritik**

### 4.3 Netlify Forms ile İletişim Formu

-   Statik sitede veritabanı olmadığından Netlify'ın ücretsiz formu kullanın
-   İletişim sayfasında form HTML'ine `data-netlify="true"` ekleyin
-   Form gönderildiğinde Netlify dashboard'a otomatik kayıt olur
-   E-posta bildirimi ayarı: Netlify panel'den yapılandırılabilir

### 4.4 Robots.txt ve Sitemap

-   `static/robots.txt` dosyası oluşturun
-   Hugo otomatik `sitemap.xml` oluşturur ancak `enableSitemap = true` config'de aktif olmalıdır
-   Google Search Console'a sitemap submit edin

### 4.5 Özel 404 Sayfası

-   `layouts/404.html` dosyası oluşturun
-   Kullanıcı dostu hata mesajı ve ana sayfaya yönlendirme
-   Site haritası veya popüler sayfalar linki ekleyin

### 4.6 KVKK Uyumluluk Sayfası

-   Türkiye'de kişisel veri toplayan siteler için zorunlu
-   `content/tr/kvkk.md` ve `content/en/privacy.md` sayfaları oluşturun
-   İletişim formu ve çerez kullanımı hakkında bilgilendirme
-   Footer'da KVKK sayfasına link ekleyin

---

## 5. Görsel Özelleştirme (Branding)

Blowfish temasının renk, font gibi görsel ayarlarını Doç. Dr. Habib ÇİL'in kurumsal kimliğine uygun şekilde özelleştirin.

**Yapılacaklar:**

-   `config/_default/params.toml` içinde:
    -   `colorScheme` ayarı (light/dark/auto)
    -   `primaryColor` → Profesyonel mavi/yeşil tonları önerilir
    -   Font ailesini (sans-serif profesyoneller için ideal)
-   `assets/` klasörüne kişisel logo PNG'sini ekleyin
-   Hero section'da Doç. Dr.'ın profesyonel fotoğrafını yerleştirin

---

## 5.5 Görsel Optimizasyon (Image Optimization)

`1-Araştırma.md`'de vurgulanan performans hedeflerine ulaşmak için görsel optimizasyonu kritik öneme sahiptir.

**Yapılacaklar:**

-   **WebP Dönüşümü:** Hugo'nun dahili resim işleyicisini kullanın:
    ```go
    {{ $img := resources.Get "images/doktor.jpg" }}
    {{ $webp := $img.Resize "800x webp q80" }}
    <img src="{{ $webp.RelPermalink }}" alt="Doç. Dr. Habib ÇİL">
    ```
-   **Lazy Loading:** `params.toml` içinde `enableImageLazyLoading = true` ayarını aktifleştirin
-   **Responsive Images:** Farklı ekran boyutları için `srcset` kullanın
-   **Boyut Hedefleri:**
    -   Hero görseli: max 200KB (WebP)
    -   Profil fotoğrafı: max 100KB (WebP)
    -   Blog görselleri: max 80KB (WebP)

**Kazanç:** %70–80 performans artışı

---

## 6. SEO ve Teknik Optimizasyon

`1-Araştırma.md`'de detaylandırıldığı gibi temel SEO ayarlarını yapın:

**Yapılacaklar:**

-   **Physician Schema (JSON-LD):** `layouts/partials/seo_schema.html` dosyası oluşturun
    -   Schema türleri: `Physician`, `MedicalBusiness`, `Person`, `LocalBusiness`
    -   Adres, telefon, koordinatlar, uzmanlık alanları, çalışma saatleri
    -   `sameAs` ile sosyal medya profilleri bağlantısı
    -   Bu şablon `baseof.html` içinde `<head>` bölümüne dahil edilmeli
-   **Meta Tags:** Her sayfada doğru `description` ve `keywords` ekleyin
-   **OG Tags:** Sosyal medya paylaşımı için Open Graph tags
-   **GA4:** Google Analytics 4 tracking code'u `params.toml`'de ayarlayın
-   **Favicon:** `static/favicon.ico` ekleyin (multi-size: 16x16, 32x32, 180x180)

---

## 7. Çoklu Dil Menüleri (i18n Menus)

`4-Çoklu-Dil.md`'de detaylı anlatılmıştır:

**Yapılacaklar:**

-   `config/_default/menus.toml` dosyasında TR ve EN menülerini ayrı ayrı tanımlayın
    -   TR Menü: "Ana Sayfa", "Hakkımda", "Kliniğim", "Yayınlar", "Blog", "İletişim"
    -   EN Menu: "Home", "About", "Clinic", "Publications", "Blog", "Contact"
-   Dil değiştirme butonu (`/tr/` ↔ `/en/`) tema başlığında otomatik görünür
-   Her sayfanın TR/EN versiyonu content klasörüne ayrı ayrı olmalıdır

---

## 8. Sürekli Lokal Test

`hugo server` komutunu kullanarak yaptığınız değişiklikleri anlık olarak yerel bilgisayarınızda test edin.

**Performans Hedefleri** (`1-Araştırma.md` referansıyla):

-   **Google PageSpeed:** 95-100 puan (hedef)
-   **SEO Skoru:** 90+ puan
-   **Core Web Vitals:**
    -   LCP (Largest Contentful Paint): < 2.5s
    -   FID (First Input Delay): < 100ms
    -   CLS (Cumulative Layout Shift): < 0.1

**Test Kontrol Listesi:**

-   ✅ Sayfa yüklenme hızı (Lighthouse'ta en az 95+ puan - hedef)
-   ✅ Mobil uyumluluğu (Telefonda menüler/butonlar düzgün mi?)
-   ✅ Çoklu dil çalışması (TR ↔ EN geçişi sorunsuz mu?)
-   ✅ Form gönderimi (Netlify Forms test edition)
-   ✅ İç linkler (404 yok mu?)
-   ✅ WhatsApp butonu (Doğru numara, açılıyor mu?)
-   ✅ Responsive tasarım (Tablet, telefon, masaüstü)
-   ✅ Schema doğrulama (Google Rich Results Test)
-   ✅ Erişilebilirlik (WCAG 2.1 AA uyumu)

---

## 9. Netlify Deployment Hazırlığı

Site tamamlandığında, `netlify.toml` konfigürasyonunu yapın ve canlıya alın.

**Yapılacaklar:**

-   Proje root'una `netlify.toml` ekleyin:

    ```toml
    [build]
      command = "hugo --gc --minify"
      publish = "public"

    [build.environment]
      HUGO_VERSION = "0.128.0"  # veya mevcut versiyon
      HUGO_ENV = "production"
      HUGO_ENABLEGITINFO = "true"

    # Güvenlik ve Performans Başlıkları
    [[headers]]
      for = "/*"
      [headers.values]
        Cache-Control = "public, max-age=31536000, immutable"
        X-Frame-Options = "DENY"
        X-Content-Type-Options = "nosniff"
        X-XSS-Protection = "1; mode=block"
        Referrer-Policy = "strict-origin-when-cross-origin"

    # Statik dosyalar için uzun cache
    [[headers]]
      for = "/css/*"
      [headers.values]
        Cache-Control = "public, max-age=31536000, immutable"

    [[headers]]
      for = "/js/*"
      [headers.values]
        Cache-Control = "public, max-age=31536000, immutable"

    [[headers]]
      for = "/images/*"
      [headers.values]
        Cache-Control = "public, max-age=31536000, immutable"
    ```

-   GitHub repo'yu Netlify'a bağlayın (portwebdesign/dr-cil)
-   Custom domain ayarı: `drhabibcil.com` (veya hedef domain)
-   SSL sertifikası otomatik uygulanacaktır (Netlify sağlıyor)
-   **Redirect kuralları:** www → non-www veya tersi için ayar yapın

---

## 10. Post-Launch İzleme ve Bakım

Siteyi yayına aldıktan sonra:

**Yapılacaklar:**

-   Google Search Console'da site doğrulaması yap
-   Bing Webmaster Tools'a submit et
-   Analytics 4'te hedef ayarları yapılandır (randevu butonuna tıklamalar, form gönderimler vb.)
-   Email bildirimleri test et (Netlify Form submissions)
-   Ayda bir SEO denetimi yap (arama terimleri, sıralama)

---

## 11. Son Kontrol Listesi (Pre-Launch)

Siteyi yayına almadan önce tüm maddelen­lerin tamamlandığını doğrulayın:

| Madde                                                                             | Durum |
| --------------------------------------------------------------------------------- | ----- |
| **Teknik**                                                                        |       |
| Hugo yapısı tamamlandı                                                            | ⬜    |
| Blowfish tema çalışır durumda                                                     | ⬜    |
| Config dosyaları (config.toml, params.toml, languages.toml, menus.toml) ayarlandı | ⬜    |
| İçerik (TR + EN) eklenmiş                                                         | ⬜    |
| **SEO & Metadata**                                                                |       |
| Physician Schema (JSON-LD) eklendi                                                | ⬜    |
| Meta descriptions tüm sayfalarda var                                              | ⬜    |
| OG tags ayarlandı                                                                 | ⬜    |
| Google Analytics 4 entegre                                                        | ⬜    |
| Favicon ve logo eklendi                                                           | ⬜    |
| **Yasal & UX**                                                                    |       |
| Footer yasal uyarı metni                                                          | ⬜    |
| WhatsApp butonu (sabit, mobil)                                                    | ⬜    |
| Netlify Forms entegrasyonu                                                        | ⬜    |
| robots.txt ve sitemap kontrol                                                     | ⬜    |
| KVKK / Gizlilik Politikası sayfası                                                | ⬜    |
| Özel 404 sayfası                                                                  | ⬜    |
| **Performans**                                                                    |       |
| Lighthouse 95+ (hedef)                                                            | ⬜    |
| PageSpeed Insights mobil ✓                                                        | ⬜    |
| Core Web Vitals iyileştirildi                                                     | ⬜    |
| WebP görsel optimizasyonu                                                         | ⬜    |
| **Güvenlik**                                                                      |       |
| Security headers (netlify.toml)                                                   | ⬜    |
| Cache headers yapılandırıldı                                                      | ⬜    |
| **Deployment**                                                                    |       |
| netlify.toml oluşturuldu                                                          | ⬜    |
| GitHub'a push edildi                                                              | ⬜    |
| Netlify deploy edildi                                                             | ⬜    |
| Custom domain ayarlandı                                                           | ⬜    |
| SSL aktif                                                                         | ⬜    |

---

## 12. Tahmini Zaman Çizelgesi

| Faz                           | Süre    | Öncelik   |
| ----------------------------- | ------- | --------- |
| 1. Projenin Başlatılması      | 1 gün   | 🔴 Yüksek |
| 2. Versiyon Kontrolü          | 0.5 gün | 🔴 Yüksek |
| 3. İçerik Yapısı              | 3-5 gün | 🔴 Yüksek |
| 4. Ekstra Özellikler          | 2-3 gün | 🔴 Yüksek |
| 5. Görsel Özelleştirme        | 2 gün   | 🟡 Orta   |
| 5.5 Görsel Optimizasyon       | 1 gün   | 🟡 Orta   |
| 6. SEO ve Teknik Optimizasyon | 2 gün   | 🔴 Yüksek |
| 7. Çoklu Dil Menüleri         | 1 gün   | 🟡 Orta   |
| 8. Test ve Performans         | 2 gün   | 🔴 Yüksek |
| 9. Netlify Deployment         | 1 gün   | 🔴 Yüksek |
| 10. Post-Launch İzleme        | Sürekli | 🟢 Düşük  |

**Toplam Tahmini Süre:** 2-3 hafta (içerik hazırlığı hariç)

---

## Özet

Bu yol haritasını **sırasıyla** takip ederek, mevcut mükemmel planınızı sorunsuz bir şekilde çalışan, hızlı, SEO-uyumlu, yasal zorunlulukları yerine getiren ve Türkiye'de hekim siteleri için standart olan bir web sitesine dönüştürebilirsiniz.

**Tahmini Zaman:** 2-3 hafta (içerik hazırlığı hariç)
**Zorluk Derecesi:** Orta (teknik bilgisi olan biri için uygulanabilir)
**Nihai Hedef:** Doç. Dr. Habib ÇİL için güvenilir, hızlı, hasta ve akademisyen çeken profesyonel bir dijital kimlik

---

## 📝 Değişiklik Geçmişi

| Tarih      | Değişiklik                                                                |
| ---------- | ------------------------------------------------------------------------- |
| 2025-12-02 | Görsel Optimizasyon bölümü (5.5) eklendi                                  |
| 2025-12-02 | Netlify güvenlik ve cache başlıkları detaylandırıldı                      |
| 2025-12-02 | KVKK uyumluluk ve 404 sayfası gereksinimleri eklendi                      |
| 2025-12-02 | Performans hedefleri güncellendi (95-100 PageSpeed, Core Web Vitals)      |
| 2025-12-02 | Physician Schema doğru implementasyon yöntemi (JSON-LD partial) açıklandı |
| 2025-12-02 | Zaman çizelgesi ve öncelik tablosu eklendi                                |
| 2025-12-02 | Son kontrol listesine güvenlik ve eksik maddeler eklendi                  |
