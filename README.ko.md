# Research Metadata Validation & Automation Pipeline

> **v1.0 — license-aware public sample**  
> A reproducible workflow for extracting, validating, and safely updating scholarly metadata **without persisting source full text**.

이 저장소는 연구성과 메타데이터 업무를 **추출(Extraction) → 일시적 문서 처리(Transient Processing) → 검증(Validation) → 시스템 반영(Automation)**으로 분리해 설명하는 공개용 샘플 프로젝트입니다.

실제 기관 시스템, 계정, 연구자 정보, 내부 URL, 실데이터, API Key, 브라우저 프로필, 출판사 원문/PDF는 포함하지 않습니다.

**Source full text is not persisted by this public sample.**

실제 운영 환경에서 원문 보관이 필요한 경우에는 해당 기관의 구독계약, TDM 조건, API 약관, OA 라이선스 및 내부 정책을 별도로 확인해야 합니다. 이 공개 저장소는 그러한 권한을 가정하지 않습니다.

## 1. Design boundary

### Persistent storage: allowed in this sample
- DOI 및 서지 메타데이터
- 구조화된 저자/기관/과제번호
- OA 판정값
- 추출기 버전
- source hash
- source type / locator 같은 provenance
- 비교 결과와 검증 상태

### Not persisted by this sample
- 논문 full text
- PDF 원문
- abstract 전문
- acknowledgement 전문
- publisher HTML/XML 원문
- LLM에 전달된 긴 source text

즉, 이 프로젝트의 저장 대상은 **source content가 아니라 derived metadata**입니다.

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
- 공개 메타데이터 API adapter 예제
- `CrossrefClient`는 bibliographic metadata만 allow-list 방식으로 매핑
- API 응답에 abstract가 포함되어도 공개 예제의 정규화 결과에는 저장하지 않음
- 출판사별 private/full-text adapter는 이 공개 저장소의 범위 밖

### Transient processing
- `samples/synthetic_article.txt`만 문서 처리 예제로 사용
- source text는 함수 내부에서 일시적으로 읽고 결과 JSON에는 포함하지 않음
- SHA-256 hash와 source locator만 provenance로 유지
- 실제 PDF 처리 코드는 의도적으로 포함하지 않음

### Validation — project core
- Excel 마스터 메타데이터 읽기
- 구조화 JSON schema 검증
- 과제번호, OA, 기관명 등 정규화
- 필드별 판정 규칙 적용
- 검증 결과 Excel 생성

### Automation
- 실제 기관 시스템이 아닌 mock HTML을 대상으로 한 Playwright 예제
- 내부 URL 및 selector를 공개하지 않고 `site_adapter` 패턴만 제공
- 저장 버튼 클릭 여부가 아니라 **저장 후 재조회 검증**을 기본 원칙으로 함

## 4. 빠른 시작 (Windows PowerShell)

모든 명령어는 `requirements.txt`가 있는 저장소 루트 폴더에서 실행합니다.

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

또는 Python 환경 설정을 위해 `setup_windows.bat`를 실행할 수 있습니다.

### 브라우저 설정

Playwright mock 자동화 예제를 실행하려면 Chromium 계열 브라우저가 필요합니다.

기본적으로 Playwright가 관리하는 Chromium 브라우저를 설치합니다.

```powershell
python -m playwright install chromium
```

기관 네트워크 또는 보안 정책으로 인해 Playwright 브라우저 다운로드가 제한되는 경우, PC에 이미 설치된 Chrome 또는 Microsoft Edge를 대신 사용할 수 있습니다.

Chrome 사용:

```powershell
$env:PLAYWRIGHT_BROWSER_CHANNEL="chrome"
```

Microsoft Edge 사용:

```powershell
$env:PLAYWRIGHT_BROWSER_CHANNEL="msedge"
```

환경변수는 현재 PowerShell 세션에 적용됩니다.

`PLAYWRIGHT_BROWSER_CHANNEL`이 설정되지 않은 경우에는 Playwright가 관리하는 Chromium을 사용합니다.

### A. Synthetic document 일시 처리

```powershell
python -m processing.transient_processor `
  --input samples/synthetic_article.txt `
  --paper-id PAPER_SYNTHETIC `
  --output output/derived_metadata_from_synthetic.json
```

생성되는 JSON에는 source text가 포함되지 않습니다.

예상 출력:

```text
Wrote derived metadata only: output\derived_metadata_from_synthetic.json
```

JSON에는 파생 메타데이터와 provenance만 포함되며, source full text는 저장되지 않습니다.

### B. 샘플 구조화 데이터 검증

```powershell
python -m validation.schema_validate `
  --input samples/extracted_metadata_sample.json `
  --schema schemas/article_metadata.schema.json
```

### C. 마스터 파일과 비교

```powershell
python -m validation.compare_metadata `
  --master samples/master_metadata_sample.xlsx `
  --extracted samples/extracted_metadata_sample.json `
  --rules rules/validation_rules.yaml `
  --output output/validation_report.xlsx
```

### D. 테스트 실행

```powershell
python -m unittest discover -s tests -v
```

### E. Playwright mock 입력 예제 실행

Playwright가 관리하는 Chromium을 설치한 경우:

```powershell
python -m automation.demo_run
```

PC에 설치된 Chrome을 사용하는 경우:

```powershell
$env:PLAYWRIGHT_BROWSER_CHANNEL="chrome"
python -m automation.demo_run
```

Microsoft Edge를 사용하는 경우:

```powershell
$env:PLAYWRIGHT_BROWSER_CHANNEL="msedge"
python -m automation.demo_run
```

이 demo는 로컬 mock HTML만을 대상으로 실행되며, 실제 기관 운영 시스템에는 연결하지 않습니다.


## 5. Sample cases

모든 샘플은 가상 데이터입니다.

- `PAPER001`: 대부분 일치
- `PAPER002`: OA 값이 마스터에서 누락
- `PAPER003`: 과제번호 불일치
- `PAPER004`: OA/소속기관 검토 사례
- `PAPER_SYNTHETIC`: 공개용으로 직접 작성한 synthetic article text 처리 예제

검증 상태 예시는 `MATCH`, `MISMATCH`, `MISSING_IN_MASTER`, `REVIEW`, `UNDETERMINED`입니다.

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
문자열 정규화, 집합 비교, 허용값 검증처럼 코드로 명확하게 표현할 수 있는 항목은 결정적 규칙으로 처리합니다.

### LLM output is an intermediate artifact
LLM 결과를 바로 시스템에 쓰지 않습니다. JSON schema 검증과 규칙 기반 비교를 거칩니다.

### Minimize source-content persistence
원문에서 필요한 사실을 추출하되, 공개 예제에서는 원문/긴 인용문을 저장하지 않습니다.

### Human review remains explicit
판정 근거가 부족하거나 정책 판단이 필요한 경우 `REVIEW` 또는 `UNDETERMINED`로 남깁니다.

### Verify after write

```text
READ -> DECIDE -> WRITE -> SAVE -> RE-READ -> VERIFY
```

브라우저 자동화는 `click()` 성공을 데이터 반영 성공으로 간주하지 않습니다.

## 8. Content and licensing note

이 저장소는 **저작권 또는 계약상 이용권한을 제공하지 않습니다.** 실제 문서에 대한 접근·처리·보관 가능 범위는 이용자가 보유한 라이선스와 기관 정책에 따라 달라질 수 있습니다.

따라서 공개 예제에서는:

1. 문서 처리 예제로 synthetic text만 사용하고,
2. full text persistence 기능을 제공하지 않으며,
3. metadata API 응답도 필요한 필드만 allow-list 방식으로 저장합니다.

자세한 원칙은 `docs/CONTENT_HANDLING.md`를 참고하세요.

## 9. Public-release safety

다음 자료는 공개 저장소에 넣지 않는 것을 전제로 합니다.

- 실제 연구자 개인정보 및 내부 관리번호
- 내부 시스템 URL, DOM dump, 실제 selector
- SSO 세션, 쿠키, Chrome profile
- 출판사 원문 PDF/HTML/XML/text
- abstract/acknowledgement 전문
- 원문 text cache 또는 full-text DB
- 운영 DB, 실행 로그, write journal, resume state
- API Key, institution token, password
- 비공개 평가기준 및 내부 전거 원본

## 10. 라이선스

이 프로젝트는 [MIT License](LICENSE)에 따라 배포됩니다.

MIT License는 이 저장소의 소스코드에 적용됩니다. 제3자의 학술 콘텐츠, 출판사 자료 또는 외부 데이터 소스에 대한 이용 권한까지 부여하는 것은 아닙니다. 사용자는 자신이 처리하는 외부 콘텐츠에 적용되는 라이선스, 이용약관, 구독계약 및 기관 정책을 직접 확인하고 준수할 책임이 있습니다.
