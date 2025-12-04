# SEO Talimatları ve İçerik Yazım Rehberi

**Tarih:** 2024-12-04  
**Versiyon:** 1.0  
**Amaç:** Hizmet, Blog ve FAQ içeriklerinin SEO optimizasyonu için standart kurallar

---

## 📋 İçindekiler

1. [Hizmet Sayfaları (MedicalProcedure)](#1-hizmet-sayfaları)
2. [Blog Yazıları (MedicalScholarlyArticle)](#2-blog-yazıları)
3. [FAQ Yazım Kuralları (FAQPage)](#3-faq-yazım-kuralları)
4. [Genel SEO Kuralları](#4-genel-seo-kuralları)
5. [Anahtar Kelime Stratejisi](#5-anahtar-kelime-stratejisi)
6. [İç ve Dış Bağlantılar](#6-iç-ve-dış-bağlantılar)

---

## 1. Hizmet Sayfaları

### Schema: `MedicalProcedure`

Hizmet sayfaları Google'a "Bu sayfa tıbbi bir prosedürü anlatıyor" mesajı verir.

### Front Matter Şablonu

```yaml
---
title: "İşlem Adı - Tam Açıklama"
description: "İstanbul'da [işlem adı]. Doç. Dr. Habib Çil ile [fayda]. [Hedef kitle] için [avantaj]. [Lokasyon]'da uzman [uzmanlık alanı]."
date: 2024-XX-XX
lastmod: 2024-XX-XX
draft: false
service_type: "MedicalProcedure"
medical_specialty: "Cardiology"
procedure_type: "PercutaneousProcedure"  # veya DiagnosticProcedure, SurgicalProcedure
body_location: "Heart"  # veya Leg, Carotid, Kidney vb.
translationKey: "islem-ingilizce-key"
showBreadcrumbs: true
showTableOfContents: true
showReadingTime: true
faq:
    - question: "Soru 1?"
      answer: "Cevap 1."
    - question: "Soru 2?"
      answer: "Cevap 2."
---
```

### Title Yazım Kuralları

| Kural | Örnek |
|-------|-------|
| Ana anahtar kelime başta | ✅ "TAVI - Transkateter Aort Kapak İmplantasyonu" |
| 50-60 karakter ideal | ✅ "Koroner Anjiyografi: İşlem, Hazırlık ve Sonrası" |
| Marka/isim sonda | ✅ "Stent Nedir? \| Doç. Dr. Habib Çil" |
| Çok uzun başlıktan kaçın | ❌ "TAVI Transkateter Aort Kapak İmplantasyonu Ameliyatsız..." |

### Description Yazım Formülü

```
[Lokasyon]'da [işlem adı]. [Doktor adı] ile [ana fayda]. [Hedef kitle] için [avantaj]. [Hastane adı]'nda uzman [uzmanlık].
```

**Örnek:**
```
İstanbul'da TAVI işlemi. Doç. Dr. Habib Çil ile ameliyatsız aort kapak değişimi. Yüksek riskli hastalarda güvenli tedavi. Avrasya Hospital'da girişimsel kardiyoloji.
```

| Kural | Açıklama |
|-------|----------|
| 150-160 karakter | Google snippet'te tam görünür |
| Anahtar kelime ilk 60 karakterde | SEO önceliği |
| CTA içersin | "Randevu alın", "Bilgi edinin" |
| Unique olmalı | Her sayfa farklı description |

### İçerik Yapısı

```markdown
# Ana Başlık (H1 - title ile aynı olabilir)

[1-2 paragraf giriş - hastalık/prosedür tanımı, önem]

## [İşlem/Hastalık] Nedir? (H2)
[Tanım, tarihçe, genel bilgi]

## Belirtileri / Endikasyonları (H2)
- Madde listesi
- Hastanın anlayacağı dilde

## [İşlem] Kimlere Uygulanır? (H2)
### Uygun Hastalar (H3)
### Uygun Olmayan Durumlar (H3)

## [İşlem] Nasıl Yapılır? (H2)
### İşlem Öncesi Hazırlık (H3)
### İşlem Aşamaları (H3)
### İşlem Sonrası Bakım (H3)

## Riskler ve Komplikasyonlar (H2)
[Şeffaf ve güven veren anlatım]

## Avantajları (H2)
- Neden bu işlem tercih edilmeli?

## Sık Sorulan Sorular

{{</* faq-list */>}}

## Sonuç / Özet (H2)
[CTA - "Randevu almak için..."]
```

### Procedure Type Değerleri

| procedure_type | Kullanım |
|----------------|----------|
| `PercutaneousProcedure` | Kateter, stent, anjiyografi |
| `DiagnosticProcedure` | EKO, Holter, efor testi |
| `SurgicalProcedure` | By-pass, açık kalp |
| `TherapeuticProcedure` | Ablasyon, kardiyoversiyon |

### Body Location Değerleri

| body_location | İşlem Örnekleri |
|---------------|-----------------|
| `Heart` | TAVI, koroner stent, ablasyon |
| `Leg` | Periferik arter, diyabetik ayak |
| `Carotid` | Karotis stent |
| `Kidney` | Renal arter stent |
| `Chest` | Aort anevrizma |

---

## 2. Blog Yazıları

### Schema: `MedicalScholarlyArticle`

Blog yazıları Google'a "Bu sayfa akademik düzeyde tıbbi içerik" mesajı verir.

### Front Matter Şablonu

```yaml
---
title: "Ana Konu: Alt Başlık veya Detay"
description: "[Konu] nedir? [Alt konular] hakkında detaylı bilgi. [Hedef kitle] için kapsamlı rehber."
date: 2024-XX-XX
lastmod: 2024-XX-XX
translationKey: "konu-ingilizce-key"
categories: ["Kardiyoloji"]
tags:
    [
        "ana anahtar kelime",
        "ilgili kelime 1",
        "ilgili kelime 2",
        "uzun kuyruk anahtar kelime",
    ]
author: "Doç. Dr. Habib ÇİL"
showTableOfContents: true
featured: "featured.svg"
faq:
    - question: "Soru 1?"
      answer: "Cevap 1."
---
```

### Blog Title Formülleri

| Formül | Örnek |
|--------|-------|
| **Soru Formatı** | "Koroner Arter Hastalığı Nedir? Nedenleri ve Tedavisi" |
| **Liste Formatı** | "Kalp Sağlığı İçin 10 Altın Kural" |
| **Kapsamlı Rehber** | "Atriyal Fibrilasyon: Eksiksiz Hasta Rehberi" |
| **Karşılaştırma** | "Stent mi By-pass mı? Hangisi Daha İyi?" |
| **Problem-Çözüm** | "Çarpıntı Problemi ve Etkili Tedavi Yöntemleri" |

### Tags Stratejisi

```yaml
tags:
    [
        "koroner arter hastalığı",      # Ana anahtar kelime
        "ateroskleroz",                  # Tıbbi terim
        "anjina pektoris",               # İlgili belirti
        "stent",                         # Tedavi yöntemi
        "kalp krizi belirtileri",        # Long-tail anahtar kelime
    ]
```

| Kural | Açıklama |
|-------|----------|
| 4-7 tag ideal | Çok fazla tag SEO'yu zayıflatır |
| İlk tag en önemli | Ana anahtar kelime olmalı |
| Long-tail ekle | "koroner stent sonrası bakım" gibi |
| Tutarlı ol | Aynı konularda aynı tag'leri kullan |

### Blog İçerik Yapısı

```markdown
{{</* lead */>}}
[2-3 cümle çarpıcı giriş - okuyucunun dikkatini çek]
{{</* /lead */>}}

## [Konu] Nedir? (H2)
[Temel tanım, önem, yaygınlık]

### Alt Konu 1 (H3)
### Alt Konu 2 (H3)

## Nedenleri ve Risk Faktörleri (H2)
### Değiştirilemez Faktörler (H3)
### Değiştirilebilir Faktörler (H3)

## Belirtileri (H2)
[Liste formatında, hastanın anlayacağı dilde]

## Tanı Yöntemleri (H2)
[Hangi testler yapılır?]

## Tedavi Seçenekleri (H2)
### İlaç Tedavisi (H3)
### Girişimsel Tedavi (H3)
### Cerrahi Tedavi (H3)

## Korunma Yolları (H2)
[Yaşam tarzı önerileri]

## Sık Sorulan Sorular

{{</* faq-list */>}}

## Sonuç (H2)
[Özet ve CTA]
```

### İçerik Uzunluğu Önerileri

| İçerik Tipi | Minimum | İdeal | Maximum |
|-------------|---------|-------|---------|
| Blog yazısı | 1500 kelime | 2500-3500 kelime | 5000 kelime |
| Hizmet sayfası | 800 kelime | 1500-2000 kelime | 3000 kelime |
| FAQ cevabı | 50 kelime | 100-200 kelime | 300 kelime |

---

## 3. FAQ Yazım Kuralları

### Schema: `FAQPage`

FAQ'lar Google arama sonuçlarında **genişletilmiş snippet** olarak görünür.

### Front Matter FAQ Yapısı

```yaml
faq:
    - question: "Soru tam ve açık olmalı?"
      answer: "Cevap 100-200 kelime arasında, bilgilendirici ve güven verici olmalı."
    - question: "Bir başka soru?"
      answer: "Bir başka cevap."
```

### FAQ Soru Yazım Kuralları

| Kural | ✅ Doğru | ❌ Yanlış |
|-------|----------|-----------|
| Soru işareti ile bitir | "TAVI ameliyat mı?" | "TAVI ameliyat mı" |
| Kısa ve net | "Stent sonrası ilaç?" | "Stent sonrası hangi ilaçları ne kadar süre kullanmam gerekir acaba?" |
| Anahtar kelime içer | "Koroner anjiyografi ağrılı mı?" | "Bu işlem ağrılı mı?" |
| Hastanın soracağı gibi | "İşlem sonrası araba kullanabilir miyim?" | "Postoperatif araç kullanımı?" |

### FAQ Cevap Yazım Kuralları

| Kural | Açıklama |
|-------|----------|
| **Direkt başla** | "Evet/Hayır" ile başla, sonra açıkla |
| **100-200 kelime** | Çok kısa: yetersiz, çok uzun: okunmaz |
| **Güven ver** | Belirsizlik yerine net bilgi |
| **CTA ekle** | "Detaylı bilgi için randevu alın" |
| **Link verme** | FAQ içinde link Google tarafından önerilmez |

### İdeal FAQ Örneği

```yaml
- question: "TAVI sonrası ne kadar süre hastanede kalırım?"
  answer: "TAVI sonrası hastanede kalış süresi genellikle 3-5 gündür. İlk 24 saat 
  yoğun bakımda takip edilir, ardından servise alınır. Komplikasyon gelişmezse 
  3. veya 4. gün taburcu edilebilirsiniz. Eve gitmeden önce yürüyüş testi ve 
  kontrol ekokardiyografi yapılır."
```

### Sayfa Başına FAQ Sayısı

| Sayfa Tipi | Minimum | İdeal | Maximum |
|------------|---------|-------|---------|
| Blog | 5 | 8-10 | 15 |
| Hizmet | 5 | 6-8 | 12 |

### FAQ Konu Dağılımı

Her sayfada şu kategorilerden FAQ olmalı:

1. **Tanım soruları** - "[İşlem] nedir?", "[Hastalık] nedir?"
2. **Süreç soruları** - "Nasıl yapılır?", "Ne kadar sürer?"
3. **Risk soruları** - "Riskli mi?", "Ağrılı mı?"
4. **Sonuç soruları** - "Sonrası nasıl?", "Ne zaman iyileşirim?"
5. **Pratik sorular** - "Fiyatı ne kadar?", "SGK karşılıyor mu?"

---

## 4. Genel SEO Kuralları

### Heading Hiyerarşisi

```
H1 - Sayfa başlığı (sadece 1 tane)
  H2 - Ana bölümler
    H3 - Alt bölümler
      H4 - Detay bölümler (nadiren)
```

| Kural | Açıklama |
|-------|----------|
| H1 sadece 1 kez | Sayfa başlığı olarak |
| H2'yi atlamadan H3 kullanma | Hiyerarşi önemli |
| Anahtar kelime H2'lerde | SEO değeri yüksek |
| H2-H3'te soru formatı | FAQ rich snippet şansı |

### Paragraf ve Okunabilirlik

| Kural | Değer |
|-------|-------|
| Paragraf uzunluğu | 3-5 cümle |
| Cümle uzunluğu | 15-25 kelime |
| Liste kullan | Uzun açıklamalar yerine |
| Görsel ekle | Her 300-500 kelimede |
| Boşluk bırak | Sıkışık metin okumayı zorlaştırır |

### URL Yapısı

```
✅ /tr/hizmetler/tavi/
✅ /tr/blog/koroner-arter-hastaligi/
❌ /tr/hizmetler/tavi-transkateter-aort-kapak-implantasyonu-nedir/
❌ /tr/blog/post-123/
```

| Kural | Açıklama |
|-------|----------|
| Kısa tut | 3-5 kelime ideal |
| Küçük harf | URL case-sensitive |
| Tire kullan | Alt çizgi değil |
| Stop word'leri çıkar | "ve", "için", "ile" gereksiz |

### Görsel Optimizasyonu

```markdown
![Koroner anjiyografi işlemi](koroner-anjiyografi.jpg "Koroner anjiyografi sırasında kateter yerleştirme")
```

| Özellik | Optimizasyon |
|---------|--------------|
| Dosya adı | `koroner-anjiyografi.jpg` (anahtar kelime) |
| Alt text | Görseli açıklayan, anahtar kelimeli metin |
| Boyut | Max 200KB, WebP formatı tercih |
| Boyutlar | İçerik genişliğine uygun |

---

## 5. Anahtar Kelime Stratejisi

### Anahtar Kelime Türleri

| Tür | Örnek | Kullanım |
|-----|-------|----------|
| **Head** | "kardiyoloji" | Rekabet çok yüksek, zor sıralanır |
| **Body** | "koroner arter hastalığı" | Ana hedef, sayfa başlığında |
| **Long-tail** | "koroner stent sonrası dikkat edilmesi gerekenler" | FAQ ve içerik içinde |
| **LSI** | "ateroskleroz", "damar tıkanıklığı", "anjina" | Semantik zenginlik |

### Anahtar Kelime Yerleşimi

| Konum | Öncelik | Örnek |
|-------|---------|-------|
| Title (başlık) | ⭐⭐⭐⭐⭐ | "TAVI - Ameliyatsız Kapak Değişimi" |
| H1 | ⭐⭐⭐⭐⭐ | Başlıkla aynı veya varyasyon |
| Description | ⭐⭐⭐⭐ | İlk 60 karakterde |
| URL | ⭐⭐⭐⭐ | `/hizmetler/tavi/` |
| İlk paragraf | ⭐⭐⭐ | İlk 100 kelimede |
| H2 başlıkları | ⭐⭐⭐ | "TAVI Nasıl Yapılır?" |
| Alt text | ⭐⭐ | Görsel açıklamalarında |
| FAQ soruları | ⭐⭐⭐ | "TAVI ameliyat mı?" |

### Anahtar Kelime Yoğunluğu

| Metrik | Değer |
|--------|-------|
| Ana anahtar kelime | %1-2 (100 kelimede 1-2 kez) |
| Varyasyonlar | Eşanlamlıları kullan |
| Aşırı kullanım | Google ceza verir |

**Örnek varyasyonlar:**
- TAVI, transkateter aort kapak, ameliyatsız kapak değişimi, kateter ile kapak
- Koroner arter hastalığı, KAH, damar tıkanıklığı, kalp damar hastalığı

---

## 6. İç ve Dış Bağlantılar

### İç Bağlantı Stratejisi

```markdown
Aort darlığının tedavisinde [TAVI işlemi](/tr/hizmetler/tavi/) önemli bir seçenektir.
Koroner arter hastalığı hakkında detaylı bilgi için [bu yazımızı](/tr/blog/koroner-arter-hastaligi/) okuyabilirsiniz.
```

| Kural | Açıklama |
|-------|----------|
| Anchor text anlamlı olsun | "buraya tıklayın" ❌, "TAVI işlemi" ✅ |
| Doğal olsun | Zoraki link ekleme |
| İlgili sayfalara link ver | Konuyla alakalı olmalı |
| Sayfa başına 3-10 iç link | Çok fazla link spam sayılır |

### İç Link Matrisi

| Kaynak Sayfa | Hedef Sayfalar |
|--------------|----------------|
| Koroner Arter Hastalığı (Blog) | Koroner Anjiyografi, Stent, By-pass |
| TAVI (Hizmet) | Aort Darlığı, Kalp Kapak Hastalıkları |
| Atriyal Fibrilasyon (Blog) | Ablasyon, Pacemaker, Antikoagülan |
| Diyabetik Ayak (Hizmet) | Periferik Arter, Anjiyo |

### Dış Bağlantı Kuralları

| Kaynak | Güvenilirlik |
|--------|--------------|
| PubMed, NCBI | ⭐⭐⭐⭐⭐ |
| Türk Kardiyoloji Derneği | ⭐⭐⭐⭐⭐ |
| ESC, AHA, ACC | ⭐⭐⭐⭐⭐ |
| Sağlık Bakanlığı | ⭐⭐⭐⭐ |
| Wikipedia | ⭐⭐⭐ |
| Haber siteleri | ⭐⭐ |

```markdown
Bu veriler [European Society of Cardiology](https://www.escardio.org/) kılavuzlarına dayanmaktadır.
```

---

## 📊 SEO Kontrol Listesi

### Yayın Öncesi Kontrol

- [ ] Title 50-60 karakter
- [ ] Description 150-160 karakter
- [ ] H1 sadece 1 tane
- [ ] Heading hiyerarşisi doğru
- [ ] Anahtar kelime ilk 100 kelimede
- [ ] En az 5 FAQ ekli
- [ ] Görseller optimize (alt text, boyut)
- [ ] En az 3 iç link
- [ ] Dış kaynaklar güvenilir
- [ ] translationKey eşleşiyor
- [ ] lastmod güncel

### Periyodik Kontrol

- [ ] Eski içerikleri güncelle (6 ayda bir)
- [ ] Kırık linkleri kontrol et
- [ ] Google Search Console hatalarını düzelt
- [ ] Düşük performanslı sayfaları optimize et

---

## 🎯 Özet Tablo

| Sayfa Tipi | Schema | Min. Kelime | FAQ Sayısı | Tags |
|------------|--------|-------------|------------|------|
| Hizmet | MedicalProcedure | 1500 | 5-8 | - |
| Blog | MedicalScholarlyArticle | 2500 | 8-10 | 4-7 |
| Klinik | MedicalWebPage | 500 | 3-5 | - |

---

**Bu talimatlar, drhabibcil.com sitesinin Google aramalarında kardiyoloji alanında 1 numara olması hedefiyle hazırlanmıştır.**

