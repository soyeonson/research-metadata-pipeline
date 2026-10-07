# Public Playwright Automation Demo

This folder does not automate a production institutional system. It targets only the local mock page at `automation/demo_site/article_form.html`.

## Run

After the environment is configured:

```powershell
python -m automation.demo_run
```

The key point of the example is not the selector itself, but the following state flow:

```text
READ
  ↓
DECIDE (compare current value with target value)
  ↓
WRITE (enter only values that need to change)
  ↓
SAVE
  ↓
RE-READ / SERVER-BACKED CHECK
  ↓
VERIFIED or UNKNOWN_AFTER_WRITE
```

## Applying the pattern to a real system

Keep the production adapter separate from the public `MockMetadataSite`, for example in a private repository or local-only module.

```text
automation/
  site_adapter.py        # public mock
private_adapters/
  organization_site.py  # do not publish
```

A real adapter may require login handling, URLs, selectors, popup handling, and save-alert handling, but those implementation details should not be included in the public repository.

## Safety principles

- Do not commit login cookies or browser profiles.
- Do not treat clicking the Save button as proof of success.
- Read the live value before writing.
- Re-read the actual value after saving and compare it with the expected value.
- Do not perform blind retries after verification failures.
- Minimize personal and confidential information in logs.
