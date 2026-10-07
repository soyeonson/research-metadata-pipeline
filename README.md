# Research Metadata Validation & Automation Pipeline

**English** | [한국어](README.ko.md)

> **v1.0 — license-aware public sample**  
> A reproducible workflow for extracting, validating, and safely updating scholarly metadata **without persisting source full text**.

This repository is a public sample project that demonstrates a research-output metadata workflow divided into four stages: **Extraction → Transient Processing → Validation → Automation**.

It does **not** include any production institutional systems, user accounts, researcher information, internal URLs, real operational data, API keys, browser profiles, or publisher full-text/PDF content.

**Source full text is not persisted by this public sample.**

If full-text storage is required in a production environment, users must separately review the applicable institutional subscription agreements, text-and-data-mining (TDM) terms, API terms of use, open-access licenses, and internal policies. This public repository does not assume that such rights have been granted.

## 1. Design boundary

### Persistent storage: allowed in this sample
- DOI and bibliographic metadata
- Structured author, affiliation, and project/funding identifiers
- Open-access status
- Extractor version
- Source hash
- Provenance such as source type and source locator
- Comparison results and validation status

### Not persisted by this sample
- Article full text
- Source PDF files
- Full abstracts
- Full acknowledgements
- Publisher HTML/XML source content
- Long source-text passages provided to an LLM

In short, this project persists **derived metadata, not source content**.

## 2. Pipeline

```text
Metadata API --------------------------+
                                       |
Synthetic / lawfully accessed document|
        |                              |
        v                              |
Transient document processor           |
(full text not persisted)              |
        |                              |
        v                              |
Structured JSON + provenance ----------+
        |
        v
Schema validation
        |
        v
Master metadata + validation rules
        |
        v
Normalization / comparison
        |
        v
Validation report
        |
        v
READ -> DECIDE -> WRITE -> SAVE -> RE-READ -> VERIFY
```

## 3. Repository scope

### Extraction
- Example adapter for public metadata APIs
- `CrossrefClient` maps only allow-listed bibliographic metadata fields
- Even if an API response contains an abstract, the public sample does not persist it in the normalized output
- Publisher-specific private/full-text adapters are outside the scope of this public repository

### Transient processing
- `samples/synthetic_article.txt` is the only document-processing example included
- Source text is read only temporarily inside the processing function and is not included in the output JSON
- Only a SHA-256 source hash and a source locator are retained as provenance
- Production PDF-processing code is intentionally excluded

### Validation — project core
- Read master metadata from Excel
- Validate structured JSON against a schema
- Normalize fields such as project identifiers, open-access status, and affiliations
- Apply field-level validation rules
- Generate an Excel validation report

### Automation
- Playwright example runs against mock HTML rather than a production institutional system
- Internal URLs and selectors are not disclosed; the repository provides only the `site_adapter` pattern
- A successful button click is **not** treated as proof of a successful update; the default pattern is to save, re-read, and verify the result

## 4. Quick Start (Windows PowerShell)

Run the following commands from the repository root directory, where `requirements.txt` is located.

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt

Alternatively, run `setup_windows.bat`.

## 4. Quick Start (Windows PowerShell)

Run the following commands from the repository root directory, where `requirements.txt` is located.

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Alternatively, run `setup_windows.bat` for the Python environment setup.

### Browser setup

The Playwright mock-automation demo requires a Chromium-based browser.

By default, install the Playwright-managed Chromium browser:

```powershell
python -m playwright install chromium
```

If browser downloads are restricted by your network or organization, you can instead use an existing Chrome or Microsoft Edge installation.

For Chrome:

```powershell
$env:PLAYWRIGHT_BROWSER_CHANNEL="chrome"
```

For Microsoft Edge:

```powershell
$env:PLAYWRIGHT_BROWSER_CHANNEL="msedge"
```

The environment variable applies to the current PowerShell session.

If `PLAYWRIGHT_BROWSER_CHANNEL` is not set, the demo uses the Playwright-managed Chromium browser.

### A. Process a synthetic document transiently

```powershell
python -m processing.transient_processor `
  --input samples/synthetic_article.txt `
  --paper-id PAPER_SYNTHETIC `
  --output output/derived_metadata_from_synthetic.json
```

The generated JSON does not contain the source text.

Expected:

```text
Wrote derived metadata only: output\derived_metadata_from_synthetic.json
```

The JSON contains derived metadata and provenance, but not the source full text.

### B. Validate sample structured data

```powershell
python -m validation.schema_validate `
  --input samples/extracted_metadata_sample.json `
  --schema schemas/article_metadata.schema.json
```

### C. Compare extracted metadata with the master file

```powershell
python -m validation.compare_metadata `
  --master samples/master_metadata_sample.xlsx `
  --extracted samples/extracted_metadata_sample.json `
  --rules rules/validation_rules.yaml `
  --output output/validation_report.xlsx
```

### D. Run tests

```powershell
python -m unittest discover -s tests -v
```

### E. Run the Playwright mock-update demo

If you installed the Playwright-managed Chromium browser:

```powershell
python -m automation.demo_run
```

If you are using an existing Chrome installation:

```powershell
$env:PLAYWRIGHT_BROWSER_CHANNEL="chrome"
python -m automation.demo_run
```

If you are using Microsoft Edge:

```powershell
$env:PLAYWRIGHT_BROWSER_CHANNEL="msedge"
python -m automation.demo_run
```

The demo runs against local mock HTML only. It does not connect to a production institutional system.


## 5. Sample cases

All sample records are synthetic.

- `PAPER001`: mostly matching metadata
- `PAPER002`: OA value missing from the master data
- `PAPER003`: project/funding identifier mismatch
- `PAPER004`: OA and affiliation review case
- `PAPER_SYNTHETIC`: synthetic article-text example created specifically for this public sample

Example validation statuses are `MATCH`, `MISMATCH`, `MISSING_IN_MASTER`, `REVIEW`, and `UNDETERMINED`.

## 6. Folder structure

```text
research-metadata-pipeline/
├─ README.md
├─ README.ko.md
├─ requirements.txt
├─ setup_windows.bat
├─ .gitignore
├─ .env.example
├─ docs/
│  ├─ ARCHITECTURE.md
│  ├─ CONTENT_HANDLING.md
│  └─ PLAYWRIGHT_DEMO.md
├─ extraction/
│  ├─ crossref_client.py
│  └─ metadata_api_client.py
├─ processing/
│  └─ transient_processor.py
├─ storage/
│  └─ result_store.py
├─ validation/
│  ├─ io_utils.py
│  ├─ normalize.py
│  ├─ schema_validate.py
│  └─ compare_metadata.py
├─ automation/
│  ├─ browser.py
│  ├─ site_adapter.py
│  ├─ runner.py
│  ├─ selectors.example.json
│  └─ demo_site/article_form.html
├─ prompts/
│  └─ metadata_extraction.md
├─ schemas/
│  └─ article_metadata.schema.json
├─ rules/
│  └─ validation_rules.yaml
├─ samples/
│  ├─ synthetic_article.txt
│  ├─ master_metadata_sample.xlsx
│  ├─ extracted_metadata_sample.json
│  └─ validation_report_sample.xlsx
└─ tests/
   ├─ test_normalize.py
   ├─ test_compare.py
   └─ test_transient_processor.py
```

## 7. Validation philosophy

### Deterministic first
Operations that can be expressed clearly in code—such as string normalization, set comparison, and allowed-value validation—are handled with deterministic rules first.

### LLM output is an intermediate artifact
LLM output is not written directly to the target system. It must first pass JSON-schema validation and rule-based comparison.

### Minimize source-content persistence
The workflow extracts the facts needed for validation while avoiding persistence of source full text or long quotations in the public sample.

### Human review remains explicit
When evidence is insufficient or a policy judgment is required, the result remains `REVIEW` or `UNDETERMINED` rather than being forced into an automatic decision.

### Verify after write

```text
READ -> DECIDE -> WRITE -> SAVE -> RE-READ -> VERIFY
```

The browser automation does not treat a successful `click()` as proof that the data was successfully updated.

## 8. Content and licensing note

This repository **does not grant copyright or contractual rights to access, process, store, or redistribute source content**. The permitted scope depends on the licenses, subscriptions, contractual terms, and institutional policies applicable to each user's environment.

For that reason, this public sample:

1. uses only synthetic text for document-processing examples,
2. does not provide a full-text persistence feature, and
3. persists only allow-listed fields from metadata API responses.

See `docs/CONTENT_HANDLING.md` for the detailed handling principles.

## 9. Public-release safety

The following materials are intentionally excluded from the public repository:

- Real researcher personal information and internal record identifiers
- Internal system URLs, DOM dumps, and production selectors
- SSO sessions, cookies, and browser profiles
- Publisher source PDFs, HTML, XML, or full text
- Full abstracts or acknowledgements
- Full-text caches or databases
- Production databases, execution logs, write journals, and resume-state files
- API keys, institutional tokens, and passwords
- Non-public evaluation criteria and internal authority/control files

## 10. License

This project is licensed under the [MIT License](LICENSE).

The MIT License applies to the source code in this repository. It does not grant rights to third-party scholarly content, publisher materials, or external data sources. Users are responsible for complying with the applicable licenses, terms of use, subscription agreements, and institutional policies for any external content they process.