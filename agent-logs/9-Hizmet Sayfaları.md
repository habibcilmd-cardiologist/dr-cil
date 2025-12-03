Service Pages Implementation Plan

## Goal

Create individual, high-performance, SEO-optimized pages for each medical service offered by Dr. Çil. These pages will utilize MedicalProcedure schema to enhance search visibility and provide detailed information to patients.

## User Review Required

-   **Priority List**: Review the list of services to prioritize (e.g., TAVI, Angiography, Stent first).
-   **Content**: The actual medical content (text) for each service will need to be generated or provided. I will create the structure and schema.

## Proposed Changes

### Schema Implementation

**[NEW]** `layouts/partials/schema-procedure.html`

-   Create a new partial to generate MedicalProcedure JSON-LD.
-   Fields: name, description, procedureType (Surgical/Non-surgical), bodyLocation, followup, howPerformed, riskFactor.

**[MODIFY]** `layouts/partials/extend-head-uncached.html`

-   Include schema-procedure.html when the content type is service or procedure.

### Content Structure

**[NEW]** `content/tr/hizmetler/[slug]/index.md` & `content/en/services/[slug]/index.md`

**Front Matter:**

```yaml
title: Service Name
description: SEO Meta description
service_type: "MedicalProcedure" or "TherapeuticProcedure"
medical_specialty: "Cardiology"
procedure_type: "Non-surgical" (Interventional) or "Surgical"
body_location: "Heart"
```

**Body Content:**

-   Overview
-   Why it is done
-   Procedure details (Before, During, After)
-   Risks
-   FAQ (using `{{< faq >}}` shortcode)

## Verification Plan

### Automated Tests

-   **Rich Results Test**: Verify MedicalProcedure and FAQPage schema validation.
-   **Hugo Build**: Ensure no 404s and correct internal linking.

### Manual Verification

-   Check URL structure: `/tr/hizmetler/koroner-anjiyografi/`
-   Verify language switching works between TR and EN service pages.
