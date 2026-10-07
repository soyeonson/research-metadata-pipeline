@echo off
setlocal
call .venv\Scripts\activate.bat

python -m processing.transient_processor --input samples\synthetic_article.txt --paper-id PAPER_SYNTHETIC --output output\derived_metadata_from_synthetic.json
if errorlevel 1 exit /b 1

python -m validation.schema_validate --input output\derived_metadata_from_synthetic.json --schema schemas\article_metadata.schema.json
if errorlevel 1 exit /b 1

python -m validation.schema_validate --input samples\extracted_metadata_sample.json --schema schemas\article_metadata.schema.json
if errorlevel 1 exit /b 1

python -m validation.compare_metadata --master samples\master_metadata_sample.xlsx --extracted samples\extracted_metadata_sample.json --rules rules\validation_rules.yaml --output output\validation_report.xlsx
if errorlevel 1 exit /b 1

python -m unittest discover -s tests -v
if errorlevel 1 exit /b 1

echo.
echo Derived metadata: output\derived_metadata_from_synthetic.json
echo Validation report: output\validation_report.xlsx
endlocal
