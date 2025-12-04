Kullanıcı FAQ Rich Snippets optimizasyonu için ne yapılması gerektiğini soruyor. Mevcut FAQ shortcode'unu daha detaylı analiz etmem ve Google'ın FAQ rich snippets gereksinimlerine göre nelerin eksik olduğunu belirlemem gerekiyor.

Şu anda PLAN MODE'dayım. Önce mevcut FAQ shortcode'unu daha detaylı inceleyeyim ve Google'ın FAQ rich snippets dokümantasyonuna göre gereksinimleri kontrol edeyim.

Mevcut FAQ shortcode'u:

1. `itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"`
2. `itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"`

Ancak Google'ın FAQ rich snippets için gerektirdiği tam yapıyı kontrol etmem lazım. Google'ın gereksinimleri:

-   FAQPage veya QAPage schema type
-   mainEntity property ile Question listesi
-   Her Question için acceptedAnswer

Ayrıca single.html dosyasında `{{ if .HasShortcode "faq" }}itemscope itemtype="https://schema.org/FAQPage" {{ end }}` kısmı var. Bu doğru ama tam FAQPage schema JSON-LD olarak da eklenmeli mi?

Şimdi daha detaylı analiz yapıp kullanıcıya öneriler sunacağım.

Mevcut FAQ shortcode'unu ve Google'ın FAQ rich snippets gereksinimlerini detaylı analiz edeyim:

Cline wants to read this file:

/layouts/shortcodes/faq.html‎

\*\*

Checkpoint

Compare

Restore

API Request$0.0034

Şimdi single.html'de FAQPage schema kontrolünü tekrar inceleyelim:

Cline wants to read this file:

/layouts/\_default/single.html‎

\*\*

Checkpoint

Compare

Restore

API Request$0.0053

## FAQ Rich Snippets Detaylı Analiz ve Öneriler

### Mevcut Durum:

1. **FAQ Shortcode'u:** Microdata formatında doğru implemente edilmiş

    - `itemscope itemtype="https://schema.org/Question"`
    - `itemprop="name"` soru metni için
    - `itemscope itemtype="https://schema.org/Answer"`
    - `itemprop="text"` cevap metni için

2. **Single.html'de Kontrol:** `{{ if .HasShortcode "faq" }}itemscope itemtype="https://schema.org/FAQPage" {{ end }}`

    - FAQ içeren sayfalarda otomatik olarak `FAQPage` itemscope ekleniyor

### Google FAQ Rich Snippets Gereksinimleri:

Google'ın resmi dokümantasyonuna göre FAQ rich snippets için iki seçenek var:

#### Seçenek 1: **Microdata (Mevcut Yaklaşım)**

```html
<div itemscope itemtype="https://schema.org/FAQPage">
	<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
		<h2 itemprop="name">Soru metni</h2>
		<div
			itemscope
			itemprop="acceptedAnswer"
			itemtype="https://schema.org/Answer"
		>
			<div itemprop="text">Cevap metni</div>
		</div>
	</div>
</div>
```

#### Seçenek 2: **JSON-LD (Önerilen)**

```json
{
	"@context": "https://schema.org",
	"@type": "FAQPage",
	"mainEntity": [
		{
			"@type": "Question",
			"name": "Soru metni",
			"acceptedAnswer": {
				"@type": "Answer",
				"text": "Cevap metni"
			}
		}
	]
}
```

### Eksiklikler ve Sorunlar:

1. **JSON-LD Eksikliği:** Google, JSON-LD formatını tercih ediyor ve daha iyi anlıyor
2. **FAQPage Wrapping:** Microdata'da `FAQPage` wrapping'i var ama JSON-LD yok
3. **Sayfa Başlığı Eksik:** FAQPage schema'da `name` property'si yok
4. **URL Eksik:** FAQPage schema'da `url` property'si yok

### Önerilen Çözümler:

#### 1. **JSON-LD FAQPage Schema Eklenmesi**

`layouts/partials/schema-faq.html` adında yeni bir partial oluşturulmalı:

```html
{{ if .HasShortcode "faq" }}
<script type="application/ld+json">
	{
	  "@context": "https://schema.org",
	  "@type": "FAQPage",
	  "@id": "{{ .Permalink }}#faqpage",
	  "name": "{{ .Title }} - Sık Sorulan Sorular",
	  "url": "{{ .Permalink }}",
	  "mainEntity": [
	    {{/* FAQ soruları buraya dinamik olarak eklenecek */}}
	  ]
	}
</script>
{{ end }}
```

#### 2. **Mevcut FAQ Shortcode'unun Geliştirilmesi**

FAQ shortcode'u, soruları bir slice'a toplayıp JSON-LD oluşturmak için kullanılabilir.

#### 3. **Alternatif: Statik JSON-LD Generation**

Her FAQ içeren sayfa için manuel JSON-LD oluşturulabilir.

### Acil Yapılması Gerekenler:

1. **JSON-LD FAQPage Schema Partial'ı oluştur**
2. **Mevcut microdata'yı koruyarak JSON-LD ekle**
3. **FAQ sayfalarında `name` ve `url` property'lerini ekle**
4. **Google Rich Results Test ile doğrulama**

### Teknik Detaylar:

```go
// Örnek implementasyon konsepti
{{ $faqQuestions := slice }}
{{ range .Page.Fragments }}
  {{ if eq .Type "faq" }}
    {{ $faqQuestions = $faqQuestions | append . }}
  {{ end }}
{{ end }}

{{ if gt (len $faqQuestions) 0 }}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{ range $index, $faq := $faqQuestions }}
    {
      "@type": "Question",
      "name": "{{ $faq.Question }}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{ $faq.Answer }}"
      }
    }{{ if not (eq $index (sub (len $faqQuestions) 1)) }},{{ end }}
    {{ end }}
  ]
}
</script>
{{ end }}
```

**Sonuç:** Mevcut implementasyon temel düzeyde çalışıyor ama Google'ın tercih ettiği JSON-LD formatı ve tam uyumluluk için geliştirme gerekiyor.
