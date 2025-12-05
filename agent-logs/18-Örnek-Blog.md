## SAMPLE BLOG POST

Create comprehensive, medically accurate blog articles about "Heart Transplantation and Artificial Heart (LVAD) - End-Stage Heart Failure Treatments" in both Turkish and English languages, following the exact structure, style, and technical specifications of existing blog posts in the codebase.

**CRITICAL REQUIREMENTS:**

-   **Writing Style:** Content MUST be humanized and natural-sounding to avoid AI detection by search engines. Use varied sentence structures, conversational tone where appropriate, and authentic medical expertise voice.
-   **Medical Accuracy:** All medical information must be current, evidence-based, and suitable for patient education while maintaining professional standards.
-   **Consistency:** Analyze existing blog posts (especially "Kalp Ritim Bozuklukları" and "Aort Anevrizması") to match their exact formatting, structure, and style patterns.

---

## 1. FILE STRUCTURE & NAMING

Create exactly 4 files with these precise paths:

**Turkish Version:**

-   Article: `content/tr/blog/kalp-nakli-lvad/index.md`
-   Featured Image: `content/tr/blog/kalp-nakli-lvad/featured.svg`

**English Version:**

-   Article: `content/en/blog/heart-transplant-lvad/index.md`
-   Featured Image: `content/en/blog/heart-transplant-lvad/featured.svg`

---

## 2. ARTICLE SPECIFICATIONS

**Word Count:** 2000-2500 words per language (excluding frontmatter and schema markup)

**Content Structure (Required Sections in Order):**

1. **Frontmatter (YAML)** - See detailed specifications below
2. **Lead Paragraph** - 2-3 sentences with `.lead` CSS class, summarizing the article
3. **Table of Contents** - Auto-generated from headings
4. **Introduction Section** - Overview of end-stage heart failure and treatment options
5. **Main Content Sections** (use ## for main headings, ### for subsections):
    - What is Heart Transplantation? (Definition, history, current state)
    - When is Heart Transplant Needed? (Indications, end-stage heart failure criteria)
    - LVAD (Left Ventricular Assist Device) Explained (What it is, how it works, types: bridge-to-transplant, destination therapy, bridge-to-recovery)
    - Heart Transplant vs LVAD: Which Treatment? (Comparison, decision factors, patient selection)
    - Pre-Transplant Evaluation Process (Medical tests, psychological evaluation, waiting list)
    - LVAD Implantation Procedure (Surgical technique, hospital stay, recovery timeline)
    - Heart Transplant Surgery (Procedure details, duration, immediate post-op)
    - Post-Transplant/LVAD Care (Medications, immunosuppression, lifestyle modifications, monitoring)
    - Success Rates and Outcomes (Statistics, survival rates, quality of life data)
    - Risks and Complications (Rejection, infection, device malfunction, bleeding)
    - Life Expectancy and Quality of Life (Long-term outcomes, return to activities)
6. **Alert Boxes** - Use Hugo alert shortcodes for critical medical information (minimum 2-3 throughout article)
7. **FAQ Section** - Exactly 8-10 frequently asked questions with detailed answers
8. **Conclusion** - Summary and encouragement for patients
9. **Appointment Call-to-Action** - Button/link to contact Dr. ÇİL
10. **Schema.org JSON-LD Markup** - At end of file (see specifications below)

---

## 3. FRONTMATTER (YAML) SPECIFICATIONS

Use this exact structure (adapt values for Turkish/English):

```yaml
---
title: "[SEO-optimized title, 50-60 characters]"
description: "[Meta description, 150-160 characters, compelling and informative]"
date: 2024-12-05
lastmod: 2024-12-05
draft: false
translationKey: "heart-transplant-lvad"
categories:
    - "Kardiyoloji" # Turkish version
    # - "Cardiology"  # English version
tags:
    - "[8-12 relevant tags in appropriate language]"
    # Turkish examples: "Kalp Nakli", "LVAD", "Kalp Yetmezliği", "Yapay Kalp", "Son Dönem Kalp Yetmezliği", "Kalp Transplantasyonu"
    # English examples: "Heart Transplant", "LVAD", "Heart Failure", "Artificial Heart", "End-Stage Heart Failure", "Cardiac Transplantation"
author: "Doç. Dr. Habib ÇİL"
featured_image: "featured.svg"
---
```

**IMPORTANT:** The `translationKey` MUST be identical in both Turkish and English versions to link them properly.

---

## 4. FEATURED SVG IMAGE SPECIFICATIONS

**Mandatory Technical Requirements:**

-   **Dimensions:** `viewBox="0 0 800 400"` (exactly 800x400, NOT 1200x400)
-   **File Format:** SVG with embedded gradients and text
-   **Style Reference:** MUST match the exact visual style of `content/tr/blog/kalp-ritim-bozukluklari/featured.svg`

**Visual Design Elements:**

1. **Background Gradient:**

    - ID: `bgGrad` (use this exact ID)
    - Colors: Purple-pink gradient (#6366F1 → #8B5CF6 → #A78BFA)
    - Direction: Diagonal (x1="0%" y1="0%" x2="100%" y2="100%")

2. **Decorative Elements:**

    - 3 semi-transparent white circles at different positions (opacity: 0.1, 0.08)
    - Positioned similar to existing blog SVGs

3. **Main Illustration (Right Side, transform="translate(480, 50)"):**

    - **Heart illustration** with gradient fill (ID: `heartGrad`, colors: #EC4899 → #F472B6)
    - **LVAD device representation** (mechanical pump connected to heart, simplified schematic)
    - **Visual indicators:** Arrows showing blood flow, connection lines
    - **Animation effect:** Pulsing/fading circle or element (using `<animate>` tag, 1.5s duration, infinite repeat)

4. **Text Content (Left Side):**

    - **Main Title** (x="60" y="110", font-size="38", font-weight="bold", white color)
        - Turkish: "Kalp Nakli ve LVAD"
        - English: "Heart Transplant & LVAD"
    - **Subtitle** (x="60" y="160", font-size="24", rgba(255,255,255,0.9))
        - Turkish: "Son Dönem Kalp Yetmezliği Tedavileri"
        - English: "End-Stage Heart Failure Treatments"

5. **Info Boxes (2 boxes, transform="translate(60, 200)" and "translate(210, 200)"):**

    - Dimensions: 130x55, rx="10", fill="rgba(255,255,255,0.15)"
    - Box 1 Text (Turkish): "Kalp Nakli" / "Yaşam Kurtarır" | (English): "Heart Transplant" / "Life-Saving"
    - Box 2 Text (Turkish): "LVAD Desteği" / "Kalp Fonksiyonu" | (English): "LVAD Support" / "Heart Function"

6. **Bottom Text (x="60" y="340", font-size="16"):**
    - Turkish: "Doç. Dr. Habib ÇİL | Kardiyoloji Uzmanı"
    - English: "Assoc. Prof. Habib ÇİL | Cardiology Specialist"

**Gradient Naming Convention:**

-   Background: `id="bgGrad"`
-   Heart/Device: `id="heartGrad"` or `id="deviceGrad"`
-   DO NOT use unique suffixes like "TR" or "EN" - use standard names

---

## 5. SCHEMA.ORG MARKUP REQUIREMENTS

Include JSON-LD structured data at the end of each markdown file (after all content, before closing):

**Required Schemas:**

1. **Article Schema** - Standard blog article markup
2. **FAQPage Schema** - For the FAQ section (include all 8-10 Q&A pairs)
3. **MedicalWebPage Schema** (optional but recommended) - Medical content markup

**Example Structure:**

```html
<script type="application/ld+json">
	{
		"@context": "https://schema.org",
		"@graph": [
			{
				"@type": "Article",
				"headline": "[Article Title]",
				"description": "[Meta Description]",
				"author": {
					"@type": "Person",
					"name": "Doç. Dr. Habib ÇİL"
				},
				"datePublished": "2024-12-05",
				"dateModified": "2024-12-05"
			},
			{
				"@type": "FAQPage",
				"mainEntity": [
					{
						"@type": "Question",
						"name": "[Question text]",
						"acceptedAnswer": {
							"@type": "Answer",
							"text": "[Answer text]"
						}
					}
					// ... repeat for all FAQ items
				]
			}
		]
	}
</script>
```

---

## 6. CONTENT QUALITY GUIDELINES

**Medical Content:**

-   Use current medical terminology and evidence-based information
-   Explain complex concepts in patient-friendly language
-   Include specific statistics and success rates where appropriate
-   Balance hope with realistic expectations
-   Address common patient concerns and fears

**Humanization Techniques:**

-   Vary sentence length and structure
-   Use transitional phrases naturally
-   Include rhetorical questions where appropriate
-   Use active voice predominantly
-   Add empathetic language for patient concerns
-   Avoid repetitive phrasing patterns common in AI writing

**SEO Optimization:**

-   Natural keyword integration (avoid keyword stuffing)
-   Use semantic variations of main keywords
-   Include long-tail keyword phrases in headings
-   Optimize meta description for click-through rate

---

## 7. WORKFLOW INSTRUCTIONS

**Step 1:** Analyze existing blog posts to understand exact formatting patterns:

-   Review `content/tr/blog/kalp-ritim-bozukluklari/index.md`
-   Review `content/tr/blog/aort-anevrizmasi/index.md`
-   Review corresponding `featured.svg` files

**Step 2:** Create Turkish version first:

-   `content/tr/blog/kalp-nakli-lvad/index.md`
-   `content/tr/blog/kalp-nakli-lvad/featured.svg`

**Step 3:** Create English version:

-   `content/en/blog/heart-transplant-lvad/index.md`
-   `content/en/blog/heart-transplant-lvad/featured.svg`

**Step 4:** Verify all requirements:

-   [ ] Word count: 2000-2500 per language
-   [ ] All required sections included
-   [ ] SVG dimensions: 800x400
-   [ ] SVG style matches existing blogs
-   [ ] translationKey identical in both versions
-   [ ] Schema markup included
-   [ ] FAQ section has 8-10 questions
-   [ ] Alert boxes used appropriately
-   [ ] Natural, humanized writing style
-   [ ] Medical accuracy verified

---

## 8. FINAL DELIVERABLES CHECKLIST

-   [ ] `content/tr/blog/kalp-nakli-lvad/index.md` (2000-2500 words)
-   [ ] `content/tr/blog/kalp-nakli-lvad/featured.svg` (800x400, purple-pink gradient)
-   [ ] `content/en/blog/heart-transplant-lvad/index.md` (2000-2500 words)
-   [ ] `content/en/blog/heart-transplant-lvad/featured.svg` (800x400, purple-pink gradient)
-   [ ] All files follow existing blog post patterns exactly
-   [ ] Content is humanized and natural-sounding
-   [ ] Medical information is accurate and current
-   [ ] SEO optimization implemented
-   [ ] Schema markup included in both versions
