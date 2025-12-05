# Arabic Content Translation Guide for Dr. Habib ÇİL Website

**Date**: 2025-12-06  
**Purpose**: Guidelines for translating blog posts and content to Arabic

---

## Blog Post Translation Process

### Step 1: Identify Source Content

Find the Turkish or English blog post you want to translate:
- Turkish: `content/tr/blog/post-name/index.md`
- English: `content/en/blog/post-name/index.md`

### Step 2: Create Arabic Version

Create corresponding Arabic file:
```
content/ar/blog/post-name/index.md
```

### Step 3: Copy and Translate Frontmatter

#### Required Frontmatter Fields

```yaml
---
title: "Arabic Title Here"
description: "Arabic description for SEO (150-160 characters)"
date: 2024-01-01  # Keep same date as original
lastmod: 2024-01-01  # Keep same date as original
draft: false
tags: ["tag1", "tag2"]  # Translate tags to Arabic
categories: ["category"]  # Translate categories to Arabic
translationKey: "unique-key"  # MUST match tr/en versions
author: "Doç. Dr. Habib ÇİL"
featured: true  # Optional
showAuthor: true
showDate: true
showReadingTime: true
showTableOfContents: true
---
```

#### FAQ Structure (Frontmatter-based)

**IMPORTANT**: Use frontmatter FAQ structure, NOT Hugo shortcodes!

```yaml
faq:
  - question: "ما هو ارتفاع ضغط الدم؟"
    answer: "ارتفاع ضغط الدم هو حالة طبية مزمنة..."
  - question: "ما هي أعراض ارتفاع ضغط الدم؟"
    answer: "في كثير من الحالات، لا توجد أعراض واضحة..."
```

**DO NOT USE** (Incorrect):
```markdown
{{< faq-list >}}
{{< faq "Question?" >}}
Answer here
{{< /faq >}}
{{< /faq-list >}}
```

### Step 4: Translate Content Body

#### Medical Content Guidelines

1. **Use Evidence-Based Language**
   - ✅ "تشير الدراسات إلى أن..." (Studies indicate that...)
   - ✅ "تشير الأبحاث إلى..." (Research shows...)
   - ✅ "تتضمن خيارات العلاج..." (Treatment options include...)
   - ❌ "نحن نقدم أفضل علاج" (We offer the best treatment)
   - ❌ "عيادتنا متخصصة في..." (Our clinic specializes in...)

2. **Maintain Educational Tone**
   - Focus on patient education
   - Avoid promotional language
   - Use objective medical terminology
   - Comply with Turkish healthcare advertising regulations

3. **Medical Terminology**
   - Use accurate Arabic medical terms
   - Maintain consistency across all content
   - Reference medical dictionaries for proper translations

#### Alert Boxes

Use Hugo shortcodes for medical information alerts:

```markdown
{{< alert "medical_info" >}}
**معلومات طبية مهمة**: هذه المعلومات للأغراض التعليمية فقط ولا تحل محل الاستشارة الطبية المهنية.
{{< /alert >}}
```

#### Appointment CTA Buttons

```markdown
{{< button href="https://wa.me/905339454639" target="_blank" >}}
احجز موعد عبر واتساب
{{< /button >}}
```

### Step 5: Add Featured Image

If the original post has a featured image:
1. Copy `featured.svg` or `featured.jpg` to Arabic post folder
2. Or reference the same image path in frontmatter

### Step 6: Verify translationKey

**CRITICAL**: Ensure `translationKey` matches across all language versions!

Example:
- Turkish: `translationKey: "hypertension-guide"`
- English: `translationKey: "hypertension-guide"`
- Arabic: `translationKey: "hypertension-guide"`

This enables Hugo's language switcher to link the pages correctly.

---

## Common Medical Terms - Arabic Translations

| English | Turkish | Arabic |
|---------|---------|--------|
| Cardiology | Kardiyoloji | أمراض القلب |
| Hypertension | Hipertansiyon | ارتفاع ضغط الدم |
| Heart Attack | Kalp Krizi | نوبة قلبية |
| Coronary Artery Disease | Koroner Arter Hastalığı | مرض الشريان التاجي |
| Echocardiography | Ekokardiyografi | تخطيط صدى القلب |
| Angioplasty | Anjiyoplasti | رأب الأوعية |
| Stent | Stent | دعامة |
| Arrhythmia | Aritmi | اضطراب نظم القلب |
| Heart Failure | Kalp Yetmezliği | قصور القلب |
| Cholesterol | Kolesterol | الكوليسترول |

---

## Example: Complete Arabic Blog Post

```markdown
---
title: "دليل شامل لارتفاع ضغط الدم"
description: "معلومات تفصيلية حول ارتفاع ضغط الدم، الأعراض، الأسباب، طرق العلاج والوقاية. دليل تعليمي من د. حبيب جيل."
date: 2024-03-15
lastmod: 2024-03-15
draft: false
tags: ["ارتفاع ضغط الدم", "صحة القلب", "الوقاية"]
categories: ["أمراض القلب"]
translationKey: "hypertension-guide"
author: "Doç. Dr. Habib ÇİL"
featured: true
showAuthor: true
showDate: true
showReadingTime: true
showTableOfContents: true
faq:
  - question: "ما هو ارتفاع ضغط الدم؟"
    answer: "ارتفاع ضغط الدم هو حالة طبية مزمنة يكون فيها ضغط الدم في الشرايين مرتفعاً بشكل مستمر."
  - question: "ما هي أعراض ارتفاع ضغط الدم؟"
    answer: "في كثير من الحالات، لا توجد أعراض واضحة، لذلك يُسمى القاتل الصامت."
---

{{< lead >}}
ارتفاع ضغط الدم هو أحد أكثر الأمراض المزمنة شيوعاً ويؤثر على ملايين الأشخاص حول العالم.
{{< /lead >}}

## ما هو ارتفاع ضغط الدم؟

تشير الدراسات إلى أن ارتفاع ضغط الدم يحدث عندما يكون ضغط الدم في الشرايين مرتفعاً بشكل مستمر...

{{< alert "medical_info" >}}
**معلومات طبية مهمة**: هذه المعلومات للأغراض التعليمية فقط ولا تحل محل الاستشارة الطبية المهنية.
{{< /alert >}}

## الأعراض

تشير الأبحاث إلى أن معظم الأشخاص المصابين بارتفاع ضغط الدم لا يعانون من أعراض واضحة...

## العلاج

تتضمن خيارات العلاج:
- تغييرات نمط الحياة
- الأدوية الخافضة للضغط
- المتابعة الطبية المنتظمة

{{< button href="https://wa.me/905339454639" target="_blank" >}}
احجز موعد للاستشارة
{{< /button >}}
```

---

## Quality Checklist

Before publishing Arabic content:

- [ ] `translationKey` matches tr/en versions
- [ ] FAQ uses frontmatter structure (not shortcodes)
- [ ] Medical terminology is accurate
- [ ] Language is educational, not promotional
- [ ] Alert boxes for medical disclaimers included
- [ ] Appointment CTA buttons use Arabic text
- [ ] Featured image included
- [ ] Meta description is 150-160 characters
- [ ] Tags and categories translated
- [ ] Content reviewed for RTL text flow
- [ ] Schema.org markup will auto-generate correctly

---

## Testing After Translation

1. **Build locally**: `hugo server -D`
2. **Check Arabic page**: `http://localhost:1313/ar/blog/post-name/`
3. **Verify language switcher**: Links to tr/en versions work
4. **Test RTL layout**: Text flows right-to-left correctly
5. **Validate Schema**: Use Google Rich Results Test
6. **Check hreflang**: Verify language alternatives in page source

---

## Support

For questions about Arabic translation or medical terminology, consult:
- Medical dictionaries for accurate term translations
- Existing Arabic medical literature
- Healthcare translation professionals for complex medical content

