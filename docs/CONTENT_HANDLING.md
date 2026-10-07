# Content Handling & Licensing Design

This document explains how scholarly content is handled in the public sample repository.

## 1. Core rule

**Do not persist source full text by default.**

Metadata may be extracted from a document, but the public sample does not persist source text in databases, JSON outputs, or logs.

## 2. Processing lifecycle

```text
Input document
    |
    v
Read into memory
    |
    v
Extract required facts
    |
    +--> derived metadata
    +--> SHA-256 source hash
    +--> source locator
    |
    v
Discard source text from pipeline state
```

Whether the original source file itself is retained is outside the scope of this code. In production environments, access rights and retention rights must be reviewed separately.

## 3. Why keep a source hash?

Even without storing the source content, a hash can support:

- detecting whether the same input file has been processed again
- linking extraction results to a specific extractor version
- tracing which input version produced a particular result

A hash is not a mechanism for reconstructing the source content.

## 4. Evidence policy

The public sample does not persist long evidence passages in the output.

Recommended example:

```json
{
  "project_number": "DEMO-2026-001",
  "source_locator": {
    "section": "Acknowledgements",
    "page": null
  }
}
```

Example to avoid:

```json
{
  "evidence_text": "<long acknowledgement paragraph copied from the article>"
}
```

## 5. Metadata API policy

Instead of storing entire API responses, use **allow-list mapping**.

Examples:

- DOI
- title
- container/journal title
- author names
- publication date

Even if a response includes an abstract, full text, or license-specific content, do not persist it unless there is a clear operational need and the applicable terms permit it.

## 6. Public samples

The document fixture in this repository is the manually created `samples/synthetic_article.txt`.

Do not commit publisher PDFs, HTML, XML, full abstracts, or full acknowledgements as fixtures.

## 7. Operational note

In production environments, review the following separately:

- institutional subscription agreements
- publisher API / TDM terms
- OA licenses
- permitted scope of source-content retention and redistribution
- organizational information-security and data-retention policies

This document is not legal advice. The goal of the public repository design is not to make legal-rights determinations, but to **structurally minimize unnecessary content persistence**.

## 8. Guard scope

The block list in `storage/result_store.py` is a **defensive helper** for the public sample. It does not replace legal-rights review, DLP controls, or confidential-information detection.

- Prohibited source content may not be detected automatically if it appears under a different field name.
- Human review of JSON/output should remain part of the pre-save process.
- The permitted scope in production environments must be determined separately based on contracts, licenses, and institutional policies.
