Aşağıda **Hugo + Blowfish teması** için **tam, eksiksiz klasör yapısı**, **örnek config dosyası**, ayrıca başlangıç seviyesinde örnek içerikler bulunuyor.
Bu yapı **sıfırdan yeni bir Hugo site** oluşturduğunuzda doğrudan çalışır.

---

# ✅ **1. HUGO + Blowfish Tam Klasör Yapısı**

Blowfish bir **Hugo Extended** temasıdır ve klasik Hugo yapısını kullanır.
Aşağıdaki yapı temiz bir Blowfish projesinin tam dizin yapısını gösterir:

```
your-site/
├── archetypes/
│   └── default.md
│
├── assets/
│   └── (Blowfish özel SCSS, logo, font override dosyaları isteğe bağlı)
│
├── config/
│   ├── _default/
│   │   ├── config.toml       <-- Ana config
│   │   ├── params.toml       <-- Tema ayarları
│   │   ├── menus.toml        <-- Menü ayarları
│   │   └── languages.toml    <-- Çoklu dil ayarları (isteğe bağlı)
│
├── content/
│   ├── _index.md
│   ├── posts/
│   │   ├── _index.md
│   │   ├── first-post.md
│   │   └── second-post.md
│   ├── pages/
│   │   └── about.md
│   └── projects/
│       ├── _index.md
│       └── example-project.md
│
├── data/
│   └── (isteğe bağlı YAML/JSON/TOML veri dosyaları)
│
├── layouts/
│   └── (override edeceğiniz temaya ait özel şablonlar)
│
├── public/
│   └── (Hugo'nun build ettiği dosyalar – otomatik oluşur)
│
├── static/
│   ├── img/
│   │   └── logo.png
│   └── uploads/
│       └── example-image.jpg
│
├── themes/
│   └── blowfish/   <-- Git submodule ile çekilen tema
│
└── hugo.toml (opsiyonel, tüm config tek dosyada da olabilir)
```

---

# ✅ **2. Blowfish İçin Çalışır Örnek `config/_default/config.toml`**

Blowfish’in resmi dokümantasyonundaki tüm kritik ayarları içeren minimal–tam çalışan bir yapı:

```toml
baseURL = "https://example.com/"
title = "My Blowfish Site"
theme = "blowfish"
languageCode = "en-us"
paginate = 10
defaultContentLanguage = "en"
enableRobotsTXT = true
enableInlineShortcodes = true

[services]
  [services.disqus]
    shortname = ""

[markup]
  [markup.goldmark.renderer]
    unsafe = true

[outputs]
  home = ["HTML", "RSS", "JSON"]
```

---

# ✅ **3. `config/_default/params.toml` – Blowfish Tema Ayarları**

Blowfish temasının tüm görsel ve özellik ayarları burada olur:

```toml
# --------------------------------------------------------
# BLOWFISH TEMA PARAMETRELERİ
# --------------------------------------------------------

colorScheme = "auto"
defaultAppearance = "light"
enableSearch = true
enableCodeCopy = true
enableImageLazyLoading = true
enableBlogSections = true

description = "Modern, hızlı, şık bir Hugo Blowfish sitesi"

[author]
  name = "John Doe"
  image = "img/profile.jpg"
  headline = "Developer"
  bio = "Software Engineer & Writer"

[header]
  logo = "img/logo.png"
  showTitle = true
  layout = "fixed"
  showToggle = true

[footer]
  showCopyright = true
  showNavigation = true
  showSocial = true
  showThemeSwitcher = true

[social]
  twitter = "https://twitter.com/username"
  github = "https://github.com/username"
  linkedin = "https://linkedin.com/in/username"
```

---

# ✅ **4. `config/_default/menus.toml` – Menü Ayarları**

Blowfish oldukça esnek bir menü yapısı kullanır:

```toml
# MAIN MENU
[[main]]
name = "Home"
url = "/"
weight = 1

[[main]]
name = "Posts"
url = "/posts/"
weight = 2

[[main]]
name = "About"
url = "/pages/about/"
weight = 3

[[main]]
name = "Projects"
url = "/projects/"
weight = 4
```

---

# ✅ **5. Örnek İçerik Dosyaları**

### `content/_index.md`

```md
---
title: "Welcome"
description: "Blowfish Hugo Temasına Hoşgeldiniz"
---

Ana sayfa içerikleri temanın hero bölümü tarafından otomatik oluşturulur.
```

### `content/posts/first-post.md`

```md
---
title: "İlk Yazım"
date: 2025-01-01
draft: false
summary: "Bu Blowfish tema ile oluşturduğum ilk yazım."
tags: ["blog", "hugo", "blowfish"]
---

Merhaba! Bu Blowfish tema ile hazırlanmış ilk yazımdır.
```

---

# ✅ **6. Blowfish Temasını Kurma Komutu**

```bash
hugo new site mysite
cd mysite
git init
git submodule add https://github.com/nunocoracao/blowfish.git themes/blowfish
```

---

# Eğer istersen:

✔ Sana **zip şeklinde tam hazır proje çıkartayım**
✔ Menü + sayfa + post şablonları ile **boş değil tam demo site oluşturayım**
✔ Hugo içinde **çoklu dil desteği** ekleyeyim
✔ Blowfish’e özel **hero slider, callout, mermaid, katex, codeblock** örnekleri ekleyeyim

Hangisini istersin?
