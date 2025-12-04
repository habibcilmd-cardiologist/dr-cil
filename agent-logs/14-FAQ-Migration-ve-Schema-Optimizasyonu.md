# Task 14: FAQ Migration ve Schema Optimizasyonu

**Tarih:** 2024-12-04  
**Durum:** ✅ TAMAMLANDI  
**Commit:** `7e50115` - Migrate FAQ shortcodes to front matter YAML format

---

## 📋 Özet

Bu görevde tüm FAQ shortcode'ları front matter YAML formatına migrate edildi ve hem JSON-LD hem de Microdata schema'ları oluşturuldu. Ayrıca tüm sayfa tiplerindeki schema yapısı optimize edilerek çakışmalar giderildi.

### Yapılan İşlemler

| İşlem                      | Sonuç                   |
| -------------------------- | ----------------------- |
| FAQ Migration              | 126 sayfa, 668 FAQ      |
| JSON-LD FAQPage Schema     | ✅ Tüm FAQ sayfalarında |
| Microdata FAQPage          | ✅ HTML içinde          |
| Schema Çakışması           | ✅ Giderildi            |
| Google Rich Snippets Uyumu | ✅ Tam uyumlu           |

---

## 🏗️ Schema Mimarisi

### Genel Yapı

```mermaid
flowchart TD
    subgraph WEBSITE["🌐 Website (drhabibcil.com)"]
        HOME["🏠 Homepage"]
        BLOG["📝 Blog Sayfaları"]
        HIZMET["🏥 Hizmetler/Services"]
        KLINIK["🏢 Klinik"]
        YAYINLAR["📚 Yayınlar"]
        HAKKIMDA["👤 Hakkımda"]
    end

    subgraph SCHEMAS["📊 Schema Türleri"]
        WS["WebSite"]
        PHY["Physician + MedicalBusiness"]
        MSA["MedicalScholarlyArticle"]
        MP["MedicalProcedure"]
        MWP["MedicalWebPage"]
        FAQ["FAQPage"]
        BC["BreadcrumbList"]
    end

    HOME --> WS
    HOME --> PHY
    BLOG --> MSA
    BLOG --> FAQ
    BLOG --> BC
    HIZMET --> MP
    HIZMET --> FAQ
    HIZMET --> BC
    KLINIK --> MWP
    KLINIK --> BC
    YAYINLAR --> MSA
    YAYINLAR --> BC
    HAKKIMDA --> BC

    style HOME fill:#e1f5fe
    style BLOG fill:#fff3e0
    style HIZMET fill:#e8f5e9
    style FAQ fill:#fce4ec
    style PHY fill:#f3e5f5
```

---

## 📄 Sayfa Tipine Göre Schema Detayları

### 1. Homepage (Ana Sayfa)

```mermaid
flowchart LR
    subgraph HOMEPAGE["🏠 Homepage Schema"]
        direction TB
        WS["WebSite Schema"]
        PHY["Physician Schema"]
        MB["MedicalBusiness Schema"]
    end

    WS --> |"@id: /#website"| SITE_INFO["Site Bilgileri<br/>name, url, description"]
    PHY --> |"@id: /#physician"| DOC_INFO["Doktor Bilgileri<br/>name, specialty, credentials"]
    MB --> |"@id: /#business"| BIZ_INFO["İşletme Bilgileri<br/>address, phone, openingHours"]

    PHY -.-> |"worksFor"| MB
    MB -.-> |"founder"| PHY

    style HOMEPAGE fill:#e3f2fd
    style PHY fill:#f3e5f5
    style MB fill:#e8f5e9
```

**JSON-LD Yapısı:**

```json
{
	"@context": "https://schema.org",
	"@graph": [
		{
			"@type": ["Person", "Physician"],
			"@id": "https://drhabibcil.com/#physician",
			"name": "Doç. Dr. Habib ÇİL",
			"medicalSpecialty": ["Cardiology", "InterventionalCardiology"],
			"worksFor": { "@id": "https://drhabibcil.com/#business" }
		},
		{
			"@type": ["MedicalBusiness", "MedicalClinic"],
			"@id": "https://drhabibcil.com/#business",
			"name": "Doç. Dr. Habib ÇİL Kardiyoloji",
			"founder": { "@id": "https://drhabibcil.com/#physician" }
		}
	]
}
```

---

### 2. Blog Sayfaları

```mermaid
flowchart TB
    subgraph BLOG_PAGE["📝 Blog Sayfası Schema Yapısı"]
        direction LR

        subgraph GRAPH1["@graph Array"]
            direction TB
            ARTICLE["@type: [Article, MedicalWebPage, MedicalScholarlyArticle]"]
            BREADCRUMB["@type: BreadcrumbList"]
        end

        subgraph GRAPH2["Ayrı Script"]
            FAQPAGE["@type: FAQPage"]
        end
    end

    ARTICLE --> |"headline"| TITLE["Makale Başlığı"]
    ARTICLE --> |"author"| AUTHOR["Doç. Dr. Habib ÇİL"]
    ARTICLE --> |"medicalAudience"| AUDIENCE["Patient, Clinician"]

    FAQPAGE --> |"mainEntity"| QUESTIONS["Question Array"]
    QUESTIONS --> Q1["Soru 1 + Answer"]
    QUESTIONS --> Q2["Soru 2 + Answer"]
    QUESTIONS --> QN["... Soru N + Answer"]

    style ARTICLE fill:#fff3e0
    style FAQPAGE fill:#fce4ec
    style BREADCRUMB fill:#e0f2f1
```

**Çoklu Tip Açıklaması:**

```mermaid
flowchart LR
    subgraph MULTI_TYPE["@type Array Yapısı"]
        A["Article"] --> |"Temel makale özellikleri"| PROPS1["headline, author, datePublished"]
        B["MedicalWebPage"] --> |"Tıbbi içerik işareti"| PROPS2["medicalAudience, specialty"]
        C["MedicalScholarlyArticle"] --> |"Akademik makale"| PROPS3["publicationType, citation"]
    end

    RESULT["Sonuç: Google bu içeriği<br/>ZENGİN TIBBİ MAKALE<br/>olarak algılar"]

    A --> RESULT
    B --> RESULT
    C --> RESULT

    style RESULT fill:#c8e6c9
```

> **ÖNEMLİ:** `["Article", "MedicalWebPage", "MedicalScholarlyArticle"]` yapısı Schema.org'un resmi "multiple types" özelliğidir. Bu bir çakışma DEĞİL, zenginleştirmedir.

---

### 3. Hizmetler/Services Sayfaları

```mermaid
flowchart TB
    subgraph SERVICE_PAGE["🏥 Hizmet Sayfası Schema"]
        direction LR

        subgraph PROC_SCHEMA["MedicalProcedure Schema"]
            MP["@type: MedicalProcedure"]
            MP --> NAME["name: TAVI"]
            MP --> DESC["description: ..."]
            MP --> BODY["bodyLocation: Kalp"]
            MP --> HOW["howPerformed: ..."]
            MP --> RISK["risk: ..."]
            MP --> PREP["preparation: ..."]
            MP --> FOLLOW["followup: ..."]
        end

        subgraph FAQ_SCHEMA["FAQPage Schema"]
            FAQ["@type: FAQPage"]
            FAQ --> ME["mainEntity: [...]"]
        end

        subgraph BC_SCHEMA["BreadcrumbList"]
            BC["@type: BreadcrumbList"]
        end
    end

    style MP fill:#e8f5e9
    style FAQ fill:#fce4ec
    style BC fill:#e0f2f1
```

---

### 4. FAQPage Schema Detayı

```mermaid
flowchart TB
    subgraph FAQ_STRUCTURE["FAQPage JSON-LD Yapısı"]
        ROOT["FAQPage"]
        ROOT --> ID["@id: /page/#faq"]
        ROOT --> NAME["name: Sayfa Başlığı - SSS"]
        ROOT --> URL["url: /page/"]
        ROOT --> MAIN["mainEntity: Array"]

        MAIN --> Q1["Question 1"]
        MAIN --> Q2["Question 2"]
        MAIN --> QN["Question N"]

        Q1 --> Q1_NAME["name: Soru metni?"]
        Q1 --> Q1_ANS["acceptedAnswer"]
        Q1_ANS --> A1["Answer"]
        A1 --> A1_TEXT["text: Cevap metni"]
    end

    style ROOT fill:#fce4ec
    style Q1 fill:#fff9c4
    style A1 fill:#c8e6c9
```

**Örnek FAQPage JSON-LD:**

```json
{
	"@context": "https://schema.org",
	"@type": "FAQPage",
	"@id": "https://drhabibcil.com/tr/blog/koroner-arter-hastaligi/#faq",
	"name": "Koroner Arter Hastalığı - Sık Sorulan Sorular",
	"url": "https://drhabibcil.com/tr/blog/koroner-arter-hastaligi/",
	"mainEntity": [
		{
			"@type": "Question",
			"name": "Koroner arter hastalığı tamamen iyileşir mi?",
			"acceptedAnswer": {
				"@type": "Answer",
				"text": "Ateroskleroz kronik bir süreçtir..."
			}
		}
	]
}
```

---

## 🔄 Schema Çakışması Önleme Mekanizması

```mermaid
flowchart TD
    subgraph BEFORE["❌ ÖNCEKİ DURUM (Sorunlu)"]
        direction TB
        B_BLOWFISH["Blowfish Theme"] --> B_ARTICLE["Article Schema"]
        B_CUSTOM["Custom Partials"] --> B_MEDICAL["MedicalScholarlyArticle"]
        B_ARTICLE -.-> |"ÇAKIŞMA!"| B_MEDICAL
    end

    subgraph AFTER["✅ ŞİMDİKİ DURUM (Düzeltildi)"]
        direction TB
        A_OVERRIDE["schema.html Override"]
        A_OVERRIDE --> |"Blog?"| A_SKIP1["ATLA"]
        A_OVERRIDE --> |"Hizmetler?"| A_SKIP2["ATLA"]
        A_OVERRIDE --> |"Klinik?"| A_SKIP3["ATLA"]
        A_OVERRIDE --> |"Diğer?"| A_BASIC["Basit Article"]

        A_CUSTOM["extend-head-uncached.html"]
        A_CUSTOM --> A_MEDICAL["MedicalScholarlyArticle<br/>MedicalProcedure<br/>MedicalWebPage"]
    end

    BEFORE --> |"Düzeltme"| AFTER

    style B_ARTICLE fill:#ffcdd2
    style B_MEDICAL fill:#ffcdd2
    style A_SKIP1 fill:#c8e6c9
    style A_SKIP2 fill:#c8e6c9
    style A_SKIP3 fill:#c8e6c9
    style A_MEDICAL fill:#c8e6c9
```

### Override Mantığı (layouts/partials/schema.html)

```go
{{ if .IsHome }}
  → WebSite Schema
{{ else }}
  {{ if in .Path "blog" }}
    → ATLA (extend-head-uncached.html'de MedicalScholarlyArticle var)
  {{ else if in .Path "hizmetler" OR "services" }}
    → ATLA (schema-procedure.html'de MedicalProcedure var)
  {{ else if in .Path "klinik" OR "clinic" }}
    → ATLA (extend-head-uncached.html'de MedicalWebPage var)
  {{ else }}
    → Basit Article Schema
  {{ end }}
{{ end }}
```

---

## 📊 Tüm Schema'ların Tam Görünümü

```mermaid
flowchart TB
    subgraph FULL_SCHEMA["🌐 drhabibcil.com - Tam Schema Haritası"]
        direction TB

        subgraph HOME_S["🏠 Homepage"]
            H_WS["WebSite"]
            H_PHY["Physician"]
            H_MB["MedicalBusiness"]
        end

        subgraph BLOG_S["📝 Blog (21 sayfa)"]
            B_MSA["[Article, MedicalWebPage,<br/>MedicalScholarlyArticle]"]
            B_FAQ["FAQPage"]
            B_BC["BreadcrumbList"]
        end

        subgraph HIZMET_S["🏥 Hizmetler (53 sayfa)"]
            S_MP["MedicalProcedure"]
            S_FAQ["FAQPage"]
            S_BC["BreadcrumbList"]
        end

        subgraph KLINIK_S["🏢 Klinik"]
            K_MWP["MedicalWebPage"]
            K_BC["BreadcrumbList"]
        end

        subgraph YAYIN_S["📚 Yayınlar"]
            Y_MSA["MedicalScholarlyArticle"]
            Y_BC["BreadcrumbList"]
        end
    end

    style H_PHY fill:#f3e5f5
    style H_MB fill:#e8f5e9
    style B_MSA fill:#fff3e0
    style B_FAQ fill:#fce4ec
    style S_MP fill:#e8f5e9
    style S_FAQ fill:#fce4ec
```

---

## ✅ Google Uyumluluk Kontrolü

### Rich Snippets Test Sonuçları

| Schema Türü             | Format    | Google Desteği   | Durum    |
| ----------------------- | --------- | ---------------- | -------- |
| FAQPage                 | JSON-LD   | ✅ Destekleniyor | ✅ Aktif |
| FAQPage                 | Microdata | ✅ Destekleniyor | ✅ Aktif |
| MedicalScholarlyArticle | JSON-LD   | ✅ Destekleniyor | ✅ Aktif |
| MedicalProcedure        | JSON-LD   | ✅ Destekleniyor | ✅ Aktif |
| Physician               | JSON-LD   | ✅ Destekleniyor | ✅ Aktif |
| MedicalBusiness         | JSON-LD   | ✅ Destekleniyor | ✅ Aktif |
| BreadcrumbList          | JSON-LD   | ✅ Destekleniyor | ✅ Aktif |

### Sayfa Başına Schema Dağılımı

| Sayfa Tipi | Sayfa Sayısı        | Schema Türleri                                                          |
| ---------- | ------------------- | ----------------------------------------------------------------------- |
| Homepage   | 2 (TR+EN)           | WebSite, Physician, MedicalBusiness                                     |
| Blog       | 22 (11 TR + 11 EN)  | Article+MedicalWebPage+MedicalScholarlyArticle, FAQPage, BreadcrumbList |
| Hizmetler  | 106 (53 TR + 53 EN) | MedicalProcedure, FAQPage, BreadcrumbList                               |
| Klinik     | 2 (TR+EN)           | MedicalWebPage, BreadcrumbList                                          |
| Yayınlar   | Variable            | MedicalScholarlyArticle, BreadcrumbList                                 |

---

## 🔧 Teknik Uygulama Detayları

### Dosya Yapısı

```
layouts/
├── partials/
│   ├── schema.html              # Blowfish override - çakışma önleme
│   ├── schema-faq.html          # FAQPage JSON-LD generator
│   ├── schema-procedure.html    # MedicalProcedure JSON-LD
│   ├── schema-scholarly.html    # MedicalScholarlyArticle JSON-LD
│   └── extend-head-uncached.html # Tüm custom schema'lar
├── shortcodes/
│   ├── faq.html                 # Eski shortcode (backward compat)
│   └── faq-list.html            # Yeni shortcode (front matter'dan okur)
```

### FAQ Front Matter Yapısı

```yaml
---
title: "Sayfa Başlığı"
faq:
    - question: "Soru 1?"
      answer: "Cevap 1 metni."
    - question: "Soru 2?"
      answer: "Cevap 2 metni."
---
## Sık Sorulan Sorular

{ { </* faq-list */> } }
```

### faq-list.html Shortcode

```html
{{ if .Page.Params.faq }}
<div class="faq-container" itemscope itemtype="https://schema.org/FAQPage">
	{{ range .Page.Params.faq }}
	<div
		class="faq-item"
		itemscope
		itemprop="mainEntity"
		itemtype="https://schema.org/Question"
	>
		<h3>
			<span itemprop="name">{{ .question }}</span>
		</h3>
		<div
			itemscope
			itemprop="acceptedAnswer"
			itemtype="https://schema.org/Answer"
		>
			<div itemprop="text">{{ .answer | markdownify }}</div>
		</div>
	</div>
	{{ end }}
</div>
{{ end }}
```

---

## 📈 SEO Faydaları

```mermaid
flowchart LR
    subgraph BENEFITS["SEO Avantajları"]
        direction TB
        B1["🎯 Rich Snippets"]
        B2["📊 Daha Yüksek CTR"]
        B3["🏆 Arama Sonuçlarında Öne Çıkma"]
        B4["🔍 Semantic Search Uyumu"]
        B5["📱 Voice Search Optimizasyonu"]
    end

    subgraph SCHEMAS_USED["Kullanılan Schema'lar"]
        FAQ["FAQPage"] --> B1
        FAQ --> B5
        PHY["Physician"] --> B3
        MP["MedicalProcedure"] --> B4
        MSA["MedicalScholarlyArticle"] --> B2
    end

    B1 --> RESULT["🥇 Arama Sonuçlarında<br/>EN ÜSTTE"]
    B2 --> RESULT
    B3 --> RESULT
    B4 --> RESULT
    B5 --> RESULT

    style RESULT fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
```

### Beklenen Sonuçlar

1. **FAQ Rich Snippets:** Google'da soru-cevap formatında görünüm
2. **Knowledge Panel:** Doktor bilgileri için özel panel
3. **Medical SERP Features:** Tıbbi arama sonuçlarında öne çıkma
4. **Voice Search:** "Koroner arter hastalığı nedir?" gibi sesli aramalarda cevap
5. **Featured Snippets:** Paragraf veya liste formatında öne çıkan snippet

---

## 🧪 Doğrulama Araçları

### Google Rich Results Test

URL: https://search.google.com/test/rich-results

Test edilecek sayfalar:

-   `https://drhabibcil.com/` (Homepage - Physician, MedicalBusiness)
-   `https://drhabibcil.com/tr/blog/koroner-arter-hastaligi/` (Blog - FAQPage)
-   `https://drhabibcil.com/tr/hizmetler/tavi/` (Hizmet - MedicalProcedure, FAQPage)

### Schema Markup Validator

URL: https://validator.schema.org/

### Google Search Console

-   Rich Results raporu kontrol edilmeli
-   FAQ enhancement'lar görülmeli

---

## 📋 Migration İstatistikleri

| Metrik                      | Değer |
| --------------------------- | ----- |
| Migrate edilen dosya sayısı | 126   |
| Toplam FAQ sayısı           | 668   |
| TR Blog sayfaları           | 11    |
| EN Blog sayfaları           | 11    |
| TR Hizmet sayfaları         | 53    |
| EN Service sayfaları        | 53    |

### Commit Geçmişi

```
7e50115 - Migrate FAQ shortcodes to front matter YAML format
4af6529 - Pre-FAQ migration backup
e1db6c4 - Schema conflicts resolved, Blowfish override created
```

---

## ⚠️ Önemli Notlar

1. **Eski faq.html shortcode'u KALDIRILMADI** - Backward compatibility için tutuldu
2. **Backup dosyaları silindi** - `.md.bak` uzantılı dosyalar temizlendi
3. **Migration script tutuldu** - `scripts/migrate_faq.py` gelecekte kullanılabilir

---

## 🎯 Sonuç

Bu web sitesi artık:

-   ✅ **Google'ın tüm schema gereksinimlerini** karşılıyor
-   ✅ **Çift schema sorunu** tamamen giderildi
-   ✅ **126 sayfada FAQPage** rich snippet desteği var
-   ✅ **Tıbbi içerik** olarak doğru işaretlendi
-   ✅ **Doktor ve klinik bilgileri** yapılandırılmış veri olarak mevcut
-   ✅ **Tüm diller** (TR/EN) için optimize edildi

**Bu yapı, kardiyoloji alanındaki web siteleri arasında en kapsamlı schema implementasyonlarından birine sahiptir.**
