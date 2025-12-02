Aşağıda **Hugo + Blowfish teması ile tam çoklu dil (i18n) desteği** eklemenin bütün yollarını _basit, adım adım ve çalışır örneklerle_ bulacaksın.

---

# 🌍 **Hugo’da Çoklu Dil Desteği Nasıl Eklenir?** (Blowfish Uyumlu)

Hugo’da çoklu dil desteği 3 temel adımda yapılır:

1. **languages.toml** oluşturmak
2. İçerikleri dil klasörlerine ayırmak
3. Menü ve tema parametrelerini dillere göre uyarlamak

Aşağıda Blowfish ile **tam çalışan bir örnek yapı** vereceğim.

---

# ✅ **1. `config/_default/languages.toml` Dosyasını Oluştur**

Bu dosya tüm dilleri tanımlar.

### **Örnek: Türkçe + İngilizce**

```toml
# --------------------------------------------------------
# LANGUAGES CONFIG — Hugo + Blowfish
# --------------------------------------------------------

defaultContentLanguage = "tr"
defaultContentLanguageInSubdir = true

[languages]

  [languages.tr]
    languageName = "Türkçe"
    weight = 1
    title = "Benim Blogum"
    languageCode = "tr"
    contentDir = "content/tr"
    hasCJKLanguage = false

  [languages.en]
    languageName = "English"
    weight = 2
    title = "My Blog"
    languageCode = "en"
    contentDir = "content/en"
    hasCJKLanguage = false
```

📌 **Önemli Not:**
`defaultContentLanguageInSubdir = true` olunca URL’ler şöyle olur:

-   Türkçe → `https://site.com/tr/`
-   İngilizce → `https://site.com/en/`

Böylece iki dil tamamen izole çalışır.

---

# ✅ **2. Content Dizini Çoklu Dile Göre Ayrılır**

```
content/
├── tr/
│   ├── _index.md
│   ├── posts/
│   │   └── ilk-yazi.md
│   └── pages/
│       └── hakkimda.md
├── en/
│   ├── _index.md
│   ├── posts/
│   │   └── first-post.md
│   └── pages/
│       └── about.md
```

---

# ✅ **3. Menüleri Dillere Göre Ayır (`menus.toml`)**

Hugo’da menüleri dil bazlı yapmak için:

### **`config/_default/menus.toml`**

```toml
# Menü — Türkçe
[languages.tr.menu]

  [[languages.tr.menu.main]]
  name = "Ana Sayfa"
  url  = "/tr/"
  weight = 1

  [[languages.tr.menu.main]]
  name = "Yazılar"
  url  = "/tr/posts/"
  weight = 2

  [[languages.tr.menu.main]]
  name = "Hakkımda"
  url  = "/tr/pages/hakkimda/"
  weight = 3


# Menü — English
[languages.en.menu]

  [[languages.en.menu.main]]
  name = "Home"
  url  = "/en/"
  weight = 1

  [[languages.en.menu.main]]
  name = "Posts"
  url  = "/en/posts/"
  weight = 2

  [[languages.en.menu.main]]
  name = "About"
  url  = "/en/pages/about/"
  weight = 3
```

Blowfish menüyü otomatik olarak dillere göre değiştirir.

---

# ✅ **4. Blowfish Tema Ayarlarını (params) Dillere Göre Ayırma**

### **`config/_default/params.toml`**

Her dil için ayrı parametre girebilirsiniz:

```toml
# Türkçe
[languages.tr.params]
  description = "Blowfish temalı Türkçe blog"
  defaultAppearance = "light"

# English
[languages.en.params]
  description = "Blowfish themed English blog"
  defaultAppearance = "light"
```

---

# ✅ **5. URL Yapısının Doğru Çalışıp Çalışmadığını Test Et**

```
hugo server -D
```

Aç:

-   [http://localhost:1313/tr/](http://localhost:1313/tr/)
-   [http://localhost:1313/en/](http://localhost:1313/en/)

Her dilin hem menüsü hem başlığı hem de içerikleri **ayrı çalışıyor** olmalı.

---

# 🇹🇷🇬🇧 **6. Çoklu Dilde Ana Sayfa İçeriği**

### `content/tr/_index.md`

```md
---
title: "Hoşgeldiniz"
---

Bu sitenin Türkçe ana sayfasıdır.
```

### `content/en/_index.md`

```md
---
title: "Welcome"
---

This is the English homepage.
```

---

# 🔥 **7. Blowfish’in Dil Değiştirici (Language Switcher) Özelliği**

Blowfish teması otomatik olarak dil değiştirici ekler.

Hiçbir ek ayar gerekmez.

Üst menüde sağda → 🌐 **Dil seçici** görünür.

---

# 🎁 **İstersen Sana Şunları da Hazırlayabilirim**

✔ Tam çalışan **2 dilli hızlı başlangıç Hugo Blowfish projesi (zip)**
✔ Her dil için **otomatik hero section**
✔ Çok dilli SEO meta ayarları
✔ Çok dilli blog taxonomileri (tags, categories)
✔ Menüde otomatik **dil bayrak ikonları eklenti**

İstersen bir **Türkçe–İngilizce hazır demo** oluşturayım mı?
