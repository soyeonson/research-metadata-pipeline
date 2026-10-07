# Architecture — v1.0

## Goal

Separate **source access**, **transient processing**, **derived-metadata persistence**, **validation**, and **system updates** in a research-output metadata workflow.

The core public-repository boundary is:

> Source documents may be processed, but source full text is not persisted by the public pipeline.

```text
       Metadata API
            |
            | bibliographic metadata only
            v
+---------------------------+
| Structured metadata       |
+-------------+-------------+
              |
              |
Document -----+
(Public sample: synthetic)  |
    |                        |
    v                        |
+---------------------------+
| Transient processing      |
| memory / temporary use    |
| NO full-text persistence  |
+-------------+-------------+
              |
              | derived fields + hash/provenance
              v
+---------------------------+
| Schema validation         |
+-------------+-------------+
              |
              v
+---------------------------+       +----------------------+
| Validation engine         | <---- | Master metadata      |
| normalize + compare       |       | Excel / DB export    |
+-------------+-------------+       +----------------------+
              |
              v
+---------------------------+
| Validation report         |
+-------------+-------------+
              |
              | approved changes
              v
+---------------------------+
| Automation adapter        |
| Playwright / mock system  |
+-------------+-------------+
              |
              v
READ -> DECIDE -> WRITE -> SAVE -> RE-READ -> VERIFY
```

## Persistence boundary

### Persistent

- identifiers and bibliographic metadata
- normalized authors / affiliations / project numbers
- validation status
- source hash
- source type
- section/page locator when available
- extractor version / timestamp

### Transient only

- source full text
- publisher HTML/XML body
- PDF-derived text
- long acknowledgement text
- abstract text when not explicitly needed and licensed for persistence
- prompt payload containing source text

## Design principles

1. **Content minimization.** Do not persist source text that does not need to be stored.
2. **Derived-data persistence.** Limit persistent storage to structured metadata and provenance required for validation.
3. **Metadata allow-list.** Do not dump entire external API responses; explicitly map only required fields.
4. **Schema before import.** Validate structured output against a JSON schema before comparison or persistence.
5. **Rules outside code where practical.** Keep frequently changing rules in YAML where appropriate.
6. **No blind write.** Read live values before writing and re-read them after saving to verify the result.
7. **Idempotent/reconcilable operations.** Do not write duplicate changes when the target state is already present.
8. **Human-review state is first-class.** Distinguish indeterminate cases from failures.

## Private implementation boundary

For institution-specific workflows, keep the following implementations in a private repository or local-only module:

- licensed publisher full-text access adapters
- institutional token / API credential handling
- production internal-system selectors
- internal authority tables
- source-content retention logic, if separately authorized

The public repository should contain only interfaces, synthetic fixtures, metadata-only adapters, and mock implementations.
