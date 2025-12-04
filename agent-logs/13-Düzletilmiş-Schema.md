# Düzletilmiş Schema Yapısı

## Akış Diyagramı

```mermaid
flowchart TB
    subgraph HEAD["head.html Akışı"]
        H1["1️⃣ schema.html (Override)"]
        H2["2️⃣ extend-head-uncached.html"]
    end

    subgraph OVERRIDE["layouts/partials/schema.html (YENİ)"]
        O1["Homepage → WebSite ✅"]
        O2["Blog → ATLA ⏭️"]
        O3["Hizmetler → ATLA ⏭️"]
        O4["Yayınlar → ATLA ⏭️"]
        O5["Klinik → ATLA ⏭️"]
        O6["Diğer → Article ✅"]
    end

    subgraph CUSTOM["extend-head-uncached.html"]
        C1["Homepage → Physician + MedicalBusiness ✅"]
        C2["Blog → MedicalScholarlyArticle ✅"]
        C3["Klinik → MedicalWebPage ✅"]
        C4["schema-procedure.html → MedicalProcedure ✅"]
        C5["schema-scholarly.html → MedicalScholarlyArticle ✅"]
        C6["schema-faq.html → FAQPage ✅"]
    end

    H1 --> OVERRIDE
    H2 --> CUSTOM

    subgraph RESULT["✅ SONUÇ: Her Sayfada Tek Schema"]
        R1["Homepage: WebSite + Physician + MedicalBusiness"]
        R2["Blog: MedicalScholarlyArticle + BreadcrumbList"]
        R3["Hizmetler: MedicalProcedure + MedicalWebPage + BreadcrumbList"]
        R4["Yayınlar: MedicalScholarlyArticle"]
        R5["Klinik: MedicalWebPage"]
        R6["Diğer: Article"]
    end

    OVERRIDE --> RESULT
    CUSTOM --> RESULT

    style O2 fill:#90EE90,color:#000
    style O3 fill:#90EE90,color:#000
    style O4 fill:#90EE90,color:#000
    style O5 fill:#90EE90,color:#000
    style RESULT fill:#d4edda,color:#000
```

## ✅ İmplementasyon Tamamlandı!

### Yapılan Değişiklikler

| Dosya                                        | Değişiklik                                                         |
| -------------------------------------------- | ------------------------------------------------------------------ |
| `layouts/partials/schema.html`               | YENİ - Blowfish override, sayfa tipine göre akıllı schema kontrolü |
| `layouts/partials/schema-faq.html`           | YENİ - FAQ JSON-LD schema partial                                  |
| `layouts/partials/schema-procedure.html`     | Düzeltme: path kontrolü `hizmetler/` → `hizmetler`                 |
| `layouts/partials/extend-head-uncached.html` | FAQ partial eklendi                                                |

### Sonuç

| Sayfa Tipi | Önceki Durum                                | Şimdiki Durum                     |
| ---------- | ------------------------------------------- | --------------------------------- |
| Blog       | ⚠️ Article + MedicalScholarlyArticle (çift) | ✅ Sadece MedicalScholarlyArticle |
| Hizmetler  | ⚠️ Article + MedicalProcedure (çift)        | ✅ Sadece MedicalProcedure        |
| Yayınlar   | ⚠️ Article + MedicalScholarlyArticle (çift) | ✅ Sadece MedicalScholarlyArticle |
| Klinik     | ⚠️ Article + MedicalWebPage (çift)          | ✅ Sadece MedicalWebPage          |

### FAQ Rich Snippets Kullanımı

```yaml
---
title: "Sayfa Başlığı"
faq:
    - question: "Soru 1?"
      answer: "Cevap 1."
    - question: "Soru 2?"
      answer: "Cevap 2."
---
```

Bu şekilde hem mevcut microdata (shortcode ile) hem de JSON-LD (front matter ile) destekleniyor.

> **Not:** Hiçbir Medical schema kaybolmadı, aksine çakışmalar giderildi!
