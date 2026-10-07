# Scholarly Metadata Extraction Prompt — Public Sample

You are extracting **derived scholarly metadata** from source content supplied for this processing step.

## Data-minimization rule

The source content is transient input. Do not reproduce or return long passages from it.
Return only the structured facts defined by `schemas/article_metadata.schema.json`.

## Output rule

Return **JSON only**.
Do not infer a value that is not supported by the source. If a value cannot be established, use `null` or an empty array as permitted by the schema.

## Fields

For each paper, extract:

- `paper_id`
- `title`
- `journal`
- `open_access`: `Y`, `N`, or `null`
- `project_numbers`: project/grant numbers only
- `authors`
  - `name`
  - `role`: `first`, `corresponding`, `coauthor`, or `unknown`
  - `affiliations`
- `provenance` when supplied by the caller
  - `source_hash`
  - `source_type`
  - `source_locator`

## Guardrails

1. Preserve source-supported spelling for names and affiliations.
2. Do not freely translate institution names.
3. Do not guess OA status from publisher branding alone.
4. Do not invent project numbers from funder names.
5. If funding information is absent, leave `project_numbers` empty.
6. Represent uncertainty explicitly instead of forcing a value.
7. Do not return full abstract text.
8. Do not return full acknowledgement/funding paragraphs.
9. Do not return full-text excerpts as evidence.
10. When evidence traceability is needed, use a section/page locator instead of copying the passage.

## Input template

```text
PAPER_ID: {{paper_id}}
SOURCE_TYPE: {{source_type}}
SOURCE_HASH: {{source_hash}}
SOURCE_CONTENT:
{{source_content}}
```
